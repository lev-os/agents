# Entity Actions

Universal lifecycle-aware logging for all entity operations. Implements pre/post/error phases with duration tracking and hook-based extensibility.

## Design Philosophy

```
                    DETERMINISTIC
  90% of work: fetch, parse, store, transform, emit
                        |
                        v
                LLM DECISION POINTS (Hooks)
  - Error triage: retry vs workaround vs escalate
  - Quality gates: pass vs fail vs needs-review
  - Routing: which handler for this input?
```

## 3-Phase Execution Pattern

Every entity action follows this pattern:

```
PRE   -> Emit pending event, validate inputs
EXEC  -> Perform the action, track duration
POST  -> Emit success event, trigger downstream
ERROR -> Escalate level, emit error event, suggest recovery
```

### Phase Details

| Phase | Status | Level | Events |
|-------|--------|-------|--------|
| pre | pending | L1 | `{entity}.{action}.pre` |
| post | success | L1 | `{entity}.{action}.post` |
| error | failure | L2+ | `{entity}.{action}.error` |

### Level Escalation on Error

| Original | Escalated |
|----------|-----------|
| L0 | L1 |
| L1 | L2 |
| L2 | L3 |
| L3 | L3 (max) |

## ActionEmitter API

```typescript
import { createEmitter, ActionEmitter } from './entity-action';

const emitter = createEmitter({
  entity: 'idea',
  defaultLevel: 'L1',
  consoleLog: true,
  auditDir: '~/clawd/logs/audit'
});

// Execute with automatic 3-phase logging
const result = await emitter.execute(
  'promote',                          // action name
  { idea_id: 'idea-001', target: 'bead' }, // metadata
  async () => {
    // Your action logic here
    return { beadId: 'lev-xyz' };
  },
  { level: 'L1', correlationId: 'corr-123' }
);
```

## Event Structure

```typescript
interface EntityAction<TMeta = Record<string, any>> {
  entity: string;      // e.g., 'idea', 'session', 'bead'
  action: string;      // e.g., 'promote', 'close', 'archive'
  phase: Phase;        // 'pre' | 'post' | 'error'
  status: Status;      // 'pending' | 'success' | 'failure'
  level: Level;        // 'L0' | 'L1' | 'L2' | 'L3'
  meta: TMeta;         // Action-specific metadata
  timestamp: string;   // ISO 8601
  duration_ms?: number; // Only on post/error
  correlationId?: string;
  parentCorrelationId?: string;
}
```

## Standard Actions

### Promote Idea {#promote}

Move idea to BD as tracked task.

```typescript
await emitter.execute(
  'promote',
  {
    idea_id: 'idea-001',
    title: 'Build Flight Deck Dashboard',
    target: 'bead',
    priority: 1
  },
  async () => {
    // 1. Read idea from ~/.lev/ideas/idea-001/
    // 2. Create BD issue: bd create "title" -p 1 -t feature
    // 3. Update idea status to 'manifesting'
    // 4. Return bead ID
    return { beadId: 'lev-xyz' };
  }
);
```

**Events:**
- `idea.promote.pre` (L1, pending)
- `idea.promote.post` (L1, success, duration_ms)

### Close Bead {#close}

Close BD issue with reason.

```typescript
await emitter.execute(
  'close',
  {
    bead_id: 'lev-001b',
    reason: 'Implemented in PR #42',
    completed_items: ['Phase 1', 'Phase 2']
  },
  async () => {
    // bd close lev-001b --reason "..."
    return { closed: true };
  }
);
```

**Events:**
- `bead.close.pre` (L1, pending)
- `bead.close.post` (L1, success)

### Archive Session {#archive}

Move session to archive after handoff.

```typescript
await emitter.execute(
  'archive',
  {
    session_id: 'ses-001',
    handoff_path: '.lev/pm/handoffs/20260115-topic.md',
    reason: 'Work completed'
  },
  async () => {
    // 1. Move handoff to archive
    // 2. Update session status
    return { archived_path: '.lev/pm/archive/20260115-topic.md' };
  }
);
```

### Move Entity {#move}

Manual state transition.

