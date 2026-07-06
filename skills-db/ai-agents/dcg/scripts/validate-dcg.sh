#!/usr/bin/env bash
# Validate DCG installation and configuration

set -e

echo "=== DCG Installation Validation ==="

# Check if dcg is installed
if ! command -v dcg &> /dev/null; then
    echo "ERROR: dcg not found in PATH"
    echo "Install from: https://github.com/anthropics/destructive-command-guard"
    exit 1
fi

echo "✓ dcg binary found: $(which dcg)"

# Check version
echo "✓ Version: $(dcg --version 2>/dev/null || echo 'unknown')"

# Check if hook is installed
if dcg doctor &> /dev/null; then
    echo "✓ Hook installed correctly"
else
    echo "⚠ Hook may not be installed. Run: dcg install"
fi

# Test pattern detection
echo ""
echo "=== Pattern Detection Tests ==="

test_command() {
    local cmd="$1"
    local expected="$2"
    local result

    if dcg test "$cmd" &> /dev/null; then
        result="allow"
    else
        result="block"
    fi

    if [ "$result" = "$expected" ]; then
        echo "✓ '$cmd' → $result (expected)"
    else
        echo "✗ '$cmd' → $result (expected: $expected)"
        return 1
    fi
}

# Commands that SHOULD be blocked
test_command "rm -rf /" "block"
test_command "git reset --hard HEAD" "block"
test_command "DROP DATABASE production" "block"

# Commands that SHOULD be allowed
test_command "git status" "allow"
test_command "rm -rf ./build" "allow"
test_command "ls -la" "allow"

echo ""
echo "=== Configuration ==="

# Check for project config
if [ -f ".dcg.toml" ]; then
    echo "✓ Project config found: .dcg.toml"
else
    echo "○ No project config (.dcg.toml)"
fi

# Check for allowlist
if [ -f ".dcg/allowlist.toml" ]; then
    echo "✓ Allowlist found: .dcg/allowlist.toml"
else
    echo "○ No allowlist (.dcg/allowlist.toml)"
fi

echo ""
echo "=== Validation Complete ==="
