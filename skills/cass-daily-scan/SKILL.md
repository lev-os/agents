---
name: cass-daily-scan
description: Workspace-first daily context scan for CASS outcomes, Lev insights, and coding-agent history patterns with actionable infra recommendations.
version: 0.1.3
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

### 1) Extract high-signal outcome clauses from CASS
```bash
if [ -f .cass/outcomes.jsonl ]; then
  jq -r '
    . as $row
    | ($row.notes // "")
    | gsub("; "; " | ")
    | split(" | ")
    | map(select(
        test("root cause|fixed |validated|tests? pass|result: done|confidence >=|smoking gun|verified gaps|highest roi|key blocker|blocked on|closed epic|priority issue|priority item|next action|recommended action"; "i")
        and (test("local-command-caveat|<task-notification>|^tasks_started:|^now launching|^launching |background agent|safe to nuke|^let me |^decisions: let me|i just launched"; "i") | not)
      ))
    | select(length > 0)
    | [$row.recordedAt, $row.outcome, join(" | ")]
    | @tsv
  ' .cass/outcomes.jsonl | head -n 300
fi
```

### 2) Use live Beads state as the second primary source
```bash
if [ -d .beads ]; then
  bd list --json
  bd ready --json
fi
```

### 3) Use CASS search only as supplemental lookup
```bash
if command -v cass >/dev/null 2>&1; then
  cass search "lev OR workflow OR agent OR mcp OR frankensearch OR fastmcp OR platform OR destructive_command_guard OR levterm"     --workspace "$PWD"     --yesterday     --source local     --json     --limit 120     --max-content-length 260
fi
```

Notes:
- Repo-root `.beads` is the live Beads store.
- Do not treat `.lev/store/.beads` as live evidence unless it contains actual issue data.
- CASS outcomes should be high-signal only for analysis: ignore launch chatter, task-notification noise, `local-command-caveat`, background-agent narration, and generic `Let me...` planning text.
- When raw artifacts and CASS disagree, prefer filtered `.cass/outcomes.jsonl` plus repo-root `.beads`.
- If the filtered high-signal set is sparse, say so explicitly instead of over-synthesizing.

### 4) Report contract
Always produce:
1. Top repeated pain points (max 10)
2. Top repeated wins (max 10)
3. Infra actions to run next (max 10, concrete command/file target)
4. Watchlist for next scan (max 10 terms)
5. Self-learning lessons derived only from the high-signal subset

## Fail-fast
- If neither `.cass/outcomes.jsonl` nor `.beads` exists and `cass` is unavailable, stop and return a missing-data error.
- If `.cass/outcomes.jsonl` exists but yields no high-signal clauses, report low-signal data instead of inventing conclusions.
- Do not silently pass on empty outputs.
