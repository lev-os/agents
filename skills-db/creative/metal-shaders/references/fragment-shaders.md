# Fragment / Pixel Shaders in Metal

## Anatomy

Fragment shaders receive interpolated per-pixel data from the vertex stage and output a color to a render target.

```
Vertex Data (position, UV, normal)
    -> Vertex Shader (transforms to clip space)
    -> Rasterizer (interpolates per-fragment)
    -> Fragment Shader (computes final color)
    -> Render Target (framebuffer / texture)
```

### Minimal Fragment Shader

```metal
#include <metal_stdlib>
using namespace metal;

struct VertexOut {
    float4 position [[ position ]];
    float2 uv;
};

fragment half4 basic_fragment(
    VertexOut in [[ stage_in ]],
    texture2d<half> tex [[ texture(0) ]],
    sampler samp [[ sampler(0) ]]
) {
    half4 color = tex.sample(samp, in.uv);
    return color;
}
```

### Stitchable Fragment for SwiftUI

For SwiftUI integration, fragment shaders use the `[[ stitchable ]]` attribute instead of `[[ stage_in ]]`:

```metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 passthrough(float2 position, half4 color) {
    return color;
}
```

---

## Post-Processing Patterns

### Bloom Threshold Extraction {#bloom}

Extract bright pixels above a luminance threshold for bloom processing.

```metal
#include <metal_stdlib>
using namespace metal;

// Standalone bloom threshold (render pipeline)
fragment half4 bloom_threshold(
    VertexOut in [[ stage_in ]],
    texture2d<half> scene [[ texture(0) ]],
    sampler samp [[ sampler(0) ]],
    constant float &threshold [[ buffer(0) ]]
) {
    half4 color = scene.sample(samp, in.uv);
    // Luminance via perceptual weights
    half luminance = dot(color.rgb, half3(0.2126h, 0.7152h, 0.0722h));
    // Soft knee: smooth transition around threshold
    half knee = 0.1h;
    half soft = clamp((luminance - threshold + knee) / (2.0h * knee), 0.0h, 1.0h);
    soft = soft * soft;
    half contribution = max(luminance - threshold, soft * knee);
    return half4(color.rgb * (contribution / max(luminance, 1e-5h)), 1.0h);
}

// SwiftUI stitchable version
[[ stitchable ]] half4 bloom_extract(float2 position, half4 color, float threshold) {
    half lum = dot(color.rgb, half3(0.2126h, 0.7152h, 0.0722h));
    half t = half(threshold);
    half contrib = max(lum - t, 0.0h);
    return half4(color.rgb * (contrib / max(lum, 1e-5h)), color.a);
}
```

### Gaussian Blur (Separable, Two-Pass) {#gaussian-blur}

Separable blur is O(2N) instead of O(N^2). Run horizontal pass first, then vertical on the result.

```metal
#include <metal_stdlib>
using namespace metal;

// 9-tap Gaussian weights (sigma ~2.0)
constant half weights[5] = { 0.2270270270h, 0.1945945946h, 0.1216216216h, 0.0540540541h, 0.0162162162h };

// Horizontal blur -- use as layerEffect
[[ stitchable ]] half4 gaussian_blur_h(
    float2 position,
    SwiftUI::Layer layer,
    float radius
) {
    half4 result = layer.sample(position) * weights[0];
    for (int i = 1; i < 5; i++) {
        float offset = float(i) * radius;
        result += layer.sample(float2(position.x + offset, position.y)) * weights[i];
        result += layer.sample(float2(position.x - offset, position.y)) * weights[i];
    }
    return result;
}

// Vertical blur -- use as layerEffect (second pass)
[[ stitchable ]] half4 gaussian_blur_v(
    float2 position,
    SwiftUI::Layer layer,
    float radius
) {
    half4 result = layer.sample(position) * weights[0];
    for (int i = 1; i < 5; i++) {
        float offset = float(i) * radius;
        result += layer.sample(float2(position.x, position.y + offset)) * weights[i];
        result += layer.sample(float2(position.x, position.y - offset)) * weights[i];
    }
    return result;
}
```

### Color Grading {#color-grading}

Simple HSV-based color grading. For LUT-based grading, sample a 3D LUT texture.

