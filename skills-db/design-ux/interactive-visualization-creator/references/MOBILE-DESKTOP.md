# Mobile & Desktop — Device-Specific Interaction Strategies

Comprehensive guide to building visualizations that excel on both desktop and mobile, drawn from production implementations.

---

## The Core Principle

Desktop and mobile are not variations of each other. They are fundamentally different interaction paradigms that happen to render the same content. Build separate interaction paths, not responsive compromises.

| Dimension | Desktop | Mobile |
|-----------|---------|--------|
| Primary input | Mouse pointer (precise, hover-capable) | Touch (imprecise, no hover) |
| Secondary input | Keyboard | Gestures (swipe, pinch) |
| Feedback | Visual (cursor, hover state) | Haptic (vibration) + Visual |
| Detail reveal | Tooltip / side panel | Bottom sheet / modal |
| Navigation | Click + hover + keyboard | Tap + swipe |
| Performance budget | High (8+ cores, 16GB+) | Low (4 cores, 3-4GB) |
| Screen real estate | Wide (1200px+) | Narrow (320-428px) |

---

## Device Detection

### Fine Pointer Detection (Preferred)

```tsx
// Detects mouse/trackpad vs touch
const hasFinePointer = window.matchMedia(
  "(hover: hover) and (pointer: fine)"
).matches;
```

This is the best test because:
- iPads with keyboard/trackpad attached report `pointer: fine`
- Laptops with touch screens report `pointer: fine` for the primary input
- It's about capability, not device type

### Mobile User-Agent Detection (For Quality Tiers)

```tsx
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
```

Use this only for quality tier decisions, not interaction model.

### Hardware Capability Detection

```tsx
const cores = navigator.hardwareConcurrency ?? 4;
const memory = (navigator as any).deviceMemory ?? 4; // GB, Chrome only
const isLowEnd = isMobile || cores <= 2 || memory <= 2;
```

---

## Interaction Patterns

### Hover → Tap Conversion

Desktop hover effects need a tap equivalent on mobile. The 900ms auto-dismiss pattern works well:

```tsx
function useDualInteraction(id: string) {
  const [active, setActive] = useState<string | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout>>();
  const isFine = useRef(false);

  useEffect(() => {
    isFine.current = window.matchMedia(
      "(hover: hover) and (pointer: fine)"
    ).matches;
  }, []);

  return {
    active,
    handlers: {
      // Desktop: instant hover
      onMouseEnter: () => isFine.current && setActive(id),
      onMouseLeave: () => isFine.current && setActive(null),
      // Mobile: tap to activate, auto-dismiss
      onTouchStart: (e: React.TouchEvent) => {
        if (isFine.current) return;
        e.stopPropagation();
        clearTimeout(timerRef.current);
        setActive(id);
        timerRef.current = setTimeout(() => setActive(null), 900);
      },
    },
  };
}
```

### Detail Panel → Bottom Sheet

Desktop side panels become bottom sheets on mobile:

```tsx
// Desktop: slide-in side panel
<AnimatePresence>
  {selectedNode && (
    <motion.div
      className="hidden md:block absolute right-0 top-0 w-80 h-full"
      initial={{ x: "100%" }}
      animate={{ x: 0 }}
      exit={{ x: "100%" }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <DetailPanel node={selectedNode} />
    </motion.div>
  )}
</AnimatePresence>

// Mobile: bottom sheet
<AnimatePresence>
  {selectedNode && (
    <motion.div
      className="md:hidden fixed inset-x-0 bottom-0 z-50 max-h-[70vh] overflow-y-auto
                 rounded-t-2xl bg-slate-900 border-t border-slate-700"
      initial={{ y: "100%" }}
      animate={{ y: 0 }}
      exit={{ y: "100%" }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <div className="w-12 h-1 bg-slate-600 rounded-full mx-auto mt-3" />
      <DetailPanel node={selectedNode} />
    </motion.div>
  )}
</AnimatePresence>
```

### Keyboard Navigation (Desktop Only)

```tsx
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    switch (e.key) {
      case "ArrowRight": nextStep(); break;
      case "ArrowLeft": prevStep(); break;
      case " ": e.preventDefault(); togglePlay(); break;
      case "Escape": closePanel(); break;
    }
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, [nextStep, prevStep, togglePlay, closePanel]);
```

### Haptic Feedback (Mobile Only)

```tsx
const haptics = useHapticFeedback();

// On step change
haptics.lightTap();

// On selection
haptics.mediumTap();

// On error/conflict
haptics.errorBuzz();
```

---

## Touch Target Sizing

### Minimum Sizes

| Element | Minimum Size | Recommended |
|---------|-------------|-------------|
| Button | 44x44px | 48x48px |
| Step indicator dot | 24x24px touch area | 32x32px |
| Node in graph | 40x40px | 48x48px |
| Close button | 44x44px | 48x48px |
| Slider thumb | 44px wide | 48px |

