---
name: eval-builder
description: "lev eval, core/eval, design eval suites, runtime scenarios, acceptance criteria, adversarial probes, or proof gates for agentic features before implementation or promotion."
---

# Eval Builder (legacy Pentagon entrypoint)

First output is a harness plan. Do not start with unit tests or a raw proof
matrix. Pentagon work asks: “what proof would survive a hostile optimizer?”

Current eval canon is `core/eval`, `docs/specs/spec-eval.md`, and
`dna/core/eval.dna.yaml`. `core/testing`, `lev pentagon`, and
`core/daemon-pentagon` are legacy migration inputs, not target authority.

## Naming and migration frame

Use `eval` and `eval-builder` language in new plans, tasks, docs, APIs, and
operator output. Treat `Pentagon` as a historical compatibility name only.

This skill has three modes:

- Standalone eval building: generate adversarial/runtime eval scenarios for any
  topic or system from the supplied context.
- Lev-managed project eval building: resolve `.lev/config.yaml`,
  `.lev/config/*.yaml`, project flows, eval roots, DNA, and workstream/task
  state before proposing evals.
- Lev self-eval building: load Lev's own specs, DNA, skills, flows, example
  apps, and owner-local package boundaries before designing runtime evals.

Do not make receipt/proof files by hand. Receipts and proof artifacts are
byproducts of real effects, deterministic score/projection code, or runtime
execution. A plan, report, or reviewer note is input evidence, not a receipt.

## Operating frame

Pentagon is Lev’s agentic proof model: conventional tests plus repeatable harnesses, receipts, adversarial evals, and real operational usage. The harness is the tooling that sets up, executes, attacks, measures, tears down, and records evidence for a use case.

LFD is now part of the Pentagon design frame. Treat every future worker as a
competent, tireless optimizer that will satisfy the target by the cheapest path:
memorizing evals, hardcoding cases, mining feedback, editing scorers, routing
around receipts, or declaring victory on weak proof. The harness plan must make
genuine capability cheaper than cheating.

Pentagon is self-contained. Do not require a separate UltraQA skill or mode. The useful part to absorb is the hostile runtime scenario matrix: happy path plus malformed input, interruption, prompt injection, cancel/resume, stale state, dirty worktree, hung command, flaky/retry, and misleading success output. In Lev, those are Pentagon adversarial/eval inputs that must become typed evidence, not a separate workflow dependency.

`core/eval` is the target shared eval coordinator. Legacy `core/testing`
Pentagon helpers are migration inputs and compatibility utilities only. Shared
code must not become the home for daemon, tmux, app, provider, browser, or
example-specific proof runners/tests.

Module-owned harnesses live with the module or example that owns the behavior:
- Daemon manifest/gate/runner suites: `core/daemon` owner-local eval/test paths;
  legacy `@lev-os/daemon-pentagon` is migration source material.
- Tmux/FlowMind runtime suites: `core/tmux-harness` owner-local eval/test paths.
- Poly provider and Poly MCP suites: `core/poly`.
- App/example suites: `community/examples/<example>/evals`.
- Live external adapter references, such as browser MCP, stay with the adapter/example because they require daemon/extension setup.

For MCP promotion proof, raw curl, raw HTTP, or direct handler invocation is not sufficient. The agent_smoke path must load an agent-style MCP config, connect with a real MCP client/transport, list tools, select the Poly-bound tool by schema, call it, and write receipt/GateProof artifacts.

Use this skill to plan or harden eval harnesses. Prefer `lev eval` and
`core/eval` surfaces when they exist. Treat `lev pentagon
propose|init|run|gate|doctor`, `core/testing/skills/pentagon/SKILL.md`, and
`core/testing/flows/pentagon-sdk-poly-binding.flow.yaml` as legacy compatibility
surfaces to inspect, not new public canon.

## Evaluation authority model

LLM-as-judge and adversarial agents are evidence generators, not promotion authorities. FlowMind may ask an LLM to observe, rank, attack, or judge samples, but certification requires typed observations, deterministic scoring or comparison, policy transitions, and receipt/GateProof refs.

Use this split:
- Deterministic: static checks, schema validation, command exit codes, fixed-seed replay, statistical comparison, threshold math, artifact existence, typed gate-chain validation.
- Non-deterministic: claim extraction, reverse brainstorming, hostile scenario design, LLM-as-judge scoring, cross-model critique, semantic adequacy review.
- Hybrid: LLM produces typed observation payloads; a code companion or `lev.validate` scorer validates shape, computes pass/fail/hold, and records the branch.
- HITL: human review can certify ambiguous semantics only when it produces an explicit receipt or approval ref.

