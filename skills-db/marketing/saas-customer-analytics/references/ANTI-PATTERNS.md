# Anti-Patterns & Failure Modes

> Every anti-pattern here was discovered the hard way. Learn from the mistakes so you don't repeat them.

## Data Integrity Anti-Patterns

### 1. Calculating Fees from Mutable Subscriptions Table

**Wrong:**
```typescript
// Counts current subscriptions, applies fee rate
const subs = await db.select().from(subscriptions).where(eq(status, 'active'));
const fees = subs.length * estimatedFeePerTransaction;
```

**Why it fails:** The subscriptions table tracks *current state*. Users who subscribed and cancelled within the period are invisible. Actual payment amounts may differ from subscription price (prorations, refunds).

**Right:** Query the immutable `paymentEvents` ledger for `invoice.payment_succeeded` and `PAYMENT.SALE.COMPLETED` events. These record what *actually happened*.

### 2. Including Test Data in Analytics

**Wrong:** Computing MRR, churn, or conversion rates without filtering test accounts.

**Why it fails:** Even one test account that creates/cancels subscriptions repeatedly will massively inflate churn rate and skew MRR.

**Right:** Filter at EVERY query:
- Individual: `email NOT LIKE '%@test.yourdomain.com'`
- Organizations: `name NOT LIKE 'E2E Team%'`
- Subscriptions: `external_id NOT LIKE 'sub_test_%'`

### 3. Treating past_due as Churned

**Wrong:**
```typescript
const churned = await db.select().from(subscriptions)
  .where(or(eq(status, 'cancelled'), eq(status, 'past_due')));
```

**Why it fails:** `past_due` means the payment failed but the subscriber is in a grace period. Many will recover. Counting them as churned inflates your churn rate and triggers false alarms.

**Right:** Count `past_due` as active for MRR purposes. Monitor separately as a payment stress signal in the behavioral scoring model.

### 4. Not Handling Event Ordering

**Wrong:** Blindly applying webhook updates to subscription status.

**Why it fails:** Webhooks arrive out of order. A `subscription.deleted` event may arrive before a `subscription.updated` event from the same second. Applying them in arrival order produces incorrect state.

**Right:** Use a `last_event_at` column and only apply updates where the new event is newer:
```sql
UPDATE subscriptions SET status = $1, last_event_at = $2
WHERE id = $3 AND (last_event_at IS NULL OR last_event_at < $2);
```

---

## Modeling Anti-Patterns

### 5. Single-Point Revenue Projections

**Wrong:** "Your MRR will be $5,000 in 12 months."

**Why it fails:** Compound growth/decay amplifies small input errors. A 1% error in churn rate becomes 12% at month 12. The single number gives false confidence.

**Right:** Monte Carlo simulation with P10/P50/P90 ranges. "Your MRR will likely be between $3,200 and $7,100, with $4,800 being the most likely outcome."

### 6. Using ML/AI for Insight Generation

**Wrong:** Training a neural network to detect revenue anomalies.

**Why it fails:** For early-stage SaaS (< 10,000 subscribers), you don't have enough data for ML. Rule-based heuristics + Z-score statistics are:
- Easier to debug ("why did it alert?")
- Faster to implement
- More transparent to stakeholders
- Sufficient for the data volumes involved

**Right:** Start with deterministic rules. Graduate to ML only when you have 12+ months of data AND the rules are demonstrably insufficient.

### 7. Ignoring Contribution Margin in Break-Even

**Wrong:** `breakEvenSubs = fixedCosts / subscriptionPrice`

**Why it fails:** Each subscriber costs you payment processing fees. If your subscription is $5/month and fees are $0.79/transaction, your contribution margin is only $4.21. Break-even requires more subscribers than the naive calculation suggests.

**Right:** `breakEvenSubs = fixedCosts / (subscriptionPrice - avgPaymentFee)`

And check: if `contributionMargin <= 0`, break-even is **mathematically unreachable** through subscriber growth alone. Surface this as a critical insight.

### 8. Predicting Churn from Billing Events Only

**Wrong:** "User's payment failed twice → high churn risk."

**Why it fails:** Payment failure is a lagging indicator. By the time payments fail, the user may have already mentally churned weeks ago. You're detecting involuntary churn but missing voluntary churn entirely.

**Right:** Behavioral signals predict churn 2-4 weeks earlier:
- Days since last activity (recency)
- Declining usage trend (engagement)
- Narrow feature adoption (breadth)
- Never activated (activation)

Payment signals are one of FIVE categories in the behavioral model, not the only one.

---

## Architecture Anti-Patterns

### 9. Failing the Whole Dashboard on One Bad Query

