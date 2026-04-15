# Recovery and Rebuild

## Commands to Provide

- `import-jsonl`: rebuild SQLite from JSONL
- `export-jsonl`: dump SQLite to JSONL

## Versioning

Store a version marker in both stores:
- DB: `meta.version` or `meta.last_synced_at`
- JSONL: header record or `.meta.json`

On startup:
```
if json_version > db_version: rebuild DB
if db_version > json_version: export JSONL
```

## Safe Rebuild Flow

1. Lock
2. Validate source (JSONL parse or DB integrity_check)
3. Rebuild to a new temp DB
4. Swap DB atomically
5. Update version markers
6. Unlock

## Git Fallback

- If JSONL is corrupt, restore from a prior Git commit.
- If DB is corrupt, rebuild from the latest valid JSONL.
- Keep old JSONL on export failures; never leave partial files.
- JSONL is human-editable; document safe manual edit + re-import flow.
- Consider pushing Git remote for off-machine backup (3-2-1 mindset).
