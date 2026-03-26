#!/usr/bin/env bash
# Validate an optimized ripgrep build
# Usage: ./validate-rg-build.sh [path-to-rg]

set -euo pipefail

RG="${1:-$(which rg)}"
PASS=0
FAIL=0

info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
pass() { echo -e "\033[1;32m[PASS]\033[0m $1"; ((PASS++)) || true; }
fail() { echo -e "\033[1;31m[FAIL]\033[0m $1"; ((FAIL++)) || true; }
warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }

info "Validating: $RG"
echo

# 1. Check binary exists
if [[ -x "$RG" ]]; then
    pass "Binary exists and is executable"
else
    fail "Binary not found or not executable: $RG"
    exit 1
fi

# 2. Get version info
VERSION_OUTPUT=$("$RG" --version 2>&1)
echo "$VERSION_OUTPUT"
echo

# 3. Check PCRE2 support
if echo "$VERSION_OUTPUT" | grep -qF "features:+pcre2"; then
    pass "PCRE2 support enabled (+pcre2)"
else
    fail "PCRE2 support missing (-pcre2 or not shown)"
fi

# 4. Check PCRE2 availability
if echo "$VERSION_OUTPUT" | grep -q "PCRE2.*is available"; then
    pass "PCRE2 library linked and available"
    if echo "$VERSION_OUTPUT" | grep -q "JIT is available"; then
        pass "PCRE2 JIT compilation available"
    else
        warn "PCRE2 JIT not available (performance may be reduced)"
    fi
else
    fail "PCRE2 library not available"
fi

# 5. Check SIMD features
if echo "$VERSION_OUTPUT" | grep -q "simd(compile):.*AVX2"; then
    pass "AVX2 SIMD compiled in"
elif echo "$VERSION_OUTPUT" | grep -q "simd(compile):.*SSE"; then
    warn "Only SSE SIMD (not AVX2) - consider native build"
else
    warn "No SIMD features detected"
fi

# 6. Test PCRE2 actually works
TEST_PATTERN='(?<=\$)\d+'
TEST_INPUT='Price is $100 dollars'
EXPECTED='100'

if RESULT=$("$RG" -Po "$TEST_PATTERN" <<< "$TEST_INPUT" 2>&1); then
    if [[ "$RESULT" == "$EXPECTED" ]]; then
        pass "PCRE2 lookbehind works correctly"
    else
        fail "PCRE2 lookbehind returned unexpected result: $RESULT"
    fi
else
    fail "PCRE2 pattern failed: $RESULT"
fi

# 7. Test Unicode support
UNICODE_PATTERN='[\x{2014}]'
UNICODE_INPUT='Test—dash'  # em-dash

if "$RG" -Po "$UNICODE_PATTERN" <<< "$UNICODE_INPUT" >/dev/null 2>&1; then
    pass "PCRE2 Unicode escape works"
else
    fail "PCRE2 Unicode escape failed"
fi

# 8. Check binary size (release-lto should be ~4MB)
SIZE=$(stat -f%z "$RG" 2>/dev/null || stat --printf="%s" "$RG" 2>/dev/null)
SIZE_MB=$(echo "scale=1; $SIZE / 1048576" | bc)
info "Binary size: ${SIZE_MB}MB"
if (( $(echo "$SIZE_MB < 6" | bc -l) )); then
    pass "Binary size optimal (<6MB, likely LTO build)"
elif (( $(echo "$SIZE_MB < 10" | bc -l) )); then
    warn "Binary size moderate (6-10MB, possibly release without LTO)"
else
    warn "Binary size large (>10MB, possibly debug build)"
fi

# Summary
echo
echo "================================"
echo "Validation Summary"
echo "================================"
echo -e "\033[1;32mPassed:\033[0m $PASS"
echo -e "\033[1;31mFailed:\033[0m $FAIL"
echo

if [[ $FAIL -eq 0 ]]; then
    echo -e "\033[1;32m✓ Optimized ripgrep build validated successfully!\033[0m"
    exit 0
else
    echo -e "\033[1;31m✗ Build validation found issues.\033[0m"
    exit 1
fi
