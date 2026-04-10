---
name: handoff
description: Session close ceremony. Writes workstream state + pbcopy resume prompt. Use when closing a session, before /clear, or when the stop hook fires.
---

# /handoff — Session Close Ceremony

Write the active workstream state and copy a resume prompt to clipboard.

## Protocol

1. **Identify the active workstream.** Scan `.lev/pm/workstreams/*/state/workstream.yaml` for `status: active`. If multiple, pick the one matching the current session's work. If none, create one from the session's work.

2. **Update the workstream YAML.** Write structured state to `.lev/pm/workstreams/<id>/state/workstream.yaml`. Include:
   - Current phase and status
   - What was shipped (files modified, beads closed)
   - Decisions made
   - Blockers
   - Vision for next session
   - Session metadata in `extensions.session_N`

3. **Commit and push.** Stage the workstream YAML + any uncommitted work. Commit. Push.

4. **Generate resume prompt and pbcopy.** Build a concise prompt that the next session can paste to recover context:

```bash
RESUME=$(cat <<'PROMPT'
Resume workstream <ID>. Read .lev/pm/workstreams/<ID>/state/workstream.yaml for full context.

Last session shipped: <1-2 sentence summary>
Blockers: <list or "none">
Next: <what to do>
PROMPT
)
echo "$RESUME" | pbcopy
echo "Resume prompt copied to clipboard."
```

5. **Report.** Tell the user what was written and that the resume is in their clipboard.

## Rules

- **Workstreams, not handoffs.** Never write to `.lev/pm/handoffs/`. Workstreams are the durable identity.
- **Structured YAML, not markdown.** The workstream state is YAML. Markdown is a projection.
- **pbcopy is the resume.** No separate resume command. Copy-paste IS the bridge.
- **Git push completes the ceremony.** Work is not done until pushed.

## Workstream YAML Shape

```yaml
workstream_id: <slug>
title: <human readable>
objective: <what this workstream achieves>
phase: plan | exec | eval
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
    ships: [list of what was done]
    beads_closed: [bead IDs]
    beads_filed: [bead IDs]
    blockers: [list]
    vision_next_session: [list]
```

## When No Workstream Exists

Create one:
1. Ask: "What's the one-sentence objective for this work?"
2. Generate workstream_id via slugify
3. Write the YAML
4. Continue with the ceremony
