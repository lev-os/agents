---
name: autodev-lev
description: "Heartbeat-driven autonomous development loop using `lev loop autodev`, with interval, budget, and tick controls for in-process SDLC execution."
metadata:
  version: 1.0.0
  related_skills:
    - autodev-loop
    - work
    - lev-core
  skill_type: workflow
  category: process-lifecycle
---

# Autodev Lev

> Heartbeat-driven autonomous development loop using Lev primitives.
> Unlike `/autodev-loop` (which uses Claude Code CronCreate), this runs through `lev loop autodev`
> with sleep-based pacing — staying in-process with full state continuity between ticks.

## Invocation

```
/autodev-lev                           # Start with defaults (5m heartbeat)
/autodev-lev 10m                       # Custom interval
/autodev-lev --budget=50k              # Token budget cap
/autodev-lev --max-ticks=5             # Stop after 5 ticks
/autodev-lev --until="all specs pass"  # Semantic exit condition
/autodev-lev status                    # Show queue and config
/autodev-lev --dry-run                 # Scan only, show what would execute
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Top-Level Orchestrator (you)                           │
│  Manages SDLC stages: SCAN → PLAN → EXEC → VALIDATE    │
└──────────────┬──────────────────────────────────────────┘
               │ /autodev-lev 5m
               ▼
┌─────────────────────────────────────────────────────────┐
│  Heartbeat Loop (lev loop autodev)                      │
│                                                         │
│  ┌──────┐  sleep(5m)  ┌──────┐  sleep(5m)  ┌──────┐   │
│  │SCAN  │────────────→│SCAN  │────────────→│SCAN  │   │
│  └──┬───┘             └──┬───┘             └──┬───┘   │
│     │ entities?           │ entities?          │ none   │
│     ▼                     ▼                    ▼        │
│  ┌──────┐             ┌──────┐           all_done      │
│  │ EXEC │             │ EXEC │                          │
│  └──┬───┘             └──┬───┘                          │
│     │                     │                              │
│     └─ runSdlcLoop()     └─ runSdlcLoop()               │
│        (token spend)        (token spend)                │
└─────────────────────────────────────────────────────────┘
```

## Key Difference from autodev-loop

| | autodev-loop | autodev-lev |
|---|---|---|
| **Runtime** | Claude Code CronCreate | `lev loop autodev` (in-process) |
| **Pacing** | Cron fires fresh invocation | Sleep between ticks (state preserved) |
| **Token efficiency** | Every tick = new context load | Scan phase = zero LLM cost |
| **State** | Stateless across ticks | Full continuity in-process |
| **Concurrency** | Single agent per cron tick | maxWorkers per tick |
| **Exit conditions** | Manual `/autodev-loop --stop` | Budget, until, max-ticks, circuit breaker |

## Protocol

### Phase 0: Pre-flight

1. Check `lev loop` for entity queue
2. Determine interval, budget, exit conditions
3. Execute `lev loop autodev` with flags

### Phase 1: Scan (zero cost)

- Filesystem glob across configured surfaces (`.lev/pm/plans/`, `docs/specs/`)
- Parse frontmatter for priority, lifecycle state, fitness functions
- Validation gates alignment: load `.lev/validation-gates.yaml`, report gate status
- Skip blocked/deferred entities
- Sort by priority (P0 > P1 > P2 > P3 > P4)

### Phase 2: Execute (token spend)

- Run `runSdlcLoop()` on discovered entities
- Uses prompt-stack for composition (default: `sdlc-exec-validate`)
- Uses exec profiles for execution (default: `sdlc.flowmind.exec`)
- Respects `maxWorkers` for concurrent execution
- Emits LevEvents for observability

### Phase 3: Exit Check

After each tick, check exit conditions in order:

1. **fail_fast** — any failure this tick + `--fail-fast` flag
2. **circuit_breaker** — 3 consecutive ticks with zero successes
3. **max_ticks** — hit `--max-ticks` limit
4. **budget_exhausted** — cumulative tokens >= `--budget`
5. **until_met** — semantic condition satisfied
6. **all_done** — no entities remaining in queue

