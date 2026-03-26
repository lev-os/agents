# Self-Test: testing-golden-artifacts

## Positive Triggers (MUST activate)

- "snapshot testing" / "snapshot test"
- "golden file" / "golden master"
- "insta" (Rust snapshot crate)
- "toMatchSnapshot" / "toMatchInlineSnapshot" / "toMatchFileSnapshot"
- "approval testing"
- "characterization testing"
- "The output is too complex to assert field-by-field"
- "CLI output regression testing"
- "Query plan golden testing"
- "UPDATE_GOLDENS" / "INSTA_UPDATE"
- "cargo insta review"
- "How do I test this rendered output?"
- "Scrub timestamps from test output"

## Negative Triggers (MUST NOT activate)

- "Compare against reference implementation" (use /testing-conformance-harnesses)
- "Find crashes" (use /testing-fuzzing)
- "Oracle problem" (use /testing-metamorphic)
- "Mock-free database tests" (use /testing-real-service-e2e-no-mocks)
- "Property-based testing" (use /testing-metamorphic or /testing-fuzzing)

## Boundary Cases

- "Snapshot test this API response" → Activate
- "Compare this against the Go reference output" → Use /testing-conformance-harnesses (reference impl is the oracle)
- "Freeze this compiler output for regression" → Activate (characterization testing)
- "Visual regression testing" → Activate for image/screenshot goldens
