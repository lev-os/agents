# Insight Engine & Anomaly Detection

> Insights are signals that demand attention. They should be actionable, evidence-backed, and dismissible.

## Two-Tier Architecture

### Tier 1: Deterministic Rule Engine

Rule-based, no ML, no AI. Evaluates current metrics against thresholds. Fast, debuggable, predictable.

### Tier 2: Statistical Anomaly Detection

Z-score based time series analysis. Detects deviations from recent patterns. Slightly more sophisticated but still fully deterministic.

---

## Tier 1: Rule-Based Insights

### Insight Data Structure

```typescript
Insight {
  id: string;                    // Stable ID for dedup/dismissal
  severity: 'critical' | 'warning' | 'info';
  category: InsightCategory;
  title: string;                 // Short headline
  description: string;           // 1-2 sentence explanation
  evidence: {
    metric: string;              // What was measured
    current: number;             // Current value
    threshold: number;           // What triggered the alert
    previous?: number;           // Comparison value
    trend: 'up' | 'down' | 'stable';
  };
  suggestedAction: string;       // What to do about it
  sourceUrl: string;             // Link to deeper investigation
  createdAt: Date;
  expiresAt?: Date;              // Auto-dismiss if stale
}
```

### Insight Categories

| Category | Examples |
|----------|---------|
| `revenue` | MRR milestone, revenue drop |
| `churn` | Churn spike, mass cancellations |
| `conversion` | Conversion rate drop |
| `fees` | Fee drift from expected rate |
| `geographic` | Concentration risk |
| `activation` | New users not activating |
| `data_quality` | Stale data, missing sources |
| `infrastructure` | Quota warnings |

### Rule Catalog

#### Revenue Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| MRR milestone | MRR crosses $1k/$5k/$10k/$20k | info | Celebrate, set next target |
| Revenue drop | WoW revenue down > 20% | warning | Investigate payment failures |

#### Churn Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Churn spike | 30d rate > 2× 90d baseline | warning | Review at-risk subscribers |
| Mass cancellation | > 5 cancellations in 24h | critical | Check for product incident |

#### Runway Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Runway critical | < 3 months | critical | Reduce burn or raise cash |
| Runway warning | < 6 months | warning | Monitor burn rate closely |

#### Break-Even Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Break-even blocked | Contribution margin <= 0 | critical | Reduce fees or raise price |

#### Conversion Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Conversion drop | > 20% WoW decline (min 10 signups) | warning | Check onboarding, pricing |

#### Fee Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Fee drift | Effective rate deviates > 0.5% | warning | Audit provider mix |

#### Geographic Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Concentration | > 80% from single country | info | Diversification opportunity |

#### Activation Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Activation lag | > 5 new users inactive > 7 days | warning | Send setup guide emails |

#### Data Quality Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Stale data | > 60 min since last event | warning | Check webhook pipeline |
| Missing Stripe | STRIPE_SECRET_KEY not set | info | Configure Stripe |
| Missing PayPal | PAYPAL_CLIENT_ID not set | info | Configure PayPal |

#### Infrastructure Rules

| Rule | Trigger | Severity | Action |
|------|---------|----------|--------|
| Quota risk | Approaching platform limits | warning | Upgrade plan |

### Threshold Configuration

```typescript
const THRESHOLDS = {
  conversionDropPercent: 20,     // Alert if conversion drops >20% WoW
  conversionMinimumSample: 10,   // Need at least 10 signups to trigger
  churnSpikeMultiplier: 2,       // Alert if churn is 2x average
  churnMinimumSample: 5,         // Need at least 5 churns to trigger
  feeDriftPercent: 0.5,          // Alert if fee rate changes >0.5%
  geoConcentrationPercent: 80,   // Alert if >80% from single country
  activationDays: 7,             // Users should activate within 7 days
  activationMinimumUsers: 5,     // Min inactive users to trigger
  stalenessMinutes: 60,          // Data staleness threshold
};
```

