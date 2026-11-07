#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://here.now"
CREDENTIALS_FILE="$HOME/.herenow/credentials"
API_KEY="${HERENOW_API_KEY:-}"
API_KEY_SOURCE="none"
if [[ -n "${HERENOW_API_KEY:-}" ]]; then
  API_KEY_SOURCE="env"
fi
ALLOW_NON_HERENOW_BASE_URL=0
SLUG=""
CLAIM_TOKEN=""
TITLE=""
DESCRIPTION=""
TTL=""
CLIENT=""
TARGET=""
HANDLE_PATH=""
JOBS="${HERENOW_UPLOAD_JOBS:-6}"
RETRIES="${HERENOW_UPLOAD_RETRIES:-5}"

usage() {
  cat <<'USAGE'
Usage: publish.sh <file-or-dir> [options]

Options:
  --api-key <key>         API key (or set $HERENOW_API_KEY)
  --slug <slug>           Update existing publish
  --claim-token <token>   Claim token for anonymous updates
  --title <text>          Viewer title
  --description <text>    Viewer description
  --ttl <seconds>         Expiry (authenticated only)
  --client <name>         Agent name for attribution (e.g. cursor, claude-code)
  --handle-path <path>    Attach to handle at this path (e.g. genuievolve → lev.here.now/genuievolve/)
  --base-url <url>        API base (default: https://here.now)
  --allow-nonherenow-base-url
                         Allow auth requests to non-default API base URL
  --jobs <n>              Uploads at a time (default 6, or $HERENOW_UPLOAD_JOBS)
  --retries <n>           Tries per file before it counts as failed (default 5, or $HERENOW_UPLOAD_RETRIES)
USAGE
  exit 1
}

die() { echo "error: $1" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BUNDLED_JQ="${SKILL_DIR}/bin/jq"

if [[ -x "$BUNDLED_JQ" ]]; then
  JQ_BIN="$BUNDLED_JQ"
elif command -v jq >/dev/null 2>&1; then
  JQ_BIN="$(command -v jq)"
else
  die "requires jq (run: curl -fsSL https://here.now/install.sh | bash)"
fi

for cmd in curl file; do
  command -v "$cmd" >/dev/null 2>&1 || die "requires $cmd"
done

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-key)      API_KEY="$2"; API_KEY_SOURCE="flag"; shift 2 ;;
    --slug)         SLUG="$2"; shift 2 ;;
    --claim-token)  CLAIM_TOKEN="$2"; shift 2 ;;
    --title)        TITLE="$2"; shift 2 ;;
    --description)  DESCRIPTION="$2"; shift 2 ;;
    --ttl)          TTL="$2"; shift 2 ;;
    --client)       CLIENT="$2"; shift 2 ;;
    --handle-path)  HANDLE_PATH="$2"; shift 2 ;;
    --base-url)     BASE_URL="$2"; shift 2 ;;
    --allow-nonherenow-base-url) ALLOW_NON_HERENOW_BASE_URL=1; shift ;;
    --jobs)         JOBS="$2"; shift 2 ;;
    --retries)      RETRIES="$2"; shift 2 ;;
    --help|-h)      usage ;;
    -*)             die "unknown option: $1" ;;
    *)              [[ -z "$TARGET" ]] && TARGET="$1" || die "unexpected argument: $1"; shift ;;
  esac
done

[[ -n "$TARGET" ]] || usage
[[ -e "$TARGET" ]] || die "path does not exist: $TARGET"

# Load API key from credentials file if not provided via flag or env
if [[ -z "$API_KEY" && -f "$CREDENTIALS_FILE" ]]; then
  API_KEY=$(cat "$CREDENTIALS_FILE" | tr -d '[:space:]')
  [[ -n "$API_KEY" ]] && API_KEY_SOURCE="credentials"
fi

BASE_URL="${BASE_URL%/}"
STATE_DIR=".herenow"
STATE_FILE="$STATE_DIR/state.json"

# Safety guard: avoid accidentally sending bearer auth to arbitrary endpoints.
if [[ -n "$API_KEY" && "$BASE_URL" != "https://here.now" && "$ALLOW_NON_HERENOW_BASE_URL" -ne 1 ]]; then
  die "refusing to send API key to non-default base URL; pass --allow-nonherenow-base-url to override"
fi

# Auto-load claim token from state file for anonymous updates
if [[ -n "$SLUG" && -z "$CLAIM_TOKEN" && -z "$API_KEY" && -f "$STATE_FILE" ]]; then
  CLAIM_TOKEN=$("$JQ_BIN" -r --arg s "$SLUG" '.publishes[$s].claimToken // empty' "$STATE_FILE" 2>/dev/null || true)
