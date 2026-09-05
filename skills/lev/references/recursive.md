# Recursive Wayfinding

Use this procedure for a long-horizon or multi-session effort, when the user
invokes `$lev --recursive`, or when an existing route becomes ambiguous after
new evidence, a failed assumption, a changed dependency, or a structural
failure. This is skill syntax, not a `lev` CLI flag.

## Navigation Objects

- **Outcome:** the observable change in the world the effort exists to create.
- **Outcome map (`outcome_map_ref`):** the durable best-known route from current
  state to that outcome, including decisions, work, evidence, shared
  dependencies, exclusions, and fog.
- **Rolling horizon:** the current ordered projection of at most ten next steps.
- **Immediate frontier:** the ready questions or actions on that horizon.
- **Wayfinding pass:** a bounded reconciliation and route revision.

- **Graph proposal:** a prospective patch offer over a revisioned baseline:
  retained, added, modified, removed and unresolved nodes/edges plus the steps,
  artifacts, effects and checks needed to realize the outcome. It is a hypothesis
  until accepted; an existing materialized read-model projection remains a view.
- **Domain specialization:** enabled domain capabilities add entity fields,
  constraints and verifiers. SDLC contributes specs and execution packets when
  software delivery applies; it is not the universal proposal schema.

The outcome map is durable; the rolling horizon is a projection. Preserve
stable entity IDs when order or wording changes. A child result updates its
parent's evidence and readiness; it does not complete the parent automatically.

## Propose the Graph

Use alignment → propose → act → verify for every coherent work unit. Alignment
shapes problem and solution; propose offers the candidate graph delta; act
realizes accepted effects through owning systems; verify checks the outcome.
Normal progression is adjacent. A gate may permit the current boundary, hold,
or reject toward an earlier stage; rejection never moves forward. In alignment,
rejection holds and reshapes. Verification success completes the unit; failure
returns to act, propose or alignment according to its cause. This phase model
does not replace workstream/task status enums without a separately tested migration.

Build the outcome map in bounded passes:

1. Ground existing nodes in source/evidence with stable identity, locator and
   revision. Resolve applicable domain capabilities from configuration; distinguish
   installed, declared, enabled and available. Directory presence is insufficient.
2. Project every relevant peer branch at one depth. Name the intended artifact or
   observable result before choosing implementation. Preserve uncertain branches.
3. Simulate each node's inputs, preconditions, effects, outputs, failure paths,
   verifier and stop condition. Label tabletop reasoning, executable dry-run and
   live observations separately. Simulated success is not completion evidence.
4. Expand missing prerequisites into children; reuse shared dependencies and
   attach alternatives without treating every alternative as mandatory. Preserve
   parent intent and connect the evidence that caused the refinement.
5. Validate the dependency DAG and patch scope, propagate readiness/invalidation,
   then repeat at the next depth within budget. Stop at the requested coverage,
   evidence/decision boundary, or budget and name the remaining frontier/fog.
6. Capture the resulting proposal, assumptions, source mappings and iteration
   deltas in the owning workstream before handoff. On a show-only/read-only request,
   honor that boundary and identify the unsaved result explicitly. Render with
   Archify when requested or useful, preserving the proposal as the source.

Controls are independent; state supplied settings and assumed defaults:

| Control | Effect |
|---|---|
| depth | Maximum decomposition depth; complete peer coverage before descent |
| density | Coverage of useful obligations, artifacts, failure paths and relationships; not arbitrary edge count |
| budget | Bound passes, nodes, elapsed time, tokens/cost and any actual executions |
| temperature | Structural flexibility: established process versus a bounded pragmatic POC; distinct from model sampling |

Temperature never relaxes permission, integrity, source fidelity, evidence truth
or accepted outcomes. Contracting a view hides detail without deleting underlying
obligations. A request for the densest/furthest map seeks useful bounded coverage,
not a claim of exhaustive knowledge. The ten-step horizon is only a view over it.

