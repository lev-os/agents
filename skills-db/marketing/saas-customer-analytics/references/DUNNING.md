# Dunning & Payment Recovery

> Failed payments cause 20-40% of all SaaS churn. Most of it is involuntary — the customer didn't intend to leave. Dunning is your highest-leverage retention mechanism.

## The Dunning Timeline

```
Day 0:  Payment fails → status = 'past_due' → dunning email #1 (immediate)
        │
Day 7:  First reminder email → "Your payment method needs updating"
        │
Day 14: Final warning email → "Access will be suspended in 7 days"
        │
Day 21: Grace period expires → status = 'cancelled' → access revoked
```

**Grace period = 21 days** from period end (NOT from payment failure date). This is critical — the period end is the contractual boundary, not the API event timestamp.

---

## Email Sequence

### Email 1: Payment Failed (Day 0)

```
Subject: Action needed: your payment didn't go through
Body: "We tried to charge your card ending in •••• 4242 for your $20/month
subscription but it was declined. Please update your payment method to
keep your access."
CTA: [Update Payment Method] → /settings/billing
```

### Email 2: Reminder (Day 7)

```
Subject: Reminder: please update your payment method
Body: "Your subscription payment is still outstanding. If we can't
process payment within 14 days, your access will be suspended."
CTA: [Update Payment Method] → /settings/billing
```

### Email 3: Final Warning (Day 14)

```
Subject: Final notice: your subscription will be cancelled in 7 days
Body: "This is your final reminder. If payment isn't resolved by [date],
your subscription will be cancelled and you'll lose access to premium features."
CTA: [Update Payment Method] → /settings/billing
```

---

## Organization (Team) Dunning

Teams have a **shorter grace period** because multiple users are affected:

```
Day 0:  Payment fails → notification to billing admin
Day 3:  First reminder → "Your team's access is at risk"
Day 7:  Suspended → team enters read-only mode
Day 30: Deactivated → all member access revoked
```

**Key difference:** Team dunning notifies the `org_owner` or `billing_email`, not individual members.

---

## Implementation Patterns

### Grace Period Check

```typescript
const GRACE_PERIOD_DAYS = 21;

function isWithinGracePeriod(subscription: Subscription): boolean {
  if (subscription.status !== 'past_due') return false;
  if (!subscription.currentPeriodEnd) return false;

  const graceEnd = new Date(subscription.currentPeriodEnd);
  graceEnd.setDate(graceEnd.getDate() + GRACE_PERIOD_DAYS);

  return new Date() <= graceEnd;
}
```

### Access Rule During Grace Period

```
if status === 'past_due' AND isWithinGracePeriod():
  → GRANT access (user is still "paying" in spirit)
  → Show banner: "Your payment needs attention"
else if status === 'past_due' AND NOT isWithinGracePeriod():
  → REVOKE access
  → Transition to 'cancelled'
```

### Dunning Cron Job

```typescript
// Runs daily at 9am UTC
async function processDunningReminders() {
  const pastDueSubscriptions = await db.select()
    .from(subscriptions)
    .where(eq(subscriptions.status, 'past_due'));

  for (const sub of pastDueSubscriptions) {
    const daysSincePeriodEnd = daysBetween(sub.currentPeriodEnd, new Date());

    if (daysSincePeriodEnd >= 7 && daysSincePeriodEnd < 14) {
      await sendDunningReminderEmail(sub.userId);
    } else if (daysSincePeriodEnd >= 14 && daysSincePeriodEnd < 21) {
      await sendFinalWarningEmail(sub.userId);
    } else if (daysSincePeriodEnd >= 21) {
      await cancelSubscription(sub);
    }
  }
}
```

### Email Deduplication

Webhook providers may retry delivery, triggering duplicate dunning emails. Protect against this:

```typescript
async function shouldSendDunningEmail(userId: string, templateKey: string): boolean {
  const recentEmail = await db.select()
    .from(emailJobs)
    .where(and(
      eq(emailJobs.userId, userId),
      eq(emailJobs.templateKey, templateKey),
      gte(emailJobs.createdAt, new Date(Date.now() - 24 * 60 * 60 * 1000))
    ))
    .limit(1);

  return recentEmail.length === 0; // Only send if no email in last 24h
}
```

---

## Recovery Metrics

Track dunning effectiveness:

| Metric | Formula | Target |
|--------|---------|--------|
| Recovery Rate | Recovered / Total Past Due × 100 | > 50% |
| Avg Recovery Time | Mean days from past_due to active | < 5 days |
| Email Open Rate | Opens / Sent × 100 | > 40% |
| Email Click Rate | Clicks / Opens × 100 | > 15% |
| Involuntary Churn Rate | Expired Grace / Total Churn × 100 | Track trend |

**Key insight:** If involuntary churn > 30% of total churn, your dunning sequence isn't aggressive enough. Consider: SMS, in-app banners, shortening the email interval.

---

## Payment Method Update Flow

The CTA in dunning emails should link to a frictionless update page:

1. User clicks "Update Payment Method" → `/settings/billing`
2. Show current payment status with clear error message
3. Pre-fill what you can (email, name)
4. After successful update, immediately retry the failed charge
5. If retry succeeds: transition `past_due` → `active`, send confirmation email
6. If retry fails: show specific error, suggest alternative payment method

---

## Multi-Provider Considerations

### Stripe
- Stripe has built-in Smart Retries (retries failed payments automatically)
- Supplement with your own dunning emails — Stripe's are generic
- Listen for `invoice.payment_failed` to trigger dunning

### PayPal
- PayPal sends its own payment failure notifications
- Listen for `BILLING.SUBSCRIPTION.SUSPENDED` to trigger dunning
- PayPal subscriptions may auto-cancel after 3 consecutive failures (`payment_failure_threshold: 3`)

### Coordination
- Track dunning state per provider to avoid duplicate emails
- Use the `paymentEvents` ledger to determine which provider's payment failed
- Don't send Stripe dunning emails for PayPal failures (and vice versa)

---

## Anti-Patterns

| Don't | Why | Do |
|-------|-----|-----|
| Start grace from failure date | Inconsistent with billing period | Start from `currentPeriodEnd` |
| Send dunning emails without dedup | Webhook retries → email spam | Check last 24h before sending |
| Cancel immediately on failure | Loses recoverable revenue | 21-day grace period |
| Use same grace for teams | Multiple users affected | Shorter grace (7 days to suspend) |
| Ignore involuntary churn | 20-40% of all churn | Track and optimize separately |
| Only email once | Users miss/ignore first email | 3-email sequence at 0/7/14 days |
