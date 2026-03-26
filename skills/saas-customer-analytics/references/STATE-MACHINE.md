# Subscription State Machine

> The subscription state machine is the most bug-prone part of any SaaS. Every edge case you don't handle is a customer who can't access what they paid for, or one who gets free access forever.

## States

```
┌──────────┐   checkout    ┌──────────┐
│   none   │──────────────►│  active   │◄─────────────────────┐
└──────────┘               └──────────┘                       │
                             │      │                          │
                    payment  │      │ user cancels             │ payment
                    fails    │      │                          │ recovered
                             ▼      ▼                          │
                         ┌──────────┐   grace     ┌──────────┐│
                         │ past_due │──expires────►│cancelled ││
                         └──────────┘              └──────────┘│
                             │                                  │
                             └──────────────────────────────────┘

                         ┌───────────────┐
                         │paused_for_org │  (individual sub paused
                         └───────────────┘   when user joins org)
```

## State Definitions

| State | Meaning | Access? | Billing? |
|-------|---------|---------|----------|
| `none` | Never subscribed | No | No |
| `active` | Current, paid | Yes | Active |
| `past_due` | Payment failed, grace period | Yes (if within grace) | Retrying |
| `cancelled` | Explicitly cancelled or grace expired | Yes (until period end) | Stopped |
| `paused_for_org` | Individual sub paused by org membership | Via org | Individual paused |

## Access Rules

The access check is the most critical function in your SaaS. Get it wrong and you either lose revenue (free access) or lose customers (blocked access).

```typescript
function canAccessPremiumContent(user: User): boolean {
  // Path 1: Individual subscription
  const sub = pickBestSubscription(user.subscriptions);
  if (sub) {
    if (sub.status === 'active') return true;
    if (sub.status === 'past_due' && isWithinGracePeriod(sub)) return true;
    if (sub.status === 'cancelled' && isPaidThrough(sub)) return true;
  }

  // Path 2: Organization membership
  const orgMembership = getActiveOrgMembership(user);
  if (orgMembership) {
    const org = orgMembership.organization;
    if (['active', 'past_due'].includes(org.subscriptionStatus)) {
      if (orgMembership.role !== 'viewer') return true;
    }
  }

  return false;
}
```

### Paid-Through Cancellations

When a user cancels mid-period, they keep access until the period ends:

```typescript
function isPaidThrough(sub: Subscription): boolean {
  if (sub.status !== 'cancelled') return false;
  if (!sub.currentPeriodEnd) return false;
  return new Date() <= new Date(sub.currentPeriodEnd);
}
```

---

## Best Subscription Selection

Users may have multiple subscriptions (e.g., switched from Stripe to PayPal). Always pick the best one:

```typescript
function pickBestSubscription(subscriptions: Subscription[]): Subscription | null {
  if (subscriptions.length === 0) return null;

  return subscriptions.reduce((best, current) => {
    const bestScore = scoreSubscription(best);
    const currentScore = scoreSubscription(current);
    if (currentScore > bestScore) return current;
    if (currentScore === bestScore) {
      // Tie-break: most recently updated wins
      return current.updatedAt > best.updatedAt ? current : best;
    }
    return best;
  });
}

function scoreSubscription(sub: Subscription): number {
  switch (sub.status) {
    case 'active': return 1000;
    case 'past_due': return isWithinGracePeriod(sub) ? 750 : 100;
    case 'cancelled': return isPaidThrough(sub) ? 500 : 50;
    case 'paused_for_org': return 250;
    default: return 0;
  }
}
```

---

## State Transitions

### Valid Transitions

| From | To | Trigger | Side Effects |
|------|----|---------|-------------|
| none → active | Checkout complete | Grant access, send welcome email |
| active → past_due | Payment fails | Start dunning sequence |
| past_due → active | Payment recovered | Stop dunning, send confirmation |
| past_due → cancelled | Grace expires | Revoke access, send goodbye email |
| active → cancelled | User cancels | Set `cancelledAt`, access until period end |
| cancelled → active | User resubscribes | New subscription, grant access |
| active → paused_for_org | User joins org | Pause individual billing |
| paused_for_org → active | User leaves org | Resume individual billing |

