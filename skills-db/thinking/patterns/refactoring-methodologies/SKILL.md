---
name: refactoring-methodologies
description: Systematically improve code structure without changing behavior using Martin Fowler's catalog of behavior-preserving transformations
---

# Refactoring Methodologies

## Overview

Refactoring is "a controlled technique for improving the design of an existing code base" through "a series of small behavior-preserving transformations," as defined by Martin Fowler. The practice emerged from the Smalltalk community in the 1980s and was codified by Fowler in his 1999 book "Refactoring: Improving the Design of Existing Code," which became foundational to modern software development. The 2018 second edition updated the catalog with JavaScript examples and functional programming patterns.

Fowler's work provides a systematic catalog of 60+ named refactoring techniques organized into categories: Composing Methods, Moving Features Between Objects, Organizing Data, and Simplifying Conditional Expressions. Each refactoring is a well-defined transformation with clear mechanics, motivation, and examples. The catalog at refactoring.com serves as the canonical reference, supporting both object-oriented and functional paradigms. Refactoring is distinguished from rewriting by its incremental, test-validated nature - you never break the code.

## When to Use

- Code smells emerge: long methods, duplicated code, large classes, divergent change
- Adding features becomes increasingly difficult due to rigid structure
- Understanding code requires excessive mental effort or documentation
- Tests are hard to write due to tight coupling or hidden dependencies
- Performance optimization requires first clarifying structure
- Preparing for architecture changes by cleaning dependencies
- Code review reveals unclear intent or unnecessary complexity

## The Process

### Step 1: Identify Code Smells - Recognize Refactoring Triggers

Code smells are symptoms indicating deeper design problems. Fowler catalogs 22 smells including Duplicated Code, Long Method, Large Class, Long Parameter List, Divergent Change (one class changes for multiple reasons), and Shotgun Surgery (one change requires touching many classes).

**Ask:** "What friction am I experiencing? What makes this code hard to work with?"

**Example:** A 200-line method with nested conditionals, temporary variables, and duplicated logic - clear "Long Method" smell.

### Step 2: Choose Appropriate Refactoring - Match Pattern to Problem

Select from Fowler's catalog based on the smell. For Long Method: Extract Method, Replace Temp with Query, Introduce Parameter Object. For Large Class: Extract Class, Extract Subclass. For Duplicated Code: Extract Method, Pull Up Method, Form Template Method.

**Ask:** "Which refactoring pattern addresses this specific smell?"

**Example:** For the 200-line method, use Extract Method to pull out logical blocks into named methods with clear intent.

### Step 3: Ensure Test Coverage - Establish Safety Net

Before refactoring, verify comprehensive test coverage or write tests for the code being changed. Tests must pass before and after each transformation. If tests don't exist, add characterization tests that document current behavior.

**Ask:** "Do I have tests proving this code works? Will they catch regressions?"

**Example:** Write unit tests covering edge cases and happy paths for the long method before extracting anything.

### Step 4: Apply Small Transformations - Refactor in Tiny Steps

Execute the chosen refactoring using its documented mechanics. Move in small, reversible steps - extract one method, run tests, commit. Never refactor and add features simultaneously. Use IDE automated refactorings when available (Rename, Extract Method, Move Class).

**Ask:** "Can I make this change in 30 seconds and verify it immediately?"

**Example:** Extract the first logical block (input validation) into `validateInput()` method. Run tests. Commit. Then extract business logic. Tests. Commit. Repeat.

### Step 5: Verify Behavior Unchanged - Run Tests After Each Step

After each micro-transformation, run the full test suite. All tests must pass before proceeding. If tests fail, undo immediately and take a smaller step. This discipline prevents compounding errors.

**Ask:** "Did I break anything? Are all tests green?"

**Example:** After extracting `validateInput()`, tests pass. After extracting `calculateDiscount()`, one test fails - undo and investigate before proceeding.

### Step 6: Remove Duplication - Eliminate Redundancy

Once structure is clear, identify and eliminate duplicated code through Extract Method, Pull Up Method, or Form Template Method. Duplication often becomes visible only after initial extractions clarify structure.

**Ask:** "Now that structure is clearer, where is the same logic repeated?"

**Example:** After extracting methods, notice three similar validation methods - apply Form Template Method to create base validator with hooks for variations.

### Step 7: Commit and Repeat - Build on Clean Foundation

Commit refactored code with descriptive message noting which refactoring was applied. Continue with next smell or feature work. Refactor opportunistically - improve code as you touch it ("boy scout rule").

**Ask:** "Is this code better than before? What's the next smell to address?"

**Example:** Commit "Refactor: Extract Method on payment processing logic." Next session, notice Large Class smell and apply Extract Class.

## Example Application

**Situation:** E-commerce checkout system with a 350-line `processOrder()` method containing payment processing, inventory checks, tax calculation, shipping, and email notifications. Adding new payment methods requires understanding entire method.

**Application:**
1. **Code Smell:** Long Method (350 lines), Divergent Change (changes for payment, tax rules, shipping)
2. **Test Coverage:** Added tests for all checkout scenarios (12 tests covering edge cases)
3. **Extract Method:** Created `validateInventory()`, `calculateTax()`, `processPayment()`, `arrangeShipping()`, `sendConfirmation()` - reduced to 40-line orchestration
4. **Extract Class:** Moved payment logic to `PaymentProcessor`, tax to `TaxCalculator`, shipping to `ShippingService`
5. **Replace Temp with Query:** Eliminated 8 temporary variables by extracting calculation methods
6. **Tests:** All 12 tests passed after each extraction

**Outcome:** Adding new payment method went from 2-day task (touching monolithic method) to 30-minute task (one new PaymentProcessor subclass). Bugs decreased 60% - smaller methods are easier to verify. Team velocity increased - clearer structure enabled parallel work.

## Anti-Patterns

- ❌ Refactoring without tests - "blind refactoring" leads to undetected breakage
- ❌ Big-bang refactoring - rewriting large sections simultaneously breaks incremental safety
- ❌ Refactoring and feature addition together - impossible to isolate what broke
- ❌ Refactoring for its own sake - every change has risk, refactor when valuable
- ❌ Ignoring code smells - "it works so don't touch it" accumulates technical debt
- ❌ Manual refactoring when IDE can automate - error-prone and time-consuming
- ❌ Committing broken intermediate states - each commit should be working code
- ❌ Over-refactoring simple code - clarity has diminishing returns

## Related

- code-smells (triggers for refactoring)
- test-driven-development (provides safety net)
- solid-principles (design targets for refactoring toward)
- clean-code-practices (complementary code quality principles)
- continuous-integration (enables safe frequent refactoring)
- boy-scout-rule (opportunistic refactoring philosophy)
