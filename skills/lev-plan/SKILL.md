# lev-plan — Plan Entity Lifecycle Management

> Create, list, show, transition, and validate plan entities.
> Plans live in `.lev/pm/plans/` with YAML frontmatter driving the lifecycle FSM.

## Plan Types

| Type | Slug Prefix | Purpose |
|------|-------------|---------|
| `plan-impl` | `plan-impl-*` | Feature or capability delivery |
| `plan-bugfix` | `plan-bugfix-*` | Defect investigation and resolution |
| `plan-chore` | `plan-chore-*` | Maintenance: cleanup, upgrades, test coverage, docs, tooling |
| `plan-research` | `plan-research-*` | Investigation with knowledge output |
| `plan-migration` | `plan-migration-*` | State transition between well-defined system shapes |

## Required Frontmatter

```yaml
---
type: plan-impl          # or plan-bugfix, plan-chore, plan-research, plan-migration
status: draft            # draft | ready | in_progress | needs_validation | validated | done | blocked | archived
priority: 2              # 0-4 (P0=critical, P4=backlog)
slug: my-feature-name    # kebab-case, <=40 chars, unique per type per week
created_at: 2026-03-14   # ISO date
done_condition: "..."    # deterministic test for completion
steps:
  - description: "..."
    validation: "..."
acceptance_criteria: []
gates: []
---
```

### Optional Fields

| Field | Type | Purpose |
|-------|------|---------|
| `bd_id` | string | Beads issue ID (e.g., `lev-abc`) |
| `entry_point` | string | Primary file or skill path |
| `code_refs` | string[] | Files this plan touches |
| `blocked_by` | string[] | BD issue IDs blocking this plan |
| `spec_refs` | string[] | Spec paths this implements |
| `confidence` | float | 0.0-1.0 author confidence |
| `fitness_functions` | string[] | Shell commands for validation |
| `owner` | string | Domain or agent handle |

### Backward Compatibility

Discovery code reads lifecycle state with fallbacks:
```
status > lifecycle_state > lifecycleState > 'unknown'
```

Canonical field is `status`. Legacy aliases accepted but should not be used in new plans.

## Lifecycle FSM

```
draft → ready → in_progress → needs_validation → validated → done
                     │              │                              │
                     │              └─ (fail) → ready (feedback)   │
                     └─ (blocked) → blocked                        └─ archived
```

### Transition Rules

| From | To | Condition |
|------|----|-----------|
| `draft` | `ready` | All required fields present, `done_condition` defined |
| `ready` | `in_progress` | BD issue claimed OR agent picks it up |
| `in_progress` | `needs_validation` | Implementation complete, awaiting validation |
| `needs_validation` | `validated` | All validation gates pass |
| `needs_validation` | `ready` | Gates failed — feedback appended, retry |
| `validated` | `done` | Promoted to `_done/` directory |
| `in_progress` | `blocked` | External dependency prevents progress |
| `blocked` | `ready` | Blocker resolved |
| `done` | `archived` | Historical reference only |

**Terminal states:** `done`, `archived`.

## Operations

### Create

```bash
# Create a plan file with proper frontmatter
cat > .lev/pm/plans/plan-impl-my-feature.md << 'EOF'
---
type: plan-impl
status: draft
priority: 2
slug: my-feature
created_at: 2026-03-14
done_condition: "Tests pass and feature accessible via CLI"
steps:
  - description: "Implement core logic"
    validation: "Unit tests pass"
acceptance_criteria: []
gates: []
---

# My Feature

## Context
...

## Implementation Notes
...
EOF
```

### List

```bash
# Via lev loop (recommended)
lev loop --json

# Via filesystem
ls .lev/pm/plans/plan-*.md

# Filter by status
grep -l "status: ready" .lev/pm/plans/plan-*.md
```

### Show

```bash
# Via bd if linked
bd show <bd_id>

# Direct read
cat .lev/pm/plans/plan-impl-my-feature.md
```

