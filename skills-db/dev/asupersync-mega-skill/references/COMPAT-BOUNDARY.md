# Tokio Compat Boundary

`asupersync-tokio-compat` is real and useful, but it is not the preferred architecture.

## When To Use It

Use compat only when a dependency still requires one of these:

- `tokio::runtime::Handle::current()`
- Tokio I/O traits
- hyper runtime traits
- a Tokio-hosted future that cannot be removed yet

Typical examples:

- `reqwest`
- `axum`
- `tonic`
- `sqlx`
- other crates that still assume Tokio is present

## Hard Rules

- the main `asupersync` crate must not depend on compat,
- Tokio must never become the primary executor for the application,
- `Cx` must cross the boundary explicitly,
- adapter-spawned work must still be region-owned and cancellation-aware.

## What Compat Actually Provides

- runtime bridge: `with_tokio_context(...)`
- sync context bridge for construction paths that need a Tokio handle
- Tokio <-> Asupersync IO adapters
- hyper executor/timer/body bridges
- tower bridge
- cancellation policies for wrapped Tokio futures

## Recommended Boundary Shape

Keep the whole thing in one module or crate.

Pattern:

- core domain code exposes native Asupersync interfaces,
- adapter module owns the Tokio-specific client/service,
- adapter functions accept `&Cx`,
- compat is the only place where Tokio types appear.

## Cancellation Policy Guidance

Compat exposes cancellation modes because Tokio-originated futures may not respect Asupersync semantics.

Prefer:

- strict handling when correctness matters,
- explicit timeout fallback only when you understand the operational tradeoff,
- best-effort only for low-risk glue where native semantics are impossible.

## Removal Plan

Compat is successful only if it shrinks over time.

Good end state:

- domain and service code are fully native,
- one or two boundary modules remain for genuinely unavoidable third-party crates,
- or the compat layer is gone entirely.

Bad end state:

- compat spreads across the codebase,
- Tokio types leak into business logic,
- new features keep being built on the bridge instead of on native surfaces.
