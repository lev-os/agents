# Graph Footer — Shared Skill Fragment

Every lifecycle skill MUST append this footer after output. Single source of truth.

## How to Include

Add to the end of any lifecycle skill's SKILL.md:

```
## Graph Footer
@import ~/.claude/skills/_shared/graph-footer.md
```

Or just paste the template below into the skill's output format.

## The Footer Template

```
---
🧬 {workstream_id} | 📐 {active_overlays} | 🎯 {lifecycle_stage}
⏭️  Next: {proposed_next_verb(s)}
🚦 Gate: {current_gate} = {pass|fail|pending}
🌀 Decision: keep | monitor | execute | reject
---
```

## How to Populate

| Field | Source | How to Read |
|---|---|---|
| workstream_id | `.lev/pm/workstreams/*/state/workstream.yaml` | `grep workstream_id:` |
| active_overlays | `.lev/tasks/<id>/overlays/active.yaml` OR infer from skill names in context | list plugin names contributing |
| lifecycle_stage | Current verb's lane (Shape/Plan/Exec/Close) | from `dna/vernacular.yaml lifecycle_verbs` |
| proposed_next_verb | Computed from gate state | if gate passes → next verb; if fails → remediation verb |
| current_gate | The transition gate being evaluated | from `dna/gates.yaml lifecycle section` |
| decision_point | Set by /capture, visible from then on | keep / monitor / execute / reject |

## Stats Table (optional, for /capture)

When outputting capture sweep results, use this format:

| Metric | Count |
|---|---|
| Total inventoried | N |
| In memory → needs filing | N |
| Transitioning | N |
| Blocked | N |
| Already captured | N files in {path} |

## Verb Reference

```
Shape:   /research  /prior-art  /interview
Plan:    /propose   /capture
Exec:    /exec
Close:   /qa  /accept  /handoff
Router:  /work
```

Full definitions: `dna/vernacular.yaml` section `lifecycle_verbs`
Gate math: `dna/gates.yaml` section `LIFECYCLE TRANSITION GATES`
Visual reference: https://ember-marvel-tbjh.here.now/