fi

compute_sha256() {
  local f="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$f" | cut -d' ' -f1
  else
    shasum -a 256 "$f" | cut -d' ' -f1
  fi
}

guess_content_type() {
  local f="$1"
  case "${f##*.}" in
    html|htm) echo "text/html; charset=utf-8" ;;
    css)      echo "text/css; charset=utf-8" ;;
    js|mjs)   echo "text/javascript; charset=utf-8" ;;
    json)     echo "application/json; charset=utf-8" ;;
    md|txt)   echo "text/plain; charset=utf-8" ;;
    svg)      echo "image/svg+xml" ;;
    png)      echo "image/png" ;;
    jpg|jpeg) echo "image/jpeg" ;;
    gif)      echo "image/gif" ;;
    webp)     echo "image/webp" ;;
    pdf)      echo "application/pdf" ;;
    mp4)      echo "video/mp4" ;;
    mov)      echo "video/quicktime" ;;
    mp3)      echo "audio/mpeg" ;;
    wav)      echo "audio/wav" ;;
    xml)      echo "application/xml" ;;
    woff2)    echo "font/woff2" ;;
    woff)     echo "font/woff" ;;
    ttf)      echo "font/ttf" ;;
    ico)      echo "image/x-icon" ;;
    *)
      local detected
      detected=$(file --brief --mime-type "$f" 2>/dev/null || echo "application/octet-stream")
      echo "$detected"
      ;;
  esac
}

# Build file manifest as JSON array
FILES_JSON="[]"

if [[ -f "$TARGET" ]]; then
  sz=$(wc -c < "$TARGET" | tr -d ' ')
  ct=$(guess_content_type "$TARGET")
  bn=$(basename "$TARGET")
  h=$(compute_sha256 "$TARGET")
  FILES_JSON=$("$JQ_BIN" -n --arg p "$bn" --argjson s "$sz" --arg c "$ct" --arg h "$h" \
    '[{"path":$p,"size":$s,"contentType":$c,"hash":$h}]')
  FILE_MAP=$("$JQ_BIN" -n --arg p "$bn" --arg a "$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")" \
    '{($p):$a}')
elif [[ -d "$TARGET" ]]; then
  # One JSON line per file, then one jq pass. The old loop re-parsed the whole list once per file, which slowed
  # a 2,000-file folder down quadratically.
  TARGET="${TARGET%/}"
  TARGET_ABS="$(cd "$TARGET" && pwd)"
  MANIFEST_NDJSON="$(mktemp)"
  while IFS= read -r -d '' f; do
    rel="${f#$TARGET/}"
    [[ "$(basename "$rel")" == ".DS_Store" ]] && continue
    sz=$(wc -c < "$f" | tr -d ' ')
    ct=$(guess_content_type "$f")
    h=$(compute_sha256 "$f")
    "$JQ_BIN" -cn --arg p "$rel" --argjson s "$sz" --arg c "$ct" --arg h "$h" --arg a "$TARGET_ABS/$rel" \
      '{path:$p,size:$s,contentType:$c,hash:$h,abs:$a}' >> "$MANIFEST_NDJSON"
  done < <(find "$TARGET" -type f -print0 | sort -z)
  FILES_JSON=$("$JQ_BIN" -s '[.[] | del(.abs)]' "$MANIFEST_NDJSON")
  FILE_MAP=$("$JQ_BIN" -s 'map({(.path): .abs}) | add // {}' "$MANIFEST_NDJSON")
  rm -f "$MANIFEST_NDJSON"
else
  die "not a file or directory: $TARGET"
fi

file_count=$(echo "$FILES_JSON" | "$JQ_BIN" 'length')
[[ "$file_count" -gt 0 ]] || die "no files found"

# Build request body
BODY=$(echo "$FILES_JSON" | "$JQ_BIN" '{files: .}')

if [[ -n "$TTL" ]]; then
  BODY=$(echo "$BODY" | "$JQ_BIN" --argjson t "$TTL" '.ttlSeconds = $t')
fi

if [[ -n "$TITLE" || -n "$DESCRIPTION" ]]; then
  viewer="{}"
  [[ -n "$TITLE" ]] && viewer=$(echo "$viewer" | "$JQ_BIN" --arg t "$TITLE" '.title = $t')
  [[ -n "$DESCRIPTION" ]] && viewer=$(echo "$viewer" | "$JQ_BIN" --arg d "$DESCRIPTION" '.description = $d')
  BODY=$(echo "$BODY" | "$JQ_BIN" --argjson v "$viewer" '.viewer = $v')
