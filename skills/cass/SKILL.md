---
name: cass
description: |
  [WHAT] Search wrapper around the external `cass` CLI for coding-agent session history.
  [HOW] Uses `cass` in machine-readable mode (`--json` or `--robot`) for health checks, search, expansion, and session inspection across Claude, Codex, Cursor, Gemini, Aider, ChatGPT, and related tools.
  [WHEN] Use when you need prior session evidence, cross-agent search, handoff recovery, or raw conversational history behind a memory/playbook claim.
  [WHY] Gives Lev a strong episodic-memory tool without importing another search runtime into core ownership paths.

  Triggers: "cass", "session search", "agent history", "search prior sessions", "cross-agent search", "hindsight", "session evidence"
---

# CASS

`cass` is raw session search. Use it when you need evidence, not distilled guidance.

## Prerequisites

```bash
command -v cass
```

If missing, stop and tell the user:

```bash
brew install dicklesworthstone/tap/cass
```

## Golden Rules

1. Never run bare `cass` in an agent context. It opens the TUI.
2. Always use `--json` or `--robot` for machine-readable output.
3. Run a cheap health check before deep searches.
4. Treat `cass` as a tool boundary; do not merge its runtime assumptions into Lev core.

## Fast Path

```bash
cass health --json || cass index --full --json
cass search "authentication timeout" --robot --limit 5 --fields minimal
```

## Core Commands

### Health and readiness

```bash
cass health --json
cass status --json
cass capabilities --json
cass introspect --json
```

### Search

```bash
cass search "query" --robot --limit 5
cass search "query" --robot --fields minimal
cass search "query" --robot --workspace /path/to/project
cass search "query" --robot --days 30
```

### Inspect specific results

```bash
cass view /path/to/session.jsonl -n 42 --json
cass expand /path/to/session.jsonl -n 42 -C 5 --json
```

### Documentation for agents

```bash
cass robot-docs guide
cass robot-docs commands
cass robot-docs schemas
```

## Recommended Workflow

### 1. Check health

```bash
cass health --json
```

If unhealthy:

```bash
cass index --full --json
```

### 2. Search narrowly

Prefer scoped searches:

```bash
cass search "database migration" --robot --workspace /abs/path --limit 5
```

### 3. Expand only the promising hits

Use `view` or `expand` after search rather than dumping large result sets.

## When To Use `cass` vs `cm`

Use `cass` for:
- raw session evidence
- exact historical wording
- line-level follow-up after search
- cross-agent recovery during handoffs

Use `cm` for:
- distilled rules
- anti-pattern recall
- pre-task memory hydration

## Anti-Patterns

- Running `cass` without `--json` or `--robot`
- Pulling large unscoped result sets into context
- Treating search hits as validated guidance without inspection
- Using `cass` as the project task tracker

## Minimal Extraction Pattern

```markdown
## CASS Evidence
- Query:
- Hits used:
- Key lines or summaries:
- Why they matter:
```

Keep this evidence summary in the current Lev artifact, not in ad hoc notes.