### Transition

Update the `status` field in frontmatter. For promotion to done:

```bash
# Move to _done/ directory
mv .lev/pm/plans/plan-impl-my-feature.md .lev/pm/plans/_done/
```

### Validate

Validation checks (run during `needs_validation` → `validated` transition):

1. All required frontmatter fields present
2. `done_condition` is satisfied
3. Fitness functions pass (if defined)
4. Acceptance criteria met
5. Code compiles/typechecks for touched packages

## Fitness Functions

Defined in frontmatter or body. Checked during validation.

**Frontmatter syntax:**
```yaml
fitness_functions:
  - "pnpm test"
  - "pnpm lint"
  - "grep -q 'export' src/index.ts"
```

**Body syntax:**
```markdown
## Fitness Functions
1. **DONE** — All tests pass (pnpm test)
2. **DONE** — No lint errors
3. UNIMPLEMENTED — Coverage > 80%
```

**Status markers:**
- Passing: `DONE`, `PASS`, `done`
- Failing: `FAIL`, `fail`
- Incomplete: `NOT YET`, `UNIMPLEMENTED`, `TODO`

## Promotion Rubric

Plans in `draft` status are scored for promotion to `ready` by the autodev loop:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Alignment | 25% | Does this align with project goals? |
| Blast radius | 20% | How many files/modules touched? (smaller = higher score) |
| Architecture impact | 20% | Does it change contracts or interfaces? (no change = higher) |
| Code refs exist | 15% | Do referenced files actually exist? |
| Acceptance criteria | 10% | Are criteria well-defined? |
| E2E path | 10% | Is the done condition testable? |

**Threshold:** Composite score >= 0.65 promotes to `ready`.

## Entity Discovery

Plans are discovered by `@lev-os/orchestration/entities`:

```typescript
discoverPlans(config) → EntitySummary[]
```

**Default surfaces:**

| Surface | Input | Done | Patterns |
|---------|-------|------|----------|
| plans | `.lev/pm/plans/` | `.lev/pm/plans/_done/` | `plan-*.md` |
| specs | `docs/specs/` | `docs/specs/_done/` | `plan-*.md`, `chore-*.md` |

**Sort order:** P0 > P1 > P2 > P3 > P4 (null priority sorts last).

**Filtered states:** `blocked`, `deferred` are skipped by default. `done`, `completed`, `validated` are excluded unless `includeAll: true`.

## Integration

### BD (Beads)

```bash
# Create linked BD issue
bd create --title="Implement feature X" --type=task -p 2

# Link in plan frontmatter
# bd_id: lev-abc

# Close when plan reaches done
bd close lev-abc --reason "per plan my-feature"
```

Plans can exist without BD issues (lightweight work). BD issues can exist without plans (simple tasks). For complex work: plan first, then BD.

### Prompt Stacks

- `sdlc-exec-validate` — Execute + validate plan entity
- `sdlc-deepen-plan` — Decompose plan into research topics

### Autodev Loop

The autodev loop uses `lev loop --json` to discover ready plans and dispatch execution ticks. Each tick follows: VALIDATE → EXECUTE → PROMOTE → DRIFT waterfall.

## Directory Structure

```
.lev/pm/plans/
├── plan-impl-*.md          # Feature delivery
├── plan-bugfix-*.md        # Defect resolution
├── plan-chore-*.md         # Maintenance
├── plan-research-*.md      # Investigation
├── plan-migration-*.md     # Structural transitions
└── _done/                  # Promoted completed plans
```

## Related Skills

- `lev-sdlc` — SDLC poly surface reference (commands, profiles)
- `/work` — FSM lifecycle router (creates/manages plans at SPEC stage)
- `/autodev-loop` — Cron-based tick scheduler (discovers and executes plans)
- `/autodev-lev` — Heartbeat-based tick scheduler via `lev loop autodev`
