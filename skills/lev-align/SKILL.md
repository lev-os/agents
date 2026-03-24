---
name: lev-align
description: >
  Project alignment validator. Loads .lev/validation-gates.yaml and checks
  current work against all applicable gates. Reports pass/fail/aspirational
  per gate. Integrates with /work ALIGN phase.
version: 1.0.0
related_skills:
  - work
  - autodev-loop
  - lev-sdlc
skill_type: validation
category: process-lifecycle
triggers:
  - "align"
  - "check gates"
  - "validation gates"
  - "alignment check"
---

# lev-align — Project Alignment Validator

Loads `.lev/validation-gates.yaml` from project root, checks current work
against all applicable gates, and reports structured pass/fail/warn per gate.

---

## On Load

1. Find `.lev/validation-gates.yaml` via project root discovery (walk up from cwd)
2. Parse gates into sections: `checks`, `architecture_compliance`, `sdk_first_compliance`, `spec_invariants`
3. Classify which gates apply to current work context based on:
   - Module being touched (path → spec → invariants)
   - Work type (feature, bugfix, refactor, sdk_pass_through_refactor)
   - Tier classification (T1-T4 based on path patterns)

---

## Alignment Check Protocol

For each applicable gate, classify and report:

| Status | Behavior | Action on Fail |
|--------|----------|----------------|
| `enforced` | MUST pass | Block execution |
| `declared` | SHOULD pass | Warn, log to handoff |
| `aspirational` | COULD pass | Note only |

### Gate Resolution Order

1. **Spec invariants** — Check `spec_invariants.*` for modules being touched
2. **Architecture compliance** — Check `architecture_compliance.*`
3. **SDK-first compliance** — Check `sdk_first_compliance.*`
4. **Mandatory checks** — Check `checks.*`
5. **Quality gates** — Check `quality_gates.*` based on task type template

### Invariant Checking

For `spec_invariants` gates (poly_binder_only, daemon_ownership, index_architecture, etc.):

1. Read the gate's `invariants` list
2. For each invariant, verify against current code state:
   - Grep for violations (e.g., "daemon implementation logic" in core/poly/src/)
   - Check file existence (e.g., "core/cli/ does not exist")
   - Verify import chains
3. Run any `gates` commands if they have associated test commands

---

## Output Format

```markdown
## Alignment Report

**Project:** {project_name}
**Module:** {module_path}
**Work Type:** {work_type}
**Date:** {date}

### Enforced Gates

| Gate | Status | Evidence |
|------|--------|----------|
| poly_binder_only | PASS | 0 daemon logic lines in core/poly/src/ |
| daemon_ownership | PASS | 0 impl files under poly |

### Declared Gates

| Gate | Status | Evidence |
|------|--------|----------|
| poly_compliance | WARN | orchestrator/ still exists (cleanup pending) |

### Aspirational Gates

| Gate | Status | Note |
|------|--------|------|
| yaml_file_routing | NOTE | 3 hardcoded routes remain |

### Verdict

{PASS | WARN | BLOCK}
- Enforced: {n}/{total} pass
- Declared: {n}/{total} pass
- Blocking issues: {list or "none"}
```

---

## Integration with /work

The `/work` ALIGN phase calls lev-align automatically when `.lev/validation-gates.yaml` exists:

1. Load and parse the gates file
2. Filter gates applicable to current workstream/module
3. Check current state against enforced gates
4. Include gate status in alignment verdict
5. Block PROPOSE if any enforced gate fails

---

## Invocation

```
/lev-align                     # Full alignment check for current module
/lev-align --module core/poly  # Check specific module
/lev-align --gate poly_binder_only  # Check specific gate
/lev-align --type refactor     # Check gates for task type
/lev-align --report            # Save report to .lev/pm/reports/
```

---

## Anti-Patterns

- **Skipping enforced gates** — enforced means enforced, no exceptions without explicit user override
- **Checking aspirational gates as blocking** — aspirational is informational only
- **Running without reading specs** — gate checking requires reading the actual spec invariants
- **Hardcoding gate lists** — always read from validation-gates.yaml, never maintain a separate list
