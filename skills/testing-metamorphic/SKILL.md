---
name: testing-metamorphic
description: >-
  Design and implement metamorphic testing for systems with the oracle problem.
  Use when: testing ML models, scientific computing, compilers, search engines,
  databases, graphics pipelines, or any system where correct output is unknown
  but input-output relationships are predictable. Metamorphic relations, property-based
  testing, MR taxonomy, oracle-free verification.
---

# Metamorphic Testing

> **The One Rule:** When you can't verify *what* the output is, verify *how* outputs
> relate to each other under known input transformations. Never guess at oracles.

## The Loop (Mandatory)

```
1. DIAGNOSE    → Is this an oracle problem? Can you compute expected output?
2. ENUMERATE   → List ALL domain properties as candidate MRs
3. CLASSIFY    → Score each MR: fault-sensitivity × independence × cost
4. IMPLEMENT   → One MR per test function, property-based input generation
5. COMPOSE     → Chain simple MRs into compound checks (multiplicative power)
6. VALIDATE    → Mutation testing: does each MR actually catch planted bugs?
7. ITERATE     → Failed MRs reveal both code bugs AND weak relation design
```

## MR Strength Matrix (Mandatory)

Before implementing, score every candidate metamorphic relation:

| MR Candidate | Fault Sensitivity (1-5) | Independence (1-5) | Cost (1-5) | Score |
|-------------|------------------------|--------------------:|------------|-------|
| *description* | How many bug classes? | Orthogonal to others? | ÷ Runtime | F×I/C |

**Rule:** Only implement Score ≥ 2.0. Low-scoring MRs waste test budget.

**Independence matters:** Two MRs that detect the same bug class are redundant.
An MR suite of 5 independent relations catches more than 20 correlated ones.

---

## The Oracle Problem — Decision Tree

```
Can you compute expected output for arbitrary inputs?
│
├─ YES → Use conventional testing (unit tests, assertions)
│
└─ NO → Is there a reference implementation?
    │
    ├─ YES → Use differential testing (conformance harness)
    │
    └─ NO → Do you know relationships between inputs/outputs?
        │
        ├─ YES → METAMORPHIC TESTING (this skill)
        │
        └─ NO → You need domain analysis first
```

**Examples of the oracle problem:**
- ML model: what's the "correct" sentiment of "The movie was not bad"?
- Search engine: what's the "correct" ranking of 10M documents?
- Compiler optimizer: does this optimization preserve semantics for ALL programs?
- Scientific simulation: is this fluid dynamics result correct to 6 decimal places?

---

## MR Taxonomy — The Six Fundamental Patterns

Every metamorphic relation falls into one of these categories. Master all six.

### 1. Equivalence (f(T(x)) = f(x))

The transformation shouldn't change the output at all.

```rust
/// Shuffling training data shouldn't change model accuracy
#[test]
fn mr_permutation_invariance() {
    proptest!(|(mut data: Vec<DataPoint>)| {
        let acc_original = model.train_and_evaluate(&data);
        data.shuffle(&mut thread_rng());
        let acc_shuffled = model.train_and_evaluate(&data);
        prop_assert!((acc_original - acc_shuffled).abs() < EPSILON,
            "Model accuracy changed by {:.4} after shuffling training data",
            (acc_original - acc_shuffled).abs());
    });
}
```

### 2. Additive (f(x + c) = f(x) + g(c))

Adding to input produces a predictable change in output.

```rust
/// Translating all points should translate the centroid
fn mr_centroid_translation(points: &[Point], offset: Vector) {
    let original_centroid = compute_centroid(points);
    let translated: Vec<Point> = points.iter()
        .map(|p| p + offset)
        .collect();
    let new_centroid = compute_centroid(&translated);
    assert_approx_eq!(new_centroid, original_centroid + offset);
}
```

### 3. Multiplicative (f(k·x) = h(k)·f(x))

Scaling input scales output by a related factor.

```rust
/// Doubling all prices should double total revenue
fn mr_revenue_linearity(transactions: &[Transaction], k: f64) {
    let original_revenue = compute_revenue(transactions);
    let scaled: Vec<Transaction> = transactions.iter()
        .map(|t| t.with_price(t.price * k))
        .collect();
    let scaled_revenue = compute_revenue(&scaled);
    assert_approx_eq!(scaled_revenue, original_revenue * k);
}
```

### 4. Permutative (f(permute(x)) = permute(f(x)))

Permuting input permutes output in a corresponding way.

