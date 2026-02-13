---
name: orb
description: |
  [WHAT] Build animated SwiftUI orbs — Siri-style mesh gradients, particle spheres, and AI assistant visualizers.
  [HOW] 7 compositing techniques (MeshGradient, Canvas particles, Metal shaders, layer rotation, angular glow, hue-shift, animated masks) with code patterns and performance rules.
  [WHEN] Use when building or modifying animated orb UIs, voice chat visualizers, AI thinking indicators, Siri-style glows, particle effects, or the Kingly Clawd avatar.
  [WHY] Animated orbs require precise layering, 60fps budgets, accessibility compliance, and cross-platform (iOS/macOS) consistency. This skill encodes battle-tested patterns.

  Triggers: "orb", "siri animation", "mesh gradient", "voice visualizer", "particle sphere", "glow effect", "animated gradient", "MeshGradient", "Canvas animation", "TimelineView", "OCMiniOrb", "Clawd orb", "kaaba", "diamond orb", "ripple effect", "audio reactive"
triggers:
  - orb animation
  - siri clone
  - mesh gradient
  - voice visualizer
  - particle sphere
  - glow shadow
  - animated orb
  - canvas particle
  - metal shader ripple
  - audio reactive UI
---

# Orb — Animated SwiftUI Visualizer Skill

## Decision Tree

```
What are you building?
|
|-- Modify existing OCMiniOrb?
|   |-- Add/change state? -> See: Existing Implementation
|   |-- Tune layers? -> See: references/existing-impl.md
|   \-- Add audio reactivity? -> Bind audioLevel to scaleEffect
|
|-- New orb variant?
|   |-- Siri iOS 18 style (edge glow)? -> T1: MeshGradient + T2: AnimatedRectangle mask
|   |-- Classic Siri (layered rotation)? -> T3: Layer rotation with Figma assets
|   |-- Particle sphere (Jarvis)? -> T6: 3D particle system in Canvas
|   |-- Kaaba/Diamond? -> See: references/variants.md
|   \-- Glow button shadow? -> T7: Angular gradient + blur
|
|-- Performance issue?
|   |-- Dropped frames? -> Check: fractal conditional removal, Canvas vs SwiftUI shapes
|   |-- High CPU idle? -> Ensure TimelineView pauses when not visible
|   \-- Memory growth? -> Check particle pool / recycle bin pattern
|
\-- Accessibility?
    \-- .accessibilityReduceMotion -> guard !reduceMotion else { return }
```

## Quick Reference: 7 Techniques

| # | Technique | API | Best For | Ref |
|---|-----------|-----|----------|-----|
| T1 | MeshGradient | `MeshGradient(width:height:points:colors:)` | Siri iOS 18 edge glow | `references/techniques.md#t1` |
| T2 | AnimatedRectangle | Custom `Shape` + `animatableData` | Breathing border mask | `references/techniques.md#t2` |
| T3 | Layer Rotation | `ZStack` + `.rotationEffect` + `.hueRotation` | Classic Siri icon | `references/techniques.md#t3` |
| T4 | Hue-Shift Gradient | `TimelineView` + `shiftHue()` | Color cycling backgrounds | `references/techniques.md#t4` |
| T5 | Metal Ripple | `ShaderLibrary.Ripple` + `.layerEffect` | Tap/activation ripple | `references/techniques.md#t5` |
| T6 | 3D Particle Sphere | `Canvas` + sphere projection math | Jarvis orb, particle clouds | `references/techniques.md#t6` |
| T7 | Angular Glow | `AngularGradient` + `.blur` | Button glow shadows | `references/techniques.md#t7` |

## Existing Implementation (OCMiniOrb)

**Path:** `packages/uikit/Sources/OCDesignKit/Components/OCMiniOrb.swift`
**Storybook:** `apps/storybook/Sources/Shared/MiniOrbPage.swift`
**Spec:** `docs/ux/orb/mini-clawd-spec.md`

6-layer stack in ZStack:

| Layer | What | How |
|-------|------|-----|
| 1. Ambient Glow | `RadialGradient` + `.blur(size*0.25)` | Opacity pulse 0.2-0.35, 2s |
| 2. Base Orb | `RadialGradient` circle | Breathe 0.98-1.02, 3s; audio in speaking |
| 3. Fractal | `Canvas` + `TimelineView(1/30fps)` | 6 Fibonacci rings, conditional on state |
| 4. Glass | `RadialGradient` + `.ultraThinMaterial` | Static 0.85x |
| 5. Smoke | 4 orbiting blobs in `Canvas` | 3-6s rotation per blob |
| 6. Eyes | 2 white circles | Dim to 0.4 in thinking |

**States:** `OrbDisplayState` — `.idle`, `.thinking`, `.speaking`, `.listening`
**Colors:** `OCColors.voiceOrb{State}Start/End`, `.voiceHighlight`, `.voiceParticle`

## Performance Rules (NON-NEGOTIABLE)

