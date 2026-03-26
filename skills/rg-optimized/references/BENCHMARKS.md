# Benchmarking ripgrep Builds

Compare your optimized build against system/stock ripgrep.

## Quick Benchmark

```bash
# Compare system rg vs your build
hyperfine \
  --warmup 3 \
  --runs 10 \
  '/usr/bin/rg "pattern" /path/to/large/codebase' \
  '~/.cargo/bin/rg "pattern" /path/to/large/codebase'
```

## Standard Benchmark Suite

```bash
# Clone ripgrep's benchsuite
cd /tmp/rg-build
git clone --depth 1 https://github.com/BurntSushi/ripgrep-bench.git

# Run benchmarks
cd ripgrep-bench
./run linux-x86_64
```

## Key Metrics

| Metric | Command | Meaning |
|--------|---------|---------|
| Search speed | `hyperfine 'rg pattern'` | Time to search |
| Startup time | `hyperfine 'rg --version'` | Cold start overhead |
| SIMD effectiveness | Check `simd(runtime)` in `--version` | AVX2 usage |

## Expected Results

### Build Profile Comparison

| Profile | Binary Size | Relative Speed |
|---------|-------------|----------------|
| `--release` | ~8MB | 1.0x (baseline) |
| `--profile release-lto` | ~4MB | 1.05-1.15x |
| release-lto + native | ~4MB | 1.10-1.25x |

### PCRE2 vs Rust Regex

| Pattern Type | Rust regex | PCRE2 |
|--------------|-----------|-------|
| Simple literal | ~1.0x | ~1.0x |
| Complex regex | 1.0x | 0.7-0.9x (slower) |
| Lookahead/behind | N/A | Works |
| Backreferences | N/A | Works |

**Takeaway:** Use Rust regex (no `-P`) for simple patterns. Use PCRE2 only when you need its features.

## Profiling

```bash
# CPU profile with flamegraph
cargo flamegraph --profile release-lto --features pcre2 -- -c 'rg pattern /large/dir'

# Perf stat
perf stat rg pattern /large/dir 2>&1 | tail -20
```

## Memory Usage

```bash
# Peak memory
/usr/bin/time -v rg pattern /large/dir 2>&1 | grep "Maximum resident"

# With heaptrack
heaptrack rg pattern /large/dir
heaptrack_print heaptrack.rg.*.gz | head -30
```

## Comparing Builds

```bash
# A/B test script
#!/bin/bash
OLD_RG=/usr/bin/rg
NEW_RG=~/.cargo/bin/rg
PATTERN="TODO|FIXME"
TARGET=/path/to/large/repo

echo "=== Old rg ==="
hyperfine --warmup 2 --runs 5 "$OLD_RG '$PATTERN' $TARGET"

echo "=== New rg ==="
hyperfine --warmup 2 --runs 5 "$NEW_RG '$PATTERN' $TARGET"

echo "=== Head-to-head ==="
hyperfine --warmup 2 --runs 5 \
  -n "old" "$OLD_RG '$PATTERN' $TARGET" \
  -n "new" "$NEW_RG '$PATTERN' $TARGET"
```

## Real-World Benchmark: Linux Kernel

```bash
# Clone linux kernel (if not available)
git clone --depth 1 https://github.com/torvalds/linux.git /tmp/linux

# Benchmark
hyperfine \
  --warmup 3 \
  'rg "[A-Z]+_SUSPEND" /tmp/linux' \
  'rg -P "[A-Z]+_SUSPEND" /tmp/linux'
```

Expected: Rust regex ~10% faster than PCRE2 for this pattern.

## Notes

1. **First run is slow** — File system cache effects. Always use `--warmup`
2. **PCRE2 adds overhead** — Only use `-P` when needed
3. **Native CPU helps most** on complex patterns with SIMD opportunities
4. **LTO helps binary size** more than raw speed (but both improve)
