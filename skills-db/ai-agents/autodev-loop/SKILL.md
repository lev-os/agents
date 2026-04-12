---
name: autodev-loop
description: >
  Autonomous development loop. Prompt generator + cron scheduler that delegates
  execution to /work, flow definitions, and bd. No custom FSM.
version: 4.0.0
extends: []
related_skills:
  - work
  - stack
  - autodev-lev
skill_type: workflow
category: process-lifecycle
primitive_owner: work
triggers:
  - "autodev"
  - "dev loop"
  - "autonomous loop"
  - "plan loop"
tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - CronCreate
  - CronDelete
  - bd CLI (graceful degradation)
storage:
  tick_log: ".lev/pm/handoffs/"
---

# Autodev Loop — Prompt Generator + Cron Scheduler

**Purpose**: Scan the work queue, generate a context-aware prompt, schedule recurring ticks.
Each tick does exactly ONE of four things: sweep, validate, execute, or hygiene.

The loop does NOT contain an FSM. It generates prompts that use /work, flow definitions, and bd.

---

## Tick Architecture

Every tick follows this priority waterfall. First match wins:

```
0. SWEEP     — Pre-check for orphaned validated entities.
   │            Scan for entities with `status: validated` NOT in `_done/`.
   │            If found → move to `_done/`, bd close, log promotion.
   │            This prevents validated entities from getting stuck.
   │
1. VALIDATE  — Did the previous tick produce work?
   │            Run exec-validate flow against it.
   │            Flow: plugins/core-sdlc/flows/exec-validate.flow.yaml
   │            CLI:  lev sdlc exec (alias)
   │            ├─ PASS → promote entity, bd close, checkpoint git
   │            └─ FAIL → append failure feedback to plan body,
   │                      set status: ready, next worker tick retries
   │
2. EXECUTE   — Is there actionable work? (bd ready + lev loop --json)
   │            Pick highest priority, implement it.
   │            Set status: needs_validation when done.
   │
3. HYGIENE   — Nothing to validate or execute. Three sub-modes:
               a) Drift detection (code ↔ specs/designs, bidirectional)
               b) Plan review (promote drafts, correct stale plans/handoffs)
               c) Proposal (deepen vague drafts, create plans from drift findings)
               Flow: plugins/core-sdlc/flows/hygiene.flow.yaml
               CLI:  lev sdlc hygiene (alias)
               EXIT: If HYGIENE produces 0 advancement for K ticks AND only
                     open questions/decisions remain → DELETE THE CRON
```

**Key rule**: The agent that does work NEVER validates its own work.
Validation is always done by the next tick.

---

## Two Modes

**Slice** (`/autodev-loop`): Run one tick. Scan → pick action → execute → checkpoint.

**Time** (`/autodev-loop 6h`): Schedule recurring ticks via CronCreate. Each tick
runs slice mode independently. If no work exists, hygiene creates it.

Time mode is slice mode on a cron. That's it.

---

## Queue Resolution

The tick resolves work in this order:

**Important**: Always re-scan surfaces at tick start. Never trust a static `prompt.md`
snapshot — entities may have been completed by concurrent ticks or previous iterations.
Use live filesystem state + `bd ready --json` as the canonical source.

1. **Check for previous tick's output needing validation**
   - `Glob` for entities with `status: needs_validation`
   - If found → this tick is a VALIDATE tick

2. **Check bd ready** → actionable issues already triaged
   - `Bash`: `bd ready --json`

3. **Check entity surfaces** → plans/specs with `status: ready | active`
   - `Bash`: `npx lev loop --json` (or filesystem scan as fallback)
   - Skip `draft`, `blocked`, `deferred`
   - Sort by priority (P0 > P1 > P2 > P3 > P4)

4. **HYGIENE** → if steps 2-3 return empty
   - Run drift detection, plan review, and proposal sub-modes
   - See HYGIENE Tick Runtime section for full procedure

