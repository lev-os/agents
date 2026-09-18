---
name: social-signal-extractor
description: >-
  Browser-only social signal extraction worker for the Lev graph. Extracts themes, hooks,
  and positioning signals from LinkedIn, X, and Substack. Produces strict JSON output conforming
  to SocialSignalExtractionSchema. All outputs must be funneled back through the Lev Graph Operator
  (Notion CMS write + Event Log emission). Never writes to Notion directly — returns JSON for
  the parent skill to persist. Use when scanning social channels for content signals, monitoring
  target creators, researching competitor positioning, or gathering data for WeeklySignalBrief.
  Triggers on: social signal, extract signals, linkedin scan, x scan, substack scan, creator
  monitoring, content signals, social extraction, signal scan.
metadata:
  author: jp-kingly
  version: '1.0'
---

# Social Signal Extractor

> Browser-only worker skill. Produces strict JSON. Never writes to Notion directly.
> All outputs re-enter the Lev graph through lev-graph-operator → write_artifact_to_notion.

---

## Hard Rules

1. **Strict JSON output only** — no prose in structured fields
2. **Never write to Notion** — return JSON to the calling skill
3. **Output must conform to SocialSignalExtractionSchema** — schema violation = failure
4. **Confidence score is mandatory** — 0.0 (no data) to 1.0 (rich, diverse sources)
5. **Respect rate limits** — max 5 LinkedIn profiles, max 3 Substacks per run
6. **No private/DM content extraction** — public posts only

---

## Output Schema: SocialSignalExtractionSchema

```json
{
  "type": "object",
  "required": ["extraction_date", "time_window", "sources_scanned", "themes", "hooks", "positioning", "audience_profile", "confidence"],
  "properties": {
    "extraction_date": { "type": "string", "format": "date" },
    "time_window": { "type": "string" },
    "sources_scanned": {
      "type": "object",
      "properties": {
        "linkedin_creators": { "type": "array", "items": { "type": "string" } },
        "substacks": { "type": "array", "items": { "type": "string" } },
        "x_queries": { "type": "array", "items": { "type": "string" } }
      }
    },
    "themes": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "hooks": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "positioning": {
      "type": "array",
      "items": { "type": "string" }
    },
    "audience_profile": {
      "type": "object",
      "required": ["primary_icp", "pain_points", "aspirations"],
      "properties": {
        "primary_icp": { "type": "string" },
        "pain_points": { "type": "array", "items": { "type": "string" } },
        "aspirations": { "type": "array", "items": { "type": "string" } }
      }
    },
    "raw_posts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "platform": { "enum": ["linkedin", "x", "substack"] },
          "author": { "type": "string" },
          "hook": { "type": "string" },
          "topic": { "type": "string" },
          "engagement": { "type": "integer" },
          "url": { "type": "string" },
          "date": { "type": "string", "format": "date" }
        }
      }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
```

---

## JP's Strategic Niche

All signal extraction is filtered through these themes:

| Theme | Keywords |
|-------|----------|
| Fail-Closed AI | fail safe, fail closed, agent safety, guardrails |
| Leases > Perms | time-bounded trust, agent permissions, lease, scope |
| Agentic UX | beyond chat, agent interfaces, agent UX, multi-modal |
| Event-Sourced Agents | event sourcing, replay, audit trail, deterministic |
| Vibe Code Critique | vibe coding, demo magic, production reality, code quality |
| Agent Runtime | orchestration, runtime, framework, agent architecture |
| Trust Infrastructure | enterprise trust, compliance, AI governance |

### Target ICP

- CTOs and VP Engineering at Series A-C startups
- AI Engineers building production agent systems
- Founders shipping AI-powered products
- Indie hackers building with AI frameworks

---

## Extraction Procedures

### 1. LinkedIn Extraction

```yaml
procedure: extract_linkedin
input:
  creators: array of LinkedIn profile URLs or names (max 5)
  time_window: string (default "7 days")
tool: browser_task
steps:
  - for each creator:
      navigate to profile activity/posts
      extract last 5-10 posts:
        - hook (first line)
        - topic classification (map to strategic themes)
        - engagement count (likes + comments)
        - comment themes (top 3 recurring topics in comments)
        - post URL
        - post date
  - compile into raw_posts array
  - if browser_task fails or is rate-limited:
      log warning, reduce to available data
      do NOT fabricate posts
```

