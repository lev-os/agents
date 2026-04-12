# Monte Carlo Revenue Simulation

> Never present a single revenue projection. Quantify uncertainty with probability distributions.

## Why Monte Carlo

Financial projections use compound growth/decay formulas that amplify small errors. A 1% error in churn rate becomes a 12% error at month 12. Monte Carlo runs thousands of simulations with randomized parameters to produce probability ranges instead of point estimates.

**Key output:** "There is a 90% chance your MRR will be between $X and $Y in 12 months" is infinitely more useful than "Your MRR will be $Z."

---

## Algorithm

### Input Parameters

```typescript
MonteCarloInput {
  currentSubscribers: number;      // Starting subscriber count
  currentMrr: number;              // Starting MRR
  cashOnHand: number;              // Available capital
  churnRate: {
    mean: number;                  // Expected monthly churn (0-1)
    stdDev: number;                // Uncertainty in churn
  };
  growthRate: {
    mean: number;                  // Expected monthly growth (0-1)
    stdDev: number;                // Uncertainty in growth
  };
  fixedCosts: number;              // Monthly infrastructure costs
  effectiveFeeRate: number;        // Blended payment fee rate (0-1)
  iterations: number;              // Simulation runs (100-10,000)
  months: number;                  // Projection horizon (1-120)
}
```

### Input Validation

```
currentSubscribers >= 0
cashOnHand >= 0
iterations >= 1 AND <= 10,000
months >= 1 AND <= 120
fixedCosts >= 0
effectiveFeeRate >= 0 AND <= 1
```

### The Simulation Loop

```
For each iteration (1..N):
  subscribers = currentSubscribers
  cash = cashOnHand
  monthResults = []

  For each month (1..M):
    // Sample parameters with uncertainty
    monthlyChurn = clamp(sampleNormal(churnRate.mean, churnRate.stdDev), 0, 1)
    monthlyGrowth = clamp(sampleNormal(growthRate.mean, growthRate.stdDev), -0.5, 2.0)

    // Apply churn and growth
    churned = round(subscribers × monthlyChurn)
    acquired = round(subscribers × monthlyGrowth)
    subscribers = max(0, subscribers - churned + acquired)

    // Revenue calculation
    grossMrr = subscribers × subscriptionPrice
    paymentFees = grossMrr × effectiveFeeRate
    netMrr = grossMrr - paymentFees - fixedCosts
    cash += netMrr

    // Bankruptcy detection
    if cash <= 0:
      Record month as final month
      BREAK (this iteration is dead)

    monthResults.push({ month, subscribers, mrr: grossMrr, netMrr, cash })

  Store iteration results
```

### Aggregation

After all iterations complete:

**Final MRR Distribution:**
```
Sort all final-month MRR values
p10 = value at 10th percentile
p50 = value at 50th percentile (median)
p90 = value at 90th percentile
mean = arithmetic mean
stdDev = standard deviation
```

**Runway Distribution:**
```
For each iteration, record the month when cash first <= 0
  (or M+1 if survived the entire horizon)
Sort survival months
p10 = pessimistic survival months
p50 = median survival months
p90 = optimistic survival months
```

**12-Month Survival Probability:**
```
probability = (iterations where cash > 0 at month 12) / total iterations
```

**Monthly Projection (for visualization):**
```
For each month 1..M:
  Collect all MRR values at that month across iterations
  Report: { month, mrrP10, mrrP50, mrrP90, cashP50 }
```

---

## The Box-Muller Transform

Generates normally-distributed random numbers from uniform random numbers:

```typescript
function sampleNormal(mean: number, stdDev: number): number {
  if (stdDev === 0) return mean;
  let u1 = 0, u2 = 0;
  while (u1 === 0) u1 = Math.random();  // (0, 1) not [0, 1)
  while (u2 === 0) u2 = Math.random();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return mean + z * stdDev;
}
```

**Why not just `Math.random()`?** Uniform distribution doesn't model real-world uncertainty. Churn rates cluster around a mean with occasional spikes — that's a normal distribution.

---

## Parameter Estimation

### Churn Rate Parameters

From historical data:
```
mean = average monthly churn rate over last 6 months
stdDev = standard deviation of monthly churn rates

If < 6 months of data:
  mean = current observed churn rate
  stdDev = mean × 0.3  (assume 30% volatility)
```

### Growth Rate Parameters

From subscriber count trend:
```
monthly_growth_rates = [(count[m] - count[m-1]) / count[m-1] for m in months]
mean = average(monthly_growth_rates)
stdDev = stdev(monthly_growth_rates)

If insufficient data:
  mean = current monthly growth rate
  stdDev = |mean| × 0.5  (assume 50% volatility)
```

---

## Clamping Rationale

| Parameter | Min | Max | Why |
|-----------|-----|-----|-----|
| Monthly churn | 0 | 1.0 | Can't have negative churn or churn > 100% |
| Monthly growth | -0.5 | 2.0 | Losing half your base or tripling in a month |

Without clamping, extreme samples can produce nonsensical results (negative subscribers, infinite growth).

---

## Performance Considerations

- **1,000 iterations × 12 months**: ~50ms on modern hardware
- **10,000 iterations × 120 months**: ~500ms — rate-limit this endpoint
- The simulation is CPU-bound with no I/O, so it blocks the event loop
- Consider: Web Worker offload, or limit iterations in the API

**Rate limiting recommendation:** Max 1 request per 5 seconds per admin user.

---

## Interpreting Results

### P10 / P50 / P90

| Percentile | Meaning | Use For |
|------------|---------|---------|
| P10 | 10% chance of being worse | Worst realistic case |
| P50 | Median outcome | Most likely scenario |
| P90 | 90% chance of being worse | Best realistic case |

**Communication pattern:**
> "We project MRR between $X (pessimistic) and $Y (optimistic), with $Z being the most likely outcome. There is an N% chance of surviving 12 months at current trajectory."

### When Survival Probability < 50%

This means more than half of simulated futures result in bankruptcy. Actions:
1. Reduce fixed costs (immediate impact)
2. Reduce churn (highest leverage)
3. Increase price (if market allows)
4. Raise capital (extends runway)

---

## Scenario Comparison

Run Monte Carlo with different parameter sets to compare strategies:

```
Scenario A (current): mean_churn=0.05, mean_growth=0.03
Scenario B (marketing push): mean_churn=0.05, mean_growth=0.08, additionalCosts=+$500
Scenario C (price increase): price=$25, mean_churn=0.07 (some churn from price hike)
```

Compare: P50 MRR at 12 months, survival probability, and P10 runway.
