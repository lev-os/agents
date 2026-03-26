#!/bin/bash
#
# Validate xf Installation — Quick health check
#
# Usage:
#     ./validate.sh
#
# Returns:
#     0 = All checks pass
#     1 = Some checks failed

set -e

echo "Validating xf installation..."
echo ""

ERRORS=0

# 1. Check xf exists
echo -n "1. xf command exists: "
if command -v xf &> /dev/null; then
    echo "✓"
else
    echo "✗ (xf not found in PATH)"
    ERRORS=$((ERRORS + 1))
fi

# 2. Check jq exists
echo -n "2. jq command exists: "
if command -v jq &> /dev/null; then
    echo "✓"
else
    echo "✗ (jq not found - install with: apt install jq)"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check xf doctor
echo -n "3. xf doctor passes: "
if xf doctor &> /dev/null; then
    echo "✓"
else
    echo "✗ (run 'xf doctor' for details)"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check xf stats works
echo -n "4. xf stats accessible: "
if xf stats --format json &> /dev/null; then
    echo "✓"
else
    echo "✗ (archive may not be indexed)"
    ERRORS=$((ERRORS + 1))
fi

# 5. Check search works
echo -n "5. xf search works: "
if xf search "test" --format json --limit 1 &> /dev/null; then
    echo "✓"
else
    echo "✗ (search failed)"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "All checks passed! ✓"
    exit 0
else
    echo "$ERRORS check(s) failed. ✗"
    exit 1
fi
