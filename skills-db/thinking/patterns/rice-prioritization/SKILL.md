---
name: rice-prioritization
description: Scoring framework using Reach, Impact, Confidence, and Effort to objectively prioritize product features and projects
---

# RICE Prioritization Framework

## Overview

RICE, developed by Intercom's product team after finding other frameworks inadequate, provides a quantitative scoring system for prioritizing disparate product ideas objectively. The framework calculates a single score representing "total impact per time worked" - exactly what product teams want to maximize. RICE uses four factors: Reach (how many users affected per time period), Impact (how much it moves the needle per user), Confidence (how certain are estimates), and Effort (person-months required). The formula (Reach × Impact × Confidence) / Effort produces comparable scores across wildly different feature types, from infrastructure to UI polish.

## When to Use

- Prioritizing a backlog with competing features across different domains
- Making objective decisions when stakeholders disagree on priority
- Comparing vastly different initiatives (new feature vs. technical debt vs. UX improvement)
- Preventing bias toward features you personally would use
- Creating transparent, data-driven roadmaps that stakeholders can challenge
- Quarterly planning when resources are constrained and trade-offs required
- Training product managers on systematic prioritization thinking

## The Process

### Step 1: Define Reach - How Many People Per Time Period?

Estimate how many users/customers/transactions will be affected within a specific timeframe (per quarter or per month). Use actual numbers from analytics, not percentages. Be consistent with time period across all initiatives. **Example:** "5,000 users per quarter" or "200 transactions per month", not "10% of users" or "some customers".

### Step 2: Score Impact - How Much Per Person?

Use a constrained scale to prevent endless debate: Massive = 3x, High = 2x, Medium = 1x, Low = 0.5x, Minimal = 0.25x. Ask: "If we built this, how much would it improve outcomes for each affected user?" Focus on your North Star Metric or key success metric. **Example:** Feature reducing checkout time 50% = Massive (3x), UI polish improving NPS by 2 points = Low (0.5x).

### Step 3: Apply Confidence - How Sure Are We?

Use percentages with discrete options to avoid analysis paralysis: 100% = high confidence (strong data), 80% = medium (some data or expertise), 50% = low (educated guess). Below 50% = moonshot (don't estimate, just mark low confidence). Confidence penalizes optimistic estimates lacking evidence. **Example:** Feature requested by 50 customers with willingness-to-pay data = 100%, CEO's hunch = 50%.

### Step 4: Estimate Effort - How Many Person-Months?

Count total team effort across all functions (design, engineering, QA, PM). Use whole numbers or 0.5 month minimum - avoid false precision. Include only build effort, not ongoing maintenance. Conservative estimates better than optimistic. **Example:** Simple UI change = 0.5 person-months, new dashboard = 2 person-months, payment integration = 6 person-months.

### Step 5: Calculate RICE Score

Apply formula: (Reach × Impact × Confidence) / Effort. Higher scores = higher priority. Score represents impact per unit of effort. **Example:** Feature A: (5,000 × 2 × 0.8) / 3 = 2,667. Feature B: (500 × 3 × 1.0) / 0.5 = 3,000. Despite lower reach, Feature B scores higher due to massive impact and low effort.

### Step 6: Rank and Validate

Sort all initiatives by RICE score descending. Review top and bottom 10% for sanity check - do rankings feel directionally right? If rankings seem off, examine which factor is likely wrong and re-estimate. Don't override the model without documenting why. **Example:** If score puts critical bug fix below minor feature, you likely underestimated Impact or Reach of bug.

### Step 7: Allocate Resources and Re-score Quarterly

Work down the ranked list until resources exhausted. As work progresses, update scores based on actual data (real reach, measured impact, true effort). Re-score backlog quarterly as context changes. **Example:** After shipping feature, actual reach was 8,000 (vs. estimated 5,000), impact validated at High (2x), effort was 4 months (vs. 3 estimated) - update model for better future estimates.

## Example Application

**Situation:** Product team with 3 engineers, 1 designer, 1 PM for Q4. Backlog has 25 features spanning onboarding improvements, API enhancements, mobile app features, and infrastructure work.

**Application (sample of 5 features scored)**:

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| A: Mobile dark mode | 8,000/qtr | 0.5 (Low) | 80% | 1 PM | 3,200 |
| B: Email onboarding flow | 12,000/qtr | 2 (High) | 100% | 2 PM | 12,000 |
| C: API rate limiting | 200/qtr | 3 (Massive) | 80% | 3 PM | 160 |
| D: Dashboard redesign | 15,000/qtr | 1 (Medium) | 80% | 6 PM | 2,000 |
| E: 2FA authentication | 20,000/qtr | 3 (Massive) | 50% | 4 PM | 7,500 |

**Prioritization**: B (12,000) → E (7,500) → A (3,200) → D (2,000) → C (160)

**Outcome:** Team has 15 person-months capacity (3 eng × 3 months + 1 design × 3 months + 1 PM × 3 months). Execute B + E + A (totaling 7 PM) and half of D. API rate limiting (C) deprioritized despite enterprise customer request due to low reach. Transparent scoring prevented political override.

## Anti-Patterns

- Using percentages instead of absolute numbers for Reach (makes comparison impossible)
- Overly precise Impact scoring (debating 1.7x vs 1.8x defeats constrained-scale purpose)
- Inflating Confidence without data to game rankings (destroys model credibility)
- Underestimating Effort systematically (optimism bias inflates all scores)
- Cherry-picking which factors to include per initiative (inconsistent methodology)
- Overriding model rankings without documenting rationale (destroys transparency)
- One-time scoring exercise without quarterly updates (stale estimates)
- Ignoring context (sometimes low-score critical bugs must be fixed regardless)

## Related

- North Star Metric - defines what "Impact" should measure against
- OKRs (Objectives and Key Results) - RICE helps prioritize initiatives within OKRs
- ICE Scoring (Impact, Confidence, Ease) - simpler variant without Reach
- WSJF (Weighted Shortest Job First) - SAFe framework with similar cost-of-delay thinking
- Kano Model - categorizes features by customer satisfaction impact (complements RICE Impact)
- Value vs. Effort Matrix - 2x2 visual alternative, less precise than RICE
- Opportunity Solution Trees (Teresa Torres) - helps identify opportunities to score with RICE
