---
name: bayes-theorem
description: Update probability estimates as new evidence emerges - prior beliefs + likelihood of evidence = refined posterior probability
---

# Bayes' Theorem

## Overview

Bayes' Theorem provides a mathematical framework for updating beliefs when new evidence arrives. The formula P(H|E) = P(E|H) * P(H) / P(E) combines your prior probability (what you believed before) with the likelihood of evidence (how likely this evidence appears if your belief is true) to produce a posterior probability (what you should believe now). Unlike binary thinking where you're either right or wrong, Bayesian updating treats beliefs as probabilities that should shift incrementally with each new data point.

The power lies in systematic belief revision: you don't abandon theories at first contradicting evidence, nor cling to them despite mounting contrary data. Each piece of evidence shifts your confidence by an amount proportional to how surprising that evidence would be under your hypothesis versus alternatives.

## When to Use

- Medical diagnosis: test positive for rare disease, but what's the actual probability given false positive rates?
- Spam filtering: given these words appear, how likely is this email spam?
- A/B testing: early results favor B, but is sample size sufficient to update confidently?
- Hiring decisions: strong interview, but how much should that update your prior from resume screening?
- Investment thesis: new earnings data arrived, should you update your position sizing?
- Debugging: error occurred after code change, how strongly does that implicate the change?

## The Process

### Step 1: Establish Your Prior Probability

Before seeing new evidence, what's your baseline belief? This comes from base rates, historical data, or domain expertise.

**Setting priors:**
- Use reference class data when available: "What % of Series A startups achieve $10M ARR?"
- Start with base rates for rare events: "How common is this disease in population?"
- For novel situations, estimate from analogous cases

**Example:** Evaluating if job candidate will succeed
- Prior P(success) = 0.30 (only 30% of hires at this role historically succeed)

### Step 2: Assess Likelihood of Evidence Under Each Hypothesis

How likely is this specific evidence if your hypothesis is true? And if it's false?

**Calculate likelihoods:**
- P(E|H) = probability of seeing this evidence if hypothesis is true
- P(E|~H) = probability of seeing this evidence if hypothesis is false

**Example continued:**
- Candidate aced technical challenge (evidence E)
- P(strong performance | will succeed) = 0.80 (good performers often succeed)
- P(strong performance | will fail) = 0.25 (some who fail still interview well)

### Step 3: Apply Bayes' Formula

Compute posterior probability: P(H|E) = P(E|H) * P(H) / P(E)

Where P(E) = P(E|H) * P(H) + P(E|~H) * P(~H)

**Example continued:**
- P(E) = (0.80 * 0.30) + (0.25 * 0.70) = 0.24 + 0.175 = 0.415
- P(success | strong performance) = (0.80 * 0.30) / 0.415 = 0.58

Posterior: 58% confidence in success, up from 30% prior.

### Step 4: Iterate as New Evidence Arrives

Yesterday's posterior becomes today's prior. Each new data point triggers another update.

**Iterative updating:**
- Reference check comes back glowing: update 58% -> 72%
- Previous employer mentions punctuality issues: update 72% -> 65%
- Accept or reject based on final probability vs. decision threshold

## Example Application

**Situation:** Product team sees 20% conversion rate in first week of A/B test (control was 15%).

**Application:**
- **Prior:** 50% chance the new design actually improves conversions (skeptical starting point)
- **Evidence:** 20% vs 15% in first 1,000 users
- **Likelihood if true improvement:** P(seeing this data | design is better) = 0.70
- **Likelihood if no real difference:** P(seeing this data | statistical noise) = 0.20
- **Posterior:** P(design is better | this data) = (0.70 * 0.50) / (0.70 * 0.50 + 0.20 * 0.50) = 0.78

**Outcome:** Confidence increased from 50% to 78%. Continue test for more data before full rollout (threshold: 95% confidence).

## Example Application 2

**Situation:** Developer sees error logs spike after deploying new feature.

**Application:**
- **Prior:** 30% chance new code caused the issue (other factors: infrastructure, third-party APIs)
- **Evidence:** Errors correlate with exact deployment timestamp
- **Likelihood if new code caused it:** P(timing correlation | code bug) = 0.90
- **Likelihood if unrelated:** P(timing correlation | coincidence) = 0.10
- **Posterior:** (0.90 * 0.30) / (0.90 * 0.30 + 0.10 * 0.70) = 0.27 / 0.34 = 0.79

**Outcome:** 79% confidence it's the new code. Roll back first, investigate second.

## Anti-Patterns

- Ignoring base rates (prior probability) and only focusing on the latest evidence
- Refusing to update beliefs despite consistent contrary evidence (motivated reasoning)
- Overcounting same evidence multiple times (double-dipping on data)
- Setting prior to 0% or 100% (these can never be updated by any amount of evidence)
- Ignoring likelihood ratio: treating all evidence as equally diagnostic
- Updating too aggressively on small samples (single data point shouldn't swing 50%)

## Related

- thinking-in-bets (practical framework for probabilistic decision-making)
- calibration (training yourself to estimate probabilities accurately)
- base-rate-analysis (establishing priors from reference class data)
- superforecasting (systematic approach to improving prediction accuracy)
- expected-value-calculation (using posterior probabilities to calculate payoffs)
