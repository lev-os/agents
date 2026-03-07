---
name: Base Rates
description: Statistical frequency of events in a reference class that provides the starting point for predictions before considering specific case details
---

# Base Rates

## Overview

Base rates are the underlying statistical frequencies or prior probabilities of events in a population or reference class. They represent "what usually happens" before you know any specific details about a particular case. Base rate thinking is a cornerstone of rational decision-making because it anchors predictions in empirical reality rather than intuition or vivid examples.

Discovered and formalized by Daniel Kahneman and Amos Tversky in their research on judgment under uncertainty, base rate neglect is one of the most common and costly cognitive biases. People systematically underweight or ignore statistical information (base rates) in favor of specific, individuating information—even when the base rate is more predictive.

The classic illustration: If you're told someone is shy, loves puzzles, and dislikes crowds, is she more likely a librarian or a farmer? Most people say librarian, but there are 20× more farmers than librarians in the U.S., making farmer far more probable even given the personality description.

Using base rates properly means starting with the outside view (what usually happens in similar cases) before adjusting for the inside view (what's special about this case). This produces dramatically more accurate predictions across domains from medical diagnosis to startup success to hiring.

**Key insight**: Specific, vivid details feel more important than statistical base rates, but base rates are usually more predictive. Start with "what usually happens" before considering "what's special here."

## When to Use

Apply base rate thinking in these situations:

- **Predictions and forecasting**: Estimating probability of any outcome where historical data exists
- **Medical diagnosis**: Considering disease prevalence before symptoms (avoiding false positives)
- **Hiring decisions**: Starting with typical success rates for candidates from similar backgrounds
- **Startup evaluation**: Using historical success rates for similar companies before evaluating the specific team
- **Investment decisions**: Considering typical returns in an asset class before evaluating specific opportunities
- **Risk assessment**: Starting with how often similar risks materialize before analyzing specifics
- **Customer conversion**: Using industry conversion rates as baseline before optimizing
- **Project planning**: Starting with typical timelines and budgets for similar projects

**Trigger question**: "What usually happens in cases like this?" or "What's the historical success rate for this type of situation?"

## Process

### 1. Identify the Reference Class

Determine what category or population this case belongs to. The reference class provides the base rate.

- Define the relevant comparison group (e.g., "enterprise SaaS startups" not just "startups")
- Consider multiple reference classes if appropriate (narrow and broad)
- Verify sufficient sample size (100+ cases preferred, 10+ minimum)
- Ensure reference class is truly comparable

**Action**: Write down 2-3 possible reference classes, from most specific to most general.

### 2. Research the Base Rate

Find statistical data on success/failure rates, typical outcomes, or frequency in the reference class.

Sources to check:
- Academic research and meta-analyses
- Industry reports and benchmarks
- Government statistics and databases
- Historical company data or case studies
- Expert surveys with large sample sizes

**Action**: Document the base rate as a percentage or ratio with source citation.

### 3. Assess Base Rate Quality

Evaluate how reliable and relevant the base rate is for your situation.

Quality factors:
- **Sample size**: Larger samples = more reliable base rates
- **Recency**: More recent data may be more relevant (technology changes fast)
- **Similarity**: How comparable is the reference class to your case?
- **Selection bias**: Is the data representative or cherry-picked?

**Action**: Rate base rate quality as High/Medium/Low and note any concerns.

### 4. Start With the Base Rate

Use the base rate as your initial probability estimate before considering case-specific details. This is your "outside view."

- If base rate is 30% success, start at 30%
- Resist the urge to immediately adjust based on how this case "feels"
- Acknowledge that most cases feel special but aren't
- Document your starting point explicitly

**Action**: Write down "Initial estimate based on base rate: X%"

### 5. Identify Individuating Information

List specific details about this case that might justify adjusting away from the base rate.

Relevant individuating information:
- Truly unusual circumstances not captured in reference class
- Strong predictive indicators (backed by research when possible)
- Information that would change your reference class choice
- Evidence that distinguishes this case from typical examples

**Action**: List 3-5 case-specific factors and assess whether each is genuinely unusual or just feels special.

### 6. Adjust Conservatively From Base Rate

Update your estimate using specific information, but make smaller adjustments than feel natural. Research shows people over-update on specific details and under-weight base rates.

Adjustment principles:
- Only adjust for information that's genuinely diagnostic (proven to predict outcome)
- Make adjustments smaller than your gut suggests (halve your initial adjustment)
- Stay within 20-30% of base rate unless evidence is overwhelming
- Justify every 10% adjustment with concrete evidence

**Action**: Calculate adjusted probability and document reasoning for each adjustment increment.

### 7. Check for Base Rate Neglect

Review your final estimate to ensure you haven't abandoned the base rate in favor of compelling specifics.

Warning signs of base rate neglect:
- Your final estimate is more than 40% different from base rate
- You can't articulate why this case is genuinely exceptional
- You're relying on anecdotes or single examples rather than patterns
- The specific details are emotionally compelling but not diagnostic

**Action**: If final estimate deviates significantly from base rate, re-examine whether adjustment is justified.

## Example

**Scenario**: Your company is considering hiring a VP of Sales who has impressive credentials: graduated from Stanford, worked at two successful startups, excellent references, and compelling interview.

**Base rate thinking in action**:

1. **Reference class**: VP-level sales hires at B2B SaaS companies

2. **Base rate research**:
   - General executive hires succeed ~50% of the time
   - Sales VPs specifically: 60% succeed (Topgrading research)
   - VP hires with 2+ startup references: 65% succeed
   - Starting estimate: **65%**

3. **Base rate quality**: Medium-High
   - Sample: Based on studies of 1,000+ executive hires
   - Recency: Data from last 5 years
   - Similarity: Directly comparable to our situation
   - Caveat: Success definition varies across studies

4. **Start at 65%**: Before considering anything specific about this candidate, the base rate suggests 65% chance of success.

5. **Individuating information**:
   - Stanford pedigree (but research shows school prestige doesn't predict sales success)
   - Two successful startups (already captured in reference class)
   - Excellent references (but 90% of candidates have good references due to selection)
   - Compelling interview (but interview performance weakly correlates with job performance)
   - Has sold similar deal sizes in similar market (+meaningful)
   - Built team from 0 to 10 exactly as we need (+meaningful)

6. **Conservative adjustment**:
   - Deal size/market similarity: +5% (65% → 70%)
   - Team building experience: +5% (70% → 75%)
   - Not adjusting for: prestige, general success, references, interview (not diagnostic)
   - **Final estimate: 75%**

7. **Check for neglect**:
   - Adjustment of 10% from base rate (65% → 75%) seems reasonable
   - Based on two genuinely diagnostic factors
   - Resisted temptation to weight impressive but non-predictive details
   - Still acknowledging that 1 in 4 candidates like this fail

**Decision**: Hire the candidate but design onboarding assuming 75% success rate. Have a 30/60/90 day performance review with clear metrics, because there's still a 25% chance this doesn't work out despite excellent credentials.

**Contrast with base rate neglect**: Without base rate thinking, you might estimate 90%+ success given the impressive profile, leading to insufficient onboarding support and delayed recognition if issues emerge.

## Anti-Patterns

**Ignoring base rates entirely**: Jumping straight to evaluating specific details without establishing what usually happens. This guarantees overconfidence and poor calibration.

**Cherry-picking reference classes**: Choosing a reference class that confirms your intuition rather than the most appropriate comparison group. If you want to be optimistic, you'll find an optimistic reference class.

**Treating all cases as special**: Believing "this time is different" or "this case is unique" so base rates don't apply. Most cases that feel special aren't, and even truly special cases should start with base rates.

**Over-adjusting on vivid details**: Making large probability shifts based on emotionally compelling but statistically weak information (story about one success, charismatic founder, compelling pitch).

**Using base rates without understanding**: Mindlessly applying statistics without considering whether the reference class is appropriate or the data is reliable.

**Confusing individual prediction with group prediction**: Base rates tell you about populations, not individuals with certainty. A 70% base rate means 3 in 10 fail—it doesn't tell you which specific one will fail.

**Failing to update base rates**: Using outdated statistics when the world has changed (e.g., startup success rates pre- and post-2008 are different).

## Related Frameworks

- **Bayesian Reasoning**: Formal framework for starting with prior probabilities (base rates) and updating with evidence.
- **Outside View vs. Inside View**: Outside view uses base rates; inside view focuses on case specifics. Combine both for best predictions.
- **Reference Class Forecasting**: Systematic methodology for finding and using base rates in project planning and predictions.
- **Regression to the Mean**: Related statistical principle where extreme outcomes tend toward average (base rate) over time.
- **Representativeness Heuristic**: The cognitive bias that causes base rate neglect by making specific details feel more important than statistics.
- **Prior Probability**: Another term for base rates in Bayesian reasoning—the probability before considering evidence.
- **Meta-Analysis**: Statistical technique for combining multiple studies to get better base rate estimates.
- **Superforecasting**: Expert prediction methodology that heavily emphasizes starting with base rates.
