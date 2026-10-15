# Metal Shaders in SwiftUI

SwiftUI (iOS 17+, macOS 14+) provides three modifier types for applying Metal shaders directly to views. The shader functions must be marked `[[ stitchable ]]` and follow exact function signature contracts.

---

## Three Modifier Types

### colorEffect {#colorEffect}

Transforms the color of each pixel independently. Cannot sample neighboring pixels.

**MSL signature:**
```metal
[[ stitchable ]] half4 name(float2 position, half4 color, <additional args...>)
```

- `position` -- pixel coordinate in the view's local coordinate space (points, not pixels)
- `color` -- current RGBA color at this pixel (premultiplied alpha)
- Returns the new color

**Swift usage:**
```swift
myView
    .colorEffect(ShaderLibrary.myShader(
        .float(time),
        .float(intensity)
    ))
```

**Complete example -- Rainbow Pulse:**

```metal
// RainbowPulse.metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 rainbowPulse(
    float2 position,
    half4 color,
    float time,
    float2 size
) {
    // Normalize position
    float2 uv = position / size;

    // Rainbow hue based on position + time
    float hue = fract(uv.x * 0.5 + uv.y * 0.3 + time * 0.2);

    // HSV to RGB
    float3 rgb = clamp(abs(fmod(float(hue) * 6.0 + float3(0, 4, 2), 6.0) - 3.0) - 1.0, 0.0, 1.0);

    // Mix with original color
    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    half3 result = mix(color.rgb, half3(rgb) * color.a, half(pulse * 0.6));

    return half4(result, color.a);
}
```

```swift
// RainbowView.swift
import SwiftUI

struct RainbowView: View {
    @State private var startTime = Date.now

    var body: some View {
        TimelineView(.animation) { timeline in
            let time = timeline.date.timeIntervalSince(startTime)

            Text("Hello Metal")
                .font(.largeTitle)
                .foregroundStyle(.white)
                .padding(40)
                .background(.black)
                .colorEffect(ShaderLibrary.rainbowPulse(
                    .float(time),
                    .float2(CGSize(width: 300, height: 100))
                ))
        }
    }
}
```

### distortionEffect {#distortionEffect}

Displaces pixels by returning the source coordinate to sample from. Does not change colors directly.

**MSL signature:**
```metal
[[ stitchable ]] float2 name(float2 position, <additional args...>)
```

- `position` -- destination pixel coordinate
- Returns the source coordinate to sample from (where to pull the color from)

**Swift usage:**
```swift
myView
    .distortionEffect(
        ShaderLibrary.myDistortion(.float(time)),
        maxSampleOffset: CGSize(width: 100, height: 100)  // REQUIRED
    )
```

**IMPORTANT:** `maxSampleOffset` tells SwiftUI the maximum distance a pixel might sample from. If your shader displaces pixels up to 50pt, set this to at least 50. Too small = clipped artifacts. Too large = wasted rendering area.

**Complete example -- Ripple Effect:**

```metal
// Ripple.metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] float2 ripple(
    float2 position,
    float time,
    float2 origin,     // center of ripple
    float amplitude,   // max displacement in points
    float frequency,   // wave frequency
    float decay        // how fast it fades with distance
) {
    float2 dir = position - origin;
    float dist = length(dir);

    // Wave function
    float wave = sin(dist * frequency - time * 6.0);

    // Decay with distance from origin
    float fade = exp(-dist * decay);

    // Apply displacement along the direction from origin
    float2 offset = normalize(dir) * wave * amplitude * fade;

    return position + offset;
}
```

```swift
// RippleView.swift
import SwiftUI

struct RippleView: View {
    @State private var startTime = Date.now
    @State private var tapLocation = CGPoint(x: 150, y: 150)

    var body: some View {
        TimelineView(.animation) { timeline in
            let time = timeline.date.timeIntervalSince(startTime)

            Image("photo")
                .resizable()
                .frame(width: 300, height: 300)
                .distortionEffect(
                    ShaderLibrary.ripple(
                        .float(time),
                        .float2(tapLocation),
                        .float(8.0),    // amplitude
                        .float(0.15),   // frequency
                        .float(0.02)    // decay
                    ),
                    maxSampleOffset: CGSize(width: 20, height: 20)
                )
                .onTapGesture { location in
                    startTime = .now
                    tapLocation = location
                }
        }
    }
}
```