## LFD target design

Every Pentagon plan for non-trivial, runtime, agentic, promotion, cleanup,
fallback, or boundary-risk work must include a loss-function contract:

```yaml
lfd:
  target:
    metric: "<mechanically computed score or pass/fail verdict>"
    bar: "<holdout or promotion bar>"
    failure_directions: [precision, recall]
  constraints:
    budget: "<wall-clock / spend / token / provider ceilings>"
    surface: "<allowed files, APIs, providers, models, concurrency>"
    methodology: "<deterministic only, LLM observer allowed, HITL, etc.>"
    capacity_caps:
      keyword_list: "<N or N/A>"
      regex_set: "<N or N/A>"
      seed_data: "<N or N/A>"
      special_case_branches: "<N or N/A>"
  instruments:
    score: "<command or scorer binding>"
    lint: "<constraint and eval-leak command>"
    probe: "<perturbation / memorization gauge>"
    status: "<time, budget, spend, token, score-history command>"
    proof: "<receipt / trace / GateProof / ProofBundle verifier>"
  forced_entropy:
    stall_rule: "<what must change after flat metric>"
    exploration_quota: "<cadence for structurally different attempts>"
    log: "<hypothesis / expected failure / diagnostic before change>"
  visibility:
    dev: "<visible inputs, capped feedback>"
    holdout: "<aggregate-only, rate-limited, answers outside worker surface>"
```

If the target cannot be mechanically scored yet, the Pentagon output is a
design-blocked diagnostic, not an execution-ready harness.

## LFD preflight technique checklist

Apply these techniques before trusting the harness:

1. Observe before asking: load repo tests, evals, scorers, CI, logs, receipts,
   AGENTS/CLAUDE guidance, installed tools, reachable surfaces, and reference
   artifacts.
2. Ask one batched interrogation only for unresolved outcome, eval source/size,
   budget, allowed surface, and acceptance bar.
3. Split inner loop from outer loop: Stage 0 is spec/tests green; outer loop is
   loss descent on dev/holdout evidence.
4. Build or identify dev/holdout cases. Inputs may be visible; answers are not.
   Warn explicitly when the set is small/enumerable.
5. Design the metric to penalize both failure directions. Recall-only,
   precision-only, latency-only, or no-regression-only targets are weak.
6. Leak-audit every feedback channel: score output, lint output, miss lists,
   logs, reviewer notes, receipts, and status output.
7. Capacity-cap lookup-shaped artifacts: keyword lists, regex sets, seed data,
   branch tables, fixture mirrors, and special cases.
8. Enumerate at least 10 cheap paths for this target, each with a fence and a
   detection instrument.
9. Calibrate known-good and known-bad candidates. The scorer must separate them
   decisively before launch.
10. Trip lint deliberately. Constraint violations must return only
    `VOID: constraint violation`; detailed findings go outside the worker read
    surface.
11. Run probe/status. Probe gap measures memorization; status exposes elapsed
    time, spend, projected burn, and score history.
12. Red-team the draft three times. Patch the loss function until three
    consecutive lazy-optimizer simulations find no cheaper path than real work.
13. Patch mode: when a running loop cheats, fix the target/harness, append the
    cheat exhibit, revert eval-shaped artifacts, and resume from the last honest
    checkpoint.

## Project and FlowMind resolution

Resolve the project root in this order: explicit `--project` or `--root-path`, nearest ancestor with `.lev`, then `~/lev` only when the work is Lev core/runtime work. Do not assume the current shell is already in the right project.

FlowMind config should carry durable defaults. Project-local config supplies derived local values. Task overlays supply the specific target and promotion gate. Runtime `--knob`/`--with` values should only specialize the current run.

```text
FlowMind defaults
  < project-local .lev/config.yaml or .lev/config/*.yaml
  < task execution.yaml / suite manifest overlay
  < runtime --knob / --with
```

For Lev-managed project mode, load project prior art before broad search:
config roots, linked flow/eval globs, DNA, active workstream state, task DNA,
project skills, owner package boundaries, and example apps. Use the refs below
as the first-pass map; skip missing paths explicitly instead of inventing a new
scanner or framework.

