#!/usr/bin/env bash
# Regression checks for whole-checkout sync and explicit optional path scope.
#
#   bash sync-own-paths.sh [scenario|all] [sync.sh]
#
# Builds throwaway repositories under /tmp, never in a real checkout, and drives
# sync.sh through them (default: the installed ~/.agents/skills/sync/scripts/sync.sh).
# Session A and session B work in one working tree with one index, as the sessions
# in a shared checkout do. Exit 0 when every chosen scenario passes, 1 when one
# fails, 64 on bad usage.
set -u

SCENARIOS="named-path untracked-unnamed unstaged-unnamed edit-and-delete submodule-pointer
default-all-states dot-takes-everything total-when-nothing-staged plan-read-only
bad-path-stops diverged-pull-stops default-staged-submodule index-only-state unresolved-merge resolved-merge syntax"
SCENARIOS=$(echo $SCENARIOS)
WANT=${1:-all}; [ "$WANT" = all ] && WANT=$SCENARIOS
SYNC=${2:-$HOME/.agents/skills/sync/scripts/sync.sh}
[ -f "$SYNC" ] || { echo "no sync.sh at $SYNC" >&2; exit 64; }
for s in $WANT; do
  case " $SCENARIOS " in *" $s "*) ;; *) echo "unknown scenario: $s (known: $SCENARIOS)" >&2; exit 64 ;; esac
done

# Never touch a real repository: drop the git variables a hook or a runner may set,
# and read neither the user's nor the system's git config.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR GIT_PREFIX
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 \
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid \
  GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
ROOT=$(mktemp -d /tmp/sync-own-paths.XXXXXX) || exit 1
trap 'rm -rf "$ROOT"' EXIT

fail() { echo "    $*"; BAD=1; }
eq() { [ "$2" = "$3" ] || fail "$1: got '$(printf %s "$2" | tr '\n' '|')', want '$(printf %s "$3" | tr '\n' '|')'"; }
files() { git diff-tree --no-commit-id -r --name-only "${1:-HEAD}" | tr '\n' ' ' | sed 's/ $//'; }
changes() { git diff-tree --no-commit-id -r --name-status "${1:-HEAD}" | tr '\t\n' ': ' | sed 's/ $//'; }

