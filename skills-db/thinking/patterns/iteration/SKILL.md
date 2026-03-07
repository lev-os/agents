---
name: iteration
description: Build, test, learn, and refine in rapid cycles when uncertainty is high and perfect upfront design is impossible
---

# Iteration

## Overview

Iteration is a fundamental process of repeated refinement where you build something, test it against reality, extract lessons, and improve in successive cycles. Unlike waterfall approaches that attempt complete planning before execution, iteration embraces uncertainty by accepting that early versions will be incomplete or flawed. The power comes from rapid feedback loops: each cycle surfaces problems, validates assumptions, and guides the next increment.

Core to Agile software development, design thinking, lean startup methodology, and scientific experimentation, iteration transforms discovery from a one-time event into a continuous process. Rather than pursuing perfection through analysis paralysis, iterative development delivers working prototypes quickly, learns from real usage, and evolves toward optimal solutions through evidence-based refinement.

## When to Use

- **High uncertainty**: Requirements unclear, technology unproven, user needs unknown
- **Complex problems**: Solution space too large to analyze exhaustively upfront
- **Learning by doing**: Hands-on experimentation reveals insights impossible to predict
- **Tight feedback loops available**: Can test, measure, and learn quickly (hours/days, not months)
- **Acceptable risk**: Early failures won't cause catastrophic harm
- **Evolving requirements**: Customer needs, technology, or market conditions changing rapidly

## The Process

### Step 1: Define Iteration Goal and Scope

Clarify what you're trying to learn or improve in this cycle. Keep scope small enough to complete in days or weeks.

**Goal types**:
- **Feasibility test**: "Can we technically build X?"
- **Usability validation**: "Will users understand this interface?"
- **Performance benchmark**: "Does this architecture handle 10K requests/sec?"
- **Market validation**: "Will customers pay for this feature?"
- **Risk reduction**: "What's the biggest unknown we need to resolve?"

**Scope constraints**:
- **Time-boxed**: 1-4 week sprints (Agile), 1-day design sprints
- **Feature-limited**: Minimum viable version, single use case
- **Throwaway allowed**: Prototype may be discarded after learning

**Example - Mobile app feature**:
- Goal: Validate if users want photo editing filters
- Scope: 3 basic filters, single-screen UI, fake processing (wizard-of-oz)
- Time: 1-week sprint
- Success metric: 60%+ of testers apply filter to photo

### Step 2: Build Minimum Testable Version

Create simplest artifact that enables testing your hypothesis. Prioritize speed over completeness.

**Fidelity levels** (choose lowest sufficient):
- **Paper prototype**: Sketches, wireframes, storyboards (hours to create)
- **Clickable mockup**: Figma/InVision prototype with simulated interactions (days)
- **Functional prototype**: Working code with hardcoded data, limited paths (week)
- **MVP (Minimum Viable Product)**: Deployable version with core functionality (weeks)

**Example iterations**:
- **Iteration 1**: Paper sketches of filter UI → test with 5 users (1 day)
- **Iteration 2**: Figma clickable prototype → remote user tests (3 days)
- **Iteration 3**: iOS app with 3 filters, real photo processing (1 week)

**Key principle: Build the minimum needed to test your riskiest assumption, not the minimum shippable product.**

### Step 3: Test with Real Users/Conditions

Expose prototype to actual use, measuring outcomes against success criteria.

**Testing methods**:
- **User testing**: Watch people use prototype, observe friction points
- **A/B testing**: Compare variant A vs B with live traffic
- **Surveys**: Post-use questionnaires on satisfaction, intent to use
- **Analytics**: Quantitative metrics (click rates, time-on-task, completion %)
- **Technical benchmarks**: Load tests, performance profiling, error rates

**Sample size guidance**:
- Qualitative feedback: 5-8 users per iteration (Nielsen Norman Group)
- Quantitative metrics: 100+ users for statistical confidence
- A/B tests: Thousands for small effect sizes

**Example - Filter feature test**:
- Recruit 8 users via UserTesting.com
- Task: "Edit this photo to make it look vintage"
- Observe: Did they find filters? Which did they try? Confusion points?
- Measure: Task success rate, time to complete, satisfaction score

### Step 4: Analyze Results and Extract Insights

Identify patterns in data, separate signal from noise, form actionable hypotheses.

**Analysis questions**:
- **What worked?** Features/designs that met or exceeded goals
- **What failed?** Pain points, confusion, errors, abandonment
- **What surprised us?** Unexpected user behaviors, edge cases
- **What assumptions were wrong?** Invalidated hypotheses
- **What new questions emerged?** Unknowns revealed by testing

**Insight documentation**:
- Quantitative: "42% couldn't find filter menu" (failure)
- Qualitative: "Users expected swipe gesture, not button tap" (insight)
- Hypothesis: "Adding visual affordance (icon animation) will increase discoverability"

**Example findings**:
- 70% applied filters successfully (exceeds 60% goal)
- "Vintage" filter most popular (50% of uses)
- Users confused by "Adjust intensity" slider (only 20% found it)
- Insight: Filters work, but advanced controls need redesign

