---
name: ll
description: "Loop maker + scheduler. Creates typed tick loops with dynamic flowmind validation, meta-prompting, and AXI-first output. Use when starting recurring work, building content pipelines, running quality loops, or scheduling autonomous ticks."
triggers:
  - ll
  - levloop
argument-hint: "[create|schedule|run|status|ticks|list|stop|pause|proposal] <description or loop-file>"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent]
---

# /ll — Loop Maker + Tick Scheduler

Create, schedule, and run typed tick loops with constraint engineering discipline.

## Invocation

```
/ll create "iterate on manifesto content"    # Generate loop YAML
/ll schedule 10m                              # Schedule via CronCreate
/ll run                                       # Run one tick now
/ll status                                    # Show loop state + tick history
/ll ticks                                     # Show tick type distribution
/ll list                                      # List all loops
/ll stop                                      # CronDelete active loop
/ll pause                                     # Pause loop (user can resume)
/ll proposal                                  # Loop proposes next actions instead of executing
/ll inspect <tick-id>                         # Show tick details + report
```

## Tick Execution Model

**Every tick parallelizes all independent work:**
- Dispatch flowminds, tasks, exec items simultaneously via Agent tool
- Use haiku subagents for small/research items (parallel_safe)
- Use direct execution for serial/dependent items
- Max 3 parallel exec agents per tick (C1 bounded)
- Each agent reports: DONE | NEEDS_CONTEXT | BLOCKED

**Self-learning:** Loop rescheduling when new data arrives mid-tick.
When /capture or user input adds new items, reschedule with updated queue.

**Preflight:** Before each tick, check:
1. Dependencies resolved (blockers cleared?)
2. Critical path via samurai scout (what unblocks the most?)
3. Budget remaining (max iterations, token budget)
4. Workstream + lifecycle hygiene (graph footer, handoff current?)

