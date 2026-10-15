# Concept Decomposition Engine

The generative process behind 100+ production visualizations. This is not "which pattern to use" — it's **how to think about turning any abstract concept into a visualization that teaches**.

---

## The 5-Step Decomposition

Every great visualization in the corpus was produced (consciously or not) by this process:

```
1. DECOMPOSE the concept into structural elements
   ↓
2. MAP each element to a visual primitive
   ↓
3. IDENTIFY the teaching variable (the one thing that must be viscerally obvious)
   ↓
4. ENGINEER the aha moment (the interaction that makes comprehension click)
   ↓
5. VALIDATE the design (does a non-expert learn the concept in 30 seconds?)
```

---

## Step 1: Decompose the Concept

Every abstract concept, no matter how complex, is composed of these structural elements:

| Element | Question | Examples |
|---------|----------|----------|
| **Entities** | What are the "things"? | Transactions, pages, nodes, writers, packets, keys |
| **Relationships** | How do entities connect? | Dependencies, data flow, containment, ordering |
| **States** | What conditions can entities be in? | Active, committed, leaked, healthy, corrupted |
| **Transitions** | How do entities change state? | Cancel signal, commit, timeout, conflict detection |
| **Dimensions** | What axes of variation exist? | Time, space, quantity, probability, nesting depth |
| **Invariants** | What must always be true? | No two in critical section, total order preserved |
| **Failure modes** | What goes wrong? | Deadlock, resource leak, data corruption, conflict |

### Decomposition Examples from Production

**MVCC Isolation (frankensqlite):**
| Element | Decomposition |
|---------|--------------|
| Entities | Transactions (writers), pages (data units) |
| Relationships | Writers target pages (read-set, write-set) |
| States | Queued, writing, committed, conflicted |
| Transitions | Start → write → commit/conflict |
| Dimensions | Time (horizontal), concurrency (vertical lanes) |
| Invariants | Snapshot isolation: reads see consistent snapshot |
| Failure modes | Write-write conflict on overlapping pages |

**CMA-ES Optimization (personal site):**
| Element | Decomposition |
|---------|--------------|
| Entities | Samples (candidate solutions), distribution (search area) |
| Relationships | Samples drawn from distribution, fitnesses rank samples |
| States | Candidate, elite (top-ranked), rejected |
| Transitions | Sample → evaluate → rank → update distribution |
| Dimensions | 2D/3D parameter space, generation (time) |
| Invariants | Distribution converges toward optimum |
| Failure modes | Premature convergence, divergence |

**Lamport's Bakery Algorithm (personal site):**
| Element | Decomposition |
|---------|--------------|
| Entities | Processes (A, B), tickets (priority numbers) |
| Relationships | Ticket ordering determines access priority |
| States | Idle, choosing, waiting, critical section |
| Transitions | Idle → choosing → waiting → critical → idle |
| Dimensions | Time (step sequence), exclusivity (only one in critical) |
| Invariants | Mutual exclusion: never two in critical simultaneously |
| Failure modes | Starvation, deadlock (prevented by algorithm) |

**Cancel Protocol (asupersync):**
| Element | Decomposition |
|---------|--------------|
| Entities | Task, resources, cancel signal, budget |
| Relationships | Task holds resources, cancel signal drains budget |
| States | Running, cancel-requested, draining, finalizing, completed |
| Transitions | cancel signal → drain → finalize → release |
| Dimensions | Time (state progression), budget (decreasing quantity) |
| Invariants | Resources always released before completion |
| Failure modes | Resource leak (what Tokio does without this) |

### How to Decompose a New Concept

Ask these questions in order:

1. **"What are the nouns?"** → Entities
2. **"How do the nouns relate to each other?"** → Relationships
3. **"What adjectives describe the nouns?"** → States
4. **"What verbs change the adjectives?"** → Transitions
5. **"What numbers vary?"** → Dimensions
6. **"What rules are never broken?"** → Invariants
7. **"What happens when rules ARE broken?"** → Failure modes

---

## Step 2: Map to Visual Primitives

Each structural element has a natural visual representation. This mapping is the bridge from abstract concept to concrete visualization.

