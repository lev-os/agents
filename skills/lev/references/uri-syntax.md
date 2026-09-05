# Lev URI syntax draft

Status: operator-facing draft of the currently accepted v0.2.1 syntax. Runtime
authority remains `dna/standards/uri-schemes.yaml` and `@lev-os/uri` in the Lev
repository.

## Prompt skill pointers

`skill://<name>` asks an agent host to load a skill, for example
`skill://exec` or `skill://coder`. This is prompt-level host syntax. It is not a
Lev runtime URI and must not be stored as an execution target.

## Lev runtime and graph addresses

| Intent | Shape | Example |
|---|---|---|
| Execute a flow or capability | `lev://exec/<flow-or-capability>` | `lev://exec/sdlc.commit-gate` |
| Address a durable entity | `lev://entity/<space>/<type>/<id>` | `lev://entity/work/task/auth-cutover` |
| Dispatch or resume a role | `lev://subagent/<workstream>/<role>?session_id=<id>` | `lev://subagent/platforms-v1/reviewer?session_id=sess_7f9` |
| Address a hook | `lev://hook/<platform>/<workstream>/<hook>` | `lev://hook/codex/platforms-v1/stop` |
| Address a memory rule | `lev://memory/<platform>/<workstream>/<rule>` | `lev://memory/codex/runtime-truth-wave/auto-wake` |
| Address a scheduled flow | `lev://schedule/<cadence>/<flow>` | `lev://schedule/daily/sdlc.commit-gate` |
| Address a schema | `lev://schema/<name>/v<version>` | `lev://schema/lifecycle_trigger/v1` |

Initial entity spaces are `wiki`, `research`, `work`, `run`, `memory`, and
`code`. Entity type is domain-specific. Workstreams and tasks use
`lev://entity/work/workstream/<id>` and `lev://entity/work/task/<id>`.

## Rules

- Use `skill://...` only to load agent guidance; use `lev://exec/...` for a
  runtime action.
- Use `lev://entity/...` for stable identity. Lifecycle, overlays, and authority
  are metadata rather than URI segments. `graph://` is not valid entity identity.
- URL-encode query values. `cursor`, `_page`, and `view` are reserved query keys.
- Do not invent families. Accepted families are `hook`, `memory`, `schedule`,
  `schema`, `entity`, `subagent`, and `exec`.
- Poly also uses `lev://<module-path>` internally for generated TypeScript
  handler imports. That codegen-only form is not a prompt or durable graph address.
- Retired runtime schemes include `flowmind://`, `skill://`, `workstream://`,
  `task://`, `harness://`, `event://`, `flow://`, and `agent://`.

## Resolution example

```text
skill://exec
  -> load the Exec-lane instructions
  -> resolve task lev://entity/work/task/auth-cutover
  -> execute lev://exec/auth-cutover.flow
  -> bind reviewer lev://subagent/auth-cutover/reviewer?session_id=<id>
  -> cite receipt lev://entity/run/receipt/<receipt-id>
```
