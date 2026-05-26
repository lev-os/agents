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

When this skill is selected for a task, translate the user's intent into a short, broad search request before running local discovery:

```bash
lev-skills "<one sentence request with broad keywords>" --json --limit=5
```

Use returned `local_path` values to load the relevant `SKILL.md` files. Do not look for a `skill-discovery` binary; `skill-discovery` is the skill name, not the command.

Treat `lev-skills` as a basic lexical search over skill metadata, not semantic retrieval. Prefer clear nouns, verbs, product names, and known tool terms over chat phrasing. For example, turn "the CI is red after merge" into `github actions ci workflow failure fix`.

If the first query is weak, run a small query set instead of overfitting one sentence:

```bash
lev-skills "github actions ci workflow failure fix" --json --limit=5
lev-skills "pull request checks pipeline yaml release automation" --json --limit=5
lev-skills "debug test failure root cause bug fix" --json --limit=5
```

If discovery still looks wrong, inspect the local corpus directly with `rg`:

```bash
rg -n "github actions|ci|workflow|pipeline" ~/.agents/skills ~/.agents/skills-db
```

## Usage

```bash
# General lookup
lev-skills "I need to deploy a react app to AWS"

# JSON output
lev-skills "Scan my code for bugs" --json

# Broad-keyword lookup
lev-skills "github actions ci workflow failure fix" --json --limit=5

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
5. **Query discipline**: Agents should decompose intent into a few broad keyword queries, then load the best returned `local_path` files.
6. **Direct corpus inspection**: If ranked results are weak, use `rg` against `~/.agents/skills` and `~/.agents/skills-db` to inspect real skill text.
7. **No fallback policy**: If local discovery and direct corpus inspection are weak or empty, report that directly. Do not recommend external discovery tools from this skill.
