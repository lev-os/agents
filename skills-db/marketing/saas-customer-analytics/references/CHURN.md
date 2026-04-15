# Churn Prediction & Behavioral Scoring

> Behavior predicts churn 2-4 weeks before billing does. Build systems that watch engagement, not invoices.

## The Core Model

### Subscriber Behavior Profile

Every active subscriber gets a profile built from their last 30 days of activity:

```typescript
SubscriberBehaviorProfile {
  // Activity volume
  activeDays7: number;          // Days with any event in last 7d
  activeDays30: number;         // Days with any event in last 30d
  events7: number;              // Total events last 7d
  events14: number;             // Total events last 14d
  events30: number;             // Total events last 30d
  eventsPrev14: number;         // Events in the 14d BEFORE last 14d (trend baseline)

  // Workflow breadth
  uniqueEventTypes30: number;   // Distinct event types in 30d
  uniqueSkills30: number;       // Distinct features/products used in 30d

  // Activation
  activationEventCount: number; // Install/onboarding events ever
  activationLagDays: number;    // Days from signup to first activation (null = never)

  // Payment stress
  paymentFailures90: number;    // Failed payments in last 90d
  failedEvents30: number;       // Product errors in last 30d

  // Temporal
  daysSinceLastActivity: number;
  subscriptionAgeDays: number;
}
```

### Health Score Calculation (0-100)

Four factors, each scored 0-25:

**Engagement Score (0-25):**
```
activeDayScore = activeDays30:
  0 → 0, 1-3 → 10, 4-10 → 18, 11+ → 25

eventVolumeBonus:
  events30 > 50 → +5 (capped at 25 total)

engagementScore = min(25, activeDayScore + eventVolumeBonus)
```

**Breadth Score (0-25):**
```
typeScore = uniqueEventTypes30:
  0-1 → 3, 2-3 → 10, 4-6 → 18, 7+ → 25

skillBonus = uniqueSkills30 > 3 → +5

breadthScore = min(25, typeScore + skillBonus)
```

**Recency Score (0-25):**
```
daysSinceLastActivity:
  0-2   → 25  (active right now)
  3-7   → 20  (recent)
  8-14  → 12  (fading)
  15-30 → 5   (stale)
  31+   → 0   (gone)
```

**Payment Score (0-25):**
```
statusScore:
  active → 25
  past_due → 10
  cancelled → 0

failurePenalty = min(15, paymentFailures90 × 5)

paymentScore = max(0, statusScore - failurePenalty)
```

**Total:** `healthScore = engagement + breadth + recency + payment`

---

## Risk Level Classification

| Range | Level | Meaning | Appropriate Response |
|-------|-------|---------|---------------------|
| 70-100 | Low | Healthy, engaged | Monitor normally |
| 50-69 | Medium | Some signals weakening | Watch for continued decline |
| 30-49 | High | Multiple warning signals | Proactive outreach |
| 0-29 | Critical | Disengaged or failing | Immediate intervention |

---

## The 19 Behavioral Risk Drivers

Churn probability is computed via a logistic function where the input is a weighted sum of binary/continuous drivers:

### Activation Category

| Driver | Trigger | Impact Weight | Rationale |
|--------|---------|--------------|-----------|
| Not activated | activationEventCount = 0 AND subscriptionAge > 3d | High (0.3) | Never used product |
| Slow activation | activationLagDays > 7 | Medium (0.15) | Delayed value realization |
| Rapid activation | activationLagDays < 1 AND events30 > 10 | Negative (-0.15) | Strong start reduces risk |

### Engagement Category

| Driver | Trigger | Impact Weight | Rationale |
|--------|---------|--------------|-----------|
| No recent activity | activeDays7 = 0 | High (0.25) | Zero engagement last week |
| Low cadence | activeDays30 < 3 | Medium (0.15) | Barely using product |
| High cadence | activeDays30 > 15 | Negative (-0.2) | Power user = low risk |
| Low event volume | events30 < 5 | Medium (0.1) | Minimal usage |
| Narrow workflow | uniqueEventTypes30 <= 1 | Medium (0.1) | Single use case, fragile |
| Broad workflow | uniqueEventTypes30 >= 5 | Negative (-0.1) | Deep adoption |

### Recency Category

| Driver | Trigger | Impact Weight | Rationale |
|--------|---------|--------------|-----------|
| 30d inactive | daysSinceLastActivity > 30 | Critical (0.35) | Effectively gone |
| 14d inactive | daysSinceLastActivity > 14 | High (0.2) | Fading fast |
| 3d inactive | daysSinceLastActivity > 3 | Low (0.05) | Brief gap |
| Recent activity | daysSinceLastActivity <= 1 | Negative (-0.1) | Active now |

