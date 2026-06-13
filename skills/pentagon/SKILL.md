---
name: pentagon
description: Use when designing Lev Pentagon harnesses, eval suites, acceptance criteria, adversarial probes, or proof gates for agentic features before implementation or promotion.
---

# Pentagon Harness Builder

First output is a harness plan. Do not start with unit tests. Pentagon work asks: “what proof would survive a hostile review?”

Current shared Pentagon library canon is `core/testing`; `core/eval` does not exist yet. Treat future `core/eval*` as an evolution path, not the active source of truth.

## Operating frame

Pentagon is Lev’s agentic proof model: conventional tests plus repeatable harnesses, receipts, adversarial evals, and real operational usage. The harness is the tooling that sets up, executes, attacks, measures, tears down, and records evidence for a use case.

Pentagon is self-contained. Do not require a separate UltraQA skill or mode. The useful part to absorb is the hostile runtime scenario matrix: happy path plus malformed input, interruption, prompt injection, cancel/resume, stale state, dirty worktree, hung command, flaky/retry, and misleading success output. In Lev, those are Pentagon adversarial/eval inputs that must become typed evidence, not a separate workflow dependency.

`core/testing` is a shared Pentagon/testing library only. It owns diagnostics, infra root helpers, proof helper primitives, suite interfaces, and generic SDK/Poly binding gates. It must not become the home for daemon, tmux, app, provider, browser, or example-specific proof runners/tests.

Module-owned harnesses live with the module or example that owns the behavior and import `@lev-os/testing/pentagon` as a library:
- Daemon manifest/gate/runner suites: `@lev-os/daemon-pentagon`.
- Tmux/FlowMind runtime suites: `@lev-os/tmux-harness/pentagon`.
- Poly provider and Poly MCP suites: `core/poly`.
- App/example suites: `community/examples/<example>/pentagon`.
- Live external adapter references, such as browser MCP, stay with the adapter/example because they require daemon/extension setup.

For MCP promotion proof, raw curl, raw HTTP, or direct handler invocation is not sufficient. The agent_smoke path must load an agent-style MCP config, connect with a real MCP client/transport, list tools, select the Poly-bound tool by schema, call it, and write receipt/GateProof artifacts.

Use this skill to plan or harden harnesses. Use the runtime wrapper in `core/testing/skills/pentagon/SKILL.md` and `core/testing/flows/pentagon-sdk-poly-binding.flow.yaml` when you need `lev pentagon propose|init|run|gate|doctor` execution.

## Evaluation authority model

LLM-as-judge and adversarial agents are evidence generators, not promotion authorities. FlowMind may ask an LLM to observe, rank, attack, or judge samples, but certification requires typed observations, deterministic scoring or comparison, policy transitions, and receipt/GateProof refs.

Use this split:
- Deterministic: static checks, schema validation, command exit codes, fixed-seed replay, statistical comparison, threshold math, artifact existence, typed gate-chain validation.
- Non-deterministic: claim extraction, reverse brainstorming, hostile scenario design, LLM-as-judge scoring, cross-model critique, semantic adequacy review.
- Hybrid: LLM produces typed observation payloads; a code companion or `lev.validate` scorer validates shape, computes pass/fail/hold, and records the branch.
- HITL: human review can certify ambiguous semantics only when it produces an explicit receipt or approval ref.

## Project and FlowMind resolution

Resolve the project root in this order: explicit `--project` or `--root-path`, nearest ancestor with `.lev`, then `~/lev` only when the work is Lev core/runtime work. Do not assume the current shell is already in the right project.

FlowMind config should carry durable defaults. Project-local config supplies derived local values. Task overlays supply the specific target and promotion gate. Runtime `--knob`/`--with` values should only specialize the current run.