---

## Tier 2: Statistical Anomaly Detection

### Z-Score Method

```
Z = (observed_value - mean) / standard_deviation
```

**Severity mapping:**

| |Z| Range | Severity | Meaning |
|-----------|----------|---------|
| 2.5 - 3.0 | low | Unusual but not alarming |
| 3.0 - 3.5 | medium | Statistically significant |
| 3.5 - 4.0 | high | Rare event (< 0.02%) |
| >= 4.0 | critical | Extremely rare |

### Welford's Algorithm

For numerical stability when computing running mean and variance:

```typescript
function welfordStats(values: number[]): { mean: number; stdDev: number } {
  let n = 0, mean = 0, m2 = 0;
  for (const x of values) {
    n++;
    const delta = x - mean;
    mean += delta / n;
    const delta2 = x - mean;
    m2 += delta * delta2;
  }
  if (n < 2) return { mean, stdDev: 0 };
  return { mean, stdDev: Math.sqrt(m2 / (n - 1)) }; // Bessel's correction
}
```

### Time Series Densification

Before computing Z-scores, fill missing days with zeros:

```typescript
function densifyTimeSeries(
  data: TimeSeriesPoint[],
  startDate: Date,
  endDate: Date,
  defaultValue = 0
): TimeSeriesPoint[] {
  const dataMap = new Map(data.map(p => [p.date, p.value]));
  const result = [];
  for (let d = startDate; d <= endDate; d = addDays(d, 1)) {
    const key = formatDate(d);
    result.push({ date: key, value: dataMap.get(key) ?? defaultValue });
  }
  return result;
}
```

Missing days are NOT anomalies — they're zeros. Without densification, Z-scores are wrong.

### Metrics Monitored

| Metric | Data Source | Aggregation |
|--------|-----------|-------------|
| Daily signups | users.createdAt | COUNT per day |
| Daily revenue | paymentEvents (succeeded) | SUM(amount) per day |
| Daily usage events | usageEvents.timestamp | COUNT per day |
| Daily error events | usageEvents WHERE success=false | COUNT per day |
| Daily installs | usageEvents WHERE type='install' | COUNT per day |

### Window Size

Default: 7 days. Too short (3d) = too noisy. Too long (30d) = too slow to react.

---

## Daily Brief Generation

Automated daily summary combining all signals:

```typescript
DailyBrief {
  type: 'daily' | 'weekly';
  summary: string;           // "MRR grew 3.2% to $1,240. 2 new subscribers, 0 churned."
  highlights: string[];      // Positive signals
  alerts: string[];          // Negative signals
  recommendations: string[]; // Suggested actions
  metrics: {
    mrr, mrrChange,
    newUsers, churnedUsers, activeUsers,
    newSubscribers, conversionRate,
    activatedSubscribers, activationRate,
    installs, installsPerSubscriber,
    errorEvents, errorRatePerSession,
    retentionD1, retentionD7,
  };
  generatedAt: string;
}
```

---

## Insight Dismissal

Insights should be dismissible to reduce noise:

```typescript
// Dismiss for 7 days (snooze)
insightDismissals table {
  insightId: string;
  adminUserId: string;
  dismissedAt: Date;
  expiresAt: Date;  // 7 days from dismissal
}

// Filter: exclude dismissed insights whose expiresAt > NOW()
```

---

## Data Quality Metadata

Track whether each data source is available and fresh:

```typescript
dataQuality: {
  stripeConfigured: boolean;     // STRIPE_SECRET_KEY exists
  paypalConfigured: boolean;     // PAYPAL_CLIENT_ID exists
  ga4Configured: boolean;        // GA4_MEASUREMENT_ID exists
  dataFreshness: 'fresh' | 'stale' | 'missing';
}
```

Display this on the dashboard so the admin knows which metrics are trustworthy.
