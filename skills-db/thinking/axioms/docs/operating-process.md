# Operating Process

How to execute Axiom Explorer commands with proper input/output management for multi-step workflows.

---

## Core Principle: File-Based Workflow

Each skill reads from and writes to markdown files in a timestamped workspace. This enables:
- **Auditability** - Full trace of reasoning steps
- **Resumability** - Pause and continue later
- **Modularity** - Replace any step without re-running entire chain
- **Synthesis** - Final step reads all artifacts to create integrated map

---

## Workspace Structure

Each exploration creates a timestamped directory:

```
./tmp/axiom-<YYYYMMDD-HHMMSS>/
├── 00-input.md               # Original belief/prompt (user input)
├── 01-paraphrase.md          # Skill output: paraphrase-engineer
├── 02-steelman.md            # Skill output: steelman-enhance
│
├── 03a-level1.md             # dig-axioms Turn 1: Level 1 why
├── 03b-level2.md             # dig-axioms Turn 2: Level 2 why
├── 03c-level3.md             # dig-axioms Turn 3: Level 3 why (optional)
├── 03-dig-axioms.md          # dig-axioms synthesis of all levels
│
├── 04-map-elements.md        # Skill output: map-elements
│
├── 05a-devils-advocate.md    # multi-devils Turn 1: Argue FOR
├── 05b-anti-devils.md        # multi-devils Turn 2: Argue AGAINST
├── 05c-synthesis.md          # multi-devils Turn 3: Integrate
├── 05-multi-devils.md        # multi-devils complete debate record
│
├── 06-synthesize.md          # Skill output: synthesize-apply
├── 07-reflection.md          # Skill output: reflection-loop
└── FINAL-synthesis.md        # Reads all above, creates final map
```

**Naming convention:**
- `<step-number>-<skill-name>.md` for single-turn skills
- `<step-number><letter>-<turn-name>.md` for multi-turn skills (03a, 03b, 03c...)
- `<step-number>-<skill-name>.md` synthesis file combines all turns
- `00-input.md` always contains the starting belief/prompt
- `FINAL-synthesis.md` always contains the complete integrated map

**Multi-turn skills:**
- **dig-axioms**: 03a (level1) → 03b (level2) → 03c (level3) → 03 (synthesis)
- **multi-devils-debate**: 05a (devils) → 05b (anti-devils) → 05c (synthesis) → 05 (complete)

---

## Skill Input/Output Contracts

### paraphrase-engineer
**Input:**
- `00-input.md` - Original belief statement

**Output:**
- `01-paraphrase.md`
  - 3-5 variations (1a, 1b, 1c...)
  - Each variation with axiom implications
  - Selected variation for next steps

---

### steelman-enhance
**Input:**
- `01-paraphrase.md` - Selected variation

**Output:**
- `02-steelman.md`
  - Strongest charitable version
  - Internal contradictions resolved
  - Supporting empirical correlations added
  - Confidence levels marked

---

### dig-axioms (MULTI-TURN)
**Process:** Each "why?" is a separate turn/file. Each turn accepts previous level as input.

**Turn 1: Level 1**
- **Input:** `02-steelman.md` OR `01-paraphrase.md` (depending on command)
- **Output:** `03a-level1.md`
  - Ask "why do you believe this?"
  - Proactive guessing (5-8 options: emotional, tribal, rational, philosophical, unconceived, other)
  - User selects or provides answer
  - Level 1 axiom identified

**Turn 2: Level 2**
- **Input:** `03a-level1.md`
- **Output:** `03b-level2.md`
  - Ask "why do you believe [Level 1 axiom]?"
  - Proactive guessing (5-8 options)
  - User selects or provides answer
  - Level 2 axiom identified

**Turn 3: Level 3 (optional, if not at root)**
- **Input:** `03b-level2.md`
- **Output:** `03c-level3.md`
  - Ask "why do you believe [Level 2 axiom]?"
  - Proactive guessing (5-8 options)
  - User selects or provides answer
  - Level 3 axiom (root presumption)

