# Bloom & Post-Processing

## Overview

Bloom simulates the way bright light bleeds into surrounding areas in a camera or the human eye. The standard pipeline: render bright areas to a separate target, blur them, and composite back additively.

---

## HDR Bloom Pipeline

### Pipeline Stages

```
Scene Render (HDR float16 target)
    |
    v
1. Threshold Extraction
    - Extract pixels with luminance > threshold (typically 1.0 for HDR)
    - Apply soft knee for smooth transition
    - Output: bright-pass texture (half or quarter resolution)
    |
    v
2. Multi-Pass Gaussian Blur
    - Separable: horizontal pass, then vertical pass (2 passes = 1 level)
    - Downscale for each level (half resolution per level)
    - 3-5 levels for wide bloom, 1-2 for tight glow
    - Ping-pong between two textures
    |
    v
3. Upsample & Composite
    - Upsample each blur level back to full resolution
    - Add all levels together (weighted)
    - Additively composite onto original scene
    - Output: final frame
```

### Stage 1: Threshold Extraction

```metal
#include <metal_stdlib>
using namespace metal;

/// Extract bright pixels above threshold
/// Soft knee creates a gradual transition instead of hard cutoff
[[stitchable]]
half4 bloomThreshold(
    float2 position,
    half4 color,
    float threshold,
    float softKnee
) {
    // Luminance (Rec. 709)
    float luma = dot(float3(color.rgb), float3(0.2126, 0.7152, 0.0722));

    // Soft knee: smoothstep transition around threshold
    float knee = threshold * softKnee;
    float soft = luma - threshold + knee;
    soft = clamp(soft, 0.0, 2.0 * knee);
    soft = soft * soft / (4.0 * knee + 0.0001);

    float contribution = max(soft, luma - threshold);
    contribution = max(0.0, contribution) / max(luma, 0.0001);

    return color * half(contribution);
}
```

### Stage 2: Separable Gaussian Blur

```metal
/// Horizontal Gaussian blur (separable)
/// Call twice: once for horizontal, once for vertical (swap direction)
[[stitchable]]
half4 gaussianBlurH(
    float2 position,
    SwiftUI::Layer layer,
    float2 texelSize,  // 1.0 / textureSize
    float radius
) {
    // 9-tap Gaussian weights (sigma ~= radius/3)
    constant float weights[9] = {
        0.0009, 0.0111, 0.0652, 0.2417, 0.3822,
        // Note: only need 5 unique weights (symmetric)
        // but listed as 9 for clarity
        0.2417, 0.0652, 0.0111, 0.0009
    };

    // Actually use a simpler 5-tap for real-time
    constant float w5[5] = { 0.0545, 0.2442, 0.4026, 0.2442, 0.0545 };

    half4 result = half4(0);

    for (int i = -2; i <= 2; i++) {
        float2 offset = float2(float(i) * texelSize.x * radius, 0.0);
        result += layer.sample(position + offset) * half(w5[i + 2]);
    }

    return result;
}

/// Vertical Gaussian blur (separable)
[[stitchable]]
half4 gaussianBlurV(
    float2 position,
    SwiftUI::Layer layer,
    float2 texelSize,
    float radius
) {
    constant float w5[5] = { 0.0545, 0.2442, 0.4026, 0.2442, 0.0545 };

    half4 result = half4(0);

    for (int i = -2; i <= 2; i++) {
        float2 offset = float2(0.0, float(i) * texelSize.y * radius);
        result += layer.sample(position + offset) * half(w5[i + 2]);
    }

    return result;
}
```

### Stage 3: Additive Composite

```metal
/// Composite bloom over original
[[stitchable]]
half4 bloomComposite(
    float2 position,
    half4 originalColor,
    SwiftUI::Layer bloomLayer,
    float intensity
) {
    half4 bloom = bloomLayer.sample(position);
    return originalColor + bloom * half(intensity);
}
```

---

## Multi-Pass Blur with Ping-Pong Buffers

For wide, cinematic bloom you need multiple blur passes at decreasing resolutions.

### Metal Render Pass Setup (Swift)

