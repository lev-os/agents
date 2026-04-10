---
name: sync
description: Full checkpoint sync only. Use when Codex must commit, pull, merge, and push all dirty work in the current checkout, its paired main checkout, and their recursive submodules. Never use this for partial/path-scoped syncs.
---

# Sync

Git here is a checkpointing mechanism, not a standard feature-branch or pull-request workflow.

## Core rule

**Sync is never scoped.**

It is always a **full checkpoint** of:
- the checkout you are currently in,
- the paired `main` checkout if you are in a non-main worktree,
- and the dirty submodules inside both.

Do **not** ask whether to sync only some files, only one repo, or only “your” changes.
If the user says `sync`, the default meaning is:

> checkpoint everything dirty in the current checkout and the paired main checkout, recursively through submodules, then land it on `main`.

This is **not** “all worktrees on disk”.
It is the **current checkout + its paired main checkout**.
Within that boundary, it is always total, never partial.

## Rules

- Do not optimize for PRs.
- Do not use `git rebase`.
- Use merge-based pulls only: `git pull --no-rebase`.
- Never do a path-scoped or feature-scoped sync.
- If you are in a worktree, the goal is to get the work onto `main`.
- Sync dirty submodules first, then sync the parent repo.
- If the paired `main` checkout is dirty, commit/pull/push there too.
- Use simple commit messages based on the changed files or area.
- Prefer durable checkpoints over perfect commit curation.
- Do not leave dirty submodules behind in either the current checkout or the paired `main` checkout.

## Recursive Model

Treat sync as a recursive checkpoint over a fixed boundary:
- boundary repo A = current checkout
- boundary repo B = paired `main` checkout, if A is a non-main worktree

There is no “selected subset” mode.

```text
SYNC_BOUNDARY(current_repo):
  SYNC_REPO(current_repo)

  if repo_is_worktree(current_repo) and branch(current_repo) != "main":
    main_repo = resolve_main_checkout(current_repo)
    SYNC_REPO(main_repo)
    MERGE_WORKTREE_INTO_MAIN(current_repo, main_repo)
    PUSH(main_repo)

SYNC_REPO(repo):
  children = dirty_submodules(repo)  # recursive

  for child in children:
    SYNC_REPO(child)

  CHECKPOINT(repo)

CHECKPOINT(repo):
  if repo has changes:
    git add .
    git commit -m "<simple message based on changed files>"
  git pull --no-rebase
  git push
```

## Workflow

1. Inspect the current state.
   - `git status --short`
   - `git branch --show-current`
   - `git worktree list`
   - `git submodule status --recursive`
2. Determine the fixed sync boundary:
   - current checkout always included
   - paired `main` checkout also included if current checkout is a non-main worktree
3. Recurse into **all dirty submodules** inside the current checkout first.
4. In each dirty repo/submodule:
   - `git add .`
   - `git commit -m "<simple message based on changed files>"` if there is anything to commit
   - `git pull --no-rebase`
   - `git push`
5. After submodules are synced, checkpoint the current checkout repo itself.
6. If the current checkout is a non-main worktree:
   - locate the paired `main` checkout
   - recurse into **all dirty submodules** in that `main` checkout
   - checkpoint the `main` checkout repo itself
   - merge the current worktree branch into `main`
   - `git pull --no-rebase`
   - `git push`
7. Finish by confirming the entire boundary is checkpointed:
   - current checkout clean or committed
   - paired `main` checkout clean or committed
   - dirty submodules in both handled
   - worktree branch landed on `main` when applicable

## Commit Message Guidance

Keep it short and obvious.

- `intent: callsign strict mode`
- `data: enrichment checkpoint`
- `sync: checkpoint current work`

## Repo-Specific Notes

- If `main` has submodules, recurse first. The parent repo sync is not complete until dirty child repos are checkpointed.
- In repos like this one, `data/` is a submodule. Commit and push there before updating the parent repo pointer.
- If multiple agents touched different areas, the job is to checkpoint **all dirty repos in boundary**, not to preserve a per-feature narrative.
- Do not stop at “my spike files are synced”. That is the old wrong behavior. Sync means **everything dirty in boundary is checkpointed**.

## What not to ask

Do **not** ask:
- “Do you want a scoped sync or full sync?”
- “Should I only sync my changes?”
- “Should I leave unrelated dirty files alone?”

If the user invoked `sync`, the answer is already:
- full checkpoint,
- current checkout + paired `main`,
- recursive submodules,
- merge onto `main` when in a worktree.

## Stop Conditions

- Stop and report if a merge conflict appears.
- Stop and report if `git push` still fails after a normal `git pull --no-rebase`.
- Do not switch to a PR-based workflow.
