# Smoke & Fog Simulation

## Overview

Three approaches ordered by complexity: (1) Canvas noise blobs, (2) SpriteKit/Vortex emitters, (3) Metal ray marching. Choose based on fidelity needs and performance budget.

## Approach 1: Canvas Noise Blobs (Simplest, SwiftUI-Native)

This is the OCMiniOrb smoke layer pattern. Soft, orbiting blobs rendered in a single Canvas draw call.

### How It Works

- N circles (4-8) orbit a center point at different radii and speeds
- Each blob has soft alpha (0.05-0.15) and large radius
- Perlin/simplex noise offsets position for organic drift
- Composite via `.normal` or `.plusLighter` blend mode

### Swift Implementation

```swift
struct SmokeLayer: View {
    let blobCount: Int = 6
    let baseRadius: CGFloat = 40
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        if reduceMotion {
            // Static fallback: single soft gradient
            Circle()
                .fill(RadialGradient(
                    colors: [.white.opacity(0.08), .clear],
                    center: .center,
                    startRadius: 0,
                    endRadius: baseRadius
                ))
        } else {
            TimelineView(.animation(minimumInterval: 1.0 / 30.0)) { ctx in
                Canvas { context, size in
                    let t = ctx.date.timeIntervalSinceReferenceDate
                    let center = CGPoint(x: size.width / 2, y: size.height / 2)

                    for i in 0..<blobCount {
                        let fi = Double(i)
                        let orbitRadius = baseRadius * (0.3 + 0.15 * fi)
                        let speed = (3.0 + fi * 0.7) // seconds per revolution
                        let angle = (t / speed + fi * .pi * 2 / Double(blobCount))
                            .truncatingRemainder(dividingBy: .pi * 2)

                        // Noise-like offset using layered sine
                        let noiseX = sin(t * 0.3 + fi * 1.7) * 8
                        let noiseY = cos(t * 0.4 + fi * 2.3) * 6

                        let x = center.x + cos(angle) * orbitRadius + noiseX
                        let y = center.y + sin(angle) * orbitRadius + noiseY
                        let blobSize = baseRadius * (0.5 + 0.3 * sin(t * 0.5 + fi))

                        let rect = CGRect(
                            x: x - blobSize / 2,
                            y: y - blobSize / 2,
                            width: blobSize,
                            height: blobSize
                        )

                        context.opacity = 0.06 + 0.04 * sin(t * 0.8 + fi * 1.3)
                        context.fill(
                            Ellipse().path(in: rect),
                            with: .radialGradient(
                                Gradient(colors: [.white.opacity(0.3), .clear]),
                                center: CGPoint(x: x, y: y),
                                startRadius: 0,
                                endRadius: blobSize / 2
                            )
                        )
                    }
                }
            }
        }
    }
}
```

### Performance Notes

- 30fps cap is sufficient for smoke (organic motion hides frame skips)
- 4-8 blobs is the sweet spot. More than 12 has diminishing returns
- Use `.opacity` on context, not SwiftUI `.opacity()` modifier (avoids extra compositing pass)
- Canvas renders all blobs in a single draw call

## Approach 2: SpriteKit / Vortex Emitters

### SpriteKit SKEmitterNode

Best for quick smoke with built-in physics (gravity, wind, turbulence).

```swift
import SpriteKit

func createSmokeEmitter() -> SKEmitterNode {
    let emitter = SKEmitterNode()

    // Emission
    emitter.particleBirthRate = 30
    emitter.numParticlesToEmit = 0  // infinite

    // Lifetime
    emitter.particleLifetime = 3.0
    emitter.particleLifetimeRange = 1.0

    // Size
    emitter.particleSize = CGSize(width: 64, height: 64)
    emitter.particleScaleRange = 0.5
    emitter.particleScaleSpeed = 0.3  // grow over lifetime

    // Movement
    emitter.emissionAngle = .pi / 2  // upward
    emitter.emissionAngleRange = .pi / 4
    emitter.particleSpeed = 20
    emitter.particleSpeedRange = 10
    emitter.yAcceleration = 15  // gentle rise

    // Alpha
    emitter.particleAlpha = 0.3
    emitter.particleAlphaRange = 0.1
    emitter.particleAlphaSpeed = -0.1  // fade out

    // Color
    emitter.particleColor = .gray
    emitter.particleColorBlendFactor = 1.0

    // Blend mode
    emitter.particleBlendMode = .alpha

    // Texture: use a soft circle or Gaussian blob texture
    emitter.particleTexture = SKTexture(imageNamed: "smoke_blob")

    return emitter
}
```

### Vortex (SwiftUI-Native)

```swift
import Vortex

struct SmokeView: View {
    var body: some View {
        VortexView(.smoke) {
            Circle()
                .fill(.gray.opacity(0.3))
                .frame(width: 32, height: 32)
                .blur(radius: 8)
                .tag("smoke")
        }
    }
}

// Custom smoke preset
extension VortexSystem {
    static var gentleSmoke: VortexSystem {
        VortexSystem(
            tags: ["smoke"],
            birthRate: 15,
            lifespan: 4,
            speed: 0.1,
            speedVariation: 0.05,
            angle: .degrees(270),
            angleRange: .degrees(30),
            size: 0.5,
            sizeVariation: 0.2,
            sizeMultiplierAtDeath: 2.0,
            stretchFactor: 1,
            position: .init(x: 0.5, y: 1.0),
            positionRange: .init(x: 0.3, y: 0),
            attractionCenter: nil,
            attractionStrength: 0,
            dampingFactor: 2,
            colors: .random(
                .gray.opacity(0.2),
                .gray.opacity(0.1),
                .clear
            ),
            blendMode: .normal
        )
    }
}
```

## Approach 3: Ray Marching (Metal Fragment Shader)

