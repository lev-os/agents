---
name: interactive-visualization-creator
description: >-
  Build interactive visualizations for Next.js (SVG, Canvas, Three.js, Framer Motion).
  Use when creating diagrams, animations, simulations, or data visualizations.
---

<!-- TOC: Golden Thread | Quick Router | Visualization Types | Creation Workflow | Tech Selection | Device Strategy | Pedagogy Principles | Performance | Accessibility | Validation | References -->

# Interactive Visualization Creator

> **When to Use:** Building interactive visualizations for Next.js/React sites that need to both look stunning AND teach concepts effectively through interactivity.
>
> **When NOT to Use:** Static charts (use a charting library), pure decoration with no pedagogical purpose, or backend data dashboards (use admin tooling).
>
> **Core Insight:** The best visualizations are not fancy effects in search of a purpose. They make concepts viscerally obvious that would take paragraphs of text to explain poorly. Every animation, every interaction, every color choice must serve comprehension.

---

## The Golden Thread

These are the invariant truths distilled from 100+ production visualizations across jeffrey_emanuel_personal_site, frankentui_website, frankensqlite_website, and asupersync_website. They are non-negotiable:

| # | Principle | Why It Matters |
|---|-----------|----------------|
| 1 | **Pedagogy drives design, not aesthetics** | A beautiful viz that doesn't teach is just a screensaver |
| 2 | **Progressive disclosure over information dump** | Reveal complexity gradually via steppers, scroll triggers, phases |
| 3 | **Device-aware quality tiers, not responsive compromise** | Low/medium/high particle counts, different interaction models per device class |
| 4 | **Dual interaction models** | Desktop = hover + parallax + keyboard; Mobile = tap + haptic + bottom-sheet |
| 5 | **Spring physics over linear interpolation** | Springs feel natural; linear feels robotic |
| 6 | **SVG for structure, Canvas/WebGL for particles** | Pick technology by visualization type, not familiarity |
| 7 | **Lazy initialization is mandatory** | IntersectionObserver + rootMargin. Never render heavy content off-screen |
| 8 | **prefers-reduced-motion is not optional** | Full accessibility support in every component, always |
| 9 | **Real algorithms, not fake data** | Embed actual implementations (CMA-ES, Myers diff, Hoeffding's D) for correctness |
| 10 | **Comparative juxtaposition** | Side-by-side before/after makes differences viscerally obvious |
| 11 | **Color is semantic** | green=success, red=error, amber=warning, cyan=active, blue=info. Consistent always |
| 12 | **useRef for high-frequency, useState for UI** | RAF loops, mouse tracking, physics sims use refs to avoid re-renders |

See [GOLDEN-THREAD.md](references/GOLDEN-THREAD.md) for the complete deep-dive with code examples from all four projects.

---

## Quick Router

| I need to... | Go to |
|---|---|
| Build a state machine / algorithm walkthrough | [COMPONENT-PATTERNS.md > Stepper Visualizations](references/COMPONENT-PATTERNS.md#stepper-visualizations) |
| Build a network graph / relationship diagram | [COMPONENT-PATTERNS.md > Network Graphs](references/COMPONENT-PATTERNS.md#network-graphs) |
| Build a particle system / 3D scene | [COMPONENT-PATTERNS.md > Particle Systems](references/COMPONENT-PATTERNS.md#particle-systems) |
| Build a scroll-triggered animation | [COMPONENT-PATTERNS.md > Scroll Animations](references/COMPONENT-PATTERNS.md#scroll-triggered-animations) |
| Build a real-time simulation with sliders | [COMPONENT-PATTERNS.md > Live Simulations](references/COMPONENT-PATTERNS.md#live-simulations) |
| Build a comparative / side-by-side view | [COMPONENT-PATTERNS.md > Comparative Views](references/COMPONENT-PATTERNS.md#comparative-views) |
| Handle mobile vs desktop properly | [MOBILE-DESKTOP.md](references/MOBILE-DESKTOP.md) |
| Make it teach effectively | [PEDAGOGY.md](references/PEDAGOGY.md) |
| Optimize performance | [PERFORMANCE.md](references/PERFORMANCE.md) |
| Copy-paste starter patterns | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| Decompose ANY concept into a visualization design | [CONCEPT-DECOMPOSITION.md](references/CONCEPT-DECOMPOSITION.md) |
| Compose visualizations into a cinematic page narrative | [SCROLL-NARRATIVE.md](references/SCROLL-NARRATIVE.md) |
| Map narrative intent to exact motion recipes | [MOTION-LEXICON.md](references/MOTION-LEXICON.md) |
| Derive premium visual aesthetic from a single accent color | [AESTHETIC-DNA.md](references/AESTHETIC-DNA.md) |

---

## Visualization Type Selector

| What you're visualizing | Type | Tech Stack |
|---|---|---|
| Process with discrete steps | **Stepper** | Framer Motion + SVG + AnimatePresence |
| Relationships between entities | **Network Graph** | SVG circular layout + Bezier curves |
| Data distribution / statistics | **Interactive Chart** | D3 math + SVG/Three.js + sliders |
| Tree / hierarchy | **Tree Viz** | SVG computed layout + path highlighting |
| Comparison of two approaches | **Side-by-Side** | Split grid + shared stepper + color contrast |
| Timeline / evolution | **Scroll-Triggered** | Framer Motion whileInView + staggered reveals |
| Particles / 3D space | **Particle System** | React Three Fiber + quality tiers |
| Ambient background | **Decorative** | GSAP/Framer + CSS + IntersectionObserver |

See [COMPONENT-PATTERNS.md](references/COMPONENT-PATTERNS.md) for architecture and code for each type.

---

## Creation Workflow

### Phase 1: Concept Design
1. **Decompose the concept**: Use the [Concept Decomposition Engine](references/CONCEPT-DECOMPOSITION.md) to identify entities, states, transitions, and the teaching variable
2. **Define the teaching goal**: What concept should the reader understand after interacting?
3. **Identify the "aha moment"**: What specific interaction makes the concept click? (See [5 aha patterns](references/CONCEPT-DECOMPOSITION.md#step-4-engineer-the-aha-moment))
4. **Choose visualization type**: Use the decision tree above
5. **Sketch the states**: What are the discrete states/phases the user will see?

### Phase 2: Architecture
1. **Select technology stack**: See [Tech Selection](#tech-selection-guide) below
2. **Establish visual aesthetic**: Derive dark canvas, glass surfaces, and color palette from accent color using [AESTHETIC-DNA.md](references/AESTHETIC-DNA.md)
3. **Design interaction model**: Desktop hover vs mobile tap paths
4. **Plan quality tiers**: What degrades on low-end devices?
5. **Define color semantics**: Map colors to meaning before coding

### Phase 3: Implementation
1. **Build the static frame first**: SVG structure, node positions, layout
2. **Add the stepper/controller**: Navigation controls for temporal visualizations
3. **Wire up animations**: Framer Motion transitions between states
4. **Add interactivity**: Hover/click/drag handlers
5. **Implement device adaptation**: Touch detection, quality scaling, bottom sheets
6. **Add accessibility**: reduced-motion, ARIA labels, keyboard nav

### Phase 4: Page Composition
1. **Choose narrative arc**: Select a [page template](references/SCROLL-NARRATIVE.md#narrative-arc-templates) that matches your content
2. **Allocate scroll budget**: Assign vertical space per section using the [scroll budget calculator](references/SCROLL-NARRATIVE.md#scroll-budget-calculator)
3. **Choreograph entrances**: Apply [SectionShell pattern](references/SCROLL-NARRATIVE.md#entrance-choreography-system) with staggered reveals
4. **Run the billboard test**: Screenshot random scroll positions — each must be coherent

### Phase 5: Polish
1. **Assign narrative beats**: Map each section's emotional intent to a [Motion Lexicon beat](references/MOTION-LEXICON.md) for exact spring/color/timing recipes
2. **Spring-tune all transitions**: Adjust stiffness/damping until motion feels natural
3. **Add micro-interactions**: Haptic feedback, particle bursts, glow effects
4. **Test on real mobile**: Not just browser resize - actual touch interactions
5. **Validate pedagogy**: Does a first-time viewer actually learn the concept?

---

## Tech Selection Guide

| Need | Technology | When to Use |
|------|-----------|-------------|
| State transitions, layout animation | **Framer Motion** | Default choice for all animated React components |
| SVG diagrams, node graphs, trees | **SVG + Framer Motion** | Structured diagrams with <50 animated elements |
| Particle systems, 3D visualization | **React Three Fiber** (Three.js) | >100 particles, 3D space, WebGL shaders |
| Canvas 2D rendering | **Raw Canvas + RAF** | Custom rendering not suited to SVG DOM |
| Statistical calculations, scales | **D3.js** (math only) | Scales, color interpolation, statistics. NOT for rendering |
| Complex data tables with viz | **TanStack Table + Virtual** | Sortable/filterable data with virtualization |
| Timeline animations | **GSAP** | Complex sequenced timelines (alternative to Framer) |
| Charts with large datasets | **ECharts** | When D3+SVG would choke on data volume |

### Technology Anti-Patterns

- **Never use D3 for DOM manipulation** in React (use D3 for math, React for rendering)
- **Never use Three.js for flat diagrams** (SVG is simpler and more accessible)
- **Never use CSS keyframe animations for interactive state** (can't respond to user input)
- **Never use react-spring AND Framer Motion together** (pick one animation library)
- **Never use force-directed layout for fixed diagrams** (compute positions deterministically)

---

## Key Reusable Patterns

**Stepper Controller** — The single most reusable pattern (used in 30+ visualizations). Prev/Next/Play controls with keyboard support, auto-play, step dots, and haptic feedback. Full implementation in [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md#stepper-component).

**Semantic Colors** — Consistent across all visualizations: `emerald`=success, `red`=error, `amber`=warning, `cyan`=active, `sky`=info, `violet`=accent, `slate`=muted. Color is never the sole indicator — always pair with icons/labels/shapes. Full palette in [GOLDEN-THREAD.md](references/GOLDEN-THREAD.md#11-color-is-semantic).

**Spring Physics** — Default transitions: `{ type: "spring", stiffness: 200, damping: 25 }`. Snappy: `stiffness: 400, damping: 35`. Magnetic: `stiffness: 150, damping: 15, mass: 0.1`. Full configs in [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md#spring-physics-constants).

---

## Validation Checklist

Before considering any visualization complete:

- [ ] **Teaches something**: A non-expert can explain the concept after interacting
- [ ] **Works without animation**: Meaningful in static/reduced-motion mode
- [ ] **Desktop interaction**: Hover states, keyboard navigation, cursor feedback
- [ ] **Mobile interaction**: Touch targets >= 44px, haptic feedback, no hover-dependent UI
- [ ] **Performance**: Lazy init via IntersectionObserver, RAF for physics, no layout thrashing
- [ ] **Accessibility**: prefers-reduced-motion, ARIA labels, focus indicators, color-not-alone
- [ ] **Spring-tuned**: All motion uses spring physics (not linear/ease), feels natural
- [ ] **Semantic colors**: Consistent with the color system above
- [ ] **No orphaned animations**: All RAF/intervals cleaned up on unmount
- [ ] **TypeScript types**: All props, state, and callbacks fully typed

---

## References

| Topic | Reference |
|-------|-----------|
| Copy-paste patterns for every viz type | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| The 12 invariant principles with code examples | [GOLDEN-THREAD.md](references/GOLDEN-THREAD.md) |
| Detailed component patterns by visualization type | [COMPONENT-PATTERNS.md](references/COMPONENT-PATTERNS.md) |
| Device-specific interaction and quality strategies | [MOBILE-DESKTOP.md](references/MOBILE-DESKTOP.md) |
| Pedagogical design principles for teaching with viz | [PEDAGOGY.md](references/PEDAGOGY.md) |
| Performance optimization patterns | [PERFORMANCE.md](references/PERFORMANCE.md) |
| Concept → visualization decomposition engine | [CONCEPT-DECOMPOSITION.md](references/CONCEPT-DECOMPOSITION.md) |
| Scroll narrative architecture for full-page composition | [SCROLL-NARRATIVE.md](references/SCROLL-NARRATIVE.md) |
| Motion lexicon — narrative beats to animation recipes | [MOTION-LEXICON.md](references/MOTION-LEXICON.md) |
| Visual design system — dark canvas, glass, shadows, typography | [AESTHETIC-DNA.md](references/AESTHETIC-DNA.md) |
