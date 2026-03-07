---
name: research
version: 1.0.1
aliases: [search, research, deep-research, sherlock, oracle, social-search]
triggers: [/research, /search, /sherlock, /oracle, /deep]
description: |
  [WHAT] Deep Research Intelligence System — Unified research orchestration with recursive confidence, multi-perspective synthesis, and session management.
  [HOW] Routes based on query complexity: QUICK (brave/firecrawl), STANDARD (multi-tool), DEEP (valyu+oracle)
  [WHEN] Any research, search, or information gathering task
  [WHY] Eliminates decision fatigue - one entry point routes to optimal backend(s)

  Keywords: search, research, deep, oracle, sherlock, social, investigate, analyze
skill_type: tool
category: process-research
primary_primitive: get

lifecycle_integration:
  stage: captured
  input_artifact: null
  output_artifact: synthesis.md
  xdg_data: ~/.config/LEV/research

backends:
  timetravel:
    library: plugins/timetravel
    strategies: [quick, full, deep, max, academic, social]
  quick:
    brave: backends/brave-web-quick/BACKEND.md
    firecrawl: backends/firecrawl-scrape-extract/BACKEND.md
    grok: backends/grok-web-twitter-realtime/BACKEND.md
    tavily: backends/tavily-ai-snippets/BACKEND.md
  specialized:
    exa: backends/exa-neural-linkedin-github/BACKEND.md
    last30days: backends/last30days-reddit-trends/BACKEND.md
  deep:
    valyu: backends/valyu-recursive-confidence/BACKEND.md
    multi_query: backends/deep-multi-query-synthesis/BACKEND.md
  synthesis:
    oracle: backends/oracle-ceo-gpt5pro/BACKEND.md

components:
  perspectives: perspectives/COMPONENT.md
  expansion: expansion/COMPONENT.md
  templates: templates/COMPONENT.md

routing:
  quick: timetravel quick (brave+tavily, first-success)
  full: timetravel full (brave+firecrawl+perplexity, parallel)
  deep: timetravel deep (valyu+perplexity+exa, parallel) -> oracle synthesis
  max: timetravel max (all 5, parallel) -> oracle synthesis
  social: timetravel social (grok+hackernews, parallel)
  academic: timetravel academic (arxiv+exa+perplexity, parallel)
  fallback_simple: brave -> firecrawl (fallback)

related_skills:
  - lev-find                         # `lev get` backend (legacy name)
  - lev-cdo                          # Use research for design/spec decisions
  - lev-orch-thinking-parliament     # Multi-model deliberation
  - notebooklm                       # Grounded cited synthesis into local markdown projections
  - workflow-cited-research          # Workflow-level cited research loop
  - bd                               # Create tasks from gaps

claude_code_shim:
  command: /search
  scope: claude-code-only
  source: ~/.claude/commands/search.md
---

# /research — Deep Research Intelligence System v1.0

**Sherlock Bytes: Where curiosity meets certainty.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔍 RESEARCH DASHBOARD                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  (q) Quick Search    — Fast web/news lookup (Brave, Firecrawl)              │
│  (d) Deep Research   — Recursive confidence loops (Valyu)                   │
│  (s) Synthesis       — Multi-source fusion (Oracle + perspectives)          │
│  (e) Extract         — Structured data extraction (Firecrawl)               │
│  (c) Crawl           — Full site analysis (Firecrawl)                       │
│  (t) Track           — Session management (list/resume/export)              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Session: {session_id} | Storage: ~/.config/LEV/research/{date}/{slug}/     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## /search Tag Routing

| Tag | Mode | Tools | Description |
|-----|------|-------|-------------|
| `quick` | ⚡ Fast | brave-search, firecrawl | Web lookup, default mode |
| `full` | 🔄 Standard | brave + firecrawl + valyu | Multi-source synthesis |
| `deep` | 🐢 Recursive | valyu research | Confidence loops until 85% |
| `max` | 🐢🐢 Team | spawn research team | Full team-based analysis |
| `sherlock` | 🔍 OSINT | Sherlock Bytes protocol | Investigation mode |
| `cdo` | 🧠 CDO | Multi-perspective overlay | MBTI + role personas |

