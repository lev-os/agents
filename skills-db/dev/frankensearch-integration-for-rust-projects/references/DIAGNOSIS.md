# Diagnosing and Fixing Broken Frankensearch Integrations

## Triage Order

Work through this sequentially. Stop when you find the root cause.

---

## Level 1: Compilation Failures

### Symptom: `Cx` type mismatch
```
error[E0308]: mismatched types
  expected `&asupersync::Cx`, found `&asupersync::Cx`
  note: perhaps two different versions of crate `asupersync` are being used?
```

**Root cause:** Two copies of asupersync in the dependency tree.

**Diagnosis:**
```bash
cargo tree -i asupersync 2>&1
# Look for multiple versions or sources
```

**Fix:**
```toml
# Force single source in Cargo.toml
[patch.crates-io]
asupersync = { path = "../asupersync" }

[patch."https://github.com/Dicklesworthstone/asupersync"]
asupersync = { path = "../asupersync" }
```

Or import `Cx` through frankensearch's re-export:
```rust
use frankensearch::Cx;  // NOT: use asupersync::Cx;
```

### Symptom: Missing types (e.g., `InMemoryTwoTierIndex`, `SyncTwoTierSearcher`)

**Root cause:** frankensearch git rev is stale — these types were added after your pinned rev.

**Diagnosis:**
```bash
# Check what rev you're pinned to
grep frankensearch Cargo.toml | grep rev
# Check if the type exists in that rev
cd ../frankensearch && git log --oneline --all -- '**/sync_searcher.rs'
```

**Fix:** Update the git rev, or switch to a path dep for development:
```toml
frankensearch = { path = "../frankensearch/frankensearch", features = ["hybrid"] }
```

### Symptom: `unresolved import frankensearch::lexical`

**Root cause:** Missing `lexical` feature flag.

**Fix:**
```toml
frankensearch = { ..., features = ["hybrid"] }  # hybrid includes lexical
```

### Symptom: Missing field `explanation` in `ScoredResult` constructor

**Root cause:** frankensearch added a new field. Your bridge constructors need updating.

**Fix:** Add `explanation: None` (and any other new fields) to all places you construct `ScoredResult`.

**Prevention:** Use struct update syntax:
```rust
ScoredResult {
    doc_id: id.to_string(),
    score: hit.score,
    source: ScoreSource::Hybrid,
    ..ScoredResult::default()  // Absorbs future field additions
}
```

---

## Level 2: Index Build Failures

### Symptom: `ModelNotFound` during `EmbedderStack::auto_detect()`

**Diagnosis:**
```rust
let diag = EmbedderStack::auto_detect()?.diagnose();
println!("Availability: {:?}", diag.availability);
println!("Cache dir: {:?}", diag.cache_dir);
println!("Fast: {:?}", diag.fast_status);
println!("Quality: {:?}", diag.quality_status);
for suggestion in &diag.suggestions {
    println!("  → {suggestion}");
}
```

**Common causes:**
- Model directory doesn't exist or isn't writable
- Models not downloaded (first run)
- `FRANKENSEARCH_OFFLINE=1` set but models not cached

**Fix:**
```bash
# Set model directory
export FRANKENSEARCH_MODEL_DIR=~/.cache/frankensearch/models
mkdir -p $FRANKENSEARCH_MODEL_DIR

# If models need downloading, ensure network access and remove OFFLINE flag
unset FRANKENSEARCH_OFFLINE
```

### Symptom: Index build succeeds but `has_quality_index = false`

**Cause:** Quality embedder (MiniLM-L6-v2) not available. Search will work with fast tier only.

**This is not a bug** — it's graceful degradation. If you need quality tier:
1. Ensure `fastembed` feature is enabled
2. Ensure MiniLM model files are in the model directory
3. Check `diag.quality_status` for specific error

### Symptom: `IndexCorrupted` on `TwoTierIndex::open()`

**Cause:** FSVI binary format corruption (incomplete write, disk error, embedder revision mismatch).

**Diagnosis:**
```bash
# Check FSVI file headers
xxd -l 64 ./my_index/fast.fsvi | head -4
# Should start with: 4653 5649 (FSVI magic bytes)
```

**Fix:** Rebuild the index from source documents. FSVI files are derived artifacts.

---

## Level 3: Search Returns Wrong Results

### Symptom: Zero results, no error

**Diagnosis:**
```rust
let (results, metrics) = searcher.search_collect(&cx, "test", 10).await?;
println!("Phase1 vectors searched: {}", metrics.phase1_vectors_searched);
println!("Lexical candidates: {}", metrics.lexical_candidates);
println!("Semantic candidates: {}", metrics.semantic_candidates);
```

**Common causes:**
- Index is empty (`phase1_vectors_searched == 0`)
- Query is empty after canonicalization
- All documents filtered out by `SearchFilter`

### Symptom: Results but wrong ranking

**Diagnosis:**
```rust
for r in &results {
    println!("{}: score={:.4} source={:?} fast={:?} quality={:?} lexical={:?}",
        r.doc_id, r.score, r.source, r.fast_score, r.quality_score, r.lexical_score);
}
println!("Kendall tau: {:?}", metrics.kendall_tau);
println!("Rank changes: {:?}", metrics.rank_changes);
```

