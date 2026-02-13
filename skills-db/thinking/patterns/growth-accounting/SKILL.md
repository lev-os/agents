---
name: growth-accounting
description: Framework for decomposing user growth into New, Retained, Resurrected, and Churned users to diagnose growth health beyond vanity metrics
---

# Growth Accounting

## Overview

Growth Accounting, popularized by Brian Balfour (founder of Reforge, former VP Growth at HubSpot), decomposes aggregate user growth into four fundamental components: New Users (first-time users in period), Retained Users (existing active users who remain active), Resurrected Users (previously churned users who reactivate), and Churned Users (previously active users who become inactive). Unlike vanity metrics that only track total user counts or percentage growth rates, Growth Accounting reveals the underlying health of growth by exposing whether expansion is driven by acquisition, retention, or resurrection - and how much churn is offsetting those gains. The framework helps identify "leaky bucket" problems where high churn cancels acquisition efforts, diagnose when to shift focus from acquisition to retention, and understand growth composition changes across lifecycle stages. The fundamental formula is: Active Users (end) = Retained + New + Resurrected - Churned. This accounting-style approach treats users like financial assets with inflows, outflows, and balance changes.

## When to Use

- Diagnosing why growth has slowed despite continued acquisition efforts
- Deciding resource allocation between acquisition, retention, and reactivation
- Identifying whether you have a "leaky bucket" (churn) or "empty pipeline" (acquisition) problem
- Evaluating the health of growth beyond total active user counts
- Understanding how growth composition shifts across company lifecycle stages
- Setting team goals that align with true growth drivers
- Communicating growth quality to investors or leadership
- Detecting early warning signals before aggregate metrics show problems

## The Process

### Step 1: Define Active Users and Time Period

Establish clear definitions for "active user" based on your product's core value delivery. For social apps, might be "posted or engaged weekly." For SaaS, "logged in and used key feature monthly." Choose time period granularity (daily, weekly, monthly) matching your product usage frequency. Monthly is most common for B2B/SaaS, weekly for consumer apps, daily for high-frequency products. Consistency is critical - changing definitions invalidates historical comparisons. **Example:** Productivity SaaS defines active as "logged in and created/edited at least one document in the past 30 days." Tracks monthly cohorts.

### Step 2: Segment Users Into Four Categories

