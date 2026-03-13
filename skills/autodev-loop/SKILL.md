---
name: autodev-loop
description: >
  Autonomous development loop. Generates a context-aware prompt from the project's
  entity surfaces — plans, specs, chores — then schedules recurring execution.
  Teaches the AI how to generate the prompt, not what to do.
version: 2.0.0
extends: []
related_skills:
  - work
  - lev-align
  - workflow
skill_type: workflow
category: process-lifecycle
primitive_owner: work
triggers:
  - "autodev"
  - "dev loop"
  - "autonomous loop"
  - "conveyor belt"
  - "plan loop"
  - "maintenance loop"
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
  - bd CLI (optional, graceful degradation)
storage:
  tick_log: ".lev/pm/handoffs/"
---

# Autodev Loop — Autonomous Entity Execution

**Purpose**: Generate and schedule a recurring prompt that discovers work from the project's
entity surfaces, implements or validates it, promotes completed work, and self-feeds the queue.

This skill TEACHES the AI how to **generate** the loop prompt. It does NOT hardcode work items.

---

## Architecture

```
┌─────────────────────────────────────┐
│         autodev-loop skill          │ ← prompt generation + AI protocol
│                                     │
│  1. Read project config             │
│  2. Resolve entity surfaces         │─── input masks: what to scan
│  3. Discover entities               │─── core-sdlc SDK or filesystem
│  4. Generate context-aware prompt   │
│  5. Schedule via CronCreate         │
└─────────────────────────────────────┘
           │
           │ generated prompt, every N minutes
           ▼
┌─────────────────────────────────────┐
│       Agent execution tick          │
│                                     │
│  SCANNING → DOING → VALIDATING     │ ← the FSM
│                                     │
│  Uses: git, bd, pnpm test, etc.    │
└─────────────────────────────────────┘
```

---

## Core Protocol

### The FSM

The agent is always in exactly one mode:

```
SCANNING ──▶ DOING ──▶ SCANNING
    │                      ▲
    └──▶ VALIDATING ───────┘
```

- **SCANNING**: Find next entity by priority across all input surfaces. If queue < threshold, drift scan.
- **DOING**: Implement the next phase. Checkpoint after natural boundaries.
- **VALIDATING**: Run fitness functions. If ALL pass → promote to done surface.

### Git Protocol (Checkpoint Style)

Every tick ends with a checkpoint: `git add . && git commit -m "checkpoint: ..." && git pull --rebase && git push`.

Checkpoints happen at natural boundaries (phase completion, validation pass), NOT per-entity.
Multiple entities can land in a single checkpoint commit. The goal is keeping main always
up to date, not creating a perfect commit history.

**Reality**: worktrees are almost always dirty (modified submodules, parallel session
artifacts). Use the stash dance when pulling:

```bash
git stash && git pull --rebase && git stash pop
```

Pre-existing dirt in submodules is normal. Only investigate unexpected diffs in files
the current tick actually touched.

### Workstream Plan Loading (D10)

**Before running the generic SCANNING phase**, check for a workstream-specific plan:

1. `Glob` for `.lev/pm/plans/plan-autodev-loop-*.md`
2. If found, `Read` the plan file FIRST
3. Use the plan's wave structure, dependency rules, and dispatch constraints
4. The plan overrides generic surface scanning — it defines:
   - Which tasks are ready (wave-aware, dependency-aware)
   - Dispatch order and parallelism limits
   - What NOT to touch (scope boundaries)
   - The compilation target and architectural constraints
5. Only fall back to generic surface scanning if NO workstream plan exists

Also check for the active handoff:
1. `Glob` for `.lev/pm/handoffs/*-session-*.md` with `status: active`
2. `Read` the handoff to understand current wave, completed work, blockers
3. Cross-reference handoff progress against the plan's wave structure

This ensures the autodev tick has full context of the workstream, not just
a blind scan of entity surfaces.

### Agent Isolation (D9)

**Default: agents work on main.** Worktree isolation is opt-in, not automatic.

The autodev loop dispatches subagents directly on main unless the user explicitly
requests worktree isolation (e.g., `--worktree`, risky experiments, independent PR work).

**Why main-first:** During integration work, agents touching overlapping files
(e.g., schema rename + parallel execution both hitting execution-contract) create
cherry-pick conflicts that cost more to resolve than they save. Working on main
means agents see each other's changes immediately.

