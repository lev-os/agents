# Commands Index

Orchestrated workflows that chain skills together for specific exploration goals. Each command follows a file-based workflow pattern for auditability and resumability.

**See `docs/operating-process.md` for complete workflow documentation.**

---

## Workflow Pattern (All Commands)

```bash
# 1. Initialize timestamped workspace
ANALYSIS_ID="axiom-$(date +%Y%m%d-%H%M%S)"
mkdir -p ./tmp/$ANALYSIS_ID

# 2. Write input to 00-input.md

# 3. Run skills in sequence, each writes to numbered file:
#    01-paraphrase.md, 02-steelman.md, 03-dig-axioms.md, etc.

# 4. FINAL-synthesis reads all files → FINAL-synthesis.md
```

---

## full-chain.md

**What it does:** Complete 7-step process for comprehensive belief exploration. Runs all core skills in sequence with full feature set enabled.

**Skill stack:** paraphrase-engineer → steelman-enhance → dig-axioms → map-elements → multi-devils-debate → synthesize-apply → reflection-loop → FINAL-synthesis

**Use when:**
- You have 30-45 minutes for deep analysis
- Complex belief or idea needs thorough examination
- Want complete map with all perspectives
- High-stakes decision or debate preparation
- Need full emotional, tribal, and rational analysis

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your belief statement
├── 01-paraphrase.md          # 3-5 variations with axiom implications
├── 02-steelman.md            # Strongest charitable version + correlations
│
├── 03a-level1.md             # TURN 1: Why believe this? (+ proactive guessing)
├── 03b-level2.md             # TURN 2: Why that? (+ proactive guessing)
├── 03c-level3.md             # TURN 3: Why that? (+ proactive guessing)
├── 03-dig-axioms.md          # Synthesis: Complete axiom hierarchy
│
├── 04-map-elements.md        # Emotions, tribal, ANS quadrants
│
├── 05a-devils-advocate.md    # TURN 1: Argue FOR position
├── 05b-anti-devils.md        # TURN 2: Argue AGAINST position
├── 05c-synthesis.md          # TURN 3: Integrate both sides
├── 05-multi-devils.md        # Complete debate record
│
├── 06-synthesize.md          # Integrated findings + Cynefin + applications
├── 07-reflection.md          # User feedback + refinements
└── FINAL-synthesis.md        # Complete map (reads all above)
```

**Final output:** `FINAL-synthesis.md` contains:
- Executive summary
- Complete axiom hierarchy
- All perspectives integrated
- Prioritized applications
- Confidence assessment

**Time:** 30-45 minutes

---

## axiom-drill-down.md

**What it does:** Quick Socratic exploration without debate or emotional mapping. Fast "why" chain to find root assumptions.

**Skill stack:** paraphrase-engineer → dig-axioms → synthesize-apply → FINAL-synthesis

**Use when:**
- Need quick root cause analysis
- Limited time (5-10 minutes)
- Focused on logical chain only
- Don't need emotional/tribal context
- Simple belief or claim to trace

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your belief statement
├── 01-paraphrase.md          # Clarified variations
│
├── 03a-level1.md             # TURN 1: Why believe this? (+ proactive guessing)
├── 03b-level2.md             # TURN 2: Why that? (+ proactive guessing)
├── 03c-level3.md             # TURN 3: Why that? (+ proactive guessing)
├── 03-dig-axioms.md          # Synthesis: Complete axiom hierarchy
│
├── 06-synthesize.md          # Basic integration + applications
└── FINAL-synthesis.md        # Quick map (reads 00, 01, 03*, 06)
```

**Note:** `03*` means reads 03a, 03b, 03c, and 03-dig-axioms.md

**Final output:** `FINAL-synthesis.md` contains:
- Clarified belief
- Root axiom chain
- Basic applications

**Time:** 5-10 minutes

---

## steelman-correlations.md

**What it does:** Build strongest charitable version of argument with empirical grounding. Strengthen weak positions with data.

