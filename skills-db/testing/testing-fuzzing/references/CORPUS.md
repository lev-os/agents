# Corpus Engineering Guide

> The corpus is the fuzzer's memory. A well-engineered corpus reaches deep code paths faster. A bloated corpus wastes cycles.

## Seed Corpus Construction

### Sources for Seeds

| Source | Best For | Example |
|--------|---------|---------|
| Existing test suite | Known-valid inputs | Copy QA test files |
| Real-world data | Production-realistic | Anonymized user uploads |
| Spec examples | RFC/standard compliance | RFC test vectors |
| Manual crafting | Boundary conditions | Empty, max-size, null-filled |
| Generated | Format-specific | Grammar-based generators |

### Minimum Seed Corpus

Every fuzz target needs at minimum:

```bash
mkdir -p fuzz/corpus/my_target

# 1. Empty input
printf '' > fuzz/corpus/my_target/empty

# 2. Minimal valid input
echo '{}' > fuzz/corpus/my_target/minimal_valid

# 3. Typical valid input
echo '{"name":"test","value":42}' > fuzz/corpus/my_target/typical

# 4. Maximum-size valid input (near your size limit)
python3 -c "print('{\"data\":' + '\"x\"*50000' + '}')" > fuzz/corpus/my_target/large

# 5. Boundary bytes
printf '\x00' > fuzz/corpus/my_target/null_byte
printf '\xff' > fuzz/corpus/my_target/high_byte
printf '\x00\xff\x00\xff' > fuzz/corpus/my_target/alternating

# 6. Previously-found crash inputs (regression)
# cp artifacts/crash-* fuzz/corpus/my_target/
```

### Dictionaries

Provide format-specific tokens to help the fuzzer past magic-number checks:

```
# fuzz/dicts/json.dict
kw1="\""
kw2=":"
kw3=","
kw4="{"
kw5="}"
kw6="["
kw7="]"
kw8="null"
kw9="true"
kw10="false"
```

```
# fuzz/dicts/http.dict
kw1="GET "
kw2="POST "
kw3="HTTP/1.1"
kw4="Content-Type"
kw5="\\r\\n"
kw6="Content-Length"
```

```bash
# Use dictionary
cargo fuzz run my_target -- -dict=fuzz/dicts/json.dict
```

---

## Corpus Maintenance

### Minimization (CRITICAL — do regularly)

```bash
# Minimize corpus: keep only inputs that contribute unique coverage
cargo fuzz cmin my_target

# Before: 50,000 inputs, 2GB
# After:  500 inputs, 50MB — same coverage, 100x faster fuzzing
```

**Rule:** Minimize weekly. A 100K-entry corpus is SLOWER than a 500-entry corpus with identical coverage because the fuzzer wastes time re-executing redundant inputs.

### Crash Minimization

```bash
# Minimize a specific crashing input to smallest reproducer
cargo fuzz tmin my_target artifacts/my_target/crash-abc123

# Before: 4,096 bytes
# After:  23 bytes — same crash, easy to debug
```

**Always tmin before debugging.** A 4KB crash input is unreadable. A 23-byte input often makes the bug obvious.

### Merge (Combining Corpora)

```bash
# Merge corpus from another fuzzing campaign
cargo fuzz cmin my_target -- additional_corpus/

# libFuzzer merge mode
./my_fuzzer -merge=1 ./merged_corpus ./corpus_a ./corpus_b
```

---

## Coverage Tracking

### Generate Coverage Report

```bash
# Rust
cargo fuzz coverage my_target
# Produces coverage data in fuzz/coverage/my_target/

# View with llvm-cov
llvm-cov show target/x86_64-unknown-linux-gnu/coverage/my_target \
    -instr-profile=fuzz/coverage/my_target/coverage.profdata \
    -show-line-counts-or-regions

# HTML report
llvm-cov show ... -format=html > coverage.html
```

### Interpreting libFuzzer Output

```
#1234   NEW    cov: 1150 ft: 3200 corp: 250/50Kb lim: 1000 exec/s: 5000 rss: 100Mb
```

| Field | Meaning | Action If Stalling |
|-------|---------|-------------------|
| `cov` | Covered edges/blocks | Add dictionaries, improve seeds |
| `ft` | Features (edges + counters + value profiles) | Enable `-use_value_profile=1` |
| `corp` | Corpus size / total bytes | Run `cmin` if too large |
| `lim` | Max input length tried so far | Increase `-max_len` if needed |
| `exec/s` | Executions per second | Target ≥1000. <100 = harness too slow |
| `rss` | Resident set size (memory) | Watch for leaks; `-rss_limit_mb` |

### Plateau Detection

If `cov` and `ft` stop growing:
1. Check coverage report: which code is NOT reached?
2. Add seed inputs that exercise unreached code
3. Add dictionary entries for magic values the fuzzer can't guess
4. Consider structure-aware fuzzing (Arbitrary) for complex input formats
5. Consider custom mutators for compressed/encrypted formats
