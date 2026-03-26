# Convergence Detection

> Skills improve through iterations like numerical optimizers converging to steady state.

---

## The Core Insight

Skill extraction is iterative refinement. The question isn't "is this done?" but "is this converging?"

**Convergence = changes getting smaller + output stabilizing**

---

## The Four Phases

| Phase | Rounds | Character | What Happens |
|-------|--------|-----------|--------------|
| **Major Fixes** | 1-3 | Wild swings | Fundamental changes, structure shifts |
| **Architecture** | 4-7 | Settling | Interface improvements, boundary clarification |
| **Refinement** | 8-12 | Tuning | Edge cases, nuanced handling |
| **Polishing** | 13+ | Converging | Minor wording, format adjustments |

### Phase Indicators

**Major Fixes (Rounds 1-3):**
- Core insight changes completely
- Triggers rewritten from scratch
- Counter-examples invalidate previous version
- Sections added or removed

**Architecture (Rounds 4-7):**
- Core insight stable, expression improves
- Triggers refined but not replaced
- New counter-examples fit existing structure
- Section order may change

**Refinement (Rounds 8-12):**
- Only edge cases addressed
- Language clarified
- Examples improved
- No structural changes

**Polishing (Rounds 13+):**
- Changes are cosmetic
- Synonym swaps
- Formatting adjustments
- Ready to finalize

---

## Convergence Signals

| Signal | Weight | How to Measure |
|--------|--------|----------------|
| **Output Size Trend** | 35% | Are responses getting shorter? |
| **Change Velocity** | 35% | Is rate of change slowing? |
| **Content Similarity** | 30% | Are successive rounds more similar? |

### Measuring Output Size Trend

```
Round 1: 450 tokens
Round 2: 380 tokens
Round 3: 320 tokens
Round 4: 310 tokens
Round 5: 305 tokens

Trend: Decreasing → Good signal
```

**Why this matters:** Large outputs indicate uncertainty. As understanding improves, explanations become more concise.

### Measuring Change Velocity

```
Round 1 → 2: 15 significant changes
Round 2 → 3: 8 significant changes
Round 3 → 4: 4 significant changes
Round 4 → 5: 2 significant changes

Trend: Decelerating → Good signal
```

**Significant changes:**
- Core insight modified
- Trigger added/removed
- Counter-example added
- Section restructured

**Not significant:**
- Wording adjustments
- Format changes
- Example tweaks

### Measuring Content Similarity

```python
# Simplified similarity check
def similarity_score(round_n, round_n_plus_1):
    # Compare section by section
    sections = ['insight', 'triggers', 'pitfalls', 'workflow']
    matches = sum(1 for s in sections if similar(round_n[s], round_n_plus_1[s]))
    return matches / len(sections)

# Score >= 0.75 = high similarity
```

---

## The Convergence Score

```
convergence_score = (
    0.35 * output_size_trend +    # Are outputs shrinking?
    0.35 * velocity_decay +        # Are changes slowing?
    0.30 * content_similarity      # Are versions similar?
)

if convergence_score >= 0.75:
    print("Ready to finalize")
else:
    print("Continue refining")
```

### Interpreting the Score

| Score | Interpretation | Action |
|-------|----------------|--------|
| < 0.50 | Still major changes | Continue iterating |
| 0.50-0.74 | Approaching convergence | 2-3 more rounds |
| ≥ 0.75 | High confidence | Ready to finalize |
| ≥ 0.90 | Diminishing returns | Stop, you're polishing |

---

## Early Termination Signals

Sometimes convergence is blocked. Recognize these patterns:

| Signal | Meaning | Action |
|--------|---------|--------|
| **Oscillation** | Alternating between two versions | Apply Third Alternative (⊥) |
| **Expansion** | Output growing each round | Step back, reframe the problem |
| **Plateau at low score** | Stuck but not improving | Kill and restart (†) |
| **Counter-example cascade** | Each fix creates new problems | Overgeneralized; narrow scope |

### Oscillation Example

```
Round 3: "Always validate before save"
Round 4: "Validate only on user input"
Round 5: "Always validate before save"
Round 6: "Validate only on user input"

Diagnosis: Two valid patterns conflated
Solution: Split into two separate skills
```

---

## Practical Convergence Check

After each refinement round, ask:

1. **Did the core insight change?**
   - Yes → Major Fixes phase, continue
   - No → Check other signals

2. **Did triggers change?**
   - Added new trigger → Architecture phase
   - Removed trigger → Check if overgeneralized
   - Refined wording only → Refinement phase

3. **Did counter-examples change?**
   - New counter-examples found → Not converged
   - Only refined existing → Approaching convergence

4. **Is this version similar to last version?**
   - >75% similar → Ready to finalize
   - <75% similar → Continue refining

---

## The Guided Iterative Mode

For extended extraction sessions:

```
┌─────────────────────────────────────────────────────────────────┐
│  ITERATE UNTIL STEADY STATE                                     │
├─────────────────────────────────────────────────────────────────┤
│  1. Extract batch of patterns from sessions                     │
│  2. Cluster similar patterns                                    │
│  3. Generate candidate generalizations                          │
│  4. Validate against quality rubric                             │
│  5. If patterns_changed < threshold: DONE                       │
│  6. Else: refine and iterate                                    │
│                                                                 │
│  Checkpoint at:                                                 │
│  - Major pattern additions                                      │
│  - Quality threshold hit                                        │
│  - User-defined intervals (e.g., every 30m)                     │
└─────────────────────────────────────────────────────────────────┘
```

### Checkpoint Protocol

At each checkpoint:

1. **Save current state** — Version the skill draft
2. **Calculate convergence score** — Is progress being made?
3. **Decision point:**
   - Score improving → Continue
   - Score plateaued → Consider termination
   - Score declining → Step back, diagnose

---

## Convergence vs. Quality

**Convergence ≠ Quality**

A skill can converge on a BAD solution. Always check:

1. Does the converged skill pass the quality rubric? (See SKILL.md)
2. Does it work on NEW instances (not training data)?
3. Do counter-examples actually fail, or are they edge cases?

**The test:** Apply the converged skill to a fresh problem. If it fails, you converged too early—the training data was biased.

---

## Quick Reference

```
Phases:
  1-3   Major Fixes   → Expect big changes
  4-7   Architecture  → Expect interface changes
  8-12  Refinement    → Expect edge cases
  13+   Polishing     → Ready to stop

Signals:
  Output shrinking?      → Good
  Changes slowing?       → Good
  Versions similar?      → Good
  Score >= 0.75?         → Finalize

Red Flags:
  Oscillating           → Split the pattern
  Expanding             → Reframe the problem
  Stuck at low score    → Kill and restart
```
