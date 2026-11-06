#!/usr/bin/env bash
# Fail if a removed third-party skill package comes back into this repository.
# These packages were removed from all history on 2026-11-06 and must not be republished.
# Checks tracked paths (whole path components only) and skill registries/catalog links.
# Usage: bash scripts/check-removed-packages.sh   (runs from any directory inside the repo)

set -euo pipefail

REMOVED='admin-page-for-nextjs-sites|automating-your-automations|frankentui|gh-og-share-images|installer-workmanship|path-rationalization|system-performance-remediation|testing-golden-artifacts'

cd "$(git rev-parse --show-toplevel)"
status=0

# 1. A tracked file or folder named exactly like a removed package.
paths=$(git ls-files | grep -E "(^|/)(${REMOVED})(/|$)" || true)
if [ -n "$paths" ]; then
  echo "ERROR: removed skill package files are tracked again:"
  echo "$paths" | head -20
  status=1
fi

# 2. A registry entry or catalog link that would list, fetch or install a removed package.
regs=$(git grep -n -I -E "\"(skills/)?(${REMOVED})\"[[:space:]]*:|[(/](${REMOVED})/SKILL\.md" \
  -- 'skills-state.json' 'skills-taxonomy.json' '.skill-lock.json' '*.md' 2>/dev/null || true)
if [ -n "$regs" ]; then
  echo "ERROR: removed skill packages are registered or linked again:"
  echo "$regs" | head -20
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "No removed skill packages found."
fi
exit "$status"
