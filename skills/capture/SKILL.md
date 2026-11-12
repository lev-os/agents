---
name: capture
description: Use when inventorying conversation state into durable artifacts with an operator-visible source-fidelity table, routing faithful items toward interview, planning, proposal, or execution, or deep-processing a brain dump.
skill_type: workflow
category: lifecycle
output_template: hud
triggers:
  - capture
  - dump
---

# /capture - Shape to Plan

Inventory conversation state, write durable artifacts, and route each entity to
its next lifecycle owner. `/dump` is `capture --deep`.

## Patch, Route, and Clear

Recognize a brain dump as deep capture. Break the source into rows before
enrichment. Capture is a sort: each row goes to the record of the type Lev
manages (idea, plan, design, decision, backlog item, task), never to a capture
file. Update the record that already holds the topic; write a new record only
when none does (see Where Rows Go).

Before routing or writing, run `lev find` when `lev` is installed. Find the
workstream that owns the topic and whether the matter is already settled:

```bash
lev find "<3-6 topic words>" --type workstream --status ephemeral,captured,crystallizing,crystallized,manifesting --json
lev find "<3-6 topic words>" --type decision --json
```

The workstream statuses are the five live stages; no workstream has the status
`active` since the stages cutover (2026-11-11), so a search for that old status
finds none.

When a row names a thing, ask for the type of record that answers it:

```bash
lev find "<the word or idea>" --type term --type lev_ir --type decision --json  # what Lev calls it; retired or not
lev find "<what it should do>" --type flow --json                              # a flow that already does it
lev find "<the symptom>" --type debt_row --json                                # a known debt row
```

Each card in `result.data.results` has `id`, `type`, `title`, `status`,
`snippet`, `path`, and `line`. A `superseded` card is history: open the record
that superseded it. Record each card that settles, supersedes, or conflicts with
a row (`id` and `path`) in that row's `relationships`. A found decision answers
its question: cite it, and never ask that question again. If `lev` is missing or
the call fails, say so in one line and `rg` over `.lev` and `dna`. `lev find`
skips source code (use codebase-memory or `rg`) and chat history (use `cass`).

Probe prior art for each material row before editing its destination. When the
active workflow authorizes delegation, use a small read-only agent fanout and
reconcile its findings centrally. Decide whether the row updates, supersedes,
duplicates, or conflicts with existing intent. Resolve a conflict from an
explicit ruling or ask the human before the dependent write; never silently
append contradictory canon.

Write through the destination's owner, then read back its relevant projection
and check source fidelity. Only after that check, mark the row `done` with
`next_route: none` and the actual `destination_ref`. Here `done` means the row
reached its record, not implemented or shipped. The table in the reply lists the
rows whose `route_state` is not `done` or `rejected`; the records and their git
history keep the rest. A missing, failed, or conflicting destination keeps the
row active. Leave future implementation work with its owning artifact.

## Source Lineage

Carry each row's original source identity in `source_refs`: the exact turn,
path, URL, ID, or revision it came from, not a later summary of it. When a
later reference, summary, or projection disagrees with that source, re-read the
original; it stands unless an explicit ruling supersedes it, recorded in
`relationships`. A source, destination, or receipt this session cannot read is
`unknown`: report it with the scope attempted, and keep the row's historical
`route_state` and settled decisions. A missing receipt does not show an
artifact is unreadable, and unproved implementation does not undo capture
routing. Quarantine only a derived claim that new evidence contradicts or its
cited source lacks: keep that claim `blocked` with the claim and searched scope
in `blocker`, and reopen only rows or routes proven to depend on it. A `done`
row changes only when new evidence invalidates its own transition. History is
append-only: add the new source span and its delta; earlier rows and summaries
stay as written. Keep exact IDs, URLs, paths, error text, failed checks, source
revisions, and unresolved needs verbatim.

## Structured Data Projection

