---
type: plan-impl
status: draft
priority: 2
slug: stable-domain-name
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
owner: domain-owner
plan_depth: light | standard | deep
source_refs: []
fidelity_score: 0.0
review_state: unreviewed | needs_review | approved | implementation_handoff
first_slice: null
open_decisions: []
done_condition: "Observable completion condition"
steps:
  - description: "Claim-shaped step"
    validation: "Check that proves the claim"
acceptance_criteria: []
gates: []
---

# Plan: Title

## How To Fill This Out

Use `light`, `standard`, or `deep` from `/lev-plan`. Preserve capture intent IDs
and source refs; delete unused placeholder rows rather than leaving template text.

This is a human runbook and broad execution source. `/propose` derives a compact
slice map or one task packet from it; task packets never replace this plan.

Adapt detail to `plan_depth`. Light plans may collapse sections. Deep plans must
retain every material section and the source-fidelity table.

## Source Context and Fidelity

Sources: capture, design, prior art, current code/docs, external authority.

| Intent ID | Source requirement | Plan destination | Preservation | Fidelity | Note / approval |
|---|---|---|---|---:|---|
| `INT-*` | Goal, constraint, non-goal, decision, acceptance, or relationship | Section/slice/decision/deferment | preserved | 1.00 | — |

No material row may be lost. Narrowing requires explicit approval.

## Outcome

Operator-visible result and why it matters.

## Done Condition

Deterministic or observable completion condition.

## Current

Evidence-backed current state, authority, freshness, and known uncertainty.

## Ideal

Target state and the minimal transition required.

## Scope, Non-Goals, and Authority

- In scope
- Out of scope
- Human decisions
- Forbidden moves
- Source and consumer ownership boundaries

## Decision Drivers and Options

| Option | Benefits | Costs / risks | Invalidated by | Ruling |
|---|---|---|---|---|
| A | | | | |
| B | | | | |

Chosen approach and explicit tradeoffs.

## Current-to-Target Map

| Current | Target | Action | Owner / gate |
|---|---|---|---|
| | | keep / change / migrate / retire | |

## Dependency and Slice DAG

```text
S1 -> S2 -> S3
```

| Slice | Covered intent IDs | Outcome | Owner | Depends on | Proof | Status | Open decisions |
|---|---|---|---|---|---|---|---|
| S1 | | | | | | ready | |

## Acceptance and Verification

| Claim / acceptance | Failure mode | Local proof | Integration/field/external proof |
|---|---|---|---|
| | | | |

## Risks and Pre-Mortem

| Failure | Mechanism | Prevention | Detection | Residual risk |
|---|---|---|---|---|
| | | | | |

Deep/high-risk plans include three credible pre-mortem scenarios and the relevant
unit, integration, e2e, and observability test shape.

## Rollback and Review Triggers

- Rollback action and evidence required.
- Architecture review threshold.
- External or human approval boundary.

## First Executable Slice

Name one vertical, reversible slice and its proof. Route it to `/propose map` or
`/propose emit <slice-id>` only after plan readiness passes.
