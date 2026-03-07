---
name: thinking-in-bets
description: Frame decisions as probability bets instead of certainties - separate decision quality from outcome quality to avoid resulting bias
---

# Thinking in Bets

## Overview

Annie Duke's "Thinking in Bets" framework, drawn from her World Series of Poker championship experience, reframes decision-making under uncertainty as probability bets rather than binary right/wrong judgments. The core insight: life is poker, not chess - you're playing with incomplete information where good decisions sometimes yield bad outcomes and vice versa. The framework combats "resulting" (judging decisions by outcomes instead of process), embraces probabilistic thinking through Bayesian updating, and calculates expected value to make rational choices even when individual results are unpredictable.

Duke's approach separates decision quality from outcome quality: a decision that had 70% odds of success but failed wasn't necessarily wrong - you'd make that same bet 100 times. This mindset shift transforms how you evaluate choices, learn from failure, and avoid hindsight bias.

## When to Use

- High-stakes decisions with uncertain outcomes (investments, hiring, strategic moves)
- Avoiding "resulting" - when people judge your decision by the outcome, not the process
- Building a learning culture that rewards good process over lucky results
- Evaluating whether to continue or abandon a strategy after setbacks
- Making decisions with incomplete information (which is most decisions)
- Calibrating confidence - distinguishing 60% sure from 90% sure matters

## The Process

### Step 1: Express Beliefs as Probability Bets

Instead of "This will work" or "This will fail," quantify your confidence as odds. Force yourself to put a number on uncertainty.

**From binary to probabilistic:**
- ❌ "We should hire this candidate - they're great"
- ✅ "I'm 70% confident this candidate succeeds in role based on interview performance, culture fit signals, and reference checks. I'd take that bet."

**Calibration practice:** Track predictions with explicit percentages. Did things you were "90% sure" about happen 90% of the time? If not, recalibrate.

### Step 2: Calculate Expected Value (EV)

Multiply each possible outcome by its probability and sum them. Choose the option with highest expected value, not the option that "feels safest" or has the best best-case scenario.

**EV Formula:** EV = (Probability of Win × Win Amount) - (Probability of Loss × Loss Amount)

**Example:** Startup decision - raise VC at $20M valuation (50% chance, but lose control) vs. bootstrap (30% chance of success, but keep 100% ownership):
- **VC path:** 50% × $5M (your exit share) = $2.5M EV
- **Bootstrap path:** 30% × $20M (full ownership) = $6M EV
Despite lower odds, bootstrap has higher EV if you care about dollars, not probability of any success.

### Step 3: Update Beliefs Bayesian-Style

Start with "prior" probability based on initial information. As new evidence emerges, update to "posterior" probability. Don't anchor on first belief or ignore contradictory evidence.

**Bayesian update example:**
- **Prior:** "70% chance this marketing channel works based on competitor benchmarks"
- **New evidence:** First 1,000 users show 2% conversion (benchmark was 5%)
- **Posterior:** "40% chance channel works at scale - evidence suggests lower performance than expected"

**Anti-resulting:** If outcome was bad but evidence was unavailable at decision time, don't retroactively judge the decision as wrong. Update beliefs for future, but don't penalize past process.

### Step 4: Separate Decision Quality from Outcome Quality

Build a 2x2 matrix: Good Decision/Bad Decision × Good Outcome/Bad Outcome. Good decisions can yield bad outcomes (bad luck). Bad decisions can yield good outcomes (good luck).

**Framework for evaluation:**
- **Good decision, bad outcome:** Learn from new information, don't regret decision
- **Bad decision, good outcome:** Don't repeat it - you got lucky
- **Good decision, good outcome:** Reinforce the process
- **Bad decision, bad outcome:** Learn from both poor process AND poor luck

**Key question:** "Knowing only what I knew then, with the probabilities I assigned, would I make this bet 100 times?"

## Example Application

**Situation:** Poker player (Duke) holding strong hand but loses to opponent's unlikely draw.

**Application:**
- **Decision:** Bet aggressively with 85% odds of winning
- **Outcome:** Lost pot to 15% outcome (opponent hit inside straight)
- **Resulting trap:** "I played it wrong" (judging by outcome)
- **Betting mindset:** "I'd make that exact play 100 times - the odds were correct, I just hit the 15% case this time"

**Outcome:** Duke maintained discipline on similar hands instead of changing strategy based on one unlucky result. Over 10,000 hands, the 85% strategy wins far more than alternatives.

## Example Application 2

**Situation:** Startup choosing between two product roadmap options after 6 months of user research.

**Application:**
- **Option A (AI feature):** 60% confidence in strong adoption, 40% risk of flopping. EV = +$2M ARR
- **Option B (integration):** 80% confidence in moderate adoption. EV = +$1.5M ARR
- **Decision:** Choose A despite lower probability - higher EV matters more
- **Outcome:** AI feature flopped (hit the 40% case)
- **Betting evaluation:** "Given the information we had, Option A was correct. Would make same choice again - but now we have new data to update our model of what users want."

**Result:** Team didn't blame decision-maker, instead incorporated learnings into updated probability model for future bets. Culture of "good process > lucky outcomes" strengthened.

## Anti-Patterns

- ❌ Resulting - judging decisions solely by outcomes instead of quality of process at decision time
- ❌ Treating 51% confidence same as 90% confidence (precision matters in betting)
- ❌ Never updating beliefs when new evidence emerges (Bayesian update required)
- ❌ Expecting 70% bets to win 100% of the time (probability means you'll lose 30% of cases)
- ❌ Punishing "good bet, bad outcome" - destroys learning culture and risk-taking
- ❌ Ignoring expected value, optimizing only for win probability or best-case scenario

## Related

- superforecasting (calibration and prediction accuracy techniques)
- bayesian-updating (formal probability updating framework)
- expected-value (core calculation method for decision quality)
- prospect-theory (explains why humans are bad at probabilistic thinking by default)
- second-order-thinking (thinking in bets reveals hidden consequences)