---

## Flow Definitions (Execution Protocol)

Flow definitions are the structured execution protocol. The loop generates prompts
that reference the right flow for the job. Each flow has exact CLI commands.

### Runbook: Validate Work (exec-validate)

**Flow definition**: `plugins/core-sdlc/flows/exec-validate.flow.yaml`
**Stack ID**: `sdlc-exec-validate`
**Steps**: exec-implement → validate-gates → verdict-routing

```bash
# 1. Init session
npx lev stack init --stack sdlc-exec-validate
# Returns: sessionId (UUID like sdlc-exec-validate-a1b2c3d4-...)

# 2. Step 1 (exec-implement): passthrough — work was done by previous tick
npx lev stack next --session $SESSION_ID
# Record a passthrough report (implementation already happened)
npx lev stack record --session $SESSION_ID --step exec-implement --report ./passthrough.md

# 3. Step 2 (validate-gates): run fitness functions
npx lev stack next --session $SESSION_ID
# Read the step prompt — it tells you to check:
#   - Fitness functions (shell commands in entity frontmatter)
#   - Acceptance criteria against code state
#   - Tests on touched packages
# Write report with per-criterion pass/fail evidence
npx lev stack record --session $SESSION_ID --step validate-gates --report ./report.md

# 4. Step 3 (verdict-routing): route the verdict
npx lev stack next --session $SESSION_ID
# If pass: move entity to _done/, bd close, checkpoint
# If fail + iterations < max: append failure notes to plan body, set status: ready
# If fail + iterations >= max: ESCALATE TO HUMAN (do NOT retry forever)
npx lev stack record --session $SESSION_ID --step verdict-routing --report ./verdict.md
```

### Runbook: Deepen a Plan (deepen-plan)

**Flow definition**: `plugins/core-sdlc/flows/deepen-plan.flow.yaml`
**Stack ID**: `sdlc-deepen-plan`
**Steps**: decompose-topics → parallel-research → synthesize-brief

```bash
# 1. Init session
npx lev stack init --stack sdlc-deepen-plan
# Returns: sessionId

# 2. Step 1: decompose-topics
npx lev stack next --session $SESSION_ID
# Read the plan file. Break into 5-10 research topics.
# Output: JSON array of topic objects {id, title, classification, queries, question}
# Write report with frontmatter + Summary/Evidence/Outcome/Next sections
npx lev stack record --session $SESSION_ID --step decompose-topics --report ./decompose.md

# 3. Step 2: parallel-research
npx lev stack next --session $SESSION_ID
# Launch 1 Opus subagent per topic (max 5 concurrent)
# Each subagent: deep research (codebase + docs + web if needed) → findings
# Collect all results, identify cross-topic themes, write combined report
npx lev stack record --session $SESSION_ID --step parallel-research --report ./research.md

# 4. Step 3: synthesize-brief
npx lev stack next --session $SESSION_ID
# Merge all research into deepened plan brief
# Update the original plan file with research-informed revisions
# Flag open questions that need human resolution
npx lev stack record --session $SESSION_ID --step synthesize-brief --report ./synthesis.md
```

**What to do with results:**
- Plan now promotable (score >= 0.65, no hard gates tripped): set `status: ready`
- Plan has open questions: set `status: blocked`, list questions in plan body
- Plan still vague after deepening: **ESCALATE TO HUMAN**

### Runbook: Hygiene Scan

**Flow definition**: `plugins/core-sdlc/flows/hygiene.flow.yaml`
**Stack ID**: `sdlc-hygiene`
**Steps**: scan-handoffs → check-alignment → propose-updates → emit-report

