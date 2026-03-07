# Phase Transitions

Validation gates, triggers, and automation for entity state transitions.

## State Machines

### Idea Lifecycle

```
captured -> classified -> crystallizing -> crystallized -> manifesting -> completed
                |                                              |
                v                                              v
             parked                                    blocked -> discarded
```

| Transition | Trigger | Validation Gate | Auto? |
|------------|---------|-----------------|-------|
| captured -> classified | PARA routing complete | confidence >= 0.6 | Yes (5s) |
| captured -> parked | Low confidence | confidence < 0.6 | Yes |
| classified -> crystallizing | User/agent starts refinement | None | Manual |
| crystallizing -> crystallized | Interview complete | handlers identified | Manual |
| crystallized -> manifesting | Execution started | handler available | Manual |
| manifesting -> completed | Done state verified | all criteria pass | Manual |
| manifesting -> blocked | Blocker detected | None | Auto |
| blocked -> discarded | Explicit abandon | User confirmation | Manual |

### Session Lifecycle

```
active -> paused -> continued -> active
            |
            v
       compacting -> compacted -> archived
```

| Transition | Trigger | Validation Gate | Auto? |
|------------|---------|-----------------|-------|
| active -> paused | `/handoff` command | Handoff created | Manual |
| paused -> continued | `/continue` command | Context loadable | Manual |
| active -> compacting | Token threshold | None | Auto |
| compacting -> compacted | Summary generated | Summary valid | Auto |
| compacted -> archived | 30 days elapsed | None | Auto |

### Bead Lifecycle

```
open -> in_progress -> completed
            |
            v
         blocked -> open (unblocked)
```

| Transition | Trigger | Validation Gate | Auto? |
|------------|---------|-----------------|-------|
| open -> in_progress | `bd update --status` | None | Manual |
| in_progress -> completed | `bd close` | Reason provided | Manual |
| in_progress -> blocked | Dependency failed | Blocker identified | Manual |
| blocked -> open | Blocker resolved | Dependencies clear | Auto (bd dep) |

### Synth Lifecycle

```
spawned -> active -> promoting -> system | archived
```

| Transition | Trigger | Validation Gate | Auto? |
|------------|---------|-----------------|-------|
| spawned -> active | First success | Execution complete | Auto |
| active -> promoting | success_count >= threshold | threshold met | Auto |
| promoting -> system | Promotion complete | Quality gate pass | Manual |
| * -> archived | 7d idle or explicit | None | Auto/Manual |

## Validation Gates {#gates}

Quality checks that must pass before transition.

### Gate Types

| Gate | Input | Output | Use Case |
|------|-------|--------|----------|
| confidence_threshold | float | pass/fail | Idea classification |
| handler_available | handler_id | pass/fail | Manifestation start |
| dependencies_clear | entity_id | pass/fail/wait | Any transition |
| quality_criteria | output | pass/remediate/block | Phase completion |
| user_confirmation | prompt | pass/fail | Destructive actions |

### Confidence Threshold Gate

```yaml
gate: confidence_threshold
input:
  entity_id: idea-001
  threshold: 0.6

validation: |
  1. Read entity confidence score
  2. Compare to threshold
  3. If >= threshold: PASS
  4. If < threshold: FAIL (route to parked)

output:
  passed: boolean
  confidence: float
  recommendation: "proceed" | "park" | "interview"
```

### Dependencies Clear Gate

```yaml
gate: dependencies_clear
input:
  entity_id: lev-001b
  dependency_ids: [lev-2598, lev-pno8]

validation: |
  1. For each dependency:
     - Check status (open/in_progress/completed)
     - If not completed: record blocker
  2. If all completed: PASS
  3. If any blocking: FAIL with blockers list

output:
  passed: boolean
  blockers: [{id, status, reason}]
  can_wait: boolean  # true if blockers are in_progress
```

### Quality Criteria Gate

```yaml
gate: quality_criteria
input:
  entity_id: idea-001
  output: {manifestation_result}
  criteria:
    - name: tests_pass
      check: "output.test_results.failed == 0"
      threshold: 1.0
    - name: docs_complete
      check: "output.docs_generated"
      threshold: 0.8

validation: |
  For each criterion:
  1. Evaluate check expression
  2. Score 0.0-1.0
  3. Compare to threshold

  Decision:
  - All pass: PROCEED
  - Some fail but recoverable: REMEDIATE
  - Critical fail: BLOCK
  - Uncertain: REVIEW

output:
  decision: "proceed" | "remediate" | "block" | "review"
  overall_score: float
  criteria_results: [{name, score, passed, details}]
  remediation_steps: [string]
```

## Automatic Triggers {#triggers}

Conditions that auto-trigger transitions.

### Time-Based Triggers

