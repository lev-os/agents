# Component Patterns — By Visualization Type

Detailed architecture patterns for each visualization category, distilled from production implementations.

---

## Stepper Visualizations

**When to use:** Visualizing any process with discrete steps — algorithms, protocols, pipelines, state machines.

**Production examples:** Bakery algorithm (5 steps), Cancel protocol (5 states), Encryption pipeline (7 steps), Query pipeline (6 layers), Conflict ladder (3 scenarios x 6 steps), Obligation flow (3 paths).

### Architecture

```
┌──────────────────────────────────────┐
│  StepperVisualization                │
│  ├─ state: { step, playing, speed } │
│  ├─ steps[]: StepDefinition[]       │
│  │                                   │
│  │  ┌─────────────────────────────┐  │
│  │  │  Visual Area (SVG/Canvas)   │  │
│  │  │  - Renders current step     │  │
│  │  │  - AnimatePresence for      │  │
│  │  │    enter/exit transitions   │  │
│  │  └─────────────────────────────┘  │
│  │                                   │
│  │  ┌─────────────────────────────┐  │
│  │  │  Description Panel          │  │
│  │  │  - Step title + explanation │  │
│  │  │  - Animated text swap       │  │
│  │  └─────────────────────────────┘  │
│  │                                   │
│  │  ┌─────────────────────────────┐  │
│  │  │  Stepper Controls           │  │
│  │  │  [Prev] [Play/Pause] [Next] │  │
│  │  │  ● ● ● ○ ○  step dots      │  │
│  │  └─────────────────────────────┘  │
│  └───────────────────────────────────┘
└──────────────────────────────────────┘
```

### Step Definition Pattern

```tsx
interface StepDefinition {
  id: string;
  title: string;
  description: string;
  // Visual state at this step
  activeNodes: string[];       // Which nodes are highlighted
  activeEdges: string[];       // Which connections are active
  nodeColors: Record<string, string>; // Override colors per node
  annotations?: { x: number; y: number; text: string }[];
}
```

### State Machine Visual Pattern

For algorithm walkthroughs where nodes represent states:

```tsx
const STATES = [
  { id: "idle",     label: "IDLE",     x: 100, y: 150, color: "#94a3b8" },
  { id: "choosing", label: "CHOOSING", x: 250, y: 150, color: "#22d3ee" },
  { id: "waiting",  label: "WAITING",  x: 400, y: 150, color: "#fbbf24" },
  { id: "critical", label: "CRITICAL", x: 550, y: 150, color: "#34d399" },
];

// Active state gets: glow filter, pulsing animation, brighter fill
// Inactive states get: dimmed opacity, no glow
// Transition arrows animate with strokeDashoffset
```

### Pipeline Visual Pattern

For data transformation pipelines (SQL query execution, encryption):

```tsx
const PIPELINE_LAYERS = [
  { id: "input",   label: "SQL Query",  y: 40,  color: "#38bdf8" },
  { id: "parser",  label: "Parser",     y: 100, color: "#a78bfa" },
  { id: "planner", label: "Planner",    y: 160, color: "#22d3ee" },
  { id: "vdbe",    label: "VDBE",       y: 220, color: "#34d399" },
  { id: "btree",   label: "B-tree",     y: 280, color: "#fbbf24" },
  { id: "storage", label: "Storage",    y: 340, color: "#f87171" },
];

// Active layer: full opacity, highlighted band
// Flow arrow animates downward between active and next layer
// Input/output boxes show transformed data at each stage
```

---

## Network Graphs

**When to use:** Showing relationships between entities — tool ecosystems, dependency graphs, synergy diagrams.

**Production examples:** Flywheel visualization (8-12 tools in circle), TLDR synergy diagram (6-8 tools), Agent flywheel (10+ nodes).

### Architecture

```
┌───────────────────────────────────────────┐
│  NetworkGraph                             │
│  ├─ nodes[]: positioned on circle/grid    │
│  ├─ edges[]: curved Bezier connections    │
│  ├─ hoveredId: string | null              │
│  ├─ selectedId: string | null             │
│  │                                        │
│  │  SVG Container (viewBox)               │
│  │  ├─ <defs> filters (glow, gradient)    │
│  │  ├─ Edge paths (background layer)      │
│  │  ├─ Node circles (foreground layer)    │
│  │  └─ Labels (topmost layer)             │
│  │                                        │
│  │  Detail Panel (conditional)            │
│  │  ├─ Desktop: side panel / HUD tooltip  │
│  │  └─ Mobile: bottom sheet               │
│  └────────────────────────────────────────┘
└───────────────────────────────────────────┘
```

