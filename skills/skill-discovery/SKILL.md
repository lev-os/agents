---
name: skill-discovery
description: "[WHAT] Local skills runtime lookup over the canonical Leviathan skills inventory.\n[HOW] Uses `~/.agents/lev-skills.sh` + `~/.agents/skills-inventory.jsonl` as the source of truth, merges lifecycle and usage metadata, and only recommends `find-skills` when local results are low quality.\n[WHEN] Used implicitly by `work`, `lev`, and runtime hubs when locating local capabilities."
skill_type: tool
category: process-find
primary_primitive: get
legacy_aliases: [discover-skills]
---

# skill-discovery

**Filesystem-first local skill lookup using `~/.agents/lev-skills.sh` inventory as the source of truth, with optional history/lifecycle metadata.**

This skill takes a task description and searches over the local skills runtime using the generated inventory at `~/.agents/skills-inventory.jsonl`, built from `~/.agents/lev-skills.sh` and the live filesystem under `~/.agents/skills` + `~/.agents/skills-db`.

## Usage

```bash
# General lookup
skill-discovery "I need to deploy a react app to AWS"

# JSON output
skill-discovery "Scan my code for bugs" --json

# Canonical inventory output
lev-skills inventory --json

# Random eligible skill from the current rotation
lev-skills pick "ux research" --json
```

## How it works

1. **Inventory build**: `~/.agents/lev-skills.sh inventory` scans active skills + catalog skills, writes `~/.agents/skills-inventory.jsonl`, and merges lifecycle/usage metadata from `~/.agents/skills-state.json`.
2. **Deterministic ranking**: `skill-discovery` tokenizes the query, scores exact metadata/tag/path matches, and hides archived/backlog/incubating buckets by default.
3. **Lifecycle awareness**: active/core skills, experimental skills, and catalog-only skills stay separable via `lifecycle` + `rotation_role`.
4. **Fallback policy**: Only recommend `find-skills` when the local discovery quality is low.
