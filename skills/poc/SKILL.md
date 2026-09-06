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

## Prototype Branches

Select the artifact from the question, not the available tool. Derive the
question from the user's prompt and surrounding code (ask when the user is
reachable), and name the state model when the question is about logic. Put a
visible, one-paragraph `Question` / `State model` / `Prototype status`
introduction at the top of the artifact, not only in a comment, so a reviewer
can re-check the intended question later or AFK. Logic/state questions use a
portable interactive model; appearance/layout questions use UI variants. If
the choice remains ambiguous and the user is unavailable, a backend module
defaults to logic and a page or component defaults to UI; state that assumption
at the top. Keep it near its owner, follow existing route conventions, and
provide one-command or one-file usage. Use in-memory state or an explicitly
authorized disposable persistence target, not production mutations. If the
question explicitly involves a database, use a scratch DB or local file whose
name visibly says `PROTOTYPE — wipe me`.

**Logic:** prefer one self-contained HTML file with a small pure reducer, state
machine or function module separated from the DOM shell. Use a state-owning
module with a clear method surface if pure transforms
do not model the question honestly. The page may call the logic module, but the
module must not call the page, DOM, or button handlers; keep that dependency
one-way so the logic can be lifted later. Arrange the demo as a title and
one-line explanation of the question, current state, free-play controls, then
guided walkthroughs. Write it for a non-developer: use domain-language labels
and explain in plain words what is happening. Render the full relevant state
after every action and call out what just changed where that helps. Provide one
always-available free-play button per action so anyone can try actions in any
order. Each guided scenario tab starts from a known reset state, includes a
short plain-language description of the situation and what to watch for, and
supplies ordered real buttons; clicking a step performs its named action and
advances to the next step. Include a normal path, a difficult edge and an
illegal transition attempt. Hand over the actual file or preview; invite
concrete counterexamples, and add requested actions or scenarios within scope
when they sharpen the same question. Surprising behavior is evidence about the
model, not automatic approval. Keep presentation restrained so state changes
remain visible; the portable logic is the candidate decision, not the HTML shell.
For a one-file or double-clickable handoff, inline every required script and
style so the file runs directly under `file://`; external modules instead require
an explicit local server and an actual preview URL. Open the delivered surface in
a browser and exercise a state-changing action—syntax or module-unit checks do
not prove that the page initialized. Render the primary state with domain labels
for a non-developer; raw JSON may be secondary evidence, not the only state view.

**UI:** prefer variants inside the existing host page so actual context and
density inform the choice. Preserve auth, data fetching, and existing route
parameters; vary only the rendered subtree. Use an obviously disposable route
only when no host fits. Start with three structurally different layouts (at most
five unless explicitly requested), using the project's components. Select via a
reload-stable URL parameter; provide a clearly prototype-only floating bottom-bar
switcher with the current label and wrapping previous/next controls. `←` and
`→` keyboard arrows also cycle variants, but must not steal input, textarea, or
contenteditable navigation. Gate prototype controls and exposure from production;
mutations use stubs. On every variant switch, render the full relevant prototype
state in a readable form, excluding secrets and unrelated personal data.
Give each variant a distinct component identity and share the switcher rather
than coupling the layouts. Return the actual preview URL and variant keys so
the user can revisit a choice. Capture combinations the user prefers across
variants, not only a forced single winner.

Capture the question, observed answer, limitations, variant choice/reason and
artifact pointer in the existing workstream/design. Preserve the prototype as
primary evidence; do not automatically create branches, commit or promote it.
Those source defaults are superseded by explicit scope and Git authorization.
On authorized implementation, carry the decision-rich logic or winning design
forward with production-quality checks and remove prototype controls/losing
variants from the shipping path while retaining the evidence pointer.

A prototype optimizes for learning quickly and needs the smallest relevant
runnable check, not a production test suite by default. Source advice to skip
all testing is superseded by Lev's claim-specific verifier requirement. A
clickable demo can resolve a design question; it cannot by itself certify a
production path or user acceptance.

## Proof Protocol

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
    action: "Pick the cheapest credible proof: command, trace, test, demo, doc evidence, or operator review."
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

## Next Routes

Route the result, not the existence of a prototype. Show only applicable next
owners as a numbered `skill://<name>` table when there is a real choice; otherwise
name one route. Proof completion does not authorize implementation.

| Result | Next owner |
|---|---|
| Supported direction spans multiple outcomes | `skill://lev-plan` |
| Supported bounded coding slice | `skill://propose` |
| Supported non-coding action with sufficient plan, scope, and checks | `skill://exec` with the domain method; proposal optional |
| Claim or decision needs reframing | `skill://interview` |
| New insight or rejected hypothesis needs preservation | `skill://capture` |
| Monitor, defer, or stop | `skill://handoff` with the revisit condition; no automatic scheduling |
| Proof itself is the completed requested outcome | `skill://close` |
| Domain route unknown | `skill://lev` |

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