### 2. X/Twitter Extraction

```yaml
procedure: extract_x
input:
  queries: array of search queries (default niche queries below)
  time_window: string (default "7 days")
tool: search_social
default_queries:
  - "agentic AI -is:retweet"
  - "agent runtime architecture -is:retweet"
  - "AI trust infrastructure -is:retweet"
  - "fail-closed AI -is:retweet"
steps:
  - for each query:
      call search_social with only_recent=true
      extract top 10 results:
        - author handle
        - tweet text (first line = hook)
        - topic classification
        - engagement (likes + retweets)
        - URL
        - date
  - deduplicate across queries
  - compile into raw_posts array
```

### 3. Substack Extraction

```yaml
procedure: extract_substack
input:
  newsletters: array of Substack URLs (max 3)
  time_window: string (default "7 days")
tool: fetch_url
steps:
  - for each newsletter:
      fetch archive page
      extract last 3-5 article titles and summaries
      identify recurring themes and narrative shifts
      extract:
        - article title (= hook)
        - topic classification
        - summary snippet
        - URL
        - date
  - compile into raw_posts array
```

---

## Synthesis Procedure

After all extractions complete:

```yaml
procedure: synthesize
input:
  raw_posts: array (combined from all platforms)
steps:
  - theme_extraction:
      cluster raw_posts by topic
      identify top 3-5 emerging themes
      rank by frequency and recency
  - hook_extraction:
      select top 5-10 strongest hooks from raw_posts
      score by: engagement, relevance to JP's niche, novelty
  - positioning_analysis:
      identify positioning patterns across creators
      note: what narratives are gaining traction
      note: what gaps exist (topics no one is covering well)
  - audience_profiling:
      from comment analysis + post targeting:
        infer primary_icp
        extract pain_points (what problems are being discussed)
        extract aspirations (what outcomes are being sought)
  - confidence_scoring:
      0.0-0.3: very few sources, unreliable data
      0.4-0.6: moderate sources, some gaps
      0.7-0.8: good coverage, diverse sources
      0.9-1.0: comprehensive, multi-platform, high-signal
  - compile final output conforming to SocialSignalExtractionSchema
```

---

## Integration with Lev Graph Operator

This skill produces a JSON object. The calling skill (lev-graph-operator) is responsible for:

1. Receiving the JSON output
2. Embedding it into a Report or Proposal artifact body
3. Writing the artifact to Lev Artifacts via `write_artifact_to_notion`
4. Appending the event to Lev Event Log via `append_event`

### Example Call Chain

```
User: "Scan social signals for agent runtime trends"

lev-graph-operator:
  1. get_or_create_entity("Agent Runtime Trends", "Signal", "agent-runtime-trends", "content", "JP")
  2. load_context("agent-runtime-trends")
  3. choose_intent → Report
  4. invoke social-signal-extractor:
       extract_x(default niche queries)
       extract_substack([known newsletters])
       synthesize → SocialSignalExtractionSchema JSON
  5. draft_artifact(entity_context, "Report", signal_json)
  6. write_artifact_to_notion(report_artifact)
  7. append_event("skill.run", "agent-runtime-trends", { skill: "social-signal-extractor" })
```

---

## Default Targets

When no specific targets are provided, use these defaults:

### LinkedIn Creators (rotate based on availability)
- Search for creators posting about: agent runtime, AI orchestration, AI safety, enterprise AI

### Substack Newsletters
- Search for newsletters covering: AI engineering, agent systems, developer tooling

### X Queries
- `"agentic AI" -is:retweet`
- `"agent runtime" OR "agent orchestration" -is:retweet`
- `"AI trust" OR "AI safety enterprise" -is:retweet`
- `"fail-closed" OR "fail safe AI" -is:retweet`

---

## Error Handling

| Error | Action |
|-------|--------|
| Browser rate limited | Reduce scope, log warning, continue with available data |
| No results from a platform | Set that platform's array to empty, reduce confidence score |
| All platforms fail | Return `{ ok: false, errors: ["All extraction sources failed"] }` |
| Schema validation fails | Fix output, retry once, then return error |

---

## Limits

- Max 5 LinkedIn profiles per run
- Max 3 Substack newsletters per run
- Max 5 X queries per run
- No private/DM content
- No authentication-required content
- Respect robots.txt and rate limits
