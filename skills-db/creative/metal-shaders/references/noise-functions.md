# Noise Functions in Metal Shading Language

MSL does not have built-in noise functions (unlike GLSL). All noise must be implemented manually or sampled from precomputed textures.

---

## Perlin Noise {#perlin}

Gradient noise using a grid of pseudo-random gradient vectors with smooth interpolation.

### 2D Perlin Noise

```metal
#include <metal_stdlib>
using namespace metal;

// Hash function for gradient generation
float2 perlin_hash2(float2 p) {
    p = float2(dot(p, float2(127.1, 311.7)),
               dot(p, float2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

float perlinNoise2D(float2 p) {
    float2 i = floor(p);
    float2 f = fract(p);

    // Quintic interpolation (smoother than cubic)
    float2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);

    // Gradients at four corners
    float a = dot(perlin_hash2(i + float2(0.0, 0.0)), f - float2(0.0, 0.0));
    float b = dot(perlin_hash2(i + float2(1.0, 0.0)), f - float2(1.0, 0.0));
    float c = dot(perlin_hash2(i + float2(0.0, 1.0)), f - float2(0.0, 1.0));
    float d = dot(perlin_hash2(i + float2(1.0, 1.0)), f - float2(1.0, 1.0));

    // Bilinear interpolation of gradient contributions
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
```

### 3D Perlin Noise

```metal
float3 perlin_hash3(float3 p) {
    p = float3(dot(p, float3(127.1, 311.7, 74.7)),
               dot(p, float3(269.5, 183.3, 246.1)),
               dot(p, float3(113.5, 271.9, 124.6)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

float perlinNoise3D(float3 p) {
    float3 i = floor(p);
    float3 f = fract(p);

    // Quintic interpolation
    float3 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);

    // 8 corners of the cube
    float n000 = dot(perlin_hash3(i + float3(0,0,0)), f - float3(0,0,0));
    float n100 = dot(perlin_hash3(i + float3(1,0,0)), f - float3(1,0,0));
    float n010 = dot(perlin_hash3(i + float3(0,1,0)), f - float3(0,1,0));
    float n110 = dot(perlin_hash3(i + float3(1,1,0)), f - float3(1,1,0));
    float n001 = dot(perlin_hash3(i + float3(0,0,1)), f - float3(0,0,1));
    float n101 = dot(perlin_hash3(i + float3(1,0,1)), f - float3(1,0,1));
    float n011 = dot(perlin_hash3(i + float3(0,1,1)), f - float3(0,1,1));
    float n111 = dot(perlin_hash3(i + float3(1,1,1)), f - float3(1,1,1));

    // Trilinear interpolation
    float n00 = mix(n000, n100, u.x);
    float n01 = mix(n001, n101, u.x);
    float n10 = mix(n010, n110, u.x);
    float n11 = mix(n011, n111, u.x);
    float n0 = mix(n00, n10, u.y);
    float n1 = mix(n01, n11, u.y);

    return mix(n0, n1, u.z);
}
```

---

## Simplex Noise {#simplex}

Faster than Perlin with fewer axis-aligned artifacts. Uses a simplex grid (triangles in 2D, tetrahedra in 3D) instead of a square/cube grid.

### 2D Simplex Noise

```metal
// Simplex noise by Ashima Arts (ported to MSL)
float3 mod289_3(float3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float2 mod289_2(float2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float3 permute(float3 x) { return mod289_3(((x * 34.0) + 1.0) * x); }

float simplexNoise2D(float2 v) {
    const float4 C = float4(
        0.211324865405187,   // (3.0 - sqrt(3.0)) / 6.0
        0.366025403784439,   // 0.5 * (sqrt(3.0) - 1.0)
       -0.577350269189626,   // -1.0 + 2.0 * C.x
        0.024390243902439    // 1.0 / 41.0
    );

    // First corner
    float2 i = floor(v + dot(v, C.yy));
    float2 x0 = v - i + dot(i, C.xx);

    // Other corners
    float2 i1 = (x0.x > x0.y) ? float2(1.0, 0.0) : float2(0.0, 1.0);
    float4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    // Permutations
    i = mod289_2(i);
    float3 p = permute(permute(i.y + float3(0.0, i1.y, 1.0))
                                     + i.x + float3(0.0, i1.x, 1.0));

    float3 m = max(0.5 - float3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
    m = m * m;
    m = m * m;

    // Gradients
    float3 x = 2.0 * fract(p * C.www) - 1.0;
    float3 h = abs(x) - 0.5;
    float3 ox = floor(x + 0.5);
    float3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);

    // Compute final noise value
    float3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);  // Range approximately -1 to 1
}
```

### 3D Simplex Noise