### layerEffect {#layerEffect}

The most powerful type. Receives the entire view as a `SwiftUI::Layer` that can be sampled at any coordinate, enabling blur, glow, edge detection, and other multi-sample effects.

**MSL signature:**
```metal
[[ stitchable ]] half4 name(float2 position, SwiftUI::Layer layer, <additional args...>)
```

- `position` -- destination pixel coordinate
- `layer` -- the source view; call `layer.sample(float2)` to read any pixel
- Returns the new color

**Swift usage:**
```swift
myView
    .layerEffect(
        ShaderLibrary.myEffect(.float(time)),
        maxSampleOffset: CGSize(width: 50, height: 50)  // REQUIRED
    )
```

**Complete example -- Pixellation:**

```metal
// Pixellate.metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 pixellate(
    float2 position,
    SwiftUI::Layer layer,
    float pixelSize
) {
    // Snap to grid
    float2 snapped = floor(position / pixelSize) * pixelSize + pixelSize * 0.5;
    return layer.sample(snapped);
}
```

```swift
// PixellateView.swift
import SwiftUI

struct PixellateView: View {
    @State private var pixelSize: Float = 1.0

    var body: some View {
        Image("photo")
            .resizable()
            .frame(width: 300, height: 300)
            .layerEffect(
                ShaderLibrary.pixellate(.float(pixelSize)),
                maxSampleOffset: .zero  // no offset needed
            )
            .onTapGesture {
                withAnimation(.spring) {
                    pixelSize = pixelSize > 1 ? 1 : 10
                }
            }
    }
}
```

**Complete example -- Frosted Glass Blur:**

```metal
// FrostedGlass.metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 frostedGlass(
    float2 position,
    SwiftUI::Layer layer,
    float radius,
    float time
) {
    half4 color = half4(0.0h);
    float totalWeight = 0.0;

    // 16-tap disc sampling for blur
    const int SAMPLES = 16;
    for (int i = 0; i < SAMPLES; i++) {
        float angle = float(i) * 6.28318 / float(SAMPLES);
        float r = radius * fract(sin(float(i) * 43758.5453 + time) * 0.5 + 0.5);
        float2 offset = float2(cos(angle), sin(angle)) * r;

        color += layer.sample(position + offset);
        totalWeight += 1.0;
    }

    return color / half(totalWeight);
}
```

---

## ShaderLibrary

`ShaderLibrary` automatically discovers all `.metal` files in the app bundle. No registration needed.

```swift
// Access by name (function name in .metal file)
ShaderLibrary.myShaderName(.float(1.0))

// Dynamic access (string-based)
ShaderLibrary[dynamicMember: "myShaderName"]

// From a specific bundle
ShaderLibrary(bundle: .module).myShaderName(.float(1.0))
```

### Parameter Types

| Swift | MSL | Notes |
|-------|-----|-------|
| `.float(1.0)` | `float` | Single float |
| `.float2(CGSize(w:100, h:100))` | `float2` | Width/height or x/y |
| `.float2(CGPoint(x:50, y:50))` | `float2` | Point as float2 |
| `.color(.red)` | `half4` | SwiftUI Color -> RGBA |
| `.image(Image("tex"))` | `texture2d<half>` | Texture from SwiftUI Image |
| `.data(Data(...))` | `device const void*` | Raw buffer |
| `.boundingRect` | `float4` | View bounds (auto-provided) |

---

## Inferno Framework Patterns