### Retention Category

| Driver | Trigger | Impact Weight | Rationale |
|--------|---------|--------------|-----------|
| Declining usage | usageTrendRatio < 0.5 | High (0.2) | Losing engagement |
| Improving usage | usageTrendRatio > 1.5 | Negative (-0.15) | Growing engagement |
| Single-skill | uniqueSkills30 <= 1 | Medium (0.1) | No stickiness |
| Multi-skill | uniqueSkills30 >= 3 | Negative (-0.1) | Cross-feature adoption |

### Payment Category

| Driver | Trigger | Impact Weight | Rationale |
|--------|---------|--------------|-----------|
| Payment failures | paymentFailures90 > 0 | High (0.25) | Involuntary churn signal |
| Product errors | failedEvents30 > 5 | Medium (0.1) | Frustration signal |

### Usage Trend Ratio

```
usageTrendRatio = events14 / eventsPrev14

Interpretation:
  > 1.5  → Improving (risk reducer)
  0.5-1.5 → Stable
  < 0.5  → Declining (risk amplifier)
  0      → Complete drop-off (if eventsPrev14 > 0)
```

---

## Churn Probability Formula

```
rawScore = SUM(driver.impact for each triggered driver)
churnProbability = 1 / (1 + exp(-rawScore))   // Logistic sigmoid

Monthly probability = churnProbability
Monthly probability % = churnProbability × 100
```

The logistic sigmoid maps the weighted sum to [0, 1]:
- Sum < 0 → probability < 50% (protective factors dominate)
- Sum = 0 → probability = 50%
- Sum > 0 → probability > 50% (risk factors dominate)

---

## Organization Scoring

Organizations have additional signals:

| Signal | Formula | Risk When |
|--------|---------|-----------|
| Member Activation Rate | activatedMembers / totalMembers | < 50% |
| Active Seat Ratio | activeMembers30 / maxSeats | < 30% |
| Seat Fill Ratio | memberCount / maxSeats | < 50% (over-provisioned) |
| Install Gap | Members without installation | > 50% of team |
| Owner Activity | Owner's days since last activity | > 14d |
| Expansion Potential | (maxSeats - memberCount) × seatPrice | Positive = upsell |

---

## Behavioral Forecast (12-Month Projection)

For each future month, project:
1. **New subscribers:** avg monthly signups × conversion rate
2. **New organizations:** avg monthly new org rate
3. **Churned individuals:** currentSubs × blended churn rate
4. **Churned organizations:** currentOrgs × org churn rate
5. **Resulting MRR:** (individuals × price) + SUM(org costs)

**Blended churn rate** combines:
- Observed historical churn (from cancellation data)
- Modeled churn (from behavioral scoring of current base)
- Weight: 50/50 blend

**Confidence intervals** widen with each future month:
```
confidence = 1 - (month × 0.05)  // 95% at month 1, 40% at month 12
lowBound = projected × confidence
highBound = projected × (2 - confidence)
```

---

## Sensitivity Analysis

Test which parameters most affect projections:

| Parameter | Delta | Measure |
|-----------|-------|---------|
| Churn rate | +1% / -1% | MRR impact at month 12 |
| Growth rate | +10% / -10% | MRR impact at month 12 |
| Conversion rate | +5% / -5% | Subscriber impact |
| Org churn | +2% / -2% | Org MRR impact |
| Price change | ±$5 | Revenue impact |

Report: `{ name, delta, mrrImpact, impactPct, rationale }`

---

## Derived Flags

These boolean flags simplify UI decisions:

| Flag | Definition |
|------|-----------|
| `hasActivation` | activationEventCount > 0 |
| `isDormant` | daysSinceLastActivity > 30 AND events30 = 0 |
| `isDeclining` | usageTrendRatio < 0.5 |
| `hasPaymentStress` | paymentFailures90 > 0 OR failedEvents30 > 10 |

---

## Data Collection Requirements

To power this model, you need these event streams:

1. **Usage events** (append-only): userId, eventType, skillId/featureId, timestamp, success, durationMs
2. **Payment events** (immutable): provider, eventType, eventId, userId, amount, payload
3. **Subscription state** (mutable): userId, provider, status, createdAt, cancelledAt
4. **User profile**: email, createdAt (for activation lag)

The behavioral model is only as good as the events you collect. No events = no prediction.
