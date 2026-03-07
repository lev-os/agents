---
name: work-mvp
description: Execute the work lifecycle through Lev runtime contracts with FlowMind-compiled SPEC and scheduler behavior. Use when the task is a dev workload and execution must be CLI-first (`lev work contract`), contract-driven (`flowmind compile`), bead-first for artifacts (`bd`), and fail-fast on missing runtime/files/gates.
---

# Work MVP

## Inputs

- `GOAL` (required): lifecycle goal text.
- `EPIC_ID` (optional): BD epic id for deterministic exec attachment.
- Environment (optional): `SDLC_MODE`, `SDLC_MAX_ITERATIONS`, `SDLC_TIMEOUT_MS`, `SCHEDULER_MODE`.

## Workflow (6 Steps)

1. Run preflight and stop immediately on any failure.

```bash
command -v lev >/dev/null 2>&1 || { echo "missing: lev"; exit 1; }
command -v flowmind >/dev/null 2>&1 || { echo "missing: flowmind"; exit 1; }
command -v bd >/dev/null 2>&1 || { echo "missing: bd"; exit 1; }
test -f plugins/core-sdlc/flows/spec-lifecycle.flow.yaml || { echo "missing: plugins/core-sdlc/flows/spec-lifecycle.flow.yaml"; exit 1; }
test -f plugins/core-sdlc/flows/commit-gate.flow.yaml || { echo "missing: plugins/core-sdlc/flows/commit-gate.flow.yaml"; exit 1; }
test -f core/flowmind/system/tick-loop.flow.yaml || { echo "missing: core/flowmind/system/tick-loop.flow.yaml"; exit 1; }
```

2. Execute lifecycle orchestration through Lev.

```bash
lev work contract "$GOAL" [--epic "$EPIC_ID"] [--contract-live]
```

3. Compile the SPEC contract from SDLC flow.

```bash
flowmind compile \
  plugins/core-sdlc/flows/spec-lifecycle.flow.yaml \
  --target system_prompt \
  --mode "${SDLC_MODE:-simulate}" \
  --max-iterations "${SDLC_MAX_ITERATIONS:-1}" \
  --timeout-ms "${SDLC_TIMEOUT_MS:-120000}"
```

4. Compile scheduler contract from tick-loop flow.

```bash
flowmind compile \
  core/flowmind/system/tick-loop.flow.yaml \
  --target system_prompt \
  --mode "${SCHEDULER_MODE:-simulate}"
```

5. Compile SDLC scheduler overlay only if the file exists.

```bash
[ -f plugins/core-sdlc/flows/sdlc-tick-overlay.flow.yaml ] && \
flowmind compile \
  plugins/core-sdlc/flows/sdlc-tick-overlay.flow.yaml \
  --target system_prompt \
  --mode "${SCHEDULER_MODE:-simulate}"
```

6. Persist and advance artifacts bead-first.

```bash
bd create --title="Report: $GOAL" --type=report --description="<findings>"
bd create --title="Proposal: $GOAL" --type=proposal --description="<proposal>"
bd create --title="Spec: $GOAL" --type=spec --description="<acceptance criteria + constraints + decomposition>"
bd update <id> --status in_progress
bd close <id>
```

## Enforcement Rules

1. Use parent `work` semantics for stages and gates.

2. Do not redefine lifecycle logic in this skill.

3. Do not dispatch implementation/testing for `flowmind` or `graph` streams before SPEC gate passes.

4. Treat beads as source of truth; markdown mirrors are projections.

5. Stop on first non-zero exit code. Do not continue partial runs.

6. Return explicit blocker text with exact missing command or file path.

## Configuration

```yaml
work:
  mode: mvp
  lifecycle_engine: flowmind
  spec_engine: sdlc
  decision_tracking: beads

sdlc:
  enabled: true
  mode: simulate
  spec_flow: plugins/core-sdlc/flows/spec-lifecycle.flow.yaml
  commit_flow: plugins/core-sdlc/flows/commit-gate.flow.yaml
  compiler_target: system_prompt
  max_iterations: 1
  timeout_ms: 120000

scheduler:
  enabled: true
  flow: core/flowmind/system/tick-loop.flow.yaml
  overlay: plugins/core-sdlc/flows/sdlc-tick-overlay.flow.yaml
  mode: simulate
```
