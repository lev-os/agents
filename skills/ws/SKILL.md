---
name: ws
description: Use when scanning, finding, resuming, merging, branching, or untangling Lev workstreams.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /ws - Workstream Operations

Workstream YAML is the durable identity for lifecycle work until workstreams are
graph ops. `/ws` is the projection and repair surface around
`.lev/pm/workstreams/*/state/workstream.yaml`.

## Work Link

Lifecycle lane: Router
Entity movement: `unknown | stale | split -> routed | active | paused`
Workstream: this skill resolves or updates workstream identity
Upstream: `/work`, any lifecycle skill missing workstream context
Downstream: `/work`, `/capture`, `/propose`, `/exec`, `/handoff`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Commands

```text
/ws                    # scan all workstreams
/ws list               # same as /ws
/ws find <query>       # search workstreams and projections
/ws show <id>          # show one workstream state
/ws resume <id>        # load state, recent projections, and next verb
/ws merge <a> <b>      # combine lineages with conflicts called out
/ws branch <id> <name> # fork a workstream
/ws untangle           # detangle agents/lane claims
```

## Protocol

```yaml
steps:
  - id: read_state
    action: Read matching workstream YAML files.
    validation: "At least one state file was read, or no match is explicit."
    on_failure: "Do not infer identity from memory only."

  - id: associate_projection
    action: Link handoffs, plans, captures, decisions, and tasks that mention the workstream.
    validation: "Output separates durable state from projection files."
    on_failure: "Show durable state only and mark projections unknown."

  - id: choose_next_verb
    action: Recommend the lifecycle owner for the next entity movement.
    validation: "Next verb is one of /capture, /prior-art, /propose, /exec, /close, /handoff."
    on_failure: "Route back to /work."
```

## Data Sources

- `.lev/pm/workstreams/*/state/workstream.yaml`
- `.lev/pm/workstreams/*/captures/*`
- `.lev/pm/tasks/*/{dna.yaml,execution.yaml}`
- `.lev/pm/handoffs/*.md` as projections
- `.lev/pm/plans/*.md`, `.lev/pm/designs/*.md`, `.lev/pm/decisions/*`
- `.lev/mail/*` when detangling

## Rules

- Workstream YAML wins over handoff markdown.
- Merges preserve both lineages and flag conflicting objectives.
- Branches copy the parent state, set provenance to the parent, and clear session extensions.
- Resume reports what changed since the last projection before proposing a next verb.

## Related

- `/work` routes after `/ws` resolves identity.
- `/handoff` writes end-of-session state.
- `/capture` writes workstream capture artifacts.
