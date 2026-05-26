---
name: sync
description: "Full-boundary checkpoint sync: commit, pull, merge, push across current + paired main checkouts and recursive submodules. Use for complete syncs, never partial/path-scoped."
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
  if branch_has_upstream:          # git rev-parse --abbrev-ref @{u} succeeds
    git pull --no-rebase
    git push
  # else: local-only branch — skip pull/push, work will land on main at MERGE step

MERGE_WORKTREE_INTO_MAIN(current_repo, main_repo):
  # cd into main_repo checkout, then:
  git merge <current_worktree_branch> --no-ff --no-edit
  # --no-rebase is NOT a valid merge flag; merge is merge-only by default
  # --no-ff preserves the merge commit so the worktree branch is visible in history
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
   - if the branch has an upstream (`git rev-parse --abbrev-ref @{u}` succeeds): `git pull --no-rebase && git push`
   - if no upstream (local-only branch): skip pull/push — the work lands on `main` at step 6
5. After the current checkout's submodules are synced, checkpoint the current checkout repo itself (same commit/pull/push rules).
6. If the current checkout is a non-main worktree:
   - locate the paired `main` checkout
   - recurse into **all dirty submodules** in that `main` checkout (apply step 4 to each)
   - checkpoint the `main` checkout repo itself (apply step 4)
   - merge the current worktree branch into `main`:
     - `git merge <worktree-branch> --no-ff --no-edit` (NOT `--no-rebase` — that flag is pull-only)
     - if conflicts appear, stop with a conflict-resolution brief; do not switch to PR workflow
   - `git pull --no-rebase` (only if main tracks an upstream, which it should)
   - `git push`
7. Finish by confirming the entire boundary is checkpointed:
   - current checkout clean or committed
   - paired `main` checkout clean or committed
   - all submodules in both checkouts handled in the required order: current-worktree subs → current worktree → main subs → main
   - worktree branch landed on `main` when applicable

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

- Stop with a conflict-resolution brief if a merge conflict appears.
- Stop and report if `git push` still fails after a normal `git pull --no-rebase`.
- Do not switch to a PR-based workflow.
