---
name: workflow-reverse-engineer-specs
description: |
  [WHAT] Reverse-engineer any SaaS product into feature inventory + architecture spec + gap map
  [HOW] Multi-source extraction → AI enhancement → synthesis against Lev/AgentPing capabilities
  [WHEN] "reverse engineer", "build like this", "spec this product", "feature inventory", "how does X work"
  [WHY] Fast path from "I saw a cool product" → actionable build plan with effort estimates
skill_type: workflow
category: research-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
tags:
  - workflow
  - research
  - reverse-engineering
  - competitive-analysis
  - architecture
  - feature-inventory
trigger_patterns:
  - "reverse engineer"
  - "build like this"
  - "spec this product"
  - "feature inventory"
  - "how does * work under the hood"
  - "analyze * architecture"
---

# Workflow: Reverse-Engineer → Specs

Transform any SaaS product into structured feature inventory, architecture spec, and prioritized build plan with effort estimates.

Every step spawns a **fresh subagent**. State flows only through handoff artifacts at `.lev/pm/handoffs/reng-*.md`.

## Trigger

- User wants to reverse-engineer a product to understand and/or build similar capability
- `/workflow reverse-engineer-specs <url> [--compare <module>] [--steps <list>] [--depth quick|standard|deep]`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `url` | yes | Product URL (SaaS web app, demo, or public docs) |
| `compare` | no | Lev module to gap-map against (default: `community/agentping`) |
| `steps` | no | Comma-separated workflow phases to execute (default: all) |
| `depth` | no | Extraction depth: quick=pages only, standard=pages+docs+api, deep=pages+docs+api+social |
| `output_dir` | no | Override output directory (default: `~/.config/LEV/reverse-eng/sessions/<date>/<product-slug>/`) |

## Steps

### Step 1: Discovery & Scrape

**Agent Type**: Research (haiku)
**Skills**: `skill://lev-research`, web scraping
**Research**:
- Visit target URL, identify product name and category
- Search for publicly accessible docs (docs.*, api.*, developers.*)
- Check for GitHub repo, changelog, blog, case studies
- Identify login flows vs public surfaces
- Read product tagline and primary use case

**Action**:
- Scrape main landing page + top 3-5 key pages (features, pricing, docs landing)
- Save raw HTML/markdown to `<session_dir>/artifacts/raw-pages/`
- Identify and list all discovery URLs: docs, API, changelog, blog
- Extract key metadata: product name, tagline, category, launch date, pricing tiers
- Create discovery manifest with confidence levels (high/medium/low)

**Handoff**: `.lev/pm/handoffs/reng-1-discovery.md`
```yaml
product_name: <name>
product_tagline: <tagline>
product_category: <category>
primary_use_case: <use case>
homepage_url: <url>
discovery_urls:
  docs: <url>
  api: <url>
  changelog: <url>
  blog: <url>
  github: <url>
public_surfaces: [<list of accessible pages>]
session_dir: <path>
```

---

### Step 2: Extract Features & API

**Agent Type**: Analyst (sonnet)
**Skills**: `skill://lev-research`, structured extraction
**Research**:
- Read discovery handoff from Step 1
- Parse scraped pages from `<session_dir>/artifacts/raw-pages/`
- Check for API documentation and OpenAPI/GraphQL specs
- Review changelog for feature history
- Identify component/UI library if publicly documented

**Action**:
- Extract all user-facing features: identify primary workflows, secondary features, integrations
- Create feature catalog with descriptions, UI hints, and dependencies
- If API docs available: parse endpoints, request/response schemas, rate limits, auth methods
- If UI component patterns visible: document layout patterns, interaction patterns, state management hints
- Build preliminary component catalog (not exhaustive, observation-based)
- Save extracted data in structured YAML formats

**Handoff**: `.lev/pm/handoffs/reng-2-extract.md`
```yaml
features_found: <n>
api_documented: true | false
api_endpoints: <n>
component_patterns_observed: <n>
extraction_confidence: <0.0-1.0>
feature_list_path: <path>
api_surface_path: <path>
component_catalog_path: <path>
```

---

### Step 3: Categorize & Estimate

