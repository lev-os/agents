# Agentic Workflow - Framework Research to SKILL.md

## Working Directory

```bash
$HOME/digital/leviathan/poc/skills
```

All paths below are relative to this directory unless specified as absolute.

---

## Architecture (v2 - Consolidated)

**2-Agent Pipeline** (was 4 agents):

1. **Research+Artifact Generator**: UNKNOWN → ARTIFACTS_READY
2. **Quality Validator**: ARTIFACTS_READY → COMPLETE

**Artifacts**: context.yaml + SKILL.md

- `context.yaml` is canonical source of truth (Leviathan format)
- `SKILL.md` is execution documentation (can be generated via adapter)
- Claude Code standard frontmatter (name, description) in SKILL.md

**Index**: skills-index.json (centralized lookup)

---

## File & Folder Naming Conventions

### Variables Used Throughout

```bash
{domain-id}         # 01, 02, 03...15 (zero-padded)
{domain-name}       # core-mental-models, cognitive-biases, etc.
{framework-id}      # ID from task.csv (01, 02, 03...) zero-padded
{framework-name}    # Exact name from task.csv: "Inversion", "First Principles"
{framework-slug}    # Generated: "inversion", "first-principles"
{track}             # mental-models | practitioner-frameworks
{status}            # UNKNOWN | VAGUE | ARTIFACTS_READY | COMPLETE | REJECTED
```

### Slug Generation Algorithm

```bash
# Framework name → slug
"Inversion"                  → inversion
"First Principles Thinking"  → first-principles-thinking
"OODA Loop"                  → ooda-loop
"Jobs to Be Done"            → jobs-to-be-done

# Rules:
# 1. Lowercase everything
# 2. Replace spaces with hyphens
# 3. Remove special characters (except hyphens)
# 4. Keep acronyms as-is but lowercase (OODA → ooda)
```

### Directory Structure

```
domains/{domain-id}-{domain-name}/
├── domain.md                                    # Framework descriptions
├── task.csv                                     # Framework inventory
└── work/                                        # Created on first framework
    └── {framework-id}-{framework-slug}/        # Per-framework workspace
        ├── 01-research-notes.md                # From research-artifact-generator
        └── 03-validation-report.md             # From quality-validator

contexts/
├── patterns/{framework-slug}/                   # Per-framework output
│   ├── context.yaml                            # Leviathan context (canonical)
│   └── SKILL.md                                # Claude Code skill (100-200 lines, optional)
└── skills-index.json                           # Centralized lookup index
```

---

## Agent Files

```
agents/research-artifact-generator.md    # Research + generate SKILL.md (UNKNOWN → ARTIFACTS_READY)
agents/quality-validator.md              # Validate + index (ARTIFACTS_READY → COMPLETE)
agents/deduplication-agent.md            # Merge duplicates across domains

# Deprecated (4-agent workflow):
agents/research-agent.md                 # Superseded
agents/content-analyst.md                # Superseded
agents/artifact-generator.md             # Superseded
```

---

## Processing a Framework: Complete Workflow

### Step 1: Initialize

```bash
# Set variables
DOMAIN_ID="01"
DOMAIN_NAME="core-mental-models"
DOMAIN_PATH="domains/${DOMAIN_ID}-${DOMAIN_NAME}"
FRAMEWORK_ID="05"
FRAMEWORK_NAME="OODA Loop"
FRAMEWORK_SLUG="ooda-loop"

# Create work directory
mkdir -p ${DOMAIN_PATH}/work/${FRAMEWORK_ID}-${FRAMEWORK_SLUG}
```

### Step 2: Agent 1 - Research+Artifact Generator

**Execute When**: status = UNKNOWN or VAGUE

```
You are executing the research-artifact-generator for the Skills & Frameworks Catalog.

**Agent Definition**: Read agents/research-artifact-generator.md completely and follow it exactly.

**Working Directory**: $HOME/digital/leviathan/poc/skills

**Framework**:
- ID: {framework-id}
- Name: "{framework-name}"
- Domain: {domain-id}-{domain-name}
- Track: {track}

**Your Outputs**:
1. domains/{domain}/work/{id}-{slug}/01-research-notes.md
2. contexts/patterns/{slug}/context.yaml (Leviathan context)
3. contexts/patterns/{slug}/SKILL.md (100-200 lines, optional - can be generated via adapter)
4. task.csv: status=ARTIFACTS_READY

**Deliverables**:
- Research notes with source + score
- context.yaml (canonical Leviathan format)
- SKILL.md (target: 100-200 lines, optional)
- Report: Score, line count, status
```

**Output Files**:

```
domains/{domain}/work/{id}-{slug}/
└── 01-research-notes.md

contexts/patterns/{slug}/
├── context.yaml                # Leviathan context (canonical)
└── SKILL.md                    # 100-200 lines (optional)
```

### Step 3: Agent 2 - Quality Validator

**Execute When**: status = ARTIFACTS_READY

```
You are executing the quality-validator for the Skills & Frameworks Catalog.

**Agent Definition**: Read agents/quality-validator.md completely and follow it exactly.

**Working Directory**: $HOME/digital/leviathan/poc/skills

**Framework**:
- ID: {framework-id}
- Name: "{framework-name}"
- Slug: {framework-slug}
- Domain: {domain-id}-{domain-name}

**Your Input**:
contexts/patterns/{slug}/context.yaml (and SKILL.md if present)

**Your Outputs**:
1. domains/{domain}/work/{id}-{slug}/03-validation-report.md
2. contexts/skills-index.json (add entry)
3. task.csv: status=COMPLETE

**Validation Checks**:
1. 5 inclusion criteria (clarity, execution, differentiation, value, source)
2. Red flags (vague language, buzzwords)
3. Technical (frontmatter, line count 100-200)

**Deliverables**:
- Validation report
- Index entry added
- Report: COMPLETE or REJECTED
```