fi

if [[ -n "$CLAIM_TOKEN" && -n "$SLUG" && -z "$API_KEY" ]]; then
  BODY=$(echo "$BODY" | "$JQ_BIN" --arg ct "$CLAIM_TOKEN" '.claimToken = $ct')
fi

# Determine endpoint and method
if [[ -n "$SLUG" ]]; then
  URL="$BASE_URL/api/v1/publish/$SLUG"
  METHOD="PUT"
else
  URL="$BASE_URL/api/v1/publish"
  METHOD="POST"
fi

# Build auth header
AUTH_ARGS=()
if [[ -n "$API_KEY" ]]; then
  AUTH_ARGS=(-H "authorization: Bearer $API_KEY")
fi

AUTH_MODE="anonymous"
if [[ -n "$API_KEY" ]]; then
  AUTH_MODE="authenticated"
fi

CLIENT_HEADER_VALUE="here-now-publish-sh"
if [[ -n "$CLIENT" ]]; then
  normalized_client=$(echo "$CLIENT" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9._-' '-')
  normalized_client="${normalized_client#-}"
  normalized_client="${normalized_client%-}"
  if [[ -n "$normalized_client" ]]; then
    CLIENT_HEADER_VALUE="${normalized_client}/publish-sh"
  fi
fi
CLIENT_ARGS=(-H "x-herenow-client: $CLIENT_HEADER_VALUE")

# Step 1: Create/update publish
echo "creating publish ($file_count files)..." >&2
RESPONSE=$(curl -sS -X "$METHOD" "$URL" \
  "${AUTH_ARGS[@]+"${AUTH_ARGS[@]}"}" \
  "${CLIENT_ARGS[@]+"${CLIENT_ARGS[@]}"}" \
  -H "content-type: application/json" \
  -d "$BODY")

# Check for errors
if echo "$RESPONSE" | "$JQ_BIN" -e '.error' >/dev/null 2>&1; then
  err=$(echo "$RESPONSE" | "$JQ_BIN" -r '.error')
  details=$(echo "$RESPONSE" | "$JQ_BIN" -r '.details // empty')
  die "$err${details:+ ($details)}"
fi

OUT_SLUG=$(echo "$RESPONSE" | "$JQ_BIN" -r '.slug')
VERSION_ID=$(echo "$RESPONSE" | "$JQ_BIN" -r '.upload.versionId')
FINALIZE_URL=$(echo "$RESPONSE" | "$JQ_BIN" -r '.upload.finalizeUrl')
SITE_URL=$(echo "$RESPONSE" | "$JQ_BIN" -r '.siteUrl')
UPLOAD_COUNT=$(echo "$RESPONSE" | "$JQ_BIN" '.upload.uploads | length')
SKIPPED_COUNT=$(echo "$RESPONSE" | "$JQ_BIN" '.upload.skipped // [] | length')

[[ "$OUT_SLUG" != "null" ]] || die "unexpected response: $RESPONSE"

# Step 2: Upload files (skipped files are unchanged from previous version)
if [[ "$SKIPPED_COUNT" -gt 0 ]]; then
  echo "uploading $UPLOAD_COUNT files ($SKIPPED_COUNT unchanged, skipped)..." >&2
else
  echo "uploading $UPLOAD_COUNT files..." >&2
fi
# One job line per file: path, url, content type, local file (tab-separated). One jq pass, not three per file.
UPLOAD_JOBS_FILE="$(mktemp)"
UPLOAD_RESULTS="$(mktemp)"
if [[ -f "$TARGET" && ! -d "$TARGET" ]]; then
  SINGLE_FILE="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"
  echo "$RESPONSE" | "$JQ_BIN" -r --arg f "$SINGLE_FILE" \
    '.upload.uploads[] | [.path, .url, (.headers["Content-Type"] // ""), $f] | @tsv' > "$UPLOAD_JOBS_FILE"
else
  echo "$RESPONSE" | "$JQ_BIN" -r --argjson map "$FILE_MAP" \
    '.upload.uploads[] | [.path, .url, (.headers["Content-Type"] // ""), ($map[.path] // "")] | @tsv' > "$UPLOAD_JOBS_FILE"
fi

# Uploads one job line, retrying with backoff. The time limit grows with the file: 60 s plus 1 s per 100 KB.
# Results go to a file, so failures are counted after the parallel run (the old counter lived in a subshell).
upload_one() {
  local line="$1" path url ct file size max code attempt=1
  IFS=$'\t' read -r path url ct file <<< "$line"
  if [[ -z "$file" || ! -f "$file" ]]; then
    printf 'fail\t%s\tmissing local file\n' "$path" >> "$UPLOAD_RESULTS"
    return 0
  fi
  size=$(wc -c < "$file" | tr -d ' ')
  max=$(( 60 + size / 102400 ))
  while :; do
    if [[ -n "$ct" ]]; then
      code=$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 20 --max-time "$max" -X PUT "$url" \
        -H "Content-Type: $ct" --data-binary "@$file" 2>/dev/null) || code="000"
    else
      code=$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 20 --max-time "$max" -X PUT "$url" \
        --data-binary "@$file" 2>/dev/null) || code="000"
    fi
    if [[ "$code" -ge 200 && "$code" -lt 300 ]]; then
      printf 'ok\t%s\n' "$path" >> "$UPLOAD_RESULTS"
      return 0
    fi
    # A 4xx other than 408 or 429 will not get better with another try.
    if [[ "$attempt" -ge "$UPLOAD_RETRIES" ]] || [[ "$code" -ge 400 && "$code" -lt 500 && "$code" -ne 408 && "$code" -ne 429 ]]; then
      printf 'fail\t%s\tHTTP %s after %s tries\n' "$path" "$code" "$attempt" >> "$UPLOAD_RESULTS"
      return 0
    fi
    sleep $(( attempt * attempt ))
    attempt=$(( attempt + 1 ))
  done
}
export -f upload_one
export UPLOAD_RESULTS
export UPLOAD_RETRIES="$RETRIES"

