---
name: prior-art
description: Use when you need an evidence-first provenance report from `cass`, repo docs, `.lev`, `~/.agents/diagrams`, `qmd`, or Grep/Glob tools.
---

# Prior Art

Find the existing evidence first, then summarize what it means. This skill is narrower than `lev-research`: it is for provenance, lineage, decision history, and "what already exists?" questions.

If the repo itself is unfamiliar, orient graph-first (tool 2 below) so the prior-art sweep starts from real project structure instead of guesses.

## 1. Frame the search

**Action:** Identify the project scope, the target question, and whether the user wants one project or many.

**Instruction:** Treat each git repo or workspace as a separate project. Use the current working tree as the default project when no path is given. If `.lev` does not exist, do not fail; widen the crawl to the repo's other docs and markdown surfaces.

**Validation:** You can name the project(s), the evidence question, and the output shape before searching.

**On failure:** Ask for the missing repo path or clarify whether this is a project-specific or global hunt.

## 2. `lev find` first for records, agent tools for code, `cass` for sessions

**Principle:** `lev find` searches the project's records under `.lev/` (decisions, captures, workstreams, ideas, tasks, plans, designs, reports, handoffs) and the Lev IR under `dna/`. A cold call takes about half a second, so run it first. It does not search source code or chat history.

**Tool priority order:**
1. **`lev find`** — records and Lev IR. Query with 3 to 6 topic words; `a|b` means either; an id such as `M340` matches only itself. Always pass `--json`.
2. **codebase-memory MCP** (if available) — for CODE prior art, use
   `search_graph`/`search_code`/`trace_path`/`get_architecture`; the
   graph knows symbols, callers, and structure Grep can't rank. If the MCP
   server is not connected this session, note that gap and continue with Grep.
3. **Grep / Glob / SemanticSearch / Read** — exact patterns, file names, meaning-based search, and files whose path you know (instant)
4. **cass** — session history (5-10s)

Count a tool or MCP server as available only after it answers in this session. A missing tool or failed backend is a recorded search
gap, not evidence that no prior art exists.

**Gitignored intake caveat:** Grep/rg respect `.gitignore`, so
`workshop/intake/` and other intake sandboxes are silently skipped. When the
hunt should cover intake clones, pass explicit paths (e.g.
`rg <q> workshop/intake/<repo>`) or `--no-ignore` — do not conclude "no prior
art" from a default sweep alone.

`lev get` and `lev gather` are removed. `lev find` is the local record search.

**Session cache (in-process):** Before running a tool again, check whether this session already ran the **same** query + scope. Reuse prior results instead of re-fetching.

**`lev find` filters** (run from the project root; each card in `result.data.results` has `id`, `type`, `title`, `status`, `snippet`, `path`, `line`):
- `--type decision` (repeatable) and `--exclude-type capture` narrow by record type. Today `decision`, `workstream`, `idea`, `task` and `lev_ir` return cards; `plan`, `design`, `capture`, `handoff` and `report` return none until indexed, so `rg` `.lev/pm` for those.
- `--status active` filters the record's own status (not a health check). A card with status `superseded` is history: open the record that superseded it.
- `--workstream <id>` keeps one workstream's records; `--limit <n>` caps the cards.
- Read the file at each card's `path` before you cite it.

**Burst budget (defaults):**
- `lev find`, Grep/Glob/SemanticSearch: run as often as the question needs; vary the topic words and the `--type` filter instead of repeating one query
- `cass`: at least **three** distinct query bands total across the task, but **no duplicate** band in the same session
- Diagrams (`~/.agents/diagrams`): at most **one** filename sweep + **one** content sweep per user question

**On failure:** If `lev` is not installed or the call fails, say so in one line and `rg` over `.lev` and `dna`. If every tool finds nothing, note it and synthesize from what you have.

## 3. Search `cass` for session history

**Action:** Search session history before the repo.

**Instruction:** Check `command -v cass`, then run `cass health --json`. Search in small bands instead of one broad query:

- exact phrases and known artifact names
- synonyms and nearby concepts
- orthogonal nouns, adjacent systems, and "same shape" ideas
- tags, dates, filenames, ticket ids, and other long-tail guesses

When a project root is known, search both scoped and global history:

```bash
cass search "<query>" --robot --workspace "<project-root>" --limit 5 --fields minimal
cass search "<query>" --robot --limit 5 --fields minimal
```

Expand only promising hits with `cass expand ... --json`.

