# Think — Multi-Perspective Deliberation Reference

5 CDO roles applied sequentially for genuine perspective diversity. Portable version of the Thinking Parliament — single model, structured role-switching, no external model dispatch.

---

## Core Principle

**Single-model, multi-perspective.** A single LLM adopting distinct roles sequentially produces better analysis than unstructured "think about it." The key is *commitment to role* — each perspective must be argued with full conviction, not hedged.

> "The test of a first-rate intelligence is the ability to hold two opposing ideas in mind at the same time and still retain the ability to function."
> — F. Scott Fitzgerald

---

## The 5 Roles

### Role 1: Advocate

**Lens:** Strongest case FOR the proposed approach.
**Mindset:** Optimistic, builds on strengths, sees opportunity.

```
PROMPT PATTERN:
"You are the Advocate. Your job is to make the strongest possible case
FOR this approach. Assume good faith. Build on its strengths. Identify
the opportunities it creates. Do not hedge or qualify — argue with
full conviction.

Problem: {problem}
Proposed approach: {approach}

Deliver:
1. Top 3 reasons this is the RIGHT approach
2. Strengths it builds on (existing assets, team capability, market timing)
3. Opportunities it creates (what becomes possible if this works)
4. Confidence (0-1) in this assessment"
```

**When to emphasize:** Skin/Services layer changes (execution focus), team morale is low, exploring new directions.

---

### Role 2: Critic

**Lens:** Strongest case AGAINST the proposed approach.
**Mindset:** Pessimistic, finds flaws, stress-tests assumptions.

```
PROMPT PATTERN:
"You are the Critic. Your job is to make the strongest possible case
AGAINST this approach. Find every flaw, risk, and failure mode. Do not
be gentle — argue with full conviction that this will fail.

Problem: {problem}
Proposed approach: {approach}

Deliver:
1. Top 3 reasons this approach will FAIL
2. Hidden risks (what could go wrong that isn't obvious)
3. Assumptions being made (what must be true for this to work)
4. Confidence (0-1) in this assessment"
```

