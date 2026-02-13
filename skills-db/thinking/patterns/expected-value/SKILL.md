---
name: Expected Value
description: Probability-weighted average of all possible outcomes used to compare uncertain options and make optimal decisions under risk
---

# Expected Value

## Overview

Expected Value (EV) is a mathematical framework for making rational decisions under uncertainty by calculating the probability-weighted average of all possible outcomes. It's the fundamental tool for comparing options when you can't predict exact results but can estimate probabilities and payoffs.

The formula is simple: EV = Σ(Probability × Outcome). For each possible scenario, multiply its probability by its value, then sum across all scenarios. A decision with positive expected value (+EV) is profitable in the long run, even if individual outcomes vary.

Expected value thinking originated in probability theory and gambling but has become essential across domains from poker to venture capital to product development. It separates short-term luck from long-term strategy by focusing on the quality of decisions rather than individual outcomes.

The power of EV thinking lies in shifting mental models from "will this work?" to "what's this worth given all possible scenarios?" This reframes decisions from binary predictions into portfolio management, where you make many +EV bets knowing some will fail but the aggregate will profit.

Professional poker players, options traders, insurance companies, and successful VCs all think primarily in expected value. They accept short-term variance because they know that repeatedly making +EV decisions compounds into long-term success.

**Key insight**: You should take +EV opportunities even when the most likely outcome is failure, and reject -EV opportunities even when success is possible. What matters is the probability-weighted average, not the modal outcome.

## When to Use

Apply expected value thinking in these situations:

- **Investment decisions**: Comparing opportunities with different risk/reward profiles
- **Product prioritization**: Weighing features with uncertain value and effort
- **Venture capital**: Evaluating startups where most fail but winners pay for losses
- **Poker and gambling**: Making betting decisions with known odds and payoffs
- **Business development**: Assessing partnership opportunities with probabilistic outcomes
- **Resource allocation**: Deciding where to invest time/money given uncertain returns
- **Hiring**: Comparing candidates with different probability distributions of success
- **Marketing spend**: Evaluating channels with different conversion rates and CAC
- **R&D investment**: Funding projects with low success probability but high potential payoff

**Trigger question**: "What's the expected value of this decision?" or "Which option has higher EV given the probabilities?"

## Process

### 1. Define Possible Outcomes

List all meaningfully different scenarios that could result from the decision. Be exhaustive but combine similar outcomes.

- Identify distinct success/failure modes
- Include the null outcome (status quo if you do nothing)
- Combine scenarios that have similar values
- Ensure outcomes are mutually exclusive and exhaustive

**Action**: Create a table with columns for Scenario, Probability, and Value.

### 2. Estimate Probabilities

Assign a probability to each scenario, ensuring they sum to 100%.

- Use base rates as starting points
- Apply probabilistic reasoning to adjust for specifics
- Consider using ranges if uncertain (best/worst case)
- Verify all probabilities sum to ~100%

**Action**: Fill in probability column using best available data and reasoning.

### 3. Quantify Outcomes

Assign a numeric value to each scenario. Use consistent units (dollars, utility points, time saved).

- Express gains as positive numbers, losses as negative
- Include all costs (opportunity costs, time investment, capital)
- Consider both financial and non-financial value
- Use realistic estimates, not best-case fantasies

**Action**: Fill in value column for each scenario in consistent units.

### 4. Calculate Expected Value

For each scenario, multiply Probability × Value. Sum across all scenarios to get total EV.

Formula: EV = (P₁ × V₁) + (P₂ × V₂) + ... + (Pₙ × Vₙ)

- Use a spreadsheet for complex calculations
- Show your work (document formula and inputs)
- Round to appropriate precision
- Sanity-check the result

**Action**: Calculate and document EV with formula showing work.

### 5. Compare to Alternatives

Calculate EV for each option you're considering, including the "do nothing" baseline.

- Rank options by EV
- Note the difference in EV between options
- Consider whether EV difference exceeds margin of error
- Identify sensitivity to key assumptions

**Action**: Create ranked list of options by EV with confidence levels.

### 6. Assess Risk Tolerance

EV assumes risk neutrality. Adjust if you can't afford to take the EV-optimal bet repeatedly.

Risk-adjusted considerations:
- Kelly Criterion: For betting, optimal stake is (edge/odds) of bankroll
- Ruin risk: Don't take bets that could bankrupt you even if +EV
- Liquidity: Account for when capital is returned, not just expected amount
- Variance: High-variance +EV may not be worth psychological cost

**Action**: Note if risk considerations should override pure EV optimization.

### 7. Set Decision Rule and Act

