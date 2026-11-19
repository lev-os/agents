---
name: lev-plan
description: Use when compiling captured or designed intent into a Lev plan (human runbook, migration, architecture plan, multi-slice roadmap, long-horizon run), deepening or reviewing a plan, changing plan state under `.lev/pm/plans/`, reviewing slice readiness, rendering a slice map, or emitting one execution-ready Lev task.
---

# /lev-plan - Plan, Slice Map, and Execution Packet

`lev-plan` is one workflow from aligned intent to the next executable unit. A
run moves through these stages in order and stops at the one the request asked
for:

1. **Alignment handoff**: bind the source and freeze the intent with its
   fidelity.
2. **The plan, when the work needs one**: compile, deepen, or review the human
   runbook under `.lev/pm/plans/` and manage its FSM.
3. **Review or map**: judge readiness and render a compact slice map.
4. **One execution packet**: write a single just-in-time task packet for a
   selected slice.

Every plan holds the same eight parts: source, outcome, current to target,
vertical slices, claims and proof, review and repair, return and resume, risk
and rollback. Depth sets how much each part holds, never which parts exist. A
schema-valid shallow plan is still a failed plan. The workflow does not
implement, dispatch, or pre-create a backlog of task folders.

Plans, maps, reviews, and specs are Markdown for humans. The task packet keeps
its established YAML payloads, and runtime state stays in the JSON its runtime
owns.

For any non-trivial direct or routed invocation, load [Project Context](../lev/references/project-context.md) before project-specific lookup. It resolves the active project and its declared breadcrumbs.

`skill://lev-plan` loads this contract. Plans, workstreams, and emitted tasks
use durable `lev://entity/work/plan/<plan-id>`,
`lev://entity/work/workstream/<workstream-id>`, and
`lev://entity/work/task/<task-id>` identities; later execution is addressed
separately as `lev://exec/<flow>`. Load `skill://lev` before introducing
another URI family.

## References

Read each file when its condition holds, before the step that needs it.

| File | Read when |
|---|---|
| [Plan parts](references/plan-parts.md) | Every mode except Lifecycle, before `bind_source`. It holds the transition packet, the source fidelity rules, the eight parts, depth, and readiness |
| [Plan template](../work/templates/plan.md) | Before `write_or_patch`, before a plan is rendered in the response, and when a Review reads a plan file: it is the one plan form |
| [Slices](references/slices.md) | Compile, Deepen, Map, and Emit, before `build_topology`, `map_slices`, or `emit_slice`; and every Review, before `judge_readiness` |
| [Proof](references/proof.md) | Before `design_proof`, `prove_requirements`, or `judge_readiness`, and whenever a claim, a check, or TDD is in question |
| [Long-horizon planning](references/long-horizon.md) | Any one holds: the run is long (multi-session or autonomous); a slice goes to a worker; two or more approach families are open; result independence matters; the question may have no solution; the user authorizes delivery through `skill://orch` |
| [Execution Packet](references/execution-packet.md) | Emit mode, a packet preview, or the review or repair of an existing task packet |
| [Lifecycle](references/lifecycle.md) | Lifecycle mode, or a write of plan frontmatter |
| [Notice](references/notice.md) | You copy or publish the adapted long-horizon material |

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

## Work Link

Lifecycle lane: Plan
Entity movement: `captured | designed | draft_plan -> planned | needs_interview | needs_review`, then `planned | aligned -> proposed | execution_ready | needs_interview | needs_plan`
Workstream: resolve the active workstream before plan writes, and the workstream that owns the slice (the `ws` skill) before task writes; the task folder goes under it
Upstream: `/capture`, `/interview`, `/prior-art`, `.lev/pm/designs/*`, existing plan under `.lev/pm/plans/*`, aligned simple-slice intent
Downstream: `/auto-enrich`, `/exec` for a ready SDLC packet, `/exec` or domain skill for non-coding, `skill://poc`, `/interview`, `/capture`, `/lev`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Modes

| Mode | Trigger | Result |
|---|---|---|
| Compile | Captured/design intent or explicit `create` | One new plan, or update the existing matching plan |
| Deepen | `deepen <plan>` or an existing shallow plan | Patch the named plan in place; never create a parallel version |
| Review | `review <plan>`, “is this plan ready?”, or a slice or aligned bounded intent with no other mode | Fidelity/readiness verdict; a slice review recommends one vertical slice; no write unless authorized |
| Lifecycle | list/show/transition/validate | FSM operation only |
| Map | `map` or `all slices` | Compact slice map only; never creates task folders |
| Emit | `emit <slice-id>` | Exactly one `{dna.yaml,execution.yaml}` task packet |

