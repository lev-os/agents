#!/usr/bin/env python3
"""Resolve [N] citations in NotebookLM answers to local wikilinks."""
import argparse
import json
import re
import sys
from pathlib import Path

VAULT = Path.cwd()


def build_source_map(sources_file: str) -> dict[str, str]:
    """Build source_id -> safe filename mapping."""
    with open(sources_file) as f:
        data = json.load(f)

    mapping: dict[str, str] = {}
    for source in data["sources"]:
        title = source["title"].strip()
        if title == "- YouTube" or len(title) < 3:
            continue
        safe = re.sub(r'[/:*?"<>|]', "-", title)
        safe = re.sub(r"\s+", " ", safe).strip()
        if len(safe) > 120:
            safe = safe[:120].rstrip(" -")
        mapping[source["id"]] = safe
    return mapping


def expand_citation_spec(spec_text: str) -> list[int]:
    """Expand '1, 2, 5-8' into concrete citation numbers."""
    numbers: list[int] = []
    for part in spec_text.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                numbers.extend(range(int(start.strip()), int(end.strip()) + 1))
            except ValueError:
                continue
        else:
            try:
                numbers.append(int(part))
            except ValueError:
                continue
    return numbers


def build_chunk_map(references: list[dict]) -> dict[int, dict]:
    """Build answer citation index -> unique evidence chunk mapping."""
    seen_texts: dict[str, int] = {}
    chunks: dict[int, dict] = {}
    for ref in references:
        key = ref.get("cited_text", "")[:100]
        if key and key not in seen_texts:
            idx = len(seen_texts) + 1
            seen_texts[key] = idx
            chunks[idx] = ref
    return chunks


def resolve_answer(
    answer: str,
    references: list[dict],
    source_map: dict[str, str],
    slug: str,
    passage_map: dict[str, dict[str, int]] | None = None,
) -> tuple[str, list[str], dict]:
    """Replace [N] markers with source/passage links."""
    chunk_map = build_chunk_map(references)
    sources_path = f"Notes/NotebookLM/{slug}/Sources"

    cited_sources: set[str] = set()
    total_sources = set(source_map.values())
    passage_hits = 0
    passage_misses = 0

    def make_wikilink(title: str, ref: dict | None = None) -> str:
        nonlocal passage_hits, passage_misses
        anchor = ""
        if passage_map and ref:
            source_id = ref["source_id"]
            chunk_key = ref.get("cited_text", "")[:100]
            source_passages = passage_map.get(source_id, {})
            passage_num = source_passages.get(chunk_key)
            if passage_num:
                anchor = f"#Passage {passage_num}"
                passage_hits += 1
            else:
                passage_misses += 1
        return f"[[{sources_path}/{title}{anchor}|{title}]]"

    def replace_citation(match: re.Match[str]) -> str:
        spec = match.group(1)
        numbers = expand_citation_spec(spec)

        seen: set[tuple] = set()
        links: list[str] = []
        for number in numbers:
            ref = chunk_map.get(number)
            if not ref:
                continue
            source_id = ref["source_id"]
            title = source_map.get(source_id)
            if not title:
                continue

            chunk_key = ref.get("cited_text", "")[:100]
            passage_num = None
            if passage_map:
                source_passages = passage_map.get(source_id, {})
                passage_num = source_passages.get(chunk_key)
            dedup_key = (source_id, passage_num) if passage_num else (source_id,)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            cited_sources.add(title)
            links.append(make_wikilink(title, ref))

        if not links:
            return match.group(0)

        return f" ({', '.join(links)})"

    resolved = re.sub(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]", replace_citation, answer)

    stats = {
        "unique_chunks": len(chunk_map),
        "total_refs": len(references),
        "cited_sources": len(cited_sources),
        "total_sources": len(total_sources),
        "uncited_sources": sorted(total_sources - cited_sources),
        "passage_hits": passage_hits,
        "passage_misses": passage_misses,
    }

    return resolved, sorted(cited_sources), stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve NotebookLM citations")
    parser.add_argument("--qa", required=True, help="NotebookLM ask --json output")
    parser.add_argument("--sources", required=True, help="Source list JSON")
    parser.add_argument("--slug", required=True, help="Notebook slug")
    parser.add_argument("--title", help="Reference note title")
    parser.add_argument("--dashboard", help="Dashboard title")
    parser.add_argument("--output", help="Vault-relative output path")
    parser.add_argument("--passages", help="Passage mapping JSON")
    parser.add_argument("--date", help="Date for frontmatter")
    args = parser.parse_args()

    source_map = build_source_map(args.sources)
    print(f"Source map: {len(source_map)} entries", file=sys.stderr)

    passage_map = None
    if args.passages:
        with open(args.passages) as f:
            passage_map = json.load(f)
        print(f"Passage map: {len(passage_map)} sources", file=sys.stderr)

    with open(args.qa) as f:
        qa_data = json.load(f)

    resolved, cited_sources, stats = resolve_answer(
        qa_data["answer"],
        qa_data["references"],
        source_map,
        args.slug,
        passage_map,
    )

    print(
        f"Refs: {stats['total_refs']} raw -> {stats['unique_chunks']} unique chunks",
        file=sys.stderr,
    )
    print(
        f"Sources cited: {stats['cited_sources']}/{stats['total_sources']}",
        file=sys.stderr,
    )
    if passage_map:
        print(
            f"Passage anchors: {stats['passage_hits']} linked, "
            f"{stats['passage_misses']} source-only",
            file=sys.stderr,
        )

    if not args.output:
        print(resolved)
        return

    if not args.title or not args.dashboard:
        raise SystemExit("--title and --dashboard are required with --output")

    output_path = VAULT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    date = args.date or qa_data.get("created_at", "")[:10]

    related_path = f"Notes/Dashboards/{args.dashboard}"
    cited_sources_block = "\n".join(f"- [[{s}]]" for s in cited_sources) or "- none"
    uncited_sources = stats["uncited_sources"]
    uncited_block = "\n".join(f"- [[{s}]]" for s in uncited_sources) or "- none"

    content = f"""---
type: reference
status: current
date: {date}
source: "notebooklm:{args.slug}"
related:
  - "[[{related_path}]]"
---

# {args.title}

## Answer

{resolved}

## Sources Referenced

{cited_sources_block}

## Uncited Sources

{uncited_block}
"""

    output_path.write_text(content)
    print(f"Wrote {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
