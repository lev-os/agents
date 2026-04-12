# Pedagogical Design — Teaching Through Interactivity

How to design visualizations that teach effectively, not just look impressive. Principles extracted from the most pedagogically successful visualizations across all four projects.

---

## The Pedagogy Test

Before writing a single line of code, answer these questions:

1. **What concept should the reader understand after interacting?** (One sentence.)
2. **What is the "aha moment"?** (The specific interaction that makes the concept click.)
3. **Could this be taught equally well with text?** (If yes, don't build a visualization.)
4. **What would a static image miss?** (The dynamic element that requires interactivity.)

If you can't answer all four, the visualization isn't ready to build.

---

## The Pedagogical Hierarchy

Not all interactivity is equally educational. Ranked by teaching effectiveness:

### Tier 1: Direct Manipulation (Most Effective)
User changes parameters and immediately sees how the system responds.

**Examples:**
- MVCC Race: Adjust writer count and conflict probability → see throughput change in real-time
- CMA-ES: Watch optimization distribution narrow as generations progress
- Scheduler Lanes: Inject cancellation → see priority reordering immediately

**Why it works:** The user forms hypotheses ("more writers = more conflicts") and tests them instantly. This is active learning.

### Tier 2: Temporal Exploration
User controls the pace of a process unfolding through time.

**Examples:**
- Bakery Algorithm: Step through 5 phases of mutual exclusion
- Encryption Pipeline: Watch plaintext become ciphertext step by step
- Cancel Protocol: See states transition one by one

**Why it works:** The user can pause, rewind, and re-examine each step. This is impossible with text.

### Tier 3: Comparative Revelation
User sees two approaches side by side and discovers the difference.

**Examples:**
- Tokio vs Asupersync: Identical setup, divergent outcomes at cancellation
- B-tree vs ECS: Same operations, different storage behaviors
- CALM Theorem: Monotone (flowing) vs non-monotone (blocked)

**Why it works:** Juxtaposition is the fastest path to "why X is better than Y."

### Tier 4: Spatial Relationship Discovery
User explores a network or hierarchy to understand connections.

**Examples:**
- Flywheel Visualization: Hover tools to see which others they connect to
- B-tree Explorer: Click nodes to inspect cell contents and traversal paths
- Version Chain: Navigate transaction visibility across versions

**Why it works:** Spatial layout turns abstract relationships into visual adjacency.

### Tier 5: Ambient Illustration (Least Effective)
Animation that reinforces a concept without direct interaction.

**Examples:**
- Glow Orbits: Background motion suggesting dynamic system activity
- GitHub Heartbeat: Pulsing indicator showing live activity
- Spectral Background: Film grain suggesting analog/physical metaphor

**Why it works (barely):** Sets emotional tone and reinforces brand, but teaches nothing specific.

---

## Pedagogical Patterns

### Pattern 1: Progressive Complexity

Start with the simplest possible version of the concept, then layer complexity.

**Encryption Pipeline implementation:**
```
Step 1: "Here's your data" (plaintext grid, green)
Step 2: "You provide a password" (key appears)
Step 3: "We derive an encryption key" (Argon2id, key transforms)
Step 4: "We generate a nonce" (random bytes appear)
Step 5: "Encryption happens" (grid randomizes — the dramatic moment)
Step 6: "On disk, it looks like this" (ciphertext + tag + nonce layout)
Step 7: "Decryption reverses it" (grid returns to green — the payoff)
```

Each step adds exactly one new concept. The user never sees two new things simultaneously.

### Pattern 2: Cause-and-Effect Immediacy

The effect must follow the cause within 200ms. Longer delays break the pedagogical link.

**Good:** Click "Trigger Cancel" → budget bar immediately starts decreasing
**Bad:** Click "Run Simulation" → wait 3 seconds → results appear

```tsx
// GOOD: Immediate visual response
onClick={() => {
  setPhase("cancelling");  // Visual state changes instantly
  // Simulation continues in background
}}

// BAD: Delayed response
onClick={async () => {
  const result = await runSimulation();  // User waits
  setPhase(result.phase);  // Response comes too late
}}
```

### Pattern 3: Failure as Teacher

Show what goes wrong, not just what goes right. Failure states are often more educational than success states.

**Conflict Ladder (frankensqlite):**
- Scenario 1: No conflict (green) — "this is fine"
- Scenario 2: Commuting writes (yellow) — "this is tricky but safe"
- Scenario 3: True conflict (red) — "THIS is what we need to protect against"

The red scenario teaches more than the green one because it shows *why the system exists*.

**Obligation Flow (asupersync):**
- Happy path: Permit → Held → Sent (green, expected)
- Abort path: Permit → Held → Aborted (orange, handled gracefully)
- Leak path: Permit → Held → LEAKED (red, compile error flash!)

The leak path is the most educational because it shows the consequence that the type system prevents.

### Pattern 4: The Dramatic Reveal

Build tension before revealing the key insight.

**Market Cap Drop (personal site):**
```
1. Chart line draws slowly (1.8s) — building anticipation
2. Drop line appears dramatically — the event
3. "$600B" counter animates up — the magnitude hits
```

**RaptorQ Healing (frankensqlite):**
```
1. Page grid shows all green (healthy)
2. User introduces corruption (red cells appear — tension)
3. Repair symbols animate from center (healing — resolution)
4. Durability probability displays "10^-15" (the punchline)
```

### Pattern 5: Semantic Color Narrative

Colors tell a story arc across visualization steps:

```
Start:   Slate (idle, calm, neutral)
  ↓
Action:  Cyan (active, processing, engaged)
  ↓
Success: Emerald (completed, healthy, correct)
  OR
Warning: Amber (caution, draining, intermediate)
  ↓
Failure: Red (error, leaked, conflict)
  OR
Resolution: Sky (settled, final, informational)
```

Every visualization that follows this color narrative creates an unconscious sense of progression.

### Pattern 6: Annotated Transitions

Don't just animate between states — label what's happening during the transition.

**Cancel Protocol:**
```
[Running ●] --"cancel signal"--> [CancelRequested ●] --"drain timeout"--> [Draining ●]
```

The transition labels ("cancel signal", "drain timeout") teach as much as the states themselves.

**Implementation:**
```tsx
// Edge label between states
<text
  x={(fromState.x + toState.x) / 2}
  y={(fromState.y + toState.y) / 2 - 12}
  textAnchor="middle"
  className="fill-slate-400 text-[9px] font-mono"
>
  {transition.label}
</text>
```

---

## Common Pedagogical Mistakes

### Mistake 1: Animation Without Purpose
Particles floating around with no connection to content. Glow effects on everything. If you remove the animation and the content is just as clear, the animation is decoration.

**Fix:** Every animated element must map to a data point, state, or concept.

### Mistake 2: Too Many Concepts Simultaneously
Showing 8 algorithm steps at once. Displaying 20 metrics simultaneously.

**Fix:** Use the stepper pattern. One concept per step. Limit visible metrics to 3-5.

### Mistake 3: Hover-Only Explanations
Tooltips that only appear on hover, making content inaccessible on mobile.

**Fix:** Critical information is always visible. Tooltips provide supplementary detail only.

### Mistake 4: Speed Without Control
Auto-playing animations that are too fast to follow.

**Fix:** Always provide play/pause. Default to paused for complex visualizations. Let users control speed.

### Mistake 5: No Static Fallback
Visualization that is meaningless when prefers-reduced-motion is enabled.

**Fix:** The static state should convey the final/summary state of the visualization. Show the "answer" even without animation.

### Mistake 6: Fake Data
Hard-coded demo data instead of actual algorithm output.

**Fix:** Embed the real algorithm. Use actual computation. Users can tell when results are fake.

---

## Measuring Pedagogical Effectiveness

After building a visualization, test with this rubric:

| Criterion | Score | Threshold |
|-----------|-------|-----------|
| Can a non-expert explain the concept after 30 seconds of interaction? | 0-5 | >= 3 |
| Does the visualization teach something text alone cannot? | 0-5 | >= 4 |
| Is the "aha moment" reachable within 3 interactions? | 0-5 | >= 3 |
| Does it work on mobile without losing educational value? | 0-5 | >= 3 |
| Is it meaningful with reduced motion enabled? | 0-5 | >= 2 |

**Minimum passing score:** 15/25

If a visualization scores below threshold, redesign it before shipping.

---

## The Best Visualizations in the Corpus

Ranked by pedagogical effectiveness:

1. **CMA-ES (personal site)** — Real algorithm, adjustable parameters, visible evolution
2. **Conflict Ladder (frankensqlite)** — Three scenarios reveal the gradation of conflict types
3. **CALM Theorem (asupersync)** — Monotone vs non-monotone tab comparison is instantly clear
4. **Bakery Algorithm (personal site)** — Step-by-step mutual exclusion with process state colors
5. **Encryption Pipeline (frankensqlite)** — 7-step progressive reveal from plaintext to ciphertext
6. **MVCC Race (frankensqlite)** — Adjustable parameters create instant cause-and-effect
7. **Obligation Flow (asupersync)** — Three paths with compile-error flash on leak path
8. **Tokio Comparison (asupersync)** — Side-by-side makes the value proposition visceral
9. **Flywheel (personal site/all)** — Network graph reveals ecosystem interconnections
10. **B-tree Explorer (frankensqlite)** — Click-to-inspect with COW path highlighting

What they share: **real algorithms, controlled pace, dramatic contrast, semantic color.**
