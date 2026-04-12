---
name: ws
description: "Workstream operations. Scan, list, resume, find, merge, branch, untangle. Stopgap until workstreams are graph ops."
---

# /ws — Workstream Operations

Quick workstream management from conversation. Wraps `.lev/pm/workstreams/` YAML state.

## Commands

```
/ws                    # scan all workstreams (status + phase)
/ws list               # same as /ws
/ws find <query>       # search workstreams + handoffs by keyword
/ws show <id>          # show full workstream state
/ws resume <id>        # load handoff, diff repo, continue
/ws merge <a> <b>      # combine two workstream lineages
/ws branch <id> <name> # fork a workstream
/ws untangle           # run detangle protocol (levmail-based)
```

## How It Works

### /ws (scan)

Read all `.lev/pm/workstreams/*/state/workstream.yaml` and output:

```
WORKSTREAMS
───────────
dna-cascade-dogfood    exec   active   owner:chidev
herenow-content        exec   active   owner:chidev
lev-now-genui          exec   active   owner:chidev
web-summit-gtm-docs    research active owner:chidev
```

### /ws find <query>

Search across:
- `.lev/pm/workstreams/*/state/workstream.yaml` (titles, objectives)
- `.lev/pm/handoffs/*.md` (frontmatter titles)
- `.lev/pm/plans/plan-*.md` (frontmatter titles)
- `.lev/mail/*.md` (subjects)

Return matches with path + workstream association.

### /ws show <id>

Read `.lev/pm/workstreams/<id>/state/workstream.yaml` and format:
- Title, objective, phase, status, owner
- Decision refs
- Latest extension/session block
- Associated handoffs (search by workstream field)
- Open beads (if bd available)

### /ws resume <id>

1. Find latest handoff for workstream
2. Diff repo state since handoff date
3. Load handoff's "Next Agent Brief"
4. Report: what changed, what's open, proposed next verb

### /ws untangle

Run the detangle protocol from `.lev/mail/20260410-detangle-protocol-all-agents.md`:
1. Each agent dumps nuggets via levmail
2. Read all dumps
3. Claim lanes
4. Mail handoffs
5. Update handoffs with detangle_sync

### /ws merge <a> <b>

Combine two workstream YAML files. Keep the one with more sessions as primary.
Merge extensions, decision_refs, follow_up_refs. Flag conflicts for human review.

### /ws branch <id> <name>

Copy workstream YAML to new id. Update provenance_ref to point at parent.
Set phase to current parent phase. Clear extensions (fresh start).

## Data Sources

- `.lev/pm/workstreams/*/state/workstream.yaml`
- `.lev/pm/handoffs/*.md`
- `.lev/pm/plans/plan-*.md`
- `.lev/mail/*.md`
- `levmail` CLI at `~/.local/bin/levmail`

## Graph Footer

After every /ws command, append the shared graph footer from `~/.claude/skills/_shared/graph-footer.md`.

## Future

When workstreams become graph ops, /ws becomes a thin projection over graph queries. The YAML files become materialized views, not the source of truth. Until then, YAML is truth.
