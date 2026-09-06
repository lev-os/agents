---
name: lev-plan
description: Compile captured or designed intent into a source-faithful Lev plan, deepen or review an existing plan, and manage its lifecycle under `.lev/pm/plans/`. Use for human runbooks, migrations, architecture plans, multi-slice roadmaps, plan review, or plan state transitions; route SDLC packets to propose and non-coding work to its domain executor.
---

# /lev-plan - Plan Compilation and Lifecycle

`lev-plan` is the missing compilation lane between captured/design intent and
execution proposal. It preserves the source fidelity table, explains current and
target state, resolves architecture and ownership, builds a dependency/slice map,
and records human-readable execution and rollback. It also manages the plan FSM.

It is not merely a frontmatter generator. A schema-valid shallow plan is still a
failed plan.

`skill://lev-plan` loads this contract. Plans and their workstreams use durable
`lev://entity/work/plan/<plan-id>` and
`lev://entity/work/workstream/<workstream-id>` identities; later execution is
addressed separately as `lev://exec/<flow>`.

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
island/provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

## Work Link

Lifecycle lane: Plan
Entity movement: `captured | designed | draft_plan -> planned | needs_interview | needs_review`
Workstream: resolve active workstream before plan writes
Upstream: `/capture`, `/interview`, `/prior-art`, existing plan
Downstream: `/auto-enrich`, `/propose` for SDLC, `/exec` or domain skill for non-coding, `/lev`
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
    validation: "Decision drivers, tradeoffs, sacrificed attributes, and chosen approach are explicit; newly derived behavior is labeled proposed or left as an open decision, never promoted into settled source intent."

  - id: build_topology
    action: Build current-to-target map, ownership boundaries, dependencies, slices, critical path, promotion gates, and administrative holds.
    validation: "Every slice has an outcome, owner, depends_on, proof, status, open decisions, and covered intent_ids; each promotion verifier is satisfiable by that slice plus completed dependencies; a slice with incomplete or blocked dependencies is blocked, not ready or merely promotion-gated."

  - id: design_proof
    action: Map each acceptance claim to the smallest relevant local, integration, field, or external-owner verifier.
    validation: "At least 90% of acceptance criteria are concrete/testable; each verifier is attached to the first slice whose scope can satisfy it; every claimed preserved boundary or compatibility form is exercised directly; missing future tests are slice work, not false blockers."

  - id: design_failure_and_rollback
    action: Record credible failure mechanisms, prevention/detection, residual risk, rollback, and architecture review triggers.
    validation: "High-risk/deep plans include a three-scenario pre-mortem and unit/integration/e2e/observability test shape where applicable; rollback returns to the latest dependency-compatible state and cannot remove compatibility still required by incomplete slices."

  - id: write_or_patch
    action: Write one plan under .lev/pm/plans/ only inside authorized scope, preserving unrelated plan history and current dirty work.
    validation: "Exactly one plan is created or updated; source refs and fidelity table are durable."

  - id: review_ready
    action: Run deterministic structure/ref checks, then semantic weak-link review. Use /auto-enrich for explicit or deep/high-risk hardening when available.
    validation: "No readiness dimension is insufficient; deterministic success is reported separately from semantic approval."

  - id: route_forward
    action: Route approved SDLC plans to /propose map or review; sufficient non-coding plans to the domain skill or /exec. Emit no task folders or execution dispatch during planning.
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

## Shared Planning and TDD Contract

### Overlay and iteration planning

Classify the domain before applying software-delivery mechanics. Coding work
uses architecture review when boundaries are unresolved and proposal packets
for SDLC execution. Non-coding work can use this plan directly with its domain
executor; `propose` is optional unless the selected overlay requires a packet.

Prepare long-running efforts for one coherent unit per future Ralph iteration:
name the next ready chunk, its acceptance/claim checks, dependencies, permitted
effects and stopping condition. Prompt: "Do the next bit of work on this effort;
select ONE ready coherent unit, finish that single thing, record the result and
remaining frontier, then stop." One thing may be a substantial vertical chunk.
The outer loop reloads state and chooses whether to continue; `lev-ralph` adds a
worker/reviewer-fixer cycle within that unit. Plan creation does not run the loop.

Use existing plan `steps[].validation` / acceptance criteria and task
`claim_verifier_map` as claim sources. Preserve stable claim references when
projecting a packet. Dedicated `claim.yaml` and direct runtime ingestion of plan
claims are future work, not newly supported schema or CLI behavior.

### Shared substance and conditional TDD

Resolve or fetch every explicitly supplied local path, issue number, tracker URL,
or external URL through its owning source, then read the full artifact/body and
all accessible comments. Report inaccessible material instead of reconstructing
it. Preserve settled decisions about changed modules/interfaces, developer
clarifications, architecture, schemas, API contracts and interactions when
applicable. Additional notes belong only when they change execution or explain
a constraint; do not fill irrelevant headings.

