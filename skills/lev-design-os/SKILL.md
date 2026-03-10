---
name: design-os
description: Product planning and design workflow for creating UI components, data models, and implementation handoffs. Use when starting a new product, defining features, designing screens, or preparing export packages for coding agents.
skill_type: playbook
category: process-design
---

# Design OS Wizard

A structured product planning workflow that guides you from vision to implementation-ready export.

## Five-Fold Understanding

Before we begin, let me understand your quest:

1. **Evolution** - What exists? Starting fresh or iterating on existing product?
2. **Impact** - What does success look like? MVP or full-featured product?
3. **Relationships** - Technical constraints? Existing codebase or greenfield?
4. **Essence** - The ONE thing this product must do exceptionally well?
5. **Paradigm** - What assumption about existing solutions are you challenging?

## Choose Your Path

**What phase are you in?**

1. **Planning** - Product vision, roadmap, data model
   → Load: `references/planning.md`

2. **Design System** - Tokens, colors, typography, shell
   → Load: `references/design.md`

3. **Sections** - Feature specs, sample data, screens
   → Load: `references/sections.md`

4. **Export** - Generate handoff package for coding agents
   → Load: `references/export.md`

5. **Full Workflow** - Walk through all phases guided
   → Start with Planning, proceed sequentially

6. **Atomic Access** - Need just one specific command?
   - Product vision only → Load `references/planning.md` § Product Vision
   - Data model only → Load `references/planning.md` § Data Model
   - Design tokens only → Load `references/design.md` § Design Tokens
   - Shell design only → Load `references/design.md` § Design Shell
   - Screen design only → Load `references/sections.md` § Design Screen

7. **Something else?** - Tell me your quest

## Workflow Overview

```
Product Vision → Product Roadmap → Data Model
                        ↓
            Design Tokens → Application Shell
                        ↓
        For Each Section:
            Shape Section → Sample Data → Design Screen → Screenshot
                        ↓
                    Export Product
```

## Output Structure

Design OS creates these artifacts:

```
product/                      # Product definition
├── product-overview.md       # Vision, problems, features
├── product-roadmap.md        # Sections breakdown
├── data-model/               # Entity definitions
├── design-system/            # Colors, typography
├── shell/                    # Navigation spec
└── sections/[name]/          # Per-section specs, data, types

src/                          # Screen designs (React components)
├── shell/components/         # App shell components
└── sections/[name]/          # Section screen components

product-plan/                 # Export package (generated)
├── prompts/                  # Ready-to-use coding agent prompts
├── instructions/             # Implementation guides
├── design-system/            # Tokens for integration
├── shell/                    # Portable shell components
└── sections/                 # Portable section components + tests.md
```

## Key Principles

- **Props-Based Components** - All screen designs accept data via props, no direct imports
- **Progressive Disclosure** - Work through phases, each building on the last
- **Design Tokens** - Tailwind colors + Google Fonts applied consistently
- **TDD-Ready Export** - Each section includes `tests.md` for test-driven implementation
- **Coding Agent Handoff** - Pre-written prompts guide implementation agents

## Quick Commands

If you know exactly what you need:

| Command | Description |
|---------|-------------|
| `/product-vision` | Define product overview |
| `/product-roadmap` | Break into sections |
| `/data-model` | Define entities & relationships |
| `/design-tokens` | Choose colors & typography |
| `/design-shell` | Design app navigation |
| `/shape-section` | Define section spec |
| `/sample-data` | Generate sample data & types |
| `/design-screen` | Create screen components |
| `/export-product` | Generate handoff package |

## Phase Navigation

Each phase follows the wizard pattern:
- 1-5 options presented based on context
- Combined choices welcome ("1,3")
- Pivot anytime ("actually, let's...")
- Back navigation available

When ready, tell me which path you'd like to take.

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-design-os, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
