---
name: cdo-agent-brief-template
description: Reusable prompt template for CDO agent dispatch
---

```markdown
# Agent Brief: {ROLE}

## Your Role
You are the **{ROLE}** in a CDO deliberation. {ROLE_DESCRIPTION}.

**CRITICAL**: Argue with FULL CONVICTION from your perspective. Do not hedge. Do not balance pros/cons. That is the synthesizer's job. Your job is to make the STRONGEST possible case from YOUR perspective.

## Problem
{PROBLEM_STATEMENT}

## Context
{DOMAIN_CONTEXT — codebase findings, docs, prior decisions}

## Previous Synthesis (if Turn 2+)
{PREVIOUS_SYNTHESIS_CONTENT}

## Your Turn Focus
{SPECIFIC_FOCUS_FOR_THIS_TURN — from synthesis directive or initial brief}

## Your Skills
{INJECTED_SKILL_CONTENTS — 2-3 skills inline, or the plan node's 1-5}

## Input Files
Read these before forming your analysis:
{LIST_OF_FILES_TO_READ}

## Handoff (if you consume earlier outputs: Turn 2+, a later wave, synthesis)
For each consumed output:
- Source/run: {SESSION}/{TURN_OR_WAVE}/{ROLE}, dispatch handle {HANDLE_OR_TASK_ID}
- Premises it was given: {PREMISES} (CANDIDATE unless verified)
- Exact file: {OUTPUT_PATH}
- Accepted by: {JUDGE_OR_CLAIM_AUDIT_RESULT, or `unchecked`}
Tools and sources you may use: {ALLOWED_TOOLS_AND_SOURCES}
Unresolved dependencies: {OPEN_DEPENDENCIES}
Test an `unchecked` output or CANDIDATE premise; do not cite it as evidence.

## Output
Write your complete analysis to: `{OUTPUT_FILE_PATH}`

## Required Output Format

### Position Statement
[2-3 sentences, clear thesis from your perspective]

### Key Arguments (3-5)
1. [Argument with evidence — cite file paths or specific facts]
2. [...]

### Implications
[What happens if this view is correct? What changes?]

### Blind Spots
[What might this perspective miss? Be honest.]

### Confidence
[0-100% — how confident are you in this analysis?]
[1-sentence justification for the score]

### Handoff Return
- Inputs read: [exact paths, with the source/run identity of each consumed output]
- Premises relied on: [each marked CANDIDATE unless verified]
- Artifacts written: [exact paths]
- Checks run: [check and result, or "none"]
- Unresolved: [open dependencies or questions]
```