```text
FlowMind defaults
  < project-local .lev/config.yaml or .lev/config/*.yaml
  < task execution.yaml / suite manifest overlay
  < runtime --knob / --with
```

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
    - id: pentagon-sdk-poly-binding
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
        Prove a Poly-bound capability across CLI, MCP generated client, HTTP,
        gRPC, generated Rust/Go/Python SDK clients, and lev-exec provider
        provenance. This is SDK/Poly binding proof, not full product adversarial
        fitness generation.
    - id: daemon-run-fabric-real-world-usage-v1
      path: core/daemon-pentagon
      owner: "@lev-os/daemon-pentagon"
      use_when: >
        Prove daemon-owned run fabric, implemented daemon surfaces, app manifests,
        and artifact-only daemon gates. Core testing may route to this owner, but
        must not import daemon protocol adapters.
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
  gates:
    - .lev/validation-gates.yaml
    - dna/gates.yaml
    - dna/testing.yaml
    - dna/hygiene/hygiene.yaml
  runtime:
    - core/testing/config.yaml
    - core/testing/src/pentagon.ts
    - core/testing/src/proof.ts
    - core/testing/src/__tests__/pentagon.test.ts
    - core/testing/skills/pentagon/SKILL.md
    - core/testing/flows/pentagon-sdk-poly-binding.flow.yaml
    - plugins/sdlc/flows/eval-harness.flow.yaml
    - plugins/sdlc/config.yaml
    - plugins/sdlc/src/handlers/sdlc.ts
  project_config:
    - .lev/config.yaml
    - .lev/config/*.yaml
    - .lev/flows/*.flow.yaml
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

  - id: load_canon
    action: Load DNA, gates, and active Pentagon runtime
    instruction: |
      Read the required refs that exist in this project. Confirm whether `core/testing` or `core/eval` is active. Today, `core/testing` owns shared Pentagon library primitives, `.lev/infra/pentagon` owns project state, and generated SDK proof is the default generic suite.
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

  - id: design_harness
    action: Specify setup, execution, observation, teardown, and receipts
    instruction: |
      Define fixtures, seed data, session/task type, tmux/exec/session behavior if relevant, attach/watch/intervene/resume checks, cleanup, cold-storage/archive policy if relevant, and exact receipt files.
      Name the owner-local path for tests, probes, fixtures, and suite-specific harness code before naming any shared `core/testing` helper.
      Verdicts must be artifact-only: manifest expected -> artifact actual -> verdict. Do not accept self-reported observations as proof.
      For runtime Pentagon proof, default required logs are cli.log, mcp.log, http.log, grpc.log, rust-client.log, go-client.log, python-client.log, and lev-exec-provider.log.
      For MCP proof, include an actual agent/coding-agent harness that loads MCP config, lists tools, calls the selected tool over MCP, and persists receipt/GateProof evidence.
    validation: "Harness has owner-local placement, setup, run, observe, teardown, receipt paths, and fail-closed missing-receipt behavior."
    on_failure: "A one-shot demo is not a harness. Add repeatable lifecycle mechanics."

  - id: attack_it
    action: Generate adversarial probes before green-lighting
    instruction: |
      Run premortem, reverse brainstorming, devops game-day, architecture fitness-function thinking, and the NAAC final-boss pattern.
      Ask: how could an agent game this while keeping checks green? Test syntactic gaming, scope escape, semantic bypass, temporal gaming, structural evasion, malformed inputs, races, flooding, weak gates, missing context, timeout paths, fake receipts, and readiness/completion conflation.
      Add a gate critic: compare source design + DNA acceptance + execution verifier; fail if the verifier does not prove the highest-risk behavioral claim.
    validation: "Plan includes L5 adversarial attempts, performance budgets, gate critic result, and the expected fail-closed branch."
    on_failure: "If the check can pass without proving the behavior, the gate is weak."

  - id: emit_plan
    action: Return a compact harness plan and next commands
    instruction: |
      Emit the template below. Include exact commands only when they are real in the repo.
      Use live help before command execution. Current verified surfaces include `lev flowmind validate <flow>`, `lev exec --flow=<path> --root-path=<project> --knob key=value`, and `lev pentagon propose|init|run|gate|doctor --project <path>`.
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
Shared Pentagon use: {core/testing helper, audit, runtime wrapper, or gate evaluator used}
FlowMind: {project-local flow or plugins/sdlc/flows/eval-harness.flow.yaml}
Config stack: {FlowMind defaults -> project config -> task/suite overlay -> runtime knobs}
Setup: {fixtures, config roots, session/task type}
Execution: {SDK/FlowMind/CLI path}
Observation: {watch/attach/intervene/resume/telemetry}
Teardown: {cleanup, archive, cold storage}
Receipts: {append-only evidence paths}

### Adversarial probes
- {probe}: expected fail-closed result {result}
- {probe}: expected fail-closed result {result}
- {probe}: expected fail-closed result {result}

### Commands
- `lev flowmind validate {flow-path}`
- `lev exec "run Pentagon adversarial eval" --root-path {project} --flow {flow-path} --knob task="{target use case and promotion gate}" --knob strategy_kind=adversarial`
- `lev pentagon propose "{intent}" --project {path}`
- `lev pentagon init --project {path}`
- `lev pentagon run --project {path}`
- `lev pentagon gate --project {path}`

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
