# Scroll Narrative Architecture

Pages are not collections of visualizations. They are **scroll-driven stories** where scroll position is the narrative clock, each section builds on the previous one, and the full experience has a dramatic arc. This reference teaches how to compose individual visualizations into cinematic page experiences.

---

## The Core Insight

The best pages across all four projects share one trait: **every scroll position tells a coherent story**. You can screenshot any random viewport and it's a self-contained visual statement. This isn't accidental — it's the result of deliberate narrative architecture.

Individual visualizations are sentences. This reference teaches paragraph structure, chapter arcs, and narrative tension.

---

## Narrative Arc Templates

Five proven page structures extracted from production. Choose the one that matches your content.

### Template 1: The Deep-Dive Explainer

**Used by:** FrankenSQLite homepage, Asupersync architecture page

**Structure:** Hook → Problem → Deep Dive (N sections) → Resolution → CTA

```
ACT I: HOOK (0-10% scroll)
├── Full-viewport hero with living illustration
├── Stats grid (animated counters on intersection)
└── Feature cards (staggered grid reveal)

ACT II: THE PROBLEM (10-20%)
├── SectionShell: sticky title left, visualization right
└── First interactive viz establishes the core tension

ACT III: DEEP DIVE (20-75%)
├── 5-9 SectionShells, each with one concept + one viz
├── Alternating complexity: simple → complex → simple
└── Each section answers "how does X work?"

ACT IV: CONFLICT & RESOLUTION (75-90%)
├── "When things go wrong" — failure modes
├── Stacked visualizations showing mitigation
└── Comparison table vs alternatives

ACT V: CTA (90-100%)
├── Install command / getting started
├── Author credit + ecosystem flywheel
└── Footer links
```

**Vertical budget:** ~5000-5500px (8-10 viewport heights)
**Best for:** Technical product landing pages, library documentation

### Template 2: The Technical Article

**Used by:** Bakery Algorithm, Hoeffding Inequality, encryption pipeline articles

**Structure:** Thesis → Theory → Interactive Proof → Implications

```
OPENING (0-20%)
├── Full-viewport hero (Three.js/particle background)
├── Reading time estimate
├── Drop cap intro paragraph + insight callout
└── Hero fades on scroll (opacity: 1→0 over first 20%)

FOUNDATION (20-45%)
├── Prose sections with editorial column (max-w-[800px])
├── Math/theory exposition with KaTeX
├── First visualization: establish the model
└── Section reveals at threshold: 0.05, rootMargin: "-60px"

INTERACTIVE PROOF (45-80%)
├── 3-5 visualizations, each with own stepper
├── Progressive complexity (each builds on previous)
├── Code playground with editable parameters
└── The "aha moment" visualization (positioned at ~65% scroll)

CONCLUSION (80-100%)
├── Implications paragraph
├── Ties back to opening metaphor
└── Related reading links
```

**Vertical budget:** ~3000-4500px (3-4.5 viewport heights)
**Best for:** Blog posts, research explanations, algorithm walkthroughs

### Template 3: The Product Showcase

**Used by:** FrankenTUI homepage, TLDR/flywheel page

**Structure:** Spectacle → Demonstration → Justification → Social Proof → CTA

```
THE SPECTACLE (0-15%)
├── GlowOrbits + video/demo centerpiece
├── Floating stats card
└── Scroll indicator that fades on scroll

THE DEMONSTRATION (15-40%)
├── Interactive terminal/demo component
├── "See it in action" proof
└── Spec evolution / architecture hint

THE JUSTIFICATION (40-70%)
├── Feature grid (staggered cards)
├── Comparison matrix vs alternatives
├── Code block showing minimal API
└── Screenshot gallery with lightbox

SOCIAL PROOF (70-90%)
├── Timeline of development milestones
├── Tweet wall / community reactions
└── Contributor credits

RESOLUTION (90-100%)
├── CTA: "Get started" with install command
├── Author + ecosystem flywheel visualization
└── Open source links
```

**Vertical budget:** ~4500-5500px (7-9 viewport heights)
**Best for:** Open source project landing pages, SaaS homepages

### Template 4: The Side-by-Side Comparison

**Used by:** Asupersync vs Tokio, CALM theorem visualization

**Structure:** Setup → Side-by-Side → Divergence Point → Resolution

