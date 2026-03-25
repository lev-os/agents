---
name: workflow-dotfiles-sync
description: "Deterministic source-first dotfiles sync workflow for chezmoi plus the local dotfiles control plane. Invoke with /workflow dotfiles-sync."
disable-model-invocation: true
allowed-tools: "Read, Write, Bash, Glob, Grep"
---

// Hint shown during autocomplete to indicate expected arguments. Example: [issue-number] or [filename] [format]

# Workflow: Dotfiles Sync

NEVER REBASE. ALWAYS MERGE.

## Trigger

Run this workflow when you need to:
- reconcile source-vs-target dotfile drift
- inspect pending chezmoi changes before apply
- promote intentional target changes back into source
- perform a safe source-first sync across machines

## Inputs

- Active dotfiles source repo at `$HOME/.local/share/chezmoi`
- Local target state under `$HOME`
- `dotfiles` helper available on PATH
- Optional handoff context in `.lev/pm/handoffs/`

## Steps

1. Run `dotfiles status` and `dotfiles sync`.
2. Classify results into:
   - source-only change
   - target-only intentional drift
   - same-area conflict
   - runtime noise
3. Resolve intent into source first:
   - source-only wins automatically
   - target-only intentional drift may be promoted back into source
   - same-area conflicts must pause and escalate
4. If source truth changed:
   - review `git -C ~/.local/share/chezmoi status --short`
   - commit
   - fetch, then merge remote changes
   - push
5. Only after source truth is settled:
   - run `chezmoi apply --force` on the chosen target set
6. Re-run `dotfiles sync` to verify the remaining drift is only expected runtime noise or clean.

## Team

| Role | Responsibility |
|------|---------------|
| dotfiles operator | Reads `dotfiles` planner output, classifies drift, and updates source truth |
| git reconciler | Commits, pulls, pushes the chezmoi source repo once intent is resolved |
| escalation agent | Opens AgentPing or human review when same-area conflicts exist |

## Outputs

- Updated chezmoi source repo state
- Updated target home state after apply
- Dry-run report at `~/.local/state/lev/dotfiles-sync-plan.latest.txt`
- Optional handoff updates documenting decisions and escalation points

## Validation

- `dotfiles sync` completes without mutating state and produces a current report
- Any committed source changes are pushed successfully
- `chezmoi apply --force` completes only after source truth is reconciled
- Same-area conflicts are escalated, never auto-merged
- Final `dotfiles status` reflects either clean state or explicitly accepted runtime noise
