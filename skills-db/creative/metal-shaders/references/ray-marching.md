# Ray Marching and Volumetrics in Metal

## Core Concept

Ray marching steps along a ray from the camera through each pixel, evaluating a **Signed Distance Function (SDF)** at each step to determine how far the nearest surface is. If the distance is below a threshold, the ray has hit a surface.

```
Camera  -----> step ----> step ----> step --> HIT (distance < epsilon)
                |           |          |
              d=5.2       d=2.1      d=0.003
              (far)      (closer)    (surface!)
```

The key insight: the SDF tells us the safe distance we can step without missing any geometry, making the algorithm adaptive and efficient.

---

## SDF Primitives {#sdf}

Each function returns the signed distance from point `p` to the surface. Negative = inside, positive = outside.

```metal
#include <metal_stdlib>
using namespace metal;

// ---- Primitives ----

// Sphere centered at origin with radius r
float sdSphere(float3 p, float r) {
    return length(p) - r;
}

// Box centered at origin with half-extents b
float sdBox(float3 p, float3 b) {
    float3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// Torus centered at origin, t.x = major radius, t.y = minor radius
float sdTorus(float3 p, float2 t) {
    float2 q = float2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// Infinite cylinder along Y axis with radius r
float sdCylinder(float3 p, float r) {
    return length(p.xz) - r;
}

// Capped cylinder along Y axis
float sdCappedCylinder(float3 p, float h, float r) {
    float2 d = abs(float2(length(p.xz), p.y)) - float2(r, h);
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

// Infinite plane at y = 0 (normal pointing up)
float sdPlane(float3 p) {
    return p.y;
}

// Plane with arbitrary normal n (must be normalized) and offset d
float sdPlaneN(float3 p, float3 n, float d) {
    return dot(p, n) + d;
}

// Rounded box (box with rounded edges)
float sdRoundBox(float3 p, float3 b, float r) {
    float3 q = abs(p) - b + r;
    return length(max(q, 0.0)) - r;
}

// Capsule from point a to point b with radius r
float sdCapsule(float3 p, float3 a, float3 b, float r) {
    float3 pa = p - a, ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}
```

### SDF Operations

```metal
// ---- Boolean Operations ----

// Union: combine two shapes (take the closer surface)
float opUnion(float d1, float d2) {
    return min(d1, d2);
}

// Intersection: keep only where both shapes overlap
float opIntersection(float d1, float d2) {
    return max(d1, d2);
}

// Subtraction: cut shape d2 from shape d1
float opSubtraction(float d1, float d2) {
    return max(d1, -d2);
}

// Smooth union: blend between shapes with radius k
float opSmoothUnion(float d1, float d2, float k) {
    float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) - k * h * (1.0 - h);
}

// Smooth subtraction
float opSmoothSubtraction(float d1, float d2, float k) {
    float h = clamp(0.5 - 0.5 * (d2 + d1) / k, 0.0, 1.0);
    return mix(d2, -d1, h) + k * h * (1.0 - h);
}

// Smooth intersection
float opSmoothIntersection(float d1, float d2, float k) {
    float h = clamp(0.5 - 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) + k * h * (1.0 - h);
}

// ---- Domain Operations ----

// Infinite repetition with spacing s
float3 opRepeat(float3 p, float3 s) {
    return fmod(p + 0.5 * s, s) - 0.5 * s;
}

// Limited repetition: repeat c times with spacing s
float3 opRepeatLimited(float3 p, float s, float3 c) {
    return p - s * clamp(round(p / s), -c, c);
}

// Symmetry across X axis
float3 opSymX(float3 p) {
    return float3(abs(p.x), p.y, p.z);
}

// Twist around Y axis
float3 opTwist(float3 p, float k) {
    float c = cos(k * p.y);
    float s = sin(k * p.y);
    float2x2 m = float2x2(c, -s, s, c);
    return float3(m * p.xz, p.y);
}

// Bend around Z axis
float3 opBend(float3 p, float k) {
    float c = cos(k * p.x);
    float s = sin(k * p.x);
    float2x2 m = float2x2(c, -s, s, c);
    float2 bent = m * float2(p.x, p.y);
    return float3(bent, p.z);
}
```

