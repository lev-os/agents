---
name: sherlock-research
description: "Investigative research engine combining OSINT tradecraft with UX research principles. Deploys an interactive dashboard with iterative deepening rounds, knowledge graph visualization, domain-based research routing, and Sherlock-style deduction chains. Use when asked to research, investigate, analyze, deep-dive, build a dossier, do OSINT, profile a person/company/topic, or conduct multi-round research. Triggers: 'research', 'investigate', 'deep dive', 'OSINT', 'dossier', 'profile', 'intelligence report', 'sherlock', 'analyze thoroughly'."
metadata:
  author: jp
  version: '1.0'
---

# Sherlock Research Engine

An investigative research system that combines OSINT (Open Source Intelligence) tradecraft with UX research synthesis principles. It produces an interactive, deployed dashboard with iterative deepening rounds, dual knowledge-graph visualization, confidence-scored findings, and Sherlock-style deduction chains.

## When to Use This Skill

Use this skill when the user asks you to:

- Research, investigate, or deep-dive into any topic, person, organization, market, or claim
- Build a dossier or intelligence report
- Conduct OSINT or open-source intelligence gathering
- Profile an entity (person, company, technology, market)
- Perform multi-round, iterative research with increasing depth
- Analyze something "like Sherlock Holmes" or "thoroughly"
- Create an investigative dashboard or research visualization

## Core Architecture

### The Intelligence Cycle (OSINT-Adapted)

Every investigation follows this cycle, repeated per round:

```
PLANNING → COLLECTION → PROCESSING → ANALYSIS → DISSEMINATION
    ↑                                                    |
    └────────── feedback loop (next round) ──────────────┘
```

1. **Planning** — Define requirements, identify domains, formulate search strategies
2. **Collection** — Execute searches, browse sources, gather raw data
3. **Processing** — Clean, normalize, cross-reference, deduplicate findings
4. **Analysis** — Apply deductive reasoning, score confidence, identify gaps
5. **Dissemination** — Update the dashboard, persist state, present findings

### Research Domains (Hybrid Detection)

The skill uses a hybrid approach: a pre-built domain library combined with auto-detection.

**Pre-Built Domain Library:**

| Domain | Icon | Description | Key Sources |
|---|---|---|---|
| **People** | 👤 | Individuals — background, roles, connections, digital footprint | LinkedIn, social media, publications, public records |
| **Organizations** | 🏢 | Companies, nonprofits, agencies — structure, leadership, financials | SEC filings, Crunchbase, news, corporate registries |
| **Financial** | 💰 | Revenue, funding, transactions, economic indicators | Financial statements, funding databases, market data |
| **Technology** | ⚙️ | Tech stacks, patents, architectures, tools, capabilities | GitHub, patents, technical docs, product pages |
| **Legal & Regulatory** | ⚖️ | Lawsuits, compliance, regulations, intellectual property | Court records, regulatory filings, patent databases |
| **Market & Competitive** | 📊 | Market sizing, competitors, positioning, trends | Industry reports, competitor sites, analyst coverage |
| **Social & Sentiment** | 💬 | Public perception, social media presence, reputation | X/Twitter, Reddit, forums, reviews, news sentiment |
| **Geographic** | 🌍 | Locations, jurisdictions, regional factors, supply chains | Maps, trade data, regional news, government data |
| **Temporal** | ⏳ | Timelines, event sequences, historical patterns, trends | News archives, Wayback Machine, historical data |
| **Network & Relationships** | 🔗 | Connections between entities, influence maps, affiliations | Cross-referencing all other domains for link analysis |

**Auto-Detection Logic:**
- Round 0 (Planning): Analyze the user's query to identify primary entities and suggest relevant domains
- Each subsequent round: If new entity types or domain signals emerge, suggest activating additional domains
- User confirms or adjusts before each round begins

### Depth Rounds — Iterative Deepening

