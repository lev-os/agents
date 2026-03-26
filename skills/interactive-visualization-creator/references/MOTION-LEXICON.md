# The Motion Lexicon

A systematic dictionary mapping **narrative intent** to **exact visual implementation**. Every motion, color shift, and timing choice in a visualization should serve an emotional purpose. This reference makes that mapping explicit and repeatable.

---

## The Gap This Fills

```
CONCEPT-DECOMPOSITION.md  →  "What story do I want to tell?"
MOTION-LEXICON.md         →  "What should each beat FEEL like?"  ← THIS
COMPONENT-PATTERNS.md     →  "What code do I write?"
```

Without this layer, the agent must intuit the connection between "I want this moment to feel dramatic" and "use `scale: [1, 1.3, 1]` with a 200ms delay and an amber→red color shift." That intuition gap is where emotionally flat visualizations come from — technically correct but narratively dead.

---

## The Eight Narrative Beats

Every visualization moment falls into one of eight beats. Each beat has a precise recipe extracted from 100+ production implementations.

---

### ESTABLISH

**Emotional goal:** "Here's the world. Orient yourself."

Calm, controlled entrance. The user sees the concept for the first time. No drama — just clarity.

**Framer Motion recipe:**
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: "easeOut" }}
/>

// For sections with title + content:
// Title: x: -20 → 0 (0.8s)
// Content: y: 40 → 0 (1.0s, 200ms delay)
```

**Color:** Slate → Cyan. Start muted, arrive at the section's accent color. No bright colors yet — save those for later beats.

**Spring config:** Not spring — use duration-based easing for calm entrances.
- Duration: 0.6–1.0s
- Easing: `easeOut` or `[0.19, 1, 0.22, 1]` (the universal entrance curve)
- Stagger: `0.1 + index * 0.1` for lists

**When to use:** First appearance of any concept, section entrances, initial state of steppers, hero text reveals.

**Production examples:**
- SectionShell left column: `x: -20 → 0`, 0.8s, `[0.19, 1, 0.22, 1]`
- Hero badge entrance: `y: 20 → 0`, 0.6s, `easeOut`
- Feature card grid: `y: 20 → 0`, 0.5s, stagger `(index % 3) * 0.1`

**Reduced motion:** Instant appearance, no motion. `skipAnim ? { opacity: 1 } : { opacity: 0, y: 20 }`

**Haptic:** None. Establish is passive.

---

### TENSION

**Emotional goal:** "Something is building. Pay attention."

Pulse, oscillation, slow color shift toward warning. The user senses that something is about to happen — the concept is approaching its critical moment.

**Framer Motion recipe:**
```tsx
// Pulsing glow (most common tension pattern)
<motion.div
  animate={{ opacity: [0.3, 0.7, 0.3] }}
  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
  style={{ boxShadow: `0 0 20px ${color}40` }}
/>

// Scale oscillation (heightened tension)
<motion.div
  animate={{ scale: [1, 1.05, 1] }}
  transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
/>

// Budget/countdown bar (tension with deadline)
<motion.div
  animate={{ width: `${remaining}%` }}
  transition={{ duration: 0.05, ease: "linear" }}
  className="bg-gradient-to-r from-green-500 via-orange-500 to-red-500"
/>
```

**Color:** Amber → Orange. The warning palette. Green drains away, amber emerges.
- Waiting/blocked: `#eab308` (amber)
- Escalating: `#f97316` (orange)
- Budget countdown: Green → Orange → Red gradient based on remaining %

**Spring config:** Not spring — use duration-based loops.
- Glow pulse: 1.5–2.5s cycle, `easeInOut`, `repeat: Infinity`
- Scale pulse: 1–1.5s cycle
- Rapid oscillation (conflict): 0.4s cycle (faster = more urgent)

**When to use:** Before a revelation, during resource countdown, when showing conflict building, writer contention in MVCC, cancel protocol draining phase.

**Production examples:**
- MVCC Race blocked writer: `opacity: [0.25, 0.55, 0.25]`, 1.2s
- Cancel Protocol budget bar: Green→Orange→Red over 3000ms
- Conflict Ladder glow: `opacity: [0.2, 0.5, 0.2]`, 2s, color matches conflict severity
- Lightning arc flicker: `opacity: [0.4, 1, 0.6, 1, 0.3]`, 0.2s

**Reduced motion:** Static amber/orange color, no animation. The color alone signals caution.

**Haptic:** `lightTap()` on each escalation step.

---

### REVELATION

**Emotional goal:** "Aha! NOW you see it."

