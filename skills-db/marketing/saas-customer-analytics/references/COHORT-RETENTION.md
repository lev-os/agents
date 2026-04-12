# Cohort Analysis & Retention

> Retention is the only metric that tells you if your product actually works. MRR can grow from acquisition alone — retention tells you if people stay.

## Cohort Retention Matrix

### The Model

Group users by signup month. For each cohort, track what percentage remain active at week 1, 2, 3, ... 12.

```
             Week 0   Week 1   Week 2   Week 3   Week 4   ...   Week 12
Jan 2026     100%     78%      65%      58%      52%            38%
Feb 2026     100%     82%      70%      63%      55%            —
Mar 2026     100%     75%      —        —        —              —
```

### Query Pattern

```sql
-- Define cohorts by signup month
WITH cohorts AS (
  SELECT
    id AS user_id,
    DATE_TRUNC('month', created_at) AS cohort_month,
    created_at
  FROM users
),

-- For each cohort user, check if they were active in each subsequent week
activity AS (
  SELECT
    c.user_id,
    c.cohort_month,
    FLOOR(EXTRACT(EPOCH FROM (ue.timestamp - c.created_at)) / (7 * 86400))::int AS week_number
  FROM cohorts c
  INNER JOIN usage_events ue ON ue.user_id = c.user_id
  WHERE ue.timestamp >= c.created_at
  GROUP BY c.user_id, c.cohort_month, week_number
)

-- Aggregate: what % of each cohort was active in each week
SELECT
  cohort_month,
  COUNT(DISTINCT user_id) AS cohort_size,
  week_number,
  COUNT(DISTINCT user_id) AS active_count,
  ROUND(COUNT(DISTINCT user_id)::numeric / NULLIF(
    (SELECT COUNT(DISTINCT user_id) FROM activity a2 WHERE a2.cohort_month = a.cohort_month), 0
  ) * 100, 1) AS retention_pct
FROM activity a
WHERE week_number BETWEEN 0 AND 12
GROUP BY cohort_month, week_number
ORDER BY cohort_month, week_number;
```

### Output Shape

```typescript
CohortRetention {
  cohorts: Array<{
    cohort: string;        // "2026-01"
    size: number;          // Users in this cohort
    retention: number[];   // [100, 78, 65, 58, ...] percentage per week
    avgLtv: number;        // Estimated LTV for this cohort
  }>;
  overallRetention: number[];  // Averaged across all cohorts
}
```

### Cohort LTV

```
Cohort LTV = (subscribedCount / cohortSize) × avgSubscriptionMonths × subscriptionPrice
```

This tells you which acquisition channels produce the highest-value customers.

---

## Point-in-Time Retention (D1, D7, D30)

Track what percentage of users return after N days:

| Metric | Definition | Healthy Benchmark |
|--------|-----------|-------------------|
| D1 Retention | % active 1 day after signup | > 40% |
| D7 Retention | % active 7 days after signup | > 25% |
| D30 Retention | % active 30 days after signup | > 15% |

### Calculation

```sql
-- D7 retention for users who signed up in the last 30 days
WITH eligible AS (
  SELECT id, created_at
  FROM users
  WHERE created_at >= NOW() - INTERVAL '30 days'
    AND created_at <= NOW() - INTERVAL '7 days'  -- Must be old enough
),
returned AS (
  SELECT DISTINCT e.id
  FROM eligible e
  INNER JOIN usage_events ue ON ue.user_id = e.id
  WHERE ue.timestamp >= e.created_at + INTERVAL '7 days'
    AND ue.timestamp < e.created_at + INTERVAL '8 days'
)
SELECT
  COUNT(returned.id)::float / NULLIF(COUNT(eligible.id), 0) * 100 AS d7_retention
FROM eligible
LEFT JOIN returned ON eligible.id = returned.id;
```

---

## Retention Curves

Plot retention percentage over time to identify the "retention cliff" — the point where most churn happens.

```
100% ─┐
      │\
  80% ─│ \
      │  \
  60% ─│   ╲
      │    ╲_________     ← Flattening = found product-market fit
  40% ─│              ╲___
      │
  20% ─│
      │
   0% ─┼───┬───┬───┬───┬───
       W0  W1  W2  W3  W4
```

**Interpretation:**
- **Steep initial drop, then flat**: Normal. Fix onboarding, not the product.
- **Gradual decline forever**: Product doesn't retain. Fix core value prop.
- **Flat then sudden drop**: Something breaks after N weeks. Investigate.

---

## Weekly Cohort Retention Heatmap

Visualization pattern for engagement analytics:

```typescript
// Build the retention matrix from engagement data
interface RetentionHeatmapCell {
  cohortWeek: string;     // "2026-W12"
  weeksSince: number;     // 0, 1, 2, ...
  retentionPct: number;   // 0-100
  activeCount: number;
  cohortSize: number;
}
```

**Color scale:**
- 80-100%: Deep green (strong retention)
- 60-79%: Light green
- 40-59%: Yellow (concerning)
- 20-39%: Orange (problematic)
- 0-19%: Red (churned)

---

## Overall Retention Curve

Aggregate across all cohorts for the "average" retention experience:

```typescript
function calculateOverallRetention(cohorts: CohortData[]): number[] {
  const maxWeeks = 12;
  const overall: number[] = [];

  for (let week = 0; week <= maxWeeks; week++) {
    let totalRetained = 0;
    let totalCohorts = 0;

    for (const cohort of cohorts) {
      if (cohort.retention[week] !== undefined) {
        totalRetained += cohort.retention[week];
        totalCohorts++;
      }
    }

    overall.push(totalCohorts > 0 ? totalRetained / totalCohorts : 0);
  }

  return overall;
}
```

---

## Conversion Paths

Track the journey from signup to paid subscriber:

```typescript
ConversionPath {
  stage: string;            // "signup_to_subscribe"
  count: number;            // Users who completed this path
  avgDaysToConvert: number; // Average time to convert
  conversionRate: number;   // % of eligible who converted
}
```

**Key metric:** Average days to subscribe. If it's > 14 days, your onboarding has a problem. If it's < 2 days, you're doing great.

---

## Cohort Comparison

Compare two cohorts head-to-head to measure the impact of product changes:

| Metric | Jan Cohort | Feb Cohort | Delta |
|--------|-----------|-----------|-------|
| Size | 120 | 145 | +20.8% |
| Conversions | 24 | 35 | +45.8% |
| Conversion Rate | 20% | 24.1% | +4.1pp |
| D7 Retention | 62% | 71% | +9pp |
| Avg LTV | $180 | $220 | +22.2% |

If you shipped an onboarding improvement between Jan and Feb, this table tells you if it worked.

---

## Anti-Patterns

| Don't | Why | Do |
|-------|-----|-----|
| Compare cohorts of different sizes | Skews percentages | Note sample size alongside % |
| Use "active" without defining it | Ambiguous | Define: "had at least 1 usage event" |
| Include test accounts | Inflates retention | Filter by email suffix |
| Measure retention from first payment | Misses free-tier behavior | Measure from signup date |
| Only look at D30 | Misses early churn cliff | Track D1, D7, D14, D30 together |
