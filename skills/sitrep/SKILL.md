---
name: sitrep
description: "Freestyle dashboard. Projects the lifecycle_trigger stream into a live view of entities + fidelity + memory + next actions. The /lev dashboard for mid-flow work. Invoke as /sitrep (alias: /status)."
triggers:
  - sitrep
  - siterep
  - status
output_template: hud
---

# /sitrep — Freestyle Dashboard (Stream Projection)

**/sitrep is a PROJECTION, not a writer.** It reads the lifecycle trigger stream and renders current state. Never mutates. Never archaeology.

Source of truth: `.lev/pm/workstreams/*/triggers/*.yaml` (lifecycle_trigger.v1)

Schema ref: `.lev/pm/proposals/20260415-lifecycle-trigger-envelope.yaml`

## When to Use

- Mid-flow: "what's happening across my queue right now?"
- After a /capture or /close tick: "did everything land?"
- Before /work: "what should I pick up?"
- After long thinking: "what's in memory vs on disk?"

Distinct from /capture (which WRITES and sweeps) — /sitrep only READS.

## Protocol

### 1. Read the stream (cheap, no archaeology)

```
Default scope: the active workstream's triggers/ dir.
  → .lev/pm/workstreams/<active-ws>/triggers/*.yaml
  → Read only the tail (last N triggers, default 20)
  → Parse cursor + outputs.items + outputs.gates + metrics

Wider scope (on request):
  → /sitrep --all  reads all workstreams
  → /sitrep --ws <id>  targets one ws
```

**Do NOT** read: handoffs/ (archaeology), workstream.yaml full file (archive policy), git log (not the source of truth for state). These are fallbacks only when no trigger stream exists yet.

### 2. Project the view

Render 5 sections from the parsed triggers:

#### A. Exec brief (current result — always present)

Mirrors /capture's "Exec Menu" shape so every verb ends the same way:

```
## /sitrep — {ws-id} — {timestamp}

### Current result
- Last verb: {cursor.last_verb} at {cursor.last_at} (commit {cursor.last_commit})
- Gates: {N_passed}/{N_total} passed · drift={value} · fidelity_avg={value}
- Sealed: {true|false}  (true if cursor.next_verb == null)
```

#### B. Active entities (what's moving)

From `outputs.items` across recent triggers, grouped by state:

| Symbol | State | Source |
|---|---|---|
| ⚡ | executing | last trigger was /exec, cursor.next_verb was set |
| 📥 | capturing | last trigger was /capture |
| 🔍 | expanding | last trigger verb was `expand` emote |
| 🧹 | collapsing | last trigger verb was `collapse` emote |
| ⏸️ | blocked | cursor.blocker != null |
| ❓ | question | last trigger was `question` emote |
| ✅ | done this session | cursor.next_verb == null (sealed) |

Show max 5 items. Rest go to queue count.

#### C. Memory state (freestyle — the user's feedback)

What's in-memory vs on-disk. From the most recent /capture trigger's `outputs.items` (after /close absorbs /capture, this is just the latest trigger's items).

```
### Memory state
- In-memory: {count} items below fidelity gate (0.8)
- Captured: {count} items shipped to disk
- Blocked: {count} items awaiting decision
```

Fidelity comes from `metrics.fidelity` per trigger. If the value is missing OR the trigger has `outputs.items != []` on a /close, flag as **⚠ theater** — the Step 0 gate was bypassed.

#### D. Next actions (from cursor.next_input + recommend)

```
### Next (from tail trigger)
1. {cursor.next_verb} {cursor.next_input}
2+. {recommend[*]} where verdict != monitor
```

Matches /capture's Exec Menu pattern — max 5 items, rest queued.

#### E. Decisions Needed (if any blockers)

```
### Decisions Needed ({count})
1. {entity}: {blocker} — since {cursor.last_at}
```

When ALL items blocked: auto-suggest `/interview` or `/expand://<entity>` for the top one.

### 3. Inline emote dispatch (new — per user feedback)

Some actions are inline-only. /sitrep supports shortcuts on entities in the rendered view:

```
/sitrep then: expand 2          → fire expand://<item-2-ref> (no full verb ceremony)
/sitrep then: collapse 4,5,6    → fire collapse:// on items 4,5,6 in batch
/sitrep then: admit 3           → fire admission:// on item 3
```

Inline emotes run a flow (flow://lifecycle/<emote>) but DON'T require /close's full ceremony. They emit a trigger each. The stream still grows. The ceremony scales with stakes.

**Heuristic:** inline for emote verbs (expand, collapse, admit, question). Full ceremony for lifecycle verbs (close, propose, exec, handoff).

## Rules

- **Projection only.** /sitrep never writes, never commits, never pushes.
- **Cheap read.** Tail the stream. Don't re-compute from git or handoffs.
- **Bucketed.** 5 active, 5 next actions, rest as counts.
- **Theater check.** Any /close trigger with items != [] gets a ⚠ flag. Non-negotiable.
- **Fallback.** If no triggers/ dir exists yet, fall back to the old TaskList + workstream.yaml scan — but print a hint: `"no trigger stream — run /close to start the stream"`.
- **Graph footer.** Always end with HUD line from `~/.claude/skills/_shared/graph-footer.md`.

## Exec Menu (same pattern as /capture — this is the convergence)

Every read-only verb ends with a concrete exec menu:

```
### Exec Menu (N of M)

1. [item] → verb: /exec  flow: ralph       effort: S  unblocks: #3,#7
2. [item] → verb: /propose                  effort: XS unblocks: #5
...

Queue: N more items (bucketed by priority)

Inline shortcuts:
  expand <n>    collapse <n>    admit <n>
```

## Relationship to /capture

| /capture | /sitrep |
|---|---|
| Writes triggers | Reads triggers |
| Mutates state | Projects state |
| Absorbs in-memory items to disk | Surfaces what's on disk |
| Ends with Exec Menu | Ends with Exec Menu (same shape) |
| Fidelity scoring (inline) | Fidelity surfacing (from stream) |

After /close absorbs /capture, /sitrep becomes the primary read interface to lifecycle state. /capture becomes the fast-write path.

## Aliases

- `/sitrep` = full dashboard (canonical)
- `/siterep` = legacy alias
- `/status` = same
- `/sitrep --brief` = exec brief + next 3 actions only (3 lines)
- `/sitrep --all` = all workstreams, not just active
- `/sitrep --ws <id>` = target one workstream

## Related

- `/capture` — mutation path (writes trigger with sweep)
- `/close` — sealing path (writes close trigger, absorbs capture)
- `/work` — router (may call /sitrep before routing)
- Schema: `.lev/pm/proposals/20260415-lifecycle-trigger-envelope.yaml`
- Stream dir: `.lev/pm/workstreams/*/triggers/`
