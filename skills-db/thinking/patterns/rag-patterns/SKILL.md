---
name: rag-patterns
description: Retrieval-Augmented Generation architectures that enhance LLMs with real-time external knowledge to reduce hallucinations
---

# RAG (Retrieval-Augmented Generation) Patterns

## Overview

RAG augments large language models with real-time external information retrieval, addressing a fundamental limitation: LLMs only know what they were trained on and hallucinate when uncertain. By retrieving relevant documents from vector databases before generation, RAG provides up-to-date, domain-specific context that dramatically improves accuracy. Organizations implementing RAG report 78% improvement in response accuracy for domain-specific queries vs. vanilla LLMs. As of 2025, 63% of enterprise AI projects incorporate retrieval augmentation. The architecture: chunk documents → generate embeddings → index in vector store → retrieve relevant chunks for each query → augment prompt with context → generate response.

## When to Use

- Building AI assistants that need current information beyond LLM training cutoff
- Reducing hallucinations in high-stakes domains (medical, legal, financial)
- Creating internal knowledge base chatbots for companies (docs, policies, support)
- Implementing semantic search with generative summarization
- Personalizing LLM responses with user-specific data or context
- Building AI applications where citations/sources are required
- Scaling knowledge systems without retraining expensive foundation models

## The Process

### Step 1: Prepare and Chunk Documents

Break source documents into chunks (typically 500-1000 tokens). Use structure-aware segmentation respecting paragraphs, sections, or semantic boundaries. Implement maximum/minimum chunk size constraints. Preserve metadata (source, timestamp, author). **Example:** 100-page technical manual → 200 chunks of ~500 tokens each, preserving section headers as metadata for context.

### Step 2: Generate Embeddings and Index

Convert each chunk to vector embedding using embedding model (OpenAI ada-002, Voyage, Cohere). Store vectors in specialized database (Pinecone, Weaviate, Qdrant, ChromaDB). Index for fast similarity search. Update regularly as documents change. **Example:** Use text-embedding-3-small (384 dimensions) for speed or text-embedding-3-large (3072 dimensions) for accuracy, store in Pinecone with metadata filters.

### Step 3: Implement Retrieval Strategy

On user query, generate query embedding using same model. Retrieve top-k most similar chunks (typically k=3-10) via cosine similarity. Optionally rerank results using cross-encoder for accuracy. Consider hybrid search (semantic + keyword). **Example:** User asks "What's our PTO policy?" → embed query → retrieve 5 most similar chunks from HR handbook → rerank by relevance.

### Step 4: Augment Prompt with Retrieved Context

Construct prompt: system instructions + retrieved chunks + user query. Clearly delimit context (XML tags or markdown sections). Include source citations. Instruct model to answer based on provided context only. **Example:** ```<context>Chunk 1: ...\\nChunk 2: ...</context> <question>User query</question> Instructions: Answer using only the context provided. Cite sources.```

### Step 5: Generate Response and Cite Sources

Pass augmented prompt to LLM (GPT-4, Claude, Gemini). Model generates answer grounded in retrieved context. Include source citations (chunk IDs, page numbers, document names). Optionally implement confidence scoring. **Example:** Response: "According to the Employee Handbook (Section 3.2), full-time employees accrue 15 PTO days annually..."

### Step 6: Implement Advanced Patterns (Optional)

Choose architecture based on complexity: (a) Simple RAG - basic retrieval, (b) RAG with Memory - conversational context across turns, (c) Long RAG - process entire documents not just chunks, (d) Self-RAG - model decides when to retrieve and self-critiques, (e) Agentic RAG - multi-step reasoning with iterative retrieval. **Example:** For customer support, use RAG with Memory to maintain conversation context across multi-turn dialog.

### Step 7: Monitor, Evaluate, and Iterate

Track metrics: retrieval precision/recall (are right chunks retrieved?), answer accuracy (is final response correct?), citation quality (sources match claims?), latency (response time). Fine-tune chunking strategy, embedding model, retrieval parameters, and prompt based on performance. **Example:** If users report missing information, increase k from 5 to 10 chunks or switch to hybrid semantic+keyword retrieval.

## Example Application

**Situation:** Legal tech startup building AI contract analyzer. Initial GPT-4 implementation hallucinated legal precedents and provided outdated advice. Needed to ground responses in current case law and firm's proprietary templates.

**Application:**
- Step 1: Chunked 5,000 legal documents (contracts, case law, internal memos) into 50,000 chunks of ~600 tokens, preserving document type and date metadata
- Step 2: Generated embeddings with Cohere embed-english-v3.0, indexed in Weaviate with metadata filters (jurisdiction, practice area, date)
- Step 3: Implemented hybrid retrieval: semantic search (top 10 chunks) + keyword search for legal citations + reranking with cross-encoder → final top 5 chunks
- Step 4: Prompt structure: "You are a legal analyst. Use only the provided context to answer. Cite specific clauses and cases. If unsure, say so."
- Step 5: Claude 4 generated responses with inline citations: "[Source: Contract Template v3.2, Clause 8.1]"
- Step 6: Used Long RAG pattern for full contract analysis (processing entire 50-page contracts as context)
- Step 7: Monitored retrieval quality - discovered date filtering improved accuracy, switched to weekly index updates for case law

**Outcome:** Hallucination rate dropped from 23% to 3%, lawyer trust increased (89% approval rating), response accuracy validated against manual review reached 94%, average contract analysis time reduced from 4 hours to 15 minutes.

## Anti-Patterns

- Chunks too large (>2000 tokens, lose semantic precision) or too small (<200 tokens, lose context)
- Using same embedding model for indexing and different one for querying (incompatible vector spaces)
- Retrieving too few chunks (k=1-2, missing relevant context) or too many (k=50+, overwhelming prompt)
- Not updating index regularly (stale information defeats real-time purpose)
- Failing to cite sources (users can't verify claims, defeats transparency benefit)
- Ignoring retrieval quality metrics (assuming retrieved chunks are always relevant)
- Overcomplicating architecture prematurely (start with Simple RAG, add complexity only if needed)
- Not filtering by metadata when applicable (searching all documents when user needs specific domain)

## Related

- Vector Databases (Pinecone, Weaviate, Qdrant) - infrastructure for embedding storage
- Embedding Models (OpenAI, Cohere, Voyage) - convert text to vector representations
- Prompt Engineering - crafting effective prompts with retrieved context
- Fine-Tuning vs. RAG - trade-offs between approaches (RAG faster to update, fine-tuning better for style)
- LangChain / LlamaIndex - frameworks simplifying RAG implementation
- Semantic Search - retrieval technique underlying RAG
- Knowledge Graphs - alternative/complementary approach to vector retrieval
- Agentic Workflows - multi-step reasoning patterns incorporating RAG
