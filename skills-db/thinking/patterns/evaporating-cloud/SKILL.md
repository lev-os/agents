---
name: Evaporating Cloud
description: A conflict resolution diagram that exposes and invalidates the hidden assumptions perpetuating dilemmas, transforming win-lose trade-offs into win-win solutions
---

## Overview

The Evaporating Cloud (also called Conflict Resolution Diagram or "the Cloud") is one of the five thinking processes in Eliyahu Goldratt's Theory of Constraints. It's a structured method for resolving conflicts that seem to have no acceptable compromise—situations where two opposing positions both appear necessary and legitimate.

Goldratt's core insight: conflicts persist because we hold at least one false assumption. By systematically surfacing and challenging the assumptions underlying each side of a conflict, we can "evaporate" the dilemma entirely rather than settling for compromise.

The Cloud uses a five-box diagram (A-B-C-D-D') that maps the logical structure of any conflict: a shared goal (A), two legitimate needs (B, C), and two opposing wants/actions (D, D') that seem to contradict each other. The power comes from examining not the positions themselves, but the hidden assumptions connecting them.

This framework produces breakthrough solutions by reframing the problem space. Instead of "which side wins?" it asks "what assumptions make this seem impossible to satisfy both?"

## When to Use

Apply the Evaporating Cloud when:

- Two sides genuinely disagree about the right course of action and both have valid points
- Trade-off decisions feel forced ("we can have quality OR speed, not both")
- Compromise solutions leave everyone unsatisfied (classic lose-lose outcome)
- Conflicts keep resurfacing despite attempts to resolve them (signal: underlying assumptions haven't changed)
- Teams are stuck between competing objectives (innovation vs. stability, growth vs. profitability)
- Personal dilemmas where both options have merit (stay in job vs. pursue new opportunity)

Don't use this framework for:

- Win-lose situations where one side is objectively wrong (use data and logic instead)
- Conflicts based purely on resource scarcity without underlying logic (you can't evaporate "we only have $100K and need $200K")
- Quick decisions under time pressure (Cloud analysis takes focused thinking time)
- Situations where conflict is interpersonal rather than logical (address relationship issues first)

## Process

### Step 1: Define the Conflict (D vs. D')

**Identify the two opposing positions or actions.** These are the visible manifestation of the conflict—what people are arguing about.

Be specific and action-oriented: "hire 5 more developers" vs. "don't hire more developers." Not vague: "invest in people" vs. "be conservative."

State them as opposites: if we do D, we cannot do D', and vice versa. This is the core dilemma.

Example: D = "Standardize on one technology stack" vs. D' = "Let teams choose their own tools"

### Step 2: Articulate the Needs (B and C)

**For each position, identify the legitimate need or requirement it's trying to satisfy.** Ask: "Why do we want D? What need does it fulfill?"

Needs are one level more abstract than positions. They explain the "why" behind the "what."

Box B is the need that D satisfies. Box C is the need that D' satisfies. Both needs must be valid—if one side's need is illegitimate, you don't have a true dilemma.

Example:
- B = "Ensure system reliability and maintainability" (why we want standardization)
- C = "Maximize team productivity and innovation" (why we want autonomy)

### Step 3: Identify the Common Goal (A)

**What shared objective do both needs serve?** There must be a higher-level goal that both B and C support, or this isn't a dilemma—it's just opposing interests.

The goal should be something all stakeholders genuinely care about and agree on.

Example: A = "Build products that delight customers while sustaining engineering excellence"

### Step 4: Draw and Validate the Cloud

**Create the five-box diagram with arrows showing logical relationships:**
- A ← B ← D
- A ← C ← D'
- D conflicts with D'

Read it aloud: "In order to achieve [A], we need [B]. To satisfy [B], we must [D]. But we also need [C] to achieve [A], and to satisfy [C], we must [D'], which conflicts with [D]."

Validate with stakeholders: Does this accurately represent the dilemma? Is anything missing or misstated?

### Step 5: Surface Assumptions

**For each arrow in the diagram, list the assumptions that make that connection seem necessary.** This is where the breakthrough happens.

Ask for each relationship:
- B→D: "Why do we assume that B requires D? What must be true for this to hold?"
- C→D': "Why do we assume that C requires D'? What hidden beliefs drive this?"
- B↔A: "Why is B necessary for A?"
- C↔A: "Why is C necessary for A?"

Be exhaustive. List 3-10 assumptions per arrow. The false assumption is hiding in here.

Example assumptions for "B (reliability) requires D (standardization)":
- "Different technologies can't talk to each other reliably"
- "We don't have expertise in multiple stacks"
- "Standardization always improves reliability"
- "Teams can't self-regulate quality without mandates"

### Step 6: Challenge and Invalidate Assumptions

**Test each assumption rigorously.** Is it always true? Can we find counter-examples? Is it based on past constraints that no longer apply?

Look for assumptions that:
- Are outdated (true 5 years ago, not today)
- Are self-imposed (policies we created but treat as immutable)
- Have hidden "all or nothing" thinking (assumes no middle ground)
- Reflect past trauma (one bad experience shaped current belief)

When you find a false assumption, you've found the breakthrough. Ask: "If this assumption is wrong, how could we satisfy both B and C?"

Example: Challenge "different technologies can't talk to each other reliably." Counter: modern APIs, containers, and service boundaries make polyglot systems common and reliable at scale (see: Netflix, Amazon, Uber).

### Step 7: Develop Injections

**Create solutions (injections) that invalidate the false assumption and satisfy both needs simultaneously.**

An injection is a new idea, policy, or action that makes the conflict disappear by breaking the logical necessity of the conflict.

Good injections:
- Directly invalidate a specific false assumption
- Enable both D and D' simultaneously (or enable both B and C through a new path)
- Are actionable (you can implement them)

Example injection: "Implement API contracts and observability standards while allowing technology choice within teams." This breaks the assumption that standardization is the only path to reliability.

## Example

**Product team conflict: build new features vs. pay down technical debt**

**Cloud diagram:**
- A (Goal): "Grow revenue and market share sustainably"
- B (Need): "Attract new customers with compelling features"
- D (Want): "Prioritize new feature development"
- C (Need): "Maintain system stability and developer velocity"
- D' (Want): "Allocate 50% of capacity to technical debt"

**Key assumptions surfaced:**
- "New features are the only way to attract customers" (B→D)
- "Technical debt requires dedicated time blocks to address" (C→D')
- "Features and tech debt are separate work streams" (both)

**False assumption identified:** "Technical debt requires dedicated time blocks to address."

**Reality:** Tech debt can be paid down incrementally within feature work through refactoring, better design, and automated testing.

**Injection:** "Implement a 'boy scout rule' (leave code better than you found it) with quality gates that prevent new debt, while building features. Reserve 20% capacity for large refactorings only."

**Result:** Both needs satisfied—features ship with improving code quality, debt decreases over time without halting feature work.

## Anti-Patterns

**Compromising instead of evaporating**: "Let's do 50% features, 50% tech debt" doesn't challenge assumptions—it just splits the difference. Both needs remain partially unsatisfied.

**Accepting the conflict as reality**: "Some conflicts can't be resolved" is premature. If the dilemma persists, you haven't found the false assumption yet.

**Stopping at surface-level assumptions**: "We assume standardization helps" is too vague. Dig deeper: "We assume that without central mandates, teams will choose incompatible technologies that can't integrate."

**Creating clouds for non-conflicts**: If one side is objectively wrong or if there's no shared goal, you don't have a dilemma worth evaporating—you have a decision to make.

**Choosing sides prematurely**: The Cloud requires suspending judgment and treating both needs as legitimate. If you've already decided D is right, you'll miss the assumptions.

**Invalidating assumptions without injections**: Identifying false assumptions feels like progress, but without actionable injections, nothing changes.

**Over-engineering solutions**: The best injections are often simple and obvious in hindsight. Don't add complexity if a straightforward change breaks the assumption.

## Related Frameworks

- **Current Reality Tree** (TOC): Diagnoses the core problem; Evaporating Cloud resolves the conflict perpetuating it
- **Future Reality Tree** (TOC): Validates that your injection actually works without creating new problems
- **Five Focusing Steps** (TOC): Systematic constraint removal; Cloud resolves conflicts about where to focus
- **Integrative Bargaining** (Negotiation Theory): Win-win negotiation approach; Cloud provides structure for finding integrative solutions
- **Polarity Management**: Managing ongoing tensions that can't be "solved"; Cloud finds new approaches to chronic dilemmas
- **Double-Loop Learning** (Argyris): Questioning underlying assumptions to change behavior; Cloud is a structured double-loop tool
- **Lateral Thinking** (de Bono): Breaking established patterns; Cloud systematically identifies which patterns to break