```python
def test_mr_sort_commutes_with_map():
    """map(f, sort(xs)) == sort(map(f, xs)) for monotonic f"""
    @given(st.lists(st.integers()))
    def check(xs):
        f = lambda x: x * 2 + 1  # monotonically increasing
        assert list(map(f, sorted(xs))) == sorted(map(f, xs))
    check()
```

### 5. Inclusive/Exclusive (subset/superset/disjoint relations)

Restricting input restricts output; broadening input broadens output.

```rust
/// Adding a search term should return a SUBSET of results
fn mr_search_narrowing(engine: &SearchEngine, base_query: &str, extra_term: &str) {
    let broad_results = engine.search(base_query);
    let narrow_results = engine.search(&format!("{base_query} {extra_term}"));

    // Every result in narrow must also appear in broad
    for result in &narrow_results {
        assert!(broad_results.contains(result),
            "Narrowed search returned result not in broad search: {:?}", result);
    }
}

/// Complementary filters should be disjoint
fn mr_filter_disjoint(data: &[Record], predicate: &str) {
    let matching = filter(data, predicate);
    let non_matching = filter(data, &format!("NOT ({predicate})"));

    let intersection: Vec<_> = matching.iter()
        .filter(|r| non_matching.contains(r))
        .collect();
    assert!(intersection.is_empty(),
        "Complementary filters share {} records", intersection.len());
}
```

### 6. Invertive (f(T(T(x))) = f(x))

Applying the transformation twice returns to the original.

```rust
/// Encrypt then decrypt recovers plaintext
fn mr_crypto_roundtrip(plaintext: &[u8], key: &Key) {
    let ciphertext = encrypt(plaintext, key);
    let recovered = decrypt(&ciphertext, key);
    assert_eq!(plaintext, &recovered[..],
        "Encrypt-decrypt roundtrip failed");
}
```

---

## Composition: Multiplying MR Power

Simple MRs compose into exponentially stronger checks.

```rust
/// Composite MR: permutation invariance + scaling linearity + translation covariance
fn mr_composite_regression(model: &LinearModel, data: &Dataset) {
    let prediction_original = model.predict(data);

    // MR1: Permutation invariance (reorder samples)
    let shuffled = data.shuffled();
    let prediction_shuffled = model.predict(&shuffled);
    assert_approx_eq!(prediction_shuffled.mean(), prediction_original.mean());

    // MR2: Scaling linearity (scale features by k → scale predictions)
    let k = 2.0;
    let scaled = data.scale_features(k);
    let prediction_scaled = model.predict(&scaled);
    assert_approx_eq!(prediction_scaled.mean(), prediction_original.mean() * k);

    // MR3 = MR1 ∘ MR2: shuffle THEN scale (compound property)
    let shuffled_scaled = shuffled.scale_features(k);
    let prediction_compound = model.predict(&shuffled_scaled);
    assert_approx_eq!(prediction_compound.mean(), prediction_original.mean() * k);
}
```

**Composition rule:** If MR₁ and MR₂ are valid, then MR₁∘MR₂ is valid.
Compound MRs catch bugs that no individual MR detects.

---

## Domain-Specific MR Catalogs

### Database Engines (SQLancer-style)

```rust
/// TLP: Ternary Logic Partitioning
/// WHERE P ∪ WHERE NOT P ∪ WHERE P IS NULL = all rows
fn mr_tlp(db: &Database, table: &str, predicate: &str) {
    let all = db.query(&format!("SELECT * FROM {table}"));
    let t = db.query(&format!("SELECT * FROM {table} WHERE {predicate}"));
    let f = db.query(&format!("SELECT * FROM {table} WHERE NOT ({predicate})"));
    let n = db.query(&format!("SELECT * FROM {table} WHERE ({predicate}) IS NULL"));
    assert_eq!(all.len(), t.len() + f.len() + n.len());
}

/// NoREC: Non-optimizing Reference Engine Check
/// Unoptimized query result == optimized query result
fn mr_norec(db: &Database, query: &str) {
    let optimized = db.query(query);
    let unoptimized = db.query_no_optimize(query);
    assert_eq!(optimized, unoptimized);
}

/// PQS: Pivoted Query Synthesis
/// Insert row → query that matches row → must find it
fn mr_pqs(db: &Database, table: &str, row: &Row) {
    db.insert(table, row);
    let predicate = row.to_exact_match_predicate();
    let results = db.query(&format!("SELECT * FROM {table} WHERE {predicate}"));
    assert!(results.contains(row), "Inserted row not found by exact-match query");
}
```

### ML/AI Models

