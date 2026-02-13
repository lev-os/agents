---
name: dry-principle
description: Eliminate code duplication by extracting shared logic into single authoritative representations - every piece of knowledge should exist once
---

# DRY Principle (Don't Repeat Yourself)

## Overview
DRY (Don't Repeat Yourself), articulated in The Pragmatic Programmer by Hunt and Thomas, states: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." Duplication creates maintenance burden—fixing bugs or changing logic requires updating multiple locations, inevitably leading to inconsistencies.

## When to Use
- Noticing copy-pasted code blocks across files
- Same business logic implemented in multiple places
- Repetitive configuration or data structures
- Multiple sources of truth causing sync issues
- Bug fixes requiring changes in 5+ locations
- Code reviews revealing duplication

## The Process

### Step 1: Identify Duplication Types
**Code duplication**: Identical or similar logic repeated. **Knowledge duplication**: Same business rule expressed differently in multiple places. **Data duplication**: Multiple sources of truth for same information.

**Example**: Validation logic for email format appears in signup form, profile update form, admin panel, and API endpoint.

### Step 2: Extract to Single Source of Truth
Create function, class, module, or configuration representing the duplicated knowledge once. All uses reference this single source.

**Example**: Extract `validateEmail(email)` function. All forms/APIs call this function instead of implementing validation inline.

### Step 3: Replace All Instances
Find and replace duplicated code with calls to the new single source. Use search tools to find all occurrences.

**Example**: Replace 12 instances of email regex validation with `validateEmail()` calls.

### Step 4: Test Thoroughly
Duplicated code often has subtle differences (intentional or bugs). Verify that single source handles all edge cases from all original contexts.

**Example**: Discover signup form allows `+` in emails but profile update doesn't. Fix `validateEmail()` to handle both correctly.

### Step 5: Prevent Future Duplication
Add linting rules, code review checklists, or architectural patterns that discourage duplication.

**Example:** Add ESLint rule detecting duplicate code blocks. Enforce code review question: "Could this be extracted?"

## Example Application

**Situation**: SaaS app with authentication checks duplicated across 47 API endpoints. Bug discovered: JWT expiration not checked consistently.

**DRY Refactoring**:
- **Before**: Each endpoint has 10-15 lines checking JWT validity, user permissions, rate limits. Some check expiration, some don't. Bug fix requires updating 47 files.
- **After**: Extract `authenticateRequest(request)` middleware. All endpoints use middleware. Bug fix requires changing 1 function.
- **Deployment**: Roll out middleware incrementally, one endpoint at a time. Test each.
- **Prevention**: Add architectural rule: "All new endpoints must use authentication middleware, no inline checks allowed."

**Outcome**: Future auth changes take minutes instead of days. Security bugs fixed once, applied everywhere. Eliminated 500+ lines of duplicated code.

## When to Allow Repetition

DRY is not absolute. Acceptable repetition:
- **Coincidental similarity**: Code looks similar but represents different concepts. Abstracting would couple unrelated logic.
- **Premature abstraction**: Don't DRY until pattern repeats 3+ times. "Rule of Three": Duplicate twice, abstract on third occurrence.
- **Optimization**: Sometimes duplicated optimized code performs better than abstracted code.
- **Testing**: Test code duplication is acceptable to keep tests independent and readable.

**Example**: `formatDateForDisplay(date)` and `formatDateForAPI(date)` look similar but serve different purposes (UI vs. serialization). Don't force them into one function with flags—that couples UI and API concerns.

## Anti-Patterns
- ❌ Premature abstraction (DRY-ing code that repeats twice but won't repeat again)
- ❌ Wrong abstraction (forcing unrelated concepts into shared function because code looks similar)
- ❌ Over-DRY: Extracting every 3-line block into separate function (decreases readability)
- ❌ Ignoring WET (Write Everything Twice) guideline—abstract on third repetition, not first
- ❌ DRY-ing across bounded contexts (microservices sharing code reduces independence)
- ❌ Treating DRY as dogma vs. guideline (sometimes duplication is correct choice)

## Related
- single-responsibility-principle
- abstraction
- refactoring
- yagni
- code-smells
