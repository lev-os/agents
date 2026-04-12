# Bridge Patterns: Async/Sync Impedance

## The Core Problem

frankensearch's `Embedder` trait is async, requiring `&Cx` (asupersync context):

```rust
pub trait Embedder: Send + Sync {
    fn embed<'a>(&'a self, cx: &'a Cx, text: &'a str) -> SearchFuture<'a, Vec<f32>>;
}
```

If your project uses synchronous embedders or tokio, you need bridge adapters.

---

## Pattern 1: SyncEmbedderAdapter (Sync → Async Bridge)

**Use when:** Your embedders are synchronous but frankensearch expects async.

```rust
use std::sync::Arc;
use frankensearch::{Embedder as FsEmbedder, SearchError, SearchFuture, ModelCategory, ModelTier};
use asupersync::Cx;

pub struct SyncEmbedderAdapter {
    inner: Arc<dyn YourSyncEmbedder>,
    model_name: String,
    dimension: usize,
    is_semantic: bool,
    category: ModelCategory,
}

impl SyncEmbedderAdapter {
    pub fn fast(inner: Arc<dyn YourSyncEmbedder>, name: &str, dim: usize) -> Self {
        Self {
            inner,
            model_name: name.to_string(),
            dimension: dim,
            is_semantic: true,
            category: ModelCategory::StaticEmbedder,
        }
    }

    pub fn quality(inner: Arc<dyn YourSyncEmbedder>, name: &str, dim: usize) -> Self {
        Self {
            inner,
            model_name: name.to_string(),
            dimension: dim,
            is_semantic: true,
            category: ModelCategory::TransformerEmbedder,
        }
    }

    pub fn hash(inner: Arc<dyn YourSyncEmbedder>, dim: usize) -> Self {
        Self {
            inner,
            model_name: "hash".to_string(),
            dimension: dim,
            is_semantic: false,
            category: ModelCategory::HashEmbedder,
        }
    }
}

impl FsEmbedder for SyncEmbedderAdapter {
    fn embed<'a>(&'a self, _cx: &'a Cx, text: &'a str) -> SearchFuture<'a, Vec<f32>> {
        Box::pin(async move {
            self.inner.embed(text).map_err(|e| SearchError::EmbeddingFailed {
                model: self.model_name.clone(),
                source: Box::new(e),
            })
        })
    }

    fn embed_batch<'a>(&'a self, _cx: &'a Cx, texts: &'a [&'a str]) -> SearchFuture<'a, Vec<Vec<f32>>> {
        Box::pin(async move {
            texts.iter()
                .map(|t| self.inner.embed(t).map_err(|e| SearchError::EmbeddingFailed {
                    model: self.model_name.clone(),
                    source: Box::new(e),
                }))
                .collect()
        })
    }

    fn dimension(&self) -> usize { self.dimension }
    fn id(&self) -> &str { &self.model_name }
    fn model_name(&self) -> &str { &self.model_name }
    fn is_semantic(&self) -> bool { self.is_semantic }
    fn category(&self) -> ModelCategory { self.category }
}
```

**Then compose with EmbedderStack:**

```rust
let fast_adapter = Arc::new(SyncEmbedderAdapter::fast(your_fast_embedder, "potion-128M", 256));
let quality_adapter = Arc::new(SyncEmbedderAdapter::quality(your_quality_embedder, "minilm-l6-v2", 384));
let stack = EmbedderStack::from_parts(fast_adapter, Some(quality_adapter));
```

---

## Pattern 2: Tokio Block-On Bridge

**Use when:** Your project uses tokio and needs to call frankensearch from a sync context.

```rust
use asupersync::runtime::Runtime as AsRuntime;
use asupersync::Cx;

pub struct TokioBridge {
    runtime: AsRuntime,
}

impl TokioBridge {
    pub fn new() -> Self {
        Self { runtime: AsRuntime::new() }
    }

    pub fn embed_sync(&self, embedder: &dyn FsEmbedder, text: &str) -> Result<Vec<f32>, SearchError> {
        let cx = Cx::for_testing();
        self.runtime.block_on(embedder.embed(&cx, text))
    }
}
```

**WARNING:** `Cx::for_testing()` is lightweight and acceptable for CLI tools and tests,
but it bypasses real cancellation propagation. For production services that need proper
cancellation, create a real `Cx` from your runtime.

---

## Pattern 3: Frankensearch Embedder Delegates (Preferred)

**Use when:** You want frankensearch to manage the actual embedding models.

Instead of wrapping YOUR embedders for frankensearch, delegate TO frankensearch's embedders:

