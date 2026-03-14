---
name: work
description: |
  [WHAT] Session lifecycle router — handoff-first, entity-tracked, prior-art-aware
  [HOW] 6-step operational loop: handoff → track → align → research → plan → close
  [WHEN] Use for all tracked work: plan, design, build, research, analyze, handoff, resume, close
  Triggers: "work", "plan", "design", "research", "handoff", "close", "resume"
---

# Work: Session Lifecycle Router (v4)

One entry point for all work. The agent's job is to maintain a living handoff that tracks what's happening, what was decided, and what's next. Everything else flows from that.

```
Save Handoff → Track Entities → Align → Prior Art + Research → Plan + Execute → Close
     ↑              ↑                         ↑                                   |
     └──────────────┴─── update handoff continuously ─────────────────────────────┘
```

Execution is optional. Brainstorming and conversation mode are valid — the handoff still tracks it.

---

## Step 1: Save the Handoff (do this NOW)

Before anything else, open or create the active handoff in `.lev/pm/handoffs/`.

**Filename:** `{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`
- `session-1` only when no predecessor exists
- Continue existing streams with `session-{N+1}`

**Handoff skeleton** (write this immediately):

```yaml
---
status: active | paused | completed
workstream: {slug}
component: {slug}
slug: {slug}
session: {N}
created_at: YYYY-MM-DD
predecessor: {filename.md | null}
confidence: 0.0-1.0
decisions_start: D{N}
---
```

```markdown
# Session Handoff: {title}

## You Are Here
**Workstream:** {x} | **Component:** {x} | **Session:** {N} | **Status:** active
{one sentence: what is in progress, what happens next}

## Next Agent Brief
- **Long-Term Goal:** {overall objective}
- **Done Condition:** {deterministic completion test}
- **Current Execution Slice:** {what this session advances}
- **Why This Slice Now:** {rationale}
- **Out of Scope:** {excluded work}

## Roadmap To Goal
**Goal:** {end state} | **Done Condition:** {test} | **Remaining Steps:** {0-10}

### Step 1: {current slice} ← detail this one
- {concrete bullets, 1-10}
- {validation/exit criteria}

### Steps 2-5 (optional, 1-3 bullets each)
### Steps 6-10 (optional, one-liners only)

Do not invent filler steps. When Step 1 completes, shift forward and detail the new Step 1.

## Timeline
| Tick | What Changed | Refs |
|------|-------------|------|
| T1 | {state delta} | `path:line` |

## Decisions Log
### D{N}: {title}
**Decision:** {what} | **Rationale:** {why} | **Alternatives:** {rejected options}

Promote to `.lev/pm/decisions/` only when: architectural, cross-workstream, or policy-setting.

## Open Questions
1. {question or unresolved decision}

## Entity Matrix
| # | Entity | Lifecycle | Blocked By | Next Action |
|---|--------|-----------|-----------|-------------|
| 1 | {name} | {state} | {blocker} | {action} |

## Meta
**Project State:** {brief} | **Current Focus:** {what + why}
**Critical Knowledge:** 1. {insight} 2. {insight} 3. {insight}

### System Prompt for Next Agent
{Summary of session + immediate next steps + files to load}

### Context Confidence: {0.0-1.0}
{What's missing, what to load first}
```

### Tick format

Log a tick for each substantive change (entity state change, decision, gate pass/fail, user correction, code modified). Not for file reads or retries.

```markdown
### T{N}: {type} {title}
{what changed}
**Now understood:** {state delta}
**Refs:** `path:line`, `doc.md`, `issue-id`
```

### Update cadence

- Context 0-50%: update handoff every 3-5 substantive turns
- Context 50-75%: every 2 turns
- Context 75%+: every turn

### Sharding

Split to `session-{N+1}` when: ~500 lines and still dense, or >15 ticks, or >5 active entities, or >3 major pivots.

---

## Step 2: Where Are We? (Track Entity Lifecycle)

Every entity being worked on gets a row in the Entity Matrix. Update lifecycle state as work progresses.

