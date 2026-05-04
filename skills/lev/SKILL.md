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

## Meta-Prompting: How to Write lev exec Prompts

Agents are junior contractors. They don't know the codebase, the constraints, or what "done" means unless you spell it out. Every prompt must answer 5 questions:

### The 5 Questions

1. **What does PASSING look like?** Show a reference file/module that already works.
2. **What does FAILING look like?** Show the exact current error output.
3. **What specifically needs to change?** File, line, old value → new value.
4. **What must NOT change?** Scope boundary. "Touch ONLY these files."
5. **How do I verify?** Shell command that exits 0 on success.

### Template

```bash
lev exec "You are fixing {what} for {module} so it passes \`{verification command}\`.

## Context
{Which contract/spec governs this. Tell the agent to READ it first.}

## Current failures (from \`{command that shows failures}\`)
1. {constraint_id}: {exact error message}. Fix: {exact change}.
2. {constraint_id}: {exact error message}. Fix: {exact change}.

## Reference: what PASSING looks like
Read {path/to/passing/example} — it passes all constraints. Key differences:
- {field}: {passing value} vs {failing value}
- {field}: {what's present vs missing}

## What to do
1. Read {file to modify}
2. {Exact change 1 — file, line, old → new}
3. {Exact change 2}
4. Do NOT change anything else.

## DONE criteria
1. \`{verify command 1}\` shows PASS
2. \`{verify command 2}\` shows PASS
3. {artifact exists check}
4. No other files modified
5. git diff shows only expected changes" \
  --flow lev-ralph \
  --verifier="{shell command that exits 0 when done}"
```

### Bad vs Good

**Bad** (vague, no context, no verification):
```bash
lev exec "fix config.yaml schema compliance for core/exec" --flow lev-ralph
```

**Good** (specific, reference, verification):
```bash
lev exec "You are fixing config.yaml for core/exec so it passes lev validate.

## Current failures
1. namespace_is_lev: package.namespace is 'exec', must start with '@lev-os/'.
   Fix: change line 8 from namespace: exec to namespace: \"@lev-os/exec\"

## Reference
Read plugins/browser-cascade/config.yaml — namespace: \"@lev-os/browser-ops\"

## DONE criteria
1. lev validate core/exec | grep namespace_is_lev shows PASS
2. No other files modified" --flow lev-ralph --verifier="npx lev validate core/exec 2>&1 | grep -c ERROR | grep -q '^0$'"
```

### Orchestrator Loop Protocol

When running ralph in a loop (multiple items from a queue):

1. **Before firing:** Run the verifier for the PREVIOUS item. If it fails, don't move on — escalate.
2. **Gather context:** Run `lev validate {module}` to get exact current failures. Don't assume.
3. **Write the prompt:** Use the 5 questions template. Include a passing reference.
4. **Set the verifier:** `--verifier` must be a shell command that exits 0 ONLY when the work is correct.
5. **After completion:** Check git diff. If unexpected files changed, revert and re-prompt.
6. **Escalate when unsure:** If the agent loops 3+ times or touches unexpected files, STOP and ask the human.

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

### Token Budgets / Adapter Context Costs

**For batch CLI-only tasks, prefer claude-agent-sdk.** Each adapter loads a
different amount of baseline context before seeing your prompt. Choosing the
wrong adapter for CLI-only work wastes tokens (up to 14x measured overhead).

| Adapter          | Baseline Tokens | Loads IDE Context | Best For                          | Measured Total (smoke) |
| ---------------- | ---------------:| :---------------: | --------------------------------- | ----------------------:|
| cursor           |      60-100K    |        Yes        | File editing, IDE-context tasks   |               488,611  |
| codex            |        ~15K     |        No         | Multi-file, OpenAI models         |                52,100  |
| claude-agent-sdk |         ~5K     |        No         | CLI-only, batch loops, SDK work   |                34,398  |
| opencode         |         ~8K     |        No         | Open-source alternative           |                41,200  |
| gemini           |        ~10K     |        No         | Gemini models                     |                44,800  |

*Measurements from NaaC project dogfood (5 trial runs, 2026-04-05).
Report: `.lev/pm/reports/adapter-cost-baseline-20260430.md`*

