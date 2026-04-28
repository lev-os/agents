#!/usr/bin/env bash
# build-index.sh — renders index.html from urls.json + verdict files
# urls.json schema:
#   { "variants":[{slug,title,blurb,url}], "components":[{slug,title,blurb,url}] }
set -u

DIR="$HOME/.agents/levnow/gxw-index"
QA_ROOT="$HOME/.agents/levnow/gxw-qa"
cd "$DIR"

if [[ ! -f urls.json ]]; then
  echo "error: $DIR/urls.json missing" >&2
  exit 1
fi

# Resolve JQ
if command -v jq >/dev/null 2>&1; then JQ=jq
elif [[ -x "$HOME/.claude/skills/here-now/bin/jq" ]]; then JQ="$HOME/.claude/skills/here-now/bin/jq"
else echo "need jq" >&2; exit 1; fi

mkdir -p thumbs

# copy 1440x900 thumbs from QA
copy_thumb() {
  local slug="$1"
  local src="$QA_ROOT/$slug/bp-1440x900.png"
  if [[ -f "$src" ]]; then
    cp "$src" "thumbs/${slug}.png"
    echo "ok"
  else
    echo "missing"
  fi
}

render_card() {
  local slug="$1"
  local title="$2"
  local blurb="$3"
  local url="$4"
  local kind="$5"  # variant|component
  local thumb_status
  thumb_status=$(copy_thumb "$slug")
  local thumb_html
  if [[ "$thumb_status" == "ok" ]]; then
    thumb_html="<img class=\"thumb\" src=\"./thumbs/${slug}.png\" alt=\"${title} preview\" loading=\"lazy\">"
  else
    thumb_html="<div class=\"thumb missing\">no preview</div>"
  fi
  local verdict_file="$QA_ROOT/$slug/verdict.md"
  local pass=0 fail=0
  if [[ -f "$verdict_file" ]]; then
    pass=$(grep -c '^- \[x\]' "$verdict_file" 2>/dev/null || echo 0)
    fail=$(grep -c '^- \[ \]' "$verdict_file" 2>/dev/null || echo 0)
  fi
  cat <<EOF
<a class="gallery-card" href="${url}" target="_blank" rel="noopener">
  ${thumb_html}
  <div class="body">
    <div class="eyebrow">${kind} · ${slug}</div>
    <div class="title">${title}</div>
    <div class="blurb">${blurb}</div>
    <div class="meta"><span class="pass">${pass} PASS</span>·<span class="fail">${fail} FAIL</span></div>
  </div>
</a>
EOF
}

VARIANT_CARDS=""
while IFS= read -r row; do
  slug=$(echo "$row" | "$JQ" -r '.slug')
  title=$(echo "$row" | "$JQ" -r '.title')
  blurb=$(echo "$row" | "$JQ" -r '.blurb')
  url=$(echo "$row" | "$JQ" -r '.url')
  VARIANT_CARDS+=$'\n'"$(render_card "$slug" "$title" "$blurb" "$url" "Variant")"
done < <("$JQ" -c '.variants[]' urls.json)

COMPONENT_CARDS=""
while IFS= read -r row; do
  slug=$(echo "$row" | "$JQ" -r '.slug')
  title=$(echo "$row" | "$JQ" -r '.title')
  blurb=$(echo "$row" | "$JQ" -r '.blurb')
  url=$(echo "$row" | "$JQ" -r '.url')
  COMPONENT_CARDS+=$'\n'"$(render_card "$slug" "$title" "$blurb" "$url" "Component")"
done < <("$JQ" -c '.components[]' urls.json)

# Build parity table
PARITY_ROWS=""
PARITY_HEADER='<tr><th>Deliverable</th><th>Masthead</th><th>Projections</th><th>Flows</th><th>Matrix</th><th>Ledger</th><th>Outliers</th><th>Promo</th><th>Judgment</th><th>Sources</th><th>Tweaks</th><th>Probes</th></tr>'

parity_cell() {
  local verdict="$1" pattern="$2"
  if [[ ! -f "$verdict" ]]; then
    echo '<td class="na">—</td>'; return
  fi
  if grep -q "^- \[x\].*${pattern}" "$verdict"; then
    echo '<td class="pass">PASS</td>'
  elif grep -q "^- \[ \].*${pattern}" "$verdict"; then
    echo '<td class="fail">FAIL</td>'
  else
    echo '<td class="na">—</td>'
  fi
}

add_parity_row() {
  local slug="$1" label="$2" kind="$3"
  local v="$QA_ROOT/$slug/verdict.md"
  local row="<tr><td>${label}</td>"
  if [[ "$kind" == "variant" ]]; then
    for p in '01 Masthead' '02 Projections' '03 Flow grid' '04 Matrix' '05 Ledger' '06 Outliers' '07 Promotion lanes' '08 Judgment calls' '09 Sources' '10 Tweaks FAB'; do
      row+=$(parity_cell "$v" "$p")
    done
    # Probes column — any PASS counts
    if [[ -f "$v" ]] && grep -q '^- \[x\] Probe:' "$v"; then
      row+='<td class="pass">OK</td>'
    elif [[ -f "$v" ]] && grep -q '^- \[ \] Probe:' "$v"; then
      row+='<td class="fail">FAIL</td>'
    else
      row+='<td class="na">—</td>'
    fi
  else
    # components: just show scaffolded cells + probe
    for _ in $(seq 1 10); do row+='<td class="na">—</td>'; done
    if [[ -f "$v" ]] && grep -q '^- \[x\]' "$v"; then
      row+='<td class="pass">OK</td>'
    elif [[ -f "$v" ]] && grep -q '^- \[ \]' "$v"; then
      row+='<td class="fail">FAIL</td>'
    else
      row+='<td class="na">—</td>'
    fi
  fi
  row+='</tr>'
  PARITY_ROWS+=$'\n'"$row"
}

while IFS= read -r row; do
  slug=$(echo "$row" | "$JQ" -r '.slug')
  title=$(echo "$row" | "$JQ" -r '.title')
  add_parity_row "$slug" "$title" "variant"
done < <("$JQ" -c '.variants[]' urls.json)
while IFS= read -r row; do
  slug=$(echo "$row" | "$JQ" -r '.slug')
  title=$(echo "$row" | "$JQ" -r '.title')
  add_parity_row "$slug" "$title" "component"
done < <("$JQ" -c '.components[]' urls.json)

PARITY_TABLE="<table class=\"parity-matrix\"><thead>${PARITY_HEADER}</thead><tbody>${PARITY_ROWS}</tbody></table>"

GENERATED_AT=$(date -u +"%Y-%m-%d %H:%MZ")

export VARIANT_CARDS COMPONENT_CARDS PARITY_TABLE GENERATED_AT

# Emit final index.html by substituting template vars
python3 - "$DIR/index.html.tpl" "$DIR/index.html" <<'PYEOF'
import sys, pathlib
tpl_path, out_path = sys.argv[1], sys.argv[2]
tpl = pathlib.Path(tpl_path).read_text()
import os
repl = {
    "{{VARIANT_CARDS}}": os.environ.get("VARIANT_CARDS",""),
    "{{COMPONENT_CARDS}}": os.environ.get("COMPONENT_CARDS",""),
    "{{PARITY_TABLE}}": os.environ.get("PARITY_TABLE",""),
    "{{GENERATED_AT}}": os.environ.get("GENERATED_AT",""),
}
for k,v in repl.items():
    tpl = tpl.replace(k, v)
pathlib.Path(out_path).write_text(tpl)
print(f"wrote {out_path}")
PYEOF

echo "index built at $DIR/index.html"
