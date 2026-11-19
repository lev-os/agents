# Tests: the checklist for a new, changed or audited test

The review skill loads this file for any test work: a new or changed test, a test
review, or a sweep of a test suite. It was the `test-audit` skill (Peter
Steinberger, OpenClaw, MIT, commit 70bfdc2b58; provenance in
[tests-upstream/upstream.yaml](tests-upstream/upstream.yaml)). It moved here on
2026-11-18 (JP: "1 yes"); there is no other copy. A project that plans where
each test runs (in Leviathan: the `lev-test-stages` skill) points here and keeps
only its stage table.

- Every new or changed test passes the [authoring gate](#authoring-gate).
- An audit removes low-value proof in coherent owner batches; never chase deletion counts.
- A whole-subsystem sweep: read [tests-campaign.md](tests-campaign.md) first.

## Authoring gate

Before you add a test, answer:

1. Which observable behaviour, invariant or independent contract does it protect?
2. Which credible regression makes it fail?
3. Why does existing proof miss it? Each contract has one primary owner at its
   strongest boundary. Another layer needs a distinct transport or lifecycle risk.
   Extend tables and shared fixtures; consolidate repeated setup.
4. Does it need an export, flag, wrapper or injection hook with no production
   caller? Then move the proof to the real boundary.

- Use the [boundary and cost guide](tests-upstream/writing-tests.md).
- A regression test fails before the fix for the intended reason and passes
  after the repair; report when no baseline proof was available.
- One owner regression covers a bug; never replay it at every crossed layer.
- A behaviour-preserving refactor does not break a good test.

## Junk patterns

Reject a new match unless the [retention bar](#retention-bar) names an
independent contract. Audit existing matches.

What the test proves:

- Assertion-free probes, self-comparisons, identity copiers, expected values the
  subject generated.
- Copied inventories, manifests and export lists; exact source, import or string greps.
- Private predicate or call-shape tests that repeat boundary proof; repeated
  invocations or provider-local replays of shared helpers.
- Test-only exports, globals and wrappers; production paths only tests call.
- Mocks that implement the asserted behaviour, or pretend distinct APIs match.
- Fixtures that supply receipts, admission or callback order the owner should
  produce; persistence asserted against a store path the code never writes.
- Capability flags asserted instead of the promised delivery or acknowledgement.
- Negative controls that pass on an unrelated guard or an unreachable rejection.
- Names that promise behaviour the inputs or assertions never exercise.

How the test waits and what it fakes (a lint rule can catch these; prior art:
`@interfere/landmines`, MIT, rules `no-test-doubles`, `no-fixed-sleep`,
`no-unsignaled-poll`, `no-flake-masking`, `strict-msw`):

- A dependency's behaviour replaced (module mocks, a stub with an
  implementation, patched globals or prototypes) where the real code can run.
  Fake only the network, at its edge, with unhandled requests failing.
  Observation-only spies are fine.
- A fixed real-time sleep. Await the operation, or a signal it emits.
- Polling a spy or a request recorder against a deadline. Await the event.
- A raised timeout or a retry. A test that passes on rerun is a flake to fix.

## Retention bar

- Keep independent public API, SDK, protocol, config, migration, storage,
  security, platform, default, prompt-byte, generated cross-language, package,
  release and architecture contracts. Keep observable ordering and credible
  regressions. Static or slow is not a reason to delete.
- Source inspection is valid when it is the cheapest independent guard of a
  user-facing key, byte or path, and it survives an identifier-only refactor.
- A check that a removed name or path stays gone is a guard, not a test of
  removed code. Keep it, or move it into the project's guard of removed names
  (in Leviathan: `tooling/scripts/check-no-compat-paths.mjs`). Never just delete it.
- A spy can be the cheapest guard of a config default no output shows. A
  call-shape assertion is junk only when a cheaper observable guard exists.
- A baseline failure may be a product bug: reproduce and repair the owner;
  never delete the test for it.

## Candidate evidence

- Before an edit, read the full test, the production owner, its entry point,
  callers, callees, siblings, overlapping proof, CI routing and history. For a
  claim that rests on a dependency, read the dependency's source or types. Read
  the root and folder instructions.
- Record for each candidate:
  - Exact name and location, and the failure it can detect.
  - Non-test callers of the covered production or support seam.
  - The stronger remaining owner proof, or why none is needed.
  - The history or reason it exists, and the deletion it unlocks.
  - The risk, and a focused validation command.
- Missing evidence: no deletion. Discovery is read-only; report before edits.
  Prefer a few high-confidence candidates. Parallel discovery may split
  independent owners.
- Delete obsolete seams and dead paths with their tests; move retained
  regressions to their owner; consolidate generic package or dependency contracts.
- Prefer net-negative production lines. Never add replacement implementation
  tests, and never turn uncertainty into cleanup.

## Validation and handoff

- Follow the project's proof policy (OpenClaw's is in
  [tests-upstream/openclaw-testing-SKILL.md](tests-upstream/openclaw-testing-SKILL.md#proof-policy);
  in Leviathan: `AGENTS.md` section 1, rules 3 and 4). Never edit the checkout
  during an active test run. Run the owner and sibling tests.
- Removed source greps or plan assertions: exercise the owning executable or dry run.
- Run the targeted format check and `git diff --check`. Run the project's
  changed-files gate and its dead-code checks before a removal batch lands:
  removed tests orphan support files and exports that ordinary CI misses.
  (OpenClaw's commands, `scripts/check-changed.mjs` and `pnpm deadcode:*`, are
  examples; use the project's own.)
- Inspect `git diff --numstat`; get a final review from a fresh reader.
- Report causes, removed categories and seams, retained false positives,
  proof and cost, production versus test lines, follow-ups.
- Commit, push or land only with task authority. Refresh from main and
  rediscover before another audit batch.
