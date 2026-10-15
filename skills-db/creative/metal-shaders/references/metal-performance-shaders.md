# Metal Performance Shaders (MPS) Framework

MPS provides highly optimized, GPU-accelerated implementations of common image processing, linear algebra, ray tracing, and neural network operations. Use MPS when a standard algorithm exists; write custom shaders only for novel effects.

---

## When to Use MPS vs Custom Shaders

| Scenario | Use MPS | Use Custom |
|----------|---------|------------|
| Gaussian blur | Yes (MPSImageGaussianBlur) | Only if you need non-standard kernel |
| Edge detection | Yes (MPSImageSobel) | For novel edge algorithms |
| Histogram | Yes (MPSImageHistogram) | For non-standard binning |
| Matrix multiply | Yes (MPSMatrixMultiplication) | Never -- MPS is optimal |
| Standard CNN inference | Yes (MPSNNGraph) | Prefer Core ML for models |
| Ray-triangle intersection | Yes (MPSRayIntersector) | For custom intersection types |
| Novel visual effect | No | Yes -- full creative control |
| Custom particle physics | No | Yes -- problem-specific |

---

## Image Processing

### Gaussian Blur Pipeline

```swift
import Metal
import MetalPerformanceShaders

class BlurPipeline {
    let device: MTLDevice
    let queue: MTLCommandQueue

    init() {
        device = MTLCreateSystemDefaultDevice()!
        queue = device.makeCommandQueue()!
    }

    func blur(source: MTLTexture, sigma: Float) -> MTLTexture {
        // Create output texture matching source
        let desc = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: source.pixelFormat,
            width: source.width,
            height: source.height,
            mipmapped: false
        )
        desc.usage = [.shaderWrite, .shaderRead]
        let output = device.makeTexture(descriptor: desc)!

        // Create blur kernel
        let blur = MPSImageGaussianBlur(device: device, sigma: sigma)
        blur.edgeMode = .clamp  // or .zero

        // Encode
        let commandBuffer = queue.makeCommandBuffer()!
        blur.encode(
            commandBuffer: commandBuffer,
            sourceTexture: source,
            destinationTexture: output
        )
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()

        return output
    }

    // In-place blur (overwrites source)
    func blurInPlace(texture: inout MTLTexture, sigma: Float) {
        let blur = MPSImageGaussianBlur(device: device, sigma: sigma)
        let commandBuffer = queue.makeCommandBuffer()!

        // MPS can allocate a temporary texture internally
        var tex: MTLTexture? = texture
        blur.encode(
            commandBuffer: commandBuffer,
            inPlaceTexture: &tex!,
            fallbackCopyAllocator: nil
        )
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
        texture = tex!
    }
}
```

### Sobel Edge Detection

```swift
func edgeDetect(source: MTLTexture) -> MTLTexture {
    let desc = MTLTextureDescriptor.texture2DDescriptor(
        pixelFormat: source.pixelFormat,
        width: source.width,
        height: source.height,
        mipmapped: false
    )
    desc.usage = [.shaderWrite, .shaderRead]
    let output = device.makeTexture(descriptor: desc)!

    let sobel = MPSImageSobel(device: device)

    let commandBuffer = queue.makeCommandBuffer()!
    sobel.encode(
        commandBuffer: commandBuffer,
        sourceTexture: source,
        destinationTexture: output
    )
    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()

    return output
}
```

### Image Histogram

```swift
func computeHistogram(source: MTLTexture) -> [UInt32] {
    let histogramInfo = MPSImageHistogramInfo(
        numberOfHistogramEntries: 256,
        histogramForAlpha: false,
        minPixelValue: vector_float4(0, 0, 0, 0),
        maxPixelValue: vector_float4(1, 1, 1, 1)
    )

    let histogram = MPSImageHistogram(device: device, histogramInfo: histogramInfo)

    // Histogram output buffer
    let bufferLength = histogram.histogramSize(forSourceFormat: source.pixelFormat)
    let histogramBuffer = device.makeBuffer(length: bufferLength, options: .storageModeShared)!

    let commandBuffer = queue.makeCommandBuffer()!
    histogram.encode(
        to: commandBuffer,
        sourceTexture: source,
        histogram: histogramBuffer,
        histogramOffset: 0
    )
    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()

    // Read results (3 channels x 256 bins)
    let count = bufferLength / MemoryLayout<UInt32>.stride
    let pointer = histogramBuffer.contents().bindMemory(to: UInt32.self, capacity: count)
    return Array(UnsafeBufferPointer(start: pointer, count: count))
}
```

### Chaining MPS Operations

