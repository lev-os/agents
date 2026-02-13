---
name: test-driven-development
description: Write reliable code by following the Red-Green-Refactor cycle - write failing test first, make it pass, then improve design
---

# Test-Driven Development (TDD)

## Overview

Test-Driven Development (TDD) is a software development technique where tests are written before production code, guiding implementation through a strict Red-Green-Refactor cycle. Created by Kent Beck in the late 1990s as part of Extreme Programming, TDD inverts the traditional code-then-test workflow. Beck's 2003 book "Test-Driven Development: By Example" established the practice, with the 2025 20th anniversary edition affirming: "Clean code that works is the goal. TDD is merely the discipline that gets us there."

The Red-Green-Refactor cycle consists of three phases: Red (write a failing test), Green (write minimum code to pass), Refactor (improve design without changing behavior). Each cycle takes 2-10 minutes, creating a tight feedback loop. TDD produces executable specifications, comprehensive test coverage as a byproduct, and designs that emerge from usage rather than upfront planning. Tests serve as documentation, design feedback, and regression protection simultaneously.

## When to Use

- Building new features from scratch with unclear design
- Working with complex business logic requiring high confidence
- Refactoring legacy code where regression risk is high
- APIs and libraries where interface design matters more than implementation
- Code requiring long-term maintainability and changeability
- Learning new languages, frameworks, or problem domains
- Debugging by writing tests that reproduce reported issues first

## The Process

### Step 1: RED - Write a Failing Test

Write the smallest possible test for the next increment of functionality. The test should fail for the right reason - the functionality doesn't exist yet, not because of compilation errors or bad test setup. Name tests descriptively using business language: `shouldCalculateDiscountForBulkOrders()` not `test1()`.

**Ask:** "What is the next smallest behavior this code should exhibit?"

**Example:** Testing a shopping cart. First test: `shouldStartEmpty()`. Assert cart.itemCount() == 0. Fails because Cart class doesn't exist yet.

### Step 2: GREEN - Make the Test Pass (Quickly)

Write the minimum code necessary to make the failing test pass. Ignore code quality temporarily - hardcoding, duplication, and "sins" are acceptable. The goal is green tests, not beautiful code. Kent Beck calls this "committing whatever sins necessary in the process."

**Ask:** "What is the simplest code that makes this test pass, even if ugly?"

**Example:** Create Cart class with `itemCount()` returning hardcoded 0. Test passes. Resist urge to implement full Cart logic.

### Step 3: REFACTOR - Improve Design While Tests Are Green

With tests passing, clean up the code. Remove duplication, extract methods, rename variables, improve structure. Tests provide safety net - if refactoring breaks behavior, tests catch it immediately. Commit only when tests are green.

**Ask:** "Now that it works, how can I make it clean? What duplication exists?"

**Example:** Notice hardcoded 0 is acceptable for now. No refactoring needed yet. Proceed to next test.

### Step 4: Repeat - Build Incrementally

Return to Red phase with the next smallest test. Each cycle adds one small behavior. Resist implementing features without a failing test first. The discipline forces incremental progress and prevents gold-plating.

**Ask:** "What's the next missing behavior to test?"

**Example:** Next test: `shouldHaveOneItemAfterAdding()`. Add item, assert count == 1. Fails because `addItem()` doesn't exist. Implement by incrementing counter. Passes. Refactor: create items list instead of counter.

### Step 5: Handle Edge Cases Through Tests

As confidence grows in core functionality, add tests for edge cases, error conditions, and boundary values. Each edge case gets its own test. Don't preemptively handle cases without tests.

**Ask:** "What can break? What inputs haven't been tested?"

**Example:** Test adding null item, adding negative quantity, removing nonexistent item. Each test drives error handling implementation.

### Step 6: Refactor Tests - Keep Tests Clean

Tests are code too. Apply refactoring to tests: extract setup helpers, use factory methods, eliminate duplication. Test readability matters - they serve as documentation.

**Ask:** "Are my tests clear? Is setup duplicated across tests?"

**Example:** Extract `createCartWithItems(3)` helper to reduce setup duplication across tests.

## Example Application

**Situation:** Building a discount calculation system for an e-commerce platform. Requirements: 10% off orders over $100, 15% off over $500, no discount otherwise. Team pressure to "just implement it quickly."

**Application of TDD:**
1. **RED:** Test `shouldReturnZeroDiscountForOrderUnder100()` with $50 order. Expected: $0 discount. Fails - no DiscountCalculator.
2. **GREEN:** Create `DiscountCalculator.calculate(order)` returning hardcoded 0. Passes.
3. **REFACTOR:** None needed yet.
4. **RED:** Test `shouldReturn10PercentDiscountForOrderOver100()` with $150 order. Expected: $15 discount. Fails - still returns 0.
5. **GREEN:** Add if-statement: `if (order.total >= 100) return order.total * 0.1; else return 0;`. Passes.
6. **RED:** Test `shouldReturn15PercentDiscountForOrderOver500()` with $600 order. Expected: $90 discount. Fails - returns $60 (10%).
7. **GREEN:** Add second if: `if (order.total >= 500) return order.total * 0.15;`. Passes.
8. **REFACTOR:** Extract threshold constants, consider strategy pattern if thresholds grow.

**Outcome:** Implementation took 20 minutes. Test suite documents exact behavior. Adding new tier ($1000 = 20% off) took 3 minutes - write test, implement, refactor. Bug discovered via test: $100 exact should qualify for discount (boundary case). Fixed in 1 minute. Manager skeptical of "test-first waste" until comparing this to previous discount feature that took 2 days and had 3 production bugs.

## Anti-Patterns

- ❌ Writing tests after implementation - loses design feedback and feels like busywork
- ❌ Writing multiple tests before implementing - defeats incremental feedback loop
- ❌ Making tests pass by changing test expectations - invalidates test purpose
- ❌ Skipping refactor step - accumulates technical debt despite good coverage
- ❌ Testing implementation details instead of behavior - brittle tests
- ❌ Large test steps - defeats "smallest increment" philosophy
- ❌ Ignoring failing tests temporarily - "I'll fix it later" breaks discipline
- ❌ TDD dogmatism on exploratory code - use spikes for unknowns, TDD for final implementation

## Related

- red-green-refactor-cycle (core TDD algorithm)
- behavior-driven-development (TDD extension with business language)
- unit-testing-patterns (test structure and organization)
- refactoring-methodologies (refactor step techniques)
- continuous-integration (enables frequent TDD cycles)
- test-doubles (mocking and stubbing for isolated tests)
