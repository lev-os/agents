---
name: delphi-method
description: Build consensus expert forecasts through iterative anonymous surveys with controlled feedback to minimize groupthink and anchor biases
---

# Delphi Method

## Overview
The Delphi Method, developed by RAND Corporation in the 1950s, is a structured forecasting technique that uses multiple rounds of anonymous expert surveys with controlled feedback. Unlike traditional meetings where loudest voices dominate, Delphi eliminates groupthink, anchoring, and status effects by keeping experts anonymous while sharing statistical summaries of group predictions between rounds.

## When to Use
- Forecasting complex uncertain futures where data is limited
- Gathering expert consensus without group meeting dynamics
- Reducing bias in collective predictions
- Long-term strategic planning (5+ years)
- Technology roadmapping
- Risk assessment requiring diverse expertise
- Scenarios where in-person meetings create groupthink

## The Process

### Step 1: Assemble Expert Panel
Select 10-30 domain experts with diverse perspectives. Larger panels (50+) dilute expertise. Smaller (<10) lack statistical power. Emphasize diversity to avoid correlated errors.

**Example:** Forecasting AI regulation: Include technologists, policymakers, ethicists, lawyers, economists—not just AI researchers.

### Step 2: Round 1 - Independent Anonymous Forecasts
Ask experts to provide numerical forecasts or qualitative predictions independently without seeing others' responses. Questions must be specific, measurable.

**Example:** "What year will fully autonomous vehicles (SAE Level 5) represent >10% of new car sales in the US?" Experts submit: 2030, 2035, 2028, Never, 2040, 2033, 2031, 2029...

### Step 3: Aggregate and Share Statistics (No Names)
Calculate median, quartiles, range. Share statistical summary with all experts anonymously. Experts see group distribution without knowing who predicted what.

**Example:** Round 1 results: Median 2031, Q1 2029, Q3 2035, Range 2028-Never. Share histogram showing distribution.

### Step 4: Round 2 - Revise with Rationale
Experts see Round 1 statistics and update forecasts. Those outside median range must provide rationale for outlier position. This surfaces reasoning without social pressure.

**Example:** Expert who predicted "Never" explains: "Liability frameworks unsolvable." Expert who predicted 2028 explains: "Technology already works, just needs regulation approval."

### Step 5: Iterate Until Convergence
Repeat 2-4 rounds. Typically convergence happens by Round 3-4. Stop when predictions stabilize or clear camps emerge (bimodal distribution = legitimate disagreement, not noise).

**Example:** Round 3 median 2032, Q1 2030, Q3 2034. Distribution tightened. Two outliers remain but provided reasoned arguments, so stop.

### Step 6: Report Final Forecast with Uncertainty
Present median forecast, uncertainty range (interquartile range), and qualitative synthesis of key assumptions and disagreements.

**Example:** "Expert consensus: Autonomous vehicles (L5) will reach >10% market share in 2032 (80% confidence interval: 2030-2034). Key uncertainty: regulatory approval timeline. Dissenting view: Liability unresolved, may never happen."

## Example Application

**Situation:** Medical research consortium forecasting when mRNA cancer vaccines will achieve FDA approval for common cancers.

**Application**:
- **Panel**: 25 oncologists, biotech researchers, regulatory experts, pharma executives
- **Round 1**: Predictions range from 2027 to 2045, median 2033
- **Feedback**: Share distribution. Outliers explain reasoning (early: "Phase 3 trials already show promise"; late: "Regulatory path unclear")
- **Round 2**: Median shifts to 2031 as experts incorporate insights about trial timelines
- **Round 3**: Convergence at median 2031, IQR 2029-2033
- **Final forecast**: "FDA approval for mRNA cancer vaccines likely 2031 ±2 years, conditional on positive Phase 3 results"

**Outcome:** Consortium aligns research funding roadmap to 2030 target, balancing early optimists with late skeptics.

## Anti-Patterns
- ❌ Revealing expert identities (reintroduces status/groupthink biases)
- ❌ Only one round (no benefit of updated information)
- ❌ Too many rounds (expert fatigue, diminishing returns after 3-4)
- ❌ Vague questions ("When will AI be important?") vs. specific measurable forecasts
- ❌ Homogeneous expert panel (correlated errors)
- ❌ Forcing consensus when legitimate disagreement exists (bimodal distribution)
- ❌ Treating median as certainty vs. acknowledging forecast uncertainty

## Related
- superforecasting
- thinking-in-bets
- base-rate-analysis
- crowd-wisdom
- prediction-markets
