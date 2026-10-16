# Long-Horizon Planning and Execution

Use this reference for multi-stage or multi-session work, long autonomous runs,
or a request to use Horizon within planning. It connects existing owners; it
adds no mode, command, task field, scheduler or runtime implementation.

## Plan the whole outcome

Read [Horizon](../../horizon/SKILL.md) as the planning method, including its
conditional worker-contract and long-run reference when applicable. Apply its
workflow to the current plan; when Horizon's Fit Check names lev-plan for work
already in this workflow, continue the selected mode instead of routing again.
Keep one plan, one slice map and the existing requirements ledger. Put the
completion predicate, excluded near misses, review and bounded repair rules,
stage exits, open branches and resume frontier in that plan, citing requirement
IDs rather than creating a second executable ledger.

Each slice names outcome, owner, dependencies, covered intent IDs, allowed
effects, artifact, proof and stop condition. For every command check, name its
known-bad control, the owner that will run it and the sensitivity evidence
required before accepting the check. Human or external-owner claims retain
their named acceptance owner; missing proof remains unresolved.

Use [Lev's rolling-horizon procedure](../../lev/references/recursive.md) when
projecting the route: detail ready near work and keep later dependencies and
uncertainties visible. [Worker contracts](../../horizon/references/task-brief.md)
are required for any delegated stage. Keep later slices in the map until their
inputs and decisions support an executable packet. Planning-only Compile,
Deepen, Review and Map requests stop at their requested artifact.

## Run the authorized effort

When the user authorizes delivery, hand the same plan, tracker, current frontier,
effect scope, limits and evidence to [Orch](../../orch/SKILL.md). Its mode and
branch-authority rules still apply; planning grants no additional effects.
The controller coordinates these owners without asking the caller to move
between skills:

1. **Select.** Reload the bound tracker, plan, current source/dependency revisions
   and accepted evidence. Choose one coherent dependency-ready unit. Route an
   unresolved decision to its owner; continue other independent authorized work.
2. **Prepare.** For coding or a selected SDLC overlay, use lev-plan Emit and
   [Execution Packet](execution-packet.md) to create or refresh exactly one
   existing-contract task packet. Validate before dispatch. Reuse a current
   packet; regenerate stale inputs. Non-coding uses its domain execution
   contract without a mandatory SDLC packet.
3. **Execute, verify, accept.** Use [Exec](../../exec/SKILL.md) or the domain
   owner within the permitted scope. Record the actual worker handle and
   artifacts. Run the declared verifier, including known-bad sensitivity checks
   before relying on command checks. core/eval decides command rows; review and
   named acceptance owners answer their rows. Accept only after the required
   current evidence passes. A dispatch, preview or worker report is not acceptance.
4. **Repair or advance.** Recall blocking failures to their responsible stage
   with failed row IDs, evidence, narrowed scope, acceptance and retry cap.
   Preserve failed attempts. Invalidate affected downstream acceptance after a
   changed or failed input; unrelated ready branches can continue. Update the
   bound tracker through its owner and the plan's evidence/resume projection.
   Continue with the next ready unit only within the authorized scope and budget.

In the existing project report, summarize each actual worker call: handle,
role, bounded ask, artifact, status and independently verified evidence. For
parallel search only, Orch also maintains the idea-keyed approach registry,
falsified hypotheses, blocked routes and reopening evidence in the existing
acceptance map or its owner-managed state. The brief states the policy and
points to that state; it is not a second changing tracker.

## Return and resume

Completing a slice advances the frontier; it does not complete the effort.
Return complete only when the whole predicate and all required rows have fresh
accepted evidence and no blocking finding remains. A branch's repair cap,
missing authority or unavailable evidence holds that branch and its affected
consumers; continue independent authorized ready work. Return the whole effort
at a global user stop or exhausted budget, the selected mode's boundary, or
when no eligible work remains. If any required branch is unresolved, label that
return incomplete with the strongest verified result, exact gaps and owners.
Do not turn an unavailable execution surface into a prose claim that the loop ran.

Save the last accepted stage and evidence, exact source/task/worker revisions,
open requirements and decisions, invalidated dependents, remaining limits and
one next ready unit in existing owner-managed state and its Markdown handoff.
On resume, recheck evidence freshness before choosing that unit. Runtime state
uses its existing JSON contract; no new parallel tracker or status file is added.
