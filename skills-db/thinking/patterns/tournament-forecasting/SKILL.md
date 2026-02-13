---
name: tournament-forecasting
description: Structure competitive prediction events with scoring, time limits, and teams to systematically improve forecast accuracy through accountability
---

# Tournament Forecasting

## Overview

Tournament forecasting is a structured competitive framework for making and evaluating probabilistic predictions about future events. Unlike informal predictions, tournaments impose rigorous constraints: specific questions with verifiable outcomes, defined time horizons, quantitative probability estimates, standardized scoring (typically Brier scores), and public accountability. Participants compete individually or in teams, creating incentives for accuracy through rankings, prizes, or reputational stakes.

The gold standard example is the Good Judgment Project (GJP, 2011-2015), which won the IARPA-ACE tournament by outperforming competitors by 35-72% through systematic improvements: cognitive debiasing training, team collaboration, "superforecaster" selection, and advanced aggregation algorithms. Tournament structure transforms forecasting from casual speculation into a disciplined practice with measurable skill development.

## When to Use

- **Policy decisions**: Government agencies need probabilistic estimates on geopolitical events, economic trends, security threats
- **Business strategy**: Companies forecasting market shifts, competitive moves, technology adoption
- **Research evaluation**: Testing which forecasting methods, training, or aggregation techniques work best
- **Skill development**: Organizations building forecasting capability through practice and feedback
- **Accountability enforcement**: Creating skin-in-the-game incentives for analysts to calibrate confidence

## The Process

### Step 1: Design Question Set

Create clear, falsifiable questions with specific resolution criteria and deadlines.

**Good question characteristics**:
- **Unambiguous outcome**: "Will Company X's revenue exceed $1B in 2026?" (yes/no or continuous)
- **Verifiable resolution**: Public data source specified (SEC filing, WHO announcement, etc.)
- **Meaningful time horizon**: More than 1 month, less than 2 years (sweet spot for skill differentiation)
- **Neither trivial nor impossible**: Avoid 5% or 95% base rate questions
- **Relevant to decision-makers**: Actual strategic value, not trivia

**Example questions from Good Judgment Open**:
- "Will North Korea conduct a nuclear test before July 1, 2026?"
- "Will Bitcoin price exceed $100,000 by December 31, 2025?"
- "Will global semiconductor sales surpass $600B in 2025?"

### Step 2: Select Scoring Metric

Choose quantitative accuracy measure to rank forecasters objectively.

**Brier Score (standard choice)**:
- Formula: Average of (forecast - outcome)²
- Range: 0 (perfect) to 1 (maximally wrong)
- Proper scoring rule (rewards honest probabilities)

**Example**:
- Forecast: 70% chance event occurs
- Outcome: Event happens (1)
- Brier score: (0.70 - 1)² = 0.09

**Alternative metrics**:
- **Log score**: Rewards extreme confidence when correct, harshly penalizes wrong extremes
- **Calibration**: Are X% forecasts correct X% of the time?
- **Discrimination**: Ability to separate events that happen from those that don't

### Step 3: Structure Competition Format

Define participation model, team structure, update frequency.

**Individual vs. teams**:
- **Individual**: Pure skill measurement, no coordination overhead
- **Teams**: Information sharing improves accuracy, tests collaboration methods
- **Hybrid**: GJP used both, creating "superforecaster teams" from top individual performers

**Update policy**:
- **Static**: One forecast per question (tests initial judgment)
- **Dynamic**: Continuous updates allowed (tests information integration)
- **GJP approach**: Forecasters could update anytime as new info emerged

**Team composition testing**:
- Regular teams vs. superforecaster teams
- Prediction markets vs. prediction polls
- Extremizing algorithms on crowd forecasts

### Step 4: Implement Training & Debiasing

Provide cognitive tools to improve forecaster accuracy.

**GJP training modules**:
- **Probabilistic thinking**: Convert verbal hedges to numbers (55% vs. 80%)
- **Base rate anchoring**: Start with outside view (historical frequency)
- **Update incrementally**: Bayesian updating on new evidence
- **Avoid overconfidence**: Fermi decomposition, scenario exploration
- **Team calibration**: Share reasoning, not just numbers

