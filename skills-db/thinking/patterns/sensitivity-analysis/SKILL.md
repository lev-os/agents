---
name: sensitivity-analysis
description: Systematic testing of how changes in input variables (assumptions) affect output results, revealing which factors drive outcomes and where model risk is concentrated.
---

# Sensitivity Analysis

**Canonical Source**: Financial Modeling / Operations Research
**Domain**: Finance, Strategy, Engineering, Decision Analysis
**Common Tools**: Excel Data Tables, Tornado Charts, What-If Analysis

## One-Line Summary

Systematic testing of how changes in input variables (assumptions) affect output results, revealing which factors drive outcomes and where model risk is concentrated.

## Core Concept

Sensitivity Analysis answers: "What matters most?" and "How wrong can I be?" It stress-tests assumptions by varying inputs one-at-a-time (or in combination) to measure impact on key outputs.

**The Core Technique**: Change one variable while holding others constant → measure output change → repeat for all variables → rank by impact.

**The Innovation**: Transforms opaque models ("trust the spreadsheet") into transparent risk maps ("here's what we're betting on").

## When to Use

**Ideal Scenarios**:
- Financial modeling (DCF valuation, project finance, pricing models)
- Strategic planning with uncertain market assumptions
- Engineering design trade-offs (cost vs. performance)
- Risk assessment to identify critical vulnerabilities
- Communicating model assumptions to non-technical stakeholders
- Validating that models behave logically (sanity checks)

**Not Suitable For**:
- When you need to test many variables simultaneously (use Monte Carlo instead)
- Highly non-linear systems where one-at-a-time testing misses interactions
- When precise probability distributions matter more than ranges
- Decisions requiring deep causal understanding (sensitivity shows correlation, not causation)

## Execution Steps

### 1. Define Base Case Model
- Build a model with clear inputs → calculations → outputs
- Set baseline assumptions for all variables (most likely values)
- Identify the KEY OUTPUT metric (NPV, IRR, profit, cost, etc.)
- Validate base case logic and formulas

*Output*: Working model with base case result

### 2. Identify Input Variables to Test
- List all assumptions that drive the output
- Focus on variables with genuine uncertainty (not fixed constraints)
- Typical candidates: growth rates, costs, prices, volumes, discount rates
- Limit to 5-10 most critical inputs for initial analysis

*Output*: Ranked list of input variables

### 3. Define Testing Ranges
- For each input, set a plausible range (low/high bounds)
- Use historical volatility, expert estimates, or ±10-20% heuristic
- Ensure ranges are realistic (not theoretically possible but practically absurd)
- Document reasoning for each range

*Output*: Range table (e.g., Revenue Growth: 5%-15%, Base: 10%)

### 4. Run One-Variable Sensitivity (One-Way)
- Change ONE input from low → high while keeping others at base
- Record output at each step (often 5-7 data points across range)
- Repeat for each input variable independently
- Calculate output swing: (Max Output - Min Output) / Base Output

*Output*: Sensitivity table showing output for each input variation

### 5. Visualize Results
- **Tornado Chart**: Horizontal bar chart ranking variables by output impact (widest = most sensitive)
- **Sensitivity Table**: Matrix showing output values across input ranges
- **Spider Chart**: Lines radiating from base case showing output response to each input

*Output*: Visual representation highlighting key drivers

### 6. Run Two-Variable Sensitivity (Two-Way)
- Select the 2-3 most impactful variables from Step 4
- Create a matrix: vary Variable A (rows) and Variable B (columns) simultaneously
- Excel Data Table is perfect for this (rows = input 1, columns = input 2, cells = output)
- Visualize with heat maps or contour plots

*Output*: 2D sensitivity matrix (e.g., NPV across revenue growth × cost inflation combinations)

### 7. Interpret and Communicate
- Identify HIGH-IMPACT inputs: Small changes → big output swings (focus risk mitigation here)
- Identify LOW-IMPACT inputs: Wide ranges → minor output change (deprioritize)
- Define "safe zones" vs. "danger zones" in two-way tables
- Communicate: "Our model is most sensitive to X; if X falls below Y, project fails"

*Output*: Executive summary with risk priorities and decision thresholds

## Common Pitfalls

**"One-at-a-Time" Blindness**
Testing variables individually misses interaction effects. Revenue growth + high costs might be survivable, but testing them separately hides the combined threat.

**Solution**: Follow one-way analysis with two-way (or three-way) for critical variable pairs. Use Monte Carlo for complex interactions.