TDD tests describe one logical behavior through the agreed public seam, using
domain vocabulary and independently derived expected values (spec examples,
known literals or a separate oracle). Avoid mirroring the implementation in the
assertion, private-method tests and side-channel checks that bypass the interface.
Prefer real internal collaborators; isolate external APIs, time/randomness and
necessary filesystem/database boundaries with existing adapters or test resources.
Use operation-specific boundary interfaces and injected dependencies where they
already fit; this is not permission to add abstractions solely for mocking.
Prefer an isolated test database when database behavior is the claim; otherwise
state what a boundary fake cannot establish. Each operation fake should expose
its expected response shape and exercised endpoint without conditional catch-all
setup, retaining the interface's type checks. Flag call-count/order assertions
and HOW-named tests when they merely couple to internals; observable protocol
ordering may itself be a legitimate contract. Check that behavior-preserving
internal refactoring would leave the test meaningful and green.
Treat every rule in this TDD subsection as active in every cycle: check it before
the first RED and again before selecting each next behavior. Work one behavior
through RED then GREEN before selecting another; GREEN adds only the current
cycle's production code needed to pass its test, with no anticipated tests or
features. A coherent Ralph unit may contain several sequential cycles. Keep
unrelated refactoring for review and an authorized follow-up; preserve the existing
frozen-test and isolation contract below.

Before forming a TDD packet, read the relevant `CONTEXT.md` when present and
applicable ADRs; record their refs and require test names plus public-interface
vocabulary to match them. Synthesize settled conversation decisions without
restarting an interview; expose only unresolved
choices that change scope or acceptance. Describe the user problem, intended
behavior, actors, exclusions and testing decisions without padding story counts.
Prefer the highest existing public test seam that actually observes the claim.
If none exists, propose a new seam at the highest viable public boundary; ask
only when that seam's tradeoff needs a user decision.

Reference current owner paths for executable handoff, with freshness context;
source advice to omit all paths is superseded by Lev's evidence-backed ownership.
When a prototype's state machine, reducer, schema or type shape expresses a
decision more precisely than prose, retain only that decision-rich snippet and
its prototype provenance, not the whole demo.

When uncertainty needs a prototype, route the question to `skill://poc`. Preserve
only its explicit question, selected logic/UI branch, stated assumptions, validated
answer, and provenance in the plan; prototype construction details remain owned by
`skill://poc`.

For wide mechanical changes that cannot land as independent vertical slices,
expand alongside the old form, migrate bounded caller batches while preserving
compatibility, then contract only after every migration dependency is satisfied
and no old caller remains. If batches cannot stay green independently, explicitly
plan a shared integration boundary and final integrate-and-verify gate; do not
promise per-batch green. Branch creation still requires the task's authority.
A behavior-changing slice at a shared seam must preserve the old caller contract
immediately or remain unexposed until compatibility proof passes; never put an
incompatible baseline before a blocked or unavailable expansion slice.
Prefactoring is justified only by a concrete dependency, with its own scope/check.

Present slice name, genuine blockers and delivered behavior when reviewing the
breakdown. Ask about granularity or merging/splitting only when unresolved; prior
approval need not be repeated. A source parent remains unchanged unless that
mutation is authorized. A map is not task emission or tracker publication.

Plan and proposal share problem/behavior, domain vocabulary, decisions, constraints,
acceptance examples, test seams, delivery slices, dependencies, evidence and
authority. The plan projects the broad runbook; proposal projects a selected
slice for review or execution. Preserve source IDs and decisions across both.
Use tracer bullets for independently demonstrable end-to-end behavior and
expand–migrate–contract for wide compatibility changes. Reuse existing public
test seams; prefactoring needs a concrete scoped reason.

When an SDLC spec projection is needed, route it to `skill://propose`; that owner
loads and renders `../work/templates/spec.md` instead of forking the source
template inline.

When TDD is relevant, plan one worker-owned RED-to-GREEN batch through the agreed
public seam, followed by the declared checks and at most one integrated checkpoint
review. The same worker may write the failing test and implementation; the
controller confirms the failure is behavioral and reruns the accepted check.
Use separate RED, GREEN, and verifier agents only when the user explicitly
selects isolated TDD or an execution contract requires hidden holdouts or enforced
role separation. Planning records that exception; it does not dispatch agents.

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

## Next-Step Mini-Router

Offer only eligible next items using a numbered `#`, `Route`, `Expected result`
table when there is a real choice. Planning approval is not execution authority.

| Result | Route | Expected result |
|---|---|---|
| Decision unresolved | `skill://interview` or `skill://arch` | Resolve product choice or technical boundary |
| Plan needs hardening | `skill://auto-enrich` | Improve the same plan |
| SDLC slice ready | `skill://propose` | Map or prepare the selected packet |
| Non-coding plan sufficient | `skill://exec` or selected domain skill | Execute within explicit scope; no mandatory proposal |
| Pause / transfer | `skill://handoff` | Persist frontier and resume pointer |

## Planning Red Flags

- "The frontmatter validates, so the plan is ready."
- "The conversation was long; the plan can summarize aggressively."
- "The task list preserves the roadmap."
- "The first slice is clear, so other source requirements can stay in chat."
- "Smaller blast radius means a migration plan is higher quality."
- "Auto-enrich can recover details that capture omitted."
- "Architect approval means execution is authorized."
- "Every alternative is shallow, so I do not need to name why."
- "The executor can decide the open product boundary."