### The Mapping Table

| Structural Element | Visual Primitive | Implementation |
|-------------------|-----------------|----------------|
| **Entities** | Nodes / shapes | SVG circles, rectangles, icons |
| **Relationships** | Edges / connections | SVG paths (Bezier curves), arrows, lines |
| **States** | Colors + labels | Semantic color palette (emerald/red/amber/cyan) |
| **Transitions** | Animations | Framer Motion animate + AnimatePresence |
| **Time dimension** | Stepper / timeline | Prev/Next/Play controls, horizontal axis |
| **Space dimension** | Spatial layout | Grid, circle, tree, swim lanes |
| **Quantity dimension** | Size / opacity / bar | Scale transforms, fill width, number counters |
| **Probability dimension** | Sliders + real-time output | Range inputs driving simulation parameters |
| **Invariants** | Persistent visual constraints | Elements that NEVER change color/position |
| **Failure modes** | Dramatic contrast | Red flash, shake animation, "leaked" label |

### Primitive Selection by Concept Type

**Algorithms (Bakery, CMA-ES, encryption):**
```
Entities     → State machine nodes (SVG circles at fixed positions)
States       → Color fills (semantic palette)
Transitions  → Animated edge traversal + node color change
Time         → Stepper (Prev/Next/Play)
Invariants   → Active state always has glow filter
```

**Concurrent Systems (MVCC, WAL, schedulers):**
```
Entities     → Swim lane rows (one per actor)
States       → Color-coded blocks within lanes
Transitions  → Blocks move horizontally (time progression)
Quantity     → Sliders (writer count, conflict probability)
Failure      → Red blocks + "conflict" label
```

**Data Structures (B-tree, version chain, ECS):**
```
Entities     → Tree nodes at computed positions
Relationships → SVG path connections (parent → child)
States       → Fill color + border style (solid vs dashed for COW shadows)
Transitions  → Animated path highlight showing traversal
Time         → Stepper for insert/update/delete operations
```

**Protocols (Cancel, Obligation, two-phase):**
```
Entities     → State machine nodes in horizontal sequence
States       → Active state glow + semantic color
Transitions  → Arrow animation between states + transition labels
Time         → Stepper or auto-play
Failure      → Red end-state with error animation (flash, shake)
```

**Comparisons (Tokio vs Asupersync, B-tree vs ECS):**
```
Layout       → Side-by-side grid (red left, green right)
Entities     → Identical structure in both panels
States       → Divergent colors showing different outcomes
Time         → Shared stepper controlling both panels simultaneously
Failure      → Left panel shows the problem; right panel shows the solution
```

### When Multiple Mappings Compete

Sometimes an element could map to multiple primitives. Choose by asking:

1. **Which mapping serves the teaching variable?** (Always wins)
2. **Which mapping is simpler?** (Prefer fewer moving parts)
3. **Which mapping works on mobile?** (If one requires hover, deprioritize it)

---

## Step 3: Identify the Teaching Variable

The **teaching variable** is the ONE thing the visualization must make viscerally obvious. It is the concept's essential truth distilled to a single visual relationship.

### How to Find It

Ask: **"If the viewer remembers only ONE thing, what should it be?"**

| Concept | Teaching Variable | Why This One |
|---------|-------------------|-------------|
| MVCC isolation | Write overlap causes conflict | The OVERLAP is what they need to see |
| CMA-ES | Distribution narrows toward optimum | The CONVERGENCE is the algorithm's essence |
| Bakery algorithm | Only one process in critical section at a time | MUTUAL EXCLUSION is the whole point |
| Cancel protocol | Resources are released before completion | GRACEFUL CLEANUP is the value proposition |
| RaptorQ healing | Redundancy enables recovery from loss | AUTOMATIC REPAIR is the insight |
| Encryption pipeline | Plaintext becomes indistinguishable noise | RANDOMIZATION is what encryption does |
| Tokio comparison | Tokio leaks; Asupersync doesn't | The CONTRAST is the argument |
| CALM theorem | Monotone = fast; non-monotone = blocked | FLOW vs BLOCKAGE is the visual metaphor |

