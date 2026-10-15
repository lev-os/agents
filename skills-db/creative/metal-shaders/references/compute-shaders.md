# Compute Shaders in Metal

## Architecture {#architecture}

Compute shaders (kernels) execute arbitrary parallel work on the GPU without the vertex/fragment pipeline. Work is dispatched as a grid of threads organized into threadgroups.

```
Dispatch Grid (total threads)
├── Threadgroup 0
│   ├── SIMD Group 0 (32 threads execute in lockstep)
│   ├── SIMD Group 1
│   └── ...
├── Threadgroup 1
│   └── ...
└── ...
```

### Thread Indexing

```metal
kernel void my_kernel(
    uint2 gid [[ thread_position_in_grid ]],          // Global ID
    uint2 lid [[ thread_position_in_threadgroup ]],    // Local ID within group
    uint2 tgid [[ threadgroup_position_in_grid ]],     // Which threadgroup
    uint2 tgSize [[ threads_per_threadgroup ]],        // Threadgroup dimensions
    uint simd_lane [[ thread_index_in_simdgroup ]],    // Lane in SIMD (0-31)
    uint simd_id [[ simdgroup_index_in_threadgroup ]]  // Which SIMD group
) {
    // gid = tgid * tgSize + lid
}
```

### Minimal Compute Pipeline (Swift Side)

```swift
import Metal

// 1. Create device and command queue (once)
guard let device = MTLCreateSystemDefaultDevice(),
      let queue = device.makeCommandQueue() else { fatalError() }

// 2. Load shader library and create pipeline
let library = device.makeDefaultLibrary()!
let function = library.makeFunction(name: "my_kernel")!
let pipeline = try device.makeComputePipelineState(function: function)

// 3. Dispatch
let commandBuffer = queue.makeCommandBuffer()!
let encoder = commandBuffer.makeComputeCommandEncoder()!
encoder.setComputePipelineState(pipeline)

// Set buffers
encoder.setBuffer(inputBuffer, offset: 0, index: 0)
encoder.setBuffer(outputBuffer, offset: 0, index: 1)

// Calculate threadgroup size
let w = pipeline.threadExecutionWidth              // typically 32
let h = pipeline.maxTotalThreadsPerThreadgroup / w // typically 32 (1024/32)
let threadsPerGroup = MTLSize(width: w, height: h, depth: 1)
let threadsPerGrid = MTLSize(width: textureWidth, height: textureHeight, depth: 1)

// dispatchThreads handles non-uniform grids (no manual bounds check needed)
encoder.dispatchThreads(threadsPerGrid, threadsPerThreadgroup: threadsPerGroup)
encoder.endEncoding()
commandBuffer.commit()
```

### Threadgroup Shared Memory

```metal
kernel void reduce_sum(
    device float* input [[ buffer(0) ]],
    device float* output [[ buffer(1) ]],
    uint gid [[ thread_position_in_grid ]],
    uint lid [[ thread_position_in_threadgroup ]],
    uint tgSize [[ threads_per_threadgroup ]]
) {
    // Declare shared memory
    threadgroup float shared[256];

    // Load into shared memory
    shared[lid] = input[gid];
    threadgroup_barrier(mem_flags::mem_threadgroup);

    // Parallel reduction
    for (uint stride = tgSize / 2; stride > 0; stride >>= 1) {
        if (lid < stride) {
            shared[lid] += shared[lid + stride];
        }
        threadgroup_barrier(mem_flags::mem_threadgroup);
    }

    // Thread 0 writes result
    if (lid == 0) {
        output[tgSize] = shared[0]; // or atomic_fetch_add
    }
}
```

---

## Particle Simulation {#particles}

### Particle Data Structure

```metal
#include <metal_stdlib>
using namespace metal;

struct Particle {
    float3 position;
    float3 velocity;
    float4 color;
    float life;        // 0.0 = dead, 1.0 = just spawned
    float size;
};
```

### Position/Velocity Update Kernel

```metal
kernel void update_particles(
    device Particle* particles [[ buffer(0) ]],
    constant float &deltaTime [[ buffer(1) ]],
    constant float3 &gravity [[ buffer(2) ]],
    constant uint &particleCount [[ buffer(3) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= particleCount) return;

    Particle p = particles[gid];

    // Skip dead particles
    if (p.life <= 0.0) return;

    // Verlet-style integration
    float dt = deltaTime;
    p.velocity += gravity * dt;

    // Drag
    p.velocity *= 0.99;

    // Integrate position
    p.position += p.velocity * dt;

    // Age
    p.life -= dt * 0.5;

    // Fade color with life
    p.color.a = p.life;
    p.size = mix(0.1, p.size, p.life);

    particles[gid] = p;
}
```

### Force Accumulation Kernel