**Final: Synthesis**
- **Input:** `03a-level1.md`, `03b-level2.md`, `03c-level3.md` (if exists)
- **Output:** `03-dig-axioms.md`
  - Complete axiom hierarchy
  - Chain visualized (belief → level1 → level2 → level3)
  - Scoring against evidence
  - Confidence assessment per level

---

### map-elements
**Input:**
- `03-dig-axioms.md` - Root axioms identified

**Output:**
- `04-map-elements.md`
  - Core axioms list
  - Emotional drivers (categorized)
  - Tribal/political alignments (Big 5, Haidt, Political Compass)
  - Optional: ANS quadrant mapping
  - Correlations with supporting data

---

### multi-devils-debate (MULTI-TURN)
**Process:** Each debate round is a separate turn/file. Each round accepts previous rounds as input.

**Turn 1: Devils Advocate**
- **Input:** `02-steelman.md` - Position to debate
- **Output:** `05a-devils-advocate.md`
  - Argue FOR the position (strengthen it further)
  - Map axioms for this perspective
  - Map emotional drivers
  - Map tribal/political alignments
  - Present strongest possible case

**Turn 2: Anti-Devils Advocate**
- **Input:** `05a-devils-advocate.md` - FOR position
- **Output:** `05b-anti-devils.md`
  - Argue AGAINST the position
  - Bring opposing viewpoints
  - Map axioms for opposition
  - Map emotional drivers for opposing side
  - Map tribal/political alignments
  - Present strongest counter-arguments

**Turn 3: Synthesis**
- **Input:** `05a-devils-advocate.md`, `05b-anti-devils.md`
- **Output:** `05c-synthesis.md`
  - Integrate insights from both sides
  - Find common ground
  - Identify tensions and trade-offs
  - Transcend binary opposition
  - Suggest nuanced position

**Final: Complete Debate Record**
- **Input:** `05a-devils-advocate.md`, `05b-anti-devils.md`, `05c-synthesis.md`
- **Output:** `05-multi-devils.md`
  - All three perspectives documented
  - Axioms/emotions/tribal for each side
  - Synthesis insights highlighted
  - Debate preparation notes
  - Areas of genuine disagreement vs misunderstanding

---

### synthesize-apply
**Input:**
- `03-dig-axioms.md` OR all prior step files (depending on command)

**Output:**
- `06-synthesize.md`
  - Integrated findings
  - Cynefin classification
  - Applications (prompts/experiments/builds)
  - Areas for further research
  - Confidence assessment

---

### reflection-loop
**Input:**
- `06-synthesize.md` - Initial synthesis
- User feedback (inline or separate file)

**Output:**
- `07-reflection.md`
  - Critique of process
  - Refinements suggested
  - Next exploration steps
  - Process improvements

---

### FINAL-synthesis
**Input:**
- ALL files in workspace (`00-input.md` through `07-reflection.md`)

**Output:**
- `FINAL-synthesis.md`
  - Complete integrated map
  - Executive summary (3-5 paragraphs)
  - Full axiom hierarchy
  - All perspectives integrated
  - Applications prioritized
  - Export-ready format

---

## Command Execution Pattern

### Example: axiom-drill-down

**Step 1: Initialize workspace**
```bash
ANALYSIS_ID="axiom-$(date +%Y%m%d-%H%M%S)"
mkdir -p ./tmp/$ANALYSIS_ID
```

**Step 2: Write input**
```bash
echo "# Input Belief

Remote work is better than office work.

## Context
Reflecting on 2 years of remote work vs 5 years in office." > ./tmp/$ANALYSIS_ID/00-input.md
```

**Step 3: Run paraphrase-engineer skill**
```
Input: ./tmp/$ANALYSIS_ID/00-input.md
Process: Generate 3-5 variations
Output: ./tmp/$ANALYSIS_ID/01-paraphrase.md
```

