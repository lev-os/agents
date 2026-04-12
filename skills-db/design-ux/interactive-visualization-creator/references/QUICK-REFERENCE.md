# Quick Reference — Interactive Visualization Patterns

Copy-paste starter patterns for every visualization type. All patterns are TypeScript, React 19+, Next.js 16+, Framer Motion 12+.

---

## Stepper Component

The universal temporal controller used in 30+ production visualizations:

```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface StepperProps {
  totalSteps: number;
  onStepChange: (step: number) => void;
  autoPlayInterval?: number; // ms, 0 = disabled
  labels?: string[];
  compact?: boolean;
}

export function Stepper({
  totalSteps,
  onStepChange,
  autoPlayInterval = 0,
  labels,
  compact = false,
}: StepperProps) {
  const [current, setCurrent] = useState(0);
  const [playing, setPlaying] = useState(false);

  const goTo = useCallback(
    (step: number) => {
      const clamped = Math.max(0, Math.min(totalSteps - 1, step));
      setCurrent(clamped);
      onStepChange(clamped);
    },
    [totalSteps, onStepChange]
  );

  // Auto-play
  useEffect(() => {
    if (!playing || autoPlayInterval <= 0) return;
    const id = setInterval(() => {
      setCurrent((prev) => {
        const next = prev < totalSteps - 1 ? prev + 1 : 0;
        onStepChange(next);
        return next;
      });
    }, autoPlayInterval);
    return () => clearInterval(id);
  }, [playing, autoPlayInterval, totalSteps, onStepChange]);

  // Keyboard support
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") goTo(current + 1);
      else if (e.key === "ArrowLeft") goTo(current - 1);
      else if (e.key === " ") {
        e.preventDefault();
        setPlaying((p) => !p);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [current, goTo]);

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={() => goTo(current - 1)}
        disabled={current === 0}
        className="rounded-md px-3 py-1.5 text-sm bg-slate-800 text-slate-300
                   hover:bg-slate-700 disabled:opacity-30 transition-colors"
        aria-label="Previous step"
      >
        Prev
      </button>

      {autoPlayInterval > 0 && (
        <button
          onClick={() => setPlaying((p) => !p)}
          className="rounded-md px-3 py-1.5 text-sm bg-slate-800 text-slate-300
                     hover:bg-slate-700 transition-colors"
          aria-label={playing ? "Pause" : "Play"}
        >
          {playing ? "Pause" : "Play"}
        </button>
      )}

      {!compact && (
        <div className="flex gap-1.5">
          {Array.from({ length: totalSteps }, (_, i) => (
            <button
              key={i}
              onClick={() => goTo(i)}
              className={`h-2 w-2 rounded-full transition-all duration-200 ${
                i === current
                  ? "bg-cyan-400 scale-125"
                  : i < current
                    ? "bg-slate-500"
                    : "bg-slate-700"
              }`}
              aria-label={labels?.[i] ?? `Step ${i + 1}`}
            />
          ))}
        </div>
      )}

      {labels?.[current] && (
        <span className="text-xs text-slate-400 font-mono">
          {labels[current]}
        </span>
      )}

      <button
        onClick={() => goTo(current + 1)}
        disabled={current === totalSteps - 1}
        className="rounded-md px-3 py-1.5 text-sm bg-slate-800 text-slate-300
                   hover:bg-slate-700 disabled:opacity-30 transition-colors"
        aria-label="Next step"
      >
        Next
      </button>
    </div>
  );
}
```

---

## Intersection Observer Lazy Init

The most critical performance pattern - used in every heavy visualization:

```tsx
import { useRef, useEffect, useState } from "react";

function useIntersectionInit(
  callback: () => (() => void) | void,
  rootMargin = "200px"
) {
  const ref = useRef<HTMLDivElement>(null);
  const initialized = useRef(false);
  const cleanupRef = useRef<(() => void) | void>();

  useEffect(() => {
    if (!ref.current) return;
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
    observer.observe(ref.current);
    return () => {
      observer.disconnect();
      cleanupRef.current?.();
    };
  }, [callback, rootMargin]);

  return ref;
}

// Usage:
function HeavyVisualization() {
  const ref = useIntersectionInit(() => {
    // Initialize expensive resources (Three.js, Canvas, etc.)
    const renderer = new THREE.WebGLRenderer();
    return () => renderer.dispose(); // Cleanup
  });

  return <div ref={ref} className="h-[400px]" />;
}
```

---

## Visibility-Gated Animation Hook

For components that should pause when off-screen:

```tsx
function useVisibilityAnimation() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => setIsVisible(entry.isIntersecting),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}
```

---

## SVG Network Graph (Flywheel Pattern)

Circular node layout with curved connections and hover highlighting:

```tsx
"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";

interface Node {
  id: string;
  label: string;
  color: string;
}

interface Edge {
  from: string;
  to: string;
  label?: string;
}

const SIZE = 600;
const CENTER = SIZE / 2;
const RADIUS = SIZE * 0.38;

function getNodePosition(index: number, total: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2;
  return {
    x: CENTER + Math.cos(angle) * RADIUS,
    y: CENTER + Math.sin(angle) * RADIUS,
  };
}

function getCurvedPath(
  from: { x: number; y: number },
  to: { x: number; y: number }
) {
  const midX = (from.x + to.x) / 2;
  const midY = (from.y + to.y) / 2;
  // Pull control point toward center for natural curves
  const controlX = midX + (CENTER - midX) * 0.3;
  const controlY = midY + (CENTER - midY) * 0.3;
  return `M ${from.x} ${from.y} Q ${controlX} ${controlY} ${to.x} ${to.y}`;
}

export function NetworkGraph({
  nodes,
  edges,
}: {
  nodes: Node[];
  edges: Edge[];
}) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  const positions = useMemo(
    () =>
      nodes.map((node, i) => ({
        ...node,
        ...getNodePosition(i, nodes.length),
      })),
    [nodes]
  );

  const connectedIds = useMemo(() => {
    if (!hoveredId) return new Set<string>();
    const ids = new Set<string>();
    edges.forEach((e) => {
      if (e.from === hoveredId) ids.add(e.to);
      if (e.to === hoveredId) ids.add(e.from);
    });
    ids.add(hoveredId);
    return ids;
  }, [hoveredId, edges]);

  const nodeMap = useMemo(
    () => new Map(positions.map((p) => [p.id, p])),
    [positions]
  );

  return (
    <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="w-full max-w-lg mx-auto">
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Edges */}
      {edges.map((edge, i) => {
        const from = nodeMap.get(edge.from);
        const to = nodeMap.get(edge.to);
        if (!from || !to) return null;
        const isHighlighted =
          hoveredId && (connectedIds.has(edge.from) && connectedIds.has(edge.to));
        return (
          <motion.path
            key={i}
            d={getCurvedPath(from, to)}
            fill="none"
            stroke={isHighlighted ? "#22d3ee" : "#334155"}
            strokeWidth={isHighlighted ? 2 : 1}
            animate={{ opacity: hoveredId ? (isHighlighted ? 0.8 : 0.15) : 0.4 }}
            transition={{ duration: 0.2 }}
          />
        );
      })}

      {/* Nodes */}
      {positions.map((node) => {
        const isActive =
          !hoveredId || connectedIds.has(node.id);
        return (
          <motion.g
            key={node.id}
            onMouseEnter={() => setHoveredId(node.id)}
            onMouseLeave={() => setHoveredId(null)}
            animate={{ opacity: isActive ? 1 : 0.3 }}
            className="cursor-pointer"
          >
            <motion.circle
              cx={node.x}
              cy={node.y}
              r={hoveredId === node.id ? 28 : 24}
              fill={node.color}
              filter={hoveredId === node.id ? "url(#glow)" : undefined}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            />
            <text
              x={node.x}
              y={node.y}
              textAnchor="middle"
              dominantBaseline="central"
              className="fill-white text-[10px] font-bold pointer-events-none"
            >
              {node.label}
            </text>
          </motion.g>
        );
      })}
    </svg>
  );
}
```

---

## Spring Physics Constants

Battle-tested spring configurations from production:

```tsx
// Framer Motion spring presets
const springs = {
  // Smooth, natural movement (default for most things)
  smooth: { type: "spring" as const, stiffness: 200, damping: 25 },

  // Snappy reaction (buttons, toggles)
  snappy: { type: "spring" as const, stiffness: 400, damping: 35 },

  // Gentle float (background elements, parallax)
  gentle: { type: "spring" as const, stiffness: 100, damping: 20 },

  // Quick response (cursor tracking, hover)
  quick: { type: "spring" as const, stiffness: 300, damping: 20 },

  // Magnetic attraction (interactive elements)
  magnetic: { type: "spring" as const, stiffness: 150, damping: 15, mass: 0.1 },

  // Pupil/eye tracking
  tracking: { type: "spring" as const, stiffness: 250, damping: 20 },

  // Layout transitions
  layout: { type: "spring" as const, stiffness: 350, damping: 30 },
};
```

---

## Reduced Motion Support

Always implement. Non-negotiable:

```tsx
import { useReducedMotion } from "framer-motion";

function Visualization() {
  const prefersReducedMotion = useReducedMotion();

  // Option 1: Show static final state
  if (prefersReducedMotion) {
    return <StaticFallback />;
  }

  // Option 2: Conditional animation props
  return (
    <motion.div
      initial={prefersReducedMotion ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={prefersReducedMotion ? { duration: 0 } : springs.smooth}
    />
  );
}
```

