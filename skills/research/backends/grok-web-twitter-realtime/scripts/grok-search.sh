#!/bin/bash
# Grok Research - Quick search via xAI API
# Usage: grok-search.sh "your query" [model]

set -euo pipefail

QUERY="${1:-}"
MODEL="${2:-grok-3}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: grok-search.sh \"your query\" [model]"
  echo "Models: grok-3 (deep), grok-3-mini (fast)"
  exit 1
fi

if [[ -z "${XAI_API_KEY:-}" ]]; then
  # Try loading from clawdbot env
  if [[ -f ~/.clawdbot/.env ]]; then
    export $(grep XAI_API_KEY ~/.clawdbot/.env | xargs)
  fi
fi

if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "Error: XAI_API_KEY not set"
  exit 1
fi

curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"$QUERY\"}]
  }" | jq -r '.choices[0].message.content // .error.message // "No response"'
