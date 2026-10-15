# Apple Native Frameworks Deep Dive

## SpriteKit

**What:** Apple's 2D game framework. Scene graph with sprite nodes, physics, particles, shaders, and actions.

**Best for:** 2D games, UI particle overlays, animated backgrounds, 2D physics simulations.

**Limitation:** 2D only, no custom render pipeline, fixed-function particle system.

**SwiftUI Integration:** `SpriteView(scene:)`

**Status:** Actively maintained. Stable API, infrequent additions.

**Minimum:** iOS 7+, macOS 10.9+

### Core Components

| Component | Class | Purpose |
|-----------|-------|---------|
| Scene | `SKScene` | Root container, coordinate system, update loop |
| Sprites | `SKSpriteNode` | Textured rectangles, atlases, animation |
| Particles | `SKEmitterNode` | GPU-accelerated particle system (fire, smoke, sparks) |
| Shaders | `SKShader` | GLSL-like fragment shaders on any node |
| Physics | `SKPhysicsWorld` / `SKPhysicsBody` | 2D rigid body physics, collision detection |
| Fields | `SKFieldNode` | Physics fields (gravity, turbulence, vortex, drag) |
| Actions | `SKAction` | Declarative animation sequences (move, rotate, fade, group, sequence, repeat) |
| Paths | `SKShapeNode` | UIBezierPath / CGPath rendering |
| Tiles | `SKTileMapNode` | Tile-based level rendering |
| Camera | `SKCameraNode` | Viewport control, zoom, follow |

### SKEmitterNode Particle System

Pre-built in Xcode particle editor (.sks file) or configured in code:

```swift
let emitter = SKEmitterNode()
emitter.particleTexture = SKTexture(imageNamed: "spark")
emitter.particleBirthRate = 200
emitter.particleLifetime = 1.5
emitter.particleSpeed = 100
emitter.particleSpeedRange = 50
emitter.emissionAngleRange = .pi * 2
emitter.particleScale = 0.3
emitter.particleScaleRange = 0.2
emitter.particleAlpha = 0.8
emitter.particleAlphaSpeed = -0.5  // fade out
emitter.particleColorBlendFactor = 1.0
emitter.particleColor = .orange
emitter.particleColorSequence = nil  // or use SKKeyframeSequence for color over lifetime
emitter.particleBlendMode = .add    // additive for glow
```

### SKShader (Custom Fragment Shaders)

GLSL-like syntax, runs per-pixel on any SKNode:

```swift
let shader = SKShader(source: """
    void main() {
        vec2 uv = v_tex_coord;
        float dist = distance(uv, vec2(0.5, 0.5));
        float glow = 0.1 / dist;
        gl_FragColor = vec4(glow * vec3(0.3, 0.6, 1.0), 1.0) * v_color_mix;
    }
""")
shader.uniforms = [SKUniform(name: "u_time", float: 0.0)]
spriteNode.shader = shader
```

Update uniforms per frame in `update(_:)` for animation.

### SKFieldNode Physics Fields

```swift
// Vortex field (swirling particles)
let vortex = SKFieldNode.vortexField()
vortex.strength = 0.5
vortex.region = SKRegion(radius: 200)
scene.addChild(vortex)

// Turbulence (organic motion)
let turbulence = SKFieldNode.turbulenceField(withSmoothness: 0.5, animationSpeed: 1.0)
turbulence.strength = 2.0
scene.addChild(turbulence)

// Radial gravity (attract/repel)
let gravity = SKFieldNode.radialGravityField()
gravity.strength = -3.0  // negative = repel
scene.addChild(gravity)
```

### SwiftUI Integration

```swift
struct GameContainerView: View {
    @State private var isPaused = false

    var body: some View {
        SpriteView(scene: GameScene(), isPaused: isPaused)
            .ignoresSafeArea()
            .overlay(alignment: .topTrailing) {
                Button(isPaused ? "Resume" : "Pause") { isPaused.toggle() }
                    .padding()
            }
    }
}
```

