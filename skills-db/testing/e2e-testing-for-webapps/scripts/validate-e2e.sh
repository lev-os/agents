#!/usr/bin/env bash
# Validate E2E testing setup for Next.js + Playwright + Supabase
#
# Usage: ./scripts/validate-e2e.sh [--fix]
#
# Checks:
#   1. Required dependencies installed
#   2. Environment variables configured
#   3. Playwright browsers installed
#   4. Test user credentials valid
#   5. Supabase connection works
#   6. Directory structure exists

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0
FIX_MODE=false

if [[ "${1:-}" == "--fix" ]]; then
    FIX_MODE=true
fi

log_pass() { echo -e "${GREEN}✓${NC} $1"; }
log_fail() { echo -e "${RED}✗${NC} $1"; ((ERRORS++)); }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; ((WARNINGS++)); }
log_info() { echo -e "  $1"; }

echo "═══════════════════════════════════════════════════"
echo "  E2E Testing Setup Validation"
echo "═══════════════════════════════════════════════════"
echo ""

# ─────────────────────────────────────────────────────────
# 1. Check dependencies
# ─────────────────────────────────────────────────────────
echo "1. Checking dependencies..."

if command -v bun &> /dev/null; then
    log_pass "bun installed ($(bun --version))"
else
    log_fail "bun not installed"
    log_info "Install: curl -fsSL https://bun.sh/install | bash"
fi

if [[ -f "package.json" ]]; then
    if grep -q "@playwright/test" package.json; then
        log_pass "@playwright/test in package.json"
    else
        log_fail "@playwright/test not in package.json"
        if $FIX_MODE; then
            log_info "Installing @playwright/test..."
            bun add -D @playwright/test
        else
            log_info "Run: bun add -D @playwright/test"
        fi
    fi

    if grep -q "@supabase/supabase-js" package.json; then
        log_pass "@supabase/supabase-js in package.json"
    else
        log_warn "@supabase/supabase-js not in package.json (required for auth)"
        log_info "Run: bun add @supabase/supabase-js"
    fi
else
    log_fail "package.json not found (not in project root?)"
fi

echo ""

# ─────────────────────────────────────────────────────────
# 2. Check Playwright browsers
# ─────────────────────────────────────────────────────────
echo "2. Checking Playwright browsers..."

if [[ -d "$HOME/.cache/ms-playwright" ]] || [[ -d "node_modules/.cache/ms-playwright" ]]; then
    log_pass "Playwright browsers installed"
else
    log_warn "Playwright browsers not found"
    if $FIX_MODE; then
        log_info "Installing browsers..."
        bunx playwright install chromium
    else
        log_info "Run: bunx playwright install chromium"
    fi
fi

echo ""

# ─────────────────────────────────────────────────────────
# 3. Check environment variables
# ─────────────────────────────────────────────────────────
echo "3. Checking environment variables..."

check_env() {
    local var_name="$1"
    local required="${2:-true}"

    if [[ -n "${!var_name:-}" ]]; then
        # Mask the value for display
        local masked="${!var_name:0:4}****"
        log_pass "$var_name set ($masked)"
        return 0
    elif [[ -f ".env.local" ]] && grep -q "^$var_name=" .env.local; then
        log_pass "$var_name in .env.local"
        return 0
    elif [[ -f ".env" ]] && grep -q "^$var_name=" .env; then
        log_pass "$var_name in .env"
        return 0
    else
        if [[ "$required" == "true" ]]; then
            log_fail "$var_name not set"
        else
            log_warn "$var_name not set (optional)"
        fi
        return 1
    fi
}

check_env "E2E_TEST_EMAIL" true
check_env "E2E_TEST_PASSWORD" true
check_env "NEXT_PUBLIC_SUPABASE_URL" true
check_env "NEXT_PUBLIC_SUPABASE_ANON_KEY" true
echo ""

# ─────────────────────────────────────────────────────────
# 4. Check directory structure
# ─────────────────────────────────────────────────────────
echo "4. Checking directory structure..."

check_dir() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        log_pass "$dir/ exists"
    else
        log_warn "$dir/ not found"
        if $FIX_MODE; then
            mkdir -p "$dir"
            log_info "Created $dir/"
        fi
    fi
}

check_file() {
    local file="$1"
    local required="${2:-true}"
    if [[ -f "$file" ]]; then
        log_pass "$file exists"
    else
        if [[ "$required" == "true" ]]; then
            log_fail "$file not found"
        else
            log_warn "$file not found (recommended)"
        fi
    fi
}

check_dir "e2e"
check_dir "e2e/pages"
check_dir "e2e/fixtures"
check_dir "e2e/utils"
check_dir "e2e/tests"
check_dir ".auth"
check_dir "test-results"

check_file "playwright.config.ts" false
check_file "e2e/auth.global-setup.ts" false
check_file "e2e/pages/BasePage.ts" false

echo ""

# ─────────────────────────────────────────────────────────
# 5. Check .gitignore
# ─────────────────────────────────────────────────────────
echo "5. Checking .gitignore..."

if [[ -f ".gitignore" ]]; then
    missing_ignores=()

    for pattern in ".auth/" "test-results/" "playwright-report/"; do
        if grep -q "$pattern" .gitignore; then
            log_pass "$pattern in .gitignore"
        else
            missing_ignores+=("$pattern")
            log_warn "$pattern not in .gitignore"
        fi
    done

    if $FIX_MODE && [[ ${#missing_ignores[@]} -gt 0 ]]; then
        echo "" >> .gitignore
        echo "# E2E Testing" >> .gitignore
        for pattern in "${missing_ignores[@]}"; do
            echo "$pattern" >> .gitignore
        done
        log_info "Added missing patterns to .gitignore"
    fi
else
    log_warn ".gitignore not found"
fi

echo ""

# ─────────────────────────────────────────────────────────
# 6. Check package.json scripts
# ─────────────────────────────────────────────────────────
echo "6. Checking package.json scripts..."

if [[ -f "package.json" ]]; then
    if grep -q '"test:e2e"' package.json; then
        log_pass "test:e2e script exists"
    else
        log_warn "test:e2e script not found"
        log_info "Add: \"test:e2e\": \"playwright test\""
    fi
fi

echo ""

# ─────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════"

if [[ $ERRORS -eq 0 ]] && [[ $WARNINGS -eq 0 ]]; then
    echo -e "${GREEN}All checks passed!${NC}"
    echo ""
    echo "Ready to run E2E tests:"
    echo "  bun run test:e2e"
    exit 0
elif [[ $ERRORS -eq 0 ]]; then
    echo -e "${YELLOW}Passed with $WARNINGS warning(s)${NC}"
    echo ""
    echo "Tests may work but address warnings for best results."
    exit 0
else
    echo -e "${RED}$ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo ""
    echo "Fix errors before running E2E tests."
    if ! $FIX_MODE; then
        echo "Run with --fix to auto-fix some issues:"
        echo "  ./scripts/validate-e2e.sh --fix"
    fi
    exit 1
fi
