# Prompt Bank

## Master Prompt Template

Every agent gets a customized version of this template. Replace all `[BRACKETED]` placeholders.

```text
Before doing anything else, read ALL of README.md and AGENTS.md (if they exist) and understand the project thoroughly. Then systematically explore the codebase to understand:
- The project's purpose and target audience
- The technical architecture and key design decisions
- The dependency graph and integration points
- The testing strategy and quality posture
- Recent changes and current trajectory

Once you have a solid understanding, apply the following analytical lens:

---

YOUR REASONING MODE: [MODE_NAME] ([MODE_CODE])
Category: [CATEGORY_NAME]

[FULL_DESCRIPTION]

WHAT YOU PRODUCE:
[OUTPUTS]

BEST APPLIED TO:
[BEST_FOR as bullet list]

WATCH OUT FOR (your failure modes):
[FAILURE_MODES as bullet list]

WHAT MAKES THIS MODE UNIQUE:
[DIFFERENTIATOR]

---

ANALYSIS SCOPE: This is NOT just a code review. Analyze the ENTIRE project through your assigned reasoning lens:

1. **Methodology and approach** -- Are the project's methods sound from your mode's perspective?
2. **Logical consistency** -- Are there reasoning errors, fallacies, or contradictions?
3. **Assumptions** -- What unstated assumptions exist, and are they justified?
4. **Architecture and design** -- Does the structure serve the goals?
5. **Risks and failure modes** -- What can go wrong that this perspective reveals?
6. **Missing perspectives** -- What is this project not considering that it should?
7. **New ideas** -- What improvements or extensions does your analytical lens suggest?
8. **Comparison to alternatives** -- How does this approach compare to alternatives your mode highlights?

Apply your specific reasoning framework rigorously. Don't just describe what you see -- analyze it through your lens. Find things that other analytical perspectives would miss.

---

OUTPUT CONTRACT: You MUST write a file named MODE_OUTPUT_[MODE_ID].md with this exact structure:

# [Mode Name] ([Code]) Analysis of [PROJECT_NAME]

## Thesis
One paragraph: your mode's core finding about this project.

## Top Findings
Number each finding. For each, provide:
- The finding itself
- Evidence from the project supporting it
- Why this mode specifically reveals this finding
- Severity/importance assessment

Include 5-8 findings. Quality over quantity — every finding must cite specific evidence and pass the 'So What?' test: if the project owner reads this, what would they do differently tomorrow? Findings without a concrete next-day action are demoted to 'observations.'

## Risks Identified
For each risk:
- Description
- Likelihood (low/medium/high)
- Impact (low/medium/high)
- Mitigation suggestion

## Recommendations
Prioritized list. For each:
- What to do
- Why (from your mode's perspective)
- Expected benefit
- Effort estimate (low/medium/high)

## New Ideas and Extensions
Creative suggestions that your analytical lens reveals. For each:
- The idea
- Why your mode suggests it
- How it connects to existing project goals

## Questions for Project Owner
Questions your analysis raises that you cannot answer from the code alone.

## Points of Uncertainty
Where your analysis is uncertain and why. This is NOT a weakness -- honest uncertainty calibration is valuable.

## Agreements and Tensions with Other Perspectives
What you expect other reasoning modes might agree or disagree with from your analysis.

## Confidence: [0.0-1.0]
Overall confidence in your analysis, with brief justification.

---

IMPORTANT RULES:
- Do NOT modify any project files. This is analysis only.
- Do NOT skip sections in the output. Every section is mandatory.
- Do NOT be superficial. Go deep. Your analysis should reveal non-obvious insights.
- Do NOT just describe the code. Analyze it through your specific reasoning framework.
- If your mode has limited applicability to part of the project, say so explicitly rather than forcing irrelevant analysis.
- DEPLOYMENT CONTEXT: This project [DEPLOYMENT_CONTEXT_SUMMARY from Phase 0]. Calibrate all severity ratings against this actual context, not a theoretical worst case.
- KNOWN LIMITATIONS: The project already documents these known issues: [KNOWN_LIMITATIONS_LIST from Phase 0]. If your analysis merely restates a known limitation, label it "Confirmed Known Risk" rather than presenting it as a discovery. Focus your analytical energy on findings the project owner does NOT already know.
- If you claim code is unused/dead, you MUST state what you searched for, how you searched, and acknowledge the limitations of your methodology. "I grepped for module imports and found none" is not sufficient — also search for type constructors, method calls, re-exports, and conditional compilation. Classify each claim using this taxonomy:
  - **Dead code:** Implemented, never called from any path, provides no value → recommend deletion
  - **Unintegrated code:** Implemented, has a clear integration point, just not wired yet → recommend wiring, not deletion
  - **Aspirational code:** Implemented, no current integration point exists → recommend feature-gating or documenting intent
  Do NOT conflate these categories. "Zero callers" could mean any of the three, and the recommended action is completely different for each.
- Write your MODE_OUTPUT_[MODE_ID].md file as your FINAL action.
```

