# Console-Quality Techniques for Apple Silicon

How to implement PS5-tier rendering techniques using Metal on Apple Silicon. Feasibility assessments, implementation patterns, and performance expectations.

## Feasibility Matrix

| Technique | M1 | M2 | M3/M4 | PS5 | Key Constraint |
|-----------|----|----|-------|-----|----------------|
| Temporal Anti-Aliasing (TAA) | Full | Full | Full | Full | Compute shader complexity |
| MetalFX Temporal Upscaling | Full | Full | Full | N/A (PSSR) | Apple-exclusive, excellent |
| MetalFX Spatial Upscaling | Full | Full | Full | N/A (FSR) | Simpler, lower quality |
| Screen-Space Reflections | Full | Full | Full | Full | Memory bandwidth |
| Mesh Shaders | No | Partial | Full | Full | M3+ for object+mesh stages |
| Variable Rate Shading | No | No | Full | Full | M3+ hardware feature |
| Hardware Ray Tracing | Basic | Better | Full | Full | BLAS/TLAS build cost |
| Volumetric Lighting | Full | Full | Full | Full | Ray march sample count |
| Global Illumination (SSGI) | Partial | Good | Full | Full | Memory bandwidth |
| Cascaded Shadow Maps | Full | Full | Full | Full | Texture memory |
| HDR + Tone Mapping | Full | Full | Full | Full | Trivial on all HW |
| Deferred Rendering | Full | Full | Full | Full | G-buffer bandwidth |

### Overall Quality Estimate

- **M1:** 60-80% of PS5 visual quality
- **M2:** 70-85% of PS5 visual quality
- **M3/M4:** 80-90% of PS5 visual quality
- **Key bottleneck:** Memory bandwidth. PS5 has 448 GB/s (GDDR6). M1 has 68 GB/s. M3 Pro has 150 GB/s. M4 Max has 546 GB/s.

---

## Temporal Anti-Aliasing (TAA)

Eliminates jagged edges by accumulating samples across frames with sub-pixel jitter.

### How It Works

1. **Jitter** the projection matrix by sub-pixel offset each frame (Halton sequence)
2. **Render** the scene normally
3. **Reproject** previous frame's result using motion vectors
4. **Blend** current frame with reprojected history (typically 90% history, 10% current)
5. **Clamp** history color to neighborhood of current frame to prevent ghosting

### Metal Implementation

```metal
// TAA resolve compute shader
kernel void taaResolve(
    texture2d<float, access::read> currentFrame [[texture(0)]],
    texture2d<float, access::read> historyFrame [[texture(1)]],
    texture2d<float, access::read> motionVectors [[texture(2)]],
    texture2d<float, access::write> output [[texture(3)]],
    uint2 gid [[thread_position_in_grid]]
) {
    float2 uv = float2(gid) / float2(output.get_width(), output.get_height());

    // Read motion vector and reproject
    float2 motion = motionVectors.read(gid).xy;
    float2 historyUV = uv - motion;

    float4 current = currentFrame.read(gid);
    float4 history = historyFrame.read(uint2(historyUV * float2(output.get_width(), output.get_height())));

    // Neighborhood clamping (3x3 min/max)
    float4 minColor = current, maxColor = current;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            float4 neighbor = currentFrame.read(gid + uint2(x, y));
            minColor = min(minColor, neighbor);
            maxColor = max(maxColor, neighbor);
        }
    }
    history = clamp(history, minColor, maxColor);

    // Blend (favor history for stability)
    float blendFactor = 0.1;  // 10% current, 90% history
    output.write(mix(history, current, blendFactor), gid);
}
```

### Jitter Pattern (Swift Side)

```swift
// Halton sequence for sub-pixel jitter
func halton(index: Int, base: Int) -> Float {
    var result: Float = 0
    var f: Float = 1.0 / Float(base)
    var i = index
    while i > 0 {
        result += f * Float(i % base)
        i /= base
        f /= Float(base)
    }
    return result
}

// Apply jitter to projection matrix
func jitteredProjection(base: float4x4, frameIndex: Int, width: Float, height: Float) -> float4x4 {
    let jitterX = (halton(index: frameIndex, base: 2) - 0.5) * 2.0 / width
    let jitterY = (halton(index: frameIndex, base: 3) - 0.5) * 2.0 / height
    var jittered = base
    jittered[2][0] += jitterX
    jittered[2][1] += jitterY
    return jittered
}
```

