# Roadmap Item #1: Build System - Research & Implementation Plan

> **Status**: Research Phase
> **Created**: 2025-12-03
> **Roadmap Item**: #1 - Build System
> **Priority**: Must complete before Adapter Architecture (#2)

---

## Research Prompt

**Investigate how to build a context compilation and indexing pipeline for Leviathan:**

### Research Questions

1. **Current Build System Analysis**
   - How does `pnpm build` currently work? What does it compile?
   - What build steps exist in `agent/package.json` (`build:embeddings`)?
   - How does `agent/src/build-embeddings.js` work?
   - What contexts are currently being compiled/indexed?
   - Where are build artifacts stored?

2. **Context Discovery & Loading**
   - How does `agent/src/context-loader.js` discover contexts?
   - What contexts exist in `core/contexts/`?
   - What contexts exist in `poc/skills/contexts/`?
   - How are contexts currently loaded at runtime?
   - What file patterns are used (context.yaml, SKILL.md)?

3. **Embeddings Engine Analysis**
   - What embeddings engines are currently in use?
     - `agent/src/semantic-lookup.js` - Uses what model?
     - `os/agent/performance-engine/semantic-search/` - Uses sentence-transformers/all-mpnet-base-v2
     - `os/kernel/src/embedding_service_impl.go` - Voyage, BGE, OpenAI
     - `poc/lookup/search.js` - Uses Xenova/all-MiniLM-L6-v2
   - Which one should we standardize on?
   - What are the trade-offs (accuracy vs speed vs local vs API)?

4. **Semantic Search Library Benchmarking**
   - **leann**: What is it? Where is it used? How does it work?
   - **docs_rag**: Analyze `tooling/docs_rag/` implementation
     - What embeddings does it use?
     - How does it index documents?
     - What vector DB does it use?
   - **Web search**: What web-based semantic search options exist?
   - **Similar libraries**: Find other local, fast semantic search libraries
     - ChromaDB, Qdrant, Milvus, Weaviate, Pinecone (local)
     - LanceDB, SQLite-VSS
     - FastEmbed, Ollama embeddings
   - **Benchmark criteria**:
     - Speed (indexing time, query latency)
     - Accuracy (semantic search quality)
     - Local vs API (privacy, cost, offline capability)
     - Memory footprint
     - Ease of integration

5. **Build Pipeline Design**
   - What should the build process compile?
     - All `context.yaml` files from `core/contexts/` and `poc/skills/contexts/`
     - Generate embeddings for semantic search
     - Create searchable index
     - Generate metadata/manifests
   - Where should build artifacts live?
   - How to handle incremental builds (only changed contexts)?
   - How to handle dependencies between contexts?

6. **Integration Points**
   - How does this integrate with existing `pnpm build`?
   - How does this integrate with `agent/src/build-embeddings.js`?
   - How does this integrate with `tooling/docs_rag/`?
   - Should this be a new package (`@lev-os/context-builder`)?

### Research Sources

- `package.json` - Root build scripts
- `agent/package.json` - Agent build scripts
- `agent/src/build-embeddings.js` - Current embeddings build
- `agent/src/context-loader.js` - Context discovery
- `agent/src/semantic-lookup.js` - Semantic search implementation
- `tooling/docs_rag/` - Existing RAG system
- `poc/lookup/search.js` - Lookup implementation
- `os/agent/performance-engine/semantic-search/` - Python semantic search
- `core/contexts/` - Context directory structure
- `poc/skills/contexts/` - Skills context directory

### Expected Research Output

1. **Current State Analysis**
   - Map of existing build systems
   - Inventory of contexts to compile
   - Current embeddings engines and their usage

2. **Benchmark Report**
   - Comparison table: leann, docs_rag, web search, similar libs
   - Recommendation with rationale
   - Performance characteristics

3. **Build Pipeline Design**
   - Architecture diagram
   - Build steps and flow
   - Artifact structure
   - Integration points

4. **Implementation Plan**
   - Step-by-step implementation sequence
   - Dependencies and prerequisites
   - Testing strategy

---

## Implementation Plan

### Phase 1: Research & Analysis (Current)

- [ ] **1.1 Analyze current build system**
  - Map `pnpm build` execution flow
  - Document existing build steps
  - Identify what's currently compiled

- [ ] **1.2 Inventory contexts**
  - Scan `core/contexts/` for all context.yaml files
  - Scan `poc/skills/contexts/` for all contexts
  - Document structure and patterns
  - Count total contexts to compile

- [ ] **1.3 Analyze embeddings engines**
  - Document all embeddings implementations
  - Compare models (accuracy, speed, local vs API)
  - Identify which one to standardize on

- [ ] **1.4 Benchmark semantic search libraries**
  - Research leann (what is it?)
  - Analyze docs_rag implementation
  - Research web search options
  - Find similar local/fast libraries
  - Create comparison matrix
  - Make recommendation

**Deliverables**: Research document, benchmark report, current state analysis

---

### Phase 2: Build Pipeline Design

- [ ] **2.1 Design build architecture**
  - Define build steps
  - Design artifact structure
  - Plan incremental build support
  - Design dependency resolution

- [ ] **2.2 Design indexing system**
  - Choose embeddings engine (from benchmark)
  - Choose vector DB/search library (from benchmark)
  - Design index structure
  - Plan query interface

- [ ] **2.3 Integration design**
  - How to integrate with `pnpm build`
  - How to integrate with existing systems
  - Package structure (`@lev-os/context-builder`?)
  - CLI commands

**Deliverables**: Architecture design, integration plan

---

### Phase 3: Implementation

- [ ] **3.1 Create build package**
  - Set up `@lev-os/context-builder` package structure
  - Implement context discovery
  - Implement context loading
  - Implement validation

- [ ] **3.2 Implement embeddings generation**
  - Integrate chosen embeddings engine
  - Generate embeddings for all contexts
  - Handle batch processing
  - Implement caching

- [ ] **3.3 Implement indexing**
  - Set up chosen vector DB/search library
  - Create index structure
  - Populate index with embeddings
  - Implement query interface

- [ ] **3.4 Build integration**
  - Create build script/command
  - Integrate with `pnpm build`
  - Add incremental build support
  - Add build artifacts management

**Deliverables**: Working build system, indexed contexts

---

### Phase 4: Testing & Optimization

- [ ] **4.1 Testing**
  - Test context discovery
  - Test embeddings generation
  - Test indexing
  - Test query performance
  - Test incremental builds

- [ ] **4.2 Performance optimization**
  - Optimize embeddings generation speed
  - Optimize index size
  - Optimize query latency
  - Add caching layers

- [ ] **4.3 Documentation**
  - Document build process
  - Document query interface
  - Document configuration
  - Create usage examples

**Deliverables**: Tested system, optimized performance, documentation

---

## Success Criteria

1. ✅ All contexts from `core/contexts/` and `poc/skills/contexts/` are compiled
2. ✅ Embeddings generated for semantic search
3. ✅ Searchable index created and queryable
4. ✅ Build integrates with `pnpm build`
5. ✅ Incremental builds work (only changed contexts)
6. ✅ Query latency < 100ms for semantic search
7. ✅ Benchmark completed and recommendation documented

---

## Dependencies

- Understanding of current build system
- Benchmark results for semantic search libraries
- Decision on embeddings engine
- Decision on vector DB/search library

---

## Next Steps After Completion

- Roadmap Item #2: Adapter Architecture (can now build adapters)
- Roadmap Item #3: Document Canonical context.yaml Format
- Roadmap Item #6: Pattern/Skill Migration (use build system for indexing)

---

## Notes

- Build system must be fast enough for development workflow
- Should support both local and CI/CD environments
- Consider caching strategies for embeddings
- May need to support multiple embeddings engines (fallback)
- Keep build artifacts versioned/tracked

