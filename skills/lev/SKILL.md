---
name: lev
description: |
  Practical CLI reference for the Lev agent framework.
  Start with: lev exec --help
  Core primitives: exec (run agents), stack (prompt workflows), work (lifecycle)
skill_type: how-to
category: cli

sub_skills:
  - work
  - stack
  - autodev-loop
---

# lev — Agent Runtime CLI

Run `lev exec --help` for the full reference. This skill covers the essentials.

## Quick Start: lev-ralph (the default for real work)

**For most tasks, use `lev-ralph`.** It runs a two-model constraint engineering loop:
worker (cursor/sonnet) codes -> deterministic gate -> oracle (opus) reviews -> ship or iterate.

```bash
# The main thing — worker + oracle review loop
lev exec "implement user auth" --flow lev-ralph

# With a validation gate (tests must pass before review)
lev exec "fix login bug" --flow lev-ralph --until="bun test"

# Simple single-model loop (no review, just iterate)
lev exec "make all tests pass" --until="bun test"

# Single dispatch (one-shot, no loop)
lev exec "quick fix" --adapter=cursor --model=composer-2-fast
```

lev runs from source via bun. No build step. Changes to core/ are live immediately.

```
~/.local/share/pnpm/lev -> exec bun core/poly/bin/lev -> imports .ts directly
```

---

## exec

### Single dispatch
```bash
lev exec "implement user auth"
lev exec "fix the login bug" --model=opus
lev exec "quick fix" --adapter=cursor --model=composer-2-fast
```

### lev-ralph (two-model constraint loop) — USE THIS
```bash
lev exec "task" --flow lev-ralph                                    # cursor codes, opus reviews
lev exec "task" --flow lev-ralph --until="bun test"                 # with hard gate
lev exec "task" --flow lev-ralph --adapter=claude-agent-sdk         # override default adapter
```

Topology: `work -> hard_gate -> review -> [green: done | advice: work]`
- **work**: Fresh worker session. Codes ONE thing. Gets oracle advice from previous review.
- **hard_gate**: Runs validation command (shell exit code). Auto-pass if empty.
- **review**: Fresh oracle session. Reads DNA, validation gates, git diff. Says GREEN or gives ADVICE.
- Per-node adapter: work uses `cursor`/`composer-2-fast`, review uses `claude-agent-sdk`/`opus`.
- Knobs: `worker_adapter`, `worker_model`, `reviewer_adapter`, `reviewer_model`, `validation_command`, `max_iterations`.

### ralph (simple single-model loop)
```bash
lev exec "task" --flow ralph                      # single adapter, fresh context per iteration
lev exec "task" --flow ralph --until="bun test"   # with validation gate
```

### Iterative loop (--until, no flow needed)
```bash
lev exec "make all tests pass" --until="bun test"
lev exec "implement feature X" --until="bun test && bun run typecheck" --max-iterations=10
```

Fresh context each iteration. Agent reads filesystem, not prior output.
Prompt: task -> "Do the most important thing. Run tests. Stop." -> DONE/CONTINUE.

### Flow execution (advanced)
```bash
# Graph-format flows (nodes:{})
lev exec "task" --flow plugins/core-sdlc/flows/exec-validate.flow.yaml

# Session-format flows (steps:[])
lev exec "task" --flow plugins/core-sdlc/flows/spec-lifecycle.flow.yaml

# Dry-run (shows graph info without executing)
lev exec "task" --flow <file> --dry-run
```

25+ SDLC flows in `plugins/core-sdlc/flows/`. All loadable via `--flow`.

### Semantic ops in flows

Flow YAML nodes can use semantic ops that the runner dispatches:

| Op | What it does | Branch routing |
|----|-------------|----------------|
| `lev.exec` | Dispatch task through adapter (per-node adapter/model override) | Last-line keyword match against `branches:` |
| `lev.validate` | Run shell command, branch on exit code | `pass` (exit 0) / `fail` (exit != 0) |

```yaml
# lev.exec — agent dispatch with per-node adapter
work:
  op: lev.exec
  inputs:
    task: "{{knobs.task}}"
    adapter: cursor
    model: composer-2-fast
  output: work_result
  next: gate

# lev.validate — deterministic shell gate
gate:
  op: lev.validate
  inputs:
    command: "bun test"
  branches:
    pass: done
    fail: work
```

### Adapters (CLI runners)

| Adapter | Binary | Models | Best for |
|---------|--------|--------|----------|
| cursor | `agent` | composer-2-fast, composer-2, claude-4 | Fast implementation work |
| codex | `codex` | gpt-5.3, o1, o3, o4 | Complex multi-file, OpenAI models |
| claude-agent-sdk | (SDK) | opus, sonnet, haiku | Programmatic control, SDK features |
| pi | `pi` | any | Multi-provider routing |
| opencode | `opencode` | any | Open-source alternative |

```bash
lev exec "task" --adapter=cursor --model=composer-2-fast   # fastest
lev exec "task" --adapter=codex --model=codex              # OpenAI
lev exec "task" --adapter=claude-agent-sdk --model=sonnet  # Claude SDK
```

