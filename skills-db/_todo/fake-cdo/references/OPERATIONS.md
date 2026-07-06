# Operations Guide

## Swarm Configuration

### Default Mix: 5 Claude Code + 5 Codex

This mix exploits model diversity -- different LLMs have different analytical strengths:
- Claude Code (Opus): stronger at systems-level reasoning, nuanced analysis, calibrated uncertainty
- Codex (GPT): stronger at pattern matching, code-level detail, enumerative thoroughness

### Assigning Modes to Agent Types

Not all modes work equally well on all agent types. Suggested affinities:

| Mode Category | Better on Claude | Better on Codex | Either |
|--------------|-----------------|-----------------|--------|
| A: Formal | A1, A3 | A7, A8 | A2, A4-A6 |
| B: Ampliative | B3, B8 | B1, B2 | B5-B7, B9-B11 |
| F: Causal | F3, F7 | F2, F4 | F1, F5, F6 |
| G: Practical | G1, G2 | G4, G9 | G3, G5-G8, G10-G11 |
| H: Strategic | H2 | -- | H1, H3, H4 |
| I: Dialectical | I4, I5 | -- | I1-I3 |
| L: Meta | L1, L2 | -- | L3-L6 |

These are suggestions, not rules. Any capable LLM can apply any mode.

### Small Swarm Variant (5 agents)

When resources are limited, select 5 modes that maximize coverage:
1. Systems-Thinking (F7) -- holistic view
2. Adversarial-Review (H2) -- stress testing
3. Root-Cause (F5) -- deep diagnosis
4. Perspective-Taking (I4) -- stakeholder views
5. Option-Generation (B5) -- alternatives

### Large Swarm Variant (10 agents with Gemini)

If Gemini agents are also available:
```bash
ntm spawn $PROJECT --cc=4 --cod=3 --gmi=3 --no-user --stagger-mode=smart
```

Assign Gemini agents modes that benefit from large context: F7, F2, B1 (pattern-heavy, codebase-spanning).

## Monitoring Protocol

### Monitoring Cron Behavior

The cron fires every 3 minutes. On each fire:

1. **Check working state:**
   ```bash
   ntm --robot-is-working=$PROJECT
   ```

2. **Read recent output for each agent:**
   ```bash
   ntm --robot-tail=$PROJECT --lines=60
   ```

3. **Check for output files:**
   ```bash
   ls -la MODE_OUTPUT_*.md 2>/dev/null
   ```

4. **Decision matrix:**

   | Agent State | Output File Exists | Action |
   |------------|-------------------|--------|
   | Working | No | Let it continue |
   | Working | Yes | Let it finish (may be revising) |
   | Idle | No | Send nudge prompt |
   | Idle | Yes | Agent is done for this mode |
   | Stuck/error | No | Send stronger nudge or reassign |
   | Rate-limited | Any | Note in status, do not nudge |

5. **Report to user** concisely: N agents working, N done, N stuck, key observations.

### Timeout Handling

Default timeouts per agent:
- **Soft timeout (15 min):** Send a nudge asking the agent to wrap up
- **Hard timeout (25 min):** Accept whatever output exists and move on
- **Total session timeout (45 min):** Collect all outputs and proceed to synthesis

If an agent never produces output:
1. Note in Mode Performance section of report
2. Explain what that mode would have contributed
3. Proceed with N-1 mode synthesis

### Stagger Pattern

Don't send all 10 prompts simultaneously. Stagger by 15-30 seconds:
```bash
for pane in 0 1 2 3 4 5 6 7 8 9; do
  ntm send $PROJECT --pane=$pane "[prompt for mode $pane]"
  sleep 20
done
```

This prevents thundering-herd effects on shared resources.

## Quality Assessment

### What Good Mode Output Looks Like

- **Thesis is specific**, not generic ("This project has a systemic problem with X" not "There are some issues")
- **Findings cite evidence** from the actual codebase, not abstract principles
- **The mode's lens is visible** -- you can tell WHICH mode wrote this from the content
- **Uncertainty is calibrated** -- findings with strong evidence say so, uncertain ones admit it
- **New ideas are grounded** -- connected to real project needs, not random brainstorming