---

## SceneKit

**What:** Apple's 3D scene graph framework. PBR materials, physics, particles, shader modifiers, post-processing.

**Best for:** 3D prototyping, mid-complexity scenes, quick 3D visualization.

**Limitation:** DEPRECATED at WWDC 2025. Critical-bug-only maintenance. No new features.

**SwiftUI Integration:** `SceneView(scene:options:)`

**Status:** DEPRECATED. Do NOT start new projects with SceneKit.

**Migration Path:** RealityKit. Apple provides migration guides.

### Why It Was Good (Historical Reference)

| Feature | API | Notes |
|---------|-----|-------|
| Scene Graph | `SCNScene` / `SCNNode` | Hierarchical transform tree |
| PBR Materials | `SCNMaterial` | Physically-based: albedo, metalness, roughness, normal, AO |
| Particles | `SCNParticleSystem` | 3D particles, gravity, collision, sub-emitters |
| Post-Processing | `SCNTechnique` | Multi-pass render pipeline definition (JSON-based) |
| Shader Modifiers | `.geometry` / `.surface` / `.fragment` / `.lighting` | Inject GLSL snippets at pipeline stages |
| Physics | `SCNPhysicsBody` / `SCNPhysicsWorld` | Bullet-based rigid body, vehicle, soft body |
| Animation | `SCNAction` / `CAAnimation` | Keyframe, skeletal, procedural |

### SCNTechnique Post-Processing (Legacy Pattern)

```swift
// Define multi-pass pipeline in JSON
let technique = SCNTechnique(dictionary: [
    "passes": [
        "bloom_threshold": [
            "draw": "DRAW_QUAD",
            "program": "bloom_threshold",
            "inputs": ["colorSampler": "COLOR"],
            "outputs": ["color": "threshold_output"]
        ],
        "bloom_blur": [
            "draw": "DRAW_QUAD",
            "program": "gaussian_blur",
            "inputs": ["colorSampler": "threshold_output"],
            "outputs": ["color": "COLOR"]
        ]
    ],
    "sequence": ["bloom_threshold", "bloom_blur"]
])
sceneView.technique = technique
```

### Migration: SceneKit to RealityKit

| SceneKit | RealityKit Equivalent |
|----------|----------------------|
| `SCNScene` | `Entity` hierarchy in `RealityView` |
| `SCNNode` | `Entity` |
| `SCNGeometry` | `MeshResource` |
| `SCNMaterial` | `PhysicallyBasedMaterial` / `CustomMaterial` |
| `SCNParticleSystem` | `ParticleEmitterComponent` (visionOS) |
| `SCNPhysicsBody` | `PhysicsBodyComponent` |
| `SCNAction` | `Transform` animation via `move(to:)` |
| `SCNTechnique` | `CustomMaterial` + Metal shaders |

---

## RealityKit

**What:** Apple's primary 3D framework. Entity-Component-System architecture, PBR rendering, physics (PhysX), spatial audio, AR integration.

**Best for:** AR, visionOS, spatial computing, 3D games on Apple platforms, any new 3D project.

**Limitation:** Less flexible than raw Metal for custom render pipelines. ECS has a learning curve. Some features visionOS-only.

**SwiftUI Integration:** `RealityView { content in ... }`

**Status:** Actively maintained. Apple's strategic investment for 3D. Major updates every WWDC.

**Minimum:** iOS 13+ (basic), iOS 17+/macOS 14+ (RealityView), visionOS 1.0+

### Core ECS Architecture

```
Entity (ID + list of Components)
  ├── TransformComponent (position, rotation, scale)
  ├── ModelComponent (mesh + materials)
  ├── PhysicsBodyComponent (dynamic, static, kinematic)
  ├── CollisionComponent (shapes for hit testing)
  ├── ParticleEmitterComponent (visionOS)
  └── Custom components (conform to Component protocol)
```

### Key APIs

