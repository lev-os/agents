---
name: sync
description: "Checkpoint sync: one bounded script run commits, merge-pulls and pushes the current checkout and its dirty submodules, with a Lore commit message per repository. Landing on main needs explicit --main."
---

# Sync

Git here is a checkpoint mechanism, not a pull-request workflow. A sync is **total** inside its boundary and **bounded** in time.

`scripts/sync.sh` does every git operation of a sync in one run. The run stops itself when its **budget** is spent (300 seconds). Your part is the commit messages and the report. A whole sync is two snippets.

## Steps

1. **Plan.** Run this from anywhere in the checkout. Add the mode flag from [Modes](#modes) when the user asked for one.

   ```bash
   ~/.agents/skills/sync/scripts/sync.sh plan
   ```

   It only reads. It lists each dirty repository, submodules first and the checkout last, with its changed paths. Then it prints the run snippet with one empty message block per repository.
   Done when: you hold a key for every dirty repository, or the output says nothing is dirty.

2. **Write the messages and run.** Fill every block of the printed snippet with a [Lore message](#lore-messages). Run the snippet as one command, with a tool timeout of 310000 ms so the run ends inside the call.

   ```bash
   ~/.agents/skills/sync/scripts/sync.sh run <<'MSG'
   == services/telemetry-ingest
   Decode the J1939 engine hours so the fleet page stops showing zero

   Confidence: high
   Scope-risk: narrow
   Tested: pnpm test decode -> 14 passed
   == .
   Point the product at the new decoder and keep today's handoff with it

   Confidence: medium
   Scope-risk: narrow
   Not-tested: no check was run on the handoff text
   MSG
   ```

   Done when: the output ends with `sync: done` or `sync: STOPPED (exit N)`.

3. **Report.** On `sync: done`, give the user the state lines the script printed: each commit, each push, each warning. On `STOPPED`, apply the row for that exit code in [Exit codes](#exit-codes).
   Done when: the user knows what is pushed, what is committed but not pushed, and what is still dirty.

**One retry.** After a `STOPPED` run, fix the cause the table names and run the snippet again once. If the second run also stops, report it to the user and end the sync.

Every git write of a sync goes through the script. The sync needs no other git command from you, before or after.

## Modes

The boundary is fixed by the mode, and inside it everything dirty is taken. The user saying "sync" has already answered "which files?": all of them.

| The user says | Flag on `plan` and `run` | What the run covers |
|---|---|---|
| "sync" | none | The current checkout and its dirty submodules, recursively. The current branch goes to its upstream. A branch with no upstream stays local. |
| "sync --main", "land this on main" | `--main` | The above, then the paired `main` checkout and its dirty submodules, then the current branch merged into `main` with `--no-ff`, then `main` pushed. |
| "main > current", "merge main into this branch" | `--from-main` | The above, then `origin/main` merged into the current branch, then the branch pushed. |
| "skip the push check", "--no-verify" | `--no-verify` | Push hooks are skipped. Use it only on the user's word in this conversation. |

Plain "sync" on a feature branch leaves `main` alone. All pulls are merges (`git pull --no-rebase`); the script never rebases, never force-pushes and never opens a pull request.

## Lore messages

Each repository gets one commit that holds everything dirty in it. Sync is the one place a whole-repository commit is right, because the user asked for a total checkpoint.

```
<intent line: why these changes exist, not what changed>

<optional body: context, or the second intent when the checkpoint holds two>

Confidence: <low|medium|high>
Scope-risk: <narrow|moderate|broad>
Tested: <command run this session> -> <result seen>
Not-tested: <the real gap>
```

- The intent line says why. Take it from the changed paths in the plan output and from what this session did. For work that another session left, say what it keeps safe ("Keep the insights runs so the next session starts from them").
- `Confidence:` and `Scope-risk:` go on every message. The script refuses a message without them, before it changes anything.
- `Tested:` quotes only a command run in this session, with its result. With no check run, write an honest `Not-tested:` line.
- Other true trailers are welcome: `Constraint:`, `Rejected: <alternative> | <reason>`, `Reversibility:`, `Directive:`, `Related:`.
- A message carries no attribution line.
- A repository with no block gets a fallback message that says so. Write the block.

The full protocol is in `~/lev/.agents/skills/lev-lore-commit/SKILL.md`. Read it when a trailer is unclear.

## Bounds

| Bound | Default | Change it with |
|---|---|---|
| Time for a whole `run` | 300 s | `SYNC_BUDGET=600` before the command, on the user's word |
| Time for a `plan` | 60 s | `SYNC_BUDGET` |
| New untracked files in one repository | 100 MB | `SYNC_MAX_ADD_MB` |
| Syncs in one checkout at a time | 1, held by `sync.lock` in the git directory | none |
| Merge-pull and push attempts per repository | 2 | none |

When the budget is spent, the script prints the step it was in and the state so far, then stops git and every hook that git started.

## Exit codes

| Exit | Meaning | What you do |
|---|---|---|
| 0 | Done | Report. |
| 2 | Merge conflict. The merge is left in place. | Write the brief in [references/conflict-brief.md](references/conflict-brief.md) and stop. |
| 3 | Untracked files over the limit. Nothing was committed in that repository. | Show the user the largest paths the script printed. Ask: ignore them, or raise the limit. |
| 4 | A commit, pull or push failed with no conflict | Read the git or hook message above the `STOPPED` line. Fix the cause, then use the one retry. |
| 64 | A message or an argument is wrong. Nothing was changed. | Fix the block the script names and run again. This run does not use up the one retry. |
| 75 | Another sync holds this checkout | See [Troubleshooting](#troubleshooting). |
| 124 | Budget spent | See [Troubleshooting](#troubleshooting). |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Exit 75, or two sessions synced one checkout at the same time and the commits look tangled | A dual sync: two sessions, for example a forked chat, ran sync together | Stop it with the command the script printed (`kill -TERM -- -<pid>`), then sync again. The new run takes everything that is dirty, merge-pulls and pushes. |
| Exit 124 during a push | A push hook hangs or runs a long check | The commit is safe in the local branch. Sync again. If it stops at the same step, tell the user which hook; raise `SYNC_BUDGET` only on the user's word. |
| The chat shows a sync with no result for many minutes | The session stopped, not the sync. A run cannot outlive its budget. | Run `plan`. It shows what is still dirty and whether a lock is left. |
| Exit 4 and the hook names a wrong Node or pnpm version | The shell found an old Node first | Put the project's Node first in `PATH` in the same snippet, then sync again. |
| Exit 4 at `git add`, and `index.lock` exists | A stopped git left its lock | Check that no git runs (`pgrep -fl git`). Remove `.git/index.lock`. Sync again. |
| `plan` notes a sync lock, and no sync runs | A stopped run left it | Nothing. The next run takes over a lock whose process is gone. |
| "N paths became dirty during the run" | Another session wrote during the sync | Sync again to take them. |
| "WARNING detached HEAD" on a submodule | The submodule is not on a branch, so its commit was not pushed | Check out its branch in the submodule and sync again, so the parent points at a pushed commit. |
