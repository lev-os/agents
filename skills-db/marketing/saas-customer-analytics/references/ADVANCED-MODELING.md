# Advanced Mathematical Modeling for SaaS Analytics

> The baseline skill uses heuristic scoring and naive Monte Carlo. This reference upgrades
> every projection, prediction, and decision into a principled, calibrated,
> uncertainty-aware system using rigorous applied mathematics.

## EV Opportunity Matrix

| Method | Impact | Confidence | Effort | Score | Natural Fit |
|--------|--------|------------|--------|-------|-------------|
| Survival Analysis | 5 | 5 | 2 | **12.5** | Subscription lifetime IS survival data |
| Bayesian Conjugate Updating | 5 | 5 | 2 | **12.5** | Churn rate = Beta-Binomial |
| Empirical Bayes / Shrinkage | 5 | 4 | 2 | **10.0** | Many small cohorts, noisy estimates |
| Sequential Testing (SPRT) | 4 | 5 | 2 | **10.0** | "When can I trust this metric?" |
| CVaR / EVT Tail Risk | 4 | 4 | 2 | **8.0** | Revenue at risk in worst scenarios |
| Renewal Theory | 3 | 4 | 2 | **6.0** | Payment cycle dynamics |
| Hidden Markov / Regime | 4 | 4 | 3 | **5.3** | Business phase transitions |
| Multi-Armed Bandits | 3 | 4 | 3 | **4.0** | Adaptive intervention selection |

**Selection principle:** All 8 are natural fits (not shoehorned). Implement top-to-bottom by score.

---

## 1. Survival Analysis (Score 12.5)

### Failure Signature

The naive churn rate `cancelled / active_at_start` treats all subscribers equally regardless of tenure.
A user subscribed for 11 months has a fundamentally different churn hazard than one subscribed for 11 days.
The simple ratio discards this temporal structure entirely.

### The Upgrade: Kaplan-Meier + Cox Proportional Hazards

**Subscriber lifetimes are literally survival data.** Every subscriber enters the study at signup.
They either churn (event) or are still active (right-censored). This is textbook survival analysis.

#### Kaplan-Meier Estimator (Non-Parametric Survival Curve)

```
S(t) = PRODUCT_{t_i <= t} (1 - d_i / n_i)

where:
  t_i = distinct event times (cancellation dates)
  d_i = number of cancellations at time t_i
  n_i = number at risk just before t_i (active + right-censored after t_i)
```

**What it gives you:** A survival curve showing the probability of a subscriber surviving past month N.
This is infinitely more informative than a single churn rate number.

```
S(t) for a healthy SaaS:
  S(1mo)  = 0.95  (5% churn in month 1)
  S(3mo)  = 0.88
  S(6mo)  = 0.80
  S(12mo) = 0.70  (30% churn by year 1)
  S(24mo) = 0.58

The SHAPE tells you everything: steep early drop = onboarding problem,
gradual late decline = feature fatigue, flat plateau = loyal base.
```

#### Cox Proportional Hazards (Feature-Weighted Churn)

```
h(t | x) = h_0(t) × exp(beta_1 × x_1 + beta_2 × x_2 + ... + beta_p × x_p)

where:
  h_0(t)  = baseline hazard (common to all subscribers)
  x_i     = covariates (behavioral features)
  beta_i  = learned coefficients (log hazard ratios)
```

**Covariates for SaaS churn:**

| Feature | Expected beta | Interpretation |
|---------|--------------|----------------|
| active_days_30 | -0.08 | Each active day reduces hazard 8% |
| days_since_last_activity | +0.03 | Each inactive day increases hazard 3% |
| unique_skills_used | -0.15 | Breadth reduces hazard 15% per skill |
| payment_failures_90d | +0.40 | Each failure increases hazard 49% |
| activation_lag_days | +0.05 | Slow activation increases hazard |
| is_org_member | -0.30 | Org membership reduces hazard 26% |

**Proof obligation:** Proportional hazards assumption — the ratio of hazards between any two individuals
is constant over time. Verify via Schoenfeld residual test. If violated, use time-varying coefficients
or accelerated failure time models.

#### Artifacts

- **Survival curves** per cohort/segment (replaces retention heatmap with calibrated curves)
- **Hazard ratios** per behavioral feature (replaces hand-tuned driver weights)
- **Median survival time** per risk segment (replaces "churn risk: high/medium/low")
- **Expected remaining lifetime** per subscriber: `E[T - t | T > t]` (the residual life, directly maps to LTV)

#### LTV via Survival (Replaces naive ARPU/churn)

```
LTV = ARPU × integral_0^∞ S(t) dt

For discrete monthly billing:
LTV = ARPU × SUM_{t=0}^{∞} S(t)
    ≈ ARPU × SUM_{t=0}^{T_max} S(t)   (truncate at T_max months)
```

This is materially more accurate than `ARPU / churn_rate` because it accounts for the
non-exponential shape of real survival curves.

---

## 2. Bayesian Conjugate Updating (Score 12.5)

### Failure Signature

