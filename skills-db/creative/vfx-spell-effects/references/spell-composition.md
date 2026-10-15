# Composing Spells

## Overview

A convincing spell effect is never a single technique -- it is a layered composition of particles, glow, distortion, audio, and screen effects orchestrated by a state machine. This reference covers the architecture for building reusable, composable spell effects.

---

## State Machine Pattern

### Spell Phases

```
.idle ──────> .charging ──────> .casting ──────> .impact ──────> .dissipating ──────> .idle
              (0.3-0.8s)        (0.1-0.5s)       (0.1-0.3s)      (0.3-1.0s)
```

| Phase | Duration | Intensity Curve | What Happens |
|-------|----------|-----------------|-------------|
| `.idle` | -- | 0 | Nothing visible. All effect layers removed from view tree. |
| `.charging` | 0.3-0.8s | 0 -> 1.0 (ease-in) | Build-up: particles gather, glow intensifies, subtle screen distortion, audio wind-up |
| `.casting` | 0.1-0.5s | 1.0 (sustained) | Release: projectile launches, main effect visible, peak audio |
| `.impact` | 0.1-0.3s | 1.0 -> 0.5 (sharp) | Hit: burst particles, bright flash, screen shake, impact audio |
| `.dissipating` | 0.3-1.0s | 0.5 -> 0 (ease-out) | Aftermath: particles drift, glow fades, smoke lingers |

### Swift Implementation

```swift
import SwiftUI

enum SpellPhase: String, CaseIterable, Sendable {
    case idle
    case charging
    case casting
    case impact
    case dissipating
}

@Observable
@MainActor
class SpellState {
    var phase: SpellPhase = .idle
    var intensity: Float = 0.0
    var elapsed: TimeInterval = 0.0
    var totalPhaseTime: TimeInterval = 0.0

    // Phase durations (configurable per spell)
    var chargeDuration: TimeInterval = 0.5
    var castDuration: TimeInterval = 0.3
    var impactDuration: TimeInterval = 0.15
    var dissipateDuration: TimeInterval = 0.6

    /// Call every frame from TimelineView
    func update(dt: TimeInterval) {
        guard phase != .idle else {
            intensity = 0
            return
        }

        elapsed += dt
        let phaseDuration = currentPhaseDuration

        switch phase {
        case .idle:
            intensity = 0

        case .charging:
            // Ease-in: slow start, accelerating
            let t = Float(min(elapsed / phaseDuration, 1.0))
            intensity = t * t  // quadratic ease-in

        case .casting:
            intensity = 1.0

        case .impact:
            // Sharp decay
            let t = Float(min(elapsed / phaseDuration, 1.0))
            intensity = 1.0 - t * 0.5  // 1.0 -> 0.5

        case .dissipating:
            // Ease-out: fast start, decelerating
            let t = Float(min(elapsed / phaseDuration, 1.0))
            intensity = 0.5 * (1.0 - t * t)  // quadratic ease-out
        }

        // Auto-advance phase
        if elapsed >= phaseDuration {
            advancePhase()
        }
    }

    func cast() {
        phase = .charging
        elapsed = 0
    }

    private var currentPhaseDuration: TimeInterval {
        switch phase {
        case .idle: return .infinity
        case .charging: return chargeDuration
        case .casting: return castDuration
        case .impact: return impactDuration
        case .dissipating: return dissipateDuration
        }
    }

    private func advancePhase() {
        elapsed = 0
        switch phase {
        case .idle: break
        case .charging: phase = .casting
        case .casting: phase = .impact
        case .impact: phase = .dissipating
        case .dissipating: phase = .idle
        }
    }
}
```

---

## Layer Stack Architecture

Every spell is a ZStack of effect layers, each controlled by the SpellState.

```
Layer 6: Screen Effects (shake, flash, vignette)     -- Overlay
Layer 5: Post-Processing (bloom)                      -- Applied as .layerEffect
Layer 4: Particles (sparks, smoke, embers)            -- Canvas / Vortex
Layer 3: Core Effect (bolt, beam, orb, projectile)    -- Canvas / Metal
Layer 2: Ground/Environment (decals, ripples, fog)    -- Canvas
Layer 1: Ambient Glow (radial gradient, atmosphere)   -- Circle + blur
```

### SwiftUI Composition

```swift
struct SpellView: View {
    @State private var spell = SpellState()
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        ZStack {
            if spell.phase != .idle && !reduceMotion {
                // Layer 1: Ambient glow
                AmbientGlowLayer(intensity: spell.intensity, color: spellColor)

                // Layer 2: Ground effect
                if spell.phase == .impact || spell.phase == .dissipating {
                    GroundRippleLayer(intensity: spell.intensity)
                }

                // Layer 3: Core effect
                CoreEffectLayer(phase: spell.phase, intensity: spell.intensity)

                // Layer 4: Particles
                ParticleLayer(phase: spell.phase, intensity: spell.intensity)
            }
        }
        // Layer 5: Bloom (applied to entire stack)
        .modifier(BloomModifier(intensity: spell.intensity))
        // Layer 6: Screen shake
        .modifier(ScreenShakeModifier(
            active: spell.phase == .impact,
            intensity: spell.intensity
        ))
    }
}
```

