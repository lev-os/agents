# Orch behavioral trials

The installed skill retains bare/auto/once/watch and passed its forward
feedback campaign. The user rejected restoring the previous feature set.
Every observed failure was preserved, diagnosed and followed by a revised
candidate before retesting. Current evidence is in FEEDBACK-ITERATIONS.yaml
and the orch-feedback-iterate-20260913 campaign.
ENTRY-RESULTS.md records the earlier failed campaign and historical rollback.

Installed g019 passed all 18 current-campaign cases and their transport audits:
eight invocation cases and ten core regressions. All 33 local tests passed.
The campaign used 58 of 70 authorized calls, retaining 14 failures from earlier
revisions. No earlier-subject result counts toward final qualification. Two
runner generations are combined only after proving their bytes differ solely
in the authorized-cap tuple; scenario and acceptance logic are identical.
See runs/feedback-current-summary.json for every attempt. This qualifies the
restricted sample environment, not production schedulers or unrestricted shell.

Reproduce the final evidence summary:

```sh
python3 evals/summarize_campaign.py ~/.local/state/lev/evals/orch-feedback-iterate-20260913/campaign.json --compatible-evaluator evals/runs/e007/run_trials.py --output evals/runs/feedback-current-summary.json
```

The earlier g005 candidate passed 20/20 live Claude Haiku 4.5 trials: two fresh sessions
for each of ten scenarios. Scope is the restricted sample-project environment.
Deterministic CLI tests are separate. `skill-builder/bin/flow eval` remains an
untouched declaration stub. This does not qualify unrestricted shell access,
native FlowMind, real schedulers or provider rotation. See [the incident](INCIDENT.md).

## Run

```sh
python3 evals/test_state_contract.py
python3 evals/test_agent_grader.py
python3 evals/test_trial_boundary.py
python3 evals/run_trials.py --case explore_repair --arm baseline
python3 evals/run_trials.py --case explore_repair --arm candidate
```

The cases and repeat policy are in `../eval.yaml`. Use `--prepare-only` to
create a disposable project without calling a model. Projects and raw receipts
live under `~/.local/state/lev/evals/orch/`; no worktree is created. Each trial
has a unique session, pinned skill/evaluator/fixture hashes, command, full
stream, stderr, final output, process handle and controller measurements.

The host fixture exposes workers and a timer registry through scoped MCP tools.
Those services are synthetic; job artifacts and Python verifiers are real.
`explore_repair` requires the agent to inspect and fix a real shared function.
Other cases test collection, dependencies, verification, continued independent
work, cancellation, and closeout. Fixture operation order is not enforced by
the host; the grader rejects invalid trajectories after they occur.

The grader has positive and deliberately bad controls, including premature
archive, premature acceptance, wrong dependency order, parent-only stop,
duplicate dispatch, missing pages, and lost user work. These controls validate
the grader; they are never counted as agent results. No rubric or expected
answer is included in the agent prompt. File access is constrained by the MCP
adapter; job execution and controller regression checks use macOS sandbox-exec.
Seven boundary tests exercise actual blocked effects. The provider itself still
uses the existing authenticated account; this is not whole-machine isolation.

Run baseline and candidate arms in fresh contexts; record any global skill
auto-loading as possible contamination. Pin one evaluator generation during
skill repair. Change evaluator and subject in separate attempts. Retain failed
trials. An authentication error, timeout, wrong model, or missing result is an
infrastructure error, never a skill pass or a behavioral failure.

The runner removes the machine's `ANTHROPIC_DEFAULT_HAIKU_MODEL` override from
its child environment and checks observed model IDs. It does not change global
settings or rotate accounts. The user restored login before the live runs.

## Current iteration

Generation g000 was preserved before repair. Its state-contract tests fail on
global blocking, unresolved-decision completion, missing dependency enforcement,
state overwrite, terminal restart, malformed input, and duplicate observation
handling. Generation g001 fixes those behaviors and sharpens the skill's
branch-local hold, collection and closeout rules. Twelve frozen state-contract
tests pass. The grader's seven test methods cover ten good trajectories and
multiple corrupt trajectories. Five of twenty allowed subject revisions were
used. Under the final evaluator, g003 passed 6/10, g004 passed 9/10, and g005
passed 20/20 across two full passes. Earlier failures remain preserved, including
the unsafe broad process-kill attempt under the abandoned shell profile.

Evaluator generation e002 removes the target skill from baseline project files,
allows equivalent non-complete status wording, and takes controller verifier
commands only from frozen evaluator code. Snapshot filenames are
`skill.snapshot.txt`, so historical candidates cannot appear in the installed
skill catalog. Older prepared projects remain evidence of preparation only;
fresh trials use the current evaluator digest.

e003 introduced the restricted MCP transport and sandboxed jobs. e004 accepts a
completed shutdown task when actual worker/timer state proves cancellation,
rather than requiring one exact status word. The scenario effect checks remained
frozen during g004 and g005 repair. The independent transport audit verifies
successful delivery of exact skill/project bytes, source hashes, model identity,
fixture and MCP generation, and absence of unscoped tool use on all final trials.

Generate the complete evidence index with:

```sh
python3 evals/summarize.py --output evals/runs/current-summary.json
python3 evals/audit_receipts.py > evals/runs/current-transport-audit.json
```

The summary retains every failed and interrupted attempt. It requires two passes
per case on the current subject and evaluator and rejects any failure in that
generation; it never selects only the best two runs. Snapshot files are named
skill.snapshot.txt so they cannot register duplicate installed skills.