if [[ "$UPLOAD_COUNT" -gt 0 ]]; then
  echo "  ($JOBS at a time, up to $RETRIES tries per file)" >&2
  tr '\n' '\0' < "$UPLOAD_JOBS_FILE" | xargs -0 -n 1 -P "$JOBS" bash -c 'upload_one "$1"' _ &  # -n 1, not -I: BSD -I caps an argument at 255 bytes
  uploader=$!
  while kill -0 "$uploader" 2>/dev/null; do
    sleep 5
    echo "  uploaded $(wc -l < "$UPLOAD_RESULTS" | tr -d ' ') of $UPLOAD_COUNT" >&2
  done
  wait "$uploader" || true
fi

upload_errors=$(grep -c '^fail' "$UPLOAD_RESULTS" || true)
uploaded=$(grep -c '^ok' "$UPLOAD_RESULTS" || true)
if [[ "$upload_errors" -gt 0 || "$uploaded" -ne "$UPLOAD_COUNT" ]]; then
  grep '^fail' "$UPLOAD_RESULTS" | cut -f2- | sed 's/^/  failed: /' >&2 || true
  rm -f "$UPLOAD_JOBS_FILE" "$UPLOAD_RESULTS"
  die "$upload_errors file(s) failed and $uploaded of $UPLOAD_COUNT uploaded, so nothing was finalized. Run the same command again to retry"
fi
rm -f "$UPLOAD_JOBS_FILE" "$UPLOAD_RESULTS"

# Step 3: Finalize
echo "finalizing..." >&2
FIN_RESPONSE=$(curl -sS -X POST "$FINALIZE_URL" \
  "${AUTH_ARGS[@]+"${AUTH_ARGS[@]}"}" \
  "${CLIENT_ARGS[@]+"${CLIENT_ARGS[@]}"}" \
  -H "content-type: application/json" \
  -d "{\"versionId\":\"$VERSION_ID\"}")

if echo "$FIN_RESPONSE" | "$JQ_BIN" -e '.error' >/dev/null 2>&1; then
  err=$(echo "$FIN_RESPONSE" | "$JQ_BIN" -r '.error')
  die "finalize failed: $err"
fi

# Save state
mkdir -p "$STATE_DIR"
if [[ -f "$STATE_FILE" ]]; then
  STATE=$(cat "$STATE_FILE")
else
  STATE='{"publishes":{}}'
fi

entry=$("$JQ_BIN" -n --arg s "$SITE_URL" '{siteUrl: $s}')

RESPONSE_CLAIM_TOKEN=$(echo "$RESPONSE" | "$JQ_BIN" -r '.claimToken // empty')
RESPONSE_CLAIM_URL=$(echo "$RESPONSE" | "$JQ_BIN" -r '.claimUrl // empty')
RESPONSE_EXPIRES=$(echo "$RESPONSE" | "$JQ_BIN" -r '.expiresAt // empty')

