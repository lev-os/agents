# Financial Formula Catalog

> Every formula used in SaaS customer analytics, with derivation and edge cases.

## Revenue Metrics

### MRR (Monthly Recurring Revenue)

```
MRR = (Individual Active Subscribers × Price) + SUM(Organization Monthly Costs)
```

**Individual MRR:**
- Count subscriptions with status IN ('active', 'past_due')
- Filter to paid providers only (exclude 'gratis')
- Exclude test accounts (email suffix, subscription ID prefix)

**Organization MRR:**
- Each org has seat-based pricing: `calculateMonthlyCost(maxSeats)`
- Only count orgs with actual payment subscription IDs (not null)
- Exclude test orgs by name convention

**Edge cases:**
- `past_due` counts as active (grace period)
- Organizations with no payment subscription ID = phantom MRR (exclude)
- Test subscription IDs (`sub_test_*`) from E2E tests must be filtered

### ARR (Annual Recurring Revenue)

```
ARR = MRR × 12
```

### MRR Breakdown

```typescript
MrrBreakdown {
  individual: individualCount × SUBSCRIPTION_PRICE,
  org: SUM(calculateMonthlyCost(org.maxSeats)),
  total: individual + org,
  individualCount: number,
  orgCount: number
}
```

### Net New MRR

```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

- **New MRR**: Subscriptions created in period × price
- **Expansion MRR**: Upgrades (requires tiered pricing)
- **Contraction MRR**: Downgrades (requires tiered pricing)
- **Churned MRR**: Cancelled subscriptions in period × their last price

### Revenue Growth Rate

```
Growth Rate = (Current MRR - Previous MRR) / Previous MRR

where Previous MRR is derived:
  Previous = Current MRR - New Subscribers In Period × Price + Cancelled In Period × Price
```

### Projected MRR

```
Projected MRR (N months) = Current MRR × (1 + Monthly Growth Rate)^N
Projected ARR (N months) = Projected MRR × 12
```

---

## Subscriber Metrics

### Churn Rate

```
Monthly Churn Rate = (Subscribers Cancelled In Period / Subscribers Active At Start) × 100
```

**Denominator (Active At Start):**
- Created before period start date
- AND (not cancelled OR cancelled after period start date)

**Numerator (Churned):**
- `cancelledAt >= startDate AND cancelledAt < endDate`

**Windows:** 30-day (standard), 90-day (baseline for spike detection)

**Edge cases:**
- Churn rate = 0 when no subscribers at start → return 0, not NaN
- Use `safeDivide(numerator, denominator, fallback=0)` everywhere
- Past_due subscribers are NOT churned (they're in grace period)

### Average Subscription Length

```
Avg Length = AVG(
  CASE
    WHEN cancelledAt IS NOT NULL THEN cancelledAt - createdAt
    ELSE NOW() - createdAt
  END
) in days
```

### Conversion Rate

```
Conversion Rate = (Users With Any Paid Subscription / Total Users) × 100
```

- "Any paid subscription" = exists in subscriptions table with provider IN ('stripe', 'paypal')

---

## Unit Economics

### ARPU (Average Revenue Per User)

```
ARPU = Subscription Price (fixed pricing)
  -- OR for variable pricing:
ARPU = Total MRR / Active Subscribers
```

### LTV (Lifetime Value)

```
LTV = ARPU / (Monthly Churn Rate / 100)

Cap: min(LTV, ARPU × 120)  -- 10 years max if churn ≈ 0
```

**Edge case:** If churn rate = 0, LTV is theoretically infinite. Cap at 120 months.

### Gross Profit Per Subscriber

```
Gross Profit = ARPU - Average Payment Fee Per Transaction
```

### Gross Margin

```
Gross Margin % = (Gross Profit / ARPU) × 100
```

### Contribution Margin

```
Contribution Margin = ARPU - Payment Processing Fees
```

This is the per-subscriber profit before fixed costs. Must be > 0 for break-even to be reachable.

### LTV/CAC Ratio

```
LTV/CAC = LTV / Customer Acquisition Cost

