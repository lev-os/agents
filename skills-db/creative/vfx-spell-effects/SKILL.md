---
name: vfx-spell-effects
description: Build game-quality spell VFX on Apple platforms with practical recipes for smoke, lightning, particles, bloom, layering, and stable 60fps performance.
triggers:
  - spell effect
  - vfx particles
  - lightning bolt effect
  - smoke fog simulation
  - bloom glow shader
  - fire effect
  - magic aura
  - Metal particle system
  - impact explosion
  - spell composition
  - procedural lightning
  - ray marching fog
  - GPU compute particles
  - Vortex preset
  - game visual effects
---

# VFX Spell Effects — Game-Quality Visual Effects for Apple Platforms

## Decision Tree

```
What effect do you want?
|
|-- Smoke / Fog / Clouds?
|   |-- Soft procedural blobs? -> Canvas noise blobs (like OCMiniOrb smoke)
|   |-- Volumetric 3D fog? -> Ray marching (Metal fragment shader)
|   |-- Quick particle smoke? -> SpriteKit SKEmitterNode or Vortex
|   \-- Fluid dynamics? -> Metal compute (Navier-Stokes, advanced)
|   -> See: references/smoke-fog.md
|
|-- Lightning / Electricity?
|   |-- Single bolt? -> Midpoint displacement (most practical)
|   |-- Smooth arc? -> Lissajous curves
|   |-- Branching tree? -> Recursive fractal (Lichtenberg figures)
|   \-- Glow on bolt? -> Additive bloom post-process
|   -> See: references/lightning-electricity.md
|
|-- Particles (fire, sparks, magic)?
|   |-- Quick preset? -> Vortex (SwiftUI-native)
|   |-- 2D overlay? -> CAEmitterLayer or SpriteKit
|   |-- Full GPU control? -> Metal compute shader pipeline
|   |-- SwiftUI-only? -> Canvas + TimelineView
|   -> See: references/particles.md
|
|-- Bloom / Glow / Post-processing?
|   |-- SwiftUI quick glow? -> .shadow() + .blur() stacking
|   |-- HDR bloom pipeline? -> Threshold -> Gaussian blur -> Composite (Metal)
|   |-- Per-object glow? -> Render to texture + blur + additive blend
|   -> See: references/bloom-glow.md
|
|-- Composing a full spell?
|   |-- State machine? -> .idle -> .charging -> .casting -> .impact -> .dissipating
|   |-- Layer ordering? -> base + particles + glow + screen shake + audio
|   |-- Audio-reactive? -> Bind intensity to RMS amplitude
|   -> See: references/spell-composition.md
|
\-- Performance issue?
    |-- Dropped frames? -> Check particle count, blur radius, draw calls
    |-- GPU bottleneck? -> Profile with Xcode GPU debugger
    |-- CPU bottleneck? -> Move particle update to compute shader
    -> See: Performance Budget Rules below
```

## Quick Reference

| Effect | Best API | Approach | Ref |
|--------|----------|----------|-----|
| Soft smoke blobs | SwiftUI Canvas | Noise-offset circles + alpha blend | `references/smoke-fog.md` |
| Volumetric fog | Metal fragment | Ray march density field, 4-8 samples | `references/smoke-fog.md` |
| Lightning bolt | SwiftUI Canvas / Metal | Midpoint displacement, 4-5 levels | `references/lightning-electricity.md` |
| Branching lightning | Canvas + recursion | Fractal tree, angle +/-30deg | `references/lightning-electricity.md` |
| Fire particles | Vortex / SpriteKit | Pre-built emitter, warm palette | `references/particles.md` |
| Magic sparks | Metal compute | GPU particle pool, 500-2000 particles | `references/particles.md` |
| Impact explosion | Vortex + Canvas | Burst emit + radial force + fade | `references/particles.md` |
| Object glow | SwiftUI `.shadow` | Stacked `.shadow(radius:)` calls | `references/bloom-glow.md` |
| HDR bloom | Metal render pass | Threshold + separable Gaussian + composite | `references/bloom-glow.md` |
| Full spell | Composite pattern | State machine + layer stack + timeline | `references/spell-composition.md` |

## Performance Budget Rules (NON-NEGOTIABLE)

1. **16ms frame budget** -- Target 60fps. All VFX layers combined must complete within 16ms GPU + CPU time.
2. **Particle limits** -- Mobile: 500-2000 active particles max. Desktop: up to 10,000 with compute shader. Never allocate mid-frame.
3. **Blur radius cap** -- `.blur(radius:)` over 20pt on mobile tanks performance. Use downscaled render targets for large blurs.
4. **Draw call budget** -- Keep under 10 draw calls for VFX overlay. Use Canvas (1 draw call per layer) or instanced rendering.
5. **Compute shader particles** -- Mandatory for >500 particles. CPU-side `for` loops over particle arrays cause frame drops on mobile.
6. **Ray march samples** -- 4-8 samples per ray for real-time fog. More than 12 is offline-quality territory.
7. **Bloom passes** -- 3-5 blur passes with ping-pong buffers. Downscale to half/quarter resolution for blur.
8. **Pool, never allocate** -- Pre-allocate particle arrays. Use recycle-bin pattern (free list). Zero heap allocation during gameplay.
9. **Reduce motion** -- `@Environment(\.accessibilityReduceMotion)` guards ALL effect starts. Provide static fallback.
10. **Profile on device** -- Simulator GPU timing is meaningless. Test on oldest supported hardware.

## Key Patterns

### State Machine for Spell Lifecycle

