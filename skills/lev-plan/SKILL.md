---
name: lev-plan
description: Compile captured or designed intent into a source-faithful Lev plan, deepen or review an existing plan, and manage its lifecycle under `.lev/pm/plans/`. Use for human runbooks, migrations, architecture plans, multi-slice roadmaps, plan review, or plan state transitions; use `propose` afterward to map or emit execution slices.
---

# /lev-plan - Plan Compilation and Lifecycle

`lev-plan` is the missing compilation lane between captured/design intent and
execution proposal. It preserves the source fidelity table, explains current and
target state, resolves architecture and ownership, builds a dependency/slice map,
and records human-readable execution and rollback. It also manages the plan FSM.

It is not merely a frontmatter generator. A schema-valid shallow plan is still a
failed plan.

## Work Link

Lifecycle lane: Plan
Entity movement: `captured | designed | draft_plan -> planned | needs_interview | needs_review`
Workstream: resolve active workstream before plan writes
Upstream: `/capture`, `/interview`, `/prior-art`, existing plan
Downstream: `/auto-enrich`, `/propose`, `/work`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Modes

| Mode | Trigger | Result |
|---|---|---|
| Compile | Captured/design intent or explicit `create` | One new plan, or update the existing matching plan |
| Deepen | `deepen <plan>` or an existing shallow plan | Patch the named plan in place; never create a parallel version |
| Review | `review <plan>` or “is this plan ready?” | Fidelity/readiness verdict; no write unless authorized |
| Lifecycle | list/show/transition/validate | FSM operation only |

Default to review without writing when the user asks what the plan should contain,
requests an audit, or has not authorized a durable plan edit.

## Plan Depth

| Depth | Use when | Required shape |
|---|---|---|
| `light` | One obvious bounded change | Goal, scope, steps, proof; suggest skipping the plan if execution is clearer |
| `standard` | One feature or coherent multi-step change | Source fidelity, current/target, boundaries, steps, risks, verification |
| `deep` | Migration, architecture, security, destructive work, 3+ authorities, or multi-slice roadmap | Full contract below, options/tradeoffs, DAG, pre-mortem, rollback, review |

Do not inflate a light plan. Do not compress deep work into a list of activities.

## Compilation Protocol

```yaml
steps:
  - id: bind_source
    action: Resolve workstream, capture/design refs, existing matching plan, source digests, and allowed planning write scope.
    validation: "Every material intent has an intent_id and source_ref; existing plan is reused when present."
    on_failure: "Route conversation-only work to /capture; unresolved product/architecture decisions to /interview."

  - id: rehydrate_fidelity
    action: Load the capture source-fidelity table and map every material row to a plan section, decision, deferment, or explicit conflict.
    validation: "No material row is lost; plan fidelity is >= 0.90 and not lower than capture fidelity."
    on_failure: "Repair capture or ask one decision question; do not draft around missing intent."

  - id: inspect_current_state
    action: Inspect current code, docs, rules, plans, dependencies, dirty work, and external authority needed for the plan.
    validation: "Current-state claims are observed or labeled stale/assumed; load-bearing claims cite exact refs."
    on_failure: "Route to /prior-art or keep the claim unknown."

  - id: choose_depth
    action: Select light, standard, or deep from risk and topology; state the selection in the plan.
    validation: "Depth matches the real blast radius and does not use length as a proxy for rigor."

  - id: frame_outcome
    action: Define operator outcome, observable done state, scope, non-goals, authority boundaries, and human decisions.
    validation: "A teammate can tell what changes, what stays unchanged, and what done looks like."

  - id: analyze_options
    action: For standard/deep plans, compare at least two meaningful approaches or record evidence that alternatives are invalid.
    validation: "Decision drivers, tradeoffs, sacrificed attributes, and chosen approach are explicit."

  - id: build_topology
    action: Build current-to-target map, ownership boundaries, dependencies, slices, critical path, promotion gates, and administrative holds.
    validation: "Every slice has an outcome, owner, depends_on, proof, status, open decisions, and covered intent_ids."

  - id: design_proof
    action: Map each acceptance claim to the smallest relevant local, integration, field, or external-owner verifier.
    validation: "At least 90% of acceptance criteria are concrete/testable; missing future tests are slice work, not false blockers."

  - id: design_failure_and_rollback
    action: Record credible failure mechanisms, prevention/detection, residual risk, rollback, and architecture review triggers.
    validation: "High-risk/deep plans include a three-scenario pre-mortem and unit/integration/e2e/observability test shape where applicable."

  - id: write_or_patch
    action: Write one plan under .lev/pm/plans/ only inside authorized scope, preserving unrelated plan history and current dirty work.
    validation: "Exactly one plan is created or updated; source refs and fidelity table are durable."

  - id: review_ready
    action: Run deterministic structure/ref checks, then semantic weak-link review. Use /auto-enrich for explicit or deep/high-risk hardening when available.
    validation: "No readiness dimension is insufficient; deterministic success is reported separately from semantic approval."

  - id: route_forward
    action: Route approved plans to /propose map or /propose review; emit no task folders.
    validation: "The first executable slice is named and the broad plan remains its source."
```