The naive churn rate `k / n` is a point estimate with no uncertainty quantification.
With 3 churns out of 20 subscribers, is the true rate 15%? Or could it plausibly be 5% or 30%?
The point estimate doesn't say.

### The Upgrade: Beta-Binomial Model

Churn is a Bernoulli process: each subscriber either churns (1) or doesn't (0) in a period.
The conjugate prior for a Bernoulli rate is the Beta distribution.

```
Prior:     Beta(alpha, beta)        — our belief before data
Likelihood: Binomial(n, p)          — k churns out of n subscribers
Posterior:  Beta(alpha + k, beta + n - k)   — updated belief

Posterior mean:     (alpha + k) / (alpha + beta + n)
Posterior mode:     (alpha + k - 1) / (alpha + beta + n - 2)   (MAP)
95% credible interval: Beta.ppf(0.025), Beta.ppf(0.975)
```

#### Choosing the Prior

| Prior | alpha | beta | Meaning |
|-------|-------|------|---------|
| Uninformative | 1 | 1 | Uniform — no prior belief |
| Weakly informative | 2 | 18 | "We expect ~10% churn" |
| Industry benchmark | 3 | 47 | "SaaS typically sees 5-8% monthly churn" |
| Empirical Bayes | data-driven | data-driven | Estimated from all cohorts (see §3) |

#### Concrete Example

```
Prior: Beta(2, 18)  — mildly informed toward 10% churn
Data:  3 churns out of 25 subscribers this month

Posterior: Beta(2+3, 18+25-3) = Beta(5, 40)
Posterior mean: 5/45 = 11.1%
95% credible interval: [4.2%, 22.0%]

Compare to naive: 3/25 = 12% (no uncertainty)
```

The credible interval tells you: "We're 95% confident the true churn rate is between 4.2% and 22%."
This honest uncertainty propagates through all downstream calculations (LTV, break-even, runway).

#### Bayesian Churn Rate as Monte Carlo Input

Instead of `churnRate: { mean: 0.05, stdDev: 0.02 }` (hand-tuned), sample directly from the posterior:

```typescript
// In Monte Carlo loop:
const churnRate = sampleBeta(posteriorAlpha, posteriorBeta);
// No hand-tuned stdDev needed — the posterior IS the uncertainty
```

This replaces the arbitrary normal distribution assumption with a principled posterior that:
- Gets tighter with more data (automatically)
- Is bounded [0, 1] (no clamping needed)
- Updates incrementally as new data arrives (no recomputation)

---

## 3. Empirical Bayes / James-Stein Shrinkage (Score 10.0)

### Failure Signature

Small cohorts (Jan signup class: 8 users, Feb: 12 users) have wildly noisy churn estimates.
Individual cohort estimates swing from 0% to 40% based on single cancellations.

### The Upgrade: Shrink Toward the Grand Mean

James-Stein showed that when you have 3+ parallel estimates, shrinking each toward the grand mean
reduces total mean squared error. Always. This is not optional — it's a provable mathematical fact.

```
Shrunk estimate = Grand mean + shrinkage_factor × (Raw estimate - Grand mean)

shrinkage_factor = 1 - (k-2) × sigma² / SUM(raw_i - grand_mean)²
```

**For SaaS cohort churn rates:**

```
Raw estimates:   [0%, 16%, 8%, 25%, 0%, 12%]  (6 monthly cohorts)
Grand mean:      10.2%
Shrunk estimates: [6.1%, 13.7%, 9.5%, 16.8%, 6.1%, 11.4%]
```

The extreme values (0% and 25%) get pulled toward the mean. The effect is strongest
for small cohorts and weakest for large ones.

#### Empirical Bayes (Robbins Lineage)

More principled than James-Stein: estimate the prior from the data itself.

```
1. Compute raw churn rate for each cohort: theta_hat_i = k_i / n_i
2. Estimate the overall distribution of true rates (the prior)
3. Compute posterior for each cohort given the estimated prior
4. Posterior mean = shrunk estimate
```

With Beta-Binomial conjugacy:
```
Global prior: Beta(alpha_0, beta_0) estimated from all cohorts via MLE or method of moments
Per-cohort posterior: Beta(alpha_0 + k_i, beta_0 + n_i - k_i)
```

#### Where to Apply Shrinkage

| Metric | Raw Source | Shrink Toward |
|--------|-----------|---------------|
| Cohort churn rate | k/n per cohort | Grand churn rate |
| Cohort LTV | Revenue / cohort size | Grand LTV |
| Segment conversion rate | Converted / segment size | Grand conversion rate |
| Feature adoption rate | Users using feature / total | Grand adoption rate |

**Rule of thumb:** If any estimate is based on < 30 observations, shrink it.

---

## 4. Sequential Testing / SPRT (Score 10.0)

### Failure Signature

"Our conversion rate dropped from 5% to 3% this week — is this real or noise?"
With classical hypothesis testing, you need to wait for a fixed sample size.
With sequential testing, you can monitor continuously with guaranteed error rates.

### The Upgrade: Sequential Probability Ratio Test (SPRT)

