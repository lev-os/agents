#!/bin/bash
# Bake all chain root transcripts via cass export-html → ~/.cache/cass-lev/<project>/<chain>/<sid>.html
# Idempotent: skips already-baked files (--lazy by default).
# Inputs:
#   --coverage <path/to/coverage.json>
#   --project <slug>            (default: from coverage.meta.project)
#   --rebake                    (force re-bake even if file exists)
set -uo pipefail

COVERAGE=""
PROJECT=""
LAZY=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --coverage) COVERAGE="$2"; shift 2;;
        --project) PROJECT="$2"; shift 2;;
        --rebake) LAZY=0; shift;;
        *) echo "unknown arg: $1" >&2; exit 1;;
    esac
done

if [ -z "$COVERAGE" ]; then
    echo "usage: bake.sh --coverage <coverage.json> [--project <slug>] [--rebake]" >&2
    exit 1
fi

if [ -z "$PROJECT" ]; then
    PROJECT=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['meta']['project'])" "$COVERAGE")
fi

CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}/cass-lev/$PROJECT"
mkdir -p "$CACHE_ROOT"
LOG="$CACHE_ROOT/bake.log"
: > "$LOG"

OVERRIDE_STYLE='<style id="__lev_override">
.message,.message-user,.message-assistant,.message-agent,.message-system,.message-tool,.message-thinking{border-left:0 !important;border-left-width:0 !important;transition:none !important}
.agent-claude .message-assistant,.agent-codex .message-assistant,.agent-cursor .message-assistant,.agent-claude .message-user,.agent-codex .message-user,.agent-cursor .message-user,.agent-claude .message-system,.agent-codex .message-system,.agent-cursor .message-system,.agent-claude .message-tool,.agent-codex .message-tool,.agent-cursor .message-tool{border-left-color:transparent !important;border-left-width:0 !important}
.message:hover{background:var(--card,#131318) !important;background-color:var(--card,#131318) !important}
.message-link{opacity:0.4 !important}.message:hover .message-link{opacity:0.8 !important}
.message{padding-left:var(--space-4,12px) !important}
</style>'

# Emit one line per (chain_id, sid, path) we want baked
python3 - <<PY > /tmp/bake_jobs.tsv
import json, re
cov = json.load(open("$COVERAGE"))
seen = set()
for c in cov["chains"]:
    if c.get("msgs", 0) < 5: continue
    cid = c["id"]
    safe = re.sub(r"[^A-Za-z0-9_-]", "", cid)
    paths = c.get("session_paths", [])
    lineage = c.get("lineage", [cid])
    for sid, p in zip(lineage, paths or [None]*len(lineage)):
        if not p: continue
        key = (safe, sid)
        if key in seen: continue
        seen.add(key)
        print(f"{safe}\t{sid}\t{p}")
PY

TOTAL=$(wc -l < /tmp/bake_jobs.tsv | tr -d ' ')
echo "$(date +%T) baking $TOTAL transcripts → $CACHE_ROOT/" | tee -a "$LOG"

OK=0; SKIP=0; FAIL=0; COUNT=0
while IFS=$'\t' read -r safe sid path; do
    COUNT=$((COUNT+1))
    out_dir="$CACHE_ROOT/$safe"
    out_file="$out_dir/$sid.html"
    if [ $LAZY -eq 1 ] && [ -f "$out_file" ]; then
        SKIP=$((SKIP+1))
        continue
    fi
    if [ ! -f "$path" ]; then
        echo "MISS $path" >> "$LOG"
        FAIL=$((FAIL+1))
        continue
    fi
    mkdir -p "$out_dir"
    if cass export-html "$path" --output-dir "$out_dir" --filename "$sid.html" --theme dark --no-cdns 2>>"$LOG" >/dev/null; then
        # Inject override CSS into baked HTML
        python3 - "$out_file" <<PY
import sys
f = sys.argv[1]
t = open(f).read()
if "__lev_override" not in t and "</head>" in t:
    open(f, "w").write(t.replace("</head>", '''$OVERRIDE_STYLE\n</head>''', 1))
PY
        OK=$((OK+1))
    else
        FAIL=$((FAIL+1))
        echo "FAIL $sid" >> "$LOG"
    fi
    if [ $((COUNT % 25)) -eq 0 ]; then
        echo "$(date +%T) progress $COUNT/$TOTAL ok=$OK skip=$SKIP fail=$FAIL" | tee -a "$LOG"
    fi
done < /tmp/bake_jobs.tsv

echo "$(date +%T) DONE total=$TOTAL ok=$OK skip=$SKIP fail=$FAIL" | tee -a "$LOG"
echo "cache: $CACHE_ROOT"
