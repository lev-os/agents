#!/usr/bin/env bash
# sync.sh: one bounded checkpoint of the current checkout and its dirty submodules.
#
#   sync.sh plan [--main] [-- <path>...]                            read-only: list dirty repos and print the run snippet
#   sync.sh run  [--main|--from-main] [--no-verify] [-- <path>...]  commit, merge-pull, push; messages on stdin
#
# Paths after -- name what this session wrote, absolute or relative to the current
# directory. Each commit then takes only those paths, plus the pointer of a submodule the
# run committed in; every other path stays as it was, staged or not. A named directory or
# submodule names everything in it, and -- . names everything. With no paths, a run takes
# every staged, unstaged and untracked non-ignored change, including other sessions' work.
#
# Messages on stdin, one block per repo key (keys come from `plan`):
#   == <key>
#   <intent line>
#
#   Confidence: <low|medium|high>
#   Scope-risk: <narrow|moderate|broad>
#
# Bounds: SYNC_BUDGET seconds for the whole run (default 300), SYNC_MAX_ADD_MB of new
# untracked files per repo (default 100), one sync per checkout (lock in the git dir).
# Exit: 0 done · 2 merge conflict · 3 untracked files over the limit · 4 pull or push failed
#       64 bad message, usage or path
#       75 another sync holds the lock · 124 budget spent
set -u

MODE="${1:-}"; [ $# -gt 0 ] && shift
# Lead a process group, so the watchdog can stop git and every hook it started.
if [ -z "${SYNC_PGL:-}" ]; then
  export SYNC_PGL=1
  exec perl -e 'setpgrp(0,0); exec @ARGV or die "exec: $!"' "$0" "$MODE" "$@"
fi

MAIN=0; FROM_MAIN=0; NOVERIFY=""; FLAGS=""; NAMED=0
while [ $# -gt 0 ]; do
  case "$1" in
    --main) MAIN=1 ;; --from-main) FROM_MAIN=1 ;; --no-verify) NOVERIFY="--no-verify" ;;
    --) shift; NAMED=1; break ;;
    *) echo "sync: unknown argument $1" >&2; exit 64 ;;
  esac
  FLAGS="$FLAGS $1"; shift
done
# "$@" now holds the paths named after --.
[ "$NAMED" = 0 ] || [ $# -gt 0 ] || { echo "sync: name at least one path after --" >&2; exit 64; }
case "$MODE" in plan) BUDGET="${SYNC_BUDGET:-60}" ;; run) BUDGET="${SYNC_BUDGET:-300}" ;;
  *) sed -n '2,25p' "$0" >&2; exit 64 ;; esac
MAX_ADD_MB="${SYNC_MAX_ADD_MB:-100}"
export GIT_TERMINAL_PROMPT=0 GIT_MERGE_AUTOEDIT=no
[ "$MODE" = plan ] && export GIT_OPTIONAL_LOCKS=0   # plan only reads: no index refresh, no lock

PREFIX=$(git rev-parse --show-prefix 2>/dev/null)
TOP=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "sync: not in a git checkout" >&2; exit 64; }
LTOP=${PWD%/}; [ -n "$PREFIX" ] && LTOP=${LTOP%/"${PREFIX%/}"}
cd "$TOP" || exit 64
LOCK="$(git rev-parse --absolute-git-dir)/sync.lock"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/sync.XXXXXX"); mkdir "$TMP/msg"; : > "$TMP/report"
START=$(date +%s); HELD=0; WD=""

step() { echo "$*" > "$TMP/step"; echo "[+$(( $(date +%s) - START ))s] $*"; }
note() { echo "  $*" >> "$TMP/report"; }
unlock() { rm -f "$LOCK/pid"; rmdir "$LOCK" 2>/dev/null; }
finish() { # runs on every exit
  [ -n "$WD" ] && kill -TERM "$WD" 2>/dev/null
  [ "$HELD" = 1 ] && unlock
  rm -r "$TMP" 2>/dev/null
}
die() { # code, message
  echo "sync: STOPPED (exit $1): $2" >&2
  [ -s "$TMP/report" ] && { echo "state so far:" >&2; cat "$TMP/report" >&2; }
  exit "$1"
}
trap finish EXIT
trap 'exit 124' TERM

