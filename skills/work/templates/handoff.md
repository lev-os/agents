---
status: active | paused | completed | processed  # processed = decisions graduated via handoff-rollup
workstream: {slug}
component: {slug}
slug: {slug}
session: {N}
created_at: YYYY-MM-DD
predecessor: {filename.md | null}
confidence: 0.0-1.0
decisions_start: D{N}
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
depends_on: []              # other plans (in .lev/pm/plans/) that must complete before this work
canonical_refs: []           # specs/designs/docs that govern this work
---

# Session Handoff: Topic

## How To Fill This Out

Use this template as the canonical session breadcrumb and recovery artifact for `$work`.

This handoff serves two roles at once:
1. A top bootstrap for the next agent or human.
2. A chronological checkpoint trail that recreates how the session reached its current state.

Update the handoff during the session, not only at the end.

Use uncertainty markers whenever needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "Checkpoint 3 captured the user pivot and linked the affected files."
- "The roadmap was refined in session 2 as the goal became clearer."

Bad:
- "Dump everything at the end."
- "Hide uncertainty and pretend context is complete."

Canonical filename format:
`{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`

## You Are Here

**Workstream:** {workstream}  
**Component:** {component}  
**Session:** {N}  
**Status:** active | paused | completed

One sentence on what is in progress and what happens next.

## Next Agent Brief

**Long-Term Goal:** What this workstream is trying to achieve overall.

**Done Condition:** Deterministic completion test for the overall workstream.

**Current Execution Slice:** What this session is actually advancing right now.

**Why This Slice Now:** Why this slice is the correct next move.

**Out of Scope This Session:** Explicitly excluded work.

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

**Roadmap Rules**
- Only Step 1 may contain detailed execution bullets.
- Steps 2-5 are medium-granularity only.
- Steps 6-10 are one-line only.
- Do not invent filler steps.
- Refine the goal, done condition, and roadmap as the work becomes clearer across sessions.
- When Step 1 completes, shift the roadmap forward and rewrite the new Step 1 in detail.

## Handoff Objective

Analyze the current conversation context and manage session state based on the mode and arguments.

For continuity, provide in chronological order:
- files worked on
- files loaded into context
- what was understood after loading them
- why each understanding is important

The goal is to produce a deterministic trail guide through code and context, key decisions, user feedback, and next actions so the next session can recover state quickly.

## Checkpoints (Required: 3-15, chronological)

Two checkpoint tiers. Use light ticks for mechanical actions. Use full checkpoints for significant milestones.

### Light tick (one-liner)

`| T+{N} | {what happened} — {key file or finding} |`

Use for: file reads, grep scans, directory listings, context loading. Anything that doesn't change your understanding or direction.

### ⚡ CHECKPOINT {N} — {title}

