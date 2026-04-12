# Download & Verification Patterns

Resilient binary acquisition, verification, and proxy support patterns from production installers.

---

## Curl One-Liner Header Format (Required)

Every installer starts with a header comment documenting the curl one-liner:

```bash
#!/usr/bin/env bash
#
# project-name installer
#
# One-liner install (with cache buster):
#   curl -fsSL "https://raw.githubusercontent.com/OWNER/REPO/master/install.sh?$(date +%s)" | bash
#
# Or without cache buster:
#   curl -fsSL https://raw.githubusercontent.com/OWNER/REPO/master/install.sh | bash
#
# Options:
#   --version vX.Y.Z   Install specific version (default: latest)
#   --dest DIR         Install to DIR (default: ~/.local/bin)
#   --system           Install to /usr/local/bin (requires sudo)
#   --easy-mode        Auto-update PATH in shell rc files
#   --verify           Run self-test after install
#   --from-source      Build from source instead of downloading binary
#   --quiet            Suppress non-error output
#   --no-gum           Disable gum formatting even if available
#   --no-configure     Skip AI agent hook configuration
#   --no-verify        Skip checksum + signature verification
#   --offline          Skip network preflight checks
#   --force            Reinstall even if same version exists
#
```

The `?$(date +%s)` cache buster prevents CDN/proxy caching of stale versions.

---

## Proxy Support (PROXY_ARGS Array Pattern)

```bash
setup_proxy() {
  PROXY_ARGS=()
  if [[ -n "${HTTPS_PROXY:-}" ]]; then
    PROXY_ARGS=(--proxy "$HTTPS_PROXY")
    info "Using HTTPS proxy: $HTTPS_PROXY"
  elif [[ -n "${HTTP_PROXY:-}" ]]; then
    PROXY_ARGS=(--proxy "$HTTP_PROXY")
    info "Using HTTP proxy: $HTTP_PROXY"
  fi
  # NO_PROXY is honored natively by curl — no need to handle it
}
```

Pass to EVERY `curl` call:
```bash
curl -fsSL "${PROXY_ARGS[@]}" "$URL" -o "$TMP/$FILE"
```

**Why a bash array?** `"${PROXY_ARGS[@]}"` expands to nothing when empty — no conditional curl construction needed.

**Priority:** HTTPS_PROXY > HTTP_PROXY (always prefer HTTPS).

---

## 4-Tier Download Fallback Chain

```bash
download_and_install() {
  local version="$VERSION"
  local target="$TARGET"

  # Tier 1: Versioned artifact from specific tag
  local versioned_url="https://github.com/${OWNER}/${REPO}/releases/download/v${version}/${REPO}-v${version}-${target}.tar.gz"
  if curl -fsSL "${PROXY_ARGS[@]}" "$versioned_url" -o "$TMP/artifact.tar.gz" 2>/dev/null; then
    extract_and_install "$TMP/artifact.tar.gz"
    return 0
  fi

  # Tier 2: Unversioned asset from latest release
  local latest_url="https://github.com/${OWNER}/${REPO}/releases/latest/download/${REPO}-${target}.tar.gz"
  if curl -fsSL "${PROXY_ARGS[@]}" "$latest_url" -o "$TMP/artifact.tar.gz" 2>/dev/null; then
    extract_and_install "$TMP/artifact.tar.gz"
    return 0
  fi

  # Tier 3: Platform-simple naming (linux-x86_64 instead of target triple)
  local simple_url="https://github.com/${OWNER}/${REPO}/releases/latest/download/${REPO}-${OS}-${ARCH}.tar.gz"
  if curl -fsSL "${PROXY_ARGS[@]}" "$simple_url" -o "$TMP/artifact.tar.gz" 2>/dev/null; then
    extract_and_install "$TMP/artifact.tar.gz"
    return 0
  fi

  # Tier 4: Build from source
  warn "No prebuilt binary found; building from source..."
  rm -rf "$TMP"  # Clean before fallback to prevent leaks
  build_from_source
}
```

**Critical:** `rm -rf "$TMP"` before every fallback to source — prevents temp directory leaks.

---

## Dual Checksum Tool Support

```bash
verify_checksum() {
  local file="$1"
  local expected="$2"

  local actual
  if command -v sha256sum >/dev/null 2>&1; then
    actual=$(sha256sum "$file" | cut -d' ' -f1)
  elif command -v shasum >/dev/null 2>&1; then
    actual=$(shasum -a 256 "$file" | cut -d' ' -f1)
  else
    warn "No SHA256 tool found; skipping checksum verification"
    return 0
  fi

  if [ "$actual" != "$expected" ]; then
    err "Checksum mismatch!"
    err "  Expected: $expected"
    err "  Got:      $actual"
    return 1
  fi
  ok "SHA256 checksum verified"
}
```

**Linux** has `sha256sum`. **macOS** has `shasum -a 256`. Always check both.

---

## Sigstore Verification (Asymmetric Failure)

```bash
verify_sigstore() {
  local file="$1"
  local bundle_url="$2"

  # No cosign → soft skip (don't punish users who lack the tool)
  if ! command -v cosign >/dev/null 2>&1; then
    warn "cosign not found; skipping Sigstore verification"
    return 0
  fi

  # Download bundle
  local bundle_file="$TMP/sigstore.json"
  if ! curl -fsSL "${PROXY_ARGS[@]}" "$bundle_url" -o "$bundle_file" 2>/dev/null; then
    warn "Could not download Sigstore bundle; skipping verification"
    return 0
  fi

  # Verify — HARD FAIL if cosign is present and verification fails
  if cosign verify-blob --bundle "$bundle_file" \
      --certificate-identity-regexp "$COSIGN_IDENTITY_RE" \
      --certificate-oidc-issuer "$COSIGN_OIDC_ISSUER" \
      "$file" 2>/dev/null; then
    ok "Sigstore signature verified"
  else
    err "Sigstore verification FAILED"
    return 1  # Hard failure — cosign IS present, signature is bad
  fi
}
```

