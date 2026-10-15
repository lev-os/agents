# VFX Architecture Patterns for Swift Apps

Design patterns for organizing rendering, effects, and game logic in Swift applications using Metal, RealityKit, SpriteKit, or custom engines.

---

## Entity-Component-System (ECS)

The dominant architecture for games and simulations. Separates identity, data, and logic.

### Core Concepts

- **Entity:** An ID (integer). Nothing more. No behavior, no data.
- **Component:** Pure data struct. Position, velocity, sprite, health, etc.
- **System:** Logic that processes entities with matching component sets.

### Why ECS?

| Problem | OOP Answer | ECS Answer |
|---------|------------|------------|
| Adding new behavior | New subclass or mixin | New component + system |
| Combining behaviors | Multiple inheritance / protocol explosion | Attach multiple components |
| Cache performance | Objects scattered in heap | Components packed in contiguous arrays |
| Querying "all entities with X" | Walk inheritance tree | Component archetype query |

### Swift Implementation (Protocol-Based)

```swift
// Component protocol
protocol Component {}

// Components are plain data
struct Position: Component {
    var x: Float
    var y: Float
}

struct Velocity: Component {
    var dx: Float
    var dy: Float
}

struct Renderable: Component {
    var textureName: String
    var scale: Float
    var opacity: Float
}

struct Health: Component {
    var current: Int
    var max: Int
}

// Entity is just an ID
typealias EntityID = UInt64

// World: the container
@Observable
class World {
    private var nextID: EntityID = 0
    private var components: [String: [EntityID: any Component]] = [:]

    func createEntity() -> EntityID {
        let id = nextID
        nextID += 1
        return id
    }

    func addComponent<T: Component>(_ component: T, to entity: EntityID) {
        let key = String(describing: T.self)
        if components[key] == nil { components[key] = [:] }
        components[key]![entity] = component
    }

    func getComponent<T: Component>(_ type: T.Type, for entity: EntityID) -> T? {
        let key = String(describing: T.self)
        return components[key]?[entity] as? T
    }

    func setComponent<T: Component>(_ component: T, for entity: EntityID) {
        let key = String(describing: T.self)
        components[key]?[entity] = component
    }

    func entitiesWith<T: Component>(_ type: T.Type) -> [(EntityID, T)] {
        let key = String(describing: T.self)
        return (components[key] ?? [:]).compactMap { (id, comp) in
            (comp as? T).map { (id, $0) }
        }
    }
}

// System: processes matching entities
protocol System {
    func update(world: World, deltaTime: Float)
}

struct MovementSystem: System {
    func update(world: World, deltaTime: Float) {
        for (entity, velocity) in world.entitiesWith(Velocity.self) {
            guard var position = world.getComponent(Position.self, for: entity) else { continue }
            position.x += velocity.dx * deltaTime
            position.y += velocity.dy * deltaTime
            world.setComponent(position, for: entity)
        }
    }
}

// Game loop
class GameLoop {
    let world = World()
    var systems: [System] = [MovementSystem()]

    func update(deltaTime: Float) {
        for system in systems {
            system.update(world: world, deltaTime: deltaTime)
        }
    }
}
```

### RealityKit's Built-in ECS

RealityKit uses ECS natively. No need for a custom implementation when using RealityKit:

```swift
import RealityKit

// Component (conform to RealityKit's Component protocol)
struct SpinComponent: Component {
    var speed: Float = 1.0
}

// System (conform to RealityKit's System protocol)
struct SpinSystem: System {
    static let query = EntityQuery(where: .has(SpinComponent.self))

    init(scene: Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            let spin = entity.components[SpinComponent.self]!
            entity.transform.rotation *= simd_quatf(angle: spin.speed * Float(context.deltaTime), axis: [0, 1, 0])
        }
    }
}

// Register system
SpinSystem.registerSystem()
SpinComponent.registerComponent()
```

---

## Render Graph

Declare render passes as a directed acyclic graph (DAG). The framework resolves execution order, resource lifetimes, and synchronization automatically.

### Why Render Graph?

