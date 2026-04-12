# Sync Strategy Patterns

## Pattern A: DB First (Recommended)

- SQLite is the source of truth.
- JSONL is a periodic export for git + human review.
- Sync triggers: on command, on exit, or on timer/quiet period.
  - Avoid per-record syncs; batch for throughput.
  - If sync is slow, run it asynchronously and show progress.

Pseudo:
```
if sync_needed:
  lock
  begin read transaction
  export DB snapshot to JSONL temp
  fsync temp
  rename to JSONL
  update last_synced_at in DB
  unlock
```

## Pattern B: JSON First

- JSONL is the source of truth (git-first workflows).
- SQLite is a cache for fast queries.
- On startup: if JSONL changed, rebuild DB.
  - Manual edits to JSONL are allowed; validate then rebuild DB.

Pseudo:
```
if jsonl_version > db_version:
  rebuild DB from JSONL
```

## Pattern C: Dual (Use Only If Required)

- Each command chooses a primary store.
- Always write version markers to both stores.
- Never sync both directions in one command unless you can detect cycles.

## Version Markers

Keep a single version string or counter in both stores:
- DB: `meta.last_synced_at` or `meta.version`
- JSONL: header record or sidecar `.meta.json`

Compare on startup to decide which store is newer.

## Eventual Consistency

- Brief divergence between DB and JSONL is normal.
- Favor fast eventual consistency over strict realtime.
- Use a quiet-period timer to batch updates and avoid commit storms.
- Design commands to tolerate short lag windows.

## Concurrency

- Use a lock file for all syncs.
- Use WAL to allow snapshot reads during writes.
- Do not allow two syncs to run in parallel.

## Startup Reconcile (Suggested)

```
load db_version
load json_version (or git commit timestamp)
if json_version > db_version:
  rebuild DB from JSONL
elif db_version > json_version:
  export JSONL from DB
```

## Lag Windows (Practical Guidance)

- If DB is source of truth, prefer DB reads for "latest" results.
- JSONL can lag by milliseconds to seconds depending on sync cadence.
- Keep the window small; document expected lag in README/help text.

## Git Discipline (When JSONL is Versioned)

- Commit on a cadence (timer/quiet period), not per record.
- Include record counts/version in commit messages.
- Use `.gitattributes` to keep JSONL line endings consistent (LF).

## JSONL Size + Throughput

- Stream JSONL reads/writes; avoid loading full files into memory.
- Consider splitting large JSONL by date/category to keep diffs manageable.
- For append-only workflows, lock + append + fsync; for full export, use temp+rename.

## Responsiveness

- For large imports/exports, print periodic progress.
- Avoid long blocking operations without feedback.