```swift
class BloomRenderer {
    let device: MTLDevice
    let blurHPipeline: MTLComputePipelineState
    let blurVPipeline: MTLComputePipelineState
    let thresholdPipeline: MTLComputePipelineState

    // Ping-pong textures at each resolution level
    var blurTextures: [(MTLTexture, MTLTexture)] = []
    let levels = 4

    func setupTextures(width: Int, height: Int) {
        blurTextures.removeAll()
        var w = width / 2
        var h = height / 2

        for _ in 0..<levels {
            let desc = MTLTextureDescriptor.texture2DDescriptor(
                pixelFormat: .rgba16Float,
                width: max(1, w),
                height: max(1, h),
                mipmapped: false
            )
            desc.usage = [.shaderRead, .shaderWrite]
            desc.storageMode = .private

            let texA = device.makeTexture(descriptor: desc)!
            let texB = device.makeTexture(descriptor: desc)!
            blurTextures.append((texA, texB))

            w /= 2
            h /= 2
        }
    }

    func encodeBloom(
        commandBuffer: MTLCommandBuffer,
        sourceTexture: MTLTexture,
        threshold: Float = 1.0,
        intensity: Float = 0.8
    ) {
        // 1. Threshold pass (source -> level 0 texture A)
        encodeThreshold(commandBuffer: commandBuffer,
                       source: sourceTexture,
                       dest: blurTextures[0].0,
                       threshold: threshold)

        // 2. Blur each level
        for level in 0..<levels {
            let (texA, texB) = blurTextures[level]
            let input = (level == 0) ? texA : blurTextures[level].0

            // Horizontal: A -> B
            encodeBlurPass(commandBuffer: commandBuffer,
                          source: input, dest: texB,
                          horizontal: true)

            // Vertical: B -> A
            encodeBlurPass(commandBuffer: commandBuffer,
                          source: texB, dest: texA,
                          horizontal: false)

            // Downscale to next level if not last
            if level < levels - 1 {
                encodeCopy(commandBuffer: commandBuffer,
                          source: texA,
                          dest: blurTextures[level + 1].0)
            }
        }

        // 3. Upsample and accumulate (reverse order)
        for level in stride(from: levels - 1, through: 1, by: -1) {
            encodeUpsampleAdd(commandBuffer: commandBuffer,
                             source: blurTextures[level].0,
                             dest: blurTextures[level - 1].0,
                             weight: intensity / Float(levels))
        }

        // 4. Final composite: blurTextures[0].0 contains the bloom
        // Additively blend onto the original in the final render pass
    }

    // ... encode helper methods omitted for brevity
}
```

---

## SwiftUI Integration Approaches

### Approach 1: `.shadow()` Stacking (Simplest, No Metal)

Quick glow for UI elements. Not true bloom but visually similar for small objects.

```swift
struct GlowingOrb: View {
    let glowColor: Color = .cyan
    let intensity: CGFloat = 0.8

    var body: some View {
        Circle()
            .fill(glowColor)
            .frame(width: 40, height: 40)
            // Stack multiple shadows for bloom-like falloff
            .shadow(color: glowColor.opacity(intensity * 0.6), radius: 8)
            .shadow(color: glowColor.opacity(intensity * 0.4), radius: 16)
            .shadow(color: glowColor.opacity(intensity * 0.2), radius: 32)
            .shadow(color: glowColor.opacity(intensity * 0.1), radius: 48)
    }
}
```

**Pros:** Zero setup, pure SwiftUI, works everywhere.
**Cons:** Not screen-space (only applies to the view), no threshold control, each `.shadow()` is a separate render pass.

### Approach 2: `.blur()` Modifier with Additive Layer

```swift
struct BloomOverlay: View {
    let intensity: Double = 0.7

    var body: some View {
        ZStack {
            // Original content
            ContentView()

            // Bloom layer: same content, blurred, additive
            ContentView()
                .blur(radius: 12)
                .blendMode(.plusLighter)
                .opacity(intensity)
                .allowsHitTesting(false)
        }
    }
}
```

**Pros:** Works with any SwiftUI content, simple.
**Cons:** Renders content twice, `.blur()` over ~20pt is expensive on mobile, no threshold (everything blooms equally).

### Approach 3: Metal `.layerEffect` (Best Quality)

```swift
struct MetalBloomView: View {
    let bloomIntensity: Float = 0.8
    let threshold: Float = 0.6

    var body: some View {
        ContentView()
            .layerEffect(
                ShaderLibrary.bloomEffect(
                    .float(threshold),
                    .float(bloomIntensity),
                    .float2(Float(UIScreen.main.bounds.width),
                            Float(UIScreen.main.bounds.height))
                ),
                maxSampleOffset: CGSize(width: 32, height: 32)
            )
    }
}
```

### Approach 4: MPS Gaussian Blur (MPSImageGaussianBlur)

Apple's Metal Performance Shaders include an optimized Gaussian blur. Best for offline/one-shot bloom on captured textures.

```swift
import MetalPerformanceShaders

func applyMPSBloom(
    commandBuffer: MTLCommandBuffer,
    source: MTLTexture,
    dest: MTLTexture,
    sigma: Float
) {
    let blur = MPSImageGaussianBlur(device: commandBuffer.device, sigma: sigma)
    blur.encode(
        commandBuffer: commandBuffer,
        sourceTexture: source,
        destinationTexture: dest
    )
}
```

---

## Unified Bloom Shader for SwiftUI

A single `.layerEffect` shader that does threshold + blur + composite in one pass. Trade-off: limited blur radius (constrained by `maxSampleOffset`), but zero setup complexity.

