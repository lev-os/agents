---
name: Expected Monetary Value
description: Probability-weighted average of all possible outcomes, calculated by multiplying each outcome's value by its likelihood to guide risk-based decisions
---

# Expected Monetary Value (EMV)

**Canonical Source**: Decision Analysis / PMBOK Guide (PMI)
**Domain**: Project Management, Risk Analysis, Decision Theory
**Standard**: PMI PMBOK Guide - Quantitative Risk Analysis

## One-Line Summary

Probability-weighted average of all possible outcomes, calculated by multiplying each outcome's value by its likelihood and summing the results to guide risk-based decision-making.

## Core Concept

EMV answers: "If I face this decision repeatedly, what's my average gain or loss per trial?" It converts uncertain scenarios into a single expected value, enabling rational comparison between alternatives.

**The Formula**: EMV = Σ(Probability × Impact)

For a single outcome: EMV = P × I
- P = Probability of occurrence (0-1 or 0-100%)
- I = Financial impact (positive for opportunities, negative for threats)

**The Innovation**: EMV transforms subjective uncertainty into quantified decision criteria. Instead of debating "should we?" it answers "what's the math?"

## When to Use

**Ideal Scenarios**:
- Project risk analysis with quantifiable financial impacts
- Go/no-go investment decisions under uncertainty
- Evaluating risk response strategies (mitigate vs. accept vs. transfer)
- Comparing multiple projects with different risk profiles
- Determining optimal bid pricing with win probability estimates
- Resource allocation across uncertain opportunities

**Not Suitable For**:
- One-time, existential bets (EMV assumes repeatability)
- Decisions with non-monetary values (reputation, lives, ethics)
- When probabilities are purely guesswork (garbage in = garbage out)
- Highly correlated risks (EMV assumes independence)
- When risk aversion matters more than expected value

## Execution Steps

### 1. Identify All Possible Outcomes
- List every distinct scenario that could occur
- Include both positive outcomes (opportunities) and negative (threats)
- Be exhaustive—missing outcomes invalidate the analysis
- For complex decisions, use a decision tree to map branches

*Output*: Complete list of mutually exclusive outcomes

### 2. Assign Probabilities
- Estimate likelihood of each outcome (must sum to 100%)
- Use historical data, expert judgment, or statistical models
- Document assumptions (especially for subjective estimates)
- Validate: Do probabilities reflect reality or wishful thinking?

*Output*: Probability distribution across all outcomes

### 3. Quantify Financial Impact
- Determine monetary value for each outcome
- Positive values for gains (revenue, cost savings)
- Negative values for losses (costs, penalties, rework)
- Use consistent units (all in USD, EUR, etc.)
- Include ALL financial effects (direct + indirect)

*Output*: Impact values for each outcome

### 4. Calculate EMV for Each Outcome
- Multiply probability × impact for each scenario
- Example: 30% chance of $100K profit → EMV = 0.30 × $100K = $30K
- Example: 10% chance of $50K cost → EMV = 0.10 × (-$50K) = -$5K
- Keep signs correct (positive = gain, negative = loss)

*Output*: Individual EMV per outcome

### 5. Sum to Total EMV
- Add all individual EMVs (respecting positive/negative signs)
- Total EMV = Σ(P₁×I₁ + P₂×I₂ + ... + Pₙ×Iₙ)
- Positive EMV suggests favorable decision
- Negative EMV suggests unfavorable decision

*Output*: Single EMV figure for the decision

### 6. Compare Alternatives
- Calculate EMV for each option (including "do nothing")
- Rank by highest EMV
- Consider risk tolerance (high EMV with high variance vs. low EMV with certainty)
- Perform sensitivity analysis on key assumptions

*Output*: EMV comparison table, recommended option

### 7. Document and Communicate
- Show decision tree or calculation table
- Explain assumptions behind probabilities and impacts
- Highlight sensitivity to key variables
- Recommend decision with rationale

*Output*: Decision memo with EMV justification

## Common Pitfalls

**"EMV is Gospel" Fallacy**
EMV is a mathematical average, not a prediction of what WILL happen. You could face the worst-case scenario even if EMV is positive.

**Solution**: Pair EMV with risk tolerance analysis. Know your "ruin threshold" (loss you cannot survive).

**Probability Estimation Bias**
People overestimate rare events (plane crashes) and underestimate common ones (project delays). Subjective probabilities are notoriously unreliable.

