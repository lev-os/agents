# Frankensearch Public API Reference

## Facade Crate (`frankensearch`)

The facade crate re-exports everything you need. Import from here, not from sub-crates.

```rust
use frankensearch::{
    // Core types
    SearchPhase, ScoredResult, ScoreSource, VectorHit, FusedHit,
    SearchError, SearchResult, TwoTierConfig, TwoTierMetrics,
    IndexableDocument, PhaseMetrics, RankChanges,

    // Traits
    Embedder, LexicalSearch, Reranker, MetricsExporter, Canonicalizer,
    SearchFilter,

    // Query
    QueryClass, Canonicalizer as CanonTrait,

    // Embedder stack
    EmbedderStack, TwoTierAvailability, ModelAvailabilityDiagnostic,
    ModelStatus, ModelInfo, ModelCategory, ModelTier,

    // Index
    TwoTierIndex, TwoTierIndexBuilder, VectorIndex, VectorMetadata,
    InMemoryTwoTierIndex, InMemoryVectorIndex,
    Quantization, FSVI_MAGIC, FSVI_VERSION,

    // Searcher
    TwoTierSearcher, SyncTwoTierSearcher,

    // Index building
    IndexBuilder, IndexBuildStats, IndexProgress,

    // Feature-gated
    #[cfg(feature = "hash")]     HashEmbedder,
    #[cfg(feature = "model2vec")] Model2VecEmbedder,
    #[cfg(feature = "fastembed")] FastEmbedEmbedder,
    #[cfg(feature = "lexical")]  TantivyIndex,
    #[cfg(feature = "rerank")]   FlashRankReranker,
    #[cfg(feature = "storage")]  Storage,

    // Async context (re-exported from asupersync)
    Cx,
};
```

---

## IndexBuilder

High-level fluent API for building search indices from documents.

```rust
pub struct IndexBuilder { ... }

impl IndexBuilder {
    /// Create a new builder targeting the given data directory
    pub fn new(data_dir: impl Into<PathBuf>) -> Self;

    /// Set search configuration
    pub fn with_config(self, config: TwoTierConfig) -> Self;

    /// Set the embedder stack (fast + optional quality)
    pub fn with_embedder_stack(self, stack: EmbedderStack) -> Self;

    /// Set batch size for embedding (default: reasonable)
    pub fn with_batch_size(self, batch_size: usize) -> Self;

    /// Set progress callback for monitoring
    pub fn with_progress(self, callback: impl FnMut(IndexProgress) + Send + 'static) -> Self;

    /// Add a single document
    pub fn add_document(self, id: impl Into<String>, content: impl Into<String>) -> Self;

    /// Add a document with title (used for relevance boosting)
    pub fn add_document_with_title(self, id, content, title) -> Self;

    /// Add multiple documents at once
    pub fn add_documents(self, docs: impl IntoIterator<Item = IndexableDocument>) -> Self;

    /// Build the index (async, requires &Cx)
    pub async fn build(self, cx: &Cx) -> SearchResult<IndexBuildStats>;
}

pub struct IndexBuildStats {
    pub doc_count: usize,
    pub error_count: usize,
    pub errors: Vec<(String, String)>,  // (doc_id, error_message)
    pub total_ms: f64,
    pub embed_ms: f64,
    pub has_quality_index: bool,
}
```

**Key points:**
- `build()` is async and requires `&Cx` from asupersync
- The embedder stack determines which tiers are built (fast only vs fast + quality)
- Documents with embedding errors are skipped (check `error_count` and `errors`)
- The data directory is created if it doesn't exist

---

## EmbedderStack

Auto-detection and lifecycle management for the fast + quality embedder pair.

```rust
pub struct EmbedderStack { ... }

impl EmbedderStack {
    /// Create from explicit embedder instances
    pub fn from_parts(fast: Arc<dyn Embedder>, quality: Option<Arc<dyn Embedder>>) -> Self;

    /// Auto-detect available models on the system
    /// Looks for potion-128M (fast) and MiniLM-L6-v2 (quality)
    pub fn auto_detect() -> SearchResult<Self>;

    /// Auto-detect with custom model root directory
    pub fn auto_detect_with(model_root: Option<&Path>) -> SearchResult<Self>;

    /// Apply MRL (Matryoshka) dimension reduction
    pub fn with_mrl_target_dim(self, target_dim: usize) -> SearchResult<Self>;

    /// Access individual embedders
    pub fn fast(&self) -> &dyn Embedder;
    pub fn fast_arc(&self) -> Arc<dyn Embedder>;
    pub fn quality(&self) -> Option<&dyn Embedder>;
    pub fn quality_arc(&self) -> Option<Arc<dyn Embedder>>;

    /// Check what's available
    pub const fn availability(&self) -> TwoTierAvailability;

    /// Detailed diagnostic for troubleshooting model availability
    pub fn diagnose(&self) -> ModelAvailabilityDiagnostic;
}

pub enum TwoTierAvailability {
    Full,       // Fast + quality both available
    FastOnly,   // Only fast-tier embedder
    HashOnly,   // Fallback to hash embedder (non-semantic)
}
```