```metal
#include <metal_stdlib>
using namespace metal;

// Convert RGB to HSV
half3 rgb2hsv(half3 c) {
    half4 K = half4(0.0h, -1.0h/3.0h, 2.0h/3.0h, -1.0h);
    half4 p = mix(half4(c.bg, K.wz), half4(c.gb, K.xy), step(c.b, c.g));
    half4 q = mix(half4(p.xyw, c.r), half4(c.r, p.yzx), step(p.x, c.r));
    half d = q.x - min(q.w, q.y);
    half e = 1.0e-10h;
    return half3(abs(q.z + (q.w - q.y) / (6.0h * d + e)), d / (q.x + e), q.x);
}

// Convert HSV to RGB
half3 hsv2rgb(half3 c) {
    half4 K = half4(1.0h, 2.0h/3.0h, 1.0h/3.0h, 3.0h);
    half3 p = abs(fract(c.xxx + K.xyz) * 6.0h - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0h, 1.0h), c.y);
}

[[ stitchable ]] half4 color_grade(
    float2 position,
    half4 color,
    float hueShift,       // -1.0 to 1.0
    float saturation,     // 0.0 to 2.0
    float brightness,     // 0.0 to 2.0
    float contrast        // 0.0 to 2.0
) {
    half3 hsv = rgb2hsv(color.rgb);
    hsv.x = fract(hsv.x + half(hueShift));         // Hue rotation
    hsv.y = clamp(hsv.y * half(saturation), 0.0h, 1.0h);  // Saturation
    hsv.z = hsv.z * half(brightness);               // Brightness
    half3 rgb = hsv2rgb(hsv);
    // Contrast around midpoint
    rgb = (rgb - 0.5h) * half(contrast) + 0.5h;
    return half4(clamp(rgb, 0.0h, 1.0h), color.a);
}

// LUT-based color grading (requires 3D LUT texture)
fragment half4 lut_grade(
    VertexOut in [[ stage_in ]],
    texture2d<half> scene [[ texture(0) ]],
    texture3d<half> lut [[ texture(1) ]],
    sampler samp [[ sampler(0) ]]
) {
    half4 color = scene.sample(samp, in.uv);
    // LUT is typically 32x32x32 or 64x64x64
    half3 graded = lut.sample(samp, float3(color.rgb)).rgb;
    return half4(graded, color.a);
}
```

### Vignette {#vignette}

```metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 vignette(
    float2 position,
    half4 color,
    float2 size,       // view dimensions
    float intensity,   // 0.0 to 1.0 (strength)
    float radius       // 0.0 to 1.0 (how far from center)
) {
    float2 uv = position / size;
    float2 center = uv - 0.5;
    float dist = length(center);
    float vig = smoothstep(radius, radius - 0.45, dist);
    half darken = half(mix(1.0, vig, intensity));
    return half4(color.rgb * darken, color.a);
}
```

### Chromatic Aberration {#chromatic-aberration}

Requires layerEffect because it samples at offset positions.

```metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 chromatic_aberration(
    float2 position,
    SwiftUI::Layer layer,
    float2 size,       // view dimensions
    float strength     // pixel offset amount
) {
    float2 uv = position / size;
    float2 center = uv - 0.5;
    float dist = length(center);
    float2 dir = normalize(center) * dist * strength;

    half r = layer.sample(position + dir).r;
    half g = layer.sample(position).g;
    half b = layer.sample(position - dir).b;
    half a = layer.sample(position).a;

    return half4(r, g, b, a);
}
```

### Film Grain {#film-grain}

```metal
#include <metal_stdlib>
using namespace metal;

// Simple hash for grain
half hash(float2 p) {
    float3 p3 = fract(float3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return half(fract((p3.x + p3.y) * p3.z));
}

[[ stitchable ]] half4 film_grain(
    float2 position,
    half4 color,
    float time,
    float intensity    // 0.0 to 0.3 typical
) {
    half noise = hash(position + float2(time * 100.0, time * 57.0));
    noise = (noise - 0.5h) * half(intensity);
    return half4(clamp(color.rgb + noise, 0.0h, 1.0h), color.a);
}
```

### CRT Scanlines {#crt-scanlines}

```metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 crt_scanlines(
    float2 position,
    half4 color,
    float lineSpacing,   // pixels between scanlines (e.g., 3.0)
    float intensity      // 0.0 to 1.0
) {
    half scanline = half(sin(position.y * 3.14159 / lineSpacing));
    scanline = scanline * scanline;  // sharpen
    half darken = 1.0h - half(intensity) * scanline;
    return half4(color.rgb * darken, color.a);
}
```

---

## Debugging {#debugging}

### GPU Frame Capture

1. In Xcode, click the camera icon in the debug bar during a running session
2. Or programmatically trigger capture:

```swift
import Metal

let captureManager = MTLCaptureManager.shared()
let captureDescriptor = MTLCaptureDescriptor()
captureDescriptor.captureObject = device
captureDescriptor.destination = .gpuTraceDocument
captureDescriptor.outputURL = URL(fileURLWithPath: "/tmp/trace.gputrace")

try captureManager.startCapture(with: captureDescriptor)
// ... render frame ...
captureManager.stopCapture()
```

### Common Debugging Techniques

| Technique | How |
|-----------|-----|
| **Visualize UV coords** | `return half4(half(uv.x), half(uv.y), 0.0h, 1.0h);` |
| **Visualize normals** | `return half4(normal * 0.5h + 0.5h, 1.0h);` |
| **Overdraw heatmap** | Increment atomic counter per fragment, color by count |
| **NaN detection** | `if (isnan(color.r)) return half4(1,0,1,1);` (magenta = NaN) |
| **Depth visualization** | `half d = half(depth); return half4(d, d, d, 1.0h);` |
| **Shader validation** | Enable `MTL_SHADER_VALIDATION=1` environment variable |

### Xcode Shader Profiler

- **Shader Profiler** tab in GPU Frame Capture shows per-instruction cost
- **Shader Timeline** shows execution across SIMD groups
- Watch for: divergent branches, high ALU:texture ratio, register spilling