```bash
# 1. Init session
npx lev stack init --stack sdlc-hygiene
# Returns: sessionId

# 2. Step 1: scan-handoffs
npx lev stack next --session $SESSION_ID
# Scan .lev/pm/handoffs/ for stale/abandoned handoffs
npx lev stack record --session $SESSION_ID --step scan-handoffs --report ./handoffs.md

# 3. Step 2: check-alignment
npx lev stack next --session $SESSION_ID
# Compare plans/specs against ARCHITECTURE.md and north star
npx lev stack record --session $SESSION_ID --step check-alignment --report ./alignment.md

# 4. Step 3: propose-updates
npx lev stack next --session $SESSION_ID
# Generate update proposals for misaligned artifacts
npx lev stack record --session $SESSION_ID --step propose-updates --report ./proposals.md

# 5. Step 4: emit-report
npx lev stack next --session $SESSION_ID
# Final hygiene report with all findings
npx lev stack record --session $SESSION_ID --step emit-report --report ./hygiene-report.md
```

### Flow-Steered Tick Flow

The orchestrator (you) drives the flow lifecycle. Each step gives you
one instruction at a time. You do the work, write the report, record it, advance.

**This is how every tick should work when using flow definitions:**

1. **Init** session for the tick's action:
   ```bash
   npx lev stack init --stack sdlc-exec-validate
   ```
   Returns `sessionId` (full UUID) + callbacks with exact CLI commands for next steps.

2. **Reveal** the active step:
   ```bash
   npx lev stack next --session $SESSION_ID
   ```
   Returns: step prompt (the instruction), report schema, orchestration envelope.
   Future steps are hidden — you only see the current one.

3. **Compose** the entity context with the step prompt:
   - Read the entity (plan/spec/chore) being worked on
   - Read any `code_refs` from the entity's frontmatter
   - The step prompt tells you WHAT to do (implement / validate / route)
   - The entity tells you WHAT to do it ON
   - Together they form the complete instruction

4. **Execute** — do the work (code, test, delegate to subagents, etc.)

5. **Write** a report matching the schema contract:
   ```yaml
   ---
   session_id: $SESSION_ID
   stack_id: sdlc-exec-validate
   step_id: exec-implement
   status: complete
   inputs:
     entity: "plan-fix-poly-build"
     code_refs: [core/poly/tsconfig.json]
   outputs:
     files_changed: [core/poly/tsconfig.json]
     tests_passed: true
   ---
   ## Summary
   What you did and why.
   ## Evidence
   Concrete proof: commands run, test output, file diffs.
   ## Outcome
   Pass/fail and what it means.
   ## Next
   What the next step or agent should do.
   ```

6. **Record** the report:
   ```bash
   npx lev stack record --session $SESSION_ID --step exec-implement --report ./report.md
   ```
   Validates schema, creates receipt with SHA256 digests, advances to next step.

7. **Repeat** from step 2 for remaining steps.

8. **Checkpoint** on completion: git add/commit/push, update handoff.

### Report Contract

Every report MUST have:
- **Frontmatter** (YAML): `session_id`, `stack_id`, `step_id`, `status`, `inputs`, `outputs`
- **Sections** (Markdown H2): `Summary`, `Evidence`, `Outcome`, `Next`

Schema validation happens at `record` time. Bad reports are rejected —
the agent must fix and re-record. The `record` command will tell you
exactly what's missing.

---

## Entity Lifecycle

```
draft → ready → in_progress → needs_validation → validated → done
                     │              │
                     │              └─ (fail) → ready (with feedback appended)
                     └─ (blocked) → blocked
```

| `status` | Tick action |
|----------|-------------|
| `draft` | HYGIENE plan-review — score against promotion rubric |
| `ready` | EXECUTE — pick it up |
| `active` | EXECUTE — continue (alias for ready) |
| `in_progress` | Skip — another agent is working on it |
| `needs_validation` | VALIDATE — run exec-validate flow |
| `validated` | Promote to `_done/` (SWEEP handles this automatically at tick start) |
| `blocked` / `deferred` | Skip |

`lifecycle_state` is accepted as a fallback field for backward compatibility.

---

