# MT Quick Reference Card

## MR Design Checklist (30 seconds)

```
1. Is this an oracle problem? (Can't compute expected output) → YES → proceed
2. What domain properties MUST hold? (List 5+)
3. Classify each: Equiv / Additive / Mult / Permut / Inclusive / Invertive
4. Score: FaultSensitivity(1-5) × Independence(1-5) / Cost(1-5) ≥ 2.0?
5. Implement with proptest/Hypothesis/fast-check
6. Validate: mutation test catches planted bugs?
```

## Copy-Paste MR Templates

### Equivalence
```rust
proptest!(|(input: InputType)| {
    let original = f(&input);
    let transformed = f(&transform(&input));
    prop_assert_eq!(original, transformed, "Equivalence MR violated");
});
```

### Subset/Inclusive
```rust
proptest!(|(base: Query, restriction: Filter)| {
    let broad = search(&base);
    let narrow = search(&base.with_filter(&restriction));
    for item in &narrow {
        prop_assert!(broad.contains(item), "Subset MR violated: narrow result not in broad");
    }
});
```

### Round-Trip
```rust
proptest!(|(value: MyType)| {
    let encoded = serialize(&value);
    let decoded = deserialize(&encoded).unwrap();
    prop_assert_eq!(value, decoded, "Round-trip MR violated");
});
```

## When to Use Which Testing Skill

| Situation | Skill |
|-----------|-------|
| Can't compute expected output | **testing-metamorphic** (this) |
| Want to find crashes/memory bugs | /testing-fuzzing |
| Have a reference implementation | /testing-conformance-harnesses |
| Output too complex for assertions | /testing-golden-artifacts |
| Need real DB, not mocks | /testing-real-service-e2e-no-mocks |
| Browser-based E2E | /e2e-testing-for-webapps |
| Performance optimization | /extreme-software-optimization |
| Formal proofs | /lean-formal-feedback-loop |
