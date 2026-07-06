---
name: modes-of-reasoning-project-analysis
description: >-
  Multi-perspective project analysis via NTM reasoning-mode agent swarm.
  Use when "modes of reasoning", "multi-perspective analysis", or
  "epistemological review" of any project.
---

<!-- TOC: Philosophy | Taxonomy Axes | Arguments | Phase 0: Context | Phase 1: Mode Selection | Phase 2: Spawn | Phase 3: Dispatch | Phase 4: Monitor | Phase 5: Collect | Phase 6: Synthesize | Phase 7: Operationalize | Progress Artifact | Circuit Breakers | Lead Agent Operator Cards | Anti-Patterns | Troubleshooting | Reference Index | Related Skills -->

# Modes of Reasoning Project Analysis

> **Core idea:** Spawn 10 agents (default), each assigned a distinct reasoning mode from the 80-mode taxonomy, to analyze a project from radically different analytical lenses. Synthesize their outputs into a single comprehensive report with provenance-tracked findings, triangulated consensus, and scored contributions.

> **Scope:** Not just software bugs. This finds methodological flaws, logical fallacies, misconceptions, reasoning errors, architectural blind spots, missing perspectives, and also generates new ideas, extensions, and radical innovations.

> **You are the lead agent.** You select modes, orchestrate the swarm, monitor progress, apply early-stopping heuristics, collect outputs, triangulate consensus, resolve disagreements with explicit conflict-resolution strategies, score contributions, and compile the final report. The swarm agents do the deep analysis; you do the meta-reasoning and synthesis.

> **Philosophical foundation:** There is no single correct way to reason. "Mode of reasoning" refers to at least four overlapping concepts: inference patterns (deduction vs abduction), uncertainty representations (probability vs fuzzy membership), problem-solving methods (planning, optimization), and domain styles (scientific, legal, ethical). Real-world reasoning is inherently hybrid. The power of this skill comes from making the hybrid explicit and orchestrating diversity with discipline.

## The Seven Taxonomy Axes

These axes are the cognitive backbone of mode selection. Most reasoning disagreements trace to mixing up which axis matters. Before selecting modes, identify which axes are load-bearing for THIS project:

| Axis | Pole 1 | Pole 2 | Selection Impact |
|------|--------|--------|-----------------|
| **Ampliative vs Non-ampliative** | Conclusions go beyond premises (induction, abduction) | Conclusions contained in premises (deduction) | Discovery needs ampliative; assurance needs non-ampliative |
| **Monotonic vs Non-monotonic** | Adding info never retracts conclusions | Adding info can retract conclusions | Most real reasoning is non-monotonic; pure math is monotonic |
| **Uncertainty vs Vagueness** | Uncertainty about crisp facts (probability) | Vagueness in predicates themselves (fuzzy) | Don't treat "tall" as a probability problem |
| **Descriptive vs Normative** | What *is* (facts, causes) | What *ought* (values, duties) | Decisions fail when values hide in "facts" |
| **Belief vs Action** | What to believe/accept | What to do/choose | Separating belief from decision improves accountability |
| **Single-agent vs Multi-agent** | Uncertainty as noise | Others respond strategically | Security, markets, governance need multi-agent modes |
| **Truth vs Adoption** | Accuracy/validity | Audience/coordination | Org failures are often rhetorical, not logical |

**Rule:** Your 10 modes MUST span at least 3 axes. If all modes sit on the same side of every axis, you have an echo chamber. See [TAXONOMY_AXES.md](references/TAXONOMY_AXES.md) for full axis analysis.

## Arguments

Parse from invocation text. Defaults:

| Argument | Default | Description |
|----------|---------|-------------|
| `--agents=N` | 10 | Number of agents (max 10, each gets one mode) |
| `--cc=N` | 5 | Claude Code agents |
| `--cod=N` | 5 | Codex agents |
| `--gmi=N` | 0 | Gemini agents (optional, for 3-model triangulation) |
| `--project=PATH` | cwd | Target project to analyze |
| `--focus=TOPIC` | (none) | Optional focus area to bias mode selection |
| `--depth=LEVEL` | deep | Analysis depth: quick (15min), deep (45min), exhaustive (90min+) |
| `--creative` | false | Bias mode selection toward innovation/ideation |
| `--adversarial` | false | Bias mode selection toward attack/critique |
| `--concise` | false | Compact 7-section report (skip appendices, scoreboard, mode perf notes) |
| `--output=PATH` | `MODES_OF_REASONING_REPORT_AND_ANALYSIS_OF_PROJECT.md` | Report filename |

## Phase 0: Context Pack Generation

Before selecting modes, build a rich understanding of the project. This prevents thin-context failures where agents analyze superficially because they lack project understanding.

### Project Profiling

```bash
# 1. Read ALL project docs
cat README.md AGENTS.md CLAUDE.md CONTRIBUTING.md 2>/dev/null
# 2. Language and framework detection
find . -type f \( -name '*.go' -o -name '*.py' -o -name '*.ts' -o -name '*.rs' -o -name '*.java' \) | head -80
# 3. Structure analysis
find . -type d -not -path './.git/*' -not -path './node_modules/*' | head -40
# 4. Recent trajectory
git log --oneline -30
git diff --stat HEAD~10..HEAD 2>/dev/null
# 5. Open issues / beads if available
br ready --json 2>/dev/null || true
# 6. Test posture
find . -name '*_test.*' -o -name '*.test.*' -o -name 'test_*' | wc -l
```