```
After each observation x_t:
  Lambda_t = Lambda_{t-1} × P(x_t | H1) / P(x_t | H0)

  if Lambda_t >= B: Accept H1 (real change detected)
  if Lambda_t <= A: Accept H0 (no change, stop testing)
  otherwise: continue collecting data

Boundaries: A = beta / (1 - alpha),  B = (1 - beta) / alpha
  alpha = false positive rate (e.g., 0.05)
  beta = false negative rate (e.g., 0.10)
```

#### For SaaS Metric Monitoring

```
H0: churn_rate = theta_0 (baseline)
H1: churn_rate = theta_1 (elevated, e.g., theta_0 × 1.5)

Each day, observe whether churns exceed expected:
  Lambda_t = Lambda_{t-1} × Binomial(k_t | n_t, theta_1) / Binomial(k_t | n_t, theta_0)

When Lambda_t crosses B: "Churn spike confirmed with false alarm rate < 5%"
```

**Advantage over Z-score:** Z-score requires a fixed window (7 days) and has no formal stopping rule.
SPRT adapts to the evidence — it stops earlier when the signal is strong and later when it's ambiguous.
This means faster alerting on real problems and fewer false alarms.

#### Anytime-Valid Confidence Sequences (E-Values)

For continuous monitoring without fixed stopping:

```
E-value e_t: A measure of evidence against H0.
  E_t >= 1/alpha at any stopping time => reject H0 at level alpha.

The key property: valid at ANY time you choose to look, not just at a pre-specified time.
```

This is the correct framework for dashboards where admins look at metrics whenever they want.

---

## 5. CVaR / EVT for Revenue Tail Risk (Score 8.0)

### Failure Signature

Monte Carlo P10 says "your MRR could be as low as $800." But what's the expected MRR
*given that you're in that worst 10%*? That's CVaR, and it's materially worse than P10.

### Conditional Value at Risk

```
CVaR_alpha = E[Loss | Loss >= VaR_alpha]

For revenue (invert for loss):
CVaR_10% = E[MRR | MRR <= P10]
         = "Expected MRR in the worst 10% of scenarios"
```

**Why it matters:** CVaR accounts for the severity of tail events, not just their threshold.
Two businesses with the same P10 can have very different CVaR_10% — one has a gentle tail
(worst case $700), the other has a catastrophic tail (worst case $0, bankrupt).

#### Implementation in Monte Carlo

```typescript
// After running N Monte Carlo iterations:
const finalMrrs = iterations.map(i => i.finalMrr).sort((a, b) => a - b);
const p10Index = Math.floor(N * 0.10);
const worstDecile = finalMrrs.slice(0, p10Index);

const cvar10 = worstDecile.reduce((sum, mrr) => sum + mrr, 0) / worstDecile.length;
// cvar10 = expected MRR given you're in the worst 10% of outcomes
```

#### Extreme Value Theory (EVT) for Rare Events

When you don't have enough Monte Carlo iterations to characterize extreme tails, use EVT:

```
Peak Over Threshold (POT): Fit a Generalized Pareto Distribution (GPD) to
observations exceeding a high threshold.

For revenue shortfall (loss = target - actual):
  Exceedances over threshold u follow GPD(xi, sigma):
    if xi > 0: heavy tail (catastrophic risk)
    if xi = 0: exponential tail (moderate risk)
    if xi < 0: bounded tail (risk is capped)
```

The shape parameter xi tells you whether your business has catastrophic tail risk.

---

## 6. Renewal Theory for Payment Cycles (Score 6.0)

### The Insight

Subscription renewals are a renewal process: each payment resets the clock.
The renewal reward theorem gives long-run average revenue per unit time:

```
Long-run revenue rate = E[payment amount] / E[inter-payment time]
```

For monthly subscriptions with some failed payments and retries:

```
E[inter-payment time] = 30 days × (1 + retry_probability × avg_retry_delay_days/30)
E[payment amount] = subscription_price × (1 - permanent_failure_rate)

Effective MRR per subscriber = E[amount] / E[time] × 30
```

This gives a more accurate per-subscriber MRR than the naive `price × is_active` because
it accounts for the stochastic reality of payment processing.

---

## 7. Hidden Markov Models for Business Regime Detection (Score 5.3)

### Failure Signature

Your growth rate has been 8% for 3 months, then suddenly drops to -2%.
Is this noise or a regime shift? The current insight engine uses a fixed 2x multiplier
against the 90-day baseline. A Hidden Markov Model detects regime changes principally.

### The Model

```
Hidden states: S = {Growth, Plateau, Decline, Crisis}
Observations: Monthly MRR growth rate, churn rate, signup rate

Transition matrix A:
         Growth  Plateau  Decline  Crisis
Growth  [0.80    0.15     0.04     0.01]
Plateau [0.10    0.75     0.12     0.03]
Decline [0.05    0.15     0.70     0.10]
Crisis  [0.01    0.04     0.25     0.70]

Emission distributions per state:
  Growth:  growth ~ Normal(0.08, 0.03), churn ~ Normal(0.03, 0.01)
  Plateau: growth ~ Normal(0.01, 0.02), churn ~ Normal(0.05, 0.02)
  Decline: growth ~ Normal(-0.03, 0.03), churn ~ Normal(0.08, 0.03)
  Crisis:  growth ~ Normal(-0.10, 0.05), churn ~ Normal(0.15, 0.05)
```

