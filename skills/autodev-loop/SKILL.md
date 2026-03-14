---
name: autodev-loop
description: >
  Autonomous development loop. Prompt generator + cron scheduler that delegates
  execution to /work, prompt stacks, and bd. No custom FSM.
version: 3.0.0
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
Each tick does exactly ONE of three things: validate, execute, or drift scan.

The loop does NOT contain an FSM. It generates prompts that use /work, prompt stacks, and bd.

---

## Tick Architecture

Every tick follows this priority waterfall. First match wins:

```
1. VALIDATE  — Did the previous tick produce work?
   │            Run sdlc-exec-validate prompt stack against it.
   │            ├─ PASS → promote entity, bd close, checkpoint git
   │            └─ FAIL → append failure feedback to plan body,
   │                      set status: ready, next worker tick retries
   │
2. EXECUTE   — Is there actionable work? (bd ready + lev loop --json)
   │            Pick highest priority, implement it.
   │            Set status: needs_validation when done.
   │
3. DRIFT     — No actionable work?
               Scan core/ vs docs/specs/ for drift.
               Create/update plans via sdlc-deepen-plan prompt stack.
               Plans land as status: ready (available next tick).
```

**Key rule**: The agent that does work NEVER validates its own work.
Validation is always done by the next tick.

---

## Two Modes

**Slice** (`/autodev-loop`): Run one tick. Scan → pick action → execute → checkpoint.

**Time** (`/autodev-loop 6h`): Schedule recurring ticks via CronCreate. Each tick
runs slice mode independently. If no work exists, drift scan creates it.

Time mode is slice mode on a cron. That's it.

---

## Queue Resolution

The tick resolves work in this order:

1. **Check for previous tick's output needing validation**
   - `Glob` for entities with `status: needs_validation`
   - If found → this tick is a VALIDATE tick

2. **Check bd ready** → actionable issues already triaged
   - `Bash`: `bd ready --json`

3. **Check entity surfaces** → plans/specs with `status: ready | active`
   - `Bash`: `npx lev loop --json` (or filesystem scan as fallback)
   - Skip `draft`, `blocked`, `deferred`
   - Sort by priority (P0 > P1 > P2 > P3 > P4)

4. **Drift scan** → if steps 2-3 return empty
   - Compare `core/` code against `docs/specs/spec-*.md`
   - Check `code_refs` paths, `validation_gates`, documented invariants
   - Create plans for real drift found (as `status: ready`)

---

## Prompt Stacks as Composition Layer

Prompt stacks are the structured execution protocol. The loop generates prompts
that reference the right stack for the job.

### For Validation Ticks

Stack: **sdlc-exec-validate** (3 steps: exec-implement → validate-gates → verdict-routing)

The validate tick runs only steps 2-3 (validate-gates + verdict-routing) against
the previous tick's output. It does NOT re-execute.

```
Invoke: bun plugins/prompt-stack/src/cli.ts init sdlc-exec-validate
        bun plugins/prompt-stack/src/cli.ts next <session-id>
```

Verdict routing:
- `pass` → promote entity to `_done/`, `bd close`
- `fail` → append failure notes to plan body, set `status: ready`

The plan becomes the feedback channel. Next worker tick sees WHY it failed.

### For Drift Scan Ticks

Stack: **sdlc-deepen-plan** (3 steps: decompose-topics → parallel-research → synthesize-brief)

When drift is detected, the deepen stack decomposes findings into structured plans:
1. Break drift findings into research topics
2. Research each topic against codebase + prior art
3. Synthesize into actionable plan entities with proper frontmatter

### For Hygiene (Periodic)

Stack: **sdlc-hygiene** (4 steps: scan-handoffs → check-alignment → propose-updates → emit-report)

