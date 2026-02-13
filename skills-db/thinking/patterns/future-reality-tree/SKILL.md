---
name: Future Reality Tree
description: A logical diagram that validates proposed solutions by mapping their cause-effect impacts, ensuring they resolve problems without creating new undesirable effects
---

## Overview

The Future Reality Tree (FRT) is the third of the five thinking processes in Eliyahu Goldratt's Theory of Constraints. After diagnosing the core problem with a Current Reality Tree and developing breakthrough solutions with an Evaporating Cloud, the FRT tests whether your proposed changes will actually work.

The FRT is a "what-if" simulation using cause-and-effect logic. It maps how your proposed injections (solutions) will cascade through the system to produce Desirable Effects (DEs) while checking for negative side effects (Negative Branches). This prevents the common mistake of implementing well-intentioned solutions that backfire.

Unlike traditional planning that lists expected benefits, the FRT requires rigorous logical proof. Each step must pass sufficiency tests: does this entity truly cause the next? Are we missing intermediate effects? This discipline catches flawed assumptions before implementation, when they're expensive to fix.

The FRT serves two critical functions: 1) Validate that solutions address root causes, and 2) Identify unintended consequences early enough to modify the approach.

## When to Use

Apply the Future Reality Tree when:

- You've identified a core problem (via CRT) and developed a solution (via Evaporating Cloud) and need to validate it will work
- Proposed changes are complex with multiple stakeholders and potential ripple effects
- Past solutions have created unexpected negative consequences and you want to avoid repeating that pattern
- You need to build buy-in by demonstrating logically how changes will produce desired outcomes
- The solution challenges established policies or practices and you face skepticism
- Implementation costs/risks are high enough to warrant thorough pre-validation

Don't use this framework for:

- Small, reversible experiments where "try it and see" is faster than extensive analysis
- Solutions with obvious, linear outcomes (FRT is for complex system changes)
- Situations where you're still identifying the problem (use CRT first)
- Time-critical decisions that can't wait for thorough analysis

## Process

### Step 1: Define Injections (Proposed Changes)

**Clearly state the actions, policies, or changes you plan to implement.** These are the injections from your Evaporating Cloud analysis or other solution design work.

Be specific and actionable: "Implement weekly cross-functional planning meetings with product, engineering, and design" not "improve communication."

Each injection should address an identified root cause from your CRT. If you're creating an FRT without first doing a CRT, you're likely solving symptoms.

Example injection: "Allocate 20% of engineering sprint capacity to technical quality improvements, tracked separately from feature work."

### Step 2: List Desired Effects (DEs)

**Identify the specific positive outcomes you want to achieve.** These should directly map to eliminating the Undesirable Effects (UDEs) from your Current Reality Tree.

Make DEs measurable and observable: "Bug backlog decreases 30% in 6 months" not "better quality." This allows post-implementation validation.

Include both immediate and downstream effects: fixing technical debt (DE1) → faster feature delivery (DE2) → increased customer satisfaction (DE3).

Typical FRT targets 5-10 major DEs. If you have 30, you're either tackling too much at once or listing granular sub-effects that belong in the causal chain.

### Step 3: Build the Causal Chain

**Map how injections logically produce DEs through intermediate effects.** Start from each injection and trace forward: if we do X, what happens next? And then what?

Use the same rigorous logic as the CRT. For each arrow, ask: "Does this entity alone cause the next? Or do we need additional factors?" If additional factors are needed, add them to the diagram (use "and" logic).

Connect entities with arrows showing causality. The tree grows upward from injections (at the base) to DEs (at the top), with intermediate effects in between.

Check for sufficiency at each step: "If we have this injection, does it truly produce this intermediate effect? Always? Or only under certain conditions?" Document assumptions.

### Step 4: Scan for Negative Branches

**Actively search for unintended negative consequences.** For each injection and intermediate effect, ask: "What else could this cause? What bad things might happen?"

This is critical. The human tendency is to see only the benefits of our own ideas. Force yourself to find problems.

When you identify a potential Negative Branch (NB)—an undesirable effect caused by your injection—add it to the tree with a different visual marker (often dashed lines or different colors).

Example: Injection = "Mandate code reviews for all changes." Positive: better code quality. Negative Branch: slows down urgent hotfixes, creates bottleneck if too few reviewers, generates interpersonal conflict over criticism.

### Step 5: Trim Negative Branches

**Modify injections or add new ones to prevent negative effects.** Don't ignore NBs hoping they won't happen—they will.

