---
name: skill-discovery
description: "[WHAT] Local contextual engine for dual-layer skill lookup.\n[HOW] Uses cm context and qmd semantic search to find relevant installed skills.\n[WHEN] Used implicitly by the `work` skill or when explicitly locating a local capability."
skill_type: tool
category: process-find
primary_primitive: get
legacy_aliases: [discover-skills]
---

# skill-discovery

**Dual-layer skill lookup using `cm` context and `qmd` semantic search.**

This skill takes a task description and searches over your local installed skills in `~/.agents/skills` and `skills-db` to figure out which tool is the right fit. 

## Usage

```bash
# General lookup
skill-discovery "I need to deploy a react app to AWS"

# JSON output
skill-discovery "Scan my code for bugs" --json
```

## How it works

1. **Layer 1 (CM Context)**: Checks against the curated `cm` playbook for high-signal matches.
2. **Layer 2 (QMD Semantic)**: Runs a vector+BM25 search via `qmd` across `skills-canonical`, `skills-db`, `skills-poc`, and `skills-polymath`.
3. **Synthesis**: Deduplicates and outputs the unique paths to the relevant `SKILL.md` files.
