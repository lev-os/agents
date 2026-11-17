# Slices

How `lev-plan` cuts work into vertical slices, for `build_topology`,
`map_slices`, and a slice review. A plan's stage and a map's slice are one
thing: a slice. The steps are in [`../SKILL.md`](../SKILL.md).

## What a slice is

A vertical slice is a narrow behavior path that cuts through every layer it
needs and is demoable or verifiable on its own. A slice is never only schema,
only API, only UI, only docs, or only tests. Use tracer bullets for
independently demonstrable end-to-end behavior. One slice is right only when
the work is already a single behavior path.

Each slice names: outcome, owner, dependencies, covered intent IDs, allowed
effects, the artifact it ends in, its proof, its stop condition, status, and
open decisions. The artifact states its premises and conclusion locally. No
slice starts before its input claims are satisfied. A slice that needs a
person (a review, a judgment, outside access, a manual check) says so in its
proof; the others an agent can run with no further decision. When you cannot
cut vertical slices, return to `/interview` with the exact missing design
decision.

The plan and the packet share problem/behavior, domain vocabulary, decisions,
constraints, acceptance examples, test seams, delivery slices, dependencies,
evidence and authority. The plan projects the broad runbook; a map or packet
projects a selected slice for review or execution. Preserve source IDs and
decisions across both. Reuse existing public test seams; prefactoring needs a
concrete scoped reason, with its own scope and check.

Detail ready near work and keep later dependencies and uncertainties visible
([Lev's rolling-horizon procedure](../../lev/references/recursive.md)). Later
slices stay in the map until their inputs and decisions support an executable
packet.

## The slice table

The plan's Slices section holds one row for each slice:

| Slice | Outcome | Artifact | Claims (proof) | Rules out | Known-bad input | Waits on | Run budget |
|---|---|---|---|---|---|---|---|
| {stable-domain-name} | {observable result} | {path; format {version, frozen} when a long run reads it} | {claim_id: program | agent | person} | {failure} | {fixture or n/a} | {none or slice} | {n worker runs, or n/a for a light plan} |

A long run reads only frozen formats. Version the format of each artifact it
reads and settle that version before the run starts; a later format change
makes the run's output stale, and the plan then names the rerun and its size.

## Wide mechanical changes

For wide mechanical changes that cannot land as independent vertical slices,
use expand–migrate–contract: expand alongside the old form, migrate bounded
caller batches while preserving compatibility, then contract only after every
migration dependency is satisfied and no old caller remains. If batches cannot
stay green independently, explicitly plan a shared integration boundary and
final integrate-and-verify gate; do not promise per-batch green. Branch
creation still requires the task's authority. A behavior-changing slice at a
shared seam must preserve the old caller contract immediately or remain
unexposed until compatibility proof passes; never put an incompatible baseline
before a blocked or unavailable expansion slice.

## Reviewing the breakdown

Present slice name, genuine blockers and delivered behavior when reviewing the
breakdown. Ask about granularity, merging or splitting, dependencies, and
missing behavior only when unresolved; prior approval need not be repeated. A
source parent remains unchanged unless that mutation is authorized. A map is
not task emission or tracker publication.

When a selected slice needs an SDLC spec projection, load and render the
canonical [`../../work/templates/spec.md`](../../work/templates/spec.md), which
this skill owns as a lane. Do not fork the template inline or invent another
spec format. A spec cites requirement rows by id; the rows stay in the task's
`dna.yaml`.

## Slice Map

```yaml
slices:
  - id: <stable-domain-name>
    operator_outcome: <observable result>
    owner: <package or plugin>
    depends_on: []
    covers_intent_ids: []
    proof: <verifier or proof profile>
    status: <ready|needs_review|blocked>
    open_decisions: []
```

The map may show every slice. It must not contain copied task packets, generic
proof boilerplate, or claims that all slices are execution-ready. A map does
not dispatch by itself, but every approved map must identify at least one
executable slice.

<slice-map>
## Slice Map: {proposal_id}

Source state: {current|stale|in_flux}
Source plan: {plan_ref_or_not_required}; fidelity {score}; coverage {covered}/{total}
Critical path: {slice_ids}
Slices: {compact_slice_records}
Promotion gates: {slice_ids_and_reason}
Administrative holds: {slice_ids_and_reason}
Next slice: {one_slice_id_or_design_decision}
</slice-map>
