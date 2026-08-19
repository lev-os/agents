---
name: eval-builder
description: Use when designing or improving Lev eval packs, inline FlowMind evaluation policy, owner-local runtime scenarios, assurance sizing, adversarial field probes, or promotion gates.
---

# Eval Builder

First output: classify the gate and expose the smallest executable slice. Do
not lead with a harness plan unless the user specifically asked to build or
promote an evaluator or harness.

Current authority is `core/eval`, `docs/specs/spec-eval.md`, and
`dna/core/eval.dna.yaml`. `core/testing`, `lev pentagon`, and
`core/daemon-pentagon` are migration inputs, not target authority.

## Current operating mode

Treat this global skill as the hand-authored evaluator UX. Do not assume the
plugin `eval-design.flow.yaml` is operational enforcement: its promotion path
currently declares commandless `lev.validate` nodes that warn/yolo-pass. Do
not invoke or project that graph as proof until its deterministic validators
are executable, fail closed, and terminate in a real `core/eval` decision.

Perform the default analysis in one model turn. Do not launch one LLM call per
conceptual stage. Escalate to independent attacks, repeated stochastic samples,
or evaluator repair generations only when the evaluator itself is the explicit
deliverable and consequence justifies the cost.

## Non-negotiable readiness rule

Use exactly these classes:

| Class | Meaning | May stop implementation? |
|---|---|---|
| `code_blocker` | A required executable, API, schema, or owner contract is unavailable for the next edit | Yes |
| `decision_blocker` | A product, architecture, or authority choice changes the implementation | Yes |
| `promotion_gate` | Evidence required for cutover, merge, release, or certification | No |
| `administrative_hold` | Queue, assignment, or workstream state | No |

A missing test or harness is work in the current or a later slice, not a
blocker. A missing receipt triggers a live dependency check; the receipt is
never the dependency. Every approved plan must expose at least one executable
slice. If none exists, simplify the dependency graph until one does.

Forbidden:

- harness required before implementing its own subject
- harness-of-harness or meta-eval recursion for owner-local deterministic work
- generated-evaluator fitness blocking Claim schemas, handlers, or known packs
- live-provider qualification blocking deterministic implementation
- agent-authored receipts or proof files

## Authority split

- Deterministic code validates schemas, runs commands, computes measurements,
  applies thresholds, emits `EvalDecision`, and controls promotion.
- FlowMind/DNA/YAML declares pack refs, inline evaluator definitions,
  requiredness, budgets, retry policy, and promotion policy.
- LLMs produce work, typed observations, candidate evaluators, attacks, and
  semantic review. They never score, certify, seal, or finalize themselves.

Pack refs and inline FlowMind definitions normally combine. Compile both once
into immutable execution requirements. Deduplicate identical evaluator id plus
digest; required wins for identical definitions; any conflicting definition
fails compilation.

## Expectation And Critical-Path Check

Where relevant, establish the product outcome, owning code areas, applicable
rules/index refs, real-world critical path, observable done state, and field
environment before designing cases. Identify code areas first, then load only
their entries from the nearest project rules index.

Start with the successful field path from trigger to external effect,
observation, `Measurement`, `EvalDecision`, and settlement. Derive failure cases
from each boundary on that path. Do not begin with a generic edge-case list.

## Progressive assurance

Stop at the first level that proves the current claim:

1. Reuse an existing owner-local test or deterministic evaluator.
2. Add one focused owner-local test or command case.
3. Add an integration or surface scenario when the boundary is the risk.
4. Add an ad hoc task-local harness for a novel operational claim.
5. Promote a reusable evaluator pack only when the need is recurring.
6. Add hostile holdouts, generated-evaluator fitness, or live-provider
   qualification only for high-risk promotion.

Do not make every feature pay levels 4-6 before level 1 can run.

## Evaluator-development branch

Use this branch only when designing, promoting, or repairing the evaluator is
itself the requested outcome. Keep ordinary implementation on the progressive
assurance path above.

First emit one assurance spine. Separate generated, compiled,
adapter-delivered, provider-visible, worker-obeyed, Claim-admitted, evaluated,
settled, finalized, and replayed states whenever they apply. For each state
name:

| Field | Requirement |
|---|---|
| input and output | Exact typed contract and digest-bearing reference. |
| owner | Code/module that can author or decide the state. |
| capture boundary | Where evidence bytes are observed and retained. |
| deterministic check | Executable predicate or command; prose is advice only. |
| falsifier | Counterexample that would look green at the wrong boundary. |
| failure route | Repair evaluator, hold promotion, or fail execution. |

Attack cross-boundary false greens: compiler success is not adapter delivery;
adapter rendering is not provider visibility; tool declaration is not worker
tool access; a log is not matching bytes; transcript success is not Claim
admission; evaluation is not settlement; cached state is not replay.