```
SETUP (0-20%)
├── Establish the two approaches being compared
├── Shared context that applies to both
└── "Watch what happens when..."

PARALLEL EXECUTION (20-60%)
├── Synchronized side-by-side panels
├── Both run identically at first (shared stepper)
├── Shared color semantics (green=both, then diverge)
└── Tension builds as differences emerge

DIVERGENCE (60-80%)
├── The moment they differ (the dramatic reveal)
├── Color split: left=red, right=emerald
├── Failure state on one side, success on other
└── "This is why X matters"

RESOLUTION (80-100%)
├── Summary comparison table
├── Key takeaway callout
└── "Learn more" links to deep dives
```

**Vertical budget:** ~2000-3000px (3-5 viewport heights)
**Best for:** Technology comparisons, before/after demonstrations

### Template 5: The Chronological Narrative

**Used by:** NVIDIA Story, development timelines

**Structure:** Dramatic Opening → Evidence Chain → Interpretation → Open Question

```
THE EVENT (0-20%)
├── Full-viewport dramatic moment (the $600B drop)
├── Staggered text reveals with 1.5-2s delays
├── Scroll indicator with opacity fade
└── Sets emotional tone immediately

THE EVIDENCE (20-55%)
├── Timeline component (staggered items)
├── Each event card reveals on scroll
├── Chronological progression builds understanding
└── Supporting data interspersed

THE INTERPRETATION (55-85%)
├── Quote wall (expert opinions, staggered)
├── Analysis sections
├── Key visualization showing the pattern
└── Multiple perspectives juxtaposed

THE QUESTION (85-100%)
├── "The story continues..." (open-ended)
├── Questions posed, not answers given
└── Links to ongoing coverage / deeper analysis
```

**Vertical budget:** ~2500-3500px (2.5-3.5 viewport heights)
**Best for:** Case studies, event analyses, narrative journalism

---

## Scroll Budget Calculator

How much vertical space each concept deserves. Based on measured allocations across 100+ production sections.

### The Formula

```
Viewport-heights = Base + Complexity Bonus + Novelty Bonus + Interaction Bonus
```

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Base** (every section) | 0.5vh | 0.75vh | 1.0vh |
| **Complexity** (concept density) | +0 | +0.25vh | +0.5vh |
| **Novelty** (how surprising) | +0 | +0.25vh | +0.5vh |
| **Interaction** (viz complexity) | +0 | +0.5vh | +1.0vh |

### Measured Allocations from Production

| Section Type | Typical Height | Padding | Content |
|---|---|---|---|
| Full-viewport hero | 90-100vh | pt-24 pb-32 | Living illustration + text |
| Stats grid | ~120px | mb-20 | 3-5 animated counters |
| SectionShell (text + viz) | 800-1200px | py-16 md:py-32 lg:py-48 | Sticky title + visualization |
| Feature grid (8-10 cards) | ~600px | py-16 md:py-32 | 3-4 column staggered cards |
| Comparison table | ~400px | py-16 md:py-32 | Feature matrix |
| Code block | ~300px | py-12 md:py-20 | Syntax-highlighted example |
| Timeline | 400-800px | py-16 md:py-32 | Staggered milestone items |
| CTA section | 200-350px | py-20 md:py-28 lg:py-36 | Centered copy + buttons |
| Author/flywheel | ~500px | py-32 | Bio + ecosystem visualization |

### Breathing Room Rules

1. **Section padding scales with viewport:** `py-16 md:py-32 lg:py-48` (64→128→192px)
2. **Between visualizations in same section:** `gap-8` (32px) minimum
3. **Between major acts:** Extra `mb-20` (80px) to signal narrative shift
4. **Hero to first content:** Generous `pb-32` (128px) for scroll affordance

### Total Page Budgets

| Page Type | Total Scroll | Viewport Heights | Sections |
|---|---|---|---|
| Product landing | 4500-5500px | 8-10vh | 12-18 |
| Technical article | 3000-4500px | 3-5vh | 6-10 |
| Comparison page | 2000-3000px | 3-5vh | 4-8 |
| Chronological narrative | 2500-3500px | 2.5-3.5vh | 5-8 |

---

## Entrance Choreography System

How elements reveal themselves as the user scrolls. Every pattern below is extracted from production code.

### The SectionShell Pattern (Most Important)

Used 30+ times across all four sites. The master scroll choreography component:

```tsx
// Left column: slides in from left
<motion.div
  initial={{ opacity: 0, x: -20 }}
  whileInView={{ opacity: 1, x: 0 }}
  viewport={{ once: true, amount: 0.05 }}
  transition={{ duration: 0.8, ease: [0.19, 1, 0.22, 1] }}
>
  {/* Title stays sticky: lg:sticky lg:top-32 */}
</motion.div>

// Right column: slides up, 200ms later
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.05 }}
  transition={{ duration: 1, ease: [0.19, 1, 0.22, 1], delay: 0.2 }}
>
  {children} {/* The visualization */}
</motion.div>
```

**Why this works:** The 200ms delay between title and content creates a reading sequence — eye goes to title first, then visualization appears to illustrate it.

### The Stagger Formula

Three production-proven stagger patterns:

```tsx
// Pattern A: Linear stagger (paragraphs, lists)
delay: 0.1 + index * 0.1
// Item 0: 100ms, Item 1: 200ms, Item 2: 300ms...

// Pattern B: Row-reset stagger (grids)
delay: (index % COLUMNS) * 0.1
// 3-column: items 0,3,6 at 0ms; items 1,4,7 at 100ms; items 2,5,8 at 200ms
// Prevents late items from appearing seconds after early ones

// Pattern C: Container variant (Framer Motion)
const staggerContainer: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.06, delayChildren: 0.1 } },
};
```

**The Row-Reset Rule:** For grids with >6 items, always use `index % COLUMNS` instead of raw `index`. A 12-item grid with linear stagger would have item 12 appearing 1.2s after item 1 — far too long. Row-reset ensures max stagger of `(COLUMNS - 1) * 0.1s`.

### The Cascade Rule

Elements enter **top-left to bottom-right**, never simultaneously. This mimics natural reading order:

```
Frame 0ms:    [Title ●] [        ] [        ]
Frame 200ms:  [Title ●] [Viz     ●] [        ]
Frame 300ms:  [Title ●] [Viz     ●] [Detail  ●]
```

**Never do this:**
```
Frame 0ms:    [Title ●] [Viz ●] [Detail ●]  ← Everything at once = no story
```

### Entrance Animation Values

Consistent across all four sites:

| Property | Entrance Value | Final Value | Notes |
|---|---|---|---|
| `opacity` | 0 | 1 | Always animated |
| `y` (slide up) | 20-40px | 0 | Sections: 40px, items: 20px |
| `x` (slide in) | -20px | 0 | Left-column titles only |
| `scale` | 0.95-0.98 | 1 | Heroes only, subtle |

### Timing Constants

| Element | Duration | Easing |
|---|---|---|
| Section entrance | 0.8-1.0s | `[0.19, 1, 0.22, 1]` |
| Grid items | 0.5s | `[0.19, 1, 0.22, 1]` |
| Hero text | 0.6s | Spring: stiffness 200, damping 25 |
| Stats counter | 2000ms + index * 200ms | `easeOutExpo` |
| Stagger interval | 0.06-0.1s | — |

### The Easing Curve

`[0.19, 1, 0.22, 1]` — Used universally across all four sites. This is a fast-out, smooth-settle curve that feels responsive without being abrupt. It's the scroll narrative equivalent of the "smooth" spring config.

### IntersectionObserver Thresholds

| Use Case | `amount` / `threshold` | `rootMargin` |
|---|---|---|
| Section reveal | 0.05 (5% visible) | `"0px"` |
| Stats counter trigger | 0.3 (30% visible) | `"0px"` |
| Heavy viz preload | 0.01 (1% visible) | `"600px 0px"` |
| Article section | 0.05 | `"0px 0px -60px 0px"` |
| Scroll progress visibility | N/A | Scroll Y > 400px |

---

## Cross-Visualization State Patterns

How multiple visualizations on a page share state and coordinate behavior.

### Pattern 1: Site Context Provider

Global state shared across all visualizations via React Context:

```tsx
interface SiteContextType {
  playSfx: (type: "click" | "zap" | "hum" | "error") => void;
  isAudioEnabled: boolean;
  toggleAudio: () => void;
  isAnatomyMode: boolean;     // Debug overlay (frankentui)
  isLabMode: boolean;          // Lab overlay (asupersync)
}

// Consumed by any visualization:
const { playSfx } = useSite();
```

