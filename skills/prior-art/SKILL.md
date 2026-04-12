---
name: prior-art
description: Use when you need an evidence-first provenance report from `cass`, repo docs, `.lev`, `~/.agents/diagrams`, `qmd`, or Grep/Glob tools.
---

# Prior Art

Find the existing evidence first, then summarize what it means. This skill is narrower than `lev-research`: it is for provenance, lineage, decision history, and "what already exists?" questions.

If the repo itself is unfamiliar, pair this with `codebase-archaeology` first so the prior-art sweep starts from real project structure instead of guesses.

## 1. Frame the search

**Action:** Identify the project scope, the target question, and whether the user wants one project or many.

**Instruction:** Treat each git repo or workspace as a separate project. Use the current working tree as the default project when no path is given. If `.lev` does not exist, do not fail; widen the crawl to the repo's other docs and markdown surfaces.

**Validation:** You can name the project(s), the evidence question, and the output shape before searching.

**On failure:** Ask for the missing repo path or clarify whether this is a project-specific or global hunt.

## 2. Use agent tools first, CLI second

**Principle:** Agent-native tools (Grep, Glob, Read, SemanticSearch) are instant. CLI tools (`lev get`, `lev find`, `cass`) have cold-start overhead (tsx compilation, FlowMind boot) and can take 30-60 seconds per invocation. **Always prefer agent tools over CLI for prior-art searches.**

**Tool priority order:**
1. **Grep** — exact keyword/pattern search across the repo (instant)
2. **Glob** — find files by name pattern (instant)
3. **SemanticSearch** — meaning-based code/doc search (fast)
4. **Read** — open files directly when you know the path (instant)
5. **cass** — session history search (5-10s, reasonable)
6. **`lev find`** — multi-backend fusion search (bd + qmd + ck; ~20s including cold start — **use only if agent tools found nothing**)

**NEVER use `lev get` or `lev gather` for prior-art.** These commands have the same cold start as `lev find` plus additional overhead (research backends, artifact writes). They are composition commands, not search primitives.

**Session cache (in-process):** Before running a tool again, check whether this session already ran the **same** query + scope. Reuse prior results instead of re-fetching.

**Burst budget (defaults):**
- Grep/Glob/SemanticSearch: unlimited — these are instant
- `cass`: at least **three** distinct query bands total across the task, but **no duplicate** band in the same session
- `lev find`: at most **one** call, only if agent tools returned nothing useful. Use `--json` flag. Default engine timeout is 20s.
- Diagrams (`~/.agents/diagrams`): at most **one** filename sweep + **one** content sweep per user question

**On failure:** If agent tools find nothing, note it and synthesize from what you have. Do not spawn CLI processes hoping for better results.

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

**Instruction:** Use **Grep** and **Glob** as primary search tools. These are instant and don't spawn processes.

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

**CLI fallback (last resort only):**

If agent tools found nothing and you believe `lev find`'s multi-backend fusion would add value, run it with a timeout:

```bash
timeout 15 lev find "<query>" --json 2>/dev/null || echo '{"timeout": true}'
```

Do NOT use `lev get` or `lev gather` — they alias to `gather` which spawns additional sub-processes (research backends, artifact writes) and doubles the cold-start cost.

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

**Validation:** The output separates evidence from interpretation and includes a concrete next step list.

**On failure:** Remove unsupported claims before you answer.

## Guardrails

- Do not write markdown files unless the user explicitly asks you to.
- Do not replace `lev-research`; use this skill when the question is specifically about prior art, provenance, lineage, or decision history.
- Do not treat search hits as proof until you have read the underlying file, expanded the session hit, or inspected the diagram.
- Do not stop after one search angle. Rephrase the question, then search again.
- **NEVER spawn `lev get`, `lev gather`, or unbounded `lev find` calls.** These are 30-60s cold-start processes that create zombie monsters when called repeatedly. Use agent-native tools (Grep, Glob, SemanticSearch, Read) as primary.
- If you must use `lev find`, wrap it with `timeout 15` and limit to one call per session.
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
