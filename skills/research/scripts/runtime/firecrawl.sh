#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"
load_env_file

API_BASE="https://api.firecrawl.dev/v1"

usage() {
  cat <<'EOF'
Usage: firecrawl [--status] | firecrawl <command> [args] [options]

Commands:
  search <query>
  scrape <url>
  map <url>
  crawl <url>
  extract <urls...>
  batch <urls...>
  status <type> <id>
  help
EOF
}

api_post() {
  local endpoint="$1"
  local body="$2"
  require_env FIRECRAWL_API_KEY
  curl -fsSL "${API_BASE}/${endpoint}" \
    -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$body"
}

api_get() {
  local endpoint="$1"
  require_env FIRECRAWL_API_KEY
  curl -fsSL "${API_BASE}/${endpoint}" \
    -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" \
    -H "Content-Type: application/json"
}

poll_job() {
  local endpoint="$1"
  local job_id="$2"
  local attempts=0
  while [[ "$attempts" -lt 120 ]]; do
    local response
    response="$(api_get "${endpoint}/${job_id}")"
    local status
    status="$(printf '%s' "$response" | jq -r '.status // .data.status // empty')"
    if [[ "$status" == "completed" ]]; then
      printf '%s' "$response"
      return 0
    fi
    if [[ "$status" == "failed" ]]; then
      printf '%s\n' "$response" >&2
      die "Firecrawl job failed"
    fi
    attempts=$((attempts + 1))
    sleep 5
  done
  die "Firecrawl job timed out"
}

global_status() {
  require_env FIRECRAWL_API_KEY
  echo "firecrawl"
  echo "  authenticated: yes"
  api_post "scrape" '{"url":"https://example.com","formats":["markdown"]}' >/dev/null
  echo "  api: ok"
}