**Step 4: Run dig-axioms skill**
```
Input: ./tmp/$ANALYSIS_ID/01-paraphrase.md
Process: Socratic questioning (3 levels)
Output: ./tmp/$ANALYSIS_ID/03-dig-axioms.md
```

**Step 5: Run synthesize-apply skill**
```
Input: ./tmp/$ANALYSIS_ID/03-dig-axioms.md
Process: Integrate findings, classify, suggest applications
Output: ./tmp/$ANALYSIS_ID/06-synthesize.md
```

**Step 6: Final synthesis**
```
Inputs:
  - ./tmp/$ANALYSIS_ID/00-input.md
  - ./tmp/$ANALYSIS_ID/01-paraphrase.md
  - ./tmp/$ANALYSIS_ID/03-dig-axioms.md
  - ./tmp/$ANALYSIS_ID/06-synthesize.md

Process: Read all files, create integrated map
Output: ./tmp/$ANALYSIS_ID/FINAL-synthesis.md
```

---

## Full-Chain Example

**Command:** `full-chain` (all 7 skills)

```bash
# 1. Initialize
ANALYSIS_ID="axiom-$(date +%Y%m%d-%H%M%S)"
mkdir -p ./tmp/$ANALYSIS_ID

# 2. Write input
cat > ./tmp/$ANALYSIS_ID/00-input.md <<EOF
# Input Belief
[Your belief here]
EOF

# 3. Run skill chain
paraphrase-engineer      → ./tmp/$ANALYSIS_ID/01-paraphrase.md
steelman-enhance         → ./tmp/$ANALYSIS_ID/02-steelman.md
dig-axioms               → ./tmp/$ANALYSIS_ID/03-dig-axioms.md
map-elements             → ./tmp/$ANALYSIS_ID/04-map-elements.md
multi-devils-debate      → ./tmp/$ANALYSIS_ID/05-multi-devils.md
synthesize-apply         → ./tmp/$ANALYSIS_ID/06-synthesize.md
reflection-loop          → ./tmp/$ANALYSIS_ID/07-reflection.md

# 4. Final synthesis
FINAL-synthesis reads all 00-07 files → ./tmp/$ANALYSIS_ID/FINAL-synthesis.md
```

---

## File Format Standards

### All Output Files Must Include

**Header:**
```markdown
# [Skill Name] Output

**Analysis ID:** axiom-20250129-001830
**Timestamp:** 2025-01-29 00:18:30
**Previous step:** [filename if applicable]
**Next step:** [filename if known]
```

**Status Section:**
```markdown
## Status
- Input file: 01-paraphrase.md
- Processing: dig-axioms skill
- Output: 03-dig-axioms.md
- Confidence: 75%
- Issues: None
```

**Content Section:**
```markdown
## Findings

[Skill-specific output content]
```

**Metadata Footer:**
```markdown
---
## Metadata
- Framework used: ACH (Analysis of Competing Hypotheses)
- Processing time: 8 minutes
- User feedback: [If applicable]
```

---

## Resumability Pattern

**To resume a paused exploration:**

```bash
# 1. Identify last completed step
ls ./tmp/axiom-20250129-001830/
# Shows: 00-input.md, 01-paraphrase.md, 02-steelman.md (stopped here)

# 2. Resume from next skill
dig-axioms --input ./tmp/axiom-20250129-001830/02-steelman.md \
           --output ./tmp/axiom-20250129-001830/03-dig-axioms.md

# 3. Continue chain
[run remaining skills]

# 4. Generate final synthesis
```

---

## Skip-Step Pattern

**To skip optional skills:**