Run every N ticks (configurable) or when explicitly requested.
Checks handoff health, spec alignment, and proposes updates.

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
| `draft` | Skip — not ready for autonomous work |
| `ready` | EXECUTE — pick it up |
| `active` | EXECUTE — continue (alias for ready) |
| `in_progress` | Skip — another agent is working on it |
| `needs_validation` | VALIDATE — run prompt stack |
| `validated` | Promote to `_done/` |
| `blocked` / `deferred` | Skip |

`lifecycle_state` is accepted as a fallback field for backward compatibility.

---

## Drift Scanning

Drift scanning is valuable work. It discovers real gaps between code and documentation.

When the queue is empty, the tick scans `docs/specs/spec-*.md` against `core/`:

1. Compare `code_refs` paths against actual file exports
2. Check `validation_gates` thresholds against test reality
3. Look for invariants violated in code
4. Check ownership tables against directory listings
5. Compare BDD scenarios against real code paths

Findings become plans via the **sdlc-deepen-plan** prompt stack, landing
with `status: ready` so the next tick can execute them.

### Internal Consistency Checks

When auditing specs, check for self-contradiction patterns:

- Executive summary vs invariants disagreement
- Ownership table vs actual directory listing
- BDD scenarios referencing phantom functions/files
- Validation gate thresholds vs test coverage reality
- Config defaults vs spec recommendations

---

## Circuit Breaker

Exit condition: **K consecutive ticks with zero lifecycle advancement**.

"Advancement" means at least one entity changed lifecycle state (ready → in_progress,
needs_validation → validated, drift → new plan created, etc.).

If the loop produces zero advancement for `circuit_breaker_threshold` consecutive
ticks (default: 3), it exits with reason `stagnation`.

This prevents infinite loops while preserving drift scanning freedom. Drift scanning
that creates plans IS advancement. Only truly stuck loops get killed.

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
5. Route to action: validate → execute → drift
6. If time mode: `CronCreate` with `Run /autodev-loop --execute`
7. Report: queue size, surfaces scanned, action taken, next recommendation

---

## Claude Code Runtime

### VALIDATE Tick

1. `Glob` for entities with `status: needs_validation`
2. `Read` the entity + files it touched (from last commit or entity body)
3. Run validation via prompt stack or inline:
   - Check fitness functions (shell commands in frontmatter)
   - Check acceptance criteria against code state
   - Run tests on touched packages
4. If ALL pass:
   - Update entity `status: validated`
   - `Bash`: `mkdir -p "$(dirname "$FILE")/_done" && mv "$FILE" "$(dirname "$FILE")/_done/"`
   - If `bd_id` → `bd close $BD_ID`
5. If ANY fail:
   - Append failure notes to entity body under `## Validation Feedback`
   - Set `status: ready`
   - Next worker tick picks it up with feedback context

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

### DRIFT Tick

1. Scan `docs/specs/spec-*.md` against `core/` for drift
2. For each drift found:
   - Use sdlc-deepen-plan stack to structure findings into plans
   - Write `plan-*.md` with `status: ready` and proper frontmatter
3. If no drift found: report "Queue empty. Codebase clean."
4. Checkpoint git

### Error Handling

| Situation | Action |
|-----------|--------|
| `bd` unavailable | Skip bd calls, filesystem state only |
| Fitness function errors | Mark entity ERROR, skip, report |
| Agent failure | Report, leave entity as `ready` |
| No entities found | Drift scan |
| All blocked/deferred | Report blocked queue, count toward circuit breaker |

---

## Anti-Patterns

- **Self-validation** — worker NEVER validates its own output
- **Custom FSM** — no SCANNING/DOING/VALIDATING modes. Use the tick waterfall
- **Unbounded ticks** — one entity per tick maximum
- **Skipping prompt stacks** — validation and drift use stacks, not ad-hoc prompts
- **No handoff** — every loop session maintains a handoff in `.lev/pm/handoffs/`
- **Static prompts** — prompt is generated from current queue state
- **Ignoring circuit breaker** — stagnation means something structural is wrong
