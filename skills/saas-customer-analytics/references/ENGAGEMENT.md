# Engagement Analytics

> Engagement is the bridge between acquisition and retention. Users who engage deeply churn less, upgrade more, and advocate for your product.

## Core Engagement Metrics

### Session Metrics

A "session" is a time-window-grouped cluster of usage events from a single user:

```typescript
SessionMetrics {
  totalSessions: number;          // Total sessions across all users
  avgDurationMs: number;          // Average session length
  avgEventsPerSession: number;    // Depth of engagement per session
}
```

**Session definition:** Events from the same user with < 30 minutes between them belong to the same session. A gap > 30 minutes starts a new session.

### Time to First Value (TTFV)

The most important activation metric. How long until a new user gets value?

```
TTFV = median(first_usage_event_timestamp - signup_timestamp) in hours
```

| TTFV | Assessment | Action |
|------|-----------|--------|
| < 1 hour | Excellent | Maintain current onboarding |
| 1-24 hours | Good | Minor friction in setup |
| 1-7 days | Concerning | Onboarding needs work |
| > 7 days | Critical | Users aren't finding value |

### Activation Rate

```
Activation Rate = (Users who performed at least 1 usage event) / (Total subscribers) × 100
```

A subscriber who never activates has a very high churn probability. This is the first signal in the behavioral model.

### DAU/MAU Ratio

```
DAU/MAU = (Daily Active Users) / (Monthly Active Users)

Benchmarks:
  > 0.5  — Exceptional (daily habit product)
  0.2-0.5 — Strong (regular use)
  0.1-0.2 — Moderate (periodic use)
  < 0.1  — Weak (monthly or less)
```

For a developer tools SaaS, 0.15-0.3 is healthy (not every day, but multiple times per week).

---

## Retention Metrics

### Point Retention (D1, D7, D30)

```sql
-- D7 retention
WITH signups AS (
  SELECT id, created_at FROM users
  WHERE created_at BETWEEN :start AND :end
),
d7_active AS (
  SELECT DISTINCT s.id
  FROM signups s
  INNER JOIN usage_events ue ON ue.user_id = s.id
  WHERE ue.timestamp >= s.created_at + INTERVAL '6 days'
    AND ue.timestamp < s.created_at + INTERVAL '8 days'
)
SELECT
  ROUND(COUNT(d7.id)::numeric / NULLIF(COUNT(s.id), 0) * 100, 1) AS d7_retention_pct
FROM signups s
LEFT JOIN d7_active d7 ON s.id = d7.id;
```

### Rolling Retention

Instead of a specific day, check if the user was active at ANY point after day N:

```
Rolling D7 = (Users active on day 7 OR later) / (Total cohort) × 100
```

Rolling retention is always >= point retention and gives a less noisy signal.

---

## Adoption Funnel

Track the user's deepening engagement:

```
Browse (view skills)
  └──► View Detail (view a specific skill)
        └──► Install (download/install a skill)
              └──► Repeat Use (use installed skill 3+ times)
```

### Funnel Metrics

```typescript
AdoptionFunnel {
  stages: Array<{
    name: string;           // "Browse", "View", "Install", "Repeat"
    count: number;          // Users who reached this stage
    dropoffPct: number;     // % lost from previous stage
  }>;
  overallConversionPct: number;  // Browse → Repeat %
}
```

### Drop-off Analysis

For each stage transition with > 10% drop-off, generate actionable recommendations:

| Transition | Drop-off > 50% | Recommendation |
|-----------|----------------|----------------|
| Browse → View | Many browsing, few clicking | Improve card previews, search relevance |
| View → Install | Looking but not installing | Reduce install friction, add social proof |
| Install → Repeat | Install once, never use again | Improve first-run experience, add tutorials |

---

## Power User Analysis

Identify your most engaged users (95th percentile by usage):

```typescript
PowerUserMetrics {
  count: number;                    // Number of power users
  percentOfTotal: number;           // % of total user base
  avgEventsPerUser: number;         // Usage intensity
  topEventTypes: string[];          // What they do most
  topCategories: string[];          // What areas they focus on
}
```

**Why it matters:** Power users are your advocates, your feature requesters, and your reference customers. Know who they are.

---

## Channel Comparison

Compare engagement across access channels:

| Channel | Metric | Web | CLI |
|---------|--------|-----|-----|
| Sessions | Count | X | Y |
| Active Days | Avg/user | X | Y |
| Events | Total | X | Y |
| Depth | Events/session | X | Y |

**Insight:** If CLI users are 3x more engaged than web users, invest more in CLI UX. If web users convert better, invest in web onboarding.

---

## Funnel Metrics (Signup → Value)

Track the full conversion funnel:

```typescript
FunnelMetrics {
  signupToSubscribe: {
    rate: number;              // % who subscribe
    avgDays: number;           // Avg days to convert
  };
  subscribeToActivate: {
    rate: number;              // % who activate
    avgHours: number;          // Avg hours to first use
  };
  installsPerSubscriber: number;  // Breadth of adoption
  errorRatePerSession: number;    // Friction indicator
}
```

### Key Conversion Points

| Stage | Healthy Rate | Action if Low |
|-------|-------------|---------------|
| Signup → Subscribe | > 5% | Improve pricing page, add testimonials |
| Subscribe → Activate | > 70% | Fix onboarding, send setup guide |
| Activate → Daily Use | > 30% | Add use cases, improve discoverability |

---

## Instrumentation Health

Track whether your analytics infrastructure is collecting data properly:

```typescript
InstrumentationHealth {
  status: 'healthy' | 'degraded' | 'missing';
  coverage: {
    cliTelemetry: boolean;     // CLI sending events?
    webTracking: boolean;      // Web sending events?
    webhookPipeline: boolean;  // Webhooks flowing?
  };
  lastEventAt: Date | null;    // Most recent event timestamp
  dataFreshness: string;       // "12 minutes ago"
}
```

**If `lastEventAt` is > 60 minutes ago**, your pipeline is broken. Surface this as a critical data quality insight.

---

## Engagement Scoring for Behavioral Model

The engagement analytics feed directly into the behavioral scoring model:

| Engagement Signal | Health Factor | Weight |
|-------------------|--------------|--------|
| Active days (30d) | Engagement (0-25) | Primary |
| Event volume (30d) | Engagement bonus | Secondary |
| Unique event types | Breadth (0-25) | Primary |
| Unique skills/features | Breadth bonus | Secondary |
| Days since last activity | Recency (0-25) | Primary |
| Session frequency | Engagement modifier | Tertiary |

This creates a feedback loop: engagement analytics → behavioral scores → churn predictions → interventions → improved engagement.

---

## Precomputed Aggregates

For dashboard performance, precompute daily aggregates via cron:

```sql
-- Daily aggregate table (sub-500ms dashboard queries)
INSERT INTO usage_stats_daily (user_id, date, total_skill_uses, unique_skills_used)
SELECT
  user_id,
  DATE(timestamp) AS date,
  COUNT(*) AS total_skill_uses,
  COUNT(DISTINCT skill_id) AS unique_skills_used
FROM usage_events
WHERE DATE(timestamp) = CURRENT_DATE - 1
GROUP BY user_id, DATE(timestamp)
ON CONFLICT (user_id, date)
DO UPDATE SET
  total_skill_uses = EXCLUDED.total_skill_uses,
  unique_skills_used = EXCLUDED.unique_skills_used;
```

Run daily at 3am UTC. This transforms slow aggregation queries into fast indexed lookups.
