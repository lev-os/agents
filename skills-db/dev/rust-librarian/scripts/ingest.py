"""
Rust Librarian Ingestion Pipeline
Ports the os/agent/performance-engine Go docs pattern to Rust books.

Usage:
    python3 ingest.py --source rust-book --path ~/lev/workshop/intake/rust-book/src/
    python3 ingest.py --source rust-by-example --path ~/lev/workshop/intake/rust-by-example/src/
    python3 ingest.py --source error-index --path ~/lev/workshop/intake/error-index/
    python3 ingest.py --status  # Show collection stats
"""

import argparse
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# --- Schema (mirrors os/agent/performance-engine/semantic-search/schemas/metadata.py) ---

class ContentType(Enum):
    FRAMEWORK = "framework"
    REQUIREMENT = "requirement"
    PRINCIPLE = "principle"


class Scope(Enum):
    GLOBAL = "global"
    PROJECT = "project"


class HierarchyLevel(Enum):
    FILE = "file"
    PACKAGE = "package"
    FUNCTION = "function"
    CONCEPT = "concept"
    MODULE = "module"
    CLASS = "class"


class DocumentType(Enum):
    API = "api"
    GUIDE = "guide"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    STANDARD = "standard"
    EXAMPLE = "example"


@dataclass
class DocumentMetadata:
    id: str
    content_type: ContentType
    project: str
    scope: Scope
    framework: str = "rust"
    document_type: DocumentType = DocumentType.REFERENCE
    hierarchy_level: HierarchyLevel = HierarchyLevel.CONCEPT
    authority: str = "external"
    source_file: str = ""
    source_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    summary: str = ""
    custom_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_type": self.content_type.value,
            "project": self.project,
            "scope": self.scope.value,
            "framework": self.framework,
            "document_type": self.document_type.value,
            "hierarchy_level": self.hierarchy_level.value,
            "authority": self.authority,
            "source_file": self.source_file,
            "source_url": self.source_url,
            "tags": self.tags,
            "keywords": self.keywords,
            "summary": self.summary,
            "custom_fields": self.custom_fields,
            "last_modified": datetime.now().isoformat(),
        }


# --- Source configs ---

SOURCES = {
    "rust-book": {
        "repo": "https://github.com/rust-lang/book",
        "collection": "project-rust-books-guides",
        "content_type": ContentType.FRAMEWORK,
        "doc_type": DocumentType.GUIDE,
        "url_base": "https://doc.rust-lang.org/book/",
        "glob": "**/*.md",
        "book_name": "the-rust-programming-language",
    },
    "rust-by-example": {
        "repo": "https://github.com/rust-lang/rust-by-example",
        "collection": "project-rust-books-guides",
        "content_type": ContentType.FRAMEWORK,
        "doc_type": DocumentType.TUTORIAL,
        "url_base": "https://doc.rust-lang.org/rust-by-example/",
        "glob": "**/*.md",
        "book_name": "rust-by-example",
    },
    "rustonomicon": {
        "repo": "https://github.com/rust-lang/nomicon",
        "collection": "project-rust-books-guides",
        "content_type": ContentType.FRAMEWORK,
        "doc_type": DocumentType.GUIDE,
        "url_base": "https://doc.rust-lang.org/nomicon/",
        "glob": "**/*.md",
        "book_name": "rustonomicon",
    },
    "rust-design-patterns": {
        "repo": "https://github.com/rust-unofficial/patterns",
        "collection": "project-rust-patterns",
        "content_type": ContentType.PRINCIPLE,
        "doc_type": DocumentType.STANDARD,
        "url_base": "https://rust-unofficial.github.io/patterns/",
        "glob": "**/*.md",
        "book_name": "rust-design-patterns",
    },
    "rust-api-guidelines": {
        "repo": "https://github.com/rust-lang/api-guidelines",
        "collection": "project-rust-patterns",
        "content_type": ContentType.PRINCIPLE,
        "doc_type": DocumentType.STANDARD,
        "url_base": "https://rust-lang.github.io/api-guidelines/",
        "glob": "**/*.md",
        "book_name": "rust-api-guidelines",
    },
    "rust-cookbook": {
        "repo": "https://github.com/rust-lang-nursery/rust-cookbook",
        "collection": "project-rust-patterns",
        "content_type": ContentType.FRAMEWORK,
        "doc_type": DocumentType.EXAMPLE,
        "url_base": "https://rust-lang-nursery.github.io/rust-cookbook/",
        "glob": "**/*.md",
        "book_name": "rust-cookbook",
    },
}

# Files to skip (TOC, summary, etc.)
SKIP_FILES = {"SUMMARY.md", "README.md", "CONTRIBUTING.md", "LICENSE.md"}


# --- Chunker ---