**Skill stack:** steelman-enhance → correlation-grounding → synthesize-apply → FINAL-synthesis

**Use when:**
- Weak or unclear argument needs strengthening
- Want most defensible version
- Need evidence and data backing
- Preparing to present position
- Testing if claim has empirical support

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your argument/claim
├── 02-steelman.md            # Strongest version + contradictions resolved
├── 02b-correlations.md       # Empirical data + evidence quality scores
├── 06-synthesize.md          # Applications + gaps identified
└── FINAL-synthesis.md        # Strengthened argument (reads 00, 02, 02b, 06)
```

**Final output:** `FINAL-synthesis.md` contains:
- Most robust version
- Supporting evidence
- Confidence levels
- Gaps in support

**Time:** 10-15 minutes

---

## unconceived-explorer.md

**What it does:** Hunt for hidden assumptions about time, causality, determinism, and other philosophical foundations. Surface blind spots.

**Skill stack:** dig-axioms + proactive-guessing (unconceived category) → map-elements → FINAL-synthesis

**Use when:**
- Sensing blind spots or missing angles
- Want to challenge unstated premises
- Philosophical foundations matter
- Need creative alternatives
- Stuck in conventional thinking

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your belief statement
│
├── 03a-level1.md             # TURN 1: Why? (emphasis on unconceived category)
├── 03b-level2.md             # TURN 2: Why? (emphasis on unconceived category)
├── 03c-level3.md             # TURN 3: Why? (emphasis on unconceived category)
├── 03-dig-axioms.md          # Synthesis: Axiom hierarchy with unconceived focus
│
├── 04-map-elements.md        # Philosophical foundations mapped
└── FINAL-synthesis.md        # Blind spots revealed (reads 00, 03*, 04)
```

**Note:** Each dig-axioms turn emphasizes "unconceived alternatives" in proactive guessing.

**Final output:** `FINAL-synthesis.md` contains:
- Hidden assumptions categorized
- Unconceived alternatives
- Philosophical analysis

**Time:** 10-15 minutes

---

## emotional-tribal-mapper.md

**What it does:** Map feelings, belonging, status drivers, and tribal affiliations behind beliefs. ANS quadrant analysis included.

**Skill stack:** map-elements + ans-quadrant-mapping → synthesize-apply → FINAL-synthesis

**Use when:**
- Exploring sensitive or toxic topics
- Tribal politics involved
- Emotional reasoning suspected
- Status/belonging factors matter
- Need somatic/embodied understanding
- Conflict resolution context

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your belief statement
├── 04-map-elements.md        # Emotions, tribal, Big 5, Haidt, Political Compass
├── 04b-ans-quadrants.md      # Fight/Flight/Freeze/Fawn + correlations
├── 06-synthesize.md          # Neutral synthesis + applications
└── FINAL-synthesis.md        # Complete emotional/tribal map (reads 00, 04, 04b, 06)
```

**Final output:** `FINAL-synthesis.md` contains:
- Emotional drivers
- Tribal affiliations
- ANS states
- Hormone/time perception correlations
- Non-judgmental framing

**Time:** 15-20 minutes

---

## multi-side-debate.md

**What it does:** Simulate 2-3 round structured debate with multiple perspectives. Each side steelmanned and analyzed.

**Skill stack:** steelman-enhance → multi-devils-debate → synthesize-apply → FINAL-synthesis

**Use when:**
- Preparing for actual debate
- Want to see strongest counter-arguments
- Need multiple perspective analysis
- Testing position robustness
- Understanding opposition deeply
- Collaborative exploration with others

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your position
├── 02-steelman.md            # Your strongest version
│
├── 05a-devils-advocate.md    # TURN 1: Argue FOR position (strengthen further)
├── 05b-anti-devils.md        # TURN 2: Argue AGAINST position (opposition)
├── 05c-synthesis.md          # TURN 3: Integrate both sides
├── 05-multi-devils.md        # Complete debate record
│
├── 06-synthesize.md          # Applications + integrated findings
└── FINAL-synthesis.md        # All perspectives (reads 00, 02, 05*, 06)
```

