---
name: lev-core-boundaries
description: Use when creating a new core/* package, adding a file/dir under core/*, moving code between core/* packages, naming a *Receipt/*Ref/*Verdict/*Result/*Envelope/*Graph/*Run*/*Effect*/*Eval*/*Proof* type, or adding any child_process/spawn/exec/tmux call. The once-and-for-all "where does X go?" authority for core/* placement.
skill_type: gate
category: architecture
output_template: hud
canonical_dna: dna/architecture/core-boundaries/concept.yaml
---

# /lev-core-boundaries — core/* Placement Gate

> **Iron Law:** ONE concern, ONE owning package, ONE word ONE meaning.
> If a name could mean two things, the boundary is wrong — split it, do not place it.
> If a placement forces an outward import edge, the placement is wrong — invert it with a port.

This skill decides **where code lives in `core/*`**. It does not implement. It returns a
package + the gate that chose it, or it **BLOCKS** with the reason. The machine-readable
boundary ontology (tiers, import allowlist, disambiguators) is
`dna/architecture/core-boundaries/concept.yaml` — this skill is its human/agent gate surface.

## WHEN THIS FIRES (any one is a trigger)
- Creating a new `core/*` package OR a new file/dir under an existing `core/*` package.
- Moving code between `core/*` packages.
- Adding a type whose name ends in `Receipt | Ref | Verdict | Result | Envelope | Graph | Run* | Effect* | Eval* | Proof*`.
- Adding ANY `child_process | spawn | spawnSync | exec | execSync | execFile | tmux` call.

## THE TEN LOCKED INVARIANTS (user-locked — do NOT relitigate)
1. `effect != orchestration`. Separate packages.
2. `core/effect` = the consolidation target for ALL effect semantics (declare/admit/observe/evaluate/seal). It must NOT absorb eval/proof.
3. `core/eval` = STRICTLY flowmind validation / proofs / evals / scorers / gate-proofs. It must NOT absorb effect sealing.
4. `run-fabric` is DEAD as a public name. Run ledger = `core/runs` (append-only SOURCE record). Observability = a PROJECTION in `core/telemetry`, NEVER the owner.
5. `core/orchestration` = dispatch + scheduling ONLY. It must NOT own receipts, effects, eval/proof, run ledger, or graph theory.
6. `core/context-graph` (renamed from `core/graph`) = the context/knowledge graph. Do NOT fold it into orchestration.
7. Pure graph algorithms = `core/graph-algorithms`, consumed by orchestration, owned by neither orchestration nor the context graph.
8. `event-*` = transport/choreography. Family-related to effect/eval (shared runner + EvidenceRef vocabulary) but NOT merged.
9. `core/exec` = the ONLY blessed effectful path + entry point. "No ledger without exec" means exec is the WRITER, not the owner of `core/runs`.
10. The last step of every run is SEAL, not always eval. The ledger RECORDS seals; it does not DECIDE truth.

> **NET-NEW PACKAGES ARE CREATED FROM SCRATCH.** `core/effect`, `core/eval`, `core/runs`,
> and `core/graph-algorithms` do **not** exist today — not even as empty dirs. There is no
> scaffold to fill; each is `mkdir` + `package.json` + populate. `core/graph` is RENAMED to
> `core/context-graph`.

---

## GATE 0 — STOP. Run the decision tree. Do not place by folder name or file proximity.
Walk gates **A→M in order. FIRST MATCH WINS.** Each gate is a yes/no predicate over file/import
facts. After a match, you MUST pass **GATE 1 (cycle guard)** before placing.

```
GATE A — cursed-exec predicate: does the code call child_process/spawn*/exec*/execFile/tmux?
  A1  is it the blessed dispatch/transport itself (createExec, transport bin|grpc|http, surface adapter, gate-run read)?  → core/exec
  A2  is it a low-level substrate primitive (tmux session, PTY, daemon supervision, provider process)?                   → core/harness | core/tmux-harness | core/daemon(-*)
  A3  ANY other spawn/shell?                                                                                             → BLOCK (cursed shadow-exec). Route through core/exec. No third option.