The commands `/propose` and `/horizon` are removed (JP 2026-11-17): `/propose` was Map or Emit, and `/horizon` was
Compile or Deepen for a long run. This skill is the one plan skill.

Default to review without writing when the user asks what the plan should
contain, requests an audit, or has not authorized a durable edit. One
exception: an explicit request for the plan itself with no write authorization
runs Compile (Deepen when a matching plan exists), skips `write_or_patch`, and
renders the plan in the response.

## Which Stage

Classify the domain and the scope before applying software-delivery mechanics.
Map and Emit simulate the SDLC overlay; they are not a mandatory gate for all
Lev work.

- **Broad work plans first.** Broad, multi-slice, migration, architecture,
  security, or cross-authority work needs a plan source before any slice is
  mapped or emitted. A Map or Emit request never authors or deepens that plan
  as a side effect: leave the entity at `needs_plan`, name Compile or Deepen as
  the next step, and continue into it only when the request and its
  authorization cover plan writes.
- **A bounded slice goes direct.** A capture or design goes straight to Review,
  Map, or Emit only when one bounded vertical outcome is already clear. Record
  `plan_not_required` with a one-sentence rationale in the transition packet
  and, on Emit, in the packet's existing `source_context` plan field.
- **Non-coding work skips the packet.** With a sufficient plan, scope,
  acceptance, and authority it routes to its domain skill or `skill://exec`;
  Map and Emit apply only to coding or an overlay that requires a packet.
- **Open decisions leave first.** Coding with unresolved architecture goes to
  `skill://arch`; an unresolved product or architecture decision goes to
  `/interview`; an unknown answer that a prototype would settle goes to
  `skill://poc`.
- **Aligned intent goes straight to the plan.** Synthesize settled decisions
  and ask only about an unresolved choice that changes scope or acceptance.

## Workflow

