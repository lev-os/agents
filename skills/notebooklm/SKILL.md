---
name: notebooklm
description: Import NotebookLM notebooks into markdown-backed knowledge projections with resolved citations and passage-level evidence links. Use when the user wants to turn multi-source research into durable local notes, ask grounded questions over a NotebookLM notebook, or publish cited research into an Obsidian-style vault/CMS adapter.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# NotebookLM - Grounded Research Projection

Use NotebookLM as a research engine, then project the results into durable markdown.

Current reference projection target is an Obsidian vault. Architecturally, that vault is a
publisher/projection adapter, not an authority plane. The valuable part of this skill is the
workflow:

1. curate sources
2. load them into NotebookLM
3. ask grounded questions
4. extract cited passages
5. resolve citations into durable local links
6. publish/project the result

## Prerequisites

### 1. Install notebooklm-py

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

### 2. Authenticate

```bash
notebooklm login
```

Cookies are stored at `~/.notebooklm/storage_state.json`.

### 3. Projection Target

The reference target is a markdown vault with Dataview support.

- Obsidian + Dataview is the default adapter
- Other CMS/publisher targets can consume the same markdown artifacts later

### 4. Optional Templates

Reference templates live in `templates/`:

- `templates/notebook-source.md`
- `templates/dashboard.md`

## Quick Start

```bash
notebooklm status
notebooklm list
notebooklm use <notebook-id>
```

## Workflow Routing

| User says | Workflow |
|-----------|----------|
| "import notebook", "notebooklm import", "import sources" | [workflows/import.md](/Users/jean-patricksmith/.agents/skills/notebooklm/workflows/import.md) |
| "notebooklm ask", "ask notebook", "Q&A" | [workflows/ask.md](/Users/jean-patricksmith/.agents/skills/notebooklm/workflows/ask.md) |

## Reference Projection Layout

```text
Your Vault
├── Notes/NotebookLM/{notebook-slug}/
│   ├── Sources/
│   │   ├── Video Title.md
│   │   └── Article Title.md
│   └── QA/
│       └── 2026-03-07 Emerging Themes.md
└── Notes/Dashboards/
    └── Research Dashboard.md
```

- Source files carry notebook/source metadata plus extracted guides/topics
- Q&A notes resolve `[N]` markers to passage-level wikilinks
- Dashboards/materialized views sit on top of the markdown output

## Data Model

**notebook-source frontmatter:**

```yaml
type: notebook-source
source_id: "uuid"
notebook_id: "uuid"
url: ""
source_type: youtube
status: active
date: YYYY-MM-DD
topics:
  - "[[Topic Name]]"
related:
  - "[[Notes/Dashboards/Dashboard Name]]"
```

**Q&A reference frontmatter:**

```yaml
type: reference
status: current
date: YYYY-MM-DD
source: "notebooklm:{notebook-slug}"
related:
  - "[[Notes/Dashboards/Dashboard Name]]"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/import_sources.py` | Import sources as markdown files with guides/topics |
| `scripts/extract_passages.py` | Extract cited passages into source files |
| `scripts/resolve_citations.py` | Replace `[N]` markers with local links |

All scripts use `Path.cwd()` as the projection root. Run them from the target vault/workspace.