---

## Quality Tier System

For particle systems and 3D scenes:

```tsx
type QualityTier = "low" | "medium" | "high";

interface QualitySettings {
  particleMultiplier: number;
  shadowsEnabled: boolean;
  postProcessing: boolean;
  geometryDetail: number; // subdivision level
}

const QUALITY_PRESETS: Record<QualityTier, QualitySettings> = {
  low:    { particleMultiplier: 0.2, shadowsEnabled: false, postProcessing: false, geometryDetail: 1 },
  medium: { particleMultiplier: 0.5, shadowsEnabled: true,  postProcessing: false, geometryDetail: 2 },
  high:   { particleMultiplier: 1.0, shadowsEnabled: true,  postProcessing: true,  geometryDetail: 4 },
};

function detectQualityTier(): QualityTier {
  if (typeof window === "undefined") return "medium";

  const isMobile = /Android|iPhone|iPad/.test(navigator.userAgent);
  const cores = navigator.hardwareConcurrency ?? 4;
  const memory = (navigator as any).deviceMemory ?? 4; // GB

  if (isMobile || cores <= 2 || memory <= 2) return "low";
  if (cores >= 8 && memory >= 8) return "high";
  return "medium";
}

function scaleCount(baseCount: number, quality: QualitySettings): number {
  return Math.max(10, Math.floor(baseCount * quality.particleMultiplier));
}
```

---

## Haptic Feedback Hook

For touch device tactile feedback:

```tsx
function useHapticFeedback() {
  const vibrate = (pattern: number | number[]) => {
    if (typeof navigator !== "undefined" && "vibrate" in navigator) {
      navigator.vibrate(pattern);
    }
  };

  return {
    lightTap: () => vibrate(10),
    mediumTap: () => vibrate(25),
    heavyTap: () => vibrate(50),
    errorBuzz: () => vibrate([30, 50, 30]),
  };
}
```

---

## Mouse Parallax with Spring Physics

For background elements that follow cursor:

```tsx
import { useMotionValue, useSpring, useTransform } from "framer-motion";

function useMouseParallax(strength = 60) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springX = useSpring(mouseX, { damping: 50, stiffness: 100 });
  const springY = useSpring(mouseY, { damping: 50, stiffness: 100 });

  const parallaxX = useTransform(
    springX,
    (val) => (val / (typeof window !== "undefined" ? window.innerWidth : 1) - 0.5) * -strength
  );
  const parallaxY = useTransform(
    springY,
    (val) => (val / (typeof window !== "undefined" ? window.innerHeight : 1) - 0.5) * -strength
  );

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };
    window.addEventListener("mousemove", handler, { passive: true });
    return () => window.removeEventListener("mousemove", handler);
  }, [mouseX, mouseY]);

  return { parallaxX, parallaxY };
}
```

---

## Magnetic Element Wrapper

For elements that lean toward the cursor:

```tsx
import { motion, useSpring } from "framer-motion";
import { useRef } from "react";

function Magnetic({
  children,
  strength = 0.3,
}: {
  children: React.ReactNode;
  strength?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const x = useSpring(0, { stiffness: 150, damping: 15, mass: 0.1 });
  const y = useSpring(0, { stiffness: 150, damping: 15, mass: 0.1 });

  return (
    <motion.div
      ref={ref}
      style={{ x, y }}
      onMouseMove={(e) => {
        if (!ref.current) return;
        const rect = ref.current.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        x.set((e.clientX - centerX) * strength);
        y.set((e.clientY - centerY) * strength);
      }}
      onMouseLeave={() => {
        x.set(0);
        y.set(0);
      }}
    >
      {children}
    </motion.div>
  );
}
```

---

## Animated Number (Scroll-Triggered Counter)

```tsx
import { useRef, useState, useEffect } from "react";

const easeOutExpo = (t: number) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));

function AnimatedNumber({
  value,
  duration = 2000,
  prefix = "",
  suffix = "",
  decimals = 0,
}: {
  value: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
}) {
  const [count, setCount] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);
  const hasAnimated = useRef(false);

  // Intersection trigger
  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated.current) {
          setIsVisible(true);
          hasAnimated.current = true;
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  // Animation
  useEffect(() => {
    if (!isVisible) return;

    // Respect reduced motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setCount(value);
      return;
    }

    let startTime: number;
    let frameId: number;
    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      setCount(easeOutExpo(progress) * value);
      if (progress < 1) frameId = requestAnimationFrame(animate);
    };
    frameId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameId);
  }, [isVisible, value, duration]);

  return (
    <span ref={ref}>
      {prefix}
      {count.toFixed(decimals)}
      {suffix}
    </span>
  );
}
```

