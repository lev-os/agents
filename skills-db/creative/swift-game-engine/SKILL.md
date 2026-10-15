---
name: swift-game-engine
description: Choose the right Swift game/VFX stack across SpriteKit, RealityKit, Metal, GameplayKit, and community engines with practical architecture and performance guidance.
triggers:
  - game engine selection
  - Swift graphics framework
  - SpriteKit vs SceneKit
  - Metal vs RealityKit
  - Apple GPU pipeline
  - ECS architecture Swift
  - render graph pattern
  - VFX pipeline design
  - MetalFX upscaling
  - console quality Apple Silicon
  - game engine comparison
  - 3D engine Swift
  - 2D game framework
  - particle system choice
  - SceneKit deprecated
---

# Swift Game Engine Selection & VFX Architecture

## Decision Tree

```
What are you building?
|
|-- 2D Game / 2D Effects?
|   |-- Simple sprites + physics? -> SpriteKit (built-in, battle-tested)
|   |-- UI particle overlays in SwiftUI? -> Vortex (zero Metal knowledge)
|   |-- GPU shader effects on SwiftUI views? -> Inferno (Metal fragments)
|   |-- Declarative particles (no Metal)? -> SwiftUI-Particles (Canvas-based)
|   |-- Cross-platform 2D? -> GateEngine (macOS/Win/Linux/iOS/Android/Web)
|   -> See: references/apple-frameworks.md#spritekit
|
|-- 3D Game / 3D Scene?
|   |-- AR / visionOS / spatial? -> RealityKit (Apple's primary 3D)
|   |-- Quick 3D prototype (non-AR)? -> RealityKit (SceneKit is deprecated)
|   |-- Pure Swift 3D engine? -> Untold Engine (custom Metal renderer)
|   |-- Cross-platform 3D? -> GateEngine or SwiftVVD
|   |-- AAA-quality custom pipeline? -> Metal direct (maximum control)
|   -> See: references/apple-frameworks.md#realitykit
|
|-- VFX / Post-Processing Pipeline?
|   |-- SwiftUI shader effects? -> .colorEffect / .layerEffect / .distortionEffect (iOS 17+)
|   |-- Full post-process stack? -> Metal render passes (effect compositor)
|   |-- Console-quality techniques? -> references/ps5-techniques.md
|   |-- Bloom / glow / TAA / SSR? -> Metal compute + render passes
|   -> See: references/architecture-patterns.md#effect-stack
|
|-- Game Logic / AI (renderer-agnostic)?
|   |-- State machines? -> GameplayKit GKStateMachine
|   |-- Pathfinding / nav mesh? -> GameplayKit GKGraphNode
|   |-- AI opponents? -> GameplayKit GKMinMaxStrategist
|   |-- Procedural noise? -> GameplayKit GKNoise
|   |-- ECS architecture? -> RealityKit (native) or Fireblade ECS (standalone)
|   -> See: references/apple-frameworks.md#gameplaykit
|
|-- Custom Render Engine?
|   |-- From scratch, maximum GPU control? -> Metal direct
|   |-- Need ECS but not RealityKit? -> Fireblade ECS + Metal
|   |-- Cross-API (Vulkan + Metal)? -> SwiftVVD
|   |-- Render graph architecture? -> references/architecture-patterns.md
|   -> See: references/apple-frameworks.md#metal
|
\-- Unsure / Need Comparison?
    -> See: Comparison Matrix below
```

## Comparison Matrix

| Framework | VFX Cap | SwiftUI | 3D | Perf Ceiling | Learning | Status |
|-----------|---------|---------|----|----|----------|--------|
| **SpriteKit** | Mid | SpriteView | No | Mid | Low | Active |
| **SceneKit** | Mid-High | SceneView | Yes | Mid | Mid | **Deprecated** (WWDC25) |
| **RealityKit** | High | RealityView | Yes | High | Mid-High | Active (primary) |
| **Metal** | Maximum | MTKView/UIViewRep | Yes | Maximum | High | Active (Metal 4) |
| **GameplayKit** | N/A (logic) | N/A | N/A | N/A | Low | Active |
| **Vortex** | Low-Mid | Native | No | Low | Very Low | Active |
| **Inferno** | Mid | Native | No | Mid | Low | Active |
| **SwiftUI-Particles** | Low | Native | No | Low | Very Low | Community |
| **GateEngine** | Mid | No | Yes | Mid | Mid | Active |
| **Untold Engine** | Mid-High | No | Yes | Mid-High | Mid-High | Active |
| **SwiftVVD** | High | No | Yes | High | High | Niche |
| **Fireblade ECS** | N/A (arch) | N/A | N/A | N/A | Mid | Active |

**Rating key:** VFX Cap = range of visual effects achievable. Perf Ceiling = maximum rendering throughput. Learning = time to first meaningful output. Status as of 2025.

**SceneKit warning:** Deprecated at WWDC 2025. Critical-bug-only maintenance. Do NOT start new projects with SceneKit. Migrate existing projects to RealityKit.

## Quick-Start Patterns

### SpriteKit (2D Game)