**Strategy:** lev-ralph for real work. composer-2-fast for routine. opus for review/oracle. haiku for triage.

### Key flags
```bash
--model=<model>        # opus, sonnet, haiku, composer-2-fast, codex, etc.
--adapter=<adapter>    # cursor, codex, claude-agent-sdk, pi, auto
--until=<condition>    # loop until shell command exits 0
--flow=<file>          # execute flow YAML (shorthand: --flow lev-ralph)
--max-iterations=<n>   # cap iterations (default 5)
--dry-run              # show plan without executing
--profile=<id>         # named execution profile
--host=<host>          # tmux://ralph (default), local, ssh://...
```

---

## Flows (FlowMind)

Flows are YAML files that define execution topology. Two formats:

### Graph format (nodes:{})
```yaml
name: my-flow
entry: work
knobs:
  task: { type: string, required: true }
nodes:
  work:
    op: lev.exec
    inputs: { task: "{{knobs.task}}", adapter: cursor }
    output: work_result
    next: gate
  gate:
    op: lev.validate
    inputs: { command: "bun test" }
    branches: { pass: done, fail: work }
    max_iterations: 5
    on_timeout: done
  done:
    terminal: true
```

Key concepts:
- **`op: lev.exec`** — dispatches to adapter with per-node adapter/model override
- **`op: lev.validate`** — runs shell command, branches on exit code (deterministic)
- **`branches:`** — route to different nodes based on result
- **`max_iterations` + `on_timeout`** — cap loops, redirect on timeout
- **`knobs:`** — flow-level parameters, CLI task auto-injected as `knobs.task`
- **`output:`** — stores result in flow vars for downstream nodes
- **`{{#if var}}...{{/if}}`** — conditional blocks in inputs

### Session format (steps:[])
```yaml
name: my-flow
steps:
  - id: gather
    op: exec
    command: "git log --oneline -10"
  - id: analyze
    description: "Analyze the recent changes"
  - id: report
    op: exec
    command: "echo 'done' > /tmp/report.txt"
```

Steps with `op: exec` + `command:` run as shell. Others dispatch to LLM adapter.

### Key flows
- `lev-ralph.flow.yaml` — **USE THIS** — worker + oracle review, per-node adapters
- `ralph.flow.yaml` — simple single-model loop
- `exec-validate.flow.yaml` — implement -> validate -> emit/escalate
- `plan-to-beads.flow.yaml` — plan -> issues with 3-pass anti-laziness review
- `hygiene.flow.yaml` — drift scan -> alignment check -> proposals

```bash
ls plugins/core-sdlc/flows/*.yaml   # 25+ flows
```

---

## stack (prompt workflows)

Prompt-stack provides structured multi-step workflows. Being replaced by flows.

```bash
bun plugins/prompt-stack/src/cli.ts list          # see all stacks
bun plugins/prompt-stack/src/cli.ts show <id>     # inspect a stack
bun plugins/prompt-stack/src/cli.ts init --stack <id>  # start session
```

Use `/stack list` for the full dashboard.

---

## work (SDLC lifecycle)

Use `/work` skill for lifecycle management (plans, specs, handoffs, beads).

---

## Config

```yaml
# .lev/config.yaml (project level)
logging:
  display_level: info    # what shows in CLI (info/warn/debug)

exec:
  adapterVariants: {}    # custom adapter configs
```

Resolution: system (~/.config/lev/) -> project (.lev/) -> module -> env vars.
Config > env > defaults. Don't rely on env vars — LLMs forget them.

### Key paths
```
~/.config/lev/              # user config
~/.local/share/lev/         # persistent data (traces, events, indexes)
~/.local/state/lev/         # runtime state
~/.cache/lev/               # disposable cache
.lev/                       # project config + steering
.lev/pm/                    # plans, handoffs, decisions, specs
```

---

## Source map

| Domain | Path | What |
|--------|------|------|
| CLI binary | `core/poly/bin/lev` | Entry point (bun shim) |
| CLI dispatch | `core/poly/src/surfaces/cli/` | Discovery, aliases |
| Exec engine | `core/harness/src/` | Adapter registry, runner, loop |
| Orchestration | `core/orchestration/src/` | Iterative runner, execution contract |
| FlowMind | `core/flowmind/src/` | Flow compilation, session manager |
| SDLC plugin | `plugins/core-sdlc/` | Flows, autodev, work lifecycle |
| Prompt stack | `plugins/prompt-stack/` | Structured prompt workflows |
| Domain types | `core/domain/` | Shared contracts |
| Event bus | `core/event-bus/` | Inter-module events |
| Logger | `core/logger/` | Pino-based, reads .lev/config.yaml |
| Config | `core/config/` | Resolver chain, XDG paths |

---

## DNA (system constraints)

Read `dna/graph.yaml` before touching core. Key constraints:
- **C1 Finitude:** Every operation must be bounded. No infinite loops.
- **C2 Non-commutation:** Order matters. Append-only. Immutable receipts.
- Validation gates: `.lev/validation-gates.yaml`

Execution primitives: loop, eval, effect, session, receipt, edge, execution_contract.
