---
name: triz-contradiction-matrix
description: Cross-reference 39 engineering parameters in a matrix to systematically identify which of 40 inventive principles resolve your technical contradiction
---

# TRIZ Contradiction Matrix

## Overview

The TRIZ Contradiction Matrix is a systematic innovation tool developed by Genrich Altshuller through statistical analysis of over 200,000 patents. The matrix maps 39 standard engineering parameters against each other in a 39×39 grid, with each cell recommending specific inventive principles that have historically resolved that type of technical contradiction.

At its core, the matrix addresses engineering contradictions: situations where improving one parameter worsens another (e.g., increasing strength while reducing weight). Rather than accepting trade-offs, the matrix guides inventors toward breakthrough solutions by applying patterns from successful innovations across all industries.

The genius of the system is abstraction: translate your specific problem into standard parameters, use the matrix to identify proven solution principles, then adapt those principles back to your context. This leverages humanity's collective problem-solving experience encoded in patent history.

## When to Use

- You face a technical contradiction: improving A worsens B
- Traditional optimization/trade-offs feel limiting (want breakthrough, not compromise)
- Stuck on a design problem where conventional approaches fail
- Need systematic ideation beyond brainstorming
- Cross-industry innovation: applying solutions from unrelated domains
- Complex technical systems (mechanical, electrical, chemical, software)
- Want to avoid "reinventing the wheel" by leveraging patent patterns

## The Process

### Step 1: State the Contradiction Clearly

Define what you want to improve and what gets worse as a result.

**Template:** "I want to improve [parameter A] without worsening [parameter B]"
**Example:** "I want to increase product strength without increasing weight"

### Step 2: Map to the 39 Standard Parameters

Translate your specific parameters into Altshuller's 39 categories (e.g., weight, speed, strength, temperature, pressure, energy, reliability, measurement accuracy, manufacturability, etc.). One problem may map to multiple parameter pairs.

**Example:** Strength → Parameter 14 (Strength), Weight → Parameter 1 (Weight of moving object)

### Step 3: Locate the Cell in the Matrix

Find the intersection: improving parameter on one axis, worsening parameter on the other. The matrix is asymmetric—improving A while worsening B yields different principles than improving B while worsening A.

**Example:** Improving Strength (row 14) while worsening Weight (column 1)

### Step 4: Review Recommended Inventive Principles

The cell contains 2-4 numbered principles from the 40 Inventive Principles (e.g., Segmentation, Asymmetry, Nested Doll, Beforehand Cushioning). These are historically proven solution patterns for this contradiction type.

**Example Cell Contents:** [1, 8, 15, 40] → Segmentation, Counterweight, Dynamicity, Composite materials

### Step 5: Brainstorm Solutions Using the Principles

Take each recommended principle and ask: "How could this pattern apply to my problem?" Generate multiple solutions per principle. The principles guide thinking; they don't provide ready-made answers.

**Example (Composite materials #40):** Replace single material with carbon fiber composite—10x strength at 1/5 the weight

### Step 6: Formulate Multiple Contradictions for Better Coverage

Reframe your problem as different contradiction pairs to surface more principles. The "strongest" principles—those appearing multiple times—often yield the best solutions.

**Example:** Also try "Improve Reliability without increasing Complexity" for additional insight angles

### Step 7: Evaluate and Prototype Solutions

Assess feasibility, cost, and impact of generated solutions. Build prototypes to test the most promising concepts.

## Example Application

**Situation (Aircraft Design):** Need stronger landing gear without adding weight (fuel efficiency constraint).

**Application:**
1. Contradiction: Improve Strength (14) without worsening Weight (1)
2. Matrix cell recommends: [1] Segmentation, [8] Counterweight, [15] Dynamicity, [40] Composite materials
3. Principle #40 (Composite materials): Replace steel with carbon fiber composite structure
4. Principle #15 (Dynamicity): Use inflatable/deployable structures that are rigid when pressurized, compact when stowed
5. Principle #1 (Segmentation): Divide landing gear into modular segments, each optimized for load distribution

**Outcome:** Boeing Dreamliner adopted carbon fiber composite landing gear components, achieving 20% weight reduction with equal strength. The matrix guided engineers toward material substitution (Principle #40) as the breakthrough solution.

## Anti-Patterns

- ❌ Accepting the contradiction as an inevitable trade-off without consulting the matrix
- ❌ Using only your industry's conventional solutions (matrix enables cross-pollination)
- ❌ Expecting ready-made solutions instead of using principles as thinking prompts
- ❌ Ignoring asymmetry: improving A→B is different from improving B→A
- ❌ Trying only one contradiction formulation (try multiple to surface more principles)
- ❌ Applying principles literally without adapting to your specific context
- ❌ Skipping lower-numbered principles in the cell (order doesn't indicate preference; all are equally valid)

## Related

- triz-segmentation (principle #1: divide into independent parts)
- triz-asymmetry (principle #4: break symmetry for optimization)
- triz-nested-doll (principle #7: nest objects for compactness)
- morphological-analysis (systematic parameter space exploration)
- theory-of-constraints (identify and exploit system bottlenecks)
- inversion (reverse problem to find solutions)