```metal
float4 mod289_4(float4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float4 permute4(float4 x) { return mod289_4(((x * 34.0) + 1.0) * x); }
float4 taylorInvSqrt(float4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

float simplexNoise3D(float3 v) {
    const float2 C = float2(1.0 / 6.0, 1.0 / 3.0);
    const float4 D = float4(0.0, 0.5, 1.0, 2.0);

    // First corner
    float3 i = floor(v + dot(v, C.yyy));
    float3 x0 = v - i + dot(i, C.xxx);

    // Other corners
    float3 g = step(x0.yzx, x0.xyz);
    float3 l = 1.0 - g;
    float3 i1 = min(g.xyz, l.zxy);
    float3 i2 = max(g.xyz, l.zxy);

    float3 x1 = x0 - i1 + C.xxx;
    float3 x2 = x0 - i2 + C.yyy;
    float3 x3 = x0 - D.yyy;

    // Permutations
    i = mod289_3(i);
    float4 p = permute4(permute4(permute4(
        i.z + float4(0.0, i1.z, i2.z, 1.0))
      + i.y + float4(0.0, i1.y, i2.y, 1.0))
      + i.x + float4(0.0, i1.x, i2.x, 1.0));

    // Gradients (7x7 points over a square mapped onto an octahedron)
    float n_ = 0.142857142857;
    float3 ns = n_ * D.wyz - D.xzx;

    float4 j = p - 49.0 * floor(p * ns.z * ns.z);

    float4 x_ = floor(j * ns.z);
    float4 y_ = floor(j - 7.0 * x_);

    float4 x = x_ * ns.x + ns.yyyy;
    float4 y = y_ * ns.x + ns.yyyy;
    float4 h = 1.0 - abs(x) - abs(y);

    float4 b0 = float4(x.xy, y.xy);
    float4 b1 = float4(x.zw, y.zw);

    float4 s0 = floor(b0) * 2.0 + 1.0;
    float4 s1 = floor(b1) * 2.0 + 1.0;
    float4 sh = -step(h, float4(0.0));

    float4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
    float4 a1 = b1.xzyw + s1.xzyw * sh.zzww;

    float3 p0 = float3(a0.xy, h.x);
    float3 p1 = float3(a0.zw, h.y);
    float3 p2 = float3(a1.xy, h.z);
    float3 p3 = float3(a1.zw, h.w);

    // Normalize gradients
    float4 norm = taylorInvSqrt(float4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;

    // Mix contributions
    float4 m = max(0.6 - float4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot(m * m, float4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
}
```

---

## Worley / Voronoi Noise {#worley}

Cellular noise based on distance to the nearest random feature point in a grid.

```metal
// 2D Worley noise
// Returns float2: x = distance to nearest, y = distance to second nearest
float2 worleyNoise2D(float2 p) {
    float2 i = floor(p);
    float2 f = fract(p);

    float d1 = 1e10;  // nearest
    float d2 = 1e10;  // second nearest

    // Search 3x3 neighborhood
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            float2 neighbor = float2(float(x), float(y));
            // Random point in neighboring cell
            float2 point = perlin_hash2(i + neighbor) * 0.5 + 0.5;  // reuse hash
            float2 diff = neighbor + point - f;
            float dist = length(diff);

            if (dist < d1) {
                d2 = d1;
                d1 = dist;
            } else if (dist < d2) {
                d2 = dist;
            }
        }
    }

    return float2(d1, d2);
}

// Variations:
// d1           -> cell shape (smooth bumps)
// d2 - d1      -> cell edges / crack patterns
// d1 * d2      -> interesting organic patterns
// d2           -> inverted cell pattern

// 3D Worley noise
float2 worleyNoise3D(float3 p) {
    float3 i = floor(p);
    float3 f = fract(p);

    float d1 = 1e10;
    float d2 = 1e10;

    for (int z = -1; z <= 1; z++) {
        for (int y = -1; y <= 1; y++) {
            for (int x = -1; x <= 1; x++) {
                float3 neighbor = float3(float(x), float(y), float(z));
                float3 point = perlin_hash3(i + neighbor) * 0.5 + 0.5;
                float3 diff = neighbor + point - f;
                float dist = length(diff);

                if (dist < d1) {
                    d2 = d1;
                    d1 = dist;
                } else if (dist < d2) {
                    d2 = dist;
                }
            }
        }
    }

    return float2(d1, d2);
}
```

---

## Fractal Brownian Motion (fBm) {#fbm}

Layer multiple octaves of noise at increasing frequency and decreasing amplitude for natural-looking complexity.

```metal
// Generic fBm -- works with any noise function
// Parameters:
//   octaves:    number of layers (4-8 typical)
//   lacunarity: frequency multiplier per octave (2.0 typical)
//   gain:       amplitude multiplier per octave (0.5 typical, aka persistence)

float fbm2D(float2 p, int octaves, float lacunarity, float gain) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int i = 0; i < octaves; i++) {
        value += amplitude * perlinNoise2D(p * frequency);
        frequency *= lacunarity;
        amplitude *= gain;
    }
    return value;
}

float fbm3D(float3 p, int octaves, float lacunarity, float gain) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int i = 0; i < octaves; i++) {
        value += amplitude * perlinNoise3D(p * frequency);
        frequency *= lacunarity;
        amplitude *= gain;
    }
    return value;
}

// Ridged multifractal: absolute value creates ridge-like features
float ridgedFbm3D(float3 p, int octaves, float lacunarity, float gain) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    float prev = 1.0;

    for (int i = 0; i < octaves; i++) {
        float n = 1.0 - abs(perlinNoise3D(p * frequency));
        n = n * n;       // sharpen ridges
        n *= prev;       // ridge weighting
        prev = n;
        value += amplitude * n;
        frequency *= lacunarity;
        amplitude *= gain;
    }
    return value;
}

// Turbulence: absolute value of noise creates billowy patterns
float turbulence3D(float3 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int i = 0; i < octaves; i++) {
        value += amplitude * abs(perlinNoise3D(p * frequency));
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```

