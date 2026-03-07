#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jean-patricksmith/.agents/skills/work"
SKILL="$ROOT/SKILL.md"
H_TPL="$ROOT/templates/handoff.md"
TEMPLATES=(
  "$ROOT/templates/report.md"
  "$ROOT/templates/proposal.md"
  "$ROOT/templates/design.md"
  "$ROOT/templates/spec.md"
  "$ROOT/templates/plan.md"
  "$ROOT/templates/handoff.md"
  "$ROOT/templates/decision.md"
  "$ROOT/templates/validation-report.md"
)

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
for file in "${TEMPLATES[@]}"; do
  [[ -f "$file" ]] || fail "Missing template ($file)"
done

[[ ! -f "$ROOT/README.md" ]] || fail "Legacy README.md should not exist"
[[ ! -f "$ROOT/templates/README.md" ]] || fail "Legacy templates/README.md should not exist"
[[ ! -f "$ROOT/templates/chore.md" ]] || fail "Legacy chore.md should not exist"

PATTERN='\{YYYYMMDD\}-\{workstream\}-\{component\}-\{slug\}-session-\{N\}'
check_contains "$SKILL" "$PATTERN" "SKILL naming contract missing"
check_contains "$H_TPL" "$PATTERN" "handoff template naming contract missing"

for section in "## You Are Here" "## Next Agent Brief" "## Roadmap To Goal" "## Timeline" "## Decisions Log" "## Open Questions" "## Entity Matrix" "## Meta" "### Active Blockers" "### Risks" "### What Worked" "### What Didn't Work" "### Context For Next Session" "#### Mental Model" "#### Quick Start Commands" "#### Configuration State"; do
  check_contains "$H_TPL" "${section//\//\\/}" "Missing required handoff section: $section"
done

check_contains "$H_TPL" "Sharding Signals" "handoff sharding section missing"
check_contains "$H_TPL" "Decision Promotion Rule" "handoff decision promotion section missing"

for file in "${TEMPLATES[@]}"; do
  check_contains "$file" "^## How To Fill This Out" "Template missing How To Fill This Out section"
done

for pattern in "\.lev/pm/reports/" "\.lev/pm/proposals/" "\.lev/pm/designs/" "\.lev/pm/specs/" "\.lev/pm/plans/" "\.lev/pm/handoffs/" "\.lev/pm/decisions/" "\.lev/pm/validation-reports/" "\.lev/scratch/"; do
  check_contains "$SKILL" "$pattern" "Missing canonical path contract: $pattern"
done

for bad in "lev-lifecycle" "templates/README.md" "README.md" "templates/chore.md"; do
  if rg -q "$bad" "$SKILL" "$ROOT/templates"; then
    fail "Found disallowed legacy reference: $bad"
  fi
done

echo "[OK] work contract lint passed"
