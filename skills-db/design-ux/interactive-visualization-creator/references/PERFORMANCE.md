# Performance Optimization — Interactive Visualization Patterns

Every performance pattern proven across 100+ production visualizations. Visualizations that drop frames destroy both trust and teaching.

---

## The Performance Budget

| Metric | Target | Failure Threshold |
|--------|--------|-------------------|
| Time to Interactive | < 500ms | > 1000ms |
| Animation frame rate | 60fps | < 30fps |
| Largest Contentful Paint impact | < 200ms added | > 500ms added |
| Memory per visualization | < 50MB | > 100MB |
| Cumulative Layout Shift | 0 | > 0.1 |

---

## Principle 1: Lazy Initialization

Heavy visualizations must not initialize until approaching the viewport. This is the single highest-impact optimization.

### IntersectionObserver Pattern

```tsx
function useIntersectionInit(
  callback: () => (() => void) | void,
  rootMargin = "200px"
) {
  const ref = useRef<HTMLDivElement>(null);
  const initialized = useRef(false);
  const cleanupRef = useRef<(() => void) | void>();

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !initialized.current) {
          initialized.current = true;
          cleanupRef.current = callback();
          observer.disconnect();
        }
      },
      { rootMargin }
    );

    observer.observe(el);
    return () => {
      observer.disconnect();
      cleanupRef.current?.();
    };
  }, [callback, rootMargin]);

  return ref;
}
```

### Dynamic Import for Heavy Dependencies

```tsx
import dynamic from "next/dynamic";

const ThreeScene = dynamic(() => import("@/components/three-scene"), {
  ssr: false,
  loading: () => (
    <div className="h-[400px] animate-pulse bg-slate-900/50 rounded-xl
                    flex items-center justify-center">
      <span className="text-slate-500 text-sm">Loading 3D scene...</span>
    </div>
  ),
});
```

**Why `ssr: false`:** Three.js, Canvas, and WebGL require browser APIs. Server rendering will crash.

---

## Principle 2: useRef for High-Frequency Updates

React state updates trigger re-renders. At 60fps, that's 60 re-renders per second for mouse tracking alone. Use refs for anything that updates faster than ~10fps.

### The MotionValue Pattern (Best for Framer Motion)

```tsx
// NO re-renders. MotionValues update the DOM directly.
const cursorX = useMotionValue(0);
const cursorY = useMotionValue(0);

useEffect(() => {
  const handler = (e: MouseEvent) => {
    cursorX.set(e.clientX);
    cursorY.set(e.clientY);
  };
  window.addEventListener("mousemove", handler, { passive: true });
  return () => window.removeEventListener("mousemove", handler);
}, [cursorX, cursorY]);

// Consumed by motion.div's style prop — no re-render needed
<motion.div style={{ x: cursorX, y: cursorY }} />
```

### The Ref + RAF Pattern (Best for Canvas/WebGL)

```tsx
const posRef = useRef({ x: 0, y: 0 });
const frameRef = useRef<number>(0);

useEffect(() => {
  const onMove = (e: MouseEvent) => {
    posRef.current = { x: e.clientX, y: e.clientY };
  };

  const flush = () => {
    // Read from ref, write to canvas/WebGL
    drawAt(posRef.current.x, posRef.current.y);
    frameRef.current = requestAnimationFrame(flush);
  };

  window.addEventListener("mousemove", onMove, { passive: true });
  frameRef.current = requestAnimationFrame(flush);

  return () => {
    window.removeEventListener("mousemove", onMove);
    cancelAnimationFrame(frameRef.current);
  };
}, []);
```

### When to Use What

| Update Frequency | Pattern | Example |
|-----------------|---------|---------|
| 60fps (mouse, RAF) | MotionValue or ref | Custom cursor, parallax |
| 10-30fps (simulation) | Ref + periodic setState | MVCC race, physics sim |
| 1-5fps (UI state) | useState | Step change, selection |
| Once (init) | useMemo or useRef | Node positions, connections |

---

## Principle 3: Visibility-Gated Animation

Animations running off-screen waste CPU and battery. Pause them.

### The IntersectionObserver Visibility Gate

```tsx
function useVisibilityGate() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => setIsVisible(entry.isIntersecting),
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}

// Usage in animation loops:
useEffect(() => {
  if (!isVisible) return; // Don't start RAF when off-screen

  let frameId: number;
  const tick = () => {
    updateParticles();
    frameId = requestAnimationFrame(tick);
  };
  frameId = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(frameId);
}, [isVisible]);
```

### CSS containment

```tsx
// Tell the browser this element's layout is independent
<div style={{ contain: "layout paint style" }}>
  <HeavyVisualization />
</div>
```

---

## Principle 4: Memoize Expensive Calculations

Node positions, connection paths, and layout calculations should compute once.

```tsx
// GOOD: Compute positions once
const positions = useMemo(
  () => nodes.map((node, i) => ({
    ...node,
    ...getNodePosition(i, nodes.length),
  })),
  [nodes] // Only recompute if nodes array changes
);

// GOOD: Compute connected set only when hover changes
const connectedIds = useMemo(() => {
  if (!hoveredId) return new Set<string>();
  const ids = new Set<string>([hoveredId]);
  edges.forEach((e) => {
    if (e.from === hoveredId) ids.add(e.to);
    if (e.to === hoveredId) ids.add(e.from);
  });
  return ids;
}, [hoveredId, edges]);

// BAD: Recompute on every render
const positions = nodes.map((node, i) => ({
  ...node,
  ...getNodePosition(i, nodes.length),
})); // Runs on EVERY render!
```

