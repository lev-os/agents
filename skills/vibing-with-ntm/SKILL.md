---
name: vibing-with-ntm
description: >-
  Run NTM swarms with Agent Mail, Beads, and BV. Use when sending marching
  orders, tending parallel coding sessions, coordinating work claims and
  reservations, or running review loops for an NTM swarm.
---

<!-- TOC: Quick Start | Marching Orders | Swarm Loop | Operator Loop | Quality Loops | Coordination | Anti-Patterns | Troubleshooting | References | Related Skills -->

# Vibing With NTM

> **Core flow:** understand the repo -> pick work intelligently -> coordinate explicitly -> keep agents moving -> review relentlessly.

> **Core insight:** every agent is fungible, but the swarm only works when work selection, reservations, mail, and operator tending all stay aligned.

> **Human vs agent surfaces:**
> - Humans can use `ntm dashboard`, `ntm palette`, `ntm view`, and other interactive surfaces.
> - Agents should avoid interactive TUIs and prefer `--robot-*` for structured state.
> - Non-interactive commands such as `ntm send`, `ntm work triage`, `ntm mail inbox`, `ntm locks list`, and `ntm assign` are still valid operator tools.

> **Isolation model:**
> - Default: Agent Mail file reservations plus clear bead ownership.
> - Optional: `--worktrees` when the repo policy allows it and branch/worktree isolation is useful.
> - Repo-local `AGENTS.md` always wins if it prefers or forbids a specific coordination model.

## Quick Start

```bash
# 1. Prerequisites
ntm deps -v
br ready
bv --robot-triage

# 2. Start a manageable swarm
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# 3. Send marching orders
ntm send myproject --all "$(cat marching_orders.txt)"

# 4. Watch the swarm
ntm dashboard myproject
ntm --robot-snapshot
```

Scale up only when the operator loop is under control.

## Marching Orders

### Start-of-Session Prompt

Send a prompt like this to every agent at session start:

```text
Before doing anything else, read all of AGENTS.md and README.md and understand both. Then inspect the codebase enough to understand the project purpose, architecture, and the specific workflows that matter for the current repo.

Register with MCP Agent Mail if the repo expects it, introduce yourself to the other agents, and check for any existing messages or active coordination threads. If the repo uses Beads and BV, use them to find ready work and pick the next bead you can usefully advance now.

Do not get stuck in communication purgatory. Announce what you are taking on, reserve the relevant files or worktree scope, start doing real work, keep your bead status current, and reply promptly to important agent mail.

If the repo AGENTS.md has special rules for builds, tests, lints, or remote execution helpers such as rch, follow those rules exactly.
```

### Next-Bead Prompt

```text
Reread AGENTS.md so the repo rules are fresh. Use the available work graph tools to choose the highest-impact ready task you can complete now, claim it clearly, coordinate with the other agents, and start coding immediately instead of waiting for more instructions.
```

For the fuller prompt bank, including code-review, post-compaction, exploration, and
commit-only variants, read [PROMPTS.md](references/PROMPTS.md).

## The Swarm Loop

```text
1. Read repo instructions and current docs
2. Register / check Agent Mail if the repo uses it
3. Use bv --robot-triage or ntm work triage
4. Claim a bead and reserve files or a worktree scope
5. Implement
6. Self-review and fix obvious issues
7. Update bead status and coordination thread
8. Pick the next ready task
```

Key commands:

```bash
bv --robot-triage
bv --robot-next
ntm work triage
ntm work next
ntm assign myproject --auto --strategy=dependency
ntm mail inbox myproject
ntm locks list myproject --all-agents
```

## Operator Loop

For a human or orchestrator agent tending the swarm:

```text
1. Bootstrap with ntm --robot-snapshot
2. Tend with ntm --robot-attention or ntm --robot-wait
3. Inspect mail, locks, conflicts, and work graph drift
4. Send targeted prompts, assignments, or interrupts
5. Repeat
```

Useful operator commands:

```bash
ntm --robot-snapshot
ntm --robot-attention --since-cursor=42
ntm --robot-markdown --md-compact
ntm --robot-terse
ntm --robot-mail-check --mail-project=myproject --urgent-only

ntm mail inbox myproject
ntm locks list myproject --all-agents
ntm coordinator digest myproject
ntm coordinator conflicts myproject
ntm work triage --format=markdown
ntm assign myproject --auto --strategy=dependency
```

If the cursor expires, re-run `ntm --robot-snapshot` and continue.

## Quality Loops

### Self-Review Prompt

```text
Read over all of the code you just wrote and the existing code you modified with fresh eyes. Look for obvious bugs, regressions, unsafe assumptions, confusing logic, missing tests, and sloppy edge cases. Fix anything you find before you move on.
```

### Cross-Review Prompt

```text
Turn your attention to code written by the other agents and review it critically for bugs, regressions, reliability problems, security issues, and poor assumptions. Diagnose root causes, then fix what actually needs fixing.
```

### Exploration Prompt

```text
Randomly explore unfamiliar parts of the codebase, trace the real execution flow, understand how those pieces fit into the larger workflow, and then do a fresh-eyes pass for obvious bugs and bad assumptions. Fix what you can justify.
```

## Coordination Patterns

Default coordination stack:

```text
Beads decide what should happen.
Agent Mail records who is doing what.
File reservations or worktrees prevent collisions.
NTM gives the operator shared state, prompts, assignments, and recovery surfaces.
```

Helpful commands:

```bash
ntm mail send myproject --all "Report blockers and current file focus."
ntm locks renew myproject
ntm checkpoint save myproject -m "before risky merge"
ntm checkpoint list myproject
ntm worktrees list
ntm worktrees merge claude_1
```

## Swarm Anti-Patterns

### Communication Purgatory

Problem: agents keep talking about coordination without actually taking work.

Fix: require every agent to announce one concrete task, claim it, reserve scope, and start coding.

### File Thrashing

Problem: multiple agents edit the same file or same logical area without coordination.

Fix: reserve files up front. When repo policy allows, use worktrees for isolation-heavy efforts. When collisions happen, explicitly pick a canonical owner and redirect everyone else.

### Stale Bead State

Problem: work is done but bead status is wrong, or blocked work never gets retriaged.

Fix: periodically run `bv --robot-triage`, `ntm work triage`, and the relevant `br` status commands. Keep the graph honest.

### Broken Build Drift

Problem: one agent breaks the build and the rest keep coding blindly.

Fix: broadcast that the build is broken, stop duplicate speculative work, and route one or two agents to repair the baseline. Obey repo rules for offloading heavy verification commands.

### TUI Misuse

Problem: an agent tries to drive `ntm dashboard` or another interactive surface.

Fix: use `--robot-*` for structured state and keep the TUI for humans.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `spawn` cannot resolve the project | Use `ntm quick`, check `ntm config get projects_base`, or make the repo discoverable from that base |
| No clear next work item | Run `bv --robot-triage`, `bv --robot-next`, or `ntm work triage` |
| Coordination feels chaotic | Check Agent Mail inboxes, lock state, and coordinator digest/conflicts |
| Agents appear idle | Inspect `ntm --robot-snapshot`, `ntm --robot-attention`, and targeted pane output with `--robot-tail` |
| Cursor expired | Re-run `ntm --robot-snapshot` |
| Beads look inconsistent | Use normal `br`/`bv` recovery commands for the repo; do not mutate `.beads` internals from habit |

## Reference Index

| Topic | Reference |
| --- | --- |
| Marching orders, review prompts, exploration prompts, commit-only prompts | [PROMPTS.md](references/PROMPTS.md) |
| Spawn mixes, monitoring loop, reservations, anti-patterns, lifecycle, FAQ, validation | [PLAYBOOK.md](references/PLAYBOOK.md) |

## Related Skills

- `ntm` for the broader NTM command surface
- `agent-mail` for inboxes, contact handshakes, and reservations
- `br` for bead state updates
- `bv` for graph-aware prioritization