For adversarial eval harnesses, prefer a project-local flow when it exists; otherwise use the Lev-provided default:

```bash
lev flowmind validate plugins/sdlc/flows/eval-harness.flow.yaml
lev exec "run Pentagon adversarial eval" \
  --root-path <project> \
  --flow <flow-path> \
  --knob task="<target use case and promotion gate>" \
  --knob strategy_kind=adversarial
```


## Pentagon FlowMind catalog

```yaml
flowminds:
  available:
    - id: eval-harness
      path: plugins/sdlc/flows/eval-harness.flow.yaml
      owner: plugins/sdlc
      entry_surfaces:
        - lev flowmind validate plugins/sdlc/flows/eval-harness.flow.yaml
        - lev exec --flow plugins/sdlc/flows/eval-harness.flow.yaml --knob task=... --knob strategy_kind=adversarial
      use_when: >
        Run produce -> judge -> compare -> keep/discard evaluation for
        metric-based, llm-as-judge, or adversarial evidence. Use it for
        Pentagon adversarial scenario matrices when the target needs hostile
        runtime proof, multi-sample judging, deterministic comparison, and
        receipt-backed fail-closed promotion gates.
    - id: legacy-pentagon-sdk-poly-binding
      path: core/testing/flows/pentagon-sdk-poly-binding.flow.yaml
      owner: core/testing
      wrapper: core/testing/skills/pentagon/SKILL.md
      registered_in:
        - core/testing/config.yaml
        - plugins/sdlc/config.yaml
      entry_surfaces:
        - lev pentagon propose|init|run|gate|doctor
        - lev sdlc pentagon
      use_when: >
        Legacy compatibility input for Poly-bound capability proof across CLI,
        MCP generated client, HTTP, gRPC, generated Rust/Go/Python SDK clients,
        and lev-exec provider provenance. Prefer eval-builder/core/eval wording
        and migrate reusable scoring/projection logic out of core/testing.
    - id: legacy-daemon-run-fabric-real-world-usage-v1
      path: core/daemon-pentagon
      owner: "@lev-os/daemon-pentagon"
      use_when: >
        Migration input for daemon-owned run fabric, implemented daemon
        surfaces, app manifests, and artifact-only daemon gates. New daemon
        eval/test code should be owner-local under core/daemon unless heavy
        optional dependencies justify an eval-prefixed package.
    - id: poly-mcp-real-capability
      path: core/poly/src/__tests__/pentagon
      owner: core/poly
      use_when: >
        Prove registry runner -> MCP tool schema -> MCP call over real MCP
        transport without mocking executeCapability.
    - id: coding-agent-mcp-load
      path: community/examples/architect-app/pentagon
      owner: community/examples/architect-app
      use_when: >
        Prove an actual coding-agent style harness loads MCP config, lists tools,
        calls the Poly-bound MCP tool, and emits Pentagon receipt/GateProof
        artifacts.
  planned:
    - id: pentagon-adversarial-claim-fitness
      proposed_path: plugins/sdlc/flows/pentagon-adversarial-claim-fitness.flow.yaml
      use_when: >
        Turn a source design into claim ledger, reverse brainstorm, false-green
        failure hypotheses, fitness functions, verifier adequacy, and trace
        requirements before /exec dispatch.
    - id: pentagon-tmux-flowmind-runtime
      proposed_path: core/tmux-harness/flows/pentagon-tmux-flowmind-runtime.flow.yaml
      use_when: >
        Prove tmux-backed FlowMind/SDK runtime behavior: attach, watch,
        intervene, resume, scrollback receipts, context budget handoff, and
        fail-closed reaper/session policy.
```

## Sources to inspect first

