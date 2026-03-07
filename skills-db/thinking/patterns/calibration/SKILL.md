---
name: calibration
description: Align predicted probabilities with actual outcomes - train yourself so things you say are 70% likely actually happen 70% of the time
---

# Calibration

## Overview

Calibration is the alignment between predicted probabilities and actual outcome frequencies - if you claim "70% confidence" and those predictions come true 70% of the time, you're well-calibrated. If they happen 40% or 90% of the time, you're miscalibrated (overconfident or underconfident). Developed through Philip Tetlock's decade-long forecasting research, calibration training transformed amateur "superforecasters" into predictors who outperformed professional intelligence analysts by 30%.

The framework is metacognitive: you're not just predicting outcomes, you're learning to accurately assess the strength of your own beliefs. Most people are terrible at this - they confuse "feels very certain" with "is actually 95% likely" - leading to systematic overconfidence in business decisions, project timelines, and strategic bets.

Calibration requires rigorous tracking: record predictions with explicit percentages, measure Brier scores (accuracy metric), identify systematic biases (always too high/low?), and adjust. Over hundreds of predictions, well-calibrated forecasters develop intuitive sense of uncertainty levels.

## When to Use

- Improving forecast accuracy in business planning, sales projections, product timelines
- Building prediction markets or forecasting tournaments within organizations
- Evaluating expertise - are "industry experts" actually calibrated or just confidently wrong?
- Training teams to express uncertainty honestly instead of false precision
- Debugging overconfidence bias in founders, executives, product managers
- Assessing risk - calibrated probabilities enable better expected value calculations

## The Process

### Step 1: Make Explicit Probability Predictions

Transform vague language ("probably," "unlikely," "very confident") into precise percentages. Force yourself to commit to a number.

**Vague → Calibrated:**
- ❌ "We'll probably hit Q3 revenue target"
- ✅ "I'm 65% confident we hit Q3 revenue target"
- ❌ "This hire seems great"
- ✅ "I'm 80% confident this hire succeeds in role for 18+ months"

**Key technique:** Use 10% increments for granularity (50%, 60%, 70%) instead of just "likely/unlikely."

### Step 2: Track Predictions and Outcomes Systematically

Create a prediction log with: (1) prediction statement, (2) probability assigned, (3) date made, (4) outcome (success/failure), (5) date resolved.

