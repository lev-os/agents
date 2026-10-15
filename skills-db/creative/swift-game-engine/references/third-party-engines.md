# Third-Party Swift Game Engines & Libraries

## Vortex (twostraws)

**What:** SwiftUI-native particle system. Drop-in particle effects with zero Metal knowledge required.

**Best for:** UI particle effects in SwiftUI apps. Confetti, fire, rain, magic sparkles, ambient particles.

**Limitation:** 2D only. Limited to pre-defined emitter model. Not suitable for complex simulations or custom GPU pipelines.

**SPM:** `github.com/twostraws/Vortex`

**Minimum:** iOS 15+ / macOS 12+

**Status:** Actively maintained by Paul Hudson.

### 8 Built-in Presets

| Preset | Effect | Use Case |
|--------|--------|----------|
| `.confetti` | Colorful falling rectangles | Celebrations, achievements |
| `.fire` | Upward orange/red particles | Torches, campfires, UI accents |
| `.fireflies` | Drifting glow dots | Ambient, magical atmosphere |
| `.fireworks` | Burst with trails | Celebrations, game rewards |
| `.magic` | Swirling sparkles | Spell effects, loading states |
| `.rain` | Falling streaks | Weather, mood |
| `.smoke` | Rising gray clouds | Atmosphere, damage indicators |
| `.snow` | Drifting white dots | Weather, winter themes |

### Basic Usage

```swift
import Vortex

// Use a preset
VortexView(.fire) {
    Circle()
        .fill(.orange)
        .frame(width: 16, height: 16)
        .blur(radius: 3)
        .tag("circle")
}

// Custom configuration
VortexView(VortexSystem(
    tags: ["spark"],
    birthRate: 100,
    lifespan: 1.5,
    speed: 200,
    speedVariation: 50,
    angle: .degrees(-90),
    angleRange: .degrees(30),
    size: 0.3,
    sizeVariation: 0.1,
    colors: [.init(.orange), .init(.red), .init(.clear)]
)) {
    Circle()
        .fill(.white)
        .frame(width: 8, height: 8)
        .tag("spark")
}
```

### VortexViewReader (Programmatic Control)

```swift
VortexViewReader { proxy in
    VortexView(.fireworks) {
        Circle().fill(.white).frame(width: 12, height: 12).tag("circle")
    }
    .onTapGesture { location in
        proxy.move(to: location)
        proxy.burst()
    }
}
```

### VortexSystem Configuration Properties

| Property | Type | Description |
|----------|------|-------------|
| `tags` | `[String]` | Which tagged child views to use as particles |
| `birthRate` | `Double` | Particles emitted per second |
| `lifespan` | `Double` | Seconds each particle lives |
| `speed` | `Double` | Initial speed (points/sec) |
| `speedVariation` | `Double` | Random speed offset |
| `angle` | `Angle` | Emission direction |
| `angleRange` | `Angle` | Spread around emission angle |
| `size` | `Double` | Scale factor |
| `sizeVariation` | `Double` | Random size offset |
| `sizeMultiplierAtDeath` | `Double` | Scale factor at end of life |
| `colors` | `[Vortex.Color]` | Color over lifetime (gradient) |
| `position` | `CGPoint` | Emitter position (0-1 normalized) |
| `shape` | `VortexSystem.Shape` | Emission shape (.point, .ring, .box, .ellipse) |
| `attractionCenter` | `CGPoint?` | Point particles are attracted to |
| `attractionStrength` | `Double` | Force toward attraction center |
| `dampingFactor` | `Double` | Velocity damping per frame |

### Secondary Systems (Multi-Stage Effects)

```swift
// Firework: primary burst spawns secondary sparkle trails
let sparkle = VortexSystem(
    tags: ["sparkle"],
    birthRate: 5,
    lifespan: 0.5,
    speed: 20,
    colors: [.init(.yellow), .init(.clear)]
)

let firework = VortexSystem(
    tags: ["circle"],
    secondarySystems: [sparkle],
    birthRate: 0,  // burst-only
    lifespan: 2.0,
    speed: 300,
    angleRange: .degrees(360),
    colors: [.init(.white), .init(.red)]
)
```

---

## Inferno (twostraws)

**What:** Collection of Metal fragment shaders designed for SwiftUI. Uses `.colorEffect()`, `.layerEffect()`, and `.distortionEffect()` modifiers.

**Best for:** GPU visual effects on SwiftUI views without writing Metal code. Emboss, wave, gradient fills, infrared, etc.

**Limitation:** Fragment shaders only (no compute, no vertex). iOS 17+ required for SwiftUI shader modifiers.

**SPM:** `github.com/twostraws/Inferno`

**Minimum:** iOS 17+ / macOS 14+

**Status:** Actively maintained by Paul Hudson.

### Available Effects

