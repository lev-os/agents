---
name: subagent-driven-development
description: Use when executing an implementation plan in the current session, trying lev exec first, parallelizing independent tasks when safe, and falling back to fresh subagents with spec/code review gates.
skill_type: workflow
category: execution
---

# Subagent-Driven Development

One skill, one contract:
- try `lev exec` first
- parallelize only when tasks are independent
- fall back to fresh subagents when `lev exec` is not the right execution surface
- never skip spec compliance review or code quality review

```yaml
steps:
  - id: read_plan
    action: Read the plan and build the task list
    instruction: |
      Read the plan once. Extract every task with:
      - task id
      - full requirement text
      - acceptance criteria
      - write scope
      - dependencies

      Create TodoWrite entries for all tasks before starting execution.

      If the plan does not define clear tasks, stop and ask for a better plan
      or route to `writing-plans`.
    validation: "TodoWrite contains all extracted tasks and each task has a write scope and dependency note."
    on_failure: "Do not execute. Missing task boundaries means the plan is not ready."

  - id: classify_tasks
    action: Classify tasks by independence and execution surface
    instruction: |
      For each task, classify:

      `independence`:
      - `parallel_safe` = disjoint write scope, no ordered dependency
      - `serial_only` = shared files, shared mutable state, or ordered dependency

      `execution_surface`:
      - `lev_exec_first` = can be expressed as a bounded implementation prompt with a verifier
      - `subagent_required` = needs heavy back-and-forth, custom context curation, or bespoke review handling

      Default to `lev_exec_first` unless there is a concrete reason not to.

      Never mark tasks as parallel-safe if they touch the same file set.
    validation: "Every task has both an independence label and an execution_surface label."
    on_failure: "If task independence is unclear, force serial execution."

  - id: try_lev_exec_first
    action: Use lev exec as the default execution substrate
    instruction: |
      For every task labeled `lev_exec_first`, attempt execution through `lev exec`
      before using subagents.

      Preferred order:
      1. `lev exec` with verifier / validation gate
      2. fresh subagent implementer

      Example prompt shape:

      ```bash
      lev exec "Implement Task {id}: {title}

      Requirements:
      {full requirement text}

      Constraints:
      - Touch only: {write scope}
      - Do not change unrelated files
      - Stop when verifier passes

      Done means:
      - {acceptance criteria}" \
        --until="{verification command}"
      ```

      If `lev exec` produces a valid result, continue to review.
      If `lev exec` is blocked, loops pointlessly, or cannot represent the task
      cleanly, fall back to subagent mode for that task.
    validation: "Each lev_exec_first task was either attempted with lev exec or explicitly downgraded with a reason."
    on_failure: "If lev exec is unavailable or unsuitable, record the reason and continue via subagent mode."

  - id: run_parallel_batches
    action: Execute independent tasks in bounded parallel batches
    instruction: |
      If 2 or more tasks are `parallel_safe`, batch them.

      Parallel batch rules:
      - maximum 3 implementation tasks at once
      - every task in the batch must have disjoint write scope
      - if one task mutates shared infra or contracts, stop parallelism and serialize

      Batch preference:
      - use parallel `lev exec` tasks first when tasks are simple and verifier-driven
      - use parallel subagent implementers when the tasks need richer context

      Do not start the next batch until the current batch has cleared review.
    validation: "No parallel batch contains overlapping write scopes and no batch exceeds 3 tasks."
    on_failure: "Collapse the batch to serial execution immediately."

  - id: implement_with_subagent
    action: Fall back to fresh subagent implementers when needed
    instruction: |
      Use a fresh implementer subagent when:
      - lev exec is not the right fit
      - the task needs richer context than a bounded lev exec prompt
      - the task needs interactive clarification while implementing

      Implementer brief template:

      ```text
      Implement Task {id}: {title}

      Full task:
      {full requirement text}

      Context:
      {scene-setting, dependencies, architectural fit}

      Constraints:
      - Touch only: {write scope}
      - Ask questions before guessing
      - Report DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED

      Before reporting done:
      - run tests / verifier
      - self-review
      - list changed files
      ```

      Reuse the same implementer for fixes on the same task. Use a fresh
      implementer for a different task.
    validation: "Every subagent task has a concrete brief with full requirement text, write scope, and report status."
    on_failure: "Do not send vague 'fix this' prompts. Rebuild the brief."

  - id: review_spec_first
    action: Run spec compliance review before code quality review
    instruction: |
      After implementation succeeds, run spec compliance review first.

      Spec reviewer checklist:
      - Did the task implement everything requested?
      - Did it add anything not requested?
      - Did it solve the correct problem?
      - Are the changed files within the allowed write scope?

      Review output must be:
      - `APPROVED`
      - or `REJECTED` with exact missing/extra items

      If rejected, send the task back to the same execution surface:
      - lev exec fix-up if the task was cleanly verifier-driven
      - same implementer subagent otherwise
    validation: "No task proceeds to code-quality review before spec review is APPROVED."
    on_failure: "Return to implementation. Never skip the spec gate."

  - id: review_quality_second
    action: Run code quality review after spec compliance passes
    instruction: |
      After spec approval, run a code quality review.

      Quality reviewer checks:
      - clarity of names and interfaces
      - maintainability
      - test quality
      - unnecessary complexity
      - obvious correctness risks

      Review output must be:
      - `APPROVED`
      - or `REJECTED` with concrete issues

      If rejected, send the task back for fixes, then re-run quality review.
    validation: "Every completed task has both spec approval and quality approval."
    on_failure: "Do not mark the task done."

  - id: serial_vs_parallel_merge
    action: Merge reviewed tasks back into the session safely
    instruction: |
      After a serial task or a parallel batch clears review:
      - mark TodoWrite complete
      - refresh local context
      - check for merge conflicts or overlapping edits

      If a parallel batch produced conflicting edits:
      - stop
      - reconcile manually
      - re-run review on the reconciled result
    validation: "TodoWrite reflects the real reviewed state, not just implementation state."
    on_failure: "Reconcile conflicts before starting new work."

  - id: finish_with_final_review
    action: Finish with one final review pass
    instruction: |
      After all tasks are complete, run one final review over the whole slice.

      Final review checks:
      - all task requirements satisfied
      - no open review issues
      - no unexpected changed files
      - verifier commands pass

      Then use `finishing-a-development-branch` if the user wants integration guidance.
    validation: "The whole implementation slice has a final approval pass."
    on_failure: "Return to the failing task or failing batch."
```

