# Agentic user research

Simulate day-in-the-life journeys to find where individual workflows and shared
projects break down over time. Findings are synthetic research hypotheses until
checked against product behavior or actual users. This method documents an
execution procedure; it does not provide a simulation engine or a new CLI.

## Contents

- [Prepare the study](#prepare-the-study)
- [Save study state](#save-study-state)
- [Allocate models and experiments](#allocate-models-and-experiments)
- [Run one synchronized tick](#run-one-synchronized-tick)
- [Recover an incomplete tick](#recover-an-incomplete-tick)
- [Select the longer continuation](#select-the-longer-continuation)
- [Keep evidence and analyze journeys](#keep-evidence-and-analyze-journeys)
- [Apply the judgment checks](#apply-the-judgment-checks)
- [Verify the method](#verify-the-method)

## Prepare the study

1. Read the supplied product stimulus and existing problem framing. Start from
   raw evidence where available: observed workflows, interviews, support cases,
   task records, and current product behavior. Reuse Persona Detection to create
   ten distinct people. Record each person's role, authority, daily agenda,
   goals, constraints, current workaround, and source evidence. Mark invented
   details as assumptions. Include people who share an organization and project
   when collaboration is in scope; include independent users where relevant.
2. Apply the write check below, then write `study_plan.md` in the existing UX run
   folder (`RUN_DIR`). Define the
   research question, success/failure observations, starting world, organizations,
   project membership, permissions, deadlines, available actions, and product
   rules with evidence references. Give each person their own knowledge, history,
   unfinished work, and local view of shared facts. A private fact reaches another
   person only through a recorded event that they can observe.
3. Declare simulated time and action-duration rules from workflow evidence.
   A tick is a synchronized decision round, not model response time. Busy people
   can choose to wait or continue existing work as their one decision. Keep
   unsupported duration estimates unknown; ten ticks alone do not prove that a
   complete workday was covered. Record any synthetic time assumptions.
4. Resolve available agent runners and actual model identifiers before launch.
   Record concurrency, finite response deadlines, token/cost limits, stop
   conditions, scenario variation, and the experiment's assignment seed. Use
   existing authorized orchestration tools; the coordinator waits for completion
   events instead of polling unchanged workers. Keep all actions simulated unless
   a separate scope authorizes product interaction. Missing runners, unresolved
   models, or an execution request that exceeds the available budget stop launch.

Completion: the study plan separates supplied facts, observed evidence,
assumptions, and unknowns; every person has an agenda and a permitted local view;
the execution budget and prerequisites are resolved before dispatch.

## Save study state

Before saving a study artifact, compile the user's intended outcome, selected
route, permitted effects, destination, and current lifecycle stage. Check that
the destination belongs to this study and that the requested effects authorize
this write. Reuse an explicitly selected run folder; preserve other sessions'
artifacts. A request to document or plan the method authorizes only that work;
dispatch and product effects need their own scope. If a destination or authority
is unresolved, record the blocker and keep the proposed content in memory or an
authorized scratch location until it is resolved. Do not mark it saved.

Keep this ledger in `study_plan.md`, with one row per artifact. Update it after
readback of a saved artifact or checkpoint, including an incomplete checkpoint.
Confidence describes the evidence for that row, with its basis; it does not turn
a simulated result into observed user behavior.

<study_state>

| compiled_intent | route | lifecycle_stage | memory_state | disk_state | artifact_ref | blocker | confidence |
|---|---|---|---|---|---|---|---|
| {requested outcome and permitted effects} | agentic-research | {current stage} | {proposed or reflects checkpoint} | {absent, saved, incomplete or committed; readback basis} | {exact path/version or unresolved} | {none or reason} | {confidence and evidence basis} |

</study_state>

Validation: every claimed saved artifact has an authorized destination and
readback evidence; each row identifies the route, lifecycle stage, memory versus
disk state, artifact reference, blocker, and confidence. A blocked launch may
still have a saved plan; a saved plan is not a committed simulation tick.

## Allocate models and experiments

Default breadth: **ten independent experiments × ten people × ten ticks = 1,000
scheduled persona decisions**. Reset world state and personal memories between
experiments. Record the scenario variation/seed so these are independent starts,
not ten continuations of one world. Retain scenarios and seeds for comparison.

Default depth: select one ten-person cohort and its checkpoint, then run **fifty
additional ticks = 500 scheduled decisions**. Total: **1,500**. An explicit
smaller rehearsal can override these sizes; record its coverage limits.

Allocate models across scheduled persona decision calls, not people or ticks:

| Model label | Share | Decisions in the default experiment |
|---|---:|---:|
| Haiku | 50% | 750 |
| Sonnet | 30% | 450 |
| Opus | 19% | 285 |
| Fable | 1% | 15 |

Construct the assignment schedule before launch using the recorded seed. Spread
assignments across people, experiments, and phases to reduce confounding. A
person's identity and memory persist when their model changes. Record requested
and actual model identifiers per call; family labels alone are insufficient.
Resolve Fable to an available provider/model rather than guessing its identity.
Report unavailable or mismatched models and hold dependent execution; substitutions
require a revised study choice. Never report an unobserved mix as achieved.

Retries and coordinator calls are separate overhead, outside these scheduled
decision quotas. On a size change, use largest-remainder rounding with table
order as the tie-breaker; report both target and achieved shares. If people
leave, preserve them in the journey history and explicitly revise the remaining
schedule rather than silently reducing the cohort or inflating completed counts.

Completion: scheduled calls sum to the declared total, assignments resolve to
available models, and the requested mix is distinguishable from actual usage.

## Run one synchronized tick

1. **Freeze the input.** Save the experiment, tick, and world version. Prepare
   one brief per person with objective, role, agenda, permitted actions, visible
   world state, personal history, and unfinished work. Reference only evidence
   they may know. Give workers no state-writing authority. Their stop condition
   is one next decision, including an explicit wait if that is their choice.
2. **Dispatch and wait.** Dispatch ten bounded persona calls using the assigned
   models. Reuse workers only when their context can be restricted to the same
   person's allowed knowledge; otherwise use fresh bounded context. The
   coordinator collects responses and measures wall-clock latency without
   steering anyone's choice or advancing the world while responses are pending.
3. **Validate decisions.** Each response identifies its person, input world
   version, one chosen action and target, brief reason, expected outcome, and
   relevant unknowns. Reject multiple actions, stale input, or use of private
   information outside the brief. A plausible attempt at a forbidden action
   remains a valid decision: product rules determine its denied outcome.
4. **Resolve and commit together.** Once all responses are valid, determine
   effects against the frozen input under the recorded product rules. Preserve
   conflicts, denials, delays, and failed attempts. For unknown concurrent-edit
   behavior, leave affected changes unapplied, record the unresolved outcome,
   and hold actions that depend on it. Never choose a winner by response order
   unless the product rule supports it. Commit one next world version and its
   outcomes, then update each person's view with only observable consequences.

Completion: one accepted decision per person, one committed world transition,
and traceable outcomes. Round two reads that committed state; it does not read
another agent's uncommitted proposal. Measure simulated time separately from
dispatch/collection/validation latency and token/cost overhead.

## Recover an incomplete tick

Keep valid responses and retry only missing, malformed, or failed responses
**once**, against the same frozen world version and model assignment. Persist
attempt counts; reopening a checkpoint does not renew the retry budget. After
the retry fails, save an incomplete checkpoint and stop before any world effect.
Record the failure and correction needed to resume.

A checkpoint includes the experiment/tick identity, frozen input and world
version, private memories, accepted responses, attempts, pending people, model
schedule, simulated time, and whether the next world version was committed.
Resume reuses accepted responses. Commit at most once for an experiment/tick;
if already committed, return its recorded outcome and advance to the next tick.
Unclear commit state must be reconciled before further action. Keep private
memories out of other personas' resumed briefs.

Completion: a failed tick has no partial effects, and resumption cannot apply
the same transition twice. Repeated provider failure remains an execution gap,
not a user behavior finding.

## Select the longer continuation

Compare all ten breadth runs using the study's coverage goals, collaboration
failures, and unresolved consequences. Write the selected cohort, exact world
checkpoint, selection rationale, and omitted coverage into `study_plan.md`.
Continue all ten people from that state for fifty additional ticks without
resetting relationships, goals, private memories, or unfinished work. If JP
selects a cohort, record that selection and its coverage tradeoff.

Completion: the depth run has a recoverable starting checkpoint and an explicit
selection rationale. Its findings remain selected-case exploration, not a
population frequency estimate.

## Keep evidence and analyze journeys

Keep the study plan, day-in-the-life narratives, findings, and `summary.md` in
`RUN_DIR` as Markdown. Keep raw JSON decisions, model usage, world versions,
timing, and checkpoints in the host-local XDG state/data route selected by the
project. Where none is declared, use `${XDG_STATE_HOME:-$HOME/.local/state}/lev/`
with a unique study directory. Link those runtime artifacts from the report;
do not commit them or copy private persona memory into shared briefs.

Maintain a source/coverage table in the study plan: user requirement or evidence
source, destination artifact, represented/assumed/unknown status, and open gap.
Distinguish in-memory state from saved/committed checkpoints. Raw responses stay
at their evidence locations; prose summaries are projections, not replacements.

For each person, narrate their agenda, decisions, delays, dependencies, failures,
recovery, and unfinished work. For each failure hypothesis, record its source
experiment/tick/person, world before/after, expected versus observed simulated
outcome, competing explanations, supporting evidence, and the smallest product
reproduction or real-user research check that could confirm or falsify it.
Separate coordination/provider errors from UX findings. Report scheduled,
completed, denied, failed, retried, and unresolved calls with actual model shares.

Completion: every finding links to raw decisions and world transitions, states
its evidence limits, and names an independent next check. Feed supported
hypotheses into existing research/JTBD artifacts where relevant; do not claim
product reproduction, real-user validation, or wireframes from simulation alone.

## Apply the judgment checks

These are synthetic teaching examples, not quotations from evaluated agents.
Use the check when its signal appears; record the actual rule or evidence that
settles the outcome rather than assuming the example describes the product.

| Notice | Why and test | Bad example → good example | Boundary |
|---|---|---|---|
| Personas agree on a failure | Agreement can share a model assumption. Trace the finding to source evidence and name a product or real-user check. | “Users cannot finish” → “Simulated users stalled at tick 4; reproduce that action on the product.” | Actual observed research can support a stronger claim, with its evidence. |
| One person knows a private fact | Omniscient briefs change behavior. Compare each brief with that person's visible events. | Give everyone the client's private note → include it only for its recipient. | Share it after a recorded disclosure that the other person can observe. |
| Two people edit the same field | Arrival order can invent product semantics. Check the recorded collision rule. | Last model reply wins → apply the supported rule, or preserve an unresolved outcome. | Arrival order matters only when the product rule says it does. |
| A tick resumes after a crash | Replaying an effect can change the journey. Read its commit identity and recorded outcome. | Apply accepted edits again after commit → reuse the committed result; resolve accepted decisions once if not committed. | Unclear commit status must be reconciled before advancing. |

Validation: the outcome cites an applicable rule or remains unresolved; examples
do not supply missing product rules, evidence, disclosure events, or commit proof.

## Verify the method

Use bounded fresh scenarios before claiming instruction behavior works. Freeze
candidate/reference digests, scenario inputs, permitted effects, and a finite
trial budget. Review raw outputs separately from structural/link checks.

Cover explicit and inferred method routing, ordinary static research and CLI UX
negative cases, one decision per person, visibility limits, and unavailable
models. Include a three-person agency rehearsal: two editors choose competing
project edits while a viewer attempts an edit. Check the recorded collision and
permission rules, then confirm the next tick sees their actual outcomes without
learning private information. Also rehearse a missing response, retry exhaustion,
and resumption both before and after the tick commits.

Completion: checks distinguish structural validity, bounded instruction behavior,
and actual provider/product integration. A rehearsal does not launch or qualify
the full 1,500-decision experiment. Preserve failed checks and remaining gaps.