**Validation:** At least three **distinct** query bands were tried (or `cass` unavailable—state that explicitly), and at least one promising hit was expanded or the search space was explicitly exhausted. Do not re-run the same band twice in one session.

**On failure:** Broaden the query band, not the conclusion.

## 4. Sweep local truth with agent tools

**Action:** Search the repo surfaces that usually hold durable evidence.

**Instruction:** Use **Grep** and **Glob** for files that `lev find` does not index. These are instant and don't spawn processes.

**Step 1 — File discovery (Glob):**
```
Glob: .lev/pm/**/*.md
Glob: docs/**/*.md
Glob: .lev/pm/specs/*.md
Glob: .lev/pm/proposals/*.md
Glob: .lev/pm/handoffs/*.md
```

**Step 2 — Content search (Grep):**
```
Grep: pattern="<query terms>" path=".lev/pm/"
Grep: pattern="<query terms>" path="docs/"
Grep: pattern="<query terms>" glob="*.md"
```

**Step 3 — Read matching files** directly with the Read tool.

**Step 4 — SemanticSearch** if keyword search missed conceptual matches:
```
SemanticSearch: query="<full question>" target_directories=[".lev/pm/"]
SemanticSearch: query="<full question>" target_directories=["docs/"]
```

**Deliberate file paths to check** (open files; do not blanket-search the repo):

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

**Records first:**

```bash
lev find "<3-6 topic words>" --json
lev find "<3-6 topic words>" --type decision --type design --json
```

If the project call is thin and the question truly needs outside-world/current information, switch to `lev-research` / `lev timetravel` instead of inventing more local search bursts.

If `.lev` is missing, keep crawling the repo's remaining markdown, docs, and exported reports instead of stopping.

**Validation:** You have either matched files, or you can say "no existing artifacts found" with confidence.

**On failure:** Search by file type, directory, tags, dates, and old project names before giving up.

## 5. Open relevant diagrams

**Action:** Inspect orphaned evidence in `~/.agents/diagrams`.

**Instruction:** Use Glob and Grep (agent tools, not CLI):

```
Glob: ~/.agents/diagrams/*<query>*
Grep: pattern="<query>" path="~/.agents/diagrams"
```

Open the most relevant HTML files and inspect their headings, source lists, and provenance notes. Use PNGs only when they are the only surviving evidence or the file name clearly points to the right artifact.

**Validation:** At least one relevant diagram file was inspected, or the diagram search is explicitly empty.

**On failure:** Search by alternate file names, adjacent project names, and date-stamped artifact names.

## 6. Synthesize the report

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

Trace each claim to its original source, not to a later summary, handoff, or report that cites it. When they disagree, cite the original with its revision or date and label the later copy `Stale` with the discrepancy. Copy paths, URLs, session IDs, line ranges, and revisions verbatim. Before calling a value absent or a claim unsupported, inspect the provided or referenced original rows within the claimed search scope; absence from a bounded summary or projection is not absence from the original. Report scope you did not search as unknown, not as unsupported.

**Validation:** The output separates evidence from interpretation and includes a concrete next step list.

**On failure:** Quarantine claims the inspected originals do not support: name each as unsupported with the scope searched, keep it out of `Verified`, and withdraw every conclusion or next step that depended on it.

## Guardrails

- Return the report inline. Save a file only when the user or the invoked workflow authorizes saving; then human-facing prose goes in Markdown, configuration and machine declarations in YAML, and runtime state in JSON.
- Do not replace `lev-research`; use this skill when the question is specifically about prior art, provenance, lineage, or decision history.
- Do not treat search hits as proof until you have read the underlying file, expanded the session hit, or inspected the diagram.
- Do not stop after one search angle. Rephrase the question, then search again.
- Do not assume `qmd` collections are healthy; they are accelerators, not a reason to stop.

### Search Exclusions (avoid getting lost in the woods)

When using Grep, exclude noise directories via the `glob` parameter. Common patterns to avoid:

- `node_modules/` — vendored JS ecosystem
- `.venv/`, `venv/` — vendored Python ecosystem
- `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `Cargo.lock` — lockfiles
- `*.min.js`, `*.min.css` — minified bundles
- `workshop/intake/*/` — may contain full cloned repos
- `__pycache__/`, `site-packages/` — compiled Python

When a broad search returns >50 hits dominated by one of these directories, narrow the scope rather than trying to filter mentally.

## Source-derived reports
For a requested codebase report, ground conclusions in source citations, separate direct evidence from inference and gaps, and match depth to the question. Finish with one next check or action a reader can verify.