Keep containment, dependencies, evidence, alternatives and feedback distinct.
Only execution dependencies must form a DAG. Represent repair loops as lifecycle
transitions or later graph revisions, not contradictory dependency edges.

For visualization, show baseline nodes with source refs; mark additions explicitly;
show modifications under the same stable ID with before/after detail; show removal
as a proposed tombstone, never erase it from the review. Label unknowns and the
expected artifact/result of each change. Color supplements status text. A layout
change is not a semantic patch. Preserve existing edges in the baseline rather
than presenting unrelated old/new boxes as a verified dependency graph.

Workstream shape grows through admitted, module-owned entity/root contracts. Keep
intent, task/spec/DNA/execution and claim/evidence identities linked without
pre-creating every possible file. Resolve accepted locators from configuration;
example `intent.yaml` or `claim.yaml` names do not prove runtime support. A graph
record about a file/API change is not that effect: each target owner must apply,
verify and, when required, compensate it. Bind candidate changes to base revisions
and reject stale application instead of overwriting concurrent work.

Use ordinary schema/reference/DAG checks first. Use Z3 for bounded constraint
consistency and counterexamples, and TLA+/state exploration for temporal gate,
retry, revocation and crash properties when consequential. Translate discovered
counterexamples into runtime tests. Accept explicit UNSAT only for an SMT
counterexample query; UNKNOWN or timeout is inconclusive, not proof. Formal model validity does not certify the
implementation, business semantics, security or perceptual diagram quality.

## Cast the Net

Work backward from the outcome before selecting a step:

1. State the actor, observable capability, intended surface or environment, and
   completion evidence. Record unresolved parts as questions or fog.
2. Inspect current state, prior decisions, evidence, and relevant learnings.
3. Identify the applicable domain overlays. For software delivery, consider
   design, build, test, documentation, packaging, release, distribution,
   support, and marketing; include only the work the outcome actually needs.
4. Search the bound task tracker for compatible existing work before creating a
   child. Release, distribution, and campaign work are common convergence
   points. Reuse requires matching product, channel/version, audience,
   constraints, and authority.
5. Map dependencies, precise questions, in-scope fog, exclusions, and the
   evidence needed to establish each outcome claim.

Marketing and publishing are conditional overlay work. They can enter the map
without gaining execution authority. An internal capability may need docs but
no campaign; an external effect still requires its own approval.

## Project the Rolling Horizon

Project one to ten steps from the current map. Do not invent steps to reach ten.

| Position | Required fidelity |
|---|---|
| 1-3 | Stable ID, outcome or question, owner/route, prerequisites, permitted effects, check/evidence, and stop condition |
| 4-10 | Stable ID, milestone, dependency, and main uncertainty; add detail only when supported |
| Later | Keep visible in the outcome map as milestones or fog; do not copy into the horizon |

Step 1 is the highest-value eligible move, not necessarily implementation. A
precise decision, evidence lookup, review, or quiet wait can be the correct
frontier. High fidelity means explicit uncertainty, not fabricated certainty.

### Required User-Facing Projection

Every user-facing wayfinding pass renders the rolling horizon as two tables.
Narrative may explain the delta, but it never substitutes for these tables.
Render only existing steps; do not pad either table.

Steps 1-3:

| # | Stable ID | Outcome or question | Owner or route | Prerequisites | Permitted effects | Check or evidence | Stop |
|---|---|---|---|---|---|---|---|
| 1 | `<stable-id>` | `<observable result or precise question>` | `<owner or skill://route>` | `<dependencies>` | `<authorized effects or none>` | `<evidence ref, check, or unknown>` | `<completion or escalation condition>` |

Steps 4-10:

| # | Stable ID | Milestone | Dependency | Main uncertainty + resolver route |
|---|---|---|---|---|
| 4 | `<stable-id>` | `<later result>` | `<dependency>` | `<uncertainty — skill://lev --recursive, skill://research, skill://prior-art, skill://interview, or none>` |

