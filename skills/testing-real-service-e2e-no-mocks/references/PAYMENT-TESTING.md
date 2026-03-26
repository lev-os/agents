# Payment Provider Test Mode Guide

> Test against REAL payment APIs in sandbox mode. Real API calls, fake money.

## Stripe Test Mode

### Setup

```bash
# Use test keys (NOT live keys)
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
```

### Test Payment Methods

| Method | Number | Behavior |
|--------|--------|----------|
| Visa (success) | `4242424242424242` | Always succeeds |
| Visa (decline) | `4000000000000002` | Always declined |
| 3D Secure | `4000000000003220` | Requires auth |
| Insufficient funds | `4000000000009995` | Insufficient funds |

### Webhook Testing

```bash
# Local: forward webhooks to your dev server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```

### Creating Test Webhooks Programmatically

```typescript
import crypto from "crypto";

function createSignedWebhook(payload: object, secret: string) {
    const body = JSON.stringify(payload);
    const timestamp = Math.floor(Date.now() / 1000);
    const signedPayload = `${timestamp}.${body}`;
    const signature = crypto
        .createHmac("sha256", secret)
        .update(signedPayload)
        .digest("hex");

    return {
        body,
        headers: {
            "stripe-signature": `t=${timestamp},v1=${signature}`,
            "content-type": "application/json",
        },
    };
}
```

## PayPal Sandbox

### Setup

```bash
PAYPAL_CLIENT_ID=sb-xxx
PAYPAL_CLIENT_SECRET=xxx
PAYPAL_ENV=sandbox
PAYPAL_PLAN_ID=P-xxx  # Sandbox plan
```

### Sandbox Accounts

Create at https://developer.paypal.com/dashboard/accounts

Test buyer: `buyer@personal.example.com` (password set in dashboard)
Test merchant: auto-created with your sandbox app

### Key Differences from Production

| Feature | Sandbox | Production |
|---------|---------|------------|
| Webhook delivery | Delayed (up to minutes) | Near real-time |
| SSL requirements | Relaxed | Strict |
| Rate limits | Generous | Standard |
| Subscription IDs | `I-xxx` prefix | Same format |

## Safety Guards (Non-Negotiable)

```typescript
// In test harness: BLOCK production URLs
const PROD_INDICATORS = [
    "sk_live_",     // Stripe live key
    "pk_live_",     // Stripe live publishable
    "production",   // PayPal env
];

function assertTestMode(env: Record<string, string>) {
    for (const indicator of PROD_INDICATORS) {
        for (const [key, value] of Object.entries(env)) {
            if (value.includes(indicator)) {
                throw new Error(
                    `SAFETY: ${key} contains production indicator "${indicator}". ` +
                    `Use test/sandbox keys for testing.`
                );
            }
        }
    }
}
```
