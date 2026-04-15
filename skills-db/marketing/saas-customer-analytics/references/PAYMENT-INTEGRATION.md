# Stripe & PayPal Integration Patterns

> Payment integrations are the bedrock of SaaS analytics. Get the webhook pipeline right and everything downstream works. Get it wrong and your MRR is a lie.

## The Immutable Ledger Pattern

### Architecture

```
Stripe/PayPal Webhook → Verify Signature → Insert into paymentEvents → Process Side Effects
                                                    │
                                                    ├── Update subscription status
                                                    ├── Invalidate user cache
                                                    └── Mark event as processed
```

**Key principle:** Record the event FIRST (immutable), THEN apply side effects. If side effects fail, the event is still recorded and can be retried.

### Schema

```sql
CREATE TABLE payment_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL,          -- 'stripe' | 'paypal'
  event_type TEXT NOT NULL,        -- 'invoice.payment_succeeded', 'BILLING.SUBSCRIPTION.ACTIVATED', etc.
  event_id TEXT NOT NULL,          -- Provider's unique event ID
  user_id UUID REFERENCES users(id),
  payload JSONB NOT NULL,          -- Full webhook body (never discard)
  processed_at TIMESTAMPTZ,        -- NULL until side effects complete
  reconciled_at TIMESTAMPTZ,       -- Distributed lock for retry
  retry_count INTEGER DEFAULT 0,
  last_error TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(provider, event_id)       -- Idempotency guarantee
);

CREATE INDEX idx_payment_events_unprocessed
  ON payment_events (created_at)
  WHERE processed_at IS NULL;

CREATE INDEX idx_payment_events_user
  ON payment_events (user_id, created_at);
```

### Idempotency

The `UNIQUE(provider, event_id)` constraint prevents duplicate processing. Stripe/PayPal may deliver the same webhook multiple times. The insert-or-skip pattern handles this:

```typescript
try {
  await db.insert(paymentEvents).values({
    provider: 'stripe',
    eventId: event.id,
    eventType: event.type,
    payload: event,
    userId: resolvedUserId,
  });
} catch (e) {
  if (isDuplicateKeyError(e)) {
    return; // Already processed — safe to ignore
  }
  throw e;
}
```

---

## Stripe Integration

### Webhook Events to Handle

| Event | Action | Analytics Impact |
|-------|--------|-----------------|
| `checkout.session.completed` | Create subscription record | New MRR |
| `customer.subscription.updated` | Update status | Status transition |
| `customer.subscription.deleted` | Mark cancelled | Churned MRR |
| `invoice.payment_succeeded` | Record payment | Revenue, fee data |
| `invoice.payment_failed` | Record failure | Payment stress signal |
| `invoice.payment_action_required` | Flag for attention | Intervention trigger |

### Signature Verification

```typescript
const event = stripe.webhooks.constructEvent(
  body,
  request.headers.get('stripe-signature')!,
  process.env.STRIPE_WEBHOOK_SECRET!
);
```

Always verify. Never skip in production.

### Analytics Data Extraction

**From Stripe API directly (for real-time dashboard):**
```typescript
// Balance
const balance = await stripe.balance.retrieve();
const available = balance.available.find(b => b.currency === 'usd')?.amount ?? 0;

// Subscription stats (paginate — may exceed 100)
let subscriptions = [];
for await (const sub of stripe.subscriptions.list({ limit: 100, status: 'all' })) {
  subscriptions.push(sub);
  if (subscriptions.length >= 10_000) break; // Safety limit
}

// Invoice stats
const invoices = await stripe.invoices.list({ limit: 100 });
const paid = invoices.data.filter(i => i.status === 'paid');
const failed = invoices.data.filter(i => i.status === 'uncollectible');

// Net revenue (balance transactions)
const txns = await stripe.balanceTransactions.list({
  created: { gte: thirtyDaysAgoUnix },
  limit: 100,
});
let grossRevenue = 0, totalFees = 0, refunds = 0;
for (const txn of txns.data) {
  if (txn.type === 'charge') { grossRevenue += txn.amount; totalFees += txn.fee; }
  if (txn.type === 'refund') { refunds += Math.abs(txn.amount); }
}
```

### Fee Calculation

```
Stripe Domestic: 2.9% + $0.30
Stripe International: 2.9% + 1.5% + $0.30

For a $20 subscription:
  Domestic fee: $0.58 + $0.30 = $0.88 (4.4% effective)
  International fee: $0.88 + $0.30 = $1.18 (5.9% effective)
```

---

## PayPal Integration

### Webhook Events to Handle

| Event | Action | Analytics Impact |
|-------|--------|-----------------|
| `BILLING.SUBSCRIPTION.CREATED` | Record pending | —  |
| `BILLING.SUBSCRIPTION.ACTIVATED` | Create active subscription | New MRR |
| `BILLING.SUBSCRIPTION.CANCELLED` | Mark cancelled | Churned MRR |
| `BILLING.SUBSCRIPTION.SUSPENDED` | Mark past_due | At-risk signal |
| `PAYMENT.SALE.COMPLETED` | Record payment | Revenue, fee data |

