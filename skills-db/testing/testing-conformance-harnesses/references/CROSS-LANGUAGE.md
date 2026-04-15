# Cross-Language Porting Conformance Guide

> When porting a library from Go/Python/C to Rust (or any other cross-language port), the conformance harness is your proof of correctness. This guide covers the patterns for verifying behavioral equivalence across language boundaries.

## The Porting Conformance Loop

```
1. GENERATE fixtures from reference implementation
   └── Run reference impl → capture output → commit as golden files
2. BUILD conformance harness in target language
   └── ConformanceTest trait, fixture loader, comparison engine
3. IMPLEMENT feature by feature
   └── Each feature: code → run conformance → fix divergences → green
4. DOCUMENT divergences in DISCREPANCIES.md
   └── Every intentional difference gets a DISC-NNN entry
5. TRACK coverage in compliance matrix
   └── Feature × reference × our impl × status
```

## Fixture Generation Patterns

### Pattern A: Reference Binary Generates Fixtures

```bash
# Go → Rust port: run Go binary to generate expected outputs
cd /path/to/go-reference
go build -o gen-fixtures ./cmd/gen-fixtures
./gen-fixtures --format json --output /path/to/rust-project/tests/conformance/fixtures/go_outputs/

# Record provenance
cat >> /path/to/rust-project/tests/conformance/fixtures/PROVENANCE.md << EOF
## Go Reference Fixtures
- Generator: \`go run ./cmd/gen-fixtures\`
- Go version: $(go version | cut -d' ' -f3)
- Library version: $(git describe --tags)
- Git ref: $(git rev-parse HEAD)
- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF
```

### Pattern B: Python Script Generates Fixtures

```bash
# Python → Rust port: use Python to generate reference data
cd /path/to/python-reference
python3 -m my_library.conformance.generate \
  --output /path/to/rust-project/tests/conformance/fixtures/python_reference.json

# For complex fixtures with multiple files:
python3 -m my_library.conformance.generate_all \
  --output-dir /path/to/rust-project/tests/conformance/fixtures/python_outputs/
```

### Pattern C: Capture Live Output

```bash
# When there's no generator script: capture output from actual usage
echo '{"test": "input"}' | reference-tool process > fixtures/case_001.expected
echo '{"edge": "case"}' | reference-tool process > fixtures/case_002.expected
```

## Cross-Language Type Mapping

| Concept | Go | Python | Rust | Comparison Note |
|---------|-----|--------|------|----------------|
| Strings | `string` (UTF-8) | `str` (Unicode) | `String`/`&str` (UTF-8) | Usually identical |
| Byte arrays | `[]byte` | `bytes` | `Vec<u8>`/`&[u8]` | Direct mapping |
| Maps | `map[K]V` | `dict` | `HashMap<K,V>` | **Iteration order differs!** Sort before compare |
| Nil/None/null | `nil` | `None` | `Option::None` | Semantics vary — test boundary |
| Errors | `error` interface | Exceptions | `Result<T, E>` | Error message format will differ |
| Integers | `int` (platform) | `int` (arbitrary) | `i32`/`i64`/`usize` | Overflow behavior differs! |
| Floats | `float64` | `float` | `f64` | Use epsilon comparison |
| Time | `time.Time` | `datetime` | `chrono::DateTime` | Timezone handling differs |

### Comparison Functions

```rust
/// Compare outputs across languages with appropriate tolerance
fn cross_language_eq(reference: &Value, ours: &Value) -> bool {
    match (reference, ours) {
        // Floats: epsilon comparison (cross-language rounding)
        (Value::Float(a), Value::Float(b)) => (a - b).abs() < 1e-10,

        // Strings: normalize unicode (NFC) before comparison
        (Value::String(a), Value::String(b)) => {
            use unicode_normalization::UnicodeNormalization;
            a.nfc().eq(b.nfc())
        }

        // Maps: sort keys (Go/Python may iterate differently)
        (Value::Map(a), Value::Map(b)) => {
            let mut a_sorted: Vec<_> = a.iter().collect();
            let mut b_sorted: Vec<_> = b.iter().collect();
            a_sorted.sort_by_key(|(k, _)| k.clone());
            b_sorted.sort_by_key(|(k, _)| k.clone());
            a_sorted.len() == b_sorted.len()
                && a_sorted.iter().zip(b_sorted.iter()).all(|((ka, va), (kb, vb))| {
                    ka == kb && cross_language_eq(va, vb)
                })
        }

        // Arrays: element-wise comparison
        (Value::Array(a), Value::Array(b)) => {
            a.len() == b.len() && a.iter().zip(b.iter()).all(|(x, y)| cross_language_eq(x, y))
        }

        // Everything else: direct equality
        _ => reference == ours,
    }
}
```

## Common Cross-Language Divergences

| Category | Issue | Resolution |
|----------|-------|------------|
| **Unicode width** | Different Unicode version tables | ACCEPTED — document in DISCREPANCIES.md |
| **Map iteration order** | Go/Python maps are unordered | Sort before comparison |
| **Float formatting** | `1.0` vs `1` vs `1.00` | Parse to f64, compare numerically |
| **Error messages** | Different wording | Test error type/category, not message text |
| **Null representation** | `null` vs `None` vs `nil` | Normalize to a common representation |
| **Date formatting** | `2006-01-02` vs `%Y-%m-%d` | Parse to timestamp, compare epochs |
| **Line endings** | `\r\n` vs `\n` | Normalize to `\n` before comparison |
| **Trailing whitespace** | Some impls add trailing spaces | Trim lines before comparison |

## Real Examples from Our Projects

### charmed_rust (Go → Rust)

```
tests/conformance/fixtures/go_outputs/
├── lipgloss/
│   ├── border_rounded.golden      # Go: lipgloss.NewStyle().Border(lipgloss.RoundedBorder())
│   ├── style_padding.golden       # Go: lipgloss.NewStyle().Padding(1, 2)
│   └── style_bold_color.golden    # Go: lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("205"))
└── DISCREPANCIES.md               # DISC-001: Unicode width tables differ
```

### mcp_agent_mail_rust (Python → Rust)

```
crates/mcp-agent-mail-conformance/tests/conformance/fixtures/
├── python_reference.json          # Full MCP Agent Mail state from Python
├── share/
│   ├── expected_archive.json      # Python: share --mode archive
│   ├── expected_standard.json     # Python: share --mode standard
│   └── expected_strict.json       # Python: share --mode strict
└── tool_filter/
    ├── cases.json                 # Input cases for tool filtering
    └── profiles.json              # Expected filter results
```
