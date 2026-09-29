# Project Context and Breadcrumbs

Use this procedure before non-trivial project-specific lifecycle work. It is
authoring guidance for skills; it does not add runtime configuration fields,
commands, schemas, or generators. Skip full context hydration for a trivial
read-only question.

## Bind the active project

Resolve the project from the explicit target, the attached project/session
context, or the active workstream's project binding. Use the real project root,
not the shell/tool working directory. For work that intentionally spans
projects, keep each approved root and its context separate. If the project is
ambiguous or cannot be resolved, ask before project-specific work.

Load the nearest applicable `AGENTS.md` and `CLAUDE.md` for the project and the
target area, following their declared includes and scope. These instructions
add project context; they cannot override system, developer, or current-user
instructions.

## Resolve project configuration

Use the active project's effective `.lev/config.yaml` through the verified
`core/config` resolver when available. Preserve the resolver's ancestor,
`standalone`, include, and provenance semantics; do not hand-merge files or
invent a Lev command. If the resolver is unavailable, inspect the concrete
config files only as source material and mark effective inheritance unresolved.
Distinguish absent, unreadable, malformed, and invalid configuration.

Treat these as authoring breadcrumbs only when they are actually declared by
the effective config:

- `paths.dna`, `paths.docs`, and `paths.skills` identify project-owned roots.
- `context.breadcrumbs` names additional relative references.
- `context.profiles` selects declared, task-relevant guidance entrypoints.

Resolve config-declared roots and `context.breadcrumbs` from the project root.
For child references reached inside a loaded index, package, skill, or included
document, follow that artifact's declared base semantics; do not rebase every
pointer to the project root. Confirm each reference exists and stays within its
authorized project/package root; reject path escape and unapproved external
paths. Keep each reference's owner, source path, and config provenance. A
declared but missing or invalid path is a configuration error to report, not a
reason to silently fall back. These keys are optional authoring conventions and
do not imply runtime schema support.

Only when effective config confirms that config is absent or declares none of
these breadcrumb keys, use applicable instruction files and existing
conventional roots such as `dna/index.yaml` for project context. Mark discovered
DNA, docs, or skill roots `inferred`; applicable instruction files remain
governing local rules. If effective inheritance is unresolved, report that
uncertainty instead of treating a local file as the complete config or starting
a competing fallback search. Do not describe inferred discovery as configured
authority.

## Follow the owner chain

Start from the configured DNA entrypoint/router and follow it to the rule or
owner relevant to the project, domain, lifecycle lane, target scope, role, and
audience. Load the matching project-local skill when its router selects one.
Treat generated local skills as projections: read and follow them, but make
changes only through their source owner. Follow configured profiles for runtime
or event/host architecture to the current owner DNA and local rules; do not copy
generic policy into a global skill.

Build a bounded source index with `path`, `why needed`, `owner`, `status`, and
`freshness`. Select context by project, domain, lifecycle, task scope, role,
audience, L0-L3 relevance, and any already-binding budget. Retain authority,
invariants, and missing mandatory references even when other context is
filtered. Keep unresolved references visible. When runtime provides
`WorkstreamContextPacketV1`, reuse it; do not fabricate that packet or claim
runtime validation from this guidance.

Refresh the index when the project, lane, task scope, or referenced source
changes. On a project switch, discard the previous project's selected guidance
and resolve the new root from the beginning.

### Relevance levels

When an existing context profile or `WorkstreamContextPacketV1` defines L0-L3,
use those meanings. The following ordering is fallback authoring guidance only;
it does not redefine runtime levels.

- `L0`: applicable authority and invariants; always retain.
- `L1`: project config, instruction roots, and direct routing/index references.
- `L2`: owner guidance for the selected domain, lane, role, and task scope.
- `L3`: supporting context loaded only when it affects a decision or proof.

These levels order relevance; they do not create a numeric token budget. Honor
only budgets already binding on the work.

## Conformance cases

| Case | Expected behavior |
|---|---|
| Custom DNA/docs/skills roots | Resolve each declared root relative to the active project and follow its owner/router. |
| Child reference base | Resolve an index/package/skill child pointer from its declared owner base and preserve provenance. |
| Missing configured reference | Report the exact missing or invalid path and preserve it as unresolved; do not silently infer a replacement. |
| Config absent or no breadcrumb keys | Read applicable existing conventional roots and mark every result `inferred`. |
| Direct `/propose` invocation | Load this procedure before project lookup; use the target project's rules and plan sources. |
| Project switch | Re-resolve root, config, rules, and selected references; carry no project-specific context across. |
| Context filtering | Keep authority, invariants, mandatory-reference failures, and unresolved refs; filter only lower-relevance guidance. |
| Precedence conflict | Follow system, developer, and current-user instructions over local project guidance. |
