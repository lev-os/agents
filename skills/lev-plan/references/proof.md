# Proof

How a plan is proved, for `design_proof`, `prove_requirements`, and
`judge_readiness`: what the claims are, who or what answers each one, and how
a check is kept from passing when it should fail. It applies at plan time and
again at Emit. The steps are in [`../SKILL.md`](../SKILL.md).

## Contents

- [Claims](#claims): the three passes, the claim table, where the rows live
- [Program, agent, or person](#program-agent-or-person): who answers a claim
- [How not to cheat a check](#how-not-to-cheat-a-check): the guards
- [Admit a check before you trust it](#admit-a-check-before-you-trust-it): the blind loop
- [Row and check shape](#row-and-check-shape): the `requirements:` row and its `check:`
- [Proof and Evaluator Selection](#proof-and-evaluator-selection): choose the proof from current contracts; holds
- [Who decides](#who-decides): code, core/eval, the LLM, a human
- [TDD Rules](#tdd-rules): only when TDD is relevant to a step or packet

## Claims

Everything the work must make true is one list of claims: operator acceptance,
slice exits, constraints, forbidden moves and source claims are all rows of it.
Write it in three passes:

1. **Think.** List what must be true when the work is done and what must never
   be true (regressions, forbidden moves, false-green paths, a second path
   left behind). This list is scratch work; only its sentences land.
2. **Write.** Each item becomes one row whose text is a plain sentence; a
   negative idea is written into the sentence ("An invalid flow never exits 0").
3. **Prove.** For every row ask "how will we prove it?" and name one of
   program, agent, or person (below). When nothing can show it, sharpen the
   sentence until something can, or route the open question to `/interview`.

The plan holds one row for each claim in the Claims and Proof table of the
[plan template](../../work/templates/plan.md): its sentence, its slice, the
failure it rules out, its proof (program, agent, or person, at the smallest
relevant level: local, integration, field, or external owner), its guard, and
its source. The guard of a program claim is its known-bad control and its
check owner. Any claim may also name what looks like proof and is not; at Emit
that text becomes the row's `invalid_proof`.

**One list.** In a plan file the Claims and Proof table is the claim list.
The frontmatter's `steps[].validation` and `acceptance_criteria` name the same
claims and add none; in an older plan that has no table, they and a task's
`claim_verifier_map` are the claim source. At Emit the claims become the
task's `requirements:` rows, each with its `source_ref` and its proof,
preserving stable claim references and keeping dependencies, scope and stop
conditions explicit; that list is then the one ledger, and the plan cites its
IDs and keeps no second executable list. Dedicated `claim.yaml` and direct
runtime ingestion of plan claims are future work, not newly supported schema
or CLI behavior.

**Plan parts as rows.** The success sentence is the operator's
`type: acceptance` row; a slice exit is an acceptance row with `owner_slice`;
constraints and checkable exclusions are `type: constraint` rows or
`invalid_proof` entries on the row they threaten. A typed check such as
`no_future_leakage: bool` becomes a row named after the failure whose `check:`
exit decides it.

## Program, agent, or person

Name one for every claim:

- **Program**: a command can show it. The claim gets a `check:`. Use a program
  only where a command decides the claim.
- **Agent**: only reading the change can show it (one path, no swallowed
  error, tests cover both outcomes). The row has no `check:`; the review agent
  answers it from the diff.
- **Person**: independent evidence (a field or external-owner verifier) or
  human review decides it. The row has no `check:`; its sentence names the
  evidence and the acceptance owner.

Decisive claims need proof from outside the model loop that is credible for
the claim. When none of the three exists yet, list the proof as unresolved
rather than manufacturing a weak command to fill the slot.

## How not to cheat a check

A check that cannot fail proves nothing. Each program claim carries its guard:

- **Name the failure.** Name every check after the failure it rules out.
- **Known-bad control.** Each program check names an input on which it must
  fail, and a check owner who runs the check against that control before the
  check can justify acceptance. Planning names the run and the required
  evidence; authorized execution collects it.
- **Red today.** Run every check once before emitting. A check for what the
  slice adds or fixes is red on today's tree; a check already green is a
  regression guard. A slice whose checks are all green today proves nothing
  new: add the red check or say why the review agent carries the change.
- **False-green list.** Record each adversarial finding on the claim it
  threatens: the path that looks like proof and is not goes in
  `invalid_proof`, and the command that falsifies it is the row's `check:` (or
  the review agent answers the row).
- **A reader that built none of it.** Agent claims are answered in fresh
  context by a reader that did not build the artifact.
- **The owner's rerun.** The plan's owner reruns every program check and every
  known-bad control once at the final commit; a worker's green report is not
  that rerun.

Stale evidence, agreement among workers, and the other near misses of the
outcome are the plan's Does Not Count list
([Plan parts](plan-parts.md#does-not-count)).

## Admit a check before you trust it

A task is ready to launch (a pre-flight before a long or costly run) when it
has a definition of done and its checks are admitted. The definition of done is
the `type: acceptance` rows. A check is admitted when it passed the blind loop
in `skill://eval-builder` (section "Admit a rule before you trust it";
`.lev/pm/decisions/20261031-rule-admission-loop.yaml`):

- An agent that sees only the row's `text`, never its `check:`, writes inputs
  with the right answer for each.
- The check runs on them. Each miss goes back to you with a review agent's note.
- Repair the check, then run a fresh blind round. Admit it when a round finds
  no miss.
- A check you tested only on your own examples is not admitted. In the spike,
  16 of 16 passed their author's examples; 0 were right on every blind input.
- A row the review agent answers (no `check:`) needs no admission.
- No flow or code runs this yet. Record the rounds in the row's
  `invalid_proof` or the plan's proof section. Hold a task whose checks are
  not admitted as `needs_review`, not `blocked`.
- The words for rule, claim, scenario and ready are not settled. Use the task's
  own words.

Worked example: the row "No module outside core/poly imports @lev-os/poly
internals" first had one regex check. It passed both of its author's examples.
Blind inputs found a dynamic `import()` into poly's built files and a relative
path into `core/poly` that the regex missed. After the review note (read every
module specifier and resolve it against poly's exports map) it was right on 6
of 6 inputs, then on 8 of 8 fresh ones; admitted. Evidence:
`~/.local/state/lev/evidence/foundation-20261030/spike-admission/`.

## Row and check shape

Row shape of a task's `requirements:` list (`core/domain/src/task-requirements.ts`;
the task reader is `core/workstream/src/task-packet.ts`). Where the list is
written is in [Execution Packet](execution-packet.md#requirements-ledger).

```yaml
schema: lev.task.v2
requirements:
  - id: invalid-flow-exits-nonzero    # unique across dna.yaml and evals/
    type: acceptance                   # acceptance | constraint | a claim type
    owner_slice: <slice id>            # set when the row is that slice's exit
    text: An invalid flow makes `lev flowmind validate <file>` exit non-zero.
    source_ref: <plan#section or path:line>   # when a plan or design states it
    risk: high                         # optional: high | medium | low
    invalid_proof: [<evidence that looks like proof and is not>]
    check:                             # omitted when the review agent answers
      command: lev                     # the program
      argv: [flowmind, validate, <known-bad file>]
      expectedExit: nonzero            # zero | nonzero | any
      timeoutMs: 120000
```

- At least one `type: acceptance` row has no `owner_slice`: the operator's
  acceptance.
- A claim type (`behavior_change`, `architecture_boundary`, `no_regression`,
  ...) is for a claim a plan or design states; its slice lists it in
  `claim_coverage` and `verifier_contract.proves_claims`, and
  `lev entity task validate` names any trace fields its type needs.
- `check:` is a core/eval command case without `id` (the row id is the case
  id; `EvalCommandCase` in `core/eval/src/command-cases.ts`): `command` is the
  program and `argv` its arguments, plus optional `cwd` (inside the project),
  `timeoutMs`, `expectedExit` or `expectedExitCode`, `stdoutContains`,
  `stderrContains`. Output-text matching is leaving the check shape: write a
  parsed-field comparison with a negative control instead
  (`.lev/pm/decisions/20261030-output-text-checks.yaml`, ruled 2026-11-01). A
  shell line is rejected: a pipe or `&&` becomes separate rows. A search that
  must find nothing is a parser lint or a behaviour test, never a text scan
  such as `git grep` (`.lev/pm/decisions/20261030-text-scan-checks-hard-cutover.yaml`).
- A check that needs a known input (a bad file, a sample) points at a fixture
  the packet writes in the task folder under `fixtures/`, named so repo-wide
  scans of that kind skip it (a flow fixture is `<name>.yaml`, never
  `<name>.flow.yaml`).

## Proof and Evaluator Selection

Planning chooses the proof before anything runs, from contracts that exist
today.

- **Current contracts only.** The current eval gate reads two inputs: the node
  packs of the selected FlowMind flow and the task's `requirements:`. Choosing
  evaluators is therefore choosing the flow: resolve it from the project's
  current FlowMind contracts (flow files that exist and validate today). A
  flow or evaluator recalled from memory, a filename, or an older plan is
  unverified until live help and the current files confirm it.
- **Record the selection for humans.** Name the selected flow and the proof it
  supplies in the plan's proof section, in the `Proof:` and `Launch:` lines of
  the output, and in existing source refs such as a row's `source_ref`. The
  task packet keeps its current keys and carries its own proof only as
  requirement rows and their `check:`.
- **Hold, never drop.** Hold the slice that carries the claim when a source
  brings an `eval_packs` key or an inline evaluator definition, when no current
  contract declares the evaluator a claim needs, or when binding the selection
  would need a packet key that does not exist (a proof-gate container, a flow
  field, a boolean packet field). A contract hold is a `code_blocker` naming
  the missing owner contract; an interview hold is a `decision_blocker` routed
  to `/interview` when choosing the proof is a human decision. A claim weakened
  to a check that happens to exist is a lost row.
- **Shared profiles by ref.** Reference shared runtime, standards, evidence,
  and proof profiles through their existing individual refs. When the
  repository has rule files or boundary laws, load the applicable files
  before judging readiness and persist only their refs. Do not copy their
  generic receipt fields, test taxonomies, or review checklists into every
  plan or task.
- **Protected holdouts stay with their owner.** Cite a holdout policy by ref;
  holdout answers, scorer internals, private lint details, and calibration
  fixtures never enter a plan, map, spec, or packet, or the authoring scope.
- **Proof is not launch.** Proof is claims and their `check:`. The launch
  commands and the flow choice are in
  [Flow and Launch](execution-packet.md#flow-and-launch).

## Who decides

- Deterministic code owns schema validation, reference existence, graph cycles,
  path policy, write-scope enforcement, and reproducible command results.
- core/eval decides whether a `check:` or evaluator passed; Exec performs
  effects and collects evidence. Planning authors requirement text and
  references, and states neither a verdict nor an effect in advance.
- The LLM owns intent interpretation, slice verticality, semantic readiness,
  verifier relevance, unnecessary complexity, and stale-context judgment.
- A human owns unresolved product tradeoffs and explicit approval where policy
  requires it.

## TDD Rules

Read this section only when TDD is relevant to a plan step or a packet, before
designing its proof.

TDD tests describe one logical behavior through the agreed public seam, using
domain vocabulary and independently derived expected values (spec examples,
known literals or a separate oracle). Avoid mirroring the implementation in the
assertion, private-method tests and side-channel checks that bypass the interface.
Prefer real internal collaborators; isolate external APIs, time/randomness and
necessary filesystem/database boundaries with existing adapters or test resources.
Use operation-specific boundary interfaces and injected dependencies where they
already fit; this is not permission to add abstractions solely for mocking.
Prefer an isolated test database when database behavior is the claim; otherwise
state what a boundary fake cannot establish. Each operation fake should expose
its expected response shape and exercised endpoint without conditional catch-all
setup, retaining the interface's type checks. Flag call-count/order assertions
and HOW-named tests when they merely couple to internals; observable protocol
ordering may itself be a legitimate contract. Check that behavior-preserving
internal refactoring would leave the test meaningful and green.
Treat every rule in this TDD section as active in every cycle: check it before
the first RED and again before selecting each next behavior. Work one behavior
through RED then GREEN before selecting another; GREEN adds only the current
cycle's production code needed to pass its test, with no anticipated tests or
features. A coherent Ralph unit may contain several sequential cycles. Keep
unrelated refactoring for review and an authorized follow-up; preserve the existing
frozen-test and isolation contract below.

Before forming a TDD packet, read the relevant `CONTEXT.md` when present and
applicable ADRs; record their refs and require test names plus public-interface
vocabulary to match them. Synthesize settled conversation decisions without
restarting an interview; expose only unresolved
choices that change scope or acceptance. Describe the user problem, intended
behavior, actors, exclusions and testing decisions without padding story counts.
Prefer the highest existing public test seam that actually observes the claim.
If none exists, propose a new seam at the highest viable public boundary; ask
only when that seam's tradeoff needs a user decision.

For ordinary TDD, plan and emit one coherent worker-owned batch: the behavioral
RED-to-GREEN cycle through the agreed public seam, its write scope, and its
verifier, followed by the declared checks and at most one integrated checkpoint
review covering spec drift and code quality. The same worker may write the
failing test and implementation; the controller confirms the failure is
behavioral and reruns the accepted check. Separate RED, GREEN, spec-review,
quality-review, or verifier agents are the isolated topology: use it only when
the user explicitly selects isolated TDD or a high-assurance execution contract
requires hidden holdouts or enforced role separation. Planning records that
exception; it does not dispatch agents.