```yaml
required_refs:
  eval_canon:
    - docs/specs/spec-eval.md
    - dna/core/eval.dna.yaml
    - core/eval/package.json
    - core/eval/src/index.ts
    - core/eval/src/registry.ts
    - core/eval/src/command-cases.ts
    - core/eval/src/trace-cases.ts
    - core/eval/src/proof/index.ts
    - plugins/sdlc/flows/eval-harness.flow.yaml
  project_config:
    - .lev/config.yaml
    - .lev/config/*.yaml
    - .lev/config/eval.yaml
    - .lev/flows/*.flow.yaml
    - dna/plugin-contract.dna.yaml
    - dna/authoring/boundaries.yaml
    - dna/fractal.yaml
    - docs/specs/spec-config.md
    - docs/specs/spec-poly.md
    - core/config/src/config-loader.ts
    - core/context-graph/config.yaml
    - core/context-graph/src/handlers/graph-project-context.ts
  lev_self_eval:
    - AGENTS.md
    - dna/core/*.dna.yaml
    - dna/standards/*.yaml
    - dna/skills/*.yaml
    - .agents/skills/*/SKILL.md
    - .codex/skills/*/SKILL.md
    - .lev/flows/*.flow.yaml
    - .lev/pm/workstreams/*/state/workstream.yaml
    - .lev/pm/tasks/*/dna.yaml
    - .lev/pm/tasks/*/execution.yaml
  legacy_migration_inputs:
    - core/testing/package.json
    - core/testing/src/pentagon.ts
    - core/testing/src/proof.ts
    - core/testing/src/project-suite.ts
    - core/testing/src/suites.ts
    - core/testing/skills/pentagon/SKILL.md
    - core/testing/flows/pentagon-sdk-poly-binding.flow.yaml
    - core/daemon-pentagon/package.json
    - core/daemon-pentagon/src/index.ts
    - core/daemon-pentagon/src/run-fabric-gate.ts
    - plugins/sdlc/config.yaml
    - plugins/sdlc/src/handlers/sdlc.ts
  showcase_and_owner_evals:
    - community/examples/*/evals/**
    - community/examples/*/pentagon/**
    - plugins/*/evals/**
    - core/*/evals/**
    - core/*/tests/**
  gates:
    - .lev/validation-gates.yaml
    - dna/gates.yaml
    - dna/testing.yaml
    - dna/hygiene/hygiene.yaml
  adversarial:
    - plugins/sdlc/flows/adversarial-review.flow.yaml
    - workshop/pocs/graph-storage-adapters/pentagon/README.md
    - workshop/pocs/graph-storage-adapters/pentagon/classes/eval_harness.ts
  constraint_engineering:
    - docs/design/design-constraint-engineering-manifesto.md
    - .lev/pm/reports/20260506-naac-candidate-promotion-dogfood-postmortem.md
    - .lev/pm/handoffs/20260401-naac-harness-constraint-engineering-session-2.md
    - docs/design/design-flowmind-authoring-guide.md
    - docs/design/design-lore-argo.md
    - .lev/pm/reports/dream-journal.md
```

Validation: `test -f .lev/validation-gates.yaml && test -f dna/gates.yaml && test -f dna/testing.yaml && (test -f plugins/sdlc/flows/eval-harness.flow.yaml || test -f "$HOME/lev/plugins/sdlc/flows/eval-harness.flow.yaml")`

## Workflow