### Screen Shake Modifier

```swift
struct ScreenShakeModifier: ViewModifier {
    let active: Bool
    let intensity: Float
    @State private var offsetX: CGFloat = 0
    @State private var offsetY: CGFloat = 0

    func body(content: Content) -> some View {
        content
            .offset(x: offsetX, y: offsetY)
            .onChange(of: active) { _, isActive in
                if isActive {
                    shake()
                } else {
                    offsetX = 0
                    offsetY = 0
                }
            }
    }

    private func shake() {
        let magnitude = CGFloat(intensity) * 4
        // 3-frame shake: strong, medium, settle
        withAnimation(.linear(duration: 0.04)) {
            offsetX = CGFloat.random(in: -magnitude...magnitude)
            offsetY = CGFloat.random(in: -magnitude...magnitude)
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.04) {
            withAnimation(.linear(duration: 0.04)) {
                offsetX = CGFloat.random(in: -magnitude/2...magnitude/2)
                offsetY = CGFloat.random(in: -magnitude/2...magnitude/2)
            }
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.08) {
            withAnimation(.easeOut(duration: 0.06)) {
                offsetX = 0
                offsetY = 0
            }
        }
    }
}
```

---

## Audio-Reactive Effects

Binding VFX intensity to audio amplitude creates effects that feel alive.

### Approach: RMS Amplitude Binding

```swift
@Observable
class AudioReactiveState {
    var rmsLevel: Float = 0.0       // 0.0-1.0, current RMS
    var peakLevel: Float = 0.0      // 0.0-1.0, current peak
    var smoothedLevel: Float = 0.0  // Smoothed for visual use

    private let smoothingFactor: Float = 0.15  // Higher = more responsive

    func update(rms: Float, peak: Float) {
        rmsLevel = rms
        peakLevel = peak
        // Exponential smoothing
        smoothedLevel += (rms - smoothedLevel) * smoothingFactor
    }
}
```

### Binding Audio to VFX

```swift
struct AudioReactiveSpell: View {
    let audioState: AudioReactiveState
    let spellState: SpellState

    var effectiveIntensity: Float {
        // Base intensity from spell phase, modulated by audio
        let base = spellState.intensity
        let audioMod = audioState.smoothedLevel

        switch spellState.phase {
        case .casting, .impact:
            // Audio amplifies during active phases
            return min(1.0, base * (1.0 + audioMod * 0.5))
        case .charging:
            // Audio adds subtle pulse during charge
            return base + audioMod * 0.15
        default:
            return base
        }
    }

    var body: some View {
        // Use effectiveIntensity for all VFX layers
        ParticleLayer(intensity: effectiveIntensity)
    }
}
```

### What to Bind

| VFX Parameter | Audio Source | Effect |
|---------------|------------|--------|
| Particle birth rate | RMS level | More particles when louder |
| Glow intensity | Smoothed RMS | Pulsing glow with voice/music |
| Scale effect | Peak level | Punch on transients |
| Particle speed | RMS derivative | Acceleration on volume changes |
| Color saturation | RMS level | More vivid when louder |

---

## Timing & Easing

### Intensity Curves by Phase

```
Intensity
1.0 |         ┌────┐
    |        /     |\_
    |       /      |  \_
0.5 |      /       |    \_
    |     /        |      \_
    |    /         |        \__
0.0 |___/         |            \___
    |   |         |         |       |
    idle charging casting impact dissipating
```

### Staggering Child Effects

Different layers should NOT all start at the same time. Stagger creates depth:

```swift
struct StaggeredSpellLayers: View {
    let spell: SpellState

    var body: some View {
        ZStack {
            // Glow starts first (0ms offset)
            AmbientGlowLayer(intensity: spell.intensity)

            // Core effect starts 50ms later
            CoreEffectLayer(intensity: delayedIntensity(delay: 0.05))

            // Particles start 100ms after core
            ParticleLayer(intensity: delayedIntensity(delay: 0.15))

            // Screen shake only on impact, 30ms after impact phase starts
            ScreenShakeModifier(
                active: spell.phase == .impact && spell.elapsed > 0.03,
                intensity: spell.intensity
            )
        }
    }

    private func delayedIntensity(delay: TimeInterval) -> Float {
        let adjustedElapsed = spell.elapsed - delay
        guard adjustedElapsed > 0 else { return 0 }
        return spell.intensity * Float(min(adjustedElapsed / 0.1, 1.0))
    }
}
```