```swift
func processImage(source: MTLTexture) -> MTLTexture {
    let desc = MTLTextureDescriptor.texture2DDescriptor(
        pixelFormat: source.pixelFormat,
        width: source.width, height: source.height,
        mipmapped: false
    )
    desc.usage = [.shaderWrite, .shaderRead]

    let temp = device.makeTexture(descriptor: desc)!
    let output = device.makeTexture(descriptor: desc)!

    let commandBuffer = queue.makeCommandBuffer()!

    // Step 1: Blur
    let blur = MPSImageGaussianBlur(device: device, sigma: 2.0)
    blur.encode(commandBuffer: commandBuffer, sourceTexture: source, destinationTexture: temp)

    // Step 2: Sharpen (Laplacian-based unsharp mask)
    let sharpen = MPSImageLaplacian(device: device)
    sharpen.encode(commandBuffer: commandBuffer, sourceTexture: temp, destinationTexture: output)

    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()

    return output
}
```

---

## Neural Networks (Inference)

For most ML inference, prefer **Core ML** (higher-level, better tooling). Use MPS directly only when you need fine-grained GPU pipeline control or are integrating with an existing Metal render pipeline.

```swift
import MetalPerformanceShaders

// Basic convolution layer
func createConvLayer(device: MTLDevice) -> MPSCNNConvolution {
    let desc = MPSCNNConvolutionDescriptor(
        kernelWidth: 3, kernelHeight: 3,
        inputFeatureChannels: 3, outputFeatureChannels: 16
    )
    desc.strideInPixelsX = 1
    desc.strideInPixelsY = 1

    // Weights data source
    let dataSource = MyWeightsDataSource(desc: desc)

    let conv = MPSCNNConvolution(device: device, weights: dataSource)
    conv.edgeMode = .zero
    return conv
}

// Simple inference graph
func buildGraph(device: MTLDevice) -> MPSNNGraph {
    // Input image node
    let inputImage = MPSNNImageNode(handle: nil)

    // Conv -> ReLU -> Pool
    let conv = MPSCNNConvolutionNode(source: inputImage, weights: myWeights)
    let relu = MPSCNNNeuronReLUNode(source: conv.resultImage)
    let pool = MPSCNNPoolingMaxNode(source: relu.resultImage, filterSize: 2)

    // Build graph
    guard let graph = MPSNNGraph(
        device: device,
        resultImage: pool.resultImage,
        resultImageIsNeeded: true
    ) else { fatalError("Failed to create graph") }

    return graph
}
```

---

## Ray Tracing

MPS provides hardware-accelerated ray-triangle intersection testing via acceleration structures.

### Basic Ray Tracing Setup

```swift
import MetalPerformanceShaders

class RayTracer {
    let device: MTLDevice
    let queue: MTLCommandQueue
    var accelerationStructure: MPSTriangleAccelerationStructure!
    var intersector: MPSRayIntersector!

    init(device: MTLDevice) {
        self.device = device
        self.queue = device.makeCommandQueue()!
    }

    func buildAccelerationStructure(
        vertices: MTLBuffer,
        vertexCount: Int,
        indices: MTLBuffer?,
        indexCount: Int
    ) {
        accelerationStructure = MPSTriangleAccelerationStructure(device: device)
        accelerationStructure.vertexBuffer = vertices
        accelerationStructure.vertexStride = MemoryLayout<SIMD3<Float>>.stride
        accelerationStructure.triangleCount = vertexCount / 3

        if let indices = indices {
            accelerationStructure.indexBuffer = indices
            accelerationStructure.indexType = .uint32
            accelerationStructure.triangleCount = indexCount / 3
        }

        // Build (compute-intensive, do once or when geometry changes)
        accelerationStructure.rebuild()
    }

    func setupIntersector() {
        intersector = MPSRayIntersector(device: device)
        intersector.rayDataType = .originMinDistanceDirectionMaxDistance
        intersector.rayStride = MemoryLayout<MPSRayOriginMinDistanceDirectionMaxDistance>.stride
        intersector.intersectionDataType = .distancePrimitiveIndexCoordinates
    }

    func trace(
        rays: MTLBuffer,
        rayCount: Int,
        intersections: MTLBuffer
    ) {
        let commandBuffer = queue.makeCommandBuffer()!

        intersector.encode(
            commandBuffer: commandBuffer,
            intersectionType: .nearest,
            rayBuffer: rays,
            rayBufferOffset: 0,
            intersectionBuffer: intersections,
            intersectionBufferOffset: 0,
            rayCount: rayCount,
            accelerationStructure: accelerationStructure
        )

        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
    }
}
```

### Ray Data Structures

```swift
// Ray struct (matches MPSRayOriginMinDistanceDirectionMaxDistance)
struct Ray {
    var origin: SIMD3<Float>
    var minDistance: Float
    var direction: SIMD3<Float>
    var maxDistance: Float
}

// Intersection result (matches MPSIntersectionDistancePrimitiveIndexCoordinates)
struct Intersection {
    var distance: Float
    var primitiveIndex: UInt32
    var coordinates: SIMD2<Float>  // barycentric
}
```

