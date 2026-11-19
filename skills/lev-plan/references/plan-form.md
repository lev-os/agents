# Plan Form

The one form of a plan: a YAML record, `.lev/pm/plans/{id}.yaml`, that states `schema: lev.plan.v1`. Read it before
`write_or_patch`, before a plan is rendered in the response, and when a Review reads a plan file.

## Contents

- [Where the form is declared](#where-the-form-is-declared)
- [The record](#the-record)
- [Depth](#depth)
- [Check it](#check-it)
- [Older plans](#older-plans)

## Where the form is declared

The plan record type declares the form (JP 2026-11-17: "the plan should be a yaml file, schema backed"; JP
2026-11-18: "validation is a product of entity/schema declaration"). In Leviathan the declaration is
`core/workstream/config/entities/plan.yaml`: its `fields` name the keys, and its check row
`plan_form_holds_eight_parts` holds the shape. This file shows the form; when it differs from the declaration, the
declaration wins. This skill holds no schema file and no check script.

## The record

The eight parts are top-level keys. What each part must hold is in [Plan parts](plan-parts.md), [Slices](slices.md)
and [Proof](proof.md); this file gives only the keys.

```yaml
id: {slug}                    # the file name without .yaml
type: plan
schema: lev.plan.v1          # exactly this value
status: crystallizing         # one of the type's states (Lifecycle)
workstream_id: {id}           # when a workstream is bound
title: {one line}
plan_type: plan-impl          # plan-impl | plan-bugfix | plan-chore | plan-research | plan-migration
depth: light                  # light | standard | deep
run: bounded                  # bounded | long | parallel
owner: {who owns the plan}
refs: []                      # typed references, for example the feature this plan implements

source:                       # part 1
  refs: [{capture | design | plan | task ref}]
  fidelity_score: 0.0
  rows:                       # one for each material source row (Source Fidelity Gate)
    - { intent_id: INT-1, source_ref: "", requirement: "", destination: "", claim: "", preservation: "", fidelity: 0.0, note: "", route: "" }
outcome:                      # part 2
  success: {the success sentence}
  why: {the result the operator sees, and why it matters}
  definitions:
    - { term: "", meaning: "", degenerate: "" }
  does_not_count:
    - { near_miss: "", excluded_by: "{claim id | guard of a claim | review checklist}" }
  in_scope: []                # core/state refuses a key named scope inside a record (core/state/src/scope.ts)
  out_of_scope: []
  human_decisions: []
  forbidden: []
  boundaries: []
current_to_target:            # part 3
  current: {evidence, authority, freshness, known uncertainty}
  target: {the target state and the smallest transition}
  options:
    - { id: a, benefits: "", costs: "", invalidated_by: "", ruling: "" }
  chosen: {the approach and its tradeoffs}
  experts:
    - { domain: "", says: "" }
  map:
    - { current: "", target: "", action: "keep | change | migrate | retire", owner: "" }
slices:                       # part 4; this list is the one slice record
  - id: s1
    intent_ids: []
    outcome: ""
    owner: ""                 # the owner skill or person (Domain Owners)
    allowed_effects: ""
    artifact: ""              # path; format {version, frozen} when a long run reads it
    depends_on: []
    claims: []
    stop: ""
    run_budget: ""
    status: ready
    open_decisions: []
claims:                       # part 5; this list is the one claim list
  - id: c1
    polarity: must            # must | must_not
    text: ""
    slice: s1
    rules_out: ""             # the failure it rules out
    proven_by: program        # program | agent | person; the proof goes under the key of the same kind (below)
    program: ""               # proven_by program: the command
    level: local              # local | integration | field | external
    guard: ""                 # program: the known-bad control and the check owner; any: what looks like proof and is not
    source: ""
  - id: c2
    polarity: must_not
    text: ""
    proven_by: agent
    question: ""              # proven_by agent: the question the agent answers; never under program
  - id: c3
    polarity: must
    text: ""
    proven_by: person
    person: ""                # proven_by person: who, with the evidence they give; never under program
review_and_repair:            # part 6
  checklist: ""
  blocks_when: ""
  non_blocking: logged; never delays return
  outside_loop_proof: ""
  review_runs: []             # the review skill's chat line for each run, with its report file
  recall: ""
  at_cap: ""
return_and_resume:            # part 7
  return_when: ""
  incomplete_only_on: ""
  frontier: ""
  open_branches: []
risk_and_rollback:            # part 8
  risks:
    - { failure: "", mechanism: "", prevention: "", detection: "", residual: "" }
  pre_mortem: []              # deep or high-risk: three credible scenarios
  rollback: ""
  review_triggers: []
first_slice: s1
next: ""                      # lev-plan emit {slice} | map | /exec | skill://poc | /interview | resume {unit}
long_run: {}                  # only when Long-horizon planning applies: its blocks, one key each
```

Write no placeholder: leave out a key of a part that has nothing to say, never the part.

## Depth

Every plan keeps all eight parts, and none is empty. A light plan writes a part as one line of text in place of its
keys (`review_and_repair: "One review read; at most one reread."`), except `slices` and `claims`: those two are a
list at every depth, and a light plan has one slice and one claim with its proof or more. A deep plan fills every key
that applies and every `source.rows` row.

## Check it

```bash
lev entity plan validate {id} --json
```

It reads the record, runs the type's check row over every plan of the project that states a plan form, and core/eval
decides pass, fail or could not check. The check refuses:

| Code | What is wrong |
|---|---|
| `PLAN_PART_MISSING` | a part is missing or empty |
| `PLAN_PART_NOT_A_LIST` | `slices` or `claims` is not a list |
| `PLAN_FORM_UNKNOWN` | `schema` is another `lev.plan.` value |
| `CLAIM_INCOMPLETE` | a claim has no id or no text |
| `CLAIM_POLARITY_UNKNOWN` | a polarity is not `must` or `must_not` |
| `CLAIM_HAS_NO_PROOF` | `proven_by` is not program, agent or person, or the key of that kind is blank: `program` for program, `question` for agent, `person` for person. A question or a person written under `program` is this fault |
| `CLAIM_SLICE_UNKNOWN` | a claim names a slice that is not in `slices` |
| `SLICE_INCOMPLETE` | a slice has no id, outcome or owner |
| `SLICE_ID_TWICE` | two slices have one id |
| `READ_PARSE_ERROR` | the file states the form and does not parse |
| `PLAN_STATUS_MISSING` | a plan of any form says no `status` (the type's second row, `plan_says_its_stage`; JP 2026-11-19) |

A pass says the form holds. It does not say the plan is good: readiness is still judged ([Plan parts](plan-parts.md#readiness)).

In a project where the command is missing or the plan type has no check row, say "could not check" and go on; do not
write a check of your own.

## Older plans

A plan file that states no `schema` is an older plan: Markdown with frontmatter, or YAML in another shape. The check
does not judge it. Keep its form when you patch it. Move it to this form only when the operator asks, or when Deepen
rewrites most of it.
