---
name: goodharts-law
description: Anticipate metric gaming and unintended optimization by recognizing that when a measure becomes a target, it ceases to be a good measure
---

# Goodhart's Law

**What**: An adage stating "When a measure becomes a target, it ceases to be a good measure." Once people optimize for a metric, they find ways to improve the metric that don't improve (or actively harm) the underlying goal.

**When to use**: When designing KPIs, performance metrics, incentive systems, or any measurement system where human behavior will adapt to the measurement.

**Introduced by**: Charles Goodhart (1975), economist studying monetary policy targets

## Core Mechanism

Metrics are proxies for goals, not the goals themselves. When you incentivize a proxy, intelligent agents find the cheapest path to move the metric—often by exploiting the gap between metric and goal rather than achieving the goal itself.

**Why it happens**: Metrics are simplifications. They capture some aspects of the goal but never all of them. Optimization pressure finds and exploits the gaps.

## When to Apply

**Use Goodhart's Law awareness when:**
- Designing performance metrics or KPIs for teams
- Creating incentive compensation structures
- Setting up A/B testing or optimization frameworks
- Establishing SLAs or quality standards
- Implementing algorithmic ranking or recommendation systems

**High-risk contexts:**
- Systems where metrics are tied to rewards (bonuses, promotions, funding)
- Automated optimization (algorithms, AI models)
- Competitive environments (rankings, leaderboards)
- High-stakes evaluations (hiring, performance reviews)

## Execution Steps

### 1. Distinguish Goal from Measure
Clearly separate what you actually want (goal) from how you're tracking it (metric). The metric is a proxy, not the objective.

### 2. Ask "How Could This Be Gamed?"
Red-team your own metrics. Brainstorm ways to improve the metric while harming the underlying goal. Those exploits will emerge naturally.

### 3. Use Metric Portfolios, Not Single Metrics
Combine multiple metrics that create tension. Gaming one should worsen another. Example: Speed + Quality + Customer Satisfaction vs. just Speed.

### 4. Separate Measurement from Target-Setting
Use metrics for visibility and diagnosis. Reserve target-setting for higher-level goals. "We measure X to understand Y" not "Hit X at all costs."

### 5. Include Counterbalancing Guardrails
For every metric you optimize, add constraints that prevent pathological optimization. Example: "Increase signups" + "Maintain activation rate above Z%."

### 6. Rotate or Evolve Metrics Over Time
Don't optimize the same metric forever. Once behavior has shifted, update the metric to capture new gaps or gaming strategies.

### 7. Inspect for Gaming Regularly
Monitor for warning signs: Metric improves while goal stagnates, clever workarounds emerge, or team behavior shifts in surprising ways.

## Real-World Applications

**Soviet Nail Factory**: Quota by weight → Factory produces fewer, heavier nails. Quota switched to count → Factory produces tiny useless nails. The metric shaped production, not customer need.

**Wells Fargo Account Scandal**: Incentivized account openings → Employees opened millions of fake accounts without customer knowledge to hit targets.

**Software Bug Counts**: Rewarding developers for fixing bugs → Developers split one bug into many tickets or write buggy code to fix later. Bug count goes up, quality doesn't.

**Academic Citations**: Promotion based on citation count → Excessive self-citation, citation rings, salami slicing papers. Citation count up, research quality unchanged.

## Key Indicators

**Signs of Goodhart's Law in action:**
- Metric improving but stakeholders aren't happier
- Creative "interpretations" of how to count metric
- Behavior shifts that technically meet target but feel wrong
- Correlation between metric and goal weakens over time

**Healthy metric systems:**
- Multiple metrics in tension with each other
- Periodic metric review and evolution
- Qualitative assessment supplements quantitative
- Metrics inform discussion, don't dictate decisions

## Common Mistakes

**Single-metric optimization**: Optimizing one number creates blind spots and gaming opportunities.

**Confusing metric with goal**: "Increase test coverage" becomes the goal, forgetting that quality is the goal and coverage is one imperfect proxy.

**Ignoring feedback loops**: Metrics change behavior, which changes what the metric measures, invalidating the original correlation.

**Over-automation**: Algorithmic optimization of metrics without human judgment accelerates gaming and weird outcomes.

## Related Frameworks

**Complementary**: Campbell's Law (same insight from social science), Cobra Effect (perverse incentives), McNamara Fallacy (over-relying on quantification)

**Contrasting**: Management by Objectives (assumes metrics can capture goals accurately), Rational Economic Actor (assumes optimization serves intended purpose)

**Sequential**: Define true goal → Select proxy metrics → Anticipate gaming → Add counterbalances → Monitor for exploitation → Evolve metrics

## Practical Examples

**GitHub Contributions Graph**:
Problem: Commit count becomes hiring signal → People make trivial commits, rewrite history, or auto-commit to look active.
Fix: View commits as one signal among many; inspect code quality, PR discussions, not just activity heatmap.

**Customer Support Response Time**:
Problem: Optimize for "first response < 1 hour" → Agents send "We're looking into it" immediately, then ignore ticket.
Fix: Add metric for "time to resolution" and "customer satisfaction rating" to balance speed with quality.

**Test Coverage Percentage**:
Problem: "Must have 80% coverage" → Developers write tests that execute code but don't assert anything meaningful.
Fix: Use coverage for discovery (where are blind spots?) not targets. Supplement with mutation testing or manual review.

## Red Flags

**Warning signs you're vulnerable:**
- Tying bonuses or promotions to single metrics
- Celebrating metric improvements without checking underlying goal
- Lack of qualitative assessment alongside quantitative
- Metrics haven't changed in years despite gaming opportunities

**Gaming in progress:**
- Metric improves suddenly without process changes
- Clever accounting or definitional tricks
- Behavior that's "technically correct" but feels wrong
- Metric up, but customer/stakeholder complaints also up

## Measurement

**System health checks:**
- Correlation between metric and goal (should be stable; degradation = gaming)
- Diversity of metrics in use (1 = danger, 3-5 = healthy)
- Frequency of metric review/evolution (never = stale, quarterly = adaptive)
- Qualitative vs. quantitative balance in decisions

**Gaming detection:**
- Anomaly detection in metric trajectories
- Behavior pattern changes after metric introduction
- User feedback sentiment vs. metric trends
- Cross-reference metrics with independent goal assessments

## Scoring Criteria

**Practitioner Weight**: 9/10 — Goodhart was a Bank of England economist studying real policy failures; widely observed in business, government, and software

**Clarity & Executability**: 9/10 — Extremely clear one-sentence formulation; actionable guidance (use metric portfolios, anticipate gaming, separate measurement from targets)

**Proven ROI**: 9/10 — Understanding this prevents costly metric gaming, improves incentive design, widely taught in business schools and economics

**Novelty**: 8/10 — Counterintuitive that measurement itself corrupts what's measured; challenges management orthodoxy

**Cross-Domain Applicability**: 10/10 — Applies universally: economics, software, management, education, healthcare, government policy, ML systems

**Total Score**: 45/50 (Tier 1: Canonical)