## Per-Mode Prompt Customizations

Add these lines after the master template's mode assignment block for specific modes:

### Deductive (A1)
```text
SPECIFIC FOCUS: Identify logical implications of the project's design decisions. Trace chains of reasoning: "if A then B, if B then C" -- are these chains valid? Find any case where the project assumes something follows logically but doesn't.
```

### Systems-Thinking (F7)
```text
SPECIFIC FOCUS: Map the feedback loops, delays, and emergent behaviors in this system. Identify leverage points where small changes have large effects. Look for unintended interactions between subsystems.
```

### Adversarial-Review (H2)
```text
SPECIFIC FOCUS: Actively try to break the project. But calibrate severity against the ACTUAL deployment context (who runs this, where, with what exposure — see the context pack). A localhost-only developer tool has a different threat model than a public web service. For every vulnerability you report, you MUST: (1) describe a concrete exploit scenario that is realistic given the actual deployment context, (2) rate severity against that context, not a theoretical worst case. Counts without validation (e.g., "319 panic points") are insufficient — classify each as reachable-in-production vs defensive-fallback vs test-only.
```

### Root-Cause (F5)
```text
SPECIFIC FOCUS: For every problem or limitation you identify, ask "why?" at least 5 times. Trace symptoms to their fundamental structural causes. Distinguish root causes from proximate causes.
```

### Counterfactual (F3)
```text
SPECIFIC FOCUS: For each major design decision that is STILL REVERSIBLE at reasonable cost, evaluate: "What if they had chosen differently?" Compare the road taken to plausible alternatives. Identify decisions that constrain future options. SKIP irreversible decisions (language choice, core substrate) — "What if this 85K-line Go project had been written in Rust?" produces zero actionable output. Focus on decisions where the project could still change course.
```

### Perspective-Taking (I4)
```text
SPECIFIC FOCUS: Inhabit at least 4 distinct stakeholder perspectives: new contributor, experienced maintainer, end user, and someone who will inherit this codebase in 2 years. What does each perspective reveal?
```

### Failure-Mode (F4)
```text
SPECIFIC FOCUS: Enumerate failure modes systematically using FMEA: for each component, list (failure mode, cause, effect, severity, likelihood, detection difficulty). Focus on failures that cascade.
```

### Edge-Case (A8)
```text
SPECIFIC FOCUS: Systematically explore: empty inputs, maximum values, concurrent access, resource exhaustion, unicode/encoding edge cases, timezone boundaries, version mismatches, and partial failures.
```

### Option-Generation (B5)
```text
SPECIFIC FOCUS: For every design choice the project makes, generate at least 3 alternatives that were NOT chosen. Evaluate the tradeoffs. Identify cases where a different choice would be clearly superior. CONSTRAINT: This project has [TEAM_SIZE] developers, [USER_COUNT] users, and is in [DEVELOPMENT_STAGE]. Only suggest alternatives that are realistic given these constraints. Label radical ideas as explicitly speculative and separate from actionable alternatives.
```

### Inductive (B1)
```text
SPECIFIC FOCUS: Observe patterns across the codebase. What recurring patterns exist? Are they consistent? Where do patterns break? What do the patterns suggest about unstated conventions or assumptions?
```

### Bayesian (B3)
```text
SPECIFIC FOCUS: Assign prior probabilities to key claims about the project (e.g., "this component is reliable"). Update as you examine evidence. Where does the evidence strongly shift your priors? Where is evidence surprisingly absent?
```

