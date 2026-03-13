---
name: work-mvp
description: Execute the work lifecycle through Lev runtime contracts with FlowMind session-driven execution and bead-first artifacts. Use when the task is a dev workload and execution must be CLI-first (`lev work contract`), session-driven (`FlowmindSessionManager`), bead-first for artifacts (`bd`), and fail-fast on missing runtime/files/gates.
---

# Work MVP

## Inputs

- `GOAL` (required): lifecycle goal text.
- `EPIC_ID` (optional): BD epic id for deterministic exec attachment.
- `STACK_ID` (optional): FlowMind stack/flow to use (default: heuristic — see below).
- Environment (optional): `SDLC_MODE`, `SDLC_MAX_ITERATIONS`, `SDLC_TIMEOUT_MS`.

## Stack Selection Heuristic

When `STACK_ID` is not provided, classify the task:

| Task Type | Stack | Rationale |
|-----------|-------|-----------|
| Implementation / bugfix | `sdlc-exec-validate` | Plan → execute → verify loop |
| Research / decomposition | `sdlc-deepen-plan` | Fan-out analysis |
| Maintenance / hygiene | `sdlc-hygiene` | Periodic repo scan |

## Workflow (5 Steps)

### 1. Preflight

Run preflight and stop immediately on any failure.

```bash
command -v lev >/dev/null 2>&1 || { echo "missing: lev"; exit 1; }
command -v bd >/dev/null 2>&1 || { echo "missing: bd"; exit 1; }
test -d core/flowmind || { echo "missing: core/flowmind"; exit 1; }
test -f plugins/core-sdlc/config.yaml || { echo "missing: plugins/core-sdlc/config.yaml"; exit 1; }
```

### 2. Initialize FlowMind Session

Start a session from the selected flow/stack. The session engine handles step-by-step progressive disclosure.

```bash
# Via FlowMind Session API (canonical)
SESSION_ID=$(lev flowmind session start --flow "$FLOW_FILE" --json | jq -r '.id')

# Or via prompt-stack CLI (backward-compat shim)
SESSION_ID=$(bun plugins/prompt-stack/src/cli.ts init --stack "$STACK_ID" --project-dir .)
```

**FlowMind Session API (programmatic):**

```typescript
import { FlowmindSessionManager } from '@lev-os/flowmind';

const mgr = new FlowmindSessionManager();
const session = mgr.startFromFile(`plugins/core-sdlc/flows/${flowFile}`);
```

### 3. Execute Steps via Session Loop

Execute each step in the session, using `lev exec` for the execution substrate:

```bash
while true; do
  STEP=$(lev flowmind session get --id "$SESSION_ID" --json)
  IS_LAST=$(echo "$STEP" | jq -r '.isLast')

  STEP_PROMPT=$(echo "$STEP" | jq -r '.step.prompt // .step.command')
  lev exec "$STEP_PROMPT" --profile "sdlc.flowmind.exec"

  RESULT=$(lev flowmind session next --id "$SESSION_ID" --json)
  STATUS=$(echo "$RESULT" | jq -r '.status')

  if [ "$STATUS" = "failed" ]; then
    echo "Step failed: $(echo "$RESULT" | jq -r '.error')"
    exit 1
  fi

  if [ "$IS_LAST" = "true" ]; then
    break
  fi
done
```

**FlowMind Session API (programmatic):**

```typescript
const mgr = new FlowmindSessionManager({
  stepExecutor: orchestrationAdapter,  // Wires agent steps to executeIterativeLoop()
});

// Progressive disclosure: get step context, execute, advance
let view = mgr.get(session.id);
while (true) {
  const result = await mgr.next(session.id);
  if (result.status === 'failed') throw new Error(result.error);

  const status = mgr.status(session.id);
  if (status.status === 'completed') break;
  view = mgr.get(session.id);
}
```

### 4. Validate and Record

```bash
SESSION_STATUS=$(lev flowmind session status --id "$SESSION_ID" --json)
echo "$SESSION_STATUS" | jq -r '.status'  # Should be "completed"
```

### 5. Persist Artifacts via Beads

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

3. Do not dispatch implementation/testing before SPEC gate passes.

4. Treat beads as source of truth; markdown mirrors are projections.

5. Stop on first non-zero exit code. Do not continue partial runs.

6. Return explicit blocker text with exact missing command or file path.

## Configuration

```yaml
work:
  mode: mvp
  lifecycle_engine: flowmind-sessions
  spec_engine: sdlc
  decision_tracking: beads

sdlc:
  enabled: true
  mode: simulate
  default_stack: sdlc-exec-validate
  flows_dir: plugins/core-sdlc/flows/

flowmind:
  session_persistence: xdg  # ~/.local/state/lev/flowmind/sessions/
  step_executor: orchestration  # Agent steps → executeIterativeLoop()

scheduler:
  enabled: true
  mode: simulate
```

## Architecture Notes

### Session → Orchestration Layering

```
FlowmindSessionManager.next()    ← picks the step (progressive disclosure)
  └→ SessionStepExecutor          ← injectable execution strategy
      └→ executeIterativeLoop()   ← orchestration's retry/budget/circuit-breaker
          └→ adapter.run()        ← actual agent execution via lev exec
```

- **FlowMind** owns *which step* to run next (session state)
- **Orchestration** owns *how* to run it (retries, budgets, context pressure)
- **SDLC** owns *what domain rules* apply (entity FSMs, validation gates)

### Migration from prompt-stack

| prompt-stack CLI | FlowMind Session API |
|-----------------|---------------------|
| `init --stack` | `mgr.startFromFile(flow)` |
| `next --session` | `mgr.next(sessionId)` |
| `record --step --report` | Automatic via `session.history` |
| `status --session` | `mgr.status(sessionId)` |
| `validate --session` | Check `session.status === 'completed'` |
