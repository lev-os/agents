# Task Tracker Adapter (bd | br | td)

The work skill is backend-agnostic for task tracking. Detect which tool is available and route through the adapter. **Preference order: bd > br > td.**

## Detection

```bash
# Prefer bd (Go, auto-commit) > br (Rust, non-invasive) > td (Python, lightweight)
command -v bd && TRACKER=bd || { command -v br && TRACKER=br || { command -v td && TRACKER=td || TRACKER=none; }; }
```

## Operation Map

| Operation | bd (preferred) | br (supported) | td (lightweight) |
|-----------|---------------|-------------|------------------|
| **create** | `bd create --title="..." --type=task` | `br create --title="..." --type=task` | `td add "..."` |
| **list** | `bd list --status=open` | `br list --status=open` | `td` / `td -g {group}` |
| **search** | `bd search "{kw}"` | `br search "{kw}"` | N/A (grep local) |
| **show** | `bd show {id}` | `br show {id}` | `td {id}` |
| **update** | `bd update {id} --status=X` | `br update {id} --status=X` | `td {id} edit` |
| **close** | `bd close {id}` | `br close {id}` | `td {id} complete` |
| **deps** | `bd dep add {p} {c}` | `br dep add {p} {c}` | N/A |
| **ready** | `bd ready` | `br ready` | N/A |
| **sync** | `bd sync` (auto-git) | `br sync --flush-only` + manual git | N/A (local SQLite) |
| **epic** | `bd epic {id}` | `br epic {id}` | N/A (use groups: `td -g {epic}`) |

## Behavioral Differences

- **bd sync** auto-commits and pushes — no manual git needed
- **br sync** exports JSONL only — you must `git add .beads/ && git commit` manually
- **td** has no sync/deps/ready — degrade gracefully (skip dep gates, no ready filtering)

## Degradation Rules

When `td` is the only backend:
- Skip dependency-based gates (no `dep` support)
- Skip `ready` filtering (list all open instead)
- Map groups to epics (`td -g {epic-name}`)
- Search falls back to `td` + grep

When no tracker is available (`TRACKER=none`):
- Continue without task integration; note in artifact
- Prior art check skips BD/tracker queries