## Execution Rules

- Try `lev exec` first when the task can be expressed as a bounded prompt plus verifier.
- Use subagents when the task needs richer context or interactive clarification.
- Parallelize only independent tasks with disjoint write scopes.
- Maximum parallel batch size: `3`.
- Review order is fixed:
  1. spec compliance
  2. code quality
- Never start code-quality review before spec review passes.

## Status Meanings

- `DONE` = implemented and verified
- `DONE_WITH_CONCERNS` = implemented, but doubts remain
- `NEEDS_CONTEXT` = missing information
- `BLOCKED` = cannot proceed without changing the plan or execution mode

## Red Flags

| Excuse | Reality |
|--------|---------|
| "I'll just spawn all implementers in parallel" | Shared write scope means conflict. Parallel is only for disjoint tasks. |
| "lev exec is optional" | It is first choice when the task is verifier-driven. Try it first. |
| "Spec review can wait until the end" | Wrong order. Spec approval must happen before quality review. |
| "The implementer self-review is enough" | It is not. External review is mandatory. |
| "This task is kind of parallel-safe" | Kind of means no. Serialize it. |

## When Not To Use

- no implementation plan exists
- tasks are tightly coupled and constantly rewrite the same files
- the work needs broad design exploration before execution
- the user wants a separate long-running execution session instead of current-session control