## HYGIENE: Promotion Algorithm

When HYGIENE runs sub-mode b (plan review), it scores draft plans for promotion.

### Promotion Rubric

Score each `status: draft` plan against these criteria (0-1 each, weighted):

| Criterion | Weight | Check |
|-----------|--------|-------|
| Alignment | 25% | Does it align with `.lev/validation-gates.yaml` and project north star? |
| Blast radius | 20% | How many modules/files does it touch? (lower = safer = higher score) |
| Architecture impact | 20% | Does it change contracts, interfaces, or module boundaries? (no = higher score) |
| Code refs exist | 15% | Do the `code_refs` in frontmatter point to real files? |
| Has acceptance criteria | 10% | Does the plan define measurable done conditions? |
| Has e2e path | 10% | Can the change be validated end-to-end? |

**Promotion threshold**: score >= 0.65 → set `status: ready`

### Hard Gates (Override Score)

These gates force escalation regardless of promotion score:

| Gate | Condition | Action |
|------|-----------|--------|
| Blast radius | Touches >3 modules OR >15 files | **ESCALATE** to human, do not auto-promote |
| Architecture impact | Changes contracts, interfaces, or module boundaries | **ESCALATE** to human |
| Tier depth | L2+ gates in >1 domain per validation-gates.yaml | **ESCALATE** to human |
| MAJOR gate failure | Any MAJOR-severity gate fails | **BLOCK** promotion |
| Uncertainty | Any criterion scored below 0.3 | **ESCALATE** to human |
| Confidence | Overall confidence < 0.70 | **ESCALATE** to human |
| Default | Score >= 0.65 AND no gates tripped | Auto-promote to `status: ready` |

Always err on escalation. If not 100% certain, escalate.

### Deepening Vague Drafts

If a draft scores below 0.4, it MUST be deepened or escalated. Not optional.

Use the deepen-plan flow:
- **Flow**: `plugins/core-sdlc/flows/deepen-plan.flow.yaml`
- **CLI**: `npx lev stack init --stack sdlc-deepen-plan`
- See the "Runbook: Deepen a Plan" section above for exact commands

```
draft (vague, score < 0.4) → deepen via flow → re-score → ready (if passes)
                                                         → ESCALATE (if still vague)
```

---

## HYGIENE: Drift Detection

Drift scanning compares what specs/designs SAY a module should do against what the
code ACTUALLY does. It is NOT file counting. It is NOT export checking. It reads
the contracts and verifies the code respects them.

### Dispatch Model

**1 Opus subagent per module** (batch small modules with <5 files together).
Haiku/Sonnet are insufficient — drift detection requires reading full specs AND
full source files AND reasoning about boundary violations. Only Opus.

### Invariant Extraction Algorithm

For each module, extract testable assertions from its spec using this 4-step procedure:

1. **Parse `## Mandatory Invariants`** — numbered constraints, each independently testable
2. **Parse `## Canonical Ownership and Placement`** — concern→owner→path table, "NOT" markers
3. **Extract forbidden terms** — scan for these 8 boundary markers:
   `"contains zero"`, `"does NOT own"`, `"must NOT"`, `"never"`, `"only"`,
   `"forbidden"`, `"prohibited"`, `"out of scope"`
4. **Parse `## Validation Gates`** — static gates with 0-threshold grep checks

This gives agents a PRECISE extraction algorithm, not "read the spec and figure it out."

### The Three Drift Modes (Priority Order)

#### 1. Boundary Violation Detection (CRITICAL — run first)

Specs and designs define what a module IS and what it is NOT.
Code that violates those boundaries is architectural drift.

**How it works:**

1. For each `docs/specs/spec-{module}.md` + `docs/design/design-{module}.md`:
   - Extract the module's **stated purpose** (executive summary, "Purpose" section)
   - Extract **non-responsibilities** ("Non-responsibilities", "What X is NOT", "Invariants")
   - Extract **ownership boundaries** (ownership tables, "belongs in" statements)
   - Extract **hard-cut invariants** ("zero business logic", "pure binder", "no daemon impl")