### Thin Context Detection

If ANY of these are true, ask the user for more context before proceeding:
- No README or it's < 100 words
- No clear entry point identified
- Project purpose is ambiguous after reading docs
- You cannot identify the primary programming language
- The focus area is specified but you don't understand what it means in this project

### Deployment Context (MANDATORY)

Before any analysis, capture the project's real-world deployment context. All severity ratings in the report MUST reference this context, not a hypothetical worst case.

Record:
- **Who runs this?** Solo developer, small team, large org?
- **Where does it run?** Localhost-only, internal network, public-facing internet?
- **Who are the users?** Just the developer, a small team, thousands of end-users, zero users (pre-release)?
- **What is the threat model?** What attackers are realistic? What's the actual attack surface?
- **Development stage:** Early prototype, active development, production, maintenance mode?

> **Why this matters:** A finding that is CRITICAL for a public-facing web service may be LOW for a localhost developer tool. A recommendation that makes sense for a 10-person team is absurd for a solo developer in early development. Three post-mortems showed severity inflation when deployment context was ignored — e.g., rating a localhost API as "CRITICAL" risk when the attacker would need shell access to exploit it (at which point they don't need the API).

### Known Limitations Pre-Filter

Before dispatch, extract all **documented limitations, caveats, and acknowledged risks** from:
- README.md, AGENTS.md, CLAUDE.md
- Issue trackers, CHANGELOG, TODO files
- Inline comments flagging known issues

Tag each as **"owner-acknowledged."** During synthesis (Phase 6), findings that merely restate owner-acknowledged limitations MUST be categorized separately as "Confirmed Known Risks" rather than presented as discoveries. This prevents the report from spending 30% of its length telling the developer what they already wrote.

### Project Identity Check

Identify the project's **core substrate** — the dependency or concept that defines what the project IS, not just what it uses:

> **Identity test:** "Would removing X change what this project IS?" If yes, coupling to X is a feature, not a bug.

Examples:
- A "Named Tmux Manager" — tmux is the identity, not an incidental dependency
- A "Rust filesystem" — Rust is the identity
- A "React dashboard" — React is a tool choice, not the identity (usually)

Record the core substrate. In Phase 6, any recommendation to "abstract away" or "decouple from" the core substrate MUST be filtered through this identity check. The skill has a documented history of recommending abstraction of the core substrate — this is always wrong.

### Project Values and Rules

Read the project's stated values and rules (from AGENTS.md, CLAUDE.md, README). Record them. Examples:
- "No tech debt, do it right" → modes penalizing complexity should have their severity discounted
- "No premature abstraction" → filter recommendations that add abstraction layers
- "Ship fast, iterate" → weight practical modes higher than formal ones

These values inform mode selection (Phase 1) and filter recommendations (Phase 6).

### Context Pack (record for later)

Write a mental note (or scratch file) capturing:
- **Project brief:** name, purpose, languages, frameworks, LOC estimate
- **Architecture:** key components, data flow, integration points
- **Recent trajectory:** what has been changing, what direction
- **Known concerns:** from docs, issues, or user's focus area
- **Stakeholders:** who uses this, who maintains it, who depends on it
- **Success criteria:** what "good" looks like for this project
- **Deployment context:** from above (who, where, users, threat model, stage)
- **Core substrate:** from identity check
- **Project values:** from rules extraction
- **Known limitations:** list of owner-acknowledged issues

This context pack will be embedded in every agent's prompt.

## Phase 1: Mode Selection

**This is the critical step.** You must select 10 modes that maximize analytical coverage for THIS specific project. Do not pick randomly.

### The Selection Algorithm

1. **Identify the 2-3 most important taxonomy axes** for this project (see table above)
2. **Read the full taxonomy** in [MODE_TAXONOMY.md](references/MODE_TAXONOMY.md)
3. **Check mode composition stacks** in [MODE_COMPOSITION.md](references/MODE_COMPOSITION.md) for proven combinations
4. **Select modes** ensuring:
   - At least 5 of 12 categories (A-L) represented
   - At least 3 of 7 taxonomy axes spanned
   - At least 2 modes that directly oppose each other (e.g., worst-case vs option-generation)
   - At least 1 meta-reasoning mode (L category) for calibration
   - If `--creative`: at least 3 from B (Ampliative) category
   - If `--adversarial`: at least 3 from F+H (Causal + Strategic) categories
5. **Check against project values** -- read the project's stated rules from Phase 0. If the project says "no premature abstraction," bias away from modes that tend to recommend decoupling (B9 Simplicity). If the project says "do it right, no tech debt," don't over-weight modes that penalize complexity.
6. **Record your rationale** -- which axes drove the selection, which modes were considered but excluded

### Selection Criteria

1. **Project type** -- a web app needs different modes than a compiler or a research paper
2. **Known risks** -- if the project has security concerns, include adversarial modes
3. **Focus area** -- if `--focus` is specified, bias selection toward relevant categories
4. **Diversity** -- spread across at least 5 of the 12 categories (A-L) to avoid blind spots
5. **Complementarity** -- pair modes that challenge each other (e.g., deductive + inductive, worst-case + option-generation)
6. **Axis coverage** -- ensure both poles of the most important axes are represented
7. **Model diversity** -- assign modes to different agent types (Claude/Codex/Gemini) to exploit model-level analytical differences

### Recommended Starting Distributions

**Software project (general):**
| Mode | Code | Why | Axis Coverage |
|------|------|-----|---------------|
| Systems-Thinking | F7 | See the whole architecture | Descriptive |
| Root-Cause | F5 | Find underlying problems, not symptoms | Descriptive, causal |
| Deductive | A1 | Verify logical consistency of design | Non-ampliative, monotonic |
| Inductive | B1 | Pattern-match from observed code to general flaws | Ampliative, non-monotonic |
| Adversarial-Review | H2 | Stress-test assumptions | Multi-agent, action |
| Failure-Mode | F4 | What can go wrong, will go wrong | Action, uncertainty |
| Edge-Case | A8 | Boundary conditions and corner cases | Non-ampliative |
| Perspective-Taking | I4 | See it from users, maintainers, attackers | Multi-agent, adoption |
| Counterfactual | F3 | What if key decisions were made differently? | Ampliative, belief |
| Debiasing | L2 | Catch cognitive biases in the other 9 modes | Meta-reasoning |

**Research/methodology project:**
Replace Edge-Case and Failure-Mode with Bayesian (B3) and Ambiguity-Detection (D2).

**Creative/product project:**
Replace Root-Cause and Adversarial with Conceptual-Blending (B8) and Analogical (B6).

**Incident/postmortem:**
Abduction (B5) + Causal-Inference (F1) + Root-Cause (F5) + Diagnostic (G11) + Counterfactual (F3) + Satisficing (G5) + Second-Order-Effects (F6) + Belief-Revision (E1) + Calibration (L2) + Adversarial (H2)

**Strategy/planning:**
Reference-Class (B10) + Game-Theoretic (H1) + Decision-Analysis (G1) + Robust/Worst-Case (L3) + Negotiation (H3) + Scenario-Simulation (F7) + Sensemaking (I5) + Fermi (B11) + Multi-Criteria (G6) + Strategic-Planning (G2)

See [MODE_COMPOSITION.md](references/MODE_COMPOSITION.md) for 12+ proven mode stacks.

After selecting, record your choices and rationale. You will need this for the report.

## Phase 2: Spawn the Swarm

```bash
ntm spawn $PROJECT \
  --cc=$NUM_CC --cod=$NUM_COD \
  --no-user \
  --stagger-mode=smart
```

Wait for agents to be ready:
```bash
ntm --robot-wait=$PROJECT --condition=idle --timeout=120
```

### Model-to-Mode Affinity

Not all modes work equally well on all models. Suggested assignments:

| Best on Claude (nuanced analysis) | Best on Codex (thorough enumeration) | Either |
|-----------------------------------|--------------------------------------|--------|
| Systems-Thinking (F7) | Edge-Case (A8) | Root-Cause (F5) |
| Counterfactual (F3) | Inductive (B1) | Deductive (A1) |
| Perspective-Taking (I4) | Failure-Mode (F4) | Adversarial (H2) |
| Debiasing (L2) | Dependency-Mapping (F2) | Option-Generation (B5) |
| Conceptual-Blending (B8) | Type-Theoretic (A7) | Bayesian (B3) |

## Phase 3: Dispatch Mode-Specific Prompts

Send each agent a **unique, mode-specific prompt**. Target agents individually by pane index. **Stagger dispatch by 15-20 seconds** to prevent thundering-herd effects:

```bash
for pane in 0 1 2 3 4 5 6 7 8 9; do
  ntm send $PROJECT --pane=$pane "$(cat <<'PROMPT'
  <INSERT MODE-SPECIFIC PROMPT FROM PROMPTS.md>
  PROMPT
  )"
  sleep 18
done
```

The prompt for each agent MUST include:
1. **Project context pack** -- the brief from Phase 0
2. **Project study directive** -- read README, AGENTS.md, understand architecture
3. **Mode assignment** -- the specific reasoning mode with full description, failure modes, and differentiator
4. **Taxonomy axis awareness** -- which axes this mode operates on
5. **Output contract** -- mandatory structured output format with provenance
6. **Scope** -- analyze the ENTIRE project, not just code
7. **Thinking directive** -- "Think hard about this. Apply your framework rigorously."

See [PROMPTS.md](references/PROMPTS.md) for the full prompt template and per-mode customization.

### The Mode Assignment Block (include in every prompt)

```text
YOUR REASONING MODE: [Mode Name] ([Code])
Category: [Category]
Taxonomy Axes: [Which axes this mode operates on]

[Full mode description from taxonomy]

WHAT YOU PRODUCE:
[Mode-specific outputs]

BEST APPLIED TO:
[List of best-for scenarios]

WATCH OUT FOR (your failure modes):
[List of failure modes for this reasoning approach]

WHAT MAKES THIS MODE UNIQUE:
[Differentiator]

COMPLEMENTARY MODES IN THIS ENSEMBLE:
[List of other modes in this run and how they relate to yours]
```

### The Output Contract (include in every prompt)

Every agent MUST produce a file named `MODE_OUTPUT_[MODE_ID].md` containing:

```markdown
# [Mode Name] ([Code]) Analysis

## Thesis
One-paragraph summary of this mode's core finding about the project.

## Top Findings
1. [Finding with evidence and reasoning]
2. ...
(5-8 findings. Every one must cite specific evidence.)

Each finding MUST include:
- §F[N]: Finding ID for cross-referencing (e.g., §F1, §F2)
- Evidence: specific file, function, line, or document reference
- Reasoning chain: how this mode specifically reveals this
- Severity: critical / high / medium / low (calibrated against deployment context, not theoretical worst case)
- Confidence: 0.0-1.0 for this specific finding
- So What?: "If the project owner reads this, what specifically would they do differently tomorrow?" (findings without a concrete next-day action are demoted to "observations")

5-8 findings. Quality over quantity. Every finding must cite specific evidence.

## Risks Identified
- [Risk with severity and likelihood assessment]

## Recommendations
- [Actionable recommendation with justification]
- Priority: P0-P4 (same scale as beads)
- Effort: low / medium / high
- Expected benefit description

## New Ideas and Extensions
- [Proposed improvement or extension with rationale]
- Innovation score: incremental / significant / radical

## Assumptions Ledger
- [Unstated assumption this analysis depends on]
- [Assumption the PROJECT makes that this mode questions]

## Questions for Project Owner
- [Question that this analytical lens raises]

## Points of Uncertainty
- [Where this mode's analysis is uncertain and why]

## Agreements and Tensions with Other Perspectives
- [What you expect other modes might agree/disagree with]

## Confidence: [0.0-1.0]
Calibration note: [brief justification -- what would change your confidence?]
```

## Phase 4: Monitor the Swarm

### Monitoring Cron (fires every 3 minutes)

Set up immediately after dispatch:

```
CronCreate(
  cron: "*/3 * * * *",
  recurring: true,
  prompt: "Check the modes-of-reasoning swarm for $PROJECT. Run these commands:
    1. ntm --robot-is-working=$PROJECT
    2. ntm --robot-tail=$PROJECT --lines=80
    3. ls -la MODE_OUTPUT_*.md 2>/dev/null

  For each agent, determine:
  (a) Working / idle / stuck / rate-limited?
  (b) Has it produced its MODE_OUTPUT_*.md file?
  (c) If output exists, is it substantive or superficial?

  ACTIONS:
  - If agent idle + no output: send nudge with mode-specific reminder
  - If agent idle + output exists: agent is done, note completion
  - If agent stuck (same output for 2+ checks): send depth nudge
  - If output superficial (< 3 findings, no evidence): send depth nudge
  - If all agents done or hard timeout reached: cancel this cron and report

  QUALITY ASSESSMENT on each check:
  - Read what agents are actually producing, not just status
  - Are findings citing specific evidence (files, lines, docs)?
  - Is the mode's unique lens visible in the analysis?
  - Flag any agent that is describing the mode instead of applying it

  EARLY STOPPING HEURISTIC:
  - If 8+ agents have produced substantive output and remaining agents show no progress for 2 consecutive checks, proceed to collection.

  Report concisely: N done, N working, N stuck, quality observations."
)
```

Save the cron job ID for later cancellation.

### Nudge Prompts for Stuck Agents

**Generic nudge (idle, no output):**
```bash
ntm send $PROJECT --pane=$N "You are analyzing this project through the lens of [MODE_NAME]. Go deeper. Don't just describe what you see -- apply your specific analytical framework to find things other perspectives would miss. Write your findings to MODE_OUTPUT_[MODE_ID].md with all required sections."
```

**Depth nudge (superficial output):**
```bash
ntm send $PROJECT --pane=$N "Your MODE_OUTPUT_[MODE_ID].md needs more depth. Each finding must cite specific evidence (file paths, function names, line numbers, document sections). Your analysis should reveal insights that ONLY the [MODE_NAME] lens can see. Rewrite with substantially more analytical depth and at least 8 findings."
```

**Completion nudge (nearly done):**
```bash
ntm send $PROJECT --pane=$N "Finalize MODE_OUTPUT_[MODE_ID].md. Ensure: (1) every finding has a §F[N] ID and evidence, (2) the Assumptions Ledger is filled in, (3) your confidence is calibrated honestly, (4) the 'Agreements and Tensions' section predicts where other modes will agree/disagree with you."
```

### Early Stopping Heuristics

Borrowed from NTM's ensemble pipeline:
- **Velocity tracking:** If an agent's findings-per-minute drops below 0.5 for 6+ minutes, it's hitting diminishing returns
- **Similarity detection:** If a new finding duplicates an existing one (same file, same issue), the mode is saturated
- **Output completeness:** If all mandatory sections are filled and confidence is calibrated, the agent is done
- Don't wait for perfection -- 8/10 substantive outputs is enough to proceed

## Phase 5: Collect and Score Outputs

Once agents have produced output (or after timeout):

1. **Cancel the monitoring cron:** `CronDelete(id: $JOB_ID)`

2. **Capture final pane state:**
   ```bash
   ntm --robot-tail=$PROJECT --lines=200
   ```

3. **Collect all output files:**
   ```bash
   ls -la MODE_OUTPUT_*.md
   ```

4. **Read every output file completely.** Do not skim. You need deep understanding for synthesis.

5. **Score each mode's contribution** using these metrics:
   - **Findings count:** total findings produced
   - **Unique findings:** findings no other mode produced
   - **Evidence quality:** proportion of findings with specific file/line references
   - **Calibration quality:** does the confidence score match the evidence quality?
   - **Mode fidelity:** is the mode's unique analytical lens visible in the output?

6. **Compute contribution scores** (from NTM's ensemble scoring):
   ```
   score = 0.40 * (findings_produced / total_findings)
         + 0.30 * (unique_insights / total_unique)
         + 0.20 * (evidence_quality_rating)
         + 0.10 * (calibration_quality_rating)
   ```

7. **Build a provenance chain** for each finding:
   ```
   §F[N] → discovered by [Mode] → deduplicated with [§F[M]] → cited in [report section]
   ```

## Phase 5.5: Ground Truth Verification

**Before synthesis, spot-check the top 3-5 highest-impact findings.** This phase prevents the single most common failure mode observed across three real-world deployments: agents making claims (especially "zero callers," "dead code," "unused module") that turn out to be wrong because grep-based verification missed indirect call paths.

For each candidate high-impact finding:
1. **Identify the specific evidence claim** (e.g., "zero callers for SpectralHealthMonitor")
2. **Run an independent verification using a different methodology** than the agent used:
   - If the agent grepped for module imports → search for type names, constructor calls (::new), method calls
   - If the agent did static analysis → run tests (`cargo test`, `npm test`, etc.) to verify dynamic behavior
   - If the agent checked file sizes → read the actual code to understand what it does
   - If the agent claimed "unused" → check for conditional compilation, re-exports, trait-mediated indirection, test-only usage
3. **If verification fails, downgrade to HYPOTHESIS** regardless of how many modes agreed on it

> **Why this phase exists:** In one deployment, 4 modes agreed code was "dead" (30-40K lines). Actual dead code was ~15-18K. The agents all used the same methodology (grep for `use` statements) and missed integration through indirect paths. The "convergence" was methodological monoculture, not independent confirmation. In another deployment, modules marked "zero callers" were actively wired into the scheduler governor. This phase would have caught both failures.

### Dynamic Analysis Requirement

For software projects, **at least one verification step in Phase 5.5 must involve running the code** — not just reading it. Execute `cargo test`, `npm test`, `go test`, or equivalent. Claims about runtime behavior, performance, or "reachability" that are based purely on static analysis have a documented false-positive rate of ~40% in complex codebases.

## Phase 6: Synthesize the Report

This is the most important phase. You are now the synthesis agent. Read [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) for the full template and [SYNTHESIS_METHODOLOGY.md](references/SYNTHESIS_METHODOLOGY.md) for the triangulation process.

### The Triangulation Protocol

Adapted from operationalizing-expertise methodology:

1. **3+ modes agree on a finding via DIFFERENT evidence → KERNEL (high confidence).** Independent discovery via different analytical frameworks AND different evidence pathways is the strongest signal. If all modes cited the same file sizes or import counts, that is ONE observation seen by many — not independent triangulation. KERNEL requires at least 2 distinct evidence methodologies.

2. **2 modes agree → SUPPORTED.** Include with note on limited cross-validation.

3. **1 mode only → HYPOTHESIS.** Present as unique insight. Valuable if evidence is strong.

4. **Modes actively disagree → DISPUTED.** Document both positions with full reasoning chains. Apply conflict resolution (see below).

### Conflict Resolution Strategies

When modes disagree, diagnose WHY before resolving:

| Diagnosis | Example | Resolution Strategy |
|-----------|---------|---------------------|
| Different evidence examined | One read code, another read docs | Both may be right in their domain -- combine |
| Different values prioritized | Security vs usability tradeoff | Present as genuine tradeoff, do not pick winner |
| Different assumptions | Current scale vs 10x growth | Present conditionally: "If X, then A; if Y, then B" |
| Analytical error | Mode misread the code | Identify error, discount that finding, note in Mode Performance |
| Genuine contradiction | "This is secure" vs "This is exploitable" | Investigate deeper yourself; one is wrong |
| Different axes | Descriptive vs normative | Both are correct; they're answering different questions |

### Explanation Layer

For every conclusion in the report, record:
- **Source modes:** which modes contributed
- **Source findings:** specific §F[N] references
- **Confidence basis:** why this confidence level
- **Supporting evidence:** what backs it up
- **Counter-evidence:** what pushes against it
- **Conflict resolution method:** if modes disagreed, how was it resolved (consensus / majority / weighted / adversarial / deferred)

### The Final Report

Write `MODES_OF_REASONING_REPORT_AND_ANALYSIS_OF_PROJECT.md` (or custom `--output` path).

The report MUST contain these sections (see [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md)):

1. **Executive Summary** -- 1 page max, 3-5 key takeaways
2. **Methodology** -- which 10 modes were selected, which axes drove selection, rationale
3. **Taxonomy Axis Analysis** -- which axes matter most for this project and what the swarm revealed about each
4. **Convergent Findings (Kernel)** -- 3+ mode agreement, highest confidence, with provenance
5. **Supported Findings** -- 2-mode agreement
6. **Divergent Findings** -- points of disagreement with full reasoning chains for each position
7. **Unique Insights by Mode** -- per-mode findings no other mode caught (the value of diversity)
8. **Risk Assessment** -- aggregated risks with severity, likelihood, and agreement level
9. **Recommendations** -- prioritized with supporting mode count and effort estimates
10. **New Ideas and Extensions** -- innovations scored as incremental/significant/radical
11. **Assumptions Ledger** -- project assumptions surfaced across all modes
12. **Open Questions** -- unresolved questions for the project owner
13. **Confidence Matrix** -- per-finding confidence with supporting/dissenting modes
14. **Contribution Scoreboard** -- per-mode scores, diversity metric, coverage analysis
15. **Mode Performance Notes** -- which modes were most/least productive and why
16. **Mode Selection Retrospective** -- would you choose different modes with hindsight?
17. **Appendix: Individual Mode Outputs** -- full text or summary of each mode's analysis
18. **Appendix: Provenance Index** -- finding ID → source mode → report location mapping

## Phase 7: Operationalize (Optional)

If the user wants to ACT on findings rather than just read them:

1. **Create beads** for top recommendations:
   ```bash
   br create --title="[Recommendation title]" --type=task --priority=[P0-P4]
   ```

2. **Offer follow-up swarm runs:**
   - "Would you like a deeper dive on any specific finding?"
   - "Should I run a focused swarm on the disputed findings?"
   - "Want me to create an implementation plan for the top 3 recommendations?"

3. **Operationalize recurring insights** using the `operationalizing-expertise` skill:
   - Extract operator cards from findings that represent reusable analytical moves
   - Build a project-specific kernel of confirmed principles
   - Create validation gates based on the risks identified

4. **Post-implementation feedback loop** (after the top 3-5 recommendations are implemented):
   - Assess: "Did implementing this reveal any issues with the original analysis?"
   - Were any findings harder/easier than expected?
   - Did implementation uncover inaccuracies in the mode outputs? (e.g., "zero callers" claim disproved when wiring the code)
   - Which mode's findings held up best under implementation? Feed this back into mode selection for future runs.
   - Record any false-positive patterns (e.g., "don't recommend abstracting the core substrate") for the next analysis of this project.

## Progress Artifact (Crash Recovery)

Write and update `MODES_ANALYSIS_PROGRESS.md` after each phase completes:

```markdown
# Modes of Reasoning Analysis Progress

## Status: [Phase N: Description]
## Started: [timestamp]
## Project: [PROJECT]

## Phase 0: Context Pack
- [x] Project profiled
- [x] Context pack built

## Phase 1: Mode Selection
- [x] Axes identified: [list]
- [x] 10 modes selected: [list with codes]

## Phase 2: Spawn
- [x] Session: $PROJECT
- [x] Agents: N cc + M cod

## Phase 3: Dispatch
- [x] Pane 0: [mode] - dispatched
- [x] Pane 1: [mode] - dispatched
- ...

## Phase 4: Monitor
- [ ] Cron ID: $JOB_ID
- Pane 0: [mode] - [working/done/stuck]
- Pane 1: [mode] - [working/done/stuck]
- ...

## Phase 5: Collect
- [ ] All outputs collected
- [ ] Contributions scored

## Phase 6: Synthesize
- [ ] Report written

## Recovery Notes
[If resuming after interruption, state what phase to continue from]
```

Update this after EVERY phase transition. If context compacts or session interrupts, re-read this file to resume.

## Circuit Breakers

Stop and reassess if ANY of these trigger:

| Breaker | Threshold | Action |
|---------|-----------|--------|
| Total time | 90 minutes (exhaustive) / 45 min (deep) / 15 min (quick) | Collect whatever exists, synthesize |
| Consecutive stuck agents | 3+ agents show no progress for 9 minutes | Cancel cron, collect, synthesize with what exists |
| All agents rate-limited | 0 agents producing output | Stop immediately, synthesize with what exists |
| Repeated identical errors | Same error in 3+ agents | Diagnose root cause before continuing |
| Context approaching limit | 80% context consumed | Stop monitoring, proceed to synthesis |

## Lead Agent Operator Cards

These are YOUR cognitive moves during orchestration. Apply them deliberately.

### ⊘ Axis Scan
**When:** Phase 1, before mode selection
**Action:** Identify which 2-3 taxonomy axes matter most. If all your modes sit on one side, you have an echo chamber.
**Failure mode:** Treating all axes as equally important (they rarely are).

### ⊕ Cross-Pollinate
**When:** Phase 6, during synthesis
**Action:** Take a finding from one mode and explicitly check whether any OTHER mode's framework would predict or contradict it.
**Failure mode:** Only comparing modes that are already similar.

### ✂ Kill Thesis (Strengthened)
**When:** Phase 6, for each convergent finding
**Action:** Actively try to find a reason the convergent finding is WRONG. For code-related findings, this means mandatory counter-search: if a finding claims "zero callers" or "dead code," search for type names, constructor calls, method names, re-exports, conditional compilation, and test usage — not just module imports. For recommendations, apply the Identity Check and Senior Engineer Gut Check. If you can't kill it, confidence is justified.
**Failure mode:** Rubber-stamping convergence because multiple modes agree. Multiple modes can share the same methodology and therefore the same blind spot.

### 🏗 Identity Check
**When:** Phase 6, before any recommendation to "abstract X" or "decouple from X"
**Action:** Ask: "Would removing X change what this project IS?" If yes, coupling to X is a feature, not a bug, and the recommendation should be filtered out. A Named Tmux Manager should not abstract away tmux. A Rust filesystem should not be ported to Go. Check the core substrate recorded in Phase 0.
**Failure mode:** Treating all dependencies as incidental. The core substrate is not a dependency to abstract — it IS the product.

### 👷 Senior Engineer Gut Check
**When:** Phase 6, after synthesis draft, before finalizing
**Action:** Role-play a senior engineer who built this system and uses it daily. For each finding, ask: "Would they agree with this finding and its severity?" For each recommendation, ask: "Would they accept this, or would they immediately say 'that's not how this works'?" The tmux-abstraction recommendation, the "scope is 5x too large" claim, and the "overengineered" verdict all failed this check in real deployments.
**Failure mode:** Analyzing from the outside consultant perspective without internalizing the builder's perspective.

### 𝓛 Level Check
**When:** Phase 6, for divergent findings
**Action:** Check if disagreeing modes are operating at different levels of abstraction. Often "disagreements" are about different things.
**Failure mode:** Forcing a resolution when the modes are answering different questions.

### ⊞ Blind Spot Scan
**When:** Phase 6, after initial synthesis
**Action:** For each of the 12 categories NOT represented in your 10 modes, ask: "What would a [Category] mode have found that we missed?"
**Failure mode:** Only looking at what modes found, never at what was structurally invisible.

### ΔE Evidence Delta
**When:** Phase 5, while scoring contributions
**Action:** For each finding, assess: "If this evidence didn't exist, would the finding still hold?" Findings that survive evidence removal are structural insights.
**Failure mode:** Weighting all evidence equally regardless of independence.

See [LEAD_AGENT_PLAYBOOK.md](references/LEAD_AGENT_PLAYBOOK.md) for the full operator card set.

## Anti-Patterns

### Mode Echo Chamber
**Problem:** Selecting modes that all say the same thing (e.g., 5 formal modes).
**Fix:** Enforce diversity across at least 5 of 12 categories AND at least 3 of 7 axes.

### Shallow Mode Application
**Problem:** Agent describes the mode instead of applying it.
**Fix:** The prompt must say "apply this framework" not "describe this framework." Send depth nudge.

### Synthesis by Concatenation
**Problem:** The report just pastes outputs end-to-end without actual synthesis.
**Fix:** The triangulation protocol forces real analytical work: kernel/supported/hypothesis/disputed.

### Premature Consensus
**Problem:** Declaring agreement when modes just didn't look at the same things.
**Fix:** Distinguish "agreement" (same claim, independent evidence) from "non-contradiction" (different topics).

### Mode Cargo-Culting
**Problem:** Forcing a mode to produce findings when it genuinely has nothing relevant to say.
**Fix:** It's fine for a mode to report "this lens has limited applicability here" with reasoning.

### Frame Lock
**Problem:** The lead agent locks onto the first interesting finding and stops exploring.
**Fix:** Apply ⊞ Blind Spot Scan operator. Force yourself to consider what's missing.

### Values Laundering
**Problem:** Normative conclusions disguised as descriptive findings (the project "should" do X presented as "the project has a problem").
**Fix:** Check the descriptive/normative axis. Separate "what is true" from "what we value."

### Narrative Closure
**Problem:** Building a satisfying story that ignores disconfirming evidence.
**Fix:** For every convergent finding, apply ✂ Kill Thesis. If you can't kill it, it's real.

### Methodological Convergence (False KERNEL)
**Problem:** Multiple modes agree on a finding, but all derive their evidence from the same methodology (e.g., grepping for imports, counting LOC). Agreement reflects shared methodology, not independent confirmation. In one deployment, 4 modes all grepped for `use` statements and agreed on "30-40K dead lines" — actual dead code was ~15-18K.
**Fix:** For KERNEL findings, require at least 2 DISTINCT evidence methodologies. "4 modes all grepped and found zero callers" is one methodology used 4 times. Require at least one mode to verify through a different path (reading call sites, tracing imports, checking runtime behavior, running tests).

### Core Substrate Blindness
**Problem:** Recommending to "abstract away" the project's core identity/substrate. A Named Tmux Manager shouldn't abstract tmux. A Rust filesystem shouldn't decouple from Rust.
**Fix:** Apply 🏗 Identity Check from Phase 0. Before any decoupling recommendation, ask: "Would removing X change what this project IS?" If yes, filter the recommendation.

### Restated Known Limitations
**Problem:** Modes "discover" things the developer already documented in README.md, AGENTS.md, or issue trackers. The report spends 30% of its length telling the developer what they already wrote.
**Fix:** Extract known limitations in Phase 0. Tag findings that merely restate documented issues as "Confirmed Known Risk" rather than presenting them as discoveries. Weight novel insights higher in scoring.

### Severity Theater
**Problem:** Rating findings as CRITICAL using a worst-case threat model that doesn't match reality. A localhost-only developer tool rated as having "CRITICAL" API security when the attacker would need shell access to exploit it.
**Fix:** All severity ratings MUST reference the actual deployment context from Phase 0. Before rating above MEDIUM, state the deployment context and explain why the severity applies to THAT context.

### Unactionable Counterfactuals
**Problem:** Analyzing irreversible decisions ("What if this had been written in Rust?") that produce zero actionable output for an 85K-line Go project.
**Fix:** Constrain counterfactual mode to decisions that are still reversible at reasonable cost. Skip language choices, core substrate selection, and other decisions where the project cannot realistically change course.

### Transient State Over-Interpretation
**Problem:** Treating a snapshot observation (e.g., "build is broken on main") as evidence of systemic quality erosion, confirmation bias, or testing failure. A broken build is likely one bad commit — a transient state, not a structural property.
**Fix:** Before using a snapshot observation as evidence, ask: "Is this a transient state or a structural property?" Broken builds, temporary test failures, and in-progress refactors are transient. Code architecture, dependency patterns, and API design are structural. Don't cite transient states as evidence for structural claims.

### Analysis Theater
**Problem:** Frameworks that add rigorous-looking structure (FMEA tables with calculated RPNs, probability matrices) but reach the same conclusions that anyone would after 5 minutes of thought. The framework adds ceremony without producing substantially different conclusions from common sense.
**Fix:** For each structured analysis output, ask: "Would someone with 5 minutes and no framework reach a different conclusion?" If the answer is no, the framework added ceremony, not insight. Report the conclusion directly without the framework scaffolding. Reserve quantitative frameworks for cases where they actually change the rank ordering or surface non-obvious interactions.

### Penalizing Honest Documentation
**Problem:** Modes flag transparent self-assessment in project documentation as a red flag. E.g., a FEATURE_PARITY.md that explicitly documents its interpretation rules gets flagged as "self-referential" or "deceptive" by multiple modes — when the developer put the caveat in the same file deliberately to be transparent.
**Fix:** Cross-reference findings with project documentation. If the developer already disclosed the limitation you're flagging, that's transparency, not deception. Penalizing honesty creates perverse incentives. Classify these as "Confirmed Known Risk," not discoveries.

### Meta-Infinite Regress
**Problem:** Spending more time reasoning about reasoning than actually reasoning.
**Fix:** Circuit breakers. Meta-reasoning serves the analysis, not the reverse.

### Ritual Calibration
**Problem:** Every finding rated 0.7 confidence (lazy default).
**Fix:** Require calibration justification: "What would change this to 0.5? What would make it 0.9?"

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent ignores its mode assignment | Resend with stronger framing; put mode name in ALL CAPS in the prompt |
| Agent doesn't write output file | Send explicit: "Write MODE_OUTPUT_X.md NOW with all sections" |
| Too few agents available | Reduce to available count; prioritize diverse mode selection across axes |
| Agents editing project code | Clarify: "This is ANALYSIS ONLY. Do not modify project files." |
| Report feels superficial | Read mode outputs more carefully; apply ⊕ Cross-Pollinate operator |
| All modes agree on everything | Either the project is simple or modes weren't diverse enough on axes |
| Agent produces generic analysis | Mode assignment wasn't specific enough; resend with failure modes and differentiator emphasized |
| Synthesis takes too long | Use the quick-synthesis variant: kernel + top disagreements + recommendations only |
| Context compaction mid-analysis | Read MODES_ANALYSIS_PROGRESS.md to resume from last completed phase |
| One mode dominates the report | Check contribution scores; weight by unique insights, not raw finding count |

## Reference Index

| Topic | Reference |
|-------|-----------|
| Full 80-mode taxonomy with descriptions, failure modes, and selection heuristics | [MODE_TAXONOMY.md](references/MODE_TAXONOMY.md) |
| The 7 taxonomy axes with per-axis mode mapping and selection guidance | [TAXONOMY_AXES.md](references/TAXONOMY_AXES.md) |
| Proven mode combinations, stacks for problem types, hybrid reasoning patterns | [MODE_COMPOSITION.md](references/MODE_COMPOSITION.md) |
| Master prompt template, per-mode customizations, nudge prompts, thinking directives | [PROMPTS.md](references/PROMPTS.md) |
| Triangulation protocol, conflict resolution, contribution scoring, provenance tracking | [SYNTHESIS_METHODOLOGY.md](references/SYNTHESIS_METHODOLOGY.md) |
| Full report template with all 18 sections and synthesis guidelines | [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) |
| Lead agent operator cards, cognitive moves, decision framework for orchestration | [LEAD_AGENT_PLAYBOOK.md](references/LEAD_AGENT_PLAYBOOK.md) |
| Swarm configuration, monitoring protocol, quality assessment, non-software projects | [OPERATIONS.md](references/OPERATIONS.md) |
| Using modes for radical innovation, creative ideation, and conceptual breakthroughs | [CREATIVE_APPLICATIONS.md](references/CREATIVE_APPLICATIONS.md) |

## NTM Installation

If NTM is not available on the current machine, install it before proceeding:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ntm/main/install.sh?$(date +%s)" | bash -s -- --easy-mode
```

NTM is required for this skill. Do not attempt to run it without NTM.

## Related Skills

- `ntm` for NTM command reference
- `vibing-with-ntm` for swarm orchestration patterns
- `code-review-gemini-swarm-with-ntm` for similar swarm-based review
- `operationalizing-expertise` for distilling findings into reusable artifacts
- `multi-model-triangulation` for cross-validating with different AI models
- `codebase-audit` for domain-parameterized auditing
- `alien-artifact-coding` for formal guarantees and mathematical optimization