**Note:** `05*` means reads 05a, 05b, 05c, and 05-multi-devils.md

**Final output:** `FINAL-synthesis.md` contains:
- All perspectives steelmanned
- Axioms/emotions/tribal for each side
- Synthesis insights
- Debate prep notes

**Time:** 20-30 minutes

---

## prompt-digger.md

**What it does:** Analyze LLM prompts to make implicit concepts explicit. Refine instructions for better outputs.

**Skill stack:** paraphrase-engineer (prompt focus) → dig-axioms → synthesize-apply → FINAL-synthesis

**Use when:**
- Refining LLM prompts or instructions
- Debugging unexpected AI outputs
- Understanding hidden assumptions in instructions
- Improving prompt clarity
- Teaching prompt engineering
- Documenting implicit requirements

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Your original prompt
├── 01-paraphrase.md          # Variations exposing different axioms
├── 03-dig-axioms.md          # Root assumptions in prompt
├── 06-synthesize.md          # Refined prompt + expected improvements
└── FINAL-synthesis.md        # Improved prompt (reads 00, 01, 03, 06)
```

**Final output:** `FINAL-synthesis.md` contains:
- Original prompt analysis
- Implicit concepts made explicit
- Refined version
- Edge cases to handle

**Time:** 10-15 minutes

---

## self-reflection.md

**What it does:** Apply framework to its own outputs for meta-analysis. Iterate and improve previous explorations.

**Skill stack:** reflection-loop → dig-axioms → synthesize-apply → FINAL-synthesis

**Use when:**
- After completing any other command
- Want to validate findings
- Process improvement needed
- Iterating on previous map
- Teaching/learning the framework itself
- Quality assurance check

**Workflow:**
```
./tmp/axiom-<timestamp>/
├── 00-input.md               # Previous FINAL-synthesis.md (from another analysis)
├── 07-reflection.md          # Critique + refinements
├── 03-dig-axioms.md          # Axioms behind the analysis process
├── 06-synthesize.md          # Process improvements + next steps
└── FINAL-synthesis.md        # Meta-insights (reads 00, 07, 03, 06)
```

**Final output:** `FINAL-synthesis.md` contains:
- Quality assessment of previous work
- Process improvements
- Iteration suggestions
- Meta-insights

**Time:** 5-10 minutes

---

## Command Execution Template

```bash
#!/bin/bash

# Example: axiom-drill-down command

# 1. Initialize
ANALYSIS_ID="axiom-$(date +%Y%m%d-%H%M%S)"
WORKSPACE="./tmp/$ANALYSIS_ID"
mkdir -p "$WORKSPACE"

echo "Analysis ID: $ANALYSIS_ID"
echo "Workspace: $WORKSPACE"

# 2. Write input
cat > "$WORKSPACE/00-input.md" <<EOF
# Input Belief

[Your belief statement here]

## Context
[Optional context]
EOF

# 3. Run skills (each skill reads previous, writes to numbered file)
echo "Running paraphrase-engineer..."
# [Skill execution writes to 01-paraphrase.md]

echo "Running dig-axioms..."
# [Skill execution reads 01-paraphrase.md, writes to 03-dig-axioms.md]

echo "Running synthesize-apply..."
# [Skill execution reads 03-dig-axioms.md, writes to 06-synthesize.md]

# 4. Final synthesis
echo "Generating final synthesis..."
# [Reads 00, 01, 03, 06 → writes FINAL-synthesis.md]

