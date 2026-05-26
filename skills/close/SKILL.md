---
name: close
description: Use when verified work is ready for QA, acceptance, checkpointing, learning, recommendation, and handoff.
skill_type: workflow
category: lifecycle
output_template: hud
triggers:
  - close
  - ok
  - done
  - accept
---

# /close - Close Lane

Close the active entity: capture leftovers, verify acceptance, checkpoint, learn,
recommend, and hand off.

## Work Link

Lifecycle lane: Close
Entity movement: `verified -> closed | monitoring | follow_up | blocked`
Workstream: update active workstream before reporting done
Upstream: `/exec`
Downstream: `/handoff`, `/work`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Protocol

```yaml
steps:
  - id: capture_gate
    action: Run capture in gate mode before closing.
    validation: "in_memory_count == 0."
    on_failure: "Route to /capture and stop close."

  - id: qa_acceptance
    action: Check output against task DNA, acceptance criteria, declared verifier evidence, and proof-gate verdicts.
    validation: "Every acceptance item and applicable proof gate is pass, fail, blocked, or explicitly not-tested with residual risk."
    on_failure: "Route failed criteria back to /exec."

  - id: proof_gate_verdict
    action: Seal Pentagon, UltraQA, and ai-slop-cleaner outcomes before acceptance.
    validation: "Feature-local Pentagon verdicts, UltraQA scenario matrix status, generated-artifact cleanup, ai-slop-cleaner review, and residual risks are recorded."
    on_failure: "Do not accept; route to /exec or /propose depending on whether runtime evidence or proof contract is missing."

  - id: accept
    action: Decide whether the work is accepted.
    validation: "Confidence >= 0.85 for auto-accept, otherwise human approval is recorded."
    on_failure: "Do not commit or handoff as closed."

  - id: checkpoint
    action: Stage, commit, pull without rebase, and push when sealing verified work.
    validation: "Commit and push succeed, or blocker is recorded."
    on_failure: "Keep entity blocked and do not claim closed."

  - id: learn
    action: Extract typed learnings with claim, evidence, applies_to, and propagates.
    validation: "At least one learning or explicit 'no new learning' is recorded."
    on_failure: "Add the learning block before handoff."

  - id: recommend
    action: Recommend keep, monitor, execute, or reject for related entities.
    validation: "Next lifecycle verb is clear."
    on_failure: "Route to /work for next-verb selection."

  - id: handoff
    action: Invoke /handoff to update workstream state and resume prompt.
    validation: "Workstream YAML reflects close result."
    on_failure: "Do not end without durable state."
```

## Trigger Record

When the workstream has a trigger stream, write:

```yaml
schema: lifecycle_trigger.v1
verb: close
entity_ref: ws://<ws-id> | task://<task-id>
outputs:
  items: []
  learnings: []
  gates: []
  proof_gates:
    pentagon: pass | fail | blocked | not_applicable
    ultraqa: pass | fail | blocked | not_applicable
    ai_slop_cleaner: pass | fail | blocked | not_applicable
  artifacts: []
metrics:
  drift: <number>
  in_memory_count: 0
cursor:
  last_verb: close
  next_verb: null
recommend: []
```

## KPI Gate

| KPI | Move on |
|---|---|
| drift_score | `< 0.3` |
| hygiene_pass_rate | `>= 0.95` |
| learning_extracted | `>= 1` or explicit none |
| proof_gate_verdicts | all applicable gates pass or have explicit blocked/follow-up routing |

Max rework: 2. Three consecutive gate failures becomes blocked.

## Red Flags

- "Ready to push when you are."
- "Close can skip capture because the task is done."
- "A passing command means acceptance."
- "Repo-wide audit passed, so feature-local Pentagon proof is done."
- "Temporary QA harness cleanup can be handled later."
- "I'll write handoff later."
- "Pull with rebase."

## Related

- `/exec` provides verified work.
- `/capture` clears in-memory leftovers.
- `/handoff` updates workstream continuity.
- `/work` routes the next entity.