```swift
enum SpellPhase: String, CaseIterable {
    case idle, charging, casting, impact, dissipating
}

@Observable
class SpellState {
    var phase: SpellPhase = .idle
    var intensity: Float = 0.0  // 0.0-1.0
    var elapsed: TimeInterval = 0.0

    func advance(dt: TimeInterval) {
        elapsed += dt
        switch phase {
        case .charging:   intensity = min(1.0, Float(elapsed / 0.5))
        case .casting:    intensity = 1.0
        case .impact:     intensity = max(0.0, 1.0 - Float(elapsed / 0.3))
        case .dissipating: intensity = max(0.0, 0.5 - Float(elapsed / 0.6))
        case .idle:       intensity = 0.0
        }
    }
}
```

### Canvas-Based Effect Layer

```swift
struct EffectLayer: View {
    let state: SpellState
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        if !reduceMotion && state.phase != .idle {
            TimelineView(.animation(minimumInterval: 1.0 / 60.0)) { ctx in
                Canvas { context, size in
                    // Draw effect here -- single draw call
                    let t = ctx.date.timeIntervalSinceReferenceDate
                    drawEffect(context: context, size: size, time: t, intensity: state.intensity)
                }
            }
        }
    }
}
```

### Midpoint Displacement Lightning (Minimal)

```swift
func generateBolt(from: CGPoint, to: CGPoint, levels: Int = 5, jaggedness: CGFloat = 0.4) -> [CGPoint] {
    var points = [from, to]
    for level in 0..<levels {
        var newPoints = [points[0]]
        let scale = jaggedness * pow(0.5, CGFloat(level))
        for i in 0..<(points.count - 1) {
            let mid = CGPoint(
                x: (points[i].x + points[i+1].x) / 2 + CGFloat.random(in: -1...1) * scale * from.distance(to: to),
                y: (points[i].y + points[i+1].y) / 2 + CGFloat.random(in: -1...1) * scale * from.distance(to: to)
            )
            newPoints.append(mid)
            newPoints.append(points[i+1])
        }
        points = newPoints
    }
    return points
}
```

## References

| File | Content |
|------|---------|
| `references/smoke-fog.md` | Noise-based smoke, ray marching fog, Canvas blobs, Metal fluid dynamics |
| `references/lightning-electricity.md` | Fractal midpoint displacement, Lissajous arcs, branching trees, glow rendering |
| `references/particles.md` | API comparison, GPU particle architecture, emission patterns, pool pattern, Vortex presets |
| `references/bloom-glow.md` | HDR bloom pipeline, threshold/blur/composite, Metal + SwiftUI integration |
| `references/spell-composition.md` | State machine, layer stacking, audio-reactive binding, timing curves, full spell examples |

## External Resources

- [Vortex](https://github.com/twostraws/Vortex) -- SwiftUI-native particle system
- [Inferno](https://github.com/twostraws/Inferno) -- Metal shader collection for SwiftUI
- [MetalNoise](https://github.com/jmade/MetalNoise) -- Perlin/Simplex noise in Metal
- [The Book of Shaders: Noise](https://thebookofshaders.com/11/) -- Noise function fundamentals
- [Ray Marching SDFs](https://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/) -- Ray marching primer
- [2D Lightning Effects](https://gamedevelopment.tutsplus.com/tutorials/how-to-generate-shockingly-good-2d-lightning-effects--gamedev-2681) -- Midpoint displacement tutorial
- [LearnOpenGL: Bloom](https://learnopengl.com/Advanced-Lighting/Bloom) -- HDR bloom pipeline reference
- [Realtime Fire Rendering](https://andrewkchan.dev/posts/fire.html) -- Procedural fire techniques

## Related Skills

- **orb** -- OCMiniOrb implementation (smoke layer, fractal layer, glow compositing)
- **swiftui-animation** -- Animation curves, springs, Metal shader integration in SwiftUI
- **swiftui-performance-audit** -- Runtime GPU/CPU profiling when effects cause frame drops
## Technique Map

- **Effect type routing** — Smoke/fog, lightning, particles, bloom, full spell; because each has distinct API and approach.
- **State machine for lifecycle** — idle→charging→casting→impact→dissipating; because spells have phases; state drives intensity.
- **16ms frame budget** — 60fps non-negotiable; because dropped frames break immersion.
- **Particle limits** — 500-2000 mobile; 10k desktop with compute; because CPU particle loops tank mobile.
- **Canvas for overlay** — Single draw call per layer; because draw call budget matters.
- **Pool, never allocate** — Recycle bin pattern; because mid-frame allocation causes hitches.
- **Reduce motion guard** — Static fallback when accessibilityReduceMotion; because necessary for compliance.
- **Midpoint displacement** — For lightning; 4-5 levels; because simple, effective, performant.

## Technique Notes

References: smoke-fog, lightning-electricity, particles, bloom-glow, spell-composition. APIs: Vortex, SpriteKit, Metal compute, Canvas. Profile on device; simulator GPU timing meaningless. Related: orb, swiftui-animation, swiftui-performance-audit.

---

## Prompt Architect Overlay

**Role Definition:** VFX spell effects builder. Game-quality smoke, lightning, particles, bloom, spell composition. 60fps performance rules. Apple platforms.

**Input Contract:** Accepts effect type (smoke, lightning, fire, glow, full spell), target API (Vortex, Metal, Canvas), or performance issue. Platform, particle count, style.

**Output Contract:** Decision tree result. Quick reference row. Code pattern (state machine, canvas layer, midpoint displacement). Performance budget rules. Reference to deep-dive. Related skills.

**Edge Cases & Fallbacks:** If performance issue→check particle count, blur radius, draw calls. If >500 particles→compute shader mandatory. If bloom→downscale for blur passes. If reduce motion→guard all effects; provide static fallback.
