---
name: sync
description: "Checkpoint sync for the current checkout and recursive dirty submodules. In feature branches, paired main checkout and feature->main landing require explicit --main."
---

# Sync

Git here is a checkpointing mechanism, not a standard feature-branch or pull-request workflow.

## Core rule

**Sync is never path-scoped, but its branch boundary depends on the requested mode.**

Default `sync` is a **full checkpoint of the current checkout only**:
- the checkout you are currently in,
- and the dirty submodules inside that checkout, recursively.

If the current checkout is a feature/non-main branch, default `sync` must **not**
touch the paired `main` checkout and must **not** merge the feature branch into
`main`.

The paired `main` checkout is included only when the user explicitly passes
`--main` or says to land/merge the current branch onto `main`.

Do **not** ask whether to sync only some files, only one repo, or only “your” changes.
If the user says `sync`, the default meaning is:

> checkpoint everything dirty in the current checkout, recursively through its
> dirty submodules, then pull/push the current branch if it has an upstream.

This is **not** “all worktrees on disk” and it is **not** “land this branch on
main”.
Within the selected boundary, it is always total, never partial.

Directional rule:
- `sync` on a feature branch: current branch only.
- `sync --main`: current branch + paired main checkout + feature branch landed
  onto main.
- `main > current`, `merge main into this branch`, or equivalent: merge main
  into the current branch, never the current branch into main.

## Rules

- Do not optimize for PRs.
- Do not use `git rebase`.
- Use merge-based pulls only: `git pull --no-rebase`.
- Never do a path-scoped sync inside the selected boundary. The branch boundary
  is selected by mode: default current checkout, optional `--main`, or explicit
  main-into-current.
- If you are in a feature/non-main worktree, the default goal is to checkpoint
  and push that feature branch, not to land it on `main`.
- Do not merge a feature branch into `main` unless the user explicitly passes
  `--main` or explicitly asks to land/merge the branch onto `main`.
- Merging `main` into the current feature branch is allowed only when the user
  asks for that direction; do not infer it from plain `sync`.
- Sync dirty submodules first, then sync the parent repo.
- If `--main` is not present, do not inspect, checkpoint, pull, push, or merge
  the paired `main` checkout as part of sync.
- If `--main` is present and the paired `main` checkout is dirty, commit/pull/push
  there too before landing the feature branch.
- Use simple commit messages based on the changed files or area.
- Prefer durable checkpoints over perfect commit curation.
- Do not leave dirty submodules behind in the selected boundary. The paired
  `main` checkout is part of that boundary only with explicit `--main`.

## Recursive Model

Treat sync as a recursive checkpoint over a fixed boundary:
- default boundary repo A = current checkout
- optional boundary repo B = paired `main` checkout, only with explicit `--main`

There is no “selected subset” mode.

```text
SYNC_BOUNDARY(current_repo):
  SYNC_REPO(current_repo)

  if mode_has_explicit_main_flag and repo_is_worktree(current_repo) and branch(current_repo) != "main":
    main_repo = resolve_main_checkout(current_repo)
    SYNC_REPO(main_repo)
    MERGE_WORKTREE_INTO_MAIN(current_repo, main_repo)
    PUSH(main_repo)

  if mode_is_main_into_current:
    MERGE_MAIN_INTO_CURRENT(current_repo)

SYNC_REPO(repo):
  children = dirty_submodules(repo)  # recursive

  for child in children:
    SYNC_REPO(child)

  CHECKPOINT(repo)

CHECKPOINT(repo):
  if repo has changes:
    git add .
    git commit -m "<simple message based on changed files>"
  if branch_has_upstream:          # git rev-parse --abbrev-ref @{u} succeeds
    git pull --no-rebase
    git push
  # else: local-only branch — skip pull/push unless explicit --main landing is requested

MERGE_WORKTREE_INTO_MAIN(current_repo, main_repo):
  # Only legal with explicit --main / explicit feature->main landing request.
  # cd into main_repo checkout, then:
  git merge <current_worktree_branch> --no-ff --no-edit
  # --no-rebase is NOT a valid merge flag; merge is merge-only by default
  # --no-ff preserves the merge commit so the worktree branch is visible in history

MERGE_MAIN_INTO_CURRENT(current_repo):
  # Only legal when the user explicitly asks for main > current.
  # Stay in the current checkout.
  git fetch origin main
  git merge origin/main --no-ff --no-edit
  # If conflicts appear, stop with a conflict-resolution brief.
```

## Workflow

1. Inspect the current state.
   - `git status --short`
   - `git branch --show-current`
   - `git worktree list`
   - `git submodule status --recursive`
2. Determine the fixed sync boundary:
   - current checkout always included
   - paired `main` checkout included only if `--main` or explicit feature->main
     landing was requested
   - main-into-current merge is a separate explicit direction, not the default
