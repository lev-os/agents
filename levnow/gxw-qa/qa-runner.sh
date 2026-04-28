#!/usr/bin/env bash
# QA runner — per-URL screenshots + functional probes.
# Usage: qa-runner.sh <slug> <url> <kind>
#   kind: variant | matrix | statline | lanefilter
set -u

SLUG="${1:?slug}"
URL="${2:?url}"
KIND="${3:?kind}"

OUTDIR="$HOME/.agents/levnow/gxw-qa/$SLUG"
mkdir -p "$OUTDIR"

log() { echo "[qa:$SLUG] $*"; }

shoot() {
  local w="$1" h="$2" label="$3"
  agent-browser set viewport "$w" "$h" >/dev/null 2>&1
  sleep 0.4
  agent-browser screenshot "$OUTDIR/bp-${label}.png" --full >/dev/null 2>&1
  log "shot bp-${label} (${w}x${h})"
}

log "open $URL"
agent-browser open "$URL" >/dev/null 2>&1 || { log "OPEN_FAIL"; exit 2; }
sleep 0.8

shoot 320 568 320x568
shoot 768 1024 768x1024
shoot 1440 900 1440x900
shoot 1920 1080 1920x1080

# bring back to 1440 for probes
agent-browser set viewport 1440 900 >/dev/null 2>&1
sleep 0.4

VERDICT="$OUTDIR/verdict.md"
: > "$VERDICT"
{
  echo "# QA Verdict — $SLUG"
  echo
  echo "- URL: $URL"
  echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- Breakpoints: 320x568, 768x1024, 1440x900, 1920x1080"
  echo
  echo "## Parity Items"
} >> "$VERDICT"

pass()  { echo "- [x] $1 — PASS" >> "$VERDICT"; }
fail()  { echo "- [ ] $1 — FAIL: $2" >> "$VERDICT"; }
note()  { echo "  - note: $1" >> "$VERDICT"; }

# Helper: eval returns 1/0/null
eval_js() {
  agent-browser eval "$1" 2>/dev/null | tr -d '\r\n'
}

