---
name: cdo-skill-injection
description: How to discover and inject skills per CDO agent or plan node (2-3 by default, 1-5 per plan node)
---

**When**: before every turn or wave for deep+, plan, and multi-wave runs. Run it again for each wave, because the right skills change as the run learns.

**Skill Discovery Protocol**:

1. Extract keywords from problem + current turn focus (in plan mode, the node's focus question)
2. Search the installed inventory with skill://skill-discovery, using broad keywords:
```bash
lev-skills "<broad keywords>" --json --limit=5
```
3. Search workshop POC catalog (weighted heavier):
```bash
node ~/lev/workshop/poc/lookup/cli.js find "<keywords>"
```
4. Browse complementsWell for power combos
5. Select 2-3 skills per agent (or the plan node's count, 1-5), matching skill to role perspective
6. Read each skill's full content
7. Inject inline into agent brief

**Workshop POC Weighting**: Skills from `~/lev/workshop/poc/skills/` are weighted heavier than generic skills because they contain tested thinking frameworks (axioms, hidden-gems). Prefer workshop POC results when relevance scores are close.

**Skill Sources** (search order):
1. `lev-skills` over `~/.agents/skills-inventory.jsonl` — installed skills (lexical ranking; use broad nouns and verbs)
2. `~/lev/workshop/poc/skills/domains/axioms/` — Core thinking frameworks
3. `~/lev/workshop/poc/skills/domains/hidden-gems/` — 35+ cognitive/strategy frameworks
4. `~/.agents/skills/` — Agent skills catalog
5. `~/lev/workshop/poc/lookup/metadata/` — 100+ framework metadata

**Power Combo Discovery**: Skills declare complementsWell metadata. Chain them:
```
decision-matrix → rice-scoring → reversibility-check
systems-thinking → first-principles → feedback-loops
```

**Injection Format**: Include the full skill content in the agent brief:
```markdown
## Your Skills

### Skill 1: {name}
{full SKILL.md or skill content pasted here}

### Skill 2: {name}
{full content}
```

**Tag-Based Discovery** for exec domains:
```bash
node ~/lev/workshop/poc/lookup/cli.js list --tag=dev     # for exec dev
node ~/lev/workshop/poc/lookup/cli.js list --tag=strategy # for exec arch
```