3. Recurse into **all dirty submodules** inside the current checkout first.
4. In each dirty repo/submodule:
   - `git add .`
   - `git commit -m "<simple message based on changed files>"` if there is anything to commit
   - if the branch has an upstream (`git rev-parse --abbrev-ref @{u}` succeeds): `git pull --no-rebase && git push`
   - if no upstream (local-only branch): skip pull/push unless explicit `--main`
     landing was requested
5. After the current checkout's submodules are synced, checkpoint the current checkout repo itself (same commit/pull/push rules).
6. If `--main` was explicitly requested and the current checkout is a non-main worktree:
   - locate the paired `main` checkout
   - recurse into **all dirty submodules** in that `main` checkout (apply step 4 to each)
   - checkpoint the `main` checkout repo itself (apply step 4)
   - merge the current worktree branch into `main`:
     - `git merge <worktree-branch> --no-ff --no-edit` (NOT `--no-rebase` — that flag is pull-only)
     - if conflicts appear, stop with a conflict-resolution brief; do not switch to PR workflow
   - `git pull --no-rebase` (only if main tracks an upstream, which it should)
   - `git push`
7. If the user explicitly requested main > current:
   - stay in the current checkout
   - `git fetch origin main`
   - `git merge origin/main --no-ff --no-edit`
   - if conflicts appear, stop with a conflict-resolution brief
   - run the requested/current verification after resolving
8. Finish by confirming the selected boundary is checkpointed:
   - current checkout clean or committed
   - current checkout dirty submodules handled before the parent
   - paired `main` checkout touched only when explicitly requested
   - worktree branch landed on `main` only when `--main` / explicit feature->main
     landing was requested

## Commit Message Guidance

Keep it short and obvious.

- `intent: callsign strict mode`
- `data: enrichment checkpoint`
- `sync: checkpoint current work`

## Conflict-Resolution Brief

When a merge or pull conflict appears, do not only list conflicted files.
Before stopping, inspect enough context to give the user actionable resolution
paths.

Required conflict inspection:
- `git status --short`
- `git diff --name-only --diff-filter=U`
- `git ls-files -u <conflicted-paths>`
- `git diff --cc -- <conflicted-files>`
- for submodules: `git -C <submodule> log --oneline --decorate --graph --all --max-count=20`
- for code conflicts: inspect both sides with `git show :2:<path>` and `git show :3:<path>` when useful

Required conflict brief:
```yaml
sync_conflict:
  state: blocked
  conflicted_paths:
    - <path>
  inferred_intents:
    ours: <what the local side was trying to preserve>
    theirs: <what the incoming side was trying to preserve>
  solution_paths:
    - option: <merge both | take ours | take theirs | advance submodule pointer | manual synthesis>
      blast_radius: <low|medium|high>
      why: <one sentence>
      risks:
        - <specific risk>
      validation:
        - <command that would prove this option>
  recommended_strategy: <one option plus why>
  next_command_sequence:
    - <minimal non-destructive commands to apply the recommendation>
```

Guidance:
- Infer intent from both sides before recommending a resolution.
- Prefer a synthesis that preserves both sides' intended behavior when the
  combined behavior is coherent and testable.
- Treat submodule conflicts as pointer-selection problems backed by submodule
  commit ancestry. State whether one pointer contains the other, whether a
  merge commit exists, or whether a new submodule merge is required.
- Include blast radius in practical terms: affected module, tests likely to
  break, deployment/runtime surfaces touched, and whether generated artifacts or
  submodule pointers are involved.
- If the correct strategy is clear and low-risk, recommend it explicitly; do not
  hide behind "resolve conflicts manually."
- Do not run the resolution automatically unless the user asked sync to continue
  and the resolution is low-risk, non-destructive, and fully justified by the
  brief.

## Repo-Specific Notes

- If `--main` is requested and `main` has submodules, recurse first. The parent
  repo sync is not complete until dirty child repos are checkpointed.
- In repos like this one, `data/` is a submodule. Commit and push there before updating the parent repo pointer.
- If multiple agents touched different areas, the job is to checkpoint **all dirty repos in boundary**, not to preserve a per-feature narrative.
- Do not stop at “my spike files are synced”. That is the old wrong behavior. Sync means **everything dirty in boundary is checkpointed**.
- On `Sunny-PC` or another feature branch, default boundary means the feature
  branch and its submodules only. Do not merge `Sunny-PC` into `main` unless
  `--main` is explicitly present.

## What not to ask

Do **not** ask:
- “Do you want a scoped sync or full sync?”
- “Should I only sync my changes?”
- “Should I leave unrelated dirty files alone?”

If the user invoked `sync`, the answer is already:
- full checkpoint,
- current checkout + dirty recursive submodules,
- recursive submodules,
- no feature->main merge unless `--main` or explicit landing request is present.

## Stop Conditions

- Stop with a conflict-resolution brief if a merge conflict appears.
- Stop and report if `git push` still fails after a normal `git pull --no-rebase`.
- Do not switch to a PR-based workflow.
