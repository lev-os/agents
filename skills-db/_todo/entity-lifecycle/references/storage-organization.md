# Storage Organization

Where Leviathan entities live and how to query them.

## Directory Structure

```
~/.lev/                         # Global Lev directory
|-- ideas/                      # Captured ideas
|   |-- _archived/              # Archived ideas
|   |-- <idea-name>/            # Idea directory
|   |   |-- idea.yaml           # Idea metadata
|   |   |-- README.md           # Idea description
|   |   |-- scratchpad.md       # Working notes
|   |   |-- artifacts/          # Generated files
|   |   |-- poc/                # Proof of concept
|   |   +-- scripts/            # Automation scripts
|-- sessions/                   # Session transcripts
|-- context/                    # Active context files
|-- events.jsonl                # Global event stream
|-- pm/                         # Project management
|   |-- handoffs/               # Session handoffs
|   |-- designs/                # Design documents
|   |-- plans/                  # Execution plans
|   +-- research/               # Research notes
|-- workshop/                   # Active development
|   |-- poc/                    # Proof of concepts
|   |-- agent-loop/             # Agent experiments
|   +-- dspy/                   # DSPy experiments
|-- intake/                     # Incoming content
|-- cache/                      # Ephemeral cache
|-- logs/                       # Runtime logs
+-- store/                      # Key-value store

.beads/                         # BD issue tracker (project-local)
|-- issues.jsonl                # Issue database
+-- last-touched                # Recent activity

~/.config/lev/                  # Global configuration
|-- config.yaml                 # Global config
|-- projects.yaml               # Registered projects
|-- events.jsonl                # Config-level events
+-- logs/                       # Daemon logs
```

## Entity Locations

### Ideas

**Location:** `~/.lev/ideas/<idea-name>/`

```yaml
# idea.yaml structure
id: async-execution
title: "Async Execution Model"
status: captured   # captured|classified|crystallizing|crystallized|manifesting|completed
handler: code
created: 2026-01-14T03:47:00Z
source: whatsapp
tags: [ralph, async, architecture]

description: |
  Problem description and solution outline...

notes:
  - Key insight 1
  - Key insight 2
```

**Query ideas:**
```bash
# List all ideas
ls ~/.lev/ideas/

# Find by status
for d in ~/.lev/ideas/*/; do
  grep -l "status: crystallizing" "$d/idea.yaml" 2>/dev/null && basename "$d"
done

# List with status
ls ~/.lev/ideas/*/idea.yaml | xargs -I{} sh -c 'echo "$(dirname {} | xargs basename): $(grep status {} | cut -d: -f2)"'
```

### Sessions

**Location:** `~/.lev/sessions/<session-name>/`

**Query sessions:**
```bash
# List recent sessions
ls -lt ~/.lev/sessions/

# Find by topic in handoffs
grep -l "topic-name" ~/.lev/pm/handoffs/*.md
```

### Beads (BD Issues)

**Location:** `.beads/issues.jsonl` (project-local)

**Query beads:**
```bash
# Ready work (unblocked)
bd ready

# All open issues
bd list --status open

# Blocked issues
bd blocked

# Search by title
bd list --search "lifecycle"

# JSON output for scripting
bd list --json | jq '.[] | select(.status == "in_progress")'
```

### Handoffs

**Location:** `.lev/pm/handoffs/` or `~/.lev/pm/handoffs/`

**Naming convention:** `{YYYYMMDD-HHMMSS}-{topic}.md`

**Query handoffs:**
```bash
# Most recent handoff
ls -t .lev/pm/handoffs/*.md | head -1

# Last 5 handoffs
ls -t .lev/pm/handoffs/*.md | head -5

# Search by topic
grep -l "lifecycle" .lev/pm/handoffs/*.md
```

### Docs

**Location:** `docs/` (project-local)

**Query docs:**
```bash
# All markdown docs
find docs/ -name "*.md"

# ADRs
ls docs/adr/

# Search content
grep -r "pattern" docs/
```

### PM Artifacts

**Location:** `pm/` or `.lev/pm/`

**Query PM:**
```bash
# Active plans
ls pm/tasks/

# Designs
ls .lev/pm/designs/

# Research
ls .lev/pm/research/
```

## Dashboard View {#dashboard}

The `/dashboard` command aggregates status across all entity types.

### Dashboard Implementation

