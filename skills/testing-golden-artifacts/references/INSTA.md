# insta Crate Complete Reference

> The gold standard for snapshot testing in Rust. By Armin Ronacher (mitsuhiko).

## Assertion Macros

| Macro | Format | Best For |
|-------|--------|---------|
| `assert_snapshot!` | Plain text | CLI output, rendered strings |
| `assert_debug_snapshot!` | Debug trait | Rust structs, enums |
| `assert_yaml_snapshot!` | YAML (serde) | Nested data structures |
| `assert_json_snapshot!` | JSON (serde) | API responses |
| `assert_compact_debug_snapshot!` | Single-line Debug | Simple values |
| `assert_csv_snapshot!` | CSV | Tabular data |

## Snapshot Types

### File Snapshots (default)

Stored in `<crate>/src/snapshots/<module>__<test_name>.snap`:

```
---
source: src/parser/tests.rs
expression: parse("1 + 2")
---
BinOp(Add, Literal(1), Literal(2))
```

### Inline Snapshots

Golden value embedded in source:

```rust
assert_snapshot!(value, @"");  // insta fills this in
// becomes:
assert_snapshot!(value, @"expected value here");
```

### Named Snapshots

```rust
assert_snapshot!("my-custom-name", value);
```

---

## Redactions (Path-Based Scrubbing)

```rust
// Redact specific fields in structured data
assert_yaml_snapshot!(response, {
    ".id" => "[uuid]",
    ".created_at" => "[timestamp]",
    ".updated_at" => "[timestamp]",
    ".**.secret" => "[redacted]",     // ** = any depth
    ".items[].id" => "[id]",          // Array elements
});

// Dynamic redaction with validation
assert_yaml_snapshot!(user, {
    ".id" => insta::dynamic_redaction(|value, _path| {
        uuid::Uuid::parse_str(value.as_str().unwrap()).unwrap();
        "[uuid]"
    }),
});

// Sort non-deterministic collections
assert_yaml_snapshot!(data, {
    ".tags" => insta::sorted_redaction(),
});
```

---

## Filters (Regex-Based Scrubbing for Text)

```rust
use insta::Settings;

let mut settings = Settings::clone_current();

// Replace timestamps
settings.add_filter(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?",
    "[timestamp]"
);

// Replace UUIDs
settings.add_filter(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "[uuid]"
);

// Replace memory addresses
settings.add_filter(r"0x[0-9a-f]+", "[addr]");

// Replace durations
settings.add_filter(r"\d+(\.\d+)?\s*(ms|us|ns|s)", "[duration]");

// Replace absolute paths
settings.add_filter(r"/home/[^/]+/", "/HOME/");

settings.bind(|| {
    assert_snapshot!(output);
});
```

---

## Glob Testing (Many Inputs → Many Snapshots)

```rust
#[test]
fn test_all_fixtures() {
    insta::glob!("fixtures/inputs/*.txt", |path| {
        let input = std::fs::read_to_string(path).unwrap();
        let output = process(&input);
        assert_snapshot!(output);
    });
}
// Creates one snapshot per input file
```

---

## Settings API

```rust
let mut settings = Settings::clone_current();
settings.set_snapshot_path("custom_snapshots/");
settings.set_prepend_module_to_snapshot(false);
settings.set_sort_maps(true);
settings.set_info(&json!({ "version": "2.0" }));
settings.bind(|| { ... });
```

---

## CLI Tool: cargo-insta

```bash
cargo insta review          # Interactive TUI: accept/reject
cargo insta accept          # Accept all pending
cargo insta reject          # Reject all pending
cargo insta test --review   # Run tests + review
cargo insta test --accept-unseen  # Accept new snapshots only
```

---

## INSTA_UPDATE Environment Variable

| Value | Behavior | Use When |
|-------|----------|----------|
| `auto` | Write `.snap.new`, don't overwrite | Default (local dev) |
| `always` | Overwrite all snapshots | Bulk update after refactor |
| `new` | Only write new, fail on mismatches | Adding new tests |
| `no` | Never write, fail on mismatch | **CI (mandatory)** |
| `unseen` | Like auto + flag unreferenced | Cleanup stale snapshots |

```yaml
# CI: always use strict mode
- run: cargo test
  env:
    INSTA_UPDATE: "no"
```

---

## expect_test (Alternative: Inline Only)

From rust-analyzer team. Rewrites source code on `UPDATE_EXPECT=1`:

```rust
use expect_test::expect;

#[test]
fn test_parser() {
    let ast = parse("1 + 2 * 3");
    let expected = expect![[r#"
        BinOp(Add, Literal(1), BinOp(Mul, Literal(2), Literal(3)))
    "#]];
    expected.assert_eq(&format!("{ast:#?}"));
}
```

```bash
UPDATE_EXPECT=1 cargo test  # Auto-update inline expected values
```

---

## goldenfile Crate (Simple File Comparison)

```rust
use goldenfile::Mint;

#[test]
fn test_output() {
    let mut mint = Mint::new("tests/goldenfiles");
    let mut f = mint.new_goldenfile("output.txt").unwrap();
    write!(f, "Hello, world!").unwrap();
    // Mint compares on drop
}
```

```bash
REGENERATE_GOLDENFILES=1 cargo test  # Update goldens
```
