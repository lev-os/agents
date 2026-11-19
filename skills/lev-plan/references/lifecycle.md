# Plan Lifecycle

For `lev-plan` Lifecycle mode and for any write of a plan's `status`: the plan types, the states, and the commands.

## Plan Types and Files

| Type | Pattern | Purpose |
|---|---|---|
| `plan-impl` | `plan-impl-*` | Feature or capability delivery |
| `plan-bugfix` | `plan-bugfix-*` | Defect investigation and resolution |
| `plan-chore` | `plan-chore-*` | Maintenance, cleanup, docs, tooling |
| `plan-research` | `plan-research-*` | Investigation with knowledge output |
| `plan-migration` | `plan-migration-*` | Transition between well-defined system shapes |

The type goes in the record's `plan_type` key. The record's keys are in the [plan form](plan-form.md).

## Lifecycle States

The plan record type declares the states and the moves; this list shows them, and the declaration wins. A plan's
`status` is one of the seven stages of work and nothing else (JP 2026-11-01, the status words cutover).

```text
ephemeral -> captured -> crystallizing -> crystallized -> manifesting -> completed
                 |             |               |              |
                 +-------------+---------------+--------------+-> discarded
```

| Event | Move | When |
|---|---|---|
| `captured` | ephemeral -> captured | the plan record exists |
| `shaped` | captured -> crystallizing | the plan is being written or deepened |
| `crystallized` | crystallizing -> crystallized | source fidelity and readiness pass; a first slice exists |
| `started` | crystallized -> manifesting | an executor takes the plan, or an emitted task names it |
| `completed` | manifesting -> completed | every claim is satisfied by its proof |
| `discarded` | captured, crystallizing, crystallized or manifesting -> discarded | the plan is dropped; a plan dropped for another names it in `superseded_by` |

Why a plan waits (blocked, needs validation) is not a state: say it in `return_and_resume`. An older plan may hold
another word (draft, ready, in_progress, done); keep it until the plan moves to the plan form.

## Operations

```bash
lev entity plan list         # the plans of the project
lev entity plan show         # one plan's state
lev entity plan validate     # structure and state checks
lev entity plan history      # past transitions
lev entity plan transition   # move a plan by one event: lev entity plan transition {id} {event}
# each verb's --help names its arguments
bd show <bd_id>
bd create --title="Implement feature X" --type=task -p 2
bd close <bd_id> --reason "completed per plan"
```

Move a plan with `lev entity plan transition`; do not edit `status` by hand in a plan that states the plan form. Do not create a second plan to represent a state
transition.
