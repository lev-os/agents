# Root router + multi-index Codebase Memory pattern

Use this when one Hermes runtime manages multiple initiatives from a shared root (for example `/opt/data`) and the agent should pick the right Codebase Memory project by Telegram topic, initiative, or workspace path.

## Pattern

1. Keep the root graph lightweight.
   - Add a root `.cbmignore` that excludes heavy repo/data/cache directories.
   - Index individual workspaces separately instead of relying on one huge root graph.

2. Create per-workspace `.cbmignore` files.
   - Start narrow: source, docs, routing/config, schemas, flows, and high-signal markdown.
   - Exclude generated state, caches, vendored dependencies, workshop dumps, binary assets, and large historical exports.
   - If indexing runs hot or stalls, tighten the ignore file first, then reindex.

3. Document routing in the root `AGENTS.md`.
   - Map topic id -> initiative -> workspace path.
   - Map topic/scope -> Codebase Memory project name.
   - Add a broad/general-topic rule: when in a general/root topic, the agent should know all initiative indexes and choose the right one per query.

4. Verify each project after indexing.
   - `list_projects` should show all expected project names and root paths.
   - Run `search_code` against each project with a known term.
   - Reindex the root after editing root router docs and verify the new section is searchable.

## CLI quirks observed

- `search_code` CLI JSON uses `pattern`, not `query`:

```bash
codebase-memory-mcp cli search_code '{"project":"opt-data","pattern":"Codebase Memory index routing","limit":5}'
```

- `index_status '{}'` can error with `project not found or not indexed`; pass a project name or use `list_projects` first.

## CPU-aware benchmark loop

When benchmarking indexing, monitor child CPU/RSS through `/proc/<pid>/stat`, set a hard timeout, and kill/retry with tighter ignores if it becomes a hog. Capture:

- wall time
- exit code
- whether killed by timeout
- CPU samples
- RSS samples
- output tail with final project stats

## Example routing text for root `AGENTS.md`

```md
## Codebase Memory index routing

Use Codebase Memory for code/docs graph search before broad filesystem scans when an indexed project fits the request. Pick the index that matches the active topic/scope:

- Root/router/all-locations index: `opt-data` -> `/opt/data`
- Lev index: `opt-data-lev` -> `/opt/data/lev`
- Kingly/Argo internal OS index: `opt-data-repos-kingly-internal-os` -> `/opt/data/repos/kingly-internal-os`

For a general/root topic, be aware of all three indexes and choose among them based on the ask.
```