### Signature Verification

PayPal uses a different verification approach — call their API to verify:

```typescript
const verifyResponse = await fetch(
  `${PAYPAL_API}/v1/notifications/verify-webhook-signature`,
  {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auth_algo: headers['paypal-auth-algo'],
      cert_url: headers['paypal-cert-url'],
      transmission_id: headers['paypal-transmission-id'],
      transmission_sig: headers['paypal-transmission-sig'],
      transmission_time: headers['paypal-transmission-time'],
      webhook_id: PAYPAL_WEBHOOK_ID,
      webhook_event: event,
    }),
  }
);
```

### PayPal Transaction Codes

| Code Range | Meaning | Analytics Category |
|-----------|---------|-------------------|
| T00xx | Payment/Sale | Revenue |
| T03xx | Subscription payment | Recurring revenue |
| T11xx | Refund | Revenue reduction |
| T12xx | Dispute/Chargeback | Revenue reduction + risk |

### Fee Calculation

```
PayPal Standard: 2.99% + $0.49

For a $20 subscription:
  Fee: $0.598 + $0.49 = $1.088 (5.44% effective)
```

PayPal is more expensive per transaction than domestic Stripe.

---

## Blended Fee Rate

```typescript
function calculateEffectiveFee(
  stripeRatio: number,
  paypalRatio: number,
  internationalRatio: number = 0.1
): number {
  const stripeDomesticFee = subscriptionPrice * 0.029 + 0.30;
  const stripeInternationalFee = subscriptionPrice * 0.044 + 0.30;
  const stripeFee = stripeDomesticFee * (1 - internationalRatio)
                  + stripeInternationalFee * internationalRatio;
  const paypalFee = subscriptionPrice * 0.0299 + 0.49;

  return (stripeRatio * stripeFee) + (paypalRatio * paypalFee);
}
```

**Default ratios when insufficient data:**
- Stripe: 70%, PayPal: 30%
- International: 10%

Derive actual ratios from the `subscriptions` table (`COUNT GROUP BY provider`).

---

## Webhook Reconciliation

### Problem
Webhooks can fail (network error, app crash, timeout). Without reconciliation, you lose payment events.

### Solution: Cron-Based Recovery

```
Every 5 minutes:
  SELECT * FROM payment_events
  WHERE processed_at IS NULL
  AND created_at < NOW() - INTERVAL '5 minutes'
  AND retry_count < 5
  ORDER BY created_at ASC
  LIMIT 50;

For each unprocessed event:
  1. Acquire distributed lock (SET reconciled_at = NOW() WHERE reconciled_at IS NULL)
  2. Re-process the event (same logic as webhook handler)
  3. On success: SET processed_at = NOW()
  4. On failure: INCREMENT retry_count, SET last_error, RELEASE lock
  5. If retry_count >= 5: Alert admin
```

### Distributed Locking

The `reconciled_at` column serves as a lease:
```sql
UPDATE payment_events
SET reconciled_at = NOW()
WHERE id = $1 AND reconciled_at IS NULL
RETURNING *;
```

If another worker already claimed it, the `WHERE reconciled_at IS NULL` returns nothing. No race condition.

---

## Event Ordering Protection

### Problem
Stripe may deliver `subscription.deleted` before `subscription.updated` due to network timing.

### Solution: `lastEventAt` Column

```sql
-- On subscription table:
last_event_at TIMESTAMPTZ;

-- In webhook handler:
UPDATE subscriptions
SET status = $newStatus, last_event_at = $eventTimestamp
WHERE id = $subId AND (last_event_at IS NULL OR last_event_at < $eventTimestamp);
```

If the event is older than what we've already processed, the `WHERE` clause prevents the stale update.

---

## Team/Organization Billing

Organizations have seat-based pricing:

```typescript
function calculateMonthlyCost(maxSeats: number): number {
  // Example: $300 base (3 seats) + $100 per additional seat
  const BASE_PRICE = 300;
  const BASE_SEATS = 3;
  const PER_SEAT_PRICE = 100;
  const additionalSeats = Math.max(0, maxSeats - BASE_SEATS);
  return BASE_PRICE + (additionalSeats * PER_SEAT_PRICE);
}
```

Track organization MRR separately from individual MRR. PayPal may require predefined plan tiers (3/5/10/20 seats) while Stripe supports dynamic quantities.

---

## Test Data Exclusion

Critical for accurate analytics. Filter at query time, not at display time:

| Type | Pattern | SQL Filter |
|------|---------|------------|
| Test emails | `*@test.yourdomain.com` | `email NOT LIKE '%@test.yourdomain.com'` |
| Test subscription IDs | `sub_test_*` | `external_id NOT LIKE 'sub_test_%'` |
| Test organizations | `E2E Team*` | `name NOT LIKE 'E2E Team%'` |

Apply these filters in EVERY analytics query. One leaked test account skews conversion rates, churn rates, and MRR.
