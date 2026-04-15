# Self-Test: testing-fuzzing

## Positive Triggers (MUST activate)

- "Fuzz this parser"
- "cargo-fuzz" / "cargo fuzz" / "libfuzzer"
- "Find crashes in this code"
- "Security audit this input processing"
- "Write a fuzz target for this"
- "Structure-aware fuzzing"
- "Differential fuzzing"
- "AFL++" / "honggfuzz" / "bolero"
- "AddressSanitizer" / "ASan" / "sanitizer"
- "How do I fuzz this protocol?"
- "Corpus management" / "seed corpus"
- "This parser handles untrusted input — how do I test it?"

## Negative Triggers (MUST NOT activate)

- "Test this ML model" (use /testing-metamorphic)
- "Compare against reference implementation" (use /testing-conformance-harnesses)
- "Snapshot test this output" (use /testing-golden-artifacts)
- "Mock-free database tests" (use /testing-real-service-e2e-no-mocks)
- "Write unit tests" (standard testing)
- "Optimize this slow function" (use /extreme-software-optimization)
- "Formal verification" / "prove this correct" (use /lean-formal-feedback-loop)

## Boundary Cases

- "proptest" → Activate (proptest is a fuzzing/PBT framework)
- "fast-check" → Activate (property-based testing is fuzzing-adjacent)
- "Round-trip testing" → Activate if testing serialization robustness; otherwise /testing-conformance-harnesses
- "Find bugs in this code" → Activate if input-processing code; otherwise /multi-pass-bug-hunting
