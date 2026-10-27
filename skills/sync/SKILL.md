---
name: sync
description: "Checkpoint and synchronize the current Git checkout and dirty submodules using Git directly. Semantically merge clear conflicts and ask only when intent is unresolved. Default scope is all dirty work; paths after -- narrow it. --handoff returns a copyable Markdown chat handoff. --main explicitly authorizes landing on main."
---

# Sync

Save the work, merge upstream without losing intent, and push the current branch.
The assistant runs Git directly. Do not require or create a custom sync shell
script, runner, lock service, or exit-code protocol.

## Scope and modes

| Request | Meaning |
| --- | --- |
| `sync` | Checkpoint all staged, unstaged and untracked non-ignored work in this checkout and its dirty submodules, including other sessions' work. Merge-pull and push each current branch to its upstream. |
| `sync -- <paths>` | Checkpoint only the named paths and necessary submodule pointers. Preserve other changes. If they prevent the merge, report that hold instead of expanding scope. |
| `sync --main` | Also checkpoint the paired main checkout, merge the current branch into main and push main. Plain sync on a feature branch leaves main alone. |
| `sync --from-main` | Also merge origin/main into the current branch, then push that branch. |
| `sync --handoff` | Perform the sync, then return the copyable chat handoff below. Combines with other modes. This is a skill flag, not a Git flag. |
| `sync --no-verify` | Skip push hooks only when the user explicitly requests it. It does not authorize skipping commit hooks or weakening repository rules. |

A checkpoint preserves drafts; it does not certify their review or release readiness.
Keep existing repository branch policies. Never rebase, force-push, stash, discard
changes, or invent an upstream to make a sync succeed.

## Work through the sync

1. **Inspect current state.** Check the repository, branch, upstream, dirty paths,
   submodules and any merge already in progress. Use `git status --short`,
   `git branch -vv`, `git remote -v` and submodule status as needed. Inspect
   incoming commits and apply relevant repository review requirements. Reuse a
   pending merge; do not start competing syncs.
2. **Checkpoint the authorized scope.** Work through dirty submodules before
   their parent. Write one truthful Lore message per repository. Stage explicit
   paths selected from the inspected status, including deletions. Default sync
   intentionally includes other sessions' drafts. Do not accidentally include
   their work when the user explicitly narrowed scope. In a pending merge,
   resolve it first and commit the complete merge.
3. **Merge and resolve.** Use merge pulls (`git pull --no-rebase`) or explicit
   fetch/merge commands when the mode or a pending merge calls for them.
   On conflict, follow [conflict handling](references/conflict-brief.md).
   Read the base and both sides, preserve the combined intent, make the smallest
   coherent resolution, validate it, and continue without reconfirmation.
4. **Check and push.** Run the affected checks and normal repository hooks.
   A hook message is evidence to inspect, not a semantic verdict to repeat
   blindly. Repair a clear defect or demonstrable false positive while retaining
   the intended invariant and regression coverage. Do not bypass a gate to get
   a green sync. Push to the verified upstream; push submodule commits before
   parent pointers. If the remote advanced again, merge the new changes and
   recheck the affected result.
5. **Verify and report.** Confirm the local/upstream commit relationship and
   remaining dirty or conflicted paths. Report what is pushed, local-only, or
   blocked. Include warnings such as detached or upstream-less submodules.
   If files changed during the sync, inspect and checkpoint them within the
   original scope, or state precisely what remains.

Use bounded command waits and preserve the process handle if a command outlives
one tool call. An observation timeout is not process failure. Investigate a
stalled hook or network operation before retrying; do not start a duplicate
operation. Do not kill another session's Git process or delete its lock.

## When to continue or ask

Continue after a clear semantic merge or a distinct, verified repair. There is
no shared one-retry quota and no requirement to ask merely because Git reported
a conflict. Keep moving while evidence establishes a safe next step.

Ask when competing intent cannot be reconciled, access is missing, or proceeding
requires a destructive choice or a policy change that is not already authorized.
Preserve the merge and explain the exact decision needed. Do not loop on an
unchanged failure. Do not choose a side solely by timestamp, rename a variable
to evade a check, or disable a hook.

## Lore messages

The subject says why the checkpoint exists. For shared drafts, say what the
checkpoint preserves. Include `Confidence:` and `Scope-risk:`; use `Tested:`
only for checks actually observed, and `Not-tested:` for material gaps.
No attribution line. Use a message file for multiline commit text.

For example:

```text
Preserve shared intake findings while integrating the current runtime

Confidence: medium
Scope-risk: broad
Tested: focused registry tests -> passed
Not-tested: unrelated drafts and whole-repository suites
```

## Handoff

With `--handoff`, finish the sync first. After success, or when a genuine
unresolved blocker prevents completion, give a short sync status followed by
**one fenced `markdown` block** the user can copy into another window or
machine. Do not return only a file link.

Write it from the conversation and verified state. Cover every substantive
work thread in the chat, including completed work needed to understand what
remains. Preserve the user's objective, scope, constraints, decisions,
corrections and relevant rejected approaches. Separate verified results from
worker claims, assumptions and proposals. Do not include credentials, tokens,
private reasoning, raw launch environments or a transcript dump.

Use these sections, omitting only empty ones:

- **Objective and scope:** outcome, boundaries and latest user steering.
- **Completed work and evidence:** changes, commits, checks and their limits,
  reports and artifacts.
- **Active and unfinished work:** each thread, its owner/session when known,
  exact stopping point and blockers.
- **Decisions and constraints:** accepted rulings, unresolved choices and
  relevant rejected approaches.
- **Checkout and sync state:** repository/remote, branch, checkpoint and merge
  commits, pushed versus local-only state, dirty/conflicted paths and failed hooks.
- **Resume here:** ordered concrete next actions and commands, including what
  must be verified first.
- **Machine-local context:** host, paths, last-verified process/session handles,
  local-only evidence and required transfers.

Prefer repository-relative source paths plus repository identity. Label absolute
paths, XDG evidence, local commits and running processes as machine-local.
A pushed source commit does not transfer runtime evidence or a live worker.
The next agent must verify its host, checkout and process identity before
resuming; it must not blindly reuse a handle or launch a duplicate worker.
Name missing context instead of inventing it. A handoff grants no new permissions.