---

## Complete Ray Marcher {#ray-marcher}

### Scene Definition + Ray March Loop

```metal
#include <metal_stdlib>
using namespace metal;

// Forward declare SDF primitives and operations (from above)

// Scene SDF: compose your world here
float sceneSDF(float3 p) {
    // Ground plane
    float ground = sdPlane(p);

    // Sphere floating above ground
    float sphere = sdSphere(p - float3(0, 1.0, 0), 0.8);

    // Box to the right
    float box = sdBox(p - float3(2.5, 0.6, 0), float3(0.6));

    // Torus on the left
    float torus = sdTorus(p - float3(-2.5, 0.8, 0), float2(0.6, 0.2));

    // Smooth union of sphere and box
    float shapes = opSmoothUnion(sphere, box, 0.5);

    return opUnion(opUnion(shapes, torus), ground);
}

// Normal via central differences
float3 calcNormal(float3 p) {
    float2 e = float2(0.001, 0.0);
    return normalize(float3(
        sceneSDF(p + e.xyy) - sceneSDF(p - e.xyy),
        sceneSDF(p + e.yxy) - sceneSDF(p - e.yxy),
        sceneSDF(p + e.yyx) - sceneSDF(p - e.yyx)
    ));
}

// Soft shadow via ray march from surface toward light
float softShadow(float3 ro, float3 rd, float mint, float maxt, float k) {
    float result = 1.0;
    float t = mint;
    for (int i = 0; i < 64; i++) {
        float d = sceneSDF(ro + rd * t);
        if (d < 0.001) return 0.0;
        result = min(result, k * d / t);
        t += d;
        if (t > maxt) break;
    }
    return result;
}

// Ambient occlusion via short SDF probes along normal
float calcAO(float3 pos, float3 nor) {
    float occ = 0.0;
    float sca = 1.0;
    for (int i = 0; i < 5; i++) {
        float h = 0.01 + 0.12 * float(i);
        float d = sceneSDF(pos + h * nor);
        occ += (h - d) * sca;
        sca *= 0.95;
    }
    return clamp(1.0 - 3.0 * occ, 0.0, 1.0);
}

// Main ray march
float rayMarch(float3 ro, float3 rd, float maxDist) {
    float t = 0.0;
    for (int i = 0; i < 256; i++) {
        float3 p = ro + rd * t;
        float d = sceneSDF(p);
        if (d < 0.0005) return t;  // Hit
        t += d;
        if (t > maxDist) break;     // Miss
    }
    return -1.0; // No hit
}

// Camera ray generation
float3x3 setCamera(float3 ro, float3 ta, float roll) {
    float3 cw = normalize(ta - ro);
    float3 cp = float3(sin(roll), cos(roll), 0.0);
    float3 cu = normalize(cross(cw, cp));
    float3 cv = cross(cu, cw);
    return float3x3(cu, cv, cw);
}

// ---- Fragment shader (render pipeline version) ----

struct VertexOut {
    float4 position [[ position ]];
    float2 uv;
};

fragment half4 ray_march_scene(
    VertexOut in [[ stage_in ]],
    constant float2 &resolution [[ buffer(0) ]],
    constant float &time [[ buffer(1) ]]
) {
    // Normalized coords: -1 to 1, aspect-corrected
    float2 uv = (2.0 * in.uv - 1.0) * float2(resolution.x / resolution.y, 1.0);

    // Camera orbit
    float3 ro = float3(4.0 * cos(time * 0.3), 2.5, 4.0 * sin(time * 0.3));
    float3 ta = float3(0.0, 0.5, 0.0);
    float3x3 ca = setCamera(ro, ta, 0.0);
    float3 rd = ca * normalize(float3(uv, 2.0));  // FOV via z component

    // Sky gradient
    float3 col = float3(0.4, 0.6, 0.9) - 0.5 * rd.y;

    // March
    float t = rayMarch(ro, rd, 40.0);

    if (t > 0.0) {
        float3 pos = ro + rd * t;
        float3 nor = calcNormal(pos);

        // Lighting
        float3 lightDir = normalize(float3(0.6, 0.8, -0.4));
        float diff = clamp(dot(nor, lightDir), 0.0, 1.0);
        float amb = 0.1 + 0.1 * nor.y;
        float shadow = softShadow(pos + nor * 0.01, lightDir, 0.02, 10.0, 16.0);
        float ao = calcAO(pos, nor);

        // Material color (simple: use normal as color)
        float3 mate = float3(0.8, 0.7, 0.6);

        col = mate * (amb * ao + diff * shadow * float3(1.0, 0.9, 0.7));

        // Fog
        float fog = 1.0 - exp(-0.005 * t * t);
        col = mix(col, float3(0.4, 0.6, 0.9), fog);
    }

    // Gamma correction
    col = pow(col, float3(0.4545));

    return half4(half3(col), 1.0h);
}

// ---- SwiftUI stitchable version (layerEffect) ----
// Note: ray marching as a layerEffect is expensive; prefer for small views

[[ stitchable ]] half4 sdf_overlay(
    float2 position,
    SwiftUI::Layer layer,
    float2 size,
    float time
) {
    float2 uv = (2.0 * position / size - 1.0) * float2(size.x / size.y, 1.0);

    float3 ro = float3(3.0 * cos(time * 0.5), 2.0, 3.0 * sin(time * 0.5));
    float3 ta = float3(0.0, 0.5, 0.0);
    float3x3 ca = setCamera(ro, ta, 0.0);
    float3 rd = ca * normalize(float3(uv, 2.0));

    float t = 0.0;
    for (int i = 0; i < 64; i++) {  // fewer steps for real-time
        float3 p = ro + rd * t;
        float d = sdSphere(p - float3(0, 1, 0), 0.8);
        if (d < 0.01) break;
        t += d;
        if (t > 20.0) break;
    }

    half4 bg = layer.sample(position);
    if (t < 20.0) {
        float3 p = ro + rd * t;
        float3 n = calcNormal(p);
        half light = half(clamp(dot(n, normalize(float3(1, 1, -1))), 0.0, 1.0));
        return half4(light * 0.8h, light * 0.6h, light * 0.9h, 1.0h);
    }
    return bg;
}
```