**Output Files**:

```
domains/{domain}/work/{id}-{slug}/
├── 01-research-notes.md
└── 03-validation-report.md        ← NEW

contexts/patterns/{slug}/
├── context.yaml                   ← Validated
└── SKILL.md                       ← Validated (if present)

contexts/skills-index.json         ← Entry added
```

---

## Resume Logic

```bash
STATUS=$(grep "^${FRAMEWORK_ID}," ${DOMAIN_PATH}/task.csv | cut -d, -f4 | tr -d '"')

case $STATUS in
  "COMPLETE")
    echo "✅ Complete, skip"
    NEXT_AGENT="skip"
    ;;
  "ARTIFACTS_READY")
    echo "→ Needs validation"
    NEXT_AGENT="quality-validator"
    ;;
  "UNKNOWN"|"VAGUE")
    echo "→ Needs research + artifact"
    NEXT_AGENT="research-artifact-generator"
    ;;
  "REJECTED")
    echo "❌ Rejected, skip"
    NEXT_AGENT="skip"
    ;;
esac
```

---

## CSV Update Mechanism

### Column Reference

```csv
id,name,track,status,detail_level,source_hint,priority,score,yaml_path,notes
```

### Status Transitions

```
UNKNOWN → ARTIFACTS_READY (Agent 1)
ARTIFACTS_READY → COMPLETE (Agent 2)
Any → REJECTED (if quality fails)
```

### Example Updates

```bash
# After Agent 1
1,"Inversion",mental-models,ARTIFACTS_READY,skill-generated,"Charlie Munger",high,42,"contexts/patterns/inversion/SKILL.md","SKILL.md 145 lines"

# After Agent 2
1,"Inversion",mental-models,COMPLETE,validated,"Charlie Munger",high,42,"contexts/patterns/inversion/SKILL.md","Validated 2025-10-30, PASS (145 lines)"
```

---

## skills-index.json Format

```json
{
  "frameworks": [
    {
      "name": "inversion",
      "description": "Solve problems by working backwards from the desired outcome",
      "path": "contexts/patterns/inversion/SKILL.md"
    },
    {
      "name": "second-order-thinking",
      "description": "Trace decisions beyond immediate effects to understand consequences",
      "path": "contexts/patterns/second-order-thinking/SKILL.md"
    }
  ]
}
```

---

## Quality Gates

**After Agent 1 (Research+Artifact)**:

- ✅ Score ≥ 15/50
- ✅ context.yaml exists (canonical Leviathan format)
- ✅ SKILL.md exists (100-200 lines, optional - can be generated via adapter)
- ✅ Frontmatter valid (name, description) if SKILL.md present
- ✅ Steps are actionable (verbs, not theory)
- ✅ CSV status = ARTIFACTS_READY

**After Agent 2 (Quality Validator)**:

Run AUTO-CORRECTING validator (handles all known issues):
```bash
./scripts/validate-patterns.sh  # Auto-fixes + reports
```

Manual CLI for single patterns:
```bash
./scripts/validate-cli.sh {slug}        # Check
./scripts/validate-cli.sh {slug} fix    # Auto-fix
```

Quality gates:
- ✅ All 5 inclusion criteria PASS
- ✅ Zero red flags
- ✅ YAML frontmatter valid (name matches slug, description adequate)
- ✅ Line count 50-400 (warn if >250)
- ✅ Index entry added
- ✅ CSV status = COMPLETE
- ✅ Validation report saved to domains/{domain}/work/{id}-{slug}/
- ⚠️ If FAIL: Failure report in `reports/failures/{slug}-failure.md`

**Co-Dependent Validation (CLI + Agent):**

**CLI auto-fixes (deterministic only):**
- Name mismatch → Changes to match slug (safe)

**CLI reports, AGENT fixes (requires intelligence):**
- Missing YAML markers → Agent reads framework, writes quality description
- Missing description field → Agent writes trigger-based description
- Poor description → Agent rewrites with trigger condition
- Missing name field → Agent adds `name: {slug}`

**Key principle**: Descriptions require understanding, not extraction.
See `docs/description-quality-guide.md` for rubric.

---

## Token Efficiency Targets

**Old (4-agent)**:

- context.yaml: 300+ lines
- SKILL.md: 400+ lines
- 12+ minutes per framework

**New (2-agent)**:

- context.yaml: Canonical source of truth
- SKILL.md: 100-200 lines (optional, can be generated via adapter)
- ~6 minutes per framework
- 60-70% token reduction

---

## Batch Operations

### Find All UNKNOWN

```bash
grep ",UNKNOWN," domains/*/task.csv
```

### Count by Status

```bash
for csv in domains/*/task.csv; do
  tail -n +2 "$csv" | cut -d, -f4 | tr -d '"'
done | sort | uniq -c
```

### List All Skills

```bash
find contexts/patterns -name "SKILL.md"
```

### Verify Index

```bash
cat contexts/skills-index.json | jq '.frameworks | length'
```

---

## File Path Reference

```bash
# Research notes
domains/{domain-id}-{domain-name}/work/{framework-id}-{framework-slug}/01-research-notes.md

# Validation report
domains/{domain-id}-{domain-name}/work/{framework-id}-{framework-slug}/03-validation-report.md

# context.yaml
contexts/patterns/{framework-slug}/context.yaml

# SKILL.md (optional, can be generated via adapter)
contexts/patterns/{framework-slug}/SKILL.md

# Index
contexts/skills-index.json

# Domain CSV
domains/{domain-id}-{domain-name}/task.csv
```
