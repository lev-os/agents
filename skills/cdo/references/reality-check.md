---
name: cdo-reality-check
description: reality modifier. Measure what is built against the stated vision, then bridge every gap.
---

# Reality Check (`reality` modifier)

Method source: the reality-check-for-project skill from jeffreys-skills.md. Its
text is not copied here; this leaf states the method in CDO terms.

Use when the user asks where a project really stands, what is missing, or
whether the work so far delivers the vision. Its purpose is to steer a long run
back toward its goals, not only to audit it.

## Principle

Documents state the promise. Code, tests and what has actually shipped state
the truth. The output is the gap between them.

## Turn 0: the vision checklist

Read the README, AGENTS.md, and every plan, spec, design or roadmap document.
Write a numbered checklist of concrete, testable goals, each with its source
line. Then, for each goal: find the code that should implement it, read it,
check its tests and whether they pass, run it when feasible, and check what has
shipped rather than what only sits in a branch.

| Status | Meaning |
|---|---|
| working | Code exists, tests pass, and end-to-end behavior was observed |
| partial | Part of the goal is implemented |
| stub | Only a placeholder or mock exists |
| unproven | Code exists without tests that cover it |
| not_started | No code exists |
| regressed | It worked before and is broken now |
| untracked | No open work item covers the goal; this is the most important gap |
| wrong_approach | It is built in a way that cannot reach the goal |

Check coverage goal by goal against the tracker (`bd` or `.lev/pm` tasks). A
completion percentage can hide a goal that nothing covers.

## Turns after Turn 0

| Turn | Agents | Output |
|---|---|---|
| T1 | One per-entity expert per goal cluster, plus a negotiate agent | A status with evidence for every goal |
| Synthesis | Gap analysis by category: vision (no tracked item, so create one), implementation (stub or partial, so finish it), proof (no tests, so add them), performance (misses targets, so profile), integration (works alone only, so add end-to-end tests), design (wrong approach, so redesign) | A directive aimed at the worst gaps |
| T2 | Bridge planners | For each gap: the change, its owner, its verification and its dependencies |
| T3 onward | Ambition waves, then refinement waves | See below |

**Ambition waves** (one to three) push the bridge plan beyond incremental fixes.
First inject project-specific depth, such as named skills, relevant methods or
mathematics, and quantitative targets; then ask for a bolder revision. Ambition
applies to the plan. A new factual claim still needs evidence.

**Refinement waves** apply one fixed checklist to every plan item: does it make
sense, is it the best option, what would serve users better, does it keep every
feature, and does it include unit tests, end-to-end tests and useful logs.
Revise the same plan in place rather than starting a new document. Plan four to
five refinement waves by default. Stop early when a full wave changes nothing, or
when the budget ends.

**Tracked work comes before code.** Convert the bridge plan into tracked work
(`bd`, or the Lev lifecycle via `/work`) before any implementation: one item per
gap, each with its verification, and a companion test item for every
implementation item. After the ambition waves, regenerate the items from the
revised plan, then refine. When the gap list is short, resolve the gaps directly
and say so. Close an item only with proof that the fix works.

Order: vision checklist, bridge plan, tracked items, ambition waves, regenerated
items, refinement waves, then implementation.

With `judge`, the vision checklist is the acceptance criteria. With `plan`, the
waves above become the planned waves.
