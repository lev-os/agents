---
name: Bayesian Updating
description: Systematically update your confidence in hypotheses as new evidence arrives, weighting both prior beliefs and new information by their respective reliability
---

# Bayesian Updating

## Overview

**Probabilistic belief revision framework**: Systematically update your confidence in hypotheses as new evidence arrives, weighting both prior beliefs and new information by their respective reliability.

**Core insight**: Neither trust new data blindly nor cling to old beliefs stubbornly—optimal belief revision lies between these extremes, proportional to precision of evidence.

**Source**: Thomas Bayes (18th century), formalized by LessWrong rationality community for practical cognition

## The Framework

### Bayes' Theorem (Simplified)

**Updated Belief = (Prior Belief × Likelihood of Evidence) / Total Probability of Evidence**

In plain language:
- **Prior**: What you believed before seeing new evidence
- **Likelihood**: How expected this evidence is if your hypothesis is true
- **Posterior**: Your updated belief after incorporating evidence
- **Precision**: How certain/reliable the information source is

### The Cognitive Process

**Step 1 - Establish Prior**: What's your current confidence level in hypothesis H?
- Example: "30% chance it will rain today" (based on historical weather patterns)

**Step 2 - Observe Evidence**: New information arrives
- Example: Weather radar shows large storm system approaching

**Step 3 - Evaluate Likelihood**: How expected is this evidence under different hypotheses?
- If raining: Storm on radar is very expected (high likelihood)
- If not raining: Storm on radar is less expected (lower likelihood)

**Step 4 - Calculate Posterior**: Update belief proportionally
- Example: Updated to "70% chance of rain" after radar evidence

**Step 5 - Iterate**: Your posterior becomes the new prior for the next evidence cycle

## When to Use

**Explicit Bayesian updating** when:
- Receiving new information that challenges existing beliefs
- Multiple information sources with different reliability levels
- Need to quantify uncertainty numerically
- Making predictions that can be calibrated over time
- Evaluating competing hypotheses

**Implicit Bayesian thinking** for:
- Any belief revision situation
- Assessing credibility of sources
- Medical diagnosis (symptoms as evidence)
- Debugging code (test results as evidence)
- Investment decisions (market signals as evidence)

## Implementation Steps

### 1. Quantify Your Prior

Make your existing belief explicit:
- "I'm 60% confident that feature X will increase engagement"
- "There's a 20% chance this bug is in the API layer"
- "I believe with 80% confidence that candidate A is better fit"

Avoid vague language like "probably" or "might"—use numbers.

### 2. Identify the Evidence

What new information are you receiving?
- User testing results
- Stack trace from error logs
- Candidate's take-home project quality
- Competitor's product launch

Be specific about what you're observing, not your interpretation yet.

### 3. Assess Likelihood Ratio

Ask: "How much more expected is this evidence if my hypothesis is true versus false?"

**Strong evidence**: Very expected under hypothesis, very unexpected otherwise
- Ratio might be 10:1 or 100:1
- Example: If bug is in API, seeing API error logs is 50x more likely than if bug is frontend

**Weak evidence**: Only somewhat more expected under hypothesis
- Ratio might be 2:1 or 3:1
- Example: User engagement up 5% could happen with or without feature

**Misleading evidence**: More expected if hypothesis is false
- Ratio less than 1:1
- Should update belief downward

### 4. Update Proportionally

**Rough heuristic** (for intuitive updating without calculation):
- Strong evidence (10:1 ratio): Update belief significantly (±20-30%)
- Moderate evidence (3:1 ratio): Update moderately (±10-15%)
- Weak evidence (1.5:1 ratio): Update slightly (±5%)

**Direction**: Move toward the hypothesis the evidence supports.

**Magnitude**: Stronger evidence = larger update, but never jump to 100% certainty from single data point.

### 5. Track Your Calibration

Periodically check: Are your 70% predictions actually coming true 70% of the time?
- If yes: Well-calibrated
- If predictions come true >70%: You're underconfident (update priors upward faster)
- If predictions come true <70%: You're overconfident (update more conservatively)

This feedback loop improves your Bayesian instincts over time.

### 6. Weight Source Precision

Not all evidence is equally reliable:

**High precision** (trust more, update more):
- Randomized controlled experiments
- Large sample sizes
- Direct observation
- Domain expert analysis

**Low precision** (trust less, update less):
- Anecdotal reports
- Small samples
- Indirect indicators
- Biased sources

