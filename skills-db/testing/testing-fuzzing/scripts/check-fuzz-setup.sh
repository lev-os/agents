#!/usr/bin/env bash
# Check if a Rust project is set up for fuzzing
set -euo pipefail

echo "=== Fuzzing Setup Check ==="

# Check for nightly toolchain
if rustup run nightly rustc --version >/dev/null 2>&1; then
    echo "OK   nightly toolchain: $(rustup run nightly rustc --version 2>/dev/null)"
else
    echo "FAIL nightly toolchain not installed (run: rustup install nightly)"
fi

# Check for cargo-fuzz
if command -v cargo-fuzz >/dev/null 2>&1; then
    echo "OK   cargo-fuzz installed"
else
    echo "FAIL cargo-fuzz not installed (run: cargo install cargo-fuzz)"
fi

# Check for fuzz directory
if [ -d "fuzz" ]; then
    targets=$(ls fuzz/fuzz_targets/*.rs 2>/dev/null | wc -l)
    echo "OK   fuzz/ directory exists ($targets targets)"
else
    echo "WARN fuzz/ directory not found (run: cargo fuzz init)"
fi

# Check for corpus
if [ -d "fuzz/corpus" ]; then
    corpus_dirs=$(ls -d fuzz/corpus/*/ 2>/dev/null | wc -l)
    echo "OK   fuzz/corpus/ exists ($corpus_dirs target corpora)"
else
    echo "WARN fuzz/corpus/ not found (create seed corpus)"
fi

# Check for dictionaries
if [ -d "fuzz/dicts" ] || ls fuzz/*.dict >/dev/null 2>&1; then
    echo "OK   dictionaries found"
else
    echo "WARN no dictionaries found (consider adding format-specific tokens)"
fi

# List fuzz targets
if [ -d "fuzz/fuzz_targets" ]; then
    echo ""
    echo "=== Fuzz Targets ==="
    for target in fuzz/fuzz_targets/*.rs; do
        name=$(basename "$target" .rs)
        corpus_count=0
        if [ -d "fuzz/corpus/$name" ]; then
            corpus_count=$(ls fuzz/corpus/"$name"/ 2>/dev/null | wc -l)
        fi
        echo "  $name (corpus: $corpus_count inputs)"
    done
fi

echo ""
echo "=== Quick Commands ==="
echo "  cargo fuzz list              # List targets"
echo "  cargo fuzz run TARGET        # Run fuzzing"
echo "  cargo fuzz cmin TARGET       # Minimize corpus"
echo "  cargo fuzz coverage TARGET   # Coverage report"