- **Automatic resource management:** Transient textures allocated/freed by the graph
- **Dependency resolution:** Passes execute in correct order based on read/write dependencies
- **Parallelism:** Independent passes can execute concurrently on GPU
- **Debugging:** Graph visualizable as DAG for understanding pipeline

### Swift Implementation

```swift
// Resource handle (lightweight reference)
struct RenderResource: Hashable {
    let name: String
    let format: MTLPixelFormat
    let width: Int
    let height: Int
}

// Render pass declaration
protocol RenderPass {
    var name: String { get }
    var inputs: [RenderResource] { get }    // textures this pass reads
    var outputs: [RenderResource] { get }   // textures this pass writes

    func execute(encoder: MTLRenderCommandEncoder, resources: [RenderResource: MTLTexture])
}

// Graph builder
class RenderGraph {
    private var passes: [RenderPass] = []
    private var sortedPasses: [RenderPass] = []

    func addPass(_ pass: RenderPass) {
        passes.append(pass)
    }

    func compile() {
        // Topological sort based on input/output dependencies
        sortedPasses = topologicalSort(passes)
    }

    func execute(commandBuffer: MTLCommandBuffer, device: MTLDevice) {
        // Allocate transient resources
        var resources: [RenderResource: MTLTexture] = [:]
        for pass in sortedPasses {
            for output in pass.outputs where resources[output] == nil {
                resources[output] = allocateTexture(device: device, resource: output)
            }
        }

        // Execute passes in order
        for pass in sortedPasses {
            let descriptor = MTLRenderPassDescriptor()
            // Configure attachments from outputs
            if let encoder = commandBuffer.makeRenderCommandEncoder(descriptor: descriptor) {
                pass.execute(encoder: encoder, resources: resources)
                encoder.endEncoding()
            }
        }

        // Transient resources freed after command buffer completes
    }

    private func allocateTexture(device: MTLDevice, resource: RenderResource) -> MTLTexture {
        let desc = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: resource.format,
            width: resource.width,
            height: resource.height,
            mipmapped: false
        )
        desc.usage = [.renderTarget, .shaderRead]
        desc.storageMode = .private
        return device.makeTexture(descriptor: desc)!
    }

    private func topologicalSort(_ passes: [RenderPass]) -> [RenderPass] {
        // Build adjacency from output->input matches, then Kahn's algorithm
        // Simplified: order passes so writers come before readers
        var sorted: [RenderPass] = []
        var remaining = passes
        var produced: Set<RenderResource> = []

        while !remaining.isEmpty {
            let (ready, notReady) = remaining.partition { pass in
                pass.inputs.allSatisfy { produced.contains($0) || !passes.contains(where: { $0.outputs.contains($0) }) }
            }
            for pass in ready {
                sorted.append(pass)
                produced.formUnion(pass.outputs)
            }
            remaining = notReady
            if ready.isEmpty && !remaining.isEmpty {
                fatalError("Render graph has a cycle")
            }
        }
        return sorted
    }
}

// Extension for partition
extension Array {
    func partition(_ predicate: (Element) -> Bool) -> ([Element], [Element]) {
        var yes: [Element] = []
        var no: [Element] = []
        for element in self {
            if predicate(element) { yes.append(element) }
            else { no.append(element) }
        }
        return (yes, no)
    }
}
```

### Example: Deferred Rendering Graph

```
GBufferPass (writes: albedo, normal, depth)
    ├── SSAOPass (reads: normal, depth; writes: ao)
    ├── ShadowPass (writes: shadowMap)
    └── LightingPass (reads: albedo, normal, depth, ao, shadowMap; writes: hdrColor)
            └── BloomPass (reads: hdrColor; writes: bloomColor)
                    └── ToneMappingPass (reads: bloomColor; writes: ldrColor)
                            └── FXAAPass (reads: ldrColor; writes: finalColor)
```

---

## Effect Stack / Compositor

Ordered list of post-processing effects applied sequentially. Each effect reads the previous output and writes a new output.

### Pattern