---

## SpellEffect Protocol

Composable protocol for building a library of spell effects.

```swift
protocol SpellEffect: View {
    var phase: SpellPhase { get }
    var intensity: Float { get }
    var position: CGPoint { get }
}

struct CompositeSpell: View {
    let effects: [AnyView]
    let state: SpellState

    var body: some View {
        ZStack {
            ForEach(effects.indices, id: \.self) { i in
                effects[i]
            }
        }
    }
}

// Builder pattern
struct SpellBuilder {
    private var layers: [(phase: SpellPhase?, view: AnyView)] = []

    mutating func addLayer<V: View>(_ view: V, activeIn phases: [SpellPhase]? = nil) {
        layers.append((phase: nil, view: AnyView(view)))
    }

    func build(state: SpellState) -> some View {
        ZStack {
            ForEach(layers.indices, id: \.self) { i in
                let layer = layers[i]
                if let phases = [layer.phase].compactMap({ $0 }) as [SpellPhase]?,
                   !phases.isEmpty {
                    if phases.contains(state.phase) {
                        layer.view
                    }
                } else {
                    layer.view
                }
            }
        }
    }
}
```

---

## Complete Spell Examples

### 1. Healing Aura

```
Layers:
1. Ring particles (green, orbiting outward, gentle speed)
2. Radial gradient glow (soft green, pulsing with intensity)
3. Rising sparkle particles (low count, slow rise, long lifetime)
4. Gentle screen tint (green overlay at 5% opacity)

No screen shake. No flash. Healing should feel calm.

Timing:
- Charge: 0.8s (slow build, particles gather inward)
- Cast: 1.5s (sustained, ring expands)
- Impact: none (healing has no impact phase)
- Dissipate: 1.0s (particles drift upward and fade)

Colors:
- Core: #4ADE80 (green-400)
- Glow: #22C55E (green-500)
- Particles: #86EFAC (green-300) with white highlights
- Bloom: soft, low intensity (0.3)
```

```swift
struct HealingAura: View {
    @State private var spell = SpellState()

    init() {
        spell.chargeDuration = 0.8
        spell.castDuration = 1.5
        spell.impactDuration = 0  // skip impact
        spell.dissipateDuration = 1.0
    }

    var body: some View {
        ZStack {
            // Ambient glow
            Circle()
                .fill(RadialGradient(
                    colors: [
                        Color.green.opacity(Double(spell.intensity) * 0.3),
                        Color.green.opacity(Double(spell.intensity) * 0.1),
                        .clear
                    ],
                    center: .center,
                    startRadius: 0,
                    endRadius: 120
                ))
                .scaleEffect(CGFloat(0.8 + spell.intensity * 0.4))
                .blur(radius: 20)

            // Ring particles
            if spell.phase != .idle {
                VortexView(.healingRing) {
                    Circle()
                        .fill(.green.opacity(0.6))
                        .frame(width: 6, height: 6)
                        .blur(radius: 2)
                        .tag("heal")
                }
            }

            // Rising sparkles
            if spell.phase == .casting || spell.phase == .dissipating {
                VortexView(.healingSparkles) {
                    Circle()
                        .fill(.white)
                        .frame(width: 3, height: 3)
                        .tag("sparkle")
                }
            }
        }
        .shadow(color: .green.opacity(Double(spell.intensity) * 0.4), radius: 30)
    }
}
```

### 2. Fireball

```
Layers:
1. Fire particle trail (orange/yellow, attached to projectile path)
2. Central fireball core (bright orange sphere, pulsing)
3. Smoke trail (dark gray particles, slower, longer lifetime)
4. Impact: explosion burst (40 particles, radial, fast)
5. Impact: bright flash (white overlay, 50ms)
6. Impact: screen shake (4px, 100ms)
7. Dissipate: smoke lingers (slow rise, 1s lifetime)

Timing:
- Charge: 0.4s (fire coalesces into sphere)
- Cast: 0.2s (projectile launches -- fast!)
- Impact: 0.15s (explosion)
- Dissipate: 0.8s (smoke clears)

Colors:
- Core: #FBBF24 (amber-400) -> #F97316 (orange-500)
- Fire particles: #FCD34D (amber-300), #EF4444 (red-500)
- Smoke: #6B7280 (gray-500) at 30% opacity
- Bloom: intense (0.8), warm tint
```

### 3. Lightning Bolt