---

## Volumetric Rendering {#volumetric}

Volumetric rendering samples a density field along the ray and accumulates color and opacity using front-to-back blending.

### Volumetric Fog Fragment Shader

```metal
#include <metal_stdlib>
using namespace metal;

// Simple 3D noise (see noise-functions.md for full implementations)
float hash3D(float3 p) {
    p = fract(p * float3(443.897, 441.423, 437.195));
    p += dot(p, p.yzx + 19.19);
    return fract((p.x + p.y) * p.z);
}

float noise3D(float3 p) {
    float3 i = floor(p);
    float3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f); // smoothstep

    return mix(
        mix(mix(hash3D(i), hash3D(i + float3(1,0,0)), f.x),
            mix(hash3D(i + float3(0,1,0)), hash3D(i + float3(1,1,0)), f.x), f.y),
        mix(mix(hash3D(i + float3(0,0,1)), hash3D(i + float3(1,0,1)), f.x),
            mix(hash3D(i + float3(0,1,1)), hash3D(i + float3(1,1,1)), f.x), f.y),
        f.z
    );
}

// fBm for cloud density
float fbmDensity(float3 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < octaves; i++) {
        value += amplitude * noise3D(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

// Density field for clouds/fog
float cloudDensity(float3 p, float time) {
    // Wind animation
    p += float3(time * 0.1, 0, time * 0.05);

    // Base shape: sphere of fog
    float falloff = 1.0 - smoothstep(0.0, 3.0, length(p));

    // Detail noise
    float density = fbmDensity(p * 0.8, 5) * falloff;

    // Threshold to create cloud-like structures
    return max(density - 0.2, 0.0) * 2.0;
}

fragment half4 volumetric_fog(
    VertexOut in [[ stage_in ]],
    constant float2 &resolution [[ buffer(0) ]],
    constant float &time [[ buffer(1) ]]
) {
    float2 uv = (2.0 * in.uv - 1.0) * float2(resolution.x / resolution.y, 1.0);

    // Camera
    float3 ro = float3(0, 0, -5.0);
    float3 rd = normalize(float3(uv, 1.5));

    // Ray march through volume
    float3 col = float3(0.0);
    float totalAlpha = 0.0;

    float stepSize = 0.1;
    int maxSteps = 64;  // 4-8 steps for mobile, 32-64 for desktop
    float t = 0.0;

    // Light direction
    float3 lightDir = normalize(float3(1.0, 1.0, -0.5));
    float3 lightColor = float3(1.0, 0.9, 0.7);
    float3 ambientColor = float3(0.2, 0.3, 0.5);

    for (int i = 0; i < maxSteps; i++) {
        float3 p = ro + rd * t;

        float density = cloudDensity(p, time);

        if (density > 0.01) {
            // Beer-Lambert absorption
            float absorption = exp(-density * stepSize * 2.0);
            float transmittance = 1.0 - totalAlpha;

            // Simple light scattering: march toward light for shadow
            float lightDensity = 0.0;
            float3 lightPos = p;
            for (int j = 0; j < 4; j++) {
                lightPos += lightDir * 0.2;
                lightDensity += cloudDensity(lightPos, time) * 0.2;
            }
            float lightTransmittance = exp(-lightDensity * 3.0);

            // Phase function (Henyey-Greenstein approximation)
            float cosTheta = dot(rd, lightDir);
            float phase = 0.25 + 0.75 * pow(0.5 + 0.5 * cosTheta, 3.0);

            // Accumulate color
            float3 sampleColor = lightColor * lightTransmittance * phase + ambientColor;
            float sampleAlpha = (1.0 - absorption) * transmittance;

            col += sampleColor * sampleAlpha;
            totalAlpha += sampleAlpha;

            // Early termination
            if (totalAlpha > 0.99) break;
        }

        t += stepSize;
        if (t > 10.0) break;
    }

    // Background sky
    float3 sky = float3(0.4, 0.6, 0.9) - 0.3 * rd.y;
    col = col + sky * (1.0 - totalAlpha);

    // Gamma
    col = pow(col, float3(0.4545));

    return half4(half3(col), 1.0h);
}
```

### Optimization Tips for Volumetrics

| Technique | Speedup | Trade-off |
|-----------|---------|-----------|
| Adaptive step size | 2-4x | Slight visual artifacts at density boundaries |
| Early termination at alpha > 0.99 | Variable | None (imperceptible) |
| Bounding volume check | 2-10x | Must define tight bounds |
| Temporal reprojection | 2-4x | Ghosting on fast motion |
| Half-resolution render | 4x | Slight blur (bilateral upsample helps) |
| Fewer light march steps | Linear | Softer shadows |
| Jittered ray start | N/A | Reduces banding at same step count |

### Adaptive Step Size

```metal
// Start with larger steps, shrink near surfaces
float stepSize = 0.2;
for (int i = 0; i < maxSteps; i++) {
    float3 p = ro + rd * t;
    float density = cloudDensity(p, time);

    if (density > 0.01) {
        stepSize = 0.05;  // Fine steps inside volume
        // ... accumulate ...
    } else {
        stepSize = 0.2;   // Large steps in empty space
    }
    t += stepSize;
}
```
