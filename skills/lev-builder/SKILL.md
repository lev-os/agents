---
name: lev-builder
description: |
  [WHAT] Builder workflow for developing `~/lev` and migrating proven work to core paths.
  [HOW] Assess existing code, run prior art checks, decide placement against `~/lev/docs`, apply patches, validate E2E.
  [WHEN] Use when formalizing POCs, placing modules, or migrating workshop output into production architecture.
  [WHY] Prevents drift and duplicate effort by enforcing file-based routing and docs-aligned placement.

  Triggers: "build feature", "migrate poc", "where should this go", "prior art check", "placement decision", "formalize"
skill_type: workflow
category: process-builder

lifecycle_integration:
  stage: manifesting
  input_artifact: design doc + POC code
  output_artifact: production code in lev/core
---

# lev-builder: POC → Formalize → Migrate

**Core principle:** Build in a workspace POC, prove it works, migrate to `~/lev` canonical paths.

## Why This Exists

```
PROBLEM:
- Work happens across mixed workspaces (project-local, workshop, plugins)
- BD issues are in lev (lev-* prefix)
- Need to know WHERE to put things in Leviathan
- Need prior art check before creating new

SOLUTION:
- lev-builder orchestrates the full workflow
- POC in `~/lev/workshop/poc` (or project-local skills) → migrate to `~/lev/core` when proven
- Uses graph operations for decisioning, then applies explicit filesystem patches during migration
```

