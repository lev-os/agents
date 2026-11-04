# Substrate-first follow-up planning

Use this when a user corrects a plan because it centered a plugin/repo/component before the underlying platform substrate was proven.

## Session lesson

A plan for a plugin such as `plugins/autoresearch` should not start with refactoring the plugin if the user's real question is about how to use Lev's existing substrate. First identify and prove the existing class-level substrate, then make the plugin migration a follow-up.

## Pattern

1. **Restate the correction explicitly.** Example: "The first plan was too plugin-centered; this one is substrate-first, with the plugin as follow-up."
2. **Inventory existing substrate owners before naming implementation work.** For Lev research-loop work this included:
   - `core/flowmind` for declarations/control plane;
   - `core/orchestration/src/loop` for bounded loop mechanics;
   - `core/eval` for measurements, evaluator bindings, EvalRun coordination, and `EvalDecision`;
   - `core/exec` for effectful work, receipts, traces, and artifact envelopes;
   - reusable flows such as `plugins/sdlc/flows/eval-harness.flow.yaml`;
   - reference plugin shapes such as CDO, where the plugin owns profiles/prompts/flows but not core runtime authority.
3. **Declare what must not happen.** For plugin follow-up plans, forbid the plugin from becoming a second generic loop runner, eval authority, proof system, scorecard, or receipt ledger.
4. **Prove locally before promoting.** Start with local `.lev` proof artifacts or neutral control-plane artifacts before moving anything into the plugin.
5. **Make the follow-up explicit.** Only after proof should the plan inventory the plugin exports, classify duplicates vs recipes vs legacy surfaces, and register thin FlowMind programs/profiles.

## Useful plan sections

- Correction
- Current-state inventory
- What must be true
- What must not be true
- Substrate-first phases
- Gate candidates
- Before breaking ground
- Plugin follow-up plan
- Open decisions

## Pitfall

Do not treat an existing plugin audit as the plan's center of gravity when the user's ask is really "how should this use the existing platform substrate?" The audit may be useful evidence, but the plan should be organized around substrate ownership and proof gates first.
