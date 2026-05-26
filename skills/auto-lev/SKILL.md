---
name: auto-lev
description: Use when running a visible Lev autopilot that coordinates research, interview, arch, propose, AgentPing, warm-worker intent, realtime dashboard intent, and lev exec updates across the lifecycle.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /auto-lev - Visible Lifecycle Autopilot

`/auto-lev` is a stopgap, text-visible autopilot skill. It virtualizes the
future FlowMind loop by stepping through Lev lifecycle skills with an explicit
sleep barrier between ticks. It must show every decision, loop route, artifact,
and handoff in text.

## Work Link

Lifecycle lane: Router -> Shape -> Plan -> Exec
Entity movement: `intent -> framed -> researched -> architected -> proposed -> execution_ready | needs_interview | blocked`
Workstream: resolve active workstream before writing, dispatching, or calling `lev exec`
Upstream: user intent, `/capture`, `/work`, existing workstream state
Downstream: `/interview`, `/research`, `/arch`, `/propose`, `/exec`, AgentPing, dashboard, FlowMind
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦auto-lev={state}/{tick} | ⏭️ {next} | 🔁{loop_state}`

## Commands

```bash
/auto-lev "<intent>"                 # run visible lifecycle autopilot
/auto-lev --dry-run "<intent>"       # show loop plan without executing
/auto-lev --max-ticks=8 "<intent>"   # cap autonomous turns
/auto-lev --sleep=1s "<intent>"      # default stopgap tick sleep
/auto-lev status                     # summarize current loop state
```

## Non-Negotiables

- Every tick prints normal text output before any sleep.
- Every sleep is visible as `bash -lc 'sleep 1'` or the requested interval.
- No hidden "I'll keep working" blocks; if work continues, the next text turn
  says what happened, what changed, and what gate is next.
- `lev exec` only runs after `/propose` or an equivalent task contract has an
  execution-ready slice and verifier.
- A warm worker is an intent or queued role unless a real runtime lease exists.
  Do not claim standby workers, dashboards, or AgentPing surfaces are live unless
  verified.

## Loop Selection

```yaml
loops:
  ambiguity:
    use_when: "Intent, outcome, scope, constraints, or success criteria are unclear."
    cycle:
      - "interview: ask or answer the smallest ambiguity question"
      - "sleep: bash -lc 'sleep 1'"
      - "arch: classify level, quality attributes, tradeoffs, and risk"
      - "sleep: bash -lc 'sleep 1'"
      - "interview: continue with the next highest-leverage question"
    exit: "ambiguity below threshold or one blocking human decision remains"

  research_options:
    use_when: "User asks to explore 2-3 solutions, compare tools, or gather current evidence."
    cycle:
      - "research: local first, external/current only when needed"
      - "sleep: bash -lc 'sleep 1'"
      - "arch: compare options, tradeoffs, quality attributes, and fitness functions"
      - "sleep: bash -lc 'sleep 1'"
      - "propose: recommend one slice or ask for one alignment decision"
    exit: "recommended route and evidence are clear"

  propose_plan:
    use_when: "Context is aligned enough to plan execution."
    cycle:
      - "propose: build or revise task DNA and execution YAML"
      - "sleep: bash -lc 'sleep 1'"
      - "arch: adversarial review of tradeoffs, risks, and fitness functions"
      - "sleep: bash -lc 'sleep 1'"
      - "propose: update gate score and next exec slice"
    exit: "execution_ready gate passes or missing decision is explicit"

  exec_update:
    use_when: "User wants updates applied through Lev."
    cycle:
      - "propose: verify execution-ready slice and write scope"
      - "sleep: bash -lc 'sleep 1'"
      - "exec: run lev exec or route to /exec with verifier"
      - "sleep: bash -lc 'sleep 1'"
      - "verify: report command, artifact, receipt, dashboard, or AgentPing state"
    exit: "verifier passes, blocker found, or human approval needed"

  surface_feedback:
    use_when: "User wants generative UI, AgentPing, realtime dashboard, or artifact visibility."
    cycle:
      - "research: inspect existing surface/runtime prior art"
      - "sleep: bash -lc 'sleep 1'"
      - "arch: choose surface boundary and observability contract"
      - "sleep: bash -lc 'sleep 1'"
      - "propose: create the smallest visible artifact/update slice"
    exit: "surface proof path is selected"
