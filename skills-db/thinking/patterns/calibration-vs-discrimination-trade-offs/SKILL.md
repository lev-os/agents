---
name: calibration-vs-discrimination-trade-offs
description: When improving forecast accuracy requires balancing how well predictions match reality vs. how well they distinguish between outcomes
tags: [forecasting, prediction, decision-making, accuracy, superforecasting]
---

# Calibration vs. Discrimination Trade-Offs

## Overview
In forecasting and prediction, two dimensions of accuracy often trade off against each other: **calibration** (how well predicted probabilities match actual frequencies) and **discrimination** (how well predictions distinguish between different outcomes). A well-calibrated forecaster who says "70% chance" should be right 70% of the time. A discriminating forecaster can tell the difference between 30% and 70% events. Optimal performance requires balancing both, but improving one can hurt the other.

## Core Concepts

### Calibration
**Do your probabilities match reality?**
- If you say "80% confident" 100 times, are you right ~80 times?
- Measures whether predicted probabilities = actual frequencies
- Overconfidence: Saying 90% when only right 70%
- Underconfidence: Saying 60% when right 80%

**Perfect calibration**: For all predictions at X%, exactly X% come true.

### Discrimination (Resolution)
**Can you tell the difference between likely and unlikely events?**
- Can you distinguish 90% probability events from 10% events?
- Measures variance in predictions
- High discrimination: Confidently predicts extremes (10%, 90%)
- Low discrimination: Everything clustered around 50% (uninformative)

**Perfect discrimination**: Always predict 100% for events that happen, 0% for those that don't.

### The Trade-Off
**Why you can't always have both:**
- **High discrimination with poor calibration**: Overconfident extremes (90% predictions right only 60% of time)
- **High calibration with poor discrimination**: Safe but uninformative (everything is 50%)
- **Sweet spot**: Maximally discriminating while maintaining calibration

## Execution Steps (Improving Both Dimensions)

### 1. Measure Current Performance
**Calibration**:
- Plot predicted probabilities vs. actual outcomes
- Calibration curve should hug the diagonal (45° line)
- Brier score captures both calibration and discrimination

**Discrimination**:
- Compare variance in predictions
- Area under ROC curve (AUC)
- How often did high-confidence predictions beat low-confidence?

**Example**: Track predictions over 100 forecasts, plot calibration curve.

### 2. Identify Bias Direction
- **Overconfident**: Calibration curve above diagonal (predicted 80%, actual 60%)
- **Underconfident**: Calibration curve below diagonal (predicted 60%, actual 80%)
- **Overly hedged**: All predictions near 50% (poor discrimination)

### 3. Adjust for Calibration
**If overconfident**:
- Regress toward 50% (moderate extreme predictions)
- Ask "What would make me wrong?"
- Track base rates more carefully

**If underconfident**:
- Push toward extremes when evidence is strong
- Trust pattern recognition
- Acknowledge uncertainty costs (hedging isn't free)

### 4. Improve Discrimination
- **Seek better information**: Distinguish strong vs. weak signals
- **Identify drivers**: What factors predict different outcomes?
- **Decompose questions**: Break complex forecasts into sub-components
- **Track leading indicators**: Early signals that differentiate

**Example**: Instead of "Will product succeed?" ask "Will it hit X downloads AND Y retention?"

### 5. Balance the Trade-Off
**Extremizing**: When aggregating forecasts, push crowd average toward extremes (improves discrimination while maintaining calibration)

**Granular confidence**: Use 1-99% scale, not just 25/50/75

**Context-dependent**: High-stakes decisions need calibration; exploratory decisions can tolerate discrimination focus

## Anti-Patterns

**False Precision**: Claiming 73% when you mean "probably" (discrimination theater without calibration)

**Perpetual Hedging**: Always saying 50-60% to avoid being wrong (good calibration, useless discrimination)

**Uncalibrated Extremes**: Bold predictions (10%, 90%) without tracking accuracy (discrimination without calibration)

**Ignoring Base Rates**: Overweighting anecdotes vs. statistical priors (poor calibration)

## Quality Indicators

**High Signal (Good Balance)**:
- Brier score < 0.20 (combines calibration + discrimination)
- Calibration curve near diagonal across full probability range
- Predictions vary meaningfully (not clustered at 50%)
- Confidence correlates with accuracy
- Regular scoring and feedback

**Low Signal**:
- Never track actual outcomes vs. predictions
- All predictions in narrow range (40-60%)
- Wildly overconfident (90% predictions right 50% of time)
- No improvement over time despite feedback

## Cross-Domain Applications

### Superforecasting
Philip Tetlock's research: Best forecasters balance both dimensions
- Track predictions in prediction markets or tournaments
- Use granular probabilities (not just high/medium/low)
- Update incrementally as new information arrives

### Machine Learning
**Model evaluation trade-offs**:
- Precision vs. recall (similar to calibration vs. discrimination)
- Confidence scores should match actual accuracy
- Platt scaling: Post-hoc calibration of model outputs

### Medical Diagnosis
- **Discrimination**: Can test distinguish sick from healthy?
- **Calibration**: Does "70% risk" mean 70 out of 100 similar patients?
- Both matter: Wrong treatment OR unnecessary anxiety

### Business Forecasting
- Revenue predictions need calibration (for budgeting)
- Opportunity prioritization needs discrimination (which bets to make?)

## Related Frameworks
- **Brier Score**: Combines calibration and discrimination in single metric
- **Superforecasting**: Tetlock's research on prediction accuracy
- **Bayesian Updating**: Incremental belief revision improves calibration
- **Base Rate Neglect**: Ignoring priors hurts calibration
- **Extremizing**: Aggregation technique that improves discrimination

## Scoring (35/50)
- **Practitioner Weight** (7/10): Core to Tetlock's forecasting research, used in prediction markets
- **Clarity** (7/10): Concepts clear but measuring them requires statistical knowledge
- **Proven ROI** (8/10): Superforecasters demonstrably outperform by balancing both
- **Novelty** (6/10): Statistical concepts applied to forecasting (moderately non-obvious)
- **Applicability** (7/10): Relevant to forecasting, ML, risk assessment, decision-making

## Sources
- Philip Tetlock: Superforecasting (calibration-discrimination trade-offs in expert predictions)
- Philip Tetlock: Expert Political Judgment (foxes vs. hedgehogs, accuracy dimensions)
- Glenn Brier: Verification of forecasts (Brier score)
- Good Judgment Project: Practical forecasting tournament findings
- Nate Silver: The Signal and the Noise (calibration in prediction)
