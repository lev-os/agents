# MR Composition & Strength Analysis

> Simple MRs compose into exponentially stronger checks. This reference covers composition strategies, strength scoring, and mutation-based validation.

## Composition Rules

### Chain Composition (MR₁ ∘ MR₂)

If MR₁ and MR₂ are independently valid, their sequential application is also valid:

```rust
fn mr_composite(data: &[f64]) {
    let original = compute(data);

    // MR1: Permutation invariance
    let mut shuffled = data.to_vec();
    shuffled.shuffle(&mut rng());
    let after_mr1 = compute(&shuffled);
    assert_approx_eq!(original, after_mr1);

    // MR2: Scaling linearity (applied to MR1's output)
    let k = 2.0;
    let scaled: Vec<f64> = shuffled.iter().map(|&x| x * k).collect();
    let after_mr1_mr2 = compute(&scaled);
    assert_approx_eq!(after_mr1_mr2, original * k);

    // MR1 ∘ MR2 = compound check: shuffle THEN scale
    // This catches bugs that neither MR catches alone
}
```

**Research finding (Chen et al.):** Composite MRs often detect faults that no individual component MR detects. However, composition ORDER matters — MR₁∘MR₂ may differ in fault detection from MR₂∘MR₁.

### Parallel Composition (MR₁ ∧ MR₂)

Both MRs must hold simultaneously for the same input pair:

```rust
fn mr_parallel_check(x: f64) {
    let y = f(x);

    // Both must hold
    assert!(y >= 0.0, "MR_nonneg: output must be non-negative");
    assert!((f(x + PERIOD) - y).abs() < EPS, "MR_periodic: must be periodic");
}
```

### Negation Composition (¬MR)

If MR holds for correct implementations, ¬MR should catch mutants:

```rust
fn validate_mr_catches_mutant(mutant_fn: fn(f64) -> f64, mr: fn(f64, f64) -> bool) -> bool {
    // If the MR is strong, it should fail for the mutant
    let x = random_input();
    let source_output = mutant_fn(x);
    let followup_output = mutant_fn(transform(x));
    !mr(source_output, followup_output) // MR should be violated
}
```

---

## MR Strength Scoring

### The Strength Matrix

| Factor | Weight | 1 (Low) | 3 (Medium) | 5 (High) |
|--------|--------|---------|------------|----------|
| **Fault sensitivity** | 3x | Catches 1 bug class | 3-5 bug classes | >5 bug classes |
| **Independence** | 2x | Same category as others | Partially overlapping | Orthogonal to all others |
| **Specificity** | 1x | Loose bound (output > 0) | Moderate (within 10%) | Exact (output = expected) |
| **Cost** | -1x | >100ms per check | 10-100ms | <10ms |

**Score = (Fault×3 + Independence×2 + Specificity×1) - Cost**

**Threshold:** Implement if Score ≥ 12. Discard if Score < 6.

### Independence Analysis

Two MRs are independent if they catch different bug classes:

```
MR_permutation: catches ordering bugs, initialization bugs
MR_scaling:     catches arithmetic bugs, overflow bugs
MR_roundtrip:   catches encoding bugs, precision bugs

Independence matrix:
              MR_perm  MR_scale  MR_round
MR_perm       -        HIGH      HIGH       → all independent
MR_scale      HIGH     -         MEDIUM     → partially overlapping
MR_round      HIGH     MEDIUM    -          → partially overlapping
```

---

## Mutation-Based MR Validation

### Step 1: Define Mutation Operators

```rust
enum Mutation {
    OffByOne(fn(i32) -> i32),     // |x| x + 1
    SignFlip(fn(i32) -> i32),     // |x| -x
    ZeroOut(fn(i32) -> i32),      // |_| 0
    DoubleValue(fn(i32) -> i32),  // |x| x * 2
    SwapArgs,                      // f(a, b) → f(b, a)
    DropElement,                   // Remove last element
    ConstantReturn,                // Always return same value
}
```

### Step 2: Run MR Suite Against Each Mutant

```rust
fn validate_mr_suite(mr_suite: &[MR], mutations: &[Mutation]) {
    let mut detection_matrix = vec![vec![false; mutations.len()]; mr_suite.len()];

    for (i, mr) in mr_suite.iter().enumerate() {
        for (j, mutation) in mutations.iter().enumerate() {
            let mutant = apply_mutation(original_fn, mutation);
            detection_matrix[i][j] = mr.detects_mutation(&mutant);
        }
    }

    // Each mutation should be caught by at least one MR
    for j in 0..mutations.len() {
        let caught = detection_matrix.iter().any(|row| row[j]);
        assert!(caught, "Mutation {:?} not caught by any MR", mutations[j]);
    }

    // Report coverage
    let total = mutations.len();
    let caught = (0..total).filter(|&j|
        detection_matrix.iter().any(|row| row[j])
    ).count();
    println!("Mutation detection: {caught}/{total} ({:.0}%)", 100.0 * caught as f64 / total as f64);
}
```

### Step 3: Identify Blind Spots

If a mutation class isn't caught:
1. Design a new MR targeting that bug class
2. Add it to the suite
3. Re-run validation
4. Repeat until all mutation classes are covered

---

## MR Coverage Metrics

### k-MR Coverage

A test input x achieves k-MR coverage if k distinct MRs have been exercised with x as a source test case.

**Target:** Every input in the corpus achieves ≥ 3-MR coverage.

```rust
fn measure_mr_coverage(inputs: &[Input], mr_suite: &[MR]) -> f64 {
    let mut covered = 0;
    for input in inputs {
        let mr_count = mr_suite.iter()
            .filter(|mr| mr.is_exercised_by(input))
            .count();
        if mr_count >= 3 { covered += 1; }
    }
    covered as f64 / inputs.len() as f64
}
```
