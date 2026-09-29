#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"
load_env_file

EXA_BASE="${EXA_BASE:-https://api.exa.ai}"
EXA_CONNECT_TIMEOUT="${EXA_CONNECT_TIMEOUT:-10}"
EXA_MAX_TIME="${EXA_MAX_TIME:-60}"
EXA_STATUS_MAX_TIME="${EXA_STATUS_MAX_TIME:-${EXA_MAX_TIME}}"

require_positive_int() {
  local name="$1"
  local value="${2:-}"
  [[ "$value" =~ ^[1-9][0-9]*$ ]] || die "${name} must be a positive integer"
}

require_value() {
  local name="$1"
  local value="${2:-}"
  [[ -n "$value" ]] || die "${name} requires a value"
}

require_url() {
  local url="$1"
  [[ "$url" =~ ^https?://[^[:space:]]+$ ]] || die "Invalid URL: ${url}"
}

require_positive_int EXA_CONNECT_TIMEOUT "$EXA_CONNECT_TIMEOUT"
require_positive_int EXA_MAX_TIME "$EXA_MAX_TIME"
require_positive_int EXA_STATUS_MAX_TIME "$EXA_STATUS_MAX_TIME"

load_exa_key() {
  if [[ -n "${EXA_API_KEY:-}" ]]; then
    return 0
  fi
  local config_file="${EXA_CREDENTIALS_FILE:-${HOME}/.clawdbot/credentials/exa/config.json}"
  if [[ -f "$config_file" ]]; then
    command -v jq >/dev/null 2>&1 || die "jq is required to read ${config_file}"
    local key
    key="$(jq -r '.apiKey // empty' "$config_file")"
    if [[ -n "$key" ]]; then
      export EXA_API_KEY="$key"
    fi
  fi
}

require_exa_key() {
  load_exa_key
  require_env EXA_API_KEY
}

usage() {
  cat <<'EOF'
Usage: exa <command> [args] [options]

Commands:
  search <query>            Search the web with Exa
  contents <urls...>        Fetch full page contents
  answer <query>            Generate an answer with citations
  status                    Verify API key and API reachability
  help                      Show help

Environment:
  EXA_API_KEY               Explicit API key (wins over env files)
  EXA_ENV_FILE              Optional env file (default: $HOME/.env.local)
  EXA_CREDENTIALS_FILE      Optional JSON credential file
  EXA_CONNECT_TIMEOUT       Curl connect timeout in seconds (default: 10)
  EXA_MAX_TIME              Curl request timeout in seconds (default: 60)
  EXA_STATUS_MAX_TIME       Status timeout in seconds (default: EXA_MAX_TIME)
EOF
}

api_post() {
  local url="$1"
  local body="$2"
  require_exa_key
  curl -fsSL \
    --connect-timeout "$EXA_CONNECT_TIMEOUT" \
    --max-time "$EXA_MAX_TIME" \
    "$url" \
    -H "x-api-key: ${EXA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$body"
}

api_get() {
  local url="$1"
  require_exa_key
  curl -fsSL \
    --connect-timeout "$EXA_CONNECT_TIMEOUT" \
    --max-time "$EXA_MAX_TIME" \
    "$url" -H "x-api-key: ${EXA_API_KEY}"
}

api_delete() {
  local url="$1"
  require_exa_key
  curl -fsSL \
    --connect-timeout "$EXA_CONNECT_TIMEOUT" \
    --max-time "$EXA_MAX_TIME" \
    -X DELETE "$url" -H "x-api-key: ${EXA_API_KEY}"
}

status_cmd() {
  require_exa_key
  echo "exa"
  echo "  key: configured"

  local response http_code
  if ! response="$(curl -sS \
    --connect-timeout "$EXA_CONNECT_TIMEOUT" \
    --max-time "$EXA_STATUS_MAX_TIME" \
    -X POST "${EXA_BASE}/search" \
    -H "x-api-key: ${EXA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"query":"test","numResults":1}' \
    -w $'\n%{http_code}')"; then
    die "Exa status request failed"
  fi
  http_code="$(printf '%s' "$response" | tail -n 1)"
  case "$http_code" in
    200)
      echo "  api: ok"
      ;;
    401|403)
      echo "  api: invalid-key-${http_code}" >&2
      return 1
      ;;
    429)
      echo "  api: rate-limited" >&2
      return 1
      ;;
    *)
      echo "  api: unexpected-status-${http_code:-transport-error}" >&2
      return 1
      ;;
  esac
}

