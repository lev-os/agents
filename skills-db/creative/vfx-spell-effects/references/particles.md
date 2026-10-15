# Particle Systems

## API Comparison

| API | Platform | SwiftUI Integration | GPU Accelerated | Custom Forces | Best For |
|-----|----------|---------------------|-----------------|---------------|----------|
| **Vortex** | iOS 16+, macOS 13+ | Native (SwiftUI view) | Partial (CPU update) | Attraction, damping | Quick prototypes, UI accents |
| **SpriteKit SKEmitterNode** | iOS 7+, macOS 10.10+ | `SpriteView` wrapper | Yes (GPU render) | Gravity, turbulence | 2D game effects, textured particles |
| **CAEmitterLayer** | iOS 5+, macOS 10.6+ | `UIViewRepresentable` | Yes (Core Animation) | Gravity, velocity | Background effects, ambient particles |
| **Metal Compute** | iOS 9+, macOS 10.11+ | `MTKView` / texture | Full GPU | Anything (custom kernel) | High particle count, complex physics |
| **SwiftUI Canvas** | iOS 15+, macOS 12+ | Native | CPU only | Manual in draw loop | Small counts (<200), full control |

### Decision Guide

```
How many particles?
|
|-- < 100 → SwiftUI Canvas (simplest, no dependencies)
|-- 100-500 → Vortex or SpriteKit (good defaults, GPU render)
|-- 500-2000 → SpriteKit or Metal compute (need GPU update)
|-- 2000-10000 → Metal compute (mandatory for mobile)
|-- 10000+ → Metal compute with instanced rendering
```

---

## GPU Particle Architecture (Metal Compute)

### Pipeline Overview

```
[Frame N]
    |
    v
Compute Pass: particleUpdate kernel
    - Read particle buffer (position, velocity, age, ...)
    - Apply forces (gravity, noise, attraction)
    - Advance position += velocity * dt
    - Age particles, mark dead for recycling
    - Write updated particle buffer
    |
    v
Vertex Pass: particle vertex shader
    - Read particle buffer
    - Generate camera-facing quads (2 triangles per particle)
    - Pass color, alpha, size to fragment shader
    |
    v
Fragment Pass: particle fragment shader
    - Sample texture (soft circle, spark, smoke)
    - Multiply by particle color and alpha
    - Output with additive or alpha blend
```

### Particle Struct (GPU-Side)

```metal
struct Particle {
    float2 position;
    float2 velocity;
    float  age;
    float  lifetime;
    float  size;
    float  rotation;
    half4  color;
    uint   flags;  // bit 0: alive, bit 1: recyclable
};
```

### Metal Compute Kernel

```metal
#include <metal_stdlib>
using namespace metal;

struct Particle {
    float2 position;
    float2 velocity;
    float  age;
    float  lifetime;
    float  size;
    float  rotation;
    half4  color;
    uint   flags;
};

struct SimParams {
    float  dt;
    float  gravity;
    float2 wind;
    float2 attractorPos;
    float  attractorStrength;
    float  noiseScale;
    float  noiseTime;
    float  damping;
    uint   particleCount;
};

// Simple 2D noise for turbulence
float hash2D(float2 p) {
    float3 p3 = fract(float3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

float noise2D(float2 p) {
    float2 i = floor(p);
    float2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = hash2D(i);
    float b = hash2D(i + float2(1, 0));
    float c = hash2D(i + float2(0, 1));
    float d = hash2D(i + float2(1, 1));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

kernel void particleUpdate(
    device Particle* particles [[buffer(0)]],
    constant SimParams& params [[buffer(1)]],
    uint id [[thread_position_in_grid]]
) {
    if (id >= params.particleCount) return;

    Particle p = particles[id];

    // Skip dead particles
    if ((p.flags & 1) == 0) return;

    // Age
    p.age += params.dt;
    if (p.age >= p.lifetime) {
        p.flags = 2;  // mark recyclable
        particles[id] = p;
        return;
    }

    float lifeRatio = p.age / p.lifetime;

    // Forces
    float2 force = float2(0);

    // Gravity
    force.y += params.gravity;

    // Wind
    force += params.wind;

    // Attractor
    float2 toAttractor = params.attractorPos - p.position;
    float dist = length(toAttractor);
    if (dist > 0.001) {
        force += normalize(toAttractor) * params.attractorStrength / (dist * dist + 1.0);
    }

    // Noise turbulence
    float2 noisePos = p.position * params.noiseScale + float2(params.noiseTime);
    float nx = noise2D(noisePos) * 2.0 - 1.0;
    float ny = noise2D(noisePos + float2(100, 100)) * 2.0 - 1.0;
    force += float2(nx, ny) * 50.0;

    // Integrate
    p.velocity += force * params.dt;
    p.velocity *= (1.0 - params.damping * params.dt);  // damping
    p.position += p.velocity * params.dt;

    // Fade alpha over lifetime
    float fadeIn = smoothstep(0.0, 0.1, lifeRatio);
    float fadeOut = 1.0 - smoothstep(0.7, 1.0, lifeRatio);
    p.color.a = half(fadeIn * fadeOut);

    // Shrink over lifetime (optional)
    // p.size *= (1.0 - lifeRatio * 0.5);

    particles[id] = p;
}
```

