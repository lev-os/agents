---
name: rust-cli-with-sqlite
description: >-
  Design SQLite + JSONL sync for Rust CLIs. Use when choosing a source of truth,
  designing sync strategy, WAL/PRAGMA tuning, atomic JSONL writes, recovery,
  or durability.
---

# Rust CLI with SQLite + JSONL

> **Core rule:** Pick a single source of truth. Every sync is one-way, locked, and atomic.

## Mental Model (30s)

- SQLite = fast, ACID, primary for reads/writes.
- JSONL = human/Git backup + inspection/editing.
- Expect brief divergence; require fast eventual consistency.

## When to Use

Use this skill when a Rust CLI needs:
- SQLite for fast queries + ACID writes
- JSONL for human/Git workflows
- A safe, cross-platform sync strategy

## Non-Goals

- General SQLite tutorials
- ORM/framework selection
- Schema design beyond sync metadata
- High-frequency, real-time replication

## Output First

Create the two operational docs up front:

```bash
cp assets/SYNC_STRATEGY_TEMPLATE.md SYNC_STRATEGY.md
cp assets/RECOVERY_RUNBOOK.md RECOVERY_RUNBOOK.md
```

- Fill `SYNC_STRATEGY.md` before coding.
- Record version markers for both stores.

## Quick Start (Code)

```rust
// SQLite setup: WAL + sensible sync
conn.pragma_update(None, "journal_mode", "WAL")?;
conn.pragma_update(None, "synchronous", "NORMAL")?; // or FULL for max durability
conn.pragma_update(None, "wal_autocheckpoint", 1000)?;
conn.pragma_update(None, "foreign_keys", "ON")?;
conn.set_busy_timeout(std::time::Duration::from_secs(5))?;
```

```rust
// Atomic JSONL write (Unix/Windows-safe via tempfile)
let tmp = tempfile::NamedTempFile::new_in(dir)?;
{
    let mut w = std::io::BufWriter::new(tmp.as_file());
    for line in lines {
        writeln!(w, "{}", line)?;
    }
    w.flush()?;
    tmp.as_file().sync_all()?;
}
let tmp_path = tmp.into_temp_path();
tmp_path.persist(jsonl_path)?; // atomic replace on Unix; safe on Windows
```

```rust
// Cross-process lock (fs4)
let lock = std::fs::OpenOptions::new()
    .read(true)
    .write(true)
    .create(true)
    .open(lock_path)?;
lock.lock_exclusive()?;
```

---

## Decision Tree: Source of Truth

```
Need fastest queries and ACID writes?
└─ Use SQLite as source of truth; JSONL is periodic export.

Need human-editable source and git-first workflows?
└─ Use JSONL as source of truth; DB is rebuildable cache.

Need both? (rare)
└─ Pick primary per command; store version markers in both.
```

---

## THE EXACT PROMPT - Strategy

```
Design a sync strategy for a Rust CLI using SQLite + JSONL.
Inputs: data size, concurrency level, durability requirements.
Output: source of truth, sync triggers, versioning, lock path, and failure handling.
Use assets/SYNC_STRATEGY_TEMPLATE.md as the output format.
```

## THE EXACT PROMPT - Implement Sync

```
Implement one-way sync for the chosen source of truth:
1) Acquire lock
2) Snapshot read transaction
3) Export/import
4) Atomic JSONL write (temp + fsync + rename)
5) Update version markers in both stores
6) Release lock
Include Windows-safe tempfile persist and busy-timeout handling.
```

## THE EXACT PROMPT - Recovery

```
Create recovery commands:
1) import-jsonl -> rebuild SQLite from JSONL
2) export-jsonl -> dump SQLite to JSONL
Add version checks to avoid overwriting newer data.
Use assets/RECOVERY_RUNBOOK.md for the runbook steps.
```

## THE EXACT PROMPT - Validation

```
Validate SQLite + JSONL sync:
- Run PRAGMA integrity_check
- Compare counts and a stable hash after sync
- Simulate crash mid-sync and verify recovery
```

---

## Workflow

### Phase 1: Strategy
- [ ] Choose source of truth and document it in `SYNC_STRATEGY.md`.
- [ ] Define sync triggers (on exit, on timer, on command).
- [ ] Define concurrency policy (single process vs multi-process).

### Phase 2: Storage
- [ ] Enable WAL and set synchronous target (FULL or NORMAL).
- [ ] Add indexes for hot query columns; verify with EXPLAIN QUERY PLAN.
- [ ] Implement transactions for multi-step writes.

### Phase 3: Sync
- [ ] Serialize syncs with a lock file.
- [ ] Export in a single snapshot (transaction for DB reads).
- [ ] Write JSONL atomically (temp + fsync + rename).
- [ ] Store data version / last_synced_at in both stores.

### Phase 4: Recovery
- [ ] Implement JSONL -> DB rebuild.
- [ ] Implement DB -> JSONL export.
- [ ] Detect stale store on startup and reconcile.

### Phase 5: Validation
- [ ] Run `PRAGMA integrity_check` on demand.
- [ ] Compare counts/hashes after sync.
- [ ] Test crash-recovery paths.

---

## Sync Invariants

- Only one sync runs at a time (lock file).
- Export uses a consistent snapshot.
- JSONL write is atomic (no partial file states).
- Version markers prevent overwriting newer data.
- Temporary divergence is OK; eventual consistency is required.

See: [SYNC_STRATEGY.md](references/SYNC_STRATEGY.md)

---