```typescript
await emitter.execute(
  'move',
  {
    entity_type: 'idea',
    entity_id: 'idea-001',
    from_state: 'crystallizing',
    to_state: 'crystallized',
    reason: 'Interview complete'
  },
  async () => {
    // 1. Validate transition is allowed
    // 2. Update entity state
    // 3. Log state_history entry
    return { success: true };
  }
);
```

## Hooks

Extend action behavior with hooks:

```typescript
const emitter = createEmitter({
  entity: 'idea',
  hooks: {
    onPre: async (action) => {
      console.log(`Starting ${action.action}...`);
    },
    onPost: async (action) => {
      // Trigger downstream
      if (action.action === 'promote') {
        await notifySlack(`Idea promoted: ${action.meta.idea_id}`);
      }
    },
    onError: async (action, error) => {
      // Log to critical audit
      await logCritical(action, error);
    }
  }
});
```

### Per-Action Hooks

```typescript
await emitter.execute(
  'promote',
  metadata,
  actionFn,
  {
    hooks: {
      onPost: async (action) => {
        // This hook only runs for this invocation
        await createFollowUpTask(action.meta.beadId);
      }
    }
  }
);
```

## Event Emission

Events are written to:

| Target | Condition | Path |
|--------|-----------|------|
| events.jsonl | All events | `{auditDir}/events.jsonl` |
| critical.jsonl | L3 events only | `{auditDir}/critical.jsonl` |
| Console | If `consoleLog: true` | stdout |

### Console Format

```
L1 [idea.promote] ▶ pre
L1 [idea.promote] ✓ post (142ms)
L2 [idea.promote] ✗ error (89ms)
```

### JSONL Format

```jsonl
{"entity":"idea","action":"promote","phase":"pre","status":"pending","level":"L1","meta":{"idea_id":"idea-001"},"timestamp":"2026-01-15T10:30:00Z","correlationId":"corr-123"}
{"entity":"idea","action":"promote","phase":"post","status":"success","level":"L1","meta":{"idea_id":"idea-001"},"timestamp":"2026-01-15T10:30:00.142Z","duration_ms":142,"correlationId":"corr-123"}
```

## Correlation IDs

Track related actions across phases:

```typescript
const correlationId = crypto.randomUUID();

// Parent action
await emitter.execute('crystallize', meta, fn, { correlationId });

// Child action references parent
await emitter.execute('validate', meta, fn, {
  correlationId: crypto.randomUUID(),
  parentCorrelationId: correlationId
});
```

## Querying Events

```bash
# All events for an entity
cat ~/clawd/logs/audit/events.jsonl | jq 'select(.entity == "idea")'

# Errors only
cat ~/clawd/logs/audit/events.jsonl | jq 'select(.phase == "error")'

# By correlation ID
cat ~/clawd/logs/audit/events.jsonl | jq 'select(.correlationId == "corr-123")'

# Duration analysis
cat ~/clawd/logs/audit/events.jsonl | jq 'select(.duration_ms > 1000)'
```

## Integration with Harness

Actions can wrap harness execution:

```typescript
await emitter.execute(
  'manifest',
  { idea_id: 'idea-001', handler: 'ralph-tui' },
  async () => {
    const harness = createHarness('sdk');
    await harness.initHarness({ mode: 'detached' });
    return await harness.execute({
      id: `manifest-${idea_id}`,
      prompt: manifestationPrompt,
      mode: 'detached'
    });
  }
);
```

## Error Handling

Errors are caught, level is escalated, and error event emitted:

```typescript
await emitter.execute(
  'promote',
  { idea_id: 'idea-001' },
  async () => {
    throw new Error('BD not initialized');
  }
);
// Emits: idea.promote.error (L2, failure)
// Error re-thrown after logging
```

## Best Practices

1. **Always use emitter** - Never perform entity actions without 3-phase logging
2. **Meaningful metadata** - Include IDs, targets, reasons in meta
3. **Correlation IDs** - Use for related operations (e.g., crystallize + validate)
4. **Check L3 events** - Critical log indicates system issues

---

*For execution modes, see `harness-pattern.md`. For storage locations, see `storage-organization.md`.*