**Runtime warning:** `lev exec` emits an `exec.cost_warning` event when a
CLI-only prompt routes to a high-IDE-context adapter. The warning suggests
using `--adapter=claude-agent-sdk` instead.

**Quick reference:**
- CLI-only work (git, deploy, read output) -> `--adapter=claude-agent-sdk`
- File editing / IDE context needed -> `--adapter=cursor`
- Batch loop with verifier -> `--adapter=claude-agent-sdk`
- When unsure -> `--adapter=claude-agent-sdk` (default is safe)

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
~/.local/share/lev/events.jsonl          # global LevEvent log (git, exec, daemon)
~/.local/share/lev/exec/traces/traces.jsonl  # per-execution traces
~/.local/state/lev/         # runtime state
~/.cache/lev/               # disposable cache
.lev/                       # project config + steering
.lev/agentfs/exec/events.jsonl  # graph exec events (node transitions, branches, completions)
.lev/pm/                    # plans, handoffs, decisions, specs
```

### Observability
```bash
# Recent graph exec events (ralph loop traces)
tail -20 .lev/agentfs/exec/events.jsonl | python3 -c "import json,sys; [print(f'{json.loads(l)[\"type\"]:30s} {json.loads(l)[\"data\"].get(\"nodeId\",\"\")}') for l in sys.stdin]"

# Global events (exec.started, exec.failed, git commits)
tail -10 ~/.local/share/lev/events.jsonl | python3 -c "import json,sys; [print(f'{json.loads(l)[\"type\"]:25s} {json.loads(l).get(\"data\",{}).get(\"executionId\",\"\")}') for l in sys.stdin]"

# Token usage from last exec
grep "token\|cost\|usage" .lev/agentfs/exec/events.jsonl | tail -5
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

---

## Parity Absorptions (Waves 4–6)

Patterns absorbed from external parity analysis. Source attribution: `.lev/pm/parity/`.

### Session Event Normalization (from Clawhip, Wave 4 — cw-01)

Canonical event name alias contract for Lev event producers that emit legacy `agent.*` shapes:

| Legacy | Canonical | Required fields |
|--------|-----------|-----------------|
| `agent.started` | `session.started` | source_agent, session_id |
| `agent.finished` | `session.completed` | duration, exit_code |
| `agent.failed` | `session.error` | error_type, message |

When receiving events from external adapters, normalize to `session.*` before routing through the event bus. Do not route `agent.*` events to downstream consumers — they expect normalized form.

Source: `workshop/analysis/clawhip/analysis.md`, `.lev/pm/parity/clawhip.yaml`

### ACP Editor Integration Registry (from Hermes, Wave 5 — hm-03)

Register Lev capabilities with editors (VS Code, Zed, JetBrains) using a JSON manifest:

```json
{
  "name": "lev",
  "version": "0.1.0",
  "capabilities": { "exec": true, "flow": true, "validate": true },
  "endpoints": {
    "exec": "lev exec {{task}}",
    "validate": "lev validate {{path}}"
  }
}
```

Manifest declares capabilities; editors discover and activate them via ACP. Lev's primary surface is terminal — this is a future integration reference for KinglyAssistant editor integration.

Source: `workshop/analysis/hermes-agent/analysis.md`, `.lev/pm/parity/hermes.yaml`

### Runtime Health Shell (from Hermes + OpenClaw, Waves 5–6 — hm-02 + oc-03)

Design reference for `lev doctor` / `lev repair` (not yet implemented — target: `lev-core` runtime ops).

What a full health check should cover:
- Provider connectivity (AI SDK key validity, rate limits)
- Tool availability (binaries present, executable)
- Terminal backend health (tmux session, shell integration)
- Memory plugin status (if configured)
- Config resolution (XDG paths, project overrides)

Returns actionable remediation steps, not just pass/fail. OpenClaw's repair surface adds migration support for in-place upgrades. Hermes does this per provider/terminal/tool/message-channel section — one obvious pass, clean output.

Distinct from `lev-align`, which validates spec/gate alignment (not runtime ops).

Source: `.lev/pm/parity/hermes.yaml`, `.lev/pm/parity/openclaw.yaml`