Mark load-bearing facts inline as `(supplied)`, `(observed)`, or `(unknown)`.
Use `verified` only beside evidence that was actually inspected or executed in
the current run and cite that evidence in the same row. A plausible sequence,
polished narrative, or prior plan does not upgrade a fact to verified.

**Narrative rationalization check:** if the tables feel repetitive, too formal,
or unnecessary because prose already explains the route, render them anyway.
That feeling is not evidence that the projection contract was satisfied.
Every `(unknown)` or unresolved condition names the skill or human authority
that can resolve it; recording an uncertainty without a resolver is incomplete.

Refresh the horizon after initial charting, material user correction, accepted
worker result, dependency change, invalidated assumption, structural failure,
or handoff. Record the delta: what changed, which evidence caused it, and which
dependent steps became stale, ready, blocked, merged, or removed.

## Recurse on Ambiguity or Failure

When a selected node is vague or fails, run this procedure on that node while
retaining its parent outcome:

1. Reconcile the freshest evidence and prior learning.
2. Classify the uncertainty: missing fact, human/product decision,
   implementation gap, verification gap, dependency, authority, or environment.
3. In frontier mode, expand until one child is actionable or a decision/budget
   boundary is reached. In full projection mode, continue across peer branches
   to the requested depth/density within budget; mark blocked leaves explicitly.
4. Execute or route one eligible child within existing authority.
5. Propagate its evidence to the parent, then reproject the affected horizon.

Use `skill://research` or `skill://prior-art` for facts, `skill://interview` for
human decisions, `skill://poc` for feasibility, and the active domain overlay
for execution. A bounded repair can remain in its current execution flow. A
changed outcome, public contract, release scope, or authority returns to the
appropriate decision owner.

## One Tracker and Shared Work

Use the workstream's bound tracker as the only task-status authority. Other
artifacts are projections or evidence links. If no tracker is bound, ask once
among the mechanically supported project choices and persist the answer before
creating tasks. Never fall back to another backend because the selected one is
unavailable.

Before creating a release, documentation, download, distribution, support, or
marketing task, search the bound tracker for a compatible entity. Multiple
features may depend on the same shared task. If its scope changes after
approval, invalidate the affected approval or create a revision; do not expand
it silently.

Shared-task compatibility is the tuple `product + channel/version + audience +
constraints + authority`. If any required value is unresolved, route to
`skill://prior-art`, `skill://research`, or a focused wayfinding pass. Do not
create a supposedly shared task by guessing the missing value. Describe any
proposed task emission as future and conditional unless the current interaction
already authorizes the write.

## Tick Selection

A goal-owned navigation heartbeat carries the stable `goal_ref`, selected
`tick_policy`, and an automation idempotency key derived from those two values.
The host uses that key for lookup, update, and creation so retries and renamed
goals cannot create parallel heartbeats. The display name is presentation only.

Reconcile first, then choose one eligible tick deterministically:

1. Required independent review.
2. Wayfind or research when ambiguity blocks the frontier.
3. Execute one ready, authorized unit.
4. Hygiene when drift is detected or its configured interval is due.
5. Release or publish only when its domain gate and authority are satisfied.

A live dependency permits a quiet wait. No eligible work is not proof of
completion and does not justify a discovery task. Pause, cancellation, and
confirmed completion stop navigation heartbeats.

## Completion Check

A wayfinding pass is complete when the requested graph proposal and material
reasoning have been captured within write authority, existing-to-proposed changes
and simulation limits are visible, and the outcome and tracker binding are known or
explicitly blocked, current evidence is reconciled, the map preserves shared
dependencies and exclusions, the horizon has at most ten stable-ID steps, its
first three meet the high-fidelity contract, and the next eligible action or
wait condition is explicit.

Append the exact lifecycle HUD supplied by the active session verbatim. If the
session supplies no HUD, omit it; never construct or substitute another status
line.
