---
name: work
description: Use when routing tracked work through lifecycle lanes, resolving workstream context, or deciding which lifecycle skill owns the next entity transition.
skill_type: router
category: lifecycle
output_template: hud
sub_skills:
  - ws
  - capture
  - prior-art
  - propose
  - exec
  - close
  - handoff
---

# /work - Lifecycle Router

`/work` is the thin lifecycle spine. It does not re-implement capture,
proposal, execution, close, or handoff protocols. It resolves workstream
context, identifies the entity movement, and routes to the owning skill.

## Work Link

Lifecycle lane: Router
Entity movement: `unknown -> routed`
Workstream: resolve active workstream before writes or dispatch
Upstream: any lifecycle skill or user request
Downstream: `/ws`, `/capture`, `/prior-art`, `/propose`, `/exec`, `/close`, `/handoff`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Inline HUD Contract

End lifecycle-skill responses with this inline HUD line:

`🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

The shared graph-footer partial is an authoring reference only until the Lev
skill-builder pipeline can project FlowMind fragments into skill bodies. Do not
make skills load or include that file at runtime.

## Human Response Contract

Keep full ledgers, scores, traces, and gate state in durable artifacts. Default
interactive output is a compact content-first projection; render the full table
only for `--full`, explicit audit/debug requests, or when one row cannot be
understood without it.

Score the default response on these ten checks. A check may be `not_applicable`
only with a concrete reason; every applicable check must pass.

| # | Check |
|---:|---|
| 1 | Lead with the outcome or current state. |
| 2 | Name the operator-visible result. |
| 3 | Name the exact asset, code area, task, or durable entity affected. |
| 4 | Name relevant code owners and rules/index refs when implementation is discussed. |
| 5 | Show the real-world critical path when behavior crosses boundaries. |
| 6 | Name the first executable or testable next slice. |
| 7 | State what done means as an observable effect. |
| 8 | State the smallest local, integration, or field proof that matters. |
| 9 | Separate deterministic code, declarative policy, LLM work, and human decisions when relevant. |
| 10 | End with one primary next action and any real blocker. |

Default target: at most 12 non-blank lines before the optional HUD. Do not print
an empty section, a full readiness matrix, or a ledger that already exists on
disk.

Render the Markdown inside live XML templates; never print the XML wrapper tags.

<lifecycle-response>
## {outcome_or_state}

Changed or saved: {durable_delta_or_none}
Proof or state: {load_bearing_evidence_or_gap}
Decision needed: {none_or_one_decision}
Next: {one_primary_action}
</lifecycle-response>

## Lifecycle Lanes

| Lane | Entity movement | Owns |
|---|---|---|
| Shape | `memory -> captured | blocked` | `/capture`, `/prior-art`, `/interview` |
| Plan | `captured | aligned -> proposed | execution_ready` | `/propose`, `/capture` |
| Exec | `execution_ready -> executing -> verified | blocked | needs_propose` | `/exec` |
| Close | `verified -> closed | monitoring | follow_up` | `/close`, `/handoff` |
| Router | `unknown -> routed` | `/work`, `/ws` |

## Entity Rules

- Resolve the active workstream before writing or dispatching.
- Every lifecycle skill has exactly one `## Work Link` section.
- Every non-trivial item is an entity with a path, URI, or task/workstream id.
- Move entities forward one lifecycle state at a time; do not skip from memory
  directly to execution unless a captured/proposed artifact already exists.
- Workstreams are durable identity. Markdown handoffs are projections, not the
  canonical state.
- If a command mutates files, records, tasks, or workstream state, route through
  the lane owner instead of freelancing.

## QA / Pentagon Gate State

QA, Pentagon, UltraQA, and ai-slop-cleaner are lifecycle gate overlays, not
separate lanes. `/work` routes by missing gate state; lane skills own the
details.

