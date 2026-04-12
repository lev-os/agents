# Self-Test: testing-metamorphic

## Positive Triggers (MUST activate)

- "How do I test this ML model? I can't compute the expected output"
- "oracle problem"
- "metamorphic testing"
- "metamorphic relation"
- "property-based testing for this scientific computation"
- "I need to test this search engine but I don't know the correct ranking"
- "How do I verify this compiler optimization doesn't change semantics?"
- "The output is correct but I can't prove it — how do I test?"
- "Test this database query engine for logic bugs"

## Negative Triggers (MUST NOT activate)

- "Write unit tests for this function" (use standard testing)
- "Find crashes in my parser" (use /testing-fuzzing)
- "Compare my Rust port against the Go reference" (use /testing-conformance-harnesses)
- "Snapshot test this CLI output" (use /testing-golden-artifacts)
- "Set up real database tests" (use /testing-real-service-e2e-no-mocks)
- "Fuzz this serialization code" (use /testing-fuzzing)
- "Profile this slow function" (use /extreme-software-optimization)

## Boundary Cases

- "Property-based testing" → Activate (MRs are a type of property)
- "Round-trip testing" → Activate only if oracle problem exists; otherwise /testing-conformance-harnesses
- "Differential testing" → Activate only if no reference impl; otherwise /testing-conformance-harnesses