# Watchdog: when the budget is spent, report, then stop the whole process group.
(
  sleep "$BUDGET" & SL=$!
  trap 'kill "$SL" 2>/dev/null; exit 0' TERM
  wait "$SL"; trap '' TERM
  echo "sync: STOPPED (exit 124): budget ${BUDGET}s spent during: $(cat "$TMP/step" 2>/dev/null)" >&2
  [ -s "$TMP/report" ] && { echo "state so far:" >&2; cat "$TMP/report" >&2; }
  [ "$(cat "$LOCK/pid" 2>/dev/null)" = "$$" ] && unlock
  kill -TERM -- "-$$" 2>/dev/null; sleep 2; kill -KILL -- "-$$" 2>/dev/null
) & WD=$!

keyfile() { echo "$TMP/msg/$(printf %s "$1" | cksum | cut -d' ' -f1)"; }

# Every repo of one checkout, deepest submodule first, the checkout itself last.
all_repos() { # checkout dir, key prefix -> lines "key<TAB>dir"
  local top="$1" pre="$2" p
  git -C "$top" submodule foreach --recursive --quiet 'echo "$displaypath"' 2>/dev/null | sed '1!G;h;$!d' |
    while IFS= read -r p; do printf '%s\t%s\n' "$pre$p" "$top/$p"; done
  printf '%s\t%s\n' "$pre." "$top"
}
dirty_repos() { # checkout dir, key prefix -> the dirty ones among all_repos
  local key dir
  all_repos "$1" "$2" | while IFS=$'\t' read -r key dir; do
    [ -n "$(git -C "$dir" status --porcelain 2>/dev/null)" ] && printf '%s\t%s\n' "$key" "$dir"
  done
  return 0
}
main_checkout() {
  git worktree list --porcelain | awk '/^worktree /{w=substr($0,10)} $0=="branch refs/heads/main"{print w; exit}'
}
main_dirty() { # with --main, the dirty repos of the paired main checkout as well
  local m; [ "$MAIN" = 1 ] || return 0
  m=$(main_checkout); [ -n "$m" ] && [ "$m" != "$TOP" ] && dirty_repos "$m" "main:"
  return 0
}
# New untracked files of a NUL-separated list that would enter git itself.
# Git LFS paths are left out: LFS is where large files belong.
untracked_plain() {
  git check-attr --stdin -z filter < "$1" |
    perl -0ne 'chomp; push @r, $_; if (@r == 3) { print "$r[0]\0" unless $r[2] eq "lfs"; @r = () }'
}
untracked_kb() { untracked_plain "$1" | xargs -0 -r du -k 2>/dev/null | awk '{s+=$1} END{print s+0}'; }
largest_untracked() {
  untracked_plain "$1" | xargs -0 -r du -k 2>/dev/null |
    awk -F'\t' '{n=split($2,p,"/"); k=(n>2)?p[1]"/"p[2]:(n>1?p[1]:$2); s[k]+=$1}
                END{for(k in s) printf "%8.1f MB  %s\n", s[k]/1024, k}' | sort -rn | head -5
}

