#!/usr/bin/env bash
# sync.sh: one bounded checkpoint of the current checkout and its dirty submodules.
#
#   sync.sh plan [--main]                 read-only: list dirty repos and print the run snippet
#   sync.sh run  [--main|--from-main] [--no-verify]   commit, merge-pull, push; messages on stdin
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
#       64 bad message or usage · 75 another sync holds the lock · 124 budget spent
set -u

MODE="${1:-}"; [ $# -gt 0 ] && shift
# Lead a process group, so the watchdog can stop git and every hook it started.
if [ -z "${SYNC_PGL:-}" ]; then
  export SYNC_PGL=1
  exec perl -e 'setpgrp(0,0); exec @ARGV or die "exec: $!"' "$0" "$MODE" "$@"
fi

MAIN=0; FROM_MAIN=0; NOVERIFY=""
for a in "$@"; do case "$a" in
  --main) MAIN=1 ;; --from-main) FROM_MAIN=1 ;; --no-verify) NOVERIFY="--no-verify" ;;
  *) echo "sync: unknown argument $a" >&2; exit 64 ;;
esac; done
case "$MODE" in plan) BUDGET="${SYNC_BUDGET:-60}" ;; run) BUDGET="${SYNC_BUDGET:-300}" ;;
  *) sed -n '2,18p' "$0" >&2; exit 64 ;; esac
MAX_ADD_MB="${SYNC_MAX_ADD_MB:-100}"
export GIT_TERMINAL_PROMPT=0 GIT_MERGE_AUTOEDIT=no

TOP=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "sync: not in a git checkout" >&2; exit 64; }
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

# Dirty repos of one checkout, deepest submodule first, the checkout itself last.
dirty_repos() { # checkout dir, key prefix -> lines "key<TAB>dir"
  local top="$1" pre="$2" p
  git -C "$top" submodule foreach --recursive --quiet 'echo "$displaypath"' 2>/dev/null | sed '1!G;h;$!d' |
    while IFS= read -r p; do
      [ -n "$(git -C "$top/$p" status --porcelain 2>/dev/null)" ] && printf '%s\t%s\n' "$pre$p" "$top/$p"
    done
  [ -n "$(git -C "$top" status --porcelain)" ] && printf '%s\t%s\n' "$pre." "$top"
  return 0
}
main_checkout() {
  git worktree list --porcelain | awk '/^worktree /{w=substr($0,10)} $0=="branch refs/heads/main"{print w; exit}'
}
# New untracked files that would enter git itself. Git LFS paths are left out: LFS is where large files belong.
untracked_plain() {
  git ls-files -o --exclude-standard -z | git check-attr --stdin -z filter |
    perl -0ne 'chomp; push @r, $_; if (@r == 3) { print "$r[0]\0" unless $r[2] eq "lfs"; @r = () }'
}
untracked_kb() { untracked_plain | xargs -0 -r du -k 2>/dev/null | awk '{s+=$1} END{print s+0}'; }
largest_untracked() {
  untracked_plain | xargs -0 -r du -k 2>/dev/null |
    awk -F'\t' '{n=split($2,p,"/"); k=(n>2)?p[1]"/"p[2]:(n>1?p[1]:$2); s[k]+=$1}
                END{for(k in s) printf "%8.1f MB  %s\n", s[k]/1024, k}' | sort -rn | head -5
}

# ---------------------------------------------------------------- plan (read-only)
if [ "$MODE" = plan ]; then
  [ -d "$LOCK" ] && echo "note: a sync lock exists (pid $(cat "$LOCK/pid" 2>/dev/null)). See Troubleshooting."
  step "plan: list dirty repos"
  { dirty_repos "$TOP" ""
    if [ "$MAIN" = 1 ]; then m=$(main_checkout); [ -n "$m" ] && [ "$m" != "$TOP" ] && dirty_repos "$m" "main:"; fi
  } > "$TMP/repos"
  if [ ! -s "$TMP/repos" ]; then
    echo "Nothing dirty. Run it anyway to merge-pull and push:"
    echo "  $0 run${*:+ $*} </dev/null"; exit 0
  fi
  while IFS=$'\t' read -r key dir; do
    cd "$dir" || continue
    echo; echo "== $key   $(git symbolic-ref -q --short HEAD || echo DETACHED) -> $(git rev-parse -q --abbrev-ref '@{u}' 2>/dev/null || echo 'no upstream')   $(git status --porcelain | wc -l | tr -d ' ') dirty"
    git status --short | head -40
    git diff HEAD --stat 2>/dev/null | tail -1
    kb=$(untracked_kb); [ "$kb" -gt $((MAX_ADD_MB * 1024)) ] && { echo "OVER LIMIT: $((kb / 1024)) MB untracked (limit $MAX_ADD_MB MB):"; largest_untracked; }
  done < "$TMP/repos"
  echo; echo "---- fill each block, then run this one snippet ----"
  echo "$0 run${*:+ $*} <<'MSG'"
  while IFS=$'\t' read -r key dir; do
    printf '== %s\n<intent line: why these changes exist>\n\nConfidence: <low|medium|high>\nScope-risk: <narrow|moderate|broad>\n' "$key"
  done < "$TMP/repos"
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

