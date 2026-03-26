# The Golden Thread — 12 Invariant Truths of Interactive Visualization

These principles are distilled from 100+ production visualizations across four projects. They are not suggestions. They are the patterns that separate visualizations people actually learn from versus those they scroll past.

---

## 1. Pedagogy Drives Design, Not Aesthetics

**The principle:** Every animation, interaction, and color choice must serve comprehension. Ask "what does the user understand after interacting that they didn't before?" If the answer is "nothing, but it looks cool," delete it.

**How the best visualizations do it:**

- **CMA-ES (personal site)**: Embeds a real optimization algorithm. Users see actual sample evolution, not canned animation. The particle colors encode elite vs. candidate selection — teaching the algorithm's core mechanism through color alone.

- **Conflict Ladder (frankensqlite)**: Three scenarios with identical visual structure but different outcomes (green/yellow/red). The concept of "what makes a write conflict" becomes viscerally obvious through comparison.

- **CALM Theorem (asupersync)**: Monotone operations show flowing green arrows; non-monotone shows red lock barriers. The visual metaphor of "flow vs. blockage" teaches the theorem faster than any text explanation.

**Anti-pattern:** Particle systems that exist purely for visual flair with no semantic meaning. If particles don't represent data points, signals, or state, they're decoration.

---

## 2. Progressive Disclosure Over Information Dump

**The principle:** Complex concepts must be revealed gradually. Never show everything at once. Use steppers, scroll triggers, and phased animations to build understanding layer by layer.

**Proven patterns:**

- **Stepper controller**: Used in 30+ visualizations. Prev/Next/Play buttons let users control the pace of revelation. Auto-play with speed control (5x to 50x) for different learning speeds.

- **Scroll-triggered whileInView**: Elements animate into existence as user scrolls, creating a reading-pace-aligned reveal. Used in Timeline, Stats Grid, Market Cap Drop.

- **Phase-based state machines**: Cancel Protocol shows 5 states one at a time. Each state builds on the previous, creating a narrative arc.

**Code pattern (Stepper with AnimatePresence):**
```tsx
<AnimatePresence mode="wait">
  <motion.div
    key={currentStep}
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: -20 }}
    transition={{ type: "spring", stiffness: 300, damping: 25 }}
  >
    {steps[currentStep].content}
  </motion.div>
</AnimatePresence>
```

---

## 3. Device-Aware Quality Tiers

**The principle:** Don't just make layouts responsive. Scale computational complexity per device class. A phone with 2 cores and 2GB RAM should not attempt 5000 particles.

**Three-tier system (from Three Scene):**

| Tier | Particle Multiplier | Shadows | Post-Processing | Detection |
|------|-------------------|---------|-----------------|-----------|
| Low | 0.2x (1000 max) | Off | Off | Mobile OR cores<=2 OR memory<=2GB |
| Medium | 0.5x (2500 max) | On | Off | Default |
| High | 1.0x (5000 max) | On | On | cores>=8 AND memory>=8GB |

**Detection code:**
```tsx
function detectQualityTier(): "low" | "medium" | "high" {
  const isMobile = /Android|iPhone|iPad/.test(navigator.userAgent);
  const cores = navigator.hardwareConcurrency ?? 4;
  const memory = (navigator as any).deviceMemory ?? 4;
  if (isMobile || cores <= 2 || memory <= 2) return "low";
  if (cores >= 8 && memory >= 8) return "high";
  return "medium";
}
```

---

## 4. Dual Interaction Models

**The principle:** Desktop and mobile are fundamentally different input paradigms. Never compromise one for the other. Build separate interaction paths.

| Interaction | Desktop | Mobile |
|------------|---------|--------|
| Exploration | Hover for preview | Tap to select |
| Detail view | Side panel / tooltip | Bottom sheet modal |
| Dismiss | Mouse leave / Escape | 900ms auto-dismiss / swipe |
| Feedback | Cursor change / glow | Haptic vibration |
| Parallax | Mouse position tracking | Disabled or gyroscope |
| Navigation | Keyboard arrows | Swipe gestures |

**Detection (from Flywheel Visualization):**
```tsx
const hasFinePointer = window.matchMedia(
  "(hover: hover) and (pointer: fine)"
).matches;

if (hasFinePointer) {
  // Desktop: hover HUD tooltip
  setHoveredNode(nodeId);
} else {
  // Mobile: tap to activate, auto-dismiss after 900ms
  setHoveredNode(nodeId);
  setTimeout(() => setHoveredNode(null), 900);
}
```

---

## 5. Spring Physics Over Linear Interpolation

**The principle:** All motion in the physical world follows spring dynamics (inertia, overshoot, settling). Linear/eased motion feels artificial. Spring-tune every transition.

**Battle-tested configurations:**

```tsx
// Natural motion for UI transitions
{ type: "spring", stiffness: 200, damping: 25 }

// Snappy for buttons and toggles
{ type: "spring", stiffness: 400, damping: 35 }

// Gentle float for backgrounds
{ type: "spring", stiffness: 100, damping: 20 }

// Quick tracking for cursors
{ type: "spring", stiffness: 300, damping: 20 }

// Magnetic attraction (low mass for responsiveness)
{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }
```

**Tuning guide:**
- **Stiffness**: Higher = faster response (100-400 range)
- **Damping**: Higher = less oscillation (15-35 range)
- **Mass**: Lower = more responsive (0.1-1.0 range)
- **Test visually**: No config is right until it "feels" right

---

## 6. SVG for Structure, Canvas/WebGL for Particles

**The principle:** Choose rendering technology based on visualization type, not familiarity.