```swift
// Effect protocol
protocol PostEffect {
    var name: String { get }
    var isEnabled: Bool { get set }

    func apply(
        input: MTLTexture,
        output: MTLTexture,
        commandBuffer: MTLCommandBuffer,
        device: MTLDevice
    )
}

// Effect stack
class EffectCompositor {
    var effects: [PostEffect] = []
    private var pingPongTextures: [MTLTexture] = []

    func addEffect(_ effect: PostEffect) {
        effects.append(effect)
    }

    func process(
        input: MTLTexture,
        output: MTLTexture,
        commandBuffer: MTLCommandBuffer,
        device: MTLDevice
    ) {
        let activeEffects = effects.filter(\.isEnabled)
        guard !activeEffects.isEmpty else {
            // Blit input to output
            blitCopy(from: input, to: output, commandBuffer: commandBuffer)
            return
        }

        ensurePingPong(matching: input, device: device)

        var currentInput = input
        for (index, effect) in activeEffects.enumerated() {
            let currentOutput: MTLTexture
            if index == activeEffects.count - 1 {
                currentOutput = output  // Last effect writes to final output
            } else {
                currentOutput = pingPongTextures[index % 2]
            }

            effect.apply(
                input: currentInput,
                output: currentOutput,
                commandBuffer: commandBuffer,
                device: device
            )

            currentInput = currentOutput
        }
    }

    private func ensurePingPong(matching texture: MTLTexture, device: MTLDevice) {
        if pingPongTextures.isEmpty || pingPongTextures[0].width != texture.width {
            let desc = MTLTextureDescriptor.texture2DDescriptor(
                pixelFormat: texture.pixelFormat,
                width: texture.width,
                height: texture.height,
                mipmapped: false
            )
            desc.usage = [.renderTarget, .shaderRead]
            desc.storageMode = .private
            pingPongTextures = [
                device.makeTexture(descriptor: desc)!,
                device.makeTexture(descriptor: desc)!
            ]
        }
    }
}

// Example effects
struct BloomEffect: PostEffect {
    var name = "Bloom"
    var isEnabled = true
    var threshold: Float = 0.8
    var intensity: Float = 1.0

    func apply(input: MTLTexture, output: MTLTexture, commandBuffer: MTLCommandBuffer, device: MTLDevice) {
        // 1. Threshold pass: extract bright pixels
        // 2. Downsample + Gaussian blur (separable, horizontal then vertical)
        // 3. Composite: output = input + blurred * intensity
    }
}

struct ColorGradingEffect: PostEffect {
    var name = "Color Grading"
    var isEnabled = true
    var lutTexture: MTLTexture?

    func apply(input: MTLTexture, output: MTLTexture, commandBuffer: MTLCommandBuffer, device: MTLDevice) {
        // Sample 3D LUT texture for color transformation
    }
}

struct VignetteEffect: PostEffect {
    var name = "Vignette"
    var isEnabled = true
    var intensity: Float = 0.5
    var radius: Float = 0.8

    func apply(input: MTLTexture, output: MTLTexture, commandBuffer: MTLCommandBuffer, device: MTLDevice) {
        // Darken corners based on distance from center
    }
}

// Usage
let compositor = EffectCompositor()
compositor.addEffect(BloomEffect())
compositor.addEffect(ColorGradingEffect())
compositor.addEffect(VignetteEffect())
// compositor.addEffect(FXAAEffect())  // Anti-aliasing last
```

### Typical Effect Stack Order

```
1. SSAO (ambient occlusion)
2. SSR (screen-space reflections)
3. Bloom (HDR glow)
4. Color grading (LUT or curves)
5. Vignette
6. Film grain / chromatic aberration (optional)
7. FXAA / TAA (anti-aliasing - always last before UI)
```

---

## VFX Manager Pattern

Centralized effect spawner that pools and recycles effect instances.

### Pattern

