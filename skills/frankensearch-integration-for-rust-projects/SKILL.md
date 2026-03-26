---
name: frankensearch-integration-for-rust-projects
description: >-
  Complete guide for integrating frankensearch hybrid search into Rust projects.
  Covers fresh integration, fixing stalled/buggy integrations, and migrating from
  ad-hoc search. Use when: frankensearch, hybrid search, two-tier search,
  TwoTierSearcher, IndexBuilder, EmbedderStack, RRF fusion, semantic search
  integration, search migration, search broken, search stalled.
metadata:
  filePattern:
    - "**/Cargo.toml"
    - "**/search*.rs"
    - "**/hybrid*.rs"
    - "**/embed*.rs"
    - "**/vector*.rs"
    - "**/fs_bridge*.rs"
    - "**/two_tier*.rs"
    - "**/rerank*.rs"
    - "**/fusion*.rs"
  bashPattern:
    - "cargo.*frankensearch"
    - "frankensearch"
  priority: 80
---

# Frankensearch Integration for Rust Projects

> **The Cardinal Rule:** Use frankensearch's built-in `TwoTierSearcher` for hybrid search.
> Do NOT roll your own RRF fusion, score blending, or progressive search orchestration.
> Every project that built ad-hoc search eventually ripped it out and replaced it with
> frankensearch's canonical implementation. Learn from their pain.

## Quick Assessment: Where Are You?

```
1. NO SEARCH YET          → Phase 1: Fresh Integration (fastest path)
2. AD-HOC SEARCH EXISTS   → Phase 2: Migration (replace custom with canonical)
3. INTEGRATION STALLED    → Phase 3: Diagnosis & Repair (unstick the build)
4. WORKS BUT SUBOPTIMAL   → Phase 4: Optimization & Audit (use higher abstractions)
```

Pick your phase and follow it. Each phase is self-contained.

---

## Phase 1: Fresh Integration (Green-Field)

### Step 1: Add Dependencies

```toml
# Cargo.toml — choose the right feature set
[dependencies]
frankensearch = { path = "../frankensearch/frankensearch", features = ["hybrid"] }
# Or from git:
# frankensearch = { git = "https://github.com/Dicklesworthstone/frankensearch", features = ["hybrid"] }
```

**Feature Flag Decision Table:**

| Goal | Feature Set | What You Get |
|------|-------------|--------------|
| CI smoke tests, zero model deps | `default` (`hash`) | Hash embedder only, no ML models |
| Semantic search only | `semantic` | hash + model2vec + fastembed embedders |
| Hybrid lexical + semantic (RECOMMENDED) | `hybrid` | semantic + Tantivy BM25 + RRF |
| Hybrid + persistent metadata | `persistent` | hybrid + FrankenSQLite storage |
| Full stack with reranking | `full` | persistent + durability + rerank + ANN + download |

**CRITICAL: asupersync Version Alignment**

frankensearch uses `asupersync` (NOT tokio). If your project also depends on asupersync,
you MUST ensure both use the same crate instance. Rust treats crates from different sources
as different types — `Cx` from crates.io != `Cx` from git.

```toml
# If frankensearch uses path dep to asupersync, your project must too:
asupersync = { path = "../asupersync" }

# OR force alignment with [patch]:
[patch."https://github.com/Dicklesworthstone/frankensearch.git"]
asupersync = { path = "../asupersync" }
```

**If your project uses tokio:** You need sync-to-async bridge adapters. See [BRIDGE-PATTERNS.md](references/BRIDGE-PATTERNS.md).

### Step 2: Build the Index

```rust
use std::sync::Arc;
use frankensearch::{EmbedderStack, IndexBuilder, TwoTierConfig};

// Auto-detect available models (potion-128M fast + MiniLM quality)
let stack = EmbedderStack::auto_detect()?;

// Build index from your documents
let stats = IndexBuilder::new("./my_index")
    .with_embedder_stack(stack)
    .add_document("doc-1", "Document content here")
    .add_document("doc-2", "More content here")
    .build(&cx)
    .await?;

println!("Indexed {} docs, quality tier: {}", stats.doc_count, stats.has_quality_index);
```

### Step 3: Create the Searcher

```rust
use frankensearch::{TwoTierIndex, TwoTierSearcher, TwoTierConfig, EmbedderStack};

let config = TwoTierConfig::default().with_env_overrides();
let index = Arc::new(TwoTierIndex::open("./my_index", config.clone())?);
let stack = EmbedderStack::auto_detect()?;

let searcher = TwoTierSearcher::new(index, stack.fast_arc(), config)
    .with_quality_embedder(stack.quality_arc().unwrap());

// Optional: add lexical backend for hybrid search
#[cfg(feature = "lexical")]
{
    let tantivy = Arc::new(TantivyIndex::open_or_create("./my_index/tantivy")?);
    searcher = searcher.with_lexical(tantivy);
}
```