```bash
#!/bin/bash
# Dashboard script

echo "=== LEVIATHAN DASHBOARD ==="
echo ""

# IDEAS
echo "IDEAS (from ~/.lev/ideas/)"
captured=$(ls ~/.lev/ideas/*/idea.yaml 2>/dev/null | xargs grep -l "status: captured" 2>/dev/null | wc -l | tr -d ' ')
crystallizing=$(ls ~/.lev/ideas/*/idea.yaml 2>/dev/null | xargs grep -l "status: crystallizing" 2>/dev/null | wc -l | tr -d ' ')
manifesting=$(ls ~/.lev/ideas/*/idea.yaml 2>/dev/null | xargs grep -l "status: manifesting" 2>/dev/null | wc -l | tr -d ' ')
echo "  Captured: $captured | Crystallizing: $crystallizing | Manifesting: $manifesting"
echo ""

# BEADS
echo "BEADS (from bd)"
if command -v bd &> /dev/null; then
  open=$(bd list --status open --json 2>/dev/null | jq length 2>/dev/null || echo "?")
  in_progress=$(bd list --status in_progress --json 2>/dev/null | jq length 2>/dev/null || echo "?")
  ready=$(bd ready --json 2>/dev/null | jq -r '.[].id' 2>/dev/null | head -5 | tr '\n' ', ' | sed 's/,$//')
  echo "  Open: $open | In Progress: $in_progress"
  echo "  Ready: ${ready:-none}"
else
  echo "  bd not available"
fi
echo ""

# HANDOFFS
echo "HANDOFFS (from .lev/pm/handoffs/)"
if [ -d ".lev/pm/handoffs" ]; then
  count=$(ls .lev/pm/handoffs/*.md 2>/dev/null | wc -l | tr -d ' ')
  latest=$(ls -t .lev/pm/handoffs/*.md 2>/dev/null | head -1 | xargs basename 2>/dev/null)
  echo "  Count: $count | Latest: ${latest:-none}"
else
  echo "  No handoffs directory"
fi
echo ""

# EVENTS
echo "EVENTS (from ~/.lev/events.jsonl)"
if [ -f ~/.lev/events.jsonl ]; then
  total=$(wc -l < ~/.lev/events.jsonl | tr -d ' ')
  errors=$(grep -c '"phase":"error"' ~/.lev/events.jsonl 2>/dev/null || echo "0")
  echo "  Total: $total | Errors: $errors"
else
  echo "  No events file"
fi
```

### Dashboard Output Example

```
=== LEVIATHAN DASHBOARD ===

IDEAS (from ~/.lev/ideas/)
  Captured: 5 | Crystallizing: 3 | Manifesting: 2

BEADS (from bd)
  Open: 12 | In Progress: 4
  Ready: lev-001b, lev-08of, lev-0kzs

HANDOFFS (from .lev/pm/handoffs/)
  Count: 25 | Latest: 20260115-071500-openprose-claude-prose-architecture.md

EVENTS (from ~/.lev/events.jsonl)
  Total: 1247 | Errors: 3
```

## Query Patterns {#query}

### Ideas by Status

```bash
# All crystallized ideas
ls ~/.lev/ideas/*/idea.yaml | \
  xargs grep -l "status: crystallized" | \
  xargs -I{} dirname {} | \
  xargs -I{} basename {}
```

### Beads by Priority

```bash
# P0 (critical) issues
bd list --json | jq '.[] | select(.priority == 0)'

# High priority ready
bd ready --json | jq '.[] | select(.priority <= 1)'
```

### Recent Events

```bash
# Last 10 events
tail -10 ~/.lev/events.jsonl | jq '.'

# Last error
grep '"phase":"error"' ~/.lev/events.jsonl | tail -1 | jq '.'

# Events for specific entity
jq 'select(.entity == "idea")' ~/.lev/events.jsonl | tail -5
```

### Cross-Entity Search

```bash
# Find all references to a topic
{
  grep -l "lifecycle" ~/.lev/ideas/*/README.md 2>/dev/null
  grep -l "lifecycle" .lev/pm/handoffs/*.md 2>/dev/null
  bd list --search "lifecycle" --json | jq -r '.[].id'
} | sort -u
```

## Storage Best Practices

1. **Ideas**: One directory per idea, include `idea.yaml` + `README.md`
2. **Handoffs**: Timestamp prefix for sorting, descriptive topic
3. **Events**: Append-only JSONL, rotate when > 10MB
4. **Beads**: Use BD CLI, don't edit `.beads/` directly
5. **Archive**: Move completed items to `_archived/` subdirectories

## Storage Locations Summary {#locations}

| Entity | Location | Query Tool |
|--------|----------|------------|
| Ideas | `~/.lev/ideas/` | `ls`, `grep`, `find` |
| Sessions | `~/.lev/sessions/` | `ls -t` |
| Beads | `.beads/issues.jsonl` | `bd list`, `bd ready` |
| Handoffs | `.lev/pm/handoffs/` | `ls -t`, `grep` |
| Docs | `docs/` | `find`, `grep -r` |
| PM | `pm/`, `.lev/pm/` | `ls`, `find` |
| Events | `~/.lev/events.jsonl` | `jq`, `grep` |
| Config | `~/.config/lev/` | `cat`, `yq` |

---

*For state transitions, see `phase-transitions.md`. For action logging, see `entity-actions.md`.*
