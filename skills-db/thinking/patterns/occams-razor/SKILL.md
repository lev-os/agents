---
name: occams-razor
description: Choose simpler explanations over complex ones when both explain the evidence equally well, avoiding unnecessary assumptions
---

# Occam's Razor

## Overview
Occam's Razor (Principle of Parsimony) states: when choosing between competing explanations that make equally accurate predictions, prefer the one requiring fewer assumptions. Named after 14th-century philosopher William of Ockham, it's a foundational heuristic in science and problem-solving. The key: this applies ONLY when explanations have equal explanatory power - it's not about oversimplifying, but avoiding unnecessary complexity.

## When to Use
- Debugging systems when multiple theories could explain a failure
- Evaluating competing scientific theories or hypotheses
- Medical diagnosis with multiple possible conditions
- Choosing between architectural designs with similar capabilities
- Deciding between simple vs. complex solutions to a problem
- Avoiding conspiracy theories or over-complicated explanations

## The Process

### Step 1: Identify Competing Explanations
List all plausible explanations for the phenomenon you're investigating. For a production outage: network failure, database corruption, memory leak, DDoS attack, configuration error, hardware failure.

**Example:** Your website is down. Possible causes: DNS misconfiguration, server crash, code deployment bug, cyber attack, hosting provider outage.

### Step 2: Evaluate Explanatory Power
Assess whether each explanation actually accounts for the observed evidence. Eliminate theories that don't match the facts. If your logs show successful requests until exactly 2 PM deployment, theories involving hardware failure (gradual) don't fit.

### Step 3: Count Assumptions Required
For explanations that fit the evidence equally well, list the assumptions each requires. Simple explanation: "deployment introduced a bug" (assumes: code changed, bug wasn't caught in testing). Complex: "coordinated attack timed with deployment" (assumes: attackers knew deployment time, bypassed security, timed perfectly, left no attack signatures).

### Step 4: Choose Fewer Assumptions
Select the explanation requiring the fewest additional assumptions. This doesn't guarantee correctness - it identifies the most likely explanation to investigate first. Save complex theories for when simpler ones fail.

**Example:** Website went down at deployment time → investigate the deployment first (1-2 assumptions) before investigating coordinated cyber attacks (5+ assumptions).

### Step 5: Test and Iterate
Verify your chosen explanation through testing. If the simple explanation is wrong, move to the next-simplest theory. Occam's Razor is a heuristic for prioritizing investigation, not a guarantee of truth.

## Example Application

**Situation:** In medicine, a patient presents with fatigue, weight loss, and fever. Multiple diseases could explain this: common viral infection, rare tropical disease, cancer, autoimmune disorder, chronic fatigue syndrome.

**Application:** Doctors apply "when you hear hoofbeats, think horses, not zebras" (medical version of Occam's Razor). Test for common conditions first (viral infection - requires few assumptions: patient exposed to virus). Only pursue rare diseases (tropical parasites - requires assumptions: recent travel, exposure to specific vectors) if common explanations fail.

**Outcome:** 95%+ of cases resolve with simple explanations. Testing for rare diseases first wastes time/money and delays treatment. But when simple tests fail, doctors DO pursue complex diagnoses - Occam's Razor prioritizes, doesn't eliminate.

## Anti-Patterns
- Using Occam's Razor to dismiss complexity when evidence actually requires it (oversimplifying)
- Applying it when explanations don't have equal predictive power (choosing "simple but wrong" over "complex but accurate")
- Confusing "fewer assumptions" with "easier to understand" (quantum mechanics is simpler than hidden variables, but harder to grasp)
- Using it to avoid investigating when simple explanation already failed tests
- Treating it as proof rather than a heuristic for prioritizing investigation

## Real-World Business Examples

**Startup Failure Analysis**
Company loses 50% of users in one month. Possible causes:
- Simple: Major competitor launched, pricing change upset users, critical bug
- Complex: Coordinated sabotage, algorithm conspiracy, market manipulation
Start with data on competitor launches and product changes before complex theories.

**Software Performance**
Application slows down after update:
- Simple: New code has inefficient query, memory leak, cache not warming
- Complex: Hardware degradation + cosmic rays + database index corruption + network interference
Investigate code changes first - they have highest prior probability.

## Bayesian Foundation

Occam's Razor emerges naturally from Bayesian probability theory:
- Simpler hypotheses have fewer free parameters
- Fewer parameters = higher prior probability (less specific claim)
- Same fit to data + higher prior = higher posterior probability
- Mathematical formalization: Minimum Description Length (MDL) principle

This explains WHY simpler is better: not philosophical preference, but mathematical consequence of probability theory.

## Common Pitfalls

- **Oversimplification**: Ignoring evidence that demands complexity
- **Premature conclusion**: Accepting simple explanation without testing
- **Confusing simple with familiar**: Choosing comfortable over genuinely parsimonious
- **Avoiding necessary complexity**: World is sometimes complex - embrace when warranted
- **Using as proof**: Razor prioritizes investigation, doesn't prove correctness

## Historical Evolution

**14th Century**: William of Ockham formulates "Entities should not be multiplied beyond necessity"
**17th-18th Century**: Becomes central to scientific method
**20th Century**: Formalized in information theory (Solomonoff, Kolmogorov complexity)
**21st Century**: Applied to machine learning (regularization, model selection)

## Success Metrics

- Faster time to correct diagnosis (start with high-probability causes)
- Fewer wasted resources on unlikely scenarios
- More testable hypotheses (simpler = easier to falsify)
- Better decision quality under uncertainty
- Reduced analysis paralysis

## Relationship to Other Frameworks

- **Hanlon's Razor**: Specific application (prefer incompetence over malice)
- **Hitchens's Razor**: Applied to claims (dismiss unfounded assertions)
- **KISS Principle**: Design philosophy (Keep It Simple, Stupid)
- **Minimum Viable Product**: Start simple, add complexity only as needed
- **First Principles Thinking**: Strip to essentials, rebuild from simplicity

## Key Insight

Occam's Razor is not a statement about reality (claiming the world is simple), but a rational strategy for investigation: simpler hypotheses have higher prior probability, are easier to test, and should be checked first. Complexity should be adopted only when evidence demands it.

---

**Primary Sources**: William of Ockham (14th century), Bayesian statistics, Solomonoff induction
**Practitioner**: Science, medicine, engineering, debugging, business analysis
**Complexity**: Low - concept simple, application requires judgment
**Estimated Learning**: 20 minutes to understand, career to master judicious application