if [[ "$KIND" == "variant" ]]; then
  # 10-point parity from qa/baseline.md
  has_masthead=$(eval_js 'document.querySelector(".masthead") ? 1 : 0')
  [[ "$has_masthead" == "1" ]] && pass "01 Masthead present" || fail "01 Masthead present" ".masthead not found"

  has_proj=$(eval_js 'document.querySelectorAll("[class*=projection]").length')
  [[ "${has_proj:-0}" -gt 0 ]] && pass "02 Projections section ($has_proj items)" || fail "02 Projections" "no projection elements"

  flow_count=$(eval_js 'document.querySelectorAll(".flow-card").length')
  [[ "${flow_count:-0}" -ge 10 ]] && pass "03 Flow grid ($flow_count cards)" || fail "03 Flow grid" "flow-card count=$flow_count"

  cell_count=$(eval_js 'document.querySelectorAll(".matrix .cell, .matrix-cell").length')
  [[ "${cell_count:-0}" -ge 100 ]] && pass "04 Matrix (cells=$cell_count)" || fail "04 Matrix" "cells=$cell_count"

  ledger_rows=$(eval_js 'document.querySelectorAll(".ledger-row").length')
  [[ "${ledger_rows:-0}" -ge 10 ]] && pass "05 Ledger ($ledger_rows rows)" || fail "05 Ledger" "rows=$ledger_rows"

  outliers=$(eval_js 'document.querySelectorAll("[class*=outlier]").length')
  [[ "${outliers:-0}" -gt 0 ]] && pass "06 Outliers ($outliers)" || fail "06 Outliers" "outliers=$outliers"

  promo=$(eval_js 'document.querySelectorAll("[class*=promo], [class*=lane-col]").length')
  [[ "${promo:-0}" -gt 0 ]] && pass "07 Promotion lanes ($promo cols)" || fail "07 Promotion lanes" "promo=$promo"

  judgment=$(eval_js 'document.querySelectorAll("[class*=judgment], [class*=split2]").length')
  [[ "${judgment:-0}" -gt 0 ]] && pass "08 Judgment calls" || fail "08 Judgment calls" "judgment=$judgment"

  sources=$(eval_js 'document.querySelectorAll("[class*=source]").length')
  [[ "${sources:-0}" -gt 0 ]] && pass "09 Sources ($sources)" || fail "09 Sources" "sources=$sources"

  tweaks=$(eval_js 'document.querySelector(".tweaks, [class*=fab], [aria-label*=tweaks]") ? 1 : 0')
  [[ "$tweaks" == "1" ]] && pass "10 Tweaks FAB present" || fail "10 Tweaks FAB" "not found"

  # Probes
  echo "" >> "$VERDICT"
  echo "## Probes" >> "$VERDICT"
  # Hover matrix cell
  cell_hover=$(eval_js '(()=>{const c=document.querySelector(".matrix .cell, .matrix-cell");if(!c)return 0;c.dispatchEvent(new MouseEvent("mouseover",{bubbles:true}));return 1;})()')
  [[ "$cell_hover" == "1" ]] && pass "Probe: hover matrix cell" || fail "Probe: hover matrix cell" "no cell"
  # Click lane chip "near"
  chip_click=$(eval_js '(()=>{const chip=[...document.querySelectorAll(".chip, [class*=chip]")].find(e=>/near/i.test(e.textContent));if(!chip)return 0;chip.click();return 1;})()')
  [[ "$chip_click" == "1" ]] && pass "Probe: click lane chip 'near'" || fail "Probe: click lane chip 'near'" "chip missing"
  # Search "eqsat"
  search_ok=$(eval_js '(()=>{const s=document.querySelector(".ledger-controls .search, .ledger input, input[placeholder*=search i]");if(!s)return 0;s.value="eqsat";s.dispatchEvent(new Event("input",{bubbles:true}));return 1;})()')
  [[ "$search_ok" == "1" ]] && pass "Probe: ledger search 'eqsat'" || fail "Probe: ledger search" "no input"

elif [[ "$KIND" == "matrix" ]]; then
  cells=$(eval_js 'document.querySelectorAll(".matrix .cell, .matrix-cell").length')
  [[ "${cells:-0}" -ge 100 ]] && pass "matrix-widget cells (n=$cells)" || fail "cells" "n=$cells"
  hover=$(eval_js '(()=>{const c=document.querySelector(".matrix .cell, .matrix-cell");if(!c)return 0;c.dispatchEvent(new MouseEvent("mouseover",{bubbles:true}));return 1;})()')
  [[ "$hover" == "1" ]] && pass "hover interaction" || fail "hover" "no cell"

elif [[ "$KIND" == "statline" ]]; then
  kpis=$(eval_js 'document.querySelectorAll(".statline, [class*=stat], [class*=kpi]").length')
  [[ "${kpis:-0}" -gt 0 ]] && pass "statline elements (n=$kpis)" || fail "statline" "n=$kpis"

elif [[ "$KIND" == "lanefilter" ]]; then
  chips=$(eval_js 'document.querySelectorAll(".chip, [class*=chip]").length')
  [[ "${chips:-0}" -gt 0 ]] && pass "lane-filter chips (n=$chips)" || fail "chips" "n=$chips"
  click=$(eval_js '(()=>{const c=document.querySelector(".chip");if(!c)return 0;c.click();return 1;})()')
  [[ "$click" == "1" ]] && pass "chip click fires" || fail "chip click" "no chip"
fi

echo "" >> "$VERDICT"
echo "## Screenshots" >> "$VERDICT"
for f in "$OUTDIR"/bp-*.png; do
  [[ -f "$f" ]] && echo "- $(basename "$f")" >> "$VERDICT"
done

log "verdict written: $VERDICT"
