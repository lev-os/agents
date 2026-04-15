# Case Studies: Three Real Frankensearch Integrations

## Case Study 1: xf (X Archive Finder)

**Context:** CLI tool for searching personal X/Twitter archives. Had hand-rolled search
with FNV hashing, manual SIMD, manual RRF fusion.

**Migration approach:** Full cutover in one day (Feb 15, 2026), feature-gated with 62 cfg gates.

### What Was Replaced

| Legacy Component | Lines | Replacement |
|------------------|-------|-------------|
| FNV-1a hash embedding | ~40 | `frankensearch_embed::HashEmbedder` delegate |
| Manual SIMD dot product | ~30 | `frankensearch_index::dot_product_f16_f32` |
| Manual RRF fusion | ~70 | `frankensearch_fusion::rrf_fuse` |
| Raw FastEmbed backend | ~50 | `frankensearch_embed::FastEmbedEmbedder` delegate |
| Model2Vec inline embed | ~30 | `frankensearch_embed::Model2VecEmbedder` delegate |
| **Total removed** | **573** | **84 lines added** |

### What Was Retained (Not Migrated)

- `FrankensearchEmbedderAdapter` — sync-to-async bridge (xf is sync internally)
- `FrankensearchRerankerAdapter` — sync-to-async bridge
- Custom `blend_two_tier()` — no frankensearch equivalent at xf's abstraction level
- Tantivy BM25 — separate from frankensearch (manages its own schema)
- StaticMrlEmbedder, FlashRankReranker, MxbaiReranker — no frankensearch equivalents

### Critical Bugs Encountered

1. **asupersync type mismatch**: xf depended on asupersync from crates.io while frankensearch used a path dep. `Cx` became two different types. Fixed with `[patch]` section.

2. **RRF precision divergence**: f32 vs f64 accumulation caused parity test failures. Fixed by NOT re-sorting after receiving frankensearch results.

3. **Cross-model embedding dedup collision**: Two-tier pipeline's fast model stored content hashes; quality model saw those hashes and skipped documents. Fixed by adding model-scoped hash lookups.

4. **Double-offset in hybrid search**: Offset applied twice — once in `rrf_fuse()` and again in common pagination. Fixed by passing 0 to fusion, letting caller handle offset.

5. **doc_id format mismatch**: Tantivy used `{chat_id}_{timestamp}_{subsec_nanos}_{sender}` while embeddings used `grok_{chat_id}_{idx}`. RRF couldn't join matching documents. Fixed by unifying format.

### Key Metrics

- **Integration time**: 1 day (foundation laid over preceding weeks)
- **Code delta**: -573, +84 (net -489 lines)
- **Test results**: All existing tests pass; migration parity tests added
- **Performance**: No measurable regression

### Lesson

xf's migration was the cleanest because it went ALL IN: replace everything, validate with parity tests, cut over in one commit. The feature-gated approach (62 cfg gates) created cleanup debt but allowed safe parallel validation.

**xf does NOT use `TwoTierSearcher`** — it maintains a custom `blend_two_tier()` function. This is an area for further optimization.

---

## Case Study 2: CASS (Coding Agent Session Search)

**Context:** TUI-based search tool for AI coding session history. Needs synchronous iterator-based search for the TUI, in-memory f16 vectors.

**Migration approach:** Partial (~15% by volume). Architectural mismatch prevents full migration.

### Integration Architecture

```
CASS Search Stack:
├── query.rs (10,274 lines) — Custom orchestration, caching, pagination
├── two_tier_search.rs (1,333 lines) — Custom sync two-tier with in-memory vectors
├── vector_index.rs (500 lines) — Semantic filter + vector search
├── tantivy.rs (150 lines) — Thin wrapper around frankensearch TantivyIndex
├── reranker.rs (150 lines) — frankensearch::SyncRerank re-export
├── embedder_registry.rs (695 lines) — DUPLICATE of frankensearch registry
└── hash_embedder.rs, fastembed_embedder.rs — Via Embedder trait
```

### What CASS Uses From Frankensearch

- All tantivy types via frankensearch re-exports (enforced by CI test)
- `SearchFilter` trait implementation (direct, no adapter)
- `SyncTwoTierSearcher` + `InMemoryTwoTierIndex` for sync search path
- `RrfConfig` and `rrf_fuse()` for fusion
- Embedder trait implementations (Hash, Model2Vec, FastEmbed)
- Reranker via `SyncRerank`

### Why Full Migration Was Blocked

**Architectural mismatch:** frankensearch's `TwoTierSearcher` is async with file-backed FSVI storage. CASS needs sync iteration for the TUI with in-memory f16 vectors. The `SyncTwoTierSearcher` and `InMemoryTwoTierIndex` were created specifically to bridge this gap but don't cover the full orchestration.

### Known Problems

1. **Duplicate embedder registry** (695 lines): CASS maintains its own model registry because `rch` (remote compilation helper) can't resolve sibling path deps. Registry drift risk.

2. **Two incompatible doc_id schemes**: `DocumentId` enum (`s:id`, `t:id:turn`, `c:id:turn:block`) vs `SemanticDocId` pipe-delimited format (`m|msg_id|chunk|agent|...`). No type safety between them.

3. **FTS5 rusqlite fallback**: FrankenSQLite's in-memory FTS5 can't read on-disk shadow tables. Retain rusqlite for MATCH queries — binary bloat and consistency risk.

4. **search_in_flight blocking**: Initial empty-query search took 60+ seconds with 41K conversations. The `search_in_flight` flag blocked user queries. Fixed by generation counter pattern.

5. **Conditional search paths**: Sometimes uses `SyncTwoTierSearcher`, sometimes falls back to direct tantivy. Code paths not equally tested.

### Lesson

