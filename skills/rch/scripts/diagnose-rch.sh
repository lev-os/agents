#!/usr/bin/env bash
# RCH Diagnostic Script
# Run: ./diagnose-rch.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo "═══════════════════════════════════════"
echo "       RCH Diagnostic Report"
echo "═══════════════════════════════════════"
echo

# 1. Daemon status
echo "1. Daemon Status"
echo "────────────────"
if rch daemon status --json 2>/dev/null | grep -q '"running": true'; then
    socket=$(rch daemon status --json 2>/dev/null | grep -o '"socket_path": "[^"]*"' | cut -d'"' -f4)
    pass "Daemon running at $socket"
else
    fail "Daemon NOT running"
    echo "   Fix: rch daemon start"
fi
echo

# 2. Socket path check
echo "2. Socket Path Consistency"
echo "──────────────────────────"
config_socket=$(grep socket_path ~/.config/rch/config.toml 2>/dev/null | cut -d'"' -f2 || echo "not set")
daemon_socket=$(rch daemon status --json 2>/dev/null | grep -o '"socket_path": "[^"]*"' | cut -d'"' -f4 || echo "unknown")

if [[ "$config_socket" == "$daemon_socket" ]]; then
    pass "Config and daemon socket match: $config_socket"
else
    fail "Socket mismatch!"
    echo "   Config: $config_socket"
    echo "   Daemon: $daemon_socket"
    echo "   Fix: Update ~/.config/rch/config.toml socket_path"
fi
echo

# 3. Output visibility
echo "3. Output Visibility"
echo "────────────────────"
visibility=$(grep -E "^visibility" ~/.config/rch/config.toml 2>/dev/null | cut -d'"' -f2 || echo "default")
if [[ "$visibility" == "none" ]]; then
    warn "Visibility set to 'none' - status commands will be silent"
    echo "   Fix: Set visibility = \"normal\" in config"
else
    pass "Visibility: $visibility"
fi
echo

# 4. Workers
echo "4. Worker Status"
echo "────────────────"
worker_count=$(rch workers list 2>/dev/null | grep -c "●" || echo "0")
echo "Configured workers: $worker_count"

if [[ "$worker_count" -gt 0 ]]; then
    echo
    echo "Probing workers..."
    rch workers probe --all 2>&1 | grep -E "^  |✓|✗" || true
fi
echo

# 5. Hook installation
echo "5. Claude Code Hook"
echo "───────────────────"
if grep -q "PreToolUse" ~/.claude/settings.json 2>/dev/null && \
   grep -q "/usr/local/bin/rch" ~/.claude/settings.json 2>/dev/null; then
    pass "Hook installed in Claude Code settings"
else
    fail "Hook NOT installed"
    echo "   Fix: rch hook install"
fi
echo

# 6. Test hook
echo "6. Hook Test"
echo "────────────"
echo "Testing hook with cargo build simulation..."
result=$(echo '{"tool_name":"Bash","tool_input":{"command":"cargo check --version"}}' | /usr/local/bin/rch 2>&1 || true)

if echo "$result" | grep -q "Remote compilation succeeded\|permissionDecision.*deny"; then
    pass "Hook intercepted and executed remotely"
elif echo "$result" | grep -q "rustup: not found\|cargo: not found"; then
    fail "Worker missing Rust toolchain"
    worker=$(echo "$result" | grep -o "Selected worker: [^ ]*" | cut -d: -f2 | tr -d ' ')
    echo "   Affected worker: $worker"
    echo "   Fix: Install Rust on worker or disable it"
elif echo "$result" | grep -q "falling back to local"; then
    warn "Hook fell back to local execution"
    echo "   Check logs above for reason"
else
    warn "Unexpected result - check manually"
fi
echo

echo "═══════════════════════════════════════"
echo "         Diagnosis Complete"
echo "═══════════════════════════════════════"
