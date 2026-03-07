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

<!--
PURPOSE: Header block that orients the next agent/human in under 10 seconds
PROCESS: Fill in all fields before writing any checkpoints. Session ID comes from the conversation metadata or generate a UUID.
GOOD: **Created:** 2026-03-06 14:32:00 PST | **Topic:** Hex adapter wiring for daemon unit testing | **Context Confidence:** 0.85
BAD: **Created:** today | **Topic:** Worked on stuff | **Context Confidence:** high
-->

**Created:** YYYY-MM-DD HH:MM:SS TZ
**Topic:** Brief description of session focus
**Context Confidence:** 0.0-1.0 (percentage or decimal)
**Session ID:** session-uuid

---

## Handoff Objective

<!--
PURPOSE: Explain WHY this handoff exists and what the next session needs to recover
PROCESS: (1) List files touched in chronological order (2) List files loaded for context (3) State what was understood (4) State why each understanding matters for continuity
GOOD: "Wired NATSClient injection into ASR daemon, validated with NATSClientStub. Next session must finish Intent and Response daemons using the same pattern established in modules/daemon/asr.py:45-80."
BAD: "Did some refactoring on the daemon code. Should keep going next time."
-->

Analyze the current conversation context and manage session state based on mode and arguments.

For continuity, provide in chronological order:
- files worked on
- files loaded into context
- what was understood after loading them
- why each understanding is important

Goal: produce a deterministic trail guide through code, context, decisions, and user feedback so the next session can recover state quickly.

---

## Checkpoints (Required: 3-15, chronological)

<!--
PURPOSE: Ordered breadcrumbs that let the next session replay your reasoning without re-reading everything
PROCESS: Create checkpoints as you go (not retroactively). Each must use exactly one of the three templates below. Aim for one checkpoint per major context shift or decision point.
GOOD: 5 checkpoints covering: initial context load, first code change, user feedback pivot, second code change, final state
BAD: 1 giant checkpoint that dumps everything, or 15 trivial checkpoints like "read file X" with no insight
-->

Use exactly one of the three templates below per checkpoint.

### ⚡ CHECKPOINT Progress

<!--
PURPOSE: Capture a snapshot of active work state at a moment in time
PROCESS: Fill every field. "Files Loaded" and "Files Modified" must use absolute paths. "Understanding" is the insight, not a file summary.
GOOD: **Understanding:** ASR daemon creates its own NATSClient in __init__ — constructor injection requires adding a broker param with a default, not a protocol change. **Why It Matters:** This means we can wire adapters incrementally without breaking existing daemon startup.
BAD: **Understanding:** Read the ASR daemon file. **Why It Matters:** It's important.
-->

