# Automated Retention Interventions

> The gap between detecting churn risk and actually preventing churn is the intervention engine.

## Architecture

```
Behavioral Snapshot
    │
    ▼
Intervention Rules (conditions + thresholds)
    │
    ▼
Threshold Evaluation
    │
    ├── Static: value > threshold
    ├── Adaptive Quantile: value <= Nth percentile of population
    ├── Adaptive Z-score: value deviates by N standard deviations
    └── Bayes Rate: rate below baseline at confidence level
    │
    ▼
Action Execution
    │
    ├── In-app Notification
    ├── Email (setup guide, rescue campaign)
    ├── Churn Prediction Record
    └── Admin Log Entry
    │
    ▼
Outcome Tracking (did the intervention work?)
```

---

## Threshold Types

### Static Threshold

Simplest: compare a metric against a fixed number.

```typescript
{
  kind: 'static',
  operator: 'gt' | 'gte' | 'lt' | 'lte',
  value: number
}
```

**Example:** `churnProbability > 0.7` → trigger rescue email.

**When to use:** When you have a known, calibrated threshold from experience.

### Adaptive Quantile Threshold

Compare against the population distribution. Self-adjusting as your user base changes.

```typescript
{
  kind: 'adaptive_quantile',
  operator: 'gte' | 'lte',
  quantile: number,       // e.g., 0.1 for 10th percentile
  floor?: number,         // Minimum threshold value
  ceiling?: number        // Maximum threshold value
}
```

**Example:** `healthScore <= 10th percentile` → high risk intervention.

**When to use:** When the absolute threshold should shift with your user base quality.

### Adaptive Z-Score Threshold

Statistical outlier detection relative to population.

```typescript
{
  kind: 'adaptive_zscore',
  operator: 'gte' | 'lte',
  zScore: number,         // e.g., 2.0 for 2 standard deviations
  floor?: number,
  ceiling?: number
}
```

**Example:** `engagementDrop Z >= 2.5` → unusual disengagement.

**When to use:** When you want to detect sudden changes relative to normal behavior.

### Bayes Rate Threshold

Confidence-bounded rate comparison. Only triggers when there's enough data to be confident.

```typescript
{
  kind: 'bayes_rate_below_baseline',
  successMetricKey: string,    // e.g., 'activatedMembers'
  trialsMetricKey: string,     // e.g., 'totalMembers'
  margin: number,              // How far below baseline
  confidence: number,          // e.g., 0.95
  minimumTrials?: number       // Minimum sample size
}
```

**Example:** Organization activation rate below 50% baseline at 95% confidence with minimum 5 members.

**When to use:** When small sample sizes could cause false positives.

---

## Action Types

### Notification Action

In-app notification displayed in the admin dashboard or user's notification center.

```typescript
{
  type: 'notification',
  recipient: 'user' | 'org_owner',
  title: string,
  body: string,
  actionUrl?: string
}
```

**Best for:** Medium risk, engagement decline. Non-intrusive.

### Email Action

Transactional email with specific template.

```typescript
{
  type: 'email',
  templateKey: 'setup_guide' | 'org_activation_rescue' | ...,
  recipient: 'user' | 'org_owner',
  respectProductUpdates?: boolean  // Check email preferences
}
```

**Templates:**
- **Setup Guide**: For users who haven't activated within N days. Contains installation instructions, quick-start guide.
- **Rescue Campaign**: For declining users. Contains value reminders, feature highlights, support offer.

**Important:** Check `userEmailPreferences` before sending. Respect opt-outs.

### Churn Prediction Action

Record the prediction for admin review. Not directly user-facing.

```typescript
{
  type: 'churn_prediction',
  recommendedActions: string[]
}
```

Writes to `churnPredictions` table with risk score, factors, and recommended actions.

### Log Action

Simple audit trail entry.

```typescript
{
  type: 'log',
  label: string
}
```

---

## Intervention Rules

### Rule Structure

```typescript
InterventionRule {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  subjectType: 'user' | 'organization';
  conditions: InterventionCondition[];        // AND conditions
  threshold: InterventionThresholdSpec;
  actions: InterventionAction[];
  cooldownHours: number;                      // Min hours between triggers for same subject
  priority: number;                           // Higher = runs first
}
```

### Condition Evaluation

```typescript
InterventionCondition {
  metricKey: string;        // Path into behavioral profile
  operator: 'eq' | 'ne' | 'gt' | 'gte' | 'lt' | 'lte' | 'in';
  value: unknown;
}
```