### Step 4: Execute Search

```rust
// Simple: collect all results
let (results, metrics) = searcher
    .search_collect(&cx, "my query", 10)
    .await?;

for result in &results {
    println!("{}: {:.3} ({})", result.doc_id, result.score, result.source);
}
println!("Phase 1: {:.1}ms, Phase 2: {:.1}ms", metrics.phase1_total_ms, metrics.phase2_total_ms);

// Progressive: get fast results first, then refined
let metrics = searcher.search(&cx, "my query", 10,
    |doc_id| load_text_from_db(doc_id),  // text callback for reranking
    |phase| match phase {
        SearchPhase::Initial { results, latency, .. } => {
            // Show these immediately (~15ms)
            display_results(&results);
        }
        SearchPhase::Refined { results, rank_changes, .. } => {
            // Update with better ranking (~150ms)
            display_results(&results);
        }
        SearchPhase::RefinementFailed { initial_results, error, .. } => {
            // Graceful degradation: keep initial results
            log::warn!("Refinement failed: {error}, keeping initial results");
        }
    }
).await?;
```

### Step 5: Map Document IDs

frankensearch uses `String` doc IDs. Your domain model likely has structured IDs.
Create a thin mapping layer:

```rust
// DO: Simple string encoding
fn to_fs_doc_id(msg_id: i64) -> String { msg_id.to_string() }
fn from_fs_doc_id(id: &str) -> Option<i64> { id.parse().ok() }

// DO: Composite key for multi-type documents
fn to_fs_doc_id(kind: DocKind, id: u64) -> String {
    format!("{}\x1f{id}", kind.prefix())  // Use unit separator
}
fn from_fs_doc_id(id: &str) -> Option<(DocKind, u64)> {
    let (prefix, num) = id.split_once('\x1f')?;
    Some((DocKind::from_prefix(prefix)?, num.parse().ok()?))
}

// DON'T: Multiple incompatible ID schemes in the same project
// DON'T: Pipe-delimited strings with 8+ fields (fragile parsing)
```

---

## Phase 2: Migration (Replace Ad-Hoc Search)

### The Migration Anti-Pattern Hall of Shame

These are real mistakes from three production integrations. Every one caused bugs.

| Anti-Pattern | What Happened | Fix |
|-------------|---------------|-----|
| Hand-rolled RRF fusion | Score precision drift (f32 vs f64), different tie-breaking | Use `frankensearch_fusion::rrf_fuse()` |
| Manual SIMD dot product | Subtle NaN handling differences, maintenance burden | Use `frankensearch_index::simd::dot_product_f16_f32()` |
| Custom score blending | Off-by-one normalization, no NaN guards | Use `TwoTierSearcher` built-in blend |
| Custom progressive search | Missing graceful degradation, no `RefinementFailed` path | Use `TwoTierSearcher.search()` with phase callback |
| Separate embedder registries | Registry drift between project and frankensearch | Use `EmbedderStack::auto_detect()` |
| Direct tantivy imports | Schema version mismatch, field name drift | Import all tantivy types through frankensearch re-exports |

### Migration Strategy: Feature-Gated Cutover

**Proven approach from xf (573 lines deleted, zero regressions):**

1. **Add frankensearch deps alongside existing code** (no removal yet)
2. **Create `cfg(feature = "frankensearch-migration")` gates** around new paths
3. **Build migration parity tests** — run both old and new paths, compare results
4. **Validate parity** — scores within epsilon, same result sets, same ordering
5. **Cut over** — remove all cfg gates and legacy code in one commit
6. **Verify** — `cargo test`, clippy, UBS scan on the cleanup commit

```rust
// During migration: run both paths and compare
#[cfg(feature = "frankensearch-migration")]
let fs_results = frankensearch_fusion::rrf_fuse(&lexical_hits, &semantic_hits, &config);

#[cfg(not(feature = "frankensearch-migration"))]
let fs_results = legacy_rrf_fuse(&lexical_hits, &semantic_hits);

// Parity check (test only):
#[cfg(all(feature = "frankensearch-migration", test))]
assert_results_equivalent(&fs_results, &legacy_results, 1e-6);
```

### What to Replace (Priority Order)

| Component | Replace With | Why First |
|-----------|-------------|-----------|
| RRF fusion function | `frankensearch_fusion::rrf_fuse()` | Highest bug surface, f64 precision |
| SIMD dot product | `frankensearch_index::simd::dot_product_f16_f32()` | NaN safety, portability |
| Score normalization | `frankensearch::fusion::normalize::normalize_scores()` | Edge case handling |
| Embedder implementations | `EmbedderStack::auto_detect()` delegates | Model lifecycle management |
| Search orchestration | `TwoTierSearcher` | Progressive phases, graceful degradation |
| Tantivy schema/search | `frankensearch::lexical::TantivyIndex` | Schema version alignment |

