# orch --herdr: multi-tab lane orchestration

Load this file only when the invocation carries `--herdr`. It adds a surface
(herdr tabs, one agent per bounded lane) to the modes in SKILL.md; it does not
replace them. The execute → verify → accept loop, branch-read rules, and
report-on-every-exit rules in SKILL.md still bind every lane.

| Invocation | What runs |
|---|---|
| `orch --herdr` | Steps 1–5: interview, scan, recommend a tab layout, write lane docs and the ledger with every lane `status: recommended`. Opens no pane and arms no wakeup. |
| `orch --herdr auto` | Steps 1–8: also open lanes per tab policy and run the tick loop until only operator decisions or live waits remain. |
| `orch --herdr --once` | One tick (step 8) against an existing ledger, then stop. |

Paths marked **Lev default** are what the Leviathan repo uses. For another
project, substitute its equivalent and write the chosen path into the ledger
so every later tick reads the same one.

## 1. Interview (one question)

Ask one question: "Which repo should I orchestrate, and is there already a
herdr workspace for it?" Offer the default in the question: the current
directory when `git -C . rev-parse --show-toplevel` succeeds, and whichever
workspace `herdr workspace list` shows with a matching cwd. When both defaults
resolve and the operator already named the target, skip the question.

Validation: the repo root and the workspace id (or "none yet") are recorded
before any scan.

## 2. Scan (read-only)

Collect the facts below. Change nothing in this step.

| Fact | Command |
|---|---|
| Workspaces, tabs, panes | `herdr workspace list`; `herdr tab list --workspace <w>`; `herdr pane list --workspace <w>` |
| What each pane is doing | `herdr pane read <pane> --source visible --lines 40` (use `recent-unwrapped` with more lines for a transcript); `herdr pane process-info --pane <id>` |
| Repo state | `git -C <repo> status --short`; `git -C <repo> rev-list --left-right --count @{u}...HEAD` (behind, ahead) |
| Tracked work | **Lev default:** `.lev/pm/workstreams/*/state/workstream.yaml`, newest `.lev/pm/handoffs/*.md`, `.lev/pm/plans/*.md`. Other projects: their tracker, plan docs, open PRs (`gh pr list`). |
| Recent agent sessions | Claude `~/.claude/projects/<cwd-slug>/*.jsonl`; omo `~/.omo/agent/sessions/<cwd-slug>/`; omp `~/.omp/agent/sessions/`. Sort by mtime; read the tail of the newest few. |
| Machine load | `sysctl vm.swapusage` (Linux: `free -m`); `sysctl -n vm.loadavg` or `uptime` |
| Orphans | `ps -axo pid,ppid,etime,command \| awk '$2==1' \| grep -E 'bun\|node\|tsx\|omo\|omp\|claude'`. On macOS every launchd service has ppid 1, so filter by agent runtimes. |

Killing an orphan is an operator decision: list it on the status page with its
pid, age and command, and wait for an answer. Kill only by exact pid, never by
process name.

Validation: each pane has a one-line "what it is doing" entry, and swap percent
is known.

## 3. Recommend a tab layout (only if none exists)

When the workspace already has lane tabs, map them to lanes and skip to step 4
for any lane that has no doc. Otherwise propose:

- **One tab per bounded lane.** A lane has a point A (where it is now, with
  evidence) and a point B (a done condition someone else can check). Example:
  "storage: the FilePort packet is written but not approved → the port and its
  packet are committed and a capture exists."
- **Dependencies between lanes.** Example: "the command registry lane waits
  until the entity lane's first three slices land, because commands are
  generated over entities."
- **An agent cap** from tab policy (step 6), and which lanes wait for a slot.
- **No overlap.** Two lanes never edit the same package. If they would, merge
  them or sequence them.

Present the layout as a short table (lane, A → B, depends on, agent, phase) and
get the operator's approval before step 7 opens anything.

## 4. Write a lane doc per lane

A pane is never started without a lane doc. Write each doc outside the repo, in
the run's state dir. **Lev default:** `~/.local/state/lev/<run-id>/NN-<lane>.md`;
elsewhere `${XDG_STATE_HOME:-~/.local/state}/<project>/<run-id>/NN-<lane>.md`.
The state dir keeps lane docs out of other sessions' commits and out of
repo auto-clean sweeps.