### Phase 4: Sleep

Sleep for `--interval` duration. Process stays alive, state preserved.
SIGINT/SIGTERM triggers graceful shutdown after current tick completes.

## Configuration

Config lives in `plugins/core-sdlc/config.yaml` under `autodev.heartbeat`:

```yaml
autodev:
  heartbeat:
    interval: 5m
    max_workers: 3
    max_entities: 5
    max_ticks: 0          # 0 = unlimited
    budget_tokens: 0       # 0 = unlimited
    stack: sdlc-exec-validate
    profile: sdlc.flowmind.exec
    circuit_breaker_threshold: 3
```

Overridable via CLI flags (flags win over config).

## Skill Routing

When invoked as `/autodev-lev`:

```bash
# 1. Parse args
INTERVAL="${1:-5m}"
FLAGS="${@:2}"

# 2. Delegate to lev loop autodev
lev loop autodev --interval=$INTERVAL $FLAGS
```

When the orchestrator (top-level agent) uses this skill:

1. **Start**: `lev loop autodev --interval=5m --max-ticks=10 --budget=100k`
2. **Monitor**: Watch stdout for tick summaries
3. **Interrupt**: SIGINT to stop gracefully
4. **Status**: `lev loop autodev status` for queue snapshot

## Integration with Prompt Stacks

Uses existing prompt-stack plugin for entity composition:

- `sdlc-exec-validate` — default: execute entity + validate gates
- `sdlc-deepen-plan` — deep plan decomposition
- `sdlc-hygiene` — hygiene scan
- Custom stacks via `--stack=<id>`

FlowMind will absorb this when it settles. Until then, prompt stacks are the steering layer.

## Exit Reasons

| Reason | Meaning |
|--------|---------|
| `all_done` | No entities remaining in queue |
| `no_work` | No entities found on first scan |
| `budget_exhausted` | Token budget consumed |
| `max_ticks` | Hit `--max-ticks` limit |
| `until_met` | Semantic exit condition satisfied |
| `fail_fast` | Stopped on first failure |
| `circuit_breaker` | 3 consecutive tick failures |
| `interrupted` | SIGINT/SIGTERM received |

## Example Session

```
$ lev loop autodev --interval=5m --max-ticks=10 --budget=50k

⚡ Tick 1 | 4 entities | interval 5.0m
  → Processed: 2 | Succeeded: 2 | Failed: 0 | 45200ms
  💤 Sleeping 5.0m...

⚡ Tick 2 | 2 entities | interval 5.0m | budget 12000/50000
  → Processed: 2 | Succeeded: 1 | Failed: 1 | 38100ms
  💤 Sleeping 5.0m...

⚡ Tick 3 | 1 entities | interval 5.0m | budget 28000/50000
  → Processed: 1 | Succeeded: 1 | Failed: 0 | 22300ms
  💤 Sleeping 5.0m...

⚡ Tick 4 | 0 entities | interval 5.0m | budget 35000/50000
  ✓ No entities remaining — all done.

─── Autodev Session Complete ───
  Ticks:      4
  Processed:  5
  Succeeded:  4
  Failed:     1
  Duration:   15.2m
  Exit:       all_done
```

## Anti-Patterns

- **Don't use CronCreate** — that's the old way. Heartbeat > cron for state continuity.
- **Don't set interval < 1m** — burns tokens. If you need faster, use `lev loop run` directly.
- **Don't skip --budget on long runs** — set a budget to prevent runaway spend.
- **Don't ignore circuit_breaker** — 3 failures = something structural is wrong. Investigate.

## Dependencies

- `@lev-os/orchestration/entities` — discoverPlans, loadLoopConfig
- `plugins/core-sdlc/src/workflows/sdlc-loop.ts` — runSdlcLoop
- `plugins/prompt-stack` — prompt composition (until FlowMind absorbs)
- `core/exec` — execution engine with semaphore + token tracking