**Current State:** [What we're actively working on]
**Context:** [Key conversation points from recent work]
**Files Loaded:** [Files loaded into context, in order]
**Files Modified:** [Recent file changes and purpose]
**Understanding:** [What was learned and why it matters]
**Progress:** [What's been accomplished this session]
**Next Steps:** [Immediate actions needed]

Use for: decisions, direction changes, significant findings, user feedback, context switches.

### 📋 Code Context: [file:line or function]

<!-- OPTIONAL — use when a specific code location is central to a decision or finding -->

```text
[Relevant code snippet with line numbers]
```

**Why Important:** [How this code relates to current work]
**Changes Made:** [If any modifications to this code]

### 📋 User feedback / ADR created

**Why Important:** [How this decision relates to current work]
**Changes Made:** [If any modifications were made]

## Timeline

Brief chronological overview of session progression.

| Time | Checkpoint |
|------|------------|
| T+0 | Session start — context loaded |
| T+1 | Key decision/milestone 1 |
| T+2 | Key decision/milestone 2 |
| T+N | Session end — handoff updated |

Use `T+N` relative offsets (not wall-clock `HH:MM`). Increment on meaningful events, not elapsed time.

## Decisions Log

Use this section for session-local decisions and ADR-grade decisions.

### D{N}: Decision Title

**When:** HH:MM
**Context:** What led to this decision
**Decision:** What was decided
**Rationale:** Why this decision was made
**Impact:** Who/what is affected
**Code Refs:** [file:line references that informed or are affected by this decision]
**Canonical Ref:** [spec/design/doc this decision should land in, if any]

**Alternatives Considered:**
- Option A: Why rejected
- Option B: Why rejected
- Chosen option: Why selected

**Promotion:** stay in handoff | promote to `.lev/pm/decisions`

**Follow-up Required:**
- [ ] Action item 1
- [ ] Action item 2

### Decision Promotion Rule

Decisions stay in the handoff by default.

Promote a decision to `.lev/pm/decisions` only when it is:
- architectural
- reusable across sessions or workstreams
- policy-setting
- likely to be cited outside this handoff

Promoted decisions should:
- link back to this handoff
- preserve the original rationale
- note whether the handoff version is now superseded by the promoted ADR

## Code Context

<!-- OPTIONAL for read-only/research sessions. Required when code was modified. -->

### Files Modified

| File | Change Type | Lines | Status | Notes |
|------|-------------|-------|--------|-------|
| path/to/file1.ts | added | +50 | complete | Purpose |
| path/to/file2.ts | modified | ~30 | complete | What changed |
| path/to/file3.ts | refactored | ~100 | in_progress | What's left |

**Total Changes:**
- Files added: N
- Files modified: N
- Files deleted: N
- Lines changed: +X / -Y

### Files Loaded Into Context

| Order | File | Why Loaded | Key Understanding | Why It Matters |
|------|------|------------|-------------------|----------------|
| 1 | path/to/fileA | reason | insight | impact |
| 2 | path/to/fileB | reason | insight | impact |

### Key Code Locations

```text
path/to/component/
├── main.ts:123            # Entry point - handles X
├── service.ts:45-67       # Core logic - implements Y
├── utils.ts:12            # Helper - calculates Z
└── tests/service.test.ts:89 # Test coverage - validates W
```

**Code Patterns Established:**
- Pattern 1: `path/to/example.ts:line` - Description
- Pattern 2: `path/to/example.ts:line` - Description

## Open Questions

### Immediate (Next Session)

1. Question or unresolved decision
2. Question or unresolved decision

### Short-term (This Week)

1. Question or unresolved decision
2. Question or unresolved decision

### Long-term (This Month)

1. Strategic item with why it matters
2. Strategic item with why it matters

## Entity Matrix

An entity is a **file or directory at a path**. Not a concept. Not a label.

| # | File | Path | State | Impact | Canonical Ref | Decision | Next |
|---|------|------|-------|--------|---------------|----------|------|
| 1 | {filename} | {path/to/file} | loaded | {1-5} | {spec or —} | {D1 or —} | {next action} |

**Impact** = 1 (cosmetic) · 2 (minor) · 3 (moderate) · 4 (significant) · 5 (critical).
**Canonical Ref** = the spec, design, or doc this file is governed by (if any).
**Decision** = which handoff decision(s) touch this entity (D1, D2, etc.).

States: `loaded` (read, not changed) · `captured` (researched, findings recorded) · `modified` (changed this session) · `created` (new file) · `planned` (future work filed) · `completed` (done)

## Meta

### Background Processes

<!-- OPTIONAL — skip if no daemons, builds, or long-running tasks -->

### Active Blockers

<!--
PURPOSE: Blockers kill momentum. Making them visible with ETAs and workarounds lets the next session route around them.
PROCESS: Every blocker MUST have an impact level and a workaround (even if "None"). "Waiting On" should name a person, team, or external dependency.
GOOD: | DeBERTa weights not on this machine | High — can't run intent model tests | Sync from training server | ~1 day | Use regex-only path for V1 flight test |
BAD: | Something is broken | Bad | Someone | Dunno | Maybe |
-->

| Blocker | Impact | Waiting On | ETA | Workaround |
|---------|--------|------------|-----|------------|
| Blocker 1 | High | External API | Unknown | None |
| Blocker 2 | Medium | Review | 1 day | Use mock data |

### Risks

<!-- OPTIONAL for research/audit sessions. Required for execution sessions. -->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | High | High | Strategy |

### Learned Patterns

#### What Worked

<!--
PURPOSE: Institutional memory — patterns that paid off and should be reused.
PROCESS: Be specific enough that someone can replicate the pattern without follow-up questions.
GOOD: 1. **NATSClientStub for daemon isolation** — Context: tests/fixtures/nats_stub.py. Why: Structurally satisfies MessageBrokerProtocol, so isinstance checks pass without monkey-patching. Reuse: Apply same stub pattern elsewhere.
BAD: 1. **Good testing** — Context: Tests. Why: They worked. Reuse: Test more.
-->

1. **Pattern/Approach:**
   - Context: Where used
   - Why it worked: Explanation
   - Reuse: How to apply elsewhere

2. **Pattern/Approach:**
   - Context: Where used
   - Why it worked: Explanation
   - Reuse: How to apply elsewhere

#### What Didn't Work

<!--
PURPOSE: Anti-patterns — prevent the next session from repeating mistakes.
PROCESS: Be honest about what failed and why. "Alternative" must be actionable.
GOOD: 1. **Tried clamping out-of-range params silently** — Context: validation. Why it failed: Users never got feedback. Alternative: HARD REJECT + clarification.
BAD: 1. **Something didn't work** — Context: Code. Why: It was wrong. Alternative: Do it right.
-->

1. **Anti-pattern:**
   - Context: Where attempted
   - Why it failed: Explanation
   - Alternative: What to do instead

2. **Anti-pattern:**
   - Context: Where attempted
   - Why it failed: Explanation
   - Alternative: What to do instead

### Context For Next Session

#### Mental Model

<!--
PURPOSE: The single most important paragraph in the handoff — the "previously on..." that lets the next session skip 30 minutes of context loading.
PROCESS: Write Project State as one sentence, Current Focus as one sentence with WHY, then 3-5 critical insights that would be expensive to re-derive.
GOOD: **Project State:** SDK-first runtime with active PM-first work-skill refactor. **Current Focus:** stabilizing the contract so later deterministic execution can bind cleanly. **Critical Knowledge:** 1. The handoff owns the long-term roadmap, not the tracker.
BAD: **Project State:** Working on stuff. **Current Focus:** Continuing work.
-->

**Project State:** Brief description of overall project state.

**Current Focus:** What we're actively working on and why it matters.

**Critical Knowledge:**
1. Insight 1: Why it matters
2. Insight 2: Why it matters
3. Insight 3: Why it matters

#### Quick Start Commands

<!--
PURPOSE: Let the next session start executing within 30 seconds of reading.
PROCESS: Include cd, git status, and the most relevant run/test commands. Use absolute paths. Only include commands that are actually needed.
GOOD: cd /Users/dev/project && git status && bash ~/.agents/skills/work/scripts/lint-work-contract.sh
BAD: npm start
-->

```bash
cd /path/to/project
git status
<relevant command 1>
<relevant command 2>
```

#### Configuration State

<!--
PURPOSE: Capture environment state that is invisible to git.
PROCESS: List active env vars, feature flags, running services with ports. If nothing special, say so explicitly.
GOOD: **Environment:** LEV_PM_PLANS=.lev/pm/plans, DEMO_MODE=false. **Services:** nats-server on :4222.
BAD: **Environment:** Normal. **Services:** Running.
-->

**Environment:**
- Active feature flags: [tbd]
- Config overrides: [tbd]

**Services:**
- Service A: Status, port, health
- Service B: Status, port, health

### Sharding Signals

Before sharding, prune irrelevant or resolved checkpoints first.

Shard to `session-{N+1}` when one or more conditions hold:
- Soft line cap: around 500 lines and unresolved context is still dense.
- Hard line cap: around 700 lines.
- Checkpoint pressure: another checkpoint would exceed 15.
- Entity pressure: more than 5 actively tracked entities.
- Complexity pressure: more than 3 major lifecycle phases or more than 2 major domain pivots.
- Depth pressure: entity-map or timeline growth makes recovery harder than a successor shard.

### System Prompt for Next Agent (Required)

Provide a system prompt that:
- summarizes the session and immediate next steps
- instructs the agent to load and analyze referenced files
- asks the agent to verify checkpoint-level understanding
- asks the agent to return a context confidence score after priming

### Context Confidence Score (Required)

**Context Confidence:** X% (or 0.0-1.0)

Explain what information is missing or uncertain and what to load first to raise confidence.

## Validation Checklist

### Session Completeness
- [ ] 3-15 chronological checkpoints included
- [ ] Files worked and files loaded are explicitly listed
- [ ] Understanding + importance captured for key files
- [ ] Decisions include rationale
- [ ] Open items are prioritized

### Knowledge Transfer
- [ ] Critical code paths documented
- [ ] Patterns and anti-patterns captured
- [ ] Next-agent system prompt included
- [ ] Context confidence score included
- [ ] Handoff is sufficient for cold-start continuation