## The Builder Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEV-BUILDER WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ ASSESS (What exists?)                                       │
│  ├─ lev get "topic" --indexes codebase,docs,skills            │
│  ├─ Check ~/lev/core/* for existing modules                    │
│  ├─ Check ~/lev/workshop/poc/* for prior POCs                  │
│  └─ Output: Related code, docs, skills found                   │
│                                                                 │
│  2️⃣ PRIOR ART CHECK (Duplicate prevention)                      │
│  ├─ ./scripts/prior-art-check.sh "topic"                       │
│  ├─ bd search "topic"                                          │
│  ├─ Skill lookup: ~/lev/workshop/poc/lookup/                   │
│  └─ Output: Existing work to patch vs. new work to create      │
│                                                                 │
│  3️⃣ PLACEMENT DECISION (Where does it go?)                      │
│  ├─ Escalate to user if ambiguous                              │
│  │   "Should this be in core/domain or a new plugin?"          │
│  ├─ Consult paths reference above + architecture primer        │
│  └─ Output: Target path confirmed                              │
│                                                                 │
│  4️⃣ GRAPH PLAN + FILE PATCH                                     │
│  ├─ Generate graph mutation plan from design doc              │
│  ├─ Materialize approved changes as filesystem patch          │
│  ├─ Apply to target location                                  │
│  └─ Output: Files created/modified                            │
│                                                                 │
│  5️⃣ E2E VALIDATION (Confirm it works)                           │
│  ├─ Run relevant tests                                         │
│  ├─ Typecheck: bun run typecheck                               │
│  ├─ Integration test if applicable                             │
│  └─ Output: Validation results                                 │
│                                                                 │
│  6️⃣ MIGRATE (POC → Production)                                  │
│  ├─ If POC in workshop/project skills: move to lev/core        │
│  ├─ Update skill registry                                      │
│  ├─ Create migration PR/commit                                 │
│  └─ Output: Migration complete                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Leviathan Paths Reference

> For current architecture, see `~/.agents/skills/lev/references/architecture-primer.md`

```yaml
# Where things go in Leviathan — sourced from real filesystem

~/lev/core/
├── build/            # Build system
├── config/           # Configuration system
├── daemon/           # Background services
├── domain/           # Domain models
├── event-bus/        # Event bus infrastructure
├── event-machines/   # Event-driven state machines
├── event-providers/  # Event source providers
├── exec/             # Execution layer
├── flowmind/         # Flow/mind orchestration
├── graph/            # Graph primitives
├── harness/          # Agent execution, adapters, Ralph
├── index/            # Index/registry
├── logger/           # Logging infrastructure
├── memory/           # Memory layer
├── orchestration/    # Orchestration engine
├── plugin-manager/   # Plugin lifecycle management
├── poly/             # Polyglot/multi-runtime support
├── storage/          # Storage abstractions
├── telemetry/        # Telemetry/observability
└── ui/               # UI layer

~/lev/plugins/        # Plugin ecosystem (60+ plugins)
├── auth-sniffer/     # Auth sniffing
├── beads/            # Issue tracking (bd)
├── browser-cascade/  # Browser automation
├── code-graph/       # Code graph analysis
├── deploy/           # Deployment
├── evolve-memory/    # Memory evolution
├── graph-adapters/   # Graph adapter layer
├── guardrails/       # Safety guardrails
├── mastra/           # Mastra integration
├── osint/            # OSINT tooling
├── voice/            # Voice capabilities
├── workshop/         # Workshop plugin
└── ...               # See ~/lev/plugins/ for full list

~/lev/workshop/
├── intake/           # Ingested external projects
├── poc/              # Proof of concepts
│   ├── lookup/       # Skill discovery system
│   ├── agentctl/     # Agent control POC
│   ├── cdo/          # CDO POC
│   └── ...           # See ~/lev/workshop/poc/ for full list
└── ...
```

## Quick Commands

### 1. Assess Topic

```bash
# If `lev get` is not available yet in your CLI build, substitute `lev find`.
# Full assessment
lev get "topic" --indexes codebase,docs,skills,tasks

# Check core modules
ls ~/lev/core/ | grep -i <topic>

# Check plugins
ls ~/lev/plugins/ | grep -i <topic>

# Check POCs
ls ~/lev/workshop/poc/ | grep -i <topic>

# Check skills
ls ~/.agents/skills/ | grep -i <topic>
```

### 2. Prior Art Check

```bash
# Deterministic check
./scripts/prior-art-check.sh "data vault leases"

# BD search
bd search "vault" --root-path ~/lev
bd search "lease" --root-path ~/lev

# Skill lookup
node ~/lev/workshop/poc/lookup/cli.js search "authorization"
```

### 3. Escalate Decision

```python
# In agent context
escalate({
  type: "PLACEMENT_DECISION",
  question: "Should fleet-rbac.ts go in core/domain or plugins/guardrails?",
  options: [
    { path: "core/domain/fleet-rbac.ts", reason: "Core domain logic" },
    { path: "plugins/guardrails/fleet-rbac.ts", reason: "Safety/access is a plugin concern" }
  ],
  context: "Fleet auth controls who can spawn agents and access data"
})
```

### 4. Graph Plan + File Patch

```bash
# Generate patch plan from design doc
cat pm/designs/<feature>.md | \
  ./scripts/design-to-patch.sh > patches/<feature>.patch

# Apply patch (preview)
./scripts/apply-patch.sh patches/<feature>.patch --dry-run

# Apply patch (execute — target a REAL core/ or plugins/ path)
./scripts/apply-patch.sh patches/<feature>.patch --target ~/lev/core/<module>/
```

### 5. Validate E2E

```bash
# Typecheck
cd ~/lev && bun run typecheck

# Run tests for target module
bun test core/<module>/

# Integration test
bun test:integration --filter "<feature>"
```

### 6. Migrate POC

```bash
# Move skill from workshop POC to lev
./scripts/migrate-skill.sh ~/lev/workshop/poc/lev-builder ~/lev/core/builder

# Update registry
./scripts/update-skill-registry.sh

# Commit
cd ~/lev && git add . && git commit -m "feat: migrate lev-builder from POC"
```

## Integration with Other Skills

| Skill | Role in Builder |
|-------|-----------------|
| `lev get` | Assessment - search across indexes |
| `lev-patch` | Prior art - check before creating |
| `planning` | Spec authoring backend - CDO graph to execution |
| `ralph` | Execution - run tasks with validation |
| `cdo` | Graph operations - state machines |

## Common Workflows

### Workflow 1: New Feature

```
USER: "Add event-driven scheduling to Leviathan"

BUILDER:
1. ASSESS: lev get "scheduling\|event\|cron"
   → Found: core/event-machines has state machines, core/orchestration exists

2. PRIOR ART: bd search "scheduling"
   → Found: core-scheduling plugin exists in plugins/

3. PLACEMENT: Escalate "core/orchestration vs plugins/core-scheduling?"
   → User: "core/orchestration — it's a core concern"

4. PATCH: Generate scheduler.ts from design doc
   → Created: ~/lev/core/orchestration/scheduler.ts

5. VALIDATE: bun run typecheck && bun test core/orchestration/
   → Passed

6. MIGRATE: N/A (already in lev/core)
```

### Workflow 2: POC to Production

```
USER: "Migrate lev-builder skill to production"

BUILDER:
1. ASSESS: ls ~/lev/workshop/poc/lev-builder/
   → Found: SKILL.md, scripts/
   
2. PRIOR ART: ls ~/lev/core/builder/
   → Not found (new module)
   
3. PLACEMENT: "core/exec" or "plugins/" (depends on scope)
   → Confirmed

4. PATCH: Copy + adapt for lev structure
   → Created: ~/lev/core/exec/builder/ (or plugins/builder/)

5. VALIDATE: bun test core/exec/
   → Passed
   
6. MIGRATE: git commit, update registry
   → Done
```

### Workflow 3: Assess & Consolidate

```
USER: "What exists for memory persistence in Leviathan?"

BUILDER:
1. ASSESS:
   lev get "memory\|persistence\|storage" --indexes codebase,docs
   → Found:
     - core/memory/ (memory layer)
     - core/storage/ (storage abstractions)
     - plugins/evolve-memory/ (memory evolution plugin)

2. REPORT:
   "Memory/persistence exists in 3 places:
    - core/memory: production memory layer
    - core/storage: storage abstractions
    - plugins/evolve-memory: evolution/migration plugin

    Recommend: Verify boundaries are clean, consolidate if overlapping"

3. ESCALATE: "Proceed with consolidation?"
```

## Escalation Patterns

```typescript
// Decision types that trigger escalation
const ESCALATION_TRIGGERS = [
  "PLACEMENT_DECISION",      // Where to put code
  "CONSOLIDATION_DECISION",  // Merge vs keep separate
  "ARCHITECTURE_DECISION",   // Significant design choice
  "MIGRATION_APPROVAL",      // Moving POC to production
  "DEPENDENCY_ADDITION",     // Adding new dependencies
];

// Escalate via Telegram (approval buttons)
await escalate({
  type: "PLACEMENT_DECISION",
  question: "...",
  options: [...],
  buttons: [
    { text: "Option A", callback_data: "placement:core/domain" },
    { text: "Option B", callback_data: "placement:plugins/guardrails" },
    { text: "Discuss", callback_data: "placement:discuss" },
  ]
});
```

## State Tracking

```jsonl
# .lev/builder/state.jsonl
{"ts":"...","action":"assess","topic":"scheduling","results":["core/orchestration","plugins/core-scheduling"]}
{"ts":"...","action":"prior_art","topic":"scheduling","found":true,"matches":1}
{"ts":"...","action":"escalate","type":"PLACEMENT_DECISION","resolved":true,"choice":"core/orchestration"}
{"ts":"...","action":"patch","target":"core/orchestration/scheduler.ts","status":"created"}
{"ts":"...","action":"validate","target":"core/orchestration/","passed":true}
```

## Summary

**lev-builder answers:**
1. **What exists?** → Assess with lev get
2. **Is there prior art?** → Check with lev-patch
3. **Where does it go?** → Escalate placement decisions
4. **How to apply?** → Graph plan + explicit filesystem patch
5. **Does it work?** → E2E validation
6. **Ready for production?** → Migrate POC to lev/core

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

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
You are the prompt-architect-enhanced specialist for lev-builder, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
