# Sanitizer Integration Guide

> Sanitizers are NON-NEGOTIABLE companions to fuzzing. A fuzzer without sanitizers is a random test generator, not a security tool.

## The Sanitizer Matrix

| Sanitizer | Flag | Detects | Overhead | When |
|-----------|------|---------|----------|------|
| **ASan** | `-fsanitize=address` | Buffer overflow, use-after-free, double-free, stack overflow | 2-4x | **ALWAYS** (default for cargo-fuzz) |
| **UBSan** | `-fsanitize=undefined` | Integer overflow, alignment, null deref, misaligned access | 1.2x | **ALWAYS** (combine with ASan) |
| **MSan** | `-fsanitize=memory` | Uninitialized memory reads | 3x | Unsafe code only |
| **TSan** | `-fsanitize=thread` | Data races, deadlocks | 5-15x | Concurrent code only |
| **LSan** | `-fsanitize=leak` | Memory leaks | 1.2x | Long-running targets |

**Incompatibility:** ASan and MSan cannot run simultaneously. ASan and TSan cannot run simultaneously. Run separate fuzzing campaigns.

## Usage

### Rust

```bash
# ASan (default for cargo-fuzz)
cargo fuzz run my_target

# UBSan (combine with ASan)
# cargo-fuzz doesn't have a direct flag; use RUSTFLAGS
RUSTFLAGS="-Zsanitizer=address,undefined" cargo +nightly fuzz run my_target

# MSan (for unsafe code — requires nightly)
RUSTFLAGS="-Zsanitizer=memory" cargo +nightly fuzz run my_target

# TSan (for concurrent code)
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly fuzz run my_target

# Safe Rust only? Disable sanitizers for speed
cargo fuzz run my_target --sanitizer=none
```

### C/C++

```bash
# Compile with sanitizers
clang -g -O1 -fsanitize=fuzzer,address,undefined target.c -o target

# MSan requires full dependency rebuild
clang -g -O1 -fsanitize=fuzzer,memory -fno-omit-frame-pointer target.c

# TSan
clang -g -O1 -fsanitize=fuzzer,thread target.c
```

### Go

```bash
# Go's native fuzzer includes race detection by default
go test -fuzz=FuzzMyTarget -race
```

### Python

```bash
# Atheris with native extension sanitizers
# Build the extension with ASan first, then:
LD_PRELOAD=$(clang -print-file-name=libclang_rt.asan-x86_64.so) \
    python fuzz_target.py
```

## Environment Variables

```bash
# ASan options
ASAN_OPTIONS="verbosity=1:abort_on_error=1:detect_leaks=0:malloc_context_size=30"

# Disable RSS limit (cargo-fuzz sets 2GB by default, can cause false OOMs)
cargo fuzz run my_target -- -rss_limit_mb=0

# MSan options
MSAN_OPTIONS="verbosity=1"

# TSan options
TSAN_OPTIONS="verbosity=1:second_deadlock_stack=1"
```

## Sanitizer Strategy

```
Campaign 1: ASan + UBSan (ALWAYS run first)
    → Finds: buffer overflows, use-after-free, integer overflow
    → Duration: Hours to days

Campaign 2: MSan (if target has `unsafe` code)
    → Finds: uninitialized memory reads
    → Duration: Hours

Campaign 3: TSan (if target has concurrency)
    → Finds: data races, lock order violations
    → Duration: Hours

Rule: Share corpus across campaigns. Bugs found in one
campaign may expose deeper bugs under another sanitizer.
```

## Critical Warning

**NEVER deploy sanitizers in production.** Sanitizers:
- Add significant overhead
- Can be exploited (ASan shadow memory is predictable)
- Abort on violations (turns bugs into crashes)
- Are for testing ONLY
