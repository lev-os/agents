# Validation Report: Shell Method (Scenario Planning)

**Framework ID**: 35
**Slug**: shell-method-scenario-planning
**Domain**: 04-decision-making
**Initial Validation**: 2025-10-27 (context.yaml only)
**Dual-Artifact Validation**: 2025-10-29 (context.yaml + SKILL.md)
**Validator**: quality-validator agent

---

## Inclusion Criteria

### 1. ✅ Clarity Test: Can explain in 2 sentences?
**PASS**

The Shell Method is a scenario planning framework that replaces single-point forecasting with exploration of 2-4 plausible future scenarios defined by critical uncertainties, enabling organizations to identify robust strategies that work across all futures and contingent strategies triggered by specific scenarios. Developed at Royal Dutch Shell in the 1960s-70s, it gained legendary status by predicting the 1973 oil crisis while competitors operated on business-as-usual assumptions.

### 2. ✅ Execution Test: 3-7 actionable steps?
**PASS**

Framework contains 7 well-defined, actionable steps:
1. Identify focal question (define strategic decision and planning horizon)
2. Research elements and uncertainties (separate predetermined from uncertain)
3. Select two critical uncertainties (create 2×2 matrix)
4. Develop rich narratives (3-5 page stories for each quadrant)
5. Test strategy against scenarios (identify robust vs contingent moves)
6. Communicate organization-wide (embed scenario language)
7. Monitor and update (track trigger events)

Each step includes specific methods, guiding questions, and concrete outputs. Far exceeds minimum threshold.

### 3. ✅ Differentiation Test: Distinct from other frameworks?
**PASS**

Highly distinctive in multiple ways:
- **Methodological**: 2×2 matrix approach using critical uncertainties as axes (vs linear forecasting)
- **Psychological**: Type A/Type B technique to overcome management resistance to uncomfortable futures
- **Strategic**: Distinction between "no-regret" (robust) and "contingent" (scenario-dependent) strategies
- **Narrative-driven**: 3-5 page storytelling approach vs bullet-point analysis
- **Historical validation**: Documented success (1973 oil crisis) that differentiated practitioners from competitors

Not a rebranding or minor variation of existing frameworks.

### 4. ✅ Value Test: Would experienced practitioner find useful?
**PASS**

Exceptional practitioner value demonstrated by:
- **50+ years institutional use** at Shell (1965-present)
- **Documented ROI**: Shell rose from 7th to 2nd largest oil company during 1973 crisis
- **Wide adoption**: Fortune 500 companies, government agencies (Singapore), military
- **Concrete outputs**: Specific deliverables (scenario narratives, trigger indicators, strategy matrices)
- **Addresses real pain**: Strategic uncertainty at 5-30 year horizons where forecasting fails
- **Practitioner-tested**: Developed by Shell executives (Wack, Newland, Schwartz), not academic theorists

Scored 44/50 by framework's own rubric (Tier 1 Canonical).

### 5. ✅ Source Test: Credible practitioner or proven?
**PASS**

Exceptionally credible sources:
- **Pierre Wack**: Shell planning executive who developed method, documented in Harvard Business Review essays
- **Ted Newland**: Shell VP who led scenario planning institutionalization
- **Peter Schwartz**: Head of Shell scenario planning (1982-1986), founded Global Business Network, wrote definitive guide "The Art of the Long View"
- **Historical validation**: 1973 oil crisis prediction, 50+ years continuous use
- **Academic recognition**: Published in HBR, taught at business schools, subject of case studies

All sources are practitioners who shipped, not consultants selling services.

---

## Red Flags Check

### ❌ No Red Flags Detected

**Vague steps check**:
- Searched for "think about", "consider", "reflect on"
- Only found legitimate uses ("forces consideration of") in context of concrete actions
- All steps have specific methods and outputs

**Obvious checklists check**:
- Not repackaged common sense
- Contains counter-intuitive insights (Type A/Type B technique, predetermined vs uncertain distinction)
- Novel methodology developed over decades

**Clear trigger check**:
- Explicit trigger conditions defined (5-30 year horizons, genuine uncertainty, strategic inflection points)
- Also includes "do_not_use_when" scenarios (short-term tactical, stable environments)

