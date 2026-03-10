---
name: rust-librarian
description: |
  [WHAT] Rust knowledge ingestion and semantic search system. Indexes Rust books, patterns,
  error examples, and crate documentation into Qdrant for agent-accessible retrieval.
  [HOW] Clones Rust book sources (markdown), chunks by chapter/section/concept, embeds via
  sentence-transformers (all-mpnet-base-v2, 768D), upserts to Qdrant collections following
  the os/agent/performance-engine schema. Provides search commands for agents.
  [WHEN] Use when ingesting new Rust learning material, querying Rust patterns during planning,
  or looking up idiomatic solutions to Rust compiler errors.
  [WHY] Agents writing Rust need access to canonical patterns, not just LLM training data.
  RAG over curated Rust books produces more idiomatic, correct code.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch
tags: rust, knowledge-base, qdrant, semantic-search, ingestion, patterns, librarian
---

# Rust Librarian

Semantic knowledge system for Rust development. Ingests authoritative Rust sources into
Qdrant and provides search tools for agents planning or writing Rust code.

## Architecture

Mirrors the Go docs indexer pattern from `os/agent/performance-engine/`:

```
[Rust Book Sources (GitHub markdown)]
        |
        v
[Chunker: split by chapter/section/concept]
        |
        v
[Embedder: sentence-transformers all-mpnet-base-v2 (768D)]
        |
        v
[Qdrant Collections]
  - project-rust-stdlib-framework-docs   (std library API docs)
  - project-rust-books-guides            (The Rust Book, Rustonomicon, etc.)
  - project-rust-patterns                (Design patterns, idioms)
  - project-rust-error-examples          (Compiler errors + fixes)
  - project-rust-crate-docs              (Popular crate documentation)
        |
        v
[Search API: POST /search with metadata filtering]
```

## Commands

### `/rust-librarian ingest <source>`

Ingest a Rust knowledge source into Qdrant.

**Supported sources:**

| Source | Repository | Collection |
|--------|-----------|------------|
| `rust-book` | `github.com/rust-lang/book` | `project-rust-books-guides` |
| `rust-by-example` | `github.com/rust-lang/rust-by-example` | `project-rust-books-guides` |
| `rustonomicon` | `github.com/rust-lang/nomicon` | `project-rust-books-guides` |
| `rust-api-guidelines` | `github.com/rust-lang/api-guidelines` | `project-rust-patterns` |
| `rust-design-patterns` | `github.com/rust-unofficial/patterns` | `project-rust-patterns` |
| `rust-cookbook` | `github.com/rust-lang-nursery/rust-cookbook` | `project-rust-patterns` |
| `effective-rust` | `github.com/brson/effective-rust` (or local) | `project-rust-patterns` |
| `std` | `doc.rust-lang.org/std` | `project-rust-stdlib-framework-docs` |
| `error-index` | `doc.rust-lang.org/error_codes` | `project-rust-error-examples` |
| `crate:<name>` | `docs.rs/<name>` | `project-rust-crate-docs` |

**Ingestion pipeline:**

```bash
# 1. Clone source
git clone --depth 1 https://github.com/rust-lang/book ~/lev/workshop/intake/rust-book

# 2. Run chunker (Python, reuses os/agent schema)
python3 rust_librarian/ingest.py --source rust-book --path ~/lev/workshop/intake/rust-book/src/
```

### `/rust-librarian search <query>`

Search the Rust knowledge base. Returns ranked results with source attribution.

```bash
# Pattern search
/rust-librarian search "lifetime elision rules"

# Error search
/rust-librarian search "error[E0502] cannot borrow as mutable"

# Idiom search
/rust-librarian search "builder pattern in Rust"
```

### `/rust-librarian status`

Show ingestion status across all collections.

## Chunking Strategy

Different sources need different chunking:

### Books (The Rust Book, Rustonomicon)
- **Unit**: Chapter section (## heading)
- **Metadata**: chapter_number, section_title, book_name
- **Hierarchy**: CONCEPT
- **DocumentType**: GUIDE or TUTORIAL
- **Content**: Full section text including code examples

### API Docs (std library)
- **Unit**: Per item (struct, enum, fn, trait, module)
- **Metadata**: module_path, item_type, signature
- **Hierarchy**: FUNCTION / CLASS / MODULE / PACKAGE
- **DocumentType**: API
- **Content**: Signature + documentation + examples

### Patterns / Guidelines
- **Unit**: Per pattern (one pattern = one chunk)
- **Metadata**: pattern_name, category, applicability
- **Hierarchy**: CONCEPT
- **DocumentType**: STANDARD
- **Content**: Description + when to use + code example + tradeoffs

### Error Examples
- **Unit**: Per error code
- **Metadata**: error_code (E0xxx), category (borrow, lifetime, type)
- **Hierarchy**: CONCEPT
- **DocumentType**: EXAMPLE
- **Content**: Error message + explanation + fix + before/after code

## Qdrant Schema

Reuses `DocumentMetadata` from `os/agent/performance-engine/semantic-search/schemas/metadata.py`:

```python
DocumentMetadata(
    id="rust-book-ch04-ownership",
    content_type=ContentType.FRAMEWORK,   # or PRINCIPLE for patterns
    project="rust-knowledge",
    scope=Scope.GLOBAL,
    framework="rust",
    document_type=DocumentType.GUIDE,
    hierarchy_level=HierarchyLevel.CONCEPT,
    authority="external",                  # from official Rust docs
    source_file="src/ch04-01-what-is-ownership.md",
    source_url="https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html",
    tags=["ownership", "memory", "borrowing"],
    keywords=["ownership", "move", "copy", "drop", "stack", "heap"],
    summary="Rust ownership: each value has one owner, transfers on assignment",
    custom_fields={
        "book": "the-rust-programming-language",
        "chapter": 4,
        "section": "4.1",
        "rust_concepts": ["ownership", "move-semantics"]
    }
)
```

**Collection config** (768D, Cosine, HNSW m=16 ef=100):
```python
VectorParams(size=768, distance=Distance.COSINE)
HnswConfigDiff(m=16, ef_construct=100)
```

## Integration Points

### SDLC Planning (workflow-rust-plan)
The `workflow-rust-plan` calls this skill's search before generating code plans:
1. Extract Rust concepts from task description
2. Query `project-rust-patterns` for relevant idioms
3. Query `project-rust-error-examples` for known pitfalls
4. Inject results into planning context

### Compile-Fix Loop (RustCoder pattern)
When `cargo build` fails:
1. Extract error code from compiler output (use `--message-format=json`)
2. Query `project-rust-error-examples` for the error code
3. Return fix examples + explanation to the fixing LLM

### Agent Context Enrichment
Any agent writing Rust can call:
```
/rust-librarian search "how to implement Display trait"
```

## Bootstrapping (priority order)

```bash
/rust-librarian ingest rust-book            # Foundation (~20 chapters)
/rust-librarian ingest rust-by-example      # Practical examples
/rust-librarian ingest error-index          # All compiler error codes
/rust-librarian ingest rust-design-patterns  # Idioms and patterns
/rust-librarian ingest rust-api-guidelines   # API design rules
/rust-librarian ingest rustonomicon         # Unsafe Rust
/rust-librarian ingest crate:serde          # Serialization
/rust-librarian ingest crate:tokio          # Async runtime
/rust-librarian ingest crate:clap           # CLI parsing
```

## Dependencies

- Python 3.8+ with `sentence-transformers`, `qdrant-client`
- Qdrant on localhost:6333 (or QDRANT_HOST)
- Git for cloning book sources
- Reuses schema from `os/agent/performance-engine/semantic-search/`

## Related

- `os/agent/performance-engine/` -- Go docs indexer (prior art, same architecture)
- `workflow-rust-plan` -- Planning workflow that consumes search
- `plugins/core-sdlc/` -- SDLC plan-execute-verify flow
- RustCoder (`~/lev/workshop/intake/RustCoder/`) -- Compile-fix loop reference
