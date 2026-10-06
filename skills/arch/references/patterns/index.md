# Patterns: router and index

## The principle

JP, 2026-10-02: "no pattern is the besst pattern, if you can manage complexity w/ conciseness and simplicity that is always the better option."

The simplest code that manages the complexity wins. A pattern is a cost you pay to buy back control of a specific force. Name the force first. If you cannot name it, the answer is no pattern. Choosing is never binary: it is a tradeoff conversation with the user, so always show 2-3 candidates with what each costs and one recommendation with the why.

Scope: these are code-level patterns (inside a repo). For system-level styles (monolith vs microservices vs serverless) load `../style-selection.md`.

## Before any pattern: the ladder

Stop at the first rung that holds.
1. Delete the code or the requirement.
2. Inline it; one function in the caller.
3. Pure function plus a plain type (functional-core).
4. Reuse a pattern the codebase already uses (consistency beats local optimum).
5. Only then a new pattern, the smallest one that names the force.

Ousterhout's test: a module earns its interface only if it hides more than it exposes (deep, not shallow).

## Router: when this, consider that

| Symptom / force | Candidates (tradeoff) | Default lean |
| --- | --- | --- |
| Two modules import each other | event-driven (decoupled, harder to trace) · move the shared type inward per clean-architecture (one edit, needs a real owner) · merge them (simplest, if they are one concept) | Move the type inward; merge if one concept |
| A type crosses three packages | put it in the shared domain package (ddd-tactical; one owner, risk of dumping ground) · parse-dont-validate at each edge (local types, more parsing) · keep one owner and import it (no move, longer edges) | Shared domain only if 2+ contexts truly need it |
| A test needs a real network, disk or clock | functional-core (move logic out, no mocks, needs refactor) · ports-and-adapters (fake adapter, one more interface) · dependency-injection of a `deps` object (cheap, keeps shape) | Functional-core first; DI for what stays effectful |
| Sprawling imports of concrete clients | dependency-injection with a composition root (explicit, one more parameter) · ports-and-adapters (contract per outside thing) · capability-based (also narrows authority) | DI, no container |
| Illegal status combos, boolean soup | state-machines as a table (cheap, explicit) · typestate in Rust/TS brands (compile-time, more types) · ddd aggregate guarding moves (rules in one place) | Transition table |
| Errors swallowed, `catch (e: unknown)` | result-types (typed, more `if (!r.ok)`) · parse-dont-validate at entry (fewer error sites) · effect-systems light form (governed effects, new concept) | Result plus boundary parse |
| `any` / raw YAML flows inward | parse-dont-validate (one schema, derived type) · value objects (ddd) · result-types for the parse outcome | Parse at the edge |
| Many variants that differ only in values | declarative-interpreter (data plus engine, risk of YAML language) · convention-over-configuration (place decides) · a plain lookup table (smallest) | Lookup table until variants need validation |
| One change edits five layer folders | vertical-slice (local, risk of copies) · modular-monolith boundaries (enforced, checker cost) · clean rings, dependency rule only | Vertical slice |
| Need audit, replay, "what happened and why" | event-sourcing for that one stream (replay, schema versioning forever) · append-only receipts without folding (cheaper) · event-driven plus a log sink | Append-only log, fold only when needed |
| Dashboard reads are slow or a different shape | cqrs light: rebuildable projection (lag, but cheap) · query the record directly (simplest) · cache with invalidation (fast, invalidation bugs) | Query directly, then projection |
| Many long-running workers that crash | actor-model with supervision (policy, more concepts) · state-machines plus a reaper (simpler) · process per worker via the substrate (OS isolation, heavier) | Machine plus reaper; supervision when restarts are routine |
| Untrusted code (plugin, model output) acts | capability-based (pass narrowed ports) · microkernel-plugins contract (registry, review gate) · process sandbox (strong, heavy) | Capabilities plus a single effect runner |
| Adding features without editing the core | microkernel-plugins (stable extension points; wait for 2 real plugins) · convention-over-configuration discovery · event-driven hooks | Plugins with discovery |
| Multi-step compile/resolve job | pipes-and-filters (testable stages) · one function (if under ~40 lines) · state-machines (if it branches back) | One function, split when a stage needs its own test |
| Rules leak into framework or transport code | functional-core · ports-and-adapters · clean-architecture dependency rule (no DTO rings) | Functional-core |

## Index: 20 patterns with fit for Lev

Fit 1-5 for a TS+Rust agent framework run by one person plus agents. "Live" means the repo already uses it.

| Pattern | Fit | Why |
| --- | --- | --- |
| [functional-core-imperative-shell](functional-core-imperative-shell.md) | 5 | Live in playbook; cheapest testability win; makes the translator boundary concrete |
| [ports-and-adapters](ports-and-adapters.md) | 5 | Live hex canon (`*Port`/`*Adapter`); provider and tool churn sits behind ports |
| [dependency-injection](dependency-injection.md) | 5 | JP's preference over sprawling imports; pure DI, no container |
| [parse-dont-validate](parse-dont-validate.md) | 5 | YAML, task specs and LLM output all enter untyped; zod/serde already present |
| [result-types](result-types.md) | 5 | Live: two-arm `EvalDecision`; failure is domain, not exception |
| [state-machines](state-machines.md) | 5 | Entity lifecycle stages; idea machine; gates as guards |
| [microkernel-plugins](microkernel-plugins.md) | 5 | Live: ~56 plugins, handlers projected by poly to every surface |
| [modular-monolith](modular-monolith.md) | 5 | Live: 42 core packages, import allowlist, boundary lint |
| [declarative-interpreter](declarative-interpreter.md) | 5 | The ratchet thesis: Lev IR plus FlowMind; keep the data shallow |
| [ddd-tactical](ddd-tactical.md) | 4 | Workstream aggregate root, bounded context per package; skip repository/factory templates |
| [vertical-slice](vertical-slice.md) | 4 | Live standard (`vertical_slice_locality`); fits agent-sized changes |
| [pipes-and-filters](pipes-and-filters.md) | 4 | Fractal resolver and compilers are pipelines |
| [event-driven](event-driven.md) | 4 | Live: `LevEvent` is the only cross-module channel |
| [event-sourcing](event-sourcing.md) | 4 | Live for the execution ledger only; do not spread to state files |
| [capability-based-security](capability-based-security.md) | 4 | Agents run untrusted actions; spawn is already single-owner |
| [convention-over-configuration](convention-over-configuration.md) | 4 | Fractal ownership via `owns:`; collisions must be build errors |
| [clean-architecture](clean-architecture.md) | 3 | Take the dependency rule and domain objects; leave DTO-per-ring cruft |
| [actor-model](actor-model.md) | 3 | Useful as a lens for sessions and supervision; not a runtime to build |
| [effect-systems](effect-systems.md) | 3 | Light form live in `core/effect`; Effect-TS fails the no-new-deps rule |
| [cqrs](cqrs.md) | 2 | Rebuildable read models exist already; full CQRS adds risk for little |

Considered and folded in or left out: onion (same as clean), humble object (inside functional-core), typestate (inside state-machines), saga (inside event-driven), data-oriented design (Rust hot paths only; no current force), reactive streams (no current force), microservices (system-level; see style-selection).

## How to use this in a conversation

1. Name the symptom in the user's words; find the row above.
2. Run the ladder; say which rung holds if it does.
3. Show the 2-3 candidates with cost in lines and concepts (from each file), one recommendation, the why, and what would change the call.
4. Point at the code that already uses the pattern before proposing a new one.

Sources are listed at the bottom of each pattern file.
