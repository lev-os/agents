# Metamorphic Relation Catalog by Domain

> Scan this catalog after identifying the oracle problem. Select MRs from multiple categories for maximum fault diversity.

## Contents

1. [Database Engines](#database-engines)
2. [ML/AI Models](#mlai-models)
3. [Compilers/Interpreters](#compilersinterpreters)
4. [Search Engines](#search-engines)
5. [Scientific Computing](#scientific-computing)
6. [Graphics/Rendering](#graphicsrendering)
7. [Cryptography](#cryptography)
8. [Web Applications](#web-applications)
9. [Parsers/Serialization](#parsersserialization)

---

## Database Engines

### TLP: Ternary Logic Partitioning (SQLancer)

The most powerful database MR. For any predicate P:

```sql
-- These three queries MUST reconstruct the full table
SELECT * FROM t WHERE P
UNION ALL
SELECT * FROM t WHERE NOT P
UNION ALL
SELECT * FROM t WHERE P IS NULL
-- = SELECT * FROM t
```

```rust
fn mr_tlp(db: &Database, table: &str, predicate: &str) {
    let all = db.query(&format!("SELECT count(*) FROM {table}"));
    let t = db.query(&format!("SELECT count(*) FROM {table} WHERE {predicate}"));
    let f = db.query(&format!("SELECT count(*) FROM {table} WHERE NOT ({predicate})"));
    let n = db.query(&format!("SELECT count(*) FROM {table} WHERE ({predicate}) IS NULL"));
    assert_eq!(all, t + f + n, "TLP violation for predicate: {predicate}");
}
```

**Found bugs in:** SQLite, PostgreSQL, MySQL, CockroachDB, TiDB, DuckDB.

### NoREC: Non-optimizing Reference Engine Check

```rust
/// Optimizer must not change query results
fn mr_norec(db: &Database, query: &str) {
    let optimized = db.query(query);
    let unoptimized = db.query_no_optimize(query);
    assert_eq!(optimized, unoptimized, "NoREC: optimizer changed results");
}
```

### PQS: Pivoted Query Synthesis

```rust
/// Insert a known row → exact-match query MUST find it
fn mr_pqs(db: &Database, row: &Row) {
    db.insert("t", row);
    let predicate = row.to_exact_match_predicate(); // col1 = val1 AND col2 = val2 ...
    let results = db.query(&format!("SELECT * FROM t WHERE {predicate}"));
    assert!(results.contains(row), "PQS: inserted row not found");
}
```

### EET: Equivalent Expression Transformation

```sql
-- These pairs must produce identical results:
SELECT * FROM t WHERE a > 5          -- original
SELECT * FROM t WHERE NOT (a <= 5)   -- equivalent

SELECT * FROM t WHERE a BETWEEN 1 AND 10
SELECT * FROM t WHERE a >= 1 AND a <= 10
```

### Query-Level MR Table

| MR | Category | Transformation | Relation |
|----|----------|---------------|----------|
| TLP | Completeness | Split by predicate truth values | Union = full table |
| NoREC | Equivalence | Disable optimizer | Same results |
| PQS | Inclusive | Insert + query | Must find inserted row |
| EET | Equivalence | Rewrite expression | Same results |
| JOIN commutativity | Permutative | A JOIN B → B JOIN A | Same result set |
| WHERE push-down | Equivalence | Filter before/after join | Same results |
| Aggregate decomposition | Additive | SUM(a∪b) = SUM(a) + SUM(b) | Matches |

---

## ML/AI Models

### Invariance MRs (Output Unchanged)

| MR | Transformation | Domain | Catches |
|----|---------------|--------|---------|
| Synonym substitution | Replace words with synonyms | NLP/sentiment | Fragile embeddings |
| Paraphrase | Rephrase sentence structure | NLP/classification | Surface-form sensitivity |
| Image rotation (small) | Rotate ≤15° | Image classification | Orientation sensitivity |
| Background change | Replace irrelevant background | Object detection | Background bias |
| Feature reordering | Shuffle feature columns | Tabular ML | Feature order dependence |
| Training data shuffle | Permute training samples | Any ML | Non-deterministic training |

### Directional MRs (Output Changes Predictably)

| MR | Transformation | Expected Change | Catches |
|----|---------------|----------------|---------|
| Negation | "good" → "not good" | Polarity flips | Negation blindness |
| Scaling features | Multiply all by k | Proportional output | Non-linearity bugs |
| Adding noise | Inject small random noise | Output within ε | Fragility |
| Irrelevant addition | Add unrelated text | Output unchanged (≈) | Attention leaks |
| Demographic swap | Change gender/race | Output unchanged | Bias detection |

### LLM-Specific MRs (Meta-Fair framework)

```python
# MR: Swapping demographic attributes should not change response quality
def mr_fairness(llm, prompt, attr_a, attr_b):
    prompt_a = prompt.replace("{ATTR}", attr_a)
    prompt_b = prompt.replace("{ATTR}", attr_b)
    response_a = llm.generate(prompt_a)
    response_b = llm.generate(prompt_b)
    quality_a = evaluate_quality(response_a)
    quality_b = evaluate_quality(response_b)
    assert abs(quality_a - quality_b) < THRESHOLD, \
        f"Quality gap: {attr_a}={quality_a:.2f} vs {attr_b}={quality_b:.2f}"
```

---

## Compilers/Interpreters

| MR | Transformation | Preserves | Found Bugs In |
|----|---------------|-----------|---------------|
| Dead code insertion | Insert unreachable code | Program output | GCC: 147 bugs |
| Constant folding | Replace `2+3` with `5` | Semantics | LLVM: 132 bugs |
| Variable renaming | Rename all variables | Behavior | Obfuscator-LLVM |
| Single-iteration loop | Wrap in `for i in 0..1 {}` | Output | GraphicsFuzz (GPU drivers) |
| Optimization toggle | `-O0` vs `-O2` | Observable output | Many compilers |
| Equivalent rewrites | `a*(b+c)` → `a*b+a*c` | Result | CSmith |
| Double obfuscation | Obfuscate(obfuscate(P)) | Functional equivalence | Cobfusc, Tigress |

---

## Search Engines

| MR | Transformation | Relation | Found Bugs In |
|----|---------------|----------|---------------|
| Query restriction | Add AND term | Subset | Microsoft Live Search |
| Query broadening | Add OR term | Superset | Yahoo, Google |
| Empty result stable | Search gibberish | 0 results | General |
| Order independence | Swap term order | Same results | General |
| Duplicate query | Repeat same query | Identical results | Caching bugs |

**Classic bug:** Microsoft Live Search: `"GLIF"` returned 11,783 results, but `"GLIF OR 5Y4W"` returned 0.

---

## Scientific Computing

| MR | Transformation | Domain |
|----|---------------|--------|
| Scaling linearity | f(kx) = kf(x) | Linear systems |
| Translation covariance | f(x+c) = f(x) + c | Coordinate transforms |
| Rotation invariance | f(R(x)) = f(x) | Physics simulations |
| Symmetry | f(x,y) = f(y,x) | Distance metrics |
| Additivity | f(A∪B) = f(A) + f(B) | Partition functions |
| Conservation | sum(output) = sum(input) | Mass/energy conservation |
| Dimensional analysis | Scale units → scale output | Any physical computation |

---

## Graphics/Rendering (GraphicsFuzz)

Google acquired GraphicsFuzz (Imperial College London) for GPU driver testing.

**Method:** Apply semantics-preserving shader transformations → render both → compare images:

| Transformation | Description | What It Catches |
|---------------|-------------|----------------|
| Dead code injection | Add `if(false){ ... }` | Optimizer bugs |
| Single-iteration loops | Wrap in `for(int i=0;i<1;i++)` | Loop handling bugs |
| Live code wrapping | Wrap in `if(true){ ... }` | Control flow bugs |
| Equivalent math | `x → x*1.0` | Floating-point handling |
| Vector swizzle | `v.xyz → v.xyz` | Register allocation |

**Impact:** Found security vulnerabilities including **whole-phone reboot** on Samsung Galaxy S6 via valid WebGL.

---

## Cryptography

| MR | Transformation | Relation |
|----|---------------|----------|
| Round-trip | decrypt(encrypt(x, k), k) | = x |
| Key independence | encrypt(x, k1) vs encrypt(x, k2) | Different ciphertext |
| Avalanche | Flip 1 input bit | ~50% output bits flip |
| Determinism | encrypt(x, k) called twice | = identical ciphertext |
| Length preservation | len(encrypt(x)) | = len(x) + constant |

---

## Parsers/Serialization

| MR | Transformation | Relation |
|----|---------------|----------|
| Round-trip | parse(serialize(x)) | = x |
| Normalize round-trip | parse(pretty(parse(s))) | = parse(s) |
| Whitespace invariance | Add/remove whitespace | Same parsed result |
| Comment invariance | Add/remove comments | Same parsed result |
| Encoding round-trip | decode(encode(x)) | = x |
| Escape round-trip | unescape(escape(x)) | = x |

---

## Web Applications

| MR | Transformation | Relation |
|----|---------------|----------|
| Same-page reload | Refresh page | Same content |
| Login/logout round-trip | Login → logout → login | Same state |
| Concurrent access | Same request from 2 sessions | Consistent data |
| Idempotent GET | Repeat GET request | Same response |
| Filter composition | filter(A) ∩ filter(B) | = filter(A AND B) |

**NIST finding:** National Australia Bank login page bug found via simple MR (enter valid credentials → page should show dashboard, not error).
