---
name: testing-fuzzing
description: >-
  Design and implement fuzzing harnesses for crash discovery, security auditing,
  and correctness verification. Coverage-guided, structure-aware, differential,
  and grammar-based fuzzing. Use when: testing parsers, protocols, serialization,
  cryptography, state machines, file formats, or any input-processing code.
  cargo-fuzz, AFL++, bolero, proptest, libFuzzer, fast-check, sanitizers.
metadata:
  filePattern:
    - "**/fuzz*"
    - "**/fuzz_targets/**"
    - "**/Cargo.toml"
  bashPattern:
    - "\\b(cargo.fuzz|cargo-fuzz|libfuzzer|afl|honggfuzz|bolero|fuzz_target)\\b"
  priority: 60
---

# Fuzzing

> **The One Rule:** Throw random-but-intelligent inputs at code until something breaks.
> Profile the fuzzer, not the code. A fuzzer that never reaches deep code paths finds nothing.

## The Loop (Mandatory)

```
1. TARGET     → Identify the narrowest input-processing boundary
2. SEED       → Craft a minimal corpus of valid + boundary inputs
3. STRUCTURE  → Derive Arbitrary impl if input has grammar/schema
4. HARNESS    → Write fuzz target: guard size, assert invariants, never panic in harness
5. SANITIZE   → Enable ASan + UBSan minimum; MSan for unsafe code
6. RUN        → Coverage-guided fuzzing, monitor new edge discovery rate
7. TRIAGE     → Minimize crashes, classify root causes, write regression tests
8. ITERATE    → New corpus → deeper coverage → new crashes → repeat
```

## Target Selection Matrix (Mandatory)

Before writing a harness, score the attack surface:

| Target Function | Untrusted Input? | Complexity (1-5) | Unsafe Code? | Prior CVEs? | Score |
|----------------|----------------:|------------------:|:------------:|:-----------:|-------|
| *func_name* | Y/N | cyclomatic | Y/N | count | Sum |

**Rule:** Fuzz highest-scoring targets first. Don't fuzz internal helpers
that only receive validated data — fuzz the validation boundary itself.

---

## Decision Tree: Which Fuzzing Approach?

```
What are you fuzzing?
│
├─ Raw bytes → parser/deserializer
│  └─ COVERAGE-GUIDED (cargo-fuzz / libFuzzer)
│     Best for: finding crashes in binary parsers, image decoders, protocol parsers
│
├─ Structured input → has grammar/schema
│  └─ STRUCTURE-AWARE (Arbitrary derive + cargo-fuzz)
│     Best for: API fuzzing, config validation, SQL, JSON with constraints
│
├─ Two implementations of same thing
│  └─ DIFFERENTIAL (both in one harness, compare outputs)
│     Best for: porting across languages, optimized vs reference impl
│
├─ Protocol with state machine
│  └─ STATEFUL (sequence of operations)
│     Best for: file systems, databases, network protocols
│
├─ Crypto / timing sensitive
│  └─ SPECIALIZED (SideFuzz, ct-fuzz, dudect)
│     Best for: constant-time verification, side-channel detection
│
└─ Already have proptest tests
   └─ UNIFIED (Bolero — same harness, any engine)
      Best for: upgrading property tests to full fuzzing without rewrite
```

---

## Harness Patterns (The Five Archetypes)

### Archetype 1: Crash Detector (Raw Bytes)

The simplest and most common. Feed arbitrary bytes, ensure no panics.

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // GUARD: Bound input size to prevent OOM
    if data.len() > 1_000_000 { return; }

    // RULE: let _ = means "may fail gracefully"
    // RULE: unwrap()/expect() means "must succeed — panic is a bug"
    let _ = my_crate::parse_message(data);
});
```

**Invariant:** `let _ =` for expected failures. `assert!` for properties that
must hold even on garbage input (e.g., "parser never corrupts global state").

### Archetype 2: Round-Trip (Serialize ↔ Deserialize)

The gold standard for serialization code. Tests both directions simultaneously.

```rust
#![no_main]
use arbitrary::Arbitrary;
use libfuzzer_sys::fuzz_target;

