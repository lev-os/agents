# Brenner Operators

> Cognitive moves for extracting skills from session history.

The Brenner Method treats skill extraction as **reverse-engineering your own cognitive architecture**. These operators are the atomic moves.

---

## The Operator Algebra

| Symbol | Name | One-Line Definition |
|--------|------|---------------------|
| ◎ | Problem Selection | Decide what's worth extracting |
| ⊟ | Hypothesis Slate | Enumerate possible generalizations |
| ⊥ | Third Alternative | Both approaches could be wrong—find another |
| ∿ | Iterative Refinement | Multiple rounds improve extraction |
| † | Ruthless Kill | Abandon failing generalizations |
| ⚡ | Quickie Pilot | Test extraction on small sample first |
| ⌂ | Materialization | "What would I see if this skill were applied?" |
| ◊ | Inner Truth | The generalizable principle |

---

## Detailed Operator Cards

### ◎ Problem Selection

**Definition:** Choose which patterns are worth extracting into skills.

**When to Use:**
- Starting a mining session
- Ritual detection returns many candidates
- Limited time, need to prioritize

**How to Apply:**
1. List all candidate patterns (rituals with count ≥ 5)
2. Score by: frequency × impact × generalizability
3. Select top 3 for extraction
4. Defer rest to backlog

**Failure Modes:**
- Extracting everything (context overload)
- Only extracting easy patterns (missing high-value complex ones)
- Ignoring low-frequency high-impact patterns

**The Question:** "If I could only extract ONE skill today, which would save me the most time over the next year?"

---

### ⊟ Hypothesis Slate

**Definition:** Generate multiple candidate generalizations before committing to one.

**When to Use:**
- After collecting 5+ instances of a pattern
- When the "obvious" generalization feels too simple
- Before formalizing a skill

**How to Apply:**
1. Write 3-5 different generalizations of the same pattern
2. For each: specify trigger, action, and reason
3. Evaluate against ALL instances (not just the first few)
4. Select the one that fits best, or combine

**Example:**
```
Instances: "Fixed aria-hidden", "Added role=presentation", "Removed decorative alt"

Hypothesis 1: "Decorative elements need aria-hidden"
Hypothesis 2: "Screen reader users need semantic hints on non-content"
Hypothesis 3: "Accessibility requires marking what to skip"

Best fit: Hypothesis 2 (covers all three, generalizes further)
```

**Failure Modes:**
- Committing to first hypothesis
- Generating hypotheses that are too similar
- Not testing against counter-examples

---

### ⊥ Third Alternative

**Definition:** When two approaches both seem wrong, find a third.

**When to Use:**
- Binary choice feels forced
- Both options have serious downsides
- Debate is going in circles

**How to Apply:**
1. State the two options clearly
2. List what's WRONG with each
3. Ask: "What would a solution look like that avoids BOTH problems?"
4. Generate 2-3 third alternatives
5. Evaluate freshly

**Example:**
```
Option A: "Always use transition-all" — Wrong: performance issues
Option B: "Never use transitions" — Wrong: poor UX

Third Alternative: "Use specific transition properties for intended effects"
```

**Failure Modes:**
- Forced synthesis (combining A and B instead of finding C)
- Third alternative is just A or B renamed
- Generating alternatives without evaluating original problems

---

### ∿ Iterative Refinement

**Definition:** Multiple passes improve extraction quality.

**When to Use:**
- First draft of a skill feels incomplete
- Edge cases keep appearing
- Quality rubric score < 0.7

**How to Apply:**
1. Generate initial skill draft
2. Test on 3 NEW instances (not training data)
3. Note failures and gaps
4. Refine: add counter-examples, clarify triggers
5. Repeat until convergence (see CONVERGENCE.md)

**The APR Pattern:**
```
Round 1: Generate raw extraction
Round 2: Identify structural issues
Round 3: Add edge cases
Round 4: Polish language
Round 5: Validate on fresh data
```

**Failure Modes:**
- Stopping after one round
- Refining indefinitely (no convergence criteria)
- Only refining language, not substance

---

### † Ruthless Kill

**Definition:** Abandon generalizations that don't hold up.

**When to Use:**
- Counter-examples exceed 20% of instances
- Generalization requires too many exceptions
- Simpler rule explains the same data