Benchmarks:
  < 1.0  — Losing money on each customer
  1.0-3.0 — Unprofitable or marginal
  3.0+   — Healthy SaaS business
  > 5.0  — Under-investing in growth
```

---

## Break-Even Analysis

### Break-Even Subscribers

```
Break-Even Subscribers = Total Fixed Costs / Contribution Margin Per Subscriber

where:
  Fixed Costs = SUM(infrastructure costs: hosting, database, domain, email, monitoring, etc.)
  Contribution Margin = ARPU - Avg Payment Fee
```

**Reachability check:** If contribution margin <= 0, break-even is unreachable by subscriber growth alone. Flag this as critical insight.

### Subscribers To Go

```
Subscribers To Go = max(0, Break-Even Subscribers - Current Subscribers)
```

### Months To Break-Even

```
Months To Break-Even = log(Break-Even Subs / Current Subs) / log(1 + Monthly Growth Rate)
```

**Conditions for calculation:**
- Growth rate > 0
- Current subscribers > 0
- Subscribers to go > 0
- Contribution margin > 0

If any condition fails → return null (not calculable).

---

## Runway Analysis

### Net Burn Rate

```
Monthly Fixed Costs = SUM(vercel, supabase, domain, email, monitoring, other)
Monthly Payment Fees = Active Subscribers × Effective Fee Per Subscriber
Total Monthly Costs = Fixed Costs + Payment Fees
Net Burn = Total Monthly Costs - MRR
```

- If Net Burn < 0: **profitable** (MRR exceeds costs)
- If Net Burn > 0: **burning cash**

### Runway Months

```
Runway = Available Cash / Net Burn  (only if burning)
```

- If profitable → runway = null (infinite)
- If net burn = 0 → runway = null (break-even)

### Profitability Check

```
isProfitable = MRR > Total Monthly Costs
monthlyProfit = |Net Burn|  (when profitable)
```

---

## Payment Fee Calculations

### Stripe Fees

```
Domestic:      2.9% + $0.30 per transaction
International: 2.9% + 1.5% + $0.30 per transaction (4.4% + $0.30)
```

### PayPal Fees

```
Standard: 2.99% + $0.49 per transaction
```

### Effective Blended Fee

```
Effective Fee = (Stripe Ratio × Stripe Fee) + (PayPal Ratio × PayPal Fee)

where:
  Stripe Ratio = Stripe Subscriptions / Total Subscriptions
  PayPal Ratio = PayPal Subscriptions / Total Subscriptions
  Stripe Fee = domesticRate × (1 - internationalRatio) + internationalRate × internationalRatio + fixedFee
  PayPal Fee = paypalRate + fixedFee
```

**Defaults when no data:**
- Stripe/PayPal ratio: 70/30
- International ratio: 10%

### Fee Report

Query the immutable `paymentEvents` table (NOT subscriptions):
- Filter: `invoice.payment_succeeded` (Stripe), `PAYMENT.SALE.COMPLETED` (PayPal)
- Group by day + provider
- Calculate: daily totals, provider breakdown, effective rate trend

---

## Safe Division Helper

```typescript
function safeDivide(numerator: number, denominator: number, fallback = 0): number {
  if (!Number.isFinite(numerator) || !Number.isFinite(denominator) || denominator === 0) {
    return fallback;
  }
  return numerator / denominator;
}
```

Use this for EVERY division in financial calculations. NaN/Infinity in a dashboard is a P0 bug.

---

## Clamping & Bounds

| Value | Min | Max | Rationale |
|-------|-----|-----|-----------|
| Churn rate (Monte Carlo) | 0 | 1 | Can't be negative or > 100% |
| Growth rate (Monte Carlo) | -0.5 | 2.0 | Losing half or tripling |
| Break-even progress | 0 | 1 | Percentage clamped |
| LTV | 0 | ARPU × 120 | 10-year cap |
| Health score | 0 | 100 | Composite of 4 × 25 |
