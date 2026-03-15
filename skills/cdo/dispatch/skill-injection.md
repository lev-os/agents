---
name: cdo-skill-injection
description: How to discover and inject 2-3 skills per CDO agent via lev-catalog
---

**Skill Discovery Protocol**:

1. Extract keywords from problem + current turn focus
2. Search workshop POC catalog (weighted heavier):
```bash
node ~/lev/workshop/poc/lookup/cli.js find "<keywords>"
```
3. Browse complementsWell for power combos
4. Select 2-3 skills per agent, matching skill to role perspective
5. Read each skill's full content
6. Inject inline into agent brief

**Workshop POC Weighting**: Skills from `~/lev/workshop/poc/skills/` are weighted heavier than generic skills because they contain tested thinking frameworks (axioms, hidden-gems). Prefer workshop POC results when relevance scores are close.

**Skill Sources** (search order):
1. `~/lev/workshop/poc/skills/domains/axioms/` — Core thinking frameworks
2. `~/lev/workshop/poc/skills/domains/hidden-gems/` — 35+ cognitive/strategy frameworks
3. `~/.agents/skills/` — Agent skills catalog
4. `~/lev/workshop/poc/lookup/metadata/` — 100+ framework metadata

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