Worked examples (read them for shape; their project details do not transfer):
`~/.local/state/lev/recovery-20260928/10-ontology.md` (a coding lane with held
decisions), `11-ooo-intake.md` (an intake lane kept open),
`12-ontology-design.md` and `13-dna-decomposition.md` (paired design lanes that
coordinate through named files).

<lane_doc>
# Lane NN: {lane name}, {one-line purpose}

Rules for every lane: stage by explicit pathspec only; never `git add -A`/`-u`;
no stash; no push unless the ledger says so; no new worktrees; targeted tests
only. Other lanes share this checkout: check `git status --short` for strangers
before any commit, and use `git commit -- <paths>` when the index holds another
session's staged files. Speak plain English; never cite a decision code without
saying what it decided. Rulings in force are in {ledger path}; anything under
`forks_for_operator` is held: work around it, do not decide it.

## Goal
{point A with evidence} → {point B}. {Why the operator wants it, quoted if possible.}

## Where things are
{paths, workstream/plan/handoff refs, sibling lanes and the files you coordinate through}

## Order of work
1. {re-verify the plan's claims against HEAD}
2. {smallest slice, with its verifier command}
3. {…}
N. Stop. Report evidence (commands and exit codes) and any open question.

## Done condition
{observable: commits exist for named paths, a named test passes, a capture or handoff is written}
</lane_doc>

Validation: every lane in the layout has a doc with all five parts, and each
done condition names a check that could fail.

## 5. Create the orchestrator ledger

One YAML file in the same state dir (**Lev default:**
`~/.local/state/lev/<run-id>/orchestrator-ledger.yaml`; worked example
`~/.local/state/lev/recovery-20260928/orchestrator-ledger.yaml`). Top-level keys:

```yaml
target_state: >   # the end state in plain words
rules: []          # checkout, commit, test and cap rules every lane follows
rulings: []        # {id, lane, ruling, why}; operator answers quoted verbatim with attribution
forks_for_operator: []   # {id, lane, question, options, evidence, why_held, recommendation, unblocks}; the Lev worked example names it forks_for_jp
phases: []         # {id, active, parked, exit}
operator_channel: {}     # step 7
tab_policy: {}     # step 6
lanes: {}          # lane -> {pane, status, last_evidence, next}
ticks: []          # {at, swap_pct, active_agents, actions, findings}
cadence_seconds: 900
```

Lanes append to this file, and an unquoted colon or a misplaced append breaks
it (it happened tonight: a ruling was appended under `tab_policy`). Before and
after every edit:

```bash
cp ledger.yaml ledger.yaml.bak-$(date +%H%M)          # before
python3 -c 'import sys,yaml; yaml.safe_load(open(sys.argv[1]))' ledger.yaml   # before and after
```

If the check fails after an edit, repair from the backup; never leave the
ledger unparseable at the end of a tick.

Validation: the file parses, and `lanes` has one entry per lane doc.

## 6. Tab policy (defaults; the ledger's values win)

Copy this block into the ledger's `tab_policy`. Every value is a default the
operator may change in the ledger; each tick reads the ledger, not this file.

```yaml
tab_policy:
  cap: {swap_over_80_pct: 6, otherwise: 8, hard_max: 8}   # active agent panes
  slot_check: [sysctl vm.swapusage, herdr pane list]       # agent_status busy|idle|done|unknown
  open_when:
    - the lane's phase is current and its declared dependencies have landed
    - a slot is free under the cap
    - the lane doc exists with rules, where it stopped, first action, done condition
  open_how:
    - herdr tab create --workspace <w> --cwd <repo> --label <lane>   # returns .result.root_pane
    - herdr pane run <pane> 'omo -n <lane>'    # or 'claude' for review-only lanes
    - herdr pane run <pane> 'Read <lane doc> in full and follow it. Stop at the done condition or any held fork.'
  close_when:
    - done with evidence (verifier commands + exit codes), every change committed by explicit pathspec, and a capture or handoff written
    - or parked with nothing uncommitted and its next step written in the lane doc
    - never with uncommitted files or an unanswered question
  close_how:
    - read the pane one last time; copy its evidence into lanes.<lane> and the tick entry
    - herdr pane run <pane> '/exit'   # agent; 'exit' for a shell
    - herdr tab close <tab_id>
  park_when: the lane hits a held fork or waits on an outside party; keep the pane only if its context is expensive to rebuild (>150K tokens) and a slot is free
  reopen: same as open_how; the lane doc plus its capture/handoff is the resume state, never the pane scrollback
  context_ceiling: panes past ~400K tokens commit, capture, close, and reopen from the lane doc
  never: [two agents editing one package, a new worktree, a pane started without a lane doc]
```

Before marking a lane done, run one check yourself (for example
`git log --oneline -1 -- <path>` or the named test). A pane saying "done" is a
claim; SKILL.md's verify-before-accept rule applies.

## 7. Operator channel

**Primary: a /now status page with feedback cards.** Use the `now` skill.
Rebuild the same slug every tick (never a new page). **Lev default:**
`.lev/now/status-orchestrator-<date>.json` rendered beside it as `.html`. Read
answers with:

```bash
python3 ~/.claude/skills/now/scripts/feedback-answers.py <spec.json>
```

An answer on the page is a ruling: quote it verbatim under `rulings` with
attribution (`<operator> (now-page)`).

**Optional: Slack self-DM**, through the `tools` skill's Slack transport. Post
and read with curl from the one shell pane that holds the token, expanding
`$SLACK_USER_TOKEN` inside that pane. Never print, echo or copy the token into
another pane, file or ledger. Do not use `slack api conversations.replies`: it
hangs. One thread per fork, the fork id in the first line; tick summaries go to
Slack only when something needs the operator or a phase closes.

Record the channel in the ledger's `operator_channel` (page path, read
command, optional Slack pane id and thread roots).