| Gate state | Meaning | Route |
|---|---|---|
| `needs_proof_design` | Highest-risk claim, fail-closed acceptance, or owner-local test placement is unclear | `/interview` or `/propose` |
| `needs_proof_gates` | A non-trivial task lacks `execution.yaml.proof_gates` | `/propose` |
| `needs_runtime_qa` | Declared baseline, Pentagon, UltraQA, or harness runtime checks still need execution | `/exec` |
| `needs_quality_review` | Cleanup, refactor, fallback, boundary, or AI-slop risk needs ai-slop-cleaner review | `/exec` |
| `needs_close_verdict` | Work is implemented but proof-gate verdicts or residual risks are not sealed | `/close` |
| `proof_blocked` | A proof gate fails or cannot run safely | `/propose` for contract repair or `/capture` for follow-up |

## Router

```yaml
steps:
  - id: resolve_workstream
    action: Identify the active workstream or route to /ws.
    validation: "A workstream id is known, or /ws is the next skill."
    on_failure: "Do not write. Route to /ws find|resume or create a workstream."

  - id: classify_entity
    action: Name the entity, current state, target state, missing gate, and proof_gate_state.
    validation: "Entity has path/id/uri plus current_state, target_state, and proof_gate_state when non-trivial."
    on_failure: "Route to /capture if it is only in conversation memory."

  - id: route_lane
    action: Select the lifecycle lane owner.
    validation: "Exactly one next skill is chosen from the lane table."
    on_failure: "Ask one routing question or route to /prior-art for evidence."

  - id: enforce_work_link
    action: Ensure the next skill declares lane, movement, upstream, downstream, and HUD.
    validation: "The selected skill has a Work Link or this session is updating it."
    on_failure: "Use skill-builder semantics to patch the skill before relying on it."

  - id: emit_hud
    action: Report current workstream, gate, next entity, and loop state.
    validation: "Response ends with the inline HUD line."
    on_failure: "Add the HUD before ending."
```

## Route Table

| Situation | Route |
|---|---|
| User dumps ideas or a thread has unfiled content | `/capture` or `/dump` as `capture --deep` |
| Need evidence, provenance, lineage, or duplicate detection | `/prior-art` |
| Idea/design is aligned but not execution-ready | `/propose` |
| Task has `dna.yaml` and `execution.yaml` with a verifier | `/exec` |
| Task needs proof design, proof gates, runtime QA, or quality review | route by `proof_gate_state` |
| Work is verified and needs sealing, learning, commit, or next recommendation | `/close` |
| Session is ending, compacting, or needs a resume prompt | `/handoff` |
| Workstream identity is missing, stale, split, or tangled | `/ws` |

## Work Link Template

Each lifecycle skill carries one block in this shape:

```md
## <Work Link>

Lifecycle lane: {Shape|Plan|Exec|Close|Router}
Entity movement: `{from_state} -> {to_state}`
Workstream: resolve active workstream before writes or dispatch
Upstream: `{skill_or_none}`
Downstream: `{skill_or_none}`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`
```

## Templates

Templates are authoring references. Copy or render them through the owning lane;
do not make another skill depend on reading them at runtime.

| Template | Destination | Owner |
|---|---|---|
| `templates/report.md` | `.lev/pm/reports/` | `/prior-art`, `/capture` |
| `templates/plan.md` | `.lev/pm/plans/` | `/propose` |
| `templates/design.md` | `.lev/pm/designs/` | `/interview`, `/propose` |
| `templates/proposal.md` | `.lev/pm/proposals/` | `/propose` |
| `templates/spec.md` | `.lev/pm/specs/` | `/propose` |
| `templates/decision.md` | `.lev/pm/decisions/` | `/close` |
| `templates/validation-report.md` | `.lev/pm/validation-reports/` | `/exec`, `/close` |

## Red Flags

- "I'll just do this without a workstream."
- "This is small enough to skip entity tracking."
- "The next skill will figure out the lifecycle state."
- "I can execute even though this only exists in chat."
- "I'll add the HUD/footer later."
- "The shared partial says it, so this skill does not need to."

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Work owns everything." | Work routes; lane skills own detailed protocols. |
| "A handoff markdown is enough." | Workstream YAML is durable identity; markdown is projection. |
| "The user asked to execute." | Execution still needs an execution-ready entity and verifier. |
| "Footer file will be loaded." | HUD is inline until FlowMind skill projection exists. |
| "I know the workstream." | Name it in the HUD or route to /ws. |