```yaml
triggers:
  - name: archive_old_sessions
    schedule: "0 0 * * *"  # Daily at midnight
    condition: |
      session.status == "compacted"
      AND days_since(session.compacted_at) > 30
    action: transition(session, "archived")

  - name: archive_idle_synths
    schedule: "0 * * * *"  # Hourly
    condition: |
      synth.status == "active"
      AND days_since(synth.last_run) > 7
    action: transition(synth, "archived")
```

### Event-Based Triggers

```yaml
triggers:
  - name: auto_classify_ideas
    event: "idea.captured"
    delay: 5s
    condition: idea.status == "captured"
    action: |
      classify_idea(idea)
      IF confidence >= 0.6:
        transition(idea, "classified")
      ELSE:
        transition(idea, "parked")

  - name: unblock_on_dependency_complete
    event: "bead.completed"
    condition: true
    action: |
      FOR each blocked_bead waiting on this bead:
        IF all_dependencies_complete(blocked_bead):
          transition(blocked_bead, "open")
```

### Threshold-Based Triggers

```yaml
triggers:
  - name: promote_successful_synths
    check_interval: 60s
    condition: |
      synth.status == "active"
      AND synth.success_count >= synth.promote_threshold
    action: transition(synth, "promoting")

  - name: compact_on_token_limit
    check_interval: continuous
    condition: |
      session.status == "active"
      AND session.token_count > TOKEN_THRESHOLD
    action: transition(session, "compacting")
```

## Transition Actions

What happens during each transition.

### Pre-Transition

1. Validate gate(s) if any
2. Emit `{entity}.{transition}.pre` event
3. Create state_history entry

### During Transition

1. Update entity status
2. Execute transition-specific logic
3. Track duration

### Post-Transition

1. Emit `{entity}.{transition}.post` event
2. Trigger downstream transitions
3. Update related entities

### On Error

1. Rollback status if possible
2. Emit `{entity}.{transition}.error` event (level escalated)
3. Log to critical audit if L3

## Manual Transition API

```bash
# Via CLI
lev lifecycle transition <entity-id> --to <state>
lev lifecycle transition idea-001 --to crystallized

# With reason
lev lifecycle transition lev-001b --to blocked --reason "Waiting for API key"

# With force (skip gates)
lev lifecycle transition idea-001 --to completed --force
```

## Event Emission

Every transition emits events:

```jsonl
{"entity":"idea","action":"transition","phase":"pre","status":"pending","level":"L1","meta":{"id":"idea-001","from":"crystallizing","to":"crystallized"},"timestamp":"..."}
{"entity":"idea","action":"transition","phase":"post","status":"success","level":"L1","meta":{"id":"idea-001","from":"crystallizing","to":"crystallized"},"timestamp":"...","duration_ms":45}
```

## State History

Entities maintain full state history:

```yaml
state_history:
  - state: captured
    timestamp: "2026-01-13T08:00:00Z"
    trigger: "WhatsApp message intake"

  - state: classified
    timestamp: "2026-01-13T08:00:05Z"
    trigger: "auto_classify_ideas"
    confidence: 0.78

  - state: crystallizing
    timestamp: "2026-01-13T09:00:00Z"
    trigger: "user_command"
    actor: "claude-cli"

  - state: crystallized
    timestamp: "2026-01-13T10:30:00Z"
    trigger: "interview_complete"
    handlers: [ralph-tui, haiku_swarm]
```

## Transition Hooks

Custom logic per transition:

```yaml
# ~/.config/lev/lifecycle-hooks.yaml
hooks:
  idea.crystallizing:
    - hook: dependency_checker
      input:
        required_dependencies:
          - { type: "config", id: "{{domain}}" }

  idea.manifesting:
    - hook: checkpoint_manager
      input: { mode: "save", interval: "5m" }
    - hook: error_handler
      on: "any_error"
    - hook: quality_gate
      before_transition_to: "completed"

  synth.promoting:
    - hook: quality_gate
      input:
        quality_criteria:
          - { name: "success_rate", check: "success_count / total_runs", threshold: 0.9 }
          - { name: "no_recent_failures", check: "days_since_last_failure", threshold: 7 }
```

## Blocked State Handling

Special handling for blocked entities:

```yaml
blocked_handling:
  detect:
    - dependency_failed
    - resource_unavailable
    - user_intervention_required

  actions:
    - record_blocker(reason, blocking_entity)
    - emit_event("blocked", {blocker, reason})
    - notify_if_critical(priority <= 1)

  unblock:
    - check_blockers_resolved()
    - IF all_resolved: transition("open")
    - emit_event("unblocked", {resolved_blockers})
```

---

*For action logging, see `entity-actions.md`. For storage locations, see `storage-organization.md`. For full hook definitions, see parent skill `lev-lifecycle` references/hooks.md.*
