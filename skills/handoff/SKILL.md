---
name: handoff
description: Use when closing or pausing a session by updating workstream state and copying a resume prompt.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /handoff - Session Close Ceremony

Update the active workstream state and copy a concise resume prompt. Handoff
markdown is a projection; workstream YAML is the durable identity.

## Work Link

Lifecycle lane: Close
Entity movement: `verified | paused | blocked -> resumable`
Workstream: update `.lev/pm/workstreams/<id>/state/workstream.yaml`
Upstream: `/close`, stop hook, user pause, context compaction
Downstream: next session via resume prompt
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Protocol

```yaml
steps:
  - id: identify_workstream
    action: Select the active workstream that matches the session.
    validation: "A single workstream id is selected or created from clear session context."
    on_failure: "Ask only if the objective cannot be inferred."

  - id: update_state
    action: Write structured state to the workstream YAML.
    validation: "State includes phase, status, shipped work, decisions, blockers, and next vision."
    on_failure: "Do not emit a resume prompt until state is durable."

  - id: copy_resume
    action: Copy a resume prompt with workstream id, last shipped summary, blockers, and next step.
    validation: "pbcopy succeeds or the prompt is printed as fallback."
    on_failure: "Report that clipboard copy failed and include the prompt."

  - id: report_hud
    action: Report updated state path and HUD.
    validation: "User sees the path and resumable next action."
    on_failure: "Add the path and HUD."
```

## Workstream YAML Shape

```yaml
workstream_id: <slug>
title: <human readable>
objective: <what this workstream achieves>
phase: shape | plan | exec | close | eval
status: active | paused | completed | superseded
owner: <who>
provenance_ref: null
lineage_ref: null
decision_refs: []
question_refs: []
follow_up_refs: []
extensions:
  session_N:
    date: 'YYYY-MM-DD'
    ships: []
    blockers: []
    vision_next_session: []
```

## Resume Prompt

```text
Resume workstream <ID>. Read .lev/pm/workstreams/<ID>/state/workstream.yaml.

Last session shipped: <1-2 sentence summary>
Blockers: <list or none>
Next: <next lifecycle verb and entity>
```

## Rules

- Do not write new `.lev/pm/handoffs/` markdown unless explicitly requested.
- Do not rebase during close or handoff.
- Do not claim closure if the workstream state was not updated.
- Commit/push belongs to `/close` when sealing verified work; `/handoff` can pause
  without forcing a commit when the user is only preserving context.