**Viterbi decoding** gives the most likely state sequence.
**Forward algorithm** gives the posterior probability of being in each state right now.

#### Artifact: Regime Dashboard Widget

```
Current regime: GROWTH (87% posterior probability)
Next most likely: PLATEAU (11%)
Transition watch: Growth→Plateau probability increased from 8% to 15% this month
Action: Monitor churn rate trend; if 2 consecutive months above 5%, regime may be shifting
```

---

## 8. Multi-Armed Bandits for Intervention Optimization (Score 4.0)

### Failure Signature

The intervention engine fires the same email template to every at-risk user.
But maybe setup guides work better for new users and feature highlights work better
for established users. You don't know which intervention works best for which segment.

### Thompson Sampling with Beta-Binomial

```
For each (intervention, user_segment) pair:
  Prior: Beta(1, 1)  — uninformative
  After observing: k successes (retained) out of n interventions
  Posterior: Beta(1 + k, 1 + n - k)

To select intervention for a new at-risk user:
  1. Sample theta_i ~ Beta(alpha_i, beta_i) for each intervention i
  2. Select intervention with highest sampled theta_i
  3. Observe outcome (retained or churned within 30 days)
  4. Update the corresponding Beta posterior
```

**Why Thompson Sampling:** It automatically balances exploration (trying under-tested interventions)
and exploitation (using the best-known intervention). The exploration rate decreases naturally
as you collect more data.

#### Cold Start

When you have zero data, all interventions are equally likely. Thompson Sampling handles
this gracefully — it randomly explores all arms until evidence accumulates.

---

## Composition: How the Families Work Together

```
RAW DATA
  │
  ├── Subscription events ──► Survival Analysis ──► Calibrated S(t), hazard ratios
  │                                                       │
  │                                                       ├──► LTV via integral of S(t)
  │                                                       └──► Cox beta → weighted churn drivers
  │
  ├── Monthly churn counts ──► Bayesian Beta-Binomial ──► Posterior churn distribution
  │                                    │
  │                                    └──► Feed posterior into Monte Carlo (replaces hand-tuned params)
  │
  ├── Cohort-level estimates ──► Empirical Bayes Shrinkage ──► Stable small-sample estimates
  │
  ├── Ongoing metric streams ──► Sequential Testing (SPRT) ──► Anytime-valid change detection
  │                                    │
  │                                    └──► Replaces Z-score anomaly detection with formal guarantees
  │
  ├── Monte Carlo outputs ──► CVaR / EVT ──► Tail-risk revenue envelope
  │
  ├── MRR + churn time series ──► Hidden Markov Model ──► Business regime posterior
  │
  └── Intervention outcomes ──► Thompson Sampling ──► Adaptive intervention selection
```

**Timescale separation:** Survival analysis and Cox models are refitted monthly.
Bayesian churn posteriors update daily. SPRT monitors continuously.
Thompson Sampling updates per intervention outcome. HMM updates monthly.

---

## Proof Obligations

| Method | Assumption | Verification |
|--------|-----------|-------------|
| Kaplan-Meier | Independent censoring | Check: do censored users look like uncensored users |
| Cox PH | Proportional hazards | Schoenfeld residual test p > 0.05 |
| Beta-Binomial | Exchangeable subscribers | Check: no strong time trend within window |
| Empirical Bayes | Cohorts share common prior | Check: between-cohort variance is moderate |
| SPRT | Known H0 and H1 | Calibrate from historical baseline |
| CVaR | Monte Carlo convergence | Check: CVaR stabilizes with increasing iterations |
| HMM | Markov property of regimes | Check: regime duration is memoryless (geometric) |
| Thompson Sampling | Stationary reward distribution | Monitor for arm quality drift |

---

## Fallback Policy

Every advanced method must have a deterministic conservative fallback:

| Method | Fallback | Trigger |
|--------|----------|---------|
| Survival curves | Naive churn rate | < 20 subscribers |
| Bayesian posterior | Uniform prior (wide CI) | < 5 observations |
| Empirical Bayes | No shrinkage (raw estimates) | < 3 cohorts |
| SPRT | Fixed-window Z-score | Insufficient sequential data |
| CVaR | P10 from Monte Carlo | < 100 iterations |
| HMM | Rule-based regime (2x threshold) | < 6 months of data |
| Thompson Sampling | Round-robin all interventions | < 10 outcomes per arm |

**Principle:** Advanced methods enhance when data is sufficient. They must never
produce worse results than the simpler baseline when data is scarce.

---

## Implementation Priority

### Phase A: Immediate (replaces existing with strictly better)
1. **Bayesian churn rate** — Drop-in replacement for point estimates. Add credible intervals.
2. **Empirical Bayes cohort shrinkage** — Drop-in improvement for cohort metrics.
3. **CVaR in Monte Carlo** — Add 5 lines to existing simulation loop.