def extract_chapter_info(filepath: str) -> Dict[str, Any]:
    """Extract chapter/section number from filename like ch04-01-ownership.md."""
    name = Path(filepath).stem
    chapter_match = re.match(r"ch(\d+)-(\d+)-(.+)", name)
    if chapter_match:
        return {
            "chapter": int(chapter_match.group(1)),
            "section": f"{chapter_match.group(1)}.{chapter_match.group(2)}",
            "slug": chapter_match.group(3),
        }
    return {"chapter": 0, "section": "0", "slug": name}


def chunk_markdown_by_sections(
    content: str, filepath: str, source_config: Dict
) -> List[Dict[str, Any]]:
    """Split a markdown file into chunks by ## headings."""
    chunks = []
    chapter_info = extract_chapter_info(filepath)
    relative_path = filepath

    # Split by ## headings
    sections = re.split(r"\n(?=## )", content)

    for i, section in enumerate(sections):
        section = section.strip()
        if not section or len(section) < 50:
            continue

        # Extract heading
        heading_match = re.match(r"^##?\s+(.+)", section)
        heading = heading_match.group(1).strip() if heading_match else f"Section {i}"

        # Extract keywords from code blocks and key terms
        code_blocks = re.findall(r"```rust\n(.*?)```", section, re.DOTALL)
        keywords = extract_rust_keywords(section)

        # Build URL
        slug = re.sub(r"[^a-z0-9-]", "", heading.lower().replace(" ", "-"))
        source_url = f"{source_config['url_base']}{Path(filepath).stem}.html#{slug}"

        chunk_id = f"{source_config['book_name']}-{chapter_info['slug']}-s{i}"

        metadata = DocumentMetadata(
            id=chunk_id,
            content_type=source_config["content_type"],
            project="rust-knowledge",
            scope=Scope.GLOBAL,
            document_type=source_config["doc_type"],
            hierarchy_level=HierarchyLevel.CONCEPT,
            source_file=relative_path,
            source_url=source_url,
            tags=extract_tags(section),
            keywords=keywords,
            summary=heading[:200],
            custom_fields={
                "book": source_config["book_name"],
                "chapter": chapter_info["chapter"],
                "section": chapter_info["section"],
                "heading": heading,
                "has_code_examples": len(code_blocks) > 0,
                "code_example_count": len(code_blocks),
            },
        )

        chunks.append({"content": section, "metadata": metadata})

    return chunks


def extract_rust_keywords(text: str) -> List[str]:
    """Extract Rust-specific keywords from text."""
    rust_terms = {
        "ownership", "borrowing", "lifetime", "trait", "impl", "struct",
        "enum", "match", "Option", "Result", "Vec", "String", "Box",
        "Rc", "Arc", "RefCell", "Mutex", "async", "await", "Future",
        "Iterator", "closure", "macro", "unsafe", "Send", "Sync",
        "Clone", "Copy", "Drop", "Deref", "From", "Into", "TryFrom",
        "Display", "Debug", "Serialize", "Deserialize", "Error",
        "HashMap", "BTreeMap", "HashSet", "PhantomData", "Pin",
        "tokio", "serde", "clap", "anyhow", "thiserror", "tracing",
    }
    found = []
    for term in rust_terms:
        if term.lower() in text.lower() or term in text:
            found.append(term)
    return found[:15]  # Cap at 15


def extract_tags(text: str) -> List[str]:
    """Extract topic tags from content."""
    tag_patterns = {
        "ownership": r"\bownership\b",
        "borrowing": r"\bborrow(ing|ed|s)?\b",
        "lifetimes": r"\blifetime",
        "traits": r"\btrait\b",
        "generics": r"\bgeneric",
        "error-handling": r"\bResult\b.*\bErr",
        "concurrency": r"\b(thread|async|concurrent)",
        "closures": r"\bclosure",
        "iterators": r"\biterator|\.iter\(\)",
        "pattern-matching": r"\bmatch\b.*\{",
        "smart-pointers": r"\b(Box|Rc|Arc|RefCell)\b",
        "unsafe": r"\bunsafe\b",
        "macros": r"\bmacro",
        "modules": r"\bmod\b",
        "testing": r"\b#\[test\]",
        "memory": r"\b(heap|stack|alloc)",
    }
    tags = []
    for tag, pattern in tag_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            tags.append(tag)
    return tags[:10]


# --- Ingestion ---