### Circular Layout Calculation

```tsx
function getNodePosition(index: number, total: number, radius: number, center: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2; // Start at top
  return {
    x: center + Math.cos(angle) * radius,
    y: center + Math.sin(angle) * radius,
  };
}
```

### Connection Curve Generation

```tsx
function getCurvedPath(from: Point, to: Point, center: Point) {
  const midX = (from.x + to.x) / 2;
  const midY = (from.y + to.y) / 2;
  // Pull toward center for inward curves (organic feel)
  const controlX = midX + (center.x - midX) * 0.3;
  const controlY = midY + (center.y - midY) * 0.3;
  return `M ${from.x} ${from.y} Q ${controlX} ${controlY} ${to.x} ${to.y}`;
}
```

### Hover Highlighting Logic

```tsx
// Compute connected set once on hover change
const connectedIds = useMemo(() => {
  if (!hoveredId) return new Set<string>();
  const ids = new Set<string>([hoveredId]);
  edges.forEach((e) => {
    if (e.from === hoveredId) ids.add(e.to);
    if (e.to === hoveredId) ids.add(e.from);
  });
  return ids;
}, [hoveredId, edges]);

// Apply to nodes: connected = full opacity, others = dimmed
// Apply to edges: both endpoints connected = highlighted, others = faded
```

### Lightning Arc Effect (Advanced)

From the Flywheel visualization — jagged electrical connections:

```tsx
function getLightningPath(from: Point, to: Point, segments = 8) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  let d = `M ${from.x} ${from.y}`;

  for (let i = 1; i <= segments; i++) {
    const t = i / segments;
    const baseX = from.x + dx * t;
    const baseY = from.y + dy * t;
    // Random jitter perpendicular to the line
    const jitter = (Math.random() - 0.5) * 15;
    const perpX = -dy / Math.sqrt(dx * dx + dy * dy) * jitter;
    const perpY = dx / Math.sqrt(dx * dx + dy * dy) * jitter;
    d += ` L ${baseX + perpX} ${baseY + perpY}`;
  }
  return d;
}

// Re-generate path every 60-120ms for flickering effect
useEffect(() => {
  const interval = setInterval(() => {
    setPath(getLightningPath(from, to));
  }, 60 + Math.random() * 60);
  return () => clearInterval(interval);
}, [from, to]);
```

---

## Particle Systems

**When to use:** High-volume animated elements — data flows, encoding processes, ambient backgrounds, 3D scenes.

**Production examples:** Three Scene (5000 particles), RaptorQ healing, Neural fragments, Glow orbits.

### Architecture

```
┌────────────────────────────────────────┐
│  ParticleSystem                        │
│  ├─ quality: QualitySettings           │
│  ├─ particles[]: ref (not state!)      │
│  ├─ canvasRef / threeRef               │
│  ├─ animationFrameRef                  │
│  │                                     │
│  │  Rendering target:                  │
│  │  ├─ Canvas 2D (simple particles)    │
│  │  ├─ Three.js Points (3D)           │
│  │  └─ SVG circles (<100 particles)   │
│  │                                     │
│  │  Animation loop:                    │
│  │  ├─ RAF updates particle positions  │
│  │  ├─ Visibility-gated (pause if      │
│  │  │   off-screen)                    │
│  │  └─ Quality-scaled count            │
│  └─────────────────────────────────────┘
└────────────────────────────────────────┘
```

### Particle with Physics

```tsx
interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;    // 0-1, decreasing
  color: string;
  size: number;
}

function updateParticles(particles: Particle[], dt: number) {
  for (const p of particles) {
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.life -= dt * 0.5;  // Decay rate
    // Optional: gravity, attraction, boundaries
  }
  // Remove dead particles
  return particles.filter((p) => p.life > 0);
}
```

### Three.js Points Pattern (from Three Scene)

```tsx
import { Points, PointMaterial } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";

function ParticleField({ count }: { count: number }) {
  const ref = useRef<THREE.Points>(null);

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }
    return pos;
  }, [count]);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    ref.current.rotation.y = clock.elapsedTime * 0.05;
  });

  return (
    <Points ref={ref} positions={positions} stride={3}>
      <PointMaterial
        transparent
        color="#22d3ee"
        size={0.05}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
}
```

---

## Scroll-Triggered Animations

