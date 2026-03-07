# Orb Techniques — Full Code Patterns

## T1: MeshGradient (iOS 18+) {#t1}

Animated 3x3 mesh with organic point motion. From [metasidd/PrototypeSiriAnimation](https://github.com/metasidd/PrototypeSiriAnimation).

```swift
import SwiftUI

struct OrbMeshGradientView: View {
    @Binding var maskTimer: Float
    @Binding var gradientSpeed: Float

    var body: some View {
        MeshGradient(width: 3, height: 3, points: [
            .init(0, 0), .init(0.0, 0), .init(1, 0),
            [sinInRange(-0.8...(-0.2), offset: 0.439, timeScale: 0.342, t: maskTimer),
             sinInRange(0.3...0.7, offset: 3.42, timeScale: 0.984, t: maskTimer)],
            [sinInRange(0.1...0.8, offset: 0.239, timeScale: 0.084, t: maskTimer),
             sinInRange(0.2...0.8, offset: 5.21, timeScale: 0.242, t: maskTimer)],
            [sinInRange(1.0...1.5, offset: 0.939, timeScale: 0.084, t: maskTimer),
             sinInRange(0.4...0.8, offset: 0.25, timeScale: 0.642, t: maskTimer)],
            [sinInRange(-0.8...0.0, offset: 1.439, timeScale: 0.442, t: maskTimer),
             sinInRange(1.4...1.9, offset: 3.42, timeScale: 0.984, t: maskTimer)],
            [sinInRange(0.3...0.6, offset: 0.339, timeScale: 0.784, t: maskTimer),
             sinInRange(1.0...1.2, offset: 1.22, timeScale: 0.772, t: maskTimer)],
            [sinInRange(1.0...1.5, offset: 0.939, timeScale: 0.056, t: maskTimer),
             sinInRange(1.3...1.7, offset: 0.47, timeScale: 0.342, t: maskTimer)]
        ], colors: [
            .yellow, .purple, .indigo,
            .orange, .red, .blue,
            .indigo, .green, .mint
        ])
        .onAppear {
            Timer.scheduledTimer(withTimeInterval: 0.01, repeats: true) { _ in
                DispatchQueue.main.async { maskTimer += gradientSpeed }
            }
        }
        .ignoresSafeArea()
    }
}

func sinInRange(_ range: ClosedRange<Float>, offset: Float, timeScale: Float, t: Float) -> Float {
    let amplitude = (range.upperBound - range.lowerBound) / 2
    let midPoint = (range.upperBound + range.lowerBound) / 2
    return midPoint + amplitude * sin(timeScale * t + offset)
}
```

**Key points:**
- Points at 0,0 and 1,0 rows are static (corners). Middle and bottom rows animate.
- Each animated point uses different offset + timeScale for non-repeating organic motion
- `gradientSpeed` controls overall animation pace (0.03 = slow, 0.05 = medium)

### MeshGradient as foregroundStyle

```swift
Image(systemName: "bubbles.and.sparkles.fill")
    .font(.system(size: 144, weight: .black))
    .foregroundStyle(
        MeshGradient(width: 2, height: 2, points: [
            [0, 0], [1, 0], [0, 1], [1, 1]
        ], colors: [.indigo, .cyan, .purple, .pink])
    )
```

---

## T2: AnimatedRectangle (Sine-Wave Edge Mask) {#t2}

Custom Shape whose edges wobble via sine functions. Used as mask for Siri breathing border.

```swift
struct AnimatedRectangle: Shape {
    var size: CGSize
    var padding: Double = 8.0
    var cornerRadius: CGFloat
    var t: CGFloat

    var animatableData: CGFloat {
        get { t }
        set { t = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let width = size.width
        let height = size.height
        let radius = cornerRadius

        let initialPoints = [
            CGPoint(x: padding + radius, y: padding),
            CGPoint(x: width * 0.25 + padding, y: padding),
            CGPoint(x: width * 0.75 + padding, y: padding),
            CGPoint(x: width - padding - radius, y: padding),
            CGPoint(x: width - padding, y: padding + radius),
            CGPoint(x: width - padding, y: height * 0.25 - padding),
            CGPoint(x: width - padding, y: height * 0.75 - padding),
            CGPoint(x: width - padding, y: height - padding - radius),
            CGPoint(x: width - padding - radius, y: height - padding),
            CGPoint(x: width * 0.75 - padding, y: height - padding),
            CGPoint(x: width * 0.25 - padding, y: height - padding),
            CGPoint(x: padding + radius, y: height - padding),
            CGPoint(x: padding, y: height - padding - radius),
            CGPoint(x: padding, y: height * 0.75 - padding),
            CGPoint(x: padding, y: height * 0.25 - padding),
            CGPoint(x: padding, y: padding + radius)
        ]

        // Sine-wave displacement per point
        let wobbleAmount: CGFloat = 10
        let points = initialPoints.map { point in
            CGPoint(
                x: point.x + wobbleAmount * sin(t + point.y * 0.1),
                y: point.y + wobbleAmount * sin(t + point.x * 0.1)
            )
        }

        path.move(to: CGPoint(x: padding, y: padding + radius))
        for point in points[0...2] { path.addLine(to: point) }
        for point in points[4...7] { path.addLine(to: point) }
        for point in points[8...10] { path.addLine(to: point) }
        for point in points[11...14] { path.addLine(to: point) }
        path.closeSubpath()
        return path
    }
}
```

**Usage as mask:**
```swift
content.mask {
    GeometryReader { geo in
        AnimatedRectangle(size: geo.size, cornerRadius: 48, t: CGFloat(maskTimer))
            .scaleEffect(isActive ? 1.0 : 1.2)
            .blur(radius: isActive ? 28 : 8)
    }
}
```

---

## T3: Layer-Based Rotation {#t3}

Classic Siri icon clone using Figma-exported PNG layers. From [Amos Gyamfi's gist](https://gist.github.com/amosgyamfi/b611c216604fd40a5aad2673fc5cf0b4).

```swift
struct LayeredSiriOrb: View {
    @State var isRotating = false

    var body: some View {
        ZStack {
            ZStack {
                Image("shadow")
                Image("icon-bg")

                Image("pink-top")
                    .rotationEffect(.degrees(isRotating ? 320 : -360))
                    .hueRotation(.degrees(isRotating ? -270 : 60))

                Image("pink-left")
                    .rotationEffect(.degrees(isRotating ? -360 : 180))
                    .hueRotation(.degrees(isRotating ? -220 : 300))

                Image("blue-middle")
                    .rotationEffect(.degrees(isRotating ? -360 : 420))
                    .hueRotation(.degrees(isRotating ? -150 : 0))
                    .rotation3DEffect(.degrees(75), axis: (x: isRotating ? 1 : 5, y: 0, z: 0))

                Image("blue-right")
                    .rotationEffect(.degrees(isRotating ? -360 : 420))
                    .hueRotation(.degrees(isRotating ? 720 : -50))
                    .rotation3DEffect(.degrees(75), axis: (x: 1, y: 0, z: isRotating ? -5 : 15))

                Image("intersect")
                    .rotationEffect(.degrees(isRotating ? 30 : -420))
                    .hueRotation(.degrees(isRotating ? 0 : 720))
                    .rotation3DEffect(.degrees(15), axis: (x: 1, y: 1, z: 1),
                                      perspective: isRotating ? 5 : -5)

                Image("green-right")
                    .rotationEffect(.degrees(isRotating ? -300 : 360))
                    .hueRotation(.degrees(isRotating ? 300 : -15))
                    .rotation3DEffect(.degrees(15), axis: (x: 1, y: isRotating ? -1 : 1, z: 0),
                                      perspective: isRotating ? -1 : 1)

                Image("green-left")
                    .rotationEffect(.degrees(isRotating ? 360 : -360))
                    .hueRotation(.degrees(isRotating ? 180 : 50))
                    .rotation3DEffect(.degrees(75), axis: (x: 1, y: isRotating ? -5 : 15, z: 0))

                Image("bottom-pink")
                    .rotationEffect(.degrees(isRotating ? 400 : -360))
                    .hueRotation(.degrees(isRotating ? 0 : 230))
                    .opacity(0.25)
                    .blendMode(.multiply)
                    .rotation3DEffect(.degrees(75), axis: (x: 5, y: isRotating ? 1 : -45, z: 0))
            }
            .blendMode(isRotating ? .hardLight : .difference)

            Image("highlight")
                .rotationEffect(.degrees(isRotating ? 360 : 250))
                .hueRotation(.degrees(isRotating ? 0 : 230))
                .padding()
                .onAppear {
                    withAnimation(.easeInOut(duration: 12).repeatForever(autoreverses: false)) {
                        isRotating.toggle()
                    }
                }
        }
        .scaleEffect(0.6)
    }
}
```

**Key patterns:**
- Each layer: different rotation angles + different hue rotation shifts
- Mix 2D `.rotationEffect` with `.rotation3DEffect` on select layers
- Blend modes (`.hardLight`, `.difference`, `.multiply`) create color mixing
- Single boolean `isRotating` drives all layers via ternary operators
- 12-second loop, no autoreversal for continuous spin

**Asset source:** Figma community "iOS 14 Siri Icon" — export each layer as PNG

---

## T4: Hue-Shifting Animated Gradient {#t4}

From [Rudrank Riyam](https://rudrank.com/exploring-swiftui-creating-new-siri-animation).

```swift
struct HueShiftGradientView: View {
    private let colors: [Color] = [
        .purple, .blue, .cyan, .pink,
        .indigo, .mint, .red, .orange, .yellow
    ]

    var body: some View {
        TimelineView(.animation) { timeline in
            MeshGradient(
                width: 3, height: 3,
                locations: .points([
                    .init(0, 0), .init(0.5, 0), .init(1, 0),
                    .init(0, 0.5), .init(0.5, 0.5), .init(1, 0.5),
                    .init(0, 1), .init(0.5, 1), .init(1, 1)
                ]),
                colors: .colors(animatedColors(for: timeline.date)),
                background: .black,
                smoothsColors: true
            )
        }
        .ignoresSafeArea()
    }

    private func animatedColors(for date: Date) -> [Color] {
        let phase = CGFloat(date.timeIntervalSince1970)
        return colors.enumerated().map { index, color in
            let hueShift = cos(phase + Double(index) * 0.3) * 0.1
            return shiftHue(of: color, by: hueShift)
        }
    }

    private func shiftHue(of color: Color, by amount: Double) -> Color {
        var hue: CGFloat = 0, saturation: CGFloat = 0
        var brightness: CGFloat = 0, alpha: CGFloat = 0
        #if canImport(UIKit)
        UIColor(color).getHue(&hue, saturation: &saturation,
                              brightness: &brightness, alpha: &alpha)
        #else
        NSColor(color).getHue(&hue, saturation: &saturation,
                              brightness: &brightness, alpha: &alpha)
        #endif
        hue += CGFloat(amount)
        hue = hue.truncatingRemainder(dividingBy: 1.0)
        if hue < 0 { hue += 1 }
        return Color(hue: Double(hue), saturation: Double(saturation),
                     brightness: Double(brightness), opacity: Double(alpha))
    }
}
```

---

## T5: Metal Ripple Shader {#t5}

From [WWDC24 session 10151](https://developer.apple.com/videos/play/wwdc2024/10151/).

### RippleEffect.metal
```metal
#include <metal_stdlib>
#include <SwiftUI/SwiftUI.h>
using namespace metal;

[[ stitchable ]]
half4 Ripple(
    float2 position, SwiftUI::Layer layer,
    float2 origin, float time,
    float amplitude, float frequency, float decay, float speed
) {
    float distance = length(position - origin);
    float delay = distance / speed;
    time -= delay;
    time = max(0.0, time);
    float rippleAmount = amplitude * sin(frequency * time) * exp(-decay * time);
    float2 n = normalize(position - origin);
    float2 newPosition = position + rippleAmount * n;
    half4 color = layer.sample(newPosition);
    color.rgb += 0.3 * (rippleAmount / amplitude) * color.a;
    return color;
}
```

### SwiftUI Modifier
```swift
struct RippleEffect<T: Equatable>: ViewModifier {
    var origin: CGPoint
    var trigger: T

    func body(content: Content) -> some View {
        content.keyframeAnimator(initialValue: 0, trigger: trigger) { view, elapsedTime in
            view.modifier(RippleModifier(origin: origin, elapsedTime: elapsedTime, duration: 3))
        } keyframes: { _ in
            MoveKeyframe(0)
            LinearKeyframe(3, duration: 3)
        }
    }
}

struct RippleModifier: ViewModifier {
    var origin: CGPoint
    var elapsedTime: TimeInterval
    var duration: TimeInterval
    var amplitude: Double = 12
    var frequency: Double = 15
    var decay: Double = 8
    var speed: Double = 2000

    func body(content: Content) -> some View {
        let shader = ShaderLibrary.Ripple(
            .float2(origin), .float(elapsedTime),
            .float(amplitude), .float(frequency), .float(decay), .float(speed)
        )
        content.visualEffect { view, _ in
            view.layerEffect(shader, maxSampleOffset: CGSize(width: amplitude, height: amplitude),
                             isEnabled: 0 < elapsedTime && elapsedTime < duration)
        }
    }
}
```

**Usage:** `.modifier(RippleEffect(at: tapPoint, trigger: tapCount))`

---

## T6: 3D Particle Sphere {#t6}

Port of JS particle sphere to SwiftUI Canvas. Particles spawn on sphere surface, rotate, fade via envelope.

```swift
struct ParticleSphereView: View {
    let sphereRadius: CGFloat
    let particleCount: Int
    let color: Color

    @State private var particles: [Particle] = []
    @State private var turnAngle: Double = 0
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    struct Particle {
        var x, y, z: Double
        var velX, velY, velZ: Double
        var age: Int = 0
        var stuckTime: Int
        var attack: Int = 50
        var hold: Int = 50
        var decay: Int = 100
        var alpha: Double = 0
        var dead: Bool = false
    }

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 30.0)) { timeline in
            Canvas { context, size in
                let center = CGPoint(x: size.width / 2, y: size.height / 2)
                let fLen: Double = 320
                let zMax = fLen - 2
                let sinA = sin(turnAngle)
                let cosA = cos(turnAngle)
                let sphereCenterZ = -3 - sphereRadius

                for p in particles where !p.dead {
                    let rotX = cosA * p.x + sinA * (p.z - sphereCenterZ)
                    let rotZ = -sinA * p.x + cosA * (p.z - sphereCenterZ) + sphereCenterZ
                    guard rotZ < zMax else { continue }

                    let m = fLen / (fLen - rotZ)
                    let projX = rotX * m + center.x
                    let projY = p.y * m + center.y

                    let depthAlpha = max(0, min(1, 1 - rotZ / -750))
                    let finalAlpha = depthAlpha * p.alpha

                    let dotSize = max(1, m * 2.5)
                    let rect = CGRect(x: projX - dotSize / 2, y: projY - dotSize / 2,
                                      width: dotSize, height: dotSize)
                    context.fill(Path(ellipseIn: rect), with: .color(color.opacity(finalAlpha)))
                }
            }
            .onChange(of: timeline.date) { _, _ in
                guard !reduceMotion else { return }
                updateParticles()
            }
        }
        .onAppear { spawnInitialParticles() }
    }

    private mutating func spawnParticle() -> Particle {
        let theta = Double.random(in: 0...(2 * .pi))
        let phi = acos(Double.random(in: -1...1))
        let x = sphereRadius * sin(phi) * cos(theta)
        let y = sphereRadius * sin(phi) * sin(theta)
        let z = sphereRadius * cos(phi) + (-3 - sphereRadius)
        return Particle(x: x, y: y, z: z,
                        velX: 0.002 * x, velY: 0.002 * y, velZ: 0.002 * (z - (-3 - sphereRadius)),
                        stuckTime: Int.random(in: 90...110))
    }

    // Update: age++, move after stuck, envelope alpha, recycle dead
    private func updateParticles() {
        turnAngle += 2 * .pi / 1200
        // ... age, move, envelope, recycle logic per T6 spec
    }
}
```

**Envelope system:**
```
age < attack:      alpha = (holdValue / attack) * age
age < attack+hold: alpha = holdValue
age < a+h+decay:   alpha = holdValue * (1 - (age-a-h) / decay)
else:               dead = true
```

---

## T7: Angular Gradient Glow Shadow {#t7}

Simple rotating glow behind any shape.

```swift
struct GlowShadow: View {
    @State private var isAnimating = false

    var body: some View {
        ZStack {
            // Shadow layer
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(
                    AngularGradient(
                        colors: [.teal, .pink, .teal],
                        center: .center,
                        angle: .degrees(isAnimating ? 360 : 0)
                    )
                )
                .frame(width: 260, height: 60)
                .blur(radius: 20)
                .onAppear {
                    withAnimation(.linear(duration: 7).repeatForever(autoreverses: false)) {
                        isAnimating = true
                    }
                }

            // Content layer
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(.teal)
                .frame(width: 260, height: 60)
                .overlay(Text("Get Premium").bold().foregroundStyle(.black))
        }
    }
}
```

**Blur radius guide:**
- 5 = tight highlight
- 20 = standard shadow
- 50 = diffused ambient glow
