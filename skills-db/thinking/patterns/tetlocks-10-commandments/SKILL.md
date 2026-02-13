---
name: tetlocks-10-commandments
description: Improve forecast accuracy by following Philip Tetlock's 10 evidence-based principles from superforecaster research distinguishing top 2% predictors
---

# Tetlock's 10 Commandments for Superforecasting

## Overview
Philip Tetlock's 20-year Good Judgment Project identified "superforecasters"—the top 2% of predictors who consistently beat experts, pundits, and prediction markets. His 10 Commandments distill their practices into actionable principles: think probabilistically, update incrementally, beware biases, aggregate perspectives, track accuracy, embrace uncertainty.

## When to Use
- Making predictions about uncertain future events
- Improving decision-making under uncertainty
- Evaluating others' forecasts (consultants, analysts, pundits)
- Building forecasting teams or processes
- Learning from prediction failures
- Competing in prediction markets or tournaments

## The 10 Commandments

### 1. Triage - Focus Effort Where It Matters
Don't waste time on unpredictable questions ("Will aliens visit?") or trivially predictable ones ("Will sun rise tomorrow?"). Focus on questions in the "Goldilocks zone": difficult but not impossible.

**Example:** Skip: "Bitcoin price in 2030" (too noisy). Focus: "Will Bitcoin ETF be approved by SEC within 18 months?" (resolvable, valuable).

### 2. Break Down Complex Questions (Fermi Estimation)
Decompose vague questions into answerable sub-questions. Aggregate sub-forecasts to avoid "holistic" guessing.

**Example:** "Will fusion energy be commercially viable by 2040?" → Break into: "Will ITER succeed?" "Will private fusion reach breakeven?" "Will costs drop below $0.10/kWh?" "Will regulations allow deployment?"

### 3. Strike the Right Balance Between Inside and Outside Views
Start with base rate (outside view): "What happened in similar cases?" Then adjust for unique details (inside view). Don't skip base rate, don't ignore specifics.

**Example:** "Will our startup succeed?" Outside view: 90% startups fail. Inside view: Strong team, proven traction. Adjusted forecast: 30% success (better than base, but not ignoring statistics).

### 4. Strike the Right Balance Between Under- and Overreacting to Evidence
Update beliefs when new evidence arrives, but don't whipsaw. Bayesian updating: Weight new evidence proportional to its quality and relevance.

**Example:** Forecast: 60% chance of product launch success. New evidence: One beta tester complains. Don't drop to 20% (overreacting). Update to 55% (slight adjustment for weak signal).

### 5. Look for the Clashing Causal Forces
Map competing forces pushing in opposite directions. Strong forecasters consider both bullish and bearish factors simultaneously.

**Example:** EV adoption forecast: Bullish forces (battery costs falling, climate policy). Bearish forces (charging infrastructure gaps, consumer range anxiety). Weigh both, don't cherry-pick.

### 6. Strive to Distinguish as Many Degrees of Doubt as Data Allow
Avoid round numbers (50%, 75%). Use granular probabilities (63%, 72%) when evidence supports it. Precision forces you to process information deeply.

**Example:** Don't say "probably" or "75%." Say "67% confident based on 3 comparable precedents showing 2/3 success rate."

### 7. Strike the Right Balance Between Under- and Overconfidence
Humans are overconfident on hard questions, underconfident on easy ones. Calibrate: Track "70% forecasts"—do they happen 70% of the time?

**Example:** "90% sure this feature ships on time." Track 50 such forecasts. Only 60% shipped on time. You're overconfident. Recalibrate "90%" to "60%."

### 8. Look for the Errors Behind Your Mistakes
When wrong, diagnose: Was it poor process (didn't check base rate), bad luck (correctly assessed 80% odds, hit the 20%), or missing information?

**Example:** Predicted 80% chance competitor wouldn't launch in Q1. They did. Diagnosis: Missed insider information (process error), not bad luck. Fix: Build better intelligence gathering.

### 9. Bring Out the Best in Others, Bring Out the Best in Yourself
Form diverse teams. Encourage dissent. Reward accuracy over ego. Practice intellectual humility.

**Example:** Amazon's "disagree and commit"—require contrary views before alignment. Surfaces blind spots.

### 10. Master the Error-Balancing Cycle
Iterate: Forecast → Track → Analyze errors → Adjust process → Repeat. Superforecasters spend 50% more time than average forecasters on post-mortems.

**Example:** Quarterly review: "I forecasted 8 events at 70%, only 4 happened (50%). I'm overconfident. Next quarter, my 70% threshold requires stronger evidence."

## Example Application

**Situation:** Product manager forecasting whether new feature will increase retention >10% in 3 months.

**Application**:
- **Commandment 1 (Triage)**: Predictable timeframe (3 months), measurable (10%), worth effort. Good question.
- **Commandment 2 (Break down)**: Sub-questions: Will users discover feature? Will they understand it? Will they find it valuable? Will it reduce churn drivers?
- **Commandment 3 (Outside/inside)**: Outside view: Similar features increased retention 5-15% (median 8%). Inside view: Our user research shows strong demand. Forecast: 60% chance of >10%.
- **Commandment 4-5 (Evidence/forces)**: Bullish: User interviews positive. Bearish: Feature is complex, onboarding weak. Balance: Lower to 55%.
- **Commandment 6 (Precision)**: Not "probably" or "60%." Use 55% based on specific evidence weighting.
- **Commandment 7 (Calibration)**: Check past "55% forecasts"—did they happen ~55% of time? Yes? Maintain.
- **Commandment 8-10 (Tracking)**: Set reminder to analyze in 3 months, learn from outcome, update process.

**Outcome:** Feature increased retention 12%. Forecast was calibrated (55% for a yes, outcome was yes, though close). Process validated. Improve calibration over 100 forecasts.

## Anti-Patterns
- ❌ Skipping base rates (inside view only)
- ❌ Never updating forecasts ("set it and forget it")
- ❌ Using vague language ("might," "could") instead of numbers
- ❌ Judging forecast quality by outcome alone (resulting bias)
- ❌ Not tracking forecasts → no calibration feedback loop
- ❌ Overconfidence on every forecast (98% sure about everything)
- ❌ Treating forecasting as innate talent vs. trainable skill

## Related
- thinking-in-bets
- bayes-theorem
- base-rate-analysis
- calibration
- superforecasting
