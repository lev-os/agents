---
name: north-star-framework
description: Product strategy model that aligns teams around a single metric capturing core customer value, plus supporting input metrics that drive it
---

# North Star Framework

## Overview

The North Star Framework, coined by Sean Ellis in 2010 and systematized by Amplitude through research across 11,000+ companies, addresses the failure mode of teams optimizing disconnected metrics. This framework identifies one North Star Metric (NSM) that best captures the core value delivered to customers, serving as a leading indicator of sustainable growth. Unlike vanity metrics (signups, downloads), a strong NSM connects customer value to business outcomes and remains relevant across growth stages. The framework extends beyond the single metric to include 3-5 input metrics (levers that move the NSM) and work streams (team initiatives targeting those inputs). Amplitude's research identified three product "games": Attention (time spent), Transaction (purchase frequency), and Productivity (efficiency gains) - each requiring different NSM structures.

## When to Use

- Aligning cross-functional teams around what actually matters (not outputs)
- Preventing optimization of local metrics that hurt overall product health
- Focusing leadership discussions on value delivery vs. activity reporting
- Onboarding new team members to product strategy quickly
- Making roadmap trade-offs transparent (does it move the North Star?)
- Diagnosing stalled growth by decomposing NSM into input metrics
- Evolving from founder-led intuition to data-driven product culture
- Preventing "metric shopping" when results disappoint

## The Process

### Step 1: Identify Your Product's Core Value Exchange

Articulate what fundamental value customers get from your product in one sentence. This is not your pitch, it's the reason customers return. Test: If this value disappeared, would customers be "very disappointed" (PMF litmus)? **Example:** Spotify: "Discover and listen to music you love", Uber: "Get reliable transportation on-demand", Notion: "Organize information for personal and team productivity".

### Step 2: Determine Your Product Game Type

Classify your product using Amplitude's three games framework. Attention game: monetize engagement (ad-supported, social). Transaction game: monetize purchases (e-commerce, SaaS subscriptions). Productivity game: monetize efficiency gains (B2B tools, enterprise software). Hybrid: some products blend games (Netflix = attention for retention, transaction for subscription). **Example:** TikTok plays Attention game (time spent watching), Shopify plays Transaction game (GMV processed), Slack plays Productivity game (messages sent/team collaboration).

### Step 3: Select Your North Star Metric (7 Criteria Checklist)

Evaluate candidate metrics against Amplitude's criteria: (1) Expresses value - captures customer benefit not company benefit, (2) Represents vision - measurable progress toward long-term goals, (3) Leading indicator - predicts future revenue/retention, (4) Actionable - teams can influence through product changes, (5) Understandable - non-technical partners grasp it, (6) Measurable - accurately tracked in analytics, (7) Not vanity - resists gaming/manipulation. **Example:** Airbnb's NSM: "Nights booked" (not signups or listings) - directly captures value exchange, predicts revenue, actionable by growth and host quality work.

### Step 4: Decompose NSM Into 3-5 Input Metrics

Break North Star into the 3-5 levers that mathematically drive it. These become focus areas for different teams. Use product analytics to identify which inputs have strongest correlation. Good inputs are: mutually exclusive (minimal overlap), collectively exhaustive (explain most NSM variance), actionable by specific teams. **Example:** Spotify's "Time Spent Listening" driven by: (1) Daily Active Users, (2) Songs per session, (3) Session frequency, (4) Listening completion rate, (5) Content catalog breadth. Each owned by different teams (Growth, Discovery, Engagement, Quality, Licensing).

### Step 5: Map Work Streams to Input Metrics

Assign cross-functional teams/squads to own each input metric. Each work stream develops hypotheses for moving their input (which flows up to NSM). Teams define their own sub-metrics and experiments. Creates clear ownership and accountability. **Example:** At Amplitude, "Weekly Querying Users" (NSM) supported by: Onboarding team → activation rate, Expansion team → feature adoption, Retention team → habit formation, Growth team → qualified signups.

### Step 6: Establish Measurement Cadence and Dashboards

Create executive dashboard showing NSM trend plus input metrics. Weekly or monthly review depending on product velocity. Include: current value, trend (vs. last period), goal/target, % of target achieved, variance explanation. Make visible to entire company. **Example:** Weekly all-hands displays: North Star (green/red trend), 5 input metrics (sparklines + owners), current quarter goal progress, biggest movers (wins and concerns).

### Step 7: Evolve NSM as Product Matures (Re-evaluate Annually)

North Star may change as company stage evolves. Early stage: activation metrics (new user value). Growth stage: engagement/retention. Maturity: monetization efficiency. Validate NSM still predicts revenue and retention quarterly. Don't change reactively to make numbers look better. **Example:** Amplitude evolved from "Weekly Querying Users" to include "Teams with 5+ WQUs" as they moved upmarket to enterprise, recognizing team-level retention matters more than individual users.

## Example Application

**Situation:** B2B SaaS project management tool, $10M ARR, 200 customers, 5,000 users. Growth stalled at 10% YoY. Three teams (Growth, Product, Engineering) optimizing different metrics: signups, feature releases, uptime. Leadership can't diagnose why growth slowed despite hitting team OKRs.

**Application**:

**Step 1-3**: Core value = "Teams complete projects faster through collaboration". Product game = Productivity. NSM candidates evaluated:
- Active projects: gameable (fake projects)
- Tasks completed: vanity (empty tasks)
- Projects completed on-time: leading indicator ✓
- **Selected NSM: "Teams with 5+ active collaborators completing 2+ projects/month"** - captures collaboration + output value.

**Step 4-5**: Input metric decomposition:
1. Team activation rate (onboarded with 5+ members) - Growth team
2. Collaboration breadth (% projects with 3+ contributors) - Product team
3. Feature adoption rate (using 4+ core features) - Product team
4. Time to first project completion - Onboarding team
5. Month-over-month project throughput - Customer success

**Step 6-7**: Quarterly review revealed: NSM flat despite 30% signup growth. Root cause: Teams activating with only 1-2 members (input #1 declining). Growth team was optimizing individual signups, not team activation. Shifted focus to "invite 4+ teammates" onboarding flow, referral incentives for team buyers.

**Outcome:** 6 months post-NSM implementation: NSM up 35% (more teams hitting 5+ collaborators), revenue retention improved from 85% to 92% (activated teams churn less), engineering stopped building single-user features that don't drive collaboration. Company aligned on one definition of success.

## Anti-Patterns

- Choosing metric that makes current results look good (vanity North Star)
- Selecting multiple North Stars for different stakeholders (defeats alignment purpose)
- Using lagging business metrics as NSM (revenue, churn - not leading indicators)
- Picking NSM before understanding core value proposition (metric-first thinking)
- Input metrics that don't mathematically drive NSM (correlation without causation)
- Changing NSM quarterly when results disappoint (destroys strategic consistency)
- Making NSM so complex that teams can't remember it (defeats communication purpose)
- No ownership of input metrics (everyone's responsibility = no one's)

## Related

- Product-Market Fit Survey - validate North Star captures "very disappointed" value
- OKRs (Objectives and Key Results) - North Star informs objective, inputs become key results
- AARRR Pirate Metrics - North Star should connect to Activation or Retention layers
- Kano Model - helps identify which features move North Star (vs. indifferent features)
- RICE Prioritization - Impact score should reference NSM impact
- Jobs to Be Done - JTBD defines customer value that North Star measures
- Product Analytics - tools like Amplitude, Mixpanel required to track NSM and inputs
- Unit Economics - North Star should have causal link to LTV and CAC efficiency