**When to use:** Sequential content that should reveal as the user reads — timelines, statistics, narrative sections.

**Production examples:** Timeline, Stats Grid, Market Cap Drop, Two Worlds parallax.

### Framer Motion whileInView

```tsx
<motion.div
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-50px" }}
  transition={{ duration: 0.5, delay: index * 0.1 }}
>
  {content}
</motion.div>
```

### Scroll-Linked Parallax (from Two Worlds)

```tsx
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start end", "end start"],
});

const leftY = useTransform(scrollYProgress, [0, 1], ["0%", "15%"]);
const rightY = useTransform(scrollYProgress, [0, 1], ["0%", "-15%"]);
const centerGlow = useTransform(scrollYProgress, [0, 0.5, 1], [0.3, 1, 0.3]);
```

### Staggered Container Pattern

```tsx
const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.21, 0.47, 0.32, 0.98] },
  },
};

<motion.ul variants={containerVariants} initial="hidden" whileInView="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

---

## Live Simulations

**When to use:** Real-time processes with adjustable parameters — MVCC race conditions, WAL lanes, physics simulations.

**Production examples:** MVCC Race (writer count, conflict probability, speed), WAL Lanes, Problem Scenario.

### Architecture

```
┌─────────────────────────────────────────┐
│  LiveSimulation                         │
│  ├─ params: useRef (avoids stale        │
│  │   closures in RAF)                   │
│  ├─ rafId: useRef                       │
│  ├─ isPlaying: useState                 │
│  │                                      │
│  │  Controls Panel:                     │
│  │  ├─ Sliders (range inputs)           │
│  │  ├─ Play/Pause button                │
│  │  └─ Reset button                     │
│  │                                      │
│  │  Visualization Area:                 │
│  │  ├─ Live-updating SVG/Canvas         │
│  │  └─ Real-time metrics display        │
│  │                                      │
│  │  Metrics Panel:                      │
│  │  ├─ TPS / throughput                 │
│  │  ├─ Conflict count                   │
│  │  └─ Completion percentage            │
│  └──────────────────────────────────────┘
└─────────────────────────────────────────┘
```

### RAF Loop with Refs (Critical Pattern)

```tsx
const paramsRef = useRef({ writerCount: 4, conflictProb: 0.3, speed: 1.0 });
const stateRef = useRef<SimState>(initialState());
const rafRef = useRef<number>(0);
const [displayState, setDisplayState] = useState<SimState>(initialState());

// Update params without re-creating RAF loop
const handleWriterCountChange = (val: number) => {
  paramsRef.current.writerCount = val;
};

// RAF loop reads from refs, writes to state periodically
useEffect(() => {
  if (!isPlaying) return;

  let lastUpdate = 0;
  const tick = (timestamp: number) => {
    const dt = (timestamp - lastUpdate) / 1000 * paramsRef.current.speed;
    lastUpdate = timestamp;

    // Update simulation (ref, no re-render)
    stateRef.current = stepSimulation(stateRef.current, paramsRef.current, dt);

    // Flush to React state at ~30fps for display
    if (timestamp % 33 < 16) {
      setDisplayState({ ...stateRef.current });
    }

    rafRef.current = requestAnimationFrame(tick);
  };

  lastUpdate = performance.now();
  rafRef.current = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(rafRef.current);
}, [isPlaying]);
```

### Slider Controls Pattern

```tsx
<label className="flex flex-col gap-1 text-xs text-slate-400">
  <span>Writers: {writerCount}</span>
  <input
    type="range"
    min={1}
    max={8}
    value={writerCount}
    onChange={(e) => {
      const val = Number(e.target.value);
      setWriterCount(val);
      paramsRef.current.writerCount = val;
    }}
    className="w-full accent-cyan-400"
  />
