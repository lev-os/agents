---
name: poc
description: Use when the user asks to prove, spike, prototype, POC, validate a production path, compare landing zones, or decide whether an idea should move to propose, monitor, reject, or archive.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /poc - Proof Lane

`/poc` owns bounded proof work between capture/design and proposal. It proves a
specific claim, not a whole project. It can produce a disposable artifact, a
production-path trace, or a decision matrix, then routes the result back into the
Leviathan lifecycle.

## Work Link

Lifecycle lane: Shape -> Plan
Entity movement: `hypothesis | captured | idea -> proven | partial | disproven | monitor | proposal_ready`
Workstream: resolve the active workstream before writing artifacts or dispatching work
Upstream: `/capture`, `/interview`, `/design`, workshop intake, `/prior-art`
Downstream: `/propose`, `/capture`, `/exec`, `/close`, archive
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦poc={verdict}/{score} | ⏭️ {next} | 🔁{loop_state}`

## Commands

```bash
/poc                         # choose the cheapest proof mode
/poc --spike                 # answer a bounded unknown with minimal evidence
/poc --prototype             # build or inspect a disposable working artifact
/poc --production-path       # prove the real integration path, not a mock demo
/poc --matrix                # compare landing zones or implementation routes
/poc --auto                  # run without asking unless a gate blocks proof
```

## Prior Art Guard

Run `/prior-art` or an equivalent local evidence pass before recommending a
matrix, implementation route, or verdict. Workshop intake treats `spike` and
`POC` as implementation routes, not terminal dispositions. The terminal
disposition must be one of `adopt`, `extract`, `monitor`, or `reject` when the
proof is part of workshop intake.

## Mode Selection

Use `--spike` when the unknown is conceptual, architectural, API, feasibility,
or fit. Output can be read-only when code is not needed.

Use `--prototype` when the user needs a tangible artifact to inspect or try. The
artifact can be throwaway, but it still needs usage notes and a verifier.

Use `--production-path` when the risk is integration, deployment, persistence,
data flow, runtime ownership, or "will this work in the real system?" Evidence
must touch the real commands, contracts, files, APIs, or gates.

Use `--matrix` when there are multiple landing zones, libraries, routes, or
approaches. Score against the claim, not against general preference.

## Protocol

```yaml
steps:
  - id: bind_claim
    action: State the single claim being proved and the proof mode.
    validation: "Claim, scope boundary, expected evidence, and stop condition are visible."
    on_failure: "Ask one narrowing question or route to /interview."

  - id: load_prior_art
    action: Search existing chats, workstreams, workshop notes, repo docs, and relevant external sources.
    validation: "Prior-art result names what is new, repeated, stale, or already decided."
    on_failure: "Do not recommend a route or write a matrix."

  - id: choose_verifier
    action: Pick the cheapest credible proof: command, trace, test, demo, doc evidence, or operator review.
    validation: "Verifier can falsify the claim or clearly explains why it cannot."
    on_failure: "Mark proof as partial instead of proven."

  - id: execute_or_design
    action: Run the proof, build the prototype, or produce the comparison matrix.
    validation: "Evidence is concrete: file, command, output, trace, screenshot, result JSON, or cited prior art."
    on_failure: "Record the failure and route to monitor, reject, or revised proof."

  - id: score_matrix
    action: Score evidence and route the result.
    validation: "Weighted score, hard blockers, verdict, and lifecycle route are visible."
    on_failure: "Do not promote to /propose."

  - id: capture_result
    action: Capture the result into the workstream, design, proposal seed, or archive note.
    validation: "The next lifecycle owner can continue without re-reading the whole chat."
    on_failure: "Emit a compact handoff block in the response."
```

## Proof Matrix

| Dimension | Weight | Pass signal |
|---|---:|---|
| Evidence strength | 0.25 | Direct artifact, trace, result, command, or source-backed finding |
| Production-path fit | 0.20 | Real integration path is named and exercised or bounded |
| Verifier strength | 0.15 | The verifier can fail for the right reason |
| Architecture fit | 0.15 | Fits known lifecycle, ownership, data, and runtime constraints |
| Operator value | 0.10 | Proves a decision the user actually needs |
| Route clarity | 0.10 | Next owner and entity state are unambiguous |
| Cost and risk | 0.05 | Effort, fragility, and cleanup are acceptable |

Verdicts:

- `proven`: score >= 0.85 and no hard blocker.
- `partial`: score >= 0.60 or useful evidence with unresolved blockers.
- `disproven`: evidence falsifies the claim or required path is blocked.
- `monitor`: not worth acting on now, but worth revisiting.
- `reject`: no current route, value, or credible proof path.

## Output Contract

```yaml
poc_result:
  claim: ""
  mode: spike|prototype|production_path|matrix
  prior_art:
    reused: []
    new: []
    stale: []
  evidence:
    artifacts: []
    commands: []
    citations: []
    gaps: []
  matrix:
    evidence_strength: 0.0
    production_path_fit: 0.0
    verifier_strength: 0.0
    architecture_fit: 0.0
    operator_value: 0.0
    route_clarity: 0.0
    cost_and_risk: 0.0
    weighted_score: 0.0
  verdict: proven|partial|disproven|monitor|reject
  route: propose|capture|exec|monitor|archive|reject|revise_poc
  next: ""
```

## Stopgap Loop Note

For handwritten skills, a temporary loop may use the operator-approved sleep
tick pattern when a real FlowMind runner is not available. Do not copy that
pattern into generated `lev exec --flow` skills. FlowMind-authored skills should
get loop behavior from the flow/runtime contract.

## Red Baseline

The proof is invalid when any of these statements are true:

- "POC is the disposition." POC is a route; disposition is adopt, extract,
  monitor, or reject when workshop intake owns the decision.
- "A demo exists, so the production path is proven." Demos prove only the demo
  unless the real path was exercised.
- "Prior art can be skipped." Repeated concepts must be identified before
  claiming novelty.
- "The verifier exists, so the claim is true." A verifier is useful only when it
  can falsify the relevant claim.

## Related

- `/capture` records proof results and entity movement.
- `/interview` and `/design` clarify ambiguous proof claims.
- `/propose` turns proven or aligned results into execution-ready task DNA.
- Workshop intake owns adopt, extract, monitor, and reject dispositions.
