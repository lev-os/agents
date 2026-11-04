# SDLC adapter convergence planning pattern

Use this when the user asks to plan a Lev SDLC/task/workstream migration while core is still settling, especially when there are competing persistence substrates such as the current `.lev/pm` files and Beads (`bd`).

## Durable pattern

1. **Keep core still** — explicitly state that the plan does not require immediate core schema churn. Treat it as a stabilization/convergence plan until core contracts are settled.
2. **Inventory sibling workstreams first** — before creating the new plan, find and link nearby convergence/runtime/lifecycle/eval/task-ontology workstreams so the new work is not an orphan.
3. **Create both a workstream and a plan** — use a canonical workstream under `.lev/pm/workstreams/<slug>/state/workstream.yaml` and a plan under `.lev/pm/plans/plan-<slug>-<date>.md`. The workstream carries ongoing state; the plan carries executable sequencing and acceptance criteria.
4. **If Beads is requested, create a Beads epic/task as a tracker, not the sole source yet** — initialize/configure `bd` if needed, create an issue/epic, and link the Beads ID from the plan/workstream. Do not discard file-based PM until the adapter cutover is explicit.
5. **Make adapter ownership explicit** — write the target shape as a storage-neutral SDLC API with at least:
   - `file` adapter: preserves today’s `.lev/pm` behavior and remains default/compat path.
   - `bd` adapter: uses Beads for graph persistence when configured.
6. **Name plugin ownership boundaries** — for Lev, `plugins/sdlc` owns Task and Workstream entities plus lifecycle/dependency semantics. Skills should call the SDLC API/SDK/CLI/MCP rather than writing storage-specific files directly.
7. **Plan skill migration as a compatibility layer** — `propose`, `capture`, `work`, `handoff`, `close`, and related lifecycle skills should gain CLI and MCP call paths. Keep current file behavior working through the file adapter until cutover.
8. **Add anti-parasitism/prior-art anchors** — link existing docs/decisions that say operations guidance should be owned by the platform/API rather than copied into every skill.
9. **Verify artifacts exist** — after creating files and Beads records, read/validate the plan/workstream paths and show the Beads record by ID.

## Acceptance criteria checklist

- New workstream exists and names related sibling workstreams.
- New plan exists and links the workstream and Beads ID if used.
- Plan states “core settles first” / no immediate core churn.
- Plan defines file and Beads adapters behind configuration.
- Plan states SDLC owns Task/Workstream; skills call API/SDK/CLI/MCP.
- Current file-based `.lev/pm` flow remains supported until explicit cutover.
- Verification includes real file existence and `bd show <id>` or equivalent when Beads is in scope.