</label>
```

---

## Comparative Views

**When to use:** Teaching "why X is better than Y" or "how A differs from B."

**Production examples:** Tokio vs Asupersync, B-tree vs ECS Storage, CALM Theorem monotone vs non-monotone.

### Side-by-Side Synchronized Pattern

```tsx
function ComparisonViz() {
  const [step, setStep] = useState(0);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Left: "Without" / "Before" / "Approach A" */}
      <div className="border border-red-500/20 rounded-xl p-4 bg-red-950/5">
        <h3 className="text-red-400 text-sm font-mono mb-3">Without Asupersync</h3>
        <ApproachA step={step} />
      </div>

      {/* Right: "With" / "After" / "Approach B" */}
      <div className="border border-emerald-500/20 rounded-xl p-4 bg-emerald-950/5">
        <h3 className="text-emerald-400 text-sm font-mono mb-3">With Asupersync</h3>
        <ApproachB step={step} />
      </div>

      {/* Shared controls */}
      <div className="col-span-full">
        <Stepper totalSteps={6} onStepChange={setStep} autoPlayInterval={2000} />
      </div>
    </div>
  );
}
```

### Key principle: **identical visual structure, contrasting outcomes.** Both sides should use the same layout, same number of elements, same animation timing. Only the behavior/result should differ.

### Tabbed Comparison Pattern

When two views can't be shown simultaneously:

```tsx
const [activeTab, setActiveTab] = useState<"monotone" | "non-monotone">("monotone");

<div className="flex gap-2 mb-4">
  {(["monotone", "non-monotone"] as const).map((tab) => (
    <button
      key={tab}
      onClick={() => setActiveTab(tab)}
      className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
        activeTab === tab
          ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
          : "bg-slate-800 text-slate-400 border border-slate-700"
      }`}
    >
      {tab === "monotone" ? "Monotone (Fast)" : "Non-Monotone (Blocked)"}
    </button>
  ))}
</div>

<AnimatePresence mode="wait">
  <motion.div
    key={activeTab}
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
  >
    {activeTab === "monotone" ? <MonotoneView /> : <NonMonotoneView />}
  </motion.div>
</AnimatePresence>
```

---

## Tree Visualizations

**When to use:** Hierarchical data — B-trees, DOM trees, region trees, version chains.

**Production examples:** B-tree Page Explorer, COW B-tree, Region Tree.

### SVG Tree Layout

```tsx
interface TreeNode {
  id: string;
  label: string;
  children: string[];
  x: number;
  y: number;
  level: number;
}

// Compute positions (simple level-based layout)
function layoutTree(root: TreeNode, nodes: Map<string, TreeNode>) {
  const LEVEL_HEIGHT = 80;
  const NODE_WIDTH = 60;

  function layout(nodeId: string, level: number, xOffset: number): number {
    const node = nodes.get(nodeId)!;
    node.level = level;
    node.y = level * LEVEL_HEIGHT + 40;

    if (node.children.length === 0) {
      node.x = xOffset + NODE_WIDTH / 2;
      return NODE_WIDTH;
    }

    let totalWidth = 0;
    for (const childId of node.children) {
      totalWidth += layout(childId, level + 1, xOffset + totalWidth);
    }

    node.x = xOffset + totalWidth / 2;
    return totalWidth;
  }

  layout(root.id, 0, 0);
}
```

### Animated Path Highlight

For showing traversal through a tree:

```tsx
function TreePath({ path, nodes }: { path: string[]; nodes: Map<string, TreeNode> }) {
  return (
    <>
      {path.map((nodeId, i) => {
        const node = nodes.get(nodeId)!;
        const next = i < path.length - 1 ? nodes.get(path[i + 1])! : null;

        return (
          <g key={nodeId}>
            {/* Highlighted node */}
            <motion.circle
              cx={node.x} cy={node.y} r={20}
              fill="#22d3ee"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: i * 0.3, ...springs.snappy }}
            />
            {/* Animated edge to next */}
            {next && (
              <motion.line
                x1={node.x} y1={node.y + 20}
                x2={next.x} y2={next.y - 20}
                stroke="#22d3ee"
                strokeWidth={2}
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ delay: i * 0.3 + 0.15, duration: 0.3 }}
              />
            )}
          </g>
        );
      })}
    </>
  );
}
```

### Copy-on-Write Visual Pattern

From the COW B-tree — shows version chains when nodes are modified:

```tsx
// Original node: solid border
// Shadow copy: dashed border + slight offset + connection to original
// Version label on each node

<motion.g>
  {/* Shadow copy (new version) */}
  <rect
    x={node.x + 8} y={node.y - 8}
    width={60} height={30}
    rx={4}
    fill="#0f172a"
    stroke="#22d3ee"
    strokeDasharray="4 2"
  />
  <text className="fill-cyan-400 text-[9px]">v{node.version + 1}</text>

  {/* Original node */}
  <rect
    x={node.x} y={node.y}
    width={60} height={30}
    rx={4}
    fill="#1e293b"
    stroke="#64748b"
  />
  <text className="fill-slate-300 text-[9px]">v{node.version}</text>
</motion.g>
```
