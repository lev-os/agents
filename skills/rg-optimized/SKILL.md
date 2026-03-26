---
name: rg-optimized
description: >-
  Build ripgrep (rg) from source with PCRE2 and max optimizations. Use when
  "PCRE2 is not available", rg -P fails, need lookahead/lookbehind, or building
  optimized rg from master.
---

# rg-optimized — ripgrep Build Guide

> **Why:** Stock ripgrep lacks PCRE2. Build from master with all features for `-P` regex support, lookahead/lookbehind, and native CPU optimizations.

## Quick Build (Copy-Paste)

```bash
# 1. Install PCRE2 dev libs
sudo apt-get update && sudo apt-get install -y libpcre2-dev pkg-config

# 2. Clone and build
git clone --depth 1 https://github.com/BurntSushi/ripgrep.git /tmp/rg-build
cd /tmp/rg-build
RUSTFLAGS="-C target-cpu=native" cargo +nightly build --profile release-lto --features pcre2

# 3. Find and install
RG_BIN=$(cargo metadata --format-version 1 | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release-lto/rg
cp "$RG_BIN" ~/.cargo/bin/rg

# 4. Verify
rg --version  # Should show: features:+pcre2
```

---

## Decision Tree

```
rg -P pattern fails?
├─ "PCRE2 is not available" → BUILD (this skill)
├─ Pattern syntax error → Check PCRE2 syntax (not Rust regex)
└─ Works fine → No action needed

Need lookahead/lookbehind?
├─ Yes → Need PCRE2 build
└─ No → Stock rg is fine

Want maximum performance?
├─ Native CPU optimizations → Use release-lto + target-cpu=native
└─ Portable binary → Skip target-cpu=native
```

---

## Build Options Matrix

| Option | Flag | Effect |
|--------|------|--------|
| PCRE2 support | `--features pcre2` | Enables `-P` flag for PCRE2 regex |
| Fat LTO | `--profile release-lto` | Smaller binary, faster execution |
| Native SIMD | `RUSTFLAGS="-C target-cpu=native"` | AVX2/SSE optimizations for your CPU |
| Nightly Rust | `+nightly` | Required for Edition 2024 |

### Profiles (from Cargo.toml)

```toml
[profile.release-lto]
inherits = "release"
opt-level = 3
debug = "none"
strip = "symbols"
debug-assertions = false
overflow-checks = false
lto = "fat"
panic = "abort"
incremental = false
codegen-units = 1
```

---

## Prerequisites

### System Dependencies

| OS | Command |
|----|---------|
| Ubuntu/Debian | `sudo apt-get install -y libpcre2-dev pkg-config` |
| Fedora/RHEL | `sudo dnf install -y pcre2-devel pkg-config` |
| macOS | `brew install pcre2 pkg-config` |
| Arch | `sudo pacman -S pcre2 pkgconf` |

### Rust Toolchain

```bash
# Ensure nightly is installed
rustup install nightly
rustup update nightly

# Verify
rustc +nightly --version  # Should be 1.85+
```

---

## Target Directory Discovery

ripgrep may use a custom target directory (e.g., `/tmp/cargo-target` for remote compilation). Always discover it:

```bash
cd /path/to/ripgrep-source
TARGET_DIR=$(cargo metadata --format-version 1 | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)
echo "Binary at: $TARGET_DIR/release-lto/rg"
```

---

## Installation Locations

| Location | When |
|----------|------|
| `~/.cargo/bin/rg` | User install (recommended) |
| `/usr/local/bin/rg` | System-wide |
| Project-local | Testing before install |

### Install Command

```bash
# Replace existing (may need to rm first if "Text file busy")
rm -f ~/.cargo/bin/rg
cp "$TARGET_DIR/release-lto/rg" ~/.cargo/bin/rg
chmod +x ~/.cargo/bin/rg
```

---

## Verification

```bash
rg --version
```

**Expected output:**
```
ripgrep 15.1.0 (rev XXXXXXXX)

features:+pcre2
simd(compile):+SSE2,+SSSE3,+AVX2
simd(runtime):+SSE2,+SSSE3,+AVX2

PCRE2 10.XX is available (JIT is available)
```

**Key indicators:**
- `features:+pcre2` — PCRE2 enabled
- `simd(compile):+SSE2,+SSSE3,+AVX2` — Native optimizations
- `PCRE2 X.XX is available (JIT is available)` — Full PCRE2 with JIT

---

## PCRE2 Usage Examples

```bash
# Lookahead: lines with 'foo' followed by 'bar' (not necessarily adjacent)
rg -P 'foo(?=.*bar)' file.txt

# Lookbehind: numbers preceded by '$'
rg -P '(?<=\$)\d+' file.txt

# Unicode property: em-dashes
rg -P '[\x{2014}]' file.txt

# Backreferences: repeated words
rg -P '\b(\w+)\s+\1\b' file.txt

# Atomic groups: possessive matching
rg -P '(?>a+)b' file.txt
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "cannot find -lpcre2-8" | Missing dev libs | Install `libpcre2-dev` |
| "Text file busy" | Binary in use | `rm` then `cp` |
| Edition 2024 error | Old Rust | `rustup update nightly` |
| Still shows `-pcre2` | Wrong binary | Check `which rg`, install to correct location |
| Slow build | No remote compilation | Consider RCH setup |

### Common Build Errors

**pkg-config not found:**
```bash
sudo apt-get install pkg-config
```

**PCRE2 headers missing:**
```bash
# Ubuntu/Debian
sudo apt-get install libpcre2-dev

# The -dev package contains headers needed for compilation
```

---

## Cleanup

```bash
rm -rf /tmp/rg-build
```

---

## References

| Topic | File |
|-------|------|
| PCRE2 regex patterns | [PCRE2-PATTERNS.md](references/PCRE2-PATTERNS.md) |
| Cross-compilation | [CROSS-COMPILE.md](references/CROSS-COMPILE.md) |
| Benchmarking builds | [BENCHMARKS.md](references/BENCHMARKS.md) |

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use `--release` | Missing optimizations | Use `--profile release-lto` |
| Skip `+nightly` | Build may fail | Always use nightly |
| Hardcode target path | May differ per system | Use `cargo metadata` |
| Install without verify | May install wrong binary | Always check `rg --version` |