### Step 5: Prioritize Changes for Next Iteration

Rank improvements by impact and effort, select highest-leverage items for next cycle.

**Prioritization frameworks**:
- **RICE score**: Reach × Impact × Confidence / Effort
- **Impact/Effort matrix**: Plot on 2×2 grid, prioritize high-impact/low-effort
- **Kano model**: Separate must-haves, performance features, delighters
- **ICE score**: Impact × Confidence × Ease (0-10 scale each)

**Example prioritization**:
1. **High priority**: Fix intensity slider discoverability (high impact, low effort)
2. **Medium**: Add 2 more popular filters (medium impact, medium effort)
3. **Low**: Professional color grading tools (low confidence users want it)
4. **Defer**: Social sharing integration (out of scope for filter validation)

### Step 6: Refine and Repeat

Implement changes, run next iteration with updated prototype, continue cycle until goals met.

**Iteration velocity**:
- **Daily iterations**: Paper prototypes, quick mockups (design thinking)
- **Weekly sprints**: Functional prototypes, user testing rounds
- **2-4 week sprints**: Agile software development standard
- **Monthly cycles**: Hardware prototypes, physical products

**Stopping conditions**:
- **Goal achieved**: Success metrics consistently met across tests
- **Diminishing returns**: Improvements plateau, effort outweighs gains
- **Pivot required**: Fundamental assumption invalidated, need different approach
- **Market launch**: MVP ready for real-world deployment

**Example - 3 iterations**:
- **Iteration 1**: Paper → Found users confused by icon-only buttons
- **Iteration 2**: Clickable prototype with labels → 70% task success
- **Iteration 3**: Functional app → 85% success, ready to build full version

### Step 7: Integrate Learnings into Final Design

Synthesize insights across iterations into production-ready implementation or next phase.

**Integration activities**:
- **Document patterns**: What worked across iterations (design system, best practices)
- **Capture edge cases**: Rare scenarios discovered during testing
- **Performance baselines**: Established benchmarks from prototypes
- **Technical debt inventory**: Quick hacks in prototypes needing refactoring
- **Roadmap updates**: New features/improvements revealed by user feedback

**Example - Final integration**:
- 3 core filters validated → ship in v1.0
- Intensity slider redesigned with visual preview
- 4 edge cases documented (landscape photos, low-res images)
- Deferred 5 "nice-to-have" features for v1.1 roadmap

## Common Pitfalls

**Iterating without clear goals** - Cycles become aimless improvements without progress toward measurable outcomes. Define success criteria upfront.

**Too large iteration scope** - 6-month "iterations" aren't iterations, they're mini-waterfalls. Keep cycles short (days to weeks).

**No real testing** - Internal review by team isn't iteration. Need actual users, real usage conditions, objective metrics.

**Ignoring qualitative insights** - Analytics show what users do, not why. Supplement quantitative with observational research.

**Perfectionism in prototypes** - Spending weeks polishing a throwaway prototype defeats the purpose. Build just enough to test.

**Not documenting learnings** - Insights lost between iterations. Maintain research repository, log decisions, track invalidated assumptions.

**Analysis paralysis between iterations** - Overthinking small changes. Implement, test, learn. Don't debate for weeks what one user test could answer in hours.

## Real-World Applications

**Agile software development**: 2-week sprints, daily standups, sprint retrospectives for continuous improvement. Working software every iteration.

**Design thinking**: IDEO's process - empathize, define, ideate, prototype, test. Multiple prototype-test cycles before final design.

**Lean startup**: Build-Measure-Learn loop. Ship MVPs, measure actual usage, pivot or persevere based on evidence.

**Scientific method**: Hypothesis → experiment → analyze results → refine hypothesis. Iteration is how science advances knowledge.

**Hardware engineering**: Rapid prototyping with 3D printing, CNC machining. Test physical designs, iterate mechanical/electrical before tooling.

## Key Insights

Iteration is fundamentally about **learning velocity** - how fast can you convert ignorance into knowledge? Traditional planning assumes you can think your way to the right answer. Iteration assumes reality is too complex, so you probe it repeatedly, building understanding incrementally.

**When iteration works best**:
- Problem is complex (many interdependent variables)
- Feedback loops are fast (hours/days)
- Cost of experiments is low (prototypes cheap, changes easy)
- Failure is acceptable (early mistakes don't cause catastrophic harm)

**When iteration struggles**:
- Feedback is slow (years to get results)
- Experiments are expensive (bridge collapses, drug trials)
- Requirements are fixed (regulatory, physics constraints)
- Integration costs are high (changing one part breaks entire system)

**The paradox**: Iteration feels slower initially (multiple cycles vs. one big push) but reaches better solutions faster overall by avoiding wrong paths early. First iteration ships in days/weeks. Waterfall might plan for months then discover fundamental flaw at launch.

**Modern trend**: Continuous deployment takes iteration to extreme - deploy code changes to production multiple times per day, measure impact, roll back instantly if needed. Iteration interval approaches zero.

The ultimate goal isn't perfection in iteration N - it's learning fast enough that iteration N+1 is substantially better than N. Velocity of learning beats depth of analysis.