**Training impact**: GJP participants with 1-hour online training improved accuracy by ~10%.

### Step 5: Run Tournament & Track Performance

Launch competition, collect forecasts, provide leaderboards, maintain engagement.

**Operational elements**:
- **Question release cadence**: 10-20 active questions simultaneously
- **Resolution timing**: Close questions when outcome determined
- **Leaderboard updates**: Weekly or real-time rankings
- **Feedback loops**: Show Brier scores, calibration charts to participants
- **Retention mechanisms**: Recognition, prizes, intellectual challenge

**GJP scale**: 2,400+ participants, 261 questions over 2 seasons.

### Step 6: Aggregate & Extremize Forecasts

Combine individual forecasts into crowd predictions using statistical methods.

**Aggregation methods tested in GJP**:
- **Simple mean**: Baseline (surprisingly good)
- **Median**: Robust to outliers
- **Weighted by past performance**: 2x weight for top forecasters
- **Temporal decay**: Recent forecasts weighted more
- **Extremizing**: Push aggregate away from 50% when forecasters converge

**GJP result**: Extremized, weighted, temporally-decayed aggregation of regular forecasters beat prediction markets and outperformed some superforecaster teams.

### Step 7: Analyze Results & Extract Insights

Identify top performers, successful methods, systematic errors.

**GJP discoveries**:
- **Superforecasters exist**: Top 2% consistently outperform by 30%+
- **Teams amplify skill**: Superforecaster teams beat individuals
- **Training works**: Debiasing improves accuracy
- **Foxes beat hedgehogs**: Generalists who know "many things" outperform domain specialists with "one big idea"
- **Frequency matters**: Active forecasters (updating 10+ times) beat passive

## Common Pitfalls

**Vague questions** - "Will AI transform society?" Unfalsifiable. Need specific, measurable outcomes.

**Short time horizons** - Forecasts <1 month often driven by noise, not skill. Need enough time for information processing.

**No updates allowed** - Static forecasts miss the core skill: integrating new evidence over time.

**Ignoring base rates** - Forecasters jump to inside view without anchoring on historical frequency.

**Herding** - If forecasters see each other's predictions, they converge on consensus regardless of accuracy.

**Poor question mix** - All 50/50 coin-flip questions or all 95% obvious questions don't differentiate skill.

## Real-World Applications

**IARPA-ACE Tournament (2011-2015)**: Five research teams competed on 100-150 geopolitical questions yearly. GJP won both seasons, 35-72% more accurate than competitors.

**Good Judgment Open (2015-present)**: Public forecasting platform with 10,000+ forecasters making predictions on current events.

**Intelligence community**: IARPA adopted tournament methods for aggregating analyst forecasts, replacing vague verbal estimates ("likely", "probable") with quantified probabilities.

**Prediction markets comparison**: Penn researchers showed statistically-aggregated prediction polls (tournaments) beat prediction markets when using GJP techniques.

**Corporate strategic planning**: Companies run internal tournaments on product launches, competitor moves, market adoption.

## Key Insights

Tournament structure transforms forecasting from subjective art to measurable skill. Three critical elements drive accuracy improvement:

1. **Accountability**: Brier scores create objective performance measurement, exposing overconfidence and rewarding calibration.

2. **Competition**: Rankings and prizes incentivize intellectual rigor - participants invest time in research, model building, Bayesian updating.

3. **Feedback loops**: Seeing your Brier score, calibration curve, and rank against peers accelerates learning faster than isolated practice.

**Superforecasters aren't geniuses** - they're disciplined practitioners who (a) break problems into components, (b) anchor on base rates, (c) update incrementally, (d) seek diverse perspectives, (e) track their own accuracy. Tournament structure cultivates these habits through repeated practice with instant feedback.

**Teams multiply skill**: Superforecaster teams sharing information beat individual superforecasters, but only when diversity exists. Clones don't help each other.

**Aggregation matters**: The best single forecast comes from extremizing the most recent predictions of top forecasters in that domain when they converge.