```swift
import SpriteKit
import SwiftUI

struct GameView: View {
    var body: some View {
        SpriteView(scene: makeScene())
            .ignoresSafeArea()
    }

    func makeScene() -> SKScene {
        let scene = GameScene(size: CGSize(width: 390, height: 844))
        scene.scaleMode = .aspectFill
        return scene
    }
}

class GameScene: SKScene {
    override func didMove(to view: SKView) {
        // Particle emitter
        if let emitter = SKEmitterNode(fileNamed: "Fire") {
            emitter.position = CGPoint(x: size.width / 2, y: size.height / 2)
            addChild(emitter)
        }
    }
}
```

### RealityKit (3D / AR)

```swift
import RealityKit
import SwiftUI

struct Scene3DView: View {
    var body: some View {
        RealityView { content in
            let sphere = MeshResource.generateSphere(radius: 0.1)
            var material = PhysicallyBasedMaterial()
            material.baseColor = .init(tint: .blue)
            material.roughness = .init(floatLiteral: 0.2)
            material.metallic = .init(floatLiteral: 0.8)
            let entity = ModelEntity(mesh: sphere, materials: [material])
            content.add(entity)
        }
    }
}
```

### Metal (Custom Pipeline)

```swift
import MetalKit
import SwiftUI

struct MetalView: UIViewRepresentable {
    func makeUIView(context: Context) -> MTKView {
        let view = MTKView()
        view.device = MTLCreateSystemDefaultDevice()
        view.delegate = context.coordinator
        view.preferredFramesPerSecond = 60
        view.colorPixelFormat = .bgra8Unorm
        return view
    }

    func updateUIView(_ uiView: MTKView, context: Context) {}

    func makeCoordinator() -> Renderer { Renderer() }

    class Renderer: NSObject, MTKViewDelegate {
        var device: MTLDevice!
        var commandQueue: MTLCommandQueue!
        var pipelineState: MTLRenderPipelineState!

        override init() {
            super.init()
            device = MTLCreateSystemDefaultDevice()!
            commandQueue = device.makeCommandQueue()!
            // Build pipeline from .metal shader file
        }

        func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {}

        func draw(in view: MTKView) {
            guard let drawable = view.currentDrawable,
                  let descriptor = view.currentRenderPassDescriptor,
                  let buffer = commandQueue.makeCommandBuffer(),
                  let encoder = buffer.makeRenderCommandEncoder(descriptor: descriptor) else { return }
            encoder.setRenderPipelineState(pipelineState)
            // Draw calls here
            encoder.endEncoding()
            buffer.present(drawable)
            buffer.commit()
        }
    }
}
```

### Vortex (SwiftUI Particles)

```swift
import Vortex
import SwiftUI

struct FireView: View {
    var body: some View {
        VortexView(.fire) {
            Circle()
                .fill(.orange)
                .frame(width: 16, height: 16)
                .blur(radius: 3)
                .tag("circle")
        }
        .frame(width: 200, height: 300)
    }
}
```

### Inferno (Metal Shader on SwiftUI View)

```swift
import Inferno
import SwiftUI

struct GlowingCard: View {
    @State private var time: Float = 0
    let timer = Timer.publish(every: 1/60, on: .main, in: .common).autoconnect()

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.blue)
            .frame(width: 200, height: 120)
            .colorEffect(ShaderLibrary.emboss(.float(time)))
            .onReceive(timer) { _ in time += 1/60 }
    }
}
```

## Architecture Patterns (Summary)

| Pattern | Use Case | Key Idea | Reference |
|---------|----------|----------|-----------|
| **ECS** | Games, simulations | Entities = IDs, Components = data, Systems = logic | `references/architecture-patterns.md#ecs` |
| **Render Graph** | Custom Metal pipelines | DAG of render passes, auto resource management | `references/architecture-patterns.md#render-graph` |
| **Effect Stack** | Post-processing | Ordered list: bloom -> color grade -> vignette -> FXAA | `references/architecture-patterns.md#effect-stack` |
| **VFX Manager** | Spawning effects | Centralized pool + spawn API | `references/architecture-patterns.md#vfx-manager` |
| **Audio-Visual Sync** | Reactive effects | FFT/RMS -> parameter bridge -> VFX intensity | `references/architecture-patterns.md#audio-visual-sync` |
| **State-Driven** | Spell lifecycles | enum state machine drives VFX transitions | `references/architecture-patterns.md#state-driven-effects` |
| **Composition** | Complex effects | SpellEffect = [Particle + Shader + Audio + Shake] | `references/architecture-patterns.md#composition` |

## Console-Quality on Apple Silicon (Summary)

| Technique | M1 | M2 | M3/M4 | PS5 Equivalent |
|-----------|----|----|-------|----------------|
| TAA | Yes | Yes | Yes | Yes |
| MetalFX Upscaling | Yes | Yes | Yes | PSSR/DLSS/FSR |
| Screen-Space Reflections | Yes | Yes | Yes | Yes |
| Mesh Shaders | No | Partial | Yes | Yes |
| Variable Rate Shading | No | No | Yes | Yes |
| Ray Tracing | Basic | Better | Full | Yes |