[[ -n "$RESPONSE_CLAIM_TOKEN" ]] && entry=$(echo "$entry" | "$JQ_BIN" --arg v "$RESPONSE_CLAIM_TOKEN" '.claimToken = $v')
[[ -n "$RESPONSE_CLAIM_URL" ]] && entry=$(echo "$entry" | "$JQ_BIN" --arg v "$RESPONSE_CLAIM_URL" '.claimUrl = $v')
[[ -n "$RESPONSE_EXPIRES" ]] && entry=$(echo "$entry" | "$JQ_BIN" --arg v "$RESPONSE_EXPIRES" '.expiresAt = $v')

STATE=$(echo "$STATE" | "$JQ_BIN" --arg slug "$OUT_SLUG" --argjson e "$entry" '.publishes[$slug] = $e')
echo "$STATE" | "$JQ_BIN" '.' > "$STATE_FILE"

# Output
echo "$SITE_URL"

PERSISTENCE="permanent"
if [[ "$AUTH_MODE" == "anonymous" ]]; then
  PERSISTENCE="expires_24h"
elif [[ -n "$RESPONSE_EXPIRES" ]]; then
  PERSISTENCE="expires_at"
fi

SAFE_CLAIM_URL=""
if [[ -n "$RESPONSE_CLAIM_URL" && "$RESPONSE_CLAIM_URL" == https://* ]]; then
  SAFE_CLAIM_URL="$RESPONSE_CLAIM_URL"
fi

echo "" >&2
echo "publish_result.site_url=$SITE_URL" >&2
echo "publish_result.auth_mode=$AUTH_MODE" >&2
echo "publish_result.api_key_source=$API_KEY_SOURCE" >&2
echo "publish_result.persistence=$PERSISTENCE" >&2
echo "publish_result.expires_at=$RESPONSE_EXPIRES" >&2
echo "publish_result.claim_url=$SAFE_CLAIM_URL" >&2

if [[ "$AUTH_MODE" == "authenticated" ]]; then
  echo "authenticated publish (permanent, saved to your account)" >&2
else
  echo "anonymous publish (expires in 24h)" >&2
  if [[ -n "$SAFE_CLAIM_URL" ]]; then
    echo "claim URL: $SAFE_CLAIM_URL" >&2
  fi
  if [[ -n "$RESPONSE_CLAIM_TOKEN" ]]; then
    echo "claim token saved to $STATE_FILE" >&2
  fi
fi

# Step 4: Handle path linking (optional)
# When --handle-path is passed, attach the slug to lev.here.now/<path>/
# via the Links API. Idempotent — creates or updates as needed.
if [[ -n "$HANDLE_PATH" && -n "$API_KEY" ]]; then
  echo "" >&2
  LINK_SLUG="$OUT_SLUG"
  LINK_RESP=$(curl -sS "$BASE_URL/api/v1/links/$HANDLE_PATH" \
    -H "Authorization: Bearer $API_KEY" 2>/dev/null || echo "{}")
  CURRENT=$(echo "$LINK_RESP" | "$JQ_BIN" -r '.slug // empty' 2>/dev/null || echo "")

  if [[ "$CURRENT" == "$LINK_SLUG" ]]; then
    echo "handle link OK: $HANDLE_PATH/ → $LINK_SLUG" >&2
  elif [[ -n "$CURRENT" ]]; then
    curl -sS -X PATCH "$BASE_URL/api/v1/links/$HANDLE_PATH" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"slug\": \"$LINK_SLUG\"}" >/dev/null 2>&1
    echo "handle link updated: $HANDLE_PATH/ → $LINK_SLUG" >&2
  else
    curl -sS -X POST "$BASE_URL/api/v1/links" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"location\": \"$HANDLE_PATH\", \"slug\": \"$LINK_SLUG\"}" >/dev/null 2>&1
    echo "handle link created: $HANDLE_PATH/ → $LINK_SLUG" >&2
  fi

  HANDLE_HOST=$(echo "$LINK_RESP" | "$JQ_BIN" -r '.hostname // empty' 2>/dev/null || echo "")
  if [[ -n "$HANDLE_HOST" ]]; then
    echo "publish_result.handle_url=https://$HANDLE_HOST/$HANDLE_PATH/" >&2
  fi
elif [[ -n "$HANDLE_PATH" && -z "$API_KEY" ]]; then
  echo "WARN: --handle-path requires authenticated publish (API key)" >&2
fi
