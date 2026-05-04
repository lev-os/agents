#!/usr/bin/env bash
# QA matrix: render variant-audit.json against every theme.
# Run from repo root or anywhere; paths are absolute.
set -euo pipefail

LEV_NOW="${HOME}/lev/plugins/now/src/cli.ts"
SPEC="${HOME}/.agents/levnow/variant-audit.json"
OUT_DIR="${HOME}/.agents/levnow/qa"

THEMES=(deep-blue-gold teal-slate midnight-ink terracotta-sage rose-cranberry amber-emerald obsidian-monolith)

mkdir -p "${OUT_DIR}"

cd "${HOME}/lev"
for theme in "${THEMES[@]}"; do
  TMP="$(mktemp -t variant-audit-${theme}.XXXX.json)"
  jq --arg t "${theme}" '.theme.preset = $t | .meta.title = "Variant audit · " + $t' "${SPEC}" > "${TMP}"
  npx tsx "${LEV_NOW}" "${TMP}" --output "${OUT_DIR}/variant-audit-${theme}.html"
  rm -f "${TMP}"
done

# Build a static index that links into all 7
cat > "${OUT_DIR}/index.html" <<'EOF'
<!doctype html>
<html><head>
<meta charset="utf-8"><title>lev-now QA matrix</title>
<style>
  body{font:14px/1.5 system-ui,sans-serif;background:#0b1326;color:#dae2fd;padding:32px;max-width:720px;margin:0 auto}
  h1{font-size:22px;margin:0 0 8px;letter-spacing:-0.02em}
  p{color:#8b95b4;margin:0 0 24px}
  ul{list-style:none;padding:0;margin:0;display:grid;gap:8px}
  a{display:block;padding:14px 18px;border-radius:8px;background:#171f33;color:#dae2fd;text-decoration:none;border:1px solid rgba(87,241,219,0.16);transition:all 0.15s}
  a:hover{border-color:#57f1db;color:#57f1db}
  code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;color:#8b95b4;display:block;margin-top:4px}
</style>
</head><body>
<h1>lev-now QA matrix</h1>
<p>Same variant-audit spec rendered against every theme preset. Use this to spot drift, broken padding, or AI-slop accents that creep in across themes.</p>
<ul>
EOF

for theme in "${THEMES[@]}"; do
  echo "  <li><a href=\"variant-audit-${theme}.html\">${theme}<code>./variant-audit-${theme}.html</code></a></li>" >> "${OUT_DIR}/index.html"
done

cat >> "${OUT_DIR}/index.html" <<'EOF'
</ul>
</body></html>
EOF

echo ""
echo "QA matrix → ${OUT_DIR}/index.html"
ls -la "${OUT_DIR}/"