---

## Principle 5: Avoid Layout Thrashing

Reading layout properties (getBoundingClientRect, offsetWidth, etc.) forces the browser to synchronously calculate layout. Batch reads before writes.

### Cache DOM Rects (From Franken Eye)

```tsx
const rectRef = useRef<DOMRect | null>(null);

function updateRect() {
  if (containerRef.current) {
    rectRef.current = containerRef.current.getBoundingClientRect();
  }
}

// Update on resize and scroll, not every frame
useEffect(() => {
  updateRect();
  window.addEventListener("resize", updateRect);
  window.addEventListener("scroll", updateRect, { passive: true });
  return () => {
    window.removeEventListener("resize", updateRect);
    window.removeEventListener("scroll", updateRect);
  };
}, []);

// In RAF loop, read from cache (no layout thrashing)
const tick = () => {
  const rect = rectRef.current;
  if (!rect) return;
  // Use rect.left, rect.top, etc. — no DOM read!
};
```

---

## Principle 6: Passive Event Listeners

Non-passive touch/scroll listeners block the main thread and cause jank.

```tsx
// ALWAYS use passive for scroll and touch tracking
window.addEventListener("scroll", handler, { passive: true });
window.addEventListener("touchmove", handler, { passive: true });
window.addEventListener("mousemove", handler, { passive: true });

// Only use non-passive when you NEED to call preventDefault()
// (e.g., preventing scroll in a custom drag handler)
element.addEventListener("touchmove", (e) => {
  e.preventDefault(); // Requires non-passive
  handleDrag(e);
}, { passive: false });
```

---

## Principle 7: Quality Tier Scaling

Scale computational complexity to device capability:

```tsx
const quality = detectQualityTier();

// Particle systems
const particleCount = Math.floor(BASE_COUNT * quality.particleMultiplier);

// Animation complexity
const enableParallax = quality.tier !== "low";
const enableCustomCursor = quality.tier !== "low";
const enablePostProcessing = quality.tier === "high";

// Spring vs duration
const transition = quality.tier === "low"
  ? { duration: 0.2 } // Cheaper than spring on low-end
  : { type: "spring", stiffness: 200, damping: 25 };

// Geometry detail (Three.js)
const segments = quality.tier === "low" ? 8 : quality.tier === "medium" ? 16 : 32;
```

---

## Principle 8: Clean Up Everything

Every RAF, interval, timeout, event listener, and WebGL context must be cleaned up on unmount.

```tsx
useEffect(() => {
  const rafId = requestAnimationFrame(tick);
  const intervalId = setInterval(update, 3000);
  const handler = (e: MouseEvent) => track(e);
  window.addEventListener("mousemove", handler, { passive: true });

  return () => {
    cancelAnimationFrame(rafId);
    clearInterval(intervalId);
    window.removeEventListener("mousemove", handler);
    // Dispose WebGL resources
    renderer?.dispose();
    geometry?.dispose();
    material?.dispose();
  };
}, []);
```

### Common cleanup failures:
- Forgotten `cancelAnimationFrame` → zombie animation loops
- Forgotten `clearInterval` → memory leak + phantom updates
- Forgotten WebGL `dispose()` → GPU memory leak
- Forgotten `removeEventListener` → memory leak + stale handlers

---

## Principle 9: Avoid CLS (Cumulative Layout Shift)

Visualizations that change size as they load cause jarring layout shifts.

```tsx
// GOOD: Reserve space before content loads
<div className="h-[400px] w-full relative">
  {loaded ? <Visualization /> : <Placeholder />}
</div>

// GOOD: Use aspect ratio to maintain space
<div className="aspect-square w-full max-w-lg mx-auto">
  <svg viewBox="0 0 600 600" className="w-full h-full">
    {/* ... */}
  </svg>
</div>

// BAD: Content pops in and pushes other content down
{loaded && <Visualization />}  // No space reserved!
```

---

## Principle 10: Virtual Scrolling for Large Datasets

For visualizations with 100+ items (spec evolution, commit lists, large tables):

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualizedList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48, // Estimated row height
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: "relative" }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Performance Debugging Checklist

When a visualization drops below 60fps:

1. **Open Chrome DevTools Performance tab** → Record → Identify long frames
2. **Check for layout thrashing**: Look for forced reflow warnings (purple bars)
3. **Check for excessive re-renders**: React DevTools Profiler → Highlight updates
4. **Check animation count**: How many simultaneous CSS/JS animations?
5. **Check particle count**: Is it scaled to device capability?
6. **Check event listeners**: Are scroll/mouse handlers passive?
7. **Check memoization**: Are expensive calculations cached with useMemo?
8. **Check cleanup**: Are all RAF/intervals cleaned up on unmount?
9. **Check off-screen**: Are invisible visualizations still animating?
10. **Check WebGL**: Is geometry/material disposed on unmount?
