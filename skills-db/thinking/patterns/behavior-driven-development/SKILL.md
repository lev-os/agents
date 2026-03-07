---
name: behavior-driven-development
description: Bridge communication gap between technical and business stakeholders using Given-When-Then scenarios in plain language
---

# Behavior-Driven Development (BDD)

## Overview

Behavior-Driven Development (BDD) is a refinement of Test-Driven Development that uses domain language to describe software behavior, bridging the gap between business stakeholders and developers. Introduced by Dan North in his 2006 blog post "Introducing BDD," the practice emerged from North's observation that naming tests using behavioral language - focusing on "should" instead of "test" - made code behavior clearer and reduced confusion about what to test.

In 2007, North introduced the Gherkin language with its Given-When-Then syntax, developed with Chris Matts. Gherkin enables non-technical stakeholders to write executable specifications: Given (context), When (action), Then (outcome). These scenarios serve as requirements, tests, and living documentation simultaneously. BDD combines TDD's test-first discipline with Domain-Driven Design's ubiquitous language, creating specifications that are both human-readable and machine-executable. Tools like Cucumber, SpecFlow, and Behave parse Gherkin into test frameworks.

## When to Use

- Collaborating with non-technical stakeholders who need to validate behavior
- Building customer-facing features where requirements often misunderstood
- Acceptance testing to verify features meet business expectations
- Creating living documentation that stays synchronized with code
- Reducing ambiguity in requirements before implementation begins
- Teams struggling with communication gap between business and engineering
- Regulatory environments requiring clear, auditable specifications

## The Process

### Step 1: Discover - Collaboratively Define Scenarios

Bring together developers, testers, and business stakeholders ("Three Amigos") to explore a feature through concrete examples. Ask "What should happen when...?" for different contexts. Focus on business outcomes, not technical implementation. Capture examples in plain language.

**Ask:** "What are real-world situations users will encounter? What's the expected outcome?"

**Example:** Feature: Apply promotional discount. Stakeholders describe: "When a customer enters a valid promo code at checkout, they should see the discount reflected in their order total before payment."

### Step 2: Formulate - Write Given-When-Then Scenarios

Translate concrete examples into Gherkin syntax. Given sets initial context (preconditions), When describes the triggering action, Then specifies expected outcomes. Use business domain language, not technical jargon. Each scenario should be independently executable.

**Ask:** "What's the starting state (Given)? What action occurs (When)? What should result (Then)?"

**Example:**
```gherkin
Scenario: Valid promo code applies discount
  Given a customer has items totaling $100 in cart
  And a "SUMMER20" promo code exists for 20% off
  When the customer enters "SUMMER20" at checkout
  Then the order total should be $80
  And the discount line should show "-$20"
```

### Step 3: Automate - Implement Step Definitions

Map each Given/When/Then step to executable code (step definitions). Developers write glue code that translates plain-language steps into system interactions. Steps are reusable across scenarios - "Given a customer has items totaling $100" can appear in multiple scenarios.

**Ask:** "How do I translate this human-readable step into system actions?"

**Example:** Step definition for "Given a customer has items totaling $100 in cart" - creates test cart, adds products totaling $100, sets up test session state.

### Step 4: Validate - Run Scenarios Against Implementation

Execute Gherkin scenarios using BDD framework (Cucumber, Behave, SpecFlow). Scenarios run as automated tests. Red scenarios indicate behavior not yet implemented or broken. Green scenarios confirm behavior works as specified. Scenarios run in CI pipeline.

**Ask:** "Do scenarios pass? If not, is it missing implementation or incorrect expectation?"

**Example:** First run shows "When customer enters promo code" fails - promo code feature not implemented yet. Implement feature. Second run passes all steps.

### Step 5: Maintain - Keep Scenarios Synchronized

As features evolve, update scenarios before changing code (specification by example). Remove obsolete scenarios. Refactor step definitions to reduce duplication. Scenarios serve as living documentation - they must stay current or they rot into misleading documentation.

**Ask:** "Do scenarios still reflect current business rules? Are there outdated scenarios to remove?"

**Example:** Business changes promo codes to apply only to orders over $50. Update scenario: "Given a customer has items totaling $60 in cart..." Adjust implementation.

### Step 6: Collaborate - Review Scenarios with Stakeholders

Regularly review scenario suite with business stakeholders to validate understanding. Scenarios often reveal hidden assumptions or edge cases. Shared understanding emerges through concrete examples, not abstract requirements documents.

**Ask:** "Do stakeholders agree these scenarios capture desired behavior? What scenarios are missing?"

**Example:** During review, product manager identifies missing scenario: "What if customer tries to use expired promo code?" Add new scenario: "Then an error message should display 'Promo code expired'."

## Example Application

**Situation:** Healthcare appointment booking system with complex business rules around cancellations. Previous text-based requirements led to 14 production bugs - developers misunderstood "24-hour cancellation window" and insurance verification rules.

**Application of BDD:**
1. **Discover:** Three Amigos session identified 8 distinct scenarios: booking with insurance, booking without insurance, canceling within 24 hours, canceling after 24 hours with valid reason, etc.
2. **Formulate:** Wrote Gherkin scenarios:
```gherkin
Scenario: Cancel appointment within 24 hours incurs fee
  Given a patient has appointment scheduled for tomorrow at 2pm
  When the patient cancels today at 3pm
  Then a $25 cancellation fee should apply
  And the patient should receive fee notification email
```
3. **Automate:** Implemented step definitions using test framework, creating test patients, appointments, mocking email service.
4. **Validate:** Ran scenarios, found insurance verification scenario failed - missing validation. Implemented. All scenarios green.
5. **Maintain:** When business changed policy ("waive fee for emergencies"), updated scenarios first, then code.

**Outcome:** Zero production bugs in 6 months. Business stakeholders gained confidence by reviewing scenarios - caught 3 incorrect assumptions before implementation. Onboarding new developers faster - scenarios serve as executable specification. Scenarios run in CI - regression protection.

## Anti-Patterns

- ❌ Writing scenarios after implementation - loses collaboration and specification value
- ❌ Technical language in scenarios - defeats non-technical stakeholder participation
- ❌ Testing implementation details - scenarios should describe behavior, not how it's built
- ❌ One massive scenario - breaks independent executability and clarity
- ❌ Developers writing scenarios in isolation - misses collaborative discovery value
- ❌ Scenarios as only test coverage - still need unit tests for edge cases
- ❌ Ignoring failing scenarios - "broken windows" erode scenario trust
- ❌ Over-specifying UI interactions - makes scenarios brittle to UI changes

## Related

- test-driven-development (TDD foundation that BDD extends)
- domain-driven-design (ubiquitous language source)
- specification-by-example (BDD's philosophical foundation)
- acceptance-test-driven-development (similar approach)
- gherkin-language (Given-When-Then syntax)
- three-amigos-practice (collaborative scenario discovery)