echo "Complete! View results:"
echo "  cat $WORKSPACE/FINAL-synthesis.md"
```

---

## Command Selection Guide

**I need to...**

- **Understand a complex belief completely** → full-chain (7 steps, 30-45 min)
- **Find root assumptions quickly** → axiom-drill-down (3 steps, 5-10 min)
- **Strengthen weak argument** → steelman-correlations (3 steps, 10-15 min)
- **Find blind spots** → unconceived-explorer (3 steps, 10-15 min)
- **Understand emotional/political drivers** → emotional-tribal-mapper (3 steps, 15-20 min)
- **Prepare for debate** → multi-side-debate (4 steps, 20-30 min)
- **Improve LLM prompts** → prompt-digger (4 steps, 10-15 min)
- **Validate my work** → self-reflection (4 steps, 5-10 min)

---

## Workflow Customization

### Skip Optional Steps
Edit the workflow to skip files:
```bash
# Skip multi-devils-debate
# Create: 00, 01, 02, 03, 04, 06 (skip 05)
# FINAL-synthesis adapts to available files
```

### Parallel Execution
Run independent skills in parallel:
```bash
# After dig-axioms, these don't depend on each other:
map-elements        → 04-map-elements.md &
proactive-guessing  → 04b-guessing.md &
wait  # Wait for both to complete
# Then run synthesize
```

### Resume from Checkpoint
```bash
# If interrupted, resume from last completed file
ls ./tmp/axiom-20250129-001830/
# Shows: 00, 01, 02 (stopped here)
# Continue from dig-axioms reading 02-steelman.md
```

---

## File Naming Convention

**Required files:**
- `00-input.md` - Always the starting belief/prompt
- `FINAL-synthesis.md` - Always the complete output

**Skill output files (single-turn):**
- `01-paraphrase.md` - paraphrase-engineer output
- `02-steelman.md` - steelman-enhance output
- `04-map-elements.md` - map-elements output
- `06-synthesize.md` - synthesize-apply output
- `07-reflection.md` - reflection-loop output

**Multi-turn skill files:**
- **dig-axioms (Step 3):**
  - `03a-level1.md` - Turn 1: First "why?" + proactive guessing
  - `03b-level2.md` - Turn 2: Second "why?" + proactive guessing
  - `03c-level3.md` - Turn 3: Third "why?" + proactive guessing (optional)
  - `03-dig-axioms.md` - Synthesis of all levels

- **multi-devils-debate (Step 5):**
  - `05a-devils-advocate.md` - Turn 1: Argue FOR
  - `05b-anti-devils.md` - Turn 2: Argue AGAINST
  - `05c-synthesis.md` - Turn 3: Integrate
  - `05-multi-devils.md` - Complete debate record

**Optional auxiliary files:**
- `02b-correlations.md` - correlation-grounding output (used with steelman)
- `04b-ans-quadrants.md` - ans-quadrant-mapping output (used with map-elements)

**Error files:**
- `03-dig-axioms-ERROR.md` - If skill fails, documents error and recovery steps

---

## Integration Notes

**With version control:**
```bash
# After final synthesis
git add ./output/analysis-name.md
git commit -m "Axiom exploration: [topic]

Analysis ID: $ANALYSIS_ID
Command: axiom-drill-down
Key findings: [summary]"
```

**With CI/CD:**
```yaml
# Run analysis as part of pipeline
- name: Run axiom exploration
  run: |
    ./run-axiom-command.sh full-chain "Feature solves user problem X"
    cp ./tmp/axiom-*/FINAL-synthesis.md ./docs/analysis/feature-x.md
```

**With project documentation:**
```bash
# Link from docs
ln -s ../tmp/axiom-20250129-001830/FINAL-synthesis.md \
      ./docs/decisions/remote-work-policy.md
```

---

## Troubleshooting

**If skill fails:**
1. Check `*-ERROR.md` file for details
2. Review previous step's output file
3. Manually edit and re-run from that step
4. Or skip failed step and note in synthesis

**If synthesis incomplete:**
- Check all expected files exist
- Verify file format matches standard
- Run synthesis with --verbose flag for details

**If results unsatisfactory:**
- Use `self-reflection` command to critique
- Re-run specific skills with different focus
- Combine with other commands for deeper analysis

---

**For complete operating process documentation, see `docs/operating-process.md`.**

**For individual skill contracts, see `skills/INDEX.md`.**