For YAML/JSON, gauge byte size and structure before loading content into agent
context. Use code mode, Bash, or Python with an available parser to inspect
top-level keys, collection counts, and the requested paths. Read a small record
directly when it fits the current question; for a large record, emit a bounded
projection with source path, selected keys/row IDs, and omitted scope. Keep
unknown fields intact when patching; use the owner writer or a layout-preserving
editor rather than rewriting the whole document from a partial projection.

Treat a large log, tool output, or transcript the same way: keep the full
observation at a retrievable location and carry its exact pointer (path with
line range, key path, or digest) beside the bounded projection. Report an empty,
malformed, truncated, or missing source as that state; none of them shows the
content does not exist.

This is a development stopgap using available tools, not a new public CLI.
Human-facing prose belongs in Markdown; YAML holds machine declarations and
established structured payloads, and JSON holds runtime state. Follow existing
contracts until their migration is authorized.

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

Lifecycle lane: Shape -> Plan
Entity movement: `memory -> captured | proposed | blocked`
Workstream: resolve the owning workstream before writing records
Upstream: conversation, `/dump`, `/work`
Downstream: `/prior-art`, `/interview`, `/lev-plan`, `/propose`, `/exec`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Canon Write Gate

If the user asks "what would you edit", "show me", "audit", "plan", "pass2",
"recommend", or "how would you", do not mutate canon files. Render the ledger
and proposed changes only. Write artifacts only when the user explicitly asks
to apply, edit, patch, emit, or record it.

## Source / wiki intake capture

When capturing source material into a wiki, hybrid brain, or company knowledge base:

- Preserve raw source/provenance first, then analyze or summarize. Keep generated synthesis separate from immutable source receipts.
- Classify the destination by workspace/company and record type before writing durable pages.
- Do not turn facets such as strategy, ops, decisions, meetings, GTM, sales, or clients into top-level folders by default. Treat them first as page types, tags/facets, structured records, report sections, review-queue items, or source receipts.
- Only create durable folder structure when the repo-local router or user explicitly defines that surface.
- Draft conversation is not wiki truth until the user accepts the artifact or explicitly says to add it to the wiki/brain.

## Protocol

```yaml
steps:
  - id: inventory
    action: Inventory ideas, decisions, follow-ups, artifacts, blockers, promises, and proof/QA risks.
    validation: "Every item has a topic and provisional lifecycle state."
    on_failure: "If the thread is too large, bucket by topic and continue."

  - id: classify
    action: Compile user/source prose into agent-operational intent, state, and route, keeping the source's modal force; a relationship the source leaves unestablished stays `unknown`, not same, different, or impossible.
    validation: "Each item has compiled_intent, route_state, and next_route."
    on_failure: "Unknown state stays in memory and becomes the first output bucket."

  - id: prior_art_probe
    action: For every material row, run `lev find` (see Patch, Route, and Clear), probe existing work, and decide update, supersession, duplicate, or conflict before writing canon.
    validation: "An existing home and reconciliation basis are recorded, or the searched scope and missing prior art are explicit; conflicts are resolved or blocked."
    on_failure: "Route to /prior-art before proposing new artifacts."

  - id: seed_qa_contract
    action: For non-trivial items, create a QA seed before route advancement.
    validation: "Runtime, agentic, promotion, cleanup, fallback, or boundary-risk items name proof_required, highest_risk_claim, scenario_classes, and owner-local placement."
    on_failure: "Keep the item captured and route to /interview or /propose before /exec."

  - id: write_artifacts
    action: Write each writable row into its own record (Where Rows Go), updating the record that already holds it.
    validation: "No writable item remains only in conversation memory; each destination is read back before the capture row leaves the active queue."
    on_failure: "List only the unwritten items under In Memory with blocker."

  - id: score_fidelity
    action: Score each new or materially changed captured row against its source before advancement. Reuse an accepted score and source mapping when neither the source nor compiled intent changed.
    validation: "Every material row has fidelity_components, fidelity_note, and fidelity >= 0.8; no material constraint, non-goal, decision boundary, relationship, or acceptance condition is silently lost, and no row states a claim more strongly than its source."
    on_failure: "Re-capture at higher zoom or route to /interview."

  - id: reconcile_capture_ledger
    action: Update the changed rows of the ledger in the reply and drop the rows whose record was read back. Write no ledger file; the records and their git history keep the history.
    validation: "Every changed row has the full ledger fields; reconciled rows identify their checked destination; unresolved rows remain active."
    on_failure: "Do not advance routes. Show unresolved ledger rows under In Memory or Blocked."

  - id: show_delta
    action: Always show the source-fidelity table plus the compact lifecycle delta. The table is the operator proof that conversation intent reached disk; it is not optional response detail.
    validation: "The user can see every material intent row, destination, fidelity score, loss/narrowing note, route state, and next owner without opening the durable artifact."
    on_failure: "Rewrite output as <capture-results> with the fidelity table present."
```