**Usage:**
```bash
/search quick "query"     # Fast web search
/search deep "query"      # Recursive until confident
/search sherlock "query"  # OSINT investigation
/search cdo               # Multi-perspective on context
```

### Grounded Citation Route

When the user wants durable, cited research output instead of search results alone:

1. Use `/search` or `lev-research` to discover/curate sources.
2. Hand off to [`notebooklm`](/Users/jean-patricksmith/.agents/skills/notebooklm/SKILL.md) for multi-source grounded Q&A.
3. Prefer [`workflow-cited-research`](/Users/jean-patricksmith/.agents/skills/workflow-cited-research/SKILL.md) when the user wants the full repeatable loop, including local markdown/CMS projection.

---

## Timetravel Integration (v1.0)

The `timetravel` adapter library provides a unified programmatic layer for all research backends.
Individual CLI tools (brave-search, firecrawl, valyu, etc.) remain available for direct use.

### Strategy Mapping

| Skill Mode | Timetravel Strategy | Adapters | Orchestration |
|-----------|-------------------|----------|---------------|
| `quick` | `quick` | brave, tavily | first-success |
| `full` | `full` | brave, firecrawl, perplexity | parallel |
| `deep` | `deep` | valyu, perplexity, exa + oracle synthesis | parallel + synthesis |
| `max` | `max` | brave, firecrawl, perplexity, exa, valyu + oracle synthesis | parallel + synthesis |
| `social` | `social` | grok, hackernews | parallel |
| `sherlock` | `deep` + OSINT overlays | valyu, perplexity, exa + perspectives | parallel + synthesis |
| `cdo` | `max` + CDO overlays | all available + multi-perspective | parallel + synthesis |

### Programmatic Usage

```typescript
import { createDefaultRegistry, STRATEGIES, executeStrategy } from '@lev-os/timetravel';

const registry = createDefaultRegistry();
const result = await executeStrategy(STRATEGIES.deep, 'query', registry);
```

### CLI Usage

```bash
timetravel search "query" --strategy quick     # Fast web search
timetravel search "query" --strategy deep      # Recursive with synthesis
timetravel search "query" --strategy social    # Social/trending
timetravel search "query" --strategy academic  # Papers + neural
timetravel search "query" --strategy max       # All adapters + synthesis
timetravel search "query" --adapter brave      # Single adapter
timetravel status                               # Adapter availability dashboard
```

### Job System

```bash
timetravel job create -q "AI frameworks 2026" -s deep    # Create recurring job
timetravel job list                                       # List all jobs
timetravel job run <id>                                   # Execute a job
```

---

## CRITICAL: Read This Entire File First

**Before ANY research operation:**
1. This skill file MUST be fully loaded into context
2. Initialize session via `research init "<query>"` or auto-create
3. All outputs save to XDG-compliant `~/.config/LEV/research/` structure
4. Validate outputs before marking complete

## Invocation Contract (Mandatory)

This section is normative and overrides convenience behavior.

1. If user input contains `$research`, `/search`, or an explicit search tag request, route through the `/search` shim contract first.
2. `/search` is a Claude Code command shim only. It is defined in `~/.claude/commands/search.md`.
3. Non-Claude runtimes MUST still apply the same tag parsing semantics from the shim:
   - `quick|full|deep|max|sherlock|cdo`
   - no tag => `quick`
   - `$research` default => `deep` unless user overrides
4. Direct backend calls (`brave`, `firecrawl`, `valyu`, etc.) are allowed only:
   - as steps inside the selected mode flow, or
   - as explicit fallback when a routed step fails.
5. Before execution, print a single route line:
   - `research-route: <mode> | source: /search-shim | fallback: <none|reason>`
6. Never bypass the mode router by jumping straight to a single backend tool when `$research` or `/search` was requested.

---

## Operational Preflight (beads/dolt)

When `$research` work needs local persistence or issue handoff, run this preflight first:

1. Health check:
```bash
bd status --json
```

2. If you see `no beads database found` but `.beads/issues.jsonl` exists, bootstrap Dolt:
```bash
bd status --db .beads/beads.db
bd migrate --yes
```

3. If SQLite→Dolt migration is blocked by stale Dolt state:
```bash
# Keep artifact for audit/recovery, then retry migration
mkdir -p /tmp/beads-migration-backup
mv .beads/dolt /tmp/beads-migration-backup/dolt.$(date +%s)
bd migrate --to-dolt --yes
bd migrate --yes
```

4. Validate migration before proceeding:
```bash
bd migrate --inspect
# Expect: Schema Version matches current bd version
```

Use this flow before starting deep sessions to prevent store-state failures from interrupting routing/synthesis work.

---

## Tool Manifest by Category

### 🔍 SEARCH (Fast Lookup)

| Tool | CLI Command | Best For | Speed |
|------|-------------|----------|-------|
| Brave Web | `brave-search search "<query>" -n 10` | General web, news | ⚡ Fast |
| Brave News | `brave-search news "<query>"` | Breaking news | ⚡ Fast |
| Brave Video | `brave-search video "<query>"` | Video content | ⚡ Fast |
| Brave Image | `brave-search image "<query>"` | Visual research | ⚡ Fast |
| Firecrawl Search | `firecrawl search "<query>"` | Web + optional scraping | ⚡ Fast |
| Valyu Search | `valyu search "<query>"` | AI-optimized search | 🔄 Medium |
| Exa Neural | `bash exa/search.sh "<query>"` | Semantic/neural search | 🔄 Medium |

### 📄 CONTENT EXTRACTION

| Tool | CLI Command | Best For | Speed |
|------|-------------|----------|-------|
| Firecrawl Scrape | `firecrawl scrape <url>` | Single page content | ⚡ Fast |
| Firecrawl Batch | `firecrawl batch <urls...>` | Multiple pages | 🔄 Medium |
| Firecrawl Extract | `firecrawl extract <urls...> -p "<prompt>"` | Structured data | 🔄 Medium |
| Valyu Contents | `valyu contents <urls...>` | AI-enhanced extraction | 🔄 Medium |

### 🕷️ CRAWLING (Site-Wide)

| Tool | CLI Command | Best For | Speed |
|------|-------------|----------|-------|
| Firecrawl Crawl | `firecrawl crawl <url> -l 100` | Full site analysis | 🐢 Slow |
| Firecrawl Map | `firecrawl map <url>` | URL discovery | 🔄 Medium |

### 🧠 SYNTHESIS (AI-Powered)

| Tool | CLI Command | Best For | Speed |
|------|-------------|----------|-------|
| Valyu Answer | `valyu answer "<query>"` | Grounded AI response | 🔄 Medium |
| Valyu Research | `valyu research "<query>" -n 5 -t 0.85` | Recursive confidence | 🐢 Slow |
| Oracle GPT-5 | `oracle -p "<prompt>" -f <files>` | Complex synthesis | 🐢 Slow |

### 📊 SPECIALIZED

| Tool | CLI Command | Best For | Speed |
|------|-------------|----------|-------|
| Grok (X/Twitter) | `bash grok/research.sh "<query>"` | Real-time social | ⚡ Fast |
| Last30Days | `bash last30days/search.sh "<topic>"` | Trend analysis | 🔄 Medium |
| Tavily | `bash tavily/search.sh "<query>"` | AI snippets | 🔄 Medium |

---

## Session Management

### XDG-Compliant Storage Structure

```
~/.config/LEV/research/
├── sessions/
│   └── {YYYY-MM-DD}/
│       └── {session-id}_{semantic-slug}/
│           ├── session.json          # Metadata + state
│           ├── queries.jsonl         # All queries issued
│           ├── sources.jsonl         # All sources found
│           ├── artifacts/            # Raw outputs
│           │   ├── search_001.json
│           │   ├── crawl_002.json
│           │   └── synthesis_003.md
│           ├── synthesis.md          # Final synthesis
│           └── validation.json       # Output validation
├── templates/
│   ├── synthesis.md.tmpl
│   ├── report.md.tmpl
│   └── citations.md.tmpl
└── config.json                       # Global settings
```

