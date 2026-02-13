---
name: base-rate-analysis
description: Start with statistical baseline frequencies before considering individual case details - combat base rate neglect by anchoring on "what usually happens"
---

# Base Rate Analysis

## Overview

Base Rate Analysis is the practice of starting probability assessments with statistical baseline frequencies (base rates) before incorporating case-specific details. Pioneered by Kahneman and Tversky's research on judgment under uncertainty, the framework combats "base rate neglect" - humans' systematic tendency to overweight vivid individual information while ignoring statistical context.

The classic demonstration: told "Steve is shy, organized, detail-oriented" and asked if he's a librarian or farmer, most choose librarian (representativeness heuristic). But with 20x more farmers than librarians in the population, Steve is far more likely to be a farmer - even if he matches librarian stereotypes. Base rate (population frequency) should dominate individual description when the description has limited diagnostic power.

Base rate neglect destroys decision quality in hiring ("this candidate seems brilliant" ignores low success rate of similar profiles), startups ("our idea is special" ignores 90% failure rate), medical diagnosis (rare disease with common symptoms), and forecasting (vivid story vs. statistical trends). The fix: always ask "what usually happens in situations like this?" before considering unique factors.

## When to Use

- Hiring decisions - candidate seems great, but what's success rate of similar profiles?
- Startup/product bets - "this will be different" requires overcoming base rate odds
- Medical diagnosis - common diseases are common, rare diseases are rare (even with symptoms)
- Fraud detection - vivid suspicious behavior vs. actual fraud frequency
- Forecasting - anchoring on statistical trends before adjusting for unique factors
- Risk assessment - base rate of project failure, accident frequency, etc.

## The Process

### Step 1: Identify the Reference Class

Before evaluating the individual case, define the broader category it belongs to. What's the statistical population this case draws from?

**Examples:**
- **Hiring:** "Software engineers with 3-5 years experience from mid-size startups"
- **Startup:** "B2B SaaS companies targeting SMB customers in healthcare vertical"
- **Diagnosis:** "Patients presenting with headache + fever in primary care setting"
- **Project:** "Complex software rewrites with 18-month timelines"

**Critical step:** Choose reference class narrow enough to be relevant, broad enough to have statistical data.

### Step 2: Find Base Rate Data

Research or estimate the frequency of the outcome in the reference class. This is your statistical anchor.

**Sources:**
- Industry benchmarks (startup survival rates, hiring success rates)
- Historical company data (past project success rates)
- Academic research (medical diagnosis rates, fraud frequencies)
- Informed estimation if no data (better than ignoring base rates entirely)

**Example base rates:**
- **VC-backed startups reaching $100M revenue:** ~1-2%
- **Senior engineering hires still at company after 2 years:** ~65%
- **Complex software rewrites finishing on time:** ~20-30%
- **Patients with headache + fever having meningitis:** 0.01% (very rare)

### Step 3: Anchor Your Initial Probability on Base Rate

Start your probability estimate at the base rate before considering individual case specifics. This combats the natural tendency to jump straight to "Steve seems like a librarian."

