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
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
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

Use exactly one of the three block types below per checkpoint.

### ⚡ CHECKPOINT Progress

**Current State:** [What we're actively working on]  
**Context:** [Key conversation points from recent work]  
**Files Loaded:** [Files loaded into context, in order]  
**Files Modified:** [Recent file changes and purpose]  
**Understanding:** [What was learned and why it matters]  
**Progress:** [What's been accomplished this session]  
**Next Steps:** [Immediate actions needed]  
**Session ID:** [For continuity tracking]

### 📋 Code Context: [file:line or function]

```text
[Relevant code snippet with line numbers]
```

**Why Important:** [How this code relates to current work]  
**Changes Made:** [If any modifications to this code]  
**Context for Next Session:** [How this code fits in timeline]

### 📋 User feedback / ADR created

**Why Important:** [How this decision relates to current work]  
**Changes Made:** [If any modifications were made]  
**Context for Next Session:** [How this fits in timeline]

## Timeline

Brief chronological overview of session progression.

| Time | Checkpoint |
|------|------------|
| HH:MM | Session start - context loaded |
| HH:MM | Key decision/milestone 1 |
| HH:MM | Key decision/milestone 2 |
| HH:MM | Session end - handoff updated |

**Total Duration:** X hours Y minutes  
**Context Switches:** N (list if relevant)

## Decisions Log

Use this section for session-local decisions and ADR-grade decisions.

### D{N}: Decision Title

**When:** HH:MM  
**Context:** What led to this decision  
**Decision:** What was decided  
**Rationale:** Why this decision was made  
**Impact:** Who/what is affected

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

## Entity Matrix

```yaml
session_state: brainstorm | refinement | crystallization | specification | execution
entities_touched:
  - type: task | feature | spec | proposal | design | decision
    id: entity-id
    lifecycle: intake -> execution -> validation
    artifact: path/to/current/artifact.md
    status: active | blocked | ready_to_promote | complete
    next_transition: proposal -> spec
```

**State Transitions:**
1. intake -> crystallization: Task clarified
2. specification -> execution: Spec approved
3. execution -> validation: Code complete, testing in progress

## Meta

### Background Processes

| PID/ID | Type | Name | Status | Notes |
|--------|------|------|--------|-------|
| 12345 | daemon | service-name | running | Health: OK |
| - | exec | build-process | completed | Exit: 0 |

### Blockers & Risks

| Item | Kind | Impact | Waiting On | Workaround |
|------|------|--------|------------|------------|
| Blocker 1 | blocker | High | External API | None |
| Risk 1 | risk | Medium | N/A | Strategy |

### Learned Patterns

#### What Worked
- Pattern, why it worked, and how to reuse it.

#### What Didn't Work
- Anti-pattern, why it failed, and what to do instead.

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
