# Conformance Harness Architecture Guide

> How to build reusable harness infrastructure that scales to thousands of test cases.

## The ConformanceTest Trait Pattern (Rust)

From charmed_rust's real harness:

```rust
use serde::Serialize;

/// Every conformance test implements this trait.
pub trait ConformanceTest: Send + Sync {
    /// Human-readable test name
    fn name(&self) -> &str;

    /// Category for grouping
    fn category(&self) -> TestCategory;

    /// RFC 2119 requirement level
    fn requirement_level(&self) -> RequirementLevel;

    /// Spec section reference (e.g., "RFC7540-6.3")
    fn spec_ref(&self) -> &str;

    /// Execute the test
    fn run(&self, ctx: &TestContext) -> TestResult;

    /// Optional: benchmark comparison
    fn bench(&self, _ctx: &BenchContext) -> Option<BenchResult> { None }
}

#[derive(Debug, Clone, Copy, Serialize)]
pub enum TestCategory { Unit, Integration, EdgeCase, Performance }

#[derive(Debug, Clone, Copy, Serialize)]
pub enum RequirementLevel { Must, Should, May }

#[derive(Debug, Clone, Serialize)]
#[serde(tag = "status")]
pub enum TestResult {
    Pass,
    Fail { reason: String },
    Skipped { reason: String },
    ExpectedFailure { reason: String, discrepancy_id: String },
}
```

## Table-Driven Test Pattern

The most scalable pattern for spec-derived tests:

```rust
struct ConformanceCase {
    id: &'static str,
    section: &'static str,
    level: RequirementLevel,
    description: &'static str,
    input: &'static str,
    expected: Expected,
}

enum Expected {
    Ok(Value),
    Err,                           // Any error is acceptable
    ErrKind(&'static str),         // Specific error category
    XFail(&'static str),           // Known divergence (DISC-NNN)
}

const CASES: &[ConformanceCase] = &[
    ConformanceCase {
        id: "RFC7159-2.1",
        section: "2",
        level: RequirementLevel::Must,
        description: "A JSON text is a serialized value",
        input: "42",
        expected: Expected::Ok(Value::Number(42)),
    },
    // ... one per requirement
];
```

## Fixture Loading Architecture

```rust
pub struct FixtureLoader {
    base_path: PathBuf,
    reference_impl: String,  // "go", "python", etc.
    version: String,         // Reference impl version
}

impl FixtureLoader {
    pub fn load(&self, name: &str) -> Fixture {
        let input_path = self.base_path.join(name).with_extension("input");
        let expected_path = self.base_path.join(name).with_extension("expected");

        Fixture {
            name: name.to_string(),
            input: fs::read(&input_path).unwrap(),
            expected: fs::read_to_string(&expected_path).unwrap(),
            provenance: format!("{}@{}", self.reference_impl, self.version),
        }
    }

    pub fn load_all(&self, pattern: &str) -> Vec<Fixture> {
        glob::glob(&self.base_path.join(pattern).to_string_lossy())
            .unwrap()
            .filter_map(|path| {
                let path = path.ok()?;
                let name = path.file_stem()?.to_str()?;
                Some(self.load(name))
            })
            .collect()
    }
}
```

## Report Generator

```rust
fn generate_markdown_report(results: &[CaseResult]) -> String {
    let mut by_section: BTreeMap<&str, SectionStats> = BTreeMap::new();

    for r in results {
        let s = by_section.entry(r.section).or_default();
        match r.level {
            Must => { s.must_total += 1; if matches!(&r.verdict, Pass) { s.must_passed += 1; } }
            Should => { s.should_total += 1; if matches!(&r.verdict, Pass) { s.should_passed += 1; } }
            May => { s.may_total += 1; if matches!(&r.verdict, Pass) { s.may_passed += 1; } }
        }
        match &r.verdict {
            Pass => s.passed += 1,
            ExpectedFailure { .. } => s.xfail += 1,
            Fail { .. } => s.failed += 1,
            Skipped { .. } => s.skipped += 1,
        }
    }

    let mut report = String::from("# Conformance Report\n\n");
    report.push_str("| Section | MUST | SHOULD | MAY | Score |\n");
    report.push_str("|---------|------|--------|-----|-------|\n");

    for (section, stats) in &by_section {
        let must_score = if stats.must_total > 0 {
            format!("{}/{}", stats.must_passed, stats.must_total)
        } else { "N/A".into() };
        let score = stats.passed as f64 / stats.total() as f64 * 100.0;
        report.push_str(&format!(
            "| {} | {} | {}/{} | {}/{} | {:.1}% |\n",
            section, must_score,
            stats.should_passed, stats.should_total,
            stats.may_passed, stats.may_total,
            score,
        ));
    }
    report
}
```

## Process-Based Conformance (External Runner)

For testing against standard conformance suites:

```rust
fn run_conformance_suite(
    server_binary: &Path,
    suite_runner: &Path,
    config: &Path,
) -> ConformanceResult {
    // 1. Start the server under test
    let server = Command::new(server_binary)
        .arg("--port=0")
        .stdout(Stdio::piped())
        .spawn()
        .expect("Failed to start server");

    let port = read_port_from_stdout(server.stdout.as_ref().unwrap());

    // 2. Run the conformance suite against it
    let output = Command::new(suite_runner)
        .args(["--mode", "server"])
        .args(["--config", config.to_str().unwrap()])
        .args(["--host", &format!("localhost:{port}")])
        .output()
        .expect("Failed to run conformance suite");

    // 3. Parse results
    ConformanceResult {
        passed: output.status.success(),
        stdout: String::from_utf8_lossy(&output.stdout).to_string(),
        stderr: String::from_utf8_lossy(&output.stderr).to_string(),
    }
}
```

## Data-Driven Harness with datatest-stable

```rust
// Cargo.toml
// [[test]]
// name = "conformance"
// harness = false

fn run_test(path: &std::path::Path) -> datatest_stable::Result<()> {
    let input = std::fs::read_to_string(path)?;
    let case: ConformanceCase = serde_json::from_str(&input)?;
    let result = execute(&case.input);

    match (result, &case.expected) {
        (Ok(actual), Expected::Ok(expected)) => {
            assert_eq!(&actual, expected, "Output mismatch for {}", case.id);
        }
        (Err(_), Expected::Err) => { /* Both reject — pass */ }
        (Err(e), Expected::Ok(_)) => {
            panic!("Expected success but got error: {e}");
        }
        (Ok(actual), Expected::Err) => {
            panic!("Expected error but got: {actual:?}");
        }
        (_, Expected::XFail(disc_id)) => {
            // Known divergence — pass with note
        }
    }
    Ok(())
}

datatest_stable::harness! {
    { test = run_test, root = "tests/fixtures", pattern = r"\.json$" }
}
```
