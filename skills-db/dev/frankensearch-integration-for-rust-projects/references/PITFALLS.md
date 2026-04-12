# Comprehensive Pitfall Catalog

Every pitfall in this document was discovered in a real production integration. Each entry
includes the root cause, how it manifested, and the fix.

---

## Category 1: Dependency Resolution

### P1.1: asupersync Cx Type Mismatch (ALL THREE PROJECTS)

**Severity:** CRITICAL (won't compile)

**Root cause:** Rust treats the same crate from two different sources as different types.
If your project depends on `asupersync` from crates.io and frankensearch depends on it
from git/path, `Cx` is two different types.

**Manifestation:**
```
error[E0308]: mismatched types
  expected `&asupersync::Cx`, found `&asupersync::Cx`
```

**Fix:**
```toml
[patch.crates-io]
asupersync = { path = "../asupersync" }
[patch."https://github.com/Dicklesworthstone/asupersync"]
asupersync = { path = "../asupersync" }
```

**Prevention:** Always run `cargo tree -i asupersync` after adding frankensearch.

### P1.2: Path Deps Not Available on Remote Workers (xf, CASS)

**Severity:** HIGH (blocks CI/remote builds)

**Root cause:** `path = "../frankensearch"` only works when the sibling directory exists.
Remote build workers (rch) and CI don't have sibling repos checked out.

**Fix:** Use path deps for development, git deps for CI/releases. Document this in your README.

### P1.3: Stale Git Rev Missing New Types (CASS)

**Severity:** HIGH (won't compile)

**Root cause:** frankensearch added `InMemoryTwoTierIndex`, `SyncTwoTierSearcher` as local
uncommitted changes. CASS's Cargo.toml pointed at a git rev that didn't have them.

**Fix:** Update git rev to include new types, or use path dep during active development.

**Prevention:** When upstream and downstream repos are both in active development, always
use path deps.

---

## Category 2: Precision and Scoring

### P2.1: f32 vs f64 RRF Score Divergence (xf)

**Severity:** MEDIUM (wrong ordering for tied scores)

**Root cause:** frankensearch accumulates RRF scores in f64 for precision. Legacy code
used f32. After truncation, tie-breaking differs by 1 ULP.

**Fix:** Never re-sort results after receiving them from frankensearch.

### P2.2: f64→f32 Config Narrowing (mcp_agent_mail)

**Severity:** LOW (negligible for weight values)

**Root cause:** Converting `quality_weight: f64` → `f32` in config bridge loses precision.

**Fix:** Acceptable for config values (weights are ~0.7). Never narrow SCORES.

### P2.3: NaN Bypasses All Threshold Checks (frankensearch code review)

**Severity:** HIGH (silent data corruption)

**Root cause:** `NaN < 0.5` is `false`. `NaN >= 0.5` is also `false`. NaN values bypass
every comparison-based guard.

**Fix:** Guard with `.is_finite()` before any comparison:
```rust
if quality_weight.is_finite() {
    config.quality_weight = quality_weight.clamp(0.0, 1.0);
}
```

### P2.4: Double-Offset in Hybrid Pagination (xf)

**Severity:** HIGH (users skip 2x intended results)

**Root cause:** Offset applied in `rrf_fuse()` AND in the caller's pagination.

**Fix:** Pass 0 as offset to `rrf_fuse()`, let caller handle pagination.

---

## Category 3: Document Identity

### P3.1: doc_id Format Mismatch Between Tantivy and Embeddings (xf)

**Severity:** CRITICAL (RRF can't join matching documents)

**Root cause:** Tantivy used `{chat_id}_{timestamp}_{nanos}_{sender}` while embeddings
used `grok_{chat_id}_{idx}`. Same document had different IDs in different backends.

**Fix:** Unify doc_id format before integration. Use a single encoding function.

### P3.2: Multiple Incompatible doc_id Schemes (CASS)

**Severity:** MEDIUM (type safety risk)

**Root cause:** `DocumentId` enum (`s:id`, `t:id:turn`, `c:id:turn:block`) and
`SemanticDocId` pipe-delimited format coexist in the same codebase.

**Fix:** Unify to one scheme. If multiple ID formats are needed, use a single enum with
proper parsing.

### P3.3: Cross-Model Embedding Dedup Collision (xf)

**Severity:** HIGH (quality model skips already-indexed documents)

**Root cause:** Hash table for "already embedded" detection wasn't scoped by model_id.
Quality model saw fast model's hashes and skipped documents.

**Fix:** Scope all embedding hash lookups by model_id:
```rust
fn load_hashes_for_model(doc_id: &str, model_id: &str) -> HashSet<ContentHash>;
```

### P3.4: i64 vs u64 Doc ID Conversion (mcp_agent_mail)

**Severity:** LOW (potential edge case)

**Root cause:** search-core uses `i64` doc IDs, db layer uses `u64`. frankensearch uses
`String`. The i64 variant correctly rejects negative strings; the u64 variant doesn't.

**Fix:** Validate all doc_id conversions; reject invalid values explicitly.

---

## Category 4: Schema and API Evolution

### P4.1: ScoredResult Field Addition Breaks Bridge (mcp_agent_mail)

**Severity:** MEDIUM (compilation failure on upstream update)

**Root cause:** When frankensearch added `explanation: Option<HitExplanation>` to
`ScoredResult`, all bridge constructors that used struct literal syntax failed.

**Fix:** Add `explanation: None` to all constructors.

**Prevention:** Use struct update syntax:
```rust
ScoredResult { doc_id, score, source, ..ScoredResult::default() }
```

### P4.2: Missing Tantivy Re-Exports (CASS)

**Severity:** MEDIUM (blocks migration of some functionality)

**Root cause:** frankensearch re-exported 17 of ~25 needed tantivy types. Missing:
`Score`, `TextOptions`, `TextFieldIndexing`, `STORED`, `TEXT`, `STRING`, `MmapDirectory`,
`FuzzyTermQuery`, `PhrasePrefixQuery`, `NgramTokenizer`.

**Fix:** Request missing re-exports from frankensearch, or temporarily import tantivy
directly (with a TODO to remove).

### P4.3: Duplicate Embedder Registry Drift (CASS)

**Severity:** MEDIUM (maintenance burden)

**Root cause:** CASS maintains a 695-line local embedder registry because rch can't resolve
path deps. This registry can drift from frankensearch's canonical registry.

**Fix:** Either expose frankensearch's registry as a public API, or auto-generate the local
registry from frankensearch source in build.rs.

---

## Category 5: Async/Sync Impedance

### P5.1: Async Probe Holding RwLock (mcp_agent_mail)

**Severity:** HIGH (potential deadlock)

**Root cause:** A synchronous search probe held an `RwLock` while doing work that became
async. When the probe was made async, the lock was held across an await point.

**Fix:** Copy data out before entering async context:
```rust
// WRONG: lock held across await
let guard = index.read();
let result = guard.search(&cx, query).await; // Lock held during await!

// RIGHT: snapshot and release
let snapshot = index.read().entries_snapshot();
drop(guard);
let result = snapshot.search(&cx, query).await;
```

### P5.2: Cx::for_testing() in Production (xf)

**Severity:** LOW (works but bypasses cancellation)

**Root cause:** Sync embedders wrapped in async adapters use `Cx::for_testing()` for every
embed call. This is lightweight but doesn't propagate cancellation from the caller.

**Fix:** Acceptable for CLI tools. For long-running services, create a real `Cx` from
your runtime.

---

## Category 6: Search Behavior

### P6.1: search_in_flight Flag Blocking User Input (CASS)

**Severity:** HIGH (60-second TUI freeze)

**Root cause:** Initial empty-query search took 60+ seconds with 41K conversations. The
`search_in_flight` boolean prevented user-typed queries from executing.

**Fix:** Replace boolean flag with generation counter:
```rust
// WRONG: boolean gate
if !search_in_flight { start_search(); search_in_flight = true; }

// RIGHT: generation counter (fire-and-forget, discard stale)
generation += 1;
let gen = generation;
start_search(gen);
// In callback: if gen != current_generation { discard; }
```

### P6.2: Quality Refinement Returns Empty (mcp_agent_mail)

**Severity:** HIGH (search returns nothing despite valid fast results)

**Root cause:** `select_best_two_tier_results()` returned the quality-tier results even
when they were empty, discarding valid fast-tier results.

**Fix:** Always prefer initial-phase results when refinement produces nothing:
```rust
fn select_best(initial: &[ScoredResult], refined: &[ScoredResult]) -> Vec<ScoredResult> {
    if refined.is_empty() {
        initial.to_vec()  // Keep fast results on refinement failure
    } else {
        refined.to_vec()
    }
}
```

### P6.3: Type-Filtered Semantic Search Broken (xf)

**Severity:** HIGH (--types flag silently returns no results)

**Root cause:** `VectorIndexCache.load()` left `type_counts` empty. `has_embeddings_for_types()`
always returned false.

**Fix:** Compute type counts during index load:
```rust
impl VectorIndex {
    pub fn type_counts(&self) -> HashMap<DocType, usize> { ... }
}
```

---

## Category 7: Build and Infrastructure

### P7.1: Absolute Paths in Cargo.toml (mcp_agent_mail)

**Severity:** HIGH (breaks all cross-machine builds)

**Root cause:** 46 occurrences of `/dp/` absolute paths in Cargo.toml. Worked on the
developer's machine, failed everywhere else.

**Fix:** Convert all to relative paths: `/dp/frankensearch` → `../frankensearch`

### P7.2: CI Missing Sibling Repo Checkouts (mcp_agent_mail)

**Severity:** HIGH (CI broken since inception)

**Root cause:** Cargo.toml referenced 5 sibling repos via relative paths that CI didn't
check out.

**Fix:** Add explicit checkout steps for each sibling repo in CI config.

### P7.3: FSVI Temp Directory Lifetime (CASS)

**Severity:** MEDIUM (silent empty results if temp dir deleted)

**Root cause:** FSVI files stored in temp directory, kept alive by `_tmpdir` field.
If temp dir gets cleaned up externally, search returns empty results silently.

**Fix:** Use persistent FSVI path, or document the lifetime requirement.

### P7.4: FrankenSQLite FTS5 Incompatibility (CASS)

**Severity:** MEDIUM (requires rusqlite fallback)

**Root cause:** FrankenSQLite's in-memory FTS5 can't read on-disk shadow tables needed
for MATCH queries.

**Fix:** Retain rusqlite for FTS5 MATCH operations. File upstream issue for FrankenSQLite.

### P7.5: FrankenSQLite INSERT...SELECT UPSERT Limitation (CASS)

**Severity:** HIGH (cass index completely broken)

**Root cause:** FrankenSQLite's `INSERT ... SELECT` fallback doesn't support `UPSERT/RETURNING`.
This broke the entire CASS indexing pipeline.

**Fix:** Fix in FrankenSQLite upstream. No workaround in the consumer.

---

## Category 8: Data Integrity

### P8.1: Backfill Skip on Zero DB Count (mcp_agent_mail)

**Severity:** HIGH (stale index marked up-to-date)

**Root cause:** Backfill logic: `if existing_count >= db_count { skip }`. When DB was
corrupted, `db_count=0`, so backfill was skipped — leaving stale Tantivy index.

**Fix:** Never treat `db_count=0` as "index is up-to-date":
```rust
if db_count == 0 {
    log::warn!("DB reports 0 documents — possible corruption, forcing reindex");
    return ReindexNeeded;
}
```

### P8.2: Embedding Validation Before Index Write (xf)

**Severity:** MEDIUM (corrupted vectors in index)

**Root cause:** Embeddings written to vector index without validation. NaN or zero-length
vectors could be stored.

**Fix:** Validate before write:
```rust
fn validate_embedding(vec: &[f32]) -> bool {
    !vec.is_empty() && vec.iter().all(|v| v.is_finite()) && vec.iter().any(|v| *v != 0.0)
}
```

### P8.3: Unbounded Embedding Reuse Cache (xf)

**Severity:** MEDIUM (memory growth)

**Root cause:** Embedding cache grew without bound during indexing of large corpora.

**Fix:** Bound the cache: `LruCache::new(NonZeroUsize::new(10_000).unwrap())`
