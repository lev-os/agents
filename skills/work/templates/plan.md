---
type: plan-impl
status: crystallizing
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

This is a human runbook and broad execution source. `/lev-plan map` derives a
compact slice map and `/lev-plan emit <slice-id>` one task packet from it; task
packets never replace this plan.

Every plan keeps all eight parts. A light plan writes each part as one or two
lines and may join sections; it deletes a section only when the section truly
cannot apply, and says so in one line. Deep plans must retain every material
section and the source-fidelity table.
What each part must hold is in `/lev-plan`'s Plan parts, Slices, and Proof
references.

Intent: {one_sentence_intent}
Source: {capture|design|plan|task refs}; intent IDs {ids}
Plan: {plan_ref | plan_not_required: one_sentence_rationale}
Run: {bounded|long|parallel search}; limits {user stops, hard budgets, permissions}
Claims: {task_ref requirements | this plan's claims | proposed rows pending Emit}
State: {memory|disk:ref}; confidence {low|medium|high}; blocker {none|code_blocker|decision_blocker: reason}

## Source Context and Fidelity

Sources: capture, design, prior art, current code/docs, external authority.

| Intent ID | Source ref | Source requirement | Plan destination | Claim | Preservation | Fidelity | Note / approval | Route / blocker |
|---|---|---|---|---|---|---:|---|---|
| `INT-*` | | | | | | | | |

The rules for each cell are `/lev-plan`'s Source Fidelity Gate.

## Outcome

Success sentence: {what must be true of the returned result, with quantifiers, scope, and the narrowing assumptions it may not make}

Operator-visible result and why it matters. Observable done condition.

Definitions:
- {term}: {meaning}; degenerate cases {empty|trivial|duplicate|boundary}

Does Not Count:
- {near miss}: excluded by {claim_id | guard of claim_id | review checklist}

## Scope, Non-Goals, and Authority

- In scope
- Out of scope
- Human decisions
- Forbidden moves
- Source and consumer ownership boundaries

## Current

Evidence-backed current state, authority, freshness, and known uncertainty.

## Ideal

Target state and the minimal transition required.

## Decision Drivers and Options

| Option | Benefits | Costs / risks | Invalidated by | Ruling |
|---|---|---|---|---|
| A | | | | |
| B | | | | |

Chosen approach and explicit tradeoffs. What experts would do: one line for each domain that fits.

## Current-to-Target Map

| Current | Target | Action | Owner / gate |
|---|---|---|---|
| | | keep / change / migrate / retire | |

## Dependency and Slice DAG

```text
S1 -> S2 -> S3
```

| Slice | Covered intent IDs | Outcome | Owner | Allowed effects | Artifact | Depends on | Claims | Stop | Run budget | Status | Open decisions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | | | | | {path; format {version, frozen} when a long run reads it} | | {claim ids} | | {n worker runs} | ready | |

## Claims and Proof

| Claim | Sentence (must or must never) | Slice | Failure it rules out | Proof: program, agent, or person | Level: local, integration, field, or external | Guard | Source |
|---|---|---|---|---|---|---|---|
| | | | | {command | question | owner and evidence} | | {program: known-bad control and check owner; any: what looks like proof and is not} | |

Unresolved proof: {none | claim_ids}

## Review and Repair

Checklist: {domain failure modes; circularity analogue; degenerate values}
Blocks when: {named condition}; evidence {failing check | counterexample | reproduction}
Non-blocking: logged; never delays return
Outside-loop proof: {program claim_id | independent evidence or human review: claim_id, owner}; unresolved {none | claim_ids}
Review runs: {the review skill's chat line for each run, with its report file}
Recall: {slice}; failed claims {ids}; evidence {ref}; narrowed scope {scope}; acceptance {claims satisfied}; cap {n}
At cap or run budget: stop with the exact gap and runs {spent}/{budget}; narrow exit {smaller sentence + one open claim}; route {/interview | code_blocker | operator}

## Return and Resume

Return when: the success sentence holds, every claim is satisfied by its proof with evidence after the last edit, and no blocking finding is open.
Incomplete only on: explicit user stop, hard budget, or unavailable required evidence; strongest verified state plus exact gap.
Frontier: last passing slice {id} at {evidence_ref}; open claims {ids}; next unit {one ready coherent unit}

Open branches:
- {later branch}: {intent_id}; open because {reason}; owner {route}; size {worker runs; machine hours; what stays unproven}

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

Name one vertical, reversible slice and its proof. Route it to `/lev-plan map` or
`/lev-plan emit <slice-id>` only after plan readiness passes.

Packet: {preview from the packet reference, unvalidated and unemitted | not requested}; emission via `/lev-plan emit`
Launch: `lev entity task validate {task}`, then `lev sdlc exec {task} --flow {selected_flow}` | none until Emit
Next: {lev-plan emit {slice_id} | map | /exec | skill://poc | /interview | resume {unit}}