## 8. The tick loop

Use the `ll` skill's tick discipline and the host's wakeup: in Claude Code, the
`loop` skill's self-paced mode with `ScheduleWakeup` at the ledger's
`cadence_seconds` (default 900). Arm it only in `auto`, or with an explicit
`--watch=<interval>`. Each tick, in order:

1. Back up and validate the ledger; read it.
2. Scan panes (step 2 rows 1–2) and swap.
3. Read operator answers (page, then Slack threads); record each as a ruling.
4. Answer panes that are waiting on a question already covered by a ruling;
   send the ruling text, not its code. Questions outside existing rulings
   become forks on the status page.
5. Close, park and open lanes per `tab_policy`.
6. Rebuild the status page.
7. Append a tick entry (`at` from `date`, never estimated; swap percent; active
   agents; actions; findings) and validate the ledger again.
8. Reschedule the wakeup.

**Pause:** stop rescheduling and write `paused: {at, by, resume}` into the
ledger, where `resume` is the exact re-arm instruction. **Resume:** read the
ledger and the page answers before the first action.

The ledger tick entry plus the rebuilt status page are this mode's report
artifact for SKILL.md's "report on every exit path" rule.

## 9. Skills this workflow uses

| Need | Skill |
|---|---|
| Tick loop discipline, schedule, pause | `ll`; Claude Code `loop` |
| Status page and feedback cards | `now` |
| Find or resume a workstream per lane | `ws` |
| Which lifecycle owner a lane's next step belongs to | `work` |
| Lane close and session transfer | `handoff`, `capture` |
| Commits: pathspec-only, `git commit -- <paths>` when the index holds another session's staged files | `lev-lore-commit` (Lev); the project's commit convention elsewhere |
| herdr and Slack transport | `tools` |
| Which agent and model runs a lane | `coder` |

## 10. How to write to the operator

These apply to every report, status page, lane doc and ledger entry:

- Plain English. Never write a decision code (R12, J1, F5) without saying what
  it decided: "the entity-definitions ruling (extend the existing key)" instead
  of "R12".
- Every abstract choice gets a concrete example a human can follow: a folder
  tree, a config snippet, or a command and what it prints.
- Decisions are synthesized into the design, docs or entities they change. The
  ledger records who ruled and when; it is not where the decision lives.
- One master tracker links every plan and gap file. Point to it; do not copy it.
