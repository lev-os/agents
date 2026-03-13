---
name: cass-daily-scan
description: Workspace-first daily context scan for CASS outcomes, Lev insights, and coding-agent history patterns with actionable infra recommendations.
version: 0.1.0
skill_type: workflow
category: memory-analysis
---

# CASS Daily Scan

## Purpose
Run one pass over local session/outcome memory and produce a compact, actionable infra report.

## Inputs
- Workspace root (default: current directory)
- Query terms (default bundle):
  - `lev`
  - `workflow`
  - `agent`
  - `mcp`
  - `frankensearch`
  - `fastmcp`
  - `platform`
  - `destructive_command_guard`
  - `levterm`

## Output
- Markdown report at `.lev/pm/reports/cass-daily-<YYYYMMDD-HHMM>.md`

## Execution (workspace-first)

### 1) Use CASS if available
```bash
if command -v cass >/dev/null 2>&1; then
  cass search "lev OR workflow OR agent OR mcp OR frankensearch OR fastmcp OR levterm" \
    --workspace "$PWD" --json --limit 80 --max-content-length 260
fi
```

### 2) Fallback when CASS CLI is unavailable
```bash
rg -n "lev|workflow|agent|mcp|frankensearch|fastmcp|destructive_command_guard|levterm" \
  .cass/outcomes.jsonl .beads 2>/dev/null | head -n 300
```

### 3) Report contract
Always produce:
1. Top repeated pain points (max 10)
2. Top repeated wins (max 10)
3. Infra actions to run next (max 10, concrete command/file target)
4. Watchlist for next scan (max 10 terms)

## Fail-fast
- If neither `.cass/outcomes.jsonl` nor `.beads` exists, stop and return a missing-data error.
- Do not silently pass on empty outputs.