**Key points:**
- `auto_detect()` never fails — it falls back to `HashEmbedder` if no models found
- Always check `availability()` to know what tier is active
- `diagnose()` gives detailed human-readable info about why models aren't loading
- The `from_parts()` constructor lets you inject custom embedders (e.g., sync adapters)

---

## TwoTierSearcher (Async)

The main search orchestrator. This is what most projects should use.

```rust
pub struct TwoTierSearcher { ... }

impl TwoTierSearcher {
    /// Create with mandatory components
    pub fn new(
        index: Arc<TwoTierIndex>,
        fast_embedder: Arc<dyn Embedder>,
        config: TwoTierConfig,
    ) -> Self;

    // --- Builder methods (all optional) ---
    pub fn with_quality_embedder(self, embedder: Arc<dyn Embedder>) -> Self;
    pub fn with_lexical(self, lexical: Arc<dyn LexicalSearch>) -> Self;
    pub fn with_reranker(self, reranker: Arc<dyn Reranker>) -> Self;
    pub fn with_canonicalizer(self, canonicalizer: Box<dyn Canonicalizer>) -> Self;
    pub fn with_embedding_cache(self, capacity: usize) -> Self;
    // ... plus 10+ more optional builder methods for advanced features

    // --- Search APIs ---

    /// Simple: collect all results (waits for refinement)
    pub async fn search_collect(
        &self, cx: &Cx, query: &str, k: usize,
    ) -> SearchResult<(Vec<ScoredResult>, TwoTierMetrics)>;

    /// With text callback (enables reranking and negation filtering)
    pub async fn search_collect_with_text(
        &self, cx: &Cx, query: &str, k: usize,
        text_fn: impl Fn(&str) -> Option<String> + Send + Sync,
    ) -> SearchResult<(Vec<ScoredResult>, TwoTierMetrics)>;

    /// Progressive: callback per phase (Initial, Refined, RefinementFailed)
    pub async fn search(
        &self, cx: &Cx, query: &str, k: usize,
        text_fn: impl Fn(&str) -> Option<String> + Send + Sync,
        mut on_phase: impl FnMut(SearchPhase) + Send,
    ) -> SearchResult<TwoTierMetrics>;
}
```

**Key points:**
- `search_collect()` is the simplest API — returns final results after both phases
- `search()` with phase callback enables progressive UX (show fast results immediately)
- The `text_fn` callback provides document text for reranking and negation queries
- All methods are async and require `&Cx`

---

## SyncTwoTierSearcher (Synchronous)

For projects that need synchronous search with precomputed embeddings.

```rust
pub struct SyncTwoTierSearcher { ... }

impl SyncTwoTierSearcher {
    pub const fn new(index: Arc<InMemoryTwoTierIndex>, config: TwoTierConfig) -> Self;
    pub fn with_lexical(self, lexical: Arc<dyn SyncLexicalSearch>) -> Self;

    /// Search with a precomputed query vector
    pub fn search_collect(
        &self, query_vec: &[f32], k: usize,
    ) -> SearchResult<(Vec<ScoredResult>, TwoTierMetrics)>;

    /// Search with optional filter
    pub fn search_collect_with_filter(
        &self, query_vec: &[f32], k: usize,
        filter: Option<&dyn SearchFilter>,
    ) -> SearchResult<(Vec<ScoredResult>, TwoTierMetrics)>;
}
```

**Key points:**
- No `&Cx` required — fully synchronous
- Requires `InMemoryTwoTierIndex` (not file-backed `TwoTierIndex`)
- You must embed the query yourself before calling search
- Good for TUI applications that can't use async

---

## TwoTierConfig

All tuning knobs in one struct.

```rust
pub struct TwoTierConfig {
    pub quality_weight: f64,          // 0.0–1.0, default 0.7 (70% quality, 30% fast)
    pub rrf_k: f64,                   // default 60.0
    pub candidate_multiplier: usize,  // default 3 (fetch 3x limit from each source)
    pub quality_timeout_ms: u64,      // default 500
    pub fast_only: bool,              // default false
    pub explain: bool,                // default false (enables HitExplanation)
    pub hnsw_ef_search: usize,        // default 100
    pub hnsw_ef_construction: usize,  // default 200
    pub hnsw_m: usize,                // default 16
    pub hnsw_threshold: usize,        // default 50_000
    pub mrl_search_dims: usize,       // default 0 (disabled)
    pub mrl_rescore_top_k: usize,     // default 30
    // ... plus graph ranking, metrics exporter
}

impl TwoTierConfig {
    /// Apply environment variable overrides (FRANKENSEARCH_*)
    pub fn with_env_overrides(self) -> Self;

    /// Load optimized params from data/optimized_params.toml
    pub fn optimized() -> Self;
}
```

