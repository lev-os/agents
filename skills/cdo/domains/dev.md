---
name: cdo-domain-dev
description: Dev team preset — POC for swarm execution following lev sdlc
---

# CDO Domain: Dev

Development team preset for implementation tasks following the lev SDLC lifecycle.

---

## Team Shape

| Role | Agent Type | Skills | Focus |
|------|-----------|--------|-------|
| **Dev Lead** | general-purpose | lev-sdlc, /work, entity lifecycle | Architecture decisions, task breakdown |
| **Implementer** | general-purpose | Domain-specific skills from context | Code implementation, patterns |
| **Reviewer** | general-purpose | code-review, SOLID principles | Quality gates, edge cases |
| **Tester** | test-runner | testing frameworks | Validation, edge cases |

---

## Integration Points

- **Entity Lifecycle**: `.lev/pm/` entities and lifecycle management
- **Task Tracking**: BD tasks for issue tracking and progress
- **Execution Plane**: `lev exec --profile=sdlc.flowmind.*` for task execution
- **Work Routing**: `/work` skill for lifecycle stage routing
- **Validation Gates**: `.lev/validation-gates.yaml` for quality enforcement

---

## Workflow

```
T1: Dev Lead + Implementer analyze problem → design approach
    - Dev Lead reads entity context, breaks down requirements
    - Implementer surveys codebase, identifies patterns and constraints
    - Output: approach doc with file targets, risks, open questions

T2: Implementer builds, Reviewer critiques design
    - Implementer writes code following approach from T1
    - Reviewer evaluates against SOLID, ownership map, contract-first rules
    - Output: implementation + review feedback

T3: Tester validates, Dev Lead synthesizes
    - Tester runs existing tests, writes new coverage for changes
    - Dev Lead merges review feedback, resolves conflicts
    - Output: passing tests + final implementation

Adaptive: add specialists if implementation reveals complexity
    - Database changes → add data modeling specialist
    - API surface changes → add contract specialist
    - Cross-module work → add integration specialist
```

---

## Context Loading

The Dev Lead auto-reads these for orientation:

- `AGENTS.md` — Ownership map, routing rules
- `docs/ARCHITECTURE.md` — System architecture
- `.lev/validation-gates.yaml` — Quality gates
- Relevant `config.yaml` for target module

---

## BD Integration

```bash
# Dev Lead claims task at start
bd update <id> --claim --json

# Implementer links discovered work
bd create "Found issue" --description="Details" -p 2 --deps discovered-from:<parent-id> --json

# Dev Lead closes on completion
bd close <id> --reason "Implemented + tested" --json
```

---

## Quality Gates

Before marking work complete:

- [ ] Typecheck passes for touched packages
- [ ] Tests pass (existing + new)
- [ ] Contract tests for changed interfaces
- [ ] No accidental archive path dependencies
- [ ] BD task updated with evidence (commit SHA, test results)
