# Lifecycle Integration

After building entities, integrate them with BD tracking and .leann indexing for full observability.

## Build Lifecycle

```
BUILD                    TRACK                    INDEX                    TEST
┌─────────┐             ┌─────────┐              ┌─────────┐              ┌─────────┐
│ Create  │ ──────────→ │ BD Bead │ ───────────→ │ .leann  │ ───────────→ │ Verify  │
│ Entity  │             │         │              │         │              │         │
└─────────┘             └─────────┘              └─────────┘              └─────────┘
```

## BD (Beads) Integration

### Create Bead for Build Work

```bash
# Create bead when starting build
bd create "Build: lev-my-skill" -t feature -p 2

# Output: lev-xxxx (bead ID)
```

### Link Entity to Bead

Add bead reference in entity metadata:

```yaml
# SKILL.md frontmatter
---
name: my-skill
description: ...
version: 1.0.0
bd_issue: lev-xxxx    # Link to tracking bead
---
```

### Update Bead on Completion

```bash
# Mark complete
bd update lev-xxxx --status=closed

# Add notes
bd comment lev-xxxx "Skill created at ~/.claude/skills/my-skill/"
```

### Bead Types for Builds

| Entity Type | BD Type | Priority |
|-------------|---------|----------|
| Skill | feature | 2 |
| Command | feature | 2 |
| Package | epic | 1 |
| Adapter | feature | 2 |

## .leann Indexing

LEANN (Latent Embedding Approximate Nearest Neighbor) provides semantic search over generated entities.

### Index New Skill

```bash
# Add skill to index
lev index add ~/.claude/skills/my-skill/

# Verify indexing
lev get "my-skill description keywords"
```

### Index New Command

Commands are indexed automatically when the package builds. Manual indexing:

```bash
# Index command file
lev index add core/my-pkg/src/commands/my-command.ts
```

### Index New Package

```bash
# Index entire package
lev index add core/my-pkg/

# Or just docs
lev index add core/my-pkg/README.md core/my-pkg/docs/
```

### Verify Indexing

```bash
# Search to confirm index entry
lev get "my-skill purpose"

# Should return the skill in results
```

## Full Build Workflow

### 1. Start Tracking

```bash
# Create bead for the work
bd create "Build: my-skill" -t feature
# → lev-abc1
```

### 2. Build Entity

```bash
# Generate skill
lev build skill --name my-skill --description "Does X"

# Or manually create
mkdir -p ~/.claude/skills/my-skill
# Write SKILL.md, references/, etc.
```

### 3. Add BD Reference

```yaml
# ~/.claude/skills/my-skill/SKILL.md
---
name: my-skill
bd_issue: lev-abc1
---
```

### 4. Index for Search

```bash
lev index add ~/.claude/skills/my-skill/
```

### 5. Test

```bash
# Test skill invocation
# "Use the my-skill skill to..."

# Test search visibility
lev get "my-skill"
```

### 6. Close Bead

```bash
bd update lev-abc1 --status=closed
bd comment lev-abc1 "Skill deployed and indexed"
```

## Automation Script

For consistent builds, use this pattern:

```bash
#!/bin/bash
# build-skill.sh

NAME=$1
DESC=$2

# 1. Create bead
BEAD=$(bd create "Build: $NAME" -t feature -p 2 | grep -oE 'lev-[a-z0-9]+')
echo "Created bead: $BEAD"

# 2. Build skill
lev build skill --name "$NAME" --description "$DESC" --bd-issue "$BEAD"

# 3. Index
lev index add ~/.claude/skills/$NAME/

# 4. Test search
lev get "$NAME"

# 5. Close bead
bd update $BEAD --status=closed

echo "Skill $NAME built, indexed, and tracked"
```

## Event Emission

Builds emit CloudEvents to `.lev/events.jsonl`:

```json
{
  "type": "lev.build.skill.created",
  "source": "lev-builder",
  "time": "2026-01-15T00:00:00Z",
  "data": {
    "name": "my-skill",
    "location": "~/.claude/skills/my-skill/",
    "bd_issue": "lev-abc1"
  }
}
```

Query events:

```bash
# Recent build events
cat .lev/events.jsonl | jq 'select(.type | startswith("lev.build"))'
```

## Integration with CI

For package builds in CI:

```yaml
# .github/workflows/build.yml
jobs:
  build:
    steps:
      - name: Build package
        run: pnpm build

      - name: Update index
        run: lev index refresh

      - name: Verify search
        run: lev get "package-name" | grep -q "package-name"
```

## BD Lifecycle States

| State | Meaning | When |
|-------|---------|------|
| open | Work started | bd create |
| in_progress | Actively building | bd update --status=in_progress |
| review | Ready for review | bd update --status=review |
| closed | Complete | bd update --status=closed |
| blocked | Waiting on dependency | bd update --status=blocked |

## Index Scopes

```bash
# Search all indexed content
lev get "query"

# Search specific scopes
lev get "query" --scope docs
lev get "query" --scope skills
lev get "query" --scope code
```

## Troubleshooting

### Entity Not Appearing in Search

```bash
# Check if indexed
lev index status ~/.claude/skills/my-skill/

# Force re-index
lev index add --force ~/.claude/skills/my-skill/
```

### BD Bead Not Linked

```bash
# Check bead exists
bd show lev-xxxx

# Update entity metadata manually
# Add bd_issue: lev-xxxx to frontmatter
```

### Events Not Recording

```bash
# Check events file exists
ls -la .lev/events.jsonl

# Verify write permissions
touch .lev/events.jsonl
```

## Source Reference

- BD skill: `~/.claude/skills/bd/SKILL.md`
- Index skill: `~/.claude/skills/lev-index/SKILL.md`
- Events: `docs/adr/060-config-cascade-pattern.md` (XDG paths)