**How to Apply:**
1. State the generalization explicitly
2. List all counter-examples
3. If counter-examples > 2-3, KILL the generalization
4. Return to Hypothesis Slate (⊟)
5. Document the kill for future reference

**The Test:** "If I have to say 'except when...' more than twice, the rule is wrong."

**Failure Modes:**
- Attachment to elegant but wrong rules
- Adding exceptions instead of killing
- Not documenting why the kill happened

---

### ⚡ Quickie Pilot

**Definition:** Test extraction on small sample before full investment.

**When to Use:**
- Before mining 500 sessions
- Before creating full skill with references
- When unsure if pattern is real

**How to Apply:**
1. Take 10 instances (not 50)
2. Attempt extraction in 5 minutes
3. If inner truth emerges → proceed to full extraction
4. If not → the pattern may not be generalizable

**Example:**
```
Pilot: 10 instances of "run tests before commit"
Result: Clear pattern, inner truth = "validation before publication"
Decision: Proceed to full extraction
```

**Failure Modes:**
- Piloting too long (defeats the purpose)
- Skipping pilot for "obvious" patterns (they often aren't)
- Piloting with biased sample

---

### ⌂ Materialization

**Definition:** Visualize what success looks like before executing.

**When to Use:**
- Before applying an extracted skill
- When skill description is abstract
- Validating that a skill is actionable

**How to Apply:**
1. Read the skill
2. Ask: "What would I literally see/type/output if I applied this?"
3. If answer is vague → skill needs more specificity
4. If answer is concrete → skill is actionable

**The Question:** "If I handed this skill to another agent, what would their first three actions be?"

**Example:**
```
Skill: "Use specific transition properties"
Materialization:
  - Open CSS file
  - Find `transition: all`
  - Replace with `transition: opacity 0.2s, transform 0.3s`
  - Verify in browser
```

**Failure Modes:**
- Accepting abstract descriptions as "good enough"
- Materializing ideal case only (not edge cases)
- Not testing materialization by execution

---

### ◊ Inner Truth

**Definition:** The generalizable principle behind specific instances.

**When to Use:**
- After collecting 5+ instances
- When moving from specific to general
- Finalizing a skill's core insight

**How to Apply:**
1. List all instances with full context
2. Strip project-specific details (names, paths, variables)
3. Ask: "What cognitive move generated ALL these?"
4. State as: "When [trigger], always [action] because [reason]"
5. Validate: does this hold for ALL instances?

**The Transformation:**
```
SPECIFIC                              INNER TRUTH
─────────────────────────────────────────────────
"Added handleScroll() on mount"  →  "Check initial state on mount"
"Fixed animation on first load"  →  "Check initial state on mount"
"Initialized tooltip position"   →  "Check initial state on mount"

Inner Truth: "Components that depend on DOM state must check it on mount"
```

**Failure Modes:**
- Overgeneralization (rule is too broad)
- Undergeneralization (rule is still project-specific)
- Missing the "why" (action without reason)

---

## The Brenner Loop

The operators combine into a workflow:

```
◎ SELECT problem
    │
    ▼
⚡ PILOT on small sample
    │
    ▼
⊟ ENUMERATE hypotheses ──────────────┐
    │                                 │
    ▼                                 │
◊ EXTRACT inner truth                 │
    │                                 │
    ▼                                 │
⌂ MATERIALIZE the skill               │
    │                                 │
    ▼                                 │
    Test against instances            │
    │                                 │
    ├─ Fails? ──► † KILL ─────────────┘
    │
    ▼
∿ REFINE iteratively
    │
    ▼
    Converged? ──► DONE
```

---

## Operator Combinations

| Combination | When to Use |
|-------------|-------------|
| ⚡ → ◎ | Pilot informs selection |
| ⊟ → ⊥ | When all hypotheses feel wrong |
| ◊ → † | Inner truth doesn't hold → kill |
| ∿ → ⌂ | Each refinement pass materializes |
| † → ⊟ | After kill, generate new hypotheses |

---

## Quick Reference

```
◎  "Is this worth extracting?"
⊟  "What are the possible generalizations?"
⊥  "What if both options are wrong?"
∿  "How can this be refined?"
†  "Should I abandon this approach?"
⚡  "Can I test this quickly first?"
⌂  "What would success look like?"
◊  "What's the underlying principle?"
```