### Phase B: Near-term (adds new capability)
4. **Survival curves** — Kaplan-Meier from subscription data. New visualization.
5. **SPRT for metric monitoring** — Replace Z-score anomaly detection.

### Phase C: Advanced (requires more data)
6. **Cox proportional hazards** — Replace hand-tuned behavioral weights with learned coefficients.
7. **Hidden Markov Model** — Regime detection for business phase transitions.
8. **Thompson Sampling** — Adaptive intervention optimization.

---

## Galaxy-Brain Transparency Cards

Every advanced modeling decision should emit a card:

```
┌─────────────────────────────────────────────────────────┐
│ GALAXY-BRAIN CARD: Churn Rate Estimation                │
├─────────────────────────────────────────────────────────┤
│ Method: Beta-Binomial conjugate updating                │
│ Prior:  Beta(2, 18) ← industry benchmark 10% churn     │
│ Data:   4 churns out of 32 subscribers this month       │
│ Posterior: Beta(6, 46) → mean 11.5%, 95% CI [4.8%, 21%]│
│ vs naive: 4/32 = 12.5% (no uncertainty)                │
│                                                         │
│ Intuition: With 32 observations and a mild prior,       │
│ the data dominates — posterior is close to naive.        │
│ With 8 observations, the prior would dominate more.     │
│                                                         │
│ Assumption: Subscribers are exchangeable within period   │
│ What would change this: strong seasonal/cohort effects   │
│ Fallback: if < 5 observations, use prior mean (10%)     │
└─────────────────────────────────────────────────────────┘
```

---

# Tier 2: Second-Order Methods (Beyond the Foundation)

These 8 families address failure signatures that the first 8 don't cover.
Implement only after the Tier 1 methods are in place and producing data.

## Tier 2 EV Matrix

| Method | Impact | Confidence | Effort | Score | Addresses |
|--------|--------|------------|--------|-------|-----------|
| Conformal Prediction | 4 | 5 | 2 | **10.0** | Uncalibrated churn probabilities |
| Causal Inference | 5 | 4 | 3 | **6.7** | "Did the intervention actually work?" |
| Influence Functions | 4 | 4 | 2 | **8.0** | Customer concentration risk |
| Convex Budget Allocation | 4 | 4 | 2 | **8.0** | Optimal intervention spend |
| Changepoint Detection (BOCPD) | 4 | 5 | 2 | **10.0** | Precise "when did things change?" |
| Bifurcation / Tipping Points | 4 | 3 | 3 | **4.0** | Self-sustaining growth threshold |
| Hawkes Processes | 3 | 3 | 3 | **3.0** | Contagious churn cascades |
| Optimal Experimental Design | 3 | 4 | 2 | **6.0** | Maximize A/B test information |

---

## 9. Conformal Prediction for Churn (Score 10.0)

### Failure Signature

The behavioral scoring model outputs `churnProbability: 0.72`. Is that calibrated?
If you take 100 users scored at 0.72, do exactly 72 of them churn? Almost certainly not.
Uncalibrated probabilities lead to wrong intervention thresholds and wasted outreach.

### The Upgrade: Distribution-Free Prediction Intervals

Conformal prediction gives **finite-sample coverage guarantees** without distributional assumptions.
For any nonconformity score function and calibration set, the coverage is PROVEN, not estimated.

```
Given: calibration set C of (behavior_profile, churned?) pairs
       new subscriber x with behavior profile

1. Compute nonconformity score: s(x) = 1 - healthScore(x) / 100
2. Compute p-value: p(x) = (1 + |{i in C : s_i >= s(x)}|) / (|C| + 1)
3. Predict "will churn" if p(x) <= alpha (e.g., 0.05)

Coverage guarantee: P(true label in prediction set) >= 1 - alpha
  This holds for ANY distribution. No assumptions needed beyond exchangeability.
```

#### Mondrian Conformal (Stratum-Aware)

Different user segments may have different calibration needs:

```
Strata: { new_users (< 30 days), established (30-180 days), veteran (> 180 days) }

For each stratum g:
  p_g(x) = (1 + |{i in C_g : s_i >= s(x)}|) / (|C_g| + 1)

Result: per-stratum coverage guarantee.
  New users might need wider prediction sets (less data).
  Veterans might need tighter ones (more calibration data).
```

#### Conformal Risk Control (CRC) for Interventions

When intervention actions have asymmetric costs:

```
Cost of false positive (unnecessary intervention): $2 (email cost)
Cost of false negative (missed churn): $240 (12 months of lost revenue)
Asymmetry ratio: 120:1

CRC objective: E[cost(decision, truth)] <= tau
  → Set intervention threshold to control expected loss, not just error rate.
```

#### Artifact: Calibration Dashboard

