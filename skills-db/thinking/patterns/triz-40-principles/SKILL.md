---
name: triz-40-principles
description: Resolve engineering contradictions by applying one of 40 inventive principles systematically derived from 200,000 patents instead of trial-and-error
---

# TRIZ (40 Inventive Principles)

## Overview
TRIZ (Theory of Inventive Problem Solving), developed by Soviet engineer Genrich Altshuller from analyzing 200,000 patents, codifies 40 universal principles used to solve technical contradictions. Rather than brainstorming randomly, TRIZ uses a contradiction matrix to suggest which principles apply to specific engineering trade-offs.

## When to Use
- Facing engineering contradictions (improving X worsens Y)
- Stuck after conventional solutions fail
- Designing products with conflicting requirements
- Need systematic innovation vs. random ideation
- Optimizing complex technical systems
- Breaking through "impossible" trade-offs

## The Process

### Step 1: Define the Contradiction
Identify the technical parameters in conflict. TRIZ recognizes 39 engineering parameters (weight, speed, strength, cost, reliability, etc.). State: "I want to improve X, but it worsens Y."

**Example:** "I want to increase airplane speed (parameter: velocity), but it increases fuel consumption (parameter: energy use)."

### Step 2: Look Up in Contradiction Matrix
TRIZ matrix maps 39×39 parameter conflicts to suggested principles (1-40). Find your contradiction, check which principles historically solved it.

**Example:** Speed vs. Energy Use matrix suggests: Principle 2 (Taking Out), Principle 15 (Dynamics), Principle 16 (Partial/Excessive Action).

### Step 3: Apply Suggested Principles
**Key TRIZ Principles** (10 most powerful):
- **1. Segmentation**: Divide object into independent parts
- **2. Taking Out**: Separate interfering part or property
- **5. Merging**: Bring closer or combine identical/similar operations
- **10. Prior Action**: Perform required change in advance
- **13. The Other Way Around**: Invert action or make movable parts fixed
- **15. Dynamics**: Make object adaptive, optimize at each stage
- **25. Self-Service**: Make object serve itself
- **35. Parameter Changes**: Change physical state, concentration, flexibility
- **40. Composite Materials**: Replace homogeneous with composite

**Example:** Apply Principle 15 (Dynamics): Variable-geometry wings that adapt shape during different flight phases (takeoff: high lift, cruise: low drag).

### Step 4: Test and Refine
Prototype the principle-based solution. Iterate if needed, try secondary principles if first doesn't work.

**Example:** F-14 Tomcat variable-sweep wings: Wings extend for takeoff/landing (low speed, high lift), retract for supersonic flight (high speed, low drag). Solved speed-vs-efficiency contradiction.

## Popular TRIZ Principles with Examples

**Segmentation**: Modular smartphone cases (easy to replace damaged parts vs. replacing entire case)

**Taking Out**: Wireless charging (remove charging port that gets damaged)

**Nested Doll**: Telescoping antenna (compact when stored, extends when needed)

**Asymmetry**: Asymmetric tire treads (optimize for wet and dry conditions simultaneously)

**Prior Cushioning**: Airbags (protection applied before collision)

**Dynamics**: Adjustable standing desks (optimize for sitting and standing)

**The Other Way Around**: Induction cooking (heat pan from underneath vs. heating element)

**Self-Service**: Self-cleaning oven (uses high heat to burn residue)

**Composite Materials**: Carbon fiber (lightweight + strong, solving weight-strength contradiction)

## Example Application

**Situation:** Medical device company needs sterile packaging that's easy to open in emergency (contradiction: strength vs. ease of opening).

**Contradiction**: Improve "ease of operation" worsens "strength" (packaging tears prematurely) or improve "strength" worsens "ease of operation" (can't open quickly).

**TRIZ Matrix Suggests**: Principle 1 (Segmentation), Principle 15 (Dynamics), Principle 24 (Intermediary).

**Applied Principle 1 (Segmentation)**: Design peel-apart packaging with strong outer layer + weak perforated inner layer. Strong when sealed, tears cleanly along perforation when pulled.

**Outcome:** Packaging maintains sterility during shipping (strong), opens in <2 seconds during emergency (easy). Contradiction resolved.

## Anti-Patterns
- ❌ Using TRIZ for non-technical problems (better frameworks exist)
- ❌ Blindly following matrix suggestions without understanding principles
- ❌ Stopping at first principle without testing others
- ❌ Applying TRIZ to problems solvable by conventional methods (overkill)
- ❌ Ignoring business constraints (technically elegant, commercially unviable)
- ❌ Treating principles as rigid rules vs. creative prompts

## Related
- first-principles-thinking
- inversion
- second-order-thinking
- systems-thinking
- design-patterns