**Common causes:**
- **Re-sorting after frankensearch**: DON'T. frankensearch's ordering is authoritative.
- **Wrong quality_weight**: Check `FRANKENSEARCH_QUALITY_WEIGHT` (default 0.7 = 70% quality)
- **fast_only mode active**: Check `FRANKENSEARCH_FAST_ONLY`
- **NaN in scores**: Check for NaN in `fast_score`/`quality_score` — indicates embedding failure

### Symptom: `RefinementFailed` appears often

**Diagnosis:**
```rust
if let SearchPhase::RefinementFailed { error, .. } = phase {
    println!("Refinement error: {error}");
}
println!("Skip reason: {:?}", metrics.skip_reason);
```

**Common causes:**
- Quality embedder too slow (increase `FRANKENSEARCH_QUALITY_TIMEOUT`)
- Quality model not loaded (check `diagnose()`)
- CPU contention from other processes

### Symptom: Double-offset pagination

**Cause:** Offset applied both in RRF fusion and in your caller code.

**Fix:** Apply offset ONCE — either in the caller or in fusion, never both:
```rust
// Correct: let frankensearch handle offset internally
let (results, metrics) = searcher.search_collect(&cx, query, limit).await?;
// Then apply YOUR offset on the results
let page = &results[offset..min(offset + page_size, results.len())];
```

### Symptom: Same document appears with different scores in lexical vs semantic

**Cause:** Document ID format mismatch between Tantivy index and vector index.

**Diagnosis:**
```rust
// Check if doc IDs match between indexes
for r in &results {
    if r.source == ScoreSource::Hybrid {
        println!("Hybrid: {} (lexical={:?}, semantic={:?})",
            r.doc_id, r.lexical_score, r.fast_score);
    }
}
// If lexical_score is None but you expect hybrid results, check ID format
```

**Fix:** Ensure both indexes use the same doc_id encoding. See SKILL.md § "Map Document IDs".

---

## Level 4: Performance Issues

### Symptom: Phase 1 is slow (>50ms)

**Expected:** Phase 1 should be <15ms for most corpora.

**Diagnosis:**
```rust
println!("fast_embed: {:.1}ms", metrics.fast_embed_ms);
println!("vector_search: {:.1}ms", metrics.vector_search_ms);
println!("lexical_search: {:.1}ms", metrics.lexical_search_ms);
println!("rrf_fusion: {:.1}ms", metrics.rrf_fusion_ms);
```

**Common causes:**
- **Fast embed slow**: Model not cached, cold start. Warm up with a dummy query.
- **Vector search slow**: Corpus too large for brute-force. Enable ANN (`ann` feature).
- **Lexical search slow**: Tantivy index needs `optimize_if_idle()`.

### Symptom: High memory usage

**Diagnosis:**
```bash
# Check FSVI file sizes
ls -lh ./my_index/*.fsvi
# Each record: dimension * 2 bytes (f16) per document per tier
```

**Mitigation:**
- Stay on f16 quantization (default) — 50% savings vs f32
- Use `fast_only=true` to skip quality index
- Enable ANN for large corpora (trades memory for speed)

### Symptom: Search screen latency in TUI (>100ms)

**Common causes (from mcp_agent_mail profiling):**
- Per-query bootstrap overhead — reuse long-lived searcher instance
- Rerank-stage cloning — reduce top-k for reranking
- Eager snippet shaping — defer until display time
- Lexical cold-start warmup — warm Tantivy reader on startup

---

## Level 5: CI/CD Failures

### Symptom: `Cargo.toml` path deps fail in CI

**Cause:** Sibling repos not checked out.

**Fix:**
```yaml
# GitHub Actions: checkout all sibling repos
- uses: actions/checkout@v4
  with:
    repository: YourOrg/frankensearch
    path: frankensearch
- uses: actions/checkout@v4
  with:
    repository: YourOrg/asupersync
    path: asupersync
```

### Symptom: `rch` (remote build worker) fails with path dep resolution

**Cause:** `rch` can't resolve `../frankensearch` on remote workers.

**Fix:** For remote builds, temporarily switch to git deps, or use `rch`'s workspace sync feature.

### Symptom: Tests pass locally, fail in CI

**Common causes:**
- Model files not available in CI (use `hash` feature for CI smoke tests)
- Different filesystem layout (relative path deps wrong)
- Temp directory cleanup timing (FSVI temp dirs)

**Fix for model-dependent tests:**
```rust
#[test]
fn test_with_hash_fallback() {
    // Use hash embedder (always available, no model files needed)
    let fast = Arc::new(HashEmbedder::default_256()) as Arc<dyn Embedder>;
    let stack = EmbedderStack::from_parts(fast, None);
    // ... test with stack
}
```

---

## Quick Diagnostic Commands

```bash
# Check frankensearch dependency tree
cargo tree -p frankensearch 2>&1 | head -30

# Check for duplicate asupersync
cargo tree -i asupersync 2>&1

# Check feature flags
cargo tree -p frankensearch -e features 2>&1 | head -20

# Verify no direct tantivy imports
rg '^use tantivy::' --type rust src/

# Check FSVI index health
xxd -l 8 ./my_index/fast.fsvi
# Expect: 4653 5649 0100 xxxx (FSVI magic + version 1)

# Check model availability
ls -la ${FRANKENSEARCH_MODEL_DIR:-~/.cache/frankensearch/models}/
```