**Bayesian formula (simplified):**
- **Prior probability:** Base rate (what usually happens)
- **Posterior probability:** Adjusted after considering case-specific evidence
- **Start with prior, then update (don't skip straight to posterior)**

**Example:** Evaluating startup idea.
- **Step 1:** Base rate - 10% of startups succeed
- **Step 2:** Initial probability - "Absent any other info, this has 10% chance"
- **Step 3:** Now consider unique factors (team, market, traction, etc.)

### Step 4: Adjust Based on Diagnostic Individual Evidence

Update from base rate ONLY if you have genuinely diagnostic information - evidence that reliably distinguishes success from failure cases.

**High diagnostic value (adjust significantly):**
- Medical test with 95% sensitivity/specificity
- Prior startup success by founder
- Demonstrated product-market fit (retention cohorts)

**Low diagnostic value (barely adjust from base rate):**
- Personality traits ("seems organized" = weak predictor)
- Enthusiastic customer interviews (selection bias)
- Confidence/passion (uncorrelated with outcomes)

**Adjustment magnitude:** How much does evidence change odds?
- **Weak evidence:** Shift 5-10 percentage points from base rate
- **Moderate evidence:** Shift 20-30 percentage points
- **Strong evidence:** Can shift 40-60 points if truly diagnostic

### Step 5: Calculate Final Probability Using Bayes Rule

Formally update base rate using Bayes' theorem when you have conditional probabilities.

**Bayes formula:**
P(A|B) = [P(B|A) × P(A)] / P(B)

**Example: Medical diagnosis**
- **Base rate:** 1% of patients have disease (P(A) = 0.01)
- **Test accuracy:** 90% sensitive (P(B|A) = 0.9 if disease present)
- **False positive rate:** 10% (P(B|not-A) = 0.1 if disease absent)
- **Test positive - what's probability of disease?**
  - P(disease|positive) = (0.9 × 0.01) / [(0.9 × 0.01) + (0.1 × 0.99)]
  - = 0.009 / 0.108 = 8.3%

**Key insight:** Even with 90% accurate test, positive result only raises disease probability from 1% to 8.3% because base rate is so low. Most positive tests are false positives when disease is rare.

### Step 6: Combat Base Rate Neglect by Making It Explicit

When presenting analysis, force yourself to state base rate before individual assessment. This resists narrative bias.

**Framework for communication:**
1. "The base rate for X is Y%"
2. "In this specific case, we have the following distinguishing evidence: [list]"
3. "Adjusting from base rate Y%, my estimate is Z%"
4. "This adjustment is justified because [diagnostic evidence explanation]"

**Example:** "The base rate for senior hires staying 18+ months is 65%. This candidate has strong referrals from past managers (diagnostic) and accepted below-market comp (commitment signal). I estimate 80% retention probability - a 15-point upward adjustment from base rate."

## Example Application

**Situation:** Startup founder pitching VC - "We have incredible team, huge market, innovative AI technology. What are our odds?"

**Base rate neglect version:**
- VC focuses on team pedigree, market size story, technology demos
- Estimates 60% chance of success based on compelling narrative
- Ignores that 90% of similar startups fail

**Base rate analysis version:**
- **Step 1:** Reference class: "Pre-seed B2B AI SaaS startups"
- **Step 2:** Base rate: ~8-10% reach meaningful success
- **Step 3:** Anchor at 10% prior probability
- **Step 4:** Diagnostic evidence: Team has prior startup success (+20 points), early customer traction (+15 points)
- **Step 5:** Adjusted probability: 45% (10% base + adjustments)
- **Outcome:** Still optimistic, but realistic about odds - 45% is high for this reference class, not guaranteed success

## Example Application 2

**Situation:** Hiring manager interviewing candidate who "absolutely crushed the technical interview" and "would be perfect for the team."

**Base rate neglect:**
- Hire immediately based on strong interview performance
- Ignore that interview performance is weakly correlated with job success

**Base rate analysis:**
- **Base rate:** 60% of hires at this level succeed (perform well for 18+ months)
- **Interview diagnostic value:** Moderate - raises success probability by ~15 points (research shows interviews are noisy)
- **Final estimate:** 75% success probability (60% base + 15% interview boost)
- **Decision framework:** 75% is good but not certain - implement 90-day check-in, invest in onboarding
- **Result:** Realistic expectations prevent shock if hire doesn't work out, better support during ramp

## Anti-Patterns

- ❌ Jumping straight to individual case analysis without checking base rates
- ❌ Treating all evidence as equally diagnostic (vague impressions ≠ hard metrics)
- ❌ Over-adjusting from base rate based on weak evidence (narrative seduction)
- ❌ Choosing overly narrow reference class to game base rate ("our situation is unique")
- ❌ Confusing vivid examples with statistical frequencies (availability bias compounds neglect)
- ❌ Ignoring base rates because "this time is different" (usually it's not)
- ❌ Using base rate to dismiss strong diagnostic evidence (opposite error - don't ignore good data)

## Related

- bayesian-updating (formal framework for updating base rates with new evidence)
- outside-view (reference class forecasting is base rate analysis for project planning)
- representativeness-heuristic (bias that causes base rate neglect)
- calibration (well-calibrated forecasts properly weight base rates)
- reference-class-forecasting (planning fallacy cure through base rate anchoring)