### Swift Host Code

```swift
import MetalKit

class ParticleSystem {
    let device: MTLDevice
    let computePipeline: MTLComputePipelineState
    let particleBuffer: MTLBuffer
    let maxParticles: Int

    // Recycle bin (free list)
    private var freeIndices: [Int] = []
    private var activeCount: Int = 0

    init(device: MTLDevice, maxParticles: Int = 2000) {
        self.device = device
        self.maxParticles = maxParticles

        let library = device.makeDefaultLibrary()!
        let function = library.makeFunction(name: "particleUpdate")!
        self.computePipeline = try! device.makeComputePipelineState(function: function)

        let bufferSize = MemoryLayout<Particle>.stride * maxParticles
        self.particleBuffer = device.makeBuffer(length: bufferSize, options: .storageModeShared)!

        // All indices start free
        self.freeIndices = Array((0..<maxParticles).reversed())
    }

    /// Emit particles (CPU-side, pre-frame)
    func emit(count: Int, at position: SIMD2<Float>, velocity: SIMD2<Float>, spread: Float, lifetime: Float) {
        let particles = particleBuffer.contents().bindMemory(to: Particle.self, capacity: maxParticles)

        for _ in 0..<min(count, freeIndices.count) {
            guard let idx = freeIndices.popLast() else { break }

            let angle = Float.random(in: -.pi...(.pi)) * spread
            let speed = Float.random(in: 0.8...1.2)
            let rotated = SIMD2<Float>(
                velocity.x * cos(angle) - velocity.y * sin(angle),
                velocity.x * sin(angle) + velocity.y * cos(angle)
            ) * speed

            particles[idx] = Particle(
                position: position + SIMD2<Float>.random(in: -2...2),
                velocity: rotated,
                age: 0,
                lifetime: lifetime * Float.random(in: 0.8...1.2),
                size: Float.random(in: 3...8),
                rotation: Float.random(in: 0...(2 * .pi)),
                color: SIMD4<Float16>(1, 1, 1, 1),
                flags: 1  // alive
            )

            activeCount += 1
        }
    }

    /// Reclaim dead particles (CPU-side, post-compute)
    func reclaimDead() {
        let particles = particleBuffer.contents().bindMemory(to: Particle.self, capacity: maxParticles)
        for i in 0..<maxParticles {
            if particles[i].flags == 2 {  // recyclable
                particles[i].flags = 0
                freeIndices.append(i)
                activeCount -= 1
            }
        }
    }

    /// Dispatch compute shader
    func update(commandBuffer: MTLCommandBuffer, params: SimParams) {
        guard let encoder = commandBuffer.makeComputeCommandEncoder() else { return }
        encoder.setComputePipelineState(computePipeline)
        encoder.setBuffer(particleBuffer, offset: 0, index: 0)

        var simParams = params
        withUnsafePointer(to: &simParams) { ptr in
            encoder.setBytes(ptr, length: MemoryLayout<SimParams>.size, index: 1)
        }

        let threadGroupSize = min(256, computePipeline.maxTotalThreadsPerThreadgroup)
        let threadGroups = (maxParticles + threadGroupSize - 1) / threadGroupSize
        encoder.dispatchThreadgroups(
            MTLSize(width: threadGroups, height: 1, depth: 1),
            threadsPerThreadgroup: MTLSize(width: threadGroupSize, height: 1, depth: 1)
        )

        encoder.endEncoding()
    }
}
```

---

## Emission Patterns

