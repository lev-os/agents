# lev-sdlc — SDLC Poly Surface Reference

> Thin skill documenting all `lev sdlc *` commands and the SDLC plugin surface.
> Source: `plugins/core-sdlc/` in the Leviathan monorepo.

## Command Surface

### `lev sdlc exec`

Execute a chore/plan entity through the SDLC pipeline.

```bash
lev sdlc exec [entity] [--dry-run] [--json]
```

**Profile:** `sdlc.flowmind.exec`
**What it does:** Runs exec (opus-4-6) + validate (codex/gpt-5.4) phases on an entity.
**Source:** `plugins/core-sdlc/src/commands/sdlc.ts`

### `lev sdlc deepen`

Fan-out plan decomposition into parallel deep-research subagents.

```bash
lev sdlc deepen [entity] [--json]
```

**Profile:** `sdlc.flowmind.deepen`
**Source:** `plugins/core-sdlc/src/commands/sdlc.ts`

### `lev sdlc hygiene`

Periodic 3-axis scan: handoffs + chore-code alignment + spec update proposals.

```bash
lev sdlc hygiene [--json]
```

**Profile:** `sdlc.flowmind.hygiene`
**Source:** `plugins/core-sdlc/src/commands/sdlc.ts`

### `lev sdlc autodev`

Heartbeat-driven autonomous development loop.

```bash
lev sdlc autodev [--interval=5m] [--max-ticks=10] [--budget=50k] [--json]
```

Routes to `lev loop autodev`. See `/autodev-lev` skill for full documentation.
**Source:** `plugins/core-sdlc/src/commands/autodev.ts`

### `lev work`

SDLC work lifecycle router with stage-based dispatch.

```bash
lev work [query] [--stage=auto|find|gather|review|contract] [--dry-run] [--json] [--epic=ID]
```

**Stages:**
- `auto` — Classify intent and route automatically
- `find` — Discover entities and prior art
- `gather` — Collect context and evidence
- `review` — Review and validate entities
- `contract` — Generate/update BDD contracts

**Source:** `plugins/core-sdlc/src/commands/work.ts`

### `lev review`

Review queue for entities pending approval.

```bash
lev review [--limit=N] [--json]
lev review approve <id>
lev review reject <id>
lev review defer <id>
```

**Config:** `sdlc.gates.review_labels`, `sdlc.review.default_limit`
**Source:** `plugins/core-sdlc/src/commands/review.ts`

### `lev loop`

Entity queue management — discover, validate, promote, budget.

```bash
lev loop [--json]              # Show entity queue
lev loop autodev [flags]       # Start heartbeat loop
```

**Exports from `@lev-os/orchestration`:** `discoverPlans`, `loadLoopConfig`, entity types.
**Source:** `plugins/core-sdlc/src/commands/loop.ts`

### `lev instruct`

Append structured instructions (rules, learnings, corrections) to a project.

```bash
lev instruct "rule text" [--source=human|agent]
```

Append-only to `.lev/instructions.md`. Never rewrites.
**Source:** `plugins/core-sdlc/src/commands/instruct.ts`

## Entity Lifecycle

The SDLC plugin manages entities through this state machine:

```
draft → ready → in_progress → needs_validation → validated → done
                    │              │
                    │              └─ (fail) → ready (with feedback)
                    └─ (blocked) → blocked
```

Entity types: `plan-impl`, `plan-chore`, `plan-bugfix`, `plan-research`, `spec`, `chore`

## Exec Profiles

| Profile | Purpose | Model |
|---------|---------|-------|
| `sdlc.flowmind.exec` | Execute + validate entity | opus-4-6 + codex |
| `sdlc.flowmind.deepen` | Deep plan decomposition | opus-4-6 |
| `sdlc.flowmind.hygiene` | Periodic health scan | sonnet-4-6 |

## Configuration

Lives in `plugins/core-sdlc/config.yaml` under the `sdlc` namespace:

```yaml
sdlc:
  paths:
    instructions: .lev/instructions.md
    evidence: .lev/evidence/
    specs: docs/specs/
  mayor_mode:
    enabled: false
  entity_definitions:
    plan: { ... }
```

Config cascade: system → project → module → env (later wins).

## Validation Gates

Spec validation includes `.lev/validation-gates.yaml` cross-reference. All SDLC checkpoints
(spec-lint, pre-execute, post-validate) check applicable enforced gates before proceeding.

## Capabilities

- `git_events` — Git hook event providers
- `bd_events` — Beads task tracking events
- `spec_linting` — Spec validation
- `instruction_capture` — Append-only instruction log
- `mayor_mode` — Notification suppression
- `exec_profiles` — SDLC-specific execution profiles

## Integration

- **Control plane hierarchy (D8):** `lev exec` is THE execution plane, `lev loop` is scheduling, `.flow.yaml` is policy
- **Skills are shims (D12):** `/work`, `/autodev-loop` are Claude Code skill shims — real functionality lives in `lev sdlc *` commands
- **Entity queue:** `lev loop --json` returns the priority-sorted entity queue

## Related Skills

- `/work` — FSM lifecycle router (Claude Code skill shim)
- `/autodev-loop` — Cron-based tick scheduler (Claude Code skill shim)
- `/autodev-lev` — Heartbeat-based tick scheduler via `lev loop autodev`
- `lev` — Master CLI reference
