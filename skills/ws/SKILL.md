---
name: ws
description: Use when attaching a session to a workstream, or scanning, finding, resuming, merging, branching, or untangling Lev workstreams.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /ws - Workstream Operations

Workstream YAML is the durable identity for lifecycle work until workstreams are
graph ops. `/ws` is the projection and repair surface around
`.lev/pm/workstreams/*/state/workstream.yaml`.

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
island/provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

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
/ws --attach [id]      # identify/reuse a workstream and bind this session
/ws merge <a> <b>      # combine lineages with conflicts called out
/ws branch <id> <name> # fork a workstream
/ws untangle           # detangle agents/lane claims
```

## Attach a Session

`skill://ws --attach` is skill syntax. It is not a claim that `lev ws --attach`
or equivalent SDK/Poly operations are implemented.

1. Announce only `🧭 locating workstream...` during orientation. Resolve the
   actual session identity, project root, existing binding and explicit target.
2. Reuse a matching workstream folder and its owned outcome/plan pointers.
   A pasted HUD or incidental filename is candidate evidence, not authorization
   to change the binding. If candidates remain ambiguous, ask for the choice.
   Create a workstream only when none fits and creation is within the request.
3. Use the installed, authorized session-binding adapter or verified runtime
   operation. Inspect its help/contract first. Persist the session-to-workstream
   reference and read it back; report attached only after IDs and paths agree.
   If no binding writer is available, retain the selected reference and report
   attachment unavailable rather than inventing a CLI command.
4. Reuse an existing Markdown context projection of relevant paths and summaries;
   create/update one only when requested. Keep workstream identity durable across
   commits, with commit/checkpoint references describing particular revisions.
   Emit available footer values only. An orientation attempt is not a successful
   attachment; record the actual outcome in the selected adapter.

When the Lev workstream CLI/SDK/Poly attachment work lands, replace the manual
adapter step with its verified operation, preserve session/workstream identity,
and test no-match, ambiguous, existing, and explicit-switch cases across surfaces.
Keep this follow-up in the existing lifecycle/Entire plans; no parallel tracker.

## Protocol

```yaml
steps:
  - id: read_state
    action: Read matching workstream YAML files.
    validation: "At least one state file was read, or no match is explicit."
    on_failure: "Do not infer identity from memory only."

  - id: associate_projection
    action: Follow the current state's named artifact pointers. Search broadly for other projections only when a pointer is missing, stale, or contradictory.
    validation: "Output separates durable state from projection files."
    on_failure: "Show durable state only and mark projections unknown."

  - id: reconcile_navigation
    action: Reuse the saved outcome map, tracker binding, evidence revision, and rolling horizon when their inputs are unchanged. Reconcile only affected fields after a material change.
    validation: "The horizon has at most ten stable-ID steps; steps 1-3 carry owner, prerequisites, permitted effects, check, and stop condition, or the missing field is an explicit blocker."
    on_failure: "Load skill://lev recursive wayfinding; do not manufacture readiness."

  - id: choose_next_verb
    action: Recommend the lifecycle owner for the next entity movement.
    validation: "Next owner is eligible for the saved entity state and active domain overlay, using the Next Routes table; read-only resume does not execute it."
    on_failure: "Route back to skill://lev."
```

## Next Routes

Preserve the saved frontier and select its owner; resolving identity does not
restart planning. Show only applicable choices as a numbered `skill://<name>`
table when uncertain; otherwise name the next route. Resume grants no new authority.

| Saved state or gap | Next owner |
|---|---|
| Uncaptured intent | `skill://capture` |
| Evidence stale or missing | `skill://prior-art` |
| Material decision open | `skill://interview` |
| Broad plan absent or incomplete | `skill://lev-plan` |
| Coding slice needs specification or revision | `skill://propose` |
| Authorized action ready with current scope and checks | `skill://exec`; non-coding may use its sufficient plan without proposal |
| Outcome verified, acceptance pending | `skill://close` |
| Pause or blocker remains | `skill://handoff` |
| Domain or transition unresolved | `skill://lev` |

## Data Sources

Resolve artifact references using their declared base. For an unqualified local
reference, check its exact project-root path and the referring artifact's
directory within authorized scope. If both exist with different content, expose
the ambiguity rather than choosing silently. If neither exists, use a bounded
filename inventory; searching file contents for a filename does not establish
that the file is absent. Report the locations actually checked and distinguish
missing, unreadable and ambiguous references before declaring the frontier blocked.

- `.lev/pm/workstreams/*/state/workstream.yaml`
- `.lev/pm/workstreams/*/captures/*`
- `.lev/pm/tasks/*/{dna.yaml,execution.yaml}`
- `.lev/pm/handoffs/*.md` as projections
- `.lev/pm/plans/*.md`, `.lev/pm/designs/*.md`, `.lev/pm/decisions/*`
- `.lev/mail/*` when detangling

## Rules

- Workstream YAML wins over handoff markdown.
- Persist outcome and map identity plus revision/event state in top-level
  `navigation_state`; persist the ordered projection in `next_10`. Keep one
  tracker binding with config provenance. The tracker owns task status; the
  workstream stores identities and relationships, not a second status database.
- Horizon positions may change while stable entity IDs remain fixed. Refresh
  after material evidence, decision, dependency, failure, or handoff changes;
  preserve later milestones and exclusions in the outcome map rather than
  crowding more than ten steps into the projection.
- Reuse compatible shared release, documentation, distribution, support, and
  marketing task identities from the bound tracker. Changing tracker backends
  requires an explicit migration and ID map.
- Merges preserve both lineages and flag conflicting objectives.
- Branches copy the parent state, set provenance to the parent, and clear session extensions.
- Resume reports what changed since the last projection and refreshes affected
  horizon steps before proposing a next verb. Resume grants no new authority.

## Related

- `/work` routes after `/ws` resolves identity.
- `/handoff` writes end-of-session state.
- `/capture` writes workstream capture artifacts.
