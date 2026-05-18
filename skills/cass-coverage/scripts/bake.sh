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
/* __lev_override v2 — chat polish for cass-baked transcripts */
:root{--lev-bg:#0a0a0c;--lev-bg2:#0f0f12;--lev-card:#131318;--lev-card2:#181820;--lev-line:#1d1d22;--lev-line2:#27272e;--lev-fg:#d4d4d8;--lev-muted:#71717a;--lev-muted2:#a1a1aa;--lev-accent:#5eead4;--lev-purple:#a78bfa;--lev-amber:#fbbf24;--lev-good:#10b981;--lev-bad:#f87171;--lev-content-w:920px;--lev-radius:8px}
html,body{background:var(--lev-bg) !important;color:var(--lev-fg) !important;font-family:-apple-system,'SF Pro Text','Inter',ui-sans-serif,system-ui,sans-serif !important;font-feature-settings:'cv11','ss01','ss03' !important;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
::selection{background:rgba(94,234,212,0.25);color:var(--lev-fg)}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--lev-line2);border-radius:5px;border:2px solid var(--lev-bg)}
::-webkit-scrollbar-thumb:hover{background:var(--lev-muted)}
.scroll-progress{height:2px !important;background:var(--lev-accent) !important;opacity:.7;box-shadow:none !important}
.header::before,.header-content::before,.header-icons,.window-controls,.traffic-lights,.macos-controls{display:none !important}
.app-container{max-width:1200px !important;margin:0 auto !important;padding:0 24px !important;background:transparent !important}
.header,.header-content,.header-title,.header-meta,.header-agent,.header-project,.toolbar,.toolbar-btn,.search-wrapper,.search-input,.search-count,.floating-nav,.floating-btn,.print-footer{display:none !important}
.conversation,.conversation-messages{max-width:var(--lev-content-w) !important;margin:0 auto !important;padding:8px 0 80px !important;background:transparent !important}
.message,.message-user,.message-assistant,.message-system,.message-tool{max-width:min(920px,calc(100vw - 48px)) !important;margin-left:auto !important;margin-right:auto !important;width:auto !important;box-sizing:border-box !important;overflow:hidden !important}
.app-container{max-width:min(1100px,calc(100vw - 16px)) !important;width:auto !important}
.message-content{max-width:100% !important;width:auto !important;box-sizing:border-box !important}
body{padding:0 12px !important;box-sizing:border-box !important;overflow-x:hidden !important}
body>*{max-width:100% !important;box-sizing:border-box !important}
.header *::before,.header-content::before,.header-title::before,.app-container::before{content:none !important;display:none !important}
.message{background:transparent !important;border:0 !important;border-radius:0 !important;padding:10px 0 12px !important;margin:0 !important;transition:none !important;backdrop-filter:none !important;-webkit-backdrop-filter:none !important;box-shadow:none !important;position:relative;opacity:1 !important;transform:none !important;border-bottom:1px solid var(--lev-line) !important;min-height:0 !important;height:auto !important}
.message:last-child{border-bottom:0 !important}
.message[style]{opacity:1 !important;transform:none !important;min-height:0 !important}
.message.in-view{opacity:1 !important;transform:none !important;min-height:0 !important}
.message-content{min-height:0 !important;height:auto !important}
.message-user{background:transparent !important}
.message-assistant{background:transparent !important}
html body .app-container,html body[class] .app-container{max-width:1100px !important;margin:0 auto !important;padding:0 24px !important;background:transparent !important;box-sizing:border-box !important}
.message-user,.agent-claude .message-user,.agent-codex .message-user,.agent-cursor .message-user{background:transparent !important;border-left:0 !important;border-left-width:0 !important;padding-left:0 !important}
.message-assistant,.agent-claude .message-assistant,.agent-codex .message-assistant,.agent-cursor .message-assistant{background:transparent !important;border-left:0 !important;border-left-width:0 !important;padding-left:0 !important}
.message-system,.message-tool,.message-thinking{background:transparent !important;border-left:0 !important;opacity:.85 !important}
.message:hover,.message-user:hover,.message-assistant:hover,.message-agent:hover,.message-system:hover,.message-tool:hover{background:transparent !important;background-color:transparent !important;backdrop-filter:none !important;-webkit-backdrop-filter:none !important;filter:none !important;box-shadow:none !important;transition:none !important}
.message-header{padding:0 0 4px !important;background:transparent !important;border:0 !important;display:flex !important;gap:8px !important;align-items:center !important;font-size:11.5px !important;color:var(--lev-muted) !important;min-height:auto !important}
.message-header-left{display:flex !important;gap:7px !important;align-items:center !important;background:transparent !important}
.message-header-right{display:flex !important;gap:6px !important;align-items:center !important;margin-left:auto !important;background:transparent !important}
.message-icon{width:14px !important;height:14px !important;font-size:11px !important;color:var(--lev-muted) !important;flex-shrink:0 !important;background:transparent !important;border:0 !important;padding:0 !important}
.message-icon .lucide-icon{width:13px !important;height:13px !important}
.message-user .message-icon,.message-user .message-author{color:var(--lev-accent) !important}
.message-assistant .message-icon,.message-assistant .message-author{color:var(--lev-purple) !important}
.message-author{font-size:11.5px !important;font-weight:600 !important;letter-spacing:0.01em !important}
.message-link{opacity:0.25 !important;font-size:10.5px !important;color:var(--lev-muted) !important;transition:opacity .12s !important;text-decoration:none !important}
.message:hover .message-link{opacity:0.7 !important}
.message-content{font-size:14.5px !important;line-height:1.65 !important;color:var(--lev-fg) !important;background:transparent !important;border:0 !important;padding:0 0 0 22px !important;max-width:100% !important;word-wrap:break-word !important;overflow-wrap:break-word !important}
.message-content p{margin:0 0 12px !important;line-height:1.65 !important}
.message-content p:last-child{margin-bottom:0 !important}
.message-content h1,.message-content h2,.message-content h3,.message-content h4{margin:18px 0 8px !important;font-weight:600 !important;letter-spacing:-0.01em !important;color:var(--lev-fg) !important;line-height:1.3 !important}
.message-content h1{font-size:18px !important;border:0 !important;padding:0 !important}
.message-content h2{font-size:16px !important;border:0 !important;padding:0 !important}
.message-content h3{font-size:14.5px !important}
.message-content h4{font-size:13.5px !important;color:var(--lev-muted2) !important}
.message-content ul,.message-content ol{margin:6px 0 12px !important;padding-left:22px !important}
.message-content li{margin:3px 0 !important;line-height:1.6 !important}
.message-content li::marker{color:var(--lev-muted) !important}
.message-content blockquote{border-left:2px solid var(--lev-line2) !important;padding:0 0 0 14px !important;margin:8px 0 12px !important;color:var(--lev-muted2) !important;font-style:normal !important;background:transparent !important}
.message-content hr{border:0 !important;border-top:1px solid var(--lev-line) !important;margin:18px 0 !important}
.message-content a{color:var(--lev-accent) !important;text-decoration:none !important;border-bottom:1px solid rgba(94,234,212,0.25) !important}
.message-content a:hover{border-bottom-color:var(--lev-accent) !important}
.message-content strong,.message-content b{color:var(--lev-fg) !important;font-weight:600 !important}
.message-content em,.message-content i{color:var(--lev-muted2) !important}
.message-content code{background:var(--lev-card) !important;color:#fce7a8 !important;padding:1.5px 5px !important;border-radius:3px !important;font-size:12.5px !important;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace !important;border:1px solid var(--lev-line) !important;font-weight:500 !important}
.message-content pre{background:var(--lev-card) !important;border:1px solid var(--lev-line) !important;border-radius:var(--lev-radius) !important;padding:12px 14px !important;margin:10px 0 14px !important;overflow-x:auto !important;font-size:12.5px !important;line-height:1.55 !important;position:relative !important}
.message-content pre code{background:transparent !important;border:0 !important;padding:0 !important;font-size:12.5px !important;color:#e4e4e7 !important;font-weight:400 !important}
.message-content pre[class*="language-"]{padding:14px 16px !important}
.copy-code-btn{position:absolute !important;top:6px !important;right:6px !important;background:var(--lev-card2) !important;border:1px solid var(--lev-line2) !important;color:var(--lev-muted) !important;padding:3px 8px !important;border-radius:4px !important;font-size:10.5px !important;cursor:pointer !important;opacity:0 !important;transition:opacity .12s,color .12s !important;font-family:inherit !important}
.message-content pre:hover .copy-code-btn{opacity:1 !important}
.copy-code-btn:hover{color:var(--lev-fg) !important;background:var(--lev-card2) !important;border-color:var(--lev-muted) !important}
.message-content table{border-collapse:collapse !important;margin:8px 0 14px !important;font-size:12.5px !important;background:var(--lev-card) !important;border-radius:6px !important;overflow:hidden !important;border:1px solid var(--lev-line) !important;width:auto !important;max-width:100% !important}
.message-content th,.message-content td{padding:6px 11px !important;border:0 !important;border-right:1px solid var(--lev-line) !important;border-bottom:1px solid var(--lev-line) !important;text-align:left !important;vertical-align:top !important}
.message-content th{background:var(--lev-card2) !important;color:var(--lev-muted2) !important;font-weight:600 !important;font-size:11px !important;text-transform:uppercase !important;letter-spacing:0.04em !important}
.message-content td:last-child,.message-content th:last-child{border-right:0 !important}
.message-content tr:last-child td{border-bottom:0 !important}
.tool-badge{background:var(--lev-card) !important;border:1px solid var(--lev-line) !important;color:var(--lev-muted2) !important;padding:2px 8px !important;border-radius:4px !important;font-size:11px !important;font-family:ui-monospace,'SF Mono',Menlo,monospace !important;display:inline-flex !important;align-items:center !important;gap:5px !important;text-decoration:none !important;transition:border-color .12s !important;cursor:pointer !important;font-weight:500 !important}
.tool-badge:hover{border-color:var(--lev-line2) !important;color:var(--lev-fg) !important}
.tool-badge-icon{width:11px !important;height:11px !important;color:var(--lev-muted) !important}
.tool-badge-icon .lucide-icon{width:11px !important;height:11px !important}
.tool-badge-text{font-weight:500 !important}
.tool-badge-status{font-size:10px !important;color:var(--lev-muted) !important;text-transform:uppercase !important;letter-spacing:0.04em !important}
.tool-status-pending,.pending{color:var(--lev-amber) !important}
.tool-overflow{color:var(--lev-muted) !important;font-size:11px !important;font-style:italic !important;padding:0 4px !important}
.tool-popover{background:var(--lev-card) !important;border:1px solid var(--lev-line2) !important;border-radius:var(--lev-radius) !important;padding:10px 12px !important;box-shadow:0 8px 24px rgba(0,0,0,0.5) !important;max-width:600px !important}
.tool-popover-header{font-size:11px !important;color:var(--lev-muted) !important;text-transform:uppercase !important;letter-spacing:0.04em !important;margin-bottom:6px !important;padding-bottom:6px !important;border-bottom:1px solid var(--lev-line) !important}
.tool-popover-section{margin:6px 0 !important}
.tool-popover-label{font-size:10.5px !important;color:var(--lev-muted) !important;text-transform:uppercase !important;margin-bottom:3px !important}
.floating-nav{background:var(--lev-card) !important;border:1px solid var(--lev-line) !important;border-radius:var(--lev-radius) !important;backdrop-filter:saturate(140%) blur(8px) !important;-webkit-backdrop-filter:saturate(140%) blur(8px) !important;box-shadow:0 4px 12px rgba(0,0,0,0.3) !important;padding:6px !important;gap:4px !important}
.floating-btn{background:transparent !important;border:0 !important;color:var(--lev-muted) !important;width:28px !important;height:28px !important;border-radius:5px !important;cursor:pointer !important;display:flex !important;align-items:center !important;justify-content:center !important;transition:all .12s !important;padding:0 !important}
.floating-btn:hover{color:var(--lev-fg) !important;background:var(--lev-card2) !important}
.floating-btn .lucide-icon{width:14px !important;height:14px !important}
.message.in-view{background:transparent !important}
.message-content kbd{background:var(--lev-card2) !important;border:1px solid var(--lev-line2) !important;border-radius:3px !important;padding:1px 5px !important;font-size:11px !important;font-family:ui-monospace,'SF Mono',Menlo,monospace !important;color:var(--lev-muted2) !important;box-shadow:0 1px 0 var(--lev-line) !important}
.message-content details{background:var(--lev-card) !important;border:1px solid var(--lev-line) !important;border-radius:6px !important;padding:8px 12px !important;margin:8px 0 !important}
.message-content summary{cursor:pointer !important;font-weight:500 !important;color:var(--lev-muted2) !important;font-size:12.5px !important;padding:0 !important}
.message-content summary:hover{color:var(--lev-fg) !important}
.message-content img{max-width:100% !important;border-radius:6px !important;border:1px solid var(--lev-line) !important;margin:6px 0 !important}
.print-only{display:none !important}
@media (max-width:900px){.app-container{padding:0 16px !important}.conversation,.conversation-messages{padding:8px 0 60px !important}.message-content{font-size:14px !important;line-height:1.6 !important;padding-left:0 !important}.message-content pre{font-size:12px !important;padding:10px 12px !important}.header{padding:12px 0 !important}.toolbar{flex-wrap:wrap !important}.search-wrapper{max-width:none !important;flex:1 1 100% !important;order:99 !important}}
@media (max-width:600px){.app-container{padding:0 12px !important}.message-content{font-size:13.5px !important}.header-title{font-size:14px !important}.message-header{font-size:11px !important}}
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