**Key principle:** Missing cosign = soft warning (return 0). Failed verification with cosign present = hard error (return 1).

**Cosign identity variables:**
```bash
COSIGN_IDENTITY_RE="${COSIGN_IDENTITY_RE:-^https://github.com/${OWNER}/${REPO}/.github/workflows/.*$}"
COSIGN_OIDC_ISSUER="${COSIGN_OIDC_ISSUER:-https://token.actions.githubusercontent.com}"
```

---

## Offline / Airgap Mode

```bash
# Flag handling
OFFLINE_TARBALL="${OFFLINE_TARBALL:-}"

# In install_binaries():
if [[ -n "$OFFLINE_TARBALL" ]]; then
  install_from_tarball "$OFFLINE_TARBALL"
  return
fi

install_from_tarball() {
  local tarball="$1"
  [[ -f "$tarball" ]] || { err "Tarball not found: $tarball"; return 1; }
  tar -xf "$tarball" -C "$TMP"
  # Find binary, install with: install -m 0755
}
```

Airgap users pre-download the tarball, then: `bash install.sh --offline /path/to/artifact.tar.gz`

---

## Version Resolution (5-Tier Cascade)

```bash
resolve_version() {
  # 1. CLI flag / environment variable
  [[ -n "$VERSION" ]] && return 0

  # 2. Cargo.toml workspace (for in-repo installs)
  if [[ -f "Cargo.toml" ]]; then
    VERSION=$(awk '
      /^\[workspace\.package\]/ { in_section=1; next }
      /^\[/ { in_section=0 }
      in_section && /^version[[:space:]]*=/ {
        gsub(/^version[[:space:]]*=[[:space:]]*"/, "")
        gsub(/".*$/, "")
        print; exit
      }
    ' Cargo.toml)
    [[ -n "$VERSION" ]] && return 0
  fi

  # 3. GitHub API (with timeout)
  VERSION=$(curl -fsSL --connect-timeout 5 "${PROXY_ARGS[@]}" \
    "https://api.github.com/repos/${OWNER}/${REPO}/releases/latest" 2>/dev/null \
    | grep '"tag_name":' | sed -E 's/.*"v?([^"]+)".*/\1/')
  [[ -n "$VERSION" ]] && return 0

  # 4. Redirect URL parsing (fallback when API rate-limited)
  VERSION=$(curl -fsSL -o /dev/null -w '%{url_effective}' "${PROXY_ARGS[@]}" \
    "https://github.com/${OWNER}/${REPO}/releases/latest" 2>/dev/null \
    | sed -E 's|.*/tag/v?||')
  [[ -n "$VERSION" ]] && return 0

  # 5. Hardcoded installer version (last resort)
  VERSION="$INSTALLER_VERSION"
}
```

---

## Extract and Install Pattern

```bash
extract_and_install() {
  local archive="$1"

  # Detect archive type and extract
  case "$archive" in
    *.tar.gz|*.tgz) tar -xzf "$archive" -C "$TMP" ;;
    *.tar.xz)       tar -xJf "$archive" -C "$TMP" ;;
    *.zip)          unzip -q "$archive" -d "$TMP" ;;
  esac

  # Find the binary (may be nested in directories)
  local binary
  binary=$(find "$TMP" -name "$BINARY_NAME" -type f | head -1)
  [[ -n "$binary" ]] || { err "Binary not found in archive"; return 1; }

  # Atomic install with correct permissions
  install -m 0755 "$binary" "$DEST/$BINARY_NAME"
  ok "Installed $BINARY_NAME to $DEST"
}
```

**Always use `install -m 0755`** for binary deployment — atomic copy-and-chmod.

---

## Build from Source Fallback

```bash
build_from_source() {
  # Ensure Rust nightly
  if ! command -v cargo >/dev/null 2>&1; then
    info "Installing Rust via rustup..."
    curl --proto '=https' --tlsv1.2 -sSf "${PROXY_ARGS[@]}" https://sh.rustup.rs \
      | sh -s -- -y --default-toolchain nightly
    [[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"
  fi

  local src_dir="$TMP/src"
  run_with_spinner "Cloning repository..." \
    git clone --depth 1 "https://github.com/${OWNER}/${REPO}.git" "$src_dir"

  run_with_spinner "Building from source (this takes a few minutes)..." \
    cargo build --release --manifest-path "$src_dir/Cargo.toml"

  install -m 0755 "$src_dir/target/release/$BINARY_NAME" "$DEST/$BINARY_NAME"
  ok "Built and installed from source"
}
```

**`--proto '=https' --tlsv1.2`** on rustup download enforces TLS security.
**`source "$HOME/.cargo/env"`** makes cargo available in the current session.

---

## WSL Detection

```bash
if [[ "$OS" == "linux" ]] && grep -qi microsoft /proc/version 2>/dev/null; then
  warn "WSL detected. Some features may need additional configuration"
  # Continue with linux platform — don't block
fi
```

WSL is detected but NOT blocked. It runs as `linux` with optional warnings.
