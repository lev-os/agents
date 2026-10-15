# Lightning & Electricity Effects

## Overview

Three approaches: (1) Procedural fractal midpoint displacement (most practical, best bang-for-buck), (2) Lissajous curves for smooth arcs, (3) Fractal branching for Lichtenberg figures. All can be rendered via Canvas paths or Metal line rendering with additive bloom.

---

## Approach 1: Midpoint Displacement (Primary Recommendation)

The workhorse algorithm for game lightning. Used in Diablo, Dota 2, and most real-time games.

### Algorithm

1. Start with a line segment from A to B
2. Find the midpoint
3. Displace the midpoint perpendicular to the segment by a random amount
4. Recurse on each half-segment with reduced displacement scale
5. After 4-5 levels, you have a jagged bolt

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `levels` | 4-6 | Subdivision depth. 5 is the sweet spot (32 segments) |
| `jaggedness` | 0.0-1.0 | How far midpoints displace. 0.3-0.5 for natural lightning |
| `scaleReduction` | 0.45-0.55 | How much displacement shrinks per level. ~0.5 is standard |
| `thickness` | 2-6pt | Base stroke width. Taper from thick (origin) to thin (tip) |
| `refreshRate` | 4-12 Hz | How often to regenerate the bolt. 8Hz feels electric |

### Full Swift Implementation

```swift
import SwiftUI

struct LightningBolt {
    let points: [CGPoint]
    let thickness: CGFloat

    /// Generate a fractal lightning bolt via midpoint displacement
    static func generate(
        from start: CGPoint,
        to end: CGPoint,
        levels: Int = 5,
        jaggedness: CGFloat = 0.4,
        scaleReduction: CGFloat = 0.5
    ) -> LightningBolt {
        let totalLength = hypot(end.x - start.x, end.y - start.y)

        // Direction and perpendicular
        let dx = end.x - start.x
        let dy = end.y - start.y
        let len = hypot(dx, dy)
        let perpX = -dy / len
        let perpY = dx / len

        var points = [start, end]

        for level in 0..<levels {
            var newPoints: [CGPoint] = [points[0]]
            let maxDisplacement = jaggedness * totalLength * pow(scaleReduction, CGFloat(level))

            for i in 0..<(points.count - 1) {
                let a = points[i]
                let b = points[i + 1]
                let mid = CGPoint(
                    x: (a.x + b.x) / 2,
                    y: (a.y + b.y) / 2
                )

                // Displace perpendicular to the ORIGINAL direction (not segment direction)
                let offset = CGFloat.random(in: -maxDisplacement...maxDisplacement)
                let displaced = CGPoint(
                    x: mid.x + perpX * offset,
                    y: mid.y + perpY * offset
                )

                newPoints.append(displaced)
                newPoints.append(b)
            }
            points = newPoints
        }

        return LightningBolt(points: points, thickness: 3.0)
    }
}

struct LightningBoltView: View {
    let from: CGPoint
    let to: CGPoint
    let color: Color
    let glowColor: Color
    let refreshRate: Double  // Hz

    @State private var bolt: LightningBolt?
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        if reduceMotion {
            // Static line fallback
            Path { path in
                path.move(to: from)
                path.addLine(to: to)
            }
            .stroke(color, lineWidth: 2)
        } else {
            TimelineView(.animation(minimumInterval: 1.0 / refreshRate)) { ctx in
                Canvas { context, size in
                    // Regenerate bolt each frame
                    let currentBolt = LightningBolt.generate(from: from, to: to)

                    // Glow layer (wide, faint)
                    drawBoltPath(context: context, bolt: currentBolt, color: glowColor, widthMultiplier: 6.0, alpha: 0.15)

                    // Mid glow (medium)
                    drawBoltPath(context: context, bolt: currentBolt, color: glowColor, widthMultiplier: 3.0, alpha: 0.3)

                    // Core (bright, thin)
                    drawBoltPath(context: context, bolt: currentBolt, color: color, widthMultiplier: 1.0, alpha: 1.0)
                }
            }
        }
    }

    private func drawBoltPath(
        context: GraphicsContext,
        bolt: LightningBolt,
        color: Color,
        widthMultiplier: CGFloat,
        alpha: Double
    ) {
        guard bolt.points.count >= 2 else { return }

        var path = Path()
        path.move(to: bolt.points[0])
        for i in 1..<bolt.points.count {
            path.addLine(to: bolt.points[i])
        }

        var ctx = context
        ctx.opacity = alpha
        ctx.blendMode = .plusLighter  // additive for glow
        ctx.stroke(
            path,
            with: .color(color),
            style: StrokeStyle(
                lineWidth: bolt.thickness * widthMultiplier,
                lineCap: .round,
                lineJoin: .round
            )
        )
    }
}
```

