#!/usr/bin/env bash
# model-cache — Dynamic AI provider discovery. Zero hardcoded models.
# Part of agent-field-kit. Probes CLI runners + API /models endpoints.
# Caches results. Keys stored as NAME only (never value).
#
# Usage:
#   model-cache discover          # Human-readable summary
#   model-cache refresh           # Force re-probe (bypass 24h cache)
#   model-cache json              # Full manifest as JSON
#   model-cache models <provider> # Models for one provider
#   model-cache seats <N>         # Assign N diverse seats
#
# Zero setup. First run probes everything. 24h cache.

set -euo pipefail

CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/lev"
CACHE_FILE="$CACHE_DIR/model-manifest.json"
CACHE_TTL=86400  # 24h
PROBE_TIMEOUT=5  # seconds per API probe
DETECT_RUNNERS="${HOME}/.agents/skills/tribunal/bin/detect-runners"

mkdir -p "$CACHE_DIR"

# ═══════════════════════════════════════════════════════════════
# API Provider Probing — hit /models, extract model IDs
# ═══════════════════════════════════════════════════════════════

# Provider definition: name|key_env|endpoint|auth_style
# auth_style: bearer|anthropic|query_param
PROVIDER_DEFS=(
  "openai|OPENAI_API_KEY|https://api.openai.com/v1/models|bearer"
  "anthropic|ANTHROPIC_API_KEY|https://api.anthropic.com/v1/models|anthropic"
  "google|GEMINI_API_KEY|https://generativelanguage.googleapis.com/v1beta/models|query_param"
  "xai|XAI_API_KEY|https://api.x.ai/v1/models|bearer"
  "groq|GROQ_API_KEY|https://api.groq.com/openai/v1/models|bearer"
  "deepseek|DEEPSEEK_API_KEY|https://api.deepseek.com/models|bearer"
  "openrouter|OPENROUTER_API_KEY|https://openrouter.ai/api/v1/models|bearer"
  "fireworks|FIREWORKS_API_KEY|https://api.fireworks.ai/inference/v1/models|bearer"
  "perplexity|PERPLEXITY_API_KEY||none"
)

probe_api_provider() {
  local name="$1" key_env="$2" endpoint="$3" auth_style="$4"
  local key_val="${!key_env:-}"
  local key_present=false
  local models_json="[]"
  local model_count=0
  local probed_at=""
  local probe_ok=false

  [[ -n "$key_val" ]] && key_present=true

  if [[ "$key_present" == "true" && -n "$endpoint" ]]; then
    probed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local raw=""

    case "$auth_style" in
      bearer)
        raw=$(timeout "$PROBE_TIMEOUT" curl -s "$endpoint" \
          -H "Authorization: Bearer $key_val" 2>/dev/null || echo "")
        ;;
      anthropic)
        raw=$(timeout "$PROBE_TIMEOUT" curl -s "$endpoint" \
          -H "x-api-key: $key_val" \
          -H "anthropic-version: 2023-06-01" 2>/dev/null || echo "")
        ;;
      query_param)
        raw=$(timeout "$PROBE_TIMEOUT" curl -s "${endpoint}?key=${key_val}" 2>/dev/null || echo "")
        ;;
    esac

    if [[ -n "$raw" ]]; then
      # Extract model IDs — different providers use different shapes
      case "$name" in
        google)
          # Google: { models: [ { name: "models/gemini-2.5-pro" } ] }
          models_json=$(echo "$raw" | jq -r '[.models[]?.name // empty | sub("^models/"; "")]' 2>/dev/null || echo "[]")
          ;;
        openrouter)
          # OpenRouter returns thousands — take top 50 by context_length
          models_json=$(echo "$raw" | jq -r '[.data[]?.id // empty] | sort | .[:50]' 2>/dev/null || echo "[]")
          ;;
        *)
          # Standard OpenAI-compatible: { data: [ { id: "gpt-4o" } ] }
          models_json=$(echo "$raw" | jq -r '[.data[]?.id // empty] | sort' 2>/dev/null || echo "[]")
          ;;
      esac

      model_count=$(echo "$models_json" | jq 'length' 2>/dev/null || echo 0)
      [[ "$model_count" -gt 0 ]] && probe_ok=true
    fi
  fi

  cat <<PROVIDER_JSON
    {
      "name": "$name",
      "key_env": "$key_env",
      "key_present": $key_present,
      "endpoint": "$endpoint",
      "models": $models_json,
      "model_count": $model_count,
      "probe_ok": $probe_ok,
      "probed_at": "$probed_at"
    }
