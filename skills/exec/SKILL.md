---
name: exec
description: Use when executing a plan, dispatching `lev exec` flows, comparing architecture reviews, or turning proposal lists into reviewed implementation work in the current session.
skill_type: workflow
category: execution
---

# /exec

One skill, one contract:
- extract the task list before acting
- create `TodoWrite` entries for the full slice
- try `lev exec` first only after verifying the surface actually supports the invocation
- enforce Lev DNA for FlowMind, plugin, scheduler, and runtime-steering work
- review spec compliance before code quality, then run one final verifier pass

```yaml
steps:
  - id: read_plan
    action: Read the plan and build the task list
    instruction: |
      Read the plan once. Extract each task with:
      - id
      - title
      - requirement text
      - write scope
      - dependency note
      - verifier command or manual verification note

      Create `TodoWrite` entries for all extracted tasks before execution.

      If the artifact is not a real plan or does not define task boundaries, stop
      and route to `writing-plans`.
    validation: "TodoWrite contains every extracted task and each task has a write-scope note plus dependency note."
    on_failure: "Do not execute. Missing task boundaries means the artifact is not execution-ready."

  - id: classify_work
    action: Classify independence and execution surface
    instruction: |
      For each task, assign both labels:

      `independence`:
      - `parallel_safe` = disjoint write scope, no ordered dependency
      - `serial_only` = shared files, ordered dependency, or shared mutable state

      `surface`:
      - `lev_exec_first` = bounded prompt + verifier + known flow surface
      - `subagent_required` = custom context curation, heavy back-and-forth, or unclear verifier

      Default to `lev_exec_first` only when you can name the verifier and the flow
      surface is known to work.
    validation: "Every task has both an independence label and a surface label."
    on_failure: "If independence or verifier is unclear, force serial execution and/or downgrade to subagent."

  - id: verify_lev_exec_surface
    action: Verify the `lev exec` surface before using it
    instruction: |
      Before you write a `lev exec` command:
      1. Run `lev exec --help`
      2. Confirm the flow file exists
      3. Confirm the command shape is supported by the current CLI

      Never invent flags. If the CLI does not support the argument passing pattern
      you want, downgrade to subagent mode and record the reason.

      Known failure patterns to avoid:
      - invented knob flags
      - assuming a flow name maps cleanly to CLI without checking
      - assuming `ralph --max-iterations=10` expands 10 proposal items by itself

      For the 10× Ralph pattern, use an outer controller loop. One successful Ralph
      run produces one proposal item, not the full list.
    validation: "Every `lev exec` use was preceded by a verified command shape, or downgraded with an explicit reason."
    on_failure: "Do not run guessed CLI syntax."

  - id: enforce_lev_contracts
    action: Load Lev contracts for FlowMind and plugin work
    instruction: |
      If the task touches FlowMind, plugin config, daemon scheduling, runtime
      steering, context injection, protocols, or graph control flow, load:
      - `dna/graph.yaml`
      - `.lev/validation-gates.yaml`
      - relevant design/spec docs for the touched module

      Then force this checklist into the plan:
      - `LevEvent` lifecycle emission at meaningful boundaries
      - trace context propagation (`trace_id`, parent/child lineage)
      - structured logging, not prose-only logs
      - bounded budgets, retry policy, and timeout policy (C1)
      - append-only receipts / no silent mutation (C2)
      - explicit scope and permissions (C5)
      - structured input/output schemas when the node exchanges machine data
      - resumability and idempotency notes for scheduled or retryable work
      - scheduling through the project scheduler, not a bespoke scheduler
      - protocol and config resolution through the fractal chain, not globals
    validation: "FlowMind/plugin tasks carry explicit notes for eventing, tracing, logging, budgets, retries, resumability, idempotency, and resolution order."
    on_failure: "Do not treat FlowMind/plugin work as ordinary coding. Add the missing runtime contract notes first."

  - id: choose_flow
    action: Map the task to the right flow or fallback
    instruction: |
      Use this routing table:

      | Situation | Surface |
      |-----------|---------|
      | DNA-first compile / validate / cascade | `lev dna ...` first |
      | bounded implementation + verifier | `lev exec --flow ralph` |
      | bounded implementation + reviewer loop | `lev exec --flow lev-ralph` |
      | architecture trade-offs | `arch-interview` if CLI shape verified, else read-only subagent |
      | multi-perspective evaluation | `cdo-standard` if CLI shape verified, else read-only subagent |
      | high-stakes multi-wave review | `cdo-bonsai-50` |
      | no clean verifier or bespoke context | fresh subagent |

      For compare tasks:
      - normalize outputs into the same headings
      - compare agreements, tensions, unique additions
      - do not collapse distinct analyses into one blended summary before comparison
    validation: "Each task has a concrete flow choice or an explicit fallback reason."
    on_failure: "Do not hand-wave the execution surface."

  - id: dispatch_batches
    action: Execute in safe batches
    instruction: |
      Batch only `parallel_safe` tasks with disjoint write scopes.
      Rules:
      - maximum 3 implementation tasks at once
      - stop parallelism if tasks touch the same files, contracts, or migration surface
      - do not start the next batch until the current batch clears review

      For `lev_exec_first` tasks, use a bounded prompt:

      ```bash
      lev exec "Implement Task {id}: {title}

      Requirements:
      {requirement}

      Constraints:
      - Touch only: {write_scope}
      - Respect existing docs/contracts
      - Stop when verifier passes

      Done means:
      - {acceptance_criteria}" \
        --until="{verifier}"
      ```

      For subagent tasks, include:
      - full requirement text
      - write scope
      - dependency note
      - required verifier
      - report status: `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`
    validation: "No parallel batch exceeds 3 tasks or overlaps write scopes."
    on_failure: "Collapse to serial execution immediately."

  - id: review_spec_first
    action: Run spec compliance review before quality review
    instruction: |
      After implementation:
      1. Review against the requested behavior
      2. Confirm no extra behavior was added
      3. Confirm write scope was respected
      4. Confirm required runtime contracts were included for FlowMind/plugin work

      Only `APPROVED` tasks proceed to quality review.
    validation: "No task proceeds to code-quality review before spec approval."
    on_failure: "Return to the same execution surface for fixes."

  - id: review_quality_second
    action: Run code quality review after spec passes
    instruction: |
      Review for:
      - clarity of interfaces
      - maintainability
      - test quality
      - unnecessary complexity
      - obvious correctness risks

      Quality review is not optional and does not replace the verifier.
    validation: "Every completed task has both spec approval and quality approval."
    on_failure: "Do not mark the task done."

  - id: final_verify
    action: Finish with one final verifier pass
    instruction: |
      Before claiming completion:
      - run the declared verifier commands
      - check for unexpected changed files
      - update TodoWrite to reflect reviewed state, not just implemented state
      - if the work created a reusable artifact, install/activate it only after the checks pass
    validation: "All declared verifiers pass and TodoWrite matches the reviewed state."
    on_failure: "Return to the failing task or failing batch."
```