---

## Result Types

```rust
pub struct ScoredResult {
    pub doc_id: String,
    pub score: f32,                    // Primary relevance score
    pub source: ScoreSource,           // Which backend produced it
    pub index: Option<u32>,            // Vector index position
    pub fast_score: Option<f32>,       // Raw fast-tier vector score
    pub quality_score: Option<f32>,    // Raw quality-tier vector score
    pub lexical_score: Option<f32>,    // Raw BM25 score
    pub rerank_score: Option<f32>,     // Cross-encoder score
    pub explanation: Option<HitExplanation>,
    pub metadata: Option<serde_json::Value>,
}

pub enum ScoreSource {
    Lexical,          // BM25 only
    SemanticFast,     // Fast-tier embedding only
    SemanticQuality,  // Quality-tier embedding only
    Hybrid,           // RRF fusion of lexical + semantic
    Reranked,         // Cross-encoder reranked
}

pub enum SearchPhase {
    Initial {
        results: Vec<ScoredResult>,
        latency: Duration,
        metrics: PhaseMetrics,
    },
    Refined {
        results: Vec<ScoredResult>,
        latency: Duration,
        metrics: PhaseMetrics,
        rank_changes: RankChanges,
    },
    RefinementFailed {
        initial_results: Vec<ScoredResult>,
        error: SearchError,
        latency: Duration,
    },
}
```

---

## Core Traits

```rust
/// Async embedding — all implementations must provide this
pub trait Embedder: Send + Sync {
    fn embed<'a>(&'a self, cx: &'a Cx, text: &'a str) -> SearchFuture<'a, Vec<f32>>;
    fn embed_batch<'a>(&'a self, cx: &'a Cx, texts: &'a [&'a str]) -> SearchFuture<'a, Vec<Vec<f32>>>;
    fn dimension(&self) -> usize;
    fn id(&self) -> &str;              // Stored in FSVI headers for version matching
    fn model_name(&self) -> &str;
    fn is_semantic(&self) -> bool;     // false for hash embedder
    fn category(&self) -> ModelCategory;
    fn tier(&self) -> ModelTier;
    fn is_ready(&self) -> bool { true }
}

/// Full-text search backend
pub trait LexicalSearch: Send + Sync {
    fn search<'a>(&'a self, cx: &'a Cx, query: &'a str, limit: usize)
        -> SearchFuture<'a, Vec<ScoredResult>>;
    async fn index_documents<'a>(&'a self, cx: &'a Cx, docs: &'a [IndexableDocument])
        -> SearchResult<()>;
}

/// Cross-encoder reranking
pub trait Reranker: Send + Sync {
    async fn rerank<'a>(&'a self, cx: &'a Cx, candidates: &'a [RerankDocument<'a>])
        -> SearchResult<Vec<RerankScore>>;
}

/// Document filter for search-time exclusion
pub trait SearchFilter: Send + Sync {
    fn matches(&self, doc_id: &str) -> bool;
}
```

---

## Low-Level Utilities (Use Sparingly)

```rust
// SIMD dot product (f16 storage, f32 query)
frankensearch::index::simd::dot_product_f16_f32(embedding: &[f16], query: &[f32]) -> Option<f32>;

// Score normalization (min-max to [0, 1])
frankensearch::fusion::normalize::normalize_scores(scores: &[f32]) -> Vec<f32>;

// RRF fusion (when you manage your own retrieval backends)
frankensearch::fusion::rrf_fuse(
    lexical: &[ScoredResult],
    semantic: &[VectorHit],
    config: &RrfConfig,
) -> Vec<FusedHit>;

// Candidate count helper
frankensearch::fusion::candidate_count(limit: usize, multiplier: usize) -> usize;
```

---

## Feature Flags

```toml
default    = ["hash"]           # Zero-dep hash embedder
semantic   = ["hash", "model2vec", "fastembed"]
hybrid     = ["semantic", "lexical"]
persistent = ["hybrid", "storage"]
durable    = ["persistent", "durability"]
full       = ["durable", "rerank", "ann", "download"]
full-fts5  = ["full", "fts5"]
```

**Recommendation for most projects:** Start with `hybrid`. Add `rerank` if you need cross-encoder precision. Add `persistent` if you need durable metadata.