### Usage

```swift
struct SpellView: View {
    var body: some View {
        ZStack {
            Color.black

            LightningBoltView(
                from: CGPoint(x: 100, y: 50),
                to: CGPoint(x: 300, y: 350),
                color: .white,
                glowColor: .cyan,
                refreshRate: 8
            )
        }
    }
}
```

### Rendering: The 3-Layer Glow Stack

The key to convincing lightning is NOT just the path -- it is layered glow:

| Layer | Width | Alpha | Blend Mode | Purpose |
|-------|-------|-------|------------|---------|
| Outer glow | 6x base | 0.10-0.15 | `.plusLighter` | Atmospheric scatter |
| Mid glow | 3x base | 0.25-0.35 | `.plusLighter` | Corona |
| Core | 1x base | 0.9-1.0 | `.plusLighter` | White-hot center |

This creates the bloom-like falloff without an actual bloom post-process pass.

---

## Approach 2: Lissajous Curves (Smooth Arcs)

For electricity that flows smoothly (Tesla coil, continuous arc, energy beam).

```swift
/// Generate a smooth electrical arc using Lissajous-like parametric curves
func generateArc(
    from start: CGPoint,
    to end: CGPoint,
    time: Double,
    segments: Int = 64,
    amplitude: CGFloat = 30,
    frequency: CGFloat = 5
) -> [CGPoint] {
    var points: [CGPoint] = []

    let dx = end.x - start.x
    let dy = end.y - start.y
    let len = hypot(dx, dy)
    let perpX = -dy / len
    let perpY = dx / len

    for i in 0...segments {
        let t = CGFloat(i) / CGFloat(segments)

        // Base position along the line
        var x = start.x + dx * t
        var y = start.y + dy * t

        // Lissajous displacement perpendicular to line
        let wave1 = sin(t * frequency * .pi * 2 + CGFloat(time) * 8) * amplitude
        let wave2 = sin(t * (frequency + 2) * .pi * 2 + CGFloat(time) * 12) * amplitude * 0.3
        let noise = sin(t * 17 + CGFloat(time) * 5) * amplitude * 0.15

        let offset = (wave1 + wave2 + noise) * sin(t * .pi)  // taper at endpoints

        x += perpX * offset
        y += perpY * offset

        points.append(CGPoint(x: x, y: y))
    }

    return points
}
```

**When to use Lissajous over midpoint displacement:**
- Continuous, flowing electricity (not a strike)
- Energy beams connecting two points
- Tesla coil arcs
- Tethering effects (linking two objects)

---

## Approach 3: Fractal Branching (Lichtenberg Figures)

For branching lightning trees (storm effects, ground strikes, shatter patterns).

### Algorithm

Starting from the main bolt, at each subdivision step there is a probability of spawning a branch:

1. Generate main bolt via midpoint displacement
2. At each midpoint, roll for branch probability (15-25% per point)
3. If branching, create a sub-bolt from that point at an angle offset
4. Sub-bolt has reduced length (60-70% of remaining), reduced thickness, reduced subdivision levels
5. Recurse up to max branch depth (2-3 levels)

### Parameters

| Parameter | Value | Effect |
|-----------|-------|--------|
| `branchProbability` | 0.15-0.25 | Chance of branch at each midpoint |
| `branchAngleVariation` | +/-30 deg | Angular spread of branches |
| `branchLengthDecay` | 0.60-0.70 | How much shorter each branch generation is |
| `branchThicknessDecay` | 0.50-0.65 | How much thinner each branch generation is |
| `maxBranchDepth` | 2-3 | Prevents exponential explosion |

