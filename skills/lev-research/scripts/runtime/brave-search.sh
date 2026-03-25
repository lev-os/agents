#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"
load_env_file

API_BASE="https://api.search.brave.com/res/v1"

usage() {
  cat <<'EOF'
Usage: brave-search <command> [args] [options]

Commands:
  search <query>    Search the web
  news <query>      Search news
  video <query>     Search videos
  image <query>     Search images
  local <query>     Search local businesses
  status            Verify API key
  help              Show help
EOF
}

run_get() {
  local endpoint="$1"
  shift
  require_env BRAVE_API_KEY
  curl -fsSLG "${API_BASE}/${endpoint}" \
    -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
    -H "Accept: application/json" \
    "$@"
}

status_cmd() {
  require_env BRAVE_API_KEY
  echo "brave-search"
  echo "  authenticated: yes"
  if response="$(curl -sSG "${API_BASE}/web/search" \
    -H "X-Subscription-Token: ${BRAVE_API_KEY}" \
    -H "Accept: application/json" \
    --data-urlencode "q=test" \
    --data-urlencode "count=1" \
    -w $'\n%{http_code}')"; then
    http_code="$(printf '%s' "$response" | tail -n 1)"
    case "$http_code" in
      200) echo "  api: ok" ;;
      401) die "Brave API key invalid" ;;
      429) echo "  api: rate-limited" ;;
      *) echo "  api: unexpected-status-${http_code}" ;;
    esac
  else
    die "Brave API verification failed"
  fi
}

search_family() {
  local endpoint="$1"
  local query="$2"
  shift 2
  local num=10
  local country="US"
  local lang="en"
  local freshness=""
  local safe="moderate"
  local output=""
  local as_json=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -n|--num|--limit)
        num="$2"; shift 2 ;;
      -c|--country)
        country="$2"; shift 2 ;;
      -l|--lang)
        lang="$2"; shift 2 ;;
      --freshness)
        freshness="$2"; shift 2 ;;
      --safe)
        safe="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --json)
        as_json=1; shift ;;
      *)
        die "Unknown arg for brave-search ${endpoint}: $1" ;;
    esac
  done

  local args=(
    --data-urlencode "q=${query}"
    --data-urlencode "count=${num}"
    --data-urlencode "country=${country}"
  )

  if [[ "$endpoint" == "web/search" ]]; then
    args+=(--data-urlencode "search_lang=${lang}" --data-urlencode "safesearch=${safe}")
  elif [[ "$endpoint" == "images/search" ]]; then
    args+=(--data-urlencode "safesearch=${safe}")
  fi

  if [[ -n "$freshness" ]]; then
    args+=(--data-urlencode "freshness=${freshness}")
  fi

  local response
  response="$(run_get "${endpoint}" "${args[@]}")"
  save_output "$output" "$response"
  if [[ "$as_json" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
  else
    printf '%s\n' "$response" | json_pretty
  fi
}

local_cmd() {
  local query="$1"
  shift
  local country="US"
  local output=""
  local as_json=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -c|--country)
        country="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --json)
        as_json=1; shift ;;
      *)
        die "Unknown arg for brave-search local: $1" ;;
    esac
  done

  local response
  response="$(run_get "web/search" \
    --data-urlencode "q=${query}" \
    --data-urlencode "country=${country}" \
    --data-urlencode "result_filter=locations")"
  save_output "$output" "$response"
  if [[ "$as_json" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
  else
    printf '%s\n' "$response" | json_pretty
  fi
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  search) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_family "web/search" "$query" "$@" ;;
  news) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_family "news/search" "$query" "$@" ;;
  video) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_family "videos/search" "$query" "$@" ;;
  image) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_family "images/search" "$query" "$@" ;;
  local) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; local_cmd "$query" "$@" ;;
  status) status_cmd ;;
  help|--help|-h) usage ;;
  *) die "Unknown brave-search command: ${cmd}" ;;
esac