## Validation Loop

```
1. PRAGMA integrity_check;
2. Export/import to a temp store and compare counts
3. Optional: stable hash comparison (sorted records + SHA-256)
4. Simulate crash during sync, verify recovery
```

See: [VALIDATION.md](references/VALIDATION.md)

---

## Failure Handling

| Scenario | Action |
|----------|--------|
| DB locked | Retry with busy timeout; if still locked, report + exit non-zero |
| JSONL parse fails | Restore from DB or last git commit |
| Sync interrupted | Keep old JSONL; retry on next run |
| Git commit fails | Keep file; warn user; allow manual commit |
| DB corruption | `integrity_check` then rebuild from JSONL |

---

## Guardrails (Fast Scan)

- Performance: WAL on; use transactions; add indexes; `ANALYZE` after big changes; `VACUUM` on demand.
- Durability: `FULL` sync (macOS also `fullfsync=ON`); fsync temp file before rename; checkpoint WAL at exit or after N transactions.
- JSONL: stream large files; consider splitting very large JSONL; atomic temp+rename; keep old file on failure.
- Concurrency: lock file for sync; busy timeout; one connection per thread; WAL snapshot reads allow concurrent writers.
- Git: commit on a cadence; include record counts/version in commit messages; keep LF line endings.
- Responsiveness: stream imports/exports, show progress, flush stdout; background thread for long ops if needed.
- Cross-platform: Windows use `tempfile::persist()`; avoid network FS for SQLite; use `PathBuf`.
- Safety: parameterized SQL; validate JSONL parse; non-zero exit on failure.

See: [PRAGMAS.md](references/PRAGMAS.md)
See: [ATOMIC_JSONL.md](references/ATOMIC_JSONL.md)

---

## Expanded Guidance (Read When Implementing)

### Performance
- Enable WAL; checkpoint at exit or after N transactions to cap WAL growth.
- Batch writes in transactions; avoid per-row commits.
- Add indexes only for hot query columns; verify via EXPLAIN QUERY PLAN.
- Use `ANALYZE` after major changes; `VACUUM` occasionally to reclaim space.
- Stream JSONL reads/writes with buffered I/O; avoid loading full files.
- If JSONL is huge, split by date/category to keep diffs manageable.

### Reliability + Durability
- `synchronous=FULL` for max durability; `NORMAL` trades speed for a small crash window.
- On macOS set `fullfsync=ON` to match Linux/Windows durability.
- Atomic JSONL: temp file in same dir → fsync → rename; keep old file on failure.
- Optionally fsync the directory after rename on Unix for extra safety.
- Always store version markers in both stores; compare at startup.

### Backup + Recovery
- Provide `import-jsonl` and `export-jsonl` commands.
- If JSONL corrupt: restore from Git history; if DB corrupt: rebuild from JSONL.
- Treat Git as audit + backup, not realtime replication; commit on cadence.
- Consider pushing to a remote for off-machine backup.

### Concurrency + Responsiveness
- Use a lock file to serialize JSONL + Git writes across processes.
- Set a busy timeout for SQLite; surface clear lock errors.
- One connection per thread; WAL snapshot reads allow concurrent writers.
- Stream large operations and show progress; flush stdout for updates.

### Cross-Platform + Safety
- Windows: use `tempfile::persist()` for atomic replace; avoid shell assumptions for git.
- Use `PathBuf` for paths; ensure JSONL stays LF (gitattributes).
- Parameterized SQL; never build SQL with string concatenation.
- Validate JSONL parse errors and return non-zero exit codes on failures.

---

## Deep Dive Index (Progressive Disclosure)

- Sync strategy + version markers: [SYNC_STRATEGY.md](references/SYNC_STRATEGY.md)
- PRAGMAs + tuning + maintenance: [PRAGMAS.md](references/PRAGMAS.md)
- Atomic JSONL + fsync + Windows: [ATOMIC_JSONL.md](references/ATOMIC_JSONL.md)
- Concurrency + locking + threads: [CONCURRENCY.md](references/CONCURRENCY.md)
- Recovery + rebuild + Git fallback: [RECOVERY.md](references/RECOVERY.md)
- Validation + integrity checks: [VALIDATION.md](references/VALIDATION.md)

---

## Done When

- `SYNC_STRATEGY.md` and `RECOVERY_RUNBOOK.md` exist and are filled.
- One source of truth is selected and documented.
- Import/export commands work end-to-end.
- Version markers are written and compared.
- Crash-recovery test passes.

---

## Anti-Patterns

- Two-way sync in a single command
- No lock around JSONL writes
- JSONL updates without atomic replace
- Missing version markers in either store
- Commit-per-record Git writes
- Full file loads for large JSONL

---

## Reference Index

| Need | Read |
|------|------|
| Source-of-truth patterns | [SYNC_STRATEGY.md](references/SYNC_STRATEGY.md) |
| PRAGMAs + tradeoffs | [PRAGMAS.md](references/PRAGMAS.md) |
| Atomic JSONL writes | [ATOMIC_JSONL.md](references/ATOMIC_JSONL.md) |
| Concurrency + locks | [CONCURRENCY.md](references/CONCURRENCY.md) |
| Recovery + versioning | [RECOVERY.md](references/RECOVERY.md) |
| Validation checklist | [VALIDATION.md](references/VALIDATION.md) |

---

## Assets

- `assets/SYNC_STRATEGY_TEMPLATE.md`
- `assets/RECOVERY_RUNBOOK.md`