search_cmd() {
  local query="$1"
  shift
  local limit=5
  local scrape=0
  local scrape_formats="markdown"
  local tbs=""
  local location=""
  local country="US"
  local output=""
  local as_json=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -l|--limit)
        limit="$2"; shift 2 ;;
      --scrape)
        scrape=1; shift ;;
      --scrape-formats)
        scrape_formats="$2"; shift 2 ;;
      --tbs)
        tbs="$2"; shift 2 ;;
      --location)
        location="$2"; shift 2 ;;
      --country)
        country="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --json)
        as_json=1; shift ;;
      *)
        die "Unknown firecrawl search arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg query "$query" \
    --argjson limit "$limit" \
    --arg country "$country" \
    --arg tbs "$tbs" \
    --arg location "$location" \
    --argjson scrape "$scrape" \
    --arg scrapeFormats "$scrape_formats" '
    {
      query: $query,
      limit: $limit
    }
    + (if $country != "" then {country: $country} else {} end)
    + (if $location != "" then {location: $location} else {} end)
    + (if $tbs != "" then {tbs: $tbs} else {} end)
    + (if $scrape == 1 then {scrapeOptions: {formats: ($scrapeFormats | split(","))}} else {} end)
  ')"

  local response
  response="$(api_post "search" "$body")"
  save_output "$output" "$response"
  if [[ "$as_json" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
  else
    printf '%s\n' "$response" | json_pretty
  fi
}

scrape_cmd() {
  local url="$1"
  shift
  local formats="markdown"
  local only_main=1
  local wait_for=0
  local include_tags=""
  local exclude_tags=""
  local output=""
  local as_json=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -f|--format)
        formats="$2"; shift 2 ;;
      -H|--html)
        formats="html"; shift ;;
      --only-main-content)
        only_main=1; shift ;;
      --wait-for)
        wait_for="$2"; shift 2 ;;
      --include-tags)
        include_tags="$2"; shift 2 ;;
      --exclude-tags)
        exclude_tags="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --json)
        as_json=1; shift ;;
      *)
        die "Unknown firecrawl scrape arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg url "$url" \
    --arg formats "$formats" \
    --argjson onlyMain "$only_main" \
    --argjson waitFor "$wait_for" \
    --arg include "$include_tags" \
    --arg exclude "$exclude_tags" '
    {
      url: $url,
      formats: ($formats | split(",")),
      onlyMainContent: ($onlyMain == 1),
      waitFor: $waitFor
    }
    + (if $include != "" then {includeTags: ($include | split(","))} else {} end)
    + (if $exclude != "" then {excludeTags: ($exclude | split(","))} else {} end)
  ')"
  local response
  response="$(api_post "scrape" "$body")"
  save_output "$output" "$response"
  if [[ "$as_json" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
  else
    printf '%s\n' "$response" | jq -r '.data.markdown // .data.html // .data.rawHtml // .data | tostring'
  fi
}

map_cmd() {
  local url="$1"
  shift
  local limit=""
  local search=""
  local include_subdomains=1
  local output=""
  local as_json=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -l|--limit)
        limit="$2"; shift 2 ;;
      -s|--search)
        search="$2"; shift 2 ;;
      --include-subdomains)
        include_subdomains=1; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --json)
        as_json=1; shift ;;
      *)
        die "Unknown firecrawl map arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg url "$url" \
    --arg search "$search" \
    --arg limit "$limit" \
    --argjson includeSubdomains "$include_subdomains" '
    {
      url: $url,
      includeSubdomains: ($includeSubdomains == 1)
    }
    + (if $search != "" then {search: $search} else {} end)
    + (if $limit != "" then {limit: ($limit | tonumber)} else {} end)
  ')"
  local response
  response="$(api_post "map" "$body")"
  save_output "$output" "$response"
  if [[ "$as_json" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
  else
    printf '%s\n' "$response" | jq -r '.links[]? | if type=="string" then . else .url end'
  fi
}

crawl_cmd() {
  local url="$1"
  shift
  local limit=100
  local max_depth=""
  local include_paths=""
  local exclude_paths=""
  local allow_subdomains=0
  local allow_external=0
  local output=""
  local wait_for_completion=1

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -l|--limit)
        limit="$2"; shift 2 ;;
      -d|--max-depth)
        max_depth="$2"; shift 2 ;;
      --include-paths)
        include_paths="$2"; shift 2 ;;
      --exclude-paths)
        exclude_paths="$2"; shift 2 ;;
      --allow-subdomains)
        allow_subdomains=1; shift ;;
      --allow-external)
        allow_external=1; shift ;;
      --no-wait)
        wait_for_completion=0; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        die "Unknown firecrawl crawl arg: $1" ;;
    esac
  done

  local body
  body="$(jq -n \
    --arg url "$url" \
    --argjson limit "$limit" \
    --arg maxDepth "$max_depth" \
    --arg include "$include_paths" \
    --arg exclude "$exclude_paths" \
    --argjson allowSubdomains "$allow_subdomains" \
    --argjson allowExternal "$allow_external" '
    {
      url: $url,
      limit: $limit,
      scrapeOptions: {formats: ["markdown"], onlyMainContent: true}
    }
    + (if $maxDepth != "" then {maxDiscoveryDepth: ($maxDepth | tonumber)} else {} end)
    + (if $include != "" then {includePaths: ($include | split(","))} else {} end)
    + (if $exclude != "" then {excludePaths: ($exclude | split(","))} else {} end)
    + (if $allowSubdomains == 1 then {allowSubdomains: true} else {} end)
    + (if $allowExternal == 1 then {allowExternalLinks: true} else {} end)
  ')"
  local response
  response="$(api_post "crawl" "$body")"
  local job_id
  job_id="$(printf '%s' "$response" | jq -r '.id')"
  if [[ "$wait_for_completion" -eq 0 ]]; then
    printf '%s\n' "$response" | json_pretty
    return 0
  fi
  local result
  result="$(poll_job "crawl" "$job_id")"
  save_output "$output" "$result"
  printf '%s\n' "$result" | json_pretty
}

