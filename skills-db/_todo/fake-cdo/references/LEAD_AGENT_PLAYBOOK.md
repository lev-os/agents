# Lead Agent Playbook

> Operator cards for the lead agent's cognitive moves during orchestration. These are YOUR tools for meta-reasoning about the swarm's output.

## Operator Card Format

Each operator has:
- **Symbol + Name:** Mnemonic for quick reference
- **When:** The trigger condition
- **Action:** What to do
- **Failure mode:** How this operator breaks
- **Prompt module:** Copy-paste text for when you need to invoke this

## Phase 1 Operators (Mode Selection)

### ⊘ Axis Scan
**When:** Before selecting modes. Always the FIRST operator.
**Action:** Read the 7 taxonomy axes. Identify the 2-3 most load-bearing axes for this project. A security project's load-bearing axes are single/multi-agent and descriptive/normative. A research paper's are ampliative/non-ampliative and truth/adoption.
**Failure mode:** Treating all axes as equally important. They rarely are.
**Prompt module:**
```
Before I select modes, I need to identify which taxonomy axes matter most for this project.
The 7 axes are: ampliative/non-ampliative, monotonic/non-monotonic, uncertainty/vagueness,
descriptive/normative, belief/action, single-agent/multi-agent, truth/adoption.
For this project, the most important axes are...
```

### ◈ Antagonist Pair
**When:** After initial mode list is drafted.
**Action:** Verify at least one pair of modes that actively OPPOSE each other. If all modes are friendly, add an antagonist.
**Failure mode:** Comfort-seeking -- choosing modes that reinforce each other.
**Prompt module:**
```
I need to verify antagonistic pairs in my selection. Modes that oppose each other:
- Deductive vs Inductive (top-down vs bottom-up)
- Worst-Case vs Option-Generation (pessimism vs possibility)
- Simplicity vs Systems-Thinking (reduce vs expand)
Which pair am I including? If none, I need to swap a mode.
```

### ◇ Coverage Check
**When:** After finalizing mode selection.
**Action:** Count categories (need 5+ of 12) and axis poles covered (need 3+ of 7 axes with both poles). Identify gaps.
**Failure mode:** Checking category count but not axis balance.

## Phase 3 Operators (Dispatch)