Rounds are the core mechanic. Each round expands the knowledge graph by either:
- **Expanding leaf nodes** — Discovering new entities connected to existing ones
- **Increasing branch density** — Finding deeper connections between known entities

**Round Mechanics:**

| Depth | Rounds | Behavior | Output Complexity |
|---|---|---|---|
| **Quick Scan** | 1 | Broad sweep across activated domains. Identify key entities and obvious connections. Surface-level confidence scores. | Summary + key findings |
| **Standard** | 5 | Iterative deepening. Each round builds on prior findings. Cross-domain correlation begins. Deduction chains form. | Full dossier with graph |
| **Deep Investigation** | 20 | Exhaustive. Multi-hop entity resolution. Counter-deception checks. Historical analysis. Gap identification and targeted fill. | Complete intelligence product |

**Per-Round Algorithm:**

```
function executeRound(roundNumber, currentGraph, config):
  1. ASSESS current graph state
     - Identify leaf nodes (entities with few connections)
     - Identify weak edges (low-confidence connections)
     - Identify domain gaps (activated domains with thin coverage)

  2. GENERATE search queries using expansion strategies:
     a. Entity Expansion: For each leaf node, search for related entities
        "[entity name] + [domain-specific qualifiers]"
     b. Relationship Mining: For weakly-connected nodes, search for evidence
        "[entity A] + [entity B] + [relationship hypothesis]"
     c. Temporal Deepening: Search for historical/timeline data
        "[entity] + [time range] + [event type]"
     d. Contradiction Seeking: Actively look for disconfirming evidence
        "[entity] + [claim] + [criticism OR controversy OR dispute]"
     e. LLM Whim (Creative Expansion): Based on pattern recognition,
        generate lateral queries that a human analyst might not think of
        — analogies, adjacent fields, unexpected connections

  3. EXECUTE searches in parallel (use search_web, search_vertical,
     search_social, fetch_url, browser_task as appropriate)

  4. PROCESS results
     - Extract entities and relationships
     - Assign confidence scores (see Confidence Scoring below)
     - Cross-reference with existing graph
     - Deduplicate and merge

  5. UPDATE graph
     - Add new nodes and edges
     - Update confidence scores on existing edges
     - Record provenance (source URLs for every claim)

  6. ANALYZE
     - Run deduction engine on new evidence
     - Identify emerging patterns
     - Flag contradictions
     - Calculate coverage metrics per domain

  7. PERSIST state to workspace file

  return updatedGraph, roundSummary
```

### Confidence Scoring System

Every finding receives a confidence score based on OSINT analytic standards:

| Level | Score | Badge | Criteria |
|---|---|---|---|
| **Confirmed** | 90-100% | ✅ | Multiple independent sources corroborate. Direct evidence. |
| **Probable** | 70-89% | 🟢 | Strong evidence from reliable sources. Minor gaps acceptable. |
| **Possible** | 50-69% | 🟡 | Some supporting evidence but significant gaps. Single-source. |
| **Doubtful** | 25-49% | 🟠 | Weak evidence, conflicting sources, or outdated information. |
| **Improbable** | 0-24% | 🔴 | Contradicted by stronger evidence or from unreliable sources. |

**Scoring Factors:**
- Source reliability (primary vs. secondary vs. tertiary)
- Source independence (different organizations vs. echo chamber)
- Recency (how current is the information)
- Corroboration count (number of independent confirmations)
- Internal consistency (does it contradict other confirmed findings)

### The Deduction Engine

Every significant finding includes a deduction chain:

```
OBSERVATION → INFERENCE → CONFIDENCE → SUPPORTING/CONTRADICTING EVIDENCE

Example:
┌─ OBSERVATION: Company X filed 3 patents in quantum computing (Q1 2026)
├─ INFERENCE: Company X is building quantum computing capabilities,
│            likely pivoting from classical cloud infrastructure
├─ CONFIDENCE: Probable (78%)
├─ SUPPORTING:
│   • CEO mentioned "post-classical computing" at CES 2026 [source URL]
│   • 2 senior hires from IBM Quantum in past 6 months [source URL]
│   • R&D budget increased 40% YoY [source URL]
├─ CONTRADICTING:
│   • Q4 2025 earnings call focused entirely on classical cloud [source URL]
│   • No quantum job postings on careers page [source URL]
└─ SYNTHESIS: Patent filing pattern suggests early-stage exploration,
             not full pivot. Monitor for Q2 2026 hiring signals.
```

## Execution Workflow

### Phase 0: Intake & Configuration

When the user triggers this skill:

1. **Parse the query** to identify the primary research target
2. **Auto-detect relevant domains** from the query
3. **Ask the user** (if not specified):
   - Which domains to activate (present auto-detected + full library)
   - Desired depth (1 / 5 / 20 rounds)
   - Any specific questions or hypotheses to investigate
4. **Create the investigation state file** at `workspace/sherlock-investigations/{investigation-id}/state.json`

### Phase 1: Round Execution

For each round (1 to N):

1. **Plan** — Assess current graph, generate queries using the per-round algorithm
2. **Collect** — Execute parallel searches using appropriate tools:
   - `search_web` for general intelligence
   - `search_vertical` with `vertical="academic"` for research papers
   - `search_vertical` with `vertical="people"` for LinkedIn profiles
   - `search_social` for X/Twitter intelligence
   - `fetch_url` for reading specific pages in depth
   - `browser_task` for interactive data collection
   - `wide_research` for batch entity research (10+ entities)
3. **Process & Analyze** — Apply confidence scoring, run deduction engine
4. **Update state** — Persist to investigation state file
5. **Build/Update dashboard** — Generate or update the HTML dashboard

### Phase 2: Dashboard Generation

After each round, generate or update the deployed dashboard. The dashboard is the primary deliverable.

**Use the HTML template** in `skills/sherlock-research/dashboard-template.html` as the starting point. Populate it with actual investigation data.

**Dashboard Sections:**

1. **Header Bar** — Investigation title, target summary, round counter, timestamp
2. **Domain Selector** — Toggle research domains on/off, shows coverage per domain
3. **KPI Strip** — Key metrics: total entities, connections, avg confidence, domains active, deductions made
4. **Graph Visualization** (dual-mode, toggleable):
   - **Force-directed graph** (D3.js) — Nodes = entities, edges = relationships, node size = importance, edge thickness = confidence, color = domain
   - **Tree/hierarchy view** — Research branching across rounds, expandable nodes
5. **Deduction Panel** — Scrollable list of deduction chains, filterable by domain and confidence
6. **Evidence Feed** — Chronological findings with source links, confidence badges, round tags
7. **Round History** — Expandable per-round summaries showing what was discovered and how the graph changed
8. **Gap Analysis** — What we don't know yet, suggested next queries, domain blind spots

**Dashboard Design Direction:**
- Dark, analytical aesthetic — think intelligence analyst workstation
- Custom color palette: deep navy/charcoal base, teal accent for confirmed findings, amber for caution, muted reds for contradictions
- Monospace font for data values, Inter for UI text
- Dense but scannable — maximize information density without overwhelming
- Every data point links to its source URL

### Phase 3: Persistence

All investigation state is saved to workspace files for cross-session continuity:

```
workspace/sherlock-investigations/{investigation-id}/
├── state.json          # Full graph state, round history, configuration
├── round-{N}.json      # Per-round raw findings and queries used
├── entities.json       # All discovered entities with metadata
├── deductions.json     # All deduction chains
└── dashboard/          # The deployed dashboard files
    ├── index.html
    ├── base.css
    ├── style.css
    ├── app.js
    └── data.js         # Investigation data injected into dashboard
```

