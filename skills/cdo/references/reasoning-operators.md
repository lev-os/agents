---
name: cdo-reasoning-operators
description: modes modifier. Reasoning modes as bounded operators, with an independent claim audit before synthesis.
---

# Reasoning Operators (`modes` modifier)

Method source: the modes-of-reasoning-project-analysis skill from
jeffreys-skills.md. Its text is not copied here; this leaf states the method in
CDO terms.

Use when a decision needs several genuinely different kinds of reasoning, or
when an ordinary review is likely to miss an assumption. A mode is an operator
that transforms one pivotal question. It is not a persona, a quota or a side
in a debate.

## Rules

- **Decision first.** Before any dispatch, write the decision contract: the question, who decides and why, the time horizon, scope and exclusions, what would make the analysis useful, which kinds of error cost most, real constraints, and which choices are still cheap to reverse.
- **Neutral case file.** Turn 0 records the evidence under stable IDs, kept apart by kind: artifact facts, executions, owner statements, external sources, derivations, inferences and unknowns. The lead's own thesis stays out of it.
- **Seats by information value.** An operator gets a seat only when a plausible answer to its question could change the decision. Most runs start with one broad mapping pass and a few operators aimed at specific questions. Each operator card names the pivotal question, the evidence it may read, its permitted operation, its valid output, how it tends to overreach, what a competent null looks like, and who consumes the result.
- **Read-only passes.** Operator passes analyze. They do not change product code, tests, fixtures, specs or the target branch. A reproduction that needs edits runs in a scratch copy or worktree and keeps its diff and command. Product changes wait until the user asks to act.
- **Nudge on integrity, not output.** Step in when an agent is stuck, asserts facts it cannot support, uses its mode as a verdict, fills fields with invented content, weakens tests or scope, or keeps going after its question is settled. Re-anchor it on its pivotal question and the evidence rule. Never ask it for more findings, more criticism or a minimum count.
- **Nulls count.** Each pass opens with one status line: material increment, no material increment, or blocked by missing evidence. A checked "nothing new" is a successful pass.
- **Claims are the unit.** Synthesis first breaks raw passes into atomic claims with IDs and evidence links, separates observation from inference, value and action, and merges duplicates without raising confidence.
- **No self-certification.** A fresh auditor, never the author, sets each material claim's status: verified, partially supported, hypothesis, rejected, duplicate, non-material or superseded. Claims about runtime, performance or reachability need a focused execution where feasible; a text search does not prove dynamic behavior.
- **Conflict only after audit.** Two claims conflict only when both survived audit, concern the same proposition at the same scope, and cannot both hold. Most apparent conflicts are different questions, scopes or values; remove them. For a real conflict that matters, run one bounded step on the deciding premise. Never vote.
- **Bounded long shots.** Keep at most the configured number of low-confidence, high-upside ideas. Each needs a mechanism, disconfirmers, a cheap test, and thresholds to promote or retire it.
- **No quotas.** Require no minimum count of findings, disagreements, ideas or recommendations. Agreement is a valid outcome. A challenge without evidence is rejected; it is not kept for balance.
- **Value test before more process.** Before adding an operator, a round or an artifact, name the uncertainty it reduces and the decision it could change. Stop when the pivotal questions are settled enough for the cost of error, when only unavailable evidence or owner authority remains, or when the next pass would repeat a method.
- **Hard breakers.** A fabricated source, command or result; a weakened test or narrowed scope; status won through votes or labels; process work that outgrows the object-level work; orchestration artifacts that outrank the evidence and the decision. On a breaker, quarantine the affected claims, return to the last trustworthy state, and continue the object-level work.

## CDO mapping

| Method element | CDO seat or step |
|---|---|
| Decision contract and neutral case file | Turn 0 research (`t0-research.md`) |
| Operator passes | Turn agents with one pivotal question each, isolated as usual |
| Claim normalization and audit | Synthesis runs a normalizer and then a fresh auditor before it writes the directive |
| Conflict detection | The directive's `tensions`, for audited claims only |
| Decision report | FINAL.md: bottom line; verified findings; pivotal unknowns; audited recommendations and experiments; real conflicts and value tradeoffs; rejected tempting claims; bounded long shots; evidence and provenance; limits of the analysis |

With `judge`, the audited claims are the evidence the judge reads. The
anti-groupthink devil's advocate still runs at more than 70% agreement, as an
operator that must attack with evidence and may return a checked null.

Inside Leviathan, `cdo modes-analysis` runs the plugin profile
`cdo.modes-project-analysis`. Read its synthesis_gate before the run. If the
gate demands a minimum count of findings, do not manufacture findings to pass
it. Report the shortfall and treat the gate as a follow-up for `plugins/cdo`
under the Safe skill update pattern.

## When the user asks to act

Turn audited recommendations into tracked work (`bd`, or `/work`). Each item cites
its claim IDs, the condition that would reverse it, and its acceptance test. Keep
immediate changes apart from experiments that gather evidence. Keep important
negative evidence. After the change, record whether the expected effect held.