```yaml
steps:
  - id: bind_source
    action: Resolve workstream, capture/design/plan refs, existing matching plan or task, source digests, and allowed write scope; freeze the aligned intent as the transition packet before broad lookup or writes. List every material intent ID with its source ref, including later branches that are still unresolved.
    validation: "Every material intent has an intent_id and source_ref; an existing plan or task is reused when present; one operator outcome, its boundaries, and a relevant verifier can be named; unresolved later branches are open rows of the fidelity table, neither resolved nor dropped."
    on_failure: "Route conversation-only work to /capture; unresolved product or architecture framing to /interview. Do not draft around missing intent."

  - id: select_mode
    action: Apply Which Stage, then select compile, deepen, review, lifecycle, map, or emit from the command. A lifecycle request performs only its FSM operation and then route_forward; one that moves a plan to ready or done runs judge_readiness first.
    validation: "Exactly one mode is selected; broad work has a plan source before map or emit; a direct bounded slice records plan_not_required with its rationale."
    on_failure: "Default to review without writing."

  - id: rehydrate_fidelity
    action: Load the capture source-fidelity table and map every material row to a plan section, decision, deferment, or explicit conflict. For map and emit, map every material intent_id to a plan-level constraint or proposed slice and reject lost rows.
    validation: "Source fidelity is current; no material row is lost; plan fidelity is >= 0.90 and not lower than capture fidelity; every slice names covered intent IDs."
    on_failure: "Route missing capture fidelity to /capture or ask one decision question; a shallow broad plan is needs_plan. Do not draft around missing intent."

  - id: inspect_current_state
    action: Run `lev find "<3-6 topic words>" --type plan --type design --type decision --type idea --json` first when `lev` is installed; when the work belongs to a workstream, run the same call again with `--workstream <its id>` and read the plain call's first 5 cards, then the scoped call's first 5 cards not already shown (decision 20261101-find-prior-art-workstream-call) (a `superseded` card is history; open its superseder; plan and design types return no cards until indexed, so also `rg` `.lev/pm/plans` and `.lev/pm/designs`; if `lev` fails, say so in one line and `rg` over `.lev`). Then identify the owning code areas and inspect only what this run needs - current code, docs, plans, dependencies, dirty work, external authority, the source capture/design/plan, workstream, existing task, verifier evidence, and the applicable entries from the project's rules index.
    validation: "Current-state claims are observed or labeled stale/assumed; load-bearing claims cite exact refs."
    on_failure: "Route to /prior-art or keep the claim unknown; mark stale or missing authority as an open decision."

  - id: choose_depth
    when: mode is compile or deepen
    action: Select light, standard, or deep from risk and topology, and say whether the run is long, delegated, or a parallel search (Depth, in Plan parts); state the selection in the plan.
    validation: "Depth matches the real blast radius and does not use length as a proxy for rigor; a long or parallel run has loaded long-horizon planning."

  - id: frame_outcome
    when: mode is compile or deepen
    action: Write the success sentence first - one sentence about the returned result with quantifiers, scope, and the narrowing assumptions it may not make. Work backward from what a complete answer lets the operator do. Then define observable done state, scope, non-goals, authority boundaries, and human decisions.
    validation: "An adversarial reader can decide from the success sentence alone whether a given result passes; every part of it that a command can decide is named as a program claim; a teammate can tell what changes, what stays unchanged, and what done looks like."
    on_failure: "Decompose to a smaller sentence, send the decision to /interview, or the unknown to skill://poc."

  - id: exclude_near_misses
    when: mode is compile or deepen
    action: Write Does Not Count with the refusal list - every result you would send back from a capable collaborator under pressure - starting from the defaults in Plan parts. Then define each load-bearing term with its degenerate cases.
    validation: "Each predictable near miss is excluded by name and mapped to a claim, a claim's guard (its invalid_proof entry at Emit), or the review checklist; terms settle the empty, trivial, duplicate, and boundary cases the success sentence must survive. A light plan may hold one line."

  - id: analyze_options
    when: mode is compile or deepen
    action: For standard/deep plans, compare at least two meaningful approaches or record evidence that alternatives are invalid.
    validation: "Decision drivers, tradeoffs, sacrificed attributes, and chosen approach are explicit; newly derived behavior is labeled proposed or left as an open decision, never promoted into settled source intent."

  - id: build_topology
    when: mode is compile or deepen
    action: Build current-to-target map, ownership boundaries, dependencies, vertical slices, critical path, promotion gates, and administrative holds (Slices).
    validation: "Every slice has an outcome, owner, depends_on, artifact, proof, stop condition, status, open decisions, and covered intent_ids; each promotion verifier is satisfiable by that slice plus completed dependencies; a slice with incomplete or blocked dependencies is blocked, not ready or merely promotion-gated; no slice starts before its input claims are satisfied; every slice names its run budget, and every artifact a long run reads names its frozen format version; a delegated slice has its worker contract (long-horizon planning)."

  - id: design_proof
    when: mode is compile or deepen
    action: Write the claims with the three passes of Proof (think, write, prove) - what must hold and what must never hold. For each claim name its proof as a program, an agent, or a person, the smallest relevant local, integration, field, or external-owner verifier chosen under Proof and Evaluator Selection, and its guard against a check that cannot fail.
    validation: "At least 90% of acceptance criteria are concrete/testable; every claim names program, agent, or person, or is listed as unresolved proof; program checks exist only where a command decides the claim; every check is named after the failure it rules out, maps to one claim id, and names a known-bad control, a check owner, and the sensitivity evidence required before acceptance; each verifier is attached to the first slice whose scope can satisfy it; every claimed preserved boundary or compatibility form is exercised directly; missing future tests are slice work, not false blockers."

  - id: set_review_and_repair
    when: mode is compile or deepen
    action: Write the review checklist, the named blocking conditions, the recall with its retry cap, and each slice's run budget from Review and Repair in Plan parts.
    validation: "The plan states which findings block and the evidence each needs; every recall has a finite cap."

  - id: set_return_and_resume
    when: mode is compile or deepen
    action: Write the return gate, the incomplete-return exits, and the resume frontier from Return and Resume in Plan parts.
    validation: "Return depends on claims and open blocking findings, never on confidence, effort, or elapsed time; a fresh session can resume from the frontier without the originating chat."

  - id: design_failure_and_rollback
    when: mode is compile or deepen
    action: Record credible failure mechanisms, prevention/detection, residual risk, rollback, and architecture review triggers.
    validation: "High-risk/deep plans include a three-scenario pre-mortem and unit/integration/e2e/observability test shape where applicable; rollback returns to the latest dependency-compatible state and cannot remove compatibility still required by incomplete slices."

  - id: write_or_patch
    when: mode is compile or deepen
    action: Write one plan under .lev/pm/plans/ only inside authorized scope, from the plan template, preserving unrelated plan history and current dirty work.
    validation: "Exactly one plan is created or updated; source refs and fidelity table are durable. The plan stays unreviewed and uncommitted until judge_readiness is done."

  - id: judge_readiness
    action: Run deterministic structure/ref checks, then the semantic weak-link review - score the readiness dimensions, classify blockers, and issue the verdict. Then load the `review` skill by its name (the Skill tool with `review`; a host with no Skill tool opens ~/.agents/skills/review/SKILL.md); name in its arguments the plan or slice, lens zoom_out, the attacker stance (its fresh reader attacks the success sentence) at standard or deep depth and for every long, delegated, or parallel run, and lev-plan as the caller. Patch each result the plan would wrongly accept with a Does Not Count line or a check, and repeat the attack on the patched text. Put its chat line (the review skill's Report section) under the verdict as advice, and in the Review and Repair section of a plan that is written; it never changes the verdict, and a blocker from it becomes a blocking condition only when it meets the blocking rule of Review and Repair (Plan parts). When review routed you here, skip this load and use the stance and lenses it gave. When review already ran on the same plan or slice in this work and it has not changed since, cite that run's report file instead of a second run. Use /auto-enrich for explicit or deep/high-risk plan hardening when available.
    validation: "No readiness dimension is insufficient; deterministic success is reported separately from semantic approval; the attacker's last pass finds only near misses already excluded or caught. Done when the reply holds the review skill's chat line for this plan or slice (the cited run's line when an earlier run is cited), with its report file's path, or, when the review skill could not be loaded, the line 'review: could not run ({reason})'. Until then the plan or slice is unreviewed: it stays uncommitted, and no reply calls it finished, ready or done."
    on_failure: "If no slice is runnable, simplify the DAG; block only on a concrete code or decision blocker."

  - id: map_slices
    when: mode is map
    action: Render compact slice records without creating task folders.
    validation: "Every record has an outcome, owner, dependencies, proof, status, and open decisions; at least one approved-map slice is runnable."

  - id: prove_requirements
    when: mode is emit and semantic readiness is ready
    action: Read references/execution-packet.md and references/proof.md, carry the slice's claims into the task's requirements list (writing with the three passes any that the plan lacks), then run every check once on today's tree.
    validation: "Every row is a prompt (often one sentence, never forced) that a check or the review agent can answer; at least one check is red today when the slice adds or fixes behaviour. A task is ready only with a definition of done and admitted checks (references/proof.md, Admit a check before you trust it)."
    on_failure: "Sharpen a row nothing can prove, or route its open question to /interview."

  - id: emit_slice
    when: mode is emit and semantic readiness is ready
    action: Write one lean task packet for the selected vertical slice, using only current packet keys.
    validation: "Exactly one task folder is created or updated, and every Emission Gate condition holds."

  - id: validate_structure
    when: mode is emit
    action: Run `lev entity task validate <task-id|task-path> --json`; it validates every `check:` through core/eval. Report deterministic failures separately.
    validation: "The command exits 0 and its JSON reports no failed row."
    on_failure: "Keep the task proposed; do not offer /exec."

  - id: compare_source
    action: Recompare intent, boundaries, requirements and their proof, dependencies, and freshness with the source. For a written plan, cold-read it in fresh context and confirm that each preserved row's constraints and unknowns are recoverable from the plan or its pointers.
    validation: "Each of the five compared items is marked same as the source or repaired, with the source ref; every preserved row passes the cold read."
    on_failure: "Repair and rejudge before offering the next route."

  - id: route_forward
    action: Name the next stage or route - an approved SDLC plan to map or slice review, a ready slice to emit, a validated packet to /exec, a sufficient non-coding plan to the domain skill or /exec. Outside emit this workflow writes no task folder, and it never dispatches execution.
    validation: "The first executable slice is named and the plan, when one exists, remains its source; Next names exactly one route, and only for a gap its owner can close; evidence with no available owner stays an unresolved blocker."
```

