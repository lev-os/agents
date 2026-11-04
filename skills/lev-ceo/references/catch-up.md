# Catch-up: the Window read, what to read, count and fold

The method behind the Catch-up reply. The format stays in `SKILL.md` §7 Catch-up; the thread-read rule stays in `SKILL.md` §1 step 10.

## Window read

Any ask with a time window ("the last 6 hours", "roll up today", "since X"). Set `from` and `to` in UTC from JP's words and `date -u` ("the last 6 hours": `to` is now, `from` is 6 hours before). At wider scopes, run steps 2 and 3 for each project in scope.

1. Live threads: the rows from boot step 6.
2. Threads that finished inside the window: `mcp__t3-code__t3_thread_list {includeSubagents:false, settled:false, statuses:["completed","idle","failed","cancelled"], limit:20}` (`projectId` per project at wider scopes). Rows come newest `updatedAt` first; page with `cursor` only while the last row's `updatedAt` is after `from`. Keep the rows inside the window. `settled` is JP's done mark, not a status: a `settled:true` read finds only threads he settled (observed 2026-10-30T06:38Z: 19 finished threads unsettled, all updated within the hour; the newest of 45 settled threads was settled 2026-10-26). One `settled:true` read with `limit:20` adds the threads whose `settledAt` falls inside the window.
3. Commits for each checkout in scope, including checkouts with no live thread: `git -C <root> log --since=<from> --until=<to> --oneline | wc -l`.
4. Read each kept thread with the thread-read rule; at most 8 in full, the rest as counts.

Done when every thread updated in the window and every checkout with commits in it has a bullet or a count.

## Steps

1. **Find the start.** With a time window, the window's `from` is the start. Without one, the start is JP's last message.
   - Read each thread with the thread-read rule: the saved `nextPosition`, or the newest 20 items.
   - No message from JP in that window: step back 100 items at a time (`limit:100`, `maxCharsPerItem:300`). Stop after three steps back and name the rest under "Not read".
   - Save the last `nextPosition` under `threads` in the handoff.

   Done when you hold the start (JP's last message or the window's `from`) and the newest position for each thread read.
2. **Count.** Count the messages and the worker updates after the start; with a window, also the threads updated and the commits per checkout. Done when the counts sit in the "What happened" line with the positions read.
3. **Answer first.** JP's last question gets its answer in the first line.
4. **Fold.** Fold worker updates into 3 to 6 events, oldest first, each with a sha, a path:line or a link. Updates bury replies when listed one by one (JP 2026-10-06, `.lev/pm/workstreams/agent-runtime-convergence/captures/20261006T234702Z-explain-missed-messages-updates-bury-replies.yaml`).
5. **Decisions.** Quote each decision made with its date and file. Decisions that wait on JP go first in Next steps, each in the Decision shape (`SKILL.md` §7 Decision).
6. **Progress.** One segment per stage from the handoff's `stages` key. A stage is ✅ only when your rerun verified it (`~/.claude/skills/explain/SKILL.md:203-215`).
7. **Coverage.** Name the positions read and every item not read.

Done when every item after the start is either in a bullet or named under "Not read".

## Example

```text
The private release for Josh is sequenced and the loader slice runs; one ruling waits on you.
**What happened** 03:10–05:39 UTC · 6 messages, 4 worker updates folded in · read positions 7007–7081 of [lev > mesh spikes](t3-thread://v1/6de05925)
- JP: Josh installs from the private repo first · capture 20261030T043752Z-onboard-josh-horizon.yaml
- The six-owner foundation landed on main · da1f61f85e
- The loader worker started; evidence folder named · handoff 20261030-private-release-josh.yaml
- The lev-ceo skill home was decided: a global skill · .lev/pm/decisions/20261030-lev-ceo-skill-home.yaml (a)
**Decisions**: made: lev-ceo skill home · 2026-10-30 · a · waiting on you: 1, first in Next steps
**Progress**: [✅ 🟡 ⬜ ⬜ ⬜ ⬜] 1/6 verified by my rerun
**Not read**: the loader worker's full log

**🪄 Next steps:**

## 1 · Where the legal material lives 📜
The private repo for Josh must not carry files he may not see.
Searched first: 155 captures, 554 decisions (`grep -ril 'legal' .lev/pm/workstreams/*/captures .lev/pm/decisions`) → none.
- a. A submodule history: no rewrite.
- b. Leviathan history: a force-push, on your word.
- c. Nowhere that matters: close the item.

I recommend (a): it takes the force-push out of the plan. Example: Josh clones leviathan and never sees a contract. Logged: `.lev/pm/decisions/20261030-legal-material-home.yaml`. (L2)

## 2 · Read the loader worker's first report at 06:00Z ⏱️ (L1)
## 3. All: 1 -> 2
## 4. ⬅️ **Back** - Return to lev > mesh
---
🧙🏽‍♂️ **[lev://mesh]** oss-projection | ⚡ WAITING ON JP: legal material home ruling | crystallizing 🔍
```