---

## MetalFX Upscaling

Apple's answer to DLSS/FSR/PSSR. Render at lower resolution, upscale to display resolution with temporal or spatial methods.

### Temporal Upscaling (Higher Quality)

Uses motion vectors and history to reconstruct detail. Best quality, requires motion vector output.

```swift
import MetalFX

// Create temporal scaler
let descriptor = MTLFXTemporalScalerDescriptor()
descriptor.inputWidth = renderWidth       // e.g., 1280
descriptor.inputHeight = renderHeight     // e.g., 720
descriptor.outputWidth = displayWidth     // e.g., 2560
descriptor.outputHeight = displayHeight   // e.g., 1440
descriptor.colorTextureFormat = .rgba16Float
descriptor.depthTextureFormat = .depth32Float
descriptor.motionTextureFormat = .rg16Float
descriptor.outputTextureFormat = .rgba16Float

guard let scaler = descriptor.makeTemporalScaler(device: device) else {
    fatalError("MetalFX temporal upscaling not supported")
}

// Each frame:
scaler.colorTexture = colorTexture           // Low-res rendered frame
scaler.depthTexture = depthTexture           // Low-res depth
scaler.motionTexture = motionVectorTexture   // Screen-space motion vectors
scaler.outputTexture = outputTexture         // High-res output
scaler.jitterOffsetX = jitterX               // Sub-pixel jitter used during rendering
scaler.jitterOffsetY = jitterY
scaler.reset = false                         // true on scene change/cut

scaler.encode(commandBuffer: commandBuffer)
```

### Spatial Upscaling (Simpler, Lower Quality)

Single-frame upscaling. No motion vectors needed. Faster setup.

```swift
let descriptor = MTLFXSpatialScalerDescriptor()
descriptor.inputWidth = renderWidth
descriptor.inputHeight = renderHeight
descriptor.outputWidth = displayWidth
descriptor.outputHeight = displayHeight
descriptor.colorTextureFormat = .rgba16Float
descriptor.outputTextureFormat = .rgba16Float
descriptor.colorProcessingMode = .perceptual

guard let scaler = descriptor.makeSpatialScaler(device: device) else {
    fatalError("MetalFX spatial upscaling not supported")
}

// Each frame:
scaler.colorTexture = colorTexture
scaler.outputTexture = outputTexture
scaler.encode(commandBuffer: commandBuffer)
```

### PSSR-Equivalent Pipeline

PS5 uses PSSR (PlayStation Spectral Super Resolution). The Apple equivalent:

1. Render at 50-67% resolution with jittered projection
2. Output motion vectors alongside color and depth
3. MetalFX temporal upscale to native resolution
4. Optional: custom sharpening pass (CAS or RCAS)

```
Render (720p) -> MetalFX Temporal (1440p) -> Sharpen (CAS) -> Display
```

---

## Screen-Space Reflections (SSR)

Ray march in screen space against the depth buffer to find reflected geometry.

### Algorithm

1. For each pixel, compute reflection ray from view direction and surface normal
2. March along the ray in screen space, sampling the depth buffer
3. When the ray goes behind geometry (depth test passes), refine intersection
4. Sample the color buffer at the hit point
5. Fade at screen edges and missing data (fall back to environment map)

### Metal Compute Shader

