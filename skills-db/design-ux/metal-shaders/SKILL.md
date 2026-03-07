---
name: metal-shaders
description: Build and debug production Metal shaders for Apple platforms, including SwiftUI stitchable effects, MPS usage, and real-time GPU performance practices.
triggers:
  - metal shader
  - MSL
  - fragment shader
  - compute shader
  - ray marching
  - SDF
  - volumetric rendering
  - noise function
  - perlin noise
  - colorEffect
  - distortionEffect
  - layerEffect
  - stitchable
  - ShaderLibrary
  - MPS
  - bloom shader
  - gaussian blur
  - post-processing
  - GPU compute
  - particle simulation
  - cloth simulation
  - threadgroup
---

# Metal Shaders -- MSL for Apple Platforms

## Decision Tree

```
What shader do you need?
|
|-- SwiftUI visual effect?
|   |-- Per-pixel color transform (tint, invert, threshold)?
|   |   -> colorEffect  -> references/swiftui-integration.md#colorEffect
|   |-- Geometric distortion (ripple, wave, lens)?
|   |   -> distortionEffect  -> references/swiftui-integration.md#distortionEffect
|   |-- Multi-sample effect (blur, glow, shadow)?
|   |   -> layerEffect  -> references/swiftui-integration.md#layerEffect
|   \-- Standard filter (blur, edge detect)?
|       -> MPS framework  -> references/metal-performance-shaders.md
|
|-- Post-processing / render pass?
|   |-- Bloom / glow extraction? -> references/fragment-shaders.md#bloom
|   |-- Color grading / LUT?     -> references/fragment-shaders.md#color-grading
|   |-- Vignette?                 -> references/fragment-shaders.md#vignette
|   |-- Chromatic aberration?     -> references/fragment-shaders.md#chromatic-aberration
|   |-- Film grain / CRT?        -> references/fragment-shaders.md#film-grain
|   \-- Gaussian blur?           -> references/fragment-shaders.md#gaussian-blur
|
|-- GPU compute workload?
|   |-- Particle simulation?      -> references/compute-shaders.md#particles
|   |-- Physics / cloth?          -> references/compute-shaders.md#physics
|   |-- Image processing?         -> references/compute-shaders.md#image-processing
|   |-- GPU-driven rendering?     -> references/compute-shaders.md#gpu-driven
|   \-- General parallel work?    -> references/compute-shaders.md#architecture
|
|-- Procedural geometry / volumetrics?
|   |-- SDF scene (shapes, booleans)? -> references/ray-marching.md#sdf
|   |-- Volumetric fog / clouds?      -> references/ray-marching.md#volumetric
|   \-- Full ray marcher?             -> references/ray-marching.md#ray-marcher
|
|-- Procedural noise / textures?
|   |-- Perlin noise?         -> references/noise-functions.md#perlin
|   |-- Simplex noise?        -> references/noise-functions.md#simplex
|   |-- Worley / Voronoi?     -> references/noise-functions.md#worley
|   |-- fBm / fractal layers? -> references/noise-functions.md#fbm
|   \-- Domain warping?       -> references/noise-functions.md#domain-warping
|
\-- Performance / debugging?
    |-- GPU frame capture?    -> references/fragment-shaders.md#debugging
    |-- Occupancy tuning?     -> references/compute-shaders.md#performance
    \-- half vs float?        -> MSL Type Reference below
```

## Quick Reference: Shader Types x Use Cases

| Type | MSL Entry Point | Use Cases | SwiftUI Modifier | Ref |
|------|----------------|-----------|------------------|-----|
| Fragment (color) | `fragment half4 fn(...)` | Post-process, color grade, bloom | `.colorEffect()` | `references/fragment-shaders.md` |
| Fragment (distort) | `fragment float2 fn(...)` | Ripple, wave, lens warp | `.distortionEffect()` | `references/swiftui-integration.md` |
| Fragment (layer) | `fragment half4 fn(...)` | Blur, glow, shadow, multi-sample | `.layerEffect()` | `references/swiftui-integration.md` |
| Compute (kernel) | `kernel void fn(...)` | Particles, physics, image proc | N/A (MTLComputeCommandEncoder) | `references/compute-shaders.md` |
| Vertex | `vertex VertexOut fn(...)` | Mesh deformation, instancing | N/A (render pipeline) | Apple docs |

