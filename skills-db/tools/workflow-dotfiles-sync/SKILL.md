---
name: workflow-dotfiles-sync
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
- promote intentional local changes back into remote
- perform a safe remote-first sync across machines

## Inputs

- Chezmoi remote repo at `$HOME/.local/share/chezmoi`
- Local state under `$HOME`
- `dotfiles` helper available on PATH
- Optional handoff context in `.lev/pm/handoffs/`

## Steps

1. Run `dotfiles status` and `dotfiles sync`.
2. Classify results into:
   - remote-only change (exists in remote, not reflected locally)
   - local-only intentional drift (local changed, remote is stale)
   - same-area conflict (both changed)
   - runtime noise (volatile files, timestamps, caches)
3. Resolve intent into remote first:
   - remote-only wins automatically UNLESS the local removal was intentional (ask)
   - local-only intentional drift gets promoted to remote via `chezmoi re-add`
   - same-area conflicts must pause and escalate
4. If remote changed:
   - review `git -C ~/.local/share/chezmoi status --short`
   - commit
   - fetch, then merge remote changes
   - push
5. Only after remote is settled:
   - run `chezmoi apply --force` on the chosen local set
6. Re-run `dotfiles sync` to verify the remaining drift is only expected runtime noise or clean.

## Team

| Role | Responsibility |
|------|---------------|
| dotfiles operator | Reads `dotfiles` planner output, classifies drift, and updates remote |
| git reconciler | Commits, pulls, pushes the chezmoi remote repo once intent is resolved |
| escalation agent | Opens AgentPing or human review when same-area conflicts exist |

## Outputs

- Updated chezmoi remote repo state
- Updated local home state after apply
- Dry-run report at `~/.local/state/lev/dotfiles-sync-plan.latest.txt`
- Optional handoff updates documenting decisions and escalation points

## Validation

- `dotfiles sync` completes without mutating state and produces a current report
- Any committed remote changes are pushed successfully
- `chezmoi apply --force` completes only after remote is reconciled
- Same-area conflicts are escalated, never auto-merged
- Final `dotfiles status` reflects either clean state or explicitly accepted runtime noise