| Feature | API | Notes |
|---------|-----|-------|
| Entities | `Entity` / `ModelEntity` | Core building block |
| Meshes | `MeshResource` | .generateBox, .generateSphere, .generate(from: [MeshDescriptor]) |
| Materials | `PhysicallyBasedMaterial` | PBR: baseColor, roughness, metallic, normal, emissive |
| Custom Shaders | `CustomMaterial` | Surface shader + geometry modifier (Metal) |
| Physics | `PhysicsBodyComponent` | PhysX: dynamic, static, kinematic bodies |
| Collision | `CollisionComponent` | Shape-based: box, sphere, capsule, mesh |
| Spatial Audio | `SpatialAudioComponent` | 3D positioned audio sources |
| Anchoring | `AnchoringComponent` | AR plane/image/face/body anchors |

### CustomMaterial (Metal Shaders in RealityKit)

```swift
var material = CustomMaterial(
    from: PhysicallyBasedMaterial(),
    surfaceShader: CustomMaterial.SurfaceShader(
        named: "mySurfaceShader",
        in: MetalLibrary.default
    )
)

// In .metal file:
#include <RealityKit/RealityKit.h>

[[visible]]
void mySurfaceShader(realitykit::surface_parameters params) {
    auto surface = params.surface();
    float time = params.uniforms().time();

    float3 baseColor = float3(0.3, 0.6, 1.0);
    float pulse = sin(time * 2.0) * 0.5 + 0.5;
    surface.set_base_color(half3(baseColor * pulse));
    surface.set_roughness(half(0.2));
    surface.set_metallic(half(0.8));
}
```

### RealityView SwiftUI Integration

```swift
struct My3DScene: View {
    @State private var selectedEntity: Entity?

    var body: some View {
        RealityView { content in
            // Initial setup (runs once)
            let floor = ModelEntity(
                mesh: .generatePlane(width: 5, depth: 5),
                materials: [SimpleMaterial(color: .gray, isMetallic: false)]
            )
            floor.components.set(PhysicsBodyComponent(mode: .static))
            floor.components.set(CollisionComponent(shapes: [.generateBox(width: 5, height: 0.01, depth: 5)]))
            content.add(floor)

            let sphere = ModelEntity(
                mesh: .generateSphere(radius: 0.2),
                materials: [SimpleMaterial(color: .blue, isMetallic: true)]
            )
            sphere.position = [0, 1, 0]
            sphere.components.set(PhysicsBodyComponent(mode: .dynamic))
            sphere.components.set(CollisionComponent(shapes: [.generateSphere(radius: 0.2)]))
            sphere.components.set(InputTargetComponent())
            content.add(sphere)
        } update: { content in
            // React to @State changes
        }
        .gesture(TapGesture().targetedToAnyEntity().onEnded { event in
            selectedEntity = event.entity
        })
    }
}
```

---

## Metal

**What:** Apple's low-level GPU API. Direct access to vertex/fragment/compute shaders, render passes, resource management, ray tracing, mesh shaders.

**Best for:** AAA-quality rendering, custom render pipelines, compute workloads, maximum GPU control.

**Limitation:** Highest complexity. No scene management, no physics, no built-in asset pipeline. You build everything.

**SwiftUI Integration:** `MTKView` wrapped in `UIViewRepresentable` / `NSViewRepresentable`. Also `.colorEffect()` / `.layerEffect()` / `.distortionEffect()` for shader effects on SwiftUI views (iOS 17+).

**Status:** Actively maintained. Metal 4 announced at WWDC 2025.

**Minimum:** iOS 8+ (Metal 1), iOS 16+ (Metal 3), macOS 10.11+

### Metal Pipeline Overview