```
Predicted churn probability | Actual churn rate | Coverage | N
0.0 - 0.1                  | 4.2%              | ✓        | 48
0.1 - 0.2                  | 11.8%             | ✓        | 34
0.2 - 0.4                  | 28.5%             | ✓        | 21
0.4 - 0.7                  | 55.2%             | ✓        | 12
0.7 - 1.0                  | 81.3%             | ✓        | 8
```

If any row shows actual rate outside the predicted range, the model is miscalibrated.
Conformal prediction guarantees this never happens (in aggregate).

---

## 10. Causal Inference for Intervention Effectiveness (Score 6.7)

### Failure Signature

The intervention engine sends 100 rescue emails. 60 of those users stay.
Did the email cause 60 saves? Or would 50 of them have stayed anyway?
Without causal reasoning, you can't tell — and your "60% save rate" is inflated.

### The Upgrade: Counterfactual Intervention Measurement

#### Propensity Score Matching

Compare intervened users to similar non-intervened users:

```
1. Score each user: P(receiving intervention | behavioral features)
   → logistic regression on: healthScore, daysSinceActivity, events30, etc.

2. Match: For each intervened user, find a non-intervened user with similar propensity score

3. Compare: Churn rate among intervened vs. matched controls

   ATE (Average Treatment Effect) = E[churn | intervened] - E[churn | matched control]
```

**If ATE = -0.15:** The intervention truly reduces churn by 15 percentage points.
**If ATE = -0.02:** The intervention barely helps — most "saved" users would have stayed anyway.

#### Instrumental Variables (for Non-Random Intervention)

When you can't randomize interventions (ethical constraints), use an instrument:

```
Instrument candidate: "Day of week the user entered high-risk"
  → Users entering high-risk on weekdays get interventions faster
     (support team is available) than weekend entries
  → Day-of-week affects intervention timing but NOT churn directly
  → Day-of-week → Intervention speed → Churn (valid IV chain)

2SLS estimate:
  Stage 1: InterventionSpeed = f(DayOfWeek, controls)
  Stage 2: Churned = g(PredictedInterventionSpeed, controls)
```

#### Difference-in-Differences (Pre/Post Product Change)

Measure the causal effect of a product change on churn:

```
Treatment group: Users exposed to new onboarding flow (after launch date)
Control group:   Users on old onboarding flow (before launch date)

DiD estimate = (Post_treatment - Pre_treatment) - (Post_control - Pre_control)
```

This removes both the pre-existing trend and the time effect.

#### Artifact: Causal Intervention Report

```
Intervention: "Setup guide email for inactive users"
Method: Propensity score matching (N=84 treated, N=84 matched controls)
ATE: -12.3 percentage points (p=0.031)
NNT (Number Needed to Treat): 8.1 (send 8 emails to save 1 subscriber)
Cost per saved subscriber: 8.1 × $0.01 email cost = $0.081
Revenue saved per intervention: 1/8.1 × $240 LTV = $29.63
ROI: 365:1
```

---

## 11. Influence Functions for Concentration Risk (Score 8.0)

### Failure Signature

Your MRR is $2,000. One enterprise customer pays $1,000/month (50% of revenue).
If they churn, you lose half your revenue. The Monte Carlo simulation treats all
subscribers equally and dramatically underestimates this concentration risk.

### The Upgrade: Sensitivity of Estimators to Individual Data Points

The influence function of an estimator T at distribution F for observation x is:

```
IF(x; T, F) = lim_{eps→0} [T(F + eps × delta_x) - T(F)] / eps
```

In plain English: "How much does our metric change if we add/remove this one customer?"

#### Per-Customer Revenue Influence

```
For each subscriber i:
  revenue_influence_i = MRR_i / Total_MRR
  concentration_risk = max(revenue_influence_i)

  Herfindahl Index: H = SUM(revenue_influence_i²)
    H close to 0: diversified
    H close to 1: concentrated in one customer
```

#### Per-Customer Churn Impact

```
For each subscriber i:
  IF removing subscriber i, how does churn rate change?

  churn_influence_i = (churn_rate_without_i - churn_rate_with_i) / churn_rate_with_i

  If |churn_influence_i| > 0.1: this single user materially affects the churn metric.
```

#### Artifact: Concentration Risk Dashboard

```
┌─────────────────────────────────────────────────┐
│ CONCENTRATION RISK REPORT                       │
├─────────────────────────────────────────────────┤
│ Herfindahl Index: 0.14 (moderate concentration) │
│ Top 1 customer: 28% of MRR ($560)               │
│ Top 3 customers: 52% of MRR ($1,040)            │
│ Revenue at risk (if top 3 churn): $1,040        │
│                                                  │
│ WARNING: Losing "Acme Corp" would reduce MRR    │
│ by 28%, exceeding the 20% single-entity limit.  │
│ Action: Prioritize retention for high-value accts│
└─────────────────────────────────────────────────┘
```

---

## 12. Convex Optimization for Intervention Budget Allocation (Score 8.0)

### Failure Signature

You have 50 at-risk subscribers and budget for 20 interventions (human outreach calls).
Currently you sort by churn probability and call the top 20. But this ignores
revenue impact — saving a $20/month individual is less valuable than saving a
$300/month organization.

