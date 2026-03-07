#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jean-patricksmith/.agents/skills/work"
SKILL="$ROOT/SKILL.md"
H_TPL="$ROOT/templates/handoff.md"
T_README="$ROOT/templates/README.md"
R_README="$ROOT/README.md"

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

check_contains() {
  local file="$1"
  local pattern="$2"
  local msg="$3"
  rg -q "$pattern" "$file" || fail "$msg ($file)"
}

[[ -f "$SKILL" ]] || fail "Missing SKILL.md"
[[ -f "$H_TPL" ]] || fail "Missing templates/handoff.md"
[[ -f "$T_README" ]] || fail "Missing templates/README.md"
[[ -f "$R_README" ]] || fail "Missing README.md"

PATTERN='\{YYYYMMDD\}-\{workstream\}-\{component\}-\{slug\}-session-\{N\}'
check_contains "$SKILL" "$PATTERN" "SKILL naming contract missing"
check_contains "$H_TPL" "$PATTERN" "handoff template naming contract missing"
check_contains "$T_README" "$PATTERN" "template README naming contract missing"
check_contains "$R_README" "$PATTERN" "README naming contract missing"

for section in "## You Are Here" "## Next Agent Brief" "## Timeline" "## Decisions Log" "## Open Questions" "## Entity Matrix"; do
  check_contains "$H_TPL" "${section//\//\\/}" "Missing required handoff section: $section"
done

# no phantom plan template references (allow explicit non-existence note)
ALLOW_MSG="There is no.*plan\.md.*template"
for file in "$SKILL" "$R_README" "$T_README" "$ROOT/templates/proposal.md" "$ROOT/templates/report.md"; do
  if rg -q "plan\.md" "$file"; then
    rg -q "$ALLOW_MSG" "$file" || fail "Unexpected plan.md reference ($file)"
  fi
done

for bad in "skill://planning" "skill://lev-test" "lev-clwd" "lev-lifecycle"; do
  if rg -q "$bad" "$SKILL" "$R_README" "$ROOT/templates"; then
    fail "Found disallowed reference: $bad"
  fi
done

check_contains "$SKILL" "process/workflow" "SKILL must declare process/workflow mode"

echo "[OK] work contract lint passed"
