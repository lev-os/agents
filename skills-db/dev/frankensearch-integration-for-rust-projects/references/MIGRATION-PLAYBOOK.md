# Migration Playbook: Ad-Hoc Search → Frankensearch

## Overview

This playbook is distilled from three real migrations:
- **xf**: 573 lines deleted, 62 cfg gates, completed in one day
- **CASS**: Partial (~15% by volume), architectural mismatch (async vs sync TUI)
- **mcp_agent_mail_rust**: Bridge pattern, local two-tier retained alongside frankensearch helpers

The xf migration was the cleanest and most complete. Follow its pattern.

---

## Pre-Migration Assessment

### What You Have (Audit Your Current Stack)

| Component | Check | If Present |
|-----------|-------|------------|
| Custom RRF fusion | `rg 'rrf_fuse\|reciprocal_rank' --type rust` | Replace first (highest bug surface) |
| Custom SIMD dot product | `rg 'dot_product\|f32x8\|wide::' --type rust` | Replace with `dot_product_f16_f32` |
| Custom score normalization | `rg 'normalize_scores\|min_max' --type rust` | Replace with frankensearch's |
| Custom embedder registry | `rg 'embedder_registry\|model_registry' --type rust` | Use `EmbedderStack::auto_detect()` |
| Direct tantivy imports | `rg '^use tantivy::' --type rust` | Route through frankensearch re-exports |
| Manual progressive search | `rg 'SearchPhase\|Initial\|Refined' --type rust` | Use `TwoTierSearcher` |
| Custom hash embedder | `rg 'fnv1a\|FNV_PRIME\|hash_embed' --type rust` | Use `HashEmbedder` delegate |
| Manual f16 quantization | `rg 'f16\|half::' --type rust` | Use FSVI format via `TwoTierIndex` |

### Decision: Full Migration or Incremental?

**Full migration** (like xf): Replace everything, feature-gate during transition, cut over in one commit.
- Choose when: Custom search is simple, well-contained, and tests exist.

**Incremental migration** (like mcp_agent_mail): Replace low-level helpers first, keep orchestration.
- Choose when: Complex search orchestration with many consumers, async/sync mismatch.

**Partial migration** (like CASS): Replace building blocks but keep domain-specific orchestration.
- Choose when: Fundamental architectural mismatch (e.g., sync TUI needs, custom caching layers).

---

## Step-by-Step: Full Migration

### Step 1: Add frankensearch alongside existing code

```toml
[dependencies]
frankensearch = { path = "../frankensearch/frankensearch", features = ["hybrid"] }
```

**Do NOT remove any existing code yet.**

### Step 2: Create feature gate

```toml
[features]
frankensearch-migration = []
```

### Step 3: Replace RRF fusion first

RRF is the highest-bug-surface component. Replace it before anything else.

```rust
#[cfg(feature = "frankensearch-migration")]
fn rrf_fuse(lexical: &[SearchResult], semantic: &[VectorResult]) -> Vec<FusedResult> {
    use frankensearch_fusion::{rrf_fuse as fs_rrf_fuse, RrfConfig};

    // Convert your types to frankensearch types
    let fs_lexical: Vec<ScoredResult> = lexical.iter().map(to_fs_scored_result).collect();
    let fs_semantic: Vec<VectorHit> = semantic.iter().map(to_fs_vector_hit).collect();

    let fused = fs_rrf_fuse(&fs_lexical, &fs_semantic, &RrfConfig::default());

    // Convert back
    fused.iter().map(from_fs_fused_hit).collect()
}

#[cfg(not(feature = "frankensearch-migration"))]
fn rrf_fuse(lexical: &[SearchResult], semantic: &[VectorResult]) -> Vec<FusedResult> {
    // Your existing implementation (unchanged)
    legacy_rrf_fuse(lexical, semantic)
}
```

### Step 4: Build migration parity tests

**This is essential.** Without parity tests, you cannot confidently cut over.

```rust
#[cfg(test)]
mod migration_parity {
    #[test]
    fn rrf_fusion_produces_equivalent_results() {
        let lexical = test_lexical_results();
        let semantic = test_semantic_results();

        let legacy = legacy_rrf_fuse(&lexical, &semantic);
        let fs = frankensearch_rrf_fuse(&lexical, &semantic);

        // Same result set (possibly different order for equal scores)
        assert_eq!(legacy.len(), fs.len());

        // Scores within epsilon (f64 vs f32 precision difference)
        for (l, f) in legacy.iter().zip(fs.iter()) {
            assert!((l.score - f.score).abs() < 1e-6,
                "Score divergence: legacy={}, fs={}", l.score, f.score);
        }
    }
}
```