### Implementation

```tsx
// Visual size can be smaller than touch area
<button
  className="relative w-6 h-6"  // Visual: 24px
  style={{ padding: "12px", margin: "-12px" }}  // Touch: 48px
>
  <span className="block w-6 h-6 rounded-full bg-cyan-400" />
</button>

// Or use Tailwind's min-h/min-w
<button className="min-h-[44px] min-w-[44px] flex items-center justify-center">
  <Icon className="w-5 h-5" />
</button>
```

---

## Quality Tier Scaling

### Particle Systems

| Tier | Base Count | Max Elements | Shadows | Post-Processing |
|------|-----------|-------------|---------|-----------------|
| Low (mobile) | 200-1000 | 20 animated | Off | Off |
| Medium | 1000-2500 | 50 animated | On | Off |
| High (desktop) | 2500-5000 | 200 animated | On | On |

### Animation Complexity

| Tier | Behavior |
|------|----------|
| Low | No parallax, no custom cursor, simpler spring configs, fewer concurrent animations |
| Medium | Basic parallax, standard springs, moderate concurrent animations |
| High | Full parallax, custom cursor, complex springs, unlimited animations |

### Implementation

```tsx
const quality = useMemo(() => detectQualityTier(), []);

// Scale particle count
const particleCount = Math.floor(5000 * quality.particleMultiplier);

// Conditional features
{quality.tier !== "low" && <MouseParallax strength={60} />}
{quality.tier === "high" && <CustomCursor />}

// Spring tuning per tier
const springConfig = quality.tier === "low"
  ? { duration: 0.2 }  // Use duration instead of spring on low-end
  : springs.smooth;     // Full spring physics on medium/high
```

---

## Layout Strategies

### Visualization Container

```tsx
// Full-width on mobile, constrained on desktop
<div className="w-full max-w-2xl mx-auto px-4 sm:px-0">
  <svg viewBox="0 0 600 600" className="w-full">
    {/* SVG scales naturally via viewBox */}
  </svg>
</div>
```

### Network Graph Scaling

The Flywheel visualization uses CSS custom properties for scaling:

```tsx
// Container applies scale based on viewport
<div
  className="relative"
  style={{
    transform: `scale(${isMobile ? 0.5 : isTablet ? 0.85 : 1})`,
    transformOrigin: "top center",
  }}
>
  <svg viewBox="0 0 600 600">{/* ... */}</svg>
</div>
```

### Side-by-Side → Stacked

```tsx
// Desktop: side by side. Mobile: stacked
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <Panel title="Without" color="red" />
  <Panel title="With" color="emerald" />
</div>
```

### Stepper Controls

```tsx
// Desktop: full controls with dots
// Mobile: compact (no dots, just prev/next)
<Stepper
  compact={isMobile}
  totalSteps={steps.length}
  onStepChange={handleStep}
/>
```

---

## Custom Cursor (Desktop Only)

All four projects disable the custom cursor on mobile:

```tsx
function CustomCursor() {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    // Only enable on desktop with fine pointer
    const mq = window.matchMedia("(hover: hover) and (pointer: fine)");
    setEnabled(mq.matches);
    const handler = (e: MediaQueryListEvent) => setEnabled(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  if (!enabled) return null;

  return (
    <>
      <style>{`* { cursor: none !important; }`}</style>
      <CursorRenderer />
    </>
  );
}
```

---

## Scroll Behavior Considerations

### Body Scroll Lock for Modals

When opening bottom sheets or fullscreen modals on mobile:

```tsx
function useBodyScrollLock(locked: boolean) {
  useEffect(() => {
    if (!locked) return;
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, [locked]);
}
```

### Passive Event Listeners

For scroll and touch tracking:

```tsx
// CORRECT: passive listener (better scroll performance)
window.addEventListener("touchmove", handler, { passive: true });
window.addEventListener("scroll", handler, { passive: true });

// WRONG: non-passive (blocks scrolling)
window.addEventListener("touchmove", handler);
```

---

## Testing Checklist

### Mobile Testing (Not Just Browser Resize)

- [ ] Test on actual iOS Safari (different touch behavior than Chrome)
- [ ] Test on actual Android Chrome
- [ ] Test with device rotation (portrait → landscape)
- [ ] Test with system-level reduced motion enabled
- [ ] Test with large text / accessibility zoom
- [ ] Verify touch targets are >= 44px
- [ ] Verify no hover-dependent functionality on touch devices
- [ ] Verify bottom sheets don't overflow viewport
- [ ] Test swipe gestures don't conflict with browser back/forward

### Desktop Testing

- [ ] Test keyboard navigation (Tab, Arrow keys, Escape, Space)
- [ ] Test with trackpad (hover and fine click)
- [ ] Test with browser zoom (100%, 125%, 150%)
- [ ] Verify hover tooltips don't go off-screen
- [ ] Test with prefers-reduced-motion enabled