The dramatic moment. A burst of color, a scale pop, a counter reaching its final value. This is the beat that justifies the entire visualization.

**Framer Motion recipe:**
```tsx
// Scale pop (most impactful)
<motion.div
  initial={{ scale: 0, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: "spring", stiffness: 400, damping: 20 }}
/>

// Color burst (for state transitions)
<motion.div
  initial={{ backgroundColor: "#1e293b" }}  // slate
  animate={{ backgroundColor: "#10b981" }}  // emerald
  transition={{ duration: 0.3 }}
/>

// Counter reveal (for numeric aha moments)
// easeOutExpo: t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
// Duration: 2000ms via requestAnimationFrame
```

**Color:** Context-dependent burst.
- Success revelation: Slate → Emerald (`#10b981`) flash
- Danger revelation: Slate → Red (`#ef4444`) with `boxShadow: 0 0 40px #ef444444`
- Data revelation: Background → Diverging color scale
- Progress fill: Purple (`#9333ea`) for expensive computation (Argon2id bar)

**Spring config:** `{ type: "spring", stiffness: 400, damping: 20 }` — the "snappy" preset. Fast arrival, minimal overshoot. For scale pops, use `stiffness: 400` minimum.

**When to use:** The aha moment in Concept Decomposition Step 4. Counter completion. Encryption step 5 (scramble). Market cap drop line. Compile error flash. Node selection in flywheel.

**Production examples:**
- Market cap drop: Chart path draws in 800ms (`easeIn`), then drop point marker pops `scale: 0→1` in 300ms
- Animated counter: 2000ms with `easeOutExpo`, green glow on completion
- Encryption scramble: Row-by-row color shift, `delay: row * 0.03`
- Compile error box: `scale: [0.8, 1.05, 1]`, 0.5s, red boxShadow glow
- Conflict Ladder resolution icon: `scale: 0→1`, spring stiffness 400, delay 0.1s

**Reduced motion:** Instant state change with color shift (no scale animation). The color change alone carries the revelation.

**Haptic:** `mediumTap()` — a satisfying thunk at the moment of understanding.

---

### FAILURE

**Emotional goal:** "THIS is what goes wrong. This is why the system exists."

Shake, red flash, collapse. Failure states are often the most educational beat because they show the consequence that the system prevents.

**Framer Motion recipe:**
```tsx
// Horizontal shake (corruption, error)
<motion.div
  animate={{ x: [0, -3, 3, -2, 2, 0] }}
  transition={{ duration: 0.4, ease: "easeInOut" }}
/>

// Red flash overlay
<motion.div
  initial={{ opacity: 0.6 }}
  animate={{ opacity: 0 }}
  transition={{ duration: 0.8 }}
  className="absolute inset-0 bg-red-500/20"
/>

// Collapse/disappear (resource leak)
<motion.div
  exit={{ opacity: 0, scale: 0.85 }}
  transition={{ duration: 0.15, ease: "easeIn" }}
/>

// Chromatic aberration glitch
<motion.div
  animate={{
    x: [0, -offset, offset, -offset/2, 0],
    textShadow: [`${offset}px 0 rgba(255,0,0,0.5)`, `${-offset}px 0 rgba(0,255,255,0.5)`]
  }}
  transition={{ duration: 0.2, repeat: Infinity, repeatType: "mirror" }}
/>
```

