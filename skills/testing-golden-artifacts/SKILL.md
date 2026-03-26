---
name: testing-golden-artifacts
description: >-
  Build golden artifact test suites that freeze known-good outputs and catch
  regressions through exact comparison. Use when: snapshot testing, approval
  testing, characterization testing, compiler output validation, query plan
  verification, UI snapshot comparison, CLI output regression, serialization
  format stability. Supports insta (Rust), jest snapshots, golden file
  workflows, scrubbing, canonicalization, and multi-format goldens.
metadata:
  filePattern:
    - "**/golden*"
    - "**/snapshot*"
    - "**/*.snap"
    - "**/*.golden"
  bashPattern:
    - "\\b(golden|snapshot|insta|UPDATE_GOLDENS|UPDATE_SNAPSHOTS|approval.test)\\b"
  priority: 60
---

# Golden Artifact Testing

> **The One Rule:** If the output is too complex to assert field-by-field,
> freeze a known-good output and diff against it forever. Every diff is either
> a bug or an intentional change that requires human review.

## The Loop (Mandatory)

```
1. GENERATE    → Run the system, capture output as golden artifact
2. CANONICALIZE → Strip non-determinism (timestamps, UUIDs, memory addresses)
3. REVIEW      → Human verifies the golden is actually correct
4. FREEZE      → Commit the golden file to version control
5. COMPARE     → Every test run diffs actual vs golden — any difference FAILS
6. UPDATE      → When behavior intentionally changes:
                  UPDATE_GOLDENS=1 → re-run → git diff goldens/ → review → commit
7. GUARD       → CI blocks merging if goldens differ without approval
```

## Golden Confidence Matrix

Before creating a golden, classify its stability:

| Golden Artifact | Deterministic? | Platform-dependent? | Volatility (1-5) | Strategy |
|----------------|:-----------:|:-------------------:|:-----------------:|----------|
| *description* | Y/N | Y/N | How often it changes | exact/fuzzy/scrubbed |

**Rule:** Volatility ≥ 4 goldens should use scrubbing or fuzzy matching.
Exact-match goldens for volatile outputs cause test rot.

---

## Decision Tree: Which Golden Pattern?

```
What kind of output are you testing?
│
├─ Deterministic text (CLI output, rendered HTML, formatted code)
│  └─ EXACT GOLDEN (Pattern 1) — byte-for-byte comparison
│
├─ Structured data with dynamic fields (JSON with timestamps/IDs)
│  └─ SCRUBBED GOLDEN (Pattern 2) — mask dynamic values, compare rest
│
├─ Floating-point or numeric output (scientific computing, ML scores)
│  └─ FUZZY GOLDEN (Pattern 3) — epsilon-based comparison
│
├─ Binary output (images, protobuf, compiled artifacts)
│  └─ SEMANTIC GOLDEN (Pattern 4) — decode then compare structure
│
├─ Multi-platform output (different line endings, paths)
│  └─ CANONICALIZED GOLDEN (Pattern 5) — normalize before comparison
│
└─ Output that changes frequently (evolving API responses)
   └─ STRUCTURAL GOLDEN (Pattern 6) — compare shape, not values
```

---

## The Six Patterns

### Pattern 1: Exact Golden (Rust — insta crate)

The gold standard for deterministic text output.

```rust
use insta::assert_snapshot;

#[test]
fn test_error_formatting() {
    let err = ParseError::new("unexpected token", 42, 5);
    assert_snapshot!(err.display());
    // First run: creates snapshots/test_error_formatting.snap
    // Subsequent runs: compares against snapshot
    // Review: cargo insta review (interactive TUI)
}

#[test]
fn test_json_output() {
    let config = Config::default();
    // assert_json_snapshot! pretty-prints and sorts keys for stability
    insta::assert_json_snapshot!(config);
}

#[test]
fn test_debug_repr() {
    let tree = build_ast("1 + 2 * 3");
    // assert_debug_snapshot! uses Debug formatting
    insta::assert_debug_snapshot!(tree);
}
```

