---
name: prior-art
description: Use when you need an evidence-first provenance report from `cass`, repo docs, `.lev`, `~/.agents/diagrams`, `qmd`, `lev get`, or `rg`.
---

# Prior Art

Find the existing evidence first, then summarize what it means. This skill is narrower than `lev-research`: it is for provenance, lineage, decision history, and “what already exists?” questions.

If the repo itself is unfamiliar, pair this with `codebase-archaeology` first so the prior-art sweep starts from real project structure instead of guesses.

## 1. Frame the search

**Action:** Identify the project scope, the target question, and whether the user wants one project or many.

**Instruction:** Treat each git repo or workspace as a separate project. Use the current working tree as the default project when no path is given. If `.lev` does not exist, do not fail; widen the crawl to the repo’s other docs and markdown surfaces.

**Validation:** You can name the project(s), the evidence question, and the output shape before searching.

**On failure:** Ask for the missing repo path or clarify whether this is a project-specific or global hunt.

## 2. Search `cass` first

**Action:** Search session history before the repo.

**Instruction:** Check `command -v cass`, then run `cass health --json`. Search in small bands instead of one broad query:

- exact phrases and known artifact names
- synonyms and nearby concepts
- orthogonal nouns, adjacent systems, and “same shape” ideas
- tags, dates, filenames, ticket ids, and other long-tail guesses

When a project root is known, search both scoped and global history:

```bash
cass search "<query>" --robot --workspace "<project-root>" --limit 5 --fields minimal
cass search "<query>" --robot --limit 5 --fields minimal
```

Expand only promising hits with `cass expand ... --json`.

**Validation:** At least three query bands were tried, and at least one promising hit was expanded or the search space was explicitly exhausted.

**On failure:** Broaden the query band, not the conclusion.

## 3. Sweep local truth

**Action:** Search the repo surfaces that usually hold durable evidence.

**Instruction:** Check these paths first when they exist:

- `docs/`
- `.lev/`
- `reports/`
- `prompt-exports/`
- `AGENTS.md`
- `README.md`
- `docs/_inbox/`
- `docs/specs/`
- `docs/design/`
- `docs/decisions/`
- `.lev/pm/`

Prefer the current Lev gather surface when available:

```bash
lev get "<query>" --json
lev gather "<query>" --research --json
```

If `lev get` / `lev gather` errors because the local package graph is incomplete, note that and fall back to `qmd` and `rg` without blocking. Use `qmd status` first if you need to discover available collections; do not assume a Lev-specific collection name exists. Use `lev find` only as a legacy fallback if the local install exposes it cleanly. For text search, use `qmd search` for phrase-heavy queries and `qmd query` for fuzzy reranked queries. Use `rg` when you need exact file hits or path-level exploration.

If `.lev` is missing, keep crawling the repo’s remaining markdown, docs, and exported reports instead of stopping.

**Validation:** You have either matched files, or you can say “no existing artifacts found” with confidence.

**On failure:** Search by file type, directory, tags, dates, and old project names before giving up.

## 4. Open relevant diagrams

**Action:** Inspect orphaned evidence in `~/.agents/diagrams`.

**Instruction:** Search filenames and contents separately, because the useful clue may be in the title, a caption, or a provenance footer:

```bash
rg --files /Users/jean-patricksmith/.agents/diagrams | rg -i "<query|tag|project|date>"
rg -n -i "<query|provenance|lineage|decision|report|handoff|breakthrough>" /Users/jean-patricksmith/.agents/diagrams
```

Open the most relevant HTML files and inspect their headings, source lists, and provenance notes. Use PNGs only when they are the only surviving evidence or the file name clearly points to the right artifact.

**Validation:** At least one relevant diagram file was inspected, or the diagram search is explicitly empty.

**On failure:** Search by alternate file names, adjacent project names, and date-stamped artifact names.

## 5. Synthesize the report

**Action:** Return the findings in the required shape.

**Instruction:** Use this response contract:

```markdown
## provenance report
- [Verified] ...
- [Stale] ...
- [Assumed] ...

**what it means**
- ...
- ...
- ...

**next steps**
- ...
- ...
- ...
```

For multi-project work, emit one project block per repo or workspace, then a final `Global` block that captures cross-project patterns. Keep the labels explicit:

- `Verified` = directly supported by a file, diagram, or expanded `cass` hit
- `Stale` = found but archived, superseded, or older than the current canon
- `Assumed` = inference from evidence, not a direct citation

Always include source paths or session references when possible. If no strong prior art is found, say so plainly and list the next searches you would run.

**Validation:** The output separates evidence from interpretation and includes a concrete next step list.

**On failure:** Remove unsupported claims before you answer.

## Guardrails

- Do not write markdown files unless the user explicitly asks you to.
- Do not replace `lev-research`; use this skill when the question is specifically about prior art, provenance, lineage, or decision history.
- Do not treat search hits as proof until you have read the underlying file, expanded the session hit, or inspected the diagram.
- Do not stop after one search angle. Rephrase the question, then search again.
- Do not assume `lev get` or `qmd` collections are healthy; they are accelerators, not a reason to stop.
