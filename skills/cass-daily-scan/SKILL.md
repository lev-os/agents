---
name: cass-daily-scan
description: Workspace-first daily context scan for CASS outcomes, Lev insights, and coding-agent history patterns with actionable infra recommendations.
version: 0.1.4
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
    def signal:
      test("root cause|fixed |validated|tests? pass|result: done|confidence >=|smoking gun|verified gaps|highest roi|key blocker|blocked on|closed epic|priority issue|priority item|next action|recommended action"; "i");
    def noise:
      test("local-command-caveat|<task-notification>|^tasks_started:|^now launching|^launching |background agent|safe to nuke|^let me |^decisions: let me|i just launched"; "i");
    def lev_context:
      test("lev|leviathan|core/|plugins/|flowmind|poly|daemon|harness|beads|bd |pnpm|workspace link|typecheck|test|spec|handoff|gate|xdg|execfile|exec\\(|gh auth"; "i");

    . as $row
    | ($row.notes // "")
    | gsub("; "; " | ")
    | split(" | ")
    | map(select(
        signal
        and (noise | not)
        and (lev_context or (($row.notes // "") | lev_context))
      ))
    | .[]
    | [$row.recordedAt, ($row.outcome // ""), .]
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
- Apply a second-stage Leviathan relevance guard before promoting any clause into an infra conclusion. Confidence-bearing language without Lev context is weak evidence by default.
- Preserve `recordedAt` for every retained clause. Every synthesized claim in the report must point back to at least one `timestamp — clause snippet` citation.
- When raw artifacts and CASS disagree, prefer filtered `.cass/outcomes.jsonl` plus repo-root `.beads`.
- If the filtered high-signal set is sparse, say so explicitly instead of over-synthesizing.

### 4) Report contract
Always produce:
1. Top repeated pain points (max 10), each with at least one `timestamp — clause snippet` citation
2. Top repeated wins (max 10), each with at least one `timestamp — clause snippet` citation
3. Infra actions to run next (max 10, concrete command/file target)
4. Watchlist for next scan (max 10 terms)
5. Self-learning lessons derived only from the high-signal subset, with timestamped evidence snippets
6. Weak/noisy evidence disclosure section explaining what was retained but downgraded and why

## Fail-fast
- If neither `.cass/outcomes.jsonl` nor `.beads` exists and `cass` is unavailable, stop and return a missing-data error.
- If `.cass/outcomes.jsonl` exists but yields no high-signal clauses, report low-signal data instead of inventing conclusions.
- Do not silently pass on empty outputs.