[Inferno](https://github.com/twostraws/Inferno) by Paul Hudson provides 17 ready-made Metal shaders for SwiftUI. Key patterns to learn from:

| Effect | Type | Key Technique |
|--------|------|---------------|
| Checkerboard | colorEffect | `fmod(floor(pos/size), 2.0)` |
| Circle waves | colorEffect | `sin(length(pos - center) * freq - time)` |
| Color shift | colorEffect | HSV rotation |
| Emboss | layerEffect | Sample offset + difference |
| Infrared | colorEffect | Luminance -> heat palette |
| Light grid | colorEffect | `sin(pos.x * freq) * sin(pos.y * freq)` |
| Noise | colorEffect | Hash-based noise pattern |
| Pixellate | layerEffect | `floor(pos / size) * size` |
| Rainbow | colorEffect | Position -> hue -> RGB |
| Relative wave | distortionEffect | `sin(pos.y * freq) * amplitude` |
| Sinebow | colorEffect | `sin(pos + offset)^2` for each channel |
| Water | distortionEffect | Layered sine waves |

---

## Gotchas and Common Pitfalls

### 1. maxSampleOffset (Critical)

`distortionEffect` and `layerEffect` REQUIRE `maxSampleOffset`. If your shader samples beyond this range, pixels will be clipped or show artifacts.

```swift
// BAD: too small, causes clipping
.layerEffect(ShaderLibrary.blur(.float(20)), maxSampleOffset: CGSize(width: 5, height: 5))

// GOOD: matches or exceeds actual sample radius
.layerEffect(ShaderLibrary.blur(.float(20)), maxSampleOffset: CGSize(width: 25, height: 25))
```

### 2. Coordinate Space

Shader position is in SwiftUI points, not pixels. On Retina displays, one point = 2-3 pixels. The shader operates in the view's local coordinate space (origin at top-left of the modified view).

### 3. Premultiplied Alpha

SwiftUI colors are premultiplied. When blending:
```metal
// CORRECT: premultiplied
half4 result = half4(newRGB * color.a, color.a);

// WRONG: will look too bright
half4 result = half4(newRGB, color.a);
```

### 4. Metal File Discovery

- `.metal` files must be in the app target (not a Swift Package by default)
- For Swift Packages: add `.metal` files to `resources` in `Package.swift` and use `ShaderLibrary(bundle: .module)`
- File must compile without errors; a broken `.metal` file crashes `ShaderLibrary` access

### 5. isEnabled Guard

Shaders are not available on all devices. Guard with availability:

```swift
if #available(iOS 17.0, macOS 14.0, *) {
    content.colorEffect(ShaderLibrary.myShader())
} else {
    content
}
```

### 6. Performance Considerations

- `colorEffect` is cheapest (single-pixel, no sampling)
- `distortionEffect` is moderate (samples one source pixel per output pixel)
- `layerEffect` is most expensive (can sample multiple source pixels)
- Avoid complex loops in `layerEffect` -- each iteration adds a texture sample
- Use `TimelineView(.animation)` sparingly; it redraws every frame

### 7. Animating Shader Parameters

SwiftUI cannot interpolate shader parameters with `withAnimation`. Use `TimelineView` for time-based animation, or animate a `@State` property that feeds into the shader:

```swift
// TimelineView for continuous animation
TimelineView(.animation) { timeline in
    let time = timeline.date.timeIntervalSinceReferenceDate
    view.colorEffect(ShaderLibrary.pulse(.float(time)))
}

// @State for triggered animation
@State private var intensity: Float = 0

view.colorEffect(ShaderLibrary.glow(.float(intensity)))
    .onTapGesture {
        withAnimation(.spring) { intensity = 1.0 }
    }
// Note: the spring interpolates `intensity`, which feeds into the shader each frame
```

---

## Complete Template: New SwiftUI Shader

### 1. Create the .metal file

```metal
// MyEffect.metal
#include <metal_stdlib>
using namespace metal;

[[ stitchable ]] half4 myEffect(
    float2 position,
    half4 color,
    float time,
    float2 size
) {
    // Your shader logic here
    float2 uv = position / size;

    // Example: pulsing brightness
    half brightness = half(sin(time * 2.0) * 0.2 + 1.0);
    return half4(color.rgb * brightness, color.a);
}
```

### 2. Apply in SwiftUI

```swift
// MyEffectView.swift
import SwiftUI

struct MyEffectView: View {
    @State private var start = Date.now

    var body: some View {
        TimelineView(.animation) { ctx in
            let t = ctx.date.timeIntervalSince(start)

            Text("Shader Demo")
                .font(.title)
                .padding()
                .colorEffect(ShaderLibrary.myEffect(
                    .float(t),
                    .float2(CGSize(width: 200, height: 50))
                ))
        }
    }
}
```

### 3. Test in preview

```swift
#Preview {
    MyEffectView()
}
```

SwiftUI Previews render Metal shaders in real-time, making iteration fast.