Adjust your update magnitude by source reliability.

## Common Pitfalls

**Ignoring base rates**: Jumping to conclusions from evidence without considering prior probability. (Example: Rare disease with 99% accurate test can still be unlikely even with positive result if disease is 0.1% prevalent.)

**Confirmation bias**: Selectively updating on evidence that supports existing beliefs, dismissing contradictory evidence. True Bayesian updating is symmetric—update in both directions.

**Overconfidence**: Updating too much from single data points, reaching near-certainty prematurely. Keep some probability mass on alternative hypotheses.

**Binary thinking**: Treating beliefs as true/false rather than probabilistic confidence levels. Everything is a percentage.

**Neglecting alternative hypotheses**: Updating P(H) without considering P(not-H) and other competing explanations for the evidence.

**Anchoring on priors**: Refusing to update sufficiently when strong evidence arrives. Your prior shouldn't be sacred—it's just your starting point.

**Conservation of expected evidence**: If you think evidence might arrive, you should already have an opinion on what different results would mean. Don't wait for the data to decide how to interpret it.

## Real-World Applications

**Medical diagnosis**: Doctor starts with base rate of disease prevalence (prior), updates based on symptoms (evidence), orders tests (more evidence), revises diagnosis (posterior).

**Software debugging**: Initial hypothesis about bug location (prior), run test revealing error location (evidence), update belief about root cause (posterior), test fix (more evidence).

**Hiring decisions**: Initial assessment from resume (prior), performance on technical interview (evidence), reference checks (more evidence), final confidence in candidate fit (posterior).

**Investment analysis**: Market belief about company value (prior), earnings report (evidence), updated stock price reflecting collective Bayesian updating (posterior).

**Product development**: Hypothesis about user need (prior), user research findings (evidence), A/B test results (more evidence), conviction to ship feature (posterior).

## Power Moves

**Pre-commit to belief changes**: Before seeing evidence, state explicitly: "If I see X, I'll update my belief from Y% to Z%." This prevents post-hoc rationalization.

**Calibration training**: Make many probabilistic predictions, track accuracy, adjust to hit calibration targets. This builds Bayesian intuition.

**Likelihood ratio shortcut**: Instead of full Bayes calculation, ask "How many times more likely is this evidence under hypothesis A vs. B?" Adjust beliefs proportionally.

**Update incrementally**: Don't wait for "decisive" evidence. Small updates from weak evidence compound over time into strong beliefs when consistent.

**Separate observation from interpretation**: Clearly distinguish what you observed (evidence) from what it means (likelihood). Mix these up and you double-count the same information.

**Quantify uncertainty explicitly**: Force yourself to use numbers. "Probably" is too vague—is it 60% or 90%? Numbers enable proper updating.

## Related Frameworks

- **Epistemic Rationality**: Bayesian updating is the mathematical foundation for systematic belief accuracy
- **Expected Value Calculation**: Uses Bayesian probabilities to weight outcomes
- **Scientific Method**: Hypothesis testing is formalized Bayesian updating
- **Prediction Markets**: Aggregated Bayesian updating across many individuals
- **Kalman Filtering**: Continuous Bayesian updating for dynamic systems (robotics, control systems)

## Technical Note

Full Bayesian calculation:
```
P(H|E) = P(E|H) × P(H) / P(E)

Where:
P(H|E) = Posterior (updated belief in hypothesis given evidence)
P(E|H) = Likelihood (probability of evidence if hypothesis true)
P(H) = Prior (initial belief in hypothesis)
P(E) = Total probability of evidence
```

For practical use, focus on likelihood ratios:
```
P(H|E) / P(~H|E) = [P(E|H) / P(E|~H)] × [P(H) / P(~H)]

Posterior Odds = Likelihood Ratio × Prior Odds
```

This "odds form" is often more intuitive for incremental updating.

## Sources

- [Princeton - Bayesian Models of Cognition](https://cocosci.princeton.edu/tom/papers/bayeschapter.pdf)
- [ScienceDirect - Bayesian Updating Overview](https://www.sciencedirect.com/topics/computer-science/bayesian-updating)
- [LessWrong - An Intuitive Explanation of Bayes' Theorem](https://www.lesswrong.com/w/rationality)
- [Springer - Introduction to Bayesian Inference for Psychology](https://link.springer.com/article/10.3758/s13423-017-1262-3)