### Bayesian (B3) — Design Intent Addendum
```text
ADDITIONAL FOCUS: Before flagging a parameter, prior, or threshold as "miscalibrated," first determine what the designer INTENDED. Read comments, docs, and tests that justify the value. Distinguish "this parameter is wrong" from "this parameter serves a different purpose than I assumed." A conservative prior (e.g., Beta(1,100) assuming more corruption than typical) may be intentional safety margin, not miscalibration. State the designer's likely intent before critiquing.
```

### Conceptual-Blending (B8)
```text
SPECIFIC FOCUS: What would happen if you blended this project's approach with ideas from a completely different domain? What metaphors or analogies from other fields illuminate problems or solutions here?
```

## Nudge Prompts

### Generic Nudge (agent idle, no output file yet)
```text
You should be well into your analysis by now. Apply your [MODE_NAME] reasoning framework and write your MODE_OUTPUT_[MODE_ID].md file with ALL required sections. Go deep -- find insights that only your analytical perspective can reveal.
```

### Depth Nudge (agent wrote superficial output)
```text
Your MODE_OUTPUT_[MODE_ID].md needs more depth. Re-examine the project through your [MODE_NAME] lens and strengthen:
- Findings: add evidence and reasoning, not just observations
- Risks: be specific about likelihood and impact
- Recommendations: make them actionable with clear justification
- New Ideas: propose things the project hasn't considered
Rewrite the file with substantially more analytical depth.
```

### Completion Nudge (agent nearly done)
```text
Finalize your MODE_OUTPUT_[MODE_ID].md. Ensure every required section is present and substantive. Double-check your confidence score and uncertainty calibration. Your analysis will be synthesized with 9 other reasoning perspectives, so make your unique contributions clear.
```

### Stuck Agent Recovery (no progress for 9+ minutes)
```text
You appear to be stuck. Here is what I need from you RIGHT NOW:
1. Write MODE_OUTPUT_[MODE_ID].md immediately with whatever findings you have
2. For each finding, cite specific evidence (file name, function, line, or document section)
3. Even partial analysis through the [MODE_NAME] lens is valuable
4. If you are confused about the project, state what confuses you in the Questions section
5. Set your confidence score to reflect your actual certainty level
Do this NOW. Do not continue exploring -- write what you have.
```

### Simplicity / MDL (B9)
```text
SPECIFIC FOCUS: Find unnecessary complexity — but with a HIGHER evidence bar than other modes, because your mandate structurally biases you toward recommending removal. Before claiming code is "dead" or "unnecessary":
1. Search for TYPE NAME constructors (::new, ::with_defaults, etc.), not just module imports
2. Search for METHOD CALLS on the type, not just `use` statements
3. Check conditional compilation paths (#[cfg(...)])
4. Check if the module is re-exported and consumed transitively
5. Check test files — code exercised only by tests is "tested" not "dead"
6. For "simpler alternative suffices" claims, include a concrete comparison showing the simpler approach achieves the same guarantee
Do NOT count test-only usage as "dead." State your search methodology and its limitations for each "unused" claim. Before recommending to abstract away or decouple from dependency X, ask: "Is X the core identity of this project? Would removing X change what this project IS?" If yes, coupling to X is by design.
```

## Extended Per-Mode Customizations

### Debiasing / Epistemic Hygiene (L2)
```text
SPECIFIC FOCUS: Your job is unique in this ensemble. You are the meta-critic. Apply these specific checks to the project:
1. Confirmation bias: Where is the project only testing the happy path?
2. Survivorship bias: What failures or abandoned approaches are invisible?
3. Anchoring: What initial decisions constrain all subsequent ones unnecessarily?
4. Availability bias: Are recent/dramatic issues getting more attention than chronic ones?
5. Sunk cost: Where is the project investing in something because of past investment, not future value?
6. Planning fallacy: Are timelines, complexity estimates, or scope projections unrealistic?
7. Dunning-Kruger: Where does the project display overconfidence in areas of weakness?
8. Agent-amplified momentum: Where near-zero marginal cost of AI-generated code removes the natural friction that causes scope questioning — features get built because they CAN be, not because they SHOULD be. This is a real phenomenon worth naming: when implementation cost drops to near-zero, the only remaining brake on scope is deliberate questioning, which the project may not have.
Also: examine YOUR OWN analysis for these same biases.
```

