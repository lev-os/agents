# Agent Instructions

Thin operating contract for work reached through `/Users/jean-patricksmith/ops`
and the symlinked agent-skill workspace. Derived from CASS-scoped conversation
patterns and local Lev/Kingly prior art on 2026-07-06.

## First Moves

- Verify the real path, git root, active branch, and symlink target before
  claiming status or editing files.
- Stay read-only for dry runs, audits, current-state questions, and prior-art
  sweeps until the user explicitly switches to implementation.
- Separate source truth from projections: raw inputs, captures, context graph
  config, reports, dashboards, Obsidian pages, and AutoWiki output are different
  layers.
- Prefer small guardrail packets and task-shaped skills over long background
  briefs.

## Ops Workspace Layout

`/Users/jean-patricksmith/ops` is an operator workspace, not a normal git repo.
It uses root-level symlinks as the working map. Expand paths in answers and
artifacts; do not leave `~` or relative symlink guesses as the only source
reference.

Primary links:

- `/Users/jean-patricksmith/ops/naac` ->
  `/Users/jean-patricksmith/digital/kingly/apps/production/drone`
- `/Users/jean-patricksmith/ops/lev` ->
  `/Users/jean-patricksmith/digital/leviathan`
- `/Users/jean-patricksmith/ops/kingly` ->
  `/Users/jean-patricksmith/digital/kingly`
- `/Users/jean-patricksmith/ops/kingly-os` ->
  `/Users/jean-patricksmith/digital/kingly/kingly-internal-os`

`/Users/jean-patricksmith/digital` is where the code projects live. Treat
`/Users/jean-patricksmith/digital/kingly/apps`, `clients`, and related product
folders as code/workspace roots, not as generic documents.

Wiki link:

- `/Users/jean-patricksmith/ops/wiki` ->
  `/Users/jean-patricksmith/ops/.lev/plugins/autowiki`

The local ops wiki instance lives at
`/Users/jean-patricksmith/ops/.lev/plugins/autowiki`. Its main sections are
`raw/`, `wiki/`, `schema/`, and `sources.yaml`. Do not add separate root
symlinks for those sections.

Lev's source implementation is
`/Users/jean-patricksmith/digital/leviathan/plugins/autowiki`. No active
`/Users/jean-patricksmith/digital/leviathan/plugins/wiki` directory was
verified.

## Operator Profile

JP works across Lev/Leviathan, Drone/NAAC, Kingly Internal OS, Argo, Ulta,
ops/reporting, finance workflows, and local agent tooling. He likes work that
turns scattered context into durable systems: FlowMind, evals, proof gates,
agent runtime design, code quality guardrails, aviation simulation, source-backed
second-brain/AutoWiki/Obsidian workflows, GTM/business operations, and reusable
skills.

Answer with the ruling first, then evidence. Use exact paths, commands, failure
classes, denominators, and owner boundaries. Do not blur local vs remote,
planned vs implemented, source vs generated output, or report-only vs execution.

## Architecture Rules

- Name components from stable system responsibilities, not chat phrasing or
  temporary project state.
- Translate intent into the smallest coherent software pattern that fits the
  system: CLI wrapper, adapter, projection, validation gate, skill, flow node, or
  report.
- Do not create abstractions for one-off work. If the change can be 50 lines,
  do not make it 200.
- Keep FlowMind as a promotion/control surface for proven behavior. Do not turn
  unproven skill prose into executable flows without contract proof and one real
  run.

## Source Discovery

- Use CASS for conversation evidence and expand promising hits before treating
  them as proof.
- Search local durable surfaces before inventing a new artifact: `.lev/pm/`,
  `docs/`, `reports/`, `brain/`, `workshop/analysis/`, and context graph files.
- For code discovery, prefer codebase-memory graph tools when available; use
  text search for docs, configs, literals, scripts, and non-code files.
- Treat stale indexed sessions, missing files, and generated projections as weak
  evidence until current files or commands confirm them.

## Skill Repository Rules

Skills in this repository should be narrowly focused on concrete workflows such
as authentication setup, schema design, Convex functions, migration planning, or
validation. Reference material belongs in a skill only when it directly helps
complete the task.

- No emojis in markdown files or code comments.
- Use `Yes/No` in tables instead of checkmarks or emoji.
- Keep examples concise and focused.
- Use `// Bad:` and `// Good:` comments in code examples.
- Follow existing file patterns in `skills/`.

## Skill Maintenance

- If skills are added, removed, renamed, or substantially repositioned, update
  the root `README.md`.
- Keep the root `README.md` skill list in sync with `skills/`.
- Validate skills in a realistic temp project or sandbox before calling them
  good.
- Feed validation lessons back into the skill as steps, gotchas, or checks.

## Validation

For implementation work, define passing evidence before editing. For reports,
preserve failed commands with exit code and useful stderr. For Drone/NAAC,
separate local baseline, gateway, Thor/final-boss, and generated evidence
surfaces. For Lev/Kingly second-brain work, keep originals immutable and treat
AutoWiki, Obsidian, Notion, dashboards, and daily briefs as projections unless a
specific source-of-truth decision says otherwise.
