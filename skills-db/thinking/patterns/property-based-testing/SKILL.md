---
name: property-based-testing
description: Test software properties with automatically generated inputs instead of hand-written examples, uncovering edge cases humans miss
---

# Property-Based Testing

## Overview

Property-Based Testing (PBT) is a testing methodology where developers define general properties that code should satisfy, and testing frameworks automatically generate hundreds of test cases to verify those properties hold across diverse inputs. Introduced by Koen Claessen and John Hughes in their 2000 paper "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs," the approach inverts traditional example-based testing: instead of writing "sort([3,1,2]) == [1,2,3]," you write "for any list, sort(sort(list)) == sort(list)" (idempotence property).

QuickCheck pioneered the technique in Haskell, automatically generating random inputs, shrinking failing cases to minimal reproducible examples, and providing property combinators. The 2010 ACM SIGPLAN award recognized its influence. By 2025, QuickCheck ideas have propagated to 57+ languages: Hypothesis (Python), ScalaCheck (Scala), fast-check (JavaScript), PropTest (Rust), JUnit-QuickCheck (Java). John Hughes' work at Quviq applied QuickCheck to Ericsson's Megaco protocol, discovering faults traditional testing missed. PBT excels at exposing edge cases, invariant violations, and assumptions developers didn't realize they made.

## When to Use

- Testing pure functions with well-defined mathematical properties
- Validating data structure invariants (balanced trees, heap property, etc.)
- Serialization/deserialization round-trip correctness
- Testing parsers, encoders, compilers with fuzzing-like coverage
- Validating business rules that should hold universally
- Comparing two implementations for equivalence (oracle testing)
- Finding edge cases before production - especially in critical systems
- Complementing example-based tests to increase confidence

## The Process

### Step 1: Identify Properties - Define Universal Truths

Determine what should always be true about your code regardless of input. Common property patterns: idempotence (f(f(x)) == f(x)), round-trip (decode(encode(x)) == x), invariants (tree stays balanced), commutativity (a + b == b + a), oracle (newImpl(x) == referenceImpl(x)).

**Ask:** "What's always true about this function's behavior? What can't break?"

**Example:** Testing a string reverse function. Properties: reversing twice returns original (reverse(reverse(s)) == s), length preserved (len(reverse(s)) == len(s)), first becomes last (reverse(s)[0] == s[-1]).

### Step 2: Define Generators - Specify Input Space

Configure generators that produce random inputs matching your domain. Most PBT frameworks provide built-in generators (integers, strings, lists) and combinators to build complex generators (lists of positive integers, valid email addresses). Generators should cover full input space, including edge cases.

**Ask:** "What's the valid input domain? What edge cases must generator cover?"

**Example:** Testing JSON parser. Generator: arbitrary nested JSON structures with strings, numbers, booleans, nulls, arrays, objects. Include edge cases: empty objects, deeply nested structures, Unicode strings, large numbers.

### Step 3: Write Property Tests - Express Properties as Code

Implement properties as test functions that assert universal truths. PBT framework generates inputs, runs property against each, reports failures. Unlike example tests with 1-5 cases, property tests run 100-10,000 generated cases.

**Ask:** "How do I express this property as executable assertion?"

**Example (Python Hypothesis):**
```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text())
def test_reverse_twice_is_identity(s):
    assert reverse(reverse(s)) == s
```
Hypothesis generates diverse strings automatically.

### Step 4: Run Tests - Let Framework Find Counterexamples

Execute property tests. Framework generates random inputs satisfying generators, evaluates property for each input. If property fails for any input, test fails and reports the failing case. Most frameworks run 100 examples by default (configurable to thousands).

**Ask:** "Does property hold for all generated inputs? What input breaks it?"

**Example:** Running reverse test discovers failure for empty string - reverse("") throws error instead of returning "". Fix implementation.

### Step 5: Shrink Failures - Find Minimal Failing Case

When a property fails, PBT frameworks automatically shrink the failing input to the simplest case that still fails. This eliminates noise, making root cause obvious. Shrinking is critical - raw failures often involve massive generated inputs.

**Ask:** "What's the simplest input that demonstrates this bug?"

**Example:** Property "sorted list has no duplicates" fails on generated list [5, 42, 1, 7, 5, 99, 5, 13]. Framework shrinks to [0, 0] - minimal duplicate case. Bug obvious: sort doesn't remove duplicates (wrong assumption).

### Step 6: Fix and Retest - Regression Protection

Correct the bug revealed by failing property. Re-run property tests. Many frameworks save discovered failing cases as regression tests, ensuring fixed bugs stay fixed. Properties complement example-based tests - use both.

**Ask:** "Does fix resolve failing property? Should I add explicit example test for this edge case?"

**Example:** After fixing empty string handling, property passes for 1000 generated cases. Add explicit example test for empty string as regression guard.

### Step 7: Increase Confidence - Scale Test Runs

For critical code, increase number of generated test cases (100 → 10,000). Use stateful property testing for complex systems (model state machine, verify implementation matches model). Integrate into CI pipeline to continuously probe for edge cases.

**Ask:** "Is standard 100-case run sufficient? Does this need deeper testing?"

**Example:** Cryptographic hash function tested with 50,000 cases to verify collision resistance, avalanche effect, distribution uniformity.

## Example Application

**Situation:** Building a distributed cache with complex eviction policy. Example-based tests covered basic cases, but production showed mysterious data loss. Suspected edge case in eviction logic but couldn't reproduce.

**Application of Property-Based Testing:**
1. **Identify Properties:** Defined invariants: cache never exceeds max size, most recently accessed items not evicted, evicted items actually removed, total items = cached + evicted.
2. **Define Generators:** Created generator for cache operations: add(key, value), get(key), remove(key), flush(). Generated sequences of 10-100 operations.
3. **Write Property Tests:** Implemented property: "After any sequence of operations, cache size ≤ max_size."
4. **Run Tests:** Framework generated random operation sequences. Failed on: [add(1), add(2), add(3), get(1), add(4), get(2)].
5. **Shrink Failures:** Framework shrunk to minimal failing sequence: [add(1), add(2), add(3), get(1)]. Bug revealed: accessing item during eviction created race condition.
6. **Fix:** Added proper locking around eviction + access. Property passed 10,000 generated sequences.

**Outcome:** Found race condition that eluded 3 months of example testing. Added 5 more properties covering concurrency invariants. Ran 100,000 property tests in CI - discovered 2 additional edge cases before production. Data loss incidents dropped to zero. Team confidence in cache robustness increased dramatically.

## Anti-Patterns

- ❌ Testing implementation details instead of observable properties
- ❌ Properties that merely restate implementation - no verification value
- ❌ Ignoring shrunk failures because minimal case "seems impossible"
- ❌ Generators that don't cover edge cases (empty lists, negative numbers, Unicode)
- ❌ Property-based testing without example tests - lose documentation value
- ❌ Too many assumptions in properties - overly constrained generators miss cases
- ❌ Not saving regression cases - lose historical bug protection
- ❌ Replacing all tests with PBT - example tests still valuable for clarity

## Related

- quickcheck (original Haskell framework)
- hypothesis (Python property-based testing framework)
- fuzzing (related technique using random inputs)
- test-driven-development (complementary discipline)
- invariant-checking (properties as runtime assertions)
- model-based-testing (stateful property testing extension)