### What Bad Mode Output Looks Like

- Generic observations that any mode would produce
- No evidence from the actual project
- Mode description repeated instead of mode application
- Every finding rated "medium" confidence (lazy calibration)
- Recommendations that are obvious without any special analysis

### Intervention Triggers

Send a depth nudge if an agent's output shows:
- Fewer than 3 findings
- No specific file/function references
- The mode name appears more than the project's actual content
- Confidence is exactly 0.5 or 0.7 (likely default, not calibrated)
- "New Ideas" section is empty or trivial

## Synthesis Decision Framework

### When Modes Converge

- 3+ modes agree: **HIGH CONFIDENCE** -- lead with this in the report
- 2 modes agree: **MODERATE** -- include but note limited cross-validation
- 1 mode only: **HYPOTHESIS** -- present as unique insight, not established finding

### When Modes Diverge

Ask: WHY do they disagree?

| Reason | Example | Resolution |
|--------|---------|------------|
| Different evidence | One mode looked at code, another at docs | Both may be right about their domain |
| Different values | Security vs usability tradeoff | Present as genuine tradeoff, don't pick a winner |
| Different assumptions | One assumes current scale, another assumes 10x | Note the assumption and present conditionally |
| Analytical error | One mode misunderstood the code | Identify the error and discount that finding |
| Genuine contradiction | "This is secure" vs "This is exploitable" | Investigate deeper; one is wrong |

### Weighting Mode Contributions

Not all modes contribute equally to every project. Weight by:

1. **Applicability** -- was this mode a good fit for this project type?
2. **Depth** -- did the agent go deep or stay superficial?
3. **Evidence quality** -- are findings backed by specific observations?
4. **Calibration** -- does the confidence score match the evidence quality?

## Non-Software Projects

This skill works for any project, not just code. For non-software projects:

### Research Papers / Academic Work
- Focus modes: A1 (logical validity), B3 (evidence quality), K2 (methodology), I1 (argument structure), L2 (biases), D2 (ambiguity)
- Output files: agents read papers/docs instead of code
- Report emphasis: logical soundness, evidence quality, methodology critique

### Business Plans / Strategy
- Focus modes: G1 (decisions), G2 (strategy), B11 (estimation), H1 (competition), F6 (second-order effects), C1 (risk quantification)
- Agents analyze documents, spreadsheets, market data
- Report emphasis: feasibility, risk, competitive positioning

### Organizational / Process
- Focus modes: F7 (systems), I4 (perspectives), H4 (incentives), G3 (resources), L1 (meta-evaluation), K3 (ethics)
- Agents analyze process docs, org charts, communication patterns
- Report emphasis: bottlenecks, misaligned incentives, stakeholder blind spots

## Post-Analysis Actions

After the report is compiled:

1. **Save the report** to the project root (default) or specified output path
2. **Do NOT delete** MODE_OUTPUT_*.md files -- they are appendix material
3. **Offer to the user:**
   - "Would you like me to create beads for the top recommendations?"
   - "Would you like me to address any specific finding?"
   - "Would you like a deeper analysis of any disagreement?"
4. **If operationalizing:** consider using the `operationalizing-expertise` skill to turn recurring findings into reusable rules

## Early Stopping: Marginal Utility Analysis

Adapted from NTM's ensemble `EarlyStopDetector`. The key insight: agents hit diminishing returns and the lead agent should detect this rather than waiting for timeouts.

### Metrics to Track Per Agent

| Metric | How to Estimate | Threshold |
|--------|----------------|-----------|
| **Findings rate** | Count §F entries in output / minutes elapsed | < 0.5 findings/min for 6+ min → saturated |
| **Output growth** | Is the output file still growing? | No growth for 6+ min → probably done |
| **Similarity** | Are new findings duplicating earlier ones? | 3+ duplicates → definitely saturated |

### The Early Stop Decision

