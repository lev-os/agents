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
```

## How it works

1. **Inventory build**: `lev-skills inventory` scans active skills + catalog skills, writes `~/.agents/skills-inventory.jsonl`, and merges lifecycle/usage metadata from `~/.agents/skills-state.json`.
2. **Graph enrichment**: `lev-skills` reads `~/.agents/skill-graph.json` and joins skill nodes by normalized skill name to add `skill_uri`, `lane`, graph lifecycle, graph degree, and graph-neighbor signals.
3. **Deterministic ranking**: `lev-skills discover` tokenizes the query, scores exact metadata/tag/path/graph matches, and hides archived/backlog/incubating buckets by default.
4. **No fallback policy**: If local discovery is weak or empty, report that directly. Do not recommend external discovery tools from this skill.
5. **QMD boundary**: `discover` does not query `qmd`. `qmd` is only touched by the explicit `lev-skills refresh` command.
