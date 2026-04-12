# Conformance Harnesses in Our Projects

> Real-world examples from this codebase. Copy these patterns.

## charmed_rust (Go → Rust Port)

**What:** Rust reimplementation of Go's Charmbracelet TUI libraries.
**Conformance strategy:** Golden file comparison against Go reference outputs.

```
tests/conformance/
├── src/
│   ├── harness/
│   │   ├── traits.rs       # ConformanceTest trait (TestCategory, TestResult)
│   │   ├── runner.rs       # Collects + runs all tests
│   │   ├── fixtures.rs     # Golden file loader
│   │   ├── comparison.rs   # Byte-level + structural comparison
│   │   ├── context.rs      # Test state, temp dirs, paths
│   │   ├── logging.rs      # JSON-line structured output
│   │   └── benchmark.rs    # Performance comparison vs Go
│   └── bin/
│       ├── run_conformance.rs
│       └── generate_report.rs
├── fixtures/
│   └── go_outputs/
│       └── lipgloss/
│           ├── border_rounded.golden
│           └── style_padding.golden
└── DISCREPANCIES.md
```

**Key pattern:** Trait-based harness where each test implements `ConformanceTest`. Tests are discovered automatically. Report generator produces a Markdown compliance matrix.

---

## mcp_agent_mail_rust (Python → Rust Port)

**What:** Rust reimplementation of Python MCP Agent Mail server.
**Conformance strategy:** JSON fixture comparison against Python reference outputs.

```
crates/mcp-agent-mail-conformance/
├── tests/conformance/
│   ├── fixtures/
│   │   ├── python_reference.json     # Python generated this
│   │   ├── cli/
│   │   │   └── legacy_cli_inventory.json
│   │   ├── share/
│   │   │   ├── expected_archive.json
│   │   │   ├── expected_scoped.json
│   │   │   ├── expected_standard.json
│   │   │   └── expected_strict.json
│   │   └── tool_filter/
│   │       ├── cases.json
│   │       ├── custom_filter.json
│   │       └── profiles.json
│   └── conformance.rs
```

**Key pattern:** Fixtures organized by feature area. Each fixture is a JSON file with input + expected output. Test file loads all fixtures and runs them as parameterized tests.

---

## frankentorch (PyTorch → Rust)

**What:** Rust reimplementation of PyTorch tensor operations.
**Conformance strategy:** Differential testing against Python/NumPy.

```
artifacts/phase2c/conformance/
└── differential_report_v1.json
```

**Key pattern:** Generates a differential report by running the same operations in both implementations and comparing results with floating-point tolerance.

---

## frankensqlite (SQLite Reimplementation)

**What:** Rust reimplementation of SQLite from scratch.
**Conformance strategy:** Differential testing against real SQLite + fuzz testing.

```
fuzz/fuzz_targets/
├── fuzz_expr_parser.rs
├── fuzz_lexer.rs
├── fuzz_record_roundtrip.rs
└── fuzz_sql_parser.rs

tests/conformance/   # (via conformance tests)
```

**Key pattern:** Combines:
1. Round-trip fuzzing (serialize → parse must round-trip)
2. Differential fuzzing (compare against real SQLite)
3. SQL Logic Test execution (7.2M queries from SQLite's SLT)

**The fuzz_record_roundtrip.rs pattern** is the template for round-trip fuzzing:
```rust
fuzz_target!(|input: FuzzInput| {
    // Strategy 1: raw bytes → must not panic
    let _ = parse_record(&input.raw);

    // Strategy 2: structured → must round-trip
    let values = input.values.iter().map(|v| v.to_sqlite_value()).collect();
    let serialized = serialize_record(&values);
    let deserialized = parse_record(&serialized)
        .expect("Cannot parse our own output");
    assert_eq!(values, deserialized);
});
```

---

## Lessons from Our Projects

| Lesson | Source |
|--------|--------|
| Trait-based harness scales to thousands of tests | charmed_rust |
| JSON fixtures are more maintainable than binary | mcp_agent_mail_rust |
| Floating-point needs epsilon comparison | frankentorch |
| Round-trip fuzzing catches serialization bugs fast | frankensqlite |
| DISCREPANCIES.md prevents "is this a bug or intentional?" debates | All projects |
| Fixture provenance prevents "where did these goldens come from?" | All projects |
| Compliance matrices give instant visibility into coverage gaps | charmed_rust |