**Tracking spreadsheet columns:**
- Prediction text
- Probability (%)
- Date predicted
- Actual outcome (1 = happened, 0 = didn't happen)
- Date resolved
- Category (hiring, product, revenue, etc.)

**Volume matters:** You need 50-100+ predictions to measure calibration accurately. Single predictions don't reveal systematic bias.

### Step 3: Calculate Brier Score

Brier score measures prediction accuracy on 0-2 scale, where 0 = perfect, 2 = worst possible. Lower scores = better calibration + resolution.

**Formula:** Brier Score = (1/n) × Σ(forecast - outcome)²
- Forecast = your probability (0.7 for 70%)
- Outcome = 1 if happened, 0 if didn't
- n = number of predictions

**Example:**
- Prediction: "70% chance we ship feature by Q3" → shipped on time
- Brier: (0.7 - 1)² = 0.09
- Prediction: "90% chance candidate accepts offer" → they declined
- Brier: (0.9 - 0)² = 0.81 (large penalty for overconfidence)

**Benchmark:** Superforecasters achieve Brier scores of 0.15-0.25. Average forecasters: 0.35-0.50.

### Step 4: Analyze Calibration Curve

Group predictions by probability bucket (60-70%, 70-80%, etc.) and compare predicted probability to actual frequency of outcomes.

**Perfect calibration:**
- 60% predictions → 60% actually happened
- 80% predictions → 80% actually happened
- 90% predictions → 90% actually happened

**Overconfidence pattern:**
- 80% predictions → only 60% happened (systematically too confident)

**Underconfidence pattern:**
- 70% predictions → 85% happened (leaving accuracy on table)

**Visualization:** Plot predicted probability (x-axis) vs. actual frequency (y-axis). Perfect calibration = diagonal line.

### Step 5: Identify and Correct Systematic Biases

Look for patterns in miscalibration - are you overconfident in certain domains? Underconfident in others? Do you cluster predictions at 50%, 80%, 90% instead of using full range?

**Common biases to detect:**
- **Domain overconfidence:** Great calibration in engineering estimates, terrible in hiring
- **50% clustering:** Defaulting to 50% when uncertain (should use wider range)
- **Overconfidence in rare events:** Saying 95% for things that happen 75% of time
- **Outcome-blind anchoring:** Anchoring on initial view, not updating with new data

**Correction strategy:** Apply domain-specific adjustments. If you're always 15 points too high on hiring, mentally subtract 15 points before recording prediction.

### Step 6: Practice Deliberate Calibration Training

Calibration improves through feedback loops - predict, observe outcome, update mental model, repeat. Superforecasters practice daily.

**Training exercises:**
- **Trivia calibration:** Predict "% confident I know the answer" then check - forces you to distinguish 60% from 90%
- **Same-day resolution:** Predict events with quick feedback (will meeting run over time? will build pass?)
- **External benchmarks:** Compare your forecasts to prediction markets, other forecasters
- **Pre-mortems:** Before launching, predict "% chance we encounter X problem" - revisit after launch

**Key insight:** Calibration is a skill, not a trait. Even poor forecasters improve 20-30% with training.

## Example Application

**Situation:** Product manager predicting feature ship dates over 6 months, tracking 25 predictions.

**Application:**
- **Initial predictions:** Average 85% confidence, actual delivery rate: 60% (severe overconfidence)
- **Brier score:** 0.42 (below average)
- **Pattern identified:** Always underestimate integration complexity, overestimate team velocity
- **Adjustment:** Reduce confidence by 15 points on features requiring backend integration
- **Month 4-6 results:** 72% confidence, 68% delivery rate (much better calibration)
- **New Brier score:** 0.28 (approaching superforecaster level)

**Outcome:** PM now expresses uncertainty honestly, sets realistic stakeholder expectations, and prioritizes better (focuses on high-confidence ships).

## Example Application 2

**Situation:** Executive team forecasting quarterly OKR achievement, historically claiming "80% confident" but only hitting 50%.

**Application:**
- **Intervention:** Implement prediction tracking across 12 OKRs per quarter
- **Training:** Each exec predicts individual OKR success probability before quarter starts
- **Q1 calibration:** 78% average prediction, 45% actual (massive overconfidence, Brier 0.48)
- **Feedback session:** Review calibration curves, identify systematic biases (underestimate competitor responses, overestimate user adoption)
- **Q2-Q3 adjustment:** Average predictions drop to 62%, actual outcomes rise to 58% (better planning + realistic confidence)
- **Q3 Brier score:** 0.31 (significant improvement)

**Result:** More honest uncertainty led to better resource allocation, contingency planning, and stakeholder trust.

## Anti-Patterns

- ❌ Vague confidence language ("probably," "likely") instead of explicit percentages - can't measure calibration
- ❌ Never tracking predictions - calibration requires feedback loops, not just guessing
- ❌ Clustering predictions at 50%, 80%, 95% - use full granularity (55%, 72%, 88%)
- ❌ Judging calibration on <20 predictions - need volume to detect systematic bias
- ❌ Ignoring domain differences - calibration varies across areas of expertise
- ❌ Confusing confidence with accuracy - you can be perfectly calibrated at 60% (not great accuracy)
- ❌ Updating predictions without recording original - defeats feedback loop learning
- ❌ Treating Brier score as only metric - calibration curve reveals different issues than resolution

## Related

- thinking-in-bets (probabilistic decision-making that depends on calibrated probabilities)
- superforecasting (broader forecasting framework where calibration is core skill)
- confidence-intervals (statistical method for expressing uncertainty ranges)
- bayesian-updating (how to update probabilities as new evidence emerges)
- brier-score (mathematical measure of forecast accuracy and calibration)