2. For the corresponding `core/{module}/` or `plugins/{module}/` directory:
   - Read ACTUAL code — not just file names, ACTUAL IMPORTS AND LOGIC
   - Identify what the code DOES: business logic, routing, orchestration, presentation
   - Compare against the spec's stated purpose and non-responsibilities

3. Flag violations:
   - Code doing X when spec says "zero X" → **CRITICAL severity boundary violation**
   - Code in module A that spec says belongs in module B → **HIGH severity misplacement**
   - Subdirectories that don't exist in spec's ownership table → **MEDIUM severity scope creep**
   - Import chains that cross stated boundaries → **MEDIUM severity coupling violation**

**Example (the one that was missed for months):**
```
spec-poly.md says: "Poly is a pure binder. Zero business logic."
design-poly.md says: "Non-responsibilities: daemon implementation, search orchestration"
core/poly/bridge/orchestrator/ contains: health monitoring, circuit breakers, result fusion
VERDICT: CRITICAL severity boundary violation — business logic in a pure binder
```

**Validation gates check:** Load `.lev/validation-gates.yaml` and check enforced gates against current code state.

#### 2. Contract Compliance (what spec says MUST exist)

After checking boundaries, verify positive assertions:

1. **Ownership table compliance** — spec lists files/dirs → do they exist with correct content?
2. **BDD scenario compliance** — spec describes behavior → does code implement it?
3. **Config declaration compliance** — spec declares poly/SDK sections → are they wired?
4. **Integration claims** — spec says X calls Y → verify the import chain exists
5. **Validation gate compliance** — spec defines gates → do they pass?

#### 3. Parity Detection (code with no spec coverage)

Walk `core/*/` and `plugins/*/` directories:
- For each module: does `docs/specs/spec-{module}.md` exist?
- For each significant subdirectory: is it covered by the spec's ownership table?
- Undocumented code gets a parity report for HUMAN REVIEW — never auto-generate specs

### Reading Specs for Drift (Methodology)

**DO NOT just grep for filenames and counts.** Actually read the spec like a human:

1. **Load the full spec** (`docs/specs/spec-{module}.md`)
2. **Load the design** (`docs/design/design-{module}.md`) if it exists
3. **Load AGENTS.md ownership map** for the module's stated boundaries
4. **Run the 4-step invariant extraction algorithm** (see above)
5. **Then scan code** against ALL extracted assertions — boundaries FIRST, then compliance

### Severity Classification

| Severity | What it means | Example |
|----------|--------------|---------|
| **CRITICAL** | Spec invariant violated | Business logic in a "zero business logic" binder |
| **HIGH** | Code in wrong module per ownership map | Search orchestration in poly instead of core/index |
| **MEDIUM** | Undocumented subdirectory or scope creep | Spike code living permanently in a core package |
| **LOW** | Count mismatch, stale reference, minor doc drift | Spec says 4 adapters, code has 3 |
| **INFO** | Parity gap, no spec exists | New plugin with no spec coverage |

### What Drift Detection is NOT

- NOT file counting
- NOT export listing
- NOT test coverage checking
- NOT "does this file exist"
- NOT mechanical grep assertions

If your drift tick produces a report that says "all clean" without having READ the
spec's purpose statement and compared it to what the code DOES, the tick is INVALID.

### Drift Cache (Dedup)

Drift scanning tracks what it already analyzed to avoid re-scanning unchanged modules.

**State file**: `.lev/sessions/drift-cache.json`

```json
{
  "core/poly": {
    "last_sha": "abc123",
    "last_spec_sha": "def456",
    "last_scan": "2026-03-14",
    "report": "report-drift-poly.md"
  }
}
```

