#!/usr/bin/env bash

set -euo pipefail

load_env_file() {
  local env_file="${HOME}/.env.local"
  if [[ -f "$env_file" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "$line" ]] && continue
      [[ "$line" =~ ^[[:space:]]*# ]] && continue
      if [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
        local key="${line%%=*}"
        local value="${line#*=}"
        value="${value%$'\r'}"
        if [[ "${value:0:1}" == "\"" && "${value: -1}" == "\"" ]]; then
          value="${value:1:${#value}-2}"
        elif [[ "${value:0:1}" == "'" && "${value: -1}" == "'" ]]; then
          value="${value:1:${#value}-2}"
        fi
        export "${key}=${value}"
      fi
    done < "$env_file"
  fi
}

die() {
  echo "Error: $*" >&2
  exit 1
}

require_env() {
  local key="$1"
  [[ -n "${!key:-}" ]] || die "${key} not set"
}

json_pretty() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

save_output() {
  local output_path="$1"
  local content="$2"
  if [[ -n "$output_path" ]]; then
    printf '%s' "$content" > "$output_path"
    echo "Saved to $output_path" >&2
  fi
}