| MR | Property | Detects |
|----|----------|---------|
| Synonym substitution | f("great movie") ≈ f("excellent movie") | Fragile embeddings |
| Negation flip | sign(f("good")) ≠ sign(f("not good")) | Negation blindness |
| Irrelevant addition | f(x) ≈ f(x + " The sky is blue.") | Attention leaks |
| Paraphrase | f(x) ≈ f(paraphrase(x)) | Surface-form sensitivity |
| Label permutation | accuracy(shuffled_labels) ≈ chance | Memorization detection |

### Compilers/Interpreters

| MR | Transformation | Must Preserve |
|----|---------------|---------------|
| Dead code insertion | Add unreachable code | Output unchanged |
| Constant folding | Replace `2+3` with `5` | Semantics |
| Variable renaming | `x` → `y` everywhere | Behavior |
| Optimization toggle | `-O0` vs `-O2` | Observable output |
| Equivalent rewrites | `a*(b+c)` → `a*b+a*c` | Result |

---

## The Elicitation Prompt

When you're stuck finding MRs for an unfamiliar domain:

```text
I have a [SYSTEM TYPE] that takes [INPUT TYPE] and produces [OUTPUT TYPE].
I cannot compute expected outputs for arbitrary inputs (oracle problem).

List ALL metamorphic relations that MUST hold for a correct implementation.
For each MR:
1. Category (equivalence/additive/multiplicative/permutative/inclusive/invertive)
2. The exact transformation T(x)
3. The exact relation R between f(x) and f(T(x))
4. What bug class it catches
5. Confidence: would violation ALWAYS indicate a bug, or only sometimes?

Prioritize by fault sensitivity × independence. I want a DIVERSE set that
covers different aspects of correctness, not 10 variations of the same property.
```

---

## Validation: Does Your MR Suite Actually Work?

### Mutation Testing for MRs

Plant known bugs and verify your MRs catch them:

```rust
#[test]
fn validate_mr_suite_catches_planted_bugs() {
    let mutations = vec![
        ("off-by-one", |x: i32| x + 1),
        ("sign-flip", |x: i32| -x),
        ("zero-out", |_: i32| 0),
        ("double", |x: i32| x * 2),
    ];

    for (name, mutant) in &mutations {
        let caught = mr_suite_detects_mutation(mutant);
        assert!(caught,
            "MR suite failed to detect '{}' mutation — add a stronger MR", name);
    }
}
```

**Target:** Each planted mutation caught by ≥ 1 MR. If not, your suite has blind spots.

---

## Anti-Patterns (Hard Constraints)

| ✗ Never | Why | Fix |
|---------|-----|-----|
| Test f(x) = f(x) | Tautology, catches nothing | Need a TRANSFORMATION |
| Derive MRs from the code | Won't catch bugs in the logic you're testing | Derive from the SPEC or domain |
| Only test with edge cases | Metamorphic power comes from diverse random inputs | Use property-based generation |
| Skip floating-point epsilon | False failures kill trust in suite | `assert_approx_eq!` everywhere |
| Implement 10 correlated MRs | Same bug class detected 10x, others missed | Score for independence |
| No mutation validation | You don't know if MRs actually catch bugs | Plant bugs, verify detection |

---

## Checklist (Before Shipping MR Suite)

- [ ] Oracle problem confirmed (can't compute expected output)
- [ ] ≥ 5 independent MRs from ≥ 3 different categories
- [ ] Strength matrix scored: all implemented MRs have Score ≥ 2.0
- [ ] Property-based input generation (not handcrafted examples only)
- [ ] Mutation testing validates MR suite catches planted bugs
- [ ] Floating-point comparisons use epsilon tolerance
- [ ] Composite MRs tested (at least one chain of 2+ simple MRs)
- [ ] Each MR named after the property it verifies (not `test_mr_1`)

---

## References

| Need | Reference |
|------|-----------|
| MR catalog by domain | [MR-CATALOG.md](references/MR-CATALOG.md) |
| Composition patterns | [COMPOSITION.md](references/COMPOSITION.md) |
| Framework integration | [FRAMEWORKS.md](references/FRAMEWORKS.md) |
| Anti-patterns & mistakes | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| Copy-paste templates & decision matrix | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| Research foundations | [RESEARCH.md](references/RESEARCH.md) |

## Relationship to Other Testing Skills

| Technique | Use INSTEAD when | Use TOGETHER with MT when |
|-----------|-----------------|--------------------------|
| /testing-fuzzing | Finding crashes in parsers | Fuzzing generates source inputs, MRs validate relations |
| /testing-conformance-harnesses | Reference implementation exists | MRs supplement conformance where spec is ambiguous |
| /extreme-software-optimization | Performance, not correctness | MRs verify optimization doesn't change behavior |
| /alien-artifact-coding | Need formal proofs | MRs are the practical bridge between testing and proofs |