### Using Intersection Results in a Shader

```metal
#include <metal_stdlib>
#include <MetalPerformanceShaders/MetalPerformanceShaders.h>
using namespace metal;

struct Intersection {
    float distance;
    uint primitiveIndex;
    float2 coordinates;  // barycentric u, v
};

kernel void shade_intersections(
    device Intersection* intersections [[ buffer(0) ]],
    device float3* vertices [[ buffer(1) ]],
    device float3* normals [[ buffer(2) ]],
    texture2d<half, access::write> output [[ texture(0) ]],
    uint2 gid [[ thread_position_in_grid ]]
) {
    uint idx = gid.y * output.get_width() + gid.x;
    Intersection hit = intersections[idx];

    if (hit.distance < 0.0) {
        // Miss -- sky color
        output.write(half4(0.4h, 0.6h, 0.9h, 1.0h), gid);
        return;
    }

    // Interpolate normal using barycentric coordinates
    uint triIdx = hit.primitiveIndex * 3;
    float3 n0 = normals[triIdx];
    float3 n1 = normals[triIdx + 1];
    float3 n2 = normals[triIdx + 2];
    float u = hit.coordinates.x;
    float v = hit.coordinates.y;
    float3 normal = normalize(n0 * (1.0 - u - v) + n1 * u + n2 * v);

    // Simple diffuse lighting
    float3 lightDir = normalize(float3(1, 1, -1));
    float diff = max(dot(normal, lightDir), 0.0);
    half3 color = half3(0.8h, 0.7h, 0.6h) * half(diff) + half3(0.1h);

    output.write(half4(color, 1.0h), gid);
}
```

---

## Linear Algebra

### Matrix Operations

```swift
func matrixMultiply(
    A: MTLBuffer, rowsA: Int, colsA: Int,
    B: MTLBuffer, rowsB: Int, colsB: Int
) -> MTLBuffer {
    let matA = MPSMatrix(
        buffer: A,
        descriptor: MPSMatrixDescriptor(
            rows: rowsA, columns: colsA,
            rowBytes: colsA * MemoryLayout<Float>.stride,
            dataType: .float32
        )
    )

    let matB = MPSMatrix(
        buffer: B,
        descriptor: MPSMatrixDescriptor(
            rows: rowsB, columns: colsB,
            rowBytes: colsB * MemoryLayout<Float>.stride,
            dataType: .float32
        )
    )

    let resultBuffer = device.makeBuffer(
        length: rowsA * colsB * MemoryLayout<Float>.stride,
        options: .storageModeShared
    )!

    let matC = MPSMatrix(
        buffer: resultBuffer,
        descriptor: MPSMatrixDescriptor(
            rows: rowsA, columns: colsB,
            rowBytes: colsB * MemoryLayout<Float>.stride,
            dataType: .float32
        )
    )

    let multiply = MPSMatrixMultiplication(
        device: device,
        transposeLeft: false,
        transposeRight: false,
        resultRows: rowsA,
        resultColumns: colsB,
        interiorColumns: colsA,
        alpha: 1.0,
        beta: 0.0
    )

    let commandBuffer = queue.makeCommandBuffer()!
    multiply.encode(commandBuffer: commandBuffer, leftMatrix: matA, rightMatrix: matB, resultMatrix: matC)
    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()

    return resultBuffer
}
```

---

## Performance Notes

1. **MPS kernels are fused** -- chaining multiple MPS operations in one command buffer lets the driver optimize memory traffic
2. **Temporary images** -- use `MPSTemporaryImage` for intermediate results; they are allocated from a pool and recycled automatically
3. **Reuse kernel objects** -- creating MPS kernels is expensive; create once and reuse across frames
4. **Async encoding** -- encode on background threads, commit from any thread
5. **Profile with Instruments** -- Metal System Trace shows MPS kernel execution alongside your custom shaders

```swift
// Using temporary images for intermediate results
let commandBuffer = queue.makeCommandBuffer()!

let tempDesc = MPSImageDescriptor(
    channelFormat: .float16,
    width: source.width,
    height: source.height,
    featureChannels: 4
)
let tempImage = MPSTemporaryImage(commandBuffer: commandBuffer, imageDescriptor: tempDesc)

blur.encode(commandBuffer: commandBuffer, sourceTexture: source, destinationTexture: tempImage.texture)
sharpen.encode(commandBuffer: commandBuffer, sourceTexture: tempImage.texture, destinationTexture: output)

// tempImage is automatically recycled after command buffer completes
commandBuffer.commit()
```
