---
name: workflow-cited-research
description: Build a grounded research loop from source acquisition through NotebookLM synthesis into local markdown/CMS projections. Invoke with /workflow cited-research.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Workflow: Cited Research

## Trigger

Run when the user wants a repeatable research workflow that:

- curates web/video/doc sources
- synthesizes them with citations
- persists the output locally
- optionally projects the result into Obsidian or another publisher target

This is the workflow-level synthesis of:

- `lev-research` for source acquisition
- `notebooklm` for grounded multi-source reasoning
- publisher/CMS projections for durable local output

## Inputs

- Research question or theme
- Source seed list, or permission to discover sources
- Preferred source classes: `youtube`, `web`, `pdf`, `notes`
- Projection target:
  - markdown only
  - Obsidian vault
  - future CMS/publisher target
- Notebook slug and dashboard title

## Steps

1. Acquire or curate sources.
   Use `lev-research` or user-provided URLs to build a deliberate source set. Prefer curated relevance over raw volume.

2. Materialize a source manifest.
   Save the final source list as JSON or markdown so the research input is inspectable and reproducible.

3. Create or select the NotebookLM notebook.
   Authenticate, create/select notebook, and add sources in batches.

4. Import the notebook into local markdown.
   Run the `notebooklm` import workflow to create source files and a dashboard/materialized view.

5. Ask grounded questions.
   Use `notebooklm ask --new --json` for each research question. Extract cited passages and resolve citations into durable local links.

6. Project the result.
   Treat Obsidian as a projection target, not a new authority. If a different publisher exists later, reuse the same markdown artifacts.

7. Close the loop.
   Produce:
   - source manifest
   - Q&A notes
   - cited passage map
   - concise synthesis of themes, gaps, and next actions

## Team

| Role | Responsibility |
|------|---------------|
| Source Curator | builds and prunes the source set |
| Notebook Operator | manages notebook creation, auth, and source import |
| Citation Resolver | extracts passages and resolves evidence links |
| Publisher Adapter | projects markdown output into Obsidian/CMS targets |

## Outputs

- `/tmp/notebooklm-sources.json` or equivalent source manifest
- `Notes/NotebookLM/{slug}/Sources/*.md`
- `Notes/NotebookLM/{slug}/QA/*.md`
- `Notes/Dashboards/{dashboard}.md`
- A short synthesis note with themes, gaps, and follow-up prompts

## Validation

- Source manifest exists and matches the notebook contents
- Q&A notes contain local resolved citations, not bare `[N]` markers
- Source files contain cited passages
- Projection target renders the result without depending on the NotebookLM web UI
- Workflow can be rerun with a fresh notebook/question set without changing the core steps
