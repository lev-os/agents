# Conflict handling

A Git conflict is not by itself a reason to pause. The sync request authorizes
semantic resolution when the intended combined result is clear. Inspect the
base, both sides, current contracts and relevant decisions. Preserve each side's
intended behavior, not merely every line.

## Inspect

- `git status --short`
- `git diff --name-only --diff-filter=U`
- `git ls-files -u -- <conflicted-paths>`
- `git diff --cc -- <conflicted-paths>`
- `git show :1:<path>`, `git show :2:<path>` and `git show :3:<path>` as needed
- For submodules, inspect commit ancestry and the relevant changes in the submodule.

## Resolve and continue when clear

Examples include independent additions, references and handoffs that can be
combined without changing their meaning, and a renamed caller that must follow
an already accepted API change. Deduplicate lists when order and duplicates
carry no meaning. Regenerate derived files through their owner after resolving
their source. A newer timestamp alone does not choose the correct behavior.

For submodules, ancestry can establish whether a candidate contains both sides;
also inspect its changes and existing branch policy. Do not choose a pointer
only because it is newer.

Make the smallest coherent resolution. Check for lost fields/references and
conflict markers, parse structured records, run `git diff --check`, and run the
affected behavioral checks for code. Preserve authority and receipt provenance;
combining histories does not certify a different task's result.

Stage only the resolved paths with `git add -- <resolved-paths>`, conclude the
merge with a truthful commit message, and continue the requested Git sync.
Keep the original mode and scope. No extra permission is needed for this clear,
validated resolution. A later distinct repair does not exhaust an arbitrary
shared retry count. Use bounded waits for Git and its hooks.

## Pause on a genuine conflict

Pause when the sources do not establish which incompatible behavior or intent
must win: competing product decisions, irreconcilable data semantics, an unclear
deletion, ownership or permission change, or divergent submodule histories with
no justified integration. A failing hook remains enforced; do not delete its
rule or bypass it to finish the merge.

Give a concise Markdown brief, then ask about the specific missing decision:

| Field | Content |
| --- | --- |
| State | Local checkpoint, pending merge and pushed/local-only state |
| Conflicted paths | Exact files or submodule pointers |
| Local intent | What the local side preserves |
| Incoming intent | What the incoming side preserves |
| Unresolved choice | Why source evidence cannot settle it |
| Options and risk | Concrete outcomes, affected behavior and potential loss |
| Recommendation | The best-supported option and its reason |
| Validation and resume | Checks and commands needed after the decision |

With `--handoff`, include this blocker in the copyable chat handoff as well.