extract_cmd() {
  [[ $# -gt 0 ]] || die "At least one URL is required"
  local prompt=""
  local schema=""
  local show_sources=0
  local enable_web_search=0
  local output=""
  local no_wait=0
  local urls=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -p|--prompt)
        prompt="$2"; shift 2 ;;
      --schema)
        schema="$2"; shift 2 ;;
      --show-sources)
        show_sources=1; shift ;;
      --enable-web-search)
        enable_web_search=1; shift ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --no-wait)
        no_wait=1; shift ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  local url_json
  url_json="$(printf '%s\n' "${urls[@]}" | jq -R . | jq -s .)"
  local body
  body="$(jq -n \
    --argjson urls "$url_json" \
    --arg prompt "$prompt" \
    --arg schema "$schema" \
    --argjson showSources "$show_sources" \
    --argjson enableWebSearch "$enable_web_search" '
    {
      urls: $urls,
      showSources: ($showSources == 1),
      enableWebSearch: ($enableWebSearch == 1)
    }
    + (if $prompt != "" then {prompt: $prompt} else {} end)
    + (if $schema != "" then {schema: ($schema | fromjson)} else {} end)
  ')"
  local response
  response="$(api_post "extract" "$body")"
  local job_id
  job_id="$(printf '%s' "$response" | jq -r '.id')"
  if [[ "$no_wait" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
    return 0
  fi
  local result
  result="$(poll_job "extract" "$job_id")"
  save_output "$output" "$result"
  printf '%s\n' "$result" | json_pretty
}

batch_cmd() {
  [[ $# -gt 0 ]] || die "At least one URL is required"
  local formats="markdown"
  local only_main=1
  local max_concurrency=""
  local output=""
  local no_wait=0
  local urls=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -f|--format)
        formats="$2"; shift 2 ;;
      --only-main-content)
        only_main=1; shift ;;
      --max-concurrency)
        max_concurrency="$2"; shift 2 ;;
      -o|--output)
        output="$2"; shift 2 ;;
      --no-wait)
        no_wait=1; shift ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  local url_json
  url_json="$(printf '%s\n' "${urls[@]}" | jq -R . | jq -s .)"
  local body
  body="$(jq -n \
    --argjson urls "$url_json" \
    --arg formats "$formats" \
    --argjson onlyMain "$only_main" \
    --arg maxConcurrency "$max_concurrency" '
    {
      urls: $urls,
      formats: ($formats | split(",")),
      onlyMainContent: ($onlyMain == 1),
      ignoreInvalidURLs: true
    }
    + (if $maxConcurrency != "" then {maxConcurrency: ($maxConcurrency | tonumber)} else {} end)
  ')"
  local response
  response="$(api_post "batch/scrape" "$body")"
  local job_id
  job_id="$(printf '%s' "$response" | jq -r '.id')"
  if [[ "$no_wait" -eq 1 ]]; then
    printf '%s\n' "$response" | json_pretty
    return 0
  fi
  local result
  result="$(poll_job "batch/scrape" "$job_id")"
  save_output "$output" "$result"
  printf '%s\n' "$result" | json_pretty
}

status_cmd() {
  local type="$1"
  local id="$2"
  shift 2
  local output=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -o|--output)
        output="$2"; shift 2 ;;
      *)
        die "Unknown firecrawl status arg: $1" ;;
    esac
  done
  local endpoint=""
  case "$type" in
    crawl) endpoint="crawl" ;;
    extract) endpoint="extract" ;;
    batch) endpoint="batch/scrape" ;;
    *) die "Invalid firecrawl status type: $type" ;;
  esac
  local response
  response="$(api_get "${endpoint}/${id}")"
  save_output "$output" "$response"
  printf '%s\n' "$response" | json_pretty
}

if [[ "${1:-}" == "--status" ]]; then
  global_status
  exit 0
fi

cmd="${1:-help}"
shift || true

case "$cmd" in
  search) [[ $# -gt 0 ]] || die "Query required"; query="$1"; shift; search_cmd "$query" "$@" ;;
  scrape) [[ $# -gt 0 ]] || die "URL required"; url="$1"; shift; scrape_cmd "$url" "$@" ;;
  map) [[ $# -gt 0 ]] || die "URL required"; url="$1"; shift; map_cmd "$url" "$@" ;;
  crawl) [[ $# -gt 0 ]] || die "URL required"; url="$1"; shift; crawl_cmd "$url" "$@" ;;
  extract) extract_cmd "$@" ;;
  batch) batch_cmd "$@" ;;
  status) [[ $# -ge 2 ]] || die "Type and id required"; type="$1"; id="$2"; shift 2; status_cmd "$type" "$id" "$@" ;;
  help|--help|-h) usage ;;
  *) die "Unknown firecrawl command: ${cmd}" ;;
esac