**Use for:** Sound effects, debug modes, global toggles that affect all visualizations uniformly.

### Pattern 2: Hover/Selection Coordination

When hovering element A should highlight element B in a different visualization:

```tsx
// Shared state
const [hoveredId, setHoveredId] = useState<string | null>(null);
const [selectedId, setSelectedId] = useState<string | null>(null);
const activeId = selectedId || hoveredId;

// Derived connections
const connectedIds = useMemo(() => {
  if (!activeId) return new Set<string>();
  const ids = new Set([activeId]);
  edges.forEach(e => {
    if (e.from === activeId) ids.add(e.to);
    if (e.to === activeId) ids.add(e.from);
  });
  return ids;
}, [activeId, edges]);

// Consumed by: SVG diagram, detail panel, card grid
// All respond to the same activeId
```

**Used in:** Flywheel (all 4 sites), synergy diagrams, network graphs.

### Pattern 3: DeferredViz Wrapper

Lazy-load heavy visualizations while maintaining layout stability:

```tsx
function DeferredViz({ children, minHeight = 400 }) {
  const { ref, isIntersecting } = useIntersectionObserver({
    threshold: 0.01,
    rootMargin: "600px 0px",  // Load 600px before viewport
    triggerOnce: true,
  });

  return (
    <div ref={ref}>
      {isIntersecting ? children : <VizSkeleton style={{ minHeight }} />}
    </div>
  );
}
```

**Used 21 times in FrankenSQLite homepage alone.** Critical for pages with 10+ heavy visualizations.

### Pattern 4: Body Scroll Lock

When a visualization opens a modal/lightbox/bottom-sheet:

```tsx
function useBodyScrollLock(isLocked: boolean) {
  useLayoutEffect(() => {
    if (!isLocked) return;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = "hidden";
    document.body.style.paddingRight = `${scrollbarWidth}px`; // Prevent layout shift
    return () => {
      document.body.style.overflow = "";
      document.body.style.paddingRight = "";
    };
  }, [isLocked]);
}
```

**Critical detail:** The scrollbar width compensation prevents content from jumping when scrollbar disappears.

---

## Attention Choreography

Where the eye goes and how to control it.

### The Visual Weight Hierarchy

At any scroll position, visual weight determines attention order:

```
1. Motion (anything animating draws eye first)
2. Color contrast (bright on dark, saturated on muted)
3. Size (largest element in viewport)
4. Position (center-left of viewport = primary attention zone)
```

### The Sweet Spot

The primary attention zone is **center-left, slightly above middle** of the viewport. This is where the "aha moment" visualization should land when the user scrolls to it.

The SectionShell pattern exploits this: the sticky title sits at left, the visualization occupies center-right. The eye goes title → viz in that order.

### Attention Rules

1. **One moving thing per viewport.** If two animations compete for attention, neither wins. Pause off-screen animations with visibility gates.

2. **The 200ms rule.** New elements should appear within 200ms of the trigger (scroll, click). Longer delays break the cause-effect link.

3. **Entrance before interaction.** Let entrance animations complete before enabling hover/click interactions. Premature interaction feels broken.

4. **Dim the background.** When a visualization is the focus, surrounding elements should be muted (opacity, saturation, blur). The `connectedIds` pattern achieves this: unconnected nodes dim to 20% opacity.

5. **Exit matches entrance.** If elements slide up on entrance, they should fade (not slide down) on exit. AnimatePresence handles this:

```tsx
<AnimatePresence mode="wait">
  {activeStep && (
    <motion.div
      key={activeStep.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}  // Fade only, no slide
    />
  )}
</AnimatePresence>
```

---

## The Billboard Test

A validation technique for scroll narrative quality.

### The Test

1. Scroll to a random position on the page
2. Take a screenshot of exactly what's visible in the viewport
3. Show the screenshot to someone who hasn't seen the page
4. Ask: "Does this look intentional and coherent?"

### What Good Looks Like

- The visible content forms a complete visual statement
- No half-cut visualizations that look broken
- Text and visualization are both partially or fully visible (not one without the other)
- Color palette is coherent within the viewport
- If a section title is visible, its content is at least partially visible too

### What Bad Looks Like

- Empty space between two sections (both just outside viewport)
- An orphaned title with its visualization scrolled past
- Two competing animations both half-visible
- A loading skeleton stuck in view (DeferredViz triggered too late)