#[derive(Debug, Arbitrary)]
struct FuzzInput {
    raw: Vec<u8>,           // Strategy 1: raw bytes → must not panic
    values: Vec<FuzzValue>, // Strategy 2: structured → must round-trip
}

#[derive(Debug, Arbitrary)]
enum FuzzValue {
    Null,
    Integer(i64),
    Float(f64),
    Text(String),
    Blob(Vec<u8>),
}

fuzz_target!(|input: FuzzInput| {
    // Strategy 1: Raw bytes — parser must handle gracefully
    if input.raw.len() <= 65536 {
        let _ = parse_record(&input.raw);
    }

    // Strategy 2: Structured values — serialize/deserialize MUST round-trip
    if !input.values.is_empty() && input.values.len() <= 1000 {
        let values: Vec<Value> = input.values.iter().map(|v| v.into()).collect();
        let serialized = serialize_record(&values);
        let deserialized = parse_record(&serialized)
            .expect("INVARIANT VIOLATION: cannot parse our own output");
        assert_eq!(values, deserialized,
            "ROUND-TRIP FAILURE: serialize→parse changed values");
    }
});
```

### Archetype 3: Differential (Two Implementations)

Compare implementations that should agree. Every divergence is a bug in one of them.

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let ours = my_parser::parse(data);
    let reference = reference_parser::parse(data);

    match (ours, reference) {
        (Ok(a), Ok(b)) => {
            // BOTH ACCEPT: outputs must match
            assert_eq!(a, b, "DIVERGENCE: both accepted but outputs differ");
        }
        (Err(_), Err(_)) => {
            // BOTH REJECT: acceptable (may differ in error type)
        }
        (Ok(_), Err(_)) => {
            // WE ACCEPT, REFERENCE REJECTS: flag for review
            // May be intentional (we're more permissive) — log, don't panic
        }
        (Err(e), Ok(_)) => {
            // REFERENCE ACCEPTS, WE REJECT: likely our bug
            panic!("CONFORMANCE BUG: reference accepts input we reject: {e}");
        }
    }
});
```

### Archetype 4: Stateful (Operation Sequences)

Fuzz sequences of operations on stateful systems. The killer pattern for databases,
file systems, and protocol stacks.

```rust
#![no_main]
use arbitrary::Arbitrary;
use libfuzzer_sys::fuzz_target;

#[derive(Debug, Arbitrary)]
enum Op {
    Insert { key: u8, value: Vec<u8> },  // u8 keys increase collision chance
    Get { key: u8 },
    Delete { key: u8 },
    BeginTx,
    Commit,
    Rollback,
    Checkpoint,
}

#[derive(Debug, Arbitrary)]
struct FuzzSession { ops: Vec<Op> }

fuzz_target!(|session: FuzzSession| {
    if session.ops.len() > 200 { return; }  // Bound sequence length
    if session.ops.iter().any(|op| matches!(op, Op::Insert { value, .. } if value.len() > 10_000)) {
        return;  // Bound value sizes
    }

    let db = Database::open_in_memory();
    let mut model = BTreeMap::new();  // Shadow model for correctness oracle

    for op in &session.ops {
        match op {
            Op::Insert { key, value } => {
                let _ = db.insert(&[*key], value);
                model.insert(*key, value.clone());
            }
            Op::Get { key } => {
                let db_result = db.get(&[*key]);
                let model_result = model.get(key);
                // ORACLE: in-memory model is ground truth
                match (db_result, model_result) {
                    (Some(db_val), Some(model_val)) => {
                        assert_eq!(&db_val, model_val,
                            "DB returned wrong value for key {key}");
                    }
                    (None, None) => {}
                    (Some(_), None) => panic!("DB has key {key} but model doesn't"),
                    (None, Some(_)) => panic!("Model has key {key} but DB doesn't"),
                }
            }
            Op::Delete { key } => {
                let _ = db.delete(&[*key]);
                model.remove(key);
            }
            _ => { let _ = db.execute_op(op); }
        }
    }

    // POST-CONDITION: DB must be in consistent state
    db.check_invariants().expect("INVARIANT VIOLATION after operation sequence");
});
```

### Archetype 5: Grammar-Based (Syntax-Aware)

Generate syntactically valid-ish inputs for language/protocol parsers.

