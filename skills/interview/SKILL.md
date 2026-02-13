---
name: interview
description: Wizard-mode questioning skill for structured decision-making. Uses framework library (SCAMPER, First Principles, Systems Thinking, etc.) to guide users through complex decisions one question at a time.
version: 1.0.0
skill_type: playbook
category: process-ask
extends: []
related_skills:
  - think
  - work
  - lev-cdo
---

# Interview: Wizard-Mode Questioning

**Framework-powered interactive decision-making.** Guides users through complex problems using strategic, creative, and philosophical frameworks.

## Quick Start

```bash
/interview                    # Start new interview session
/interview --framework=SCAMPER  # Start with specific framework
```

## How It Works

1. **Context Analysis** - Detect input complexity
2. **Framework Recommendation** - Suggest best-fit frameworks (SWOT, First Principles, Design Thinking, etc.)
3. **Question Loop** - Walk through structured questions, one at a time
4. **MBTI Overlay** (optional) - Test perspectives across personality types

## Framework Library

### Strategic/Systems Thinking
- SWOT, First Principles, Systems Thinking, Theory of Constraints
- McKinsey 7S, Cynefin, Jobs to Be Done

### Creative Thinking
- SCAMPER, Reverse Brainstorming, Extreme Users
- Six Thinking Hats, Figure Storming, TRIZ, Design Thinking

### Philosophical/Spiritual
- Taoist Wu Wei, Ubuntu, Ayurvedic Doshas
- Buddhist Non-Attachment, Sufi/Rumi Poetry, I Ching, Stoicism

### Psychological/Cognitive
- MBTI (8 Cognitive Functions), Big Five (OCEAN), Ladder of Inference

## Output Format

Single question with options:
```
q1) {Question title}
🧠 {Framework Name} Analysis:
{1-3 sentence framework insight}

Options:
a. {Concrete option A with trade-off}
b. {Concrete option B with trade-off}
c. {Concrete option C with trade-off}

🧭 Follow-Up Menu:
1. [{Action for option A}]
2. [{Action for option B}]
3. [{Alternative perspective}]
4. [Deep dive into trade-offs]
5. [Go back]
6. [Switch framework]
```

## Integration

- **Command:** `/interview` (formerly `/guideme`)
- **Skill Route:** `skill://interview`
- **Used by:** `work` skill for wizard-mode context gathering

---

**Status:** v1.0.0
**Migrated from:** /guideme command

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for interview domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