```bash
# Example: Skip multi-devils-debate, go straight to synthesis

paraphrase-engineer      → 01-paraphrase.md
steelman-enhance         → 02-steelman.md
dig-axioms               → 03-dig-axioms.md
map-elements             → 04-map-elements.md
# SKIP: multi-devils-debate
synthesize-apply         → 06-synthesize.md  # Reads 00-04, skips 05
FINAL-synthesis          → FINAL-synthesis.md
```

**Note in FINAL-synthesis.md:**
```markdown
## Workflow Notes
- Skipped: multi-devils-debate (05)
- Reason: Single perspective analysis, debate not needed
```

---

## Parallel Skill Execution

**Some skills can run in parallel if independent:**

```bash
# After dig-axioms completes, these can run in parallel:
map-elements             → 04-map-elements.md    # Uses 03-dig-axioms.md
proactive-guessing       → 04b-guessing.md       # Uses 03-dig-axioms.md
correlation-grounding    → 04c-correlations.md   # Uses 02-steelman.md

# Then synthesis reads all:
synthesize-apply reads 03, 04, 04b, 04c → 06-synthesize.md
```

---

## Error Handling

**If a skill fails:**

```bash
# Skill writes error file
./tmp/$ANALYSIS_ID/03-dig-axioms-ERROR.md

Content:
# Error Report

## Skill: dig-axioms
## Timestamp: 2025-01-29 00:25:43

## Error:
Unable to identify root axioms - belief too vague.

## Suggested fix:
- Return to paraphrase-engineer
- Request more specific belief statement
- Re-run dig-axioms

## User can:
1. Edit 01-paraphrase.md manually
2. Re-run dig-axioms
3. Or skip to synthesis with partial results
```

---

## Synthesis Process Details

**FINAL-synthesis reads in order:**

1. **00-input.md** - Original belief
2. **01-paraphrase.md** - Interpretations
3. **02-steelman.md** - Strongest version
4. **03-dig-axioms.md** - Root assumptions
5. **04-map-elements.md** - Emotional/tribal drivers
6. **05-multi-devils.md** - Alternative perspectives
7. **06-synthesize.md** - Initial integration
8. **07-reflection.md** - Refinements

**Creates sections:**
- Executive Summary (3 paragraphs)
- Belief Evolution (input → paraphrase → steelman)
- Axiom Hierarchy (tree view from 03)
- Emotional & Tribal Map (from 04)
- Alternative Perspectives (from 05)
- Integrated Findings (from 06 + 07)
- Applications (prioritized list)
- Confidence Assessment
- Areas for Further Exploration

---

## Workspace Cleanup

**After exploration:**

```bash
# Option 1: Archive
tar -czf axiom-20250129-001830.tar.gz ./tmp/axiom-20250129-001830/
mv axiom-20250129-001830.tar.gz ./archive/

# Option 2: Keep only final synthesis
cp ./tmp/axiom-20250129-001830/FINAL-synthesis.md ./output/remote-work-analysis.md
rm -rf ./tmp/axiom-20250129-001830/

# Option 3: Keep for learning/iteration
# Leave in ./tmp/ for reference
```

---

## Integration with Version Control

**To track explorations over time:**

```bash
# After final synthesis, commit to git
git add ./output/remote-work-analysis.md
git commit -m "Axiom exploration: Remote work belief

Analysis ID: axiom-20250129-001830
Command: axiom-drill-down
Key findings: 3 root axioms identified, autonomy primary driver"
```

---

## Summary: Operating Checklist

For every command execution:

- ☐ Initialize timestamped workspace (`./tmp/axiom-<timestamp>/`)
- ☐ Write input belief to `00-input.md`
- ☐ Run each skill in sequence, outputting numbered files
- ☐ Each skill reads from previous step's file
- ☐ Each skill writes to its own numbered file
- ☐ Run FINAL-synthesis reading all intermediate files
- ☐ Review `FINAL-synthesis.md` for complete map
- ☐ Archive or cleanup workspace

**This file-based workflow ensures every exploration is traceable, resumable, and auditable.**