**Known parity issues:**
- **f32 vs f64 accumulation**: frankensearch accumulates RRF scores in f64, then truncates. Legacy code in f32 will have different tie-breaking. This is expected — frankensearch is MORE precise.
- **Ordering of equal scores**: When two docs have the same RRF score, tie-breaking may differ. Don't assert strict ordering for equal scores.

### Step 5: Replace SIMD and normalization

```rust
// Replace custom dot product
#[cfg(feature = "frankensearch-migration")]
fn dot_product(embedding: &[f16], query: &[f32]) -> f32 {
    frankensearch::index::simd::dot_product_f16_f32(embedding, query).unwrap_or(0.0)
}

// Replace custom normalization
#[cfg(feature = "frankensearch-migration")]
fn normalize(scores: &[f32]) -> Vec<f32> {
    frankensearch::fusion::normalize::normalize_scores(scores)
}
```

### Step 6: Replace embedder implementations

Switch from your embedder implementations to frankensearch delegates:

```rust
// Before: raw FastEmbed TextEmbedding
let model = TextEmbedding::try_new(InitOptions { ... })?;
let embedding = model.embed(vec![text], None)?;

// After: frankensearch delegate
let embedder = FastEmbedEmbedder::new(model_path)?;
let embedding = runtime.block_on(embedder.embed(&cx, text))?;
```

### Step 7: Replace search orchestration

This is the biggest change. Replace your custom search loop with `TwoTierSearcher`:

```rust
// Before: manual progressive search
let fast_vec = fast_embedder.embed(query);
let semantic_results = vector_index.search(fast_vec, k * 3);
let lexical_results = tantivy.search(query, k * 3);
let fused = rrf_fuse(&lexical_results, &semantic_results);
// Emit initial results...
let quality_vec = quality_embedder.embed(query);
let quality_scores = quality_index.score(&quality_vec, &fused);
let blended = blend(fused, quality_scores, 0.7);
// Emit refined results...

// After: one line
let (results, metrics) = searcher.search_collect(&cx, query, k).await?;
```

### Step 8: Validate parity, then cut over

```bash
# Run both paths in tests
cargo test --features frankensearch-migration

# If all parity tests pass, remove legacy code
# Do this in ONE commit for clean git history
```

### Step 9: Post-cutover cleanup

- Remove all `#[cfg(feature = "frankensearch-migration")]` gates
- Remove the `frankensearch-migration` feature from Cargo.toml
- Delete legacy functions (RRF, SIMD, normalization, embedder implementations)
- Run: `cargo check && cargo clippy && cargo test`
- Verify: `rg 'legacy_\|old_\|deprecated_' --type rust` returns nothing

---

## Parity Testing: The RRF Precision Problem

The most common parity failure is RRF score divergence due to f32/f64 accumulation.

**Root cause:** Legacy code computes `1.0 / (k + rank + 1)` in f32, accumulates in f32.
frankensearch computes in f64, accumulates in f64, then truncates to f32.

**Example:**
```
Doc A: legacy_score = 0.016393441 (f32)
Doc A: fs_score     = 0.016393442 (f32, from f64 0.016393442622950825)
```

This 1-ULP difference can change tie-breaking order.

**Solution:** After receiving results from frankensearch, DO NOT re-sort them. frankensearch's
f64-precision ordering is authoritative. If you truncate to f32 and re-sort, you get different
(worse) ordering.

```rust
// WRONG: truncates f64 ordering
let mut results = searcher.search_collect(&cx, query, k).await?.0;
results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap()); // DON'T DO THIS

// RIGHT: trust frankensearch's ordering
let (results, metrics) = searcher.search_collect(&cx, query, k).await?;
// results are already in correct order
```

---

## Migration Checklist

- [ ] frankensearch dependency added with correct features
- [ ] asupersync version aligned (single copy in dep tree)
- [ ] Feature gate created for migration path
- [ ] RRF fusion replaced (highest priority)
- [ ] Parity tests written and passing
- [ ] SIMD dot product replaced
- [ ] Score normalization replaced
- [ ] Embedder implementations delegated to frankensearch
- [ ] Search orchestration replaced with TwoTierSearcher
- [ ] All tantivy imports routed through frankensearch
- [ ] Direct tantivy dependency removed from Cargo.toml
- [ ] Legacy code removed in single commit
- [ ] `cargo check && cargo clippy && cargo test` all pass
- [ ] No `rg '^use tantivy::' --type rust` matches remain
- [ ] Decommission manifest created documenting what was removed/retained