```metal
kernel void ssrTrace(
    texture2d<float, access::read> colorBuffer [[texture(0)]],
    texture2d<float, access::read> depthBuffer [[texture(1)]],
    texture2d<float, access::read> normalBuffer [[texture(2)]],
    texture2d<float, access::write> reflectionBuffer [[texture(3)]],
    constant SSRParams &params [[buffer(0)]],
    uint2 gid [[thread_position_in_grid]]
) {
    float2 texSize = float2(colorBuffer.get_width(), colorBuffer.get_height());
    float2 uv = float2(gid) / texSize;

    float depth = depthBuffer.read(gid).r;
    if (depth >= 1.0) { reflectionBuffer.write(float4(0), gid); return; }

    float3 normal = normalBuffer.read(gid).xyz * 2.0 - 1.0;
    float3 viewPos = reconstructViewPos(uv, depth, params.invProjection);
    float3 viewDir = normalize(viewPos);
    float3 reflectDir = reflect(viewDir, normal);

    // Ray march in screen space
    float3 rayOrigin = viewPos;
    float stepSize = params.stepSize;
    float4 hitColor = float4(0);

    for (int i = 0; i < params.maxSteps; i++) {
        rayOrigin += reflectDir * stepSize;

        // Project to screen
        float4 projected = params.projection * float4(rayOrigin, 1.0);
        float2 sampleUV = projected.xy / projected.w * 0.5 + 0.5;
        sampleUV.y = 1.0 - sampleUV.y;

        // Bounds check
        if (sampleUV.x < 0 || sampleUV.x > 1 || sampleUV.y < 0 || sampleUV.y > 1) break;

        uint2 samplePos = uint2(sampleUV * texSize);
        float sampleDepth = depthBuffer.read(samplePos).r;
        float rayDepth = projected.z / projected.w;

        if (rayDepth > sampleDepth && rayDepth - sampleDepth < params.thickness) {
            hitColor = colorBuffer.read(samplePos);
            // Edge fade
            float edgeFade = 1.0 - max(
                abs(sampleUV.x - 0.5) * 2.0,
                abs(sampleUV.y - 0.5) * 2.0
            );
            hitColor *= saturate(edgeFade * 4.0);
            break;
        }

        // Hierarchical step size (accelerate in empty space)
        stepSize *= 1.2;
    }

    reflectionBuffer.write(hitColor, gid);
}
```

### Hierarchical Tracing (Performance Optimization)

For production SSR, use Hi-Z (hierarchical Z-buffer):

1. Build mipmap chain of depth buffer
2. Start tracing at coarse mip level (large steps)
3. When potential intersection found, drop to finer mip (smaller steps)
4. Repeat until pixel-level precision or miss

This reduces average step count from 64 to ~12 steps.

---

## Mesh Shaders (Metal 3, M3+)

Replace the traditional vertex processing pipeline with two programmable stages:

- **Object Shader:** Per-meshlet processing (culling, LOD selection)
- **Mesh Shader:** Output final vertices and primitives

### Why Mesh Shaders?

- GPU-driven culling (no CPU drawcall overhead)
- Meshlet-level frustum/occlusion culling
- Dynamic LOD without CPU intervention
- Procedural geometry generation on GPU
- Amplification (one object shader can spawn many mesh shaders)

### Metal 3 Implementation

```metal
// Object shader: per-meshlet culling
[[object, max_total_threads_per_threadgroup(32)]]
void objectShader(
    object_data MeshletPayload *payload [[payload]],
    constant Meshlet *meshlets [[buffer(0)]],
    constant CullParams &cull [[buffer(1)]],
    uint meshletIndex [[thread_position_in_grid]],
    mesh_grid_properties meshGridProps
) {
    Meshlet meshlet = meshlets[meshletIndex];

    // Frustum cull this meshlet
    bool visible = frustumCull(meshlet.boundingSphere, cull.viewProjection);

    if (visible) {
        payload[meshletIndex].meshletIndex = meshletIndex;
        meshGridProps.set_threadgroups_per_grid(uint3(1, 1, 1));
    }
}

// Mesh shader: output vertices and triangles
using MeshType = metal::mesh<VertexOut, void, 64, 126, metal::topology::triangle>;

[[mesh, max_total_threads_per_threadgroup(64)]]
void meshShader(
    MeshType output,
    object_data const MeshletPayload *payload [[payload]],
    constant Vertex *vertices [[buffer(0)]],
    constant uint *indices [[buffer(1)]],
    uint tid [[thread_index_in_threadgroup]]
) {
    uint meshletIndex = payload->meshletIndex;
    // Fetch vertex data, write to output mesh
    // Set triangle indices
    output.set_primitive_count(triangleCount);
}
```

