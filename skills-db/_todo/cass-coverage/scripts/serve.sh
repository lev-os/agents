#!/bin/bash
# Serves the dashboard + cache via local HTTP so iframe transcripts actually load.
# Chrome blocks file:// → file:// iframes from different directories; HTTP fixes it.
#
# Usage:
#   bash serve.sh                              # serves $HOME on :8765
#   bash serve.sh --port 9000                  # custom port
#   bash serve.sh --coverage <dir>             # auto-open dashboard in dir
set -uo pipefail

PORT=8775
COVERAGE=""
ROOT="/"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port) PORT="$2"; shift 2;;
        --coverage) COVERAGE="$2"; shift 2;;
        --root) ROOT="$2"; shift 2;;
        -h|--help)
            sed -n '2,12p' "$0"
            exit 0;;
        *) echo "unknown arg: $1" >&2; exit 1;;
    esac
done

if ! command -v python3 >/dev/null; then
    echo "python3 required" >&2
    exit 1
fi

# Bind to localhost only — never expose
echo "Serving $ROOT on http://127.0.0.1:$PORT"
echo "Press Ctrl+C to stop."

if [ -n "$COVERAGE" ]; then
    DASH=$(realpath "$COVERAGE/dashboard.html")
    REL_DASH="${DASH#$ROOT}"
    URL="http://127.0.0.1:$PORT$REL_DASH?serve=1"
    echo "Open: $URL"
    (sleep 1 && open "$URL" 2>/dev/null) &
fi

cd "$ROOT" && exec python3 -m http.server "$PORT" --bind 127.0.0.1