```rust
use frankensearch::{HashEmbedder, Model2VecEmbedder, FastEmbedEmbedder};

// Your sync embedder wraps frankensearch's async one
pub struct MyHashEmbedder {
    delegate: frankensearch::HashEmbedder,
}

impl YourSyncEmbedder for MyHashEmbedder {
    fn embed(&self, text: &str) -> Result<Vec<f32>> {
        // HashEmbedder has a sync path
        Ok(self.delegate.embed_sync(text))
    }
}

pub struct MyFastEmbedEmbedder {
    runtime: AsRuntime,
    delegate: frankensearch::FastEmbedEmbedder,
}

impl YourSyncEmbedder for MyFastEmbedEmbedder {
    fn embed(&self, text: &str) -> Result<Vec<f32>> {
        let cx = Cx::for_testing();
        self.runtime.block_on(self.delegate.embed(&cx, text))
            .map_err(|e| YourError::from(e))
    }
}
```

**This pattern is better** because:
- One source of truth for embedding logic
- Model loading, caching, and lifecycle handled by frankensearch
- No duplicate model registry to maintain

---

## Pattern 4: Reranker Adapter

```rust
use frankensearch::{Reranker as FsReranker, RerankDocument, RerankScore, SearchFuture};

pub struct SyncRerankerAdapter {
    inner: Box<dyn YourSyncReranker>,
    id: String,
}

impl FsReranker for SyncRerankerAdapter {
    fn rerank<'a>(
        &'a self,
        _cx: &'a Cx,
        candidates: &'a [RerankDocument<'a>],
    ) -> SearchFuture<'a, Vec<RerankScore>> {
        Box::pin(async move {
            let texts: Vec<&str> = candidates.iter().map(|c| c.text).collect();
            let query = candidates.first().map(|c| c.query).unwrap_or("");

            let scores = self.inner.rerank(query, &texts)
                .map_err(|e| SearchError::RerankFailed { source: Box::new(e) })?;

            Ok(scores.into_iter().enumerate().map(|(i, score)| RerankScore {
                index: i,
                score,
                doc_id: candidates[i].doc_id.to_string(),
            }).collect())
        })
    }
}
```

---

## Version Alignment (CRITICAL)

The most common compilation failure in frankensearch integration is `Cx` type mismatch.

**Symptoms:**
```
error[E0308]: mismatched types
  --> src/search.rs:42:30
   |
42 |     searcher.search_collect(&cx, "query", 10).await?;
   |                              ^^^ expected `&asupersync::Cx`, found `&asupersync::Cx`
   = note: perhaps two different versions of crate `asupersync` are being used?
```

**Root cause:** Two copies of asupersync in the dependency graph (one from crates.io,
one from git or path).

**Fix:**

```toml
# Option 1: Both use same path
asupersync = { path = "../asupersync" }

# Option 2: Force alignment with [patch]
[patch.crates-io]
asupersync = { path = "../asupersync" }

[patch."https://github.com/Dicklesworthstone/asupersync"]
asupersync = { path = "../asupersync" }

# Option 3: Import Cx through frankensearch's re-export
use frankensearch::Cx;  # Instead of: use asupersync::Cx;
```

**Verification:**
```bash
cargo tree -i asupersync 2>&1 | head -20
# Should show exactly ONE version of asupersync
```

---

## Error Mapping

Map frankensearch errors to your domain error type:

```rust
pub fn map_fs_error(err: SearchError) -> YourError {
    match err {
        SearchError::ModelNotFound { name } =>
            YourError::SearchUnavailable(format!("model not found: {name}")),
        SearchError::ModelLoadFailed { path, source } =>
            YourError::Internal(format!("model load failed at {path}: {source}")),
        SearchError::EmbeddingFailed { model, source } =>
            YourError::Internal(format!("embedding failed ({model}): {source}")),
        SearchError::Cancelled { phase, reason } =>
            YourError::Timeout(format!("{phase}: {reason}")),
        SearchError::IndexCorrupted { path, detail } =>
            YourError::DataCorruption(format!("{path}: {detail}")),
        other => YourError::Internal(other.to_string()),
    }
}
```

---

## Config Conversion

If your project has its own search config, create bidirectional mapping:

```rust
impl YourConfig {
    pub fn to_frankensearch(&self) -> FsTwoTierConfig {
        FsTwoTierConfig {
            quality_weight: f64::from(self.blend_factor.clamp(0.0, 1.0)),
            quality_timeout_ms: self.quality_timeout_ms,
            fast_only: self.quality_timeout_ms == 0,
            rrf_k: f64::from(self.rrf_k),
            ..FsTwoTierConfig::default()
        }
    }

    pub fn from_frankensearch(fs: &FsTwoTierConfig) -> Self {
        Self {
            // CAUTION: f64 → f32 precision loss (acceptable for weights)
            blend_factor: fs.quality_weight as f32,
            quality_timeout_ms: fs.quality_timeout_ms,
            rrf_k: fs.rrf_k as f32,
            ..Self::default()
        }
    }
}
```

**WARNING:** f64 → f32 narrowing loses precision. This is acceptable for config values
(weights are ~0.7, precision loss is negligible) but NEVER truncate scores.