**Implementation evidence check**:
- Documented 1973 oil crisis success with specific metrics
- 50+ years institutional use
- Government adoption (Singapore)
- Fortune 500 clients through GBN

**Consultantware check**:
- Developed by Shell internal executives for Shell's strategic needs
- Made public through HBR articles and books, not consulting engagements
- No requirement to hire consultants to use

**Buzzword check**:
- Searched for "synergy", "leverage", "paradigm shift", "game-changer"
- Zero matches found
- Language is precise and operational

---

## Technical Validation - context.yaml

### ✅ YAML Parsing
```bash
python3 -c "import yaml; yaml.safe_load(open('context.yaml'))"
✅ YAML parses successfully
```

### ✅ Lookup/Semantic Search
```bash
cd ../lookup
node cli.js index
✅ Index built successfully! Skills indexed: 25

node cli.js find "strategic uncertainty multiple futures"
Found 4 skills:
1. Shell Method (Scenario Planning) - 79% match (TOP RESULT)
```

Framework appears as #1 result for semantic trigger query, validating searchability.

### ✅ Cross-References
**Complements** (all valid references):
- backcasting
- three-horizons-framework
- monte-carlo-simulation
- swot-analysis
- red-team-analysis
- morphological-analysis
- horizon-scanning

**Conflicts with** (logical opposites):
- single-point-forecasting
- rigid-strategic-plans
- short-term-thinking

**Leads to** (natural progressions):
- decision-trees
- real-options-analysis
- strategic-early-warning-systems
- wargaming-simulation
- adaptive-strategy-execution

All cross-references are conceptually sound and represent real frameworks/concepts.

### ✅ metadata.version
```yaml
metadata:
  version: "1.0.0"
```

**Result**: ✅ PASS - All technical validations for context.yaml complete

---

## Technical Validation - SKILL.md

### ✅ File Exists
```bash
ls contexts/patterns/shell-method-scenario-planning/SKILL.md
# File exists: 11KB
```

### ✅ YAML Frontmatter Present
```yaml
---
name: shell-method-scenario-planning
description: Navigate strategic uncertainty through multiple plausible future scenarios rather than single-point forecasting. Developed at Royal Dutch Shell, this framework replaces single-point predictions with 2-4 rich narratives representing genuinely different futures defined by critical uncertainties.
---
```

Frontmatter is properly formatted with opening/closing `---` delimiters.

### ✅ Name Matches Slug
```
Directory name:  shell-method-scenario-planning/
context.yaml id: shell-method-scenario-planning
SKILL.md name:   shell-method-scenario-planning
```

Perfect consistency across all three identifiers.

### ✅ Structure Completeness

Required sections for Claude Code skill:
- ✅ **# Shell Method (Scenario Planning)** - Main title
- ✅ **## Purpose** - Clear explanation with historical validation
- ✅ **## When to Use This Skill** - 6 criteria-based triggers + semantic triggers
- ✅ **## Core Approach** - Central distinction (predetermined vs uncertain) + key insight
- ✅ **## Process** - 6 detailed steps with substeps, questions, deliverables, examples
- ✅ **## Practical Techniques** - 3 techniques (Type A/B, Predetermined Filter, Early Warning)
- ✅ **## Common Pitfalls** - 6 anti-patterns with corrections
- ✅ **## Integration** - Complements, conflicts with, leads to
- ✅ **## Time Estimates** - Full/rapid/refresh + complexity note
- ✅ **## Reference** - Authors, category, historical context

### ✅ Claude Code Skill Quality Standards

**When-to-Use Clarity**: ✅
- Clear criteria-based triggers (strategic uncertainty 5-30 years, experts disagree, disruption)
- Semantic search triggers ("scenario planning", "strategic foresight", "multiple futures")

**Actionability**: ✅
- Step-by-step process with concrete substeps
- Questions to answer at each step
- Clear deliverables defined
- Examples from Shell 1971-1973 throughout

**Practitioner Focus**: ✅
- No academic jargon
- Operational language
- Historical validation with metrics
- Time/complexity estimates for planning

**Integration**: ✅
- Maps to complementary frameworks
- Identifies conflicts
- Shows natural progressions

**Result**: ✅ PASS - SKILL.md meets all Claude Code skill standards