```
Application (CPU)
  └── MTLCommandQueue
        └── MTLCommandBuffer
              ├── MTLRenderCommandEncoder (vertex + fragment)
              │     ├── Set render pipeline state (compiled shaders)
              │     ├── Set vertex buffers
              │     ├── Set textures
              │     └── Draw primitives / indexed
              ├── MTLComputeCommandEncoder (compute shaders)
              │     ├── Set compute pipeline state
              │     ├── Set buffers / textures
              │     └── Dispatch threadgroups
              └── MTLBlitCommandEncoder (copy resources)
```

### Key Metal APIs

| Feature | API | Metal Version |
|---------|-----|---------------|
| Device | `MTLCreateSystemDefaultDevice()` | 1 |
| Command Queue | `device.makeCommandQueue()` | 1 |
| Shaders | `device.makeLibrary()` -> `.makeFunction()` | 1 |
| Render Pipeline | `MTLRenderPipelineDescriptor` | 1 |
| Compute Pipeline | `MTLComputePipelineState` | 1 |
| Textures | `MTLTextureDescriptor` | 1 |
| Buffers | `device.makeBuffer()` | 1 |
| Render Pass | `MTLRenderPassDescriptor` | 1 |
| Indirect Rendering | `MTLIndirectCommandBuffer` | 2 |
| Mesh Shaders | Object + Mesh shader stages | 3 (M3+) |
| Ray Tracing | `MTLAccelerationStructure` | 3 |
| MetalFX | `MTLFXTemporalScaler` / `MTLFXSpatialScaler` | MetalFX |
| Inline RT | Intersection queries in any shader | 3 |

### Minimal Metal Render Pipeline

```swift
// 1. Create device and queue
let device = MTLCreateSystemDefaultDevice()!
let queue = device.makeCommandQueue()!

// 2. Load shaders
let library = device.makeDefaultLibrary()!
let vertexFn = library.makeFunction(name: "vertexShader")!
let fragmentFn = library.makeFunction(name: "fragmentShader")!

// 3. Create pipeline
let descriptor = MTLRenderPipelineDescriptor()
descriptor.vertexFunction = vertexFn
descriptor.fragmentFunction = fragmentFn
descriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
let pipelineState = try! device.makeRenderPipelineState(descriptor: descriptor)

// 4. Render loop (in MTKViewDelegate.draw(in:))
let buffer = queue.makeCommandBuffer()!
let encoder = buffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor)!
encoder.setRenderPipelineState(pipelineState)
encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
encoder.drawPrimitives(type: .triangle, vertexStart: 0, vertexCount: 3)
encoder.endEncoding()
buffer.present(drawable)
buffer.commit()
```

### Metal Shader Language (MSL) Basics

```metal
#include <metal_stdlib>
using namespace metal;

struct VertexIn {
    float4 position [[attribute(0)]];
    float2 texCoord [[attribute(1)]];
};

struct VertexOut {
    float4 position [[position]];
    float2 texCoord;
};

vertex VertexOut vertexShader(VertexIn in [[stage_in]],
                              constant float4x4 &mvp [[buffer(1)]]) {
    VertexOut out;
    out.position = mvp * in.position;
    out.texCoord = in.texCoord;
    return out;
}

fragment float4 fragmentShader(VertexOut in [[stage_in]],
                               texture2d<float> tex [[texture(0)]]) {
    constexpr sampler s(filter::linear);
    return tex.sample(s, in.texCoord);
}
```

### SwiftUI Shader Effects (iOS 17+)

```swift
// .colorEffect — per-pixel color transformation
RoundedRectangle(cornerRadius: 12)
    .fill(.blue)
    .colorEffect(ShaderLibrary.myColorShader(.float(time)))

// .layerEffect — access neighboring pixels (blur, distortion with offset)
Text("Hello")
    .layerEffect(ShaderLibrary.pixelate(.float(pixelSize)), maxSampleOffset: .init(width: 10, height: 10))

// .distortionEffect — displace pixel positions
Image("photo")
    .distortionEffect(ShaderLibrary.wave(.float(time), .float(amplitude)), maxSampleOffset: .init(width: 50, height: 50))
```

