---
name: time-value-of-money
description: Value money received today higher than the same amount in the future because present money can be invested to earn returns—use Net Present Value to compare cash flows across time and make rational investment decisions
---

# Time Value of Money

## Overview
A dollar today is worth more than a dollar tomorrow because today's dollar can be invested to earn returns. Time value of money (TVM) is the foundational principle of finance, enabling comparison of cash flows occurring at different times. Core concepts: Present Value (PV) discounts future cash to today's value, Future Value (FV) projects today's cash forward, Net Present Value (NPV) evaluates investments by discounting all future cash flows to present. TVM informs capital budgeting, investment analysis, pricing, and strategic decisions across business and personal finance.

## When to Use
- Evaluating investment opportunities or projects
- Comparing financial options with different timing
- Setting prices for subscriptions or payment plans
- Deciding between lump sum or annuity payments
- Assessing business acquisitions or capital expenditures
- Personal finance (mortgages, retirement planning, car leases)
- Strategic planning with multi-year cash flows

## The Process

### Step 1: Identify All Cash Flows and Timing
List every cash inflow and outflow with precise timing (Year 0 = today, Year 1 = one year from now, etc.). Include initial investment, operating cash flows, terminal value.

**Example:** Project requires $100k investment today (Year 0). Generates $30k/year for 5 years (Years 1-5). Calculate NPV to decide if project is worth it.

### Step 2: Determine Discount Rate
Discount rate reflects opportunity cost of capital (what you could earn elsewhere) and risk. Use risk-free rate (government bonds) + risk premium. Higher risk = higher discount rate.

**Example:** Risk-free rate = 3%. Project has moderate risk, add 5% risk premium → Discount rate = 8%. This is the hurdle rate: project must beat 8% return to add value.

### Step 3: Calculate Present Value of Each Cash Flow
PV = FV / (1 + r)^n, where FV = future value, r = discount rate, n = years. Discount each future cash flow to today's value.

**Example:** Year 1 cash flow = $30k. PV = $30k / (1.08)^1 = $27,778. Year 5 cash flow = $30k. PV = $30k / (1.08)^5 = $20,418. Distant cash is worth less today.

### Step 4: Calculate Net Present Value (NPV)
NPV = Sum of all PV (inflows and outflows). Positive NPV = investment adds value. Negative NPV = investment destroys value. Zero NPV = breakeven.

**Example:** NPV = -$100k (initial investment) + $27,778 (Y1) + $25,720 (Y2) + $23,815 (Y3) + $22,051 (Y4) + $20,418 (Y5) = $19,782. NPV > 0 → Accept project.

### Step 5: Apply Decision Rule
Accept all positive NPV projects (when capital unlimited). When choosing between mutually exclusive projects, select highest NPV. Reject negative NPV projects unless strategic benefits exist.

**Example:** Project A: NPV = $20k, Project B: NPV = $15k, Project C: NPV = -$5k. If unlimited capital, do A and B. If capital constrained (can only do one), do A (highest NPV). Never do C (destroys value).

## Example Application

**Situation:** SaaS company choosing between annual subscription ($1,200 upfront) or monthly subscription ($120/month for 12 months = $1,440 total).

**Application:**
- **Customer Perspective**: Discount rate = 5% (opportunity cost of capital). Annual option: pay $1,200 today. Monthly option: 12 payments of $120 discounted to present.
- **Monthly PV Calculation**: Month 1 = $120/(1.05)^(1/12) = $119.50. Month 12 = $120/(1.05)^1 = $114.29. Total PV of monthly = $1,410.
- **Comparison**: Annual = $1,200 vs Monthly PV = $1,410. Annual saves $210 in present value terms (not just $240 nominal).
- **Vendor Perspective**: Getting $1,200 today (can reinvest immediately) worth more than $1,440 over 12 months. Vendor prefers annual, offers discount to incentivize.

**Outcome:** TVM explains why annual subscriptions offer discounts (vendors value cash today) and why customers should take them (even ignoring discount, paying later has time value).

## Anti-Patterns
- Ignoring time value and comparing nominal dollar amounts across years (adding Year 1 and Year 10 cash without discounting)
- Using wrong discount rate (too low undervalues risk, too high rejects good projects)
- Forgetting opportunity cost (comparing investment to zero instead of next-best alternative)
- Confusing NPV with payback period (payback ignores cash flows after breakeven and time value)
- Discounting sunk costs (only future cash flows matter, ignore unrecoverable past spend)
- Applying TVM to decisions where time isn't the key variable (comparing products with same timing)
- Over-relying on NPV when intangible strategic benefits matter (brand, optionality, learning)

## Related
- compound-interest
- opportunity-cost
- sunk-costs
- expected-value
- discount-rate
- risk-premium
