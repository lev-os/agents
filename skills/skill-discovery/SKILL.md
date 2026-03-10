---
name: skill-discovery
description: "[WHAT] Local skills runtime lookup over qmd collections whose names start with `skills`.\n[HOW] Uses cm + qmd, prefers canonical and skills-db hits in post-processing, and only recommends `find-skills` when local results are low quality.\n[WHEN] Used implicitly by `work`, `lev`, and runtime hubs when locating local capabilities."
skill_type: tool
category: process-find
primary_primitive: get
legacy_aliases: [discover-skills]
---

# skill-discovery

**Dual-layer local skill lookup using `cm` context and `qmd` semantic search.**

This skill takes a task description and searches over the local skills runtime, preferring `~/.agents/skills` and `~/.agents/skills-db` while still being able to read every qmd collection whose name begins with `skills`.

## Usage

```bash
# General lookup
skill-discovery "I need to deploy a react app to AWS"

# JSON output
skill-discovery "Scan my code for bugs" --json
```

## How it works

1. **Layer 1 (CM Context)**: Checks against the curated `cm` playbook for high-signal matches.
2. **Layer 2 (QMD Semantic)**: Runs qmd over every collection matching `skills*`.
3. **Post-processing**: Boosts canonical and `skills-db` hits, prefers actual `SKILL.md` files over readmes/indexes, hides maintenance buckets, and normalizes qmd URIs back to local paths.
4. **Fallback policy**: Only recommend `find-skills` when the local discovery quality is low.