```swift
@Observable
class VFXManager {
    private var pools: [String: [VFXInstance]] = [:]
    private var activeEffects: [VFXInstance] = []
    private let maxPoolSize = 50

    // Spawn an effect
    func spawn(type: VFXType, at position: SIMD3<Float>, params: VFXParams = .default) {
        let instance = acquire(type: type)
        instance.position = position
        instance.params = params
        instance.activate()
        activeEffects.append(instance)
    }

    // Update all active effects
    func update(deltaTime: Float) {
        activeEffects.removeAll { effect in
            effect.update(deltaTime: deltaTime)
            if effect.isFinished {
                release(effect)
                return true
            }
            return false
        }
    }

    // Pool management
    private func acquire(type: VFXType) -> VFXInstance {
        let key = type.rawValue
        if var pool = pools[key], let instance = pool.popLast() {
            pools[key] = pool
            return instance
        }
        return VFXInstance(type: type)
    }

    private func release(_ instance: VFXInstance) {
        let key = instance.type.rawValue
        instance.deactivate()
        if (pools[key]?.count ?? 0) < maxPoolSize {
            if pools[key] == nil { pools[key] = [] }
            pools[key]!.append(instance)
        }
        // else: let it deallocate (pool full)
    }
}

enum VFXType: String {
    case explosion, sparks, smoke, heal, shield, lightning, impact
}

struct VFXParams {
    var intensity: Float = 1.0
    var color: SIMD3<Float> = [1, 1, 1]
    var duration: Float = 1.0
    var scale: Float = 1.0

    static let `default` = VFXParams()
}

class VFXInstance {
    let type: VFXType
    var position: SIMD3<Float> = .zero
    var params: VFXParams = .default
    var elapsed: Float = 0
    var isFinished: Bool { elapsed >= params.duration }

    init(type: VFXType) { self.type = type }

    func activate() { elapsed = 0 }
    func deactivate() { /* reset state */ }

    func update(deltaTime: Float) {
        elapsed += deltaTime
        // Update particles, shaders, etc. based on type and elapsed/duration
    }
}
```

### Usage in Game Loop

```swift
class GameScene {
    let vfxManager = VFXManager()

    func onEnemyHit(at position: SIMD3<Float>, damage: Int) {
        vfxManager.spawn(type: .impact, at: position, params: VFXParams(
            intensity: Float(damage) / 100.0,
            color: [1, 0.3, 0],
            duration: 0.5
        ))
        vfxManager.spawn(type: .sparks, at: position, params: VFXParams(
            intensity: 0.8,
            duration: 0.3,
            scale: 1.5
        ))
    }

    func update(deltaTime: Float) {
        vfxManager.update(deltaTime: deltaTime)
    }
}
```

---

## Audio-Visual Sync

Bind effect parameters to real-time audio analysis for reactive visuals.

### Pattern

