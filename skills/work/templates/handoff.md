---
type: handoff
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
session_id: session-uuid
from_agent: agent-name
to_agent: next-agent | human | team
status: active | archived
stage: manifesting
context_confidence: 0.0-1.0
topic: topic-slug
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
---

# Session Handoff: Topic

**Created:** YYYY-MM-DD HH:MM:SS TZ
**Topic:** Brief description of session focus
**Context Confidence:** 0.0-1.0 (percentage or decimal)
**Session ID:** session-uuid

---

## Handoff Objective

Analyze the current conversation context and manage session state based on mode and arguments.

For continuity, provide in chronological order:
- files worked on
- files loaded into context
- what was understood after loading them
- why each understanding is important

Goal: produce a deterministic trail guide through code, context, decisions, and user feedback so the next session can recover state quickly.

---

## Checkpoints (Required: 3-15, chronological)

Use exactly one of the three templates below per checkpoint.

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

---

## Timeline Summary

Brief chronological overview of session progression.

| Time | Checkpoint |
|------|------------|
| HH:MM | Session start - context loaded |
| HH:MM | Key decision/milestone 1 |
| HH:MM | Key decision/milestone 2 |
| HH:MM | Session end - handoff created |

**Total Duration:** X hours Y minutes
**Context Switches:** N (list if relevant)

---

## Key Decisions

### 1. Decision Title

**When:** HH:MM
**Context:** What led to this decision
**Decision:** What was decided
**Rationale:** Why this decision was made
**Impact:** Who/what is affected

**Alternatives Considered:**
- Option A: Why rejected
- Option B: Why rejected
- Chosen option: Why selected

**Follow-up Required:**
- [ ] Action item 1
- [ ] Action item 2

---

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

---

### Key Code Locations

**Critical paths for next session:**

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

---

## State Machine

### Current State

```yaml
session_state: brainstorm | refinement | crystallization | specification | execution
entities_touched:
  - type: task
    id: task-123
    lifecycle: intake -> execution -> validation
  - type: feature
    id: feature-x
    lifecycle: specification -> execution
```

**State Transitions:**
1. intake -> crystallization: Task clarified
2. specification -> execution: Spec approved
3. execution -> validation: Code complete, testing in progress

---

### Background Processes

| PID/ID | Type | Name | Status | Notes |
|--------|------|------|--------|-------|
| 12345 | daemon | service-name | running | Health: OK |
| - | exec | build-process | completed | Exit: 0 |
| - | watch | file-watcher | stopped | Manually stopped |

---

## Open Items

### Immediate (Next Session)

1. **Task Title**
   - **Context:** Why this is needed
   - **Status:** not_started | blocked | in_progress
   - **Blocker:** What's preventing progress (if blocked)
   - **Next Steps:** Specific actions to take
   - **Files:** Relevant file paths
   - **Estimate:** Quick | Medium | Deep work

2. **Task Title**
   - **Context:** Why this is needed
   - **Status:** not_started | blocked | in_progress
   - **Dependencies:** What must complete first
   - **Next Steps:** Specific actions to take

### Short-term (This Week)

1. Task with brief context and next steps
2. Task with brief context and next steps
3. Task with brief context and next steps

### Long-term (This Month)

1. Task with strategic importance
2. Task with strategic importance

---

## Blockers & Risks

### Active Blockers

| Blocker | Impact | Waiting On | ETA | Workaround |
|---------|--------|------------|-----|------------|
| Blocker 1 | High | External API | Unknown | None |
| Blocker 2 | Medium | Review | 1 day | Use mock data |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | High | High | Strategy |
| Risk 2 | Medium | Low | Strategy |

---

## Learned Patterns

### What Worked

1. **Pattern/Approach:**
   - Context: Where used
   - Why it worked: Explanation
   - Reuse: How to apply elsewhere

2. **Pattern/Approach:**
   - Context: Where used
   - Why it worked: Explanation
   - Reuse: How to apply elsewhere

### What Didn't Work

1. **Anti-pattern:**
   - Context: Where attempted
   - Why it failed: Explanation
   - Alternative: What to do instead

2. **Anti-pattern:**
   - Context: Where attempted
   - Why it failed: Explanation
   - Alternative: What to do instead

---

## Context for Next Session

### Mental Model

**Project State:** Brief description of overall project state.

**Current Focus:** What we're actively working on and why it matters.

**Critical Knowledge:**
1. Insight 1: Why it matters
2. Insight 2: Why it matters
3. Insight 3: Why it matters

### Quick Start Commands

```bash
cd /path/to/project
git status
pnpm test
pnpm dev
```

### Configuration State

**Environment:**
- NODE_ENV: development | production
- Active feature flags: flag1, flag2
- Config overrides: path/to/config

**Services:**
- Service A: Status, port, health
- Service B: Status, port, health

---

## System Prompt for Next Agent (Required)

Provide a system prompt that:
- summarizes the entire session and immediate next steps
- instructs the agent to load and analyze referenced files
- asks the agent to verify checkpoint-level understanding
- asks the agent to return a context confidence score after priming

---

## Context Confidence Score (Required)

**Context Confidence:** X% (or 0.0-1.0)

Explain what information is missing or uncertain and what to load first to raise confidence.

---

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
