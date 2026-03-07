---
name: brier-score
description: Measure forecasting accuracy by calculating mean squared error between predicted probabilities and outcomes when improving calibration through systematic feedback
---

# Brier Score

**Category:** Decision-Making & Strategic Thinking
**Source:** Glenn W. Brier (1950) / Meteorology / Forecasting Science
**Practitioner Score:** 42/50 (Tier 1)

## Overview

The Brier Score is a strictly proper scoring rule that measures the accuracy of probabilistic predictions. It calculates the mean squared error between predicted probabilities and actual outcomes, providing a single numeric measure of forecast quality. Lower scores indicate better accuracy, with 0 being perfect and 2 being worst possible.

**Core Insight:** You can't improve what you don't measure. The Brier Score converts vague notions of "good forecasting" into quantifiable performance, enabling systematic improvement through calibration feedback.

**Formula:** BS = (1/N) Σ(fᵢ - oᵢ)²
- fᵢ = forecasted probability (0-1)
- oᵢ = actual outcome (1 if event occurred, 0 if not)
- N = number of forecasts

## When to Use

- **Calibration assessment** - Are your 70% predictions actually happening 70% of the time?
- **Forecaster comparison** - Which analyst/model produces more accurate predictions?
- **Training feedback** - Providing objective performance scores for improvement
- **Decision validation** - Evaluating quality of past predictions over time
- **Model selection** - Comparing machine learning models or forecasting systems

**Anti-patterns:**
- Single predictions (need 20+ for statistical validity)
- Non-probabilistic forecasts (binary yes/no)
- Events without clear resolution criteria
- Immediate feedback needs (requires outcome data)

## How to Execute

### Step 1: Record Probabilistic Forecast
**Action:** Document your prediction as a probability between 0% and 100%
- **Precision:** Use granular probabilities (65%, not "likely")
- **Timestamp:** Record when prediction was made
- **Resolution criteria:** Define exactly what constitutes "event occurred"
- **Output:** Logged forecast with probability, date, and outcome definition

### Step 2: Wait for Event Resolution
**Action:** Allow sufficient time for outcome to be determined
- **Clear endpoint:** Specify resolution date/trigger in advance
- **Unambiguous outcome:** 1 (occurred) or 0 (did not occur)
- **No gaming:** Outcome determination must be independent of forecaster
- **Output:** Resolved outcome (1 or 0)

### Step 3: Calculate Individual Forecast Error
**Action:** Compute squared difference between forecast and outcome
- **If event occurred (oᵢ = 1):** Error = (1 - fᵢ)²
- **If event did not occur (oᵢ = 0):** Error = (0 - fᵢ)² = fᵢ²
- **Example:** Predicted 70% (0.7), event happened → (1 - 0.7)² = 0.09
- **Output:** Single forecast Brier score

### Step 4: Aggregate Across Multiple Forecasts
**Action:** Average squared errors across N predictions
- **Minimum sample:** 20+ forecasts for meaningful assessment
- **Formula:** BS = (Error₁ + Error₂ + ... + Errorₙ) / N
- **Output:** Overall Brier score for forecast set

### Step 5: Interpret Score Against Benchmarks
**Action:** Compare your score to reference points
- **Perfect accuracy:** 0.00 (impossible in practice)
- **Excellent:** < 0.10 (superforecaster level)
- **Good:** 0.10 - 0.20 (well-calibrated forecaster)
- **Average:** 0.20 - 0.30 (typical expert)
- **Poor:** > 0.30 (worse than random guessing)
- **Output:** Performance classification

### Step 6: Decompose into Calibration vs. Resolution
**Action:** Break Brier score into skill components
- **Calibration:** Are X% forecasts correct X% of the time?
- **Resolution:** Can you distinguish different probability levels?
- **Formula:** BS = Reliability - Resolution + Uncertainty
- **Output:** Diagnostic breakdown identifying improvement areas

### Step 7: Implement Calibration Improvements
**Action:** Use insights to adjust forecasting behavior
- **Overconfident (too many extremes):** Pull predictions toward 50%
- **Underconfident (clustered near 50%):** Increase differentiation
- **Systemic bias:** Adjust all forecasts by consistent offset
- **Output:** Updated forecasting protocol

## Real-World Examples