```metal
#include <metal_stdlib>
using namespace metal;

/// Single-pass bloom effect for SwiftUI .layerEffect
/// Limited by maxSampleOffset but good enough for UI glow
[[stitchable]]
half4 bloomEffect(
    float2 position,
    SwiftUI::Layer layer,
    float threshold,
    float intensity,
    float2 size
) {
    half4 original = layer.sample(position);

    // Bright pass
    float luma = dot(float3(original.rgb), float3(0.2126, 0.7152, 0.0722));
    float brightMask = smoothstep(threshold, threshold + 0.2, luma);

    // Multi-sample blur (2 rings)
    half4 blurred = half4(0);
    float totalWeight = 0;

    // Inner ring (8 samples, radius ~8)
    for (int i = 0; i < 8; i++) {
        float a = float(i) / 8.0 * 6.28318;
        float2 off = float2(cos(a), sin(a)) * 8.0;
        half4 s = layer.sample(position + off);
        float sLuma = dot(float3(s.rgb), float3(0.2126, 0.7152, 0.0722));
        float w = smoothstep(threshold, threshold + 0.2, sLuma) * 1.0;
        blurred += s * half(w);
        totalWeight += w;
    }

    // Outer ring (8 samples, radius ~20)
    for (int i = 0; i < 8; i++) {
        float a = float(i) / 8.0 * 6.28318 + 0.39;
        float2 off = float2(cos(a), sin(a)) * 20.0;
        half4 s = layer.sample(position + off);
        float sLuma = dot(float3(s.rgb), float3(0.2126, 0.7152, 0.0722));
        float w = smoothstep(threshold, threshold + 0.2, sLuma) * 0.5;
        blurred += s * half(w);
        totalWeight += w;
    }

    if (totalWeight > 0) {
        blurred /= half(totalWeight);
    }

    // Composite
    return original + blurred * half(intensity) * half(brightMask > 0 ? 1.0 : 0.3);
}
```

---

## Performance Guide

| Technique | GPU Cost | Quality | Max Blur Radius | Best For |
|-----------|----------|---------|-----------------|----------|
| `.shadow()` stacking | Low | Soft halo | ~48pt effective | UI buttons, icons |
| `.blur()` overlay | Medium | Uniform glow | ~20pt mobile | Quick prototype |
| Single-pass `.layerEffect` | Medium | Threshold + glow | ~32pt (maxSampleOffset) | SwiftUI VFX |
| Multi-pass Metal pipeline | High (but efficient) | Cinematic HDR | Unlimited | Game rendering |
| MPS Gaussian | Low (optimized) | Clean Gaussian | Unlimited | Offline / captured |

### Budget Rules

1. **`.blur()` radius** -- Keep under 15pt on mobile for full-screen overlays. Under 25pt for small views.
2. **`.shadow()` count** -- Max 4-5 stacked shadows before render cost becomes noticeable.
3. **Metal bloom passes** -- 3-5 blur levels at decreasing resolution. Each level is half the resolution of the previous.
4. **`maxSampleOffset`** -- Set to the actual maximum pixel distance your shader samples. Setting it too large wastes GPU time. Setting it too small clips the bloom.
5. **Downscale first** -- Always blur at half or quarter resolution. Full-resolution blur is 4-16x more expensive.
6. **Separable blur** -- Always split blur into horizontal + vertical passes. A 9x9 blur kernel becomes 9+9=18 samples instead of 81.

### Frame Budget Impact

| Effect | iPhone 12 | iPhone 15 Pro | M1 Mac |
|--------|-----------|---------------|--------|
| 4x `.shadow()` on 1 view | 0.2ms | 0.1ms | 0.05ms |
| `.blur(15)` full-screen | 3ms | 1.5ms | 0.5ms |
| `.layerEffect` bloom | 2ms | 1ms | 0.3ms |
| 4-level Metal bloom pipeline | 1.5ms | 0.8ms | 0.3ms |

The Metal pipeline is actually *cheaper* than `.blur()` for wide blooms because it operates at reduced resolution.

---

## Bloom Color Palette

Different spell types benefit from specific bloom colors:

| Spell Type | Core Color | Bloom Color | Notes |
|------------|-----------|-------------|-------|
| Fire | Orange/Yellow | Red-orange | Warm, saturated |
| Ice | White | Cyan/Light blue | Cool, desaturated |
| Lightning | White | Blue-purple | Very bright core |
| Healing | Green | Soft green | Lower intensity, gentle |
| Dark magic | Purple | Deep violet | Low threshold, wide bloom |
| Holy/Light | White | Gold/Warm white | High intensity, wide |
| Arcane | Pink-purple | Magenta | Saturated, medium bloom |

---

## Cross-References

- **orb skill** -- OCMiniOrb glow layer (Layer 1) uses RadialGradient + `.blur()` for simple ambient glow
- **swiftui-animation** `references/metal-shaders.md` -- Metal shader authoring and SwiftUI integration
- **Inferno** -- Pre-built bloom and glow shaders for SwiftUI
- **LearnOpenGL Bloom** -- Canonical reference for the multi-pass pipeline