```yaml
steps:
  - id: frame_proof_target
    action: Name the operational use case and promotion risk
    instruction: |
      State the user story, daily usage path, promotion decision, and the claim that would cost money, trust, or safety if false.
      If the feature is agentic, assume the implementation was written by untrusted contractors and must be remediated to NASA-grade production quality.
    validation: "Harness plan names one concrete use case, one promotion gate, and one high-risk behavioral claim."
    on_failure: "Stop and interview; tests without a target claim become dashboard decoration."

  - id: observe_before_asking
    action: Inventory existing proof, eval, tool, and reference surfaces
    instruction: |
      Before asking the user anything, inspect repo tests, existing eval cases,
      scoring scripts, CI, receipts, traces, logs, task contracts, AGENTS/CLAUDE
      guidance, installed tools, and reference artifacts. Reuse existing scorers
      and cases before generating parallel ones.
    validation: "Plan names observed tests/evals/scorers/tools/surfaces or states their absence."
    on_failure: "Do not ask broad questions; first prove what the repo already knows."

  - id: interrogate_once
    action: Ask only the unresolved LFD design fields
    instruction: |
      Ask one batched round only for missing outcome, eval source/size, budget,
      allowed surface, and holdout acceptance bar. If repo evidence answers a
      field, do not ask it again.
    validation: "Unresolved LFD fields are either answered by evidence or listed as a compact question set."
    on_failure: "Route to interview; do not invent acceptance or budget."

  - id: load_canon
    action: Load DNA, gates, and active Pentagon runtime
    instruction: |
      Read the required refs that exist in this project. Confirm active eval
      canon from `docs/specs/spec-eval.md`, `dna/core/eval.dna.yaml`, and
      `core/eval`. Treat `core/testing`, `.lev/infra/pentagon`, and generated
      SDK proof flows as migration/compatibility inputs unless current repo
      evidence proves otherwise.
      Confirm the eval FlowMind path: prefer project-local `.lev/flows/<name>.flow.yaml`; otherwise use `plugins/sdlc/flows/eval-harness.flow.yaml` from the project or `~/lev`.
      Assign module-owned proof runners/tests to the behavior owner before adding files.
    validation: "Plan cites active shared package, state root, eval FlowMind path, owner package/example for each suite, required refs, and any drift."
    on_failure: "Do not invent a new framework; reconcile with current canon first."

  - id: map_layers
    action: Build the five-axis proof map
    instruction: |
      Map the target across: contracts/unit, integration, surface E2E, acceptance harness ratchet, and adversarial/eval/performance stress.
      Also map to current `dna/testing.yaml` classes: unit, integration, e2e_surface, harness_ratchet, agent_smoke, eval_harness.
    validation: "Every required class is marked pass/fail/skip with a reason and an owner."
    on_failure: "Missing class coverage becomes a finding, not an excuse."

  - id: build_eval_corpus
    action: Define dev/holdout cases and visibility policy
    instruction: |
      Build or specify dev and holdout inputs from source truth. Dedup, check
      diversity, reject seed/fixture overlap, and mark small evals as enumerable.
      Inputs may be visible; answers must live inside the scorer or outside the
      worker read surface. Holdout output is aggregate-only and rate-limited.
    validation: "Plan names dev/holdout source, size, diversity risk, visibility, and holdout feedback policy."
    on_failure: "No outer-loop claim can be trusted; mark eval_design_missing."

  - id: design_loss_function
    action: Specify target, constraints, instruments, and forced entropy
    instruction: |
      Define the metric at the right resolution, with both precision and recall
      style penalties. Name budgets, surfaces, methodology, capacity caps,
      score/lint/probe/status/proof commands or bindings, stall rule,
      exploration quota, and log requirements.
    validation: "The lfd block has target, constraints, instruments, forced_entropy, and visibility."
    on_failure: "A constraint without an instrument is a vibe; block the plan."

  - id: design_harness
    action: Specify setup, execution, observation, teardown, and receipts
    instruction: |
      Define fixtures, seed data, session/task type, tmux/exec/session behavior if relevant, attach/watch/intervene/resume checks, cleanup, cold-storage/archive policy if relevant, and exact receipt files.
      Name the owner-local path for tests, probes, fixtures, and suite-specific harness code before naming any shared `core/testing` helper.
      Verdicts must be artifact-only: manifest expected -> artifact actual -> verdict. Do not accept self-reported observations as proof.
      For runtime Pentagon proof, default required logs are cli.log, mcp.log, http.log, grpc.log, rust-client.log, go-client.log, python-client.log, and lev-exec-provider.log.
      For MCP proof, include an actual agent/coding-agent harness that loads MCP config, lists tools, calls the selected tool over MCP, and persists receipt/GateProof evidence.
      Include score/lint/probe/status mechanics when the use case needs loss
      descent or repeated optimization. Score must run lint first; lint must
      VOID without leaking eval membership; status must expose time/budget/spend
      and score history.
    validation: "Harness has owner-local placement, setup, run, observe, teardown, receipt paths, and fail-closed missing-receipt behavior."
    on_failure: "A one-shot demo is not a harness. Add repeatable lifecycle mechanics."

  - id: attack_it
    action: Generate adversarial probes before green-lighting
    instruction: |
      Run premortem, reverse brainstorming, devops game-day, architecture fitness-function thinking, and the NAAC final-boss pattern.
      Ask: how could an agent game this while keeping checks green? Test syntactic gaming, scope escape, semantic bypass, temporal gaming, structural evasion, malformed inputs, races, flooding, weak gates, missing context, timeout paths, fake receipts, and readiness/completion conflation.
      Add a gate critic: compare source design + DNA acceptance + execution verifier; fail if the verifier does not prove the highest-risk behavioral claim.
      Also run the LFD cheat pass: seed mirroring, miss-list mining, brute
      enumeration, scorer editing, judge gaming, one-sided metrics, dev-set
      victory, eval peeking, special-case branching, clock/budget amnesia,
      same-knob descent, and oracle-mining the enforcement instrument.
    validation: "Plan includes L5 adversarial attempts, performance budgets, gate critic result, and the expected fail-closed branch."
    on_failure: "If the check can pass without proving the behavior, the gate is weak."

  - id: preflight_loss_function
    action: Prove the harness is not trivially gameable
    instruction: |
      Before launch, define known-good and known-bad artifacts, run score/lint/
      probe/status, trip lint deliberately, attempt to read holdout answers from
      the worker surface, and simulate at least three lazy-optimizer cheap wins.
      Patch the loss function until those cheap wins fail closed or are more
      expensive than real work.
    validation: "Known-good passes, known-bad fails, lint VOID is non-oracular, probe/status run, holdout blinding check is documented, and cheap-win simulations are closed."
    on_failure: "Do not mark Pentagon ready; emit patch-mode next steps."

  - id: emit_plan
    action: Return a compact harness plan and next commands
    instruction: |
      Emit the template below. Include exact commands only when they are real in the repo.
      Use live help before command execution. Prefer `lev eval` surfaces when
      present. Compatibility surfaces may include `lev flowmind validate <flow>`,
      `lev exec --flow=<path> --root-path=<project> --knob key=value`, and
      legacy `lev pentagon propose|init|run|gate|doctor --project <path>`.
    validation: "Output includes user stories, acceptance criteria, owner-local placement, proof matrix, FlowMind path, adversarial probes, receipts, commands, and open decisions."
    on_failure: "Do not proceed to implementation; the harness plan is incomplete."
```

