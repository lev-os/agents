# Existing Implementation — OCMiniOrb

## File Paths

| File | Purpose |
|------|---------|
| `packages/uikit/Sources/OCDesignKit/Components/OCMiniOrb.swift` | 6-layer composited orb view |
| `apps/storybook/Sources/Shared/MiniOrbPage.swift` | Storybook showcase page |
| `docs/ux/orb/mini-clawd-spec.md` | Visual spec + 5-axis nano banana prompts |
| `packages/uikit/Sources/OCDesignKit/Theme/OCColors.swift` | Color tokens |

## OrbDisplayState

```swift
public enum OrbDisplayState: String, CaseIterable, Identifiable, Sendable {
    case idle, thinking, speaking, listening

    public var gradientStart: Color { ... } // OCColors.voiceOrb{State}Start
    public var gradientEnd: Color { ... }   // OCColors.voiceOrb{State}End
}
```

## Layer-by-Layer Modification Guide

### Layer 1: Ambient Glow
- **What:** RadialGradient circle at 1.3x size, blurred by `size * 0.25`
- **Modify opacity range:** Change `glowPulse ? 0.35 : 0.2` (line ~100)
- **Modify glow size:** Change `endRadius: s * 0.65` and `frame: s * 1.3`
- **Add color cycling:** Replace static gradient with TimelineView + hue shift (T4)

### Layer 2: Base Orb
- **What:** RadialGradient at 1.0x with off-center highlight (0.35, 0.3)
- **Audio reactive:** `scaleEffect(1.0 + audioLevel * 0.08)` in speaking state
- **Modify breathe range:** Change `1.02 : 0.98` values in `baseScale`
- **Add mesh gradient:** Replace RadialGradient with MeshGradient(width:2, height:2, ...) (T1)

### Layer 3: Fractal Overlay
- **What:** Canvas with 6 Fibonacci-count rings (5, 8, 13, 8, 5, 3 dots)
- **Only rendered in:** `.thinking` and `.speaking` states
- **Modify density:** Change `ringCounts = [5, 8, 13, 8, 5, 3]`
- **Modify speed:** Change `0.4 + Double(ring) * 0.15`
- **Add swirl:** Apply spiral path offset: `ringRadius * (1 + 0.1 * sin(now * 0.5 + phase))`

### Layer 4: Glass
- **What:** RadialGradient with ultraThinMaterial at 0.85x
- **Modify frost:** Change `.ultraThinMaterial.opacity(0.15)` — higher = more frosted
- **Modify highlight position:** Change center `.init(x: 0.35, y: 0.3)`

### Layer 5: Smoke/Vapor
- **What:** 4 blurred circles orbiting center in Canvas
- **Modify orbit speed:** Change `[3.0, 4.5, 5.0, 6.0]` array
- **Modify blob size:** Change `[0.22, 0.18, 0.20, 0.16]` array
- **Add temperature:** Use warm/cool colors based on state instead of `state.gradientStart`

### Layer 6: Eye Highlights
- **What:** 2 white circles (0.12x + 0.07x) with offset positioning
- **Thinking dim:** `opacity(state == .thinking ? 0.4 : 0.8)`
- **Add blinking:** Animate opacity to 0 briefly every 3-5 seconds
- **Known gotcha:** `.offset()` does NOT move hit-test area (see CLAUDE.md)

## Adding a New State

1. Add case to `OrbDisplayState` enum
2. Add `gradientStart`/`gradientEnd` colors
3. Add color tokens to `OCColors` (voiceOrb{NewState}Start/End)
4. Update `baseScale` computed property
5. Update `startAnimations()` switch
6. Update fractal conditional: `if state == .thinking || state == .speaking || state == .newState`
7. Add storybook preview in `MiniOrbPage`

## 5-Axis Design System (from spec)

| Axis | Low | High |
|------|-----|------|
| Fractal Density | 3 rings, 3-5 dots | 8 rings, 8-21 dots |
| Blur Radius | < 2px (crisp) | > size*0.4 (dreamy) |
| Glass Coverage | 0.05 opacity, 0.5x | 0.3 opacity, 0.95x |
| Eye Proportion | 0.08x + 0.04x (subtle) | 0.18x + 0.10x (kawaii) |
| Smoke Temperature | Blue-violet (cool) | Amber-rose (warm) |
