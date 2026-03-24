---
name: research
version: 1.0.3
aliases: [search, research, deep-research, sherlock, oracle, social-search]
triggers: [/research, /search, /sherlock, /oracle, /deep]
description: |
  Canonical research router for web, docs, current events, product comparisons, and multi-source synthesis. Use when the user asks to search, research, investigate, analyze, fact-check, compare sources, or gather current information. Route all tagged requests through the declared mode (`quick|full|deep|max|social|academic|sherlock|cdo`) and fail fast if the routed runtime or backend command is unavailable. Prefer the canonical Timetravel runtime at `~/lev/plugins/core-timetravel` for orchestrated search; use direct backend commands only when explicitly requested or when the route says so.

  Keywords: search, research, deep, oracle, sherlock, social, investigate, analyze
skill_type: tool
category: process-research
primary_primitive: get
claude_code_shim:
  command: /search
  scope: claude-code-only
  source: ~/.claude/commands/search.md
---

# Research

Treat this skill as a strict router, not a bag of optional tools.

## Mandatory Contract

1. If the user asks for `$research`, `/search`, or a tagged research mode, emit:
   - `research-route: <mode> | source: /search-shim | fallback: <none|reason>`
2. Run the canonical route first.
3. After every backend attempt, emit:
   - `research-attempts: <backend> | status: <ok|failed|skipped> | reason: <short reason>`
4. If the routed command fails, stop immediately unless the selected route explicitly declares a fallback.
5. Never replace a failed deep route with ad hoc manual browsing.
6. Direct backend commands are allowed only when:
   - the user explicitly asks for that backend, or
   - the route declares that backend as a fallback.

## Canonical Runtime

- Canonical orchestrator: [core-timetravel](/Users/jean-patricksmith/lev/plugins/core-timetravel)
- Canonical command: `timetravel`
- Canonical deep route:
  ```bash
  timetravel search "<query>" --strategy deep
  ```
- Session helper:
  ```bash
  research init "<query>"
  research list
  research validate <session-id>
  ```

## Backend Reality Map

| Command | Runtime | Location | Use |
|---|---|---|---|
| `timetravel` | Canonical orchestrator | `~/lev/plugins/core-timetravel/dist/cli.js` via `~/.local/bin/timetravel` | `quick/full/deep/max/social/academic` |
| `brave-search` | Dependency-free wrapper | `~/.local/bin/brave-search` -> `scripts/runtime/brave-search.sh` | Direct Brave search |
| `firecrawl` | Dependency-free wrapper | `~/.local/bin/firecrawl` -> `scripts/runtime/firecrawl.sh` | Direct Firecrawl search/scrape/map/crawl/extract/batch |
| `valyu` | Dependency-free wrapper | `~/.local/bin/valyu` -> `scripts/runtime/valyu.sh` | Direct Valyu search/answer/contents/research |
| `oracle` | Existing installed CLI | system PATH | Synthesis / second opinion |
| `exa` | Dependency-free wrapper | `~/.local/bin/exa` -> `scripts/runtime/exa.sh` | Direct Exa search, contents, answer |
| Grok | Shell script | `backends/grok-web-twitter-realtime/scripts/grok-search.sh` | Direct X/current events |
| Tavily | Node script, no deps | `backends/tavily-ai-snippets/scripts/search.mjs` | Direct snippet search |
| Last30Days | Python script | `backends/last30days-reddit-trends/scripts/last30days.py` | Social trend analysis |

## Routing

| Mode | First Command | Notes |
|---|---|---|
| `quick` | `timetravel search "<query>" --strategy quick` | Use direct backend only if explicitly requested |
| `full` | `timetravel search "<query>" --strategy full` | Parallel multi-source |
| `deep` | `timetravel search "<query>" --strategy deep` | Canonical deep route |
| `max` | `timetravel search "<query>" --strategy max` | Maximum coverage |
| `social` | `timetravel search "<query>" --strategy social` | Social + trend sources |
| `academic` | `timetravel search "<query>" --strategy academic` | Papers + academic sources |
| `sherlock` | `timetravel search "<query>" --strategy deep` | Add adversarial and OSINT framing in the prompt |
| `cdo` | `timetravel search "<query>" --strategy max` | Add multi-perspective overlays in synthesis |

### Fallback Rules

- `quick`: if `timetravel` is unavailable, fallback is `brave-search search`.
- All other routes: no implicit fallback. Fail fast and report the failing command.

## Direct Backend Commands

Use these only when the user explicitly requests the backend or when the route allows it.

```bash
brave-search search "<query>" -n 10
brave-search news "<query>"
firecrawl search "<query>" --json
firecrawl scrape <url> -o out.md
firecrawl map <url> --json
firecrawl crawl <url>
firecrawl extract <urls...> -p "<prompt>"
firecrawl batch <urls...>
valyu search "<query>"
valyu answer "<query>"
valyu contents <urls...>
valyu research "<query>"
oracle -p "<prompt>" -f <files>
bash backends/exa-neural-linkedin-github/scripts/search.sh "<query>"
bash backends/exa-neural-linkedin-github/scripts/content.sh "<url>"
exa search "<query>"
exa contents <urls...>
exa answer "<query>"
bash backends/grok-web-twitter-realtime/scripts/grok-search.sh "<query>"
node backends/tavily-ai-snippets/scripts/search.mjs "<query>"
python3 backends/last30days-reddit-trends/scripts/last30days.py "<topic>" --emit=compact
```

## Fail-Fast Rules

- Missing command: stop immediately.
- Missing API key for selected command: stop immediately.
- Non-zero exit from the routed command: stop immediately.
- Empty result from the routed command:
  - `quick` may fallback to `brave-search search`
  - all other modes stop and report failure
- Never silently replace a failed routed command with manual web browsing.

## References

- Exa backend: [BACKEND.md](backends/exa-neural-linkedin-github/BACKEND.md)
- Firecrawl backend: [BACKEND.md](backends/firecrawl-scrape-extract/BACKEND.md)
- Valyu backend: [BACKEND.md](backends/valyu-recursive-confidence/BACKEND.md)
- Timetravel plugin tests live in:
  - [cli.e2e.test.ts](/Users/jean-patricksmith/lev/plugins/core-timetravel/tests/integration/cli.e2e.test.ts)
  - [strategy.e2e.test.ts](/Users/jean-patricksmith/lev/plugins/core-timetravel/tests/integration/strategy.e2e.test.ts)