CASS demonstrates that **not every project can fully adopt `TwoTierSearcher`**. When fundamental architectural requirements (sync TUI, in-memory vectors) don't match frankensearch's primary async/file-backed model, the right approach is to adopt the building blocks (traits, embedders, fusion, SIMD) while keeping domain-specific orchestration.

The duplicate embedder registry is the biggest maintenance risk — it will drift.

---

## Case Study 3: mcp_agent_mail_rust

**Context:** MCP server for multi-agent coordination. Search is a secondary feature for finding messages/threads.

**Migration approach:** Bridge pattern with `fs_bridge.rs` module. Local two-tier implementation retained.

### Integration Architecture

```
mcp_agent_mail_rust Search Stack:
├── search_service.rs (6,405 lines) — Unified entry point, #[cfg(feature = "hybrid")]
├── search_fs_bridge.rs (648 lines) — Re-exports with Fs prefix, adapters, converters
├── search_model2vec.rs (288 lines) — Thin wrapper around frankensearch Model2VecEmbedder
├── search_auto_init.rs (685 lines) — Zero-config embedder stack setup
├── search_fusion.rs (1,169 lines) — RRF fusion with frankensearch-backed path
├── search_two_tier.rs — Local two-tier implementation (STILL ACTIVE)
└── FlashRank reranker integration via frankensearch-rerank
```

### The Bridge Pattern

mcp_agent_mail uses a dedicated bridge module with these conventions:

1. **Fs-prefixed re-exports**: `FsTwoTierSearcher`, `FsScoredResult`, etc. to avoid name collisions
2. **Doc ID conversion**: Domain `i64` ↔ frankensearch `String` via `doc_id_to_string()`/`doc_id_from_string()`
3. **Config conversion**: Bidirectional `to_fs_config()`/`from_fs_config()` with documented precision loss
4. **SyncEmbedderAdapter**: Wraps sync embedders for frankensearch's async trait
5. **Error mapping**: `map_fs_error()` translates all SearchError variants

### What frankensearch Provides (Actually Used)

- SIMD dot product: `dot_product_f16_f32()` — delegated from local search
- Score normalization: `normalize_scores()` — used in local blend
- Model2Vec embedder: Thin wrapper around frankensearch's implementation
- FlashRank reranker: Full integration with lazy init and env configuration
- RRF fusion: frankensearch-backed path in `search_fusion.rs`

### What frankensearch Provides (Bridge Ready, Not Yet Active)

- `TwoTierSearcher` — bridge adapters exist but not called in production paths
- `IndexBuilder` — `create_fs_embedder_stack()` exists but not invoked
- `EmbedderStack` — constructed in auto_init but used only for diagnostics

### Critical Bugs Encountered

1. **Absolute paths in Cargo.toml** (46 occurrences of `/dp/`): Broke CI/CD and cross-machine builds. Fixed by converting to relative paths.

2. **Fresh startup DB corruption**: FrankenSQLite JIT opcode issues caused malformed database within seconds. Search backfill then failed.

3. **ScoredResult schema drift**: When frankensearch added `explanation` field, all bridge constructors needed updating.

4. **Async probe holding RwLock**: Original sync probe held `RwLock` across async work. Fixed by `entries_snapshot()` copy.

5. **Quality refinement empty results**: `select_best_two_tier_results` returned empty when quality tier produced nothing, even though fast tier had valid results. Fixed to prefer initial-phase results.

6. **Intermediate crate boundary overhead**: The `mcp-agent-mail-search-core` separation from `mcp-agent-mail-db` created ~30 lines of type mapping per test. Eventually abandoned (inlined modules).

### Lesson

mcp_agent_mail demonstrates the **bridge-first** approach: create thorough conversion utilities, comprehensive tests, and Fs-prefixed re-exports BEFORE attempting to replace the production search path. The bridge pattern is safe but creates maintenance burden when upstream types evolve (schema drift on `ScoredResult`).

The local two-tier implementation is still the production path — frankensearch is used for helpers only. This is the least-complete integration of the three.

---

## Cross-Cutting Lessons

### 1. Version Alignment Is Not Optional

All three projects hit asupersync version conflicts. The fix is always: ensure one copy of asupersync in the dep tree via `[patch]` or consistent path deps.

### 2. RRF Fusion Is the Highest-Value Migration Target

Every project that replaced its custom RRF with `frankensearch_fusion::rrf_fuse()` eliminated bugs (f32 precision, tie-breaking, dedup key inconsistency). Do this first.

### 3. Sync-to-Async Bridges Are Unavoidable

None of the three consumer projects use asupersync natively. All needed bridge adapters. This is a design trade-off in frankensearch's API — the async `Embedder` trait provides proper cancellation but requires bridging.

### 4. Feature-Gated Migration Works But Creates Cleanup Debt

xf's 62 cfg gates validated correctness but took effort to clean up. Limit the migration period — don't leave cfg gates in for weeks.

### 5. Doc ID Encoding Must Be Unified Early

Both CASS and xf had doc_id format mismatches (Tantivy vs embeddings, multiple ID schemes). Unify the encoding before integrating, not after.

### 6. Test That No Direct Tantivy Imports Remain

CASS's CI test that scans source for `use tantivy::` is an excellent pattern. Adopt it to prevent drift.

### 7. Schema Drift Between Bridge and Upstream Is Real

When frankensearch adds fields to `ScoredResult`, every bridge constructor breaks. Consider generating bridge code from frankensearch's types, or accept the maintenance cost.

### 8. Path Deps vs Git Deps Must Match Your Workflow

- **Active development**: Path deps (immediate access to upstream changes)
- **CI/CD**: Git deps with pinned rev (reproducible builds)
- **Release**: Published crate versions (stable)

Switching between these at different lifecycle stages is normal and expected.
