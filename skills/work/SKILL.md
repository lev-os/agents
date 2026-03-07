---
name: work
description: Process/workflow router for tracked workstreams. Use when users ask to plan, execute, validate, handoff, resume, or close work. On trigger, immediately initialize the active handoff, derive the current execution slice, initialize/update a tracker only for that slice, track entities, and append tick updates every substantive iteration.
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
4. Record or confirm the long-term goal, done condition, roadmap, and current execution slice in the handoff.
5. Initialize or update entity matrix.
6. Initialize or update a tracker only for the current execution slice.
7. Append current tick (`Tn`) with objective and first evidence.

If step 3 fails, stop implementation work and create the handoff first.

## Storage Boundary (Hard Contract)

The handoff is the canonical planning artifact.

Store in the handoff:
- long-term goal
- done condition
- roadmap
- deferred work
- evolving decisions
- open questions
- why the current execution slice exists

Trackers (`bd`, `br`, `td`) are execution-plane only.

Store in the tracker:
- the current execution slice
- active implementation task
- blockers on the current slice
- validation or closeout status
- evidence links

Never store long-term plans, end-state framing, or multi-session roadmaps in tracker title, description, or comments unless the user explicitly asks for duplication.

Before every tracker write, check:
1. Is this only about the current execution slice?
2. Would this still be valid if the long-term plan changed?

If either answer is "no", write it to the handoff instead.

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
3. `Roadmap To Goal`
4. `Timeline` (tick log)
5. `Decisions Log`
6. `Open Questions`
7. `Entity Matrix`
8. `Meta`

### Required Next Agent Brief Fields

Every `Next Agent Brief` must state:
- `Long-Term Goal`
- `Done Condition`
- `Current Execution Slice`
- `Why This Slice Now`
- `Out of Scope This Session`

## Roadmap To Goal (Hard Contract)

The handoff must contain a rolling roadmap from current state to the done condition.

### Scope

- The roadmap is a projection of remaining work, not a requirement to invent 10 steps.
- Maximum projection is 10 steps.
- If fewer than 10 steps remain, only list the real remaining steps.
- If remaining steps = 0, the work is in a done-candidate state and must enter reflection before close.

### Required format

```md
## Roadmap To Goal

**Goal**: <one-sentence end state>
**Done Condition**: <deterministic completion test>
**Remaining Steps**: <0-10>

### Step 1: <current execution slice>
- <1-10 concrete bullets>
- <only this step gets full detail>
- <include validation or exit criteria when useful>

### Steps 2-5 (Optional)

#### Step 2: <next phase>
- <1-3 bullets if needed>

#### Step 3: <next phase>
- <1-3 bullets if needed>

#### Step 4: <next phase>
- <1-3 bullets if needed>

#### Step 5: <next phase>
- <1-3 bullets if needed>

### Steps 6-10 (Optional)
6. <one-line future step>
7. <one-line future step>
8. <one-line future step>
9. <one-line future step>
10. <one-line future step>
```

### Rules

- Only Step 1 may contain detailed execution bullets.
- Steps 2-5 are optional and medium-granularity only.
- Steps 6-10 are optional and one-line only.
- Do not invent filler steps to reach 10.
- Tracker items may only represent `Step 1` unless a later step is explicitly pulled forward into the current execution slice.
- When Step 1 completes, shift the roadmap forward and rewrite the new Step 1 in detail.
- When the goal or done condition changes, update the roadmap in the handoff before changing tracker scope.

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

### Tracker Write Rules (Hard Contract)

- Tracker title names the current execution slice, not the full program.
- Tracker description describes only what will be executed in this slice.
- Tracker may link to the handoff path for context.
- Tracker must not duplicate long-term roadmap text from the handoff.
- If tracker text starts reading like a roadmap, stop and move that text to the handoff.

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
- long-term goal recorded in handoff
- done condition recorded in handoff
- `Roadmap To Goal` present, with Step 1 matching the current execution slice
- at least one evidence reference

If a tracker exists:
- tracker scope matches the execution slice only

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
- next action clear, or explicit `done confirmed` from Done Candidate Protocol
- reflection completed if work is in done-candidate state

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
| Tracker-plan boundary violated | Rewrite tracker to execution-slice scope, record correction tick in handoff |
| Validation failed | Block close, add remediation tick |
| Done claimed without reflection | Run Done Candidate Protocol, update roadmap if gaps found, block close |
| Repeated gate failure (3x) | Escalate to user with options |

## Done Candidate Protocol (Hard Contract)

"Done" must be deterministic.

A workstream is not done because implementation appears complete.
A workstream is done only when the done condition is satisfied and the reflection pass finds no material gaps.

### Trigger

Run this protocol whenever:
- `Remaining Steps = 0`, or
- the agent believes the current workstream may be complete

### Required reflection

Before marking a handoff `completed`, the agent must:

1. Review the current handoff.
2. Review all predecessor handoffs in the same workstream.
3. Produce a full status report and alignment check against:
   - goal
   - done condition
   - roadmap
   - decisions log
   - open questions
   - validation evidence
4. Record:
   - lessons learned
   - gaps or misses discovered during reflection
   - whether any pattern, command, template, or rule should be promoted into a skill or AGENTS.md
5. Decide:
   - `done confirmed`, or
   - `not done`

### If reflection finds gaps

- Do not close the workstream.
- Update the handoff roadmap with the newly discovered remaining steps.
- Re-enter the lifecycle at the appropriate stage.
- Record a tick explaining why the done-candidate failed.

### If reflection confirms done

- Mark the handoff `completed`.
- Record the deterministic evidence that satisfied the done condition.
- Record any skill-promotion or process-promotion recommendations.

### Rule

Assume reflection will often find something.
The purpose of the done protocol is to reveal misses before close, not to justify closing.

## Session Close Checklist

1. Final handoff update (entity matrix, decisions, ticks, open questions).
2. Mark session status (`active` or `completed`).
3. Record next concrete action in `Next Agent Brief`.
4. If code changed, run applicable validations and record evidence.
5. Verify tracker text still describes only the execution slice; move any long-term framing back to the handoff.

## Non-Goals for This Skill

- Defining FlowMind action vocabularies.
- Defining graph runtime semantics.
- Defining protocol-handler architecture.

Those belong to dedicated skills/workstreams.

## Status

`work` is now process/workflow-only and self-contained.