```swift
import Accelerate

@Observable
class AudioAnalyzer {
    var rmsLevel: Float = 0       // 0.0-1.0, overall volume
    var bassLevel: Float = 0      // Low frequency energy
    var midLevel: Float = 0       // Mid frequency energy
    var trebleLevel: Float = 0    // High frequency energy
    var peakDetected: Bool = false

    private let fftSetup: vDSP_DFT_Setup
    private let fftSize = 1024
    private var magnitudes: [Float]

    init() {
        fftSetup = vDSP_DFT_zop_CreateSetup(nil, vDSP_Length(fftSize), .FORWARD)!
        magnitudes = [Float](repeating: 0, count: fftSize / 2)
    }

    func analyze(buffer: [Float]) {
        // RMS (overall level)
        var rms: Float = 0
        vDSP_rmsqv(buffer, 1, &rms, vDSP_Length(buffer.count))
        rmsLevel = min(rms * 5.0, 1.0)  // scale to 0-1

        // FFT for frequency bands
        var realPart = [Float](repeating: 0, count: fftSize)
        var imagPart = [Float](repeating: 0, count: fftSize)
        realPart.replaceSubrange(0..<min(buffer.count, fftSize), with: buffer.prefix(fftSize))

        var realOut = [Float](repeating: 0, count: fftSize)
        var imagOut = [Float](repeating: 0, count: fftSize)
        vDSP_DFT_Execute(fftSetup, &realPart, &imagPart, &realOut, &imagOut)

        // Compute magnitudes
        for i in 0..<fftSize/2 {
            magnitudes[i] = sqrt(realOut[i] * realOut[i] + imagOut[i] * imagOut[i])
        }

        // Band energy (assuming 44100 Hz sample rate)
        let binWidth = 44100.0 / Float(fftSize)
        let bassEnd = Int(250 / binWidth)       // 0-250 Hz
        let midEnd = Int(4000 / binWidth)       // 250-4000 Hz

        var bassSum: Float = 0
        vDSP_sve(Array(magnitudes[0..<bassEnd]), 1, &bassSum, vDSP_Length(bassEnd))
        bassLevel = min(bassSum / Float(bassEnd) * 2.0, 1.0)

        var midSum: Float = 0
        vDSP_sve(Array(magnitudes[bassEnd..<midEnd]), 1, &midSum, vDSP_Length(midEnd - bassEnd))
        midLevel = min(midSum / Float(midEnd - bassEnd) * 3.0, 1.0)

        var trebleSum: Float = 0
        let trebleCount = fftSize/2 - midEnd
        vDSP_sve(Array(magnitudes[midEnd..<fftSize/2]), 1, &trebleSum, vDSP_Length(trebleCount))
        trebleLevel = min(trebleSum / Float(trebleCount) * 5.0, 1.0)

        // Peak detection (simple threshold)
        peakDetected = rmsLevel > 0.8
    }
}

// Bridge: audio analysis -> VFX parameters
struct EffectParameterBridge {
    let analyzer: AudioAnalyzer

    var glowIntensity: Float { analyzer.rmsLevel }
    var pulseScale: Float { 1.0 + analyzer.bassLevel * 0.3 }
    var particleRate: Float { analyzer.midLevel * 200 }
    var colorShift: Float { analyzer.trebleLevel }
    var shouldBurst: Bool { analyzer.peakDetected }
}
```

### SwiftUI Integration

```swift
struct AudioReactiveOrb: View {
    let analyzer: AudioAnalyzer
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Circle()
            .fill(
                RadialGradient(
                    colors: [
                        Color(hue: Double(analyzer.trebleLevel * 0.3), saturation: 0.8, brightness: 1.0),
                        .purple
                    ],
                    center: .center,
                    startRadius: 0,
                    endRadius: 60
                )
            )
            .frame(width: 120, height: 120)
            .scaleEffect(reduceMotion ? 1.0 : 1.0 + CGFloat(analyzer.bassLevel) * 0.2)
            .shadow(color: .purple.opacity(Double(analyzer.rmsLevel) * 0.8), radius: CGFloat(analyzer.rmsLevel) * 30)
            .animation(.easeOut(duration: 0.05), value: analyzer.rmsLevel)
    }
}
```

---

## State-Driven Effects

Use a state machine (Swift enum or GameplayKit GKStateMachine) to drive VFX transitions.

### Swift Enum State Machine

```swift
enum SpellPhase: String, CaseIterable {
    case idle
    case charging
    case casting
    case impact
    case dissipating

    var duration: TimeInterval {
        switch self {
        case .idle: return .infinity
        case .charging: return 0.5
        case .casting: return 1.0
        case .impact: return 0.3
        case .dissipating: return 0.8
        }
    }

    var next: SpellPhase? {
        switch self {
        case .idle: return nil  // Trigger manually
        case .charging: return .casting
        case .casting: return .impact
        case .impact: return .dissipating
        case .dissipating: return .idle
        }
    }
}

@Observable
class SpellState {
    var phase: SpellPhase = .idle
    var elapsed: TimeInterval = 0
    var progress: Float { min(Float(elapsed / phase.duration), 1.0) }

    // Per-phase VFX parameters
    var particleRate: Float {
        switch phase {
        case .idle: return 0
        case .charging: return 50 * progress
        case .casting: return 200
        case .impact: return 500 * (1 - progress)
        case .dissipating: return 20 * (1 - progress)
        }
    }

    var glowIntensity: Float {
        switch phase {
        case .idle: return 0
        case .charging: return progress * 0.5
        case .casting: return 1.0
        case .impact: return 1.5 * (1 - progress)
        case .dissipating: return 0.3 * (1 - progress)
        }
    }

    var shakeAmplitude: Float {
        switch phase {
        case .impact: return 10 * (1 - progress)
        default: return 0
        }
    }

    func trigger() {
        guard phase == .idle else { return }
        transition(to: .charging)
    }

    func update(deltaTime: TimeInterval) {
        guard phase != .idle else { return }
        elapsed += deltaTime

        if elapsed >= phase.duration, let next = phase.next {
            transition(to: next)
        }
    }

    private func transition(to newPhase: SpellPhase) {
        phase = newPhase
        elapsed = 0
        onPhaseEnter(newPhase)
    }

    private func onPhaseEnter(_ phase: SpellPhase) {
        switch phase {
        case .impact:
            // Trigger burst effects, screen shake, sound
            break
        case .idle:
            // Clean up all effects
            break
        default:
            break
        }
    }
}
```