### Meshlet Preparation (CPU Side)

```swift
// Divide mesh into meshlets (groups of ~64 vertices, ~126 triangles)
struct Meshlet {
    var vertexOffset: UInt32
    var vertexCount: UInt32
    var triangleOffset: UInt32
    var triangleCount: UInt32
    var boundingSphere: SIMD4<Float>  // xyz = center, w = radius
}

// Use meshoptimizer or Metal's mesh shader sample code for meshlet building
```

---

## Variable Rate Shading (VRS) — Metal 3, M3+

Render different screen regions at different shading rates. Critical for performance optimization.

### Use Cases

- **Foveated rendering** (visionOS): Full rate at gaze point, reduced at periphery
- **Motion blur regions:** Reduce rate where heavy blur is applied
- **Background/sky:** Lower rate for distant, low-detail areas
- **Performance headroom:** Maintain framerate by reducing non-critical areas

### Metal 3 Per-Tile Rasterization Rate

```swift
// Create rasterization rate map
let rateMapDescriptor = MTLRasterizationRateMapDescriptor(screenSize: MTLSize(width: 2560, height: 1440, depth: 1))

// Define rate layers
let layerDescriptor = MTLRasterizationRateLayerDescriptor(sampleCount: MTLSize(width: 16, height: 16, depth: 1))

// Set per-tile rates (0.0 = lowest, 1.0 = full rate)
for y in 0..<16 {
    for x in 0..<16 {
        let distFromCenter = sqrt(pow(Float(x) - 8, 2) + pow(Float(y) - 8, 2))
        let rate: Float = distFromCenter < 4 ? 1.0 : (distFromCenter < 8 ? 0.5 : 0.25)
        layerDescriptor.setSampleCount(MTLSize(width: Int(rate * 4), height: Int(rate * 4), depth: 1), at: MTLSamplePosition(x: x, y: y))
    }
}

rateMapDescriptor.setLayer(layerDescriptor, at: 0)
let rateMap = device.makeRasterizationRateMap(descriptor: rateMapDescriptor)!

// Apply to render pass
renderPassDescriptor.rasterizationRateMap = rateMap
```

---

## Ray Tracing (Metal 3, M1+ basic)

### Acceleration Structures

```swift
// Bottom-Level Acceleration Structure (BLAS) — per-mesh geometry
let geometryDescriptor = MTLAccelerationStructureTriangleGeometryDescriptor()
geometryDescriptor.vertexBuffer = vertexBuffer
geometryDescriptor.vertexStride = MemoryLayout<SIMD3<Float>>.stride
geometryDescriptor.indexBuffer = indexBuffer
geometryDescriptor.indexType = .uint32
geometryDescriptor.triangleCount = triangleCount

let blasDescriptor = MTLPrimitiveAccelerationStructureDescriptor()
blasDescriptor.geometryDescriptors = [geometryDescriptor]

let blas = device.makeAccelerationStructure(descriptor: blasDescriptor)!

// Top-Level Acceleration Structure (TLAS) — scene instances
let instanceDescriptor = MTLAccelerationStructureInstanceDescriptor()
instanceDescriptor.accelerationStructureIndex = 0
instanceDescriptor.transformationMatrix = /* 4x3 transform */

let tlasDescriptor = MTLInstanceAccelerationStructureDescriptor()
tlasDescriptor.instancedAccelerationStructures = [blas]
tlasDescriptor.instanceCount = instanceCount
tlasDescriptor.instanceDescriptorBuffer = instanceBuffer

let tlas = device.makeAccelerationStructure(descriptor: tlasDescriptor)!
```

### Ray Tracing in Compute Shader