GATE B — pure-contract predicate: zero I/O AND zero behavior body AND no node:* import AND no mutable module singleton AND imported by ≥2 bounded contexts?
  → core/domain
  BLOCK if: it has a validate()/evaluate()/compute() body · needs fs/child_process/node:* · holds a `let _x` singleton · is imported by exactly ONE context (→ that context owns it).

GATE C — graph-math predicate: a function that TAKES an opaque {nodes,edges} and returns a graph result (toposort/cycle/critical-path/waves/SCC/causal-sort), with zero knowledge of what a node MEANS?
  → core/graph-algorithms
  BLOCK if it imports any domain/entity/task/schedule type (then it is not pure math).

GATE D — effect predicate: does it declare an EffectEnvelope, admit/gate one, observe an ObservedEffect, run a substrate evaluator, or seal an EffectReceipt (the describe→perform→seal lifecycle)?
  → core/effect
  BLOCK if it also scores cases or discharges a proof obligation (split that half to core/eval via a port).

GATE E — eval/proof predicate: does it produce a graded SCORE over cases ("how good?": grader/scorer/judge/benchmark/scorecard) OR discharge a binary OBLIGATION with a re-verifiable attestation ("did it hold?": ProofSpec/verifier/gate-proof/witness/proof-bundle/intent-conservation/Pentagon/ConstraintManifold axioms)?
  → core/eval
  BLOCK if you are tempted to merge Score and Verdict into one Result type. (See VERDICT RULE below.)

GATE F — ledger predicate: is it an append-only source record of a run/action/attempt/seal, the RunEnvelope aggregate, the run store/service, run admission/idempotency/lifecycle, run-outcome classification, or the run lifecycle event factories?
  → core/runs
  BLOCK placing in core/exec (writer ≠ owner; cycle), core/storage (substrate ≠ ledger), or core/telemetry (read-side ≠ source).

GATE G — projection predicate: is it a rebuildable read-model derived from the ledger (dashboard/status/freshness/query-replay/trace-view/effect-receipt replay/incident/alert)?
  → core/telemetry
  BLOCK if it holds authoritative state or cannot be rebuilt by replaying core/runs.

GATE H — control-plane predicate: does it DECIDE what-runs-next (DAG/loop/wave/critical-path-as-control-flow/queue/worker-or-agent SELECTION/retry POLICY/compensation/team A2A dispatch)?
  → core/orchestration   (the MATH → GATE C; the WORK it triggers → core/exec; the SEAL → core/runs)
  BLOCK if it owns a receipt/effect/proof/ledger type, or reimplements a graph algorithm.

GATE I — meaning predicate: does it model entities/triples/overlays/graph-patch/lineage/provenance/context-projection?
  → core/context-graph   (MAY call core/graph-algorithms; must not fork it)
  BLOCK if it is a workflow run-plan (→ GATE H — different edges, different cadence).

GATE J — eventing predicate: pub/sub bus, event schema/provider, trigger→flow dispatch, or an XState lifecycle machine?
  → core/event-bus | core/event-providers | core/event-dispatch | core/event-machines   (ONE canonical matchPattern, in event-bus)

GATE K — authoring predicate: FlowMind YAML IR parse, compile-to-target, graph-executor, intent-compiler, tiered T1-T3, transpiler, WorkflowGraph visualization?
  → core/flowmind (shell-only: NO inline exec; routing DECISION → GATE H; execution → core/exec; effect lifecycle → GATE D; gate-evaluator → GATE E)

GATE L — substrate predicate: execution-binding resolution, tmux session/warm-worker, process/PTY, daemon supervision, or a daemon-* surface protocol adapter?
  → core/harness | core/tmux-harness | core/daemon | core/daemon-{grpc,http,mcp,websocket,pentagon}