**After first schedule:** Run first tick immediately (don't wait for cron).

**CPU scheduling:** Each loop has workstream-scoped lifecycle hygiene ticks
interleaved with execution ticks. Hygiene = drift check, orphan scan, HUD check.

## HUD — Always-On Status Line

Every /ll response ends with a single HUD line. Not a footer. A status bar.

```
🧬 {ws} ⚡{exec} 📥{capture} ⏸️{paused} ✅{done} | 🚦{gate}={score} | ⏭️ {next} | 🔁ll:t{N} {delay}s
```

**Symbols:**
- `⚡` = executing right now
- `📥` = in capture/classify
- `⏸️` = paused (needs decision)
- `✅` = done this session
- `🚦` = current gate + score
- `⏭️` = what's next
- `🔁` = loop tick + delay

**/siterep** = expanded view (full dashboard). The HUD is the collapsed always-on version.

**This replaces the graph footer.** One line > six lines. Always present. Never forgotten.

## /ll IS /work (converging)

/ll and /work are the same thing at different timescales:
- `/work` = interactive, human-paced, one entity at a time
- `/ll` = autonomous, loop-paced, parallel entities per tick
- Both use `lifecycle-manifest.yaml` for verb→skill routing
- Both check gates via `DefaultGateEvaluator` (now with UNCERTAIN + variable triples)
- Both follow `idle-exec-policy.yaml` for auto-advance vs HITL decisions

The merge: /work calls /ll for execution. /ll calls /siterep for status. /siterep reads the same state.

---

## Loop Definition Generator

`/levloop create` produces a YAML file at `.lev/loops/<loop-id>/loop.yaml`:

```yaml
id: content-gtm-sprint
name: "Constraint Engineering GTM Content Loop"
description: "Iterate manifesto, articles, tweets, and publish pipeline"

tick_types:
  - id: manifesto
    description: "Create or iterate manifesto /now pages"
    weight: 25
    max_consecutive: 2

  - id: article
    description: "Write or improve articles"
    weight: 30
    max_consecutive: 3

  - id: research
    description: "Re-read source docs, identify gaps"
    weight: 15
    requires_after: [manifesto, article]  # must follow creative work
    min_interval: 3  # ticks between research ticks

  - id: review
    description: "De-slopify, quality check, voice alignment"
    weight: 15
    requires_after: [article]

  - id: discover
    description: "Identify new top-level themes, promote to manifesto"
    weight: 10
    min_interval: 5

  - id: publish
    description: "Publish to here.now, Substack, social"
    weight: 5
    requires_after: [review]

tick_constraints:
  ordering: weighted_random    # weighted_random | round_robin | priority | waterfall
  self_validation: false       # agent that does work NEVER validates its own
  max_ticks_per_session: 20

validation:
  between_ticks: true          # generate adversarial flowmind between ticks
  flowmind_template: adversarial-review  # base template
  auto_escalate_after: 3       # escalate to human after 3 consecutive failures

schedule:
  interval: 10m                # CronCreate interval
  duration: 6h                 # auto-stop after duration
  circuit_breaker:
    threshold: 3               # consecutive no-advancement ticks
    action: stop               # stop | escalate | hygiene

execution:
  adapter: claude-agent-sdk
  model: sonnet
  max_turns_per_tick: 15
  verifier: null               # shell command, exits 0 on success

knobs:
  source_dir: "~/.agents/levnow"
  content_dir: "content/"
  prd_path: "content/ralph/prd.json"
```

---

## Tick Type System

### Built-in Types

| Type | Purpose | Default Weight |
|------|---------|---------------|
| `sweep` | Pre-check: move validated entities to done | 5% |
| `validate` | Verify previous tick's output (never self-validate) | 15% |
| `execute` | Do actionable work (highest priority ready item) | 30% |
| `research` | Re-read source material, identify gaps | 15% |
| `review` | Quality check, de-slopify, voice alignment | 20% |
| `discover` | Identify new topics, promote to top-level | 10% |
| `publish` | Push to here.now, Substack, social platforms | 5% |

### Ordering Strategies

| Strategy | How It Works |
|----------|-------------|
| `weighted_random` | Random selection weighted by type weight %. Good for balanced loops. |
| `round_robin` | Cycles through types in declared order. Predictable. |
| `priority` | Always picks highest-weight eligible type. Work-heavy. |
| `waterfall` | Autodev-loop style: sweep → validate → execute → hygiene. Falls through. |

### Selection Algorithm

Each tick:
1. Filter by `max_consecutive` — skip types that hit their consecutive limit
2. Filter by `min_interval` — skip types that ran too recently
3. Filter by `requires_after` — skip types whose prerequisite hasn't run
4. From remaining, select by ordering strategy
5. If nothing eligible, run hygiene/discover (always eligible)

### Self-Validation Rule

**The agent that does work NEVER validates its own work.**
Validation is always done by the NEXT tick. This is inherited from autodev-loop
and is non-negotiable. Set `self_validation: false` (the default).

---

## Meta-Prompting: How to Write Tick Prompts

Every tick generates a prompt for `lev exec`. The prompt must answer 5 questions:

### The 5 Questions

1. **What does PASSING look like?** Show a reference file/module that already works.
2. **What does FAILING look like?** Show the exact current state or error.
3. **What specifically needs to change?** File, section, old value → new value.
4. **What must NOT change?** Scope boundary. "Touch ONLY these files."
5. **How do I verify?** Shell command that exits 0 on success.

### Tick Prompt Template

```
You are executing a [{tick_type}] tick for loop [{loop_id}].

## Context
{Read the loop YAML. Read the PRD. Read the last tick report.}

## Current State
{What exists now. Word counts, file paths, quality scores.}

## Task
{Specific work for this tick type. ONE actionable item.}

## Reference
{A file that shows what "good" looks like for this type of work.}

## Scope
Touch ONLY: {list of files}
Do NOT modify: {exclusion list}

## Done Criteria
1. {Verifiable condition 1}
2. {Verifiable condition 2}
3. {Shell command that exits 0}
```

### Bad vs Good

**Bad** (vague, no verification):
```
Write another article about constraint engineering.
```

**Good** (specific, bounded, verifiable):
```
You are executing an [article] tick for loop [content-gtm-sprint].

## Task
Write article "Two Axioms and Everything That Follows" (WRITE-011 from PRD).
Deep dive into C1 Finitude and C2 Non-Commutation from dna/graph.yaml.

## Reference
Read content/articles/the-genesis-pattern-four-steps-to-ai-native-software.md
— it demonstrates the right voice, structure, and depth. 2,118 words.

## Scope
Create ONLY: content/articles/two-axioms-and-everything-that-follows.md
Do NOT modify existing articles.

## Done Criteria
1. File exists at content/articles/two-axioms-and-everything-that-follows.md
2. Word count >= 1200
3. Contains "C1 Finitude" and "C2 Non-Commutation"
4. Contains at least one quote from dna/graph.yaml
5. wc -w content/articles/two-axioms-and-everything-that-follows.md | awk '{exit ($1 < 1200)}'
```

---

## Single Tick Execution

Each tick follows this 10-step procedure:

```
1. LOAD loop YAML from .lev/loops/<loop-id>/loop.yaml
2. LOAD state from .lev/loops/<loop-id>/state.json
3. SELECT tick type using ordering strategy + constraints
4. GENERATE prompt using meta-prompting template + current state
5. EXECUTE via lev exec or inline (Agent tool for complex, Read/Edit for simple)
6. RECORD result to .lev/loops/<loop-id>/ticks/<tick-number>.json
7. UPDATE state.json (tick count, type history, advancement tracking)
8. CHECKPOINT git (git add . && git commit -m "levloop: {tick_type} — {summary}")
9. EMIT telemetry (tick type, duration, files changed, advancement)
10. SELECT next tick (or exit if circuit breaker / duration limit)
```

### State Schema

```json
{
  "loop_id": "content-gtm-sprint",
  "total_ticks": 14,
  "ticks_by_type": { "article": 5, "review": 3, "manifesto": 3, "research": 2, "discover": 1 },
  "consecutive_type": { "type": "article", "count": 2 },
  "consecutive_no_advancement": 0,
  "last_tick": { "number": 14, "type": "review", "advanced": true, "timestamp": "..." },
  "created": "2026-04-10T18:00:00Z",
  "scheduled_cron_id": "cron-abc123"
}
```

---

## Scheduling

### Slice Mode (one tick)
```
/levloop run     # Scan → pick type → execute → checkpoint
```

### Time Mode (recurring)
```
/levloop schedule 10m        # CronCreate with 10min interval
/levloop schedule 6h         # Auto-stop after 6 hours
/levloop stop                # CronDelete
```

Time mode is slice mode on a cron. Each tick runs independently with fresh context.
Memory persists through the filesystem (state.json, tick reports, git history).

### Exit Taxonomy

| Exit Reason | Trigger |
|-------------|---------|
| `no_work` | First scan found zero actionable items |
| `all_done` | PRD stories all have `passes: true` |
| `budget_exhausted` | Token usage crossed budget |
| `circuit_breaker` | K consecutive no-advancement ticks |
| `duration_limit` | Schedule duration exceeded |
| `interrupted` | SIGINT, SIGTERM, or manual `/levloop stop` |

---

## Dynamic Flowmind Generation

Between ticks, auto-generate an adversarial validation flowmind:

1. Read the previous tick's output (files changed, report)
2. Extract invariants that should hold (word count, voice consistency, no forbidden patterns)
3. Generate a 3-node flowmind YAML:

```yaml
name: tick-validation-{tick_number}
entry: check
nodes:
  check:
    op: lev.validate
    inputs:
      command: |
        # Check invariants from previous tick
        wc -w {file} | awk '{exit ($1 < 1200)}'
        grep -q "constraints are the product" {file}
        ! grep -qi "game-changer\|rapidly evolving\|in conclusion" {file}
    branches:
      pass: report
      fail: escalate
  report:
    terminal: true
  escalate:
    op: lev.exec
    inputs:
      task: "Previous tick output failed validation. Fix: {failure details}"
    next: check
    max_iterations: 2
    on_timeout: report
```

4. Save to `.lev/loops/<loop-id>/flowminds/validate-tick-{n}.flow.yaml`
5. Run before the next creative tick

### C4 Ratchet for Validation

If the same invariant fails 3+ times across ticks, promote it from the generated
flowmind to the loop's `validation` section (permanent). Gates only move forward.

---

## Rounds vs Turns

| Unit | Definition |
|------|-----------|
| **Turn** | One agent interaction (one prompt → one response) |
| **Round** | A unit of work measured by context fill % OR turn count |
| **Tick** | One loop iteration. May contain multiple rounds. |
| **Loop** | The entire scheduled sequence of ticks. |

```
Loop
└── Tick (selected by type system)
    └── Round (bounded by context % or turn count)
        └── Turn (single agent interaction)
```

### Configuration

```yaml
rounds:
  strategy: context_fill    # context_fill | turn_count | hybrid
  context_threshold: 0.7    # exit round when context is 70% full
  max_turns: 10             # hard cap on turns per round
  telemetry_routing: true   # use session telemetry in flowmind if/else
```

### Telemetry-Driven Routing

Session telemetry feeds into flowmind routing decisions:
- `tokens_used` / `context_window` → context pressure
- `turns_completed` → progress indicator
- `gates_passed` / `gates_failed` → quality signal
- `files_changed` → blast radius

FlowMind nodes can branch on these:
```yaml
check_progress:
  op: lev.validate
  inputs:
    command: "test $(cat .lev/loops/state.json | jq '.consecutive_no_advancement') -lt 3"
  branches:
    pass: next_tick
    fail: escalate
```

---

## TOON-First CLI Output

Follow AXI principles — base command shows data + next action, no `--help` walls.

### `/levloop status` output:
```
content-gtm-sprint  14 ticks  6 types  ▓▓▓▓▓▓▓▓░░ 70%
  last: review #14 (2m ago)  next: article (weighted)
  articles: 10/15  manifesto: 1/6  tweets: 50

  Next: /levloop run
  Schedule: /levloop schedule 10m
```

### `/levloop ticks` output:
```
  article   ████████████████  5  (36%)
  review    █████████         3  (21%)
  manifesto █████████         3  (21%)
  research  ██████            2  (14%)
  discover  ███               1  (7%)
  publish                     0  (0%)

  Recent: review → article → article → manifesto → research
  Next eligible: article, manifesto, discover, publish
```

---

## Loop Catalog

### 1. Content Iteration Loop
```yaml
tick_types:
  - { id: manifesto, weight: 25 }
  - { id: article, weight: 30, max_consecutive: 3 }
  - { id: review, weight: 20, requires_after: [article] }
  - { id: research, weight: 15, min_interval: 3 }
  - { id: discover, weight: 10, min_interval: 5 }
```

### 2. Code Quality Loop
```yaml
tick_types:
  - { id: drift_scan, weight: 25, description: "Spec-code drift detection" }
  - { id: gate_fix, weight: 30, description: "Fix failing validation gates" }
  - { id: test_write, weight: 25, requires_after: [gate_fix] }
  - { id: cleanup, weight: 15, description: "Dead code, unused imports" }
  - { id: audit, weight: 5, min_interval: 5 }
```

### 3. Spec Alignment Loop
```yaml
tick_types:
  - { id: scan, weight: 20, description: "Read spec, compare to code" }
  - { id: update_spec, weight: 25, requires_after: [scan] }
  - { id: update_code, weight: 25, requires_after: [scan] }
  - { id: verify, weight: 20, requires_after: [update_spec, update_code] }
  - { id: document, weight: 10, min_interval: 4 }
```

### 4. Deep Research Loop
```yaml
tick_types:
  - { id: read_source, weight: 30, description: "Read primary sources" }
  - { id: synthesize, weight: 25, requires_after: [read_source] }
  - { id: compare, weight: 20, description: "Compare against existing knowledge" }
  - { id: gap_fill, weight: 15, requires_after: [compare] }
  - { id: summarize, weight: 10, min_interval: 3 }
```

---

## Integration Points

| System | How /levloop Uses It |
|--------|---------------------|
| autodev-loop | Tick waterfall pattern, self-validation ban, entity lifecycle |
| `executeIterativeLoop()` | Runtime primitive for bounded iteration within a tick |
| `runHeartbeat()` | Runtime primitive for sleep-paced tick scheduling |
| EventBus + TriggerDispatcher | Event-driven tick triggering (future: git commit → tick) |
| CronCreate | Time-based scheduling |
| bd (beads) | Issue tracking per tick output |
| FlowMind | Validation flowminds between ticks |
| lev exec | Agent dispatch for tick execution |

---

## Anti-Patterns

- **Self-validation** — worker NEVER validates its own output
- **Unbounded ticks** — one actionable item per tick maximum
- **Skipping validation** — always run generated flowmind between creative ticks
- **No state persistence** — state.json must be written after every tick
- **Static prompts** — prompts are generated from current state, not templates
- **Ignoring circuit breaker** — 3 no-advancement ticks means something structural is wrong
- **Giant ticks** — if a tick needs 20+ turns, it should be split into rounds
- **No handoff** — loop maintains handoff at `.lev/pm/handoffs/`

---

## On Load

1. Parse invocation args
2. If `create`: generate loop YAML interactively
3. If `run`: load loop YAML → load state → select tick → execute → checkpoint
4. If `schedule`: CronCreate with interval
5. If `status/ticks/list`: read state, format TOON output
6. If `stop`: CronDelete, write final state
