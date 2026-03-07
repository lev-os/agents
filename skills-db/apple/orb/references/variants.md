# Orb Variants

## Variant 1: Kaaba / Diamond Orb

Diamond shape with rounded corners, concentric circle flashes, blur trails, glow pulsing.

### Shape Foundation
```swift
// Diamond = RoundedRectangle rotated 45 degrees
RoundedRectangle(cornerRadius: 12, style: .continuous)
    .fill(gradient)
    .frame(width: size, height: size)
    .rotationEffect(.degrees(45))
```

### Trail Effect (Duplicated at Varying Blur)
```swift
struct DiamondTrailOrb: View {
    let size: CGFloat
    @State private var rotation: Double = 0

    var body: some View {
        ZStack {
            // Trail layer 3 (most blurred, largest)
            diamond(size: size * 1.15)
                .blur(radius: 12)
                .opacity(0.15)
                .rotationEffect(.degrees(rotation * 0.7))

            // Trail layer 2
            diamond(size: size * 1.08)
                .blur(radius: 6)
                .opacity(0.3)
                .rotationEffect(.degrees(rotation * 0.85))

            // Core diamond
            diamond(size: size)
                .blur(radius: 1)
                .rotationEffect(.degrees(rotation))
        }
        .onAppear {
            withAnimation(.linear(duration: 8).repeatForever(autoreverses: false)) {
                rotation = 360
            }
        }
    }

    func diamond(size: CGFloat) -> some View {
        RoundedRectangle(cornerRadius: size * 0.15, style: .continuous)
            .fill(
                AngularGradient(colors: [.purple, .cyan, .purple],
                                center: .center)
            )
            .frame(width: size, height: size)
            .rotationEffect(.degrees(45))
    }
}
```

### Concentric Circle Flashes
```swift
struct ConcentricFlash: View {
    let ringCount: Int = 5
    @State private var flash: Bool = false

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 30.0)) { timeline in
            let now = timeline.date.timeIntervalSinceReferenceDate
            ZStack {
                ForEach(0..<ringCount, id: \.self) { i in
                    Circle()
                        .stroke(Color.white.opacity(
                            0.1 + 0.3 * abs(sin(now * 2 + Double(i) * 0.8))
                        ), lineWidth: 1)
                        .frame(width: CGFloat(30 + i * 20),
                               height: CGFloat(30 + i * 20))
                }
            }
        }
    }
}
```

### Full Kaaba Composite
```swift
struct KaabaOrb: View {
    let state: OrbDisplayState
    var size: CGFloat = 64

    var body: some View {
        ZStack {
            // Concentric flash rings
            ConcentricFlash()

            // Diamond with trail
            DiamondTrailOrb(size: size * 0.6)

            // Particle swirls around diamond
            ParticleSwirl(size: size, particleCount: 40, color: state.gradientStart)

            // Glow pulse overlay
            Circle()
                .fill(state.gradientStart.opacity(0.1))
                .frame(width: size * 1.5)
                .blur(radius: size * 0.3)
        }
        .frame(width: size * 2, height: size * 2)
    }
}
```

---

## Variant 2: Mesh Gradient Orb (Siri iOS 18)

Full-screen edge glow with animated mesh + breathing mask.

### Composition
```
Layer 1: MeshGradientView (T1) — fullscreen, .scaleEffect(1.3)
Layer 2: RoundedRectangle stroke — white, .blur(4) — visible in active state
Layer 3: Content — masked by AnimatedRectangle (T2)
```

### Integration
```swift
struct SiriGlowOrb: View {
    @Binding var isActive: Bool
    @State private var maskTimer: Float = 0
    @State private var gradientSpeed: Float = 0.03

    var body: some View {
        GeometryReader { geo in
            ZStack {
                OrbMeshGradientView(maskTimer: $maskTimer, gradientSpeed: $gradientSpeed)
                    .scaleEffect(1.3)
                    .opacity(isActive ? 1 : 0)

                if isActive {
                    RoundedRectangle(cornerRadius: 52, style: .continuous)
                        .stroke(Color.white, lineWidth: 4)
                        .blur(radius: 4)
                }

                // Your content here
                Color.black
                    .mask {
                        AnimatedRectangle(size: geo.size, cornerRadius: 48, t: CGFloat(maskTimer))
                            .scaleEffect(isActive ? 1.0 : 1.2)
                            .blur(radius: isActive ? 28 : 8)
                    }
            }
        }
        .ignoresSafeArea()
        .onAppear {
            Timer.scheduledTimer(withTimeInterval: 0.01, repeats: true) { _ in
                DispatchQueue.main.async {
                    maskTimer += (isActive ? 0.03 : 0)
                }
            }
        }
    }
}
```

---

## Variant 3: Particle Cloud Orb

Loose particle field without rigid sphere projection. Good for ambient/idle states.

```swift
struct ParticleCloudOrb: View {
    let color: Color
    let size: CGFloat
    let count: Int = 60

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 30.0)) { timeline in
            let now = timeline.date.timeIntervalSinceReferenceDate
            Canvas { context, canvasSize in
                let center = CGPoint(x: canvasSize.width / 2, y: canvasSize.height / 2)
                let radius = size * 0.4

                for i in 0..<count {
                    let seed = Double(i) * 1.618  // golden ratio spacing
                    let angle = now * (0.3 + seed * 0.01) + seed
                    let r = radius * (0.2 + 0.8 * abs(sin(seed * 0.7)))
                    let wobble = 3 * sin(now * 2 + seed)

                    let x = center.x + cos(angle) * r + wobble
                    let y = center.y + sin(angle) * r + wobble * 0.5
                    let dotSize = max(1, size * 0.02 * (1 + 0.5 * sin(now + seed)))
                    let alpha = 0.2 + 0.5 * abs(sin(now * 1.5 + seed * 0.3))

                    let rect = CGRect(x: x - dotSize/2, y: y - dotSize/2,
                                      width: dotSize, height: dotSize)
                    context.fill(Path(ellipseIn: rect),
                                 with: .color(color.opacity(alpha)))
                }
            }
            .frame(width: size, height: size)
        }
    }
}
```

---

## Variant 4: Random Swirl Particles

Particles following spiral/swirl paths around center point.

```swift
struct SwirlParticle {
    var angle: Double       // current angular position
    var radius: Double      // current distance from center
    var angularSpeed: Double // radians per frame
    var radialOscillation: Double // how much radius varies
    var phase: Double       // phase offset for oscillation
    var size: Double
}

// In Canvas draw:
for p in particles {
    let currentRadius = p.radius + p.radialOscillation * sin(now * 2 + p.phase)
    let currentAngle = p.angle + now * p.angularSpeed
    let x = center.x + cos(currentAngle) * currentRadius
    let y = center.y + sin(currentAngle) * currentRadius
    // draw dot at (x, y)
}
```

Key: each particle has its own `angularSpeed` (some fast, some slow) and `radialOscillation` (some tight orbits, some wide swings) for chaotic-but-beautiful motion.
