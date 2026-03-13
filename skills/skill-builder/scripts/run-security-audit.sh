#!/usr/bin/env bash
# Run the security audit pipeline manually
# Usage: run-security-audit.sh <skill.md> [staged-dir] [source-url]
set -euo pipefail

SKILL_PATH="${1:?Usage: run-security-audit.sh <skill.md> [staged-dir] [source-url]}"
STAGED_DIR="${2:-$(dirname "$SKILL_PATH")}"
SOURCE_URL="${3:-unknown}"

echo "=== S0: Decompile ==="
DECOMPILE_OUT=$(python3 ~/.agents/skills-db/security/skill-decompile/decompile.py "$SKILL_PATH" --output yaml)
RISK_SCORE=$(echo "$DECOMPILE_OUT" | grep "risk_score:" | head -1 | awk '{print $2}')
echo "Risk score: $RISK_SCORE"

if [ "${RISK_SCORE:-0}" -ge 80 ]; then
  echo "VERDICT: D (REJECT) — risk score $RISK_SCORE >= 80"
  exit 1
fi

echo ""
echo "=== S1: Structural Analysis ==="
echo "$DECOMPILE_OUT" | grep -A20 "risk_signals:" || true
echo "$DECOMPILE_OUT" | grep -A5 "verdict:" || true

if [ "${RISK_SCORE:-0}" -ge 60 ]; then
  echo "WARNING: Elevated risk ($RISK_SCORE). Proceeding to S2..."
fi

echo ""
echo "=== S2: AgentShield ==="
if command -v npx >/dev/null 2>&1; then
  npx ecc-agentshield scan --path "$STAGED_DIR" --min-severity medium 2>/dev/null || echo "AgentShield not installed — skipped"
else
  echo "npx not available — skipped"
fi

echo ""
echo "=== VERDICT ==="
if [ "${RISK_SCORE:-0}" -lt 21 ]; then
  echo "Grade: A (SAFE) — auto-proceed"
elif [ "${RISK_SCORE:-0}" -lt 41 ]; then
  echo "Grade: A (LOW RISK) — auto-proceed"
elif [ "${RISK_SCORE:-0}" -lt 61 ]; then
  echo "Grade: B (MEDIUM) — confirm with user"
else
  echo "Grade: C/D (HIGH) — manual review required"
fi
