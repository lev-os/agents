---
name: algorithmic-art
description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration.
---

Algorithmic philosophies are computational aesthetic movements expressed through code. Output .md files (philosophy), .html files (interactive viewer), and .js files (generative algorithms).

## Two-Step Process

1. **Algorithmic Philosophy Creation** (.md file)
2. **Express by creating p5.js generative art** (.html + .js files)

## Philosophy Creation

Create an ALGORITHMIC PHILOSOPHY interpreted through:
- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation and controlled chaos

### Name the Movement (1-2 words)
"Organic Turbulence" / "Quantum Harmonics" / "Emergent Stillness"

### Articulate the Philosophy (4-6 paragraphs)
Express how this philosophy manifests through:
- Computational processes and mathematical relationships
- Noise functions and randomness patterns
- Particle behaviors and field dynamics
- Temporal evolution and system states
- Parametric variation and emergent complexity

## Philosophy Examples

**"Organic Turbulence"**
Philosophy: Chaos constrained by natural law, order emerging from disorder.
Expression: Flow fields driven by layered Perlin noise. Thousands of particles following vector forces, their trails accumulating into organic density maps.

**"Quantum Harmonics"**
Philosophy: Discrete entities exhibiting wave-like interference patterns.
Expression: Particles initialized on a grid, each carrying a phase value. When near, phases interfere - constructive creates bright nodes, destructive creates voids.

**"Recursive Whispers"**
Philosophy: Self-similarity across scales, infinite depth in finite space.
Expression: Branching structures that subdivide recursively. L-systems generate tree-like forms that feel both mathematical and organic.

## P5.js Implementation

**Seeded Randomness (Art Blocks Pattern)**:
```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

**Parameter Structure**:
```javascript
let params = {
  seed: 12345,
  // Add parameters that control YOUR algorithm:
  // - Quantities, Scales, Probabilities
  // - Ratios, Angles, Thresholds
};
```

## Craftsmanship Requirements

- **Balance**: Complexity without visual noise, order without rigidity
- **Color Harmony**: Thoughtful palettes, not random RGB values
- **Composition**: Even in randomness, maintain visual hierarchy
- **Reproducibility**: Same seed ALWAYS produces identical output

## Output Format

1. **Algorithmic Philosophy** - Markdown explaining the generative aesthetic
2. **Single HTML Artifact** - Self-contained interactive generative art