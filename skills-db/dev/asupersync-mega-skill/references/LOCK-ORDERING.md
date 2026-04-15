# Lock Ordering and Concurrency Discipline

## Canonical Lock Order

When acquiring multiple locks, the strict order is:

```
E(Config) -> D(Instrumentation) -> B(Regions) -> A(Tasks) -> C(Obligations)
```

Violating this order causes deadlocks. This is enforced by:

- `ShardGuard` variants with label system
- Debug checks that verify acquisition order
- 23 dedicated tests for lock ordering correctness

Source: `src/runtime/sharded_state.rs`

## ShardedState

Runtime state split into independently locked shards:

| Shard | Label | Contents |
|-------|-------|----------|
| E | Config | Immutable runtime configuration |
| D | Instrumentation | Trace surfaces, metrics |
| B | Regions | Region ownership tree, state transitions |
| A | Tasks | Task table, stored futures, intrusive queue links |
| C | Obligations | Permit/ack/lease lifecycle, leak tracking |

### Why Independent Shards?

Hot-path polling proceeds without serializing every region or obligation mutation. Each shard can be locked independently when only one table is needed.

### Multi-Shard Operations

Use `ShardGuard` to acquire multiple shards in canonical order. The guard variants enforce ordering at compile time (type system) and runtime (debug assertions).

## ContendedMutex

Source: `src/sync/contended_mutex.rs`

Wrapper around `parking_lot::Mutex` with optional contention metrics (feature: `lock-metrics`):
- Wait time tracking
- Hold time tracking
- Contention event counting

Use for all shard locks in `ShardedState`.

## Channel Waker Dedup

Pattern used across the codebase: `Arc<AtomicBool>` on:
- mpsc `SendWaiter`
- broadcast receivers
- watch `WatchWaiter`

Prevents duplicate wakeups and reduces contention on the wake path.

## Worker Wake Coordination

- `Idle -> Polling -> Notified` state machine for centralized wake dedup
- Scheduling paths route through `wake_state.notify()`
- Wakes during poll are coalesced (no double-enqueueing)
- `Waker::will_wake` guards skip redundant clones on waiter registration

## Lost-Wakeup Prevention

Multiple strategies used:
- Permit-style `Parker` with queue rechecks after wakeup
- Capacity re-checks after waiter registration (closes capacity-check/registration race)
- Both send and receive waiters woken on channel close

## Intrusive Queue Links

Source: `src/runtime/scheduler/intrusive.rs`

- Links stored directly in `TaskRecord`
- Queue-tag membership checks (O(1) pop without allocation)
- Owner pop and thief steal stay O(1)

## Atomic Counter Discipline

Source: `src/runtime/scheduler/global_injector.rs`

- Timed counters incremented before heap insert
- Saturating decrements on pop
- Cached earliest-deadline fast path
- Workers skip timed-lane mutex when no deadline work exists

## Steal-Path Locality

Source: `src/runtime/scheduler/local_queue.rs`

- Local queues track pinned local tasks
- When none present, stealers take no-branch non-local path
- When locals exist, skipped/restored with `SmallVec` (allocation-free common path)

## Migration to parking_lot

Runtime, scheduler, I/O, lab, networking, and transport internals all use `parking_lot` primitives where it improves lock-path cost. This was a deliberate, measured migration.

## Rules

1. Always acquire in canonical order: E -> D -> B -> A -> C
2. Never hold a shard lock across an await point
3. Use `ContendedMutex` for shard locks (enables metrics)
4. Use `ShardGuard` for multi-shard operations
5. Prefer atomic operations over locks on hot paths
6. Use `Waker::will_wake` to skip redundant clone operations