### Implementation

```swift
struct LightningTree {
    struct Branch {
        let points: [CGPoint]
        let thickness: CGFloat
        let depth: Int
    }

    let branches: [Branch]

    static func generate(
        from start: CGPoint,
        to end: CGPoint,
        levels: Int = 5,
        jaggedness: CGFloat = 0.4,
        branchProbability: CGFloat = 0.2,
        branchAngleVariation: CGFloat = .pi / 6,  // 30 degrees
        branchLengthDecay: CGFloat = 0.65,
        branchThicknessDecay: CGFloat = 0.6,
        maxBranchDepth: Int = 2,
        baseThickness: CGFloat = 3.0
    ) -> LightningTree {
        var allBranches: [Branch] = []

        func buildBranch(
            from: CGPoint,
            to: CGPoint,
            depth: Int,
            thickness: CGFloat,
            subdivisions: Int
        ) {
            // Generate this branch
            let bolt = LightningBolt.generate(
                from: from,
                to: to,
                levels: subdivisions,
                jaggedness: jaggedness
            )
            allBranches.append(Branch(points: bolt.points, thickness: thickness, depth: depth))

            guard depth < maxBranchDepth else { return }

            // Check each midpoint for branching
            for i in stride(from: 2, to: bolt.points.count - 2, by: 2) {
                guard CGFloat.random(in: 0...1) < branchProbability else { continue }

                let branchStart = bolt.points[i]

                // Direction at this point
                let prev = bolt.points[i - 1]
                let next = bolt.points[min(i + 1, bolt.points.count - 1)]
                let dirX = next.x - prev.x
                let dirY = next.y - prev.y
                let dirLen = hypot(dirX, dirY)
                guard dirLen > 0 else { continue }

                // Rotate direction by random angle
                let baseAngle = atan2(dirY, dirX)
                let branchAngle = baseAngle + CGFloat.random(in: -branchAngleVariation...branchAngleVariation)

                // Branch endpoint
                let remainingLength = hypot(to.x - branchStart.x, to.y - branchStart.y) * branchLengthDecay
                let branchEnd = CGPoint(
                    x: branchStart.x + cos(branchAngle) * remainingLength,
                    y: branchStart.y + sin(branchAngle) * remainingLength
                )

                buildBranch(
                    from: branchStart,
                    to: branchEnd,
                    depth: depth + 1,
                    thickness: thickness * branchThicknessDecay,
                    subdivisions: max(2, subdivisions - 1)
                )
            }
        }

        buildBranch(
            from: start,
            to: end,
            depth: 0,
            thickness: baseThickness,
            subdivisions: levels
        )

        return LightningTree(branches: allBranches)
    }
}
```

### Rendering Branching Lightning

```swift
struct LightningTreeView: View {
    let tree: LightningTree

    var body: some View {
        Canvas { context, size in
            // Render branches back-to-front (deepest first for proper layering)
            let sorted = tree.branches.sorted { $0.depth > $1.depth }

            for branch in sorted {
                guard branch.points.count >= 2 else { continue }

                var path = Path()
                path.move(to: branch.points[0])
                for i in 1..<branch.points.count {
                    path.addLine(to: branch.points[i])
                }

                // Brightness decreases with depth
                let brightness = 1.0 - Double(branch.depth) * 0.25

                // Glow
                var glowCtx = context
                glowCtx.opacity = 0.15 * brightness
                glowCtx.blendMode = .plusLighter
                glowCtx.stroke(path, with: .color(.cyan),
                    style: StrokeStyle(lineWidth: branch.thickness * 5, lineCap: .round))

                // Core
                var coreCtx = context
                coreCtx.opacity = 0.9 * brightness
                coreCtx.blendMode = .plusLighter
                coreCtx.stroke(path, with: .color(.white),
                    style: StrokeStyle(lineWidth: branch.thickness, lineCap: .round))
            }
        }
    }
}
```

---