For each time period, categorize all users: (1) **New Users** - first activity ever in this period, (2) **Retained Users** - active in previous period AND active this period, (3) **Resurrected Users** - inactive in previous period (churned) but active again this period, (4) **Churned Users** - active in previous period but NOT active this period. Track the count in each category. These four buckets are mutually exclusive and collectively exhaustive. **Example:** Month 5 has 1,000 New, 8,000 Retained (from Month 4's active users), 500 Resurrected (were inactive in Month 4), 2,000 Churned (were active in Month 4 but not in Month 5).

### Step 3: Calculate Net Growth Formula

Apply the core formula: **Active Users (current period) = Retained Users + New Users + Resurrected Users**. Then calculate: **Net Growth = New + Resurrected - Churned**. Verify totals: Active Users (previous period) + Net Growth = Active Users (current period). Express as absolute numbers and percentages. Track trends over multiple periods. **Example:** Month 4 had 10,000 active. Month 5: 8,000 Retained + 1,000 New + 500 Resurrected = 9,500 Active. Net Growth = 1,000 + 500 - 2,000 = -500 (-5%). Despite adding 1,000 new users, total users declined due to churn.

### Step 4: Analyze Growth Composition and Health

Examine the ratio of components to diagnose growth health. **Healthy growth:** Retention >70%, New/Resurrected cover Churned with surplus, Net Growth positive and accelerating. **Leaky bucket:** High New but Churned nearly equals or exceeds New + Resurrected, flat or negative Net Growth. **Acquisition problem:** Low New, high Retention, limited upside without more top-of-funnel. **Resurrection opportunity:** Significant Churned population available for win-back campaigns. Calculate "Quick Ratio" (New + Resurrected) ÷ Churned - above 4 indicates very healthy growth. **Example:** Company has 60% Retained, 15% New, 5% Resurrected, 20% Churned. Quick Ratio = (15 + 5) ÷ 20 = 1.0. Just replacing churn, not growing. Problem is retention, not acquisition.

### Step 5: Track Cohort-Based Retention Curves

Beyond aggregate accounting, analyze retention by cohort (users who joined in the same period). Plot retention curves showing what percentage of each cohort remains active after 1 month, 3 months, 6 months, etc. Overlay curves to see if retention is improving for recent cohorts. Identify when retention flattens (good) vs continues declining (bad). Cohorts with improving retention suggest product-market fit strengthening. **Example:** January cohort: 100% active Month 0, 40% Month 1, 25% Month 3, 20% Month 6. March cohort: 100% Month 0, 60% Month 1, 50% Month 3, 45% Month 6. Retention improved significantly - recent users stick better.

### Step 6: Set Targeted Initiatives by Component

Based on which component is weakest, prioritize interventions. **Low New:** Increase acquisition spend, expand channels, improve conversion funnels. **Low Retained:** Fix onboarding, improve core product value, increase engagement triggers. **High Churned:** Identify churn reasons, implement retention features, improve customer success. **Low Resurrected:** Create win-back campaigns, re-engagement emails, special offers. Set team OKRs against specific components rather than aggregate growth. **Example:** Data shows 25% monthly churn. Form retention squad focused exclusively on reducing churn to 15% through onboarding improvements, engagement loops, and at-risk user interventions.

### Step 7: Monitor as Leading Indicator Dashboard

Build real-time dashboard tracking all four components plus Quick Ratio and cohort retention. Set alert thresholds for concerning changes (churn spike, retention drop, acquisition decline). Review weekly in leadership meetings. Compare against historical baselines and growth targets. Growth Accounting provides leading indicators before aggregate metrics show problems - catching a retention drop early prevents compounding negative effects. **Example:** Dashboard shows Churned increased from 15% to 22% week-over-week. Investigation reveals recent product bug affecting power users. Fix deployed immediately before churn compounds into massive user loss.

## Example Application

**Situation:** B2B SaaS company with 50,000 active users growing 5% monthly. CEO excited about growth, but CFO concerned about efficiency. Leadership debate: invest more in paid ads or focus on product improvements?

**Application:**
- **Step 1 (Define):** Active = "logged in and used core features at least once in past 30 days." Track monthly.
- **Step 2 (Segment):** Month 12 data: 47,500 Previous Active Users. Current month: 33,250 Retained, 5,000 New, 2,000 Resurrected, 14,250 Churned. Total Active: 40,250 (33,250 + 5,000 + 2,000).
- **Step 3 (Calculate):** Net Growth = 5,000 + 2,000 - 14,250 = -7,250 (-15% from previous period). Wait - total active should be 47,500 + (-7,250) = 40,250. Matches. Actually shrinking despite CEO's perception of 5% growth (was looking at MRR, not user count).
- **Step 4 (Analyze):** Retention = 33,250 ÷ 47,500 = 70%. Churn = 30%. Quick Ratio = (5,000 + 2,000) ÷ 14,250 = 0.49. Severely unhealthy - adding 1 user for every 2 lost. Classic "leaky bucket." Problem is retention/churn, NOT acquisition. More paid ads would waste money.
- **Step 5 (Cohorts):** Recent cohort analysis shows Month 10 cohort has 40% retention at Month 2, vs Month 6 cohort had 65% retention at Month 2. Retention is degrading - recent product changes harmed experience.
- **Step 6 (Initiatives):** Shift all resources to retention. Freeze acquisition spend. Form retention taskforce: (1) Conduct churn surveys, (2) Improve onboarding flow, (3) Add engagement triggers, (4) Launch customer success outreach to at-risk users, (5) Fix product issues identified in feedback.
- **Step 7 (Monitor):** Build Growth Accounting dashboard reviewed in weekly exec meetings. Set targets: reduce churn to 15%, increase Retained to 85%, achieve Quick Ratio >2.0 within 6 months.

**Result:** Within 4 months, churn dropped to 18%, retention increased to 82%, Quick Ratio reached 2.3. Net growth turned positive at +8%. Company avoided wasting $500K on acquisition that would have compounded the leaky bucket problem.

## Anti-Patterns

**Tracking Only Total Active Users:** Aggregate metrics hide underlying problems. Total users can grow while health deteriorates (high churn masked by aggressive acquisition). Growth Accounting exposes composition and quality of growth.

**Conflating Revenue Growth with User Growth:** Revenue can grow (upsells, price increases) while user base shrinks. Tracking MRR alone misses user retention problems that eventually impact revenue. Monitor both separately.

**Ignoring Churn Until It's a Crisis:** Small churn rate increases compound catastrophically over time. 20% monthly churn means 89% of users gone within 12 months. Early detection through Growth Accounting prevents disasters.

**Overinvesting in Acquisition with Poor Retention:** Pouring money into ads while churning 30%+ monthly is like filling a bathtub with the drain open. Fix retention before scaling acquisition. Quick Ratio <1.0 means net negative growth regardless of spend.

**Not Segmenting Cohorts:** Aggregate retention rates hide whether recent cohorts are improving or degrading. Always analyze cohort-based retention curves to detect product-market fit changes.

## Real-World Examples

**Slack (Retention-First Growth):** Focused obsessively on 2,000 message milestone (teams sending 2K messages have 93% retention). Prioritized retention improvements over acquisition. Result: low churn, high Quick Ratio, sustainable exponential growth.

**Facebook (Resurrection Focus):** Noticed large population of churned users. Built dedicated team for re-engagement through email campaigns, friend invitations, and content notifications. Resurrected Users became 15%+ of active base, driving growth revival.

**HubSpot (Cohort Retention Improvement):** Tracked cohort retention curves aggressively. Identified that onboarding changes improved Month 1 retention from 70% to 85% for new cohorts. Compounding effect of higher retention enabled scaling acquisition with confidence.

## Sources

- [Brian Balfour (Reforge): A Deep Dive Into How the Best AI Products Grow](https://creatoreconomy.so/p/brian-balfour-how-top-ai-products-grow)
- [The Universal Growth Loop — Brian Balfour](https://brianbalfour.com/quick-takes/universal-growth-loop)
- [Growth Accounting Framework - Reforge Resources](https://www.reforge.com/)
