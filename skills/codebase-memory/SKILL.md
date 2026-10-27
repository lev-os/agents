---
name: codebase-memory
description: "Use the codebase knowledge graph for structural code queries. Triggers on: explore the codebase, understand the architecture, what functions exist, show me the structure, find code from plain words, search by meaning, who calls this function, what does X call, trace the call chain, find callers of, show dependencies, impact analysis, refactor safety, what a diff touches, dead code, unused functions, near-duplicate code, high fan-out, refactor candidates, code quality audit, index coverage, graph query syntax, Cypher query examples, edge types, how to use search_graph."
---

# Codebase Memory — Knowledge Graph Tools

Graph tools return precise structural results in ~500 tokens vs ~80K for grep.

## Quick Decision Matrix

| Question | Tool call |
|----------|----------|
| Find code when you know the name | `search_graph(query="addItemToBag")` or `search_graph(name_pattern=".*AddToBag.*")` |
| Find code from plain words | `search_graph(semantic_query=["bag","checkout","action"])` |
| Who calls X? | `trace_path(direction="inbound")` |
| What does X call? | `trace_path(direction="outbound")` |
| Full call context | `trace_path(direction="both")` |
| Read the real source | `get_code_snippet(qualified_name="...")` |
| What a file defines | `get_file_outline` |
| Project overview | `get_architecture(aspects=[...])` |
| Impact of local changes | `detect_changes()`; `scope="tests"` adds test impact |
| Risk-classified trace | `trace_path(risk_labels=true)` |
| Diff two index snapshots | `compare_graphs` |
| Dead code | `search_graph(max_degree=0, exclude_entry_points=true)` |
| Near-duplicate code | `query_graph` over `SIMILAR_TO` edges |
| Cross-service edges | `query_graph` with Cypher |
| Is a path indexed | `check_index_coverage` |
| Text search (literals, config, errors) | `search_code` or Grep |

## Finding code you cannot name

`search_graph` ranks in one mode per call; run both when the user's words are not code names:

- `query: "add to bag"` — BM25 over symbol names, file paths and markdown headings (`Section` nodes).
- `semantic_query: ["bag", "checkout", "action"]` — vector ranking, built into the index. It must be a list of keywords, not a sentence; each keyword is scored on its own.

`query` and `semantic_query` cannot share a call. Confirm every candidate with `get_code_snippet`.

## Evidence tiers

Pick one before querying and say which one you used.

- **Scout:** 3-4 narrow calls; positive findings only, marked provisional. No absence, exhaustive-impact or dead-code claims.
- **Verify (default):** task-directed graph evidence, both trace directions where relevant, `get_code_snippet` for every material claim, full pagination of relevant results.
- **Auditor:** bounded scope, current index, complete pagination, both call directions and broader relationships; state every limitation.

Once the evidence paths are known, call `check_index_coverage` once with all of them. A claim that something is absent or complete also needs the relevant scopes checked. A clean result means "no recorded gap", not proof.

## Exploration Workflow
1. `list_projects` — pick the entry whose `root_path` contains your working directory; pass its `name` (or the absolute directory) as `project`, never a repo or folder name
2. `get_graph_schema` — understand node/edge types
3. `search_graph` (`query`, `semantic_query` or `name_pattern`) — find code
4. `get_code_snippet(qualified_name="project.path.FuncName")` — read source

## Tracing Workflow
1. `search_graph(name_pattern=".*FuncName.*")` — discover exact name
2. `trace_path(function_name="FuncName", direction="both", depth=3)` — trace
3. `detect_changes()` — map git diff to affected symbols

## Refactor Workflow
1. `trace_path(direction="inbound")` on each symbol you will change — every caller
2. `detect_changes(scope="tests")` after the edit — affected symbols and tests
3. `check_index_coverage` on the touched paths before saying nothing else breaks

## Quality Analysis
- Dead code: `search_graph(max_degree=0, exclude_entry_points=true)` — check dynamic dispatch, framework conventions and coverage gaps before deleting
- High fan-out: `search_graph(min_degree=10, relationship="CALLS", direction="outbound")`
- High fan-in: `search_graph(min_degree=10, relationship="CALLS", direction="inbound")`

## 17 MCP Tools
`index_repository`, `index_status`, `list_projects`, `delete_project`,
`search_graph`, `search_code`, `trace_path`, `detect_changes`,
`query_graph`, `get_graph_schema`, `get_code_snippet`, `get_file_outline`,
`get_architecture`, `check_index_coverage`, `compare_graphs`,
`manage_adr`, `ingest_traces`

## Edge Types
CALLS, HTTP_CALLS, GRAPHQL_CALLS, ASYNC_CALLS, IMPORTS, DEFINES, DEFINES_METHOD,
HANDLES, IMPLEMENTS, OVERRIDE, USAGE, WRITES, CONFIGURES, TESTS_FILE,
FILE_CHANGES_WITH, SIMILAR_TO, SEMANTICALLY_RELATED, MENTIONS,
CONTAINS_FILE, CONTAINS_FOLDER, CONTAINS_PACKAGE

Run `get_graph_schema` for the exact set in a given project.

## Cypher Examples (for query_graph)
```
MATCH (a)-[r:HTTP_CALLS]->(b) RETURN a.name, b.name, r.url_path, r.confidence LIMIT 20
MATCH (f:Function) WHERE f.name =~ '.*Handler.*' RETURN f.name, f.file_path
MATCH (a)-[r:CALLS]->(b) WHERE a.name = 'main' RETURN b.name
MATCH (a)-[:SIMILAR_TO]->(b) RETURN a.name, a.file_path, b.name, b.file_path LIMIT 20
```

## Gotchas
1. `search_graph(relationship="HTTP_CALLS")` filters nodes by degree — use `query_graph` with Cypher to see actual edges.
2. `query_graph` has a 200-row cap — use `search_graph` with degree filters for counting.
3. `trace_path` needs exact names — use `search_graph` first.
4. `direction="outbound"` misses cross-service callers — use `direction="both"`.
5. Results default to 10 per page — check `has_more` and use `offset`.
6. Markdown headings are indexed as `Section` nodes; the text under a heading is not ranked.
7. A subagent does not inherit MCP tools or the conversation. Query in the parent and pass the tier, project, paths and symbols.
