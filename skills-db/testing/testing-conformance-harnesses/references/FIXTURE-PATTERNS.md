# Fixture Management Patterns

> Fixtures are the bridge between specification and verification. Their provenance, organization, and maintenance determine conformance suite reliability.

## Directory Layout

```
tests/conformance/
├── fixtures/
│   ├── PROVENANCE.md              # HOW fixtures were generated (mandatory)
│   ├── go_outputs/                # From Go reference impl
│   │   ├── feature_a/
│   │   │   ├── basic.golden
│   │   │   ├── edge_empty.golden
│   │   │   └── edge_unicode.golden
│   │   └── feature_b/
│   ├── python_reference.json      # From Python reference impl
│   ├── rfc_vectors/               # From RFC test vectors
│   │   ├── section_4.1/
│   │   └── section_7.2/
│   └── protocol/                  # Protocol test data
│       ├── valid_handshake.bin
│       └── invalid_handshake.bin
├── DISCREPANCIES.md               # Known divergences
└── COVERAGE.md                    # What's tested vs not
```

## PROVENANCE.md Template (Mandatory)

```markdown
# Fixture Provenance

## Go Reference Outputs

- **Generator:** `go run ./cmd/gen-fixtures > fixtures/go_outputs/`
- **Go version:** 1.22.1
- **Library version:** v0.15.2 (git ref: abc123)
- **Generated:** 2026-03-15
- **Regeneration command:**
  ```bash
  cd /path/to/go-reference
  git checkout v0.15.2
  go run ./cmd/gen-fixtures --output /path/to/tests/conformance/fixtures/go_outputs/
  ```

## Python Reference Fixtures

- **Generator:** `python -m my_lib.conformance.generate`
- **Python version:** 3.12.1
- **Library version:** 0.9.1 (pip install my-lib==0.9.1)
- **Generated:** 2026-03-10

## RFC Test Vectors

- **Source:** RFC 7539 Appendix A
- **Copied from:** https://www.rfc-editor.org/rfc/rfc7539#appendix-A
- **Verified date:** 2026-03-01
```

## DISCREPANCIES.md Template

```markdown
# Known Conformance Divergences

All intentional differences from the reference implementation.
Each divergence is ACCEPTED, INVESTIGATING, or WILL-FIX.
Tests for accepted divergences use XFAIL, not SKIP.

## DISC-001: Unicode Width Tables
- **Reference:** Unicode 13.0 tables (go-runewidth v0.14)
- **Our impl:** Unicode 15.1 tables (unicode-width v0.2)
- **Impact:** Some CJK characters have different widths
- **Resolution:** ACCEPTED — newer tables are more correct
- **Tests affected:** `lipgloss/cjk_alignment_*`
- **Review date:** 2026-03-15

## DISC-002: Error Message Format
- **Reference:** Returns "invalid at byte 42"
- **Our impl:** Returns "parse error at offset 42"
- **Impact:** Error strings differ (semantics identical)
- **Resolution:** ACCEPTED — test error types, not messages
- **Tests affected:** `parser/error_*`
- **Review date:** 2026-03-15
```

## Fixture Naming Convention

| Pattern | Meaning |
|---------|---------|
| `feature/basic.golden` | Happy-path test for feature |
| `feature/edge_empty.golden` | Edge case: empty input |
| `feature/edge_max.golden` | Edge case: maximum input |
| `feature/error_invalid.golden` | Error case: invalid input |
| `feature/error_malformed.golden` | Error case: malformed data |
| `feature/regression_123.golden` | Regression from issue #123 |

## JSON Schema Test Suite Format

The canonical format for data-driven conformance (from json-schema-org):

```json
[
  {
    "description": "Human-readable group name",
    "schema": { /* the specification */ },
    "tests": [
      {
        "description": "Individual test description",
        "data": /* input */,
        "valid": true
      },
      {
        "description": "Invalid case",
        "data": /* bad input */,
        "valid": false
      }
    ]
  }
]
```

## Fixture Regeneration Workflow

```bash
# 1. Check reference impl version
cd /path/to/reference && git log -1 --oneline

# 2. Regenerate fixtures
go run ./cmd/gen-fixtures --output /path/to/fixtures/go_outputs/

# 3. Diff against existing
diff -r fixtures/go_outputs/ fixtures/go_outputs.bak/

# 4. Review EVERY change
# If changes are expected (new features) → accept
# If changes are unexpected → investigate before accepting

# 5. Update PROVENANCE.md with new version info

# 6. Commit with clear message
git add fixtures/ PROVENANCE.md
git commit -m "Regenerate fixtures from go-reference v0.16.0"
```

## Cross-Implementation Round-Trip Fixtures

For formats that must interoperate:

```
fixtures/
├── generated_by_go/
│   ├── message_a.bin     # Go serialized this
│   └── message_b.bin
├── generated_by_rust/
│   ├── message_a.bin     # Rust serialized this
│   └── message_b.bin
└── cross_validation.json # Expected parsed values for both
```

Test matrix:
```
go_serialized  → go_parser   = PASS (baseline)
go_serialized  → rust_parser = MUST PASS (conformance)
rust_serialized → go_parser   = MUST PASS (interop)
rust_serialized → rust_parser = PASS (baseline)
```