## Routes

Select routes using the active domain overlay. These are next-owner suggestions,
not permission to execute. Show only applicable rows as a numbered table when a
choice is needed; otherwise name the single next route using `skill://<name>`.

| Item | Route |
|---|---|
| Constraint, invariant, gate, policy | `skill://lev-plan` for broad changes; `skill://propose` for a bounded SDLC change |
| Brief or design framing | `skill://interview`; preserve the resulting design before choosing the next owner |
| Broad, multi-slice, migration, architecture, or roadmap work | `skill://lev-plan`; preserve the whole effort before task slicing |
| Runtime, agentic, promotion, cleanup, fallback, or boundary-risk item | `skill://interview` or SDLC `skill://propose` with `qa_seed` |
| Coding slice ready for contract review | `skill://propose` |
| Authorized execution with sufficient scope, claims, and checks | `skill://exec`; non-coding may use a sufficient plan without `propose` |
| Provenance or duplicate check needed | `skill://prior-art` |
| Ambiguous intent or boundary | `skill://interview` |
| Workstream identity missing | `skill://ws` |
| Different domain or no matching owner | `skill://lev` |

## Deep Mode

`/capture --deep` and `/dump` add a convergence loop:

```yaml
deep_capture:
  repeat_until: "all writable items have stored fidelity >= in-memory fidelity and every material source row has a visible destination"
  loop:
    - inventory by topic
    - prior-art per material row
    - write or update durable route
    - read back destination and score fidelity
    - clear reconciled rows from the active queue while retaining history
    - enrich weak captures
  circuit_breaker: "3 iterations without fidelity improvement"
```

## Fidelity Gate

```
fidelity = 0.30*detail_preservation
         + 0.25*relationship_preservation
         + 0.20*source_attribution
         + 0.15*neighbor_context
         + 0.10*actionability
```

`fidelity >= 0.8` clears the capture preservation floor; `plan_required` still
controls the next route. Broad work advances to `/lev-plan`, not directly to
proposal or execution. Lower scores stay in capture, prior-art, or interview.

Fidelity is a weak-link gate, not permission to average away a missing material
constraint. A row with a silent loss in scope, non-goals, decision boundaries,
acceptance, relationships, or authority stays captured even if its weighted
number is above 0.8.

## Source Fidelity Table

Render this table in every non-trivial capture response. One row may summarize
several sentences only when they share one destination and lifecycle route.

| Field | Meaning |
|---|---|
| `intent_id` | Stable identity carried into plans, proposals, and tasks |
| `source_refs` | Conversation turn, file, URL, or prior durable artifact supporting the row |
| `source_intent` | Concise statement of the user's goal, constraint, non-goal, decision, or acceptance requirement |
| `destination_ref` | Exact durable destination, or `memory` with a blocker |
| `preservation` | `preserved`, `narrowed-approved`, `deferred-explicit`, `conflict`, or `lost` |
| `fidelity_components` | Detail, relationships, attribution, neighbor context, and actionability scores |
| `fidelity` | Weighted score from the formula above |
| `fidelity_note` | What changed, narrowed, remains absent, or needs human confirmation |