# A repository with one pushed commit (seed.txt, old.txt, gone.txt) and a bare remote.
world() {
  W="$ROOT/$CUR"; mkdir -p "$W"
  git init -q --bare -b main "$W/remote.git"
  git init -q -b main "$W/work"
  cd "$W/work" || exit 1
  printf 'seed\n' > seed.txt; printf 'old\n' > old.txt; printf 'gone\n' > gone.txt
  git add seed.txt old.txt gone.txt && git commit -q -m seed
  git remote add origin "$W/remote.git" && git push -q -u origin main
}
# world, plus a submodule sub (s.txt, t.txt) with its own bare remote.
world_with_sub() {
  world
  git init -q --bare -b main "$W/sub.git"
  git init -q -b main "$W/subseed"
  ( cd "$W/subseed" && printf 's\n' > s.txt && printf 't\n' > t.txt && git add s.txt t.txt &&
    git commit -q -m seed && git remote add origin "$W/sub.git" && git push -q -u origin main )
  git -c protocol.file.allow=always submodule add -q "$W/sub.git" sub
  git commit -q -m "add sub" && git push -q
}
# Run sync.sh in the scratch repository, with one message block for each key.
sync_run() { # keys, then the sync.sh arguments
  local keys="$1" k; shift
  case "$PWD" in "$ROOT"/*) ;; *) echo "refusing to run sync.sh outside $ROOT" >&2; exit 1 ;; esac
  for k in $keys; do
    printf '== %s\nKeep the work of session B\n\nConfidence: high\nScope-risk: narrow\nNot-tested: fixture commit\n' "$k"
  done | "$SYNC" "$@" > "$W/out" 2>&1
}
snapshot() {
  git rev-parse HEAD; git ls-files --stage; git status --porcelain
  git -C sub ls-files --stage; git -C sub status --porcelain; git -C "$W/remote.git" rev-parse main
}

s_named_path() { # A stages a.txt; B's sync names only b.txt
  world
  printf 'a\n' > a.txt; git add a.txt
  printf 'b\n' > b.txt
  sync_run . run -- b.txt; eq "exit" "$?" 0
  eq "B's commit" "$(files)" "b.txt"
  eq "staged after the run" "$(git diff --cached --name-only)" "a.txt"
  eq "pushed" "$(git -C "$W/remote.git" rev-parse main)" "$(git rev-parse HEAD)"
}
s_untracked_unnamed() { # an untracked file that nobody named is not added
  world
  printf 'c\n' > c.txt
  printf 'b\n' > b.txt
  sync_run . run -- b.txt; eq "exit" "$?" 0
  eq "B's commit" "$(files)" "b.txt"
  eq "c.txt after the run" "$(git status --porcelain -- c.txt)" "?? c.txt"
}
s_unstaged_unnamed() { # A's unstaged edit is not taken
  world
  printf 'edit by A\n' >> seed.txt
  printf 'b\n' > b.txt
  sync_run . run -- b.txt; eq "exit" "$?" 0
  eq "B's commit" "$(files)" "b.txt"
  eq "seed.txt after the run" "$(git status --porcelain -- seed.txt)" " M seed.txt"
}
s_edit_and_delete() { # B names an edited file and a deleted one; A's staged a.txt stays out
  world
  printf 'a\n' > a.txt; git add a.txt
  printf 'new\n' >> old.txt; rm gone.txt
  sync_run . run -- old.txt gone.txt; eq "exit" "$?" 0
  eq "B's commit" "$(changes)" "D:gone.txt M:old.txt"
  eq "dirty after the run" "$(git status --porcelain)" "A  a.txt"
}
s_submodule_pointer() { # B names a file inside a submodule; the parent takes only the new pointer
  world_with_sub
  printf 'a\n' > a.txt; git add a.txt
  printf 'edit by A\n' >> sub/t.txt
  printf 'edit by B\n' >> sub/s.txt
  sync_run "sub ." run -- sub/s.txt; eq "exit" "$?" 0
  eq "submodule commit" "$(cd sub && files)" "s.txt"
  eq "submodule dirty after the run" "$(git -C sub status --porcelain)" " M t.txt"
  eq "submodule pushed" "$(git -C "$W/sub.git" rev-parse main)" "$(git -C sub rev-parse HEAD)"
  eq "parent commit" "$(files)" "sub"
  eq "pointer" "$(git rev-parse HEAD:sub)" "$(git -C sub rev-parse HEAD)"
  eq "parent staged after the run" "$(git diff --cached --name-only)" "a.txt"
  eq "parent pushed" "$(git -C "$W/remote.git" rev-parse main)" "$(git rev-parse HEAD)"
}
s_default_all_states() {
  world
  printf 'staged\n' > a.txt; git add a.txt
  printf 'unstaged\n' >> old.txt; rm gone.txt; printf 'untracked\n' > b.txt
  sync_run . run; eq "exit" "$?" 0
  eq "saved files" "$(changes)" "A:a.txt A:b.txt D:gone.txt M:old.txt"
  eq "clean checkout" "$(git status --porcelain)" ""
  eq "remote" "$(git -C "$W/remote.git" rev-parse main)" "$(git rev-parse HEAD)"
}
s_dot_takes_everything() { # -- . names everything, staged paths included
  world
  printf 'a\n' > a.txt; git add a.txt
  printf 'b\n' > b.txt; printf 'edit\n' >> seed.txt
  sync_run . run -- .; eq "exit" "$?" 0
  eq "the commit" "$(files)" "a.txt b.txt seed.txt"
  eq "dirty after the run" "$(git status --porcelain)" ""
}
s_total_when_nothing_staged() { # with nothing staged, a run that names no paths takes everything, submodules too
  world_with_sub
  printf 'edit\n' >> seed.txt; rm gone.txt; printf 'n\n' > new.txt
  printf 'edit\n' >> sub/s.txt
  sync_run "sub ." run; eq "exit" "$?" 0
  eq "submodule commit" "$(cd sub && files)" "s.txt"
  eq "parent commit" "$(changes)" "D:gone.txt A:new.txt M:seed.txt M:sub"
  eq "dirty after the run" "$(git status --porcelain)" ""
  eq "pushed" "$(git -C "$W/remote.git" rev-parse main)" "$(git rev-parse HEAD)"
}
s_plan_read_only() { # plan writes nothing, and its snippet carries the named paths
  local before
  world_with_sub
  printf 'a\n' > a.txt; git add a.txt
  printf 'b\n' > b.txt; printf 'edit\n' >> seed.txt; printf 'edit\n' >> sub/s.txt
  before=$(snapshot)
  "$SYNC" plan -- b.txt sub/s.txt > "$W/out" 2>&1; eq "exit of plan with paths" "$?" 0
  grep -q -- ' run -- b.txt sub/s.txt <<' "$W/out" || fail "the snippet does not carry -- b.txt sub/s.txt"
  grep -qx '== sub' "$W/out" && grep -qx '== \.' "$W/out" || fail "the snippet lacks a block for sub or for ."
  "$SYNC" plan > "$W/out2" 2>&1; eq "exit of plan with no paths" "$?" 0
  grep -q ' run <<' "$W/out2" || fail "ordinary plan does not emit an ordinary total run"
  if grep -q 'staged already\|run -- <path>' "$W/out2"; then fail "ordinary plan still refuses staged work"; fi
  eq "state after both plans" "$(snapshot)" "$before"
  [ ! -d .git/sync.lock ] || fail "a sync lock is left"
}
s_bad_path_stops() { # a named path that names nothing, or lies outside, stops the run before any change
  local before
  world
  printf 'b\n' > b.txt
  before=$(git rev-parse HEAD)
  sync_run . run -- b.txt nope.txt; eq "exit for nope.txt" "$?" 64
  grep -q 'nope\.txt' "$W/out" || fail "the stop does not name nope.txt"
  sync_run . run -- /etc/hosts; eq "exit for /etc/hosts" "$?" 64
  grep -q '/etc/hosts' "$W/out" || fail "the stop does not name /etc/hosts"
  eq "HEAD" "$(git rev-parse HEAD)" "$before"
  eq "b.txt after the runs" "$(git status --porcelain -- b.txt)" "?? b.txt"
}
s_diverged_pull_stops() { # origin moved and A's path is staged: git refuses the merge, B's commit stays local
  world
  git clone -q "$W/remote.git" "$W/other"
  ( cd "$W/other" && printf 'x\n' > x.txt && git add x.txt && git commit -q -m other && git push -q )
  printf 'a\n' > a.txt; git add a.txt
  printf 'b\n' > b.txt
  sync_run . run -- b.txt; eq "exit" "$?" 4
  eq "B's commit" "$(files)" "b.txt"
  eq "staged after the run" "$(git diff --cached --name-only)" "a.txt"
  grep -q 'git refuses a merge while any path is staged' "$W/out" || fail "the stop does not say that a staged path blocks the merge"
}
s_default_staged_submodule() {
  world_with_sub
  printf 'parent staged\n' > a.txt; git add a.txt
  printf 'sub staged\n' > sub/new.txt; git -C sub add new.txt
  printf 'sub unstaged\n' >> sub/s.txt; printf 'sub untracked\n' > sub/u.txt
  sync_run "sub ." run; eq "exit" "$?" 0
  eq "sub files" "$(cd sub && files)" "new.txt s.txt u.txt"
  eq "sub clean" "$(git -C sub status --porcelain)" ""
  eq "parent clean" "$(git status --porcelain)" ""
  eq "pointer" "$(git rev-parse HEAD:sub)" "$(git -C sub rev-parse HEAD)"
  eq "sub pushed" "$(git -C "$W/sub.git" rev-parse main)" "$(git -C sub rev-parse HEAD)"
}
s_index_only_state() {
  world
  printf 'staged intermediate\n' > seed.txt; git add seed.txt
  printf 'seed\n' > seed.txt
  sync_run . run; eq "exit" "$?" 0
  eq "current content" "$(git show HEAD:seed.txt)" seed
  eq "clean checkout" "$(git status --porcelain)" ""
}
merge_fixture() {
  world
  git checkout -q -b other; printf 'other\n' > seed.txt; git add seed.txt; git commit -qm other
  git checkout -q main; printf 'main\n' > seed.txt; git add seed.txt; git commit -qm main
  git merge other > "$W/merge-out" 2>&1
}
s_unresolved_merge() {
  merge_fixture
  local before; before=$(git rev-parse HEAD)
  sync_run . run; eq "exit" "$?" 2
  eq "HEAD unchanged" "$(git rev-parse HEAD)" "$before"
  eq "conflict retained" "$(git diff --name-only --diff-filter=U)" seed.txt
}
s_resolved_merge() {
  merge_fixture
  printf 'resolved\n' > seed.txt; git add seed.txt
  sync_run . run; eq "exit" "$?" 0
  eq "merge parents" "$(git rev-list --parents -n 1 HEAD | wc -w | tr -d ' ')" 3
  eq "clean checkout" "$(git status --porcelain)" ""
  eq "remote" "$(git -C "$W/remote.git" rev-parse main)" "$(git rev-parse HEAD)"
}
s_syntax() { bash -n "$SYNC" || fail "bash -n failed"; }

FAILED=0
for s in $WANT; do
  CUR=$s
  echo "-- $s"
  if ( BAD=0; "s_$(printf %s "$s" | tr - _)"; exit "$BAD" ); then echo "PASS $s"
  else
    echo "FAIL $s"; FAILED=1
    [ -s "$ROOT/$s/out" ] && sed 's/^/    | /' "$ROOT/$s/out"
  fi
done
exit "$FAILED"