**Wrong:**
```typescript
const [mrr, churn, fees, health] = await Promise.all([
  calculateMrr(),
  calculateChurn(),
  calculateFees(),
  calculateHealth(),
]);
```

**Why it fails:** If ANY of these throws, the entire `Promise.all` rejects. Admin sees a blank page.

**Right:**
```typescript
const [mrr, churn, fees, health] = await Promise.allSettled([...]);
// Each metric is independent — show what you have, mark what failed
```

### 10. Aggressive Caching of Subscriber Counts

**Wrong:** Caching MRR for 1 hour to reduce DB load.

**Why it fails:** If a subscriber joins or churns, the admin dashboard shows stale MRR for up to an hour. For an early-stage SaaS where each subscriber matters, this creates confusion ("I just signed up a user but MRR didn't change").

**Right:** 60-second TTL for the summary widget. The DB can handle one aggregation query per minute. Use TanStack Query's `staleTime` to prevent excessive client-side refetching.

### 11. Not Rate-Limiting Compute-Heavy Endpoints

**Wrong:** Letting admins run Monte Carlo simulations with 10,000 iterations without throttling.

**Why it fails:** Monte Carlo is CPU-bound with no I/O yields. It blocks the Node.js event loop for hundreds of milliseconds. Multiple concurrent requests = server brownout.

**Right:** Rate-limit to 1 request per 5 seconds per admin. Cap iterations at 10,000. Cap months at 120.

### 12. Storing Analytics in the Same DB Transaction as Webhooks

**Wrong:**
```typescript
await db.transaction(async (tx) => {
  await tx.insert(paymentEvents).values(event);
  await tx.update(subscriptions).set({ status: 'active' });
  await updateDailyAnalytics(tx);  // Expensive aggregation
});
```

**Why it fails:** The analytics computation holds the transaction open. If it's slow, the webhook handler times out. Stripe/PayPal retry. You get duplicate processing attempts.

**Right:** Insert the event and update subscription status in one fast transaction. Run analytics as a separate post-processing step (or via cron).

---

## Behavioral Scoring Anti-Patterns

### 13. Scoring Users with No Usage Data

**Wrong:** Computing health scores for users who signed up but have zero usage events.

**Why it fails:** A user who signed up yesterday with no events is in a completely different state than a user who's been subscribed for 30 days with no events. The former needs activation nudging; the latter is a critical churn risk.

**Right:** Gate health scoring on `subscriptionAgeDays > 3`. For users < 3 days old, use a separate "activation tracking" path instead of the full behavioral model.

### 14. Equal Weighting of All Behavioral Factors

**Wrong:** Treating a payment failure the same as a slightly below-average engagement day.

**Why it fails:** Not all signals are equal predictors. Recency of last activity is the strongest single predictor of churn. Payment failures are a strong secondary signal. Event volume is useful but noisy.

**Right:** Use the weighted driver model with empirically calibrated weights. The 19-driver model assigns impact weights from -0.2 (protective) to +0.35 (high risk) based on predictive power.

### 15. Not Accounting for Usage Trend Direction

**Wrong:** "User had 10 events in the last 30 days → medium engagement."

**Why it fails:** 10 events that were all in the first week (declining) is very different from 10 events that were all in the last week (improving). Same number, opposite trajectory.

**Right:** Compare `events14` vs `eventsPrev14` (usage trend ratio). A ratio < 0.5 = declining, > 1.5 = improving. This directional signal is more predictive than absolute volume.

---

## Dashboard Anti-Patterns

### 16. Showing Raw Numbers Without Context

**Wrong:** "MRR: $1,200"

**Why it fails:** Is $1,200 good or bad? Up or down? The number alone doesn't inform decisions.

**Right:** "MRR: $1,200 (+8.1% MoM)" with a sparkline showing the 30-day trend and a trend indicator (green up arrow).

### 17. Alert Fatigue from Non-Dismissible Insights

**Wrong:** Showing the same "Conversion rate is low" insight every page load forever.

**Why it fails:** Admin learns to ignore all insights. Critical alerts get buried.

**Right:** Implement dismissal (7-day snooze). Track dismissals in DB with expiry. Auto-expire stale insights. Use severity levels so critical alerts stand out.

### 18. Monte Carlo Fan Charts Without Explanation

**Wrong:** Showing P10/P50/P90 bands without explaining what they mean.

**Why it fails:** Most people don't intuitively understand probability distributions. They'll focus on P90 (best case) and be disappointed.

**Right:** Label bands clearly: "Pessimistic (10th percentile)", "Most likely (median)", "Optimistic (90th percentile)". Add a survival probability number: "78% chance of surviving 12 months."
