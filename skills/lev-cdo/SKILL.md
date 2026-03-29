---
name: lev-cdo
description: "Lev-specific CDO deliberation. Injects architecture context into cdo agent briefs. Use for architecture decisions, protocol design, module placement, and cross-cutting concerns in ~/lev."
---

# Lev CDO — Architecture-Aware Deliberation

Thin wrapper over the `cdo` skill. Adds lev-specific context to every agent brief.

## How It Works

1. Generate architecture context on the fly (bash commands, not static files)
2. Inject into every CDO agent's system prompt as `<lev-context>` block
3. Delegate to `cdo` skill for turn execution, synthesis, and convergence
4. All CDO presets (quick/think/deep/full/debug) work — this just adds context

## Context Injection

Before dispatching any CDO agent, generate and prepend this context:

```bash
# Run these to get current architecture state:
ls ~/lev/core/ | sort                              # 20 core modules
grep "id:" ~/lev/dna/*.dna.yaml                    # DNA constraint IDs
head -30 ~/lev/core/domain/src/execution-protocol.ts  # ExecTransport pattern
head -20 ~/lev/core/orchestration/src/intent/types.ts  # IntentDeclaration
```

Key decisions (session 3, verified):
- Poly owns protocols + surfaces (not just surface projection)
- Domain owns shared types (ProtocolAdapter, ExecTransport, Route, Target)
- Harness owns runtime execution (TmuxHarness, AdapterRegistry, profile-loader)
- Orchestration owns dispatch (A2A AgentJob → JobExecutor)
- Nobody owns the registry — emergent from protocol instances on disk
- Fractal config: inline → file → folder glob
- DNA contracts are behavioral gates, not documentation
- ntm is EXTERNAL — we own TmuxHarness, not ntm
- CLI agents are a protocol, not a config schema
- Intent should NOT live in orchestration (placement TBD — likely domain)

## When to Use lev-cdo vs cdo

| Use lev-cdo when... | Use cdo when... |
|---|---|
| Deciding where code lives in ~/lev | General architecture decisions |
| Protocol design (poly-protocol, runners) | Non-lev deliberations |
| Module placement (core vs plugin) | Cross-project questions |
| DNA contract changes | General trade-off analysis |
| ExecOptions / adapter design | |
| Intent protocol placement | |
| FlowMind stabilization review | |

## Skill Discovery for Agents

When composing agent briefs, discover relevant skills:
- `arch` — system design, C4, trade-offs
- `mcp-server-design` — agent-friendly API patterns
- `agent-fungibility-philosophy` — fungible agent architecture
- `lev-builder` — module placement decisions
- `lev-align` — validation gate checking
- `operationalizing-expertise` — distilling methods into artifacts
- `testing-conformance-harnesses` — protocol conformance

## CDO Templates

### Protocol Design
Turn 0: Research (read code, web search, cass history)
Turn 1: Framing (8 agents — architect, taxonomist, prior art, transport, adversarial, adoption, network, naming)
Turn 2: Deepening (6 agents — schema, discovery, MCP bridge, spikes, analogy, unifier)
Turn 3: Stress Test (4 agents — devil's advocate, complexity, streaming gap, versioning)
Turn 4: Synthesis (3 agents — synthesizer, visual explainer, readme)

### Module Placement
Turn 0: Read the module code + DNA contracts
Turn 1: Where does it live? (3 agents — domain advocate, poly advocate, harness advocate)
Turn 2: Integration (2 agents — dependency analyzer, DNA compliance checker)

### Architecture Review
Turn 0: Read specs + design docs + code
Turn 1: Multi-perspective analysis (5 agents — each a Six Hats color)
Turn 2: Synthesis + pre-mortem (2 agents)

### FlowMind Stabilization
Turn 0: Read executor.ts, schema.ts, execution-contract/, gate-evaluator.ts, plugins/dna/
Turn 1: 10-question arch review (10 parallel agents, one per question)
Turn 2: Synthesis + reconciliation
Turn 3: Spec draft