## SwiftUI Integration Cheat Sheet

### Three Modifier Types with Exact Signatures

```
colorEffect  ->  [[ stitchable ]] half4 name(float2 position, half4 color, <args...>)
                 Receives: pixel position + current color
                 Returns: new color

distortionEffect  ->  [[ stitchable ]] float2 name(float2 position, <args...>)
                      Receives: pixel position
                      Returns: source coordinate to sample from
                      Requires: maxSampleOffset

layerEffect  ->  [[ stitchable ]] half4 name(float2 position, SwiftUI::Layer layer, <args...>)
                 Receives: pixel position + layer (can sample any coordinate)
                 Returns: new color
                 Requires: maxSampleOffset
```

### Swift-Side Parameter Passing

```swift
.colorEffect(ShaderLibrary.myShader(
    .float(time),           // float
    .float2(CGSize(w, h)),  // float2
    .color(.red),           // half4
    .image(Image("tex")),   // texture2d
    .data(Data(...))        // device buffer
))
```

### TimelineView Animation Pattern

```swift
TimelineView(.animation) { timeline in
    let time = timeline.date.timeIntervalSinceReferenceDate
    content
        .colorEffect(ShaderLibrary.pulse(.float(time)))
}
```

## MSL Type Quick Reference

| MSL Type | Bytes | Use For | Notes |
|----------|-------|---------|-------|
| `half` | 2 | Scalars (color, alpha) | Prefer over float for color math |
| `half4` | 8 | Colors (RGBA) | Standard SwiftUI color type |
| `float` | 4 | Position, time, angles | Full precision when needed |
| `float2` | 8 | UV coords, positions | Standard position type |
| `float3` | 12 | 3D position, RGB | |
| `float4` | 16 | Homogeneous coords | |
| `float4x4` | 64 | Transform matrices | |
| `texture2d<half>` | -- | Color textures | Use `half` access for perf |
| `texture2d<float>` | -- | Data textures (normals, depth) | When precision matters |
| `uint2` | 8 | Thread position | `thread_position_in_grid` |
| `ushort2` | 4 | Thread position (small) | Save registers |

### Key MSL Qualifiers

| Qualifier | Meaning |
|-----------|---------|
| `[[ stitchable ]]` | Function can be called from SwiftUI shader modifiers |
| `[[ position ]]` | Vertex output clip-space position |
| `[[ color(0) ]]` | Fragment output to color attachment 0 |
| `[[ stage_in ]]` | Interpolated vertex output → fragment input |
| `[[ thread_position_in_grid ]]` | Global thread ID in compute |
| `[[ thread_position_in_threadgroup ]]` | Local thread ID in threadgroup |
| `[[ threadgroup_position_in_grid ]]` | Threadgroup ID |
| `[[ threads_per_threadgroup ]]` | Threadgroup dimensions |
| `constant` | Read-only buffer (uniform) |
| `device` | Read/write buffer (SSBO) |
| `threadgroup` | Shared memory within threadgroup |
| `thread` | Per-thread local |

## Performance Rules (Top 10)

1. **Use `half` over `float`** for color math -- conversions are free on Apple GPU
2. **Minimize texture samples** -- each sample is expensive; cache in registers
3. **Branch-free code** -- SIMD groups execute both branches; use `mix()`/`select()` instead of `if`
4. **Threadgroup size = multiple of threadExecutionWidth** (typically 32) -- avoids wasted lanes
5. **Memory coalescing** -- adjacent threads should access adjacent memory addresses
6. **Avoid threadgroup bank conflicts** -- stagger access patterns or pad shared arrays
7. **Early termination** in ray marching -- `if (totalAlpha > 0.99) break;`
8. **Separable filters** -- 2-pass (H+V) is O(2N) vs O(N^2) for 2D convolution
9. **Texture-based noise lookup** vs computed -- precompute for static noise, compute for animated
10. **Profile with GPU Frame Capture** in Xcode before optimizing -- measure, don't guess

