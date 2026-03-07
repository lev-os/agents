#!/bin/bash
# Shell wrapper for embed.py
# Usage: embed.sh "text to embed"
#        echo "text" | embed.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "$1" ]; then
    python3 "$SCRIPT_DIR/embed.py" "$@"
else
    python3 "$SCRIPT_DIR/embed.py"
fi