```metal
struct ForceField {
    float3 position;
    float strength;
    float radius;
    uint type;  // 0 = attract, 1 = repel, 2 = vortex
};

kernel void apply_forces(
    device Particle* particles [[ buffer(0) ]],
    constant ForceField* fields [[ buffer(1) ]],
    constant uint &fieldCount [[ buffer(2) ]],
    constant uint &particleCount [[ buffer(3) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= particleCount) return;

    Particle p = particles[gid];
    if (p.life <= 0.0) return;

    float3 totalForce = float3(0.0);

    for (uint i = 0; i < fieldCount; i++) {
        ForceField f = fields[i];
        float3 dir = f.position - p.position;
        float dist = length(dir);

        if (dist > f.radius || dist < 0.01) continue;

        float falloff = 1.0 - (dist / f.radius);
        falloff = falloff * falloff; // quadratic falloff

        switch (f.type) {
            case 0: // attract
                totalForce += normalize(dir) * f.strength * falloff;
                break;
            case 1: // repel
                totalForce -= normalize(dir) * f.strength * falloff;
                break;
            case 2: // vortex
                float3 tangent = normalize(cross(dir, float3(0, 1, 0)));
                totalForce += tangent * f.strength * falloff;
                break;
        }
    }

    p.velocity += totalForce;
    particles[gid] = p;
}
```

### Spatial Hashing for Collision Detection

```metal
constant uint HASH_TABLE_SIZE = 65536;

uint hash_cell(int3 cell) {
    // Spatial hash: combine cell coords
    return uint((cell.x * 73856093) ^ (cell.y * 19349663) ^ (cell.z * 83492791))
           % HASH_TABLE_SIZE;
}

kernel void build_spatial_hash(
    device Particle* particles [[ buffer(0) ]],
    device atomic_uint* hashTable [[ buffer(1) ]],
    device uint* particleIndices [[ buffer(2) ]],
    constant float &cellSize [[ buffer(3) ]],
    constant uint &particleCount [[ buffer(4) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= particleCount) return;

    Particle p = particles[gid];
    int3 cell = int3(floor(p.position / cellSize));
    uint bucket = hash_cell(cell);

    // Atomic insert into bucket (linked list or counter approach)
    uint index = atomic_fetch_add_explicit(&hashTable[bucket], 1, memory_order_relaxed);
    particleIndices[bucket * 64 + min(index, 63u)] = gid;
}
```

---

## Physics Simulation {#physics}

### Verlet Integration

```metal
struct VerletPoint {
    float3 position;
    float3 previousPosition;
    float3 acceleration;
    float mass;
    bool pinned;
};

kernel void verlet_integrate(
    device VerletPoint* points [[ buffer(0) ]],
    constant float &dt [[ buffer(1) ]],
    constant float &damping [[ buffer(2) ]],
    constant uint &count [[ buffer(3) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= count) return;

    VerletPoint p = points[gid];
    if (p.pinned) return;

    float3 velocity = (p.position - p.previousPosition) * damping;
    p.previousPosition = p.position;
    p.position += velocity + p.acceleration * dt * dt;
    p.acceleration = float3(0.0);

    points[gid] = p;
}
```

### Constraint Solving (Cloth Simulation)

```metal
struct Constraint {
    uint indexA;
    uint indexB;
    float restLength;
    float stiffness;
};

kernel void solve_constraints(
    device VerletPoint* points [[ buffer(0) ]],
    constant Constraint* constraints [[ buffer(1) ]],
    constant uint &constraintCount [[ buffer(2) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= constraintCount) return;

    Constraint c = constraints[gid];
    VerletPoint a = points[c.indexA];
    VerletPoint b = points[c.indexB];

    float3 delta = b.position - a.position;
    float currentLength = length(delta);
    if (currentLength < 1e-6) return;

    float diff = (currentLength - c.restLength) / currentLength;
    float3 correction = delta * diff * c.stiffness * 0.5;

    if (!a.pinned) {
        a.position += correction;
        points[c.indexA] = a;
    }
    if (!b.pinned) {
        b.position -= correction;
        points[c.indexB] = b;
    }
}
```

**Note:** Constraint solving has data races when multiple constraints share points. Standard approaches:
1. **Color-based batching** -- group constraints so no two in the same batch share a point, dispatch batches sequentially
2. **Jacobi iteration** -- each constraint writes to a separate correction buffer, then apply all corrections in a second pass
3. **Atomic operations** -- use `atomic_fetch_add` on position components (slower but simpler)

---

## Image Processing {#image-processing}

### Convolution Kernel

```metal
kernel void convolution3x3(
    texture2d<half, access::read> input [[ texture(0) ]],
    texture2d<half, access::write> output [[ texture(1) ]],
    constant float* kernelWeights [[ buffer(0) ]],  // 9 floats
    uint2 gid [[ thread_position_in_grid ]]
) {
    if (gid.x >= input.get_width() || gid.y >= input.get_height()) return;

    half4 sum = half4(0.0h);
    int k = 0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            uint2 coord = uint2(
                clamp(int(gid.x) + x, 0, int(input.get_width()) - 1),
                clamp(int(gid.y) + y, 0, int(input.get_height()) - 1)
            );
            sum += input.read(coord) * half(kernelWeights[k]);
            k++;
        }
    }
    output.write(sum, gid);
}

// Sobel edge detection weights:
// Gx: [-1,0,1, -2,0,2, -1,0,1]
// Gy: [-1,-2,-1, 0,0,0, 1,2,1]
```