### Session ID Format

```
{timestamp}_{slug}
Example: 20260203-2248_ai-agent-frameworks
```

### CLI Commands

```bash
# Initialize new research session
research init "What are the best AI agent frameworks in 2026?"

# Resume existing session
research resume 20260203-2248_ai-agent-frameworks

# List all sessions
research list [--status=open|completed|all]

# Export session to markdown
research export <session-id> --format=md|json|pdf

# Validate session outputs
research validate <session-id>

# Mark session complete
research complete <session-id>
```

---

## Complexity Assessment (Auto-Routing)

### QUICK (Direct execution)
**Triggers:** "search", "quick search", "lookup", "find"
**Route:** brave -> firecrawl (fallback)
**Example:** "search React hooks documentation"

### SOCIAL (Specialized path)
**Triggers:** "twitter", "reddit", "social", "trending", "sentiment"
**Route:** grok + last30days
**Example:** "what's trending about AI on Twitter"

### DEEP (Full orchestration)
**Triggers:** "research", "deep", "comprehensive", "analyze", "compare", "investigate", "sherlock"
**Route:** valyu research -> oracle (synthesis)
**Example:** "research the state of AI safety in 2026"

---

## Workflow Patterns

### Pattern 1: Quick Search (1-2 min)
```bash
# User: "What is X?"
brave search "X" -n 5
# → Return top results with snippets
```

### Pattern 2: Standard Research (5-10 min)
```bash
# User: "Research X thoroughly"
research init "X"
brave search "X"                    # Get overview
firecrawl scrape <top-3-urls>       # Deep content
valyu answer "X"                    # Synthesize
research complete
```

### Pattern 3: Deep Research (15-30 min)
```bash
# User: "Deep dive into X"
research init "X" --depth=deep
valyu research "X" -n 5 -t 0.85     # Recursive until confident

# Multi-perspective overlay:
valyu answer "X from engineering perspective"
valyu answer "X market analysis"
valyu answer "X user experience implications"

oracle -p "Synthesize all findings" -f artifacts/*.json
research validate && research complete
```

### Pattern 4: Comprehensive (30-60 min, spawn team)
```bash
# User: "Complete analysis of X"
# Spawn research team:
#   • Lead Researcher (coordinator)
#   • Domain Expert (valyu recursive)
#   • Source Validator (firecrawl extraction)
#   • Synthesizer (oracle GPT-5)
# Parallel workstreams with validation gates
# Consolidated final report
```

---

## Multi-Perspective Overlays

### MBTI-Inspired Personas

| Persona | Lens | Query Modification |
|---------|------|-------------------|
| Architect (INTJ) | Systems/Strategy | "architectural implications of X" |
| Analyst (INTP) | Logic/Theory | "theoretical foundations of X" |
| Commander (ENTJ) | Execution/ROI | "business case for X" |
| Visionary (ENTP) | Innovation | "disruptive potential of X" |
| Mediator (INFP) | Values/Ethics | "ethical considerations of X" |
| Advocate (INFJ) | Long-term Impact | "societal implications of X" |

### Role-Based Perspectives

| Role | Focus | Example Query |
|------|-------|---------------|
| UX Designer | User needs | "user pain points with X" |
| Security Engineer | Vulnerabilities | "security risks of X" |
| Product Manager | Market fit | "competitive landscape for X" |
| DevOps | Operations | "operational complexity of X" |
| Legal | Compliance | "regulatory requirements for X" |

### CDO (Cognitive Diversity Overlay)

Run these in parallel for comprehensive coverage:
1. **Breadth First**: Wide exploration, many sources
2. **Depth First**: Deep dive into top 3 sources
3. **Contrarian**: "arguments against X"
4. **Historical**: "evolution of X over time"
5. **Future**: "X predictions 2027-2030"

---

## Output Templates

### Synthesis Template

