# MT Anti-Patterns & Common Mistakes

> Each anti-pattern includes the bug it hides and the fix.

## Anti-Pattern 1: Tautological MRs

```rust
// WRONG: Tests nothing — always passes
fn mr_tautology(x: f64) {
    let y1 = f(x);
    let y2 = f(x);
    assert_eq!(y1, y2); // f(x) = f(x) is always true for deterministic f
}

// RIGHT: Apply a TRANSFORMATION
fn mr_periodicity(x: f64) {
    let y1 = f(x);
    let y2 = f(x + 2.0 * PI);
    assert_approx_eq!(y1, y2);
}
```

**Why it matters:** Tautological MRs create false confidence. They pass for both correct and incorrect implementations.

## Anti-Pattern 2: Implementation-Derived MRs

```rust
// WRONG: MR mirrors the implementation
fn mr_mirrors_code(data: &[f64]) {
    // This is just re-implementing the function, not testing a property
    let expected = data.iter().sum::<f64>() / data.len() as f64;
    assert_eq!(mean(data), expected);
}

// RIGHT: Derive from DOMAIN knowledge
fn mr_mean_scaling(data: &[f64], k: f64) {
    // Mathematical property: mean(k*data) = k*mean(data)
    let original = mean(data);
    let scaled: Vec<f64> = data.iter().map(|&x| x * k).collect();
    assert_approx_eq!(mean(&scaled), original * k);
}
```

**Why it matters:** If the MR tests the same logic as the implementation, bugs in that logic will satisfy both.

## Anti-Pattern 3: Too Few MRs

```rust
// WRONG: Single MR covers one dimension
#[test]
fn only_one_mr() {
    proptest!(|(data: Vec<i32>)| {
        // Only testing idempotency — misses element preservation, stability, etc.
        let mut d = data.clone();
        d.sort();
        let once = d.clone();
        d.sort();
        prop_assert_eq!(d, once);
    });
}

// RIGHT: Multiple independent MRs
// MR1: Idempotency (sort(sort(x)) = sort(x))
// MR2: Preservation (sort(x) is a permutation of x)
// MR3: Ordering (sort(x)[i] <= sort(x)[i+1])
// MR4: Additive (sort(x ++ [min-1]) puts new element first)
// MR5: Subset (sort(x) contains all elements of x)
```

**Why it matters:** NIST showed each of their 4 MRs found DIFFERENT bugs. Single MRs have blind spots.

## Anti-Pattern 4: Ignoring Floating-Point

```rust
// WRONG: Exact comparison for floats
fn mr_wrong_float(x: f64) {
    assert_eq!(sin(x), sin(PI - x)); // Fails due to floating-point!
}

// RIGHT: Epsilon comparison
fn mr_right_float(x: f64) {
    assert!((sin(x) - sin(PI - x)).abs() < 1e-10);
}

// BEST: Relative epsilon for scale-invariance
fn mr_best_float(x: f64) {
    let a = sin(x);
    let b = sin(PI - x);
    let eps = f64::max(a.abs(), b.abs()) * 1e-12 + 1e-15;
    assert!((a - b).abs() < eps);
}
```

## Anti-Pattern 5: Only Testing Edge Cases

```python
# WRONG: Hand-picked edge cases only
def test_mr_edge_cases():
    assert_mr_holds(f, [0])       # empty-ish
    assert_mr_holds(f, [1])       # single
    assert_mr_holds(f, [1, 2])    # pair

# RIGHT: Property-based generation covers diverse inputs
@given(st.lists(st.integers(), min_size=1, max_size=1000))
def test_mr_diverse(data):
    assert_mr_holds(f, data)
```

**Why it matters:** Metamorphic testing's power comes from DIVERSE random inputs, not curated examples. Many bugs only manifest with specific data patterns that humans wouldn't think to test.

## Anti-Pattern 6: No Mutation Validation

```rust
// WRONG: Assume MRs catch bugs without evidence
fn mr_untested() {
    // Looks good, but does it actually catch real bugs?
    assert_eq!(sort(&permute(data)), sort(data));
}

// RIGHT: Plant bugs, verify MR catches them
#[test]
fn validate_mr_catches_off_by_one() {
    let mutant = |data: &[i32]| -> Vec<i32> {
        let mut result = data.to_vec();
        result.sort();
        result.pop(); // Bug: drops last element
        result
    };
    // MR_preservation should catch this
    let data = vec![3, 1, 4, 1, 5];
    let sorted = mutant(&data);
    assert_ne!(sorted.len(), data.len(), "MR should detect dropped element");
}
```

## Anti-Pattern 7: Correlated MRs Masquerading as Diverse Suite

```
// WRONG: All MRs test the same property from slightly different angles
MR1: sort(reverse(x)) = sort(x)         // Permutation invariance
MR2: sort(shuffle(x)) = sort(x)          // Permutation invariance
MR3: sort(rotate(x)) = sort(x)           // Permutation invariance
MR4: sort(swap_first_last(x)) = sort(x)  // Permutation invariance
// These are all the SAME property — 4 variants of permutation invariance

// RIGHT: Each MR tests a DIFFERENT property
MR1: Permutation invariance (sort(permute(x)) = sort(x))
MR2: Element preservation (sort(x) is a permutation of x)
MR3: Monotonicity (sort(x)[i] <= sort(x)[i+1])
MR4: Minimum placement (sort(x ++ [min-1])[0] = min-1)
MR5: Stability (equal elements preserve relative order in stable sort)
```

**Fix:** Use the Independence column in the Strength Matrix. If two MRs would catch the same mutation set, they're correlated — keep only the stronger one.

## Anti-Pattern 8: MRs as Specification Substitutes

```python
# WRONG: "My MR suite passes, so the code is correct"
# MRs are NECESSARY conditions, not SUFFICIENT conditions
# A function that always returns 0 satisfies sin(x) = sin(x)

# RIGHT: MRs augment other testing methods
# Use MRs WHERE you can't use assertions (oracle problem)
# Use assertions WHERE you can (known expected values)
# Use both for maximum coverage
```
