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
    action: Reconcile evidence, refresh the rolling horizon, then write structured state to the workstream YAML.
    validation: "State includes phase, status, shipped work, decisions, blockers, outcome/map refs, tracker binding, and at most ten stable-ID horizon steps; steps 1-3 meet the recursive wayfinding fidelity contract."
    on_failure: "Do not emit a resume prompt until state is durable."

  - id: copy_resume
    action: Copy a redacted pointer-first resume prompt tailored to the requested next-session focus, with workstream id, last shipped summary, blockers, and suggested skill routes.
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
phase: plan | exec | eval
sub_phase: <optional descriptive lane, e.g. shape or close>
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

If the user supplies a next-session focus, tailor the prompt to that focus while
preserving unresolved constraints and blockers. Reference existing plans, ADRs,
issues, commits and diffs by path or URL instead of copying their contents.
Preserve observed status literally: `implementation incomplete` does not prove
that nothing shipped, and an unknown cause does not become a diagnosis. Separate
completed work, partial work, observed symptoms, hypotheses and unknowns; omit a
category when the source does not establish it.
Include suggested `skill://<name>` routes with the condition for invoking each.
Redact credentials, tokens and unnecessary personal information from exported
text and clipboard content; point to the authorized source without reproducing
secrets. Handoff does not grant the next agent new permissions.

For a long-horizon effort, read
[recursive wayfinding](../lev/references/recursive.md) before updating state.
Project the current rolling horizon from the outcome map after reconciling this
session's evidence. Preserve stable IDs when positions change. Include all
available detail for steps 1-3: outcome/question, owner or route, prerequisites,
permitted effects, check/evidence, and stop condition. Summarize steps 4-10 by
milestone, dependency, and main uncertainty. Keep later milestones and
exclusions in the outcome map rather than copying them into the resume prompt.
Name what changed and why; do not convert unknowns into planned actions.

When the user requests a portable handoff document, write the redacted projection
in an OS temporary directory and return its exact path. Keep workstream YAML as
canon; the export is disposable and must identify the canonical state reference.
Ordinary handoff uses the resume prompt only; create a repository Markdown
handoff only when explicitly requested. If the destination lacks repository
access, state which references must be supplied rather than silently presenting
an inaccessible pointer as sufficient context.

```text
Resume workstream <ID>. Read .lev/pm/workstreams/<ID>/state/workstream.yaml.

Last session shipped: <1-2 sentence summary>
Blockers: <list or none>
Outcome: <stable outcome or ref>
Tracker: <bound backend and task identity or blocker>
Rolling horizon: <steps 1-10 with stable IDs; steps 1-3 highest fidelity>
Navigation delta: <what changed and evidence that changed it>
Next: <next eligible lifecycle verb and entity, or quiet wait condition>
Suggested skills: <skill://name — invocation condition>
Next-session focus: <requested focus or saved next action>
```

## Next Routes

Handoff preserves a next route for a later session; it does not dispatch it.
Include the applicable `skill://<name>` destination in the resume prompt. Show a
numbered table only if the user must choose among genuinely different resumptions.

| Resumption condition | Next owner |
|---|---|
| Resume the saved effort | `skill://ws` with the workstream ID, then its saved eligible next verb |
| New evidence or intent to preserve | `skill://capture` |
| Decision blocking resumption | `skill://interview` |
| Plan needs repair before more work | `skill://lev-plan` |
| Coding slice needs a revised contract | `skill://propose` |
| Authorized action ready; contract remains current | `skill://exec`; non-coding may consume its sufficient plan directly |
| Domain or next owner unknown | `skill://lev` |

## Rules

- Do not write new `.lev/pm/handoffs/` markdown unless explicitly requested.
- Do not rebase during close or handoff.
- Do not claim closure if the workstream state was not updated.
- Commit/push belongs to `/close` when sealing verified work; `/handoff` can pause
  without forcing a commit when the user is only preserving context.