Options for trimming:
- **Refine the injection**: "Mandate code reviews for all changes except documented emergency hotfixes" (addresses the urgent fix problem)
- **Add a new injection**: "Train 5 additional senior engineers as reviewers and distribute load" (addresses bottleneck)
- **Add monitoring**: "Track review cycle time; escalate if >4 hours" (catches problems early)

Treat each NB as a mini-problem requiring its own solution. Add the trimming injection to your FRT and trace its effects.

Re-scan for new NBs introduced by your trimming injections. This is iterative—trimming one branch might create another.

### Step 6: Validate Completeness

**Check that the FRT addresses all original UDEs from your CRT.** Every problem you identified should have a corresponding solution and DE in the FRT.

If a UDE isn't addressed, either: 1) your injections are incomplete, or 2) that UDE wasn't actually caused by the core problem you identified (go back to CRT).

Ensure logical completeness: are there gaps in the causal chain? Places where "then magic happens" connects two entities? Fill those gaps.

Test with stakeholders: walk through the logic from injections to DEs. Do they buy it? Where do they see holes or risks?

### Step 7: Assess Implementation Readiness

**Use the FRT to identify obstacles and implementation requirements.** Look at the entities in your tree—what has to be true for them to occur?

This leads naturally into the next TOC thinking process tools (Prerequisite Tree for obstacles, Transition Tree for implementation steps).

Document assumptions clearly. These become hypotheses to test during implementation.

Create success metrics based on the intermediate effects and DEs. How will you know if the causal chain is playing out as predicted?

## Example

**Problem (from CRT):** Engineering team has growing bug backlog and declining velocity because they're constantly firefighting issues caused by technical debt.

**Injection (from Evaporating Cloud):** "Allocate 20% of sprint capacity to technical quality work, tracked separately from features."

**FRT causal chain:**
1. Injection → Engineers spend 1 day/week on refactoring, test coverage, automation
2. → Code quality gradually improves in high-churn areas
3. → Fewer bugs introduced in new features (DE1)
4. → Bug backlog begins decreasing (DE2)
5. → Less time spent firefighting → More predictable velocity (DE3)
6. → Faster feature delivery (DE4)
7. → Improved team morale (DE5)

**Negative Branch identified:**
- Injection → 20% less capacity for features → Short-term feature delivery slows → Product management pushes back → Initiative gets cancelled before benefits materialize

**Trimming injection:**
- "Communicate projected benefits timeline (3-month ROI) to product leadership and secure commitment before starting"
- "Start with 10% allocation for 1 sprint to demonstrate quick wins, then increase to 20%"

**Validation:** FRT shows that with proper expectation-setting and phased rollout, the injection will eliminate the core problem without creating new ones.

## Anti-Patterns

**Wishful thinking instead of logic**: Assuming "training → better performance" without intermediate steps. What specific knowledge/skills does training provide? How do those translate to performance? Be rigorous.

**Ignoring negative branches**: "Our solution is perfect; no downsides." Every intervention creates trade-offs. If you don't see them, you're not looking hard enough.

**Building FRTs for solutions that don't address root causes**: If your injection isn't connected to the core problem from your CRT, it won't fix anything. The FRT will show this—you won't be able to logically connect it to resolving UDEs.

**Making the tree too complex**: 100+ entities means you're either: 1) trying to solve too many problems at once, or 2) including excessive detail. Focus on major causal relationships.

**Treating the FRT as a guarantee**: The FRT is a logical model based on current understanding. Reality may differ. Use it to improve your solution, not to claim certainty.

**Skipping validation with stakeholders**: Building the FRT in isolation produces a beautiful diagram that doesn't survive contact with people who know the system intimately.

**Confusing correlation with causation**: "We'll implement agile and productivity will increase." Does agile alone cause increased productivity? Or do you need specific practices, cultural changes, training, tools, etc.? Map the actual causal mechanisms.

## Related Frameworks

- **Current Reality Tree** (TOC): Diagnoses the problem; FRT tests whether your solution fixes it
- **Evaporating Cloud** (TOC): Generates breakthrough solutions; FRT validates they'll work
- **Prerequisite Tree** (TOC): Next step after FRT—identifies implementation obstacles
- **Transition Tree** (TOC): Converts validated FRT into step-by-step implementation plan
- **Premortem Analysis**: Imagines how plans fail; FRT's Negative Branch analysis is similar but more structured
- **Theory of Change** (Program Evaluation): Maps interventions to outcomes in social programs; similar logic structure
- **Causal Loop Diagrams** (System Dynamics): Shows feedback effects over time; complements FRT's causal chains
- **Impact Mapping**: Product planning tool linking goals to deliverables; FRT is more rigorous about cause-effect logic
