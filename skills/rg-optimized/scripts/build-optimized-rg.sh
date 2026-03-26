#!/usr/bin/env bash
# Build optimized ripgrep with PCRE2 support
# Usage: ./build-optimized-rg.sh [install-path]
#
# Default install: ~/.cargo/bin/rg
# Requires: git, cargo (nightly), libpcre2-dev, pkg-config

set -euo pipefail

INSTALL_PATH="${1:-$HOME/.cargo/bin/rg}"
BUILD_DIR="/tmp/rg-build-$$"
CLEANUP=${CLEANUP:-1}  # Set CLEANUP=0 to keep build dir

info() { echo -e "\033[1;34m==>\033[0m $1"; }
success() { echo -e "\033[1;32m==>\033[0m $1"; }
error() { echo -e "\033[1;31m==>\033[0m $1" >&2; exit 1; }

cleanup() {
    if [[ "$CLEANUP" == "1" && -d "$BUILD_DIR" ]]; then
        info "Cleaning up $BUILD_DIR"
        rm -rf "$BUILD_DIR"
    fi
}
trap cleanup EXIT

# Check prerequisites
info "Checking prerequisites..."

command -v git >/dev/null 2>&1 || error "git not found"
command -v cargo >/dev/null 2>&1 || error "cargo not found"
command -v pkg-config >/dev/null 2>&1 || error "pkg-config not found (install: apt-get install pkg-config)"

# Check for PCRE2
if ! pkg-config --exists libpcre2-8 2>/dev/null; then
    error "libpcre2-dev not found. Install with:
    Ubuntu/Debian: sudo apt-get install libpcre2-dev
    Fedora/RHEL:   sudo dnf install pcre2-devel
    macOS:         brew install pcre2"
fi

# Check for nightly Rust
if ! rustc +nightly --version >/dev/null 2>&1; then
    info "Installing nightly Rust..."
    rustup install nightly
fi

RUST_VERSION=$(rustc +nightly --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
info "Using Rust nightly $RUST_VERSION"

# Clone ripgrep
info "Cloning ripgrep master branch..."
git clone --depth 1 https://github.com/BurntSushi/ripgrep.git "$BUILD_DIR"
cd "$BUILD_DIR"

# Build
info "Building with PCRE2 and LTO optimizations..."
info "  Profile: release-lto"
info "  Features: pcre2"
info "  RUSTFLAGS: -C target-cpu=native"

RUSTFLAGS="-C target-cpu=native" cargo +nightly build --profile release-lto --features pcre2

# Find binary
TARGET_DIR=$(cargo metadata --format-version 1 | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)
RG_BIN="$TARGET_DIR/release-lto/rg"

if [[ ! -f "$RG_BIN" ]]; then
    error "Build succeeded but binary not found at: $RG_BIN"
fi

# Install
info "Installing to $INSTALL_PATH..."
mkdir -p "$(dirname "$INSTALL_PATH")"

# Handle "Text file busy" error
if [[ -f "$INSTALL_PATH" ]]; then
    rm -f "$INSTALL_PATH" 2>/dev/null || {
        info "Binary in use, using temporary rename..."
        mv "$INSTALL_PATH" "${INSTALL_PATH}.old" 2>/dev/null || true
    }
fi

cp "$RG_BIN" "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"

# Verify
info "Verifying installation..."
"$INSTALL_PATH" --version

# Check PCRE2
if "$INSTALL_PATH" --version | grep -q "features:+pcre2"; then
    success "PCRE2 support verified!"
else
    error "PCRE2 support not enabled in build"
fi

# Test PCRE2 functionality
if echo '$100' | "$INSTALL_PATH" -Po '(?<=\$)\d+' | grep -q '100'; then
    success "PCRE2 lookbehind test passed!"
else
    error "PCRE2 functionality test failed"
fi

success "Optimized ripgrep installed successfully to: $INSTALL_PATH"
echo
info "Binary size: $(du -h "$INSTALL_PATH" | cut -f1)"
echo
info "Test it with: $INSTALL_PATH -P '(?<=pattern)text' file.txt"
