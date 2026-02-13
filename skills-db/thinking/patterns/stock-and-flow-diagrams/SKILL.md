---
name: stock-and-flow-diagrams
description: Model system dynamics with stocks (accumulations), flows (rates of change), and feedback to quantitatively predict behavior over time
---

# Stock and Flow Diagrams: Quantitative System Dynamics Modeling

## Overview

Stock and Flow Diagrams, pioneered by Jay Forrester at MIT and refined by Donella Meadows in "Thinking in Systems", are the foundational tool for quantitative system dynamics modeling. Where Causal Loop Diagrams show qualitative feedback structure, stock-flow diagrams add mathematical precision: stocks (accumulations you can measure at any moment), flows (rates that fill or drain stocks), and converters (calculations/parameters). Meadows' core principle: "If you understand the dynamics of stocks and flows, you understand a good deal about the behavior of complex systems."

The key insight: all dynamic behavior comes from how stocks accumulate and deplete through flows. A bathtub fills (inflow) and drains (outflow) - the water level (stock) at any moment equals initial level plus all inflows minus all outflows. This simple structure explains inventory dynamics, population growth, skill acquisition, market share shifts, and epidemic spread. Stocks create inertia (can't change instantly), flows create momentum, and the interplay generates oscillation, overshoot, collapse, and equilibrium.

## When to Use

- Predicting quantitative system behavior over time (not just direction, but magnitude)
- Testing policy interventions before implementation (run simulations with different parameters)
- Understanding why systems overshoot or oscillate (delays between stocks and flows)
- Designing systems with desired behavior (stable, self-regulating, adaptive)
- Explaining counterintuitive dynamics (why "obvious" solutions fail)
- Building consensus through simulation (stakeholders see consequences of decisions)

## The Process

### Step 1: Identify Stocks (Accumulations)

Stocks are elements you can see, measure, or count at any given moment. They are nouns that accumulate over time. Stocks change slowly and create system inertia.

**Stock identification:**
- Can you measure it right now without observing flow? (Inventory level, bank balance, population)
- Does it persist if all flows stop? (Water in bathtub, not water flowing)
- Is it an accumulation of past flows? (Knowledge = accumulated learning, debt = accumulated borrowing)

**Notation:** Rectangle or bold text: `[Stock Name]`

**Examples:**
- Physical: Inventory, cash reserves, pollutants in atmosphere
- Informational: Knowledge, reputation, technical debt
- Human: Population, skilled workforce, customer base

### Step 2: Identify Flows (Rates of Change)

Flows are rates that increase or decrease stocks over time. Flows are verbs - actions happening now. Flows can change instantly (turn faucet on/off).

**Flow identification:**
- Does it represent a rate? (Measured in units/time: customers/month, $/day, people/year)
- Does it fill or drain a stock?
- Can it change abruptly? (Hire 10 people today, fire 5 tomorrow)

**Notation:** Arrow with valve symbol: `→|>→` pointing into (inflow) or out of (outflow) stock

**Examples:**
- Inflows: Hiring rate, sales rate, learning rate, births
- Outflows: Attrition rate, churn rate, forgetting rate, deaths
- Bidirectional: Can have both inflows and outflows on same stock

### Step 3: Add Converters and Connectors

Converters are parameters, constants, or calculations that influence flows. Connectors show information links (not material flows).

**Converters:**
- Constants: Market size, cost per unit, retention rate (%)
- Calculations: Revenue = customers × price, capacity utilization = production / max capacity
- Exogenous inputs: Interest rates, seasonality, competitor actions

**Notation:** Circle or plain text: `(Converter Name)`

**Connectors:** Thin arrows showing information flow (what influences what)
- Stock → flow connector: Stock level influences flow rate (more inventory → reduce production)
- Converter → flow: Parameter affects flow (higher price → lower sales rate)

### Step 4: Define Mathematical Relationships

Specify equations for each flow and converter. Stocks automatically integrate flows (stock = previous stock + inflows - outflows).

**Flow equations:**
- Linear: `Sales rate = marketing spend × conversion rate`
- Nonlinear: `Adoption rate = contacts × adoption probability × (1 - market saturation)`
- Feedback-driven: `Production rate = desired inventory - actual inventory / adjustment time`

**Stock equations (implicit):**
- `Stock(t) = Stock(t-1) + (Inflows - Outflows) × dt`
- Simulation tools handle integration automatically

**Example:**
- Stock: `[Customer Base]`
- Inflow: `New customers/month = marketing spend × 0.02 × (market size - customer base)`
- Outflow: `Churn/month = customer base × 0.05` (5% monthly churn)
- Converter: `Market size = 10,000` (constant), `Marketing spend = revenue × 0.3`

### Step 5: Simulate and Validate Behavior

Run the model forward in time (simulation). Compare output to observed behavior. Adjust equations and parameters until model reproduces reality.

**Simulation questions:**
- Does the model reproduce historical behavior? (Validation)
- How does it respond to parameter changes? (Sensitivity analysis)
- What scenarios produce desired outcomes? (Policy testing)
- Where are tipping points? (When does behavior change qualitatively?)

**Validation tactics:**
- Test against historical data (does model match past trends?)
- Extreme conditions test (what happens if flows go to zero or infinity?)
- Check units (dimensional consistency - all equations must have correct units)

## Example Application

**Situation:** Manufacturing company struggling with inventory oscillation - alternating between stockouts and excess inventory.

**Application:**

**Step 1 - Define stocks:**
- `[Inventory]` (units)
- `[Orders in Pipeline]` (units ordered but not yet arrived)

**Step 2 - Define flows:**
- Inflow to Inventory: `Arrival rate = Orders in Pipeline / lead time` (lead time = 4 weeks)
- Outflow from Inventory: `Sales rate = 100 units/week` (constant demand)
- Inflow to Pipeline: `Order rate = desired inventory - actual inventory / adjustment time`
- Outflow from Pipeline: `Arrival rate` (same as inflow to Inventory)

**Step 3 - Define converters:**
- `Desired inventory = 8 weeks × sales rate = 800 units`
- `Lead time = 4 weeks` (supplier delay)
- `Adjustment time = 2 weeks` (how fast we correct deviations)

**Step 4 - Mathematical relationships:**
- `Order rate = (800 - Inventory) / 2` (order to close gap in 2 weeks)
- Problem: When inventory drops, we order aggressively. But orders take 4 weeks to arrive. We don't see effect, so we keep ordering. Inventory arrives all at once → overshoot → stop ordering → inventory depletes → cycle repeats.

**Step 5 - Simulate:**
- Initial inventory: 800 units
- Sales rate: 100/week constant
- Shock: Sales spike to 150/week for 2 weeks
- Result: Inventory oscillates with 8-week period (2× lead time), swinging between 400-1200 units

**Intervention:** Change order rate equation to account for pipeline:
- `Order rate = (desired inventory - actual inventory - orders in pipeline) / adjustment time`
- Now we see "orders already placed" and don't overreact
- Result: Oscillation damped by 80%, inventory stays within 700-900 range

**Outcome:** Stock-flow model revealed that ignoring pipeline orders caused oscillation. Simple equation change (adding pipeline awareness) stabilized system without changing lead time or demand.

## Example Application 2

**Situation:** Epidemic spreading through population - model to predict healthcare capacity needs.

**Application:**

**Stocks:**
- `[Susceptible]` - can be infected
- `[Infected]` - currently sick
- `[Recovered]` - immune after recovery

**Flows:**
- `Susceptible → Infected` (infection rate)
- `Infected → Recovered` (recovery rate)

**Equations:**
- `Infection rate = contact rate × transmission probability × Susceptible × Infected / Population`
- `Recovery rate = Infected / illness duration`

**Converters:**
- `Contact rate = 10 people/day`
- `Transmission probability = 0.02` (2% per contact)
- `Illness duration = 14 days`

**Simulation results:**
- Peak infected occurs at day 45: 2,800 people
- Total infected over 6 months: 78% of population
- Intervention test: Reduce contact rate to 5/day (lockdown) → peak drops to 800 people, spreads over 4 months

**Outcome:** Model shows healthcare capacity planning (need 2,800 beds without intervention, 800 with lockdown). Stock-flow structure reveals why "flattening curve" works - reduces peak load by spreading infections over time.

## Anti-Patterns

- Confusing stocks with flows (revenue is a flow, bank balance is a stock)
- Missing critical feedback loops (flows depend on stocks, stocks depend on flows)
- Ignoring delays (stock-flow systems often oscillate due to information/material delays)
- Overly complex first model (start simple, add detail iteratively)
- Forgetting conservation laws (matter/energy conserved - if it leaves one stock, enters another)
- Using model without validation (must match historical behavior before trusting predictions)
- Assuming linear relationships (most real flows are nonlinear - saturation, thresholds, S-curves)

## Related

- stocks-flows-delays (conceptual foundation - this is the implementation tool)
- causal-loop-diagrams (qualitative structure precedes quantitative stock-flow model)
- feedback-loops (stock-flow diagrams show how feedback loops create behavior over time)
- system-dynamics (stock-flow diagrams are core tool of system dynamics practice)
- twelve-leverage-points (stock-flow models reveal leverage points quantitatively)
- unintended-consequences (simulation exposes unintended feedback before real-world implementation)