**Before scanning a module:**
1. Read drift-cache.json
2. `git diff --quiet <last_sha> HEAD -- core/<module>/` — code changed?
3. `git diff --quiet <last_spec_sha> HEAD -- docs/specs/spec-<module>.md` — spec changed?
4. If NEITHER changed → skip (already analyzed)
5. If EITHER changed → rescan, update cache entry

**Cache invalidation**: delete `.lev/sessions/drift-cache.json` to force full rescan.

### Canonical Report Naming

Drift and parity reports use canonical names — one per module, overwritten on rescan:

| Report type | Filename | Purpose |
|-------------|----------|---------|
| Spec drift | `report-drift-{module}.md` | Spec claims code doesn't satisfy |
| Code parity | `report-parity-{module}.md` | Code exists with no spec coverage |

Reports live in `.lev/pm/reports/`. Git history IS your scan history.

---

## Circuit Breaker

Exit condition: **K consecutive ticks with zero lifecycle advancement**.

"Advancement" means at least one entity changed lifecycle state (ready → in_progress,
needs_validation → validated, drift → new plan created, etc.).

If the loop produces zero advancement for `circuit_breaker_threshold` consecutive
ticks (default: 3), it exits with reason `stagnation`.

This prevents infinite loops while preserving hygiene scanning freedom. Hygiene
that creates plans IS advancement. Only truly stuck loops get killed.

### Deep-Hygiene Escalation

After 2 consecutive no-advancement ticks (but before circuit breaker trips at K=3):

1. **Lower coverage threshold**: scan specs with lower coverage scores, not just uncached modules
2. **Check bd backlog**: `bd list --status=open --json` — are there old issues that can be promoted to plans?
3. **Widen parity scan**: include `plugins/` and `apps/` directories, not just `core/`
4. **Full hygiene sweep**: run the sdlc-hygiene flow for handoff health check:
   - **Flow**: `plugins/core-sdlc/flows/hygiene.flow.yaml`
   - **CLI**: `npx lev stack init --stack sdlc-hygiene`

This gives the loop one more productive tick before circuit breaker kills it.

### Cron Teardown: Only Decisions Remain

If HYGIENE produces 0 advancement for K ticks AND the remaining work is exclusively
blocked on human decisions, **delete the cron** instead of just exiting with stagnation.

**Detection**: scan all non-done entities for `status: blocked` where `blocked_reason`
matches any of: `decision`, `design`, `human`, `review`, `approval`, `question`.

If ALL remaining entities match → this is a decisions-only state. The loop cannot
make progress without human input. Continuing to tick wastes compute.

```bash
# Teardown sequence:
1. Write final hygiene report documenting decisions-only state
2. List all blocked entities with their blocked_reason
3. CronDelete the active cron
4. Set handoff status to "paused-decisions"
5. Log: "Cron deleted: only human decisions remain. Entities: [list]"
```

The loop auto-resumes when a human resolves decisions and runs `/autodev-loop` again.

---

## Git Protocol

Every tick ends with a checkpoint:

```bash
git stash && git pull --rebase && git stash pop  # handle dirty worktree
git add . && git commit -m "autodev: {action} — {entity}" && git push
```

Checkpoints happen at natural boundaries, not per-file.
Pre-existing dirt in submodules is normal — only investigate unexpected diffs
in files the current tick actually touched.

---

## Multi-Agent Awareness

Multiple autodev loops can run concurrently on different workstreams.

Before dispatching work:

1. `Glob` for `.lev/pm/handoffs/*-session-*.md` with `status: active`
2. Filter to handoffs NOT from your workstream, modified in last 30 minutes
3. Check for file overlap between their work and your dispatch queue
4. If overlap: skip conflicting entity, pick the next one

When touching shared modules, append cross-agent notes to your handoff:

```markdown
### Cross-Agent Notes
- [timestamp] Touching {file} — {what changed}
```

---

## Surface Config