**Agent Type**: Analyst (sonnet)
**Skills**: None
**Research**:
- Read extraction handoff from Step 2
- Read feature and API catalog files
- Review Lev/AgentPing existing capabilities if `--compare` specified

**Action**:
- Categorize each feature into bins: core_api, streaming, components, theming, integrations, infrastructure
- Assign effort estimates to each feature: S (1-3 days), M (3-7 days), L (1-2 weeks), XL (2+ weeks)
- Mark dependencies: which features depend on others
- Note integrations and external services required
- Create feature inventory with all metadata

**Handoff**: `.lev/pm/handoffs/reng-3-inventory.md`
```yaml
total_features: <n>
core_features: <n>
secondary_features: <n>
integrations: <n>
estimated_total_effort: <S|M|L|XL>
category_breakdown:
  core_api: <n>
  streaming: <n>
  components: <n>
  theming: <n>
  integrations: <n>
  infrastructure: <n>
feature_inventory_path: <path>
```

---

### Step 4: Architecture Synthesis

**Agent Type**: Analyst (sonnet)
**Skills**: `skill://lev-research`, architecture analysis
**Research**:
- Read all previous handoffs
- Read feature inventory
- Review scrape artifacts for technical hints
- Check for mentions of: tech stack, deployment strategy, data model hints, real-time capabilities

**Action**:
- Synthesize request flow diagram: user input → processing → output
- Infer data model: core entities, relationships, state management patterns
- Document API surface: endpoint categories, authentication, data formats
- Identify rendering pipeline: client-side vs server-side, streaming vs batch
- Note architectural patterns observed: MVC, event-driven, state machines, etc.
- Create architecture document with diagrams (mermaid)

**Handoff**: `.lev/pm/handoffs/reng-4-architecture.md`
```yaml
request_flow_documented: true | false
data_model_inferred: true | false
api_surface_mapped: true | false
rendering_pipeline_identified: true | false
architectural_patterns: [<list>]
architecture_document_path: <path>
diagram_format: mermaid
```

---

### Step 5: Gap Mapping (Conditional)

**Agent Type**: Analyst (sonnet)
**Skills**: None
**Research**:
- Skip this step if `--compare` not specified
- Read all previous handoffs
- Read target module code at specified path
- Examine target module's feature set, API, components

**Action**:
- For each feature in reverse-engineered product: mark status vs target module
  - has: feature already implemented
  - partial: feature partially implemented or needs enhancement
  - missing: not implemented
- Reference real file paths in target module for each capability
- Identify extension points where feature could be added
- Create gap analysis table with all three columns
- Recommend priority order for closing gaps

**Handoff**: `.lev/pm/handoffs/reng-5-gap-map.md`
```yaml
compare_module: <path>
total_features: <n>
has_count: <n>
partial_count: <n>
missing_count: <n>
coverage_percentage: <0-100>
gap_map_path: <path>
priority_gaps: [<top 3-5 missing features>]
```

---

### Step 6: Build Plan Generation

**Agent Type**: Analyst (sonnet)
**Skills**: None
**Research**:
- Read all previous handoffs and documents
- Review gap map if available
- Consider feature dependencies and effort estimates

**Action**:
- Create prioritized phases ordered by dependency and value
- Each phase includes:
  - Phase name and goal
  - Features included
  - Key files to modify or create
  - Estimated duration (e.g., "3-5 days")
  - Dependencies on prior phases
  - Success criteria
- Optimize for: early wins → core functionality → polish → integrations
- Keep phases to 1-2 weeks of effort each
- Generate build plan document

**Handoff**: `.lev/pm/handoffs/reng-6-build-plan.md`
```yaml
total_phases: <n>
estimated_duration: <duration>
phase_list_path: <path>
phases:
  - name: <phase>
    effort: <duration>
    feature_count: <n>
    depends_on: [<prior phases>]
```

---

### Step 7: Report & Synthesis

**Agent Type**: Analyst (sonnet)
**Skills**: None
**Research**:
- Read all prior handoffs and artifacts
- Compile comprehensive evidence