### The Upgrade: Revenue-Weighted Optimal Allocation

```
maximize  SUM_i x_i × P(save_i) × Revenue_i

subject to:
  SUM_i x_i <= Budget  (intervention budget constraint)
  x_i in {0, 1}        (binary: intervene or not)
  SUM_i x_i × cost_i <= CostBudget  (total cost constraint)
```

This is a 0-1 knapsack problem — NP-hard in general but solvable via LP relaxation
for practical sizes (< 10,000 at-risk users).

#### LP Relaxation (Continuous)

```
Relax x_i in {0, 1} to x_i in [0, 1].
Sort by bang-per-buck: (P(save_i) × Revenue_i) / cost_i descending.
Greedy fill until budget exhausted.
Fractional last item → round or skip.
```

This gives a provably near-optimal allocation.

#### Dual Variables (Shadow Prices)

The Lagrange multiplier on the budget constraint gives the **marginal value of one
more intervention slot**:

```
lambda* = marginal revenue saved per additional intervention

If lambda* = $45: each additional intervention slot saves $45 in expected revenue.
  → If an intervention costs < $45, expand the budget.
  → If an intervention costs > $45, budget is sufficient.
```

This dual variable directly informs the "how much should we spend on retention?" question.

---

## 13. Bayesian Online Changepoint Detection / BOCPD (Score 10.0)

### Failure Signature

The current insight engine detects churn spikes when 30d rate > 2x 90d baseline.
This is a fixed rule with no uncertainty. BOCPD gives the **posterior probability
that a changepoint occurred at each timestep**, updating in real-time.

### The Model

```
At each time t, maintain a distribution over run length r_t:
  r_t = number of observations since the last changepoint

P(r_t | data_{1:t}) ∝ P(x_t | r_t, data) × P(r_t | r_{t-1}) × P(r_{t-1} | data_{1:t-1})

Growth probability:  P(r_t = r_{t-1} + 1) = 1 - H(r_{t-1})
Changepoint probability: P(r_t = 0) = H(r_{t-1})

where H(r) is the hazard function (prior probability of changepoint after r observations)
  Constant hazard: H(r) = 1/lambda (geometric prior, expected run length = lambda)
```

#### For SaaS Metrics

```
Observable: daily MRR growth rate, daily churn count, daily signup count

At each day:
  Update run-length distribution
  If P(r_t = 0 | data) > threshold (e.g., 0.5):
    → "Changepoint detected with 50%+ posterior probability"
    → Report: previous regime parameters vs. new regime parameters

Advantage over 2x-threshold: BOCPD detects GRADUAL shifts, not just spikes.
A slow, steady increase in churn from 4% to 7% over 3 months would be invisible
to the 2x rule but would accumulate strong BOCPD evidence.
```

#### Artifact: Changepoint Timeline

```
2026-01-15: Churn regime shift detected (P=0.82)
  Before: mean churn 4.2%, stddev 1.1%
  After:  mean churn 6.8%, stddev 1.5%
  Possible cause: competitor launch, pricing change, product regression

2026-02-28: Growth regime shift detected (P=0.91)
  Before: mean daily signups 2.1
  After:  mean daily signups 4.8
  Possible cause: viral content, marketing campaign, feature launch
```

---

## 14. Bifurcation Analysis for Business Tipping Points (Score 4.0)

### Failure Signature

Linear projections assume growth rate stays constant. In reality, SaaS businesses
have tipping points: below a certain subscriber count, costs > revenue (death spiral);
above it, word-of-mouth growth exceeds churn (virtuous cycle).

### The Model

Model subscriber dynamics as a differential equation:

```
dN/dt = growth(N) - churn(N) - fixed_cost_pressure(N)

where:
  growth(N) = g × N + w × N²/(K + N²)     (linear + word-of-mouth with saturation)
  churn(N)  = c × N                         (proportional churn)
  fixed_cost_pressure = if N × ARPU < fixed_costs then drag else 0

Equilibria: dN/dt = 0 → solve for N*
```

#### Saddle-Node Bifurcation (The Viability Threshold)

```
For a simplified model: dN/dt = (g - c) × N + w × N² - F/ARPU

Two equilibria exist when (g - c)² + 4w × F/ARPU > 0:
  N_lower = unstable (below this = death spiral)
  N_upper = stable (above this = self-sustaining)

Critical threshold: N_crit = F / (ARPU × (g - c))
  = Fixed costs / (Price × net growth rate per subscriber)
```

**This is a mathematically principled version of break-even analysis** that accounts
for nonlinear growth dynamics (word-of-mouth, network effects) rather than assuming
constant growth.

#### Early Warning Signals

Near a tipping point, the system exhibits:
1. **Critical slowing down**: Recovery from perturbations takes longer
2. **Increased variance**: Metrics fluctuate more
3. **Increased autocorrelation**: Today's value predicts tomorrow's more strongly

Monitor these three signals in your MRR time series. If all three increase
simultaneously, you may be approaching a tipping point.

---

## 15. Hawkes Processes for Contagious Churn (Score 3.0)