```yaml
# .lev/config.yaml or defaults
autodev:
  tick_interval: 10m
  circuit_breaker_threshold: 3
  surfaces:
    - name: plans
      input: .lev/pm/plans/
      done: .lev/pm/plans/_done/
      patterns: ["plan-*.md"]
    - name: specs
      input: docs/specs/
      done: docs/specs/_done/
      patterns: ["plan-*.md", "chore-*.md"]
```

Config cascade: system → project → CLI flags (later wins).

---

## Invocation

```
/autodev-loop                    # One tick: scan → act → checkpoint
/autodev-loop 10m                # Schedule recurring ticks
/autodev-loop 6h                 # Duration-based (cron that auto-stops)
/autodev-loop --scan             # Read-only scan, show queue
/autodev-loop --execute          # Execute one tick now
/autodev-loop --dry-run          # Show what would happen, don't do it
/autodev-loop --stop             # CronDelete active loop
/autodev-loop --status           # Show queue + active cron + last tick
/autodev-loop --worktree         # Opt-in: worktree isolation for subagents
```

---

## On Load

1. Parse invocation args
2. Check for workstream plan: `Glob` for `.lev/pm/plans/plan-autodev-loop-*.md`
   - If found, load it FIRST — it defines wave structure and scope boundaries
3. Scan surfaces, build priority queue
4. Check for `needs_validation` entities from previous ticks
5. Route to action: validate → execute → hygiene
6. If time mode: `CronCreate` with `Run /autodev-loop --execute`
7. Report: queue size, surfaces scanned, action taken, next recommendation

---

## Claude Code Runtime

### VALIDATE Tick

Uses the **exec-validate** flow (steps 2-3 only):
- **Flow**: `plugins/core-sdlc/flows/exec-validate.flow.yaml`
- **CLI**: `npx lev stack init --stack sdlc-exec-validate`

1. `Glob` for entities with `status: needs_validation`
2. `Read` the entity + files it touched
3. Init flow session:
   ```bash
   npx lev stack init --stack sdlc-exec-validate
   ```
4. Step 1 (exec-implement): record a passthrough report — implementation
   was done by the previous tick, this tick is validation only
   ```bash
   npx lev stack next --session $SESSION_ID
   npx lev stack record --session $SESSION_ID --step exec-implement --report ./passthrough.md
   ```
5. Step 2 (validate-gates):
   ```bash
   npx lev stack next --session $SESSION_ID
   ```
   - Read the step prompt — it tells you to run fitness functions
   - Check fitness functions (shell commands in entity frontmatter)
   - Check acceptance criteria against code state
   - Run tests on touched packages
   - Write report with per-criterion pass/fail evidence
   ```bash
   npx lev stack record --session $SESSION_ID --step validate-gates --report ./report.md
   ```
6. Step 3 (verdict-routing):
   ```bash
   npx lev stack next --session $SESSION_ID
   ```
   - Read the step prompt — it tells you to route the verdict
   - If `pass`: promote entity to `_done/`, `bd close`, checkpoint
   - If `fail` + iterations < max: append failure notes, set `status: ready`
   - If `fail` + iterations >= max: **ESCALATE TO HUMAN**
   ```bash
   npx lev stack record --session $SESSION_ID --step verdict-routing --report ./verdict.md
   ```

### EXECUTE Tick

1. Pick highest-priority ready entity from queue
2. `Read` full plan + all `code_refs`
3. If `bd_id` → `bd update $BD_ID --status=in_progress`
4. Dispatch based on complexity:
   - **Simple** (1-2 code_refs): inline Read/Edit/Write/Bash
   - **Medium** (3-5 code_refs): Agent tool, single subagent
   - **Complex** (6+ code_refs): Agent tool, 2-4 parallel subagents
     (sequential for overlapping files, parallel for non-overlapping)
5. After execution:
   - Set entity `status: needs_validation`
   - Checkpoint git (do NOT validate your own work)
