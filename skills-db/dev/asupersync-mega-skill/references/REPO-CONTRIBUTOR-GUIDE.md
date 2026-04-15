# Working Inside the Asupersync Repo

Rules from AGENTS.md for AI coding agents working in this codebase.

## Critical Rules

1. **NEVER delete files** without express written permission. Even files you created.
2. **NEVER run destructive commands** (`git reset --hard`, `git clean -fd`, `rm -rf`) without explicit user authorization.
3. **Branch is `main`**, never `master`. Update any `master` references to `main`.
4. **Rust 2024 edition**, nightly toolchain (pinned in `rust-toolchain.toml`).
5. **Cargo only** -- no other package manager.
6. **`#![deny(unsafe_code)]`** with per-module `#[allow(unsafe_code)]` where required.
7. **No backwards compatibility** concern -- early development, do things the right way.

## Forbidden Crates

`tokio`, `hyper`, `reqwest`, `axum`, `tower` (tokio adapter only), `async-std`, `smol`, or any crate that transitively depends on tokio.

## Code Editing Discipline

- **Never** run scripts that process/change code files. Make changes manually.
- **Never** create file variations (e.g., `mainV2.rs`, `main_improved.rs`).
- New files only for genuinely new functionality. Bar is very high.
- Revise existing code files in place.

## Compiler Checks (Mandatory After Code Changes)

```bash
rch exec -- cargo check --all-targets
rch exec -- cargo clippy --all-targets -- -D warnings
rch exec -- cargo fmt --check
```

`rch` offloads builds to remote workers when available. Falls back to local if unavailable.

## Testing

Every module includes inline `#[cfg(test)]` unit tests. Tests must cover:
- Happy path
- Edge cases (empty input, max values, boundary conditions)
- Error conditions

For concurrency-sensitive behavior, prefer deterministic lab-runtime tests.

### Test Commands

```bash
cargo test                           # all tests
cargo test -- --nocapture            # with output
cargo test --lib <module_name>       # specific module
cargo test -p asupersync-macros      # workspace member
cargo test -p asupersync-conformance
cargo test -p franken-kernel
cargo test -p frankenlab
```

### Test Categories

| Area | Focus |
|------|-------|
| `types/` | IDs, outcomes, budgets, policies, serialization round-trips |
| `record/` | Task/region/obligation record creation, state transitions |
| `runtime/` | Scheduler fairness, state management, region lifecycle |
| `cx/` | Capability context, scope API, structured concurrency contracts |
| `channel/` | Two-phase reserve/send, MPSC/oneshot, cancel-correctness |
| `sync/` | Mutex, RwLock, Semaphore, Pool, Barrier, OnceLock -- cancel-awareness |
| `combinator/` | Join, race, timeout, bulkhead, retry -- loser drain correctness |
| `cancel/` | Cancellation protocol, symbol cancel, drain/finalize lifecycle |
| `obligation/` | Permit/ack/lease commit/abort, no-leak invariant |
| `lab/` | Virtual time, deterministic scheduling, DPOR, oracles |
| `net/` + `io/` | Async I/O adapters, socket integration |
| `http/` | HTTP/1.1, HTTP/2 protocol correctness |
| `codec/` | Framing, encoding/decoding round-trips |
| `conformance/` | Cross-component conformance suite |
| `benches/` | Scheduler, timer wheel, reactor, cancel/drain, RaptorQ |

### E2E and Benchmarks

```bash
./scripts/run_all_e2e.sh
NO_PREFLIGHT=1 ./scripts/run_raptorq_e2e.sh --profile fast --bundle
cargo bench --bench scheduler_benchmark
cargo bench --bench timer_wheel
```

## Feature Flags

| Flag | What |
|------|------|
| `test-internals` (default) | Test helpers -- NOT for production |
| `proc-macros` | `scope!`, `spawn!`, `join!`, `race!` |
| `tls` / `tls-native-roots` / `tls-webpki-roots` | TLS via rustls |
| `sqlite` / `postgres` / `mysql` | Database clients |
| `io-uring` | Linux io_uring reactor |
| `tower` | Tower Service adapter |
| `metrics` | OpenTelemetry |
| `lock-metrics` | ContendedMutex tracking |
| `loom-tests` | Loom verification |
| `simd-intrinsics` | AVX2/NEON GF(256) for RaptorQ |

## Output Style

- Core code should not write to stdout/stderr
- Use structured tracing via `Cx::trace` for observability
- Keep tests deterministic; avoid time-based logging outside lab runtime

## Key Dependencies

| Crate | Purpose |
|-------|---------|
| `thiserror` | Error derivation |
| `crossbeam-queue` | Lock-free queues |
| `parking_lot` | Fast sync primitives |
| `polling` | Portable epoll/kqueue/IOCP |
| `slab` | Pre-allocated storage |
| `smallvec` | Stack-allocated vectors |
| `pin-project` | Safe pin projections |
| `serde` + `serde_json` | Serialization |
| `socket2` | Low-level sockets |
| `rustls` | TLS (optional) |
| `rusqlite` | SQLite (optional) |
| `proptest` | Property testing (dev) |
| `criterion` | Benchmarks (dev) |

## Dependency Policy

- Prefer `std`/`core` and small, focused crates
- No other executor/runtime in core
- New crates must preserve determinism in lab runtime
- No ambient globals

## Multi-Agent Environment

Other agents may be working on the project simultaneously. Treat their changes as your own -- never stash, revert, overwrite, or disturb their work.

## Session Completion Protocol

1. File issues for remaining work
2. Run quality gates (if code changed)
3. Update issue status
4. Sync beads: `br sync --flush-only`
5. Hand off context for next session

## Key Documentation

| File | Purpose |
|------|---------|
| `asupersync_plan_v4.md` | Design bible and core invariants |
| `asupersync_v4_formal_semantics.md` | Small-step operational semantics |
| `TESTING.md` | Comprehensive testing guide |
| `AGENTS.md` | AI agent guidelines (source of truth) |
| `README.md` | Project overview |

## RCH (Remote Compilation Helper)

`rch` offloads cargo builds to 8 remote workers:

```bash
rch exec -- cargo build --release
rch exec -- cargo test
rch exec -- cargo clippy
rch doctor       # health check
rch workers probe --all  # test connectivity
```

If unavailable, builds run locally as normal.

## UBS (Ultimate Bug Scanner)

```bash
ubs file.rs                          # specific file
ubs $(git diff --name-only --cached) # staged files
ubs --ci --fail-on-warning .         # CI mode
```

Exit 0 = safe. Exit >0 = fix and re-run.

## Beads Issue Tracking

```bash
br ready              # show ready work
br list --status=open # all open
br show <id>          # issue details
br create --title="..." --type=task --priority=2
br update <id> --status=in_progress
br close <id> --reason "Completed"
br sync --flush-only  # export (no git ops)
```

Always `br sync --flush-only && git add .beads/` before ending sessions.
