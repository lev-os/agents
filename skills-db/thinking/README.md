# Thinking Frameworks Library

496 thinking frameworks organized across 15 domains, with 414 pattern definitions containing individual SKILL.md files.

**Source:** `~/lev/workshop/poc/skills/` (POC skills research project)

**Migrated:** 2026-02-09

---

## Quick Navigation

### Domains (15)

Each domain directory contains `domain.md` (rationale and core content) and `task.csv` (framework classifications).

| # | Domain | Description |
|---|--------|-------------|
| 01 | **Core Mental Models** | Foundation layer — universal thinking tools (Munger's latticework, inversion, first principles) |
| 02 | **Cognitive Biases** | Bias recognition and correction (anchoring, availability, confirmation bias) |
| 03 | **Systems Thinking** | Interconnected system analysis (feedback loops, leverage points, emergence) |
| 04 | **Decision Making** | Structured decision frameworks (DACI, Delphi method, expected value) |
| 05 | **Domain Specific** | Field-specific models (economics, physics, biology, law) |
| 06 | **Problem Solving** | Decomposition and resolution (5 Whys, root cause, constraint theory) |
| 07 | **Strategy & Wisdom** | Strategic thinking and ancient wisdom (7 Powers, game theory, Stoicism) |
| 08 | **Futures Thinking** | Forecasting and scenario planning (backcasting, scenario matrix, megatrends) |
| 09 | **Software Engineering** | Code and architecture patterns (DRY, SOLID, domain-driven design) |
| 10 | **App Development** | Application-specific patterns (cold start, network effects, platform strategy) |
| 11 | **UI/UX** | Design thinking and usability (Don Norman, design systems, information architecture) |
| 12 | **Growth & Distribution** | Growth loops, viral mechanics, distribution strategy |
| 13 | **Management & Strategy** | Organizational patterns (OKRs, leadership, team topology) |
| 14 | **Product Development** | Product lifecycle and methodology (lean, agile, product-market fit) |
| 15 | **CS & AI/ML** | Computer science and machine learning fundamentals |

### Patterns (`patterns/`)

414 individual framework definitions. Each pattern directory contains a `SKILL.md` with:

- Framework name and description
- When to apply
- Step-by-step application process
- Examples and anti-patterns

### Index (`skills-index.json`)

Master index with 54 priority frameworks including name, description, and path references.

### Special Directories

- `axioms/` — Foundational axioms underlying multiple frameworks
- `hidden-gems/` — Underutilized frameworks with high leverage

---

## Usage

**Browse by domain:** Start with a domain's `domain.md` for overview, then `task.csv` for the full framework list.

**Browse by pattern:** Go directly to `patterns/<framework-name>/SKILL.md` for any specific framework.

**Search:** Use `skills-index.json` for programmatic access to the priority set.

**Agent loading:** `s://thinking/patterns/<name>/SKILL.md` or load the domain overview with `s://thinking/<domain-num>/domain.md`

---

## Methodology

Frameworks were sourced from canonical texts (Munger, Parrish/Farnam Street, Bevelin, Weinberg, and others), classified by domain, deduplicated, and converted to structured SKILL.md definitions. See `~/.agents/skills-db/_workshop/poc-migration/docs/` for full process documentation and source references.
