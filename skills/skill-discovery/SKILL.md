---
name: skill-discovery
description: "Filesystem-first local skill lookup and ranking from lev-skills inventory. Use when work, lev, or hubs need to discover installed skills without low-quality fallbacks."
skill_type: tool
category: process-find
primary_primitive: get
legacy_aliases: [discover-skills]
---

# skill-discovery

**Filesystem-first local skill lookup using `lev-skills` as the CLI and `~/.agents/skills-inventory.jsonl` as the file-resolution source of truth.**

This skill takes a task description and searches the local skills runtime. It resolves concrete `SKILL.md` files from the generated inventory at `~/.agents/skills-inventory.jsonl`, built from the live filesystem under `~/.agents/skills` + `~/.agents/skills-db`, then enriches ranking with `~/.agents/skill-graph.json` when graph metadata exists.

## Operational Rule

When this skill is selected for a task, run local discovery first:

```bash
lev-skills "<task description>" --json --limit=5
```

Use returned `local_path` values to load the relevant `SKILL.md` files. Do not look for a `skill-discovery` binary; `skill-discovery` is the skill name, not the command.

## Usage

```bash
# General lookup
lev-skills "I need to deploy a react app to AWS"

# JSON output
lev-skills "Scan my code for bugs" --json

# Canonical inventory output
lev-skills inventory --json

# Random eligible skill from the current rotation
lev-skills pick "ux research" --json

# Graph status
lev-skills graph stats --json

# Rebuild graph, then rebuild inventory
lev-skills graph rebuild --verify
```

## How it works

1. **Inventory build**: `lev-skills inventory` scans active skills + catalog skills, writes `~/.agents/skills-inventory.jsonl`, and merges lifecycle/usage metadata from `~/.agents/skills-state.json`.
2. **Graph enrichment**: `lev-skills` reads `~/.agents/skill-graph.json` and joins skill nodes by normalized skill name to add `skill_uri`, `lane`, graph lifecycle, graph degree, and graph-neighbor signals.
3. **Deterministic ranking**: `lev-skills discover` tokenizes the query, scores exact metadata/tag/path/graph matches, and hides archived/backlog/incubating buckets by default.
4. **Graph rebuild**: `lev-skills graph rebuild` runs `~/lev/workshop/pocs/skill-graph/seed.py`, writes `~/.agents/skill-graph.json`, exports GraphML from the graph builder, then rebuilds `~/.agents/skills-inventory.jsonl`.
5. **No fallback policy**: If local discovery is weak or empty, report that directly. Do not recommend external discovery tools from this skill.
6. **QMD boundary**: `discover` does not query `qmd`. `qmd` is only touched by the explicit `lev-skills refresh` command.