# Named paths become pathspecs, NUL-separated, in a spec file for each repo key.
owner_of() { # path from the top -> path of the submodule that holds it, "" for the checkout itself
  local s best=""
  while IFS= read -r s; do case "$1" in "$s"/*) [ ${#s} -gt ${#best} ] && best=$s ;; esac; done < "$TMP/subs"
  printf '%s' "$best"
}
spec_add() { # repo path from the top ("" for the checkout), path inside that repo ("." for all of it)
  local s=":(literal)$2"; [ "$2" = . ] && s=.
  printf '%s\0' "$s" >> "$(keyfile "${1:-.}").spec"
}
add_pointer() { # repo key -> when it is a submodule of this checkout, its parent takes its pointer
  local parent
  case "$1" in .|main:*) return 0 ;; esac
  parent=$(owner_of "$1")
  spec_add "$parent" "${1#"$parent"/}"
}
with_spec() { # spec file, git command... -> runs the command with the spec's pathspecs after --
  local f="$1" p; shift
  set -- "$@" --
  while IFS= read -r -d '' p; do set -- "$@" "$p"; done < "$f"
  "$@"
}
literal() { perl -0pe 's/^/:(literal)/' "$1" > "$1.lit"; echo "$1.lit"; }

if [ "$NAMED" = 1 ]; then
  git submodule foreach --recursive --quiet 'echo "$displaypath"' > "$TMP/subs" 2>/dev/null
  for p in "$@"; do
    case "$p" in
      /*) case "$p/" in "$TOP"/*) r=${p#"$TOP"} ;; "$LTOP"/*) r=${p#"$LTOP"} ;;
            *) die 64 "$p is outside the checkout $TOP. Nothing was changed" ;; esac ;;
      *) r=$PREFIX$p ;;
    esac
    r=$(perl -e 'for (split m{/}, $ARGV[0]) { next if $_ eq "" || $_ eq "."; if ($_ eq "..") { exit 1 unless @o; pop @o } else { push @o, $_ } } print join "/", @o' -- "$r") ||
      die 64 "$p is outside the checkout $TOP. Nothing was changed"
    o=$(owner_of "$r")
    if [ -z "$r" ]; then spec_add "" .
    elif [ -e "$r" ] || [ -L "$r" ] || git -C "${o:-.}" cat-file -e "HEAD:${r#"$o"/}" 2>/dev/null ||
         git -C "${o:-.}" ls-files --error-unmatch -- ":(literal)${r#"$o"/}" >/dev/null 2>&1; then
      spec_add "$o" "${r#"$o"/}"
    else
      die 64 "$p names nothing in the checkout. Nothing was changed"
    fi
    # A named directory or submodule takes every submodule inside it whole.
    while IFS= read -r s; do case "$s/" in "${r:+$r/}"*) spec_add "$s" . ;; esac; done < "$TMP/subs"
  done
fi

# ---------------------------------------------------------------- plan (read-only)
if [ "$MODE" = plan ]; then
  [ -d "$LOCK" ] && echo "note: a sync lock exists (pid $(cat "$LOCK/pid" 2>/dev/null)). See Troubleshooting."
  step "plan: list dirty repos"
  { dirty_repos "$TOP" ""; main_dirty; } > "$TMP/repos"
  if [ ! -s "$TMP/repos" ]; then
    echo "Nothing dirty. Run it anyway to merge-pull and push:"
    echo "  $0 run$FLAGS </dev/null"; exit 0
  fi
  : > "$TMP/blocks"
  while IFS=$'\t' read -r key dir; do
    cd "$dir" || continue
    echo; echo "== $key   $(git symbolic-ref -q --short HEAD || echo DETACHED) -> $(git rev-parse -q --abbrev-ref '@{u}' 2>/dev/null || echo 'no upstream')   $(git status --porcelain | wc -l | tr -d ' ') dirty"
    git status --short | head -40
    git diff HEAD --stat 2>/dev/null | tail -1
    git ls-files -z -o --exclude-standard > "$TMP/new"
    kb=$(untracked_kb "$TMP/new"); [ "$kb" -gt $((MAX_ADD_MB * 1024)) ] && { echo "OVER LIMIT: $((kb / 1024)) MB untracked (limit $MAX_ADD_MB MB):"; largest_untracked "$TMP/new"; }
    if [ "$NAMED" = 0 ]; then
      echo "$key" >> "$TMP/blocks"
    elif [ -s "$(keyfile "$key").spec" ] && [ -n "$(with_spec "$(keyfile "$key").spec" git status --porcelain)" ]; then
      echo "takes:"; with_spec "$(keyfile "$key").spec" git status --short | head -40
      echo "$key" >> "$TMP/blocks"; add_pointer "$key"
    else
      echo "takes: nothing named here, so this repo stays as it is"
    fi
  done < "$TMP/repos"
  echo; echo "---- fill each block, then run this one snippet ----"
  printf '%s run%s' "$0" "$FLAGS"
  if [ "$NAMED" = 1 ]; then printf ' --'; printf ' %q' "$@"; fi
  echo " <<'MSG'"
  while IFS= read -r key; do
    printf '== %s\n<intent line: why these changes exist>\n\nConfidence: <low|medium|high>\nScope-risk: <narrow|moderate|broad>\n' "$key"
  done < "$TMP/blocks"
  echo "MSG"; exit 0
fi

# ---------------------------------------------------------------- run
# 1. Messages: parse and check before any git change.
if [ ! -t 0 ]; then
  cur=""
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in "== "*) cur=$(keyfile "${line#== }"); echo "${line#== }" >> "$TMP/keys"; : > "$cur" ;;
      *) [ -n "$cur" ] && printf '%s\n' "$line" >> "$cur" ;; esac
  done
  bad=0
  while IFS= read -r k; do
    f=$(keyfile "$k")
    [ -n "$(sed -n '1p' "$f")" ] || { echo "sync: message for '$k' has no intent line" >&2; bad=1; }
    grep -qE '^Confidence: (low|medium|high)$' "$f" || { echo "sync: message for '$k' needs 'Confidence: low|medium|high'" >&2; bad=1; }
    grep -qE '^Scope-risk: (narrow|moderate|broad)$' "$f" || { echo "sync: message for '$k' needs 'Scope-risk: narrow|moderate|broad'" >&2; bad=1; }
    grep -qiE '^(Co-Authored-By|Claude-Session):|Generated with|<intent line' "$f" && { echo "sync: message for '$k' has an attribution line or an unfilled placeholder" >&2; bad=1; }
  done < <(cat "$TMP/keys" 2>/dev/null)
  [ "$bad" = 0 ] || die 64 "fix the messages; nothing was changed"
fi

# 3. One sync per checkout.
if ! mkdir "$LOCK" 2>/dev/null; then
  opid=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$opid" ] && kill -0 "$opid" 2>/dev/null; then
    die 75 "another sync runs in this checkout (pid $opid). Let it finish, or stop it with: kill -TERM -- -$opid"
  fi
  unlock; mkdir "$LOCK" || die 75 "cannot take $LOCK"
fi
HELD=1; echo $$ > "$LOCK/pid"
printf '.\0' > "$TMP/all"   # with no paths named, each dirty repo takes everything

message_for() { # key, NUL list of the paths the commit takes -> path of the commit message file
  local f; f=$(keyfile "$1")
  if [ ! -s "$f" ]; then
    printf 'Keep %s changed paths under %s in a checkpoint\n\nNo message was written for this repository before the run.\n\nConfidence: low\nScope-risk: moderate\nNot-tested: nothing was run for this checkpoint\n' \
      "$(tr -cd '\0' < "$2" | wc -c | tr -d ' ')" \
      "$(tr '\0' '\n' < "$2" | cut -d/ -f1 | sort -u | head -4 | paste -sd, -)" > "$f"
    note "$1: no message supplied, a fallback message was used"
  fi
  echo "$f"
}

# A default run stages the whole working tree; an explicit spec takes only its paths.
# Return 1 when there is nothing to commit after staging.
commit_named() { # key, spec file
  local key="$1" kb base
  with_spec "$2" git ls-files -z -o --exclude-standard > "$TMP/new"
  kb=$(untracked_kb "$TMP/new")
  if [ "$kb" -gt $((MAX_ADD_MB * 1024)) ]; then
    echo "largest untracked paths in $key:" >&2; largest_untracked "$TMP/new" >&2
    die 3 "$key: $((kb / 1024)) MB of untracked files, over the $MAX_ADD_MB MB limit. Ignore them, or raise SYNC_MAX_ADD_MB."
  fi
  if [ "$NAMED" = 0 ]; then
    if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
      die 2 "$key: unresolved merge conflicts remain. Resolve them before syncing; nothing was staged."
    fi
    git add -- . || die 4 "$key: git add failed (a stale index.lock? See Troubleshooting)"
    git diff --cached -z --name-only --no-renames > "$TMP/take"
    if [ ! -s "$TMP/take" ] && ! git rev-parse -q --verify MERGE_HEAD >/dev/null; then return 1; fi
    git commit -q -F "$(message_for "$key" "$TMP/take")" ||
      die 4 "$key: the commit was refused. Fix what the hook names."
    note "$key: committed $(git rev-parse --short HEAD) on $br"
    return 0
  fi
  if [ -s "$TMP/new" ]; then
    git add --pathspec-from-file="$(literal "$TMP/new")" --pathspec-file-nul ||
      die 4 "$key: git add failed (a stale index.lock? See Troubleshooting)"
  fi
  base=$(git rev-parse -q --verify HEAD) || base=$(git hash-object -t tree /dev/null)
  with_spec "$2" git diff -z --name-only --no-renames --ignore-submodules=dirty "$base" > "$TMP/take"
  if [ ! -s "$TMP/take" ]; then [ "$NAMED" = 0 ] || note "$key: the named paths hold no change"; return 1; fi
  if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
    [ "$NAMED" = 0 ] || die 2 "$key: a merge is in progress, and git concludes a merge only as a whole. Conclude it with a run that names no paths, or by hand; then sync again"
    git add --pathspec-from-file="$(literal "$TMP/take")" --pathspec-file-nul &&
      git commit -q -F "$(message_for "$key" "$TMP/take")" || die 4 "$key: the commit was refused. Fix what the hook names."
  else
    git commit -q --only --pathspec-from-file="$(literal "$TMP/take")" --pathspec-file-nul -F "$(message_for "$key" "$TMP/take")" ||
      die 4 "$key: the commit was refused. Fix what the hook names."
  fi
  note "$key: committed $(git rev-parse --short HEAD) on $br"
}

staged_hint() { # -> a sentence when paths are staged, because git refuses a merge while any path is staged
  local n; n=$(git diff --cached --name-only | wc -l | tr -d ' ')
  [ "$n" = 0 ] || printf '. %s paths are staged, and git refuses a merge while any path is staged; the commit is safe on the local branch, so sync again once they are committed' "$n"
}
merge_stop() { # what failed -> exit 2 on a conflict, which is left in place; exit 4 otherwise
  if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    echo "conflicted paths:" >&2; git diff --name-only --diff-filter=U >&2
    die 2 "$1 conflicts. The merge is left in place; write the conflict brief."
  fi
  die 4 "$1 failed without a conflict (network, credentials or a hook)$(staged_hint)"
}

sync_repo() { # key, dir
  local key="$1" br up try spec="$TMP/all" took=0
  cd "$2" || die 4 "$key: cannot enter $2"
  br=$(git symbolic-ref -q --short HEAD || echo DETACHED)
  [ "$NAMED" = 1 ] && spec="$(keyfile "$key").spec"
  if [ -s "$spec" ] && [ -n "$(git status --porcelain)" ]; then
    step "$key: commit"
    commit_named "$key" "$spec" && took=1
  fi
  if [ "$NAMED" = 1 ]; then
    [ "$took" = 1 ] && add_pointer "$key"
    # A repo the run took nothing from is left alone; the checkout itself still merge-pulls and pushes.
    case "$key" in .|main:.) ;; *) [ "$took" = 1 ] || return 0 ;; esac
  fi
  if [ "$br" = DETACHED ]; then note "$key: WARNING detached HEAD, not pushed. The parent may point at an unpushed commit."; return 0; fi
  if ! up=$(git rev-parse -q --abbrev-ref '@{u}' 2>/dev/null); then note "$key: $br has no upstream, kept local"; return 0; fi
  for try in 1 2; do
    step "$key: merge-pull $up (try $try)"
    git pull --no-rebase --no-edit -q || merge_stop "$key: the merge-pull of $up"
    step "$key: push (try $try)"
    # shellcheck disable=SC2086
    if git push -q $NOVERIFY; then note "$key: pushed $br at $(git rev-parse --short HEAD)"; return 0; fi
  done
  die 4 "$key: push failed twice after a merge-pull. Read the hook or remote message above."
}

sync_checkout() { # checkout dir, key prefix
  local key dir
  dirty_repos "$1" "$2" > "$TMP/repos"
  # The checkout itself always gets its merge-pull and push, dirty or clean.
  grep -q "^$2\.	" "$TMP/repos" || printf '%s\t%s\n' "$2." "$1" >> "$TMP/repos"
  while IFS=$'\t' read -r key dir <&3; do sync_repo "$key" "$dir"; done 3< "$TMP/repos"
}

sync_checkout "$TOP" ""
BR=$(git -C "$TOP" symbolic-ref -q --short HEAD || echo DETACHED)

if [ "$FROM_MAIN" = 1 ]; then
  cd "$TOP" || exit 4
  step "merge origin/main into $BR"
  git fetch -q origin main || die 4 "fetch of origin main failed"
  git merge origin/main --no-ff --no-edit -q || merge_stop "merging main into $BR"
  # shellcheck disable=SC2086
  git push -q $NOVERIFY || die 4 "push of $BR failed after merging main"
  note "main merged into $BR, pushed at $(git rev-parse --short HEAD)"
fi

if [ "$MAIN" = 1 ] && [ "$BR" != main ]; then
  M=$(main_checkout); [ -n "$M" ] || die 64 "--main: no worktree has main checked out"
  sync_checkout "$M" "main:"
  cd "$M" || exit 4
  step "land $BR on main"
  git merge "$BR" --no-ff --no-edit -q || merge_stop "landing $BR on main in $M"
  # shellcheck disable=SC2086
  git push -q $NOVERIFY || die 4 "push of main failed after landing $BR"
  note "main: $BR landed, pushed at $(git rev-parse --short HEAD)"
fi

echo "sync: done in $(( $(date +%s) - START ))s"; cat "$TMP/report"
left=$(git -C "$TOP" status --porcelain | wc -l | tr -d ' ')
if [ "$left" != 0 ] && [ "$NAMED" = 1 ]; then echo "  note: $left dirty paths are left as they were: the run took only the paths named after --."
elif [ "$left" != 0 ]; then echo "  note: $left paths became dirty during the run (another writer). Sync again to take them."; fi
exit 0
