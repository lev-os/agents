#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"
load_env_file

EXA_BASE="https://api.exa.ai"

load_exa_key() {
  if [[ -n "${EXA_API_KEY:-}" ]]; then
    return 0
  fi
  local config_file="${HOME}/.clawdbot/credentials/exa/config.json"
  if [[ -f "$config_file" ]]; then
    export EXA_API_KEY
    EXA_API_KEY="$(jq -r '.apiKey // empty' "$config_file")"
  fi
}

usage() {
  cat <<'EOF'
Usage: exa <command> [args] [options]

Commands:
  search <query>            Search the web with Exa
  contents <urls...>        Fetch full page contents
  answer <query>            Generate an answer with citations
  status                    Verify API key
  help                      Show help
EOF
}

api_post() {
  local url="$1"
  local body="$2"
  load_exa_key
  require_env EXA_API_KEY
  curl -fsSL "$url" \
    -H "x-api-key: ${EXA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$body"
}

api_get() {
  local url="$1"
  load_exa_key
  require_env EXA_API_KEY
  curl -fsSL "$url" -H "x-api-key: ${EXA_API_KEY}"
}

api_delete() {
  local url="$1"
  load_exa_key
  require_env EXA_API_KEY
  curl -fsSL -X DELETE "$url" -H "x-api-key: ${EXA_API_KEY}"
}

status_cmd() {
  load_exa_key
  require_env EXA_API_KEY
  echo "exa"
  echo "  authenticated: yes"
  local response
  response="$(curl -sS -X POST "${EXA_BASE}/search" \
    -H "x-api-key: ${EXA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"query":"test","numResults":1}' \
    -w $'\n%{http_code}')"
  local http_code
  http_code="$(printf '%s' "$response" | tail -n 1)"
  case "$http_code" in
    200) echo "  api: ok" ;;
    401) die "Exa API key invalid" ;;
    429) echo "  api: rate-limited" ;;
    *) echo "  api: unexpected-status-${http_code}" ;;
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
  local location="NL"
  local include_text=1
  local include_summary=1
  local output=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--num)
        num="$2"; shift 2 ;;
      --type)
        type="$2"; shift 2 ;;
      --category)
        category="$2"; shift 2 ;;
      --domains)
        domains="$2"; shift 2 ;;
      --exclude)
        exclude="$2"; shift 2 ;;
      --since)
        since="$2"; shift 2 ;;
      --until)
        until="$2"; shift 2 ;;
      --location)
        location="$2"; shift 2 ;;
      --no-text)
        include_text=0; shift ;;
      --no-summary)
        include_summary=0; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        die "Unknown exa search arg: $1" ;;
    esac
  done

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
      numResults: $numResults,
      userLocation: $location
    }
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
  [[ $# -gt 0 ]] || die "At least one URL is required"
  local max_chars=2000
  local num_sentences=3
  local highlights_per_url=2
  local with_summary=1
  local output=""
  local urls=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --max-chars)
        max_chars="$2"; shift 2 ;;
      --num-sentences)
        num_sentences="$2"; shift 2 ;;
      --highlights-per-url)
        highlights_per_url="$2"; shift 2 ;;
      --no-summary)
        with_summary=0; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  local url_json
  url_json="$(printf '%s\n' "${urls[@]}" | jq -R . | jq -s .)"
  local body
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

  local response
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
        output="$2"; shift 2 ;;
      *)
        die "Unknown exa answer arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg query "$query" \
    --argjson withText "$with_text" '
    {
      query: $query
    }
    + (if $withText == 1 then {text: true} else {} end)
  ')"

  local response
  response="$(api_post "${EXA_BASE}/answer" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}
cmd="${1:-help}"
shift || true

case "$cmd" in
  search) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_cmd "$query" "$@" ;;
  contents) contents_cmd "$@" ;;
  answer) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; answer_cmd "$query" "$@" ;;
  status) status_cmd ;;
  help|--help|-h) usage ;;
  *) die "Unknown exa command: ${cmd}" ;;
esac