### Histogram Computation

```metal
kernel void compute_histogram(
    texture2d<half, access::read> input [[ texture(0) ]],
    device atomic_uint* histogram [[ buffer(0) ]],  // 256 bins
    uint2 gid [[ thread_position_in_grid ]]
) {
    if (gid.x >= input.get_width() || gid.y >= input.get_height()) return;

    half4 color = input.read(gid);
    half lum = dot(color.rgb, half3(0.2126h, 0.7152h, 0.0722h));
    uint bin = min(uint(lum * 255.0h), 255u);
    atomic_fetch_add_explicit(&histogram[bin], 1, memory_order_relaxed);
}
```

---

## GPU-Driven Rendering {#gpu-driven}

### Indirect Draw Arguments

```metal
struct MTLDrawIndexedPrimitivesIndirectArguments {
    uint indexCount;
    uint instanceCount;
    uint indexStart;
    int baseVertex;
    uint baseInstance;
};

// Visibility/culling kernel writes draw args
kernel void cull_meshlets(
    constant float4x4 &viewProj [[ buffer(0) ]],
    constant BoundingSphere* bounds [[ buffer(1) ]],
    device MTLDrawIndexedPrimitivesIndirectArguments* drawArgs [[ buffer(2) ]],
    device atomic_uint &drawCount [[ buffer(3) ]],
    constant uint &meshletCount [[ buffer(4) ]],
    uint gid [[ thread_position_in_grid ]]
) {
    if (gid >= meshletCount) return;

    BoundingSphere b = bounds[gid];

    // Frustum cull (simplified -- check all 6 planes in production)
    float4 clipPos = viewProj * float4(b.center, 1.0);
    float radius = b.radius;

    // Check if sphere is outside any clip plane
    bool visible = true;
    visible = visible && (clipPos.x + radius * abs(viewProj[0][0]) > -clipPos.w);
    visible = visible && (clipPos.x - radius * abs(viewProj[0][0]) < clipPos.w);
    visible = visible && (clipPos.y + radius * abs(viewProj[1][1]) > -clipPos.w);
    visible = visible && (clipPos.y - radius * abs(viewProj[1][1]) < clipPos.w);
    visible = visible && (clipPos.z + radius > 0.0);  // near plane

    if (visible) {
        uint slot = atomic_fetch_add_explicit(&drawCount, 1, memory_order_relaxed);
        drawArgs[slot].indexCount = bounds[gid].indexCount;
        drawArgs[slot].instanceCount = 1;
        drawArgs[slot].indexStart = bounds[gid].indexStart;
        drawArgs[slot].baseVertex = bounds[gid].baseVertex;
        drawArgs[slot].baseInstance = gid;
    }
}
```

---

## Performance {#performance}

### Threadgroup Sizing Rules

```
Rule 1: threads_per_group MUST be <= pipeline.maxTotalThreadsPerThreadgroup (usually 1024)
Rule 2: threads_per_group SHOULD be multiple of pipeline.threadExecutionWidth (usually 32)
Rule 3: Prefer square-ish groups for 2D work: 16x16=256 or 32x8=256
Rule 4: 1D work: use threadExecutionWidth (32) or multiples up to 256
```

### Memory Access Patterns

```
GOOD (coalesced):  thread[i] reads buffer[i]      -- adjacent threads, adjacent memory
BAD  (strided):    thread[i] reads buffer[i * N]   -- adjacent threads, scattered memory
GOOD (shared):     load into threadgroup[], barrier, read from threadgroup[]
BAD  (global R/W): multiple passes reading same global buffer
```

### Simdgroup Operations (Apple GPU Feature)

```metal
// Simdgroup shuffle -- read value from another lane without shared memory
float val = simd_shuffle(myValue, otherLaneId);

// Simdgroup reductions
float sum = simd_sum(myValue);
float maxVal = simd_max(myValue);
float minVal = simd_min(myValue);

// Simdgroup prefix sum (scan)
float prefixSum = simd_prefix_exclusive_sum(myValue);

// Simdgroup ballot
bool active = (myValue > threshold);
simd_vote::vote_t vote = simd_ballot(active);
```

### Occupancy Checklist

1. **Reduce register pressure** -- fewer variables per thread = more threadgroups in flight
2. **Minimize shared memory** -- less threadgroup memory = more concurrent threadgroups
3. **Balance ALU vs memory** -- Apple GPUs are TBDR; prefer compute over bandwidth
4. **Use `half` types** -- doubles the effective register count for color math
5. **Profile with Xcode GPU Profiler** -- check shader timeline for stalls

### Avoid Bank Conflicts

```metal
// BAD: all threads in SIMD group access same bank
threadgroup float data[256];
data[lid * 32];  // stride of 32 = same bank

// GOOD: pad the array to avoid conflicts
threadgroup float data[256 + 8];  // +8 padding breaks bank alignment
data[lid * 32 + lid / 4];        // or offset access pattern
```