### How to Fix Billboard Failures

| Failure | Fix |
|---|---|
| Empty viewport between sections | Reduce section padding or add transitional content |
| Orphaned title | Make title sticky (`lg:sticky lg:top-32`) so it stays while content scrolls |
| Competing animations | Increase spacing between animated sections |
| Stuck skeleton | Increase DeferredViz rootMargin (e.g., "600px" → "800px") |
| Half-cut visualization | Ensure viz height < viewport height, or make it scroll-contained |

### Automated Billboard Testing

```tsx
// Scroll through page, screenshot at intervals
const viewportHeight = window.innerHeight;
const totalHeight = document.documentElement.scrollHeight;
const steps = Math.ceil(totalHeight / (viewportHeight * 0.5)); // Every half-viewport

for (let i = 0; i <= steps; i++) {
  window.scrollTo(0, i * viewportHeight * 0.5);
  await new Promise(r => setTimeout(r, 1500)); // Wait for animations
  // Screenshot and inspect
}
```

---

## Mobile Narrative Restructuring

The narrative arc adapts for mobile's different scroll behavior and constraints.

### What Changes on Mobile

| Aspect | Desktop | Mobile |
|---|---|---|
| Scroll velocity | Precise (trackpad) | Fast flicks (touch) |
| Viewport width | 1200px+ | 320-428px |
| Side-by-side | Two columns | Stacked |
| Sticky sidebars | `lg:sticky lg:top-32` | Not sticky (flows with content) |
| Section padding | `lg:py-48` (192px) | `py-16` (64px) |
| Stagger count | Full grid visible | Only 1-2 items per row |

### The Stacking Rule

Side-by-side layouts become stacked on mobile. This means the narrative must work vertically:

```tsx
// Desktop: title left, viz right (simultaneous)
// Mobile: title above, viz below (sequential)
<div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-16">
  <div className="lg:col-span-4 lg:sticky lg:top-32">
    {/* Title — sticky on desktop, flows on mobile */}
  </div>
  <div className="lg:col-span-8">
    {/* Visualization */}
  </div>
</div>
```

**On mobile, the title is no longer sticky** — it scrolls away as the user moves through the visualization. This is fine because mobile users scroll faster and are used to sequential content.

### Mobile Scroll Budget Adjustments

Mobile pages are taller (stacked content) but need less breathing room (smaller padding):

```
Desktop section: py-48 (192px) + content + py-48 = ~384px padding
Mobile section:  py-16 (64px) + content + py-16  = ~128px padding

Desktop side-by-side: ~800px tall
Mobile stacked:       ~1000px tall (content stacks)

Net effect: Mobile pages are ~80-90% of desktop height despite stacking
```

### Mobile-Specific Narrative Patterns

1. **Reduce stagger on mobile.** With only 1-2 items per row, `(index % 4) * 0.1` wastes time. Use `(index % 2) * 0.08` for mobile grids.

2. **Skip hero parallax.** Mouse parallax doesn't exist on touch. Replace with gentle auto-animation or static hero.

3. **Increase DeferredViz rootMargin.** Mobile users scroll faster — preload earlier: `rootMargin: "800px 0px"`.

4. **Bottom sheets replace side panels.** Detail panels slide up from bottom instead of appearing at right:

```tsx
// Desktop: side panel
<div className="hidden lg:block absolute right-0 w-80">
  <DetailPanel />
</div>

// Mobile: bottom sheet
<AnimatePresence>
  {selected && (
    <motion.div
      className="lg:hidden fixed inset-x-0 bottom-0 z-50 max-h-[70vh]
                 rounded-t-2xl bg-slate-900 border-t border-slate-700"
      initial={{ y: "100%" }}
      animate={{ y: 0 }}
      exit={{ y: "100%" }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <div className="w-12 h-1 bg-slate-600 rounded-full mx-auto mt-3" />
      <DetailPanel />
    </motion.div>
  )}
</AnimatePresence>
```

---

## Scroll-Linked Animation Patterns

### Scroll Progress Bar

Tracks reading position through an article:

```tsx
const progress = useMotionValue(0);
const scaleX = useSpring(progress, { stiffness: 100, damping: 30 });

useEffect(() => {
  let ticking = false;
  const onScroll = () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
        progress.set(Math.min(window.scrollY / maxScroll, 1));
        ticking = false;
      });
      ticking = true;
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  return () => window.removeEventListener("scroll", onScroll);
}, [progress]);

// Fixed bar at top of page
<motion.div
  className="fixed top-0 left-0 right-0 h-1 bg-cyan-400 origin-left z-40"
  style={{ scaleX }}
/>
```

### Hero Fade on Scroll

Hero disappears as user scrolls past:

```tsx
const { scrollYProgress } = useScroll();
const heroOpacity = useTransform(scrollYProgress, [0, 0.15], [1, 0]);
const heroScale = useTransform(scrollYProgress, [0, 0.15], [1, 0.95]);

<motion.div style={{ opacity: heroOpacity, scale: heroScale }}>
  <Hero />
</motion.div>
```

### Scroll Indicator Fade

The "scroll down" indicator disappears after the user starts scrolling:

```tsx
const scrollIndicatorOpacity = useTransform(
  scrollYProgress,
  [0, 0.05],   // Disappears by 5% scroll depth
  [0.5, 0]
);
```

---

## Worked Example: FrankenSQLite Homepage

The most complex page in the corpus, decomposed into its narrative architecture.

### The Arc (14 sections, ~5200px)

```
SCROLL %    SECTION                     PURPOSE IN NARRATIVE
─────────────────────────────────────────────────────────────
0-8%        Hero + living illustration  "Meet the monster" — emotional hook
8-12%       Stats grid                  "It's real" — credibility proof
12-18%      Feature cards               "Here's what it does" — value prop
18-25%      The Problem (MVCC Race)     "Here's why it exists" — tension
25-70%      7x SectionShells            "Here's how it works" — deep dive
            (each ~6% of scroll)         One concept per section
70-78%      Conflict resolution         "What about edge cases?" — realism
78-85%      Comparison table            "Better than alternatives" — proof
85-92%      Timeline                    "Built with care" — trust
92-100%     CTA + author flywheel       "Start using it" — resolution
```

### Entrance Choreography Timeline

```
t=0ms    User scrolls section into viewport
t=0ms    Left column begins: opacity 0→1, x -20→0 (800ms)
t=200ms  Right column begins: opacity 0→1, y 40→0 (1000ms)
t=200ms  DeferredViz triggers (if not already loaded from rootMargin preload)
t=800ms  Left column animation complete — title fully visible
t=1200ms Right column animation complete — visualization fully visible
t=1200ms+ Visualization interactive (hover/click handlers active)
```

### Cross-Viz State Flow

```
useSite() Context
    ├── playSfx("click") ← MVCC Race buttons
    ├── playSfx("zap")   ← Lightning arcs in flywheel
    ├── isAnatomyMode    ← Debug toggle affects all cards
    └── (no cross-viz hover coordination on homepage —
         each SectionShell is self-contained)
```

### Billboard Test Results

At every half-viewport scroll position:
- **Pass:** Sticky titles ensure text context is always visible alongside visualization
- **Pass:** DeferredViz with 600px rootMargin prevents skeleton-in-viewport
- **Pass:** Section padding (py-16 to py-48) prevents empty viewport gaps
- **One risk:** Between Acts (e.g., Features → Problem) there can be a brief "gap" — mitigated by `mb-32` spacing

---

## Quick Implementation Checklist

Before considering a page's scroll narrative complete:

- [ ] **Narrative arc identified**: Which template? What's the dramatic progression?
- [ ] **Scroll budget allocated**: Each section has deliberate vertical space
- [ ] **SectionShell pattern**: Sticky titles, staggered entrance, once-only animations
- [ ] **DeferredViz wrappers**: All heavy visualizations lazy-loaded with skeletons
- [ ] **Stagger formula chosen**: Linear, row-reset, or container variant
- [ ] **Billboard test passed**: Random viewport screenshots are coherent
- [ ] **Mobile restructuring**: Stacked layout, reduced padding, bottom sheets
- [ ] **One motion per viewport**: No competing animations
- [ ] **Scroll progress indicator**: For articles / long-form pages
- [ ] **Reduced motion support**: `skipAnim` flag throughout all entrance animations
- [ ] **Cross-viz state planned**: Context provider if visualizations need to coordinate
- [ ] **Breathing room verified**: Adequate padding between narrative acts