```bash
# Workflow with insta
cargo test                    # Run tests — new/changed snapshots FAIL
cargo insta review            # Interactive TUI: accept/reject each change
cargo insta test --review     # Run tests then immediately review
cargo insta test --accept-unseen  # Accept all NEW snapshots (careful!)
```

**insta settings for scrubbing:**
```rust
use insta::Settings;

#[test]
fn test_with_scrubbing() {
    let mut settings = Settings::clone_current();
    // Replace UUIDs with placeholder
    settings.add_filter(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "[UUID]"
    );
    // Replace timestamps
    settings.add_filter(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
        "[TIMESTAMP]"
    );
    settings.bind(|| {
        assert_snapshot!(generate_report());
    });
}
```

### Pattern 2: Scrubbed Golden (Dynamic Values)

For output containing timestamps, UUIDs, or other non-deterministic values.

```rust
/// Scrub non-deterministic values before golden comparison
fn scrub(output: &str) -> String {
    let mut scrubbed = output.to_string();

    // UUIDs → [UUID]
    let uuid_re = regex::Regex::new(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    ).unwrap();
    scrubbed = uuid_re.replace_all(&scrubbed, "[UUID]").to_string();

    // ISO timestamps → [TIMESTAMP]
    let ts_re = regex::Regex::new(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?"
    ).unwrap();
    scrubbed = ts_re.replace_all(&scrubbed, "[TIMESTAMP]").to_string();

    // Memory addresses → [ADDR]
    let addr_re = regex::Regex::new(r"0x[0-9a-f]{6,16}").unwrap();
    scrubbed = addr_re.replace_all(&scrubbed, "[ADDR]").to_string();

    // Durations → [DURATION]
    let dur_re = regex::Regex::new(r"\d+(\.\d+)?\s*(ms|us|ns|s|sec|min)").unwrap();
    scrubbed = dur_re.replace_all(&scrubbed, "[DURATION]").to_string();

    scrubbed
}

#[test]
fn test_api_response() {
    let response = call_api();
    let scrubbed = scrub(&serde_json::to_string_pretty(&response).unwrap());
    assert_golden("api/user_profile", &scrubbed);
}
```

### Pattern 3: Fuzzy Golden (Numeric Output)

For floating-point or numeric results where exact comparison is inappropriate.

```rust
/// Compare numeric golden with epsilon tolerance
fn assert_fuzzy_golden(test_name: &str, actual: &[f64], epsilon: f64) {
    let golden_path = golden_path(test_name);

    if updating_goldens() {
        let text = actual.iter()
            .map(|v| format!("{:.10e}", v))
            .collect::<Vec<_>>()
            .join("\n");
        fs::write(&golden_path, text).unwrap();
        return;
    }

    let expected: Vec<f64> = fs::read_to_string(&golden_path)
        .unwrap()
        .lines()
        .map(|l| l.parse().unwrap())
        .collect();

    assert_eq!(actual.len(), expected.len(),
        "Length mismatch: actual {} vs golden {}", actual.len(), expected.len());

    for (i, (a, e)) in actual.iter().zip(expected.iter()).enumerate() {
        let diff = (a - e).abs();
        let rel_diff = if e.abs() > f64::EPSILON { diff / e.abs() } else { diff };
        assert!(rel_diff < epsilon,
            "Fuzzy golden mismatch at index {i}: actual={a:.10e}, expected={e:.10e}, \
             rel_diff={rel_diff:.2e}, epsilon={epsilon:.2e}");
    }
}
```

### Pattern 4: Semantic Golden (Binary/Structured)

For binary output where byte-for-byte comparison is too strict.

```rust
/// Compare binary output semantically (decode then compare structure)
fn assert_semantic_golden(test_name: &str, actual_bytes: &[u8]) {
    let golden_path = golden_path_bin(test_name);

    if updating_goldens() {
        fs::write(&golden_path, actual_bytes).unwrap();
        return;
    }

    let expected_bytes = fs::read(&golden_path).unwrap();

    // Decode both to structured representation
    let actual_decoded = decode_protobuf(actual_bytes).unwrap();
    let expected_decoded = decode_protobuf(&expected_bytes).unwrap();

    // Compare structure, not bytes (handles field reordering, default values)
    assert_eq!(actual_decoded, expected_decoded,
        "Semantic golden mismatch for {test_name}");
}
```

