# Work Skill Configuration

## Environment Variables

| Env Var | Default | Purpose |
|---------|---------|---------|
| `LEV_PM_REPORTS` | `.lev/pm/reports/` | Report output dir |
| `LEV_PM_PROPOSALS` | `.lev/pm/proposals/` | Proposal output dir |
| `LEV_PM_SPECS` | `.lev/pm/specs/` | Spec output dir |
| `LEV_PM_HANDOFFS` | `.lev/pm/handoffs/` | Handoff output dir |

**Stage override:** `work --stage={ephemeral|captured|crystallizing|crystallized|manifesting}`

## FlowMind SPEC Engine Config

```yaml
work:
  lifecycle_engine: flowmind
  spec_engine: sdlc

sdlc:
  enabled: true
  mode: simulate            # simulate | enforce
  spec_flow: plugins/core-sdlc/flows/spec-lifecycle.flow.yaml
  commit_flow: plugins/core-sdlc/flows/commit-gate.flow.yaml
  compiler_target: system_prompt
  max_iterations: 1
  timeout_ms: 120000
```

## Execution Semantics

1. `simulate`: compile and run prompt-driven spec generation without enforcing plugin hooks.
2. `enforce`: require plugin lifecycle checks and fail closed on gate violations.
3. Missing flow files: degrade to template fallback and emit WARN in artifact.

## SPEC Engine Command Contract

Option A (preferred):

```bash
lev exec flowmind compile \
  --flow "${SDLC_SPEC_FLOW:-plugins/core-sdlc/flows/spec-lifecycle.flow.yaml}" \
  --target "${SDLC_COMPILER_TARGET:-system_prompt}" \
  --mode "${SDLC_MODE:-simulate}" \
  --max-iterations 1 \
  --timeout-ms 120000
```

Fallback if `lev exec flowmind` unavailable:

```bash
flowmind compile \
  --flow "${SDLC_SPEC_FLOW:-plugins/core-sdlc/flows/spec-lifecycle.flow.yaml}" \
  --target "${SDLC_COMPILER_TARGET:-system_prompt}" \
  --mode "${SDLC_MODE:-simulate}" \
  --max-iterations 1
```