**Color:** Red (`#ef4444`), always.
- Error state: `#ef4444` border + `bg-red-500/15`
- Corruption indicator: Red with "ERR" label
- Leaked resource: Red badge with glowing boxShadow
- Chromatic split: Red (#ff0000) and Cyan (#00ffff) at 0.5 opacity

**Spring config:** No spring — failure is abrupt. Use short durations with `easeIn` or `easeInOut`.
- Shake: 0.4s
- Flash: 0.15–0.8s
- Collapse: 0.15s, `easeIn`
- Glitch: 0.2s, `repeat: Infinity`

**When to use:** MVCC conflict, RaptorQ corruption, leaked obligations, Tokio instant-drop, SSI write-skew abort, encryption showing plaintext vulnerability.

**Production examples:**
- RaptorQ corruption: `x: [0, -3, 3, -2, 2, 0]`, 0.4s, red border
- Tokio resource leak: `exit: { opacity: 0, scale: 0.85 }`, 0.15s
- Obligation leak: Compile error box `scale: [0.8, 1.05, 1]`, red glow 40px
- FrankenGlitch: Offset 2–10px, textShadow chromatic split, 0.2s repeat
- MVCC conflict: `r: [5, 7, 5]`, 0.4s rapid oscillation, amber FCW tag

**Reduced motion:** Static red color + error icon. No shake or flash.

**Haptic:** `errorBuzz()` — a sharp warning vibration.

---

### COMPARISON

**Emotional goal:** "See the difference. One is better than the other."

Side-by-side with synchronized timing, then color divergence at the critical moment. The user sees both approaches and the difference becomes visceral.

**Framer Motion recipe:**
```tsx
// Synchronized split panels
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <Panel
    borderColor={phase === "diverged" ? "#ef4444" : "#3b82f6"}
    style={{ boxShadow: `0 0 6px ${color}80` }}
  />
  <Panel
    borderColor={phase === "diverged" ? "#22c55e" : "#3b82f6"}
    style={{ boxShadow: `0 0 6px ${color}80` }}
  />
</div>

// Color divergence at critical moment
<motion.div
  animate={{ borderColor: diverged ? "#ef4444" : "#3b82f6" }}
  transition={{ duration: 0.3 }}
/>
```

**Color:** Start identical (both blue `#3b82f6`), then diverge.
- Before divergence: Both panels blue
- After divergence: Left = Red (`#ef4444`), Right = Emerald (`#22c55e`)
- Tab comparison: Green badge for monotone, Red badge for non-monotone

**Spring config:** Standard `smooth` spring for transitions. The comparison itself is static layout — the drama is in the color divergence.

**When to use:** Tokio vs Asupersync, CALM theorem tabs, Conflict Ladder scenarios (green vs amber vs red), any before/after.

**Production examples:**
- Tokio comparison: Both start blue → Tokio turns red (leaked), Async turns green (closed)
- CALM theorem: Monotone tab green with flowing arrows, Non-monotone tab red with barriers
- Conflict Ladder: Three scenarios with green/amber/red borders and symbols (||, ↔, ⚡)
- Spec Evolution diff: Pink (#fb7185) deletions vs Green (#34d399) additions

**Reduced motion:** Static split layout with color contrast. No animated transitions between states.

**Haptic:** `lightTap()` on tab/scenario switch.

---

### PROGRESSION

**Emotional goal:** "Step by step. Follow along."

Stepper transitions, active indicator advancement, sequential reveals. The user controls the pace and sees each step of a process.

**Framer Motion recipe:**
```tsx
// Step content cross-fade (AnimatePresence)
<AnimatePresence mode="wait">
  <motion.div
    key={step.id}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ type: "spring", stiffness: 200, damping: 25 }}
  />
</AnimatePresence>

// Active step indicator
<motion.div
  animate={{ scale: isActive ? 1.05 : 1 }}
  transition={{ duration: 0.3 }}
  className={isActive ? "border-cyan-400 bg-cyan-400/10" : "border-slate-600"}
/>

// State machine color advance
<motion.div
  animate={{ stroke: isPassed ? nextColor : "#1e293b" }}
  transition={{ duration: 0.3 }}
/>
```

**Color:** Cyan (`#38bdf8`) for active, Slate for inactive, step-specific colors for state machines.
- Active step: `#38bdf8` (cyan) or `#22c55e` (green) border + glow
- Completed step: Full color, checkmark
- Future step: Slate (`#475569`), muted
- State machine: Each state has its own color (Running=green, CancelRequested=amber, etc.)

**Spring config:** `smooth` preset — `{ type: "spring", stiffness: 200, damping: 25 }`. Smooth enough to follow, snappy enough to feel responsive.

**When to use:** Encryption pipeline 7 steps, Bakery algorithm phases, cancel protocol state sequence, COW B-tree cascading copies, any stepper visualization.

**Production examples:**
- Encryption pipeline: Content cross-fade with step index, color shifts per phase
- Cancel state machine: Box `scale: 1.05`, glow `opacity: [0.3, 0.7, 0.3]`, 1.5s
- COW B-tree cascade: Node copies at 0ms, 600ms, 1200ms intervals, scale pulse 1.1
- Obligation flow: Permit icon follows path with `spring: { stiffness: 180, damping: 22 }`

**Reduced motion:** Instant state change, no cross-fade. Active indicator changes color without animation.

**Haptic:** `lightTap()` on each step advance.

---

### RESOLUTION

**Emotional goal:** "Now you understand. Everything settles into place."

Spring settle, green glow, opacity reaching full. The concept is understood, the system is stable, the drama is over. This beat is earned — it only works after tension or failure.

**Framer Motion recipe:**
```tsx
// Spring settle to final state
<motion.div
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: "spring", stiffness: 100, damping: 20 }}
  style={{ boxShadow: "0 0 20px rgba(16, 185, 129, 0.3)" }}
/>

// Success flash + fade
<motion.div
  initial={{ opacity: 0.6 }}
  animate={{ opacity: 0 }}
  transition={{ duration: 0.8 }}
  className="absolute inset-0 bg-teal-400/20"
/>

// Completion message fade-in
<motion.div
  initial={{ opacity: 0, y: 6 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4 }}
  className="text-emerald-400"
/>
```

**Color:** Emerald (`#10b981`) or Teal (`#14b8a6`). Green = safe, resolved, understood.
- Success: `#10b981` border + glow
- Repaired: `#14b8a6` flash → settle to `#10b981`
- Completed: `#22c55e` with shield/check icon
- Resolution message: Emerald text

**Spring config:** `gentle` preset — `{ type: "spring", stiffness: 100, damping: 20 }`. Slow, deliberate settle. The motion should feel like exhaling.

**When to use:** After failure states (RaptorQ repair complete), after tension (cancel protocol completed), verification success (encryption decrypted), WAL checkpoint complete.

**Production examples:**
- RaptorQ repaired: Teal flash `opacity: 0.6→0`, 0.8s, then "OK" label
- Encryption verification: Shield icon `scale: 0→1`, spring, emerald
- WAL checkpoint: "WAL recycled" message in emerald, `opacity: 0→1`
- Async resource cleanup: Row backgroundColor transitions to `#22c55e`, stagger `i * 500ms`

**Reduced motion:** Instant green state. No spring settle.

**Haptic:** `mediumTap()` — a satisfying confirmation.

---

### AMBIENT

**Emotional goal:** "This is alive. The system is breathing."

Continuous background motion that creates atmosphere without demanding attention. Orbits, floats, parallax, slow pulses. Never the focus — always the context.

**Framer Motion recipe:**
```tsx
// Breathing glow (reactor core)
<motion.div
  animate={{
    boxShadow: [
      "0 0 20px rgba(56, 189, 248, 0.2)",
      "0 0 60px rgba(56, 189, 248, 0.5)",
      "0 0 20px rgba(56, 189, 248, 0.2)",
    ],
    scale: [1, 1.05, 1],
  }}
  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
/>

// Particle drift
<motion.div
  animate={{
    x: [0, driftX, 0],
    y: [0, driftY, 0],
    opacity: [0.15, 0.7, 0.15],
  }}
  transition={{ duration: 8 + prng * 20, repeat: Infinity, ease: "linear" }}
/>

// Parallax response (mouse-following)
const springX = useSpring(mouseX, { damping: 50, stiffness: 100 });
const parallaxX = useTransform(springX, v => (v / window.innerWidth - 0.5) * -60);
<motion.div style={{ x: parallaxX, y: parallaxY }} />
```

**Color:** Muted accent colors at low opacity.
- Glow blobs: `teal-500/20`, `blue-500/20`
- Ring spectrum: 8 colors at 0.1–0.25 opacity
- Neural fragments: Spectrum colors at 0.15–0.7 opacity pulse

**Spring config:** For parallax only: `{ damping: 50, stiffness: 100 }` — slow, smooth follow. Everything else uses duration-based `linear` or `easeInOut`.

**Timing:**
- Breathing glow: 4–10s cycle
- Particle drift: 8–28s per particle
- Ring rotation: 30–40s (Web Animations API)
- Parallax: Real-time with spring damping

**When to use:** Hero section backgrounds, flywheel reactor core, GlowOrbits, neural fragments, border traveling sparks, any "living system" atmosphere.

**Production examples:**
- GlowOrbits rings: `rotate(0→360deg), scale(1→1.15→1)`, 30000+i*8000ms
- Flywheel reactor: `boxShadow` pulse, `scale: [1, 1.05, 1]`, 4s
- Neural fragments: 18 particles, 8–28s drift, spectrum colors
- NeuralPulse spark: Border traverse, 4s per lap, 2 staggered sparks
- Synergy indicator: `scale: [1, 1.3, 1], opacity: [0.7, 1, 0.7]`, 2s

**Reduced motion:** Static state — no orbits, no particles. Show a single still frame of the ambient effect, or hide entirely.

**Haptic:** None. Ambient is invisible to touch.

---

## Beat Composition Grammar

Beats follow narrative rules. Certain sequences work; others feel wrong.

### Valid Sequences

```
ESTABLISH → TENSION → REVELATION      (The classic arc)
ESTABLISH → PROGRESSION → RESOLUTION   (Step-by-step mastery)
ESTABLISH → COMPARISON → REVELATION    (Side-by-side discovery)
TENSION → FAILURE → RESOLUTION         (Crisis and recovery)
ESTABLISH → TENSION → FAILURE          (Showing what goes wrong)
PROGRESSION → TENSION → REVELATION     (Building to aha moment)
```

### Invalid Sequences (anti-patterns)

```
REVELATION → ESTABLISH    ← Anticlimactic. Never introduce AFTER the aha.
RESOLUTION → TENSION      ← Breaks trust. Once resolved, stay resolved.
FAILURE → ESTABLISH       ← Disorienting. After failure, resolve or explain.
AMBIENT → REVELATION      ← Ambient can't build enough context for aha.
```

### The Meta-Sequence (Full Visualization Arc)

```
AMBIENT (background running continuously)
  │
  ├── ESTABLISH (user enters viewport)
  │     │
  │     ├── TENSION (optional: build anticipation)
  │     │     │
  │     │     ├── REVELATION (the aha moment)
  │     │     │     │
  │     │     │     └── RESOLUTION (settle into understanding)
  │     │     │
  │     │     └── FAILURE (show what goes wrong)
  │     │           │
  │     │           └── RESOLUTION (show how the system fixes it)
  │     │
  │     ├── PROGRESSION (step through the concept)
  │     │     │
  │     │     └── RESOLUTION (final step understood)
  │     │
  │     └── COMPARISON (show two approaches)
  │           │
  │           └── REVELATION (the difference is clear)
  │
  └── (User scrolls to next section → new ESTABLISH)
```

---

## Beat × Concept Decomposition Mapping

How the 5 aha patterns from [CONCEPT-DECOMPOSITION.md](CONCEPT-DECOMPOSITION.md#step-4-engineer-the-aha-moment) map to beat sequences:

| Aha Pattern | Beat Sequence |
|---|---|
| **A: Parameter Manipulation** | ESTABLISH → TENSION (parameter changes) → REVELATION (effect is visible) |
| **B: State Progression** | ESTABLISH → PROGRESSION (step through) → RESOLUTION (concept understood) |
| **C: Side-by-Side Divergence** | ESTABLISH → COMPARISON → TENSION (difference builds) → REVELATION (divergence) |
| **D: Failure Revelation** | ESTABLISH → TENSION → FAILURE (what goes wrong) → RESOLUTION (system prevents it) |
| **E: Spatial Discovery** | ESTABLISH → AMBIENT (network visible) → PROGRESSION (hover/explore) → REVELATION (connections discovered) |

---

## Worked Example: Encryption Pipeline

The 7-step encryption pipeline mapped to narrative beats:

```
Step 1: ESTABLISH    — Plaintext grid (green, structured, visible)
Step 2: ESTABLISH    — Passphrase appears (amber key)
Step 3: TENSION      — Argon2id bar fills slowly (purple, 2s, expensive)
Step 4: ESTABLISH    — Nonce + AAD appear (blue, deterministic)
Step 5: REVELATION   — Grid scrambles! (row-by-row color chaos, 0.03s stagger)
Step 6: RESOLUTION   — On-disk format shown (ciphertext + tag + nonce, settled)
Step 7: RESOLUTION   — Decrypt succeeds (green grid returns, shield icon pops)
```

**The emotional arc:** Calm → Calm → Building weight → Calm → DRAMA → Settle → Relief

Note how Steps 1-2-4 are all ESTABLISH — they add one concept at a time without drama. Step 3 introduces TENSION with the slow progress bar. Step 5 is the REVELATION — the actual encryption, the visual transformation. Steps 6-7 RESOLVE into understanding.

---

## Quick Reference Card

| Beat | Duration | Easing | Color | Spring |
|------|----------|--------|-------|--------|
| ESTABLISH | 0.6–1.0s | `[0.19, 1, 0.22, 1]` | Slate → Accent | None (duration) |
| TENSION | 1.5–2.5s loop | `easeInOut` | Amber/Orange | None (duration loop) |
| REVELATION | 0.3–0.5s | `easeOut` | Context burst | `stiffness: 400, damping: 20` |
| FAILURE | 0.15–0.4s | `easeIn` | Red `#ef4444` | None (abrupt) |
| COMPARISON | 0.3s switch | `easeOut` | Blue → Red vs Green | `smooth` (200/25) |
| PROGRESSION | 0.3–0.5s/step | Spring | Cyan active | `smooth` (200/25) |
| RESOLUTION | 0.4–0.8s | `easeOut` | Emerald `#10b981` | `gentle` (100/20) |
| AMBIENT | 4–30s loop | `linear`/`easeInOut` | Muted, 0.1–0.25 opacity | Parallax: damping 50, stiffness 100 |
