#!/bin/bash
# Exa content extraction from URLs

if [ $# -eq 0 ]; then
    echo "Usage: bash content.sh \"url1\" \"url2\" ..." >&2
    exit 1
fi

# Load API key: env var > credentials file
if [ -z "${EXA_API_KEY:-}" ]; then
    CONFIG_FILE="$HOME/.clawdbot/credentials/exa/config.json"
    if [ -f "$CONFIG_FILE" ]; then
        EXA_API_KEY=$(jq -r '.apiKey' "$CONFIG_FILE")
    fi
fi

if [ -z "${EXA_API_KEY:-}" ]; then
    echo "Error: EXA_API_KEY not found. Set EXA_API_KEY env var or create $HOME/.clawdbot/credentials/exa/config.json" >&2
    exit 1
fi

# Build URLs array
URLS=$(printf '%s\n' "$@" | jq -R . | jq -s .)

# Build payload
PAYLOAD=$(jq -n \
    --argjson urls "$URLS" \
    '{
        urls: $urls,
        text: { maxCharacters: 2000 },
        highlights: { numSentences: 3, highlightsPerUrl: 2 },
        summary: {}
    }')

# Call API
curl -s -X POST 'https://api.exa.ai/contents' \
    -H "x-api-key: $EXA_API_KEY" \
    -H 'Content-Type: application/json' \
    -d "$PAYLOAD"
