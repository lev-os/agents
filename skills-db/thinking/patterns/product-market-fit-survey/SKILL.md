---
name: product-market-fit-survey
description: Sean Ellis test using the 40% rule to measure if your product has achieved product-market fit by surveying active user disappointment
---

# Product-Market Fit Survey

## Overview

The Product-Market Fit (PMF) Survey, developed by Sean Ellis after analyzing hundreds of startups, provides a quantitative threshold for the historically fuzzy concept of "product-market fit". Ellis discovered that companies achieving sustainable growth consistently had 40%+ of users respond "very disappointed" when asked how they'd feel if the product disappeared. Below 40% signals premature scaling risk; above 40% indicates readiness to invest in growth. The survey consists of three core questions: the must-have question, main benefit question, and user type question. Modern implementations (2025) incorporate behavioral data alongside survey responses, recognizing PMF varies by segment. The framework prevents false positives (users who claim to love product but don't use it) by surveying only recently active users.

## When to Use

- Deciding whether to scale growth investment or improve product first
- Measuring PMF progress quarterly as you iterate core product
- Segmenting customers to find which personas have PMF (vs. overall average)
- Validating new product lines or market expansions before scaling
- Diagnosing why growth has stalled despite marketing spend
- Prioritizing feature roadmap by analyzing "disappointed" user feedback
- Communicating product-market fit progress to investors with data
- Determining when to pivot vs. persevere using objective threshold

## The Process

### Step 1: Define Your Active User Population

Only survey users who have experienced core product value. Criterion: used product at least twice in past 14 days. Exclude: brand new users (under 1 week), dormant users (30+ days inactive), team members/internal users. One-time trial users distort results. **Example:** SaaS tool surveys users with 2+ logins in past 2 weeks and completed at least one core workflow. Excludes: signups who never onboarded, churned users, free trial day 1 users.

### Step 2: Design Three-Question Survey (Keep It Short)

**Question 1 (Must-Have):** "How would you feel if you could no longer use [product]?" Options: Very disappointed, Somewhat disappointed, Not disappointed, N/A - I no longer use [product]. **Question 2 (Main Benefit):** "What is the main benefit you receive from [product]?" (open-ended text). **Question 3 (User Type):** "What type of user are you?" Options: (varies by product - job role, use case, company size). **Example:** Superhuman asks: Q1 (must-have with 4 options), Q2 (main benefit - open text), Q3 (role: Founder/Exec, Sales, Support, Other).

### Step 3: Send Survey Anonymously to Target 40-100 Responses

Anonymous responses reduce social desirability bias (users being "nice"). In-app survey tool (Typeform, Sprig, Pendo) better than email for response rate. Target minimum 30 responses for statistical confidence, 100+ ideal. Single reminder okay, don't spam. Takes users 2-3 minutes. **Example:** Send to 300 active users, expect 30-40% response rate (90-120 responses), sufficient for 95% confidence interval.

### Step 4: Calculate PMF Score (% "Very Disappointed")

PMF Score = (number "very disappointed" / total respondents) × 100. Exclude "N/A - no longer use" from denominator (false actives). **Thresholds:** 40%+ = strong PMF (ready to scale), 25-40% = marginal PMF (iterate core value), under 25% = weak PMF (major changes needed), under 10% = no PMF (pivot risk). **Example:** 120 responses: 52 "very disappointed", 38 "somewhat", 25 "not disappointed", 5 "no longer use". PMF Score = 52/(120-5) = 45.2% → strong PMF.

### Step 5: Segment PMF Score by User Type

Calculate PMF score separately for each user type (Q3). Often reveals: one segment has strong PMF while overall score is weak, company serving wrong customer segment, need to focus on high-PMF cohort and deprioritize others. **Example:** Overall PMF = 32%. By role: Founders 58%, Sales 45%, Support 12%. **Insight:** Product has PMF with founders/sales, not support teams. Roadmap should double down on founder/sales workflows.

### Step 6: Analyze "Main Benefit" Responses (Qualitative)

Read all open-ended Q2 responses. Categorize into themes (5-7 buckets). Compare themes between "very disappointed" vs. "not disappointed" cohorts. High-PMF users often cite different benefits than low-PMF users - reveals true value prop. **Example:** Very disappointed users say "saves me 3 hours/day" (time savings), not disappointed users say "clean interface" (aesthetics). Real value = time savings, not design.

### Step 7: Re-Survey Quarterly and Track Trend

PMF is not static - products can lose fit or gain fit as market evolves. Re-run survey every 3 months with new active user cohort. Track: overall PMF trend, segment PMF trends, benefit theme shifts. Product iterations should move PMF score up. **Example:** Q1 PMF 28% → focus on activation improvements → Q2 PMF 35% → add enterprise features → Q3 PMF 43%. Crossed 40% threshold in 6 months.

## Example Application

**Situation:** Superhuman (email client startup, 2017) ran Sean Ellis survey early and scored 22% PMF - far below 40% threshold. Founders had to decide: pivot, keep iterating, or ignore survey and scale anyway. Survey data showed segmentation opportunity.

**Application**:

**Segment Analysis Revealed:**
- Overall PMF: 22% (weak)
- Founders/Execs: 40%+ (strong)
- Sales reps: 35% (marginal)
- Support teams: 8% (no fit)

**Main Benefit Analysis (Very Disappointed Cohort):**
- "Inbox zero achievable" (mentioned 40% of high-PMF)
- "Keyboard shortcuts save time" (mentioned 35%)
- "Beautifully designed" (mentioned 10%)

**Strategic Decision:** Focus exclusively on users who value speed and inbox zero (founders/execs and sales). Stop optimizing for support teams. Roadmap: faster search, better triage, team collaboration for sales orgs. Deprioritize: integrations for support workflows.

**Outcome:** 18 months of focused iteration on high-PMF segment:
- Overall PMF → 52% (crossed threshold)
- Founder segment PMF → 65%
- Added $10M+ ARR selling to founder/exec buyers
- Superhuman became reference case for PMF methodology

**2025 Update:** Modern PMF assessment adds behavioral signals (retention curve, usage frequency, NPS) alongside survey. Benchmark: SaaS companies with 40%+ PMF and 65%+ D7 retention have 5x better funding outcomes (data from 500+ companies, Q1 2025 benchmarks).

## Anti-Patterns

- Surveying all users including inactive/churned (dilutes signal with users who never got value)
- Surveying too early (users haven't experienced enough of product to judge)
- Changing question wording (breaks comparability across quarters)
- Sample size under 30 (statistically unreliable, high margin of error)
- Ignoring segmentation (one segment may have PMF while overall average doesn't)
- Treating PMF as binary gate (it's a continuous improvement metric)
- Optimizing for PMF score itself (gaming the metric vs. delivering value)
- One-time measurement without quarterly tracking (PMF changes over time)

## Related

- North Star Metric - PMF survey validates North Star captures customer value
- Retention Cohorts - behavioral complement to PMF survey (D7, D30 retention)
- Jobs to Be Done - explains why "very disappointed" users hire your product
- Kano Model - Must-Be features drive PMF, Attractive features don't (until competitors add)
- The Mom Test - interview methodology for following up with survey respondents
- Continuous Discovery - PMF survey is one data input for weekly discovery decisions
- NPS (Net Promoter Score) - measures advocacy (different from PMF/essentiality)
- AARRR Metrics - PMF primarily impacts Activation and Retention layers