| Effect | Type | Description |
|--------|------|-------------|
| Animated Gradient Fill | colorEffect | Smoothly animated multi-color gradient |
| Checkerboard | colorEffect | Animated checkerboard pattern overlay |
| Circle Wave | distortionEffect | Ripple rings emanating from a point |
| Color Planes | colorEffect | RGB channel separation |
| Emboss | colorEffect | Raised/stamped appearance |
| Infrared | colorEffect | Heat-vision false-color mapping |
| Interlace | colorEffect | Scanline/CRT effect |
| Pixellate | layerEffect | Mosaic pixelation |
| Rainbow Noise | colorEffect | Animated chromatic noise |
| Sinebow | colorEffect | HSL rainbow color cycling |
| Water | distortionEffect | Liquid surface distortion |

### Usage Pattern

```swift
import Inferno

struct EffectDemo: View {
    @State private var time: Float = 0
    let timer = Timer.publish(every: 1/60, on: .main, in: .common).autoconnect()

    var body: some View {
        Image("landscape")
            .resizable()
            .aspectRatio(contentMode: .fill)
            // Apply as color effect (per-pixel color transform)
            .colorEffect(ShaderLibrary.infrared(.float(time)))
            // Or as distortion (per-pixel position offset)
            // .distortionEffect(ShaderLibrary.circleWave(.float(time), .float2(center)), maxSampleOffset: .init(width: 100, height: 100))
            .onReceive(timer) { _ in time += 1/60 }
    }
}
```

### Creating Custom Inferno-Style Shaders

```metal
// MyShaders.metal
#include <metal_stdlib>
#include <SwiftUI/SwiftUI_Metal.h>
using namespace metal;

// colorEffect: transforms color per pixel
[[stitchable]] half4 myGlow(float2 position, half4 color, float time) {
    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    return color * half4(1.0 + pulse * 0.5, 1.0, 1.0 + pulse * 0.3, 1.0);
}

// distortionEffect: offsets sample position
[[stitchable]] float2 myWave(float2 position, float time, float amplitude) {
    float2 offset;
    offset.x = sin(position.y * 0.05 + time * 2.0) * amplitude;
    offset.y = cos(position.x * 0.05 + time * 2.0) * amplitude * 0.5;
    return position + offset;
}

// layerEffect: reads from layer at offset positions
[[stitchable]] half4 myBlur(float2 position, SwiftUI::Layer layer, float radius) {
    half4 total = half4(0);
    int samples = 0;
    for (float x = -radius; x <= radius; x += 1.0) {
        for (float y = -radius; y <= radius; y += 1.0) {
            total += layer.sample(position + float2(x, y));
            samples++;
        }
    }
    return total / half4(samples);
}
```

---

## SwiftUI-Particles (benlmyers)

**What:** Declarative particle system built on SwiftUI Canvas. No Metal or SpriteKit dependency.

**Best for:** Simple particle effects that need to stay entirely within the SwiftUI view hierarchy without bridging to other frameworks.

**Limitation:** CPU-bound (Canvas rendering). Performance ceiling is lower than GPU-based systems. Limited particle count.

**SPM:** `github.com/benlmyers/swiftui-particles`

**Status:** Community maintained.

### Usage

```swift
import Particles

ParticleSystem {
    Emitter(every: 0.02) {
        Particle {
            Circle().fill(.orange).frame(width: 8, height: 8)
        }
        .initialVelocity(x: { .random(in: -50...50) }, y: { .random(in: -200 ... -100) })
        .lifetime(1.5)
        .opacity(over: .lifetime) { t in 1.0 - t }
        .scale(over: .lifetime) { t in 0.5 + t * 0.5 }
    }
}
.frame(width: 200, height: 300)
```

---

## GateEngine

**What:** Cross-platform Swift game engine supporting macOS, Windows, Linux, iOS, Android, and Web (via WASM). Full 2D/3D rendering, audio, input, physics.

**Best for:** Cross-platform Swift games that need to run beyond Apple ecosystems.

**Limitation:** Smaller community. Less polished than Unity/Unreal. Documentation is evolving.

**SPM:** `github.com/STREGAsGate/GateEngine`

**Status:** Actively maintained. Growing ecosystem.

### Platform Support

| Platform | Rendering | Audio | Input |
|----------|-----------|-------|-------|
| macOS | Metal | CoreAudio | Keyboard/Mouse/Gamepad |
| iOS | Metal | CoreAudio | Touch/Gamepad |
| Windows | DirectX 12 | XAudio2 | Keyboard/Mouse/Gamepad |
| Linux | Vulkan | OpenAL | Keyboard/Mouse/Gamepad |
| Android | Vulkan | OpenSL | Touch/Gamepad |
| Web | WebGPU/WebGL | WebAudio | Keyboard/Mouse/Touch |

### Architecture

GateEngine uses an ECS-inspired architecture:

```swift
import GateEngine

@main
struct MyGame: Game {
    static let title = "My Game"

    func didFinishLaunching(game: Game, options: LaunchOptions) {
        game.insertSystem(RenderingSystem.self)
        game.insertSystem(PhysicsSystem.self)
        game.insertSystem(PlayerControlSystem.self)
    }
}

class PlayerControlSystem: System {
    override func update(game: Game, input: HID, withTimePassed deltaTime: Float) {
        // Process input, update entities
    }
}
```

---

## Untold Engine

**What:** 3D Swift game engine with custom Metal renderer, ECS, and physics. Pure Swift implementation.

**Best for:** 3D games in pure Swift without Objective-C bridging. Learning Metal rendering pipeline through a real engine.

**Limitation:** Smaller community than commercial engines. macOS/iOS only.

**SPM:** `github.com/untoldengine/UntoldEngine`

**Status:** Actively maintained. Educational focus.

### Features

- Custom Metal renderer (forward + deferred paths)
- Entity-Component-System architecture
- Rigid body physics
- Skeletal animation
- Scene graph with spatial partitioning
- Shadow mapping
- PBR materials

### Basic Usage

```swift
import UntoldEngine

class GameScene: Scene {
    override func sceneDidLoad() {
        let entity = createEntity()
        entity.addComponent(RenderComponent(meshName: "character"))
        entity.addComponent(TransformComponent(position: float3(0, 0, 0)))
        entity.addComponent(PhysicsComponent(mass: 1.0))
    }

    override func update(deltaTime: Float) {
        // Game logic
    }
}
```

---

## SwiftVVD

**What:** 3D cross-platform engine using Vulkan on non-Apple platforms and Metal on Apple platforms. Advanced rendering features.

**Best for:** Projects that need both Vulkan and Metal backends. Advanced 3D rendering requiring low-level API access.

**Limitation:** High complexity. Small community. Requires understanding of both Vulkan and Metal concepts.

**Status:** Niche, specialized use cases.

### Key Features

- Dual-backend: Vulkan + Metal
- Custom render graph
- PBR pipeline
- Shadow mapping (cascaded, point, spot)
- Post-processing framework
- GPU particle system

---

## Fireblade ECS

**What:** Standalone Entity-Component-System framework for Swift. No rendering -- pure architecture pattern.

**Best for:** Building custom game engines that need proper ECS without RealityKit's overhead or opinions.

**SPM:** `github.com/fireblade-engine/ecs`

**Status:** Actively maintained. Focused and lean.

### Core API

```swift
import FirebladeECS

// Create world (nexus)
let nexus = Nexus()

// Create entity with components
let entity = nexus.createEntity()
entity.assign(Position(x: 0, y: 0))
entity.assign(Velocity(dx: 1, dy: 0))
entity.assign(Sprite(texture: "hero"))

// Define components
struct Position: Component {
    var x: Float
    var y: Float
}

struct Velocity: Component {
    var dx: Float
    var dy: Float
}

struct Sprite: Component {
    var texture: String
}

// Query entities with specific components
let movers = nexus.family(requiresAll: Position.self, Velocity.self)

// System: iterate matching entities
func movementSystem(deltaTime: Float) {
    movers.forEach { (position: inout Position, velocity: Velocity) in
        position.x += velocity.dx * deltaTime
        position.y += velocity.dy * deltaTime
    }
}
```

### Why Standalone ECS?

| Approach | When to Use |
|----------|-------------|
| RealityKit ECS | 3D/AR apps on Apple platforms, need rendering + physics out of the box |
| Fireblade ECS | Custom renderer (Metal direct), need ECS without RealityKit opinions |
| GameplayKit Entities | Simple cases, already using SpriteKit |
| Roll your own | Educational, very specialized needs |

Fireblade ECS is ~2000 lines. Lean, fast, well-tested. Pair with Metal for a custom engine stack.

---

## OctopusKit (Archived)

**What:** ECS game framework built on SpriteKit + SwiftUI. Provided components, systems, and state management.

**Best for:** Was good for 2D games with SwiftUI integration.

**Status:** ARCHIVED. Unmaintained. Do NOT use for new projects.

**Note:** Included for historical reference. If you find OctopusKit code in a codebase, recommend migration to SpriteKit + Fireblade ECS or Vortex.

---

## Comparison: Which Third-Party Engine?

```
Need particles in SwiftUI?
|-- Zero config presets? -> Vortex (8 presets, burst control)
|-- GPU shader effects on existing views? -> Inferno (Metal fragment shaders)
|-- CPU-only, pure Canvas? -> SwiftUI-Particles
|
Need a full game engine?
|-- Apple only, 3D? -> Untold Engine (pure Swift, Metal renderer)
|-- Cross-platform? -> GateEngine (6 platforms)
|-- Cross-API (Vulkan + Metal)? -> SwiftVVD
|
Need ECS architecture?
|-- With rendering? -> RealityKit (built-in) or GateEngine
|-- Standalone, pair with Metal? -> Fireblade ECS
|
Just need logic?
|-- GameplayKit (state machines, pathfinding, AI, noise)
```
