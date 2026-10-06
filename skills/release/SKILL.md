---
name: release
description: Use when preparing a project release, updating release documentation with --docs, or reconciling implemented changes with project work records.
---

# Release

Produce the documentation changes, checks, and work-record updates for an actual
change set. Use the project's existing release tools and lifecycle writers.

`release --docs` is skill invocation syntax. It updates documentation and owned
Lev IR sources and performs scoped project hygiene. It does not claim a new Lev
CLI command or change the existing agent-assignment meaning of `work.release`.

## Load the owners

For every project-specific run, load
[project context](../lev/references/project-context.md). Resolve configured docs,
skills, Lev IR paths and relevant rules through the current project context.
Preserve current `dna/` filenames until the separately declared cutover.

For README and changelog prose, invoke `writing`; it loads its four required
references. For a changed FlowMind definition, invoke `flowmind-author`. For
entity completion, invoke `close` with that entity's actual acceptance contract.
Use `lev-plan` for plan lifecycle and the workstream CLI proxy for workstreams.
Repo-local generated skills are changed through their declared source and compiler.

## 1. Save the change scope

Identify the reader outcome, exact commit range or named working-tree files,
current revisions, source digests, allowed writes and project release tools.
Inspect tracked, staged and explicitly named untracked changes separately.
Keep unrelated work out of the scope. Use an explicit supplied range when a
release baseline is unavailable; an arbitrary last-N-commits window is not a baseline.

Check: every proposed edit has an inspected source and owner. Missing or
conflicting scope remains an explicit gap; do not invent a release history.

## 2. Update the owning documentation and Lev IR

Draft or update the affected README, changelog, specs and accepted/implemented
contracts. Preserve existing obligations and human edits. Explain proposals as
proposals. Update generated projections through their intent/flow source.
Use the normal scoped task execution path for document or metadata edits.

In Leviathan, use `.changeset/README.md` for project notes versus package notes.
Changesets owns package selection, version planning and changelog generation.
Other projects use their actual configured release mechanism.

Check: claims match current source; runnable examples succeed; touched YAML and
flows pass their existing validators; source/projection pairs remain consistent.

## 3. Map change notes to work records

For each changed entry, record:

| Change entry | Entity reference | Current source/digest | Acceptance evidence | Owner/action | Result |
| --- | --- | --- | --- | --- | --- |
| Exact note or changeset | Real task/plan/workstream ID, or unmatched | Inspected bytes | Current checks, decisions or successor refs | Verified owner transition, or hold | updated, no_change, or unresolved |

Resolve the effective lifecycle schema for each kind and project. A note proposes
a match; it does not establish completion. A draft README remains pending until
applied and verified. Completing one task does not complete a larger plan with
remaining work. Ambiguous, shared and partial scope keeps its current state.

Check: each completion has its own acceptance evidence and each archive retains
valid references. An unavailable writer holds that row, not unrelated docs work.

## 4. Run existing hygiene and reconcile

Reuse relevant current repo-audit results only when their source revision and
domain coverage match this run. Inspect docs and links explicitly: the existing
Leviathan audit scanner has no docs domain. Reuse lifecycle reconciliation,
accepted-design projection and metadata repair from the existing project hygiene
plan. The reviewed hygiene effect handles one status field; document edits use
normal scoped execution rather than widening that effect.

Apply supported transitions through the actual bound tracker or per-kind writer.
Archive only accepted completed scope through its declared storage route; preserve
successor, decision and evidence links. Never infer a generic close/archive command.
Canonical runtime acceptance remains with `core/eval`, not prose or model confidence.

Check: source digests and effective states still match before writes, intended
changes read back correctly, and a repeat on unchanged inputs adds no edits.

## 5. Finish with an inspectable result

Save the scope, source-to-owner links, document diffs, change-to-entity map,
commands, failures and readback as JSON in the resolved Lev XDG artifact route or
a fresh system-temp directory. Report what changed, what was completed/archived,
what stayed pending and the exact next owner. Keep private source instructions
out of published reports.

For `--docs`, finish after those scoped maintenance results. For a full release,
continue through the project's existing authorized version/build/publication
route and its checks; documentation success is not publication evidence.

## Recovery and limits

Retain scoped preimages before writes. After interruption, inspect actual bytes
and existing recovery evidence before retrying. Restore only owned preimages
whose current bytes have not received conflicting edits. The current narrow
reviewed hygiene path retains recovery evidence; it has no automatic rollback.

Keep runtime receipts with their owning runtime writer; this skill's JSON is a
report, not a fabricated receipt. Use one bounded worker and one integrated
review when warranted. Add no scheduler or new FlowMind for the first skill run.
