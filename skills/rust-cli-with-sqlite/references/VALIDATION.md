# Validation Checklist

## SQLite

- Run `PRAGMA integrity_check;` after crashes or on demand.
- Use `EXPLAIN QUERY PLAN` to confirm index usage.

## JSONL

- Parse each line with serde_json; fail fast on errors.
- Ensure newline-delimited format (no trailing garbage).
- Stream large files; avoid loading the full file into memory.

## Cross-Store

- Compare record counts after sync.
- Optionally compute a stable hash:
  - Sort records by ID
  - Serialize canonical JSON
  - Hash with SHA-256
- Compare version markers (timestamp or monotonic counter).

## Failure Simulation

- Kill during sync and confirm next run detects stale store.
- Corrupt JSONL line and verify fallback to DB or git history.
- Force a Git commit failure and verify you surface a clear error.
- Simulate disk-full and verify a clean error + no partial JSONL.