**When to emphasize:** Site/Structure layer changes (high stakes), irreversible decisions, high-confidence situations (>70% agreement triggers devil's advocate).

---

### Role 3: Systems Thinker

**Lens:** Second-order effects, emergent behavior, feedback loops.
**Mindset:** Holistic, relational, temporal.

```
PROMPT PATTERN:
"You are the Systems Thinker. Your job is to trace the ripple effects
of this approach through the entire system. What does this touch that
isn't obvious? What feedback loops does it create or disrupt? What
emerges from the interaction of components?

Problem: {problem}
Proposed approach: {approach}
System context: {known components, dependencies, stakeholders}

Deliver:
1. Second-order effects (what happens because of what happens)
2. Feedback loops (reinforcing or balancing) created or disrupted
3. Stakeholders affected beyond the obvious
4. Temporal effects (what changes over time, not just immediately)
5. Confidence (0-1) in this assessment"
```

**When to emphasize:** Site/Structure layer changes, cross-team impact, platform decisions.

---

### Role 4: Pragmatist

**Lens:** Implementation reality, constraints, execution feasibility.
**Mindset:** Practical, resource-aware, deadline-conscious.

```
PROMPT PATTERN:
"You are the Pragmatist. Your job is to assess whether this can
actually be built with the resources available. What are the real
constraints? What's the simplest version that delivers value? Where
will the team struggle?

Problem: {problem}
Proposed approach: {approach}
Constraints: {time, team, tech, budget if known}

Deliver:
1. Feasibility assessment (can this actually be built? how long?)
2. Simplification opportunities (what's the MVP version?)
3. Execution risks (where will the team get stuck?)
4. Resource requirements (what do we need that we don't have?)
5. Confidence (0-1) in this assessment"
```

**When to emphasize:** Skin/Services/Space Plan layer changes, deadline pressure, resource constraints.

---

### Role 5: Wild Card

**Lens:** Unconsidered alternatives, creative disruption, reframing.
**Mindset:** Divergent, irreverent, questioning the question itself.

```
PROMPT PATTERN:
"You are the Wild Card. Your job is to challenge the framing entirely.
What if we're solving the wrong problem? What would a completely
different approach look like? What would happen if we did nothing?
What would a 10x simpler solution look like?

Problem: {problem}
Proposed approach: {approach}

Deliver:
1. Alternative framing (is this even the right problem to solve?)
2. Radically different approach (what would {industry} do?)
3. Do-nothing scenario (what happens if we skip this entirely?)
4. 10x simplification (what if we removed 90% of the requirements?)
5. Confidence (0-1) in this assessment"
```

**When to emphasize:** Space Plan/Stuff layer changes (speed + creativity), stuck situations, groupthink detected.

---

## Sequential Application Pattern

```
STEP 1: Frame the problem clearly
  → State: problem, proposed approach, context

STEP 2: Run Advocate
  → Capture: 3 reasons FOR, strengths, opportunities, confidence

STEP 3: Run Critic
  → Capture: 3 reasons AGAINST, risks, assumptions, confidence

STEP 4: Run Systems Thinker
  → Capture: 2nd-order effects, feedback loops, temporal effects, confidence

STEP 5: Run Pragmatist
  → Capture: feasibility, MVP, execution risks, confidence

STEP 6: Run Wild Card
  → Capture: reframing, alternatives, do-nothing, 10x simpler, confidence

STEP 7: Synthesize
  → Common ground: where 3+ roles agree
  → Genuine tensions: where roles disagree (these are the real decisions)
  → Decision framework: "Choose A when X, choose B when Y"
  → Weighted confidence: average of 5 role confidences
```

---

## Devil's Advocate Trigger

When 4+ roles agree on the same direction (>70% agreement):

```
TRIGGER: Agreement too high → groupthink risk

ACTION: Re-run Critic with amplified prompt:
"OVERRIDE: Despite the apparent consensus, you MUST find at least 3
substantial reasons this approach will fail. The other 4 perspectives
all agree this is right — your job is to be the one voice of dissent.
Find the blind spot."

PURPOSE: Prevent false confidence. Consensus without dissent is
suspicious, not reassuring.
```

---

## Layer-Weighted Application

The layers classifier determines which roles get extra emphasis:

### Site / Structure Changes (High Stakes)

```
Weight distribution:
  Advocate:     15%  (reduced — we know the upside)
  Critic:       30%  ★ (amplified — find the risks)
  Systems:      30%  ★ (amplified — trace the ripples)
  Pragmatist:   15%
  Wild Card:    10%
```

### Skin / Services Changes (Execution Focus)

```
Weight distribution:
  Advocate:     25%  ★ (amplified — build momentum)
  Critic:       15%
  Systems:      10%
  Pragmatist:   35%  ★ (amplified — execution reality)
  Wild Card:    15%
```

### Space Plan Changes (Balanced)

```
Weight distribution:
  Advocate:     20%
  Critic:       20%
  Systems:      20%
  Pragmatist:   20%
  Wild Card:    20%  (equal weight — explore freely)
```

### Stuff Changes (Speed + Creativity)

```
Weight distribution:
  Advocate:     10%
  Critic:       10%
  Systems:      10%
  Pragmatist:   35%  ★ (amplified — just ship it)
  Wild Card:    35%  ★ (amplified — creative alternatives)
```

---

## Light Deliberation Mode

For high-confidence situations (≥0.80), run only Advocate + Critic:

```
STEP 1: Advocate (3 reasons FOR)
STEP 2: Critic (3 reasons AGAINST)
STEP 3: Quick synthesis (common ground + one key tension)

Total time: ~30 seconds vs ~2 minutes for full deliberation
Use when: confidence is high but you want a sanity check
```

---

## Output Format

```
## 🧠 Think: {problem title}

### Advocate
{3 key points}
Confidence: {0-1}

### Critic
{3 key points}
Confidence: {0-1}

### Systems
{3 key points}
Confidence: {0-1}

### Pragmatist
{3 key points}
Confidence: {0-1}

### Wild Card
{3 key points}
Confidence: {0-1}

### Synthesis
**Common ground:** {where roles agree}
**Genuine tensions:** {where roles disagree — these are the real decisions}
**Decision framework:** {when to choose A vs B}
**Weighted confidence:** {average}
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Hedging within a role | "The Advocate says it's good but also risky" defeats the purpose | Each role argues with FULL conviction |
| Skipping synthesis | 5 opinions without integration = noise, not insight | Always synthesize |
| Treating roles as sequential filters | Critic shouldn't veto Advocate; they coexist | All roles contribute to synthesis equally |
| Running think on trivial tasks | Deliberation on "fix typo" wastes time | Skip think when confidence ≥0.90 |
| Ignoring the Wild Card | "That's impractical" dismisses the reframing value | Wild Card challenges the frame, not the answer |

---

## Quick Reference Card

```
🧠 THINK — 5 roles, 2 minutes

1. Advocate  — Why YES
2. Critic    — Why NO
3. Systems   — What ELSE happens
4. Pragmatist — Can we ACTUALLY do it
5. Wild Card — Are we asking the WRONG question

Then: Synthesize → common ground + tensions + framework
Trigger devil's advocate if agreement > 70%
```