Use a human checkpoint when ambiguity changes the target, the acceptable error
direction, protected holdout policy, or consequence. Do not spend an automated
multi-generation loop discovering a product decision the operator can answer
directly.

## Candidate integrity and calibration

Freeze the exact evaluator candidate before calibration. Give every repair a
new digest and evaluator generation. Preserve known-good and known-bad
subjects, raw samples, seeds, commands, prompt/model/profile refs, typed
observations, capabilities, cleanup results, and evidence digests.

Keep product repair and evaluator repair in different attempts. An agent may
propose both, but the same attempt must not modify both and then certify the
result. Protect holdout answers from the authoring worker and compare both
failure directions; a lucky sample is not calibration.

Only call a candidate `admission_ready` when a real, current-generation
evaluator-fitness `EvalDecision` and its evidence refs exist. Otherwise return
the candidate with a promotion gate or typed hold. Never manufacture receipts,
measurements, decision refs, or an admission chain in prose.

## Assurance demand and field qualification

Size promotion evidence from machine-readable obligations, not a requested test
count. Normalize and digest-deduplicate acceptance criteria, proof or claim
obligations, and constraints inside the existing `Task Eval Instance`.

Keep per-item planning and assurance metadata distinct:

- `complexity` and `effort` size implementation work and execution budget.
  They do not create proof by making the test count larger.
- `confidence` normalizes to uncertainty `0..2`; missing confidence is `2`.
- the affected boundary or fix area selects applicable boundary failure modes.
- DNA idiom and rule refs contribute mandatory failure modes, not a scalar
  "rule density" score.

The deterministic assurance compiler builds the unique set of
`(obligation_digest, failure_mode_id)` pairs. One base mode plus `0..2`
uncertainty modes may be derived for each obligation; matching DNA rules add
their mandatory modes. Then calculate:

~~~text
pairs_required = count(unique obligation_digest x failure_mode_id)
target = clamp(ceil(pairs_required * profile.multiplier),
               profile.floor, profile.cap)
~~~

The profile is named, versioned policy. Profile `field` is multiplier `1.0`,
floor `10`, cap `20`; an owner pack may strengthen it. LLMs may propose cases
but cannot set the target, delete mandatory modes, or certify coverage. Every
case maps to at least one required pair, duplicate pair sets do not count, and
every high-risk obligation needs a falsifier.

For a real provider or operational claim, promotion requires the actual
FlowMind -> Exec -> Eval path. Unit fixtures and direct provider smoke tests
support earlier levels but cannot certify the field claim. Split field cases:

1. blocked-lane cases run the real pipeline and prove rejection before the
   external effect;
2. admitted-lane cases perform the real effect only with an explicitly safe
   payload, isolated workspace, clean environment, and recorded admission.

At promotion, an unresolved provider privacy or retention claim selects the
high-risk field-qualification branch before baseline reuse, even when
owner-local tests pass or the live provider is unavailable. It must remain
visible in the `EvalDecision` and cap qualification scope. When that uncertainty
does not change the implementation contract, classify it as a promotion gate,
not a `decision_blocker`. A public synthetic workload may prove provider
functionality; it cannot prove the provider safe for private workloads.

## DNA rule projection

Resolve owner and project DNA at compile time through the existing catalog.
Emit one provenance- and digest-pinned rule packet, then project it through an
existing FlowMind overlay at named lifecycle gates. Do not restore runtime DNA
compilation or mutable-latest rule loading.

A DNA rule with a deterministic predicate becomes a verification checkpoint.
A rule without one becomes prompt advice. Eval verifies the packet digest and
requires a result for every gate rule; prose alone never blocks or certifies.

## Project resolution

Resolve the root from explicit `--project`/`--root-path`, then nearest `.lev`,
then the Lev repository only for Lev core work. Inspect only the refs needed for
the current claim:

```yaml
canon:
  - docs/specs/spec-eval.md
  - dna/core/eval.dna.yaml
  - core/eval/src/index.ts
  - plugins/sdlc/flows/eval-harness.flow.yaml
project:
  - .lev/config.yaml
  - .lev/config/*.yaml
  - .lev/flows/*.flow.yaml
  - .lev/pm/workstreams/*/state/workstream.yaml
  - .lev/pm/tasks/*/dna.yaml
owner_local:
  - core/*/tests/**
  - core/*/evals/**
  - plugins/*/tests/**
  - plugins/*/evals/**
  - community/examples/*/evals/**
```

Reuse existing tests, scorers, and fixtures. Module-specific harnesses stay
with their module or example; shared `core/eval` owns contracts and evaluation,
not every product runner.

## Workflow