**State Schema (state.json):**
```json
{
  "id": "investigation-id",
  "title": "Investigation Title",
  "target": "Primary research target",
  "created": "ISO timestamp",
  "updated": "ISO timestamp",
  "config": {
    "maxRounds": 5,
    "completedRounds": 2,
    "activeDomains": ["people", "organizations", "financial"],
    "hypotheses": ["User-provided hypotheses to test"]
  },
  "graph": {
    "nodes": [
      {
        "id": "entity-uuid",
        "label": "Entity Name",
        "type": "person|org|tech|event|claim|location",
        "domain": "people",
        "confidence": 85,
        "round_discovered": 1,
        "sources": ["url1", "url2"],
        "metadata": {}
      }
    ],
    "edges": [
      {
        "source": "entity-uuid-1",
        "target": "entity-uuid-2",
        "relationship": "employs|funds|competes_with|...",
        "confidence": 72,
        "sources": ["url"],
        "round_discovered": 1
      }
    ]
  },
  "deductions": [
    {
      "id": "deduction-uuid",
      "observation": "What was directly observed",
      "inference": "What we conclude from it",
      "confidence": 78,
      "supporting": [{"claim": "...", "source": "url"}],
      "contradicting": [{"claim": "...", "source": "url"}],
      "synthesis": "Net assessment",
      "round": 2,
      "domain": "financial"
    }
  ],
  "roundHistory": [
    {
      "round": 1,
      "timestamp": "ISO",
      "queriesExecuted": 12,
      "newNodes": 8,
      "newEdges": 15,
      "avgConfidence": 67,
      "summary": "Round summary text",
      "expansionStrategy": "leaf_expansion"
    }
  ],
  "gaps": [
    {
      "domain": "financial",
      "description": "No revenue data found for 2025",
      "suggestedQueries": ["company X 2025 revenue", "company X annual report 2025"],
      "priority": "high"
    }
  ]
}
```

### Resuming an Investigation

When the user wants to continue a previous investigation:

1. Search memory for the investigation ID and path
2. Read `state.json` from the investigation directory
3. Restore graph state and configuration
4. Continue from the last completed round
5. Offer to adjust domains or depth before continuing

## Research Techniques by Domain

### People Domain
- LinkedIn profile analysis (use `search_vertical` with `vertical="people"`)
- Social media footprint mapping (use `search_social`)
- Publication and patent authorship search
- Public records and news mentions
- Conference talks and media appearances

### Organizations Domain
- Corporate structure and subsidiaries
- Leadership team and board composition
- Funding history and financial health
- Strategic partnerships and acquisitions
- News timeline and reputation analysis

### Financial Domain
- Revenue, funding rounds, valuations
- SEC filings and financial statements
- Investor relationships and cap table (if public)
- Market cap and stock performance (if public)
- Competitive financial benchmarking

### Technology Domain
- Tech stack analysis (job postings, GitHub repos, tech blogs)
- Patent portfolio analysis
- Open-source contributions
- Technical architecture decisions
- Tool and vendor relationships

### Legal & Regulatory Domain
- Court records and litigation history
- Regulatory filings and compliance
- Patent and trademark portfolio
- Data privacy compliance posture
- Industry-specific regulatory exposure

### Market & Competitive Domain
- TAM/SAM/SOM estimation
- Competitive landscape mapping
- Positioning and messaging analysis
- Pricing intelligence
- Market share estimation

### Social & Sentiment Domain
- X/Twitter conversation analysis
- Reddit and forum sentiment
- Review aggregation (G2, Trustpilot, etc.)
- News sentiment tracking
- Brand perception mapping

### Geographic Domain
- Headquarters and office locations
- Market presence by region
- Jurisdictional considerations
- Supply chain geography
- Regional regulatory exposure

### Temporal Domain
- Company timeline construction
- Event sequence analysis
- Trend identification over time
- Historical pattern matching
- Pivot and strategy shift detection