| State | Artifact Path | Trigger Keywords |
|-------|--------------|-----------------|
| `ephemeral` | `.lev/scratch/` | "explore", "brainstorm" |
| `captured` | `.lev/pm/reports/` | "research", "analyze", "scan" |
| `classified` | `.lev/pm/reports/` | "classify", "align", "categorize" |
| `crystallizing` | `.lev/pm/proposals/` or `.lev/pm/designs/` | "design", "propose", "architect" |
| `crystallized` | `.lev/pm/specs/` or `.lev/pm/plans/` | "plan", "specify", "implement" |
| `manifesting` | `.lev/pm/handoffs/` | "working on", "in progress" |
| `completed` | `.lev/pm/validation-reports/` | "done", "finished", "closed" |

Entity matrix format:

```markdown
| # | Entity | Lifecycle | Blocked By | Next Action |
|---|--------|-----------|-----------|-------------|
| 1 | work-skill-v4 | crystallized | none | implement |
```

---

## Step 3: Conversation Until Aligned

You're either **brainstorming** (exploring, no clear target) or **planning** (clear target, refining approach). Both are valid. The handoff tracks either mode.

1. If objective, scope, or constraints are unclear — ask focused questions
2. Update the handoff with each substantive exchange (ticks)
3. When the user signals alignment ("agreed", "let's do it", "yes", or equivalent) → move to Step 4
4. If staying in conversation mode, keep updating the handoff — skip Steps 4-5

---

## Step 4: Prior Art + Research (launch subagents automatically)

Before planning or creating new artifacts, search for what already exists. Launch 1-n subagents in parallel for these searches:

### Search matrix

| Source | Command | Finds |
|--------|---------|-------|
| PM designs | `ls .lev/pm/designs/` + `grep -rl "{topic}" .lev/pm/designs/` | Existing design proposals |
| PM plans | `ls .lev/pm/plans/` + `grep -rl "{topic}" .lev/pm/plans/` | Active execution plans (skip `_done/`) |
| PM specs | `grep -rl "{topic}" .lev/pm/specs/` | PM-level specifications |
| PM decisions | `grep -rl "{topic}" .lev/pm/decisions/` | Prior architectural decisions |
| Canonical specs | `grep -rl "{topic}" docs/specs/` | Published specifications |
| Design docs | `grep -rl "{topic}" docs/design/` | Design rationale |
| Architecture | `grep -l "{topic}" docs/ARCHITECTURE.md` | Architectural constraints |
| Vernacular | `grep "{topic}" docs/vernacular.md` | Terminology conventions |
| Tracker | `bd search "{topic}"` | Open/closed work items |
| Codebase | `grep -r "{topic}" --include="*.ts" --include="*.md" -l` | Code + docs references |

### What to do with findings

Present a summary table to the user:

```markdown
| Found | Path | Relationship | Action |
|-------|------|-------------|--------|
| {artifact} | {path} | extends / supersedes / related | Update existing / Create new |
```

If substantial prior art exists, ask: **extend existing or create new?**

### Research report skeleton (save to `.lev/pm/reports/`)

```yaml
---
type: report
status: complete
scope: prior-art | research | analysis
confidence: 0.0-1.0
---
```

```markdown
# {Topic} Prior Art + Research

## Findings
| Source | Path | Key Insight |
|--------|------|------------|
| {source} | {path} | {what it says} |

## Recommendations
- Extend: {list artifacts to update}
- Create: {list new artifacts needed}
- Skip: {list irrelevant findings}
```

For deeper research (web, external libraries, academic), use `lev-research` or web search tools as needed.

---

## Step 5: Plan and Execute (optional)

Skip this step if you're in conversation/brainstorm mode. Enter when there's a concrete execution slice.

### Route by keyword

