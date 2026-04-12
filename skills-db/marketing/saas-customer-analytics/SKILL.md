---
name: saas-customer-analytics
description: >-
  SaaS analytics: MRR, churn, behavioral scoring, Monte Carlo, interventions, Stripe/PayPal.
  Use when building subscription analytics, revenue projections, or admin dashboards.
---

# SaaS Customer Analytics

> **Core Insight:** Revenue is a lagging indicator. Behavior is the leading one.
> By the time MRR drops, the subscriber already disengaged weeks ago.
> Build systems that detect behavioral decay, not just billing events.

## The Architecture (Data Flow)

```
Stripe/PayPal Webhooks
    │
    ▼
Immutable Payment Event Ledger ──────────────────────────────────────────┐
    │                                                                    │
    ▼                                                                    │
Subscription Status (mutable, current state only)                        │
    │                                                                    │
    ├──► MRR/ARR Calculation ◄───── Organization Billing                 │
    │        │                                                           │
    │        ├──► Unit Economics (ARPU, LTV, gross margin)               │
    │        ├──► Break-Even Analysis                                    │
    │        ├──► Runway Calculator                                      │
    │        └──► Revenue Projections (30/60/90d)                        │
    │                                                                    │
    ├──► Churn Rate (30d/90d windows) ──► Monte Carlo Simulation         │
    │                                                                    │
    ├──► Payment Fee Tracker ◄───────────────────────────────────────────┘
    │        (queries ledger, NOT mutable subscription table)
    │
Usage Events (append-only) ──► Behavioral Scoring ──► Customer Health
    │                              │                       │
    │                              ├──► Churn Prediction    │
    │                              └──► Risk Drivers        │
    │                                                       │
    └──► Insight Engine ◄──────────────────────────────────┘
              │
              ├──► Anomaly Detection (Z-score)
              ├──► Rule-Based Alerts (thresholds)
              └──► Intervention Engine (automated retention)
```

## The Five Pillars