**Arbitrary Ranges**
Setting input ranges like ±50% just because it's a round number, ignoring actual historical volatility.

**Solution**: Ground ranges in data (standard deviations, historical min/max, expert calibrated estimates).

**Confusing Sensitivity with Probability**
High sensitivity means "this variable matters IF it changes," not "this variable WILL change significantly."

**Solution**: Combine sensitivity analysis with probability assessments (which variables are both high-impact AND likely to vary?).

**Analysis Paralysis**
Testing 30 variables and overwhelming stakeholders with information.

**Solution**: Focus on the vital few (80/20 rule). Start with 5-7 key drivers, expand only if needed.

## Key Insights

**Tornado Charts Rule**: Named for their shape (widest bars at top, narrowing down), tornado charts instantly communicate "what matters" to executives. They're the gold standard for sensitivity visualization.

**Excel's Hidden Power**: Data Tables (What-If Analysis tool) automate sensitivity calculations. One-variable tables test a single input across a range; two-variable tables create matrices testing two inputs simultaneously.

**Model Validation Trick**: If changing a variable produces counterintuitive results (higher price → lower revenue in isolation), you've found a model bug or faulty logic.

**The "Swing Weight"**: In decision analysis, swing weight = the range of output values as an input swings from low to high. Larger swing = higher priority for risk management or better information gathering.

## Real-World Application

**DCF Valuation**: Valuing a startup with huge uncertainty. Sensitivity analysis tests revenue growth (5-25%), operating margin (10-30%), and discount rate (12-20%). Tornado chart reveals discount rate drives 60% of valuation variance → negotiate equity terms around cost of capital.

**Project Finance**: Solar farm NPV model depends on electricity price, construction cost, and tax incentives. Two-way table (price × cost) shows project is viable only if price stays above $0.08/kWh AND costs below $1.2M/MW. This defines the "go/no-go" zone for final investment decision.

**Pricing Strategy**: SaaS company tests pricing model sensitivity to churn rate (2-8%), conversion rate (10-25%), and CAC (50-200). Analysis shows churn has 3x impact of conversion → prioritize retention over acquisition.

## Related Frameworks

- **Tornado Diagram**: Visual output of sensitivity analysis, ranking variables by impact
- **Monte Carlo Simulation**: Probabilistic version (tests all variables simultaneously with distributions)
- **Scenario Analysis**: Tests discrete scenarios (best/base/worst) vs. continuous ranges
- **Break-Even Analysis**: Special case finding the input value where output = 0
- **Value at Risk (VaR)**: Sensitivity analysis applied to portfolio loss distributions
- **Stress Testing**: Extreme sensitivity analysis (push inputs to crisis levels)

## Anti-Patterns

**"It's All Red" Syndrome**
Setting every variable to worst-case simultaneously to show "look how risky this is." That's not sensitivity analysis—it's fear-mongering.

**Output Overload**
Generating 50-page sensitivity reports with every possible variable combination, ensuring nobody reads it.

**Ignoring Correlations**
Testing oil price sensitivity and shipping cost sensitivity independently when they're highly correlated (both driven by crude prices).

**"Set It and Forget It"**
Running sensitivity analysis once during planning and never updating as assumptions change or new data emerges.

## Score Justification

**Framework Assessment**: 44/50 (Tier 1 - Canonical)

- **Practitioner Weight (9/10)**: Ubiquitous in investment banking, corporate finance, consulting (McKinsey/Bain/BCG all use religiously), and engineering. Every financial model includes sensitivity analysis. Minor deduction: sometimes performed mechanically without insight.
- **Clarity & Executability (9/10)**: Extremely clear concept. Excel makes execution trivial (Data Tables automate calculations). Anyone can run a tornado chart within an hour of learning.
- **Proven ROI (9/10)**: Prevents disasters by revealing fragile assumptions. McKinsey studies show companies using sensitivity analysis outperform in volatile markets. Saved countless projects from over-optimistic projections.
- **Novelty (7/10)**: Conceptually straightforward (vary inputs, measure outputs). The insight is systematic application and visualization (tornado charts), not mathematical innovation.
- **Cross-Domain Applicability (10/10)**: Universal. Finance, engineering, pharma R&D, public policy, climate modeling, supply chain optimization, marketing mix modeling—any domain with uncertain inputs.

**Notable**: Excel's Data Table feature (introduced 1990s) democratized sensitivity analysis. Before spreadsheets, this was tedious manual calculation. Now it's 3 clicks. Tornado charts became the de facto standard for communicating model risk to boards and executives.