| Pattern | Shape | Use Case | Code Snippet |
|---------|-------|----------|-------------|
| Point | Single position | Sparks from impact | `pos = center` |
| Ring | Circle circumference | Healing aura, shockwave | `pos = center + r * [cos(a), sin(a)]` |
| Sphere | 3D sphere surface | Explosion, magic burst | `pos = center + r * randomOnSphere()` |
| Cone | Directional cone | Fire breath, jet stream | `pos = origin; vel = rotated(forward, random(-half_angle, half_angle))` |
| Line | Along a line segment | Sword trail, laser | `pos = lerp(start, end, random())` |
| Mesh surface | Triangle surface | Aura around character | `pos = randomPointOnTriangle(mesh)` |

### Sphere Emission Helper

```swift
func randomOnUnitSphere() -> SIMD3<Float> {
    let theta = Float.random(in: 0...(2 * .pi))
    let phi = acos(Float.random(in: -1...1))
    return SIMD3<Float>(
        sin(phi) * cos(theta),
        sin(phi) * sin(theta),
        cos(phi)
    )
}
```

---

## Particle Lifecycle

```
SPAWN                      UPDATE                         FADE & RECYCLE
  |                          |                               |
  v                          v                               v
Allocate from pool    Apply forces each frame         Alpha -> 0 over
Set initial pos/vel   Gravity, wind, noise            last 30% of lifetime
Set lifetime          Collision (optional)             Size -> 0 (optional)
Set color/size        Age += dt                        flags = recyclable
flags = alive         Clamp to bounds                  Return to free list
```

### Pool Pattern (CRITICAL for Performance)

**NEVER** allocate or deallocate particles during gameplay. Pre-allocate the full buffer once.

```swift
// BAD: Array append/remove (allocations every frame)
particles.append(Particle(...))  // malloc
particles.remove(at: deadIndex)  // realloc + shift

// GOOD: Fixed buffer + free list (zero allocation)
let idx = freeList.popLast()!
buffer[idx] = Particle(...)  // overwrite in-place
buffer[idx].flags = .alive

// On death:
buffer[idx].flags = .recyclable
freeList.append(idx)
```

---

## Vortex Presets

### Fire

```swift
import Vortex

extension VortexSystem {
    static var magicFire: VortexSystem {
        VortexSystem(
            tags: ["fire"],
            birthRate: 60,
            lifespan: 1.5,
            speed: 0.3,
            speedVariation: 0.15,
            angle: .degrees(270),     // upward
            angleRange: .degrees(20),
            size: 0.3,
            sizeVariation: 0.15,
            sizeMultiplierAtDeath: 0.1,
            stretchFactor: 1.5,
            position: .init(x: 0.5, y: 0.9),
            positionRange: .init(x: 0.1, y: 0),
            attractionCenter: nil,
            attractionStrength: 0,
            dampingFactor: 3,
            colors: .ramp(
                .yellow,
                .orange,
                .red,
                .red.opacity(0.3),
                .clear
            ),
            blendMode: .plusLighter
        )
    }
}

// Usage
VortexView(.magicFire) {
    Circle()
        .fill(.white)
        .frame(width: 16, height: 16)
        .blur(radius: 4)
        .tag("fire")
}
.frame(width: 200, height: 300)
```

### Magic Sparkles

```swift
extension VortexSystem {
    static var magicSparkles: VortexSystem {
        VortexSystem(
            tags: ["sparkle"],
            birthRate: 40,
            lifespan: 2.0,
            speed: 0.15,
            speedVariation: 0.1,
            angle: .degrees(270),
            angleRange: .degrees(360),  // all directions
            size: 0.15,
            sizeVariation: 0.1,
            sizeMultiplierAtDeath: 0.0,
            stretchFactor: 1,
            position: .init(x: 0.5, y: 0.5),
            positionRange: .init(x: 0.3, y: 0.3),
            attractionCenter: .init(x: 0.5, y: 0.5),
            attractionStrength: -0.5,  // repel from center
            dampingFactor: 2,
            colors: .random(
                .cyan,
                .blue,
                .purple,
                .white
            ),
            blendMode: .plusLighter
        )
    }
}
```

### Impact Burst

```swift
extension VortexSystem {
    static var impactBurst: VortexSystem {
        VortexSystem(
            tags: ["spark"],
            birthRate: 200,           // high burst
            emissionLimit: 40,         // only 40 total
            lifespan: 0.6,
            speed: 1.0,
            speedVariation: 0.5,
            angle: .degrees(0),
            angleRange: .degrees(360), // radial
            size: 0.1,
            sizeVariation: 0.05,
            sizeMultiplierAtDeath: 0.0,
            stretchFactor: 3,          // elongated sparks
            position: .init(x: 0.5, y: 0.5),
            positionRange: .zero,
            attractionCenter: nil,
            attractionStrength: 0,
            dampingFactor: 4,          // decelerate quickly
            colors: .ramp(
                .white,
                .yellow,
                .orange,
                .clear
            ),
            blendMode: .plusLighter
        )
    }
}
```