**Weather Forecasting:**
- Meteorologists tracked with Brier scores for 50+ years
- Led to dramatic improvements in precipitation forecasting
- Result: Today's 5-day forecast as accurate as 1-day forecast in 1970s

**Good Judgment Project:**
- Superforecasters averaged 0.15-0.18 Brier scores
- Regular forecasters averaged 0.25-0.30
- Intelligence analysts (with classified info) averaged 0.30+
- Result: Validated that systematic methodology beats expertise

**Sports Betting Markets:**
- Bookmakers use Brier scores to evaluate odds accuracy
- Prediction markets (PredictIt, Polymarket) track participant scores
- Result: Efficient markets reflect well-calibrated probabilities

## Integration Points

**Complements:**
- **Superforecasting:** Brier score measures effectiveness of 10 commandments
- **Calibration:** Primary diagnostic tool for improving calibration
- **Bayesian Updating:** Tracks whether belief updates improve accuracy
- **Prediction Markets:** Aggregation mechanism with Brier-optimized incentives

**Enables:**
- **Performance tracking:** Quantitative measure for deliberate practice
- **A/B testing:** Compare forecasting methodologies empirically
- **Incentive design:** Reward accurate probabilistic predictions

## Common Pitfalls

**Pitfall 1: Conflating Low Score with Skill**
- **Warning sign:** 0.05 score from 10 predictions all at 51%/49%
- **Fix:** Check resolution - can you distinguish probability levels?

**Pitfall 2: Ignoring Calibration Components**
- **Warning sign:** Good overall score masking systemic bias
- **Fix:** Decompose into reliability, resolution, and uncertainty

**Pitfall 3: Small Sample Sizes**
- **Warning sign:** Declaring "good forecaster" from 5 predictions
- **Fix:** Require minimum 20-50 forecasts before drawing conclusions

**Pitfall 4: Cherry-Picking**
- **Warning sign:** Only tracking predictions you feel confident about
- **Fix:** Commit to scoring ALL forecasts in domain upfront

**Pitfall 5: Resolution Ambiguity**
- **Warning sign:** Disputes about whether event "really" occurred
- **Fix:** Define resolution criteria precisely when making forecast

## Multi-Category Extension

For events with more than 2 outcomes (e.g., election with 3+ candidates):

**Formula:** BS = (1/N) Σ Σⱼ (fᵢⱼ - oᵢⱼ)²

**Example:** Three-way race forecast of A=60%, B=10%, C=30%
- If A wins: (1-0.6)² + (0-0.1)² + (0-0.3)² = 0.16 + 0.01 + 0.09 = 0.26
- If B wins: (0-0.6)² + (1-0.1)² + (0-0.3)² = 0.36 + 0.81 + 0.09 = 1.26
- If C wins: (0-0.6)² + (0-0.1)² + (1-0.3)² = 0.36 + 0.01 + 0.49 = 0.86

**Note:** Multi-category scores range from 0 (perfect) to 2 (worst possible).

## Validation Checklist

- [ ] All forecasts are probabilistic (0-100%), not binary
- [ ] Resolution criteria defined before outcome known
- [ ] Outcomes recorded honestly (no retroactive "adjustments")
- [ ] Sample size sufficient (20+ forecasts minimum)
- [ ] Score decomposed into calibration and resolution components
- [ ] Comparison made to baseline (random guessing, other forecasters)
- [ ] Trend tracked over time to measure improvement

## Practical Tips

**Tracking System:**
- Spreadsheet columns: Date, Question, Forecast %, Outcome (0/1), Error²
- Running average in final column
- Monthly review of calibration plots

**Calibration Plot:**
- X-axis: Your forecasted probability (grouped into bins)
- Y-axis: Actual frequency of occurrence
- Perfect calibration = diagonal line

**Improvement Signals:**
- Score decreasing over time (learning)
- Calibration plot approaching diagonal
- Resolution increasing (more differentiation)

## Further Reading

- **Original paper:** "Verification of Forecasts Expressed in Terms of Probability" - Glenn W. Brier (1950)
- **"Superforecasting"** - Philip Tetlock (Brier score as key metric)
- **Good Judgment Open:** Platform with automatic Brier score calculation
- **Cultivate Labs:** Forecasting guide with Brier score tutorials