### Invalid Transitions (Guard Against)

| Transition | Why It's Wrong |
|-----------|---------------|
| cancelled → past_due | Can't fail a payment on a cancelled sub |
| none → past_due | Can't fail a payment that never existed |
| paused_for_org → cancelled | Should resume, not cancel |

### Event Ordering Protection

Webhooks arrive out of order. A `subscription.deleted` may arrive before `subscription.updated`:

```typescript
// Only apply if this event is newer than what we have
await db.update(subscriptions)
  .set({
    status: newStatus,
    lastEventAt: eventTimestamp,
    updatedAt: new Date(),
  })
  .where(and(
    eq(subscriptions.id, subId),
    or(
      isNull(subscriptions.lastEventAt),
      lt(subscriptions.lastEventAt, eventTimestamp)
    )
  ));
```

---

## Multi-Provider Scenarios

A user might have both a Stripe and PayPal subscription. Handle this:

1. **Both active:** Use the one updated most recently (prefer the "primary" provider)
2. **One active, one cancelled:** Use the active one
3. **Both past_due:** Use the one with more grace period remaining
4. **Switching providers:** User cancels Stripe, subscribes via PayPal. Both records exist.

The `pickBestSubscription()` function handles all of these by scoring and tie-breaking.

---

## Organization Access Model

Organizations add a second access path independent of individual subscriptions:

```
User Access = Individual Subscription Access OR Organization Membership Access
```

**Organization rules:**
- Org subscription must be `active` or `past_due`
- Member role must NOT be `viewer` (viewers get limited access)
- If user has BOTH individual and org access, the individual sub is `paused_for_org`

```typescript
function getEffectiveAccess(user: User): AccessResult {
  const individualAccess = checkIndividualAccess(user);
  const orgAccess = checkOrgAccess(user);

  return {
    hasAccess: individualAccess.granted || orgAccess.granted,
    source: orgAccess.granted ? 'organization' : 'individual',
    subscription: individualAccess.subscription,
    organization: orgAccess.organization,
  };
}
```

---

## Provider Count Queries

For analytics, count active subscribers by provider:

```sql
-- Individual subscribers by provider
SELECT
  provider,
  COUNT(*) AS count
FROM subscriptions
WHERE status IN ('active', 'past_due')
  AND provider IN ('stripe', 'paypal')
GROUP BY provider;

-- Organization subscribers by provider
SELECT
  CASE
    WHEN stripe_subscription_id IS NOT NULL THEN 'stripe'
    WHEN paypal_subscription_id IS NOT NULL THEN 'paypal'
  END AS provider,
  COUNT(*) AS count
FROM organizations
WHERE subscription_status IN ('active', 'past_due')
GROUP BY provider;
```

---

## Testing the State Machine

The state machine must be exhaustively tested. Key test cases:

```
✓ Active subscription grants access
✓ past_due within grace grants access
✓ past_due outside grace denies access
✓ Cancelled with future period end grants access
✓ Cancelled with past period end denies access
✓ paused_for_org denies individual access
✓ Org membership grants access when org active
✓ Org membership denies access when org cancelled
✓ Stale webhook doesn't overwrite newer status
✓ Multiple subscriptions: best one wins
✓ Provider switch: old cancelled + new active = access
✓ Viewer role in org gets limited access
```

---

## Cache Invalidation

Subscription changes must immediately invalidate user access caches:

```typescript
// After any subscription status change:
await invalidateUserCache(userId);
await invalidateSubscriptionCache(subscriptionId);

// If org subscription changes:
for (const member of orgMembers) {
  await invalidateUserCache(member.userId);
}
```

Without this, users may see stale access state for the duration of the cache TTL.