```
Layers:
1. Pre-flash: white screen overlay, 50ms, then off
2. Bolt path: midpoint displacement, 5 levels, refresh at 8Hz
3. 3-layer glow: outer (cyan, 6x width), mid (cyan, 3x), core (white, 1x)
4. Branching arcs: 2-3 sub-bolts from main path
5. Impact sparks: 30 particles, radial burst, 0.3s lifetime
6. Thunder shake: 3px, 100ms, ease-out
7. Residual glow: fading bolt path, 200ms

Timing:
- Charge: 0.3s (crackling buildup, small sparks)
- Cast: 0.05s (bolt appears -- nearly instant)
- Impact: 0.2s (sparks + shake)
- Dissipate: 0.4s (glow fades, smoke wisps)

Colors:
- Core: #FFFFFF (pure white)
- Glow: #22D3EE (cyan-400)
- Branch glow: #06B6D4 (cyan-500)
- Sparks: #FCD34D (amber-300), #FFFFFF
- Bloom: very intense (1.0), cool tint
```

---

## Architecture: SpellTimeline Sequencer

For complex spells with precisely timed events (audio cues, haptics, phase transitions).

```swift
struct SpellEvent {
    let time: TimeInterval      // seconds from spell start
    let action: SpellAction
}

enum SpellAction {
    case setPhase(SpellPhase)
    case emitParticles(count: Int, pattern: EmissionPattern)
    case flash(color: Color, duration: TimeInterval)
    case shake(magnitude: CGFloat, duration: TimeInterval)
    case playAudio(name: String)
    case haptic(style: UIImpactFeedbackGenerator.FeedbackStyle)
    case setIntensity(Float)
}

@Observable
class SpellTimeline {
    let events: [SpellEvent]
    var currentIndex: Int = 0
    var elapsed: TimeInterval = 0
    var isPlaying: Bool = false

    init(events: [SpellEvent]) {
        self.events = events.sorted { $0.time < $1.time }
    }

    func update(dt: TimeInterval) -> [SpellAction] {
        guard isPlaying else { return [] }
        elapsed += dt

        var fired: [SpellAction] = []
        while currentIndex < events.count && events[currentIndex].time <= elapsed {
            fired.append(events[currentIndex].action)
            currentIndex += 1
        }

        if currentIndex >= events.count {
            isPlaying = false
        }

        return fired
    }

    func play() {
        currentIndex = 0
        elapsed = 0
        isPlaying = true
    }
}

// Example: Lightning bolt timeline
let lightningTimeline = SpellTimeline(events: [
    SpellEvent(time: 0.0,   action: .setPhase(.charging)),
    SpellEvent(time: 0.0,   action: .playAudio(name: "lightning_charge")),
    SpellEvent(time: 0.1,   action: .emitParticles(count: 5, pattern: .point)),
    SpellEvent(time: 0.25,  action: .haptic(style: .light)),
    SpellEvent(time: 0.3,   action: .setPhase(.casting)),
    SpellEvent(time: 0.3,   action: .flash(color: .white, duration: 0.05)),
    SpellEvent(time: 0.3,   action: .setIntensity(1.0)),
    SpellEvent(time: 0.3,   action: .playAudio(name: "lightning_strike")),
    SpellEvent(time: 0.35,  action: .setPhase(.impact)),
    SpellEvent(time: 0.35,  action: .emitParticles(count: 30, pattern: .radialBurst)),
    SpellEvent(time: 0.35,  action: .shake(magnitude: 4, duration: 0.1)),
    SpellEvent(time: 0.35,  action: .haptic(style: .heavy)),
    SpellEvent(time: 0.55,  action: .setPhase(.dissipating)),
    SpellEvent(time: 0.55,  action: .setIntensity(0.3)),
    SpellEvent(time: 1.15,  action: .setPhase(.idle)),
])
```

---

## Design Principles

### 1. Less is More

The most common mistake is overloading effects. Dota 2's effects are impactful because they are **brief, focused, and precisely timed**. A lightning bolt that lasts 0.15s with a sharp crack feels more powerful than one that lingers for 2s.

### 2. Audio-Visual Sync

The audio cue should lead the visual by 0-30ms for perceived synchrony. The brain interprets light as "faster" so a slight audio lead feels more natural.

### 3. Contrast Creates Impact

A bright flash only reads as bright if the surrounding frame is dark. Use pre-flash dimming or vignette to increase perceived dynamic range.

### 4. Silhouette Readability

Effects must not obscure gameplay-critical information. Use additive blending for glow (preserves underlying content) and keep opaque elements small and brief.

### 5. Graceful Degradation

Every effect needs a reduce-motion fallback: static icon swap, color tint, or simple opacity change. The game must be playable without animation.

---

## Cross-References

- **references/smoke-fog.md** -- Smoke layers for spell trails and aftermath
- **references/lightning-electricity.md** -- Bolt rendering for lightning spell core
- **references/particles.md** -- Particle emission for sparks, fire, magic
- **references/bloom-glow.md** -- Bloom post-processing for spell glow
- **orb skill** -- OCMiniOrb demonstrates a 6-layer composited effect with state machine
- **swiftui-animation** -- Animation timing curves, springs, and Metal shader integration