GATE M — leaf/foundation predicate: a generic pure helper (isRecord/stableStringify/pathAllowed/token-math/case-bridge)?  → core/utils (NEVER duplicate)
  else a foundational/delivery context (config/logger/uri/storage/poly/sdk/ui/validator/workstream/lifecycle/memory/onboarding/testing/build/index) → its existing bounded context.

DEFAULT (no gate matched): X is a MISSING bounded context. Name its ubiquitous language by
industry meaning, give it ports in core/domain + adapters outward, verify GATE 1, then ADD it
to this tree and to the dna. NEVER dump it in core/domain or core/orchestration.
```

## GATE 1 — CYCLE GUARD (applies to EVERY placement; this is the BLOCK predicate)
The new import edge MUST point **inward** along the stability arrow (source of truth =
`dna/architecture/core-boundaries/concept.yaml#tier_import_allowlist`):

```
surfaces → {exec, orchestration} → {effect, eval, runs} → telemetry(read) → {context-graph} → {graph-algorithms} → domain → {utils, uri}
substrate {harness, tmux-harness, daemon, daemon-*} = a driven-adapter ring imported BY exec
```

- **VERIFIED FACT (corrected):** `exec → harness → {orchestration, flowmind, telemetry}`; `orchestration` does **NOT** import `exec`. The run-ledger service is pure persistence — `run-service.ts` imports `node:crypto` + `@lev-os/domain/run-fabric`; its companion `jsonl-run-store.ts` adds `@lev-os/config` xdg + `node:path/fs`. Both carry zero orchestration logic and move to `core/runs` together. Therefore the ledger lives in `core/runs` at the inner tier (read by exec/orchestration/telemetry and by projection adapters), **not** in `core/exec`. `core/event-bus` receives projected run/action events but must not import the run ledger.
- **LEDGER-WRITE RULE (invariant 9):** ONLY `core/exec` writes to `core/runs`. `core/effect` and `core/eval` emit **domain-typed** receipts/refs and **never import `core/runs`** — the `RunLedgerWriter` port lives in `core/domain`, `core/runs` implements it, `core/exec` invokes it. So `core/effect`/`core/eval` allowlist = `[core/domain]` only.
- **PREDICATE:** if placing X here forces package P to import a package that is *not* in P's allowlist, the placement is **WRONG**. Invert it with a port interface in the inner package and an adapter in the outer one.

## BLOCK — what "BLOCK" means (the consequence is real, not advisory)
1. **Refuse the placement.** Do not create the file/package at the proposed location.
2. **State the gate + the violated invariant/edge.** e.g. "GATE F BLOCK: ledger in core/exec violates the cycle guard (orchestration→exec upward edge)."
3. **Offer the inversion.** Name the inner package + the port that resolves it.
4. **CI enforcement.** An import-boundary lint rule **generated from** `core-boundaries#tier_import_allowlist` (dependency-cruiser `forbidden` rule, or eslint `no-restricted-imports` per-package allowlist, or Nx module boundaries) fails the build on any outward edge. The dna allowlist is the single source; the lint config is derived, never hand-maintained.

## VERDICT RULE (resolves the merge tension)
- Merge ONLY the **verdict discriminator base** — one `EvalVerdict` union for the binary axis (`pass | fail | conditional | deferred`). Collapse the 8 scattered verdict shapes onto it.
- KEEP **two distinct typed output families**: `Score` (gradient/aggregate — "how good") and `Verdict + Attestation` (binary/load-bearing — "did it hold"). They share the runner substrate (core/exec) and the discriminator base only.
- "Never one merged Result/Verdict" means: **never collapse `Score` INTO `Verdict`** (or invent a universal `Result`). A shared discriminator is not a universal result type.

