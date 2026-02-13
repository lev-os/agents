---
name: Probability
description: Systematic approach to quantifying uncertainty and making better predictions by thinking in terms of likelihoods rather than certainties
---

# Probability

## Overview

Probability is a mental model that involves thinking about outcomes and decisions in terms of likelihoods rather than binary certainties. It's the foundation of rational decision-making under uncertainty, enabling practitioners to quantify risks, weigh options, and make predictions based on evidence rather than intuition.

Unlike the common tendency to think in absolutes ("this will definitely work" or "that's impossible"), probabilistic thinking recognizes that most outcomes exist on a spectrum. By assigning numerical probabilities to events, decision-makers can compare options systematically, update beliefs with new information, and avoid the overconfidence that comes from binary thinking.

This framework is particularly powerful because it:
- Forces explicit reasoning about uncertainty
- Enables quantitative comparison of options
- Provides a language for updating beliefs (Bayesian reasoning)
- Reveals hidden assumptions in predictions
- Improves calibration over time through feedback

Practitioners from poker players to venture capitalists to military strategists rely on probabilistic thinking to navigate uncertainty. The key is not achieving perfect accuracy but developing better calibration—learning to distinguish between 60% likely and 90% likely events.

**Key insight**: Good decisions can lead to bad outcomes, and bad decisions can lead to good outcomes. Probabilistic thinking separates decision quality from outcome quality.

## When to Use

Apply probabilistic thinking in these situations:

- **Strategic decisions**: Evaluating business opportunities, product launches, hiring decisions where outcomes are uncertain
- **Risk assessment**: Quantifying security threats, financial risks, project failure modes
- **Forecasting**: Making predictions about markets, technology adoption, competitive moves
- **Resource allocation**: Deciding where to invest time, money, or attention given uncertain returns
- **Negotiations**: Estimating BATNA probabilities, deal success likelihood, counterparty positions
- **Product development**: Weighing feature priorities, technical feasibility, market acceptance
- **Hiring**: Assessing candidate success probability given limited interview data
- **Investment decisions**: Evaluating expected returns across different scenarios

**Trigger question**: "What's the probability that X happens?" or "How confident am I in this prediction?"

## Process

### 1. Frame the Question Precisely

Define exactly what outcome you're trying to assess. Vague questions produce meaningless probabilities.

- Specify the timeframe ("within 6 months" not "eventually")
- Define success criteria objectively ("achieve 100K MRR" not "succeed")
- Identify mutually exclusive outcomes (if multiple possibilities exist)
- Clarify measurement method (how will you know if it happened?)

**Action**: Write down the specific question in the form "What is the probability that [specific outcome] occurs by [specific date/condition]?"

### 2. Gather Base Rate Information

Before making predictions, research how often similar events have occurred historically. Base rates provide an "outside view" anchor.

- Find comparable situations from history or industry
- Look for statistical data on similar outcomes
- Identify reference classes (what category does this belong to?)
- Note sample sizes (10 examples vs. 10,000 examples)

**Action**: Research at least 3 comparable situations and note their success/failure rates.

### 3. Make an Initial Estimate

Generate a first-pass probability based on base rates and general knowledge, before considering specific details.

- Use reference class forecasting (what happened in similar cases?)
- Express as a percentage (0-100%) or odds ratio (1:3 means 25%)
- Consider using ranges if uncertain (40-60% likely)
- Write down your reasoning explicitly

**Action**: Record your initial probability estimate and the 2-3 key factors driving it.

### 4. Adjust for Specific Information

Update your base rate estimate using information specific to this situation. Apply Bayesian reasoning: how should evidence shift your belief?

