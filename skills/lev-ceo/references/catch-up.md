# Catch-up: what to read, count and fold

For "catch me up", "what did I miss", and any ask with a time window ("the last 6 hours", "roll up today", "since X"). The thread-read rule is `references/sweep.md`, step 4.

## Window read

Set `from` and `to` in UTC from JP's words and `date -u`. At a wider scope, run steps 2 and 3 for each project.

1. Live chats: the rows of the sweep's list call.
2. Chats that finished inside the window: `mcp__t3-code__t3_thread_list {includeSubagents:false, settled:false, statuses:["completed","idle","failed","cancelled"], limit:20}`. Rows come newest first; page only while the last row's `updatedAt` is after `from`. One more read with `settled:true` and `limit:20` adds the chats settled inside the window.
3. Commits for each checkout in scope: `git -C <root> log --since=<from> --until=<to> --oneline | wc -l`.
4. Read each kept chat with the thread-read rule; at most 8 in full, the rest as counts.

Done when every chat updated in the window and every checkout with commits in it has a bullet or a count.

## Steps

1. **Find the start.** With a window, the start is `from`. Without one, it is JP's last message: read back 100 items at a time, stop after three steps, and name the rest under "Not read".
2. **Count** the messages and the worker updates after the start; with a window, also the chats updated and the commits per checkout.
3. **Answer first.** JP's last question gets its answer in the first line.
4. **Fold** worker updates into 3 to 6 events, oldest first, each with a sha, a path or a link. Updates listed one by one bury the replies.
5. **Decisions.** Quote each decision made, with its date and file. A decision that waits on JP goes under For you.
6. **Progress.** One bar segment per stage from the handoff's `stages`; ✅ only when your rerun verified it.
7. **Coverage.** Name the positions read and every item not read.

Done when every item after the start is in a bullet or named under "Not read".

## Shape

About 15 lines above For you; prose over tables.

```text
{Where things stand, 1-2 sentences; JP's last question answered first.}
**What happened** {from}–{to} UTC · {n} messages, {m} worker updates folded in · read positions {a}–{b} of {link}
- {event} · {sha | path | link}   (3 to 6 bullets, oldest first)
**Decisions:** made: {title · date · choice} | none · waiting on you: {n}, under For you
**Not read:** {what | nothing}
```

Then the reply template of `~/.claude/CLAUDE.md` and the mesh line (`references/replies.md`).