**Feasibility:** M1 = 60-80% PS5 quality. M2 = 70-85%. M3/M4 = 80-90%. Key bottleneck: memory bandwidth.

See `references/ps5-techniques.md` for implementation details.

## Framework Selection Cheat Sheet

```
Need SwiftUI integration?
|-- Yes + 2D particles? -> Vortex
|-- Yes + shader effects? -> Inferno or .colorEffect/.layerEffect
|-- Yes + 3D scene? -> RealityView (RealityKit)
|-- Yes + 2D game? -> SpriteView (SpriteKit)
|-- Yes + custom GPU? -> MTKView in UIViewRepresentable
\-- No? -> Metal direct, GateEngine, or Untold Engine

Need cross-platform?
|-- Apple only? -> SpriteKit / RealityKit / Metal
|-- Apple + Windows + Linux? -> GateEngine
|-- Apple + Vulkan platforms? -> SwiftVVD
\-- Apple + Web? -> GateEngine

Need ECS?
|-- Built into renderer? -> RealityKit
|-- Standalone (any renderer)? -> Fireblade ECS
\-- With SpriteKit? -> OctopusKit (archived, use cautiously)
```

## References

| File | Content |
|------|---------|
| `references/apple-frameworks.md` | Deep dive on SpriteKit, SceneKit, RealityKit, Metal, GameplayKit |
| `references/third-party-engines.md` | Vortex, Inferno, GateEngine, Untold, SwiftVVD, Fireblade ECS, OctopusKit |
| `references/ps5-techniques.md` | TAA, MetalFX, SSR, mesh shaders, VRS, ray tracing, feasibility matrix |
| `references/architecture-patterns.md` | ECS, render graph, effect stack, VFX manager, audio-visual sync, state-driven, composition |

## Related Skills

- **vfx-spell-effects** -- Specific VFX implementations (smoke, lightning, particles, bloom, spell composition)
- **metal-shaders** -- Shader authoring for any engine (MSL, vertex/fragment/compute)
- **orb** -- Practical multi-layer VFX composition in SwiftUI (OCMiniOrb)
- **swiftui-animation** -- Animation integration with engine rendering

## External Resources

- [Apple Metal](https://developer.apple.com/metal/)
- [Apple SpriteKit](https://developer.apple.com/documentation/spritekit/)
- [Apple SceneKit](https://developer.apple.com/documentation/scenekit/)
- [Apple RealityKit](https://developer.apple.com/documentation/realitykit/)
- [Apple MetalFX](https://developer.apple.com/documentation/metalfx)
- [Vortex](https://github.com/twostraws/Vortex) -- SwiftUI particles
- [Inferno](https://github.com/twostraws/Inferno) -- Metal shaders for SwiftUI
- [GateEngine](https://github.com/STREGAsGate/GateEngine) -- Cross-platform Swift
- [Untold Engine](https://github.com/untoldengine/UntoldEngine) -- Pure Swift 3D
- [Fireblade ECS](https://github.com/fireblade-engine/ecs) -- Standalone ECS
- [SpriteKit vs SceneKit vs Metal](https://www.brsoftech.com/blog/spritekit-vs-scenekit-vs-metal/)
## Technique Map

- **Decision tree by target** — 2D game, 3D/AR, VFX pipeline, game logic, custom renderer; because framework choice depends on use case.
- **SceneKit deprecated** — Do not start new projects; migrate to RealityKit; because WWDC 25 deprecation.
- **SwiftUI integration check** — Vortex (particles), Inferno (shaders), RealityView, SpriteView; because many needs are SwiftUI-embedded.
- **ECS when needed** — RealityKit native or Fireblade standalone; because games/simulations benefit from entity-component architecture.
- **Reference routing** — apple-frameworks, third-party-engines, ps5-techniques, architecture-patterns; because each has deep content.

## Technique Notes

Comparison matrix: SpriteKit, RealityKit, Metal, GameplayKit, Vortex, Inferno, GateEngine, Untold, SwiftVVD, Fireblade. M1-M4 feasibility for console-quality: 60-90% PS5. References: apple-frameworks.md, architecture-patterns.md, ps5-techniques.md.

---

## Prompt Architect Overlay

**Role Definition:** Swift game engine and VFX stack selector. SpriteKit, RealityKit, Metal, GameplayKit, Vortex, Inferno, GateEngine. Architecture patterns, performance, cross-platform.

**Input Contract:** Accepts "which engine for X," 2D/3D game, VFX pipeline, particle system, or framework comparison. Target platform, SwiftUI needs, cross-platform needs.

**Output Contract:** Decision tree result with framework recommendation. Quick-start code pattern. Comparison matrix row. Reference to deep-dive (apple-frameworks, architecture-patterns). Related skills (vfx-spell-effects, metal-shaders, orb).

**Edge Cases & Fallbacks:** If SceneKit mentioned→warn deprecated; recommend RealityKit. If SwiftUI required→Vortex, Inferno, or MTKView in UIViewRepresentable. If cross-platform→GateEngine or SwiftVVD. If ECS→RealityKit or Fireblade.