### Pattern 5: Canonicalized Golden (Cross-Platform)

```rust
/// Normalize platform differences before comparison
fn canonicalize(output: &str) -> String {
    output
        .replace("\r\n", "\n")                    // Windows line endings
        .replace('\\', "/")                       // Windows path separators
        .replace("/home/runner/", "/HOME/")       // CI home directories
        .replace("/Users/", "/HOME/")             // macOS home directories
        .lines()
        .map(|l| l.trim_end())                    // Trailing whitespace
        .collect::<Vec<_>>()
        .join("\n")
}
```

### Pattern 6: Structural Golden (Shape-Only)

For output where values change but structure must be stable.

```typescript
// Jest structural snapshot — checks shape, not exact values
test("API response has correct shape", async () => {
  const response = await fetchUserProfile();
  expect(response).toMatchInlineSnapshot(`
    {
      "id": Any<String>,
      "email": Any<String>,
      "createdAt": Any<String>,
      "subscription": {
        "status": Any<String>,
        "provider": Any<String>,
      },
    }
  `);
});
```

---

## The Golden File Infrastructure

### Universal `assert_golden` Implementation

```rust
/// The core golden comparison function. Used by all patterns.
fn assert_golden(test_name: &str, actual: &str) {
    let golden_path = Path::new("tests/golden")
        .join(format!("{test_name}.golden"));

    // UPDATE MODE: overwrite golden with actual output
    if std::env::var("UPDATE_GOLDENS").is_ok() {
        fs::create_dir_all(golden_path.parent().unwrap()).unwrap();
        fs::write(&golden_path, actual).unwrap();
        eprintln!("[GOLDEN] Updated: {}", golden_path.display());
        return;
    }

    // COMPARE MODE: diff actual vs golden
    let expected = fs::read_to_string(&golden_path)
        .unwrap_or_else(|_| panic!(
            "Golden file missing: {}\n\
             Run with UPDATE_GOLDENS=1 to create it\n\
             Then review and commit: git diff tests/golden/",
            golden_path.display()
        ));

    if actual != expected {
        // Write actual for easy diffing
        let actual_path = golden_path.with_extension("actual");
        fs::write(&actual_path, actual).unwrap();

        // Generate unified diff for error message
        let diff = unified_diff(&expected, actual, 3);

        panic!(
            "GOLDEN MISMATCH: {test_name}\n\n\
             {diff}\n\n\
             To update: UPDATE_GOLDENS=1 cargo test -- {test_name}\n\
             To review: diff {} {}",
            golden_path.display(),
            actual_path.display(),
        );
    }
}

fn unified_diff(expected: &str, actual: &str, context: usize) -> String {
    // Use similar crate or manual diff generation
    let expected_lines: Vec<&str> = expected.lines().collect();
    let actual_lines: Vec<&str> = actual.lines().collect();
    // ... generate unified diff with context lines
    format!("--- expected\n+++ actual\n(diff output)")
}
```

### Directory Layout

```
tests/golden/
├── cli/
│   ├── help_output.golden          # CLI --help output
│   ├── version_output.golden       # CLI --version output
│   └── error_messages/
│       ├── missing_arg.golden
│       └── invalid_format.golden
├── api/
│   ├── user_profile.golden         # API response (scrubbed)
│   └── error_response.golden
├── rendering/
│   ├── table_basic.golden          # Rendered table output
│   └── chart_svg.golden            # SVG chart output
└── PROVENANCE.md                   # How goldens were generated
```

---

## CI Integration

```yaml
# GitHub Actions: fail if goldens differ
- name: Run tests with golden comparison
  run: cargo test
  # Fails if any golden doesn't match

# On failure: upload actual outputs as artifacts for review
- name: Upload golden diffs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: golden-diffs
    path: |
      tests/golden/**/*.actual
    retention-days: 7
```