### Rules for Teaching Variables

1. **There can be only one.** If you have two, you need two visualizations.
2. **It must be visual.** If you can't point to it on screen, it's not a teaching variable.
3. **It must change.** Static truth is for text. The teaching variable must be something the user watches happen.
4. **It must surprise.** If the result is obvious before interacting, the visualization adds nothing.

---

## Step 4: Engineer the Aha Moment

The **aha moment** is the specific interaction that makes the teaching variable click. It's the moment the viewer goes from "I see shapes moving" to "OH, THAT'S why it works."

### The Five Aha Patterns

#### Pattern A: Parameter Manipulation → Visible Consequence
**User adjusts a parameter, system behavior visibly changes.**

Best for: Understanding how inputs affect outputs.

```
User adjusts slider → System responds in real-time → Consequence is visible

MVCC Race: Writer count slider (1→8) + conflict probability slider (0→100%)
  → Throughput visibly drops as conflicts increase
  → Aha: "More writers with overlapping targets = more conflicts"

CMA-ES: Play button runs generations
  → Distribution visibly narrows and moves toward optimum
  → Aha: "The algorithm literally evolves toward the answer"
```

**Implementation recipe:**
```tsx
// Slider controls param → ref avoids re-render → RAF reads ref → display updates
const paramRef = useRef(initialValue);
<input type="range" onChange={e => paramRef.current = Number(e.target.value)} />
// RAF loop reads paramRef.current and updates simulation
```

#### Pattern B: State Progression → Dramatic Transition
**User steps through phases, one step creates dramatic visual change.**

Best for: Understanding processes and protocols.

```
User clicks Next through mundane steps → Dramatic step arrives → Contrast is stark

Encryption Pipeline: Steps 1-4 are setup (key, nonce, AAD)
  → Step 5: Grid colors RANDOMIZE (plaintext → ciphertext)
  → Aha: "THAT's what encryption actually does to data"

Cancel Protocol: Running → CancelRequested → Draining (budget bar shrinking)
  → Budget hits zero → Finalizing → Completed (all green)
  → Aha: "It waits for cleanup instead of just dropping everything"
```

**Implementation recipe:**
```tsx
// Build tension through mundane steps, then deliver dramatic step
const steps = [
  { visual: "subtle", description: "Setup..." },
  { visual: "subtle", description: "Preparing..." },
  { visual: "DRAMATIC", description: "THE KEY TRANSFORMATION" },  // ← Aha
  { visual: "resolution", description: "Complete" },
];
```

#### Pattern C: Side-by-Side Divergence
**Two approaches start identical, then one fails while the other succeeds.**

Best for: Arguing "why X is better than Y."

```
Both panels start the same → Trigger event → Panels diverge → Contrast is visceral

Tokio vs Asupersync:
  Step 1: Both running (both blue)
  Step 2: Cancel signal (both yellow)
  Step 3: Tokio drops instantly (RED/leaked) | Asupersync drains (orange/draining)
  Step 4: Tokio done with leaks (red) | Asupersync done cleanly (green)
  → Aha: "Same situation, completely different outcomes"
```

**Implementation recipe:**
```tsx
// Shared step counter, divergent renderers
<ComparativeView
  leftRenderer={(step) => <TokioBehavior step={step} />}   // Goes red at step 3
  rightRenderer={(step) => <AsyncBehavior step={step} />}   // Goes green at step 4
/>
```

#### Pattern D: Failure Revelation
**System works fine, then user triggers a failure, and the consequence is dramatic.**

Best for: Understanding why guardrails exist.

```
Happy path shown first → User triggers failure → Consequence is visually alarming

Obligation Flow: Happy path (green flow) → Abort path (orange, handled)
  → Leak path: Permit LEAKED → compile error flash overlay!
  → Aha: "The type system PREVENTS this from compiling"

Conflict Ladder: Non-conflicting writes (green) → Commuting writes (yellow)
  → True conflict (RED, retry animation, performance impact visible)
  → Aha: "THIS is what the conflict resolution protects against"
```

