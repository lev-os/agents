---
name: dotfiles-sync
description: Use when reconciling chezmoi local-vs-remote drift, reviewing pending machine-state changes, or performing safe remote-first dotfiles sync across machines.
---

# Workflow: Dotfiles Sync

NEVER REBASE. ALWAYS MERGE.

## Terminology

| Term | Meaning | Path |
|------|---------|------|
| **local** | The actual dotfiles on this machine (chezmoi target) | `$HOME/.<file>` |
| **remote** | The chezmoi source repo, git-tracked and pushed | `$HOME/.local/share/chezmoi` |

Always use "local" and "remote" when presenting drift reports. Never use chezmoi's internal "source/target" terminology in user-facing output.

## Trigger

Run this workflow when you need to:
- reconcile local-vs-remote dotfile drift
- inspect pending chezmoi changes before apply
- perform a safe remote-first sync across machines

## Inputs

- Chezmoi remote repo at `$HOME/.local/share/chezmoi`
- Local state under `$HOME`
- `dotfiles` helper available on PATH
- Optional handoff context in `.lev/pm/handoffs/`
- Workstream state at `.lev/pm/workstreams/dotfiles-sync/state/workstream.yaml`

## Steps

### Phase 1: Scan + Auto-Classify (immediate, no user interaction)

1. Run `dotfiles status` and `dotfiles sync` in parallel.
2. Run `dotfiles inspect chezmoi-diff` to get full diff content for every entry.
3. **Auto-classify every diff** into exactly one of these buckets. There is NO "manual review" bucket — every diff MUST be classified:
   - **remote-only** — exists in remote, not reflected locally. This does not automatically mean local intentionally removed it; it can also mean this machine never installed or does not use an optional file.
   - **local-drift** — local changed intentionally, remote is stale (MM where target newer)
   - **conflict** — both changed in the same area (MM where both recent, content diverges structurally)
   - **volatile** — runtime noise: `.tmp`, `installation_id`, cache files, lockfiles, IDE state (auto NO-GO, silent skip)
   - **script-rename** — chezmoi script naming convention change (R status). Inspect source to confirm equivalence, then classify as GO.
   - **intentional-removal** — file deleted locally on purpose (check memory + handoff history for prior decisions before asking user)

   Classification rules:
   - If the path is in `.chezmoiignore`, skip entirely — it should not appear in the report.
   - If the path matches known volatile patterns (`.tmp`, `installation_id`, `plugins/`, `cache/`, `*.log`, `*.lock`), classify as **volatile** automatically.
   - If the diff shows only whitespace, line-ending, or timestamp changes, classify as **volatile**.
   - If DA and source is newer, inspect intent before recommending apply. Local absence can mean "not installed on this machine", not "removed globally". Example: `.config/opencode/oh-my-opencode.json` existed only in remote while local `opencode.json` was newer; the correct action was to forget the remote-only optional file, not apply it locally.
   - If MM and target is newer, classify as **local-drift**.
   - If R (rename), read both old and new source files to determine if content is equivalent or changed.
   - If any parent source path starts with `exact_`, audit the parent ownership before classifying child diffs. Exact directories make local runtime files appear as delete/re-add drift. Example: `exact_dot_codex` caused Codex sqlite/native-host/runtime files to recur every sync; the correct action was to convert to non-exact `dot_codex/AGENTS.md`, not classify every runtime file independently.
   - Treat `run_onchange_*` scripts as executable side effects, not normal file updates. Inspect the script before GO. Example: the QMD installer was narrow; `install-deps` triggered broad Homebrew upgrades and was not safe as a QMD-scoped action.
   - Check `.lev/pm/handoffs/` and memory for prior decisions about specific paths before classifying ambiguous items.

4. For each classified diff, determine GO/NO-GO:
   - **remote-only** → GO only when the remote file is clearly desired on this machine; otherwise ESCALATE or intentional-removal/forget
   - **local-drift** → GO (re-add from local to remote)
   - **conflict** → ESCALATE (present both sides, require explicit user decision)
   - **volatile** → NO-GO (skip silently, recommend adding to `.chezmoiignore` if not already there)
   - **script-rename** → GO only after side-effect review confirms the script is safe for this sync scope
   - **intentional-removal** → GO (remove from remote via `chezmoi forget`)

### Phase 2: Enriched Report (first response to user)

Present a single enriched report. Use `/now` or a clear table format. The report MUST include:

```
DOTFILES SYNC REPORT — {hostname} — {date}

SUMMARY
  Total diffs: N
  Auto-resolved: N (GO)
  Escalations: N (need your call)
  Volatile skipped: N

ACTIONS (GO)
| # | Path | Direction | What changes | Classification |
|---|------|-----------|-------------|----------------|
| 1 | .claude/settings.json | local → remote | +3 hooks, -1 deprecated key | local-drift |
| 2 | .codex/AGENTS.md | local → remote | updated agent list | local-drift |
| ... | | | | |

ESCALATIONS (need decision)
| # | Path | Local intent | Remote intent | My recommendation |
|---|------|-----------|-------------|-------------------|
| (none if clean) | | | | |

VOLATILE (auto-skipped)
| Path | Reason |
|------|--------|
| .codex/.tmp | runtime temp dir |

CHEZMOIIGNORE CANDIDATES
| Path | Why |
|------|-----|
| (paths that keep showing up as volatile but aren't in .chezmoiignore yet) |
```

For escalations, explain intent, not just timestamps. Timestamp is evidence only. Example: local OpenCode config newer than remote means local may win, but a single remote package-name correction can still be merged intentionally.

End the report with a single go/no-go prompt:
- If zero escalations: "All N actions are auto-classified GO. Execute? [y/n]"
- If escalations exist: "N actions ready, M need your call. Resolve escalations first, then execute."

### Phase 3: Execute (only after user confirms)

5. Re-add local-drift files to remote: `chezmoi re-add <paths>`
6. Remove intentional-removal files from remote: `chezmoi forget --force <paths>`
7. Review `git -C ~/.local/share/chezmoi status --short`
8. Commit with descriptive message
9. Fetch, then merge remote changes (NEVER rebase)
10. Push
11. Only after remote is settled: `chezmoi apply --force` for remote-only and script-rename paths
12. Re-run `dotfiles sync` to verify clean state
13. Report final state

## Team

| Role | Responsibility |
|------|---------------|
| dotfiles operator | Scans, auto-classifies ALL diffs, builds enriched report |
| git reconciler | Commits, merges, pushes the chezmoi remote repo |
| escalation agent | Only activates when true conflicts exist (both sides changed structurally) |

## Outputs

- Enriched drift report (first response, always)
- Updated chezmoi remote repo state
- Updated local home state after apply
- Dry-run report at `~/.local/state/lev/dotfiles-sync-plan.latest.txt`
- Workstream state update at `.lev/pm/workstreams/dotfiles-sync/state/workstream.yaml`

## Validation

- Every diff is classified — zero items in any "manual review" or "unclassified" bucket
- `dotfiles sync` completes clean after execution
- Any committed remote changes are pushed successfully
- `chezmoi apply --force` runs only after remote is reconciled
- True conflicts (both sides changed structurally) are escalated, never auto-merged
- Final `dotfiles status` reflects either clean state or explicitly accepted volatile noise
- Volatile paths not in `.chezmoiignore` are flagged as candidates for addition
