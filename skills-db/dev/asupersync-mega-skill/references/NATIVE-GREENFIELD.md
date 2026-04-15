# Native Greenfield Asupersync

This is the preferred path when you control the architecture.

## Build Around The Real Core

- `RuntimeBuilder` owns runtime bootstrap and process-level configuration.
- `Cx` is the capability token that carries cancellation, tracing, time, randomness, budget, and scoped authority.
- `Scope` owns spawned work and child regions.
- `LabRuntime` gives deterministic execution, replay, and invariant checks.
- `AppSpec` / supervision / actors / spork are higher-level composition layers when you need long-lived supervised systems.

## Process Bootstrap

Pattern:

```rust
use asupersync::runtime::RuntimeBuilder;

fn main() -> Result<(), asupersync::Error> {
    let rt = RuntimeBuilder::current_thread().build()?;
    rt.block_on(async {
        // prefer runtime-managed contexts in production,
        // use Cx::for_request() only as a convenience seam
    });
    Ok(())
}
```

Useful runtime builder levers:

- worker count
- blocking pool bounds
- observability hooks
- deadline monitoring
- env or config-file overrides
- logical clock mode
- root-region limits

## API Design Rules

- Put `&Cx` first in async APIs you own.
- Use `Scope` or child-region APIs for owned concurrency.
- Add checkpoints in loops, long retries, and handler bodies.
- Surface cancellation, panic, or cleanup semantics at orchestration boundaries.
- Narrow `Cx` capabilities at framework boundaries instead of passing full power everywhere.

## Request / Service Shape

Good pattern:

- per-request region or per-call region,
- wrap request metadata and `Cx` together,
- narrow capabilities for handlers,
- let handler-spawned work live inside the request region.

Relevant repo patterns:

- `web::request_region::{RequestRegion, RequestContext}`
- `grpc::CallContext::with_cx(...)`

## Concurrency Guidance

Prefer:

- `Scope::spawn`
- child regions with tighter budgets
- explicit race/join semantics that preserve loser draining where needed
- native channel and sync primitives

Be careful with:

- proc macros beyond `scope!`
- low-level `Cx::race*` variants that may drop losers instead of proving they drained

If loser drain matters, use the manual scope/task APIs that preserve the stronger semantics.

## Supervision / OTP-Style Systems

Reach for:

- `app::AppSpec`
- `actor`
- `gen_server`
- `supervision`
- `spork`

Use these when your system has:

- long-lived workers,
- named processes or registries,
- restart strategies,
- explicit application startup/shutdown trees.

The best repo example is `examples/spork_minimal_supervised_app.rs`.

## Greenfield Default Stack

For a fully native app, prefer this stack:

- runtime: `RuntimeBuilder`
- app/task model: `Cx`, `Scope`, child regions
- channels/sync: `channel::*`, `sync::*`
- time: `time::*`
- networking: `net::*`, `tls::*`, `websocket::*`
- web: `web::*`, `service::*`
- grpc: `grpc::*`
- database: `database::*`
- testing: `test_utils`, `LabRuntime`
- observability: `observability::*`

## Greenfield Validation Checklist

- all owned async APIs accept `&Cx`,
- no detached tasks,
- checkpoints exist in long-running loops,
- service boundaries narrow capabilities,
- tests use deterministic helpers,
- no Tokio dependency is present in core code.
