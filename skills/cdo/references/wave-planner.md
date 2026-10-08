---
name: cdo-wave-planner
description: Plan mode. Plan many waves ahead, attach 1-5 skills per node, judge each wave, amend the plan.
---

# Wave Planner (`plan` modifier)

Use when the user wants waves planned in advance, wants to attach skills to
nodes, or invokes `/cdo plan,...`. Plan mode implies `judge`.

## A plan is a forecast, not a contract

The approved plan proposes each wave. Before a wave runs, the previous synthesis
directive and the judge's unmet criteria may keep, amend or replace it. Record
every change as planned versus actual. CDO stays adaptive, and the user still
sees and shapes the whole run before it starts.

## Flow

```yaml
steps:
  - id: frame
    action: State the goal, the acceptance criteria and the budget before planning anything.
    validation: "Each acceptance criterion is observable. The budget names max_waves (default 5; up to 10, or the user's number), a consecutive no-progress limit (default 2) and, when relevant, a wall-clock limit."
  - id: discover
    action: Run skill discovery for each candidate node focus. Use skill://skill-discovery first (`lev-skills "<broad keywords>" --json --limit=5`), rg over ~/.agents/skills and ~/.agents/skills-db when results are weak, and dispatch/skill-injection.md for weighted workshop skills.
    validation: "Each node lists the skills considered and chosen, and every chosen skill has a local path that exists."
  - id: draft
    action: Draft the waves as a DAG. Each wave has a purpose, the criteria it should move, and nodes; each node has a role, a focus question, inputs, an output file and 1-5 skills.
    validation: "Every node names 1-5 existing skills, and at least one wave targets every acceptance criterion."
  - id: render
    action: Render the Wave Plan dashboard from templates/dashboard.md in the reply itself. Use an embedded visualizer or the user's established renderer when available; otherwise use the Markdown dashboard. A plan that exists only in a file is not rendered.
    validation: "The reply shows every wave, node, skill, criterion, the judge and the budget."
  - id: edit
    action: Offer numbered edits (add or remove waves or nodes, swap skills, change a node's skill count from 1 to 5, change criteria, budget or judge, re-run discovery for a node) and re-render until the user approves.
    validation: "Approval is explicit. Silence is not approval. No wave runs before approval: end the reply after the dashboard and the edit menu."
  - id: freeze
    action: Freeze the acceptance criteria, the budget and the judge, and save the approved plan as tmp/cdo-{session}/plan.yaml.
    validation: "plan.yaml exists with goal, acceptance, budget, judge and waves."
  - id: run_wave
    action: Before each wave, re-run discover for its nodes and apply the previous synthesis directive and the judge's unmet criteria. Then compose, dispatch and synthesize per execute_turns.
    validation: "The wave's artifacts and its synthesis directive exist on disk."
  - id: judge
    action: Dispatch the judge on the frozen criteria (engine/convergence.md, Type 5).
    validation: "The judge returned satisfied or not_satisfied with evidence for each criterion."
  - id: amend
    action: If the judge is not satisfied and budget remains, amend the remaining waves toward the unmet criteria, update the dashboard with planned versus actual, and run the next wave. If the judge is satisfied, or the budget ends, go to synthesize_final.
    validation: "The dashboard shows planned versus actual for every completed wave. A run that ends on budget lists its unmet criteria and does not claim satisfaction."
```

With `hitl`, the user confirms each amended wave. Without `hitl`, show the
dashboard update and continue. With `autoresearch`, the approved plan is the
scheduler's candidate queue; the scheduler still picks each quantum from live
evidence and unmet metrics.

## Plan file

```yaml
plan:
  goal: "<what the run must achieve>"
  acceptance:
    - {id: A1, criterion: "<observable result>", check: "<how the judge verifies it>"}
  budget: {max_waves: 5, max_no_progress_waves: 2, wall_clock: null}
  judge: "fresh judge agent; inside Leviathan, also record the plugin receipt"
  waves:
    - id: W1
      purpose: "<what this wave learns or builds>"
      targets: [A1]
      nodes:
        - {id: W1N1, role: "<role>", focus: "<question>", skills: [skill-a, skill-b], output: t1-<role>.md}
  history: []   # one entry per wave: planned, actual, verdict, unmet
```

## Execution backends

| Where | Backend | Notes |
|---|---|---|
| Inside `digital/leviathan` | Lev plugin: `cdo run` with a profile | Deterministic. On a failed completion_gate, the flow schedules another round, up to max_ticks. Check `plugins/cdo/profiles/` for a profile that carries the wave plan, and read what the completion_gate tests. If no profile carries the plan, keep plan.yaml as the plan and run the Type 5 judge beside the plugin receipt. |
| Claude Code, and the user opted in to workflows | Workflow tool | Load the workflow-authoring skill that the Workflow tool names first. Map each wave to a `phase()`, its nodes to `agent()` calls inside `parallel()`, and the judge to an `agent()` with a schema that returns `{satisfied, unmet}`. Loop in the script while the judge is not satisfied and budget remains. |
| Any host | Agent tool or TeamCreate, per execute_turns | Default. |

Call the Workflow tool only after the user explicitly opts in, for example by
saying "use a workflow". When a workflow would help, describe it with its rough
agent count and ask. Without opt-in, run the same plan on the default backend.