**Implementation recipe:**
```tsx
// Tabs or stepper showing increasingly problematic scenarios
const scenarios = [
  { name: "Happy Path", outcome: "success", color: "emerald" },
  { name: "Edge Case", outcome: "warning", color: "amber" },
  { name: "Failure", outcome: "error", color: "red" },  // ← Most educational
];
```

#### Pattern E: Spatial Discovery
**User explores a network and discovers hidden connections or structure.**

Best for: Understanding ecosystems, dependencies, architectures.

```
Network appears as a collection of nodes → User hovers/clicks a node
  → Connected nodes illuminate, others fade → Structure emerges

Flywheel: Hover "Claude Code" → MCP Agent Mail, NTM, Beads all highlight
  → Lightning arcs show active connections
  → Aha: "These tools aren't isolated — they form an interconnected system"
```

**Implementation recipe:**
```tsx
// Compute connected set on hover, apply opacity to all nodes
const connectedIds = useMemo(() => {
  const set = new Set([hoveredId]);
  edges.forEach(e => {
    if (e.from === hoveredId) set.add(e.to);
    if (e.to === hoveredId) set.add(e.from);
  });
  return set;
}, [hoveredId, edges]);
```

---

## Step 5: Validate the Design

Before writing code, validate the complete design against these criteria:

### The 30-Second Test

Imagine a smart non-expert seeing this visualization for the first time:

1. **In 5 seconds:** Do they understand what they're looking at? (Layout + labels must be clear)
2. **In 15 seconds:** Do they understand how to interact? (Controls must be obvious)
3. **In 30 seconds:** Do they understand the teaching variable? (The aha moment must be reachable)

If any answer is "no," simplify.

### The Removal Test

For each visual element, ask: "If I remove this, does the teaching variable become less clear?"

- **Yes** → Keep it. It serves the concept.
- **No** → Remove it. It's decoration.

This test eliminates decorative particles, unnecessary glow effects, and animations that don't serve comprehension.

### The Static Test

Set `prefers-reduced-motion: reduce` and look at the visualization:

- **Still meaningful?** → Good. The static state shows the answer.
- **Meaningless?** → Bad. You've hidden the content behind animation.

### The Mobile Test

View the visualization on a 375px-wide screen:

- **Touch targets ≥ 44px?**
- **No hover-dependent content?**
- **Bottom sheet instead of side panel?**
- **Reduced quality tier engaged?**

---

## Complete Worked Example: Designing a New Visualization

**Task:** "Visualize how a Write-Ahead Log ensures durability."

### Step 1: Decompose

| Element | Decomposition |
|---------|--------------|
| Entities | Transactions, WAL file, database pages, checkpoint |
| Relationships | Transactions write to WAL first, then pages |
| States | Transaction: pending → WAL-written → page-written → checkpointed |
| Transitions | Write → fsync WAL → apply to page → checkpoint |
| Dimensions | Time (left to right), order (top to bottom for multiple txns) |
| Invariants | WAL always written BEFORE page modification |
| Failure modes | Crash between WAL write and page write → WAL replays on recovery |

### Step 2: Map to Visual Primitives

```
Transactions     → Colored blocks (one color per transaction)
WAL file         → Horizontal strip at top (append-only, blocks accumulate left to right)
Database pages   → Grid of cells below WAL
Checkpoint       → Animated sweep from WAL entries to page cells
Crash            → Red lightning bolt icon + screen flash
Recovery         → WAL entries replay (animate from WAL strip to page grid)
```

### Step 3: Identify Teaching Variable

**"WAL is written BEFORE the page, so crashes can always be recovered."**

The ORDERING (WAL first, page second) is the teaching variable. The visualization must make this temporal ordering viscerally obvious.

### Step 4: Engineer Aha Moment

**Pattern B (State Progression) + Pattern D (Failure Revelation):**

```
Step 1: Transaction writes to WAL (block appears in WAL strip)
Step 2: WAL fsynced (checkmark on WAL block)
Step 3: Page updated (block appears in page grid)
Step 4: All good — transaction complete (green)

Step 5: NEW TRANSACTION starts, writes to WAL
Step 6: WAL fsynced
Step 7: ⚡ CRASH ⚡ (before page update!)
Step 8: System restarts — WAL entries detected
Step 9: WAL replays → page updated from WAL
Step 10: No data lost! (green, all consistent)

Aha: "The data was in the WAL the whole time. The crash didn't matter."
```

