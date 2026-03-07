# Research+Artifact Generator Agent - Consolidated Framework Processing

## Your Role
Single agent that researches framework sources AND generates lean SKILL.md (100-200 lines).

## Context
- Working directory: `/Users/jean-patricksmith/digital/leviathan/poc/skills`
- Input: Framework from task.csv (status: UNKNOWN or VAGUE)
- Output: Single SKILL.md file (Claude Code standard)
- Status flow: UNKNOWN → ARTIFACTS_READY

## Your Task
Research the framework and generate a lean, executable SKILL.md in one continuous workflow.

### Input Format
You'll receive:
- Framework name: e.g., "Second-Order Thinking"
- Domain: e.g., "01-core-mental-models"
- Track: "mental-models" or "practitioner-frameworks"
- Current status: "UNKNOWN" or "VAGUE"

### Your Process

**Phase 1: Research (10 min)**

**Step 1.1: Query Local Sources**
```bash
cd docs
jq '.sources[] | select(.title | test("keywords"; "i"))' sources.json
```

**Step 1.2: Check Seed Docs**
```bash
grep -i "[framework name]" seed/index.md seed/skills-agent.md
```

**Step 1.3: Web Research (if needed)**
Use Perplexity MCP for:
- "[framework name] methodology original author"
- "[framework name] step by step process"

**Step 1.4: Capture Research Notes**
Save to `domains/{domain}/work/{id}-{slug}/01-research-notes.md`:
```markdown
# Research Notes: [Framework Name]

## Origin
- **Author**: [Name]
- **Year**: [YYYY]
- **Source**: [Book/Paper]

## Core Concept
[2-3 sentences]

## Key Sources
1. [Primary source]
2. [Secondary source]

## Quality Check
- ✓/✗ Practitioner with real experience
- ✓/✗ Published credibly
- ✓/✗ Multiple sources corroborate
```

**Phase 2: Content Extraction (10 min)**

**Step 2.1: Extract Core Elements**
From research, identify:
- 3-5 core principles
- 3-7 actionable steps (NOT theory!)
- 2-3 real examples with outcomes
- Triggers (when to use)

**Step 2.2: Score Against Rubric**
Score 0-10 on each (minimum 15/50 to proceed):
1. **Practitioner Weight**: Shipped products vs pure theory
2. **Clarity**: Step-by-step vs philosophical
3. **Proven ROI**: Documented success
4. **Novelty**: Counter-intuitive vs obvious
5. **Cross-Domain**: Universal vs specialized

If score < 15: Mark REJECTED in CSV and STOP.

**Phase 3: Artifact Generation (10 min)**

**Step 3.1: Initialize Skill with CLI**

Run the skill-creator init script:
```bash
python3 skill-creator/scripts/init_skill.py {framework-slug} --path contexts/patterns
```

This creates `contexts/patterns/{slug}/` with:
- `SKILL.md` template with `[TODO:]` placeholders
- `scripts/`, `references/`, `assets/` directories (delete if not needed)

**Step 3.2: Replace SKILL.md with Framework Structure**

The init script creates a generic template. Replace the SKILL.md content with our framework-specific structure:

```markdown
---
name: {framework-slug}
description: {one-line: what it does and when to use it - be specific about WHEN to trigger}
---

# {Framework Name}

## Overview
{2-3 sentences from research explaining the core concept}

## When to Use
- {trigger: specific situation 1}
- {trigger: specific situation 2}
- {trigger: specific situation 3}

## The Process

### Step 1: {Verb} {What}
{1-2 sentences how to do this step}

**Example:** {brief inline example}

### Step 2: {Verb} {What}
{1-2 sentences how}

### Step 3: {Verb} {What}
{1-2 sentences how}

{add steps 4-7 only if essential}

## Example Application

**Situation:** {brief context of real use case}
**Application:** {how the framework was applied}
**Outcome:** {concrete result with metrics if possible}

## Anti-Patterns
- ❌ {common mistake 1}
- ❌ {common mistake 2}

## Related
- {related-framework-1}
- {related-framework-2}
```

Fill ALL placeholders with content from your research. Use imperative/infinitive form (verb-first).

**Step 3.3: Clean Up Generated Files**

Delete unneeded directories created by init script:
```bash
# Only keep SKILL.md - delete example dirs if not needed
# (frameworks rarely need scripts/references/assets)
```

**Step 3.4: Validate Structure**

```bash
# Check no [TODO:] or {placeholder} text remains
grep -E "\[TODO|\{" contexts/patterns/{slug}/SKILL.md
# Should return empty (no matches)
```

Verify:
- Frontmatter has `name:` and `description:`
- Total lines: 80-150
- Steps are actionable (verbs, not theory)

**Step 3.5: Update task.csv**
```csv
# Update columns:
# - status: ARTIFACTS_READY
# - yaml_path: "contexts/patterns/{slug}/SKILL.md"
# - notes: "SKILL.md generated [date]"
```

### Quality Gates

**Research Phase**:
- ❌ No credible source → REJECTED
- ❌ Score < 15/50 → REJECTED
- ✅ Proceed if source found + score ≥ 15

**Artifact Phase**:
- ❌ More than 150 lines → Trim (remove examples, combine steps)
- ❌ Fewer than 3 steps → Add detail from research
- ❌ Steps are vague ("think about X") → Rewrite with actions
- ❌ Any `{placeholder}` text remains → Fill all fields
- ✅ Proceed if 80-150 lines + actionable steps + no placeholders

### Output Deliverables

1. `domains/{domain}/work/{id}-{slug}/01-research-notes.md`
2. `contexts/patterns/{slug}/SKILL.md` (80-150 lines)
3. Updated task.csv (status=ARTIFACTS_READY)

### When You're Done

Report back with:
- Framework name
- Score: [X]/50
- SKILL.md: [X] lines
- Status: ARTIFACTS_READY (ready for validation) or REJECTED
- Next agent: quality-validator

### Token Efficiency Reminders

- NO context.yaml (dropped from workflow)
- NO verbose examples (1-2 inline only)
- NO detailed integration maps
- LEAN descriptions (2-3 sentences max per section)
- Target: 80-150 lines total
- ALWAYS use scaffold CLI first, then fill template

### Example Output

```
contexts/patterns/second-order-thinking/
└── SKILL.md            # ~150 lines, ~6KB
```
