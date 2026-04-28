---
name: lev-research/expansion
description: |
  [WHAT] Query expansion patterns and domain ladder for unsticking searches
  [HOW] 6-level domain ladder (file→component→topic→similar→goals→ideas) + perplexity expansion + stuck detector
  [WHEN] Use when initial search returns insufficient results or when exploring unfamiliar domains
  [WHY] Specific queries fail in unfamiliar territory; expanding to higher abstraction levels surfaces relevant context

  Triggers: "expand query", "domain ladder", "stuck search", "no results", "perplexity expansion"

lifecycle_integration:
  stage: captured
  input_artifact: query-string
  output_artifact: expanded-queries.yaml

related_skills:
  - lev-find
  - lev-research/perspectives
---

# lev-research/expansion - Query Expansion Patterns

## Lev Concept

**What is query expansion?**

Transforming narrow/specific queries into broader, multi-angle queries that surface relevant context. When a search fails or returns sparse results, expansion helps escape the "too specific" trap.

**Why does it exist?**

In unfamiliar domains, we don't know the right terminology. Specific searches fail. The domain ladder climbs from concrete (file names) to abstract (concepts), widening the aperture until results appear.

**When to use expansion:**
- Initial search returns 0-2 results
- Searching unfamiliar codebase/domain
- Need comprehensive coverage (not just exact matches)
- Exploring prior art or alternatives
- Research question is vague or exploratory

---

## CLI Commands

### Basic Expansion

```bash
# Auto-expand query
lev get "auth" --expand

# Domain ladder (auto-climb when stuck)
lev get "bd-daemon.ts" --ladder

# Perplexity expansion (AI-powered)
lev get "caching strategies" --expand-with=perplexity
```

### Manual Level Selection

```bash
# Start at specific domain level
lev get "authentication" --level=component
lev get "secure sessions" --level=goals

# Multi-level search (try 2 levels)
lev get "JWT" --levels=topic,similar
```

---

## Workflows

### Workflow 1: Domain Expansion Ladder (6 Levels)

**Use case:** Search stuck at specific level, need to broaden scope.

**The Ladder:**
```
🎯 Level 1: File/Function (SPECIFIC)
    "find the auth middleware file"
    "show me the validateToken function"

    ↓ Expand to Level 2

🔧 Level 2: Component/Module
    "authentication module for session handling"
    "token validation for API security"

    ↓ Expand to Level 3

📚 Level 3: Topic/Pattern
    "JWT authentication patterns"
    "session management approaches"

    ↓ Expand to Level 4

🌐 Level 4: Similar Projects
    "how does NextAuth handle sessions"
    "Passport.js vs custom auth"

    ↓ Expand to Level 5

🎯 Level 5: Goals/Problems
    "secure stateless authentication"
    "preventing session hijacking"

    ↓ Expand to Level 6

💡 Level 6: Ideas/Concepts (GENERAL)
    "zero-trust authentication principles"
    "identity vs authentication vs authorization"
```

**Climbing rules:**
- Start at highest certainty level
- Expand UP when results < threshold
- Typical sweet spot: Level 2-3 (component/topic)

**Example:**
```bash
# Level 1: Too specific, 0 results
lev get "bd-daemon.ts" --indexes codebase
# → 0 results, STUCK

# Auto-climb to Level 2
lev get "daemon sync module" --indexes codebase,documentation
# → 29 results, UNSTUCK

# Still too specific? Climb to Level 3
lev get "background daemon patterns" --indexes codebase,ideas
# → 156 results
```

---

### Workflow 2: Perplexity Reason Expansion

**Use case:** Unknown domain where you don't know what questions to ask.

**How it works:**

Uses `mcp__perplexity-mcp__reason` to generate intelligent query variations based on context analysis.

**Process:**
```bash
# 1. Send query to Perplexity Reason
mcp__perplexity-mcp__reason "
Given the research topic: 'authentication best practices'

Generate 5 search queries that would comprehensively cover:
1. Technical implementation details
2. Design rationale and alternatives
3. Common pitfalls and solutions
4. Related concepts I should understand
5. Emerging trends or best practices

Format as a numbered list of specific, searchable queries.
"

# 2. Extract generated queries
# Example output:
# 1. "multi-factor authentication implementation patterns"
# 2. "JWT vs session-based auth tradeoffs"
# 3. "authentication bypass vulnerabilities"
# 4. "OAuth2 vs OIDC protocol differences"
# 5. "passwordless authentication 2025 trends"

# 3. Execute expanded queries via lev get
lev get "multi-factor authentication implementation patterns"
lev get "JWT vs session-based auth tradeoffs"
# ... etc
```

