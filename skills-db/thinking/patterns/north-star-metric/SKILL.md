---
name: north-star-metric
description: Single metric framework that captures core product value and aligns teams on sustainable growth
---

# North Star Metric Framework

## Overview

The North Star Framework, popularized by Sean Ellis and formalized by Amplitude's research across 11,000+ companies, identifies a single crucial metric that best captures the core value your product delivers to customers. Unlike vanity metrics (signups, downloads), the North Star Metric (NSM) measures actual value delivery, serves as a leading indicator of sustainable growth, and directly connects to revenue. The framework includes the NSM plus key Input Metrics that teams can influence daily, creating alignment between product work and business outcomes.

## When to Use

- Aligning cross-functional teams (product, growth, engineering) around shared success definition
- Prioritizing features and experiments against clear value metric
- Diagnosing why growth has stalled or plateaued
- Replacing vanity metrics with actionable growth indicators
- Onboarding new team members to product strategy quickly
- Communicating product vision to stakeholders and investors
- Shifting from output-focused (ship features) to outcome-focused (deliver value) culture

## The Process

### Step 1: Identify Your Product's Core Value

Define what value users get when your product works perfectly. Ask: "What would users miss if this product disappeared?" Distinguish between activation (first value) and sustained value. **Example:** Spotify's core value is "time spent listening to music you love", not downloads or signups.

### Step 2: Choose Your Product "Game"

Amplitude identifies three archetypes: (1) Attention (maximize time/engagement - social, media), (2) Transaction (maximize purchases/exchanges - marketplace, e-commerce), (3) Productivity (maximize efficiency/output - SaaS tools). **Example:** Slack = Productivity game, Instagram = Attention game, Airbnb = Transaction game.

### Step 3: Define Your North Star Metric

Select ONE metric that reflects core value delivery, predicts revenue, and teams can influence. Test against six criteria: expresses value, represents strategy, leading indicator, actionable, understandable, measurable. **Example:** Airbnb uses "Nights Booked" (not signups or searches), Amplitude uses "Weekly Querying Users" (not total users).

### Step 4: Identify Key Input Metrics

Break down 3-5 measurable drivers that collectively produce your NSM. These should be metrics teams directly control through product changes. Map the causal relationship. **Example:** For "Nights Booked" → Inputs: active listings, search quality, booking conversion rate, host response time, guest retention rate.

### Step 5: Assign Team Ownership

Allocate specific teams to own each Input Metric. Give autonomy to experiment and improve their metric. Create accountability through regular metric reviews. **Example:** Search team owns "search quality", Host team owns "active listings", Booking team owns "conversion rate".

### Step 6: Instrument Measurement

Implement analytics to track NSM and Inputs in real-time. Build dashboards visible to entire company. Set up alerts for significant changes. Ensure data accuracy before making decisions. **Example:** Daily NSM dashboard, weekly team reviews, automated anomaly detection, quarterly deep-dives.

### Step 7: Test and Iterate

Run experiments to improve Input Metrics, measure impact on NSM. If NSM doesn't move, revisit Inputs or metric definition. Refine as business model evolves. **Example:** Test new search algorithm → measure search quality Input → validate impact on Nights Booked NSM.

## Example Application

**Situation:** B2B SaaS productivity tool had 50,000 users but flat revenue growth. Teams shipped features but unclear which mattered.

**Application:**
- Step 1: Core value = "Teams completing projects faster than alternatives"
- Step 2: Productivity game
- Step 3: NSM = "Weekly Active Collaborative Projects" (not total users or projects created)
- Step 4: Inputs = (a) Teams invited, (b) Project creation rate, (c) Cross-user collaboration actions, (d) Week-over-week project continuation, (e) Integration usage
- Step 5: Assigned 5 pod teams to own one Input each with OKRs
- Step 6: Built real-time dashboard, weekly metric reviews, experiment tracking
- Step 7: Ran 12 experiments in Q1, 60% moved Input metrics positively, 40% improved NSM

**Outcome:** NSM grew 35% in 6 months, revenue per user increased 28%, team velocity increased (fewer wasted features), clearer prioritization reduced roadmap conflicts.

## Anti-Patterns

- Choosing vanity metrics that don't predict revenue (total signups, page views, downloads)
- Multiple "North Stars" that conflict (defeats single-metric alignment purpose)
- NSM too far from team influence (annual revenue for engineering team)
- Ignoring Input Metrics and only tracking NSM (no actionable levers)
- NSM doesn't reflect actual user value ("daily logins" when users don't need daily usage)
- Gaming the metric (optimizing for measurement artifact, not real value)
- Changing NSM frequently (quarterly pivots destroy trend analysis)
- Not connecting NSM to business outcomes (metric moves but revenue doesn't)

## Related

- OKRs (Objectives and Key Results) - execution framework for NSM improvement
- AARRR Pirate Metrics - broader funnel view, NSM typically in Retention/Revenue
- Product-Market Fit Measurement - NSM helps quantify PMF strength
- Jobs to Be Done - defines core value that NSM should measure
- Growth Accounting - decomposes NSM into acquisition, retention, resurrection
- RICE Prioritization - uses NSM impact as the "Impact" scoring dimension
- Sean Ellis PMF Survey - "40% very disappointed" threshold, NSM tracks post-PMF