<pentagon_harness_plan>
## Pentagon harness plan: {target}

### User stories and acceptance criteria
- {operator story with daily-use path}
- {maintainer/reviewer story with promotion gate}
- {fail-closed acceptance criterion}

### Proof matrix
| Axis | Current canon class | Owner-local placement | Proof | Receipt | Gate |
|---|---|---|---|---|---|
| Contract/unit | unit | {owner module path} | {pure behavior} | {path} | {command} |
| Integration | integration | {owner module path} | {pipeline behavior} | {path} | {command} |
| Surface E2E | e2e_surface / agent_smoke | {owner module path} | {CLI/SDK/MCP/HTTP/gRPC use} | {path} | {command} |
| Harness ratchet | harness_ratchet | {owner module path} | {AC conformance} | {path} | {command} |
| Adversarial/eval | eval_harness | {owner module path} | {break attempts + perf budget} | {path} | {command} |

### Harness mechanics
Owner-local code: {module/package path for tests, probes, fixtures, and suite-specific harness}
Shared eval use: {core/eval helper, audit, runtime wrapper, gate evaluator, or legacy core/testing compatibility input used}
FlowMind: {project-local flow or plugins/sdlc/flows/eval-harness.flow.yaml}
Config stack: {FlowMind defaults -> project config -> task/suite overlay -> runtime knobs}
Setup: {fixtures, config roots, session/task type}
Execution: {SDK/FlowMind/CLI path}
Observation: {watch/attach/intervene/resume/telemetry}
Teardown: {cleanup, archive, cold storage}
Receipts: {append-only evidence paths}

### LFD contract
Target: {metric, bar, precision/recall failure directions}
Constraints: {budget, spend, surface, methodology, capacity caps}
Instruments: {score, lint, probe, status, proof commands/bindings}
Forced entropy: {stall rule, exploration quota, iteration log}
Visibility: {dev input policy, holdout aggregate-only/rate-limited policy, answer storage}

### Adversarial probes
- {probe}: expected fail-closed result {result}
- {probe}: expected fail-closed result {result}
- {probe}: expected fail-closed result {result}

### LFD preflight
- known-good: {artifact or fixture}; expected {score/verdict}
- known-bad: {artifact or fixture}; expected {score/verdict}
- lint trip: {violation}; expected `VOID: constraint violation`
- probe gap: {threshold and expected result}
- holdout blinding: {worker read-surface check}
- cheap paths closed: {count and summary}

### Commands
- `lev flowmind validate {flow-path}`
- `lev exec "run adversarial eval" --root-path {project} --flow {flow-path} --knob task="{target use case and promotion gate}" --knob strategy_kind=adversarial`
- `lev eval --help`
- legacy only when no eval surface exists: `lev pentagon propose|init|run|gate --project {path}`

### Open decisions
- {decision needing human review}
</pentagon_harness_plan>


## NAAC final-boss and anti-cheat patterns

Use these patterns when the feature is safety-critical, behavioral, or easy for an agent to fake.