**When to use Perplexity expansion:**
- Unknown domain (need AI to identify what you don't know)
- Complex multi-faceted topics
- Basic expansion misses context
- Cross-domain research (code + external knowledge)

**Example:**
```bash
# Topic: "How does our caching work?"
# Perplexity expands to:
# → "in-memory vs distributed caching strategies"
# → "cache invalidation patterns and edge cases"
# → "cache key design and namespace conventions"
# → "monitoring cache hit rates and performance"
# → "when to cache vs when to compute"
```

---

### Workflow 3: Stuck Detector (Auto-Climb Heuristic)

**Use case:** Automatically detect when search is stuck and suggest next level.

**Stuck signals:**

| Signal | Meaning | Action |
|--------|---------|--------|
| 0 results | Query too specific or wrong terminology | Climb 2 levels |
| 1-2 results | Query slightly too narrow | Climb 1 level |
| All results same file | Found it but need context | Search adjacent (deps, tests) |
| Results span 5+ dirs | Query too broad | Descend 1 level or add filters |
| No consensus across indexes | Terminology mismatch | Try synonyms + climb 1 level |

**Thresholds:**
```yaml
stuck_detector:
  thresholds:
    level_1_file:      results < 2  → climb to level 2
    level_2_component: results < 5  → climb to level 3
    level_3_topic:     results < 3  → climb to level 4
    level_4_similar:   results < 2  → climb to level 5
    level_5_goals:     results < 2  → climb to level 6
    level_6_ideas:     # Terminal - try different angle
```

**Auto-climb example:**
```bash
# Search: "bd-daemon.ts"
# Results: 0
# Detector: STUCK at level 1 (file)
# Suggestion: Climb to level 2 (component)
# Auto-expanded: "daemon sync module"
# New results: 29

# If still stuck at level 2 (< 5 results):
# Suggestion: Climb to level 3 (topic)
# Auto-expanded: "background daemon patterns"
```

**Implementation (pseudo-code):**
```python
def detect_stuck(query, results, current_level):
    if len(results) < THRESHOLDS[current_level]:
        return {
            "stuck": True,
            "reason": f"Only {len(results)} results at level {current_level}",
            "suggestion": f"Climb to level {current_level + 1}",
            "expanded_query": LADDER_TEMPLATES[current_level + 1].format(query)
        }
    return {"stuck": False}
```

---

## Query Expansion Patterns (Quick Reference)

### Pattern 1: Broad to Specific
```
"caching" →
  → "cache implementation"
  → "cache middleware"
  → "Redis integration"
  → "cache invalidation strategy"
```

### Pattern 2: Component Decomposition
```
"authentication system" →
  → "auth middleware"
  → "session management"
  → "token validation"
  → "user authentication endpoints"
  → "auth configuration"
```

### Pattern 3: Temporal Expansion
```
"error handling" →
  → "current error handling" (codebase)
  → "error handling decisions" (docs)
  → "error handling discussions" (sessions)
  → "TODO error handling improvements" (tasks)
```

### Pattern 4: Dependency Expansion
```
"API endpoints" →
  → "endpoint implementation" (what exists)
  → "endpoint middleware" (what connects)
  → "endpoint tests" (what validates)
  → "endpoint documentation" (what explains)
```

---

## Domain Ladder Level Details

### Level 1: File/Function (Exact Match)
**When to use:** You know the exact name
**Example queries:**
- "find auth.ts"
- "show validateToken function"
- "locate config.yaml"

**Typical results:** 0-3 (very specific)

---

### Level 2: Component/Module (Sweet Spot)
**When to use:** You know the feature area
**Example queries:**
- "authentication module"
- "caching component"
- "error handling middleware"

**Typical results:** 5-30 (focused but comprehensive)

**⭐ Recommended starting point for most searches**

---

### Level 3: Topic/Pattern (Design Patterns)
**When to use:** You know the pattern type
**Example queries:**
- "JWT authentication patterns"
- "hexagonal architecture"
- "repository pattern implementation"

**Typical results:** 10-100 (broad but relevant)

---

### Level 4: Similar Projects (Prior Art)
**When to use:** Exploring how others solved it
**Example queries:**
- "how NextAuth handles sessions"
- "Passport.js authentication flow"
- "Express vs Fastify middleware"

**Typical results:** External sources (exa-plus, web search)

**Note:** Requires external search backends (exa-plus)

---

### Level 5: Goals/Problems (Problem Space)
**When to use:** Understanding the "why"
**Example queries:**
- "secure stateless authentication goals"
- "preventing session hijacking"
- "ACID compliance requirements"

**Typical results:** Architecture docs, ADRs, requirements

---

### Level 6: Ideas/Concepts (Foundational)
**When to use:** Learning fundamentals
**Example queries:**
- "zero-trust security principles"
- "CAP theorem implications"
- "eventual consistency concepts"

**Typical results:** Ideas, sessions, learning resources

**⚠️ Terminal level - if stuck here, try different domain**

---

## Relates

### Depends On
- `lev-find` - Executes expanded queries

### Works With
- `lev-research/perspectives` - Expansion used in perspective queries
- `exa-plus` - External expansion (similar projects, prior art)
- `mcp__perplexity-mcp__reason` - AI-powered query generation

### Enables
- Unsticking blocked research
- Exploring unfamiliar codebases
- Comprehensive discovery

---

## Tips

**Start at Level 2 (component) by default:**
- Most searches succeed at component level
- Specific enough to be relevant
- Broad enough to surface context

**Use Perplexity for unknown domains:**
- Don't know the right questions? Ask AI
- Generates comprehensive query set
- Surfaces concepts you didn't know to search for

**Watch for stuck signals:**
- 0-2 results = too specific
- No consensus across indexes = wrong terminology
- All results in one file = found it, now search adjacent

**Combine with perspectives:**
```bash
# Expand query to level 3, then apply 5 perspectives
lev get "auth" --level=topic --perspectives=all
# → "auth patterns" × 5 perspectives = 25 queries
```

**Don't over-expand:**
- Level 6 (ideas/concepts) is terminal
- If stuck at 6, try a different angle or domain
- Sometimes the answer truly doesn't exist yet
