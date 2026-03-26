# Fuzzing Troubleshooting Guide

## "Coverage isn't growing"

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cov:` stuck at same number | Fuzzer can't bypass validation | Add dictionary with magic values |
| `cov:` grows slowly | Input format too strict for mutations | Switch to structure-aware (Arbitrary) |
| `ft:` stuck but `cov:` growing | Edge counts saturated | Enable `-use_value_profile=1` |
| `exec/s:` below 100 | Harness too slow | Move initialization to `LLVMFuzzerInitialize` |
| `corp:` growing but `cov:` not | Corpus bloat | Run `cargo fuzz cmin` |

## "OOM / RSS limit exceeded"

```bash
# Increase RSS limit (default: 2GB for cargo-fuzz)
cargo fuzz run my_target -- -rss_limit_mb=0    # Disable limit
cargo fuzz run my_target -- -rss_limit_mb=4096  # 4GB limit

# Bound input size in harness
if data.len() > MAX_INPUT_SIZE { return; }
```

**Root cause:** Usually unbounded allocation in the target (e.g., `Vec::with_capacity(attacker_controlled_size)`). Fix the target, don't just increase the limit.

## "Timeout"

```bash
# Increase per-input timeout (default: 10s for cargo-fuzz)
cargo fuzz run my_target -- -timeout=30

# But usually indicates a real bug:
# - Infinite loop in parser
# - Exponential regex backtracking
# - O(n²) algorithm with large input
```

## "Can't reproduce crash"

| Cause | Fix |
|-------|-----|
| Non-determinism in target | Remove `rand`, `SystemTime::now()`, `HashMap` iteration |
| Environment difference | Use same sanitizer flags, same nightly version |
| Crash was in sanitizer, not target | Check if crash is ASan false positive |
| File too large to repro | Run `cargo fuzz tmin` first |

## "ASan: heap-buffer-overflow" but code is safe Rust

This means the overflow is in a dependency's C code, a `build.rs` compiled library, or in the Rust standard library's allocator interaction. Check:

```bash
# Get detailed stack trace
ASAN_OPTIONS="symbolize=1:abort_on_error=1" cargo fuzz run my_target
```

## "Tests pass but fuzzer finds bugs"

This is expected and is WHY you fuzz. The fuzzer generates inputs your tests didn't consider. Convert each crash to a regression test:

```rust
#[test]
fn regression_crash_abc123() {
    let input = include_bytes!("../fuzz/artifacts/my_target/crash-abc123");
    let _ = my_crate::parse(input);
}
```

## "Fuzzing is too slow" (< 1000 exec/s)

| Bottleneck | Fix |
|-----------|-----|
| Expensive initialization per input | Move to `LLVMFuzzerInitialize` or `lazy_static` |
| Heap allocation in hot loop | Reuse buffers, use `SmallVec` |
| File I/O in target | Use in-memory variants |
| Logging in target | Disable logging during fuzzing |
| Target processes huge inputs | Add `if data.len() > N { return; }` early |