1. **Canvas over shapes** — Use `Canvas` for particle systems (single draw call per layer)
2. **Conditional hierarchy** — Remove fractal/smoke from view tree when idle: `if state == .thinking { ... }`
3. **30fps cap** — `TimelineView(.animation(minimumInterval: 1.0 / 30.0))`
4. **Reduce motion** — `@Environment(\.accessibilityReduceMotion)` guards ALL animation starts
5. **Pool particles** — Recycle bin pattern (linked list, not array append/remove)
6. **No SpriteKit** — Pure SwiftUI + Canvas + optional Metal
7. **Target** — 60fps at 48pt on iPhone 12 / M1 Mac

## Compositing Recipe: New Orb

```swift
// Minimal orb skeleton
struct MyOrb: View {
    let state: OrbDisplayState
    var size: CGFloat = 48
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        ZStack {
            // 1. Glow (always)
            Circle().fill(RadialGradient(...)).blur(radius: size * 0.25)
            // 2. Base (always)
            Circle().fill(RadialGradient(...)).scaleEffect(breatheScale)
            // 3. Active layers (conditional)
            if state != .idle {
                activeLayer(size)  // Canvas-based
            }
            // 4. Glass (always)
            Circle().fill(...).background(.ultraThinMaterial.opacity(0.15))
            // 5. Highlights (always)
            eyeDots(size)
        }
        .frame(width: size * 1.3, height: size * 1.3)
        .accessibilityLabel("Assistant \(state.label)")
    }
}
```

## Key Helper: sinInRange

```swift
func sinInRange(_ range: ClosedRange<Float>, offset: Float, timeScale: Float, t: Float) -> Float {
    let amplitude = (range.upperBound - range.lowerBound) / 2
    let midPoint = (range.upperBound + range.lowerBound) / 2
    return midPoint + amplitude * sin(timeScale * t + offset)
}
```

Used by MeshGradient (T1) and AnimatedRectangle (T2) for organic motion.

## References

| File | Content |
|------|---------|
| `references/techniques.md` | Full code for all 7 techniques with copy-paste patterns |
| `references/existing-impl.md` | OCMiniOrb layer-by-layer analysis, modification guide |
| `references/variants.md` | Kaaba/Diamond, particle sphere, mesh orb variant specs |

## External Sources

- [metasidd/PrototypeSiriAnimation](https://github.com/metasidd/PrototypeSiriAnimation) — iOS 18 Siri mesh gradient prototype
- [Rudrank Riyam — Siri Animation](https://rudrank.com/exploring-swiftui-creating-new-siri-animation) — MeshingAIProgressView deep dive
- [Hacking with Swift — MeshGradient](https://www.hackingwithswift.com/quick-start/swiftui/how-to-create-a-mesh-gradient) — API reference
- [Amos Gyamfi — Siri Clone Gist](https://gist.github.com/amosgyamfi/b611c216604fd40a5aad2673fc5cf0b4) — Layer rotation approach
- [insidegui/MeshBuddy](https://github.com/insidegui/MeshBuddy) — Visual MeshGradient editor

## Related Skills

- **pencil** — Visual design prompts and character art for orb avatars (concept → prompt)
- **swiftui-animation** — General SwiftUI animation patterns (broader scope)
- **swiftui-performance-audit** — Runtime perf diagnostics (when orb causes frame drops)
## Technique Map

- **6-layer ZStack compositing** — Ambient glow, base orb, fractal (conditional), glass, smoke, eyes; because layering order determines visual hierarchy and performance.
- **Canvas over shapes for particles** — Single draw call per layer; because SwiftUI shapes = many draw calls; Canvas = one.
- **Conditional hierarchy** — Remove fractal/smoke when idle; because redundant layers drain GPU when not visible.
- **30fps cap for TimelineView** — minimumInterval: 1.0/30.0; because 60fps for decorative layers wastes budget.
- **Reduce motion guard** — @Environment(\.accessibilityReduceMotion) on ALL animation; because accessibility compliance is non-negotiable.
- **sinInRange helper** — Organic motion for MeshGradient and AnimatedRectangle; because procedural variation feels more natural than linear.
- **Pool particles** — Recycle bin pattern, not array append/remove; because mid-frame allocation causes frame drops.

## Technique Notes

7 techniques: T1 MeshGradient, T2 AnimatedRectangle, T3 layer rotation, T4 hue-shift, T5 Metal ripple, T6 particle sphere, T7 angular glow. OCMiniOrb path: OCDesignKit/Components/OCMiniOrb.swift. Target: 60fps at 48pt on iPhone 12.

---

## Prompt Architect Overlay

**Role Definition:** Animated SwiftUI orb builder. Siri-style mesh gradients, particle spheres, AI assistant visualizers. Encodes 7 compositing techniques with performance rules and accessibility compliance.

**Input Contract:** Accepts orb variant (Siri iOS 18, classic Siri, particle sphere, Kaaba/Diamond), modification target (existing OCMiniOrb or new), or performance issue. State (idle/thinking/speaking/listening) if modifying existing.

**Output Contract:** Layer-by-layer compositing recipe, technique references, performance rules checklist. SwiftUI code snippets. Accessibility labels. References to techniques.md, existing-impl.md, variants.md.

**Edge Cases & Fallbacks:** If frame drops→check conditional hierarchy, Canvas vs shapes, particle count. If modify OCMiniOrb→reference existing-impl.md. If audio reactive→bind audioLevel to scaleEffect. If Metal needed→orb skill T5; metal-shaders for MSL.
