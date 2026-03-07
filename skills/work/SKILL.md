---
name: work
description: Process/workflow router for tracked workstreams. Use when users ask to plan, execute, validate, handoff, resume, or close work. On trigger, immediately initialize tracker + active handoff, track entities, and append tick updates every substantive iteration.
---

# Work: Self-Contained Process Router

`/work` is process and workflow only.

- No FlowMind runtime assumptions.
- No graph-runtime assumptions.
- No external design-theory dependency to run the loop.

## On Load: Do This Immediately (Hard Contract)

1. Detect tracker backend (`bd > br > td > none`).
2. Resolve active workstream name from user request.
3. Open or create active handoff file in `.lev/pm/handoffs/`.
4. Initialize or update entity matrix.
5. Append current tick (`Tn`) with objective and first evidence.

If step 3 fails, stop implementation work and create the handoff first.

## Canonical Naming (Hard Contract)

Use this filename format for handoffs:

`{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`

Examples:
- `20260301-work-skill-core-reconstruction-session-1.md`
- `20260301-sdlc-docs-gates-audit-session-3.md`

Rules:
- `session-1` only when `predecessor: null`.
- Continue an existing stream with `session-{N+1}`.
- Do not start a new `session-1` for the same active stream unless explicitly requested.

## Required Handoff Frontmatter

```yaml
---
status: active | paused | completed
workstream: <slug>
component: <slug>
slug: <slug>
session: <N>
created_at: YYYY-MM-DD
predecessor: <filename.md | null>
confidence: 0.0-1.0
decisions_start: D<N>
---
```

## Required Handoff Sections

Every active handoff must contain:

1. `You Are Here`
2. `Next Agent Brief`
3. `Timeline` (tick log)
4. `Decisions Log`
5. `Open Questions`
6. `Entity Matrix`
7. `Meta`

## Entity Model (Minimum)

Track entities in the handoff `Entity Matrix`.

Required columns:

`# | Entity | Lifecycle | Blocked By | Next Action`

Lifecycle values (process-only):
- `intake`
- `researching`
- `proposing`
- `specifying`
- `executing`
- `validating`
- `completed`
- `parked`

Use one row minimum even for single-entity sessions.

## Tick Definition and Update Rule (Hard Contract)

A tick is required for each substantive change.

Substantive means:
- Entity lifecycle state changed.
- Decision made.
- Gate pass/fail evaluated.
- Research batch completed.
- User correction changed direction.
- Code/docs/tests were modified.

Not substantive:
- Basic file reads.
- Command retries.
- Internal thinking without state change.

### Tick Entry Format

```markdown
### T{N}: <type> <title>

<what changed>

**Now understood**: <state delta>
**Refs**: `path:line`, `doc.md`, `issue-id`
```

## Handoff Update Cadence (Hard Contract)

- Context 0-50%: update handoff every 3-5 substantive turns.
- Context 50-75%: update every 2 substantive turns.
- Context 75%+: update immediately after each substantive turn.

Do not defer handoff updates until session end.

## Tracker Adapter (Inline, No External Read Required)

Detection:

```bash
command -v bd >/dev/null && TRACKER=bd || { command -v br >/dev/null && TRACKER=br || { command -v td >/dev/null && TRACKER=td || TRACKER=none; }; }
```

Command map:

| Operation | bd | br | td |
|---|---|---|---|
| create | `bd create --title "..." --type task` | `br create --title "..." --type task` | `td add "..."` |
| list | `bd list --status open` | `br list --status open` | `td` |
| show | `bd show <id>` | `br show <id>` | `td <id>` |
| update status | `bd update <id> --status <s>` | `br update <id> --status <s>` | `td <id> edit` |
| close | `bd close <id>` | `br close <id>` | `td <id> complete` |
| search | `bd search "<q>"` | `br search "<q>"` | grep fallback |

Degrade gracefully:
- `td`: no deps/ready/sync semantics.
- `none`: continue without tracker, but record it in handoff.

## Process Loop (Operational Core)

Run this loop for each entity:

1. **DISCOVER**
- Gather context from code/docs/tasks/history.
- Record first evidence in tick log.

2. **ALIGN**
- Confirm objective, scope, constraints, success criteria.
- If underspecified, ask focused questions before executing.

3. **RESEARCH**
- Pull prior art and current implementation facts.
- Record sources in tick refs.

4. **PROPOSE**
- Write concrete approach and alternatives.
- If non-trivial, produce proposal artifact.

5. **SPECIFY**
- Produce behavioral spec with BDD-style scenarios and acceptance criteria.

6. **EXECUTE**
- Implement smallest testable slice.
- For substantial work: use `impl` + `review/fixes` subagents.

7. **VALIDATE**
- Validate changed behavior (tests/build/checks or doc consistency checks).
- Record pass/fail in tick.

8. **EMIT**
- Emit artifact updates (report/proposal/spec/handoff updates).

9. **LEARN**
- Capture what worked/failed in handoff `Learned Patterns`.

## Minimal Gates (Enforceable)

### Gate A: Preflight (before execute)
Must have:
- active handoff
- objective stated
- at least one evidence reference

Else: block execution.

### Gate B: Design Ready (non-trivial work)
Must have:
- proposal-level approach
- acceptance criteria
- rollback note

Else: block execution.

### Gate C: Validate Before Close
Must have:
- validation evidence recorded
- open blockers listed or resolved
- next action clear

Else: block close.

## Template Loading Rules (Hard Contract)

Load templates explicitly:

1. Always load:
- `~/.agents/skills/work/templates/handoff.md`

2. Load as needed:
- `~/.agents/skills/work/templates/report.md`
- `~/.agents/skills/work/templates/proposal.md`
- `~/.agents/skills/work/templates/spec.md`

Do not assume any other template exists.

## Subagent Contract

For substantial work (multi-file, cross-module, high-risk):
- Spawn `impl` subagent.
- Spawn `review/fixes` subagent.

Each subagent must return:
- `edited_files`: absolute paths
- `summary`: 1-2 sentence executive brief
- `report_path`: only if output > 5000 tokens

## Error Handling

| Error | Response |
|---|---|
| Missing handoff | Create handoff first, then continue |
| Missing tracker | Continue and note `TRACKER=none` |
| Missing template | Fallback to inline section format, record deviation |
| Validation failed | Block close, add remediation tick |
| Repeated gate failure (3x) | Escalate to user with options |

## Session Close Checklist

1. Final handoff update (entity matrix, decisions, ticks, open questions).
2. Mark session status (`active` or `completed`).
3. Record next concrete action in `Next Agent Brief`.
4. If code changed, run applicable validations and record evidence.

## Non-Goals for This Skill

- Defining FlowMind action vocabularies.
- Defining graph runtime semantics.
- Defining protocol-handler architecture.

Those belong to dedicated skills/workstreams.

## Status

`work` is now process/workflow-only and self-contained.
