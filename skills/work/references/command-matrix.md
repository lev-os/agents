# UMD Command Matrix (Single Source)

This is the canonical mapping for command primitives across:

- CLI surface (`core/cli/bin/lev`)
- Lifecycle router (`~/.agents/skills/work/SKILL.md`)
- Schema router (`context/schemas/stream-router.yaml`)

Use this file as the source of truth when updating aliases, routing, or stage ownership.

## Primitive Matrix

| Primitive | Primary Aliases | CLI Entry | SDK Surface | Work Stage | Schema/Router Handler | Notes |
|---|---|---|---|---|---|---|
| `get` | `find`, `search`, `lookup`, `read`, `ls`, `scan`, `research`, `prior art` | `lev get "<query>"`, `lev gather "<query>"`, legacy `lev find` | `lev.get(query, { depth })` | `captured` | `query -> lev-get/memory` | Progressive depth: `context -> fs -> bd -> research` |
| `work` | `plan`, `spec`, `propose`, `implement`, `execute` | `lev work [auto|find|gather|review] ...` / `lev go ...` | `lev.work(...)` | stage-classified (`ephemeral`..`completed`) | lifecycle path in `work` FSM | `work auto` defaults toward gather/get for context-first routing |
| `ask` | `wiz`, `wizard`, `guide me`, `unstuck` | alias via CLI to wizard path (`ask`, `wiz`) | `lev.ask(...)` | `crystallizing` (intake) | interview path in `work` DISCOVER | Auto-trigger when guard underspec is high |
| `check` | `align`, `scan`, `security`, `validate` | alias via CLI to validate path (`check`) | `lev.check(...)` | `classified` / `validate` | validation gates in `work`; schema escalation paths | Includes drift/alignment/security checks |
| `go` | `run`, `do it`, `ship` | alias `go -> work` | `lev.go(...)` | `manifesting` | `task -> bd/ralph` when explicit task intent | Starts execution path; respects FSM gates |
| `handoff` | `checkpoint`, `resume context`, `session compact`, `exit` | routed through `work` manifesting output | `lev.handoff(...)` (conceptual) | `manifesting -> completed` | handoff/checkpoint artifacts | Must emit checkpoint contract + confidence score |
| `learn` | `reflect`, `retro` | `work` LEARN ceremony | `lev.learn(...)` | `completed (post-close)` | post-execution learning capture | Records outcomes into memory artifacts |
| `workflow` | `workflow run`, `workflow list`, `workflow create` | `workflow` skill route | N/A | not lifecycle ownership | explicit workflow-management route | Distinct from `work` lifecycle FSM |

## CLI Alias Constellation (Authoritative)

From `core/cli/bin/lev` built-in aliases:

- `get -> gather`
- `lookup -> get`
- `research -> get`
- `scan -> get`
- `go -> work`
- `ask -> wizard`
- `wiz -> wizard`
- `check -> validate`
- `f -> find` (legacy)
- `g -> gather`
- `w -> workflow`

## Discoverability Map (CLI Surface)

- `lev get "<query>"`: progressive context gather via `gather` pipeline (find + optional research).

- `lev find "<query>"`: legacy direct hybrid search path (RRF fusion backends).

- `lev search "<query>"`: semantic index search surface (index backend).

- `lev workflow ...`: legacy workflow command, superseded by `lev exec` and `lev work`.


## Ownership Rules

- `lev` owns CLI syntax, alias resolution, and primitive dispatch.
- `work` owns lifecycle-stage detection and artifact contracts.
- `workflow` owns workflow CRUD/run operations, not lifecycle.

## Change Protocol

When changing command semantics:

1. Update CLI aliases/routes in `core/cli/bin/lev`.
2. Update lifecycle ownership/routing in `~/.agents/skills/work/SKILL.md`.
3. Update schema handlers in `context/schemas/stream-router.yaml`.
4. Update this matrix.
5. Run validations:
   - `node tooling/scripts/check-cli-surface.js`
   - YAML parse for touched schemas.
