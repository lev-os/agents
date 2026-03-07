#!/usr/bin/env python3
"""Extract cited_text passages from Q&A JSONs and append to source files."""
import argparse
import json
import re
import sys
from pathlib import Path

VAULT = Path.cwd()


def safe_filename(title: str) -> str:
    """Same logic as import_sources.py."""
    title = re.sub(r'[/:*?"<>|]', "-", title)
    title = re.sub(r"\s+", " ", title).strip()
    if len(title) > 120:
        title = title[:120].rstrip(" -")
    return title


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract NotebookLM cited passages into source files"
    )
    parser.add_argument("--qa", nargs="+", required=True, help="Q&A JSON files")
    parser.add_argument("--sources", required=True, help="Sources JSON file")
    parser.add_argument("--slug", required=True, help="Notebook slug")
    args = parser.parse_args()

    with open(args.sources) as f:
        sources_data = json.load(f)

    source_titles: dict[str, str] = {}
    for source in sources_data["sources"]:
        title = source["title"].strip()
        if title == "- YouTube" or len(title) < 3:
            continue
        source_titles[source["id"]] = title

    source_chunks: dict[str, list[str]] = {}
    seen_keys: dict[str, set[str]] = {}

    for qa_file in args.qa:
        with open(qa_file) as f:
            data = json.load(f)
        for ref in data["references"]:
            cited_text = ref.get("cited_text", "").strip()
            if not cited_text:
                continue
            source_id = ref["source_id"]
            if source_id not in source_titles:
                continue
            dedup_key = cited_text[:100]
            if source_id not in seen_keys:
                seen_keys[source_id] = set()
                source_chunks[source_id] = []
            if dedup_key not in seen_keys[source_id]:
                seen_keys[source_id].add(dedup_key)
                source_chunks[source_id].append(cited_text)

    print(f"Sources with passages: {len(source_chunks)}", file=sys.stderr)

    sources_dir = VAULT / "Notes" / "NotebookLM" / args.slug / "Sources"
    updated = 0
    skipped = 0

    for source_id, chunks in source_chunks.items():
        title = source_titles[source_id]
        filename = safe_filename(title) + ".md"
        filepath = sources_dir / filename

        if not filepath.exists():
            print(f"  MISSING: {filename}", file=sys.stderr)
            skipped += 1
            continue

        content = filepath.read_text()
        if "## Cited Passages" in content:
            existing_keys = set()
            existing_count = 0
            for match in re.finditer(
                r"### Passage (\d+)\n\n(.+?)(?=\n### Passage |\Z)",
                content,
                re.DOTALL,
            ):
                existing_count = max(existing_count, int(match.group(1)))
                existing_keys.add(match.group(2).strip()[:100])

            new_chunks = [chunk for chunk in chunks if chunk[:100] not in existing_keys]
            if not new_chunks:
                print(
                    f"  CURRENT: {filename} ({existing_count} passages, no new)",
                    file=sys.stderr,
                )
                skipped += 1
                continue

            new_passages = ""
            for index, chunk in enumerate(new_chunks, existing_count + 1):
                new_passages += f"\n### Passage {index}\n\n{chunk}\n"

            filepath.write_text(content.rstrip() + "\n" + new_passages)
            print(
                f"  APPENDED: {filename} (+{len(new_chunks)} passages, "
                f"{existing_count + len(new_chunks)} total)",
                file=sys.stderr,
            )
            updated += 1
        else:
            passages = "\n## Cited Passages\n"
            for index, chunk in enumerate(chunks, 1):
                passages += f"\n### Passage {index}\n\n{chunk}\n"

            filepath.write_text(content.rstrip() + "\n" + passages)
            print(f"  CREATED: {filename} ({len(chunks)} passages)", file=sys.stderr)
            updated += 1

    print(f"\nDone: {updated} updated, {skipped} skipped", file=sys.stderr)

    mapping: dict[str, dict[str, int]] = {}
    for source_id, chunks in source_chunks.items():
        mapping[source_id] = {}
        for index, chunk in enumerate(chunks, 1):
            mapping[source_id][chunk[:100]] = index
    json.dump(mapping, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
