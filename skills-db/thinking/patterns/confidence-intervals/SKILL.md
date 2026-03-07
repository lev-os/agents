---
name: confidence-intervals
description: Express uncertainty as a plausible range instead of false precision - quantify how confident you are in estimates to avoid overconfidence in decisions
---

# Confidence Intervals

## Overview

Confidence Intervals (CIs) transform point estimates into ranges that quantify uncertainty - the difference between "conversion rate is 5.2%" (false precision) and "conversion rate is between 4.1-6.3% with 95% confidence" (honest uncertainty). Originated in statistical inference, CIs have become essential for decision-making under uncertainty across A/B testing, forecasting, risk assessment, and resource allocation.

A 95% confidence interval means: if you repeated this measurement 100 times, 95 of those intervals would contain the true value. It's NOT "95% chance the true value is in this range" (common misinterpretation) - it's about the reliability of your estimation method, not probability of a specific outcome.

The framework combats overconfidence bias by forcing explicit acknowledgment of uncertainty ranges. Wide intervals signal "we need more data" while narrow intervals justify action. The width reveals how much you actually know versus how much you're guessing.

## When to Use

- A/B testing decisions - is the 2% lift real or random noise?
- Forecasting with small samples - sales projections, user growth, churn rates
- Assessing if effect size is practically meaningful, not just statistically detectable
- Risk assessment - bounding worst-case and best-case scenarios with confidence levels
- Challenging overconfident estimates - "How sure are you? Express it as a range."
- Resource allocation - deciding if you need more data before committing resources

## The Process

### Step 1: Calculate Your Point Estimate

Start with the sample statistic you're measuring - mean, proportion, difference between groups, regression coefficient, etc.

**Example:** After 500 signups, 26 converted to paid. Point estimate = 26/500 = 5.2% conversion rate.

**Critical question:** How reliable is this 5.2% estimate of the true long-term conversion rate?

### Step 2: Determine Confidence Level

Choose how confident you need to be - typically 90%, 95%, or 99%. Higher confidence = wider intervals = more conservative estimates.

**Trade-off:**
- **95% CI:** Standard for most business decisions (balance precision vs. confidence)
- **90% CI:** Faster decision-making, tolerate more risk of being wrong
- **99% CI:** High-stakes decisions (medical, safety, irreversible choices)

**Rule of thumb:** Use 95% unless you have specific reason for higher/lower confidence.

### Step 3: Calculate Standard Error

Standard error measures how much your sample estimate typically differs from the true population value. Smaller samples = larger standard error = wider confidence intervals.

**Formula for proportions:** SE = sqrt(p × (1-p) / n)
- Example: SE = sqrt(0.052 × 0.948 / 500) = 0.0099

**Formula for means:** SE = (standard deviation) / sqrt(n)

**Key insight:** Standard error shrinks with sqrt(n), so 4x sample size only halves uncertainty.

### Step 4: Construct the Interval

Multiply standard error by appropriate z-score or t-score, then add/subtract from point estimate.

**For 95% confidence interval:** Point estimate ± (1.96 × SE)
- Example: 5.2% ± (1.96 × 0.99%) = 5.2% ± 1.94% = [3.26%, 7.14%]

**Interpretation:** "We're 95% confident the true conversion rate is between 3.3% and 7.1%."

### Step 5: Make Decisions Based on Interval Width and Position

Don't just report the interval - use it for decision quality.

**Decision frameworks:**
- **Interval excludes status quo:** Strong evidence for change (e.g., new feature CI is [2%, 8%], old feature was 1%)
- **Interval includes zero:** No clear winner, need more data (difference CI: [-1%, 3%])
- **Interval too wide:** Uncertainty too high for confident decision, increase sample size
- **Interval narrow enough:** Precision sufficient, act on point estimate

**Example:** A/B test shows variant B has [+2%, +12%] lift over variant A. Even worst-case (+2%) beats status quo, so ship variant B with confidence.

### Step 6: Update Sample Size if Needed

If interval is too wide for confident decision, calculate required sample size to achieve desired precision.

**Sample size formula:** n = (z² × p × (1-p)) / (margin of error)²
- To get conversion rate within ±1% at 95% confidence: n = (1.96² × 0.052 × 0.948) / 0.01² ≈ 1,900 samples needed

**Trade-off:** More data narrows interval but costs time and resources. Is precision worth delay?

## Example Application

**Situation:** SaaS startup testing new onboarding flow with 300 users, 21 activated (7% activation rate). Old flow was 5%. Should they roll out the new flow?

**Application:**
- **Point estimate:** 7% activation (21/300)
- **Standard error:** sqrt(0.07 × 0.93 / 300) = 1.47%
- **95% CI:** 7% ± (1.96 × 1.47%) = 7% ± 2.88% = [4.12%, 9.88%]
- **Decision:** Interval includes old 5% rate AND extends significantly above it. Evidence is suggestive but not conclusive - the "true" rate could be anywhere from 4-10%.

**Outcome:** Team decides to test 700 more users before full rollout. At n=1,000, they get tighter CI of [5.5%, 8.5%] which excludes old 5% rate - now confident enough to ship.

## Example Application 2

**Situation:** Clinical trial shows new drug reduces symptoms by 12 points on 100-point scale. Existing drug reduces by 10 points. Is new drug better?

**Application:**
- **New drug 95% CI:** [8, 16] points reduction
- **Existing drug 95% CI:** [7, 13] points reduction
- **Difference:** New drug is +2 points better (point estimate)
- **Critical insight:** CIs overlap heavily - could be +9 points better or -3 points worse

**Decision:** Overlapping intervals mean evidence is inconclusive. Need larger trial or accept that drugs are roughly equivalent. The 2-point difference is within noise.

## Anti-Patterns

- ❌ Reporting only point estimates without ranges (false precision kills decision quality)
- ❌ Confusing "95% confidence" with "95% probability" (it's about method reliability, not outcome probability)
- ❌ Ignoring interval width - a [1%, 50%] interval and [24%, 26%] interval are VERY different
- ❌ Using 95% CI for every decision - high-stakes needs 99%, fast decisions can use 90%
- ❌ Assuming overlapping CIs mean "no difference" (difference-of-intervals ≠ interval-of-differences)
- ❌ Cherry-picking confidence level after seeing data to get desired result (p-hacking cousin)
- ❌ Acting on wide intervals as if they're narrow (3% ± 10% is not actionable at 3%)

## Related

- expected-value-calculation (CIs inform probability distributions for EV)
- thinking-in-bets (probabilistic decision-making under uncertainty)
- calibration (checking if your 95% CIs actually contain true value 95% of time)
- base-rate-analysis (prior probability informs how much to trust narrow CIs)
- bayesian-updating (CIs are frequentist; Bayesian credible intervals are alternative)