---

## Dota 2 Particle Reference

Dota 2 effects are the gold standard for game VFX readability. Key principles:

| Principle | Value | Why |
|-----------|-------|-----|
| Particles per impact | 20-40 | Enough to read, not enough to obscure gameplay |
| Particle lifetime | Matches audio cue | A/V sync makes effects feel "real" |
| Color palette | 2-3 colors per effect | Readability; too many colors = visual noise |
| Additive blend | Glow particles only | Core shapes use alpha blend for silhouette |
| Trail particles | 5-10 per frame | Attached to projectile, low birth rate |
| Screen-space effects | Sparingly | Flash/shake reserved for high-impact moments |

### Storm Spirit Ball Lightning (Trailing Effect)

```
Main body: Central glow sphere (1 quad, additive)
Ring: Rotating disc texture (1 quad, additive, rotates at 720 deg/s)
Trail: 8-12 particles per frame along path, lifetime 0.3s, size decay
Sparks: 2-4 random sparks per frame, short lifetime (0.15s), high velocity
Environment: Ground lightning decal at travel position
```

---

## Canvas Particle System (SwiftUI-Only, No Dependencies)

For small particle counts (<200) when you want zero external dependencies.

```swift
struct CanvasParticleSystem: View {
    @State private var particles: [SimpleParticle] = []
    let maxParticles = 150

    struct SimpleParticle {
        var x, y: CGFloat
        var vx, vy: CGFloat
        var age: CGFloat
        var lifetime: CGFloat
        var size: CGFloat
        var color: Color
        var alive: Bool
    }

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 60.0)) { ctx in
            Canvas { context, canvasSize in
                let dt: CGFloat = 1.0 / 60.0

                for i in particles.indices where particles[i].alive {
                    var p = particles[i]
                    p.age += dt
                    if p.age >= p.lifetime {
                        p.alive = false
                        particles[i] = p
                        continue
                    }

                    // Simple gravity
                    p.vy += 50 * dt

                    p.x += p.vx * dt
                    p.y += p.vy * dt

                    let lifeRatio = p.age / p.lifetime
                    let alpha = 1.0 - lifeRatio
                    let currentSize = p.size * (1.0 - lifeRatio * 0.5)

                    context.opacity = alpha
                    context.fill(
                        Circle().path(in: CGRect(
                            x: p.x - currentSize / 2,
                            y: p.y - currentSize / 2,
                            width: currentSize,
                            height: currentSize
                        )),
                        with: .color(p.color)
                    )

                    particles[i] = p
                }
            }
        }
        .onAppear { preallocate() }
    }

    private func preallocate() {
        particles = (0..<maxParticles).map { _ in
            SimpleParticle(x: 0, y: 0, vx: 0, vy: 0, age: 0, lifetime: 1, size: 4, color: .white, alive: false)
        }
    }

    func emit(at position: CGPoint, count: Int, color: Color = .orange) {
        var emitted = 0
        for i in particles.indices where !particles[i].alive && emitted < count {
            particles[i] = SimpleParticle(
                x: position.x, y: position.y,
                vx: CGFloat.random(in: -100...100),
                vy: CGFloat.random(in: -200...(-50)),
                age: 0,
                lifetime: CGFloat.random(in: 0.5...1.5),
                size: CGFloat.random(in: 3...8),
                color: color,
                alive: true
            )
            emitted += 1
        }
    }
}
```

**Limitations:** CPU-bound update loop. Fine for <200 particles, starts dropping frames around 300+ on older phones.

---

## Performance Guidelines

| Particle Count | Recommended API | CPU Time | GPU Time |
|---------------|-----------------|----------|----------|
| 1-100 | Canvas | <1ms | <0.5ms |
| 100-500 | Vortex / SpriteKit | 1-3ms | 0.5-2ms |
| 500-2000 | Metal Compute | <0.5ms | 1-3ms |
| 2000-10000 | Metal Compute + Instanced | <0.5ms | 2-5ms |

**Rules of thumb:**
- If you see >4ms CPU in the particle update loop, move to GPU compute
- Texture atlas for particle sprites (one draw call for all particle types)
- Sort back-to-front only for alpha-blended particles; skip sort for additive
- Reduce particle birth rate before reducing count -- fewer, longer-lived particles look better than many short-lived ones