---

## Composition Over Inheritance

Build complex effects by composing independent components rather than inheriting from a base effect class.

### Pattern

```swift
// Each component handles one concern
protocol EffectComponent {
    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float)
    func render(context: inout GraphicsContext, size: CGSize)
}

struct ParticleEffectComponent: EffectComponent {
    var particles: [Particle] = []
    var emissionRate: Float = 100
    var color: Color = .orange

    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float) {
        // Spawn and update particles based on phase
    }

    func render(context: inout GraphicsContext, size: CGSize) {
        for particle in particles {
            context.fill(
                Circle().path(in: CGRect(x: CGFloat(particle.x), y: CGFloat(particle.y), width: 4, height: 4)),
                with: .color(color.opacity(Double(particle.alpha)))
            )
        }
    }
}

struct ShaderEffectComponent: EffectComponent {
    var shaderName: String
    var intensity: Float = 0

    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float) {
        intensity = phase == .casting ? 1.0 : progress
    }

    func render(context: inout GraphicsContext, size: CGSize) {
        // Apply shader via context or view modifier
    }
}

struct AudioEffectComponent: EffectComponent {
    var soundName: String
    var isPlaying: Bool = false

    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float) {
        switch phase {
        case .charging: if !isPlaying { play(); isPlaying = true }
        case .idle: if isPlaying { stop(); isPlaying = false }
        default: break
        }
    }

    func render(context: inout GraphicsContext, size: CGSize) {
        // Audio has no visual render
    }

    private func play() { /* AVAudioPlayer or AudioEngine */ }
    private func stop() { /* stop playback */ }
}

struct ScreenShakeComponent: EffectComponent {
    var amplitude: CGFloat = 0
    var offset: CGSize = .zero

    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float) {
        if phase == .impact {
            amplitude = CGFloat(10 * (1 - progress))
            offset = CGSize(
                width: CGFloat.random(in: -amplitude...amplitude),
                height: CGFloat.random(in: -amplitude...amplitude)
            )
        } else {
            amplitude = 0
            offset = .zero
        }
    }

    func render(context: inout GraphicsContext, size: CGSize) {
        // Shake applied as view offset, not in context
    }
}

// Composed effect
struct ComposedSpellEffect {
    var components: [any EffectComponent] = [
        ParticleEffectComponent(emissionRate: 150, color: .cyan),
        ShaderEffectComponent(shaderName: "glow"),
        AudioEffectComponent(soundName: "spell_cast"),
        ScreenShakeComponent()
    ]

    mutating func update(deltaTime: Float, phase: SpellPhase, progress: Float) {
        for i in components.indices {
            components[i].update(deltaTime: deltaTime, phase: phase, progress: progress)
        }
    }
}
```

### Benefits of Composition

- **Mix and match:** Fire spell = [particles(orange) + shader(distortion) + audio(fire_crackle)]
- **Reuse:** Same particle component in explosion, magic, and rain effects
- **Test independently:** Each component has clear inputs/outputs
- **Add without modifying:** New components don't touch existing ones
- **Performance:** Disable individual components without rebuilding the effect
