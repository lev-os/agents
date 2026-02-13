---
name: Throughput Accounting
description: An alternative to traditional cost accounting that measures organizational performance through Throughput, Investment, and Operating Expense to focus decision-making on increasing the rate of money generation through sales
---

## Overview

Throughput Accounting (TA) is a management accounting methodology developed by Eliyahu Goldratt as part of the Theory of Constraints. It rejects traditional cost accounting's allocation-based approach in favor of three simple measures that directly link operational decisions to bottom-line profitability.

The core insight: Traditional cost accounting treats all costs as equal and focuses on efficiency metrics that often drive suboptimal behavior—building inventory, optimizing non-constraints, and cutting expenses that actually generate revenue. Throughput Accounting instead asks: "Does this decision increase the rate at which we generate money through sales?"

Unlike cost accounting which allocates overhead across products (distorting true profitability), TA treats most costs as fixed operating expenses and focuses on maximizing Throughput at the constraint. This leads to radically different decisions about product mix, pricing, and capacity investment.

## When to Use

Apply Throughput Accounting when:

- Making product mix decisions (which products to prioritize when capacity is limited)
- Evaluating new business opportunities (should we take this order at this price?)
- Deciding on capital investments (will this equipment increase Throughput?)
- Analyzing pricing strategies (what's the minimum price we can accept?)
- Comparing operational alternatives (which option generates more Throughput per constraint minute?)
- Diagnosing why "efficient" operations aren't profitable

Don't use this framework for:

- Early-stage startups without stable constraint identification
- Pure service businesses with no capacity constraints (though adapted versions exist)
- Situations requiring GAAP-compliant financial reporting (TA is for management decisions, not external reporting)
- One-time strategic decisions unrelated to operational throughput

## Process

### Step 1: Define the Three Measures

**Throughput (T)**: Revenue minus Truly Variable Costs (TVC). TVC includes only costs that vary directly with each unit of sales—typically raw materials and sales commissions. Labor is NOT included (it's a fixed cost in most organizations).

**Investment/Inventory (I)**: All money tied up in the system—raw materials, work-in-process, finished goods, plus equipment and facilities. The goal is to minimize this while maintaining Throughput.

**Operating Expense (OE)**: All money spent to turn Investment into Throughput. This includes labor, rent, utilities, depreciation—essentially all costs except TVC.

### Step 2: Calculate Key Metrics

**Net Profit**: NP = T - OE

**Return on Investment**: ROI = NP / I = (T - OE) / I

**Productivity**: P = T / OE

For product-level decisions, calculate:

**Throughput per Unit**: T/unit = Selling Price - TVC

**Throughput per Constraint Minute**: T/cm = (Selling Price - TVC) / Minutes on Constraint

### Step 3: Identify the Constraint

Throughput Accounting decisions revolve around the system constraint—the resource that limits total Throughput. All decisions should be evaluated based on their impact on constraint utilization.

Ask: What resource is currently limiting our ability to generate more sales? This could be a machine, a department, a skill, or market demand.

### Step 4: Evaluate Decisions Through the TA Lens

For any operational decision, ask:

1. Will this increase Throughput? (Most important)
2. Will this decrease Investment? (Important)
3. Will this decrease Operating Expense? (Least important)

Prioritize in this order. A decision that increases Throughput by $1M but increases OE by $100K is strongly positive. Traditional cost accounting might reject it due to "increased costs."

### Step 5: Apply Product Mix Logic

When constraint capacity is limited, prioritize products by T/cm (Throughput per constraint minute), not by margin percentage or total margin.

A product with 20% margin but 60 T/cm beats a product with 40% margin but 30 T/cm—you generate twice the profit per minute of constraint time.

### Step 6: Make Pricing Decisions

Minimum acceptable price = Truly Variable Costs (assuming spare constraint capacity exists).

If selling one more unit doesn't consume scarce constraint capacity, any price above TVC contributes to profit. Traditional "cost plus margin" pricing leaves money on the table.

## Example

**Manufacturing scenario**: A factory makes two products on a shared machine (the constraint).

| Product | Price | TVC | T/unit | Minutes on Constraint | T/cm |
|---------|-------|-----|--------|----------------------|------|
| A | $100 | $40 | $60 | 10 min | $6.00 |
| B | $150 | $80 | $70 | 20 min | $3.50 |

**Traditional analysis**: Product B has higher margin ($70 vs $60). Prioritize B.

**Throughput Accounting analysis**: Product A generates $6.00 per constraint minute vs $3.50 for B. Prioritize A.

With 1000 constraint minutes available:
- All A: 100 units x $60 = $6,000 Throughput
- All B: 50 units x $70 = $3,500 Throughput

**TA produces 71% more profit** from the same capacity.

**Pricing scenario**: Customer offers $45 for Product A (normally $100). TVC is $40.

Traditional cost accounting: Reject—"we can't sell below full cost of $65."

Throughput Accounting: If spare constraint capacity exists, accept—$5 contribution to profit that would otherwise be $0. If constraint is fully utilized, compare T/cm of this order vs. current products.

## Anti-Patterns

**Treating labor as variable cost**: In most organizations, you pay employees regardless of output. Including labor in product costs distorts profitability calculations and leads to wrong product mix decisions.

**Optimizing non-constraints**: Improving efficiency on a non-constraint resource adds no Throughput. It just creates more work-in-process inventory. Focus on the constraint.

**Prioritizing OE reduction over T increase**: Cutting costs has a floor (zero). Increasing Throughput has no ceiling. Companies that obsess over cost-cutting often starve Throughput-generating activities.

**Using margin percentage for product mix**: A 50% margin product that consumes 10x the constraint time is far worse than a 20% margin product. Always use T/cm.

**Building inventory "to absorb overhead"**: Traditional cost accounting encourages building inventory because it "absorbs" fixed costs into balance sheet assets. This is an accounting fiction that destroys cash flow.

**Ignoring the constraint**: TA decisions only make sense when you know your constraint. If you don't know it, find it first using the Five Focusing Steps.

## Related Frameworks

- **Five Focusing Steps** (TOC): The process for identifying and exploiting constraints—essential context for TA decisions
- **Drum-Buffer-Rope** (TOC): Production scheduling method that protects constraint Throughput
- **Current Reality Tree** (TOC): Diagnoses why Throughput is limited; TA measures the impact
- **Activity-Based Costing**: Alternative to traditional cost accounting; more accurate than traditional but still allocation-based unlike TA
- **Lean Accounting**: Another challenge to traditional cost accounting; shares TA's skepticism of absorption costing
- **Economic Value Added (EVA)**: Another attempt to align accounting with true value creation; focuses on capital costs

## Sources

- Goldratt, Eliyahu M. "The Goal" (1984) - Original introduction of TOC concepts
- Corbett, Thomas. "Throughput Accounting" (1998) - Definitive practitioner guide
- Theory of Constraints Institute - https://www.tocinstitute.org/theory-of-constraints.html
