---
name: cass
description: "cass CLI session search across coding agents with JSON or robot output. Use when user needs session evidence, cross-agent search, handoff recovery, or transcript-backed claims."
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
cass status --json
# When `.index.status` is "stale":
/Users/jean-patricksmith/.local/bin/cass-maintain
tail -n 1 /Users/jean-patricksmith/.local/state/cass/auto-index-telemetry.jsonl
cass status --json
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

### 1. Check index freshness

```bash
cass status --json
```

If `.index.status` is `stale`, run the bounded incremental wrapper and wait for
it to exit before searching:

```bash
/Users/jean-patricksmith/.local/bin/cass-maintain
tail -n 1 /Users/jean-patricksmith/.local/state/cass/auto-index-telemetry.jsonl
cass status --json
```

Treat `success`, `idle`, and `overlap_skipped` as handled outcomes. For
`hard_timeout` or `failed`, stop and report the last telemetry row and log tail;
do not widen the operation. After a handled refresh, rerun the user's original
search exactly—the status check alone is not freshness proof.

Never use bare `cass index`, `--full`, `--force`, or `--force-rebuild` to make a
search fresh. If the index is `missing`, stop and request an explicit bootstrap
decision; routine search freshness is owned only by `cass-maintain`.

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
