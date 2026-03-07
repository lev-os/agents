---
name: wisdom-of-crowds-aggregation
description: Combine diverse independent estimates to produce more accurate predictions than any single expert, when conditions support collective intelligence
---

# Wisdom of Crowds Aggregation

**What**: A method of improving forecast accuracy by aggregating multiple independent estimates from a diverse group, which often outperforms individual experts—provided the crowd meets specific conditions.

**When to use**: When making predictions or estimates where no single person has complete information, and you can gather independent judgments from diverse participants.

**Introduced by**: Francis Galton (1907 ox weight estimation), popularized by James Surowiecki (2004), formalized by Tetlock's Good Judgment Project

## Core Mechanism

**The magic**: Average 100 mediocre estimates and you often beat the best individual expert.

**Why it works**: Individual errors cancel out if they're random and independent. The signal (truth) reinforces, while noise (individual biases) cancels.

**Critical conditions (Surowiecki's four pillars)**:
1. **Diversity**: Participants have different information and perspectives
2. **Independence**: Estimates made without influence from others
3. **Decentralization**: People draw on local/specialized knowledge
4. **Aggregation mechanism**: A method to combine judgments into collective decision

## When to Apply

**Use wisdom of crowds when:**
- Estimating uncertain quantities (timelines, costs, probabilities)
- Making predictions where expertise is distributed
- No single person has monopoly on relevant information
- You can ensure independent judgments
- Diverse perspectives exist in the group

**Skip if:**
- Objective correct answer is easily verifiable (don't need a crowd to count inventory)
- Group lacks diversity (homogeneous groups don't benefit)
- Independence impossible (groupthink, cascades, public estimates)
- Specialized domain requires deep expertise (surgery techniques)

## Execution Steps

### 1. Assemble Diverse Group
Recruit participants with varied backgrounds, information sources, and perspectives. Homogeneous crowds lose advantage.

### 2. Ensure Independence
Collect estimates separately before discussion. Public estimates create herding and destroy independence.

### 3. Provide Clear Question Framing
Use precise, unambiguous questions. "When will X ship?" should specify definition of "ship" (code complete, QA pass, deployed).

### 4. Choose Aggregation Method
- **Simple average**: Works well for symmetric error distributions
- **Median**: Robust to outliers
- **Trimmed mean**: Remove extreme 10% on each end
- **Extremizing**: Adjust away from 50% for tournament-style predictions (Tetlock)

### 5. Collect Rationales (Optional)
Ask participants to briefly explain reasoning. Helps identify who has relevant information vs. guessing.

### 6. Iterate if Possible
After aggregation, share result and ask for updates. Crowds can improve over rounds if independence maintained.

### 7. Weight by Track Record
If you have historical calibration data, weight forecasters who've been accurate. Tetlock's superforecasters improved crowd estimates.

## Real-World Applications

**Galton's Ox**: 787 fairgoers estimated ox weight. Median guess: 1207 pounds. Actual: 1198 pounds. Crowd error: 0.8%. No individual that accurate.

**Tetlock's Good Judgment Project**: Aggregated forecasts from thousands of participants outperformed intelligence analysts with classified information. Simple averaging worked; weighting by track record worked even better.

**Planning Poker (Agile)**: Team estimates task complexity independently, reveals simultaneously, discusses outliers, converges. Reduces anchoring bias from first speaker.

**Google Internal Forecasting**: Aggregates employee predictions on product launches, hiring pipeline, project timelines. Outperforms individual manager estimates.

## Key Indicators

**Signs it's working:**
- Aggregate more accurate than most individuals
- Diversity of estimates (not everyone clustering)
- Improves over time as poor forecasters learn or exit
- Outlier explanations reveal useful information

**Red flags:**
- All estimates suspiciously similar (herding)
- Groupthink or public discussion before independent estimates
- Lack of diversity in perspective or information
- Aggregate no better than random individual

## Common Mistakes

**Failing to ensure independence**: Letting people see others' estimates before committing. Destroys the main advantage.

**Insufficient diversity**: Asking 10 people from same team, background, or information source. Correlated errors don't cancel.

**Expert dismissal**: "Why ask non-experts?" But diverse crowd often beats expert in uncertain domains with distributed information.

**Mistiming aggregation**: Aggregating too early (not enough data) or too late (independence compromised by discussion).

## Related Frameworks

**Complementary**: Prediction Markets (mechanism to aggregate), Delphi Method (structured expert consensus), Superforecasting (improving individual inputs)

**Contrasting**: Expert Opinion (single source), Consensus Building (seeks agreement, not aggregation), Autocracy (single decision-maker)

**Sequential**: Frame question → Collect independent diverse estimates → Aggregate with appropriate method → Evaluate accuracy → Iterate or weight future contributions

## Practical Examples

**Project Timeline Estimation**:
Ask 5 team members independently: "Probability we ship by March 31?"
Responses: 30%, 45%, 60%, 40%, 50%
Average: 45% (likely more accurate than any individual)
Median: 45%
Action: Plan for ~50% confidence level, prepare contingencies.

**Bug Severity Triage**:
3 engineers independently assess: "How critical is this bug?"
A: High (UI breaks for 10% of users)
B: Medium (workaround exists)
C: High (affects checkout flow)
Aggregate: High severity (2/3 vote, both cite customer impact)

**Market Sizing**:
Diverse team estimates TAM independently:
Sales: $5M (bottom-up from leads)
Marketing: $8M (top-down from market research)
Finance: $6M (comparable company analysis)
Product: $7M (user survey extrapolation)
Average: $6.5M (probably better than any single estimate)

## Measurement

**Accuracy metrics:**
- Absolute error: |Aggregate estimate - Actual outcome|
- Compared to: Best individual, Median individual, Random individual
- Track over time: Does aggregate improve with more forecasts?

**Process health:**
- Diversity score: Variance in estimates (low variance = potential groupthink)
- Independence verification: Time-stamped submissions, sealed estimates
- Participant calibration: Track individual accuracy over time

## Scoring Criteria

**Practitioner Weight**: 10/10 — Validated by Galton, Surowiecki, Tetlock's extensive research, and widespread adoption by Google, prediction platforms, agile teams

**Clarity & Executability**: 9/10 — Clear concept and straightforward execution; main challenge is ensuring independence and diversity

**Proven ROI**: 9/10 — Demonstrated accuracy improvements across forecasting tournaments, estimation tasks, and organizational prediction problems

**Novelty**: 8/10 — Counterintuitive that aggregating non-experts beats individual experts; challenges traditional authority structures

**Cross-Domain Applicability**: 9/10 — Applies to forecasting, estimation, decision-making, prediction markets, agile planning, risk assessment

**Total Score**: 45/50 (Tier 1: Canonical)
