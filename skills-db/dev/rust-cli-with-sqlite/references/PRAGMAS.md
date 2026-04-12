# SQLite PRAGMA Guide

## Baseline (Most Projects)

```
journal_mode=WAL
synchronous=NORMAL
foreign_keys=ON
busy_timeout=5000
wal_autocheckpoint=1000
```

## Durability High (Mission Critical)

```
journal_mode=WAL
synchronous=FULL
fullfsync=ON   # macOS only
```

## Performance High (Accept Risk)

```
synchronous=OFF
journal_mode=MEMORY
```

## Tuning Notes

- WAL improves read/write concurrency and reduces writer blocking.
- NORMAL reduces fsync frequency; may lose last transactions on power loss.
- FULL maximizes durability; slower on some disks.
- fullfsync is required on macOS for true durability.
- cache_size can improve read speed for large datasets.
- ANALYZE helps the query planner use indexes correctly.
- VACUUM rebuilds the DB file and reclaims space (not frequent).
- Use transactions for batch inserts/updates; commit once.
- Use EXPLAIN QUERY PLAN to verify index usage.
- Consider raising cache_size for hot datasets (memory tradeoff).
- Checkpoint WAL at exit or after N transactions to bound WAL growth.
- journal_mode=MEMORY + synchronous=OFF is fast but unsafe for power loss.
- synchronous=OFF risks losing the last transactions; acceptable only for low-value data.
- FULL in WAL mode issues extra fsyncs on commit for maximum durability.

## Validate

```
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA integrity_check;
```
