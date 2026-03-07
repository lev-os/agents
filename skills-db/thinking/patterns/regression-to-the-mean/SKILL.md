---
name: regression-to-the-mean
description: Extreme outcomes tend to be followed by more average ones due to statistical variation
---

# Regression to the Mean

## Overview

Regression to the mean is the statistical phenomenon where extreme measurements tend to be followed by less extreme ones, moving back toward the average. This isn't magic or causation - it's pure mathematics. When performance depends on both skill and luck, extreme results typically involve luck aligning with skill. Since luck varies randomly, the next measurement likely has average luck, so the result moves toward the mean. Understanding this prevents one of the most common errors in decision-making: mistaking statistical reversion for causal effects.

Daniel Kahneman discovered the power of this insight while teaching Israeli Air Force flight instructors. They believed punishment worked better than praise because cadets improved after criticism but got worse after praise. The reality? Regression to the mean. Extremely bad performances (already below average) were likely followed by better ones regardless of criticism. Extremely good performances (already above average) were likely followed by worse ones regardless of praise. The instructors were seeing pure statistics and inventing causal stories. This pattern repeats everywhere: business performance, sports, investing, health outcomes.

## When to Use

- **Performance evaluation**: Distinguishing genuine improvement from statistical reversion
- **Talent assessment**: Avoiding over-reaction to single extreme performances
- **Investment decisions**: Understanding why hot funds cool off and cold funds warm up
- **Medical treatment**: Recognizing when symptoms improve naturally versus due to treatment
- **Quality control**: Not over-correcting processes when extreme results appear
- **Prediction**: Making more accurate forecasts by accounting for regression

## The Process

### Step 1: Recognize When Regression to the Mean Applies
Regression to the mean occurs whenever outcomes depend on both systematic factors and random variation.

**Required conditions**:
- Measurement includes random error or luck component
- You're observing an extreme value (far from average)
- Underlying ability/quality hasn't fundamentally changed
- Repeated measurements are possible

**Common scenarios**:
- Sports performance (skill + luck on the day)
- Test scores (knowledge + question selection + mood)
- Business metrics (quality + market conditions + randomness)
- Medical symptoms (underlying health + daily variation)
- Stock returns (company fundamentals + market noise)

**Key insight**: The more extreme the initial measurement, the stronger regression to the mean will be on the next measurement.

### Step 2: Decompose Performance into Signal and Noise
Every measurement combines true ability (signal) with random variation (noise).

**Signal (systematic)**:
- True skill, ability, or quality
- Persists across measurements
- What you're trying to measure

**Noise (random)**:
- Luck, measurement error, external factors
- Varies randomly across measurements
- Obscures the true signal

**Mathematical reality**:
- Extreme performance = High signal + Lucky noise
- Or: Extreme performance = Average signal + Very lucky noise
- Or: Extreme performance = Low signal + Extremely lucky noise
- Next measurement: Signal stays same, but noise regresses to average

**Example - Baseball batting**:
- Player bats .450 in April (extreme)
- Components: .300 true skill + .150 luck (hot streak, weak pitchers, good calls)
- May prediction: .300 + 0 expected luck = .300 (regression toward true ability)

### Step 3: Calculate the Correlation to Predict Regression Strength
The degree of regression depends on the correlation between measurements.

**Perfect correlation (r = 1.0)**:
- No random component
- Extreme value means genuinely extreme ability
- No regression to mean
- Example: Height (measuring same person twice gives same result)