**When worktrees make sense (user opts in):**
- Risky experiments you might throw away
- Independent PRs for review
- Long-running work that shouldn't block main
- Explicit `--worktree` flag on `/autodev-loop`

**When to stay on main (default):**
- Integration work with overlapping files
- Sequential wave dispatch
- Checkpoint-style development

For tasks with overlapping `code_refs`, dispatch sequentially, not in parallel.
For truly independent tasks (non-overlapping files), parallel subagents on main are fine.

### Multi-Agent Awareness (D11)

Multiple autodev loops can run concurrently on different workstreams (e.g.,
`/autodev-loop` for graph-convergence, `/autodev-lev` for sdlc-convergence).
Each loop must be aware of the others to avoid conflicts.

**Scan phase addition — fresh handoff check:**

Before dispatching work, scan for OTHER active handoffs:

1. `Glob` for `.lev/pm/handoffs/*-session-*.md`
2. Filter to `status: active` handoffs that are NOT your own workstream
3. If any were modified in the last 30 minutes (fresh), `Read` their:
   - `You Are Here` section (what they're working on)
   - `Entity Matrix` (what files they're touching)
   - Any notes/warnings left for other agents
4. Check for file overlap between their active work and your dispatch queue
5. If overlap detected: skip the conflicting entity, log why, pick the next one

**Leaving notes for other agents:**

When your tick touches shared modules (e.g., `execution-contract/`, `schema.ts`,
`orchestration/`), append a brief note to your handoff:

```markdown
### Cross-Agent Notes
- [2026-03-11 18:45] Touching execution-contract/types.ts — added hitl to InstructionKind
- [2026-03-11 19:02] Modified schema.ts GraphNodeType union — downstream consumers need update
```

Other agents scan these notes during their fresh handoff check.

**Conflict resolution priority:**
- Whichever agent has the task `in_progress` first owns the file
- If both agents need the same file, the one with the higher-priority task wins
- If tied, the graph-convergence workstream (policy plane) takes precedence
  over sdlc (execution plane) since policy changes cascade

### State Encoding

State lives in the **filesystem**, not metadata:

| Location | State |
|----------|-------|
| `{surface}/` | Active — needs work or validation |
| `{surface}/_done/` | Validated and promoted |

The `status` frontmatter field is advisory (falls back to `lifecycle_state` for backward compat). The file location is canonical.

---

## Entity Surface Model

The loop doesn't hardcode where work lives. It reads **input surfaces** from config.
Each surface defines what to scan, where done items go, and what file patterns to match.

### Default Surfaces (no config required)

When no `autodev` config exists, the loop uses these defaults:

```yaml
autodev:
  surfaces:
    - name: plans
      input: .lev/pm/plans/
      done: .lev/pm/plans/_done/
      patterns: ["plan-*.md"]

    - name: specs
      input: docs/specs/
      done: docs/specs/_done/
      patterns: ["plan-*.md", "chore-*.md"]  # backward compat
```

### Per-Project Config

Projects override surfaces in `.lev/config.yaml`:

```yaml
autodev:
  tick_interval: 10m
  max_parallel_agents: 6
  drift_scan_threshold: 3
  priority_field: priority
  blocked_states: [blocked, deferred]

  surfaces:
    # The PM surface — structured entity lifecycle
    - name: plans
      input: .lev/pm/plans/
      done: .lev/pm/plans/_done/
      patterns: ["plan-*.md"]

    # The specs surface — where specs and legacy chores live
    - name: specs
      input: docs/specs/
      done: docs/specs/_done/
      patterns: ["plan-*.md", "chore-*.md"]

    # Example: a project that wants root-level specs/
    # - name: root-specs
    #   input: specs/
    #   done: specs/_done/
    #   patterns: ["*.md"]
```

### Input Masks (Backward Compatibility)

The `patterns` array is the input mask. It controls what the loop sees.

| Pattern | What it matches | Use case |
|---------|----------------|----------|
| `plan-*.md` | Forward-looking plans | New convention |
| `chore-*.md` | Legacy cleanup items | Leviathan backward compat |
| `*.md` | Everything | Broad scan |

**The key insight**: if you like seeing chores in `docs/specs/`, just add `chore-*.md` to your
specs surface pattern. The loop doesn't care about the prefix — it reads frontmatter for priority,
status, and fitness functions regardless.

### Output Convention

When the loop generates NEW entities (from drift scans), it writes to the **first writable surface**
using the project's preferred naming:

```yaml
autodev:
  output:
    prefix: plan       # or "chore" for legacy projects
    surface: plans     # which surface to write new entities to
```

Default: `prefix: plan`, `surface: plans` (writes `plan-*.md` to `.lev/pm/plans/`).

If you flip `prefix: chore`, drift-discovered items get written as `chore-*.md` — fully backward
compatible with the 34-tick session that just shipped 76 chores.

---

## Entity Lifecycle Integration

The loop is entity-lifecycle aware. It understands the `work` skill's entity states:

```
ephemeral → captured → classified → crystallizing → crystallized → manifesting → completed
```

### How status maps to loop behavior

`status` is the canonical frontmatter field (falls back to `lifecycle_state` for backward compat).

| `status` | Loop action |
|----------|-------------|
| `draft` | Skip (not ready for autonomous work) |
| `active` | DOING — implement next phase |
| `implementing` | DOING — continue implementation |
| `blocked` | Skip |
| `deferred` | Skip |
| `ready_for_validation` | VALIDATING — run fitness functions |
| `validated` | Promote to done surface |
| `completed` | Should already be in `_done/` |

### Frontmatter Contract

Every entity the loop processes should have:

```yaml
---
title: "Human-readable title"
status: active                   # required (canonical field; `lifecycle_state` accepted as fallback)
priority: P1                     # P0-P4 or 0-4
type: plan-impl | plan-chore | plan-bugfix | plan-research | plan-migration
fitness_functions:               # optional section name or inline
  - "pnpm --filter @lev-os/foo test"
  - "grep -q 'export function bar' core/foo/src/index.ts"
tags: [needs-runtime]            # optional skip tags
---
```

---

## Fitness Functions

Every entity SHOULD define fitness functions. No fitness functions = promote on implementation
completion only (weaker gate, but practical for small items).

Fitness functions can be:
- **Inline** — described in markdown (AI evaluates against code)
- **Executable** — shell command that exits 0/1
- **Test reference** — `pnpm --filter @lev-os/foo test`
- **Structural** — "exports X from Y", "no imports from Z"

---

## Drift Scanning

When active entities < `drift_scan_threshold`, the loop self-feeds:

1. For each spec in `docs/specs/spec-*.md`:
   - Compare `code_refs` paths against actual exports
   - Check `validation_gates` thresholds against test coverage
   - Look for documented invariants violated in code
2. Generate new entity files in the configured output surface
3. Resume normal SCANNING

### Internal Consistency Checks

When auditing specs (AUDITING mode), check for these self-contradiction patterns:

1. **Executive summary vs invariants** — if the summary says "pure re-export" but an invariant
   acknowledges mutable state, the spec contradicts itself
2. **Ownership table vs directory listing** — run `ls src/` and compare against ownership rows.
   Missing files = undocumented surface area
3. **BDD scenarios vs code paths** — scenarios should reference real functions/files.
   Phantom references = spec drift
4. **Validation gate thresholds vs test reality** — if a gate says "100% coverage" but
   the module has 60%, the gate is aspirational not descriptive
5. **Config defaults vs spec recommendations** — if code defaults to `xenova` but spec
   waterfall never recommends it, there's a gap

When contradictions are found, create a new chore entity documenting the specific
contradictions with line references to both the spec and the code.

---

## Agent Orchestration

The loop can dispatch work to parallel agents when entities are independent.

### When to Parallelize

- **YES**: Entities with non-overlapping `code_refs` (e.g., 3 spec fixes touching different modules)
- **YES**: Audit chores that only READ code (no writes to shared files)
- **NO**: Entities sharing the same spec file (concurrent edits conflict)
- **NO**: Entities with overlapping `code_refs` paths

### Orchestration Pattern

```
Main agent: strategic work (roadmap updates, build analysis, handoff)
Background agents: independent chores (spec fixes, ownership table updates)
```

Launch 3-4 background agents on independent entities. Main agent continues with
the next priority item or strategic planning. Background agents return manifests
of files touched — main agent commits and pushes.

### Agent Brief Template

Each background agent gets:
1. The entity file path and content
2. The relevant spec file (if fixing a spec)
3. The `_done/` path for promotion
4. Instruction: "Fix, validate fitness functions, move to _done/, return manifest"

---

## Entity Sizing

Estimate tick budget before starting work. Prevents scope explosion.

| Size | Ticks | Signals | Action |
|------|-------|---------|--------|
| S | 1 | 1-3 code_refs, <5 steps, typo/label fix | Do in current tick |
| M | 1-2 | 4-10 code_refs, new ownership rows + BDD scenarios | Do or split across 2 ticks |
| L | 3-5 | 10+ code_refs, multi-file extraction, new package creation | Decompose into S/M entities first |
| XL | Epic | Multiple directories, >2500 LOC moved, design decisions needed | Create epic with sub-entities, schedule as separate workstream |

### Sizing Heuristics

- Count `code_refs` entries in frontmatter — each ref ≈ 1 file to read/validate
- Count `## Steps` in the entity body — each step ≈ one focused action
- If LOC estimate > 500 in a single entity → decompose
- If entity mentions "design decision needed" → it's L or XL, not M

---

## Blocked Entities

Detect and skip blocked entities gracefully. Don't waste ticks on unactionable work.

### Detection

Frontmatter signals:
- `status: blocked` or `deferred` (also accepts `lifecycle_state` as fallback)
- `blocker:` field (freetext describing the blocker)
- `blocked_by:` field (entity ID or external dependency)

Body signals:
- "BLOCKED" in a status column
- "blocked on" or "waiting for" in step descriptions
- Steps with status "blocked" in tables

### Handling

1. Skip blocked entities in the priority queue
2. Log them in the tick summary: `Blocked: [entity] — [reason]`
3. Check blockers periodically — if a blocker resolves, the entity becomes actionable
4. Never attempt to "work around" a blocker by partially implementing — park it cleanly

---

## Prompt Generation

The skill generates the prompt dynamically from current project state.

### Generation Algorithm

```
1. Read project config for autodev section (or defaults)
2. Resolve all surfaces from config
3. For each surface, scan matching patterns
4. Parse frontmatter: priority, status (fallback: lifecycle_state), fitness_functions
5. Merge all entities into priority queue (P0 first, skip blocked)
6. Count active → decide if drift scan needed
7. Generate prompt with:
   - All surface locations
   - Merged queue summary
   - Mode rules (DOING/VALIDATING/SCANNING)
   - Git protocol (commit + push every tick)
   - Parallel agent cap
   - Handoff location
```

### Generated Prompt Template

```
scan these surfaces for work:
{for each surface: "  - {input}/{patterns}"}

you are always in one of three modes:
DOING (implementing a plan phase), VALIDATING (checking fitness functions),
or SCANNING (finding next entity).

rules:
- prioritize P0 > P1 > P2 > P3 > P4. skip BLOCKED/DEFERRED items.
- when DOING: implement one phase. commit after each phase.
- when VALIDATING: run fitness functions. if ALL pass → move to surface's _done/.
  update status in frontmatter to "validated".
- when SCANNING and active entities < {threshold}: run drift scan against specs.
- use up to {max_agents} parallel agents for independent work.
- skip entities tagged needs-runtime.
- git pull --rebase && push every tick.
- update handoff in .lev/pm/handoffs/ with tick log.
- keep entity yaml frontmatter `status` current (accepted alias: `lifecycle_state`).

current queue ({n} active across {s} surfaces):
{priority-sorted entity list with surface, status, and FF indicator}
```

### Invocation

```
/autodev-loop                    # generate prompt + schedule at default interval
/autodev-loop 5m                 # custom interval
/autodev-loop --dry-run          # show generated prompt without scheduling
/autodev-loop --surface plans    # scan only the named surface
/autodev-loop --stop             # kill active loop
```

---

## On Load: Immediate Actions

1. Read project config for `autodev` section (or use defaults)
2. Resolve all entity surfaces
3. Scan all surfaces, merge into priority queue
4. Generate the prompt
5. Parse invocation args:
   - `--dry-run`: show prompt and stop
   - `--stop`: CronDelete active loop and stop
   - `--surface X`: filter to named surface only
   - `Nm` / `Nh`: override tick interval
6. CronCreate with generated prompt at configured interval
7. Confirm to user: what's scheduled, queue size, surfaces scanned, cron expression

---

## Integration with core-sdlc

The skill calls SDK functions when available:

```typescript
import { discoverPlans, promotePlan, generateLoopPrompt } from '@lev-os/core-sdlc';
```

When SDK is not available (pure skill mode), the loop uses filesystem operations directly:
- `glob` / `find` for discovery
- Read frontmatter for priority + fitness functions
- `mv` for promotion
- `grep` for drift scanning

The SDK functions in `plugins/core-sdlc/src/commands/loop.ts` handle:
- `discoverPlans(config)` — multi-surface scan + frontmatter parse + priority sort
- `generateLoopPrompt(config)` — context-aware prompt compilation
- `promotePlan(path, config)` — filesystem state transition
- `extractFrontmatter(content)` — minimal YAML parser (zero deps)

---

## Config Hierarchy

The autodev config follows lev's fractal config model:

```
system config  (~/.config/lev/config.yaml)    ← global defaults
  ↓ overridden by
project config (.lev/config.yaml)             ← per-project surfaces
  ↓ overridden by
CLI flags      (--surface, interval arg)      ← per-invocation
```

This means:
- Global defaults give every project a working autodev loop out of the box
- Projects customize surfaces, patterns, and output conventions
- One-off invocations can narrow scope without changing config

---

## Relationship to Existing Systems

| System | Role | Autodev's relationship |
|--------|------|----------------------|
| `work` skill | FSM lifecycle router | Autodev is the **autonomous mode** of work |
| `core-sdlc` plugin | SDLC commands + event providers | Autodev's SDK runtime |
| `core/config` | Config resolution | Reads `autodev` namespace |
| `.lev/pm/plans/` | Canonical plan surface | Primary input surface |
| `docs/specs/` | Spec + legacy chore surface | Secondary input surface |
| `prompt-stack` | Deterministic step execution | Future: ticks run as prompt-stack sessions |
| `bd` tracker | Execution-plane tracking | Loop can create/update bd issues per tick |

---

## Anti-Patterns

- **Hardcoded work items** — prompt MUST be generated from surfaces, not static
- **Skipping fitness functions** — no "looks done" promotions. Binary pass/fail.
- **Unbounded blast radius** — each tick: 1 entity or 1 phase of 1 entity
- **No handoff** — every loop session must maintain a tick log
- **Static prompts** — the whole point is the prompt adapts to current state
- **Single surface assumption** — always resolve ALL configured surfaces

---

## Handoff Format

The handoff is a **roadmap with scorecard**, not a tick journal. Tick-by-tick logs get
compacted away — the roadmap survives.

### Template

```markdown
# Loop Session — {date}

## Scorecard

**Aligned (N/M):** module1, module2, ...
**Active (K chores):** [chore] — [status/next action]
**Blocked:** [chore] — [blocker]

## Tracks

### Track 1: {category}
| Entity | Priority | Status | Next Action |
|--------|----------|--------|-------------|
| ... | ... | ... | ... |

### Track 2: {category}
...
```

### Rules

- Update the scorecard after EVERY tick, not just at session end
- Tracks group related entities (spec alignment, integration, extraction, blocked)
- Never append per-tick logs — summarize progress into the track tables
- The handoff should be readable by a cold-start agent in <30 seconds

---

## Semantic Notes

- **"Plan" not "chore"** — plans are forward-looking. The loop handles both but semantics are aspirational.
- **"Entity"** — generic term for any work item the loop processes (plan, chore, task).
- **"Surface"** — a directory + pattern that defines where entities live.
- **"Promote" not "close"** — moving to `_done/` preserves the artifact as evidence.
- **"Fitness function" not "test"** — broader than unit tests: structural checks, linting, analysis.
- **"Input mask"** — the pattern array that controls what the loop sees on a surface.

---

## Migration Path

For projects currently using `chore-*.md` in `docs/specs/`:

1. **No change required** — default config includes `chore-*.md` in the specs surface pattern
2. **Gradual migration** — new entities go to `.lev/pm/plans/` as `plan-*.md`
3. **Full migration** — remove `chore-*.md` from specs surface pattern when all chores are promoted
4. **Config flag** — set `output.prefix: chore` to keep generating chore-prefixed files

The system is backward compatible by default. Migration is opt-in and gradual.

---

## Claude Code Runtime (Canonical Execution Protocol)

When running in Claude Code (no lev CLI available), use these concrete tool mappings.
This is the **actual execution protocol** — everything above is architecture and config.

### Quick Start

```
/autodev-loop              # Scan queue, show status, ask before scheduling
/autodev-loop 5m           # Scan + schedule at 5 min intervals
/autodev-loop --scan       # Read-only scan, show queue
/autodev-loop --execute    # Execute highest-priority item now
/autodev-loop --worktree   # Opt-in: use worktree isolation for subagents
/autodev-loop --dry-run    # Show what --execute would do, without doing it
/autodev-loop --stop       # CronDelete the active loop
/autodev-loop --status     # Show queue, active cron, last tick
```

### SCAN → Claude Code

1. `Glob` for `**/.lev/pm/plans/plan-*.md` — primary surface.
2. `Glob` for `**/.lev/pm/specs/**/*.md` and `**/docs/specs/**/*.md` — secondary surfaces.
3. Filter out `_done/` paths.
4. `Read` each file, parse YAML frontmatter.
5. Skip `status: blocked | deferred | draft` (also checks `lifecycle_state` fallback).
6. If `depends_on` / `blocked_by` in frontmatter → check dependency files, skip if not in `_done/`.
7. Sort by `priority` (P0 > P1 > P2 > P3 > P4).
8. For each entity with `fitness_functions`, run via `Bash`. Record pass/fail.
9. If ALL fitness functions pass → auto-promote:
   - `Bash`: `mkdir -p "$(dirname "$FILE")/_done" && mv "$FILE" "$(dirname "$FILE")/_done/"`
   - If `bd_id` set → `Bash`: `bd close $BD_ID` (skip if bd unavailable)
10. Output queue table.

### EXECUTE → Claude Code

1. Run SCAN, pick highest-priority "Ready" entity.
2. `Read` full plan + all `code_refs`.
3. If `bd_id` → `Bash`: `bd update $BD_ID --status=in_progress` (skip if unavailable).
4. Assess complexity:
   - **Simple** (1-2 code_refs, <5 steps): inline `Read`/`Edit`/`Write`/`Bash`.
   - **Medium** (3-5 code_refs): `Agent` tool, single subagent on main.
   - **Complex** (6+ code_refs): `Agent` tool, 2-4 parallel subagents on main. Sequential for overlapping files, parallel only for non-overlapping `code_refs`. Use `isolation: "worktree"` only when `--worktree` flag was passed.
5. After execution → run VALIDATE.
6. If pass: checkpoint commit (`git add . && git commit && git pull --rebase && git push`), promote.
7. If fail: update `lifecycle_state: active`, report remaining work.

### SCHEDULE → Claude Code

1. Run SCAN to show current queue.
2. `CronCreate` with prompt: `Run /autodev-loop --execute`
3. Report cron ID for later `--stop`.

### Drift Scan → Claude Code

When SCAN finds zero actionable entities:

1. `Bash`: run project test command (`npm run test:run`, `pnpm test`, etc.)
2. `Bash`: `npx tsc --noEmit` (TypeScript projects)
3. `Grep` for `TODO|FIXME|HACK` in recently modified files
4. If issues found → `Write` new `plan-*.md` entities with proper frontmatter
5. If clean → report "Queue empty. Codebase clean." and idle.

### Error Handling

| Situation | Action |
|-----------|--------|
| `bd` not available | Skip all bd calls, filesystem state only |
| Fitness function errors | Mark ERROR, skip entity, report |
| Agent failure | Report, leave entity active |
| No entities found | Drift scan |
| No fitness_functions | Execute, promote on completion |
| All blocked/deferred | Report blocked queue |

### Report Format

```
## Autodev Loop Report

**Mode**: SCAN | EXECUTE | SCHEDULE | STOP | STATUS
**Queue**: N items (X ready, Y partial, Z promoted)
**Action taken**: <what was done>
**Files touched**: <absolute paths>
**Next**: <recommendation>
```

### Rules

- One entity per tick maximum.
- Checkpoint after completing an entity (not per-phase commits).
- Use absolute paths in all tool calls.
- Pass full plan content + file contents to subagents (no worktree isolation).
- Degrade gracefully when tools/CLIs are missing.
- Never promote without running fitness functions first.
- Always load workstream plan before generic scanning (D10).
