---
name: cdo-node-properties
description: Workshop POC node-centric specification — reference only, not prescriptive
---

# CDO Node Properties — Workshop POC Reference

This documents the node-centric model from the workshop POC. Reference material, not prescriptive.

---

## Core Principle

CDO nodes have **composable behavioral properties**, not separate types. A node isn't "a streaming node" or "a parallel node" — it's a node with streaming and parallel properties enabled.

## Property Definitions

```yaml
node_properties:
  streaming: true      # Process until confidence/satisfaction threshold
  parallel: true       # Part of cognitive ensemble, runs concurrently
  adaptive: true       # Can modify behavior based on intermediate results
  memory: true         # Persistent context across cycles
  feedback: true       # Iterate until convergence criterion met
  pipeline: true       # Sequential dependency, output feeds next node
```

### Property Details

**`streaming`** — Node processes continuously rather than in discrete batches. Useful for research tasks where you want progressive refinement until a confidence threshold is met.

**`parallel`** — Node runs as part of a concurrent ensemble. Multiple parallel nodes execute simultaneously, each with independent context.

**`adaptive`** — Node can change its own behavior based on what it's learned. This is the key property — it's what makes a node "intelligent" rather than just "automated."

**`memory`** — Node retains context across execution cycles. Without memory, each invocation is stateless.

**`feedback`** — Node participates in iterative refinement loops. Output is evaluated against convergence criteria, and the node re-executes if criteria aren't met.

**`pipeline`** — Node has explicit sequential dependencies. Its output feeds directly into the next node's input.

---

## Breakthrough Pattern

The combination that worked in the workshop POC:

```
4 Research Nodes          →  4 Parliament Nodes        →  1 CEO Node
(streaming, parallel)        (parallel, personality)       (adaptive, meta-cognitive)
```

### Why This Worked

1. **Research phase**: 4 nodes explore the problem space simultaneously, each streaming results until they hit confidence threshold. No coordination needed — pure parallel exploration.

2. **Parliament phase**: 4 nodes with distinct personality lenses (critic, advocate, systems thinker, pragmatist) evaluate the research output in parallel. Independence enforced — no anchoring.

3. **CEO phase**: 1 node with adaptive + meta-cognitive properties synthesizes everything. It can change its evaluation criteria based on what the parliament surfaced.

---

## Key Insight

> "Adaptive" is not a node type — it's a research workflow.

The adaptive turn engine in CDO implements this property at the **workflow level**, not the node level. Individual nodes don't need to be adaptive — the orchestration layer decides whether to expand, contract, or redirect based on aggregate results.

This is the difference between:
- **Node-level adaptive**: Each node adjusts itself (complex, hard to reason about)
- **Workflow-level adaptive**: The engine adjusts the ensemble (simpler, observable)

CDO chose workflow-level. The engine watches convergence metrics and adjusts width/depth/composition. Nodes stay focused on their single job.

---

## Composition Examples

Common property combinations:

| Pattern | Properties | Use Case |
|---------|-----------|----------|
| **Explorer** | streaming, parallel | Research, data gathering |
| **Deliberator** | parallel, feedback | Parliament, multi-perspective |
| **Sequencer** | pipeline, memory | Multi-step workflows |
| **Sentinel** | streaming, feedback | Monitoring, validation |
| **Integrator** | adaptive, memory | Synthesis, decision-making |

---

## Reference

Full specification: `~/digital/leviathan/workshop/poc/cdo/docs/cdo-node-centric-specification.md`