# 2. One sync per checkout.
if ! mkdir "$LOCK" 2>/dev/null; then
  opid=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$opid" ] && kill -0 "$opid" 2>/dev/null; then
    die 75 "another sync runs in this checkout (pid $opid). Let it finish, or stop it with: kill -TERM -- -$opid"
  fi
  unlock; mkdir "$LOCK" || die 75 "cannot take $LOCK"
fi
HELD=1; echo $$ > "$LOCK/pid"

message_for() { # key -> path of the commit message file
  local f; f=$(keyfile "$1")
  if [ ! -s "$f" ]; then
    printf 'Checkpoint %s changed paths under %s so the sync leaves nothing dirty\n\nNo message was written for this repository before the run.\n\nConfidence: low\nScope-risk: moderate\nNot-tested: nothing was run for this checkpoint\n' \
      "$(git diff --cached --name-only | wc -l | tr -d ' ')" \
      "$(git diff --cached --name-only | cut -d/ -f1 | sort -u | head -4 | paste -sd, -)" > "$f"
    note "$1: no message supplied, a fallback message was used"
  fi
  echo "$f"
}

sync_repo() { # key, dir
  local key="$1" br up kb try
  cd "$2" || die 4 "$key: cannot enter $2"
  br=$(git symbolic-ref -q --short HEAD || echo DETACHED)
  if [ -n "$(git status --porcelain)" ]; then
    kb=$(untracked_kb)
    if [ "$kb" -gt $((MAX_ADD_MB * 1024)) ]; then
      echo "largest untracked paths in $key:" >&2; largest_untracked >&2
      die 3 "$key: $((kb / 1024)) MB of untracked files, over the $MAX_ADD_MB MB limit. Ignore them, or raise SYNC_MAX_ADD_MB."
    fi
    step "$key: commit"
    git add . || die 4 "$key: git add failed (a stale index.lock? See Troubleshooting)"
    if ! git diff --cached --quiet; then
      git commit -q -F "$(message_for "$key")" || die 4 "$key: the commit was refused. Fix what the hook names."
      note "$key: committed $(git rev-parse --short HEAD) on $br"
    fi
  fi
  if [ "$br" = DETACHED ]; then note "$key: WARNING detached HEAD, not pushed. The parent may point at an unpushed commit."; return 0; fi
  if ! up=$(git rev-parse -q --abbrev-ref '@{u}' 2>/dev/null); then note "$key: $br has no upstream, kept local"; return 0; fi
  for try in 1 2; do
    step "$key: merge-pull $up (try $try)"
    if ! git pull --no-rebase --no-edit -q; then
      if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
        echo "conflicted paths in $key:" >&2; git diff --name-only --diff-filter=U >&2
        die 2 "$key: merge conflict. The merge is left in place; write the conflict brief."
      fi
      die 4 "$key: pull failed without a conflict (network, credentials or a hook)"
    fi
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
  git merge origin/main --no-ff --no-edit -q || { git diff --name-only --diff-filter=U >&2; die 2 "merging main into $BR conflicts. The merge is left in place; write the conflict brief."; }
  # shellcheck disable=SC2086
  git push -q $NOVERIFY || die 4 "push of $BR failed after merging main"
  note "main merged into $BR, pushed at $(git rev-parse --short HEAD)"
fi

if [ "$MAIN" = 1 ] && [ "$BR" != main ]; then
  M=$(main_checkout); [ -n "$M" ] || die 64 "--main: no worktree has main checked out"
  sync_checkout "$M" "main:"
  cd "$M" || exit 4
  step "land $BR on main"
  git merge "$BR" --no-ff --no-edit -q || { git diff --name-only --diff-filter=U >&2; die 2 "landing $BR on main conflicts. The merge is left in place in $M; write the conflict brief."; }
  # shellcheck disable=SC2086
  git push -q $NOVERIFY || die 4 "push of main failed after landing $BR"
  note "main: $BR landed, pushed at $(git rev-parse --short HEAD)"
fi

echo "sync: done in $(( $(date +%s) - START ))s"; cat "$TMP/report"
left=$(git -C "$TOP" status --porcelain | wc -l | tr -d ' ')
[ "$left" = 0 ] || echo "  note: $left paths became dirty during the run (another writer). Sync again to take them."
exit 0
