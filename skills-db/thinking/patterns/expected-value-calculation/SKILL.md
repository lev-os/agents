---
name: expected-value-calculation
description: Calculate probability-weighted outcomes to make rational decisions under uncertainty by comparing expected values across options
---

# Expected Value Calculation

## Overview
Expected Value (EV) is the probability-weighted average of all possible outcomes for a decision. Rather than guessing or hoping, you multiply each outcome's value by its probability and sum the results. This transforms uncertain choices into comparable numbers: the decision with the highest expected value is mathematically optimal over many trials. EV thinking is fundamental to poker, investing, product decisions, and any situation involving risk and uncertainty.

## When to Use
- Choosing between options with different risk/reward profiles
- Evaluating investments, bets, or business opportunities
- Prioritizing features or projects with uncertain payoffs
- Deciding whether to pursue risky opportunities
- Comparing options where outcomes are probabilistic
- Making repeated decisions where long-run average matters more than single outcome

## The Process

### Step 1: List All Possible Outcomes for Each Option
Identify every distinct outcome that could result from the decision. Be comprehensive—include best case, worst case, and likely scenarios. Don't forget zero or negative outcomes.

**Example (feature development):** Outcomes: (1) Feature succeeds, drives 20% revenue increase. (2) Feature neutral, no impact. (3) Feature confuses users, 5% churn increase.

### Step 2: Estimate Probability for Each Outcome
Assign probability to each outcome (must sum to 100%). Use historical data when available, expert judgment when not. Be honest—wishful thinking breaks EV analysis.

**Example:** Success 20%, Neutral 60%, Negative 20% (based on past feature launches and market research).

### Step 3: Assign Dollar Value to Each Outcome
Quantify outcomes in consistent units (usually dollars, but could be users, time saved, etc.). Include costs. Negative outcomes have negative values.

**Example:** Success = +$500K annual revenue. Neutral = $0. Negative = -$100K (lost customers + support costs). Development cost = $80K.

### Step 4: Calculate Expected Value
Multiply each outcome's probability by its value, then sum all results. Formula: EV = Σ(Probability × Value). Subtract any upfront costs.

**Example:**
- EV = (0.20 × $500K) + (0.60 × $0) + (0.20 × -$100K) - $80K
- EV = $100K + $0 - $20K - $80K = $0

### Step 5: Compare EVs Across Options
Calculate EV for each alternative (including "do nothing"). Choose highest EV. If EVs are close, consider risk tolerance and second-order effects.

**Example:** Compare feature EV ($0) vs. investing $80K in customer success (EV = +$120K based on retention data). Customer success has higher EV, choose that.

### Step 6: Remember EV Is Long-Run Average
Single outcomes may differ wildly from EV. But making +EV decisions repeatedly produces positive results over time. Avoid results-oriented thinking after one trial.

**Example:** Even if feature succeeded, EV analysis was correct—you shouldn't make $0 EV bets just because one worked out. Process matters, not single outcomes.

## Classic Poker Example

**Situation:** You have $100 in pot, opponent bets $50. You have 4 cards to a flush (9 outs, ~20% to hit on river). Should you call?

**Application:**
1. **Outcomes:** Win pot ($150) or lose call ($50)
2. **Probabilities:** Hit flush 20%, miss 80%
3. **Values:** Win = +$150, lose = -$50
4. **Calculate:** EV = (0.20 × $150) + (0.80 × -$50) = $30 - $40 = -$10
5. **Decision:** -EV call. Fold is correct.

**But if pot was $300:** EV = (0.20 × $350) + (0.80 × -$50) = $70 - $40 = +$30. Now calling is +EV.

## Example Application

**Situation:** SaaS company deciding between three growth strategies: (A) Enterprise sales team, (B) Product-led growth, (C) Partnership channel.

**Application:**

**Option A (Enterprise Sales):**
- 30% chance: Close 5 enterprise deals = +$1M ARR
- 50% chance: Close 2 deals = +$300K ARR
- 20% chance: Zero traction = $0
- Cost: $400K (headcount + tools)
- EV = (0.30 × $1M) + (0.50 × $300K) + (0.20 × $0) - $400K = $50K

**Option B (PLG):**
- 40% chance: Viral adoption, 10K users, 2% convert = +$600K ARR
- 40% chance: Moderate adoption, 3K users = +$200K ARR
- 20% chance: Poor fit, minimal adoption = $0
- Cost: $200K (product development)
- EV = (0.40 × $600K) + (0.40 × $200K) + (0.20 × $0) - $200K = $120K

**Option C (Partnerships):**
- 20% chance: Major partner drives $800K ARR
- 30% chance: Medium partner drives $250K ARR
- 50% chance: Partnership delays, minimal revenue = $50K
- Cost: $150K (BD headcount)
- EV = (0.20 × $800K) + (0.30 × $250K) + (0.50 × $50K) - $150K = $80K

**Decision:** PLG has highest EV ($120K), choose that strategy.

## Investment Decision Example

**Situation:** Angel investor evaluating startup investment: $50K for 2% equity.

**Outcomes:**
- 10% chance: Startup becomes unicorn ($1B+ exit) → 2% = $20M return
- 20% chance: Solid exit ($100M) → 2% = $2M return
- 30% chance: Modest exit ($20M) → 2% = $400K return
- 40% chance: Failure → $0

**Calculate:**
EV = (0.10 × $20M) + (0.20 × $2M) + (0.30 × $400K) + (0.40 × $0) - $50K
EV = $2M + $400K + $120K + $0 - $50K = $2.47M

**Interpretation:** Massive +EV investment ($2.47M expected return on $50K). Even with 40% failure rate, math strongly favors investing.

## Anti-Patterns
- ❌ Confusing single-trial outcome with EV (one loss doesn't mean -EV decision was wrong)
- ❌ Using garbage probabilities (wishful thinking: "90% this succeeds!")
- ❌ Ignoring costs or negative outcomes (only calculating upside)
- ❌ Forgetting that real life isn't infinite trials (bankroll matters—avoid ruin)
- ❌ Paralysis by analysis (not every decision needs rigorous EV calculation)
- ❌ Treating EV as only factor (ignore risk tolerance, optionality, learning value)

## Related
- thinking-in-bets
- probabilistic-thinking
- base-rate-analysis
- monte-carlo-simulation
- kelly-criterion
- expected-monetary-value
- risk-vs-reward