## Metal Glow Shader (Alternative to Multi-Layer Canvas)

For higher quality glow, render the bolt path to a texture and apply a bloom shader.

```metal
#include <metal_stdlib>
using namespace metal;

/// Simple additive glow: blur the source and add it back
/// Apply as .layerEffect after rendering the bolt to a layer
[[stitchable]]
half4 lightningGlow(
    float2 position,
    SwiftUI::Layer layer,
    float2 size,
    float glowRadius,
    float glowIntensity
) {
    half4 original = layer.sample(position);

    // Sample surrounding pixels for blur
    half4 blurred = half4(0);
    float totalWeight = 0;
    int samples = 8;

    for (int i = 0; i < samples; i++) {
        float angle = float(i) / float(samples) * 6.28318;
        for (float r = 1; r <= glowRadius; r += glowRadius / 3.0) {
            float2 offset = float2(cos(angle), sin(angle)) * r;
            float weight = 1.0 / (1.0 + r * 0.5);
            blurred += layer.sample(position + offset) * half(weight);
            totalWeight += weight;
        }
    }

    blurred /= half(totalWeight);

    // Additive composite
    return original + blurred * half(glowIntensity);
}
```

### SwiftUI Usage

```swift
ZStack {
    // Bolt rendered normally
    LightningBoltView(...)
}
.layerEffect(
    ShaderLibrary.lightningGlow(
        .float2(Float(size.width), Float(size.height)),
        .float(12.0),   // glow radius
        .float(2.5)     // glow intensity
    ),
    maxSampleOffset: CGSize(width: 20, height: 20)
)
```

---

## Dota 2 Reference: Zeus Lightning Bolt

Dota 2's Zeus lightning bolt effect combines several layers for its iconic look:

| Layer | Technique | Duration |
|-------|-----------|----------|
| Pre-flash | Screen-space white flash, 50ms | Alerts player something is coming |
| Bolt path | Midpoint displacement, ~6 segments, refreshed 2-3x during lifetime | The actual bolt |
| Volumetric glow | Line renderer with soft falloff texture, additive blend | Makes bolt feel thick and bright |
| Impact sparks | 20-40 particles at impact point, radial burst, 200-400ms lifetime | Ground contact feedback |
| Impact light | Point light at impact, sharp falloff, 150ms | Illuminates nearby geometry |
| Screen shake | 2-4px displacement, 100ms, ease-out | Sells the impact force |
| Audio sync | Thunder crack peaks 50ms after bolt appears | Tight A/V coupling |

**Key takeaway:** The bolt itself is simple midpoint displacement. The convincing-ness comes from the supporting layers (flash, sparks, light, shake, audio).

---

## Timing & Animation

### Bolt Lifecycle

```
[0ms]   Pre-flash (optional white overlay, 30-50ms)
[30ms]  Bolt appears at full brightness
[30-200ms] Bolt regenerates 2-3 times (flicker)
[200ms] Bolt fades out over 100ms
[200ms] Impact sparks (separate particle system, 200-400ms)
[250ms] Screen shake (2-4px, 100ms, ease-out)
```

### Flicker Pattern

Real lightning flickers. Regenerate the bolt path 2-3 times during its visible lifetime:

```swift
@State private var flickerPhase = 0

TimelineView(.animation(minimumInterval: 1.0 / 8.0)) { ctx in
    // Regenerate bolt every ~125ms (8Hz)
    Canvas { context, size in
        let bolt = LightningBolt.generate(from: start, to: end)
        // ... render bolt
    }
}
```

---

## Performance Notes

| Metric | Budget |
|--------|--------|
| Points per bolt | 32-64 (5-6 subdivision levels) |
| Branch count | 3-8 total (including sub-branches) |
| Refresh rate | 4-12 Hz (8 Hz recommended) |
| Canvas draw calls | 1 per layer (glow + core = 2-3 calls) |
| Max concurrent bolts | 3-5 on mobile, 10+ on desktop |

Lightning is cheap. The bolt is just a path with 32-64 points. The expensive part is the glow -- use the 3-layer Canvas trick instead of a real bloom pass for simple cases.