## Write Gate

Render review output by default. Write a plan only inside authorized planning
scope. Write task artifacts only after explicit `emit`, `apply`, `edit`, or
`patch` authorization, or an approved capture row routed to Emit. `all slices`
is map authorization, not task-emission authorization. Emit must also pass the
[Emission Gate](references/execution-packet.md#emission-gate). A packet
preview stays in the response, labeled preview: not validated, executed, or
emitted. A plan with no write authorization stays in the response; a bounded
plan may be saved as a light plan when authorized.

## Output

Render the Markdown inside live templates; do not print the XML wrapper tags.
Plan modes render `<plan-review>`, a slice review renders `<proposal-review>`,
Map renders `<slice-map>` from [Slices](references/slices.md#slice-map), and
Emit renders `<final-proposal>` from the packet reference. The plan itself is
written from the [plan template](../work/templates/plan.md).

<plan-review>
## Plan: {slug}

Verdict: {ready|needs_review|needs_interview|implementation_handoff}
Depth: {light|standard|deep}; run {bounded|long|parallel search}
Source fidelity: {score}; lost rows {count}; narrowed rows {count}
Outcome: {success_sentence}
Current -> target: {one_sentence_transition}
First slice: {slice_id}; {outcome}; proof {verifier}
Proof: programs {claim_ids}; agent-answered {claim_ids}; person {claim_id: owner}; unresolved {none | claim_ids}
Weakest point: {dimension}; {reason}
Open decisions: {none_or_list}
Artifact: {plan_ref}
Next: {/auto-enrich|map|emit <slice-id>|/interview|skill://poc|implementation spike|resume {unit}}
</plan-review>

<proposal-review>
## Proposal: {proposal_id}

Verdict: {ready|needs_review|blocked}
Outcome: {operator_visible_result}
When done: {observable_effect}
Source: {plan_or_capture_ref}; fidelity {score}; covered intent {count}/{total}
Code and rules: {owner_paths}; {rules_index_refs}
First testable slice: {slice_id} - {behavior}
Proof: local {check}; integration {check_or_na}; field {check_or_na}
Weakest point: {dimension}: {reason}
Open decisions: {none_or_decisions}
Next: {emit_slice|repair_question|interview}
</proposal-review>

## Next-Step Mini-Router

Offer only eligible next items using a numbered `#`, `Route`, `Expected result`
table when there is a real choice. Clear authorized transitions proceed
directly. Planning approval is not execution authority.

| Result | Route | Expected result |
|---|---|---|
| Decision unresolved | `skill://interview` or `skill://arch` | Resolve product choice or technical boundary before emission |
| Plan needs hardening | `skill://auto-enrich` | Improve the same plan |
| Plan missing, stale, or incomplete | Compile or Deepen | Repair the source plan before slicing |
| SDLC slice ready | Map or Emit | Map, or prepare the selected packet |
| Ready authorized SDLC packet | `skill://exec` | Execute the selected unit |
| Non-coding plan sufficient | `skill://exec` or selected domain skill | Execute within explicit scope; no SDLC packet |
| Pause / transfer / deferred | `skill://handoff` | Persist frontier, packet state, and resumption condition |

## Red Flags

- "The frontmatter validates, so the plan is ready."
- "The conversation was long; the plan can summarize aggressively."
- "The task list preserves the roadmap."
- "The first slice is clear, so other source requirements can stay in chat."
- "Smaller blast radius means a migration plan is higher quality."
- "Auto-enrich can recover details that capture omitted."
- "Architect approval means execution is authorized."
- "Every alternative is shallow, so I do not need to name why."
- "The executor can decide the open product or architecture decision."
- "All slices means emit all tasks."
- "A generated backlog is a roadmap."
- "Task validation passed, so semantic quality is proven."
- "More proof metadata makes the task more ready."
- "A task generated from an older design is still current."
- "Verifier exists, so the behavior is proven."
- "Session notes belong in task canon."
- "The proposal exists, so implementation can start."
- "The plan is optional; the slice map can recover it from chat."
- "A 95% fidelity average is fine even though one material constraint disappeared."
- "Emit can deepen a shallow migration plan while writing the first task."
- "The harness or receipt is missing, so implementation is blocked."
- "Every slice is held, but the map is still approved."
- "No current contract declares that evaluator, so the packet can define it inline or drop the claim."
- "It is a light plan, so it needs no success sentence and no proof."

## Field notes from Hermes

Each note is one past session's lesson. Read one only when the plan in hand
matches its case.

- [plan-first-sdlc-discovery](references/plan-first-sdlc-discovery.md): SDLC discovery or execution routing must choose between a plan and a task
- [sdlc-adapter-convergence-planning](references/sdlc-adapter-convergence-planning.md): a Lev SDLC, task, or workstream migration is planned while core is still settling, or two persistence substrates compete
- [sparse-taxonomy-gate-shaping](references/sparse-taxonomy-gate-shaping.md): a routing, config, or taxonomy migration is being shaped and no code should start yet; it lists what must and must not be true
- [substrate-first-follow-up-planning](references/substrate-first-follow-up-planning.md): the user corrects a plan that centered a plugin or component before the platform substrate under it was proven