## RATIONALIZATION TABLE (excuse → ruling)
| Excuse | Ruling |
|---|---|
| "It's a receipt, put it with the other receipts" | NO. `EffectReceipt`→core/effect; `RunSeal`→core/runs; `ProofBundle`→core/eval; `QueueAck`→core/event-bus. 'Receipt' is overloaded; split by meaning. |
| "Effect and eval can share a package, both are verification" | NO. Locked #2/#3. Effect seals effects; eval discharges obligations. Shared runner (exec) + shared vocab (domain) only. |
| "The ledger needs exec, so put it in exec" | NO. Exec is the WRITER (locked #9), not the owner. `core/runs` is inner-tier; exec imports it. In-exec = cycle (verified topology). |
| "Observability is where the run records are" | NO. Locked #4. `core/runs` = write-side truth; `core/telemetry` = read-side projection. Never co-located, never inverted. |
| "Orchestration already has the toposort" | NO. Locked #7. Pure math → `core/graph-algorithms`. Orchestration consumes it. Volatile must not own stable. |
| "It's a graph thing, put it in core/graph" | NO. 'graph' = compute(`graph-algorithms`) / mean(`context-graph`) / schedule(`orchestration`). Pick by the question it answers. |
| "One merged Result/Verdict is simpler" | NO. See VERDICT RULE. Score (gradient) ≠ Verdict (binary). Merging is the overloading we are deleting. |
| "I'll copy isRecord locally, it's tiny" | NO. `core/utils` owns it. **46 duplicate copies** is the disease, not the cure. |
| "I'll add it to domain, everything imports domain" | NO. domain = types + ports ONLY. Behavior/I/O/singletons → the owning context. One-context types are mis-homed in domain. |
| "I'll just spawn here, it's quick" | NO. GATE A3. Cursed shadow-exec. Route through `core/exec` or it does not merge. |
| "flowmind owns the effect lifecycle / gate-evaluator" | NO. Lifecycle is substrate-agnostic → `core/effect`. Gate-evaluator is eval → `core/eval`. flowmind = authoring only. |
| "core/effect already exists, I'll add to it" | NO. It does NOT exist yet (create-from-scratch). Stand it up per the migration slices, don't assume a scaffold. |

## WORD DISAMBIGUATORS (one word → never one type)
- **receipt** → `EffectReceipt`(core/effect) · `RunSeal`(core/runs) · `ProofBundle` ref(core/eval) · `QueueAck`(core/event-bus)
- **verdict** → `EffectVerdict`(core/effect) · `Score` vs `Verdict+Attestation`(core/eval) · `RunOutcomeStatus`(core/runs)
- **graph** → compute(`graph-algorithms`) · mean(`context-graph`) · schedule(`orchestration`)
- **log / ledger / trace** → source-of-truth(`core/runs`) · projection(`core/telemetry`) · signal(`core/telemetry`+`core/logger`)
- **evidence** → reference pointer `EvidenceRef`(core/domain shape, core/runs records) · knowledge claim `ClaimEvidence`(core/context-graph)

## GREEN LIGHT — all five must hold before placing X
1. Walked gates A→M top-down; first match recorded with the gate id.
2. GATE 1 cycle guard passes (the new edge is in the target package's allowlist).
3. No word in X's name means two things across contexts (checked the disambiguators).
4. If X needs another engine's behavior, it crosses a PORT, not an inline import.
5. X did NOT land in domain-with-behavior or orchestration-as-dumping-ground.

## OUTPUT CONTRACT
Return: `placement: core/<pkg>` · `chosen_by: GATE <X>` · `cycle_guard: pass` · (on BLOCK) `block_reason` + `inversion`. Keep it to those lines; do not restate the tree.

## RELATED
- Machine-readable ontology + tier allowlist: `dna/architecture/core-boundaries/concept.yaml`
- Migration sequence (9 slices) + worst-tangle inventory: `.lev/pm/workstreams/core-module-audit/state/workstream.yaml#session_6_boundary_cartography`
- Supersedes the package-count guidance in the `eval-framework-1-0` boundary handoff (its facts preserved).
