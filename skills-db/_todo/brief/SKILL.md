---
name: brief
description: Use when the user wants the current conversation or captured context turned into a lifecycle artifact without a long interview, especially before proposal planning.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /brief - Artifact Brief Route

`/brief` is a thin lifecycle route into `interview --auto`. It exists because
`/design` reads as UI/UX even when the needed output is a product,
architecture, decision, or planning artifact.

## Work Link

Lifecycle lane: Shape -> Plan
Entity movement: `captured | context -> artifact_ready | needs_interview | needs_prior_art`
Workstream: resolve active workstream before writing artifacts
Upstream: `/capture`, `/dump`, conversation, `/work`
Downstream: `/interview --auto`, `/prior-art`, `/propose`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦brief={gate}/{score} | ⏭️ {next} | 🔁{loop_state}`

## Commands

```bash
/brief                 # run /interview --auto --standard --compact
/brief --quick         # auto artifact pass, ambiguity gate <= 0.30
/brief --standard      # default, ambiguity gate <= 0.20
/brief --deep          # higher rigor, ambiguity gate <= 0.15
/brief --full          # show richer evidence and trade-offs
/capture --brief       # capture delegation route into /brief
```

## Protocol

```yaml
steps:
  - id: resolve_context
    action: Identify the active workstream, source conversation, and target artifact subject.
    validation: "Workstream, subject, source context, and likely artifact path are known."
    on_failure: "Route to /capture or /ws before writing."

  - id: choose_depth
    action: Select quick, standard, or deep; default to standard.
    validation: "Depth threshold is explicit."
    on_failure: "Use --standard."

  - id: run_auto_interview
    action: Delegate to /interview --auto with the selected depth and output mode.
    validation: "The auto pass inspects context before asking."
    on_failure: "Ask one blocking ambiguity question."

  - id: write_or_route
    action: Write/update the lifecycle artifact or route to prior-art/interview.
    validation: "Artifact path, blocker, or next owner is explicit."
    on_failure: "Keep the item captured; do not promote to /propose."

  - id: offer_next
    action: Route artifact-ready output to /propose or keep it in capture.
    validation: "Next lifecycle step is one of propose, prior-art, interview, capture, or hold."
    on_failure: "Emit the HUD with needs_interview."
```

## Artifact Target

For now, `/brief` still writes through the existing interview artifact contract:
`.lev/pm/designs/<slug>.md` using the work design template. The surface name is
`brief`; the storage contract stays unchanged until decisions, PM mirroring, and
cascading contexts are aligned.

## Auto Gate

```yaml
auto_gate:
  pass_when:
    - ambiguity <= selected_depth_threshold
    - subject is named
    - source context is cited
    - artifact owner/path is known
    - unresolved human judgments are not blocking
  ask_when:
    - subject is unclear
    - artifact path would be invented
    - constraints or success criteria are below threshold
    - prior-art is required before safe synthesis
```

## Output Contract

```yaml
brief_result:
  subject: ""
  source_context: []
  depth: quick|standard|deep
  ambiguity: 0.0
  artifact_path: ""
  status: artifact_ready|needs_interview|needs_prior_art|captured
  next: propose|interview|prior-art|capture|hold
```

## Red Baseline

- Do not use `/design` as the user-facing command for this route.
- Do not turn `/brief` into a UI/UX design skill.
- Do not write an artifact when ambiguity is above the selected gate.
- Do not promote to `/propose` without a concrete artifact path or captured blocker.

## Related

- `/capture --brief` delegates here.
- `/interview --auto` does the artifact synthesis.
- `/propose` consumes aligned artifact output.
