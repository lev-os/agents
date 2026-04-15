# Source Map

## What Is Asupersync?

A spec-first, cancel-correct, capability-secure async runtime for Rust with ~500 source files across 40+ modules. Not a Tokio wrapper -- a complete replacement with stronger guarantees:

- **Structured concurrency**: every task owned by a region; region close = quiescence
- **Cancel-correctness**: cancellation is request -> drain -> finalize (not silent drop)
- **Two-phase effects**: reserve/commit prevents data loss on cancellation
- **Capability security**: all effects flow through explicit `Cx`; no ambient authority
- **Deterministic testing**: `LabRuntime` with virtual time, DPOR, oracles, chaos injection
- **Obligation tracking**: permits/acks/leases must be committed or aborted (linear resources)
- **Full networking stack**: TCP, HTTP/1.1, HTTP/2, WebSocket, TLS, gRPC, DNS, QUIC (in progress)
- **Database clients**: SQLite, PostgreSQL (wire protocol), MySQL (wire protocol)
- **OTP-style supervision**: actors, GenServer, supervision trees, AppSpec, Spork

### Six Non-Negotiable Invariants

1. **Structured concurrency**: every task/fiber/actor owned by exactly one region
2. **Region close = quiescence**: no live children + all finalizers done
3. **Cancellation is a protocol**: request -> drain -> finalize (idempotent)
4. **Losers are drained**: races must cancel and fully drain losers
5. **No obligation leaks**: permits/acks/leases must be committed or aborted
6. **No ambient authority**: effects flow through `Cx` and explicit capabilities

## Core Types Quick Reference

| Type | Purpose |
|------|---------|
| `Cx` | Capability context -- first param to all async ops, no ambient authority |
| `Scope` | API for creating child regions and spawning tasks |
| `Outcome<T, E>` | Four-valued: `Ok`, `Err`, `Cancelled(reason)`, `Panicked(payload)` |
| `Budget` | Bounded cleanup: deadline, poll_quota, cost_quota, priority. Semiring: meet = tighter wins |
| `Region` / `RegionId` | Structured concurrency scope -- owns tasks, closes to quiescence |
| `TaskId` | Identifier for spawned tasks |
| `ObligationId` | Tracked permit/ack/lease -- must be committed or aborted |
| `CancelKind` | User, Timeout, FailFast, RaceLost, ParentCancelled, Shutdown |
| `LabRuntime` / `LabConfig` | Deterministic runtime with virtual time for testing |
| `RuntimeBuilder` | Construct production runtime: `current_thread()`, `low_latency()`, `high_throughput()` |
| `AppSpec` | Application topology with supervision, registry, restart policy |

Severity lattice: `Ok < Err < Cancelled < Panicked`. Monotone aggregation.

## Workspace Structure

| Crate | Purpose |
|-------|---------|
| `asupersync` | Main runtime (~500 files, 40+ modules) |
| `asupersync-macros` | Proc macros: `scope!`, `spawn!`, `join!`, `race!`, `session_protocol!` |
| `conformance` | Conformance test suite |
| `franken_kernel` | FrankenSuite type substrate |
| `franken_evidence` | Evidence ledger schema |
| `franken_decision` | Decision contract runtime |
| `frankenlab` | Deterministic testing harness |

## Module Map (src/)

| Module | What It Does |
|--------|--------------|
| `types/` | IDs, Outcome, Budget, CancelKind, Policy, WASM ABI |
| `record/` | TaskRecord, RegionRecord, ObligationRecord |
| `runtime/` | Three-lane scheduler, sharded state, builder, config, reactor, blocking pool, timer, region heap |
| `cx/` | Cx, Scope, registry |
| `channel/` | MPSC, oneshot, broadcast, watch, session (two-phase) |
| `sync/` | Mutex, RwLock, Semaphore, Barrier, Notify, OnceLock, Pool, ContendedMutex |
| `combinator/` | join, race, timeout, quorum, hedge, circuit_breaker, bulkhead, retry, rate_limit, bracket, pipeline, map_reduce, first_ok, laws.rs |
| `cancel/` | Cancellation protocol, progress certificates (Freedman/Azuma) |
| `obligation/` | Permit/ack/lease tracking, e-process monitoring |
| `lab/` | LabRuntime, virtual time wheel, DPOR explorer, oracle suite, conformal, chaos, snapshots |
| `trace/` | Mazurkiewicz/Foata canonicalize, geodesic, DPOR, boundary (persistent homology), GF(2), sheaf, TLA+ export, crashpack |
| `time/` | Sleep, timeout, interval, timer wheel, driver |
| `io/` | Async I/O traits and adapters |
| `net/` | TCP, UDP, Unix, DNS, WebSocket, QUIC |
| `http/` | HTTP/1.1, HTTP/2, body, pool, compression |
| `tls/` | rustls TLS 1.2/1.3 |
| `bytes/` | Zero-copy Bytes, BytesMut, Buf, BufMut |
| `codec/` | Framing, encoding/decoding |
| `web/` | Router, extractors, middleware, request regions |
| `service/` | ServiceBuilder, Tower adapter |
| `grpc/` | gRPC client/server, CallContext |
| `database/` | SQLite (blocking pool), PostgreSQL (wire), MySQL (wire) |
| `stream/` | map, filter, merge, zip, fold, buffered, try_stream |
| `transport/` | Router, aggregator, sink (low-level delivery) |
| `plan/` | DAG IR, rewrite engine, analysis lattices |
| `observability/` | LogEntry, metrics, TaskInspector, Diagnostics, spectral health |
| `raptorq/` | RFC 6330 fountain codes, GF(256), pipeline |
| `distributed/` | Consistent hashing, snapshots |
| `remote.rs` | Named remote spawn, leases, idempotency, sagas |
| `actor.rs` | Bounded mailbox actors |
| `gen_server.rs` | Request/reply server (OTP GenServer) |
| `supervision.rs` | Supervision trees, restart policies |
| `spork.rs` | OTP-style layer on kernel |
| `app.rs` | AppSpec for application topology |

## Read In This Order

### 1. Project posture

- `/data/projects/asupersync/AGENTS.md`
- `/data/projects/asupersync/README.md`
- `/data/projects/asupersync/Cargo.toml`
- `/data/projects/asupersync/src/lib.rs`

### 2. Integration entrypoints

- `/data/projects/asupersync/docs/integration.md`
- `/data/projects/asupersync/docs/macro-dsl.md`
- `/data/projects/asupersync/src/runtime/mod.rs`
- `/data/projects/asupersync/src/cx/mod.rs`

### 3. Native replacement surfaces

- `/data/projects/asupersync/src/web/mod.rs`
- `/data/projects/asupersync/src/service/mod.rs`
- `/data/projects/asupersync/src/http/mod.rs`
- `/data/projects/asupersync/src/grpc/mod.rs`
- `/data/projects/asupersync/src/database/mod.rs`
- `/data/projects/asupersync/src/actor.rs`
- `/data/projects/asupersync/src/supervision.rs`
- `/data/projects/asupersync/src/gen_server.rs`
- `/data/projects/asupersync/src/observability/mod.rs`

### 4. Migration and interop docs

- `/data/projects/asupersync/docs/tokio_migration_cookbooks.md`
- `/data/projects/asupersync/docs/tokio_adapter_boundary_architecture.md`
- `/data/projects/asupersync/docs/tokio_interop_support_matrix.md`
- `/data/projects/asupersync/docs/tokio_compatibility_limitation_matrix.md`

### 5. Browser / WASM docs

- `/data/projects/asupersync/docs/wasm_quickstart_migration.md`
- `/data/projects/asupersync/docs/wasm_canonical_examples.md`
- `/data/projects/asupersync/docs/wasm_react_reference_patterns.md`
- `/data/projects/asupersync/docs/wasm_nextjs_template_cookbook.md`
- `/data/projects/asupersync/docs/wasm_troubleshooting_compendium.md`

### 6. Examples

- `/data/projects/asupersync/examples/macros_basic.rs`
- `/data/projects/asupersync/examples/macros_nested.rs`
- `/data/projects/asupersync/examples/cancellation_injection.rs`
- `/data/projects/asupersync/examples/chaos_testing.rs`
- `/data/projects/asupersync/examples/spork_minimal_supervised_app.rs`
- `/data/projects/asupersync/examples/prometheus_metrics.rs`

## When You Need Tracker Context

Use:

```bash
br list --json
br list --status closed --json
```

What to look for:

- open browser DX / QA / release beads
- closed Tokio-replacement and migration-cookbook programs
- active RaptorQ and Lean-coverage hardening work
