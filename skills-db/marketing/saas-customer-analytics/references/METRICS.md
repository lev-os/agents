# Complete Metrics Catalog

> Every metric tracked in a production SaaS analytics system, organized by domain.

## Revenue Metrics

| Metric | Definition | Update Frequency | Source |
|--------|-----------|------------------|--------|
| MRR | Active subs × price + org billing | Real-time (cached 60s) | DB subscriptions + organizations |
| ARR | MRR × 12 | Derived from MRR | Calculated |
| Net New MRR | New + Expansion - Contraction - Churned | 30d rolling | DB subscriptions |
| Revenue Growth Rate | (Current - Previous) / Previous | 30d rolling | Derived |
| MRR by Provider | Stripe vs PayPal breakdown | Real-time | DB subscriptions |
| MRR by Segment | Individual vs Organization | Real-time | DB subscriptions + organizations |
| Projected MRR | Current × (1 + growth)^N | On-demand | Calculated |

## Subscriber Metrics

| Metric | Definition | Update Frequency | Source |
|--------|-----------|------------------|--------|
| Active Subscribers | status IN ('active', 'past_due') | Real-time | DB subscriptions |
| Churn Rate (30d) | Cancelled / Active at start × 100 | Rolling 30d | DB subscriptions |
| Churn Rate (90d) | Same, 90d window (baseline) | Rolling 90d | DB subscriptions |
| Avg Subscription Length | Mean(end - start) in days | On-demand | DB subscriptions |
| Conversion Rate | Paid users / Total users × 100 | On-demand | DB users + subscriptions |
| New Subscribers (period) | Created in period | Rolling | DB subscriptions |
| Churned Subscribers (period) | Cancelled in period | Rolling | DB subscriptions |

## Unit Economics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| ARPU | Price (or MRR / subs) | $20/mo for this product |
| LTV | ARPU / churn rate | > 12× ARPU = healthy |
| LTV/CAC | LTV / acquisition cost | > 3.0 = healthy |
| Gross Margin | (ARPU - fees) / ARPU | > 80% for software |
| Contribution Margin | ARPU - payment fees | Must be > 0 |
| Break-Even Subscribers | Fixed costs / contribution margin | Key milestone |
| Months to Break-Even | log formula with growth rate | < 12 = good trajectory |

## Runway Metrics

| Metric | Definition | Alert Thresholds |
|--------|-----------|-----------------|
| Available Cash | Input parameter (bank balance) | Manual input |
| Monthly Fixed Costs | Sum of infrastructure costs | Track for drift |
| Monthly Payment Fees | Subscribers × effective fee | Provider-dependent |
| Net Burn Rate | Total costs - MRR | Negative = profitable |
| Runway Months | Cash / net burn | < 3 = critical, < 6 = warning |
| Is Profitable | MRR > total costs | Boolean milestone |

## Customer Health Metrics

| Metric | Range | Weight | Factors |
|--------|-------|--------|---------|
| Health Score | 0-100 | Composite | Sum of 4 factors below |
| Engagement Score | 0-25 | 25% | Active days in 30d, event volume |
| Breadth Score | 0-25 | 25% | Unique event types, unique skills/features |
| Recency Score | 0-25 | 25% | Days since last activity |
| Payment Score | 0-25 | 25% | Status + failure history |
| Churn Probability | 0-1 | Derived | Logistic from weighted drivers |
| Churn Risk Level | low/med/high/critical | Derived | From health score thresholds |

## Behavioral Signals

| Signal | Meaning | Data Source |
|--------|---------|-------------|
| Active Days (7d/30d) | Days with any usage event | usageEvents |
| Event Count (7d/14d/30d) | Total events in window | usageEvents |
| Events Previous 14d | Comparison baseline for trend | usageEvents |
| Unique Event Types (30d) | Workflow breadth | usageEvents |
| Unique Skills/Features (30d) | Multi-product adoption | usageEvents |
| Activation Event Count | Install/sync/onboarding events | usageEvents |
| Activation Lag Days | Days from signup to first use | users + usageEvents |
| Payment Failures (90d) | Failed payment attempts | paymentEvents |
| Failed Product Events (30d) | CLI/API errors | usageEvents |
| Days Since Last Activity | Staleness signal | usageEvents |
| Subscription Age Days | Tenure (new vs established) | subscriptions |
| Usage Trend Ratio | events14 / eventsPrev14 | Calculated |

## Organization-Specific Metrics

| Metric | Definition | Risk Signal |
|--------|-----------|-------------|
| Member Count | Total members | — |
| Active Members (7d/30d) | Members with usage | Low = underutilization |
| Activated Members | Members who completed onboarding | Low = adoption failure |
| Seat Fill Ratio | Members / Max Seats | Low = over-provisioned |
| Active Seat Ratio | Active Members / Max Seats | Low = waste |
| Member Activation Rate | Activated / Total Members | < 50% = risk |
| Install Gap Count | Members without installation | High = onboarding failure |
| Expansion Potential | Available seats × seat price | Upsell opportunity |
| Owner Activity | Owner's last activity timestamp | Stale = high risk |
| Telemetry Coverage | Members sending telemetry | Low = blind spot |

## Anomaly Detection Metrics

| Metric | Window | Z-Score Thresholds |
|--------|--------|-------------------|
| Daily Signups | 7d | 2.5=low, 3=med, 3.5=high, 4=critical |
| Daily Revenue | 7d | Same |
| Daily Usage Events | 7d | Same |
| Daily Error Counts | 7d | Same |
| Daily Installs | 7d | Same |

## Payment Analytics

| Metric | Source | Update |
|--------|--------|--------|
| Stripe Balance (available + pending) | Stripe API | Real-time |
| PayPal Balance (by currency) | PayPal API | Real-time |
| Net Revenue | Balance transactions | On-demand |
| Fee Rate (effective) | Payment events ledger | 30d rolling |
| Invoice Success Rate | Paid / Total invoices | On-demand |
| Refund Count + Amount | Balance transactions | On-demand |
| Dispute Count + Amount | Balance transactions | On-demand |
| Payout Schedule | Stripe/PayPal APIs | Real-time |

## Engagement Analytics

| Metric | Definition | Benchmark |
|--------|-----------|-----------|
| DAU/MAU Ratio | Daily active / Monthly active | > 0.2 = engaged |
| Session Count | Time-window grouped activity | Track trend |
| TTFV | Time to first value (activation) | < 24h = good |
| D1/D7/D30 Retention | Users returning after N days | D30 > 20% |
| Feature Adoption Depth | Unique features used | Breadth indicator |
| Power Users | 95th percentile usage | Advocacy candidates |
| Channel Mix | CLI vs Web usage | Product health |

## Dashboard Refresh Strategy

| Metric Group | TTL | Rationale |
|-------------|-----|-----------|
| Summary Widget | 60s | Balance freshness vs DB load |
| Revenue Analytics | 5min | Acceptable staleness for graphs |
| Health Scores | On-demand | Expensive computation |
| Monte Carlo | Per-request | Compute-heavy, rate-limited |
| Live Metrics | SSE streaming | Real-time where needed |
| Behavioral Snapshot | On-demand | Heavy aggregation |
| Insights | 5min | Rule evaluation is fast |
