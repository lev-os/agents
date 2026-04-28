#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"
load_env_file

API_BASE="https://api.valyu.ai/v1"

usage() {
  cat <<'EOF'
Usage: valyu <command> [args] [options]

Commands:
  search <query>
  answer <query>
  contents <urls...>
  research <query>
  help
EOF
}

api_post() {
  local endpoint="$1"
  local body="$2"
  require_env VALYU_API_KEY
  curl -fsSL "${API_BASE}/${endpoint}" \
    -H "x-api-key: ${VALYU_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$body"
}

search_cmd() {
  local query="$1"
  shift
  local num=10
  local search_type="all"
  local fast=0
  local start_date=""
  local end_date=""
  local output=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--num)
        num="$2"; shift 2 ;;
      -t|--type)
        search_type="$2"; shift 2 ;;
      -f|--fast)
        fast=1; shift ;;
      --start)
        start_date="$2"; shift 2 ;;
      --end)
        end_date="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        die "Unknown valyu search arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg query "$query" \
    --argjson max_num_results "$num" \
    --arg search_type "$search_type" \
    --arg start_date "$start_date" \
    --arg end_date "$end_date" \
    --argjson fast "$fast" '
    {
      query: $query,
      max_num_results: $max_num_results,
      search_type: $search_type,
      fast_mode: ($fast == 1)
    }
    + (if $start_date != "" then {start_date: $start_date} else {} end)
    + (if $end_date != "" then {end_date: $end_date} else {} end)
  ')"
  local response
  response="$(api_post "search" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

answer_cmd() {
  local query="$1"
  shift
  local search_type="all"
  local instructions=""
  local streaming=0
  local output=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--type)
        search_type="$2"; shift 2 ;;
      -i|--instructions)
        instructions="$2"; shift 2 ;;
      --stream)
        streaming=1; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        die "Unknown valyu answer arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg query "$query" \
    --arg search_type "$search_type" \
    --arg instructions "$instructions" \
    --argjson streaming "$streaming" '
    {
      query: $query,
      search_type: $search_type,
      streaming: ($streaming == 1)
    }
    + (if $instructions != "" then {system_instructions: $instructions} else {} end)
  ')"
  local response
  response="$(api_post "answer" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

contents_cmd() {
  [[ $# -gt 0 ]] || die "At least one URL is required"
  local length="short"
  local effort="normal"
  local summary=""
  local screenshot=0
  local output=""
  local urls=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -l|--length)
        length="$2"; shift 2 ;;
      -e|--effort)
        effort="$2"; shift 2 ;;
      -s|--summary)
        summary="$2"; shift 2 ;;
      --screenshot)
        screenshot=1; shift ;;
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
    --arg response_length "$length" \
    --arg extract_effort "$effort" \
    --arg summary "$summary" \
    --argjson screenshot "$screenshot" '
    {
      urls: $urls,
      response_length: $response_length,
      extract_effort: $extract_effort,
      screenshot: ($screenshot == 1)
    }
    + (if $summary != "" then {summary: $summary} else {} end)
  ')"
  local response
  response="$(api_post "contents" "$body")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

research_cmd() {
  local query="$1"
  shift
  local turns=5
  local threshold="0.85"
  local output_dir="./valyu-research"
  local strategy="balanced"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--turns)
        turns="$2"; shift 2 ;;
      -t|--threshold)
        threshold="$2"; shift 2 ;;
      -o|--output)
        output_dir="$2"; shift 2 ;;
      --strategy)
        strategy="$2"; shift 2 ;;
      *)
        die "Unknown valyu research arg: $1" ;;
    esac
  done

  node "${SCRIPT_DIR}/valyu-research.mjs" \
    --query "$query" \
    --turns "$turns" \
    --threshold "$threshold" \
    --output "$output_dir" \
    --strategy "$strategy"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  search) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_cmd "$query" "$@" ;;
  answer) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; answer_cmd "$query" "$@" ;;
  contents) contents_cmd "$@" ;;
  research) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; research_cmd "$query" "$@" ;;
  help|--help|-h) usage ;;
  *) die "Unknown valyu command: ${cmd}" ;;
esac