### Step 5: Validate

- **30-second test:** Labels say "WAL" and "Pages." Stepper shows sequence. User sees crash and recovery. Teaching variable (WAL-first ordering) is visible by step 2.
- **Removal test:** WAL strip = essential. Page grid = essential. Crash animation = essential (it's the drama). Glow effects on blocks = removable.
- **Static test:** Final state shows WAL entries with checkmarks and pages filled. Meaningful without animation.
- **Mobile test:** Vertical layout (WAL on top, pages below). Stepper controls at bottom. 44px touch targets.

### Resulting Component Architecture

```tsx
interface WALVisualizationProps {
  // No props needed — self-contained with internal stepper
}

// State: { step: 0-10, crashed: boolean }
// Visual: SVG with WAL strip (top) + Page grid (bottom)
// Controls: Stepper with 10 steps + auto-play
// Aha: Step 7 (crash) → Step 9 (replay) → Step 10 (no data lost)
```

---

## Quick Decomposition Template

Copy this and fill it out before writing any visualization code:

```markdown
## Visualization Design Brief

**Concept:** [One sentence]
**Teaching variable:** [The ONE thing the viewer must understand]
**Aha moment pattern:** [A: Parameter | B: Progression | C: Side-by-Side | D: Failure | E: Spatial]

### Decomposition
| Element | Values |
|---------|--------|
| Entities | |
| Relationships | |
| States | |
| Transitions | |
| Dimensions | |
| Invariants | |
| Failure modes | |

### Visual Mapping
| Element | Visual Primitive | Implementation |
|---------|-----------------|----------------|
| | | |

### Aha Moment Engineering
- **Setup steps:** [What builds to the aha]
- **The aha step:** [The specific interaction/reveal]
- **Resolution:** [What the viewer sees after understanding]

### Validation
- [ ] 30-second test: Non-expert can understand in 30 seconds
- [ ] Removal test: Every element serves the teaching variable
- [ ] Static test: Meaningful with prefers-reduced-motion
- [ ] Mobile test: Works on 375px with touch
```

---

## Decomposition Cheat Sheet

For rapid decomposition of common concept categories:

### Algorithms
```
Entities     = data structures + operations
States       = before/during/after each operation
Transitions  = algorithm steps
Dimensions   = iteration count (time), data size (space)
Invariant    = correctness property
Failure      = incorrect input, worst case
Aha pattern  = B (step through) or A (adjust input, watch behavior)
```

### Protocols
```
Entities     = actors + messages + resources
States       = phase of each actor
Transitions  = message send/receive events
Dimensions   = time (sequence), actors (parallel)
Invariant    = safety property (mutual exclusion, no deadlock)
Failure      = what happens WITHOUT the protocol
Aha pattern  = C (with protocol vs without) or D (trigger failure)
```

### Data Structures
```
Entities     = nodes + edges + data
States       = node contents, tree shape
Transitions  = insert, delete, update, rebalance
Dimensions   = depth, breadth, version
Invariant    = structural property (balanced, ordered, etc.)
Failure      = degenerate case, overflow
Aha pattern  = B (step through operation) or A (insert data, watch restructure)
```

### Comparisons
```
Entities     = two approaches, same problem
States       = running, encountering scenario, outcome
Transitions  = shared trigger event
Dimensions   = time (synchronized progression)
Invariant    = same input, different output
Failure      = the "bad" approach's failure IS the teaching
Aha pattern  = C (side-by-side divergence, always)
```

### Distributed Systems
```
Entities     = nodes + network + messages
States       = node: leader/follower/candidate, message: in-flight/delivered/lost
Transitions  = timeout, election, partition, recovery
Dimensions   = time, network topology, failure probability
Invariant    = consistency/availability guarantee
Failure      = partition, split brain, stale read
Aha pattern  = A (adjust failure rate, watch consensus degrade) or D (trigger partition)
```