```metal
kernel void rayTraceReflections(
    instance_acceleration_structure tlas [[buffer(0)]],
    texture2d<float, access::read> normalBuffer [[texture(0)]],
    texture2d<float, access::read> depthBuffer [[texture(1)]],
    texture2d<float, access::write> reflectionBuffer [[texture(2)]],
    constant CameraParams &camera [[buffer(1)]],
    uint2 gid [[thread_position_in_grid]]
) {
    float2 uv = float2(gid) / float2(reflectionBuffer.get_width(), reflectionBuffer.get_height());
    float3 worldPos = reconstructWorldPos(uv, depthBuffer.read(gid).r, camera);
    float3 normal = normalBuffer.read(gid).xyz * 2.0 - 1.0;
    float3 viewDir = normalize(worldPos - camera.position);
    float3 reflectDir = reflect(viewDir, normal);

    // Create ray
    ray r;
    r.origin = worldPos + normal * 0.001;  // bias to avoid self-intersection
    r.direction = reflectDir;
    r.min_distance = 0.001;
    r.max_distance = 100.0;

    // Trace
    intersector<triangle_data> intersector;
    auto intersection = intersector.intersect(r, tlas);

    if (intersection.type == intersection_type::triangle) {
        // Hit: read material, compute lighting
        float4 hitColor = /* shade hit point */;
        reflectionBuffer.write(hitColor, gid);
    } else {
        // Miss: sample environment map
        reflectionBuffer.write(sampleEnvironment(reflectDir), gid);
    }
}
```

### MPSRayIntersector (Simpler API)

For less complex use cases, MPS provides a higher-level ray tracing API:

```swift
import MetalPerformanceShaders

let intersector = MPSRayIntersector(device: device)
intersector.rayDataType = .originMinDistanceDirectionMaxDistance
intersector.intersectionDataType = .distancePrimitiveIndexCoordinates

let accelerationStructure = MPSTriangleAccelerationStructure(device: device)
accelerationStructure.vertexBuffer = vertexBuffer
accelerationStructure.triangleCount = triangleCount
accelerationStructure.rebuild()

intersector.encode(
    commandBuffer: commandBuffer,
    intersectionType: .nearest,
    rayBuffer: rayBuffer,
    rayBufferOffset: 0,
    intersectionBuffer: intersectionBuffer,
    intersectionBufferOffset: 0,
    rayCount: rayCount,
    accelerationStructure: accelerationStructure
)
```

---

## Performance Optimization Pipeline

### Recommended Order of Techniques

For a PS5-quality rendering pipeline on Apple Silicon:

```
1. Deferred or Forward+ rendering base
2. Cascaded shadow maps (3-4 cascades)
3. TAA (always-on, low cost)
4. MetalFX temporal upscaling (render at 50-67% res)
5. SSR for reflective surfaces
6. SSAO for ambient occlusion
7. Bloom post-process
8. HDR tone mapping (ACES or similar)
9. Optional: ray-traced reflections/shadows (M3+)
10. Optional: mesh shaders for GPU-driven rendering (M3+)
11. Optional: VRS for foveated/adaptive quality (M3+)
```

### Memory Bandwidth Budget

The primary constraint on Apple Silicon vs PS5:

| Chip | Bandwidth | % of PS5 | Strategy |
|------|-----------|----------|----------|
| M1 | 68 GB/s | 15% | Aggressive resolution scaling, minimal G-buffer |
| M1 Pro/Max | 200-400 GB/s | 45-89% | Standard deferred, MetalFX upscaling |
| M2 | 100 GB/s | 22% | Lean G-buffer, spatial upscaling |
| M2 Pro/Max | 200-400 GB/s | 45-89% | Full pipeline viable |
| M3 | 100 GB/s | 22% | VRS + MetalFX compensate |
| M3 Pro/Max | 150-400 GB/s | 33-89% | Near-PS5 pipeline |
| M4 Max | 546 GB/s | 122% | Exceeds PS5 bandwidth |
| PS5 | 448 GB/s | 100% | Reference |

**Key insight:** M-series Max chips match or exceed PS5 bandwidth. The gap is primarily on base M-series chips, where MetalFX upscaling and VRS are critical compensations.