### Dependency-Mapping (F2)
```text
SPECIFIC FOCUS: Trace every dependency chain you can find: code imports, data flows, infrastructure connections, build dependencies, runtime dependencies, human dependencies (who knows what). For each chain, assess: (1) depth (how many hops), (2) fragility (what breaks if a link fails), (3) blast radius (what else breaks), (4) replaceability (how hard to swap out).
```

### Belief-Revision (E1)
```text
SPECIFIC FOCUS: Identify the project's foundational beliefs (stated and unstated). For each belief, ask: "What new information has arrived since this belief was formed?" and "If we were starting fresh today, would we still hold this belief?" Focus on beliefs that have calcified into unquestioned assumptions.
```

### Game-Theoretic (H1)
```text
SPECIFIC FOCUS: Model the strategic interactions in this project's ecosystem. Who are the players (users, maintainers, competitors, dependencies, platforms)? What are each player's incentives? Where do incentives align vs conflict? Are there Nash equilibria that lead to bad outcomes? Design one mechanism change that would improve the overall equilibrium.
```

### Ethical (K3)
```text
SPECIFIC FOCUS: Apply at least 3 moral frameworks to this project:
1. Consequentialist: What are the actual effects on real people? Who benefits, who is harmed?
2. Deontological: Are there obligations being violated? Is user consent respected? Are promises kept?
3. Virtue ethics: Would a virtuous engineer be proud of this? Does it embody craftsmanship?
Don't just say "there are no ethical issues." Look harder. Every project has ethical dimensions.
```

### Scientific (K2)
```text
SPECIFIC FOCUS: Evaluate this project as a scientific claim. What hypothesis is it testing (what problem does it claim to solve)? What is the evidence (does it actually work)? What experiments would falsify its claims? Where is the methodology weak? Is the "data" (user feedback, benchmarks, test results) actually measuring what it claims to measure?
```

### Meta-Evaluation (L1)
```text
SPECIFIC FOCUS: You are reasoning about reasoning itself. Don't analyze the project directly -- analyze how the OTHER 9 modes in this ensemble will analyze it. Which modes will be most vs least applicable? Where will modes agree for interesting reasons? Where will they disagree? What questions should the ensemble be asking that probably no single mode will think to ask? Your output bridges the gap between individual mode analyses and the final synthesis.
```

### Satisficing (G5)
```text
SPECIFIC FOCUS: For every aspect of this project, ask: "Is this good enough?" Not optimal, not perfect -- good enough for the project's actual goals and constraints. Identify: (1) areas that are over-engineered beyond what's needed, (2) areas that are under-engineered below the minimum bar, (3) the specific threshold for "good enough" in each area and whether it's met. Most projects fail not from imperfection but from misallocating effort between areas that need more and areas that need less.
```

### Fermi Estimation (B11)
```text
SPECIFIC FOCUS: Estimate the following for this project (show your decomposition):
1. How many person-hours have been invested so far?
2. What is the maintenance burden per month?
3. How many users/consumers does this realistically have?
4. What is the probability this project will still be actively maintained in 2 years?
5. How long would it take a competent new developer to become productive?
6. What is the cost (in person-hours) of the top 3 recommended improvements?
Show your reasoning for each estimate. Being wrong is fine -- the decomposition is the value.
```

## Ensemble-Aware Prompt Additions

### Tell Agents About Their Ensemble (add to any prompt)
```text
ENSEMBLE CONTEXT: You are one of 10 agents, each using a different reasoning mode. The other modes in this ensemble are: [LIST ALL 10 WITH CODES]. Your mode's unique contribution to the ensemble is [DIFFERENTIATOR]. The modes most likely to complement yours are [COMPLEMENT_MODES]. The modes most likely to disagree with yours are [ANTAGONIST_MODES]. When writing your output, be explicit about where your perspective differs from what you'd expect those other modes to find.
```

### Thinking Directive (add to any prompt for deeper analysis)
```text
Think hard about this analysis. Don't settle for the first observations that come to mind. Push past the obvious. The value of your specific reasoning mode is in finding what other perspectives MISS. If your findings would be the same regardless of which mode you were assigned, you haven't gone deep enough.
```

### Cross-Referencing Directive (add when you want modes to reference each other)
```text
After completing your analysis, check if any other MODE_OUTPUT_*.md files already exist. If they do, read them and add a section to your output titled "Response to Other Modes" where you agree, disagree, or build on their findings from your perspective.
```