```

## Protocol

```yaml
steps:
  - id: resolve_context
    action: Load active workstream, related entities, current request inventory, and prior artifacts.
    validation: "Response names workstream id, intent, candidate loop, artifact targets, and unresolved gates."
    on_failure: "Route to /work or /capture before autopilot starts."

  - id: bind_intent
    action: Restate what the user wants working first and what should be explored next.
    validation: "Intent has first outcome, 2-3 solution/exploration branches if requested, and success signal."
    on_failure: "Run the ambiguity loop."

  - id: run_visible_tick
    action: Execute exactly one lifecycle skill move and print the result.
    validation: "Tick output includes skill, reason, artifacts touched, gate score or blocker, and next loop."
    on_failure: "Stop the loop and explain the missing contract."

  - id: sleep_barrier
    action: Run a visible sleep between ticks.
    validation: "The sleep command and duration are shown in text."
    on_failure: "Do not pretend a paced loop happened."

  - id: route_artifacts
    action: Move results into capture, decision, proposal, task, dashboard, AgentPing, or exec lane.
    validation: "Each artifact has a path/id or is explicitly marked proposed/not-yet-real."
    on_failure: "Keep it ephemeral and route to capture."

  - id: decide_next
    action: Continue, ask, propose, exec, monitor, or stop based on gates and budget.
    validation: "Next action is one slice, not a batch of unrelated work."
    on_failure: "Emit a one-question alignment prompt."
```

## Tick Template

<auto-lev-tick>
## auto-lev tick {n}: {loop_name}

Intent: {intent}
Loop route: {previous_skill} -> {current_skill} -> {next_skill}
Why now: {gate_or_reason}
Visible work:
- {fact_or_action_1}
- {fact_or_action_2}
Artifacts:
- {path_or_id_or_ephemeral}
Gate: {score_or_state}
Sleep: `bash -lc 'sleep {seconds}'`
Next: {one_next_tick_or_question}
</auto-lev-tick>

## Warm Worker Virtualization

Represent standby execution as structured intent until runtime proves it:

```yaml
warm_worker_intent:
  role: updater|researcher|architect|proposal_writer|verifier
  desired_state: standby
  runtime: tmux|lev-daemon|flowmind|not_started
  lease_id: null
  proof_required:
    - heartbeat
    - inbox
    - transcript_or_receipt
    - active_workstream
```

## RED Baseline

These are the failure modes this skill exists to prevent:

| Excuse | Reality |
|---|---|
| "I'll continue silently and summarize later." | Autopilot must show every tick in text. |
| "The user asked for exec, so I can run it now." | `lev exec` requires an execution-ready contract and verifier. |
| "A warm worker is on standby because we described one." | Standby requires a real lease, heartbeat, inbox, and transcript. |
| "Research can come from memory." | Current/external research routes through the research surface; local truth routes through repo search. |
| "Architecture can be skipped because propose will catch it." | Arch review owns tradeoffs, quality attributes, and fitness functions before risky execution. |
| "AgentPing/dashboard exists as intent, so it is done." | Surface artifacts are proposed until verified by path, command, URL, or receipt. |

## Stop Conditions

- Human asks to stop or changes direction.
- Max ticks, token budget, or time budget reached.
- Ambiguity cannot reduce without human judgment.
- Execution-ready gate fails.
- Verifier fails or a safety/permission gate blocks.
- All requested artifacts have paths/ids and next owner is clear.

## Related

- `/interview` reduces ambiguity.
- `/research` gathers current or deep external evidence.
- `/arch` evaluates architecture tradeoffs and fitness functions.
- `/propose` creates task DNA and execution YAML.
- `/exec` runs verified execution slices.
- `/autodev-lev` is the longer-running heartbeat implementation this skill should eventually compile into or hand off to.
