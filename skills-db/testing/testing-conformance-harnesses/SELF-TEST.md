# Self-Test: testing-conformance-harnesses

## Positive Triggers (MUST activate)

- "Port this Go library to Rust — how do I verify correctness?"
- "conformance test" / "conformance suite" / "conformance harness"
- "Compare our implementation against the reference"
- "RFC compliance" / "spec compliance"
- "golden file testing with reference implementation"
- "Differential testing against Go/Python/C reference"
- "DISCREPANCIES.md"
- "Coverage matrix" / "compliance matrix"
- "Round-trip testing for wire compatibility"
- "Contract testing" / "Pact" / "Dredd" / "Hurl"
- "test262" / "WPT" / "Web Platform Tests"
- "How do I know my implementation matches the spec?"

## Negative Triggers (MUST NOT activate)

- "Test this ML model" (use /testing-metamorphic)
- "Find crashes in this parser" (use /testing-fuzzing)
- "Snapshot test CLI output" (use /testing-golden-artifacts — unless comparing to reference)
- "Set up mock-free database tests" (use /testing-real-service-e2e-no-mocks)
- "I can't compute the expected output" (use /testing-metamorphic — oracle problem)

## Boundary Cases

- "Golden file testing" → Activate if golden files come from a reference implementation; otherwise /testing-golden-artifacts
- "Differential testing" → Activate (primary pattern for conformance)
- "Round-trip" → Activate if testing format interop; use /testing-metamorphic if testing internal consistency only
- "Porting to Rust" → Activate alongside /porting-to-rust (conformance is PART of porting)
