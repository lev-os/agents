---
name: dominant-strategy-analysis
description: Identify strategies that outperform alternatives regardless of competitor actions - simplify decisions by finding moves that win in all scenarios
---

# Dominant Strategy Analysis

## Overview

A dominant strategy is one that yields the best outcome for a player regardless of what opponents do. When you have a dominant strategy, decision-making simplifies dramatically: you don't need to predict competitor behavior or calculate complex equilibria - just execute the dominant strategy. Conversely, identifying opponents' dominant strategies reveals predictable behavior you can exploit or prepare for.

Dominant strategies are rare in complex real-world competition, but recognizing when they exist (or nearly exist) provides decisive clarity. The framework also helps through elimination: removing dominated strategies (those always worse than alternatives) narrows the strategic space to viable options worth analyzing.

## When to Use

- Strategic planning: before investing in competitive analysis, check if dominant strategy exists
- Game theory modeling: simplify complex competitive scenarios
- Negotiation: identify what the other party will rationally do regardless of your moves
- Risk assessment: find strategies that perform acceptably across all scenarios
- Decision paralysis: cut through uncertainty when one option dominates others
- Competitive response planning: predict competitor moves when they have dominant strategies

## The Process

### Step 1: Map Your Available Strategies

Enumerate all realistic strategic options available to you. Be comprehensive but practical - include major directional choices, not every tactical variation.

**Strategy enumeration:**
- Market positioning options (premium, mid-market, budget)
- Investment levels (aggressive growth, moderate, conservative)
- Competitive postures (attack, defend, differentiate, exit)
- Timing choices (first mover, fast follower, wait and see)

### Step 2: Identify Possible Competitor Actions

List the key strategies competitors might employ. Focus on major moves that significantly affect your payoffs.

**Competitor strategy space:**
- Likely actions based on their stated strategy
- Capabilities they could deploy
- Historical patterns of behavior
- Rational responses to your potential moves

### Step 3: Build Payoff Matrix and Compare Strategies

For each combination of your strategy and competitor action, estimate your payoff. Then compare: does any of your strategies beat all alternatives in every scenario?

**Payoff comparison example:**

|                     | Competitor Aggressive | Competitor Passive |
|---------------------|----------------------|-------------------|
| **You: Invest**     | $5M profit           | $15M profit       |
| **You: Hold**       | $3M profit           | $8M profit        |
| **You: Divest**     | $2M profit           | $4M profit        |

**Analysis:** "Invest" beats "Hold" and "Divest" in both scenarios (5>3>2, 15>8>4). **Invest is dominant.**

### Step 4: Eliminate Dominated Strategies

Even when no dominant strategy exists, removing dominated strategies simplifies analysis. A strategy is dominated if another strategy is always at least as good and sometimes better.

**Iterated elimination:**
1. Remove clearly dominated strategies from your set
2. Assume rational opponents eliminate their dominated strategies
3. Re-analyze with reduced strategy space
4. Repeat until no more strategies can be eliminated

**Result:** Remaining strategies are the only rational options worth detailed analysis.

### Step 5: Determine Strategic Implications

If you have a dominant strategy, execute it. If opponent has one, plan for it. If neither exists, deeper game-theoretic analysis is needed.

**Strategic conclusions:**
- **You have dominant strategy:** Execute without hesitation. Competitor behavior irrelevant to your choice.
- **Opponent has dominant strategy:** They will play it. Plan your response to that specific action.
- **No dominant strategies:** Requires Nash Equilibrium analysis or alternative decision frameworks.
- **Weak dominance exists:** Strategy ties in some scenarios but wins in others - often worth pursuing.

## Example Application

**Situation:** SaaS company deciding between building enterprise features or improving SMB product.

**Application:**
- **Your strategies:** Focus Enterprise, Focus SMB, Split Resources
- **Competitor strategies:** Target Enterprise, Target SMB
- **Payoff analysis:**

|                      | Competitor: Enterprise | Competitor: SMB |
|----------------------|----------------------|-----------------|
| **You: Enterprise**  | $8M (split market)   | $12M (SMB alone)|
| **You: SMB**         | $15M (SMB alone)     | $7M (split)     |
| **You: Split**       | $6M                  | $6M             |

**Finding:** No dominant strategy exists. When competitor targets Enterprise, you prefer SMB ($15M). When they target SMB, you prefer Enterprise ($12M). Need game theory to find equilibrium.

**Insight:** But "Split" is dominated - always worse than focusing. Eliminate it. Then analyze 2x2 game.

## Example Application 2

**Situation:** E-commerce company deciding on return policy while competitors vary their policies.

**Application:**
- **Your strategies:** 30-day returns, 90-day returns, No returns
- **Customer response modeling shows:** 90-day returns generates more revenue regardless of competitor policy due to consumer trust
- **Cost analysis confirms:** Even with higher return rates, net profit higher with 90-day

**Finding:** 90-day returns is dominant - wins in all competitive scenarios.

**Outcome:** Implement 90-day policy immediately. No need to monitor competitor return policies for this decision.

## Anti-Patterns

- Assuming dominance without checking all scenarios (confirmation bias)
- Ignoring weakly dominated strategies that might be "good enough"
- Over-simplifying opponent strategy space (missing key alternatives)
- Confusing "best response" with dominant strategy (best response depends on opponent; dominance doesn't)
- Paralysis when no dominant strategy exists (move to equilibrium analysis instead)
- Ignoring dynamic changes (today's dominant strategy may not be tomorrow's)

## Related

- nash-equilibrium (when dominant strategy doesn't exist, equilibrium analysis needed)
- game-theory (broader framework for strategic interaction)
- prisoners-dilemma (classic example where dominant strategy leads to bad equilibrium)
- decision-matrix (structured payoff comparison approach)
- scenario-planning (evaluating strategies across multiple futures)