**Action**:
- Generate executive summary: what is this product, why it matters, build complexity
- Create output directory structure summary
- Write final synthesis document tying all findings together
- Output single consolidated markdown report suitable for sharing

**Handoff**: `.lev/pm/handoffs/reng-7-final.md`
```yaml
status: complete
product_analyzed: <name>
total_features: <n>
estimated_build_effort: <duration>
report_path: <path>
all_artifacts_generated: true | false
```

## Outputs

All files written to `~/.config/LEV/reverse-eng/sessions/<date>/<product-slug>/`:

```
{product-slug}/
├── artifacts/
│   ├── raw-pages/              # Raw HTML/markdown from scrape
│   ├── search_results.json     # If web search used
│   └── cache/
├── extraction/
│   ├── raw.md
│   ├── enhanced.md
│   ├── api-surface.yaml
│   └── component-catalog.yaml
├── feature-inventory.yaml      # Categorized with effort estimates
├── architecture.md             # Request flow + data model + API
├── gap-map.md                  # (if --compare specified)
├── build-plan.md               # Phases with effort estimates
├── final-report.md             # Executive summary + synthesis
└── session.json                # Metadata
```

## Validation Checklist

- [ ] Discovery found product homepage and at least 1 additional source (docs, API, changelog)
- [ ] Feature inventory has at least 8 features with categories and effort estimates
- [ ] Architecture document includes request flow diagram and data model
- [ ] If gap-map generated: every feature has status (has/partial/missing) with file references
- [ ] Build plan has 3-5 phases with clear dependencies and success criteria
- [ ] Final report includes executive summary and can be shared with stakeholders
- [ ] All 7 handoff files created

## Usage Examples

### Basic reverse-engineering

```bash
/workflow reverse-engineer-specs https://www.thesys.dev/
```

### Compare against AgentPing

```bash
/workflow reverse-engineer-specs https://v0.dev/ --compare community/agentping
```

### Quick extraction only

```bash
/workflow reverse-engineer-specs https://bolt.new/ --steps extract,enhance,inventory,architecture --depth quick
```

### Deep analysis with gap map

```bash
/workflow reverse-engineer-specs https://perplexity.ai/ --compare community/agentping --depth deep
```

## Team Structure

| Role | Model | Steps | Purpose |
|------|-------|-------|---------|
| scraper | haiku | 1-2 | Fast discovery and extraction |
| analyst | sonnet | 3-7 | Deep synthesis and planning |

## Technique Map

- **Multi-source extraction** - Combine homepage + docs + API + social for comprehensive understanding
- **Structured categorization** - Sort features by architectural concern (api, ui, infra) for clarity
- **Effort estimation** - Realistic time budgets enable prioritization
- **Gap mapping** - Direct comparison to target module reveals build priorities
- **Dependency ordering** - Phase sequencing prevents blocking work
- **Evidence preservation** - All artifacts saved for team review and iteration

## Technique Notes

These techniques improve reverse-engineering accuracy and actionability. Evidence-first approach (scrape real products) beats speculation. Structured output enables handoff between team members. Gap mapping bridges "what exists" to "what we build."

## Prompt Architect Overlay

### Role Definition

You are the prompt-architect-enhanced specialist for workflow-reverse-engineer-specs, responsible for deterministic extraction and synthesis of product specifications while preserving team handoff patterns.

### Input Contract

- Required: valid product URL and clear user intent
- Preferred: comparison module path if gap mapping desired, depth preference
- If ambiguous: clarify scope (architecture understanding vs build planning vs feature inventory)

### Output Contract

- Structured handoff files at `.lev/pm/handoffs/reng-*.md`
- All session artifacts in `~/.config/LEV/reverse-eng/sessions/<date>/<slug>/`
- Validation checklist items verified before declaring steps complete
- Actionable build plan with effort estimates and dependency ordering

### Edge Cases & Fallbacks

- If product is private/behind auth: note access limitations and infer from marketing materials only
- If API is undocumented: mark as "inferred from UI behavior" and lower confidence
- If scope is too broad: suggest phasing extraction (vertical slices vs features)
- If compare module doesn't exist: skip gap mapping and note in handoff
