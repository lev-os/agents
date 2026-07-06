---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks - dispatch coder agents for bounded slices and run reviewer agents on cadence, size, risk triggers, and final integration
---

# Subagent-Driven Development

Execute an implementation plan with fresh coder agents and bounded reviewer agents.

**Core principle:** the controller owns the plan, context, verification, and escalation. Coder agents implement bounded slices until there is a coherent PR-sized batch to review. Reviewer agents do code quality plus spec/drift detection for that batch, not after every slice by default. After all slices are complete, one wider integration reviewer checks that the app/workflow works as a whole.

This skill is project-agnostic. Use the current repository's plans, architecture docs, coding standards, tests, evals, apps, and runtime surfaces as evidence. Do not hand-author proof or certification artifacts; when a project has those concepts, they must be byproducts of real commands or runtime effects.

## Use When

- A plan has multiple independent or mostly independent implementation slices.
- Fresh subagent context helps implementation quality.
- Review should happen at PR-sized checkpoints, with task count, changed-line budget, and risk triggers preventing oversized batches.
- The controller can inspect reports, run verifiers, and keep integration state.

Do not use this for a single small edit, unclear requirements, or tightly coupled work that needs one owner to keep the full implementation in context.

## Files

- `coder-prompt.md` - template for the implementation agent.
- `reviewer-prompt.md` - template for checkpoint review: code quality plus spec/drift detection.
- `final-integration-reviewer-prompt.md` - template for the end-of-slices integration review.

## Controller Loop

1. Read the plan once and extract slices, acceptance criteria, constraints, and verifier commands.
2. Set review cadence before coding starts.
3. Dispatch one coder agent for the next bounded slice.
4. Inspect the coder report, changed files, diffstat, and verifier output.
5. Run declared controller-side gates before review whenever they are available.
6. If a declared gate fails, return to implementation or fix directly before launching a reviewer; do not ask reviewers to approve known-failing batches.
7. Run a reviewer only when gates pass and cadence, changed-line budget, or an immediate trigger fires.
8. Fix checkpoint reviewer findings through a coder agent or directly when the patch is surgical.
9. Continue until all planned slices are implemented or a real blocker stops progress.
10. Run project-level verification and one final integration reviewer over the whole implementation.
11. Close with completed slices, files changed, verifier results, review status, integration status, unresolved risks, and next action.

## Review Cadence

The default review unit is a **meaty PR-sized batch**: as much completed work as can be safely grouped into one coherent pull-request-sized review. Do not review every task by default, and do not keep coding past the point where the batch would be too large to review well.

At the start, the controller sets a batch target:

- Batch goal: the largest coherent feature/fix unit that is still safe and reviewable as one PR-sized chunk.
- Task cap: default 3 completed tasks/slices before review, unless the PR-sized batch is clearly smaller.
- Size cap: default roughly 500 changed lines since the last review.
- Trigger cap: review immediately on any trigger below.
- End cap: run one final integration review after all slices are complete.

Tune the caps to the work: smaller batches for shared/risky code; larger batches for mechanical edits with strong deterministic tests. If a slice alone is PR-sized, review after that slice; if several small slices compose one coherent PR-sized chunk, review them together.

The controller runs declared verifiers before checkpoint review. If those gates
fail, the batch is not ready for approval review. Either fix it directly when
the patch is surgical or send the concrete failure back to a coder. Use a
reviewer on a known-failing batch only when the reviewer is being asked for
diagnosis, not approval.

## Immediate Review Triggers

Run a checkpoint reviewer before continuing when a slice touches:

- Public API, schema, protocol, CLI, config, storage format, migration, or compatibility behavior.
- Security, auth, permissions, secrets, money, deletion, data loss, sandboxing, concurrency, lifecycle, process/session management, or remote execution.
- Cross-package boundaries, dependency direction, generated code, ownership boundaries, or architectural seams.
- More than 5 files, more than 500 changed lines, or a file that is becoming large or unfocused.
- A failed, flaky, skipped, or changed verifier.
- A coder concern, validator concern, unexpected runtime behavior, or uncertainty about whether implementation still matches the plan.

## Reviewer Scope

Checkpoint reviewers only do:

- **Code quality:** correctness, maintainability, simplicity, naming, boundaries, tests, size/complexity, and obvious failure paths.
- **Spec/drift detection:** missing requirements, extra work, behavior drift, public contract drift, architectural drift, and mismatch between coder claims and actual diff.

They do not invent new requirements, run broad architecture redesign, produce certification, or ask for re-review loops. They report blocking evidence and concrete patch recommendations for the PR-sized batch under review.

## Evidence Packet

Give reviewers a compact packet:

```text
Objective:
Completed slices since last review:
Remaining slices:
Batch boundary / why this is PR-sized:
Acceptance criteria:
Risk triggers hit:
Changed files:
Diffstat:
Important file refs/diffs:
Verifier commands and results:
App/runtime smoke or e2e status:
Known concerns/blockers:
Questions for reviewer:
```

Ask for new blocking evidence. Do not ask for generic commentary.

## Review Policy

- `APPROVED`: continue.
- `NEEDS_CHANGES`: fix the concrete findings, verify with commands, and continue; do not spawn an approval loop.
- `BLOCKED`: stop new slices until the blocker is resolved, reduced, or explicitly deferred by the controller.
- `NO_RESULT` or timeout: retry once only with a smaller evidence packet or clearer prompt; if it fails again, escalate.

There is no automatic re-review after every fix. The next scheduled checkpoint or the final integration review validates that prior fixes stayed fixed.

No subagent should run silently past the batch's expected window. The
controller should set a bounded wait for each coder/reviewer based on batch
size, poll or request status when needed, and avoid blocking the whole run on a
stale child. If a coder or reviewer produces no usable result after one retry,
the controller either continues locally when safe or escalates with the exact
blocker.

When the project goal says pass = commit/push, `APPROVED` means the controller
stages only scoped files, follows the repository commit protocol, pushes, and
leaves unrelated dirty work untouched.

Escalate when:

- The same finding appears in two checkpoint reviews.
- Two reviewer attempts produce no usable result.
- Reviewer count exceeds coder count for the current batch without producing new blocking evidence.
- A finding requires changing the plan, architecture, or public contract.

## Final Integration Review

After all planned slices are complete, run one final integration reviewer with the whole evidence packet.

The final reviewer verifies:

- The app/workflow works through the intended user/runtime path.
- Slices are integrated, not just locally green.
- Tests/evals/smokes cover realistic usage and important negative cases.
- Public boundaries are coherent and do not create duplicate implementations or truth stores.
- Code follows repository standards for size, complexity, naming, ownership, and maintainability.

If the app or runtime cannot be exercised, the closeout must say exactly what was not verified.

## Red Flags

Never:

- Review every task by default.
- Let a batch grow beyond PR-sized reviewability just because the task cap has not been reached.
- Split ordinary review into separate spec and quality reviewers.
- Launch approval reviewers before declared controller gates have passed.
- Loop reviewers until approval.
- Treat subagent reports, chat text, generated artifacts, or dashboard text as proof without real verifier/runtime evidence.
- Let coder agents widen scope, rename concepts, or introduce architecture from conversation artifacts.
- Skip final integration review.
- Claim the app works when only isolated unit tests ran.
- Hide skipped, failed, or unavailable verifier commands.

## Completion Report

```text
Completed:
Files changed:
Verification:
Reviews:
Integration status:
Unresolved risks:
Next action:
```
