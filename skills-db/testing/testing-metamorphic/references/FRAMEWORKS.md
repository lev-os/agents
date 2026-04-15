# MT Framework Integration Guide

> How to implement metamorphic testing with existing PBT frameworks.

## Contents

1. [Rust: proptest](#rust-proptest)
2. [Python: Hypothesis + GeMTest](#python-hypothesis--gemtest)
3. [TypeScript: fast-check](#typescript-fast-check)
4. [Go: rapid](#go-rapid)
5. [Java/Kotlin: jqwik](#javakotlin-jqwik)
6. [Framework Comparison](#framework-comparison)

---

## Rust: proptest

proptest is the natural home for MRs in Rust. Each MR becomes a property.

```rust
use proptest::prelude::*;

// Strategy: generate domain-specific inputs
fn search_query_strategy() -> impl Strategy<Value = (String, String)> {
    (
        "[a-z]{3,10}",           // base query
        "[a-z]{3,10}",           // additional term
    )
}

proptest! {
    // MR: Narrowing a search returns a subset
    #[test]
    fn mr_search_narrowing(
        (base, extra) in search_query_strategy()
    ) {
        let broad = search_engine::search(&base);
        let narrow = search_engine::search(&format!("{base} {extra}"));

        // Every narrow result must appear in broad results
        for result in &narrow {
            prop_assert!(
                broad.contains(result),
                "Narrow result {:?} not in broad results", result
            );
        }
    }

    // MR: Sorting is idempotent
    #[test]
    fn mr_sort_idempotent(mut data: Vec<i32>) {
        data.sort();
        let once = data.clone();
        data.sort();
        prop_assert_eq!(&data, &once);
    }

    // MR: Round-trip preservation
    #[test]
    fn mr_serialize_roundtrip(value: MyStruct) {
        let bytes = serialize(&value);
        let recovered = deserialize(&bytes)?;
        prop_assert_eq!(&value, &recovered);
    }
}
```

### Custom Strategies for Domain Inputs

```rust
// Generate realistic database queries for TLP testing
fn sql_predicate_strategy() -> impl Strategy<Value = String> {
    let leaf = prop_oneof![
        "[a-z]+ > [0-9]+".prop_map(|s| s),
        "[a-z]+ = '[a-z]+'".prop_map(|s| s),
        "[a-z]+ IS NULL".prop_map(|s| s),
        "[a-z]+ BETWEEN [0-9]+ AND [0-9]+".prop_map(|s| s),
    ];
    // Use prop_recursive for bounded depth (max 3 levels)
    leaf.prop_recursive(3, 64, 4, |inner| {
        prop_oneof![
            inner.clone().prop_map(|p| format!("NOT ({p})")),
            (inner.clone(), inner).prop_map(|(a, b)| format!("({a}) AND ({b})")),
        ]
    })
}
```

---

## Python: Hypothesis + GeMTest

### Hypothesis (built-in)

```python
from hypothesis import given, strategies as st, settings, assume
import math

@given(st.floats(min_value=-1e6, max_value=1e6, allow_nan=False))
@settings(max_examples=1000)
def test_mr_sin_periodicity(x):
    """MR: sin(x) = sin(x + 2π)"""
    assert abs(math.sin(x) - math.sin(x + 2 * math.pi)) < 1e-10

@given(st.lists(st.integers(), min_size=1))
def test_mr_mean_permutation_invariance(data):
    """MR: mean(data) = mean(shuffled(data))"""
    import random
    shuffled = data.copy()
    random.shuffle(shuffled)
    original_mean = sum(data) / len(data)
    shuffled_mean = sum(shuffled) / len(shuffled)
    assert abs(original_mean - shuffled_mean) < 1e-10

@given(st.text(min_size=1), st.text(min_size=1))
def test_mr_search_subset(query, extra):
    """MR: Adding a term to a search narrows results"""
    broad = search(query)
    narrow = search(f"{query} {extra}")
    assert narrow.issubset(broad)
```

### GeMTest Framework

GeMTest (TUM, ICSE 2025) provides decorators for structured MT:

```bash
pip install gemtest
```

```python
import gemtest as gmt

# Define the MR
mr = gmt.create_metamorphic_relation(
    name="sin_shift",
    data=range(100),
)

# Define the input transformation
@gmt.transformation(mr)
def shift_by_2pi(source_input: float) -> float:
    return source_input + 2 * math.pi

# Define the output relation
@gmt.relation(mr)
def approximately_equal(source_output: float, followup_output: float) -> bool:
    return gmt.relations.approximately(source_output, followup_output)

# Define the SUT
@gmt.system_under_test(mr)
def test_sin(input: float) -> float:
    return math.sin(input)

# GeMTest has 218 pre-built MRs across 16 domains
```

---

## TypeScript: fast-check

```typescript
import * as fc from "fast-check";

// MR: Sorting is idempotent
test("mr: sort idempotent", () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted1 = [...arr].sort((a, b) => a - b);
      const sorted2 = [...sorted1].sort((a, b) => a - b);
      expect(sorted1).toEqual(sorted2);
    }),
    { numRuns: 1000 }
  );
});

// MR: JSON round-trip
test("mr: json roundtrip", () => {
  fc.assert(
    fc.property(fc.jsonValue(), (value) => {
      const rt = JSON.parse(JSON.stringify(value));
      expect(rt).toEqual(value);
    })
  );
});

// MR: Filtering then sorting = sorting then filtering (for stable sort)
test("mr: filter-sort commutativity", () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({ name: fc.string(), age: fc.nat(100) })),
      fc.nat(100),
      (people, minAge) => {
        const filterThenSort = people
          .filter((p) => p.age >= minAge)
          .sort((a, b) => a.age - b.age);
        const sortThenFilter = people
          .sort((a, b) => a.age - b.age)
          .filter((p) => p.age >= minAge);
        expect(filterThenSort).toEqual(sortThenFilter);
      }
    )
  );
});
```

---

## Go: rapid

```go
import "pgregory.net/rapid"

func TestMR_SortIdempotent(t *testing.T) {
    rapid.Check(t, func(t *rapid.T) {
        data := rapid.SliceOf(rapid.Int()).Draw(t, "data")
        sort.Ints(data)
        once := make([]int, len(data))
        copy(once, data)
        sort.Ints(data)
        if !reflect.DeepEqual(data, once) {
            t.Fatal("Sort is not idempotent")
        }
    })
}
```

---

## Framework Comparison

| Framework | Language | MR Support | Shrinking | Speed |
|-----------|---------|------------|-----------|-------|
| proptest | Rust | Native properties | Yes | Fast |
| Hypothesis | Python | Via `@given` + manual | Yes | Medium |
| GeMTest | Python | Dedicated decorators | Via Hypothesis | Medium |
| fast-check | TypeScript | Via `fc.property` | Yes | Fast |
| rapid | Go | Via `rapid.Check` | Yes | Fast |
| jqwik | Java/Kotlin | Via `@Property` | Yes | Medium |
| QuickCheck | Haskell | Native properties | Yes | Fast |

**Recommendation:** Use your language's PBT framework. MRs are just a specific type of property. GeMTest adds MT-specific infrastructure (transformation + relation decorators) but isn't required.