## Lev-Specific Guardrails

- `lev exec` is first choice only when the surface is verified, not guessed.
- For DNA-first work, prefer the repo DNA surface (`lev dna compile|validate|cascade`) before falling back to direct `lev exec --dna` or guessed cascade invocations.
- For FlowMind/plugin/runtime work, eventing and trace are part of done.
- Use the project scheduler (`.schedule.yaml`, cron-tick-provider) instead of inventing a second scheduler.
- Put content and steering in protocols/config registries; flows schedule behavior.
- Use structured schemas for machine-readable node outputs.
- For resumable work, define checkpoint boundaries and idempotency keys up front.

## Quick Routing Table

| Need | Preferred surface |
|------|-------------------|
| execute a real plan | this skill + `TodoWrite` + verified `lev exec` / subagents |
| architecture interview | `arch-interview` if CLI shape verified |
| compare architecture passes | run both surfaces, normalize headings, compare deltas |
| expand 5 amendments into 10 proposals | outer loop controller + one Ralph item per success |
| FlowMind/plugin design | load DNA + validation gates + design docs before dispatch |

## Red Flags

- “Just ship the skill.”
- “We don’t need all the checks.”
- “FlowMind plugin is probably fine; skip DNA.”
- “Just make a scheduler.”
- “I’d use `lev exec` only where it clearly matches an existing flow or program.”
- “Smallest relevant checks.”
- “Assume the names map to invocable flows in the user’s environment.”
- “Delta summary + matrix instead of fully merging long outputs.”
- “I’d pick the smallest integration that already fits FlowMind.”
- “I’d defer advanced distributed sagas.”

If you hear one of those thoughts, stop and re-check the surface, verifier, and Lev contract notes.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| “Just ship the skill.” | Shipping still requires task extraction, verifiers, and reviewed state. Speed comes from narrowing scope, not deleting gates. |
| “We don’t need all the checks.” | The declared verifier and review order are mandatory. Remove scope, not safeguards. |
| “FlowMind plugin is probably fine; skip DNA.” | FlowMind/plugin work must load DNA and validation gates, then carry explicit runtime contract notes. |
| “Just make a scheduler.” | Use the project scheduler and schedule files. Do not create a second scheduler in plugin code. |
| “I’d use `lev exec` only where it clearly matches an existing flow or program.” | Verify the surface. If it matches, use it first. If it does not, downgrade explicitly. |
| “Smallest relevant checks.” | The declared verifier is mandatory, not optional. |
| “Assume the names map to invocable flows in the user’s environment.” | Flow names and flags must be checked against the actual CLI. |
| “Delta summary + matrix instead of fully merging long outputs.” | Compare first, but keep both raw outputs readable until the user’s comparison need is satisfied. |
| “I’d pick the smallest integration that already fits FlowMind.” | Smallest is fine only if it still satisfies DNA: LevEvent, trace, budgets, retries, resumability, idempotency. |
| “I’d defer advanced distributed sagas.” | Deferral is fine, but resumability and idempotency still need an explicit target-state note. |