- Identify evidence that makes this case different from the reference class
- For each piece of evidence, ask: "Does this make success more or less likely, and by how much?"
- Avoid over-weighting vivid or recent information
- Update incrementally (don't jump from 20% to 90% without strong evidence)

**Action**: List 3-5 factors specific to this case and note whether each increases or decreases probability.

### 5. Consider Alternative Scenarios

Break down the probability space into mutually exclusive scenarios. This prevents overlooking possibilities and ensures probabilities sum to 100%.

- List 3-5 distinct ways the outcome could occur (or fail to occur)
- Estimate probability of each scenario independently
- Verify all scenarios sum to ~100%
- Identify which scenarios you're most uncertain about

**Action**: Create a scenario breakdown with probabilities that sum to 100%.

### 6. Test Your Calibration

Check whether your probability estimate is internally consistent and well-calibrated.

- Would you take a bet at these odds? (If you say 70%, would you bet $7 to win $10?)
- Compare to similar past predictions you've made
- Ask: "If I made 10 predictions at this probability level, how many should come true?"
- Identify the evidence that would move you to 90% or 10%

**Action**: Write down what evidence would make you change your estimate significantly.

### 7. Update Based on New Information

As new evidence emerges, systematically update your probabilities using Bayesian reasoning.

- When evidence confirms your prediction: increase probability (but not to 100%)
- When evidence contradicts your prediction: decrease probability (but not to 0%)
- Consider strength of evidence (strong evidence = larger update)
- Document why you updated and by how much

**Action**: Set triggers for when you'll revisit and update your probability estimate.

## Example

**Scenario**: Your startup is evaluating whether to pursue an enterprise customer that could become a $500K/year account.

**Probabilistic thinking in action**:

1. **Frame precisely**: "What's the probability we close this deal within 6 months, defined as signed contract with first payment?"

2. **Base rates**: Research shows:
   - Enterprise deals in our space close 20-30% of the time
   - Deals with warm intros (which we have) close at 35%
   - Deals with budgets confirmed (which this one lacks) close at 45%

3. **Initial estimate**: Starting point: 30% (we have warm intro but no confirmed budget)

4. **Specific adjustments**:
   - Champion has budget authority (+10%): 30% → 40%
   - They're evaluating 2 competitors (-5%): 40% → 35%
   - We're 6 months from their fiscal year end (-10%): 35% → 25%
   - They have existing legacy solution creating switching costs (-5%): 25% → 20%

5. **Alternative scenarios**:
   - Close in Q1 with full contract: 10%
   - Close in Q2 with pilot program: 10%
   - Verbal commitment but legal delays past 6 months: 15%
   - Lost to competitor: 30%
   - Lost to status quo (no decision): 35%

6. **Calibration test**: At 20%, this is a 1-in-5 shot. Would I spend $100K in sales effort for a 20% chance at $500K ARR? Yes, expected value is positive ($100K EV vs $100K cost). But I wouldn't spend $200K.

7. **Update triggers**: Will revisit estimate after:
   - Discovery call (better sense of pain level)
   - Budget confirmation
   - Proposal submission
   - Champion meeting with decision-maker

**Decision**: Pursue the deal but keep customer acquisition cost under $150K given 20% probability. Run 5 similar deals in parallel to hit revenue targets.

## Anti-Patterns

**False precision**: Claiming 73.4% probability when you have limited information. Use round numbers (20%, 30%, 50%) unless you have statistical models. Spurious precision masks uncertainty.

**Ignoring base rates**: Jumping straight to your specific case without researching historical success rates. Most predictions should start with "what usually happens" before adjusting for specifics.

**Probability neglect**: Making yes/no decisions instead of weighing probabilities. Saying "I think it'll work" rather than "I estimate 60% chance of success" prevents rational comparison of options.

**Extreme probabilities without justification**: Assigning 95%+ or 5%- probabilities to uncertain events. Research shows experts are overconfident. Reserve extreme probabilities for near-certainties backed by strong evidence.

**Updating too much on single data points**: Shifting from 30% to 80% based on one customer conversation or one data point. Update incrementally unless evidence is overwhelming.

**Confusing outcome with decision quality**: Judging the decision by whether it worked rather than whether it was rational given available information. A 70% probability means it fails 30% of the time—that doesn't make it a bad decision.

**Anchoring on initial estimates**: Failing to update probabilities as new information arrives. Treat estimates as living documents that change with evidence.

## Related Frameworks

- **Expected Value**: Probability × Outcome = Expected value. Essential for comparing options with different risk/reward profiles.
- **Bayesian Reasoning**: Formal method for updating probabilities based on new evidence. P(H|E) = P(E|H) × P(H) / P(E).
- **Base Rate Neglect**: Common error of ignoring statistical base rates in favor of specific information.
- **Power Laws**: Some domains follow power law distributions rather than normal distributions, changing probability calculations.
- **Fat Tails**: Extreme events are more probable than normal distributions suggest, requiring different probability models.
- **Monte Carlo Simulation**: Computational method for estimating probabilities when analytical solutions are difficult.
- **Calibration Training**: Systematic practice to improve probability estimate accuracy over time.
- **Superforecasting**: Methodology developed by Philip Tetlock for making highly accurate probabilistic predictions.