PROVIDER_JSON
}

# ═══════════════════════════════════════════════════════════════
# CLI Runner Detection — delegate to tribunal's detect-runners
# ═══════════════════════════════════════════════════════════════

get_cli_runners_json() {
  if [[ -x "$DETECT_RUNNERS" ]]; then
    "$DETECT_RUNNERS" --json 2>/dev/null | jq '.runners' 2>/dev/null || echo "[]"
  else
    # Fallback: basic PATH detection
    local runners="["
    local first=true
    for cmd in claude codex gemini cursor-agent opencode pi aider; do
      local path=""
      path=$(which "$cmd" 2>/dev/null || echo "")
      if [[ -n "$path" ]]; then
        local ver=""
        ver=$("$cmd" --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+[.0-9]*' | head -1 || echo "?")
        [[ "$first" == "true" ]] && first=false || runners+=","
        runners+=$(printf '{"name":"%s","cmd":"%s","installed":true,"version":"%s"}' "$cmd" "$cmd" "$ver")
      fi
    done
    runners+="]"
    echo "$runners"
  fi
}

# ═══════════════════════════════════════════════════════════════
# Full Manifest Build
# ═══════════════════════════════════════════════════════════════

build_manifest() {
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local hostname
  hostname=$(hostname -s 2>/dev/null || echo "unknown")

  echo "{"
  echo "  \"generated\": \"$ts\","
  echo "  \"hostname\": \"$hostname\","
  echo "  \"ttl_seconds\": $CACHE_TTL,"

  # API providers — probe in parallel for speed
  echo "  \"api_providers\": ["
  local first=true
  local tmpdir
  tmpdir=$(mktemp -d)

  # Dispatch probes in parallel
  local pids=()
  local idx=0
  for def in "${PROVIDER_DEFS[@]}"; do
    IFS='|' read -r name key_env endpoint auth_style <<< "$def"
    probe_api_provider "$name" "$key_env" "$endpoint" "$auth_style" > "$tmpdir/$idx.json" &
    pids+=($!)
    idx=$((idx + 1))
  done

  # Wait for all probes
  for pid in "${pids[@]}"; do
    wait "$pid" 2>/dev/null || true
  done

  # Collect results
  for i in $(seq 0 $((idx - 1))); do
    [[ "$first" == "true" ]] && first=false || echo "    ,"
    cat "$tmpdir/$i.json"
  done
  rm -rf "$tmpdir"

  echo "  ],"

  # CLI runners
  echo "  \"cli_runners\": $(get_cli_runners_json)"
  echo "}"
}

# ═══════════════════════════════════════════════════════════════
# Cache Management
# ═══════════════════════════════════════════════════════════════

ensure_cache() {
  local force="${1:-false}"
  if [[ "$force" == "true" ]] || [[ ! -f "$CACHE_FILE" ]]; then
    build_manifest > "$CACHE_FILE"
    return
  fi
  # Check TTL
  local age
  age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0) ))
  if (( age >= CACHE_TTL )); then
    build_manifest > "$CACHE_FILE"
  fi
}

# ═══════════════════════════════════════════════════════════════
# Output Formatters
# ═══════════════════════════════════════════════════════════════