**Zero correlation (r = 0.0)**:
- Pure randomness
- Extreme value means nothing about next measurement
- Complete regression to population mean
- Example: Coin flips (100 heads doesn't predict next flip)

**Partial correlation (0 < r < 1)**:
- Mix of skill and luck
- Extreme value regresses partially toward mean
- Most real-world phenomena
- Formula: Predicted next value = r × (current value) + (1-r) × (population mean)

**Example - Test scores with r = 0.7**:
- Student scores 120 on test (mean = 100, you scored 20 above)
- Prediction for next test: 0.7 × 20 + 100 = 114
- Regress 30% of the way back to mean (from 120 to 114)

### Step 4: Avoid Inventing Causal Explanations for Statistical Reversion
The most common error is creating causal stories when you're just seeing regression to the mean.

**Classic mistake pattern**:
1. Observe extreme performance
2. Implement intervention (punishment, praise, strategy change)
3. Performance regresses toward mean
4. Conclude intervention caused the change
5. **Wrong**: The regression would have happened anyway

**Kahneman's flight instructor story**:
- Bad landing (extreme performance) → Instructor yells → Next landing better
- Great landing (extreme performance) → Instructor praises → Next landing worse
- Conclusion: Punishment works, praise backfires
- Reality: Both groups regressing to their average ability

**Business example**:
- Salesperson has worst month ever → Manager implements coaching → Next month improves
- Manager concludes coaching works
- Reality: Worst month probably involved bad luck; regression to mean would happen without intervention

**How to avoid**:
- Compare to control group (people who didn't receive intervention)
- Look for repeated extreme performances (if it happens consistently, it's not regression)
- Check baseline correlation (how much variation is random vs. systematic)

### Step 5: Use Regression to Make Better Predictions
When predicting future performance from current extreme values, adjust toward the mean.

**Naive prediction (wrong)**:
- Player batting .450 → Predict .450 for rest of season
- Company grew 50% last year → Predict 50% growth this year
- Ignores regression to mean

**Regression-adjusted prediction (better)**:
- Know the correlation between periods (historical data)
- Extreme current performance → Predict between current and average
- The more extreme, the more you adjust toward mean

**Example - Mutual fund returns**:
- Fund returned 40% last year (market average: 10%)
- Historical correlation between consecutive years: r = 0.3
- Prediction: 0.3 × 40 + 0.7 × 10 = 19% (not 40%)
- Research shows: Top-performing funds regress dramatically toward average

**Practical rule**: Expect roughly half the extreme deviation to disappear due to regression (varies by domain).

### Step 6: Recognize Regression in Medical and Health Contexts
Many "miracle cures" are just regression to the mean.

**The pattern**:
- Symptom reaches extreme (severe pain, high blood pressure, etc.)
- Patient seeks treatment
- Symptom improves
- Treatment gets credit
- Reality: Symptoms naturally fluctuate; extreme values regress

**Example - Cold remedies**:
- Feel worst on Day 3 → Take remedy → Feel better Day 4-5
- Did remedy work, or did cold naturally peak and regress?
- Most colds peak days 2-4, then improve regardless of treatment

**How to detect real treatment effects**:
- Randomized controlled trials with placebo groups
- Compare regression in treatment vs. control
- If treatment group regresses MORE than control, treatment works
- If both groups regress equally, it's just regression to mean

**Sports injury example**:
- Athlete performs badly → Gets diagnosed with minor issue → Treatment → Performance improves
- Was treatment effective, or were they regressing from unlucky bad performance?

### Step 7: Build Regression Awareness into Organizational Systems
Create processes that account for regression rather than over-reacting to extremes.

**Quality control**:
- Don't adjust process every time you see extreme result
- Use control charts with statistical bounds
- Only intervene when patterns appear, not single extremes

**Performance management**:
- Don't promote solely based on last period's extreme performance
- Look for sustained high performance across multiple periods
- Expect "hot hands" to cool off

**Evaluation systems**:
- Measure performance across multiple periods
- Weight long-term average more than recent extremes
- Account for regression when setting expectations

**Forecasting**:
- Build regression to mean into models
- Don't extrapolate extremes linearly
- Use historical correlation to adjust predictions

## Example: "Sports Illustrated Cover Jinx"

**The phenomenon**: Athletes featured on Sports Illustrated covers often have worse performance afterward.

**Naive explanation**: 
- The cover jinxes them
- Fame and pressure hurt performance
- Magazine curse

**Regression to the mean explanation**:
- Athletes get on cover BECAUSE of extreme recent performance
- Extreme performance = Skill + Lucky streak
- Next period: Skill remains, but luck regresses to average
- Performance declines toward their true ability level
- No jinx - pure statistics

**Evidence**:
- Researchers analyzed pre-cover vs. post-cover performance
- Decline matches regression to mean predictions exactly
- Control group (athletes NOT on cover but with similar extreme performance) showed same decline
- Conclusion: 100% explained by regression to mean, 0% by jinx

**Lesson**: Before inventing causal stories for performance declines after extreme success, check if it's just regression to the mean.

## Anti-Patterns

**"They performed great, then I praised them, and they got worse - praise backfires"**: No, extreme performance naturally regresses. Praise isn't causing decline.

**"The worst performers improved after intervention - my intervention works"**: Maybe, or maybe they were just regressing from extremely unlucky period. Need control group.

**"This stock fund crushed the market last year, so I'm investing heavily"**: Past extreme returns don't predict future returns. Expect regression toward market average.

**"My symptoms were terrible, I tried this supplement, now I'm better - it works"**: Symptoms fluctuate. Extreme symptoms naturally improve. Need RCT to know if supplement helped.

**"We had our worst quarter ever, implemented new strategy, next quarter improved - success"**: Worst quarter probably involved bad luck. Would have improved without strategy change.

**"Top performers deserve huge bonuses based on last quarter"**: Last quarter might be extreme luck. Bonuses should be based on sustained multi-period performance.

## Related Frameworks

- **Normal Distribution**: Context where regression to mean is strongest and most predictable
- **Randomness**: Understanding role of luck and chance in outcomes
- **Signal vs. Noise**: Decomposing performance into systematic and random components
- **Base Rates**: Using population averages as anchor for predictions
- **Correlation**: Strength of correlation determines degree of regression
- **Hindsight Bias**: Tendency to invent causal stories for statistical patterns
- **Survivorship Bias**: Related error where we focus on extreme performers who "survived"