```yaml
steps:
  - id: classify
    action: Classify every alleged blocker before designing proof.
    instruction: |
      Name the next code change. Check live whether its executable, API,
      schema, and owner contract exist. Put every remaining item into
      code_blocker, decision_blocker, promotion_gate, or administrative_hold.
    validation: "At least one executable slice is named, or one concrete code/decision blocker has a falsifier command."
    on_failure: "Collapse proof and receipt dependencies; do not return a globally blocked plan."

  - id: frame
    action: Name the operational claim and consequence.
    instruction: |
      State the user-visible behavior, the false-green that matters, and
      whether this run is implementation, cutover, or promotion. Trace the
      successful real-world path from trigger through effect and final verdict.
    validation: "One behavior, one false-green, one lifecycle phase, and the load-bearing critical path are explicit."
    on_failure: "Ask one compact question only when the missing choice changes the implementation."

  - id: reuse
    action: Find the cheapest existing proof surface.
    instruction: |
      Inspect owner-local tests and existing eval packs first. Prefer one
      focused deterministic check over a new harness.
    validation: "An existing check is selected or its absence is recorded as current-slice work."
    on_failure: "Do not invent a framework; add the smallest owner-local check."

  - id: size
    action: Compile assurance demand from distinct obligations.
    instruction: |
      Deduplicate acceptance, proof, and constraint obligations by digest.
      Derive uncertainty modes, resolve mandatory DNA failure modes, select a
      named profile, and compute the unique pair target deterministically.
    validation: "Target, input digest, profile, and obligation-to-mode matrix can be independently recomputed."
    on_failure: "Use conservative uncertainty and unresolved-rule defaults; never lower demand because metadata is missing."

  - id: design
    action: Design only the assurance level the claim needs.
    instruction: |
      For implementation, put the focused test beside the code. For a novel
      operational claim, specify a task-local harness. For recurring policy,
      define a pack. Combine pack and inline FlowMind policy at compile time.
      Derive each negative case from a named critical-path boundary.
    validation: "The selected level is the first progressive-assurance level that proves the claim."
    on_failure: "Delete unnecessary harness, holdout, meta-eval, and provider layers."

  - id: attack
    action: Attack promotion claims without blocking unrelated code.
    instruction: |
      For cutover or promotion, cover the compiled obligation-mode matrix with
      the smallest credible malformed, stale, concurrent, misleading-success,
      and reward-hack cases. Keep holdout answers outside the worker surface.
      Real provider claims require both blocked and safely admitted field lanes.
      LLM judges emit typed observations; deterministic code emits the verdict.
    validation: "The unique pair target is met, every high-risk claim has a falsifier, and every result reaches EvalDecision."
    on_failure: "Mark promotion blocked while leaving implementation ready."

  - id: emit
    action: Return an executable slice and separate promotion gates.
    instruction: |
      Exact commands must exist in the repo. Receipts are listed only as
      expected runtime outputs, never as inputs the agent must manufacture.
    validation: "Output has one runnable next command and no circular proof dependency."
    on_failure: "Simplify again; never emit a plan with no runnable first move."
```

Render the Markdown inside this template; do not print the XML wrapper tags.

<eval-plan>
## Eval: {target}

Gate: {implementation|cutover|promotion}; blockers {code_or_decision_or_none}
Outcome: {operator_visible_effect}
Critical path: {trigger -> effect -> observation -> Measurement -> EvalDecision -> settlement}
Code and rules: {owner_paths}; {rules_index_refs}
Field proof: {one_real_world_run_or_not_applicable}
Derived failures: {boundary -> falsifier summaries}
Typed evidence: {observations_and_artifact_refs}; target {pairs_required}/{target}
Promotion gate: {none_or_minimum_remaining_gate}
Next executable slice: {owner, behavior, command}
</eval-plan>

## Rationalization checks

| Excuse | Correction |
|---|---|
| "The harness is missing, so code is blocked." | Building the harness is work; start the owner-local slice. |
| "No receipt exists." | Check the live API/code dependency; receipts come after execution. |
| "The evaluator needs an evaluator." | Deterministic fixtures validate the first evaluator; no infinite regress. |
| "We need all hostile cases first." | Only promotion needs full hostile coverage. |
| "A live provider is unavailable." | Deterministic completion can still be verified; live qualification stays blocked. |
| "The judge said pass." | Judge output is observation; `core/eval` owns the verdict. |

## Done check

The plan is invalid if implementation is marked blocked solely because a test,
harness, receipt, meta-eval, holdout, or live-provider run has not happened yet.
A promotion claim about a real provider or operational boundary is invalid
until the computed field target has run through FlowMind, Exec, and Eval; an
unavailable live provider leaves promotion blocked, not implementation.