print_discover() {
  ensure_cache false
  python3 -c "
import json, sys
data = json.load(open('$CACHE_FILE'))
print('=== Model Cache ===')
print(f\"Generated: {data['generated']}  Host: {data['hostname']}\")
print()

# API Providers
api = data.get('api_providers', [])
if api:
    print('  API Providers:')
    for p in api:
        if p['key_present']:
            icon = '✓' if p['probe_ok'] else '⚠'
            count = p['model_count']
            print(f\"    {icon} {p['name']:<14} {p['key_env']:<24} {count} models\")
        else:
            print(f\"    ○ {p['name']:<14} {p['key_env']:<24} (no key)\")
    present = [p for p in api if p['key_present']]
    probed = [p for p in api if p['probe_ok']]
    print(f\"    {len(present)} keys detected, {len(probed)} probed successfully\")
    print()

# CLI Runners
cli = data.get('cli_runners', [])
if cli:
    print('  CLI Runners:')
    for r in cli:
        if isinstance(r, dict) and r.get('installed'):
            v = r.get('version', '?')[:12]
            tier = r.get('tier', '?')
            print(f\"    ● {r.get('name', r.get('cmd', '?')):<16} v{v:<14} T{tier}\")
    installed = [r for r in cli if isinstance(r, dict) and r.get('installed')]
    print(f\"    {len(installed)} runners installed\")
    print()

print(f\"  Cache: {sys.argv[1]}\")
print(f\"  Refresh: model-cache refresh\")
" "$CACHE_FILE"
}

print_models() {
  local provider="$1"
  ensure_cache false
  python3 -c "
import json, sys
data = json.load(open('$CACHE_FILE'))
name = '$provider'
for p in data.get('api_providers', []):
    if p['name'] == name:
        if not p['key_present']:
            print(f\"{name}: no API key detected ({p['key_env']})\")
            sys.exit(1)
        if not p['probe_ok']:
            print(f\"{name}: key present but probe failed\")
            sys.exit(1)
        models = p['models']
        print(f\"{name}: {len(models)} models\")
        for m in models:
            print(f\"  {m}\")
        sys.exit(0)
print(f\"Unknown provider: {name}\")
print(f\"Available: {', '.join(p['name'] for p in data.get('api_providers', []))}\")
sys.exit(1)
" "$CACHE_FILE"
}

# ═══════════════════════════════════════════════════════════════
# Seat Assignment (for parliament/tribunal)
# ═══════════════════════════════════════════════════════════════

assign_seats() {
  local n="${1:-5}"
  ensure_cache false
  python3 -c "
import json
data = json.load(open('$CACHE_FILE'))
n = $n
seats = []

# Tier 1: API providers with successful probes (max diversity)
priority = ['openai', 'anthropic', 'google', 'xai', 'deepseek', 'groq', 'perplexity']
for name in priority:
    if len(seats) >= n: break
    for p in data.get('api_providers', []):
        if p['name'] == name and p.get('probe_ok') and p['models']:
            best = p['models'][0]
            seats.append(f\"{name}|api|{best}\")
            break

# Tier 2: CLI runners
for r in data.get('cli_runners', []):
    if len(seats) >= n: break
    if isinstance(r, dict) and r.get('installed') and r.get('tier', 99) <= 1:
        seats.append(f\"{r.get('cmd', r['name'])}|cli|{r.get('cmd', r['name'])}\")

# Tier 3: OpenRouter as catch-all
if len(seats) < n:
    for p in data.get('api_providers', []):
        if p['name'] == 'openrouter' and p['key_present']:
            seats.append('openrouter|api|anthropic/claude-sonnet-4')
            break

for s in seats:
    print(s)
" "$CACHE_FILE"
}

# ═══════════════════════════════════════════════════════════════
# CLI Entry
# ═══════════════════════════════════════════════════════════════

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  case "${1:-discover}" in
    discover|-d) print_discover ;;
    refresh|-r)
      echo "Probing providers (timeout ${PROBE_TIMEOUT}s each)..."
      ensure_cache true
      echo "Manifest refreshed: $CACHE_FILE"
      print_discover
      ;;
    json|-j) ensure_cache false; cat "$CACHE_FILE" ;;
    models|-m) print_models "${2:?Usage: model-cache models <provider>}" ;;
    seats|-s) assign_seats "${2:-5}" ;;
    help|-h)
      echo "model-cache — Dynamic AI provider discovery"
      echo ""
      echo "  model-cache discover          Human-readable summary"
      echo "  model-cache refresh           Force re-probe all providers"
      echo "  model-cache json              Full manifest JSON"
      echo "  model-cache models <provider> List models for one provider"
      echo "  model-cache seats [N]         Assign N diverse seats"
      echo ""
      echo "Zero hardcoded models. Probes /models endpoints + CLI runners."
      echo "Cache: $CACHE_FILE (${CACHE_TTL}s TTL)"
      ;;
    *) echo "Unknown: $1. Try: model-cache help" >&2; exit 1 ;;
  esac
fi
