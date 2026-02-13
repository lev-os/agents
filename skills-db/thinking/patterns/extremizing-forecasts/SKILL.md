---
name: extremizing-forecasts
description: Adjust aggregated probability forecasts upward when diverse forecasters converge, compensating for crowd conservatism
---

# Extremizing Forecasts

## Overview

Extremizing is a statistical technique from Philip Tetlock's superforecasting research that compensates for the conservatism bias in aggregated probability forecasts. When multiple independent forecasters converge on similar probabilities, their collective wisdom is typically underconfident - if everyone says 66%, the real probability is likely higher. Extremizing pushes aggregate forecasts away from 50% toward the extremes (0% or 100%) based on forecaster diversity and agreement levels.

Developed through the Good Judgment Project (2011-2015), extremizing uses a log-odds algorithm to systematically adjust crowd predictions. The technique doesn't apply equally to all forecasts - it's most powerful when applied to diverse crowds with information asymmetry, and least necessary for expert "superforecaster" teams who already share common knowledge.

## When to Use

- **Aggregating mass forecasts**: Combining predictions from large, diverse crowd (100+ forecasters)
- **Tournament competitions**: When you need maximum accuracy from pooled predictions
- **Forecaster diversity exists**: Groups with varied backgrounds, information access, methods
- **Convergence observed**: Independent forecasters arriving at similar probabilities
- **Not for superforecasters**: Skip extremizing when elite forecasters already collaborate

## The Process

### Step 1: Collect Independent Forecasts

Gather probability estimates from multiple forecasters on the same question. Ensure independence - forecasters shouldn't coordinate before submitting.

**Example question**: "Will Company X's stock price exceed $150 by Dec 31?"

**Raw forecasts from 50 forecasters**:
- 20 forecasters: 65%
- 15 forecasters: 70%
- 10 forecasters: 60%
- 5 forecasters: 75%

**Average**: 67%

### Step 2: Calculate Simple Aggregate

Compute the baseline aggregate using mean, median, or weighted average (weight by past accuracy).

**Weighted by Brier score performance**:
- Top performers (5 forecasters at 75%): 2x weight
- Average performers: 1x weight
- Result: 68% weighted average

### Step 3: Assess Forecaster Diversity

Evaluate information diversity using two signals:
- **Spread of estimates**: Wide spread (40%-90%) = high diversity, narrow spread (65%-70%) = low diversity
- **Knowledge overlap**: Do forecasters share common sources/methods?

**Diversity score**:
- High diversity (independent info sources) = extremize more aggressively
- Low diversity (everyone reads same news) = minimal extremizing
- Zero diversity (clones/teammates) = no extremizing

### Step 4: Apply Extremizing Algorithm

Use log-odds transformation to push forecast away from 50%:

**Log-odds formula**:
1. Convert probability to odds: p/(1-p)
2. Take logarithm: log(odds)
3. Multiply by extremizing factor (typically 1.2-1.5)
4. Convert back to probability

**Example with 68% aggregate, extremizing factor 1.3**:
- Odds: 68/32 = 2.125
- Log-odds: log(2.125) = 0.754
- Extremized log-odds: 0.754 × 1.3 = 0.980
- Extremized odds: exp(0.980) = 2.664
- Extremized probability: 2.664/(1 + 2.664) = **73%**

**Result**: Original 68% becomes 73% after extremizing.

### Step 5: Calibrate Extremizing Strength

Adjust extremizing factor based on:
- **Agreement level**: High convergence (narrow range) = stronger extremizing
- **Track record**: If past extremizing improved accuracy, increase factor
- **Question type**: Binary outcomes vs. continuous values
- **Time horizon**: Near-term vs. long-term forecasts

**Good Judgment Project findings**:
- Regular teams: extremizing factor 1.2-1.5 optimal
- Superforecaster teams: extremizing factor ~1.0 (no adjustment needed)
- Mass crowds: extremizing can boost accuracy by 10-20%

### Step 6: Validate Against Outcomes

Track extremized forecasts vs. raw aggregates using Brier scores (lower is better).

**Brier score formula**: Average of (forecast - outcome)²

**Example results**:
- Raw aggregate (68%): Brier = 0.18
- Extremized (73%): Brier = 0.14 (20% improvement)

## Common Pitfalls

**Over-extremizing superforecasters** - Elite teams with shared knowledge don't benefit from extremizing. They're already at optimal confidence levels.

**Extremizing small samples** - Need 20+ forecasters for statistical validity. With 5 forecasters, extremizing adds noise.

**Ignoring herding** - If forecasters see each other's predictions, they're not independent. Extremizing amplifies groupthink.

**Fixed extremizing factor** - Optimal factor varies by question type, forecaster pool, time horizon. Test and calibrate.

**Extremizing outliers** - Remove statistical outliers (>3 standard deviations) before extremizing, or they'll distort the adjustment.

## Real-World Applications

**Good Judgment Project (2011-2015)**: Extremizing regular forecaster teams boosted them past some superforecaster teams in IARPA tournament accuracy rankings.

**Prediction markets alternative**: Tetlock's team showed extremized prediction polls outperformed prediction markets when using temporal decay, differential weighting, and recalibration.

**Intelligence community**: IARPA adopted extremizing for aggregating analyst forecasts on geopolitical events.

**Financial markets**: Hedge funds apply extremizing to analyst consensus estimates when dispersion is low but conviction is high.

## Key Insights

Extremizing works because crowds are systematically underconfident. When diverse forecasters independently arrive at 70%, they're hedging uncertainty by staying closer to 50%. But their convergence is itself a signal - if people with different information reach similar conclusions, truth is likely more extreme.

The technique only applies when forecasters have information asymmetry. A team with zero diversity (clones who know everything each other knows) should never be extremized - they're already optimally calibrated. Superforecaster teams approach this ideal, which is why extremizing doesn't help them much.

**When extremizing works best**: Apply to mass forecasts from diverse crowds. Extremizing brings regular crowds almost to parity with superforecaster accuracy in many cases.

**When to skip extremizing**: Superforecaster teams, small samples, herding/coordination, purely random forecasts.
