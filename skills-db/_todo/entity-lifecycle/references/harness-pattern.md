# Harness Execution Pattern

Abstract execution framework for all entity lifecycle operations. Supports inline, detached, and background execution modes with full event bus integration.

## Architecture

```
[Task] -> [Harness.execute()] -> [Adapter.run()] -> [EventBus] -> [Result]
               |
         [JobSpawner] (for detached mode)
               |
         [.lev/ralph/] (persistent state)
```

## Execution Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `inline` | Synchronous, blocks until complete | Quick operations, validations |
| `detached` | Survives parent exit, state persisted | Long-running jobs, deployments |
| `background` | Async, returns immediately | Non-critical updates, notifications |

### Inline Execution {#inline}

Default mode. Task runs in current process, result returned directly.

```typescript
const harness = createHarness('sdk');
await harness.initHarness({ mode: 'inline' });
const result = await harness.execute({
  id: 'task-001',
  prompt: 'Execute operation',
  mode: 'inline'
});
// Blocks until complete, result.success indicates outcome
```

**Events emitted:**
- `harness.initializing` (L1)
- `harness.ready` (L1)
- `job.started` (L1)
- `job.completed` (L1) or `job.failed` (L2)

### Detached Execution {#detached}

Job survives parent process exit. State persisted to disk.

```typescript
const result = await harness.execute({
  id: 'deploy-001',
  prompt: 'Deploy to production',
  mode: 'detached',
  jobMeta: { environment: 'prod' }
});
// Returns immediately with job ID
// result.statePath = '.lev/ralph/deploy-001-xxx/state.json'
// result.logPath = '.lev/ralph/deploy-001-xxx/log.jsonl'
```

**State file structure:**
```json
{
  "jobId": "deploy-001-m3k-7x9f",
  "status": "running",
  "startedAt": "2026-01-15T10:30:00Z",
  "lastHeartbeat": "2026-01-15T10:31:00Z",
  "progress": 0.45,
  "metadata": { "environment": "prod" }
}
```

**Monitoring detached jobs:**
```bash
# Check state
cat .lev/ralph/deploy-001-*/state.json | jq '.status'

# Tail logs
tail -f .lev/ralph/deploy-001-*/log.jsonl

# List all running jobs
ls -la .lev/ralph/*/state.json | xargs grep '"status": "running"'
```

### Background Execution {#background}

Fire-and-forget within current process. Useful for non-blocking side effects.

```typescript
const result = await harness.execute({
  id: 'notify-001',
  prompt: 'Send notification',
  mode: 'background'
});
// Returns immediately with job ID
// Events emitted when job completes (later)
```

**Events emitted:**
- `job.started` (L1)
- `job.background.completed` (L1) or `job.background.failed` (L3)

## Harness Status Lifecycle

```
idle -> initializing -> ready -> executing -> awaiting -> completing -> completed
                                    |             |             |
                                    v             v             v
                                 failed       aborted       completed
```

| Status | Description | Mapped Adapter Status |
|--------|-------------|-----------------------|
| `idle` | Not started | ready |
| `initializing` | Config loading | initializing |
| `ready` | Ready to execute | ready |
| `executing` | Task in progress | running |
| `awaiting` | Waiting for external | running |
| `completing` | Cleanup in progress | running |
| `completed` | Success terminal | ready |
| `failed` | Error terminal | error |
| `aborted` | Cancelled | aborting |

## Extended Task Interface

```typescript
interface HarnessTask {
  id: string;           // Task identifier
  prompt: string;       // Task instruction
  mode?: ExecutionMode; // inline | detached | background
  promise?: string;     // Completion detection string
  maxIterations?: number; // Max retries
  jobMeta?: Record<string, unknown>; // Metadata for state tracking
}
```

## Extended Result Interface

```typescript
interface HarnessResult {
  success: boolean;
  output: string;
  error?: string;
  durationMs?: number;
  jobId?: string;        // For tracking
  statePath?: string;    // Detached mode
  logPath?: string;      // Detached mode
  promiseDetected?: boolean;
  iterations?: number;
}
```

## Promise Detection

Detect completion via output markers:

```typescript
const result = await harness.execute({
  id: 'build-001',
  prompt: 'Build project',
  promise: 'BUILD_COMPLETE'  // Looks for <promise>BUILD_COMPLETE</promise>
});

if (result.promiseDetected) {
  // Completion marker found in output
}
```

## Event Bus Integration

All operations emit events to the global event bus:

```typescript
// Subscribe to events
const unsub = harness.subscribeToEvents('job.*', (event) => {
  console.log(`${event.source}.${event.event}: ${event.level}`);
});

// Get history for specific job
const events = harness.getEventHistory('deploy-001-m3k-7x9f');
```

## Event Levels

| Level | Severity | Use Case |
|-------|----------|----------|
| `L0` | Trace | Status changes, debug |
| `L1` | Info | Normal operations |
| `L2` | Warning | Non-critical failures |
| `L3` | Error | Critical, requires attention |

## Creating Custom Harnesses

Extend the base class:

```typescript
import { Harness, registerHarness } from './harness';

class MyHarness extends Harness {
  async doInit(config: HarnessConfig): Promise<void> {
    // Provider-specific initialization
  }

  async doRun(task: Task): Promise<Result> {
    // Provider-specific execution
  }

  async doAbort(reason: string): Promise<void> {
    // Provider-specific abort
  }

  protected buildDetachedArgs(task: HarnessTask): string[] {
    return ['run', task.prompt, '--detached'];
  }
}

registerHarness('my-harness', () => new MyHarness());
```

## Integration with Entity Actions

The harness wraps `EntityAction` emitter for 3-phase logging:

```typescript
const emitter = createEmitter({ entity: 'idea' });

await emitter.execute(
  'promote',
  { idea_id: 'idea-001', target: 'bead' },
  async () => {
    // PRE: event emitted automatically
    const result = await harness.execute(promoteTask);
    // POST: event emitted automatically
    return result;
  }
);
// ERROR: event emitted automatically on throw
```

## Storage Locations

| Artifact | Path | Purpose |
|----------|------|---------|
| Detached state | `.lev/ralph/<job-id>/state.json` | Job status tracking |
| Detached logs | `.lev/ralph/<job-id>/log.jsonl` | Execution logs |
| Checkpoints | `.lev/ralph/<job-id>/checkpoint.json` | Crash recovery |
| Events | `~/.lev/events.jsonl` | Global event stream |
| Audit | `~/clawd/logs/audit/events.jsonl` | Critical events (L3) |

---

*For lifecycle state machines, see parent skill `lev-lifecycle`. For entity-specific actions, see `entity-actions.md`.*