| Visualization Type | Technology | Why |
|-------------------|-----------|-----|
| Node graphs, trees, state machines | SVG | DOM events, accessibility, CSS styling |
| Flowcharts, diagrams | SVG | Text rendering, arrow markers, responsiveness |
| Particle systems (>100 particles) | Canvas / WebGL | GPU acceleration, no DOM overhead |
| 3D space, terrain | Three.js / R3F | Perspective, lighting, shaders |
| Simple animations (<20 elements) | Framer Motion divs | Simplest solution wins |

**Anti-patterns:**
- Using Canvas for a 10-node diagram (SVG is simpler and accessible)
- Using SVG for 5000 particles (DOM will choke)
- Using Three.js for a 2D flowchart (massive overkill)

---

## 7. Lazy Initialization Is Mandatory

**The principle:** Heavy visualizations must not initialize until approaching the viewport. This isn't optimization — it's required for usable page load.

**The pattern (from RaptorQ Visualization):**
```tsx
const observer = new IntersectionObserver(
  ([entry]) => {
    if (entry.isIntersecting && !initialized.current) {
      initialized.current = true;
      cleanupRef.current = initializeHeavyVisualization();
      observer.disconnect();
    }
  },
  { rootMargin: "200px" } // Start 200px before visible
);
```

**Additional lazy patterns:**
- `next/dynamic` with `ssr: false` for Three.js/Canvas components
- Visibility-gated RAF loops (pause animation when off-screen)
- Resource disposal on unmount (dispose WebGL contexts, cancel RAF)

---

## 8. prefers-reduced-motion Is Not Optional

**The principle:** Every animated component must respect the user's motion preferences. This is both accessibility compliance and basic respect.

**Implementation hierarchy:**

1. **Check early, bail fast:**
```tsx
const prefersReducedMotion = useReducedMotion();
if (prefersReducedMotion) return <StaticFallback />;
```

2. **Conditional animation props:**
```tsx
initial={prefersReducedMotion ? false : { opacity: 0, y: 20 }}
```

3. **Duration zero for transitions:**
```tsx
transition={prefersReducedMotion ? { duration: 0 } : springs.smooth}
```

4. **Static values for counters:**
```tsx
if (prefersReducedMotion) { setCount(finalValue); return; }
```

---

## 9. Real Algorithms, Not Fake Data

**The principle:** When visualizing an algorithm or process, embed the actual implementation. Don't pre-compute results or fake the animation.

**Examples:**
- **CMA-ES**: Full `ProCMAES` class with `sample()`, `update()`, `eigen()` methods (~150 lines)
- **Hoeffding's D**: Actual statistical calculation of the D statistic with ranked data
- **Myers Diff**: Real edit distance computation for the Spec Evolution viewer
- **MVCC Race**: Stochastic conflict detection based on actual page overlap

**Why this matters:**
- Users can adjust parameters and see real results
- The visualization is guaranteed correct (it IS the algorithm)
- Edge cases reveal naturally through interaction
- The teaching is authentic, not staged

---

## 10. Comparative Juxtaposition

**The principle:** The fastest way to teach "why X is better than Y" is to show them side by side with identical visual structure but different outcomes.

**Proven formats:**
- **Split screen**: Tokio (left, red) vs Asupersync (right, green) — identical structure, contrasting outcomes
- **Tabbed comparison**: CALM theorem monotone vs non-monotone — same visual space, different behavior
- **Sequential steps**: Storage modes B-tree vs ECS — same 6 steps, different visual results at each step

**Key: the visual structure must be identical.** Only the behavior/outcome should differ. This isolates the teaching variable.

---

## 11. Color Is Semantic

**The universal palette across all four projects:**

| Semantic | Color | Tailwind | Usage Examples |
|----------|-------|----------|----------------|
| Success | `#34d399` | emerald-400 | Committed transactions, healthy pages, completed states |
| Error | `#f87171` | red-400 | Conflicts, leaked resources, corruption |
| Warning | `#fbbf24` | amber-400 | Draining, waiting, commuting writes |
| Active | `#22d3ee` | cyan-400 | Currently processing, choosing, scanning |
| Info | `#38bdf8` | sky-400 | Idle states, informational, completed |
| Selection | `#a78bfa` | violet-400 | User-selected, highlighted connections |
| Muted | `#94a3b8` | slate-400 | Disabled, background, inactive |

**Rule:** Color is never the sole indicator. Always pair with shape, icon, or label.

---

## 12. useRef for High-Frequency, useState for UI

**The principle:** React state updates trigger re-renders. Mouse position at 60fps = 60 re-renders/second. Use refs for anything that updates faster than the user can perceive discrete changes.

**Use useRef for:**
- Mouse position (custom cursor, eye tracking, parallax)
- RAF animation IDs
- Canvas/WebGL contexts
- Physics simulation state
- Interval/timeout IDs
- Previous values for comparison

**Use useState for:**
- Which step is active (user clicks, discrete changes)
- Whether playing or paused
- Selected node ID
- Hover state (only when it changes UI layout)
- Modal open/closed

**The pattern (from Custom Cursor):**
```tsx
const posRef = useRef({ x: 0, y: 0 });
const frameRef = useRef<number>(0);

// Mouse events write to ref (no re-render)
const onMove = (e: MouseEvent) => {
  posRef.current = { x: e.clientX, y: e.clientY };
};

// RAF reads from ref and updates MotionValues (no re-render)
const flush = () => {
  motionX.set(posRef.current.x);
  motionY.set(posRef.current.y);
  frameRef.current = requestAnimationFrame(flush);
};
```