---

## Comparative Side-by-Side Layout

```tsx
function ComparativeView({
  leftTitle,
  rightTitle,
  leftContent,
  rightContent,
  leftColor = "red",
  rightColor = "emerald",
}: {
  leftTitle: string;
  rightTitle: string;
  leftContent: React.ReactNode;
  rightContent: React.ReactNode;
  leftColor?: string;
  rightColor?: string;
}) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className={`rounded-xl border border-${leftColor}-500/20 bg-${leftColor}-950/10 p-4`}>
        <h3 className={`text-sm font-mono text-${leftColor}-400 mb-3`}>
          {leftTitle}
        </h3>
        {leftContent}
      </div>
      <div className={`rounded-xl border border-${rightColor}-500/20 bg-${rightColor}-950/10 p-4`}>
        <h3 className={`text-sm font-mono text-${rightColor}-400 mb-3`}>
          {rightTitle}
        </h3>
        {rightContent}
      </div>
    </div>
  );
}
```

---

## Touch Detection Utility

```tsx
function useTouchDevice() {
  const [isTouch, setIsTouch] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(hover: hover) and (pointer: fine)");
    setIsTouch(!mq.matches);

    const handler = (e: MediaQueryListEvent) => setIsTouch(!e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return isTouch;
}
```

---

## RAF-Based Mouse Tracking (High Performance)

For custom cursors, eye tracking, etc. Uses refs to avoid re-renders:

```tsx
function useRAFMouseTracking(
  onUpdate: (x: number, y: number) => void,
  enabled = true
) {
  const frameRef = useRef<number>(0);
  const posRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    if (!enabled) return;

    const onMove = (e: MouseEvent) => {
      posRef.current = { x: e.clientX, y: e.clientY };
    };

    const flush = () => {
      onUpdate(posRef.current.x, posRef.current.y);
      frameRef.current = requestAnimationFrame(flush);
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    frameRef.current = requestAnimationFrame(flush);

    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(frameRef.current);
    };
  }, [onUpdate, enabled]);
}
```

---

## SVG Glow Filter (Reusable)

```xml
<defs>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
  <filter id="strongGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="8" result="blur" />
    <feComposite in="blur" in2="SourceGraphic" operator="over" />
  </filter>
</defs>
```

---

## Dynamic Import for Heavy Components

```tsx
import dynamic from "next/dynamic";

const HeavyVisualization = dynamic(
  () => import("@/components/heavy-visualization"),
  {
    ssr: false,
    loading: () => (
      <div className="h-[400px] bg-slate-900/50 rounded-xl animate-pulse
                      flex items-center justify-center text-slate-500 text-sm">
        Loading visualization...
      </div>
    ),
  }
);
```

---

## State Machine Visualization Skeleton

```tsx
interface State {
  id: string;
  label: string;
  color: string;
  x: number;
  y: number;
}

interface Transition {
  from: string;
  to: string;
  label: string;
}

function StateMachineViz({
  states,
  transitions,
  activeStateId,
}: {
  states: State[];
  transitions: Transition[];
  activeStateId: string;
}) {
  return (
    <svg viewBox="0 0 600 300" className="w-full">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b" />
        </marker>
      </defs>

      {/* Transition arrows */}
      {transitions.map((t, i) => {
        const from = states.find((s) => s.id === t.from)!;
        const to = states.find((s) => s.id === t.to)!;
        return (
          <g key={i}>
            <line
              x1={from.x} y1={from.y} x2={to.x} y2={to.y}
              stroke="#475569" strokeWidth="1.5"
              markerEnd="url(#arrow)"
            />
            <text
              x={(from.x + to.x) / 2}
              y={(from.y + to.y) / 2 - 8}
              textAnchor="middle"
              className="fill-slate-500 text-[9px]"
            >
              {t.label}
            </text>
          </g>
        );
      })}

      {/* State nodes */}
      {states.map((state) => (
        <motion.g key={state.id}>
          <motion.circle
            cx={state.x} cy={state.y} r={30}
            fill={state.id === activeStateId ? state.color : "#1e293b"}
            stroke={state.color}
            strokeWidth={state.id === activeStateId ? 3 : 1.5}
            animate={{
              scale: state.id === activeStateId ? [1, 1.05, 1] : 1,
            }}
            transition={{
              repeat: state.id === activeStateId ? Infinity : 0,
              duration: 2,
            }}
          />
          <text
            x={state.x} y={state.y}
            textAnchor="middle" dominantBaseline="central"
            className="fill-white text-[10px] font-mono pointer-events-none"
          >
            {state.label}
          </text>
        </motion.g>
      ))}
    </svg>
  );
}
```