**Current State:** [What we're actively working on]
**Context:** [Key conversation points from recent work]
**Files Loaded:** [Files loaded into context, in order]
**Files Modified:** [Recent file changes and purpose]
**Understanding:** [What was learned and why it matters]
**Progress:** [What's been accomplished this session]
**Next Steps:** [Immediate actions needed]
**Session ID:** [For continuity tracking]

### 📋 Code Context: [file:line or function]

<!--
PURPOSE: Pin a specific code location that the next session MUST understand to continue
PROCESS: (1) Include the minimal code snippet with line numbers (2) Explain its role in the current work (3) Note any changes made or planned
GOOD: **Why Important:** This is the exact injection point — `asr_daemon.py:52` where `self.broker = NATSClient()` must become `self.broker = broker or NATSClient()` to enable stub injection in tests.
BAD: **Why Important:** This file has some code in it that we looked at.
-->

```text
[Relevant code snippet with line numbers]
```

**Why Important:** [How this code relates to current work]
**Changes Made:** [If any modifications to this code]
**Context for Next Session:** [How this code fits in timeline]

### 📋 User feedback / ADR created

<!--
PURPOSE: Record a user decision or architectural decision that constrains future work
PROCESS: Capture the decision verbatim if possible. Note what it overrides or locks in. Link to ADR file if one was created.
GOOD: **Why Important:** User locked in "NATS stays for external, direct bus for internal" — this means the bus abstraction flag (internal_bus: nats|direct) is required before any daemon can drop NATS internally.
BAD: **Why Important:** User said something about NATS.
-->

**Why Important:** [How this decision relates to current work]
**Changes Made:** [If any modifications were made]
**Context for Next Session:** [How this fits in timeline]

---

## Timeline Summary

<!--
PURPOSE: Give a scannable chronological view of the session — what happened and when
PROCESS: Fill the table with real timestamps (or relative offsets). Include context switches explicitly — they're the #1 cause of lost state.
GOOD: | 14:32 | Loaded ASR daemon + NATSClient, discovered structural Protocol conformance | | 14:50 | User pivoted to Intent daemon — context switch #1 |
BAD: | start | Did things | | end | Finished |
-->

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

<!--
PURPOSE: Decisions are the highest-value content in a handoff — they prevent the next session from re-litigating settled questions
PROCESS: (1) State what was decided (2) State WHY with enough context that someone who disagrees can understand the reasoning (3) List rejected alternatives — these prevent re-exploration
GOOD: **Decision:** Use strategy pattern for hallucination filters, not a monolithic validator. **Rationale:** poc/cleanup already has 7 independent strategies with 33+ tests — promoting as-is preserves test coverage and allows per-strategy toggling.
BAD: **Decision:** We went with strategy pattern. **Rationale:** It seemed better.
-->

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

<!--
PURPOSE: Manifest of every file touched — the next session's first grep target
PROCESS: List ALL files, even partially modified ones. "Status: in_progress" is critical — it tells the next session where to resume. Use absolute paths.
GOOD: | modules/daemon/asr.py | modified | ~15 | in_progress | Added broker param to __init__, wiring incomplete — needs default fallback |
BAD: | some file | changed | ? | done | updated it |
-->

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

<!--
PURPOSE: Distinguish files READ (for understanding) from files MODIFIED — the next session needs both lists but for different reasons
PROCESS: Order matters. List in the order they were loaded. "Key Understanding" must be an insight, not a description. "Why It Matters" connects the insight to the active work.
GOOD: | 3 | modules/transcription/config.py | Checking if ValidationConfig is wired | Defined at L92-99 but never imported by any daemon | Confirms hex adapter gap — config exists but injection path is missing |
BAD: | 1 | some_file.py | wanted to read it | it has code | it's relevant |
-->

| Order | File | Why Loaded | Key Understanding | Why It Matters |
|------|------|------------|-------------------|----------------|
| 1 | path/to/fileA | reason | insight | impact |
| 2 | path/to/fileB | reason | insight | impact |

---

### Key Code Locations

<!--
PURPOSE: A spatial map of the codebase areas the next session will need — faster than grepping from scratch
PROCESS: Use tree format with file:line references. Only include locations actively relevant to the current work stream. Add one-line annotations.
GOOD: path/to/daemon/ with entries like "asr.py:52 # Injection point — broker param added here" and "tests/test_asr.py:0 # DOES NOT EXIST — must create"
BAD: A flat list of every file in the project with no line numbers or annotations
-->

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

<!--
PURPOSE: Track entity lifecycle states so the next session knows what phase each workstream is in
PROCESS: Use the YAML block for machine-readable state. List transitions that happened THIS session only. This section is essential for multi-session epics.
GOOD: session_state: execution, with entity "uav-jo0u hex adapters" at lifecycle "specification -> execution" and transition note "Spec approved after interview Q1 lock"
BAD: session_state: working, with no entities listed
-->

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

<!--
PURPOSE: Capture any running processes, watchers, or daemons that the next session needs to be aware of (or restart)
PROCESS: Include PIDs for running processes. Mark stopped processes with reason. If nothing was running, write "None" — don't omit the section.
GOOD: | 48201 | daemon | nats-server | running | Started for integration tests, port 4222, must kill before next test run |
BAD: | - | - | something | - | - |
-->

| PID/ID | Type | Name | Status | Notes |
|--------|------|------|--------|-------|
| 12345 | daemon | service-name | running | Health: OK |
| - | exec | build-process | completed | Exit: 0 |
| - | watch | file-watcher | stopped | Manually stopped |

---

## Open Items

### Immediate (Next Session)

<!--
PURPOSE: The next session's TODO list, ordered by priority. This is the #1 section that gets read on cold start.
PROCESS: (1) Each item must have enough context to start without re-reading the full handoff (2) Include file paths (3) Mark blockers explicitly (4) Estimate effort: Quick (<30min), Medium (30min-2hr), Deep (2hr+)
GOOD: 1. **Wire broker param into Intent daemon** — Context: ASR daemon pattern established at asr.py:52, replicate for intent.py:38. Status: not_started. Files: modules/daemon/intent.py, tests/fixtures/nats_stub.py. Estimate: Quick.
BAD: 1. **Keep working on daemons** — Context: Need to do more. Status: not done.
-->

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

<!--
PURPOSE: Work that's important but not the immediate next action — prevents tunnel vision
PROCESS: One line per item with enough context to promote to "Immediate" without research. Link to bd issue IDs if they exist.
GOOD: 1. Promote poc/cleanup hallucination filter to modules/ (uav-nuxg) — 7 strategies, 33 tests, needs config flag wiring
BAD: 1. Do more testing
-->

1. Task with brief context and next steps
2. Task with brief context and next steps
3. Task with brief context and next steps

### Long-term (This Month)

<!--
PURPOSE: Strategic items that inform prioritization but aren't actionable this week
PROCESS: Focus on WHY these matter, not HOW to do them. Link to epics or design docs if available.
GOOD: 1. Dual-lane ATC conversation management — deferred per Q3 decision, but session FSM is already wired for multi-turn. Revisit after single-lane MVP ships.
BAD: 1. Make things better eventually
-->

1. Task with strategic importance
2. Task with strategic importance

---

## Blockers & Risks

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

<!--
PURPOSE: Risks are blockers that haven't happened yet. Capturing them prevents surprise.
PROCESS: Be specific about mitigation — "be careful" is not a strategy. Likelihood/Impact should be High/Medium/Low.
GOOD: | NATS connection timeout under load | Medium | High — drops transcriptions silently | Add circuit breaker (uav-kvq9) before load testing |
BAD: | Things might break | Maybe | Bad | Be careful |
-->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | High | High | Strategy |
| Risk 2 | Medium | Low | Strategy |

---

## Learned Patterns

### What Worked

<!--
PURPOSE: Institutional memory — patterns that paid off and should be reused
PROCESS: Be specific enough that someone can replicate the pattern without asking follow-up questions. Include the file/location where the pattern was applied.
GOOD: 1. **NATSClientStub for daemon isolation** — Context: tests/fixtures/nats_stub.py. Why: Structurally satisfies MessageBrokerProtocol, so isinstance checks pass without monkey-patching. Reuse: Apply same stub pattern to any daemon needing broker isolation.
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

### What Didn't Work

<!--
PURPOSE: Anti-patterns — prevent the next session from repeating mistakes
PROCESS: Be honest about what failed and why. "Alternative" must be actionable.
GOOD: 1. **Tried clamping out-of-range params silently** — Context: Heading/altitude validation. Why it failed: Pilots never got feedback, kept issuing bad commands. Alternative: HARD REJECT + log + clarification through session FSM (Q7 decision).
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

---

## Context for Next Session

### Mental Model

<!--
PURPOSE: The single most important paragraph in the handoff — it's the "previously on..." that lets the next session skip 30 minutes of context loading
PROCESS: (1) Write Project State as one sentence (2) Write Current Focus as one sentence with WHY (3) List 3-5 critical insights that would be expensive to re-derive
GOOD: **Project State:** Pipes-and-filters ATC drone system with 3 daemons, hex protocols defined but not injected. **Current Focus:** Wiring adapter injection into daemons — this unblocks all unit testing. **Critical Knowledge:** 1. NATSClient structurally satisfies MessageBrokerProtocol (isinstance=True) — gap is injection, not interface.
BAD: **Project State:** Working on the project. **Current Focus:** Continuing work. **Critical Knowledge:** 1. Read some files.
-->

**Project State:** Brief description of overall project state.

**Current Focus:** What we're actively working on and why it matters.

**Critical Knowledge:**
1. Insight 1: Why it matters
2. Insight 2: Why it matters
3. Insight 3: Why it matters

### Quick Start Commands

<!--
PURPOSE: Let the next session start executing within 30 seconds of reading
PROCESS: Include cd, git status, and the most relevant run/test commands. Use absolute paths. Only include commands that are actually needed.
GOOD: cd /Users/dev/drone && git status && uv run pytest modules/daemon/ -x -v && bd ready --json
BAD: npm start
-->

```bash
cd /path/to/project
git status
pnpm test
pnpm dev
```

### Configuration State

<!--
PURPOSE: Capture environment state that's invisible to git — the next session can't derive this from code alone
PROCESS: List active env vars, feature flags, running services with ports. If nothing special, write "Default development environment — no overrides."
GOOD: **Environment:** NATS_URL=nats://localhost:4222, VAD_STRATEGY=silero, DEMO_MODE=false (must stay false per Q12). **Services:** nats-server on :4222 (started manually, not systemd).
BAD: **Environment:** Normal. **Services:** Running.
-->

**Environment:**
- NODE_ENV: development | production
- Active feature flags: flag1, flag2
- Config overrides: path/to/config

**Services:**
- Service A: Status, port, health
- Service B: Status, port, health

---

## System Prompt for Next Agent (Required)

<!--
PURPOSE: A self-contained prompt that primes the next agent to full context in one shot — this IS the handoff mechanism for agent-to-agent continuity
PROCESS: (1) Summarize the session in 2-3 sentences (2) List the 3-5 files to load first (3) State the immediate next action (4) Ask the agent to verify understanding and return a confidence score
GOOD: "You are continuing hex adapter wiring for the drone ATC system. Last session wired ASR daemon (modules/daemon/asr.py:52). Load these files first: [asr.py, intent.py, nats_stub.py]. Your immediate task: replicate the broker injection pattern from ASR into Intent daemon. After loading context, state your understanding and return a confidence score 0-1."
BAD: "Keep working on what we were doing. Check the code."
-->

Provide a system prompt that:
- summarizes the entire session and immediate next steps
- instructs the agent to load and analyze referenced files
- asks the agent to verify checkpoint-level understanding
- asks the agent to return a context confidence score after priming

---

## Context Confidence Score (Required)

<!--
PURPOSE: A calibrated self-assessment of how much context was successfully captured — low scores tell the next session to verify before acting
PROCESS: Score honestly. 0.9+ means the next session can act immediately. 0.7-0.9 means load files to verify. Below 0.7 means significant context was lost. Explain what's missing.
GOOD: **Context Confidence:** 0.82 — All decisions captured, code locations verified. Missing: exact line numbers for Intent daemon injection point (file was read but not annotated). Load modules/daemon/intent.py first to fill gap.
BAD: **Context Confidence:** 1.0 — Everything is fine.
-->

**Context Confidence:** X% (or 0.0-1.0)

Explain what information is missing or uncertain and what to load first to raise confidence.

---

## Validation Checklist

<!--
PURPOSE: A gate that prevents shipping incomplete handoffs — run through this before marking the handoff done
PROCESS: Check each box honestly. If any box is unchecked, go back and fix it. An incomplete handoff is worse than no handoff — it creates false confidence.
GOOD: All boxes checked, or unchecked boxes with explicit notes like "[ ] Patterns captured — N/A, no new patterns this session"
BAD: All boxes checked without actually verifying each one
-->

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