### ⟐ Context Inject
**When:** Constructing each agent's prompt.
**Action:** Include the project context pack from Phase 0 in every prompt. Without it, agents analyze superficially.
**Failure mode:** Assuming agents will discover context on their own (they often don't explore deeply enough).

### ≋ Complementary Framing
**When:** Constructing each agent's prompt.
**Action:** Tell each agent what OTHER modes are in the ensemble and how theirs relates. "You are the adversarial reviewer. The deductive agent is checking logic; the inductive agent is finding patterns. Your job is to break what they find."
**Failure mode:** Treating each agent as isolated. They produce better output when they know their role in the ensemble.

## Phase 4 Operators (Monitoring)

### ⏱ Velocity Check
**When:** On each monitoring cron fire (every 3 minutes).
**Action:** Estimate each agent's output rate. If an agent has been working for 10+ minutes with nothing to show, send a nudge. If output file exists but hasn't grown in 6 minutes, the agent may be done or stuck.
**Failure mode:** Waiting too long for perfection. 80% output from all agents beats 100% from half.

### ⚡ Quality Pulse
**When:** On each monitoring cron fire, when output files exist.
**Action:** Quickly assess: Does the output cite specific evidence? Is the mode's analytical lens visible? Are there at least 5 findings? If not, send a depth nudge.
**Failure mode:** Checking only for file existence, not content quality.

### 🛑 Early Stop Decision
**When:** When 8+ agents have substantive output.
**Action:** Ask: "Will waiting for the remaining agents materially change the synthesis?" If no, proceed. If the missing modes are critical (e.g., the only adversarial mode), wait longer.
**Failure mode:** Stopping too early (losing a critical perspective) or too late (wasting time).

## Phase 5 Operators (Collection)

### ΔE Evidence Delta
**When:** Scoring each mode's contribution.
**Action:** For each finding, ask: "If this evidence didn't exist, would the finding still hold?" Findings that survive evidence removal are structural insights; findings that collapse are evidence-dependent observations.
**Failure mode:** Treating all findings equally regardless of evidence independence.

### ⊞ Blind Spot Scan
**When:** After collecting all outputs, before synthesis.
**Action:** For each of the 12 categories NOT represented in the 10 modes, ask: "What would a [Category] mode have found?" For each uncovered axis pole, ask: "What are we missing by not having a [pole] perspective?"
**Failure mode:** Only looking at what modes found, never at what was structurally invisible.

## Phase 6 Operators (Synthesis)

### ⊕ Cross-Pollinate
**When:** For each finding during synthesis.
**Action:** Take the finding and explicitly check: Does any OTHER mode's framework predict, explain, or contradict this? Cross-pollination reveals connections that no single mode sees.
**Failure mode:** Only comparing modes that are already similar (formal with formal, causal with causal).

### ✂ Kill Thesis
**When:** For each convergent (KERNEL) finding.
**Action:** Actively try to find a reason the finding is WRONG. What evidence would disprove it? Is there a plausible alternative explanation? If you can't kill it, confidence is justified. If you can, downgrade it.
**Failure mode:** Rubber-stamping convergence because multiple modes agree. Multiple modes can share the same blind spot.

### 𝓛 Level Check
**When:** For each divergent (DISPUTED) finding.
**Action:** Check if the disagreeing modes are operating at different levels of abstraction. A code-level finding and an architecture-level finding about the same area may look contradictory but actually be about different things.
**Failure mode:** Forcing a resolution when the modes are answering different questions. The correct resolution may be "separate" rather than "one side wins."

### ⊗ Values Surface
**When:** For any finding that contains "should," "must," "ought," "need to," "better."
**Action:** Check the descriptive/normative axis. Is this a factual observation or a value judgment? If normative, make the value explicit. "The code SHOULD be tested" contains an implicit value judgment about testing coverage.
**Failure mode:** Values laundering -- presenting normative conclusions as descriptive facts.

### ◈ Narrative Resistance
**When:** During executive summary and conclusion writing.
**Action:** Resist the urge to build a clean, satisfying narrative. Real analysis has loose ends, unresolved tensions, and honest "I don't know" answers. If the report feels too neat, something was smoothed over.
**Failure mode:** Narrative closure -- dropping disconfirming evidence because it doesn't fit the story.

### ⟳ Reflective Calibration
**When:** After writing the full report, before finalizing.
**Action:** Re-read your own synthesis and ask:
- Did I weight modes I personally find more compelling?
- Did I resolve conflicts in the direction I wanted?
- Did any mode's findings get lost in synthesis?
- Is my confidence calibrated or am I defaulting to 0.7?
- Would the project owner agree with my framing?
**Failure mode:** Skipping this step because you're tired of the analysis. This is the most important operator.

### 🏗 Identity Check
**When:** Phase 6, before any recommendation to "abstract," "decouple," or "introduce an interface for" a dependency.
**Action:** Check the core substrate recorded in Phase 0. Ask: "Would removing this dependency change what this project IS?" If yes, the coupling is intentional and the recommendation should be filtered out.
**Failure mode:** Treating the project's defining technology as an incidental dependency. A Named Tmux Manager's coupling to tmux is not technical debt.
**Prompt module:**
```
Before recommending to abstract away [DEPENDENCY], I need to check:
Is [DEPENDENCY] the core identity of this project? Would removing it change what
this project IS, or just how it's implemented? If the former, this coupling is
by design and the recommendation is wrong.
```

### 📐 Deployment Context Check
**When:** Phase 6, before rating any finding above MEDIUM severity.
**Action:** Reference the deployment context from Phase 0. State who runs this, where, with what exposure. Explain why the severity applies to THAT context, not a hypothetical worse one. A localhost tool used by one developer has a fundamentally different severity scale than a public web API.
**Failure mode:** Defaulting to worst-case threat models regardless of actual deployment context. "This localhost API has no auth" is LOW for a dev tool, not CRITICAL.

### 👷 Senior Engineer Gut Check
**When:** Phase 6, after synthesis draft, before finalizing.
**Action:** Role-play a senior engineer who built this system and uses it daily. For each finding and recommendation, ask: "Would they agree? Would they immediately say 'that's not how this works' or 'that's the whole point'?" Three real-world deployments showed that findings which fail this check (tmux abstraction, "overengineered" verdicts, scope-too-large claims) were consistently rejected by project owners.
**Failure mode:** Analyzing exclusively from the outside-consultant perspective. The skill systematically over-indexes on theoretical risks and architectural ideals while under-indexing on practical constraints, project identity, and the economics of who actually uses the tool.

### ⚔ Adversarial Verification
**When:** Phase 5.5 / Phase 6, after collecting mode outputs but before synthesis.
**Action:** For the top 3 highest-impact findings, actively try to DISPROVE them. Use a different search methodology than the original finding used. If a finding claims "zero callers," search for type names, constructors, method calls, re-exports, and conditional compilation — not just module imports. If a finding claims code is "dead," run the test suite to check if tests exercise it.
**Failure mode:** Only trying to CONFIRM findings during synthesis. Confirmation bias is the lead agent's signature trap.

### 🔄 Internal Contradiction Check
**When:** Phase 5, while reading each mode's output.
**Action:** For each mode, list all recommendations and check: do any pull in opposite directions? One deployment had a Bayesian agent simultaneously recommending "increase warmup period" (be more conservative) and "use dual-rate EMA for faster detection" (be more responsive). These are in tension and the synthesis should either resolve the contradiction or flag it explicitly.
**Failure mode:** Treating each recommendation independently without checking for internal consistency.

## Operator Composition Chains

Like reasoning modes, operators can chain:

```
Selection chain:     ⊘ Axis Scan → ◈ Antagonist Pair → ◇ Coverage Check
Quality chain:       ⏱ Velocity Check → ⚡ Quality Pulse → 🛑 Early Stop
Synthesis chain:     ⊕ Cross-Pollinate → ✂ Kill Thesis → 🏗 Identity Check → 📐 Deployment Context → 𝓛 Level Check → ⊗ Values Surface
Verification chain:  ⚔ Adversarial Verification → 🔄 Internal Contradiction Check
Finalization chain:  👷 Senior Engineer Gut Check → ◈ Narrative Resistance → ⟳ Reflective Calibration
```

The full lead-agent workflow chains all of these:
```
Phase 1: ⊘ → ◈ → ◇
Phase 3: ⟐ → ≋
Phase 4: [⏱ → ⚡ → 🛑] (repeating on each cron)
Phase 5: ΔE → ⊞
Phase 5.5: ⚔ → 🔄
Phase 6: ⊕ → ✂ → 🏗 → 📐 → 𝓛 → ⊗ → 👷 → ◈ → ⟳
```

## Decision Framework: When to Intervene

| Signal | Intervention | Operator |
|--------|-------------|----------|
| Agent idle 6+ min, no output | Send mode-specific nudge | ⏱ |
| Output exists but < 3 findings | Send depth nudge | ⚡ |
| Output describes mode, doesn't apply it | Resend with "APPLY, don't describe" | ⚡ |
| All agents done except 1-2 non-critical | Proceed to collection | 🛑 |
| Critical mode (adversarial/meta) still working | Wait up to 10 more minutes | 🛑 |
| 3+ findings look identical across modes | Deduplicate early, note in provenance | ΔE |
| No findings from a critical axis | Consider spawning 1 gap-filler agent | ⊞ |
| Report draft has no tensions | You over-smoothed -- go back to raw outputs | ◈ |
| Confidence scores don't vary | Re-calibrate each finding individually | ⟳ |
| Recommendation to abstract core substrate | Apply 🏗 Identity Check — likely a false positive | 🏗 |
| Finding rated CRITICAL for localhost tool | Apply 📐 Deployment Context Check — likely severity inflation | 📐 |
| Mode contradicts itself (recommend X and not-X) | Flag with 🔄 Internal Contradiction Check | 🔄 |
| Top finding based on grep-only evidence | Apply ⚔ Adversarial Verification with different methodology | ⚔ |
