# Structured Test Logging Formats

> When a test fails in CI, you need: WHAT happened, WHEN, and the DB state. Not just "assertion failed".

## JSON-Line Format (Our Standard)

Every line is a self-contained JSON object to stderr:

```json
{"ts":"2026-03-23T07:10:11Z","level":"info","suite":"billing","test":"checkout flow","phase":"setup","event":"test_start"}
{"ts":"2026-03-23T07:10:11Z","level":"debug","suite":"billing","test":"checkout flow","phase":"setup","event":"db_snapshot","data":{"table":"users","row_count":1}}
{"ts":"2026-03-23T07:10:11Z","level":"debug","suite":"billing","test":"checkout flow","phase":"act","event":"phase_start"}
{"ts":"2026-03-23T07:10:11Z","level":"debug","suite":"billing","test":"checkout flow","phase":"assert","event":"assertion","data":{"field":"status","expected":"active","actual":"active","match":true}}
{"ts":"2026-03-23T07:10:11Z","level":"info","suite":"billing","test":"checkout flow","event":"test_end","data":{"result":"pass","duration_ms":45}}
```

## TestLogger API

```typescript
export class TestLogger {
    testStart(name: string): void;
    phase(p: "setup" | "act" | "assert" | "teardown"): void;
    dbSnapshot(table: string, rows: unknown[], label?: string): void;
    assertMatch(field: string, expected: unknown, actual: unknown): boolean;
    testEnd(result: "pass" | "fail" | "skip"): void;
    summary(): SuiteSummary;
}

// Auto-hook into Vitest lifecycle:
export function withTestLogging(suite: string): TestLogger;
```

## Vitest Built-In Reporters

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    reporters: [
      "default",                                         // Terminal
      ["json", { outputFile: "./reports/results.json" }], // Machine
      ["junit", { suiteName: "integration-tests" }],     // CI systems
      process.env.GITHUB_ACTIONS ? "github-actions" : [], // GH annotations
    ].flat(),
  },
});
```

| Reporter | Format | Use |
|----------|--------|-----|
| `default` | Terminal | Local dev |
| `verbose` | Per-test terminal | Debugging |
| `json` | JSON file | Dashboards |
| `junit` | XML | Jenkins, GitLab, Azure |
| `github-actions` | GH commands | PR annotations |
| `html` | HTML | Visual exploration |

## Rust: nextest

```bash
cargo nextest run --message-format libtest-json  # JSON stream
cargo nextest run --profile ci                   # JUnit XML output
```

```toml
# .config/nextest.toml
[profile.ci]
retries = 2
fail-fast = false

[profile.ci.junit]
path = "target/nextest/ci/junit.xml"
report-name = "integration-tests"
```

## Log Level Configuration

```bash
# Default: info (shows test lifecycle only)
LOG_LEVEL=info bun test

# Debug: includes phase timing, DB snapshots, assertions
LOG_LEVEL=debug bun test

# Trace: includes full DB row data in snapshots
LOG_LEVEL=trace bun test

# CI: info + JSON reporter
CI=true LOG_LEVEL=info bun test
```