Volumetric fog using density field sampling. Most realistic but most expensive.

### Algorithm

1. Cast a ray from camera through each pixel
2. Step along the ray at fixed intervals (4-8 steps for real-time)
3. At each step, sample a 3D noise function for density
4. Accumulate color and alpha using Beer-Lambert absorption
5. Early-out when accumulated alpha > 0.95

### MSL Fragment Shader

```metal
#include <metal_stdlib>
using namespace metal;

// Simple 3D hash for noise
float hash3D(float3 p) {
    p = fract(p * float3(443.897, 441.423, 437.195));
    p += dot(p, p.yzx + 19.19);
    return fract((p.x + p.y) * p.z);
}

// Value noise 3D
float valueNoise3D(float3 p) {
    float3 i = floor(p);
    float3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);  // smoothstep

    float a = hash3D(i);
    float b = hash3D(i + float3(1, 0, 0));
    float c = hash3D(i + float3(0, 1, 0));
    float d = hash3D(i + float3(1, 1, 0));
    float e = hash3D(i + float3(0, 0, 1));
    float g = hash3D(i + float3(1, 0, 1));
    float h = hash3D(i + float3(0, 1, 1));
    float k = hash3D(i + float3(1, 1, 1));

    return mix(
        mix(mix(a, b, f.x), mix(c, d, f.x), f.y),
        mix(mix(e, g, f.x), mix(h, k, f.x), f.y),
        f.z
    );
}

// Fractal Brownian Motion
float fbm3D(float3 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < octaves; i++) {
        value += amplitude * valueNoise3D(p * frequency);
        amplitude *= 0.5;
        frequency *= 2.0;
    }
    return value;
}

// Density function for fog volume
float fogDensity(float3 p, float time) {
    // Base density from FBM noise
    float density = fbm3D(p * 0.5 + float3(time * 0.1, 0, time * 0.05), 4);

    // Vertical falloff (fog heavier at bottom)
    density *= smoothstep(1.0, 0.0, p.y);

    // Shape mask (spherical bounds)
    float dist = length(p);
    density *= smoothstep(2.0, 0.5, dist);

    return max(0.0, density - 0.2);  // threshold
}

// Ray march fog
[[stitchable]]
half4 volumetricFog(
    float2 position,
    half4 currentColor,
    float2 size,
    float time,
    float fogIntensity
) {
    float2 uv = position / size;
    uv = uv * 2.0 - 1.0;  // -1 to 1
    uv.x *= size.x / size.y;  // aspect correction

    // Camera setup
    float3 ro = float3(0, 0.3, -2);   // ray origin
    float3 rd = normalize(float3(uv, 1.0));  // ray direction

    // March
    float4 accum = float4(0);
    float stepSize = 0.3;
    int steps = 8;  // keep low for real-time

    for (int i = 0; i < steps; i++) {
        float t = float(i) * stepSize;
        float3 p = ro + rd * t;

        float d = fogDensity(p, time) * fogIntensity;

        if (d > 0.01) {
            // Beer-Lambert absorption
            float3 fogColor = float3(0.6, 0.65, 0.7);  // blue-gray
            float alpha = 1.0 - exp(-d * stepSize * 3.0);

            // Front-to-back compositing
            accum.rgb += (1.0 - accum.a) * alpha * fogColor;
            accum.a += (1.0 - accum.a) * alpha;
        }

        if (accum.a > 0.95) break;  // early out
    }

    // Blend with existing content
    half4 fog = half4(half3(accum.rgb), half(accum.a));
    return mix(currentColor, fog, fog.a);
}
```

### SwiftUI Integration

```swift
struct FogOverlay: View {
    let intensity: Float

    var body: some View {
        TimelineView(.animation) { ctx in
            let time = Float(ctx.date.timeIntervalSinceReferenceDate)
            Rectangle()
                .fill(.clear)
                .colorEffect(
                    ShaderLibrary.volumetricFog(
                        .float2(400, 400),   // size
                        .float(time),
                        .float(intensity)
                    )
                )
        }
    }
}
```

## Performance Comparison

| Approach | Draw Calls | GPU Cost | Fidelity | Best For |
|----------|-----------|----------|----------|----------|
| Canvas blobs | 1 | Low | Soft, stylized | UI accents, orb layers |
| SpriteKit emitter | 1-2 | Low-Med | Textured smoke | 2D game effects |
| Vortex | 1 | Low | SwiftUI-styled | Quick prototypes |
| Metal ray march | 1 | High | Volumetric 3D | Hero effects, cutscenes |

## When to Use Flipbook vs Procedural

**Flipbook (pre-rendered sprite sheet):**
- Consistent look across devices
- Zero runtime computation for smoke shape
- Best when art direction demands a specific smoke style
- 16-64 frames, atlas texture, cycle or one-shot

**Procedural (noise-based):**
- Infinite variation, never repeats
- Reacts to parameters (wind, intensity, color)
- Higher GPU cost but smaller asset size
- Best for dynamic, interactive effects

## Blur Radius Budget

| Platform | Max Safe Blur | Notes |
|----------|---------------|-------|
| iPhone 12 | 15pt | Full-screen fog overlay |
| iPhone 15 Pro | 25pt | With downscaled target |
| M1 Mac | 40pt | Desktop has headroom |
| visionOS | 20pt | Shared GPU with compositor |

Exceeding these causes >16ms frame times. For larger blurs, render to a half-resolution texture first.

## Cross-References

- **orb skill** `references/existing-impl.md` -- OCMiniOrb smoke layer (Layer 5) uses the Canvas blob approach
- **swiftui-animation** -- TimelineView patterns and animation interval tuning
- **Inferno** -- Pre-built Metal noise shaders that can serve as density functions