6. **Record learning**: capture what changed and why for procedural memory:
   ```bash
   cm add "{entity}: {what changed and why}" --category {execution|refactor|bugfix} --json
   ```
   This prevents institutional memory loss across long autonomous runs.

### HYGIENE Tick

Runs when no entities need validation and no ready work exists. Three sub-modes
execute in sequence:

#### Sub-mode A: Drift Detection

1. Load `.lev/sessions/drift-cache.json` (create empty `{}` if missing)
2. **Dispatch 1 Opus subagent per module** (batch modules with <5 files):
   - Each subagent runs the full drift methodology:
     a. Check cache — skip if neither code nor spec SHA changed
     b. Run 4-step invariant extraction algorithm on spec
     c. Read actual source code in the module
     d. Check boundary violations FIRST (CRITICAL/HIGH)
     e. Check contract compliance (HIGH/MEDIUM)
     f. Check parity (MEDIUM/LOW/INFO)
     g. Write `report-drift-{module}.md` to `.lev/pm/reports/`
     h. Update cache entry with current SHAs
   - A report that says "clean" without citing specific invariants checked is **INVALID**
3. Collect all subagent reports, rank by severity
4. For CRITICAL/HIGH drift: create plans immediately
   - Use deepen-plan flow for complex findings:
     **Flow**: `plugins/core-sdlc/flows/deepen-plan.flow.yaml`
     **CLI**: `npx lev stack init --stack sdlc-deepen-plan`
5. For MEDIUM/LOW drift: append to existing plans or create new ones
6. For parity findings: save reports only (human-gated)

#### Sub-mode B: Plan Review (Promotion)

1. `Glob` for `.lev/pm/plans/plan-*.md` with `status: draft`
2. For each draft plan:
   - Read plan, extract frontmatter (code_refs, priority, acceptance criteria)
   - Score against promotion rubric (see HYGIENE: Promotion Algorithm)
   - Check hard gates (blast radius, architecture impact, tier depth, confidence)
   - If score >= 0.65 AND no gates tripped: update `status: ready`, append evidence
   - If score < 0.65 OR gate tripped: see gate action table
   - If score < 0.4: MUST deepen via flow or escalate (not optional)
3. Scan `.lev/pm/handoffs/` for stale handoffs (>48h with status: active)
4. Promoting a draft IS lifecycle advancement (resets circuit breaker)

#### Sub-mode C: Proposal

1. Review drift findings that don't have plans yet
2. For CRITICAL/HIGH findings without plans: create plan entities
3. For vague findings: deepen using deepen-plan flow before creating plans
   - **Flow**: `plugins/core-sdlc/flows/deepen-plan.flow.yaml`
   - **CLI**: `npx lev stack init --stack sdlc-deepen-plan`
4. Creating a plan IS lifecycle advancement (resets circuit breaker)

**Checkpoint git after all three sub-modes complete.**

### Error Handling

| Situation | Action |
|-----------|--------|
| `bd` unavailable | Skip bd calls, filesystem state only |
| Fitness function errors | Mark entity ERROR, skip, report |
| Agent failure | Report, leave entity as `ready` |
| No entities found | HYGIENE tick |
| All blocked/deferred | Report blocked queue, count toward circuit breaker |

---

## Anti-Patterns

- **Self-validation** — worker NEVER validates its own output
- **Custom FSM** — no SCANNING/DOING/VALIDATING modes. Use the tick waterfall
- **Unbounded ticks** — one entity per tick maximum
- **Skipping flows** — validation and drift use flow definitions, not ad-hoc prompts
- **No handoff** — every loop session maintains a handoff in `.lev/pm/handoffs/`
- **Static prompts** — prompt is generated from current queue state
- **Ignoring circuit breaker** — stagnation means something structural is wrong
- **File-counting drift** — drift detection reads specs and compares to code, not counts
- **Vague stack references** — every flow reference includes file path + exact CLI commands
