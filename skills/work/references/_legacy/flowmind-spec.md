# FlowMind-Driven SPEC Wiring

`work` remains the cross-domain scheduler/orchestrator. SDLC behavior is delegated at the `SPEC` stage through a FlowMind compile simulation path.

## Routing

```
User intent
  -> lev router
    -> work FSM
      -> if sdlc.enabled && stage==SPEC:
           load SDLC FlowMind YAML
           compile -> system_prompt (simulate)
           run spec generation from compiled prompt
           emit custom:spec artifact
      -> else:
           fallback to existing template/planning route
```

## Ownership Split

1. `work`: lifecycle scheduling, entity dispatch, handoff continuity.
2. `core-sdlc`: coding-task gates, spec lifecycle transitions, commit gates.
3. FlowMind YAML: executable contract source for spec behavior.

## Hard Constraints

1. **C1 finitude**: bounded runs only (`max_iterations`, timeout, explicit transitions).
2. **C4 ratchet**: append-only lifecycle moves, no implicit state rewrites, explicit compensation via events.

## Roadmap

1. **Option A** (`simulate`): compile-only SPEC path in `work` with fallback. **← Active**
2. **Option B** (`simulate+run`): adapter executes compiled prompt through `lev exec` and records transition evidence.
3. **Option C** (`enforce`): plugin discovery/registration/hooks fully wired; `core-sdlc` gates become mandatory.
4. **Graph/CMS convergence**: bind lifecycle/state outputs to graph entities and CMS materialized views (`docs/specs/spec-graph.md`, `docs/plugins/cms.md`).