### Failure Signature

The behavioral model treats each subscriber's churn as independent.
But in reality, churn can be **self-exciting**: a team lead churns, their
team members follow. A public figure leaves, word spreads. Each cancellation
increases the probability of the next one.

### The Model

```
Intensity function lambda(t):
  lambda(t) = mu + SUM_{t_i < t} alpha × exp(-beta × (t - t_i))

where:
  mu    = baseline churn rate (spontaneous cancellations)
  alpha = excitation factor (how much each churn event amplifies future churn)
  beta  = decay rate (how quickly the amplification fades)
  t_i   = times of past churn events

Branching ratio: alpha/beta
  < 1: subcritical (contagion dies out) — normal business
  = 1: critical (each churn triggers exactly one more on average) — crisis
  > 1: supercritical (churn cascade) — existential threat
```

#### When This Matters

For most SaaS products with independent individual subscribers, Hawkes is overkill.
But if you have:
- **Team/org subscriptions** where one member leaving triggers others
- **Community-driven products** where social proof matters
- **Enterprise customers** where a public departure creates PR risk

Then the branching ratio is the key metric. Monitor it monthly.

---

## 16. Optimal Experimental Design for A/B Tests (Score 6.0)

### Failure Signature

You want to test 3 pricing tiers but only get 50 signups per month.
A naive 1/3 split gives ~17 users per variant — far too few for significance.
Optimal design maximizes information per observation.

### D-Optimal Design

```
Choose experimental allocations to maximize det(X'X)
  where X is the design matrix (observations × parameters)

For comparing K treatments with unequal prior information:
  Allocate proportional to sqrt(variance of estimated effect)
  → Treatments with higher uncertainty get more observations
```

#### Sequential Allocation for SaaS

Instead of fixed splits, use sequential allocation:

```
At each new signup:
  1. Compute current Fisher information matrix for each variant
  2. Assign to variant that maximizes information gain
  3. Update estimates

This converges to optimal allocation much faster than equal-split randomization.
```

#### Sample Size via Expected Loss

Instead of "how many users for significance?", ask:
```
What is the expected monetary loss from choosing the wrong variant?

E[Loss] = P(wrong choice) × |Revenue difference between best and second-best|

Stop when E[Loss] < acceptable_threshold (e.g., $100)
```

---

## Extended Composition: Full Method Stack

```
TIER 1 (Foundation)
  Survival Analysis ──► Calibrated lifetimes
  Bayesian Updating ──► Posterior churn rates with uncertainty
  Empirical Bayes ──► Shrunk cohort estimates
  SPRT ──► Formal change detection
  CVaR/EVT ──► Tail-risk revenue envelope
  Renewal Theory ──► Stochastic payment cycle MRR
  HMM ──► Business regime identification
  Thompson Sampling ──► Adaptive intervention selection

TIER 2 (Second-Order, requires Tier 1 outputs)
  Conformal Prediction ──► Calibrated churn predictions (uses Tier 1 scores)
  Causal Inference ──► True intervention effectiveness (uses Tier 1 intervention data)
  Influence Functions ──► Customer concentration risk (uses Tier 1 MRR data)
  Convex Allocation ──► Optimal intervention targeting (uses Tier 1 churn + revenue)
  BOCPD ──► Precise changepoint timing (extends Tier 1 SPRT)
  Bifurcation ──► Tipping point identification (uses Tier 1 dynamics model)
  Hawkes ──► Contagion-aware churn (extends Tier 1 survival model)
  Optimal Design ──► Efficient A/B testing (extends Tier 1 Bayesian framework)
```

## Extended Proof Obligations

| Method | Assumption | Verification |
|--------|-----------|-------------|
| Conformal | Exchangeable calibration data | Check for time trends in residuals |
| Causal (PSM) | No unmeasured confounders | Sensitivity analysis (Rosenbaum bounds) |
| Causal (IV) | Instrument validity (exclusion restriction) | Over-identification test |
| Influence | Estimator is differentiable | Check smoothness of metric function |
| Convex | Objective is convex | Verify concavity of P(save) × Revenue |
| BOCPD | Observations within regime are i.i.d. | Check residual autocorrelation |
| Bifurcation | ODE model captures dominant dynamics | Compare model predictions to data |
| Hawkes | Events are point processes | Check inter-event time distribution |
| Optimal Design | Linear model for treatment effects | Check residual diagnostics |

## Extended Fallback Policy

| Method | Fallback | Trigger |
|--------|----------|---------|
| Conformal | Raw churn probability (uncalibrated) | < 30 calibration points |
| Causal | Naive before/after comparison | < 50 per treatment arm |
| Influence | Equal-weight customer importance | < 10 subscribers |
| Convex | Sort by churn probability × revenue | < 5 at-risk users |
| BOCPD | Fixed 2x threshold rule | < 30 days of time series |
| Bifurcation | Linear break-even analysis | Insufficient growth nonlinearity |
| Hawkes | Independent churn model | Branching ratio < 0.1 |
| Optimal Design | Equal-split randomization | < 3 variants |