### Configuring fBm for Different Effects

| Effect | Octaves | Lacunarity | Gain | Notes |
|--------|---------|------------|------|-------|
| Clouds | 5-8 | 2.0 | 0.5 | Standard fBm |
| Terrain | 6-10 | 2.0 | 0.5 | Higher octaves for detail |
| Marble | 4 | 2.0 | 0.5 | `sin(x + fbm(p))` for veins |
| Wood | 3-4 | 2.0 | 0.5 | `sin(sqrt(x^2+z^2) + fbm(p))` for rings |
| Fire | 4-6 | 2.0 | 0.5 | Ridged + scroll UV upward over time |
| Water | 4-6 | 2.0 | 0.45 | Domain warp + animate time offset |
| Rough surface | 3-4 | 3.0 | 0.4 | Higher lacunarity for grit |

---

## Domain Warping {#domain-warping}

Feed noise output back as input coordinates to another noise function. Creates organic, fluid distortions.

```metal
// Single-level warp
float warpedNoise(float2 p, float time) {
    float2 q = float2(
        fbm2D(p + float2(0.0, 0.0), 4, 2.0, 0.5),
        fbm2D(p + float2(5.2, 1.3), 4, 2.0, 0.5)
    );

    return fbm2D(p + 4.0 * q + float2(time * 0.1), 4, 2.0, 0.5);
}

// Double-level warp (more organic, more expensive)
float doubleWarpedNoise(float2 p, float time) {
    float2 q = float2(
        fbm2D(p + float2(0.0, 0.0), 4, 2.0, 0.5),
        fbm2D(p + float2(5.2, 1.3), 4, 2.0, 0.5)
    );

    float2 r = float2(
        fbm2D(p + 4.0 * q + float2(1.7, 9.2) + float2(time * 0.15), 4, 2.0, 0.5),
        fbm2D(p + 4.0 * q + float2(8.3, 2.8) + float2(time * 0.126), 4, 2.0, 0.5)
    );

    return fbm2D(p + 4.0 * r, 4, 2.0, 0.5);
}

// SwiftUI stitchable example: animated domain warp
[[ stitchable ]] half4 domain_warp_effect(
    float2 position,
    half4 color,
    float2 size,
    float time
) {
    float2 uv = position / size;
    float warp = doubleWarpedNoise(uv * 3.0, time);

    // Map noise to color palette
    half3 col1 = half3(0.1h, 0.2h, 0.5h);  // deep blue
    half3 col2 = half3(0.8h, 0.4h, 0.1h);  // warm orange
    half3 col3 = half3(0.1h, 0.6h, 0.3h);  // green

    half t = half(warp * 0.5 + 0.5);
    half3 result = mix(col1, col2, smoothstep(0.0h, 0.5h, t));
    result = mix(result, col3, smoothstep(0.5h, 1.0h, t));

    return half4(result, 1.0h);
}
```

---

## Texture-Based Noise vs Computed {#performance}

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Computed** (above functions) | No texture memory, tileable at any scale, animated easily | ALU-heavy, complex implementations | Animated noise, procedural worlds, parameters change per frame |
| **Texture lookup** (precomputed) | Single texture sample per noise call, trivial implementation | Texture memory, tiling visible at close range, static | Static noise patterns, normal maps, terrain heightmaps |

### Texture-Based Noise Lookup

```swift
// Swift: create noise texture
func createNoiseTexture(device: MTLDevice, size: Int = 256) -> MTLTexture {
    let desc = MTLTextureDescriptor.texture2DDescriptor(
        pixelFormat: .r32Float, width: size, height: size, mipmapped: true
    )
    desc.usage = [.shaderRead]
    let texture = device.makeTexture(descriptor: desc)!

    var data = [Float](repeating: 0, count: size * size)
    for i in 0..<data.count {
        data[i] = Float.random(in: 0...1)  // Or use computed Perlin
    }
    texture.replace(
        region: MTLRegionMake2D(0, 0, size, size),
        mipmapLevel: 0,
        withBytes: &data,
        bytesPerRow: size * MemoryLayout<Float>.stride
    )
    return texture
}
```

```metal
// MSL: sample noise from texture (much cheaper per call)
float textureNoise(float2 uv, texture2d<float> noiseTex, sampler s) {
    return noiseTex.sample(s, uv).r;
}

float textureFbm(float2 uv, texture2d<float> noiseTex, sampler s, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < octaves; i++) {
        value += amplitude * textureNoise(uv * frequency, noiseTex, s);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```