### What to Keep (Don't Over-Migrate)

- Domain-specific document types and ID mapping
- Application-level search filters (implement `SearchFilter` trait)
- UI/presentation layer for search results
- Custom text preprocessing before indexing

---

## Phase 3: Diagnosis & Repair (Stalled Integration)

### Diagnostic Checklist

Run through this in order. Stop when you find the root cause.

**1. Does it compile?**
```bash
CARGO_TARGET_DIR=target_check cargo check --workspace --all-targets 2>&1 | head -50
```

Common compilation failures:
- **"type mismatch" on `Cx`**: asupersync version conflict. See [BRIDGE-PATTERNS.md § Version Alignment](references/BRIDGE-PATTERNS.md).
- **"cannot find type `InMemoryTwoTierIndex`"**: frankensearch rev is stale. Update git rev or switch to path dep.
- **"unresolved import `frankensearch::lexical`"**: Missing `lexical` feature flag in Cargo.toml.
- **"missing field `explanation`"**: frankensearch added a field to `ScoredResult`. Add `explanation: None` to all bridge constructors.

**2. Does the index build?**
```rust
let diag = EmbedderStack::auto_detect()?.diagnose();
println!("{:#?}", diag);
// Check: diag.availability, diag.fast_status, diag.quality_status
```

Common index failures:
- **Model not found**: Set `FRANKENSEARCH_MODEL_DIR` to a writable path with models.
- **Quality tier unavailable**: This is OK — search works with fast tier only.
- **Index directory permissions**: Ensure write access to the FSVI output directory.

**3. Does search return results?**
```rust
let (results, metrics) = searcher.search_collect(&cx, "test query", 10).await?;
println!("Results: {}, Skip: {:?}", results.len(), metrics.skip_reason);
```

Common search failures:
- **Zero results, no error**: Index is empty or query doesn't match. Check `metrics.phase1_vectors_searched`.
- **`skip_reason = "fast_only"`**: `FRANKENSEARCH_FAST_ONLY=true` or no quality embedder. Expected behavior.
- **`RefinementFailed`**: Quality model timeout. Increase `FRANKENSEARCH_QUALITY_TIMEOUT`.
- **Results but wrong ranking**: Check if you're re-sorting after receiving frankensearch results (DON'T — frankensearch's f64 ordering is authoritative).

**4. Is there an async/sync impedance?**

If your project is sync (no async runtime) or uses tokio:
- frankensearch requires `&Cx` (asupersync context) for all async operations
- You need a `SyncEmbedderAdapter` bridge — see [BRIDGE-PATTERNS.md](references/BRIDGE-PATTERNS.md)
- For tests: `Cx::for_testing()` is lightweight and acceptable
- For production sync paths: use `SyncTwoTierSearcher` with `InMemoryTwoTierIndex`

**5. Is there a dependency resolution failure?**

Path deps to sibling directories (`../frankensearch`) don't work on:
- Remote build workers (`rch`) — they can't see sibling repos
- CI/CD — sibling repos not checked out by default
- Other developers' machines — different directory layout

**Fix for CI:**
```yaml
# .github/workflows/ci.yml
- uses: actions/checkout@v4
  with:
    repository: YourOrg/frankensearch
    path: frankensearch
- uses: actions/checkout@v4
  with:
    repository: YourOrg/your-project
    path: your-project
```

**Fix for development:** Use path deps locally, git deps for releases:
```toml
# Development (local):
frankensearch = { path = "../frankensearch/frankensearch", features = ["hybrid"] }

# Release (git):
# frankensearch = { git = "https://github.com/...", rev = "abc123", features = ["hybrid"] }
```

---

## Phase 4: Optimization & Audit

### Integration Quality Audit Checklist

| Check | Pass | Fail |
|-------|------|------|
| Uses `TwoTierSearcher` (not custom orchestration) | Using built-in progressive search | Has custom `blend_two_tier()` or manual phase logic |
| Uses `rrf_fuse()` from frankensearch (not custom) | Single source of RRF truth | Has duplicate RRF implementation |
| Uses `EmbedderStack::auto_detect()` (not manual model init) | Automatic model discovery | Has duplicate embedder registry |
| All tantivy types imported through frankensearch | Schema version aligned | Direct `use tantivy::` imports |
| Single doc ID encoding scheme | One `to_doc_id` / `from_doc_id` pair | Multiple incompatible ID formats |
| No re-sorting after frankensearch results | Preserves f64-precision ordering | Truncates to f32 then re-sorts |
| Handles `SearchPhase::RefinementFailed` | Graceful degradation | Panics or returns empty on quality failure |
| Feature-gated frankensearch deps | Compiles without search subsystem | Hard dependency even when search unused |
| `ScoredResult` fields mapped completely | All 10 fields handled | Missing `explanation`, `metadata`, `rerank_score` |
| Tests verify no direct tantivy imports | CI enforcement | Silent drift possible |

