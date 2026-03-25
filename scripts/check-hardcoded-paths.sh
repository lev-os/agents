#!/usr/bin/env bash
# Fail if staged files contain hardcoded Unix home paths (e.g. /Users/username, /home/user).
# Use $HOME or relative paths instead.

set -e

PATTERN='/Users/[a-zA-Z0-9_.-]+|/home/[a-zA-Z0-9_.-]+'
FILES=$(git diff --cached --name-only 2>/dev/null || true)

if [ -z "$FILES" ]; then
  exit 0
fi

OFFENDERS=$(echo "$FILES" | xargs grep -l -E "$PATTERN" 2>/dev/null || true)
if [ -n "$OFFENDERS" ]; then
  echo "ERROR: Hardcoded home paths found. Use \$HOME or relative paths instead."
  echo ""
  echo "Offending files:"
  echo "$OFFENDERS" | xargs grep -n -E "$PATTERN" 2>/dev/null || true
  exit 1
fi

exit 0