---

## Consistency Check (Dual-Artifact)

### ✅ Both Files in Same Directory
```bash
ls -lh contexts/patterns/shell-method-scenario-planning/
# context.yaml (23KB)
# SKILL.md (11KB)
```

Both artifacts co-located as required.

### ✅ Names Match Across All Identifiers
- Directory name: `shell-method-scenario-planning`
- context.yaml metadata.id: `shell-method-scenario-planning`
- SKILL.md frontmatter name: `shell-method-scenario-planning`

### ✅ Descriptions Consistent

**context.yaml**:
> "Navigate strategic uncertainty through multiple plausible future scenarios rather than single-point forecasting"

**SKILL.md**:
> "Navigate strategic uncertainty through multiple plausible future scenarios rather than single-point forecasting. Developed at Royal Dutch Shell, this framework replaces single-point predictions with 2-4 rich narratives representing genuinely different futures defined by critical uncertainties."

SKILL.md expands with attribution but core description is identical.

### ✅ File Sizes Reasonable
- context.yaml: 23KB (within 10-50KB optimal range)
- SKILL.md: 11KB (within 5-20KB optimal range)

Both comprehensive without bloat.

**Result**: ✅ PASS - Full consistency across both artifacts

---

## Overall Decision (Dual-Artifact Validation)

**STATUS**: ✅ **COMPLETE**

**Both Artifacts**: ✅ PASS
- context.yaml: PASS (all technical validations)
- SKILL.md: PASS (all Claude Code skill standards)

**Score**: 44/50 (Tier 1 Canonical Framework)
- Practitioner Weight: 10/10
- Clarity & Executability: 8/10
- Proven ROI: 10/10
- Novelty: 7/10 (revolutionary in 1960s-70s, mainstream by 2020s)
- Cross-Domain: 9/10

### Reasoning

This framework passes all 5 inclusion criteria with flying colors and exhibits zero red flags. Both artifacts (context.yaml and SKILL.md) meet all quality standards and are fully consistent. It represents the gold standard for scenario planning methodology:

1. **Historical validation**: Documented success predicting 1973 oil crisis
2. **Institutional longevity**: 50+ years continuous use at Shell
3. **Practitioner pedigree**: Developed by operational executives who shipped
4. **Methodological rigor**: 7-step process with specific techniques and outputs
5. **Cross-domain adoption**: Energy, tech, government, finance, military
6. **Clear documentation**: Definitive books, HBR articles, case studies
7. **Actionable outputs**: Scenario narratives, strategy matrices, trigger indicators

The framework is complex (8/10 vs 10/10 on Clarity) due to requiring skilled facilitation for quality execution, but this is appropriate given the strategic time horizons and organizational scope it addresses. Complexity is not vagueness—all steps are well-defined.

### Strengths
- Legendary track record with documented metrics
- Counter-intuitive techniques (Type A/Type B psychological reframing)
- Distinction between predetermined elements and critical uncertainties
- Robust vs contingent strategy framework
- Narrative-driven approach that creates shared organizational language
- Rich detail (389 lines of YAML, comprehensive coverage)

### Minor Notes
- Resource-intensive (3-6 months for full process)
- Requires skilled facilitation for quality
- Novelty reduced over time (score 7/10 vs 10/10 for hidden gems)
- These are appropriate trade-offs for strategic-level frameworks

---

### Artifacts Summary
- **context.yaml**: 23KB, 389 lines - Comprehensive Lev pattern with all required sections
- **SKILL.md**: 11KB, 223 lines - Complete Claude Code skill with clear usage triggers

---

## Next Steps

1. ✅ Mark status=COMPLETE in task.csv
2. ✅ Update notes: "Validated 2025-10-29, YAML + SKILL both PASS, 44/50 Tier 1 Canonical"
3. ✅ Framework ready for production use in both Lev and Claude Code contexts
4. Consider using as template/benchmark for other Tier 1 frameworks (score 40-50)

---

**Initial Validation (YAML only)**: 2025-10-27
**Dual-Artifact Validation (YAML + SKILL)**: 2025-10-29
**Confidence**: Very High
**Recommendation**: Accept and mark COMPLETE - Both artifacts production-ready
