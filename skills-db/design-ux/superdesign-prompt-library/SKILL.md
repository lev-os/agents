---
name: superdesign-prompt-library
description: |
  Query and retrieve Superdesign prompt-library entries (style prompts, layout prompts, and component prompts)
  from a local JSONL export. Use when you need reusable UI prompt building blocks or want to extract all prompts
  for a style/category/slug.

  Triggers: "superdesign", "design prompt", "prompt library", "style prompt", "layout prompt", "mosaic"
skill_type: tool
category: process-design-prompts
version: 1.0.0
---

# Superdesign Prompt Library

Local exported prompt library with 355 entries.

## Data Files

- `references/superdesign-prompts.jsonl` - normalized prompt entries
- `references/summary.txt` - fetch metadata + counts

## Query Commands

### Find by slug/title/tag

```bash
rg -n "mosaic-grid-architecture-style|Mosaic Grid" ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/superdesign-prompts.jsonl
```

```bash
jq -c 'select(.slug=="mosaic-grid-architecture-style")' ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/superdesign-prompts.jsonl
```

### Extract only style prompts

```bash
jq -r 'select(.style_prompt!=null) | [.slug,.style_prompt] | @tsv' ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/superdesign-prompts.jsonl
```

### Extract all layout prompts for one entry

```bash
jq -r 'select(.slug=="mosaic-grid-architecture-style") | .layout_prompts[]?.prompt' ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/superdesign-prompts.jsonl
```

### Export flat prompt corpus

```bash
jq -r '[.summary_prompt,.style_prompt, (.layout_prompts[]?.prompt), (.special_component_prompts[]?.prompt)] | .[] | select(.!=null)' ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/superdesign-prompts.jsonl > /tmp/superdesign-all-prompts.txt
```

## Record Shape

Each JSONL record contains:

- `id`, `slug`, `title`, `description`, `tags`
- `summary_prompt`
- `style_prompt`
- `layout_prompts[]` (`part`, `prompt`)
- `special_component_prompts[]` (`component`, `prompt`)
- `raw_prompt_json`
## Technique Map

- **rg + jq for slug/title/tag lookup** — Fast local search without loading full corpus; because 355 entries; grep beats parse-all.
- **jq select(.style_prompt!=null)** — Extract only style prompts; because layout/component prompts differ in structure.
- **jq for layout_prompts[]?.prompt** — Per-entry layout extraction; because nested structure needs explicit path.
- **Flat export to file** — summary_prompt, style_prompt, layout_prompts, component_prompts concatenated; because LLM ingestion often needs flat corpus.
- **Record shape awareness** — id, slug, title, description, tags, summary_prompt, style_prompt, layout_prompts, special_component_prompts; because query patterns depend on structure.

## Technique Notes

Data: references/superdesign-prompts.jsonl, references/summary.txt. Path: ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/. Use jq -c for single record, jq -r for tab/newline output. Triggers: superdesign, design prompt, prompt library, mosaic.

---

## Prompt Architect Overlay

**Role Definition:** Superdesign prompt library query tool. Retrieves style, layout, and component prompts from local JSONL export. Provides reusable UI prompt building blocks.

**Input Contract:** Accepts slug, title, tag, or category query. Style/layout/component extraction request. "Extract all prompts for X" or "get prompts for style/category."

**Output Contract:** JSONL records or extracted prompt text. jq/rg command examples for self-service. Record structure (id, slug, style_prompt, layout_prompts, etc.). Flat export when requested.

**Edge Cases & Fallbacks:** If slug not found→suggest rg partial match or list available slugs. If structure unclear→show record shape. If path wrong→use ~/.agents/skills-db/design-ux/superdesign-prompt-library/references/.