## Cross-References

| Skill | Relation |
|-------|----------|
| `orb` | T5 Metal ripple shader -- practical SwiftUI shader example |
| `swiftui-animation` | Animation-driven shader parameters (TimelineView, spring) |
| `vfx-spell-effects` | Effect composition using these shader patterns |
| `swiftui-expert-skill` | SwiftUI view lifecycle for shader integration |
| `swiftui-performance-audit` | Diagnosing GPU-related SwiftUI perf issues |

## Key Resources

- [Metal Shading Language Specification (PDF)](https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf)
- [Metal Overview -- Apple Developer](https://developer.apple.com/metal/)
- [Metal Performance Shaders](https://developer.apple.com/documentation/metalperformanceshaders)
- [Metal in SwiftUI -- Jacob Bartlett](https://blog.jacobstechtavern.com/p/metal-in-swiftui-how-to-write-shaders)
- [Metal Shaders in SwiftUI -- Hacking with Swift](https://www.hackingwithswift.com/quick-start/swiftui/how-to-add-metal-shaders-to-swiftui-views-using-layer-effects)
- [Inferno -- 17 SwiftUI Metal Shaders](https://github.com/twostraws/Inferno)
- [The Book of Shaders -- Noise](https://thebookofshaders.com/11/)
- [Ray Marching & SDFs -- Jamie Wong](https://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/)
- [SDF Primitives -- Inigo Quilez](https://iquilezles.org/articles/distfunctions/)
- [Ray Marching Distance Fields -- Inigo Quilez](https://iquilezles.org/articles/raymarchingdf/)
## Technique Map

- **Shader type routing** — colorEffect (per-pixel), distortionEffect (geometric), layerEffect (multi-sample); because each modifier has distinct signature and use case.
- **Stitchable qualifier** — Required for SwiftUI shader modifiers; because enables function call from SwiftUI.
- **half over float for color** — Use half/half4 for color math; because conversions are free on Apple GPU; reduces register pressure.
- **Branch-free code** — Use mix()/select() instead of if; because SIMD groups execute both branches; branches cost.
- **Profile with GPU Frame Capture** — Measure before optimizing; because guessing causes wrong optimizations.
- **Threadgroup size = multiple of 32** — Align to threadExecutionWidth; because avoids wasted SIMD lanes.
- **Separable filters** — 2-pass H+V for blur; because O(2N) vs O(N²) for 2D convolution.

## Technique Notes

MSL types: half4 for colors, float2 for positions. Swift passes .float(time), .float2(CGSize), .color(), .image(). TimelineView drives animation. References: fragment-shaders.md, compute-shaders.md, ray-marching.md, noise-functions.md.

---

## Prompt Architect Overlay

**Role Definition:** Metal shader expert for Apple platforms. Covers MSL, SwiftUI stitchable effects (colorEffect, distortionEffect, layerEffect), MPS, compute shaders, ray marching, and GPU performance.

**Input Contract:** Accepts shader type (visual effect, post-process, compute, procedural), target (SwiftUI, Metal pipeline), and performance constraints. Code or description of desired effect.

**Output Contract:** MSL code with correct signatures, Swift integration snippet, performance considerations. Routes to appropriate reference (fragment, compute, ray-marching, noise). Decision tree for shader type selection.

**Edge Cases & Fallbacks:** If SwiftUI modifier not working→verify stitchable, maxSampleOffset. If performance issue→profile first; check half vs float, texture samples, branch-free. If cross-platform→note iOS 17+ for SwiftUI shaders.
