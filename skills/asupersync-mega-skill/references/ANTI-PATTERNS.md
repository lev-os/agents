# Asupersync Anti-Patterns

These are the fastest ways to sabotage a migration.

## Architecture Mistakes

- Treating Asupersync as a drop-in executor swap.
- Keeping Tokio as a silent co-runtime in core code.
- Hiding `Cx` in globals, thread-locals, or hidden framework state.
- Building new features on compat because it is easier than going native.
- Treating `RuntimeBuilder + block_on` as the final architecture for a long-lived service that really wants `AppSpec` / supervision.
- Recreating a global process registry or service locator instead of using capability-scoped naming.

## Concurrency Mistakes

- Leaving `tokio::spawn` or detached equivalents inside handlers and services.
- Starting request-local or task-local work with no owning region.
- Using race/select patterns that abandon losers without proving cleanup.
- Forgetting checkpoints in loops, retries, or long handlers.
- Holding wide cancellation masks around normal business logic instead of short cleanup-critical sections.

## Resource / Cleanup Mistakes

- Holding permits, locks, or leases across indefinite waits.
- Assuming drop-based cleanup is good enough.
- Failing to verify quiescence and leak behavior after migration.
- Dropping `AppHandle`, named-server lease handles, or other obligation-like lifecycle handles without explicit resolution.
- Using plain channels where reply obligations or typed protocol edges should be explicit.

## Testing Mistakes

- Converting runtime code but leaving `#[tokio::test]` patterns untouched.
- Using wall clock or ambient randomness in deterministic tests.
- Accepting non-deterministic flakes as normal after adopting Asupersync.
- Only testing happy-path completion and never testing cancel/drain/finalize behavior.
- Ignoring replay artifacts, futurelock warnings, or leak oracles because "the test usually passes."

## API / Ergonomics Mistakes

- Assuming proc macros are more authoritative than manual APIs.
- Overusing `Cx::for_testing()` or `Cx::for_request()` instead of designing the real ownership flow.
- Passing full-capability `Cx` everywhere instead of narrowing at boundaries.
- Flattening `Outcome::Cancelled` and `Outcome::Panicked` into generic `Err` too early.
- Using `Budget::INFINITE` everywhere because budget design feels inconvenient.

## Status / Capability Mistakes

- Assuming every feature documented in the repo is equally mature.
- Ignoring partial or unsupported classifications for QUIC/H3, SQLx compile-time macros, Kafka advanced consumers, Windows signals, or PTY support.

## Recovery Rule

If you notice any of the above, stop optimizing for low churn. Rework the design around:

- explicit `Cx`,
- region-owned work,
- native replacements,
- deterministic validation,
- explicit boundary bridges only where unavoidable.