search_cmd() {
  local query="$1"
  shift
  local num=10
  local type="auto"
  local category=""
  local domains=""
  local exclude=""
  local since=""
  local until=""
  local location=""
  local include_text=1
  local include_summary=1
  local output=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--num)
        require_value "$1" "${2:-}"
        num="$2"; shift 2 ;;
      --type)
        require_value "$1" "${2:-}"
        type="$2"; shift 2 ;;
      --category)
        require_value "$1" "${2:-}"
        category="$2"; shift 2 ;;
      --domains)
        require_value "$1" "${2:-}"
        domains="$2"; shift 2 ;;
      --exclude)
        require_value "$1" "${2:-}"
        exclude="$2"; shift 2 ;;
      --since)
        require_value "$1" "${2:-}"
        since="$2"; shift 2 ;;
      --until)
        require_value "$1" "${2:-}"
        until="$2"; shift 2 ;;
      --location)
        require_value "$1" "${2:-}"
        location="$2"; shift 2 ;;
      --no-text)
        include_text=0; shift ;;
      --no-summary)
        include_summary=0; shift ;;
      -o|--output)
        require_value "$1" "${2:-}"
        output="$2"; shift 2 ;;
      *)
        die "Unknown exa search arg: $1" ;;
    esac
  done

  require_positive_int num "$num"
  local body
  body="$(jq -n \
    --arg query "$query" \
    --arg type "$type" \
    --argjson numResults "$num" \
    --arg location "$location" \
    --arg category "$category" \
    --arg domains "$domains" \
    --arg exclude "$exclude" \
    --arg since "$since" \
    --arg until "$until" \
    --argjson includeText "$include_text" \
    --argjson includeSummary "$include_summary" '
    {
      query: $query,
      type: $type,
      numResults: $numResults
    }
    + (if $location != "" then {userLocation: $location} else {} end)
    + (if ($includeText == 1) or ($includeSummary == 1) then {
        contents: (
          (if $includeText == 1 then {text: {maxCharacters: 2000}} else {} end)
          + (if $includeSummary == 1 then {summary: {}} else {} end)
        )
      } else {} end)
    + (if $category != "" then {category: $category} else {} end)
    + (if $domains != "" then {includeDomains: ($domains | split(","))} else {} end)
    + (if $exclude != "" then {excludeDomains: ($exclude | split(","))} else {} end)
    + (if $since != "" then {startPublishedDate: ($since + "T00:00:00.000Z")} else {} end)
    + (if $until != "" then {endPublishedDate: ($until + "T23:59:59.999Z")} else {} end)
  ')"

  local response
  response="$(api_post "${EXA_BASE}/search" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

contents_cmd() {
  local max_chars=2000
  local num_sentences=3
  local highlights_per_url=2
  local with_summary=1
  local output=""
  local urls=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --max-chars)
        require_value "$1" "${2:-}"
        max_chars="$2"; shift 2 ;;
      --num-sentences)
        require_value "$1" "${2:-}"
        num_sentences="$2"; shift 2 ;;
      --highlights-per-url)
        require_value "$1" "${2:-}"
        highlights_per_url="$2"; shift 2 ;;
      --no-summary)
        with_summary=0; shift ;;
      -o|--output)
        require_value "$1" "${2:-}"
        output="$2"; shift 2 ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  [[ ${#urls[@]} -gt 0 ]] || die "At least one URL is required"
  require_positive_int max-chars "$max_chars"
  require_positive_int num-sentences "$num_sentences"
  require_positive_int highlights-per-url "$highlights_per_url"
  local url
  for url in "${urls[@]}"; do require_url "$url"; done

  local url_json body response
  url_json="$(printf '%s\n' "${urls[@]}" | jq -R . | jq -s .)"
  body="$(jq -n \
    --argjson urls "$url_json" \
    --argjson maxChars "$max_chars" \
    --argjson numSentences "$num_sentences" \
    --argjson highlightsPerUrl "$highlights_per_url" \
    --argjson withSummary "$with_summary" '
    {
      urls: $urls,
      text: {maxCharacters: $maxChars},
      highlights: {numSentences: $numSentences, highlightsPerUrl: $highlightsPerUrl}
    }
    + (if $withSummary == 1 then {summary: {}} else {} end)
  ')"

  response="$(api_post "${EXA_BASE}/contents" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

answer_cmd() {
  local query="$1"
  shift
  local output=""
  local with_text=1

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --no-text)
        with_text=0; shift ;;
      -o|--output)
        require_value "$1" "${2:-}"
        output="$2"; shift 2 ;;
      *)
        die "Unknown exa answer arg: $1" ;;
    esac
  done

  local body response
  body="$(jq -n \
    --arg query "$query" \
    --argjson withText "$with_text" '
    {
      query: $query
    }
    + (if $withText == 1 then {text: true} else {} end)
  ')"
  response="$(api_post "${EXA_BASE}/answer" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  search)
    [[ $# -gt 0 ]] || die "Query required"
    query="$1"; shift
    search_cmd "$query" "$@"
    ;;
  contents)
    contents_cmd "$@"
    ;;
  answer)
    [[ $# -gt 0 ]] || die "Query required"
    query="$1"; shift
    answer_cmd "$query" "$@"
    ;;
  status)
    status_cmd
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    die "Unknown exa command: ${cmd}"
    ;;
esac
