# Concurrency and Locking

## Cross-Process Locks

Use a lock file to serialize sync or write operations:
```rust
use fs4::FileExt;
let lock = std::fs::OpenOptions::new().read(true).write(true).create(true).open(lock_path)?;
lock.lock_exclusive()?;
```

## SQLite Busy Timeout

```rust
conn.set_busy_timeout(std::time::Duration::from_secs(5))?;
```

## Threading Notes

- Do not share rusqlite::Connection across threads unless explicitly enabled.
- Prefer one connection per thread; open a fresh connection in worker threads.
- WAL allows readers during writes (snapshot reads).
- For a consistent export snapshot, start a read transaction before scanning.
- Serialize JSONL writes + Git commits with the same lock.
 - Locks release on process exit, but still handle stale-lock edge cases.

## Sync Serialization

Only one sync should run at a time. Use the lock in all commands that write JSONL.

## Environment Notes

- Avoid network filesystems for SQLite; locking can be unreliable.
- Use `PathBuf` for cross-platform file paths.