## Source Fidelity Gate

Reuse the five capture components:

```
fidelity = 0.30*detail_preservation
         + 0.25*relationship_preservation
         + 0.20*source_attribution
         + 0.15*neighbor_context
         + 0.10*actionability
```

The plan must contain this table for every material capture/design row:

| Intent ID | Source requirement | Plan destination | Preservation | Fidelity | Note / approval |
|---|---|---|---|---:|---|
| `INT-*` | Goal, constraint, non-goal, decision boundary, acceptance, or relationship | Section/slice/decision/deferment | `preserved`, `narrowed-approved`, `deferred-explicit`, `conflict`, `lost` | 0.00-1.00 | What changed and who approved it |

Rules:

- `lost` blocks planning.
- `narrowed-approved` requires an explicit source/user decision.
- Every material relationship and non-goal gets its own coverage, not just goals.
- Overall fidelity must be at least 0.90 and must not be lower than the source capture.
- An average cannot hide one missing material row.

## Plan Contract

Every standard/deep plan includes, adapting headings to the domain:

1. Source context and fidelity table.
2. Outcome and observable done condition.
3. Current state with evidence and freshness.
4. Target state and current-to-target map.
5. Scope, non-goals, authority, and forbidden moves.
6. Decision drivers, options, tradeoffs, and rejected alternatives.
7. Ownership/container/component boundaries where architecture matters.
8. Dependency and slice DAG with critical path.
9. Per-slice outcome, proof, status, covered intent IDs, and open decisions.
10. Acceptance/claim-to-verifier map.
11. Risks, pre-mortem where required, mitigation, detection, and residual risk.
12. Rollback and architecture review triggers.
13. First executable slice and next lifecycle route.

Deep evidence targets, borrowed from demonstrated planning practice:

- At least 80% of load-bearing current-state claims cite exact files, lines, commands,
  or external authority refs.
- At least 90% of acceptance criteria are observable/testable.
- A plan is not complete merely because required headings exist.

## Semantic Readiness

Judge each dimension `insufficient`, `sufficient`, or `strong`; use the weakest
dimension for the verdict:

1. source fidelity
2. outcome demonstrability
3. current-state evidence and freshness
4. scope/non-goal/authority clarity
5. option and tradeoff quality
6. ownership and dependency quality
7. slice verticality and DAG coherence
8. verifier relevance
9. rollback and failure handling
10. cold-start context sufficiency
11. implementation simplicity

Verdicts:

- `ready`: every dimension is at least sufficient, fidelity passes, and no decision
  blocker remains.
- `needs_review`: planning-local gaps are repairable in the named plan.
- `needs_interview`: a human product, architecture, authority, or irreversible
  decision is unresolved.
