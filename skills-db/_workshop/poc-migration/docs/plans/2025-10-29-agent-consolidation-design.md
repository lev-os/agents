# Agent Consolidation & Token Optimization Design

**Date**: 2025-10-29
**Status**: Approved
**Context**: Pipeline validated (Second-Order Thinking test), scaling to 500 frameworks requires efficiency

---

## Problem Statement

Current 4-agent pipeline (Research → Content Analyst → Artifact Generator → Quality Validator) generates:
- SKILL.md: 400+ lines
- context.yaml: 300+ lines
- High token usage per framework
- 12+ minutes per framework

**At 500 frameworks scale**: Inefficient, expensive, slow.

---

## Design Goals

1. **Reduce token usage 60-70%** through leaner outputs and fewer agents
2. **Align with Claude Code standards** (single SKILL.md with minimal frontmatter)
3. **Maintain quality** (validated frameworks, searchable index)
4. **Simplify architecture** (fewer moving parts, easier to debug)

---

## Approved Architecture

### Single Artifact: SKILL.md Only

**Format**: Claude Code standard
```yaml
---
name: framework-slug
description: One-line description of framework and when to use it
---

# Framework Name

[100-200 lines of lean execution guide]
```

**Drop entirely**:
- context.yaml (redundant with SKILL.md)
- Verbose examples and explanations
- Detailed integration maps

**Keep**:
- Core steps (3-7)
- 1-2 examples
- Key triggers
- Anti-patterns

**Target**: 100-200 lines per SKILL.md (vs current 400+)

---

### Consolidated Agents: 4 → 2

**Agent 1: Research+Artifact Generator**
**Status flow**: UNKNOWN → ARTIFACTS_READY
**Responsibilities**:
1. Source discovery (docs/sources.json, seed docs, Perplexity)
2. Content extraction (principles, steps, examples)
3. Generate lean SKILL.md (100-200 lines)
4. Update CSV

**Agent 2: Quality Validator**
**Status flow**: ARTIFACTS_READY → COMPLETE
**Responsibilities**:
1. Run 5 inclusion criteria checks
2. Detect red flags
3. Validate SKILL.md technical structure
4. Generate validation report
5. Update skills-index.json
6. Update CSV

---

### Indexing Strategy: skills-index.json

**Purpose**: Centralized lookup registry for all 500 frameworks

**Format**:
```json
{
  "frameworks": [
    {
      "name": "second-order-thinking",
      "description": "Trace decisions beyond immediate effects...",
      "path": "contexts/patterns/second-order-thinking/SKILL.md"
    },
    ...
  ]
}
```

**Build process**: Quality validator appends entry after validation passes

**Deferred**: Advanced tagging, triggers, relationships (revisit later with usage data)

---

## File Structure Changes

**Before**:
```
contexts/patterns/{slug}/
├── context.yaml        (300+ lines)
└── SKILL.md            (400+ lines)
```

**After**:
```
contexts/patterns/{slug}/
└── SKILL.md            (100-200 lines)

skills-index.json       (root level, all frontmatter)
```

---

## Agent Prompt Updates

### Agent 1: Research+Artifact (New Combined Agent)

**Key changes from current agents**:
- Merge research-agent + content-analyst + artifact-generator logic
- Single continuous process (no handoffs)
- Direct SKILL.md generation (skip YAML entirely)
- Lean output template (100-200 line target)
- Use skill-creator skill for SKILL.md formatting

**Output**:
- SKILL.md in contexts/patterns/{slug}/
- Updated task.csv: status=ARTIFACTS_READY

### Agent 2: Quality Validator (Updated)

**Key changes**:
- Remove context.yaml validation entirely
- Add skills-index.json update step
- Simplified consistency checks (only one file now)

**Output**:
- 03-validation-report.md
- Updated skills-index.json
- Updated task.csv: status=COMPLETE

---

## Migration Strategy

**Completed frameworks** (Shell Method, Second-Order Thinking):
- Keep as-is (already validated, working in Claude Code)
- Optional: Backfill to new format if time permits

**New frameworks** (remaining 498):
- Use new 2-agent consolidated workflow
- Generate SKILL.md only
- Build skills-index.json incrementally

**No breaking changes**: Existing validated frameworks continue working

---

## Expected Benefits

**Token Reduction**:
- SKILL.md: 400 → 150 lines (~60% reduction)
- No context.yaml generation (~50% fewer writes)
- 4 → 2 agents (~50% fewer agent spawns)
- **Total: 60-70% token usage reduction**

**Time Savings**:
- Pipeline: 12 → 6 minutes per framework (estimate)
- 500 frameworks: 100 hours → 50 hours saved

**Simplicity**:
- Single source of truth (SKILL.md)
- No sync issues between YAML and SKILL
- Clearer mental model (one file = one framework)

**Alignment**:
- Matches Claude Code standards exactly
- Skills immediately usable without conversion
- Standard frontmatter format

---

## Implementation Steps

1. ✅ Validate design with user
2. Create new `agents/research-artifact-generator.md`
3. Update `agents/quality-validator.md`
4. Update `docs/00-process.md` (2-agent workflow)
5. Test on 1 fresh framework (validate 2-agent flow)
6. Pilot 3-5 hidden gems (test SKILL.md-only approach)
7. Batch remaining 493 frameworks

---

## Open Questions (Deferred)

**Tagging & Advanced Search** (Later):
- When usage patterns emerge, revisit trigger indexing
- Consider semantic embeddings for discovery
- May add richer schema to skills-index.json

**context.yaml Deprecation**:
- Existing files can stay (not breaking anything)
- Future: Delete or archive after validation

**References/** (Optional enhancement):
- SKILL.md can reference deeper docs in references/ folder
- Not implemented initially (YAGNI)

---

## Success Metrics

- [ ] 2-agent workflow executes UNKNOWN → COMPLETE
- [ ] SKILL.md generates at 100-200 lines
- [ ] skills-index.json builds correctly
- [ ] Framework searchable and usable in Claude Code
- [ ] Token usage reduced 60-70% vs current
- [ ] Time per framework: ~6 minutes (vs 12)

---

**Next Step**: Implement new research-artifact-generator agent