| Keywords | Action | Artifact | Skill |
|----------|--------|----------|-------|
| "research", "analyze", "scan" | Gather evidence | `.lev/pm/reports/` | `lev-research` |
| "design", "propose", "architect" | Shape solution | `.lev/pm/designs/` or `.lev/pm/proposals/` | `cdo`, `ux` |
| "plan", "implement", "bugfix" | Execution slice | `.lev/pm/plans/` | inline or subagents |
| "specify", "spec" | Behavioral contract | `.lev/pm/specs/` | inline |
| "learn", "guide me" | Guided intake | `.lev/pm/proposals/` | `interview` |

### Plan skeleton (save to `.lev/pm/plans/`)

```yaml
---
type: plan
plan_kind: impl | bugfix | chore | research
status: draft | ready | in_progress | complete
confidence: 0.0-1.0
---
```

```markdown
# Plan: {title}

## Goal
{one sentence}

## Done Condition
{deterministic test}

## Execution Steps
1. {step}
2. {step}

## Validation
- [ ] {check}

## Risks
- {risk or unknown}
```

### Subagent spawning

For multi-file or cross-module work:
- Spawn `impl` subagent with: task description + inlined skill content + workspace context
- Spawn `review` subagent after implementation
- Each returns: `edited_files` list + 1-2 sentence summary + `report_path` if >5000 tokens

### Gates (3 total)

**Preflight (before execute):** Active handoff exists + objective stated + at least one evidence reference. Else block.

**Design ready (non-trivial work):** Approach documented + acceptance criteria + rollback note. Else block.

**Validate before close:** Validation evidence recorded + open blockers listed or resolved + next action clear. Else block.

---

## Step 6: Close Session

1. Final handoff update — entity matrix, decisions, ticks, open questions
2. Mark session status (`active` or `completed`)
3. Record next concrete action in Next Agent Brief
4. If code changed: run applicable validations, record evidence
5. Capture learned patterns (what worked / what didn't) in handoff Meta
6. If any decision is architectural/cross-workstream: promote to `.lev/pm/decisions/`
7. Git commit + push

### Decision skeleton (for promotion to `.lev/pm/decisions/`)

```yaml
---
id: "dXX"
title: "Decision Title"
status: accepted | proposed | superseded
---
```

```markdown
# ADR: {title}

## Context
{what led to this}

## Decision
{what was decided}

## Rationale
{why}

## Alternatives
- {option}: {why rejected}

## Consequences
- {impact}
```

### Done check

Before marking `completed`, verify: goal met + done condition satisfied + no material gaps in reflection. If gaps found, update roadmap and re-enter the lifecycle.

---

## Tracker Adapter

Detect: `bd > br > td > none`. Degrade gracefully.

```bash
command -v bd && TRACKER=bd || { command -v br && TRACKER=br || { command -v td && TRACKER=td || TRACKER=none; }; }
```

| Operation | bd | br | td |
|-----------|-----|-----|-----|
| create | `bd create --title "..." --type task` | `br create --title "..." --type task` | `td add "..."` |
| list | `bd list --status open` | `br list --status open` | `td` |
| show | `bd show {id}` | `br show {id}` | `td {id}` |
| update | `bd update {id} --status {s}` | `br update {id} --status {s}` | `td {id} edit` |
| close | `bd close {id}` | `br close {id}` | `td {id} complete` |
| search | `bd search "{q}"` | `br search "{q}"` | grep fallback |

If `TRACKER=none`, continue without tracker and note it in the handoff.

Tracker items represent the current execution slice ONLY. Long-term roadmap stays in the handoff.

---

## Error Handling

| Error | Response |
|-------|----------|
| Missing handoff | Create handoff first, then continue |
| Missing tracker | Continue, note `TRACKER=none` in handoff |
| Validation failed | Block close, add remediation tick |
| Repeated gate failure (3x) | Escalate to user with options |
| Prior art search empty | Proceed to planning, note "no prior art found" |

---

## Non-Goals

- Defining FlowMind action vocabularies or graph runtime semantics
- Defining protocol-handler architecture
- Replacing specialist skills (cdo, ux, lev-research) — route to them instead