```
IF (8+ agents have substantive output)
  AND (remaining agents show no progress for 2 consecutive cron checks)
THEN proceed to collection

UNLESS a remaining agent is assigned a critical mode:
  - The only adversarial mode
  - The only meta-reasoning mode
  - The debiasing mode
  In which case: wait up to 10 additional minutes
```

### What "Substantive Output" Means

- At least 5 findings with evidence
- At least 3 recommendations
- Confidence is calibrated (not exactly 0.5 or 0.7)
- The mode's lens is visible (findings differ from generic code review)
- At least 1 finding cites a specific file/function/line

## Velocity Tracking

Track findings-per-minute for each agent during monitoring:

```
Agent 1 (Systems-Thinking): 2.1 findings/min → HIGH velocity
Agent 2 (Deductive):        0.8 findings/min → NORMAL velocity  
Agent 3 (Adversarial):      0.3 findings/min → LOW velocity (might be stuck)
```

Low-velocity agents get nudge prompts. Very-low-velocity agents (< 0.2 for 10+ min) may be stuck and need the recovery prompt.

Velocity data goes into the Contribution Scoreboard and Mode Performance Notes in the final report.

## Progress Artifact Protocol

The progress artifact `MODES_ANALYSIS_PROGRESS.md` serves two purposes:
1. **Crash recovery:** If context compacts or session interrupts, re-read this file to resume
2. **User visibility:** The user can check this file to see where the analysis stands