```rust
#![no_main]
use arbitrary::{Arbitrary, Unstructured};
use libfuzzer_sys::fuzz_target;

/// Generate random but syntactically plausible SQL
#[derive(Debug)]
struct FuzzSQL(String);

impl<'a> Arbitrary<'a> for FuzzSQL {
    fn arbitrary(u: &mut Unstructured<'a>) -> arbitrary::Result<Self> {
        let stmt = match u.int_in_range(0..=4)? {
            0 => format!("SELECT {} FROM {}", fuzz_columns(u)?, fuzz_table(u)?),
            1 => format!("INSERT INTO {} VALUES ({})", fuzz_table(u)?, fuzz_values(u)?),
            2 => format!("DELETE FROM {} WHERE {}", fuzz_table(u)?, fuzz_predicate(u)?),
            3 => format!("UPDATE {} SET {} WHERE {}", fuzz_table(u)?,
                         fuzz_assignment(u)?, fuzz_predicate(u)?),
            _ => format!("CREATE TABLE {} ({})", fuzz_table(u)?, fuzz_columns_def(u)?),
        };
        Ok(FuzzSQL(stmt))
    }
}

fuzz_target!(|sql: FuzzSQL| {
    // Each invocation creates a fresh in-memory database
    let db = Database::open_in_memory();
    let _ = db.execute(&sql.0);  // Must not panic or corrupt state
    db.check_invariants().expect("Invariants violated after SQL execution");
});
```

---

## Sanitizer Discipline (Non-Negotiable)

```bash
# MINIMUM: AddressSanitizer (buffer overflow, use-after-free, double-free)
# This is the DEFAULT for cargo-fuzz — always active
cargo fuzz run my_target

# ADD: UndefinedBehaviorSanitizer (integer overflow, alignment, null deref)
RUSTFLAGS="-Zsanitizer=undefined" cargo +nightly fuzz run my_target

# FOR UNSAFE CODE: MemorySanitizer (uninitialized memory reads)
RUSTFLAGS="-Zsanitizer=memory" cargo +nightly fuzz run my_target

# FOR CONCURRENT CODE: ThreadSanitizer (data races)
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly fuzz run my_target
```

| Sanitizer | Catches | Overhead | When |
|-----------|---------|----------|------|
| ASan | Buffer overflow, UAF, double-free | 2x | **Always** |
| UBSan | Integer overflow, alignment | 1.2x | **Always** |
| MSan | Uninitialized reads | 3x | Unsafe code |
| TSan | Data races | 5-15x | Concurrent code |

**Anti-pattern:** Running without sanitizers. A fuzzer without ASan is a
random test generator, not a security tool.

---

## Corpus Engineering

### Seed Corpus (Day 0)

```bash
mkdir -p fuzz/corpus/my_target

# Valid inputs that exercise different code paths
echo '{}' > fuzz/corpus/my_target/empty_object
echo '{"key": "value"}' > fuzz/corpus/my_target/simple
echo '{"nested": {"deep": [1,2,3]}}' > fuzz/corpus/my_target/nested

# Boundary values
printf '' > fuzz/corpus/my_target/empty          # 0 bytes
printf '\x00' > fuzz/corpus/my_target/null_byte  # Single null
printf '\xff' > fuzz/corpus/my_target/high_byte  # Max byte value
head -c 65536 /dev/urandom > fuzz/corpus/my_target/large_random
```

### Corpus Maintenance

```bash
# Minimize corpus: remove redundant inputs (same coverage)
cargo fuzz cmin my_target

# Minimize a specific crashing input to smallest reproducer
cargo fuzz tmin my_target artifacts/my_target/crash-abc123

# Check corpus coverage
cargo fuzz coverage my_target
```

**Rule:** Minimize corpus weekly. A 100K-entry corpus is slower than a
500-entry corpus with the same coverage.

---

## Triage Pipeline

When fuzzing finds a crash:

```
1. MINIMIZE    → cargo fuzz tmin my_target crash-xxx
2. REPRODUCE   → cargo fuzz run my_target artifacts/crash-xxx (deterministic?)
3. CLASSIFY    → Memory bug? Logic bug? Panic? OOM? Timeout?
4. ROOT-CAUSE  → Read the stack trace, write the fix
5. REGRESSION  → Convert to permanent unit test:

    #[test]
    fn regression_crash_abc123() {
        let input = include_bytes!("../fuzz/artifacts/my_target/crash-abc123");
        let _ = my_crate::parse(input);  // Must not panic after fix
    }

6. RE-FUZZ     → Run again to find deeper bugs now that shallow ones are fixed
```

---

## Bolero: Write Once, Fuzz Everywhere

```rust
use bolero::check;

#[test]
fn fuzz_parser_bolero() {
    check!()
        .with_type::<Vec<u8>>()
        .cloned()
        .for_each(|data| {
            let _ = my_crate::parse(&data);
        });
}
```

```bash
# Same harness, different engines
cargo bolero test fuzz_parser_bolero --engine libfuzzer
cargo bolero test fuzz_parser_bolero --engine afl
cargo bolero test fuzz_parser_bolero --engine honggfuzz
cargo test fuzz_parser_bolero   # Property-based (random) mode in CI
```

**Why Bolero:** Write the harness once. Run with libFuzzer for deep coverage,
AFL++ for deterministic mutation, honggfuzz for hardware-assisted feedback,
and plain `cargo test` for CI regression. Zero harness duplication.

---

## Anti-Patterns (Hard Constraints)

| ✗ Never | Why | Fix |
|---------|-----|-----|
| Fuzz target is the entire program | Coverage too thin, never reaches interesting code | Narrow to one parser/function |
| No input size guards | OOM kills mask real bugs | `if data.len() > MAX { return; }` |
| `unwrap()` in the harness itself | Harness crash ≠ code bug | Use `let _ =` for expected failures |
| No seed corpus | Fuzzer wastes hours on trivially invalid inputs | Seed with valid + boundary examples |
| Never minimize crashes | 100KB crash input is undebuggable | Always `cargo fuzz tmin` |
| Run without sanitizers | Miss the bugs fuzzing is best at finding | ASan + UBSan minimum |
| Fuzz forever, never triage | Crashes pile up without fixes | Triage daily, fix weekly |
| Check error message strings | Brittle, breaks on rewording | Check error *types/categories* |

---

## Checklist (Before Shipping Fuzz Harness)

- [ ] Target function identified (narrowest input boundary)
- [ ] Seed corpus created (valid + boundary + adversarial)
- [ ] Input size bounded (`if len > MAX { return; }`)
- [ ] Value sizes bounded (no unbounded `Vec<u8>` in Arbitrary)
- [ ] ASan enabled (default for cargo-fuzz)
- [ ] UBSan enabled for integer-heavy code
- [ ] MSan enabled if target has unsafe code
- [ ] `let _ =` for expected failures, `assert!` for invariant violations
- [ ] Invariant checks at end of harness (state consistency)
- [ ] Crash artifacts convert to regression tests
- [ ] CI runs regression corpus on every PR

---

## References

| Need | Reference |
|------|-----------|
| Complete harness catalog | [HARNESS-CATALOG.md](references/HARNESS-CATALOG.md) |
| Sanitizer deep-dive | [SANITIZERS.md](references/SANITIZERS.md) |
| Corpus engineering guide | [CORPUS.md](references/CORPUS.md) |
| Real-world CVEs found by fuzzing | [CVE-TABLE.md](references/CVE-TABLE.md) |
| CI/CD fuzzing integration | [CI-FUZZING.md](references/CI-FUZZING.md) |
| Language-specific guides | [LANGUAGES.md](references/LANGUAGES.md) |
| Troubleshooting common issues | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |

## Relationship to Other Testing Skills

| Technique | Use INSTEAD when | Use TOGETHER when |
|-----------|-----------------|-------------------|
| /testing-metamorphic | Logic bugs, not crashes | Fuzzing generates inputs, MRs check relations |
| /testing-conformance-harnesses | Spec compliance, not crashes | Fuzz-generated inputs feed conformance checks |
| /extreme-software-optimization | Perf, not correctness | Fuzz after optimization to verify no regressions |
| /lean-formal-feedback-loop | Need mathematical proof | Fuzzing finds counterexamples, proofs close the gap |