**Solution**: Use reference class forecasting, historical data, or calibrated expert judgment (Tetlock's Superforecasting).

**Ignoring Correlations**
Calculating EMVs independently when risks are correlated (e.g., market crash affects all projects simultaneously).

**Solution**: Use Monte Carlo simulation for correlated variables, or adjust probabilities for joint scenarios.

**Overlooking Risk Aversion**
EMV assumes risk neutrality. In reality, losing $1M hurts more than gaining $1M feels good.

**Solution**: Apply utility theory (risk-adjusted EMV) or set EMV thresholds based on organizational risk appetite.

## Key Insights

**PMP Exam Essential**: EMV is heavily tested on PMP certification. Common question format: "Given these probabilities and impacts, what's the EMV?" or "Which project has the highest EMV?"

**Decision Trees = Visual EMV**: Decision trees represent EMV calculations graphically. Each branch shows probabilities, each end node shows impact, and EMV flows backward from outcomes to decision nodes.

**EMV ≠ Most Likely Outcome**: A project with 90% chance of $10K profit and 10% chance of $200K loss has positive EMV (+$9K - $20K = -$11K)—yet the most likely outcome is a $10K profit. EMV captures expected value over many trials.

**Opportunity vs. Threat**: EMV handles both. Positive impacts = opportunities to pursue; negative impacts = threats to mitigate. Combined EMV shows net expected position.

## Real-World Application

**Project Bidding**: A contractor estimates 60% chance of winning a $500K profit bid, vs. 40% chance of losing $100K (preparation costs). EMV = (0.6 × $500K) + (0.4 × -$100K) = $300K - $40K = $260K → Bid is favorable.

**Risk Response Strategy**: A project faces a 20% risk of $150K overrun. Mitigation costs $25K upfront but reduces risk to 5%. Option A (accept risk): EMV = -0.20 × $150K = -$30K. Option B (mitigate): EMV = -$25K + (-0.05 × $150K) = -$25K - $7.5K = -$32.5K → Accept risk is optimal.

**Product Launch Decision**: Three scenarios: Best case (30%, +$2M), Base case (50%, +$500K), Worst case (20%, -$300K). EMV = (0.30 × $2M) + (0.50 × $500K) + (0.20 × -$300K) = $600K + $250K - $60K = $790K → Launch decision supported.

## Related Frameworks

- **Decision Tree Analysis**: Visual representation of EMV calculations across sequential decisions
- **Monte Carlo Simulation**: Advanced EMV calculation with probability distributions (not point estimates)
- **Expected Utility Theory**: Risk-adjusted EMV accounting for diminishing marginal utility
- **Value at Risk (VaR)**: Focuses on downside tail risk rather than expected average
- **Real Options Analysis**: EMV applied to valuing strategic flexibility (option to delay/expand)
- **Sensitivity Analysis**: Tests how EMV changes with varying probabilities/impacts

## Anti-Patterns

**False Precision**
Reporting EMV to the nearest dollar when probabilities are educated guesses.

**Ignoring the Variance**
Choosing a project with EMV of $100K ± $1M over one with EMV of $90K ± $10K without considering volatility.

**One-and-Done Analysis**
Calculating EMV once at project start and never updating as new information emerges.

**Overcomplicating Simple Decisions**
Spending 10 hours on EMV analysis for a $500 decision. Use heuristics for low-stakes choices.

## Score Justification

**Framework Assessment**: 40/50 (Tier 1 - Canonical)

- **Practitioner Weight (8/10)**: Standard practice in project management (PMBOK), finance, and strategy consulting. Used daily by PMs worldwide. Slight deduction: Often formulaic in practice rather than deeply understood.
- **Clarity & Executability (9/10)**: Dead simple formula (P × I). Anyone with basic math can calculate EMV. Crystal clear steps.
- **Proven ROI (7/10)**: Prevents irrational risk-taking and enables data-driven decisions. However, limited evidence of EMV directly causing superior outcomes (correlation ≠ causation).
- **Novelty (6/10)**: Straightforward application of probability theory. Not particularly counter-intuitive, though the "average over many trials" framing trips up beginners.
- **Cross-Domain Applicability (10/10)**: Universally applicable: project management, venture capital, product development, procurement, R&D portfolio optimization, disaster planning.

**Notable**: PMBOK certification ensures millions of project managers know EMV. It's the foundation for more advanced frameworks like Real Options and Monte Carlo simulation.