### Update Triggers
- After completing each phase (write the phase as completed)
- After each cron fire (update agent statuses)
- Before any long-running operation (record what's about to happen)
- After any error (record what went wrong and recovery plan)

### Recovery Protocol
If you're resuming after interruption:
1. Read `MODES_ANALYSIS_PROGRESS.md`
2. Determine last completed phase
3. If Phase 3-4: check which agents have produced output files, update status
4. If Phase 5+: collect whatever outputs exist and proceed
5. Never re-dispatch to agents that already produced output

## Three-Model Triangulation

When `--gmi=N` is specified (Gemini agents added), exploit model diversity for stronger triangulation:

### Why Model Diversity Matters
Different LLMs have different analytical biases:
- **Claude (Opus):** Stronger at nuanced analysis, calibrated uncertainty, philosophical reasoning
- **Codex (GPT):** Stronger at pattern matching, enumerative thoroughness, code-level detail
- **Gemini:** Stronger at large-context reasoning, cross-file pattern detection

### Cross-Model Convergence
A finding that's independently discovered by agents running on different underlying models is stronger than one discovered by agents on the same model:
- Same finding from Claude + Codex + Gemini agents → VERY high confidence (model-triangulated)
- Same finding from 3 Claude agents → High confidence but possibly shared model bias

### Recommended 3-Model Split
```bash
ntm spawn $PROJECT --cc=4 --cod=3 --gmi=3 --no-user --stagger-mode=smart
```

Assign modes by model affinity:
- Gemini (large context): Systems-Thinking, Dependency-Mapping, Inductive (benefit from seeing entire codebase at once)
- Claude (nuance): Perspective-Taking, Counterfactual, Debiasing, Conceptual-Blending
- Codex (thoroughness): Edge-Case, Failure-Mode, Type-Theoretic

## Dynamic Analysis Requirement

For software projects, at least one agent (ideally assigned an Edge-Case, Deductive, or Formal Verification mode) MUST be instructed to **run the code**, not just read it:

```text
DYNAMIC ANALYSIS DIRECTIVE: You MUST run the project's test suite (cargo test, npm test, go test, 
or equivalent) and report:
1. Whether tests pass/fail
2. What the test coverage tells you about code health
3. Any runtime behaviors that contradict static analysis assumptions

Claims about "dead code," "unreachable paths," or "unused modules" based purely on static analysis 
have a documented ~40% false-positive rate in complex codebases with conditional compilation, 
re-exports, and trait-mediated indirection.
```

Include this directive in at least one agent's prompt, or send it as an additional instruction to at least one NTM pane.

**Why this matters:** In one deployment, no agent ran `cargo test` or `cargo bench`. Claims about "9.5x expected loss" couldn't be verified because nobody ran the test that computes it. "319 panic points" included defensive fallbacks and test-only code that a single `cargo test` run would have classified correctly.

## Depth Modes

The `--depth` argument controls the analysis intensity:

### Quick (15 minutes)
- 5 agents instead of 10
- No monitoring cron (just wait for completion)
- Simplified report: Executive Summary + Top Findings + Recommendations only
- No provenance tracking
- Best for: getting a quick read on a project before deciding whether to invest in a deep analysis

### Deep (45 minutes, default)
- 10 agents with full monitoring cron
- Full report with all 18 sections
- Provenance tracking and contribution scoring
- Best for: standard project analysis

### Exhaustive (90+ minutes)
- 10 agents with extended monitoring
- Multi-round: after first synthesis, identify 2-3 gap-filling modes and spawn additional agents
- Cross-referencing directive: agents read each other's outputs and respond
- Includes second-pass validation: send key findings back to selected agents for confirmation
- Best for: pre-release audits, major architecture decisions, high-stakes projects

### Concise (--concise flag, any depth)
- Uses the compressed 7-section report template instead of the full 18-section version
- Skips: contribution scoreboard, mode performance notes, taxonomy axis analysis, full explanation layer, mode selection retrospective
- Keeps: executive summary, convergent findings (max 5), critical disagreements (max 3), security findings, top recommendations (max 5), open questions, provenance summary
- Best for: solo developers, early-stage projects, or when the full 18-section report would be disproportionate to the project size
- Can be combined with any depth (quick+concise, deep+concise, exhaustive+concise)

## Handling Non-Software Projects

### The Key Difference
For non-software projects, agents can't explore a codebase. They need the relevant materials provided IN the prompt or as accessible files.

### Setup for Document-Based Projects
1. Put all relevant documents in a single directory
2. Tell agents to read specific files rather than "explore the codebase"
3. Adjust the output contract: replace file/line references with document/section/page references

### Document-Based Prompt Addition
```text
PROJECT MATERIALS: The following documents contain the project being analyzed:
- [filename1]: [brief description]
- [filename2]: [brief description]
Read ALL of these before beginning your analysis. Your evidence citations should reference specific documents, sections, pages, or paragraphs.
```

### Research Papers / Academic Work
- Focus modes: A1 (logical validity), B3 (evidence quality), K2 (methodology), I1 (argument structure), L2 (biases), D2 (ambiguity)
- Additional modes to consider: I5 (steelmanning), E1 (belief revision), C1 (probabilistic reasoning)
- Output emphasis: logical soundness, evidence quality, methodology critique, statistical validity
- Special prompt: "Evaluate the claims made in this paper. For each claim, assess: (1) is the evidence sufficient, (2) does the reasoning chain hold, (3) what alternative explanations exist?"

### Business Plans / Strategy
- Focus modes: G1 (decisions), G2 (strategy), B11 (estimation), H1 (competition), F6 (second-order effects), C1 (risk quantification)
- Additional: B10 (reference-class forecasting), H3 (negotiation), G10 (cost-benefit)
- Output emphasis: feasibility, risk, competitive positioning, financial viability
- Special prompt: "Evaluate this business plan as if you were an investor. What would make you invest? What would make you walk away?"

### Organizational / Process
- Focus modes: F7 (systems), I4 (perspectives), H4 (incentives), G3 (resources), L1 (meta-evaluation), K3 (ethics)
- Additional: H1 (game-theoretic), I3 (rhetorical), E1 (belief revision)
- Output emphasis: bottlenecks, misaligned incentives, stakeholder blind spots, cultural assumptions
- Special prompt: "Analyze this organization/process as a system. Where are the feedback loops? Where are the delays? Where do incentives misalign?"

## NTM Installation

If NTM is not available on the current machine, install it before proceeding:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ntm/main/install.sh?$(date +%s)" | bash -s -- --easy-mode
```

NTM is required for this skill. Do not attempt to run it without NTM.