```yaml
patterns:
  final_boss_loop:
    shape: "run-final-boss -> triage -> fix-one -> re-run"
    use_when: "release truth needs daemon/process health plus invariant catalog coverage"
    note: "If daemon health matters, use a spawning final-boss path, not a catalog-only probe."
  artifact_only_verdicts:
    shape: "manifest expected -> artifact actual -> verdict"
    rejects: "self-reported observations, diagnostic-only event streams, scenario_results in acceptance path"
  gate_critic:
    shape: "source design + DNA acceptance + execution verifier -> claim coverage verdict"
    rejects: "no-regression gates that do not prove the behavioral claim"
  claim_ledger:
    shape: "claims -> evidence -> verdict"
    receipt_index: "receipt_id and exec_id resolve prompts, outputs, commands, stdout/stderr, final branch, touched files, and claim coverage"
  deterministic_kernel_track:
    shape: "FlowMind/Argo/WASM gate evaluation for portable fail-closed deterministic checks"
    use_when: "browser/edge/offline or untrusted plugin gates need replayable evaluation traces"
  llm_judge_as_observer:
    shape: "LLM judge -> typed observation payload -> deterministic score/compare -> receipt-backed branch"
    rejects: "judge prose as certification, single-sample decisions, post-hoc criteria, missing evidence refs"
```

## Rationalization table

| Excuse | Reality |
|---|---|
| “Unit/integration/e2e is enough.” | Not for agentic systems; eval/simulation plus harness proof catches gaming, weak gates, and operational drift. |
| “The demo worked once.” | A demo without setup/teardown/receipts is not repeatable and cannot ratchet. |
| “The constraint says PASS.” | Ask the adversarial-review question: should it pass, or was it gamed in letter not spirit? |
| “542 tests passed.” | Real-world usage still broke `lev exec`; surface behavior and receipts must be proven. |
| “The flow produced a receipt.” | Receipt success is command evidence, not acceptance-coverage evidence, unless it ties claims to proof. |
| “Raw HTTP proves cross-language parity.” | Current `core/testing` defaults to generated SDK proof for Rust, Go, and Python; raw HTTP is explicit fallback only. |
| “We can add performance later.” | Performance budgets are part of adversarial L5 for operational claims. |
| “The judge said pass.” | Judge output is an observation; promotion needs typed evidence, deterministic scoring, and receipt refs. |
| “This is overkill.” | The mental model is hostile handoff: untrusted contractors left, lives or money are on the line, and the harness saves the company. |

## Red flags

- The plan says “tests” but not “receipts”.
- The verifier can pass without proving the highest-risk behavioral claim.
- Timeouts route to success or “best effort” without explicit policy.
- LLM-as-judge output is treated as a promotion verdict without deterministic scoring or typed evidence refs.
- The agent sees no gate catalog or context needed to satisfy the real constraint.
- CLI/MCP/HTTP/SDK paths are assumed equivalent instead of proven through surfaces.
- Project-specific harness logic leaks into generic core helpers.
- `core/testing/src/__tests__` contains module-owned daemon, tmux, Poly provider, app, or browser proof tests.
- `core/testing` imports daemon protocol adapters or owns daemon surface manifests/runners.
- MCP transport proof uses curl/raw HTTP/direct handler calls without an actual agent-style MCP config, tool listing, tool selection, call, and receipt.

## Done checks

```bash
test -f .lev/validation-gates.yaml
test -f dna/gates.yaml && test -f dna/testing.yaml
test -f plugins/sdlc/flows/eval-harness.flow.yaml || test -f "$HOME/lev/plugins/sdlc/flows/eval-harness.flow.yaml"
test ! -d core/testing || test -f core/testing/skills/pentagon/SKILL.md
test ! -d core/testing || test -f core/testing/flows/pentagon-sdk-poly-binding.flow.yaml
test -f plugins/sdlc/flows/adversarial-review.flow.yaml || true
! rg -n "@lev-os/daemon-http|@lev-os/daemon-grpc|daemon-surface-app-manifest|daemon-surface-artifact-gate|daemon-surface-real-app-runner" core/testing/src core/testing/package.json
! find core/testing/src/__tests__ -maxdepth 1 -type f | rg "daemon|tmux|poly-provider|architect-app|browser-mcp"
wc -l .agents/skills/pentagon/SKILL.md
```

A Pentagon plan is complete only when missing receipts, malformed context, weak verifiers, fake provider provenance, and unobserved sessions fail closed.
