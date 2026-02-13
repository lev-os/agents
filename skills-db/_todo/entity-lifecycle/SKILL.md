---
name: entity-lifecycle
description: |
  Entity execution harness with 3-phase logging (pre/post/error), dashboard views,
  and lifecycle actions. Powers the /dashboard command. Use when executing entity
  operations, viewing entity status, or managing lifecycle transitions.

  **Activation:** /dashboard, entity status, move entity, promote idea, close bead
version: 1.0.0
extends: lev-lifecycle
tools:
  - bd (beads issue tracker)
  - jq (JSONL queries)
  - lev lifecycle (CLI)
storage:
  ideas: ~/.lev/ideas/
  sessions: ~/.lev/sessions/
  beads: .beads/issues.jsonl
  docs: docs/
  pm: pm/, .lev/pm/
  events: ~/.lev/events.jsonl
  handoffs: .lev/pm/handoffs/
---

# Entity Lifecycle

Execution harness and dashboard for Leviathan entities. Routes to specialized references based on operation type.

## Decision Tree

```
What entity operation?
|
+-> VIEW STATUS
|   +-> /dashboard               -> references/storage-organization.md#dashboard
|   +-> entity status <type>     -> references/storage-organization.md#query
|   +-> list ideas|beads|docs    -> references/storage-organization.md#locations
|
+-> EXECUTE ACTION
|   +-> promote idea             -> references/entity-actions.md#promote
|   +-> close bead               -> references/entity-actions.md#close
|   +-> archive session          -> references/entity-actions.md#archive
|   +-> move entity              -> references/entity-actions.md#move
|
+-> LIFECYCLE TRANSITION
|   +-> transition <id> --to <state>  -> references/phase-transitions.md
|   +-> validate gate            -> references/phase-transitions.md#gates
|   +-> auto-transition          -> references/phase-transitions.md#triggers
|
+-> EXECUTION HARNESS
    +-> inline execution         -> references/harness-pattern.md#inline
    +-> detached job             -> references/harness-pattern.md#detached
    +-> background task          -> references/harness-pattern.md#background
```

## Quick Reference

| Command | Description | Reference |
|---------|-------------|-----------|
| `/dashboard` | Entity overview dashboard | storage-organization.md |
| `bd ready` | Ready beads (unblocked) | BD skill |
| `lev lifecycle show <id>` | Entity details | entity-actions.md |
| `promote idea <id>` | Idea -> BD task | entity-actions.md#promote |
| `close bead <id>` | Close with reason | entity-actions.md#close |
| `move <id> --to <state>` | Manual transition | phase-transitions.md |

## State Machine Summary

```
IDEA:    captured -> classified -> crystallizing -> crystallized -> manifesting -> completed
SESSION: active -> paused -> continued | compacting -> compacted -> archived
BEAD:    open -> in_progress -> blocked | completed
DOC:     draft -> review -> published | archived
SYNTH:   spawned -> active -> promoting -> system | archived
```

## Entity Types

| Type | Storage | Query | Actions |
|------|---------|-------|---------|
| Ideas | `~/.lev/ideas/` | `ls ~/.lev/ideas/` | promote, crystallize, archive |
| Sessions | `~/.lev/sessions/` | `ls ~/.lev/sessions/` | handoff, continue, archive |
| Beads | `.beads/issues.jsonl` | `bd list`, `bd ready` | close, update, dep add |
| Docs | `docs/`, project-local | `find docs/ -name "*.md"` | publish, archive |
| PM | `pm/`, `.lev/pm/` | `ls .lev/pm/handoffs/` | archive, reference |
| Handoffs | `.lev/pm/handoffs/` | `ls -t .lev/pm/handoffs/` | continue, archive |

## Execution Pattern (3-Phase)

All entity operations follow the pre/post/error pattern:

```
PRE  -> emit event, validate inputs, check dependencies
EXEC -> perform action, track duration
POST -> emit success event, trigger downstream
ERROR -> escalate level, emit error event, suggest recovery
```

See `references/harness-pattern.md` for full execution mechanics.

## Dashboard View (`/dashboard`)

Quick status across all entity types:

```bash
# IDEAS (from ~/.lev/ideas/)
Ideas: 5 captured, 3 crystallizing, 2 manifesting

# BEADS (from bd)
Beads: 12 open, 4 in_progress, 2 blocked
  Ready: lev-001b, lev-08of, lev-0kzs

# SESSIONS (from handoffs)
Sessions: 1 active, 3 paused (last: 20260115-skills-audit)

# DOCS (from docs/)
Docs: 15 published, 2 draft
```

## Integration

- **lev-lifecycle** - State machine definitions (parent skill)
- **bd** - Bead tracking and queries
- **momentum-anchor** - Energy state on handoff
- **lev-learn** - Pattern analysis from events

## References

Load based on operation type:

- **references/harness-pattern.md** - Execution modes, job lifecycle
- **references/entity-actions.md** - Pre/post/error logging, action handlers
- **references/storage-organization.md** - Where entities live, dashboard queries
- **references/phase-transitions.md** - Validation gates, auto-triggers

---

*For state machine details and session continuity, see the parent `lev-lifecycle` skill.*