### Network & Relationships Domain
- Cross-entity relationship mapping
- Influence and centrality analysis
- Board interlock detection
- Investment network mapping
- Partnership ecosystem visualization

## UX Research Synthesis Principles

Apply these UX research methods to structure and synthesize findings:

### Affinity Mapping
- Group related findings into thematic clusters
- Use the graph's community detection to identify natural groupings
- Label clusters with descriptive theme names

### Insight Extraction (Atomic Research)
- Each finding = one atomic insight
- Template: "We observed [X] which suggests [Y] because [Z]"
- Link insights to specific evidence and sources

### Persona-Style Profiles
- For People domain: build behavioral profiles, not just biographical data
- For Organizations: build "organizational personas" — what drives their decisions

### Journey Mapping
- For temporal analysis: construct event timelines as journey maps
- Identify decision points, triggers, and outcomes

### Triangulation
- Never rely on a single source for critical findings
- Cross-reference across domains (e.g., financial data + news + social sentiment)
- Flag single-source findings for additional research

## Dashboard Template Usage

The dashboard template at `skills/sherlock-research/dashboard-template.html` provides the complete HTML/CSS/JS structure. When building a dashboard for an investigation:

1. Copy the template to the investigation's dashboard directory
2. Create `data.js` with the investigation data from `state.json`:
   ```javascript
   const INVESTIGATION_DATA = { /* state.json contents */ };
   ```
3. The template reads from `INVESTIGATION_DATA` and renders all panels
4. Deploy using `deploy_website`
5. After each round, update `data.js` and re-deploy

## Examples

### Example 1: Company Investigation
```
User: "Investigate Anthropic — 5 rounds deep"

Round 1: Broad sweep
- Auto-detect domains: Organizations, People, Financial, Technology, Market
- Gather: Leadership, funding, products, competitors, recent news
- Graph: ~20 nodes, ~30 edges

Round 2: Deepen key nodes
- Expand on key leaders (backgrounds, prior companies)
- Financial deep dive (all funding rounds, investors)
- Technology analysis (Claude models, safety research)
- Graph: ~45 nodes, ~80 edges

Round 3: Cross-domain correlation
- Map investor overlap with competitors
- Trace employee movement patterns
- Analyze patent/publication strategy
- Graph: ~70 nodes, ~140 edges

Round 4: Gap filling + contradiction seeking
- Fill identified gaps (missing financial data, etc.)
- Seek contradicting evidence for top deductions
- Temporal analysis of strategic shifts
- Graph: ~90 nodes, ~180 edges

Round 5: Synthesis + deduction refinement
- Final deduction chain refinement
- Net assessment across all domains
- Gap analysis for future research
- Graph: ~100+ nodes, ~200+ edges
```

### Example 2: Person Investigation
```
User: "Research John Doe, CTO of Acme Corp — quick scan"

Round 1: Single-round sweep
- Domains: People, Organizations, Technology, Social
- LinkedIn profile, publications, talks, social presence
- Role history, technical expertise, public opinions
- Graph: ~15 nodes, ~20 edges
- Deductions: 3-5 key inferences about expertise and influence
```

### Example 3: Resuming an Investigation
```
User: "Continue the Anthropic investigation — add 5 more rounds"

- Load state from workspace/sherlock-investigations/anthropic-{id}/state.json
- Resume from round 6 (previous investigation completed 5 rounds)
- Expand graph from existing ~100 nodes
- Focus on gaps identified in round 5
```

## Quality Standards

- **Every claim must have a source URL.** No unsourced assertions in the dashboard.
- **Confidence scores must be justified.** Not arbitrary — follow the scoring criteria.
- **Deduction chains must be falsifiable.** Include contradicting evidence when it exists.
- **The dashboard must be visually polished.** Follow the website-building skill's dashboard guidelines.
- **Persistence is mandatory.** Every round saves state for cross-session continuity.
- **Memory integration.** After each investigation, save a memory entry with the investigation ID, target, and key findings for future reference.