Establish your decision threshold and execute.

Common rules:
- "Take any +EV opportunity above $X threshold"
- "Choose highest EV option if difference exceeds Y%"
- "Require Z:1 EV ratio for high-risk bets"
- "Portfolio approach: take top N options by EV"

**Action**: Document decision rule and implement the highest EV option(s).

## Example

**Scenario**: Your startup can pursue one of three product features. You have engineering capacity for only one this quarter.

**Expected value in action**:

**Option A: Enterprise SSO integration**
- 60% chance: 5 enterprise customers sign ($500K ARR) = 0.60 × $500K = $300K
- 30% chance: 2 enterprise customers sign ($200K ARR) = 0.30 × $200K = $60K
- 10% chance: 0 customers (no enterprise demand) = 0.10 × $0 = $0
- **EV = $360K**
- Cost: $80K engineering time
- **Net EV = $280K**

**Option B: AI-powered recommendation engine**
- 20% chance: Viral growth, 10X user engagement ($2M ARR) = 0.20 × $2M = $400K
- 50% chance: Moderate improvement ($400K ARR) = 0.50 × $400K = $200K
- 30% chance: Users don't engage ($0 ARR) = 0.30 × $0 = $0
- **EV = $600K**
- Cost: $120K engineering time
- **Net EV = $480K**

**Option C: Mobile app (currently web-only)**
- 70% chance: Incremental growth ($300K ARR) = 0.70 × $300K = $210K
- 20% chance: Significant mobile user adoption ($600K ARR) = 0.20 × $600K = $120K
- 10% chance: No meaningful adoption ($50K ARR) = 0.10 × $50K = $5K
- **EV = $335K**
- Cost: $100K engineering time
- **Net EV = $235K**

**Comparison**:
1. Option B (AI recommendations): **+$480K EV**
2. Option A (Enterprise SSO): +$280K EV
3. Option C (Mobile app): +$235K EV

**Risk assessment**:
- Option B has highest variance but we can afford a $0 outcome
- We have 12 months of runway, so we can take high-variance +EV bets
- If we were at 3 months runway, might choose Option A (lower variance, more certain)

**Decision**: Build Option B (AI recommendations) based on highest expected value. Accept that there's a 30% chance it fails completely, but the weighted value makes it optimal.

**Long-term thinking**: Over 4 quarters, if we consistently choose highest EV options, we'll outperform choosing "safest" or "most likely to succeed" options. Some will fail, but the portfolio will win.

## Anti-Patterns

**Confusing EV with most likely outcome**: The highest probability scenario isn't necessarily the highest EV. A 5% chance of $1M can have higher EV than a 60% chance of $50K.

**Ignoring low-probability, high-impact scenarios**: Fat tail events matter enormously in EV calculations. Don't round small probabilities to zero if the payoff is large.

**Using EV for single, irreversible decisions**: EV reasoning assumes you can make the same decision repeatedly. If you can't afford to lose even once (Russian roulette at any price), pure EV is insufficient.

**Fabricating precise probabilities**: False precision (37.4% probability × $127,483 value) when you're actually guessing. Use round numbers and ranges when uncertainty is high.

**Cherry-picking scenarios**: Only including optimistic scenarios or ignoring downside cases. EV requires honest accounting of all possible outcomes.

**Treating sunk costs as relevant**: Including money/time already spent in EV calculations. Only future costs and benefits matter.

**Paralysis from uncertainty**: Waiting for perfect information before calculating EV. Use best available estimates and update as you learn.

**Optimizing for EV while ignoring ruin risk**: Taking +EV bets that could bankrupt you. Kelly Criterion and risk management matter.

## Related Frameworks

- **Probability Thinking**: Foundation for estimating likelihoods in EV calculations.
- **Kelly Criterion**: Formula for optimal bet sizing based on EV and variance—prevents ruin even with +EV bets.
- **Monte Carlo Simulation**: Computational method for estimating EV when analytical calculation is complex.
- **Decision Trees**: Visual tool for mapping scenarios and calculating EV in multi-stage decisions.
- **Real Options Theory**: Applying EV thinking to strategic decisions with future decision points.
- **Portfolio Theory**: Diversification to capture EV across multiple uncorrelated bets.
- **Utility Functions**: Adjusting EV for risk preferences (risk-averse, risk-seeking, risk-neutral).
- **Bayesian Decision Theory**: Formal framework for optimal decisions under uncertainty using EV.
- **Opportunity Cost**: The EV of the next-best alternative you're forgoing.
- **Positive Sum vs. Zero Sum**: EV calculation differs based on whether value is created or redistributed.
