# Cross-Compilation Guide

Build ripgrep for different platforms from a single machine.

## Target Triples

| Target | Description | PCRE2 Lib |
|--------|-------------|-----------|
| `x86_64-unknown-linux-gnu` | Linux x64 (glibc) | `libpcre2-dev` |
| `x86_64-unknown-linux-musl` | Linux x64 (musl, static) | `musl-tools` + static pcre2 |
| `aarch64-unknown-linux-gnu` | Linux ARM64 | Cross toolchain needed |
| `x86_64-apple-darwin` | macOS Intel | macOS SDK |
| `aarch64-apple-darwin` | macOS Apple Silicon | macOS SDK |

## Linux to Linux (Same Architecture)

```bash
# Standard build
RUSTFLAGS="-C target-cpu=native" cargo +nightly build \
  --profile release-lto \
  --features pcre2
```

## Linux Static (musl)

```bash
# Install musl toolchain
sudo apt-get install musl-tools

# Build static PCRE2 first (or skip PCRE2 for static builds)
cargo +nightly build \
  --profile release-lto \
  --target x86_64-unknown-linux-musl
```

**Note:** PCRE2 static linking is complex. For portable binaries without PCRE2, omit `--features pcre2`.

## Cross-Compile to ARM64

```bash
# Install cross-compilation toolchain
sudo apt-get install gcc-aarch64-linux-gnu

# Add target
rustup target add aarch64-unknown-linux-gnu

# Build (without PCRE2 - requires cross-compiled PCRE2)
cargo +nightly build \
  --profile release-lto \
  --target aarch64-unknown-linux-gnu
```

## macOS from Linux

Requires macOS SDK. Easier to build on macOS directly.

```bash
# On macOS:
brew install pcre2 pkg-config
RUSTFLAGS="-C target-cpu=native" cargo +nightly build \
  --profile release-lto \
  --features pcre2
```

## Using cross (Docker-based)

```bash
# Install cross
cargo install cross

# Build for target (may not support all features)
cross build --release --target aarch64-unknown-linux-gnu
```

**Caveat:** PCRE2 support in cross is limited. Test thoroughly.

---

## Binary Size Comparison

| Build | Size | Notes |
|-------|------|-------|
| Debug | ~50MB | Symbols, no optimization |
| Release | ~8MB | Optimized |
| release-lto | ~4MB | LTO + stripped |
| release-lto + UPX | ~1.5MB | Compressed (slower startup) |

### Further Size Reduction

```bash
# Already in release-lto:
# strip = "symbols"
# lto = "fat"
# codegen-units = 1

# Optional: UPX compression (trades startup time for size)
upx --best --lzma target/release-lto/rg
```

---

## Portable vs Native

| Choice | Flag | Binary Works On |
|--------|------|-----------------|
| Native | `-C target-cpu=native` | Same CPU only |
| Portable | (default) | Any x86_64 |
| Baseline | `-C target-cpu=x86-64` | Oldest x86_64 |
| Modern | `-C target-cpu=x86-64-v3` | AVX2-capable (2013+) |

### Recommendation

- **Server/desktop you control:** Use `target-cpu=native`
- **Distribution:** Use `target-cpu=x86-64-v3` or default
- **Maximum compatibility:** Use `target-cpu=x86-64`