- `implementation_handoff`: the next uncertainty requires a spike/runtime proof,
  not more plan prose.

## Auto-Enrich Integration

`auto-enrich` works after source fidelity exists. It is a hardener, not a capture
replacement.

- Existing deep/high-risk plan: enrich the named plan in place, preserving fidelity.
- Existing design without a plan: enrich decisions, then compile with `lev-plan`
  before proposal slicing when work is multi-slice or cross-authority.
- Raw conversation: run `/capture` first.
- After every auto-enrich edit, recompute the plan fidelity table; no material row may
  disappear while architecture quality improves.
- Approval by an Architect/Critic loop is semantic evidence, not execution authority.

## Plan Types and Files

| Type | Pattern | Purpose |
|---|---|---|
| `plan-impl` | `plan-impl-*` | Feature or capability delivery |
| `plan-bugfix` | `plan-bugfix-*` | Defect investigation and resolution |
| `plan-chore` | `plan-chore-*` | Maintenance, cleanup, docs, tooling |
| `plan-research` | `plan-research-*` | Investigation with knowledge output |
| `plan-migration` | `plan-migration-*` | Transition between well-defined system shapes |

Required frontmatter remains backward-compatible:

```yaml
---
type: plan-impl
status: draft
priority: 2
slug: stable-kebab-name
created_at: YYYY-MM-DD
done_condition: "observable deterministic completion"
steps:
  - description: "claim-shaped step"
    validation: "check that can prove the claim"
acceptance_criteria: []
gates: []
---
```

New or materially updated standard/deep plans should also include:

```yaml
plan_depth: standard | deep
source_refs: []
fidelity_score: 0.0
review_state: unreviewed | needs_review | approved | implementation_handoff
first_slice: stable-slice-id | null
open_decisions: []
```

## Lifecycle FSM

```text
draft -> ready -> in_progress -> needs_validation -> validated -> done -> archived
                         |              |
                         +-> blocked    +-> ready on failed validation
```

Transitions:

- `draft -> ready`: source fidelity and semantic readiness pass; first slice exists.
- `ready -> in_progress`: an executor claims the plan or an emitted task references it.
- `in_progress -> needs_validation`: implementation is complete, not merely attempted.
- `needs_validation -> validated`: fitness functions and acceptance pass.
- `validated -> done`: move to `_done/` when no remaining plan work exists.
- `in_progress -> blocked`: concrete code/decision dependency prevents progress.
- `done -> archived`: historical reference only.

## Operations

```bash
lev loop --json
bd show <bd_id>
bd create --title="Implement feature X" --type=task -p 2
bd close <bd_id> --reason "completed per plan"
```

Update `status` in frontmatter for transitions. On validated completion, move the
plan to `.lev/pm/plans/_done/`. Do not create a second plan to represent a state
transition.

## Output

<plan-review>
## Plan: {slug}

Verdict: {ready|needs_review|needs_interview|implementation_handoff}
Depth: {light|standard|deep}
Source fidelity: {score}; lost rows {count}; narrowed rows {count}
Outcome: {operator_visible_result}
Current -> target: {one_sentence_transition}
First slice: {slice_id}; {outcome}; proof {verifier}
Weakest point: {dimension}; {reason}
Open decisions: {none_or_list}
Artifact: {plan_ref}
Next: {/auto-enrich|/propose map|/interview|implementation spike}
</plan-review>

## Red Flags

- "The frontmatter validates, so the plan is ready."
- "The conversation was long; the plan can summarize aggressively."
- "The task list preserves the roadmap."
- "The first slice is clear, so other source requirements can stay in chat."
- "Smaller blast radius means a migration plan is higher quality."
- "Auto-enrich can recover details that capture omitted."
- "Architect approval means execution is authorized."
- "Every alternative is shallow, so I do not need to name why."
- "The executor can decide the open product boundary."