def ingest_source(source_name: str, path: str) -> Dict[str, Any]:
    """Ingest a Rust documentation source into Qdrant."""
    if source_name not in SOURCES:
        raise ValueError(f"Unknown source: {source_name}. Known: {list(SOURCES.keys())}")

    config = SOURCES[source_name]
    source_path = Path(path)

    if not source_path.exists():
        raise FileNotFoundError(f"Source path not found: {path}")

    # Find all markdown files
    md_files = sorted(source_path.glob(config["glob"]))
    md_files = [f for f in md_files if f.name not in SKIP_FILES]

    logger.info(f"Found {len(md_files)} markdown files in {path}")

    # Chunk all files
    all_chunks = []
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            relative = str(md_file.relative_to(source_path))
            chunks = chunk_markdown_by_sections(content, relative, config)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.warning(f"Failed to process {md_file}: {e}")

    logger.info(f"Generated {len(all_chunks)} chunks from {source_name}")

    # Try to import and use Qdrant + embeddings
    try:
        from sentence_transformers import SentenceTransformer
        from qdrant_client import QdrantClient
        from qdrant_client.models import (
            Distance,
            HnswConfigDiff,
            PointStruct,
            VectorParams,
        )

        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        client = QdrantClient(host=qdrant_host, port=qdrant_port)

        collection = config["collection"]

        # Create collection if needed
        collections = [c.name for c in client.get_collections().collections]
        if collection not in collections:
            client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                hnsw_config=HnswConfigDiff(m=16, ef_construct=100),
            )
            logger.info(f"Created collection: {collection}")

        # Load embedding model
        model = SentenceTransformer("all-mpnet-base-v2")
        logger.info("Loaded embedding model: all-mpnet-base-v2")

        # Embed and upsert in batches
        batch_size = 64
        total_upserted = 0

        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i : i + batch_size]
            texts = [c["content"][:2048] for c in batch]  # Truncate for embedding
            embeddings = model.encode(texts, show_progress_bar=False)

            points = []
            for j, chunk in enumerate(batch):
                point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, chunk["metadata"].id))
                payload = {**chunk["metadata"].to_dict(), "content": chunk["content"]}
                points.append(
                    PointStruct(id=point_id, vector=embeddings[j].tolist(), payload=payload)
                )

            client.upsert(collection_name=collection, points=points)
            total_upserted += len(points)
            logger.info(
                f"  Batch {i // batch_size + 1}: upserted {len(points)} points "
                f"({total_upserted}/{len(all_chunks)})"
            )

        return {
            "status": "completed",
            "source": source_name,
            "collection": collection,
            "files_processed": len(md_files),
            "chunks_created": len(all_chunks),
            "chunks_upserted": total_upserted,
        }

    except (ImportError, Exception) as e:
        # No qdrant/sentence-transformers or server unavailable — save chunks as JSON
        output_path = Path(f"~/lev/workshop/intake/{source_name}-chunks.json").expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        serializable = []
        for chunk in all_chunks:
            serializable.append({
                "content": chunk["content"],
                "metadata": chunk["metadata"].to_dict(),
            })

        with open(output_path, "w") as f:
            json.dump(serializable, f, indent=2, default=str)

        return {
            "status": "saved_json",
            "source": source_name,
            "output": str(output_path),
            "chunks_created": len(all_chunks),
            "note": f"Install deps first: pip install sentence-transformers qdrant-client ({e})",
        }


def show_status():
    """Show collection stats from Qdrant."""
    try:
        from qdrant_client import QdrantClient

        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", "6333"))
        client = QdrantClient(host=host, port=port)

        collections = client.get_collections().collections
        rust_collections = [c for c in collections if "rust" in c.name]

        if not rust_collections:
            print("No Rust collections found in Qdrant.")
            return

        print(f"\nRust Librarian Collections ({host}:{port}):")
        print("-" * 60)
        for col in rust_collections:
            info = client.get_collection(col.name)
            print(f"  {col.name}: {info.points_count} vectors")
        print()

    except Exception as e:
        print(f"Cannot connect to Qdrant: {e}")


def main():
    parser = argparse.ArgumentParser(description="Rust Librarian Ingestion")
    parser.add_argument("--source", choices=list(SOURCES.keys()), help="Source to ingest")
    parser.add_argument("--path", help="Path to source content")
    parser.add_argument("--status", action="store_true", help="Show collection stats")
    parser.add_argument("--clone", action="store_true", help="Clone source repo first")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.status:
        show_status()
        return

    if not args.source:
        parser.error("--source is required (unless using --status)")

    config = SOURCES[args.source]

    # Clone if requested
    if args.clone:
        intake_dir = Path(f"~/lev/workshop/intake/{args.source}").expanduser()
        if not intake_dir.exists():
            import subprocess
            logger.info(f"Cloning {config['repo']}...")
            subprocess.run(
                ["git", "clone", "--depth", "1", config["repo"], str(intake_dir)],
                check=True,
            )
        path = str(intake_dir / "src") if (intake_dir / "src").exists() else str(intake_dir)
    elif args.path:
        path = args.path
    else:
        parser.error("--path or --clone is required")

    result = ingest_source(args.source, path)
    print(f"\n{json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
