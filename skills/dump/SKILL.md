---
name: dump
description: "Brain dump mode. Runs /capture on everything, auto /research + /prior-art per topic, dispatches shovel-ready items to /exec, and /propose's the rest. Nothing should remain in memory."
---

# /dump — Brain Dump → Auto-Research → Exec / Propose

One command. You talk, it captures, researches, and routes every item to a durable next state.

## What It Does

```
/dump                     # process everything in current conversation
/dump <topic>             # focused dump on one topic
/dump --dry-run           # show what WOULD be captured without filing
```

## The Pipeline

```
BRAIN DUMP (you talk)
    │
    ▼
/capture (inventory + classify)
    │ for each in-memory item:
    ▼
/prior-art (smart — 2-3 queries per topic, not exhaustive)
    │ found existing home? → route there
    │ no home? → continue
    ▼
/research (if topic needs evidence gathering)
    │ evidence gathered
    ▼
/exec (if item is shovel-ready)
    │ execution started or verifier-bound batch prepared
    ▼
/propose (everything else that is concrete but not shovel-ready)
    │ dna.yaml + execution.yaml written
    ▼
DECISION POINT
    keep | monitor | execute | reject
```

## How "Smart" Research Works

NOT exhaustive. Per topic, the skill:

1. **Prior-art probe** (3 queries max):
   - Exact phrase in `.lev/pm/` and `docs/`
   - Synonym/adjacent concept search
   - `cass search` for session history (if cass healthy)

2. **Route decision** (based on probe + execution readiness):
   - Found existing file → UPDATE that file (don't create new)
   - Found prior art in cass → surface the session reference
   - Shovel-ready with clear verifier/write scope → route to `/exec`
   - Concrete but not execution-ready → route to `/propose`
   - Found nothing → mark as genuinely new, continue to `/propose` or `/interview`

3. **Batch, don't serial**:
   - Group related topics together
   - One /prior-art probe covers 3 related topics if they share keywords
   - Parallel research agents for independent topics

## What It Produces

For each topic in the brain dump:

```yaml
# Per-topic output
topic: "hygiene as a lifecycle primitive"
prior_art_found:
  - plugins/core-sdlc/flows/hygiene.flow.yaml (existing)
  - plugins/core-sdlc/flows/weekly-hygiene.flow.yaml (existing)
route: UPDATE existing flows
ambiguity_score: 0.15  # below threshold
proposal: null  # routed to existing file, no new proposal needed
```

OR if genuinely new:

```yaml
topic: "background context chunking via haiku"
prior_art_found: []
route: NEW proposal
ambiguity_score: 0.35  # above threshold
action: needs /interview before /propose
```

## When to Use vs Other Verbs

| Situation | Use |
|---|---|
| Long brainstorm, many ideas, need to capture ALL | `/dump` |
| One specific idea, know what it is | `/propose` |
| Need more clarity on one topic | `/interview` |
| Just want to inventory without acting | `/capture` |
| Need deep research on one thing | `/research` |

`/dump` = `/capture` + `/prior-art` + `/research` + `/exec?` + `/propose?`. It's the "I just talked for 20 minutes, now process it all" button.

## Anti-Patterns

- **Don't dump and disappear** — `/dump` must leave nothing only in memory; every item needs a durable route
- **Don't dump 50 topics** — if > 10 topics, `/dump` should suggest splitting into workstreams
- **Don't skip prior-art** — the whole point is avoiding duplicate work. If you skip it, just use `/capture`

## Graph Footer

After /dump completes, append the shared graph footer from `~/.claude/skills/_shared/graph-footer.md`.

Show the stats table (from /capture format):

| Metric | Count |
|---|---|
| Total inventoried | N |
| Routed to existing files | N |
| New proposals created | N |
| Needs /interview first | N |
| Blocked | N |

## Relationship to /capture

`/capture` inventories and routes. `/dump` inventories, researches, then dispatches shovel-ready work to `/exec` and sends the rest to `/propose`. `/dump` calls `/capture` as its first step, then extends with research + durable routing.

```
/dump = /capture + for_each(topic => /prior-art → /research? → (/exec | /propose))
```

## Skill Builder Fast-Follow

This skill and all other new skills from this session (/ws, /mail, /capture, graph-footer) need a `/skill-builder` audit to ensure they meet skill standards (trigger types, metadata, test fixtures, etc.).