| # | Pillar | Purpose | Key Principle |
|---|--------|---------|---------------|
| 1 | [Financial Metrics](#1-financial-metrics) | Know your unit economics | Derive from immutable ledger, not mutable state |
| 2 | [Behavioral Scoring](#2-behavioral-scoring) | Predict churn before it happens | Weight recency > frequency > breadth |
| 3 | [Stochastic Modeling](#3-stochastic-modeling) | Quantify uncertainty | Never present a single projection |
| 4 | [Insight Generation](#4-insight-generation) | Surface actionable signals | Rule-based first, ML never |
| 5 | [Automated Intervention](#5-automated-intervention) | Retain at-risk subscribers | Trigger on behavior, not billing |

---

## 1. Financial Metrics

### MRR Calculation (The Foundation)

```
MRR = (Active Individual Subscribers × Price) + SUM(Org Monthly Costs)
```

**Critical rules:**
- Count `active` AND `past_due` (grace period = still paying)
- Exclude test accounts by email suffix AND subscription ID prefix
- Exclude E2E test organizations by naming convention
- Query the DB for real counts — never cache subscriber counts stale

**Full formula catalog:** [FORMULAS.md](references/FORMULAS.md)

### The Immutable Ledger Principle

**NEVER calculate financial metrics from mutable state.** Subscription tables track *current* status. Payment event ledgers track *what happened*. For fee calculations, revenue attribution, and audit trails — always query the immutable ledger.

```
paymentEvents table (append-only, immutable)
├── provider: "stripe" | "paypal"
├── eventType: "invoice.payment_succeeded" | "PAYMENT.SALE.COMPLETED" | ...
├── eventId: unique per (provider, eventId) — idempotency key
├── payload: JSONB (full webhook body)
├── processedAt: timestamp (null until side effects complete)
└── reconciledAt: timestamp (distributed lock for retry)
```

### Unit Economics Stack

| Metric | Formula | Reference |
|--------|---------|-----------|
| ARPU | Subscription price (fixed or weighted average) | [FORMULAS.md](references/FORMULAS.md) |
| LTV | ARPU / (Monthly Churn Rate) | Cap at 120x price if churn = 0 |
| Gross Margin | (ARPU - Avg Payment Fee) / ARPU | Provider-weighted blend |
| Contribution Margin | ARPU - Payment Fees | Per-subscriber |
| Break-Even Subs | Fixed Costs / Contribution Margin | Must be > 0 to be reachable |
| Months to Break-Even | log(BE Subs / Current) / log(1 + Growth) | Only if growth > 0 |
| Runway | Available Cash / Net Burn | null if profitable |

**Deep dive:** [METRICS.md](references/METRICS.md)

---

## 2. Behavioral Scoring

### Health Score (0-100)

Four equally weighted factors, each 0-25:

| Factor | Signal | Score Logic |
|--------|--------|-------------|
| **Engagement** | Active days in 30d | 0→0, 1-3→10, 4-10→18, 11+→25 |
| **Breadth** | Unique event types + skills | Narrow=5, moderate=15, broad=25 |
| **Recency** | Days since last activity | 0-2→25, 3-7→20, 8-14→12, 15-30→5, 30+→0 |
| **Payment** | Status + failure history | Active+clean=25, past_due=10, failures=5 |

### Risk Level Mapping

| Score | Level | Action |
|-------|-------|--------|
| 70-100 | Low | Monitor only |
| 50-69 | Medium | Watch for decline |
| 30-49 | High | Proactive outreach |
| 0-29 | Critical | Immediate intervention |

### Churn Probability

Logistic function from 19 weighted behavioral drivers across 5 categories:
- **Activation** — not activated, slow activation, rapid activation
- **Engagement** — active days, event volume, workflow breadth
- **Recency** — inactivity thresholds (3d, 14d, 30d)
- **Retention** — usage trend (declining/improving), multi-product adoption
- **Payments** — payment failures, product error frequency

**Full scoring model:** [CHURN.md](references/CHURN.md)

---

## 3. Stochastic Modeling

### Monte Carlo Revenue Simulation

**Never present a single revenue projection.** Show P10/P50/P90 ranges.

```
For each of N iterations (100-10,000):
  For each month (1-120):
    churn_rate = sample_normal(mean_churn, stddev_churn) clamped [0, 1]
    growth_rate = sample_normal(mean_growth, stddev_growth) clamped [-0.5, 2]
    churned = round(subscribers × churn_rate)
    acquired = round(subscribers × growth_rate)
    subscribers = max(0, subscribers - churned + acquired)
    gross_mrr = subscribers × price
    net_mrr = gross_mrr - fees - fixed_costs
    cash += net_mrr
    if cash <= 0: BANKRUPT — stop this run
```

**Output:** P10/P50/P90 for MRR, runway months, 12-month survival probability.

**Box-Muller transform:** `sqrt(-2 * ln(U1)) * cos(2pi * U2)` for normal sampling.

**Full methodology:** [MONTE-CARLO.md](references/MONTE-CARLO.md)

### Scenario Planning

What-if analysis with parameter overrides:
- Price change (test new pricing)
- Churn rate override (model improvement)
- Growth rate override (marketing investment)
- Additional costs (new infrastructure)

Each scenario runs the full financial stack with overridden params.

---

## 4. Insight Generation

### Two-Tier System

**Tier 1: Deterministic Rule Engine** (no ML, no AI)
- Churn spike: 30d rate > 2x 90d baseline
- Runway alerts: < 3 months critical, < 6 months warning
- Break-even blocked: contribution margin <= 0
- MRR milestones: $1k, $5k, $10k, $20k thresholds
- Conversion drops: > 20% WoW decline
- Fee drift: > 0.5% change from expected
- Geographic concentration: > 80% from single country
- Activation lag: > 7 days without product use

**Tier 2: Statistical Anomaly Detection** (Z-score)
- Window: 7 days, Welford's algorithm for numerical stability
- Severity: |Z| 2.5-3=low, 3-3.5=medium, 3.5-4=high, >=4=critical
- Metrics: daily signups, revenue, usage, errors, installs

**Full insight catalog:** [INSIGHTS.md](references/INSIGHTS.md)

---

## 5. Automated Intervention

### Threshold Types

| Type | When | Example |
|------|------|---------|
| **Static** | Known threshold | `churnProbability > 0.7` |
| **Adaptive Quantile** | Relative to population | `healthScore <= 10th percentile` |
| **Adaptive Z-score** | Statistical outlier | `engagementDrop Z >= 2.5` |
| **Bayes Rate** | Confidence-bounded | `activationRate below baseline at 95% CI` |

### Action Types

| Action | Target | When |
|--------|--------|------|
| Notification | In-app | Medium risk, engagement drop |
| Email (setup guide) | Inactive new user | Not activated within 7 days |
| Email (rescue) | Declining user | High churn probability |
| Churn prediction log | Admin dashboard | All at-risk users |

**Full intervention model:** [INTERVENTION.md](references/INTERVENTION.md)

---

## Aggregation Pattern (The Adapter)

Combine all metrics into a single cached summary for dashboard widgets:

```typescript
const settled = await Promise.allSettled([
  calculateUnitEconomics(),
  getPaymentFeeReport(days),
  calculateRunway(availableCash),
  calculateBreakEven(),
  calculateChurnRate(30),
  calculateChurnRate(90),
  getBehavioralSnapshot(),
]);
// Each metric fails independently — graceful degradation
```

**Cache:** 60s TTL keyed on `${availableCash}:${days}`. Widget shows stale data with indicator rather than crashing.

---

## 6. Subscription State Machine

The most bug-prone layer. Every edge case you don't handle = a customer locked out of what they paid for.

```
none ──checkout──► active ──payment fails──► past_due ──grace expires──► cancelled
                     ▲                          │                           │
                     │        payment recovered  │      user resubscribes   │
                     └──────────────────────────┘◄──────────────────────────┘
```

### Access Rules (Critical Path)

```
Access = Individual Access OR Organization Access

Individual:
  active → YES
  past_due + within 21-day grace → YES (show banner)
  cancelled + period not expired → YES (paid-through)
  else → NO

Organization:
  org.status IN (active, past_due) AND member.role ≠ viewer → YES
```

### Multi-Subscription Tie-Breaking

Score: active=1000, past_due-in-grace=750, cancelled-paid-through=500, paused_for_org=250. Tie-break on `updatedAt`.

**Full state machine:** [STATE-MACHINE.md](references/STATE-MACHINE.md)

---

## 7. Dunning & Payment Recovery

Failed payments cause 20-40% of all SaaS churn. Most is involuntary.

```
Day 0:  Payment fails → past_due → dunning email #1
Day 7:  Reminder email → "Update your payment method"
Day 14: Final warning → "Access suspended in 7 days"
Day 21: Grace expires → cancelled → access revoked
```

**Key rules:**
- Grace period starts from `currentPeriodEnd`, not failure date
- Deduplicate emails within 24h (webhook retries cause duplicates)
- Team dunning uses shorter grace (3→7→30 days)
- Track recovery rate — if < 50%, your sequence is too passive

**Full dunning system:** [DUNNING.md](references/DUNNING.md)

---

## 8. Engagement Analytics

The bridge between acquisition and retention.

| Metric | Formula | Healthy Benchmark |
|--------|---------|-------------------|
| TTFV | median(first_event - signup) | < 24 hours |
| D1 Retention | % active 1 day after signup | > 40% |
| D7 Retention | % active 7 days after signup | > 25% |
| D30 Retention | % active 30 days after signup | > 15% |
| DAU/MAU | daily active / monthly active | > 0.15 for dev tools |

### Adoption Funnel

```
Browse → View Detail → Install → Repeat Use (3+ times)
```

For each stage, track drop-off % and generate recommendations when > 50% drop.

**Full engagement model:** [ENGAGEMENT.md](references/ENGAGEMENT.md)

---

## 9. Cohort Analysis

Group users by signup month, track retention week-by-week. This is how you measure product-market fit.

```
             W0    W1    W2    W3    W4    ...   W12
Jan 2026    100%   78%   65%   58%   52%         38%
Feb 2026    100%   82%   70%   63%   55%         —
```

### Cohort LTV

```
Cohort LTV = (subscribedCount / cohortSize) × avgSubscriptionMonths × price
```

Compare cohorts to measure impact of product changes: if Feb retention > Jan, your onboarding improvement worked.

**Full cohort methodology:** [COHORT-RETENTION.md](references/COHORT-RETENTION.md)

---

## 10. Resilience Patterns

Your analytics are only as reliable as the event pipeline.

### Email Retry: Exponential backoff (1m→2m→4m→8m), max 5 attempts, then DLQ.
### Distributed Locks: Redis SET NX PX for cross-worker serialization; Postgres advisory locks for transaction-scoped.
### Rate Limiting: Tiered (anon 600/min, auth 30K/min, subscriber unlimited). **Never rate-limit paying customers.**
### Cron Idempotency: All aggregation jobs use `ON CONFLICT DO UPDATE` (upsert).
### Fail Open: If Redis is down, allow all requests. Log warning, exponential backoff on reconnect.

**Full resilience patterns:** [RESILIENCE.md](references/RESILIENCE.md)

---

## 11. Rigorous Mathematical Modeling

Upgrade from heuristics to principled, calibrated, uncertainty-aware models. These 8 methods are ranked by EV and natural fit — implement top-to-bottom.

| # | Method | Replaces | Key Artifact |
|---|--------|----------|-------------|
| 1 | **Survival Analysis** (Kaplan-Meier + Cox PH) | Naive churn rate | Calibrated survival curves, hazard ratios, LTV via ∫S(t)dt |
| 2 | **Bayesian Conjugate Updating** (Beta-Binomial) | Point estimate churn rates | Posterior with credible intervals, automatic uncertainty |
| 3 | **Empirical Bayes / Shrinkage** | Noisy small-cohort estimates | Shrunk estimates that are provably better (James-Stein) |
| 4 | **Sequential Testing** (SPRT / e-values) | Z-score anomaly detection | Anytime-valid change detection with formal error guarantees |
| 5 | **CVaR / EVT** | P10 from Monte Carlo | Expected revenue in worst 10% of outcomes (tail severity) |
| 6 | **Renewal Theory** | Naive is_active × price | Effective MRR accounting for payment failure/retry dynamics |
| 7 | **Hidden Markov Models** | 2x threshold regime detection | Posterior probability of business regime (Growth/Plateau/Decline/Crisis) |
| 8 | **Multi-Armed Bandits** (Thompson Sampling) | Static intervention rules | Adaptive intervention selection that learns which action works for which segment |

**Tier 2 (requires Tier 1 outputs):**

| # | Method | Replaces | Key Artifact |
|---|--------|----------|-------------|
| 9 | **Conformal Prediction** | Uncalibrated churn probabilities | Finite-sample coverage guarantees, Mondrian per-segment |
| 10 | **Causal Inference** (PSM, IV, DiD) | "Did the intervention work?" guessing | ATE, NNT, ROI per intervention with confounding control |
| 11 | **Influence Functions** | Equal-weight customer treatment | Concentration risk dashboard, Herfindahl Index |
| 12 | **Convex Budget Allocation** | Sort-by-churn-probability | Revenue-weighted optimal targeting with shadow prices |
| 13 | **BOCPD** (Bayesian Changepoint) | 2x threshold rule | Posterior probability of change at each timestep |
| 14 | **Bifurcation Analysis** | Linear break-even | Tipping point identification, early warning signals |
| 15 | **Hawkes Processes** | Independent churn assumption | Contagion-aware churn with branching ratio monitoring |
| 16 | **Optimal Experimental Design** | Equal-split A/B tests | D-optimal allocation, sequential sample sizing |

**Fallback principle:** Every advanced method must degrade to the simpler baseline when data is insufficient. Bayesian posteriors widen to priors. Survival curves fall back to naive rates. SPRT falls back to Z-score.

**Full methodology (16 methods), composition diagram, proof obligations, and fallback tables:** [ADVANCED-MODELING.md](references/ADVANCED-MODELING.md)

---

## 12. Visualization & Dashboard UX

Every metric needs 5 layers: NUMBER → COMPARISON (▲ 8.1%) → SHAPE (sparkline) → WHY (decomposition) → SO WHAT (action). Most dashboards stop at layer 2.

**Library stack:** Recharts + Tremor + Nivo + Framer Motion. Add D3/Visx only for bespoke.

### Chart Type Rules

| Metric | Chart | Never Use |
|--------|-------|-----------|
| Revenue over time | Filled area | Bar (too discrete) |
| Monte Carlo P10/P50/P90 | Fan chart (3-band) | Single line (false precision) |
| Cohort retention | Heatmap | Line per cohort (spaghetti) |
| Health distribution | Horizontal stacked bar | Pie (too many segments) |
| Survival curve | Step function | Smooth line (implies interpolation) |

### The KPI Card: Value (28-32px) → Trend (emerald ▲ / rose ▼) → Sparkline (30d, no axes). Invert color for "down is good" metrics. Click → detail page.

### Color: emerald=growth, rose=decline, amber=warning. **Never color alone** — always pair with icon/label (8% of men are red-green color blind).

**Full library guide, cognitive principles, layout patterns, a11y, responsive, anti-patterns:** [VISUALIZATION.md](references/VISUALIZATION.md)

---

## 13. Agent-Optimized Interfaces (Robot Mode)

Every metric visible to humans MUST be available via structured JSON. Design both human and agent interfaces as first-class from day one.

### CLI: `your-cli analytics summary --json`
~500 tokens: full business state + pre-computed `signals[]` + `next_actions[]` with exact follow-up commands. Agents don't compute thresholds — the system pre-digests intelligence.

### Diff: `your-cli analytics diff --json --since 24h`
Token-efficient delta. Each change has `significance` field (`normal`/`notable`/`anomaly`) pre-computed via Z-score.

### Compact mode (`--compact`): Abbreviated keys, omit nulls/defaults — 40-60% token savings.

### Autonomous Workflows
- **Every 5 min:** diff → alert on anomalies → auto-intervene on critical at-risk users
- **Daily:** summary → compose executive brief → send to human operator
- **Weekly:** summary + cohorts + monte-carlo → strategic report with P10/P50/P90

### Safety: Agents read everything, trigger emails/notifications. CANNOT cancel subs, issue refunds, or change pricing. All actions audit-logged.

### MCP: 5 tools (`saas_analytics_summary`, `_diff`, `_at_risk`, `_intervene`, `_monte_carlo`) for any MCP-compatible agent.

**Full CLI tree, REST API, JSON schemas, interpretation templates, token patterns, MCP tools, safety, testing:** [AGENT-INTERFACE.md](references/AGENT-INTERFACE.md)

---

## Maturity Model: Build Order

### Phase 1: Foundation
- [ ] Immutable payment event ledger + webhook handlers
- [ ] Subscription state machine with access rules
- [ ] MRR calculation (individual + org)
- [ ] Basic admin dashboard with MRR, subscriber count
- [ ] Test data exclusion

### Phase 2: Core Analytics
- [ ] Churn rate (30d/90d windows)
- [ ] Unit economics (ARPU, LTV, gross margin, break-even)
- [ ] Runway calculator
- [ ] Payment fee tracking (blended Stripe/PayPal)
- [ ] Dunning sequence (3-email, 21-day grace)

### Phase 3: Behavioral Intelligence
- [ ] Usage event collection (append-only)
- [ ] Health score (4-factor, 0-100)
- [ ] Churn prediction (19 behavioral drivers)
- [ ] D1/D7/D30 retention tracking
- [ ] Engagement analytics (TTFV, sessions, adoption funnel)

### Phase 4: Forecasting
- [ ] Monte Carlo simulation (P10/P50/P90)
- [ ] Scenario planning (what-if analysis)
- [ ] Cohort retention matrices
- [ ] Behavioral forecast (12-month projection)

### Phase 5: Automation
- [ ] Insight engine (rule-based + Z-score)
- [ ] Intervention engine (threshold → action)
- [ ] Webhook reconciliation cron
- [ ] Email retry + DLQ
- [ ] Daily brief generation

### Phase 6: Mathematical Rigor
- [ ] Bayesian churn posteriors (replace point estimates with Beta-Binomial)
- [ ] Empirical Bayes shrinkage for small cohorts
- [ ] CVaR in Monte Carlo (tail-risk severity)
- [ ] Survival curves (Kaplan-Meier from subscription data)
- [ ] Sequential testing (SPRT replaces Z-score)
- [ ] Cox proportional hazards (learned churn drivers)
- [ ] Thompson Sampling for intervention optimization

---

## Checklist: Building From Scratch

- [ ] **Schema**: Immutable `paymentEvents` + mutable `subscriptions` + append-only `usageEvents`
- [ ] **Webhooks**: Stripe + PayPal handlers → ledger first, side effects second
- [ ] **Reconciliation**: Cron job retries unprocessed events (5min window, max 5 retries)
- [ ] **State Machine**: Subscription states (active/past_due/cancelled/paused) with access rules
- [ ] **Dunning**: 3-email sequence over 21-day grace period, dedup within 24h
- [ ] **MRR**: Query real subscriber counts, exclude test data, handle multi-provider
- [ ] **Unit Economics**: ARPU, LTV, gross margin, contribution margin, break-even
- [ ] **Churn Rate**: 30d and 90d rolling windows with proper denominator
- [ ] **Engagement**: TTFV, D1/D7/D30 retention, adoption funnel, session metrics
- [ ] **Cohort Analysis**: Monthly cohorts, retention heatmap, cohort LTV
- [ ] **Behavioral Scoring**: Health score per subscriber, 4-factor model
- [ ] **Monte Carlo**: P10/P50/P90 projections, bankruptcy detection
- [ ] **Insights**: Rule-based alerts + Z-score anomalies
- [ ] **Interventions**: Threshold → action mapping with cooldowns
- [ ] **Dashboard**: Graceful degradation, TanStack Query, skeleton states
- [ ] **Resilience**: Email DLQ, distributed locks, rate limiting, cron idempotency
- [ ] **Audit Logging**: Non-blocking, before/after state, IP tracking
- [ ] **Test Data Exclusion**: Filter by email suffix, subscription ID prefix, org name

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Calculate fees from subscriptions table | Mutable, loses history | Query immutable payment event ledger |
| Show single-point projections | False precision under uncertainty | Monte Carlo P10/P50/P90 ranges |
| Use ML for insight generation | Opaque, hard to debug, overkill | Rule-based heuristics + Z-score |
| Cache subscriber counts aggressively | Stale data → wrong MRR | Short TTL (60s), DB is source of truth |
| Treat past_due as churned | Grace period — they may recover | Count as active, flag for monitoring |
| Include test accounts in metrics | Skews all calculations | Filter by email suffix, sub ID prefix |
| Fail the whole dashboard if one metric fails | One bad query kills admin UX | `Promise.allSettled()` + graceful degradation |
| Predict churn from billing events alone | Billing is lagging indicator | Behavioral signals predict 2-4 weeks earlier |

**Full anti-patterns:** [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md)

---

## Reference Index

| Need | Reference |
|------|-----------|
| All financial formulas | [FORMULAS.md](references/FORMULAS.md) |
| Complete metrics catalog | [METRICS.md](references/METRICS.md) |
| Churn prediction & behavioral scoring | [CHURN.md](references/CHURN.md) |
| Monte Carlo methodology | [MONTE-CARLO.md](references/MONTE-CARLO.md) |
| Stripe/PayPal integration patterns | [PAYMENT-INTEGRATION.md](references/PAYMENT-INTEGRATION.md) |
| Insight engine & anomaly detection | [INSIGHTS.md](references/INSIGHTS.md) |
| Automated retention interventions | [INTERVENTION.md](references/INTERVENTION.md) |
| Database schema patterns | [SCHEMA.md](references/SCHEMA.md) |
| Admin dashboard architecture | [DASHBOARD.md](references/DASHBOARD.md) |
| Anti-patterns & failure modes | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| Cohort analysis & retention matrices | [COHORT-RETENTION.md](references/COHORT-RETENTION.md) |
| Dunning & payment recovery | [DUNNING.md](references/DUNNING.md) |
| Subscription state machine | [STATE-MACHINE.md](references/STATE-MACHINE.md) |
| Engagement analytics (TTFV, DAU/MAU) | [ENGAGEMENT.md](references/ENGAGEMENT.md) |
| Resilience (DLQ, locks, rate limits) | [RESILIENCE.md](references/RESILIENCE.md) |
| Advanced modeling (survival, Bayesian, CVaR) | [ADVANCED-MODELING.md](references/ADVANCED-MODELING.md) |
| Visualization & chart library guide | [VISUALIZATION.md](references/VISUALIZATION.md) |
| Agent/CLI/API interface design | [AGENT-INTERFACE.md](references/AGENT-INTERFACE.md) |