```markdown
# Research Synthesis: {query}

**Session**: {session_id}
**Date**: {date}
**Confidence**: {confidence}%

## Executive Summary
{2-3 sentence overview}

## Key Findings
1. {finding with source citation}
2. {finding with source citation}
3. {finding with source citation}

## Evidence
| Claim | Source | Confidence |
|-------|--------|------------|
| {claim} | [{source}]({url}) | {high/medium/low} |

## Perspectives Analyzed
- **{perspective_1}**: {summary}
- **{perspective_2}**: {summary}

## Open Questions
- {question requiring further research}

## Sources
{numbered list with URLs}

---
*Generated by Sherlock Bytes v1.0 | Validated: {validation_status}*
```

---

## Validation Rules

Before marking any research session complete, validate:

### Structure Validation
- [ ] `session.json` exists and has valid schema
- [ ] At least 3 unique sources in `sources.jsonl`
- [ ] `synthesis.md` follows template structure
- [ ] All URLs are reachable (sample check)

### Content Validation
- [ ] Executive summary ≤ 100 words
- [ ] Each claim has source citation
- [ ] Confidence levels justified
- [ ] No hallucinated sources (cross-check)

### Quality Validation
- [ ] Addresses original query directly
- [ ] Multiple perspectives represented
- [ ] Contrarian view included if controversial
- [ ] Open questions identified

### Validation Output

```json
{
  "session_id": "...",
  "validated_at": "ISO8601",
  "structure": {"passed": true, "checks": 4},
  "content": {"passed": true, "checks": 4},
  "quality": {"passed": true, "checks": 4},
  "overall": "PASS",
  "warnings": [],
  "errors": []
}
```

---

## Team Configuration (Complex Requests)

For requests requiring >30 min or multi-domain expertise:

```yaml
# Team spawned via Task tool
name: Deep Research Team
roles:
  - Lead Researcher (coordinator): valyu, brave, research-cli
  - Source Hunter (worker): firecrawl, brave
  - Domain Expert (worker): valyu, oracle
  - Validator (qa): research-cli validation
```

---

## Environment Variables

```bash
# Required (in ~/.env.local)
BRAVE_API_KEY=...        # Brave Search API
FIRECRAWL_API_KEY=...    # Firecrawl API
VALYU_API_KEY=...        # Valyu API
OPENAI_API_KEY=...       # Oracle (GPT-5)

# Optional
EXA_API_KEY=...          # Exa neural search
XAI_API_KEY=...          # Grok/X search
TAVILY_API_KEY=...       # Tavily AI search
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `brave-search search "<query>"` | Fast web search |
| `brave-search news "<query>"` | News search |
| `firecrawl scrape <url>` | Extract page content |
| `firecrawl crawl <url>` | Crawl entire site |
| `firecrawl search "<query>"` | Search + scrape |
| `valyu search "<query>"` | AI-optimized search |
| `valyu answer "<query>"` | Grounded AI answer |
| `valyu research "<query>"` | Recursive confidence |
| `oracle -p "<prompt>" -f ...` | GPT-5.2 Pro synthesis |

---

## Backend Reference

| Backend | CLI | Tools |
|---------|-----|-------|
| **brave** | `brave-search` | search, news, video, image, local, status |
| **firecrawl** | `firecrawl` | scrape, crawl, map, extract, batch, search, status |
| **valyu** | `valyu` | search, answer, contents, research |
| **oracle** | `oracle` | prompt + file synthesis |
| **exa** | scripts | search, content |
| **grok** | scripts | research |
| **tavily** | scripts | search, extract |
| **last30days** | scripts | search, trends |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.1 | 2026-02-19 | Added beads/dolt operational preflight + recovery flow for migration edge cases |
| 1.0.0 | 2026-02-09 | Timetravel adapter library integration, 10 adapters, 6 strategies, job system |
| 0.9.0 | 2026-02-03 | Unified skill, XDG storage, validation, CLI tools |
| 0.8.x | 2026-01 | Individual backend skills |

---

*🔍 Sherlock Bytes — "When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-research, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
