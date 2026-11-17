# Plan Lifecycle

For `lev-plan` Lifecycle mode and for any write of plan frontmatter: the plan
types, the frontmatter keys, the states, and the commands.

## Plan Types and Files

| Type | Pattern | Purpose |
|---|---|---|
| `plan-impl` | `plan-impl-*` | Feature or capability delivery |
| `plan-bugfix` | `plan-bugfix-*` | Defect investigation and resolution |
| `plan-chore` | `plan-chore-*` | Maintenance, cleanup, docs, tooling |
| `plan-research` | `plan-research-*` | Investigation with knowledge output |
| `plan-migration` | `plan-migration-*` | Transition between well-defined system shapes |

Required frontmatter remains backward-compatible. These keys go between the `---` lines at the top of the plan file:

```yaml
type: plan-impl
status: crystallizing
priority: 2
slug: stable-kebab-name
created_at: YYYY-MM-DD
done_condition: "observable deterministic completion"
steps:
  - description: "claim-shaped step"
    validation: "check that can prove the claim"
acceptance_criteria: []
gates: []
```

New or materially updated standard/deep plans should also include:

```yaml
plan_depth: standard | deep
source_refs: []
fidelity_score: 0.0
review_state: unreviewed | needs_review | approved | implementation_handoff
first_slice: stable-slice-id | null
open_decisions: []
```

## Lifecycle FSM

```text
draft -> ready -> in_progress -> needs_validation -> validated -> done -> archived
                         |              |
                         +-> blocked    +-> ready on failed validation
```

Transitions:

- `draft -> ready`: source fidelity and semantic readiness pass; first slice exists.
- `ready -> in_progress`: an executor claims the plan or an emitted task references it.
- `in_progress -> needs_validation`: implementation is complete, not merely attempted.
- `needs_validation -> validated`: fitness functions and acceptance pass.
- `validated -> done`: move to `_done/` when no remaining plan work exists.
- `in_progress -> blocked`: concrete code/decision dependency prevents progress.
- `done -> archived`: historical reference only.

The frontmatter example's `status` word and this state list differ, and real
plans use both. Which list wins is not settled (Leviathan debt row M1131): keep
the word the plan file already uses, and for a new plan take the word that
`lev entity plan validate` accepts.

## Operations

```bash
lev entity plan list                # the plans of the project
lev entity plan show <plan-id>      # one plan's state
lev entity plan validate <plan-id>  # structure and state checks
lev entity plan history <plan-id>   # past transitions
lev entity plan transition --help   # move a plan along the FSM; --help names its arguments
bd show <bd_id>
bd create --title="Implement feature X" --type=task -p 2
bd close <bd_id> --reason "completed per plan"
```

Update `status` in frontmatter for transitions. On validated completion, move the
plan to `.lev/pm/plans/_done/`. Do not create a second plan to represent a state
transition.