**PR workflow:**
```bash
# Developer flow:
cargo test                              # FAIL: golden changed
UPDATE_GOLDENS=1 cargo test             # Regenerate goldens
git diff tests/golden/                  # Review EVERY change
git add tests/golden/                   # Stage approved changes
git commit -m "Update goldens: [reason]"
```

---

## The Scrubber Registry

For projects with many dynamic values, build a reusable scrubber:

```rust
pub struct Scrubber {
    rules: Vec<(Regex, &'static str)>,
}

impl Scrubber {
    pub fn standard() -> Self {
        Self {
            rules: vec![
                (uuid_regex(), "[UUID]"),
                (iso_timestamp_regex(), "[TIMESTAMP]"),
                (duration_regex(), "[DURATION]"),
                (memory_address_regex(), "[ADDR]"),
                (port_number_regex(), "[PORT]"),
                (absolute_path_regex(), "[PATH]"),
            ],
        }
    }

    pub fn with_custom(mut self, pattern: &str, replacement: &'static str) -> Self {
        self.rules.push((Regex::new(pattern).unwrap(), replacement));
        self
    }

    pub fn scrub(&self, input: &str) -> String {
        let mut result = input.to_string();
        for (regex, replacement) in &self.rules {
            result = regex.replace_all(&result, *replacement).to_string();
        }
        result
    }
}
```

---

## Anti-Patterns (Hard Constraints)

| ✗ Never | Why | Fix |
|---------|-----|-----|
| Goldens without review mechanism | Blindly accepted goldens contain bugs | Always: update → diff → review → commit |
| Exact golden for non-deterministic output | Test rot: flaky failures | Scrub or fuzzy-match dynamic values |
| Golden tests for implementation details | Breaks on refactors that don't change behavior | Golden = observable output only |
| Huge golden files (>100KB) | Impossible to review diffs | Split into smaller, focused goldens |
| No PROVENANCE.md | Can't reproduce goldens when they go stale | Record generator version + command |
| Skipping golden diff review | "It changed, just update it" → bugs accepted | `git diff tests/golden/` BEFORE commit |
| Platform-specific golden without canonicalization | CI fails on different OS | Canonicalize line endings, paths |
| Committing `.actual` files | Clutters repo with transient data | `.gitignore` `*.actual` files |

---

## Checklist (Before Shipping Golden Suite)

- [ ] `assert_golden` infrastructure with `UPDATE_GOLDENS` support
- [ ] Scrubber handles all dynamic values (UUIDs, timestamps, durations, paths)
- [ ] Every golden file reviewed by human before first commit
- [ ] PROVENANCE.md records how goldens were generated
- [ ] `.gitignore` includes `*.actual` files
- [ ] CI fails on golden mismatch (no auto-update in CI)
- [ ] Diff output in failure messages (not just "mismatch")
- [ ] Golden files organized by feature/module
- [ ] Cross-platform canonicalization if needed

---

## References

| Need | Reference |
|------|-----------|
| Insta crate deep-dive | [INSTA.md](references/INSTA.md) |
| Scrubber patterns catalog | [SCRUBBERS.md](references/SCRUBBERS.md) |
| Binary golden techniques | [BINARY-GOLDENS.md](references/BINARY-GOLDENS.md) |
| CI workflows | [CI-GOLDENS.md](references/CI-GOLDENS.md) |
| Troubleshooting common issues | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |

## Relationship to Other Testing Skills

| Technique | Use INSTEAD when | Use TOGETHER when |
|-----------|-----------------|-------------------|
| /testing-conformance-harnesses | Have a reference impl to diff against | Goldens ARE the frozen reference outputs |
| /testing-fuzzing | Looking for crashes, not output stability | Fuzz-found bugs become golden regression tests |
| /testing-metamorphic | Can't verify exact output (oracle problem) | Metamorphic if no golden exists; golden once validated |