### Metal 3 Features (M3+ for full support)

- **Mesh Shaders:** Replace vertex stage with object shader (per-meshlet culling) + mesh shader (output primitives). GPU-driven rendering.
- **Ray Tracing:** Build acceleration structures (BLAS for geometry, TLAS for instances). Intersection functions for custom geometry. Used for reflections, GI, AO.
- **Offline Compilation:** Pre-compile Metal libraries to binary archives. Eliminates shader compilation stutter.

### Metal 4 (WWDC 2025)

- Unified shader compilation model
- Enhanced debugging and profiling
- Performance improvements for Apple Silicon
- Check Apple documentation for latest API additions

---

## GameplayKit

**What:** Framework-agnostic game logic toolkit. State machines, pathfinding, AI, procedural generation, random sources.

**Best for:** Game logic that pairs with ANY renderer (SpriteKit, RealityKit, Metal, or custom).

**Limitation:** Logic only. No rendering. Must pair with a rendering framework.

**SwiftUI Integration:** N/A (logic framework, renderer-independent)

**Status:** Actively maintained. Stable API.

**Minimum:** iOS 9+, macOS 10.11+

### Components

| Component | Class | Purpose |
|-----------|-------|---------|
| State Machine | `GKStateMachine` / `GKState` | Finite state machine with enter/exit/update |
| Pathfinding | `GKGraphNode` / `GKGraph` | A* pathfinding on grids, navmesh, or custom graphs |
| AI Strategy | `GKMinMaxStrategist` | Minimax with alpha-beta pruning (board games) |
| AI Behavior | `GKAgent` / `GKGoal` / `GKBehavior` | Steering behaviors (seek, flee, wander, avoid) |
| Noise | `GKNoise` / `GKNoiseSource` | Perlin, Voronoi, ridged, billow noise for procedural generation |
| Random | `GKRandomSource` | Mersenne Twister, ARC4, linear congruential, shuffled distributions |
| Entities | `GKEntity` / `GKComponent` | Basic ECS (simpler than RealityKit's) |
| Rules | `GKRuleSystem` | Rule-based AI with fuzzy logic |

### State Machine Pattern

```swift
class IdleState: GKState {
    override func isValidNextState(_ stateClass: AnyClass) -> Bool {
        stateClass == AttackingState.self || stateClass == MovingState.self
    }

    override func didEnter(from previousState: GKState?) {
        // Start idle animation
    }

    override func update(deltaTime seconds: TimeInterval) {
        // Check for state transitions
    }
}

class AttackingState: GKState {
    override func isValidNextState(_ stateClass: AnyClass) -> Bool {
        stateClass == IdleState.self
    }
}

// Usage
let stateMachine = GKStateMachine(states: [IdleState(), AttackingState(), MovingState()])
stateMachine.enter(IdleState.self)

// In game loop:
stateMachine.update(deltaTime: dt)
```

### Procedural Noise

```swift
// Perlin noise for terrain
let noiseSource = GKPerlinNoiseSource(
    frequency: 1.0,
    octaveCount: 6,
    persistence: 0.5,
    lacunarity: 2.0,
    seed: 42
)
let noise = GKNoise(noiseSource)
let noiseMap = GKNoiseMap(noise, size: [256, 256], origin: [0, 0], sampleCount: [256, 256], seamless: true)

// Sample values
let height = noiseMap.value(at: [128, 128])  // -1.0 to 1.0
```

### Agent Behaviors (Steering)

```swift
let agent = GKAgent2D()
agent.maxSpeed = 100
agent.maxAcceleration = 50

let seekGoal = GKGoal(toSeekAgent: targetAgent)
let avoidGoal = GKGoal(toAvoid: obstacles, maxPredictionTime: 1.0)
let wanderGoal = GKGoal(toWander: 10.0)

agent.behavior = GKBehavior(goals: [seekGoal, avoidGoal, wanderGoal], andWeights: [1.0, 2.0, 0.3])
```