No row marked `lost` advances. `narrowed-approved` requires an explicit user or
source decision; agent simplification alone is not approval.

## Lifecycle Ledger Contract

The lifecycle ledger is the core visibility primitive at lifecycle trigger
points. `/capture`, `/capture --deep`, and `/dump` all build the same ledger
before claiming route advancement. The ledger lives in the reply, never in a
file: each row's durable home is its own record. The default human response
renders its delta; `--full`, audit, and debug may render the complete table.

| Field | Meaning |
|---|---|
| `intent_id` | Stable row id for this lifecycle turn |
| `topic` | Short label for the source material |
| `source_refs` | Conversation/file/artifact anchors used to re-derive the row |
| `source_intent` | Concise source-faithful goal, constraint, non-goal, decision, acceptance, or relationship |
| `compiled_intent` | Agent-operational interpretation, not raw user prose |
| `relationships` | Dependencies, conflicts, supersession, grouping, and ordering that must survive routing |
| `current_location` | `disk`, `memory`, `both`, `external`, or `unknown` |
| `artifact_ref` | Path or durable id; `none` if only in memory |
| `destination_ref` | Next durable design, plan, proposal, task, or existing authority |
| `route_state` | `in_memory`, `captured`, `planned`, `proposed`, `execution_ready`, `blocked`, `done`, or `rejected` |
| `fidelity` | Preservation score plus reason if below 0.8 |
| `fidelity_components` | Five component scores used to derive fidelity |
| `fidelity_note` | Explicit preservation, narrowing, conflict, deferment, or loss note |
| `plan_required` | True for broad/multi-slice/migration/architecture/roadmap work |
| `next_route` | `/interview`, `/prior-art`, `/lev-plan`, `/propose`, `/exec`, `/close`, or `none` |
| `blocker` | `null` or the reason this row cannot advance |

No route can advance if a row has `current_location: memory` without a blocker
or planned destination. This prevents hidden in-chat state from being mistaken
for durable work.

## Analysis Extension Captures

When the user asks to capture and extend an analysis thread, do not leave the improvement only in chat or only in an ignored/raw workshop artifact. Create a readable analysis companion, cross-link it from the nearest roadmap/analysis docs, and write each conceptual unit to its own record (Where Rows Go) with compiled intent, route state, QA seed, blockers, and next route. If the user requested a numbered structure such as "10 must / 10 must-not", verify section presence and counts before closing.

See `references/analysis-extension-capture-pattern.md` for the detailed pattern and verification checklist.

## Repository rename inventory captures

When asked to assess or record a repository rename, build a durable YAML ledger *before* changing names. Inventory structural identifiers separately from active prose, historical evidence, external identity, Office/binary artifacts, and ignored/runtime material. A raw hit count is discovery evidence, not a list of approved substitutions.

If the requested target spelling conflicts with an existing repository canonical name or partially completed migration, make the spelling decision a blocking, explicit ledger gate. Do not make a second structural rename, rewrite source evidence, or globally replace external URLs/IDs until the operator confirms the target.

Validate the YAML and inspect the Git delta; until the gate is resolved, the ledger should be the only repository mutation. See [references/repository-rename-ledger.md](references/repository-rename-ledger.md) for the schema, bucket definitions, and verification steps.

## Secret-backed runtime handoffs

When an operational handoff involves credentials injected into an agent/container environment, capture **four separate contracts**: host secret-variable names, the consumer tool's expected names/format, a child-process-only activation mapping, and the durable encrypted-cache/keyring location used by later scheduled runs. Never capture values or raw environment files.

Verification must distinguish:

1. non-empty host-variable names (without printing values),
2. successful activation/import under the intended user and `HOME`,
3. non-secret cache/workspace discovery, and
4. a later bounded operational proof plus its heartbeat.

A successful activation alone is not evidence that a future export or cron run works. If host and consumer variable names differ, document the scoped aliasing explicitly; do not create persistent aliases in repo files, profiles, or cron arguments. Keep unrelated credential namespaces separate in the capture.

See [references/secret-backed-runtime-handoff.md](references/secret-backed-runtime-handoff.md) for the reusable protocol and a Slackdump-specific example.

## Where Rows Go

Each row goes to the record of its type, where that type lives in the project.
In Lev:

| Row | Record |
|---|---|
| Idea | `.lev/pm/ideas/` |
| Plan, or broad and multi-slice work | `.lev/pm/plans/` |
| Design | `.lev/pm/designs/` |
| Ruling | `.lev/pm/decisions/`, with the user's words and the date; a ruling that changes an earlier one is a new decision with `supersedes`, and the old one gets `superseded_by` in the same commit |
| "Do later" or "add it to the MVP" | one item in `.lev/pm/roadmap/backlog.yaml` |
| Task | `lev entity task create` |
| Known fault | one debt row (`lev find "<the symptom>" --type debt_row --json` first) |

Run `lev find` for each row first and update the record that holds it. In a
project without Lev, use the project's own record homes and `rg` for prior art.
Write no file that lists the conversation's items (a capture, sweep or ledger
file), under any folder name: that ledger lives in the reply. The one file
called a ledger that you do write is a rename inventory (Repository rename
inventory captures): it lists repository names, not what was said. A row that
needs proof carries its QA seed in its destination plan or task:

```yaml
qa_seed:
  proof_required: true | false
  proof_gate_state: needs_proof_design | needs_proof_gates | needs_runtime_qa | needs_quality_review | needs_close_verdict | proof_blocked | none
  highest_risk_claim: "<claim or null>"
  scenario_classes: []
  owner_local_test_placement: "<module path or null>"
  shared_testing_boundary: "core/testing is a library/evaluator source, not the home for module-specific tests"
```

## Output

Render the Markdown inside this template; do not print the XML wrapper tags.

<capture-results>
## /capture results

### Source Fidelity

| ID | Source intent | Durable destination | Preservation | Detail | Relations | Attribution | Context | Action | Fidelity | Gap / decision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| {intent_id} | {source_intent} | {destination_ref} | {preservation} | {detail} | {relationships} | {attribution} | {context} | {actionability} | {fidelity_pct} | {fidelity_note} |

### Lifecycle Delta

Saved: {count_and_artifact_refs_or_none}
Still in memory: {count_and_topics_or_none}
Blocked or decision needed: {count_and_highest_leverage_decision_or_none}
Ready next: {count_and_route_or_none}
Next: {one_primary_action}
</capture-results>

## Red Flags

- "I'll show the list first and save after approval."
- "This follow-up is obvious enough to leave in chat."
- "Done items should be listed again."
- "Prior art can wait until proposal."
- "The table is optional because I wrote the artifact."
- "The fidelity score is enough; the user does not need to see the row mapping."
- "I can route broad work directly to propose; the task slices will preserve the roadmap."
- "A routed item can stay only in chat memory."
- "I will keep the rows in a capture file until they are routed."
- "Copying user prose is the same as compiling intent."
- "What would you edit means patch it now."

## Related

- `/work` routes lifecycle lanes.
- `/dump` is a focused alias for `/capture --deep`.
- `/brief` turns conversation context into a lifecycle artifact via `/interview --auto`.
- `/prior-art` finds existing homes.
- `/lev-plan` compiles captured/design intent into a fidelity-checked human runbook and slice DAG.
- `/propose` turns captured/aligned items into task DNA.
- `/exec` runs shovel-ready items.
