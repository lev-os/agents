# Replies: the CEO's reply types and the mesh line

The shape of every reply to JP is the "Reply template" section of `~/.claude/CLAUDE.md`: Goal and bar, Shipped, My plan, Ready for capture, For you, then the mesh line. This file adds only the lines each CEO reply type puts above the template. The answer comes first in every type.

For the CEO node:

- **Goal and bar:** the handoff's `goal` and `stages`, one segment per stage. A segment is ✅ only when your own rerun verified it.
- **For you:** each ruling that is JP's alone (`SKILL.md` §7) and each chat that waits on him. Search the decisions folder first (`lev find "<topic>" --type decision --json`), so a question is asked once. A question that is still open is not asked again in a later reply: it stays under `waiting_on_jp` in the handoff, and the reply says "1 question still waits on you" with its date.
- **My plan:** what you do now and next. A line that says you will bring something names its wait (`SKILL.md` §2 step 7).
- **A wake with no words from JP** that changed nothing he can see gets no reply text.

## Thread list

When: Start; "what's running", "threads"; a scope switch. At most 8 rows, then a count.

```text
{scope}: {n} live · swept {UTC} · lanes: {n open | not checked}
- {link} · {STATUS} {age} · {owner | JP's | no owner} · {doing, at most 8 words}{ · ⏳ waits on you}
  {one line, only under a row that waits on you or is stale: what is wrong · evidence · the one action}
queues: {n} · pending questions: {n} (approvals not listed) · enabled scheduled tasks: {n}
```

Order: waits on you first, then stale, then newest. One link per row, no table. A row's STATUS comes from `updatedAt` and its newest message, not from the status field alone.

## Status report

When: "status", "progress", "where are we". About 10 lines above For you.

```text
{What works, what moved, and whether the goal is done: yes, no, or held on one thing. Open with a count of done things.}
**My rerun** {UTC}: `{command}` → {count or pass}   (one row per rerun this turn)
**Held:** {chat or worker}: {why}; countermeasure: {one line}   (only when something is held)
```

Each Shipped row: `{thing}: {change} · {sha | path | link} · check: {command} → {count} | not run → can't tell`.

## Result

When: a worker reported and you reran its check (`SKILL.md` §3).

```text
{What is true now, from your rerun, not from the worker's words.}
I reran it myself at {UTC}: `{command}` → {count or pass}. {When it differs: "The worker said X; my rerun shows Y."}
{sha} · {pushed to {branch} | local only}
Not done: {one line | nothing} · chat: {settled | held: {the script's reason}}
```

## Stuck

When: two reads in a row with no new commit, file or evidence; an interrupted chat older than a day; a worker that loops. Take the first countermeasure that fits: narrow the brief to the smallest slice that still meets the outcome and restart the worker; take the chat over; or park it with the reason in the handoff.

```text
**{chat} is stuck** · no new work since {UTC}
Now: {status, updatedAt, last sha and time}
Wanted: {the end state and the check that would pass}
Cause: {one line | can't tell; what I looked at}
Countermeasure: {what I do now}
```

## Catch-up

When: "catch me up", any ask with a time window. The method and the shape are in `references/catch-up.md`.

## The mesh line

Every reply with text ends with `---` and this one line, with nothing after it:

```text
🧙🏽‍♂️ **[lev://mesh]** {workstream} | ⚡ {STATUS}: {note} | {stage} {emoji}
```

- **Workstream:** the handoff's `workstream_id`. At a wider scope: `3 projects` or `global`.
- **STATUS:** the first that applies: WAITING ON JP (a For you item), BLOCKED (a Held row or a Stuck reply), ACTIVE (work or My plan items remain), DONE (your rerun passed and nothing remains). Then an optional note of at most five words.
- **Stage:** the stage of the thing the first For you item moves, else the first My plan item. The stages are in `core/domain/src/entity-lifecycle.ts`: ephemeral 💭, captured 📝, crystallizing 🔍, crystallized 🔒, manifesting 🔨, completed ✅, discarded 🗑️. Unsure: captured 📝.

Draw no board and no table of entities under the line.