All conditions must be true (AND logic). If ANY condition fails, the rule doesn't fire.

### Example Rules

**Rule: New User Not Activated**
```typescript
{
  name: 'new_user_activation_nudge',
  subjectType: 'user',
  conditions: [
    { metricKey: 'hasActivation', operator: 'eq', value: false },
    { metricKey: 'subscriptionAgeDays', operator: 'gte', value: 3 },
    { metricKey: 'subscriptionAgeDays', operator: 'lte', value: 14 },
  ],
  threshold: { kind: 'static', operator: 'lte', value: 0 },  // activationEventCount = 0
  actions: [
    { type: 'email', templateKey: 'setup_guide', recipient: 'user' },
    { type: 'log', label: 'activation_nudge_sent' },
  ],
  cooldownHours: 168,  // Once per week max
}
```

**Rule: High Churn Risk User**
```typescript
{
  name: 'high_churn_rescue',
  subjectType: 'user',
  conditions: [
    { metricKey: 'churnRisk', operator: 'in', value: ['high', 'critical'] },
  ],
  threshold: { kind: 'static', operator: 'gte', value: 0.6 },  // churnProbability >= 60%
  actions: [
    { type: 'churn_prediction', recommendedActions: ['personal outreach', 'feature highlight'] },
    { type: 'notification', recipient: 'user', title: 'We miss you!', body: '...' },
  ],
  cooldownHours: 336,  // Every 2 weeks max
}
```

**Rule: Organization Low Activation (Bayes)**
```typescript
{
  name: 'org_low_activation_bayes',
  subjectType: 'organization',
  conditions: [
    { metricKey: 'memberCount', operator: 'gte', value: 5 },
  ],
  threshold: {
    kind: 'bayes_rate_below_baseline',
    successMetricKey: 'activatedMembers',
    trialsMetricKey: 'memberCount',
    margin: 0.2,
    confidence: 0.95,
    minimumTrials: 5,
  },
  actions: [
    { type: 'email', templateKey: 'org_activation_rescue', recipient: 'org_owner' },
  ],
  cooldownHours: 336,
}
```

---

## Execution Tracking

### Execution Record

```sql
CREATE TABLE intervention_executions (
  id UUID PRIMARY KEY,
  rule_id TEXT NOT NULL,
  subject_type TEXT NOT NULL,
  subject_id TEXT NOT NULL,           -- userId or orgId
  actions_taken JSONB NOT NULL,
  metrics_snapshot JSONB,             -- Behavioral profile at time of execution
  executed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Outcome Tracking

```sql
CREATE TABLE intervention_outcomes (
  id UUID PRIMARY KEY,
  execution_id UUID REFERENCES intervention_executions(id),
  outcome TEXT NOT NULL,              -- 'retained' | 'churned' | 'upgraded' | 'no_change'
  measured_at TIMESTAMPTZ,
  days_after_intervention INTEGER
);
```

Track what happened 7/14/30 days after intervention to measure effectiveness.

---

## Cooldown Logic

Prevent intervention fatigue:

```typescript
async function shouldExecute(ruleId: string, subjectId: string, cooldownHours: number): boolean {
  const lastExecution = await db
    .select({ executedAt: interventionExecutions.executedAt })
    .from(interventionExecutions)
    .where(and(
      eq(interventionExecutions.ruleId, ruleId),
      eq(interventionExecutions.subjectId, subjectId),
    ))
    .orderBy(desc(interventionExecutions.executedAt))
    .limit(1);

  if (!lastExecution[0]) return true;

  const hoursSince = (Date.now() - lastExecution[0].executedAt.getTime()) / (1000 * 60 * 60);
  return hoursSince >= cooldownHours;
}
```

---

## Intervention Effectiveness Metrics

After running interventions for 30+ days, measure:

| Metric | Formula | Target |
|--------|---------|--------|
| Save rate | Retained after intervention / Total interventions | > 30% |
| False positive rate | Interventions on users who weren't going to churn | < 50% |
| Annoyance rate | Users who unsubscribe from notifications after intervention | < 5% |
| Time to impact | Days between intervention and re-engagement | < 7d |

---

## Implementation Order

1. **Start with static thresholds** — simplest, most debuggable
2. **Add email actions** — highest impact retention tool
3. **Add cooldown logic** — prevent spam
4. **Add execution tracking** — know what you did
5. **Add adaptive quantile thresholds** — self-calibrating
6. **Add outcome tracking** — measure effectiveness
7. **Add Bayes thresholds** — for organization-level rules with small samples
8. **Iterate on rules** — tune based on outcome data
