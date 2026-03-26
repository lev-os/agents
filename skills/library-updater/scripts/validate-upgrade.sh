#!/usr/bin/env bash
# Validate that dependency upgrades were successful
# Exit codes: 0=success, 1=error, 2=validation failed

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_fail() { echo -e "${RED}✗${NC} $1"; }

ERRORS=0
WARNINGS=0

# Detect project type
detect_language() {
    if [[ -f "Cargo.toml" ]]; then echo "rust"
    elif [[ -f "pyproject.toml" ]] || [[ -f "requirements.txt" ]]; then echo "python"
    elif [[ -f "package.json" ]]; then echo "node"
    elif [[ -f "go.mod" ]]; then echo "go"
    elif [[ -f "Gemfile" ]]; then echo "ruby"
    else echo "unknown"
    fi
}

LANG=$(detect_language)

if [[ "$LANG" == "unknown" ]]; then
    log_fail "Could not detect project type (no manifest found)"
    exit 1
fi

log_ok "Detected language: $LANG"

# Check for UPGRADE_LOG.md
if [[ -f "UPGRADE_LOG.md" ]]; then
    log_ok "UPGRADE_LOG.md exists"
else
    log_warn "UPGRADE_LOG.md not found"
    ((WARNINGS++))
fi

# Language-specific validation
case $LANG in
    rust)
        echo "Running Rust validation..."

        # Clean build
        if cargo build 2>&1; then
            log_ok "cargo build succeeded"
        else
            log_fail "cargo build failed"
            ((ERRORS++))
        fi

        # Tests
        if cargo test 2>&1; then
            log_ok "cargo test succeeded"
        else
            log_fail "cargo test failed"
            ((ERRORS++))
        fi

        # Security audit (if available)
        if command -v cargo-audit &> /dev/null; then
            if cargo audit 2>&1; then
                log_ok "cargo audit passed"
            else
                log_warn "cargo audit found vulnerabilities"
                ((WARNINGS++))
            fi
        else
            log_warn "cargo-audit not installed, skipping"
        fi
        ;;

    python)
        echo "Running Python validation..."

        # Install deps
        if [[ -f "pyproject.toml" ]]; then
            if command -v uv &> /dev/null; then
                uv sync 2>&1 && log_ok "uv sync succeeded" || { log_fail "uv sync failed"; ((ERRORS++)); }
            elif command -v poetry &> /dev/null; then
                poetry install 2>&1 && log_ok "poetry install succeeded" || { log_fail "poetry install failed"; ((ERRORS++)); }
            fi
        fi

        # Tests
        if command -v pytest &> /dev/null; then
            if pytest 2>&1; then
                log_ok "pytest succeeded"
            else
                log_fail "pytest failed"
                ((ERRORS++))
            fi
        fi

        # Security audit
        if command -v pip-audit &> /dev/null; then
            if pip-audit 2>&1; then
                log_ok "pip-audit passed"
            else
                log_warn "pip-audit found vulnerabilities"
                ((WARNINGS++))
            fi
        fi
        ;;

    node)
        echo "Running Node.js validation..."

        # Install
        if npm install 2>&1; then
            log_ok "npm install succeeded"
        else
            log_fail "npm install failed"
            ((ERRORS++))
        fi

        # Tests
        if npm test 2>&1; then
            log_ok "npm test succeeded"
        else
            log_fail "npm test failed"
            ((ERRORS++))
        fi

        # Audit
        if npm audit 2>&1; then
            log_ok "npm audit passed"
        else
            log_warn "npm audit found vulnerabilities"
            ((WARNINGS++))
        fi
        ;;

    go)
        echo "Running Go validation..."

        # Tidy
        if go mod tidy 2>&1; then
            log_ok "go mod tidy succeeded"
        else
            log_fail "go mod tidy failed"
            ((ERRORS++))
        fi

        # Build
        if go build ./... 2>&1; then
            log_ok "go build succeeded"
        else
            log_fail "go build failed"
            ((ERRORS++))
        fi

        # Tests
        if go test ./... 2>&1; then
            log_ok "go test succeeded"
        else
            log_fail "go test failed"
            ((ERRORS++))
        fi

        # Security
        if command -v govulncheck &> /dev/null; then
            if govulncheck ./... 2>&1; then
                log_ok "govulncheck passed"
            else
                log_warn "govulncheck found vulnerabilities"
                ((WARNINGS++))
            fi
        fi
        ;;

    ruby)
        echo "Running Ruby validation..."

        # Install
        if bundle install 2>&1; then
            log_ok "bundle install succeeded"
        else
            log_fail "bundle install failed"
            ((ERRORS++))
        fi

        # Tests
        if bundle exec rspec 2>&1; then
            log_ok "rspec succeeded"
        else
            log_fail "rspec failed"
            ((ERRORS++))
        fi

        # Audit
        if command -v bundle-audit &> /dev/null; then
            if bundle audit check --update 2>&1; then
                log_ok "bundle audit passed"
            else
                log_warn "bundle audit found vulnerabilities"
                ((WARNINGS++))
            fi
        fi
        ;;
esac

echo ""
echo "================================"
if [[ $ERRORS -gt 0 ]]; then
    log_fail "Validation FAILED: $ERRORS errors, $WARNINGS warnings"
    exit 2
elif [[ $WARNINGS -gt 0 ]]; then
    log_warn "Validation PASSED with $WARNINGS warnings"
    exit 0
else
    log_ok "Validation PASSED"
    exit 0
fi