### Abstraction Level Guide

Use the **highest abstraction** that meets your needs:

```
HIGHEST ABSTRACTION (prefer this)
├── TwoTierSearcher.search_collect()     ← Most projects should use this
├── TwoTierSearcher.search()             ← When you need progressive phases
├── SyncTwoTierSearcher.search_collect() ← When you need sync + precomputed embeddings
│
MEDIUM ABSTRACTION (when you need control)
├── IndexBuilder + TwoTierIndex          ← Custom index building
├── EmbedderStack + manual searcher      ← Custom embedder lifecycle
├── rrf_fuse() directly                  ← When you have your own retrieval backends
│
LOWEST ABSTRACTION (avoid unless necessary)
├── VectorIndex direct access            ← Raw SIMD search
├── dot_product_f16_f32()                ← Individual vector operations
├── normalize_scores()                   ← Manual score manipulation
└── HashEmbedder/Model2VecEmbedder/etc   ← Individual embedder instances
```

**Rule of thumb:** If you're using more than 3 low-level frankensearch APIs, you're
probably reimplementing something that `TwoTierSearcher` already does better.

---

## Async/Sync Decision Matrix

| Your Project's Runtime | Recommended Pattern | Bridge Needed? |
|------------------------|--------------------|----|
| asupersync (`Cx`) | Direct integration — no bridge | No |
| tokio | `SyncEmbedderAdapter` + `Cx::for_testing()` or block_on bridge | Yes |
| No async (pure sync) | `SyncTwoTierSearcher` + `InMemoryTwoTierIndex` | Partial |
| rayon (CPU parallelism) | Direct — rayon composes with asupersync | No |

See [BRIDGE-PATTERNS.md](references/BRIDGE-PATTERNS.md) for complete adapter implementations.

---

## Environment Variables Quick Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `FRANKENSEARCH_MODEL_DIR` | `~/.cache/frankensearch/models` | Model file location |
| `FRANKENSEARCH_FAST_ONLY` | `false` | Skip quality refinement |
| `FRANKENSEARCH_QUALITY_WEIGHT` | `0.7` | Blend balance (0=fast, 1=quality) |
| `FRANKENSEARCH_RRF_K` | `60` | RRF fusion constant |
| `FRANKENSEARCH_QUALITY_TIMEOUT` | `500` | Quality phase timeout (ms) |
| `FRANKENSEARCH_LOG` | `info` | Tracing filter level |
| `FRANKENSEARCH_OFFLINE` | unset | Prevent model downloads |

---

## Common Bug Patterns in Integrations

These are real bugs found across 3 production integrations (82+ bugs total):

| Bug Pattern | How It Manifests | Prevention |
|-------------|-----------------|------------|
| f32→f64 precision loss in RRF | Tie-breaking changes between runs | Never truncate frankensearch scores before final display |
| NaN in quality_weight | All threshold checks bypassed | Guard with `.is_finite()` before `.clamp()` |
| `as u32` truncation on doc count | Silent data loss above 4B docs | Use `u64::try_from()` |
| Double-offset in hybrid pagination | Users skip 2x intended results | Apply offset ONCE (in caller, not in fusion) |
| Cross-model embedding hash collision | Quality model skips documents "already embedded" | Scope hash lookups by model_id |
| `zip()` drops trailing elements | Mismatched fast/quality index sizes silently lose docs | Validate lengths first |
| `Path::join()` with untrusted doc paths | Path traversal via `../` in doc IDs | Validate no `../` or absolute components |
| `Duration::from_secs_f64` with NaN | Panic on NaN timeout config | Guard with `.is_finite()` first |
| `#[derive(Deserialize)]` on config | Bypasses constructor invariants | Add runtime validation at usage |
| Temp dir deleted externally | FSVI index silently returns empty | Use persistent FSVI path or document lifetime |

---

## References

| Need | Reference |
|------|-----------|
| Complete frankensearch public API | [API-REFERENCE.md](references/API-REFERENCE.md) |
| Sync-to-async bridge implementations | [BRIDGE-PATTERNS.md](references/BRIDGE-PATTERNS.md) |
| Full migration playbook with parity testing | [MIGRATION-PLAYBOOK.md](references/MIGRATION-PLAYBOOK.md) |
| Real integration case studies (CASS, xf, mcp_agent_mail) | [CASE-STUDIES.md](references/CASE-STUDIES.md) |
| Diagnosing and fixing broken integrations | [DIAGNOSIS.md](references/DIAGNOSIS.md) |
| All discovered pitfalls with root causes and fixes | [PITFALLS.md](references/PITFALLS.md) |
