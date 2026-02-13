---
name: pencil
description: |
  [WHAT] Character design and illustration assistant for AI product mascots, orb avatars, and animated companions.
  [HOW] Generates text-to-image prompts, character reference sheets, animation state matrices, Lottie motion specs, and SwiftUI animation parameters. Uses "nano banana" quick-render mode for rapid 5-sample concept exploration.
  [WHEN] Use when designing mascots, avatars, orb characters, animated blobs, onboarding animations, emote sheets, or character state systems. Triggers on: "character design", "mascot", "avatar", "orb", "blob", "emote", "animation states", "reference sheet", "turnaround", "expression sheet", "ClawBuddy", "pencil", "nano banana", "character render".
  [WHY] AI products need personality through visual identity. This skill bridges the gap between concept and implementation — from prompt engineering to Lottie/SwiftUI specs.
triggers:
  - pencil
  - character design
  - mascot
  - avatar design
  - orb character
  - blob animation
  - emote sheet
  - reference sheet
  - nano banana
  - ClawBuddy
  - animation states
  - character render
  - turnaround sheet
  - expression sheet
---

# Pencil — Character Design & Illustration Assistant

## Quick Start

```
/pencil                     → Interactive mode (asks what you need)
/pencil nano <concept>      → 5 quick render prompts for <concept>
/pencil states <character>  → Full state matrix with animation specs
/pencil emotes <character>  → Emote/expression sheet prompts
/pencil onboard <steps>     → Custom animation per onboarding step
/pencil ref <character>     → Full reference sheet (turnaround + states + emotes)
/pencil lottie <state>      → Lottie-compatible motion spec
/pencil swift <state>       → SwiftUI animation parameters
```

## Decision Tree

```
What does the user need?
│
├─→ Quick concept exploration?
│   └─→ Nano Banana Mode (5 samples per concept)
│       Output: 5 text-to-image prompts with style variations
│
├─→ Character reference sheet?
│   ├─→ Turnaround (front/side/back/3-4)
│   ├─→ Expression sheet (8-12 emotions)
│   ├─→ State sheet (idle/think/speak/sleep/etc)
│   └─→ Full ref (all three combined)
│
├─→ Animation specs?
│   ├─→ Lottie JSON motion parameters
│   ├─→ SwiftUI animation code
│   └─→ State machine definition
│
├─→ Onboarding animations?
│   └─→ Per-step custom emotes + transitions
│
└─→ ClawBuddy specific?
    └─→ See ClawBuddy State Matrix below
```

## Nano Banana Mode

Quick-render 5 samples per concept. Each sample varies ONE axis while keeping the others constant.

**Axes of variation:**
1. **Style** — flat/3D/glassmorphic/pixel/watercolor
2. **Mood** — playful/serious/warm/mysterious/energetic
3. **Palette** — brand colors / monochrome / neon / pastel / dark
4. **Detail** — minimal/medium/rich/hyper/abstract
5. **Context** — isolated / in-situ / with-UI / with-hands / environmental

**Prompt template:**
```
A {style} {character_description}, {mood} mood, {palette} color palette,
{detail_level} detail, {context}, dark background, centered composition,
{additional_modifiers}. --ar 1:1 --s 250 --q 2
```

**5 samples for an orb character:**
```
Sample 1 (Style):     "A glassmorphic luminous orb with two subtle eye highlights..."
Sample 2 (Mood):      "A playful bouncing orb with warm inner glow..."
Sample 3 (Palette):   "A deep purple to electric blue gradient orb..."
Sample 4 (Detail):    "A minimal single-gradient sphere with soft shadow..."
Sample 5 (Context):   "A glowing orb floating above a dark macOS dock..."
```

## Character State Matrix

### Universal States (any character)

| State | Visual | Motion | Duration | Trigger |
|-------|--------|--------|----------|---------|
| **idle** | Resting pose, subtle breathing | Scale 0.98→1.02 | 3s ease-in-out loop | Default |
| **thinking** | Focused, internal glow intensifies | Slow orbital rotation | 2s loop | Processing request |
| **speaking** | Mouth/surface animates with amplitude | Waveform distortion | Variable (speech length) | TTS active |
| **listening** | Alert, receptive pose | Ring ripple expanding outward | 1.5s loop | Mic active |
| **sleeping** | Dimmed, minimal glow | Slow float up/down 2px | 4s ease-in-out | Idle > 5min |
| **error** | Red flash, alarmed | Shake X ±4px | 0.5s, 3 cycles | Error state |
| **bg-processing** | Pulsing accent ring | Rotating dashed border | 1s loop | Background task |
| **writing** | Pen/cursor indicator | Bounce dots (typing indicator) | 0.6s loop | Generating text |
| **researching** | Magnifying glass overlay | Scan left→right sweep | 2s loop | Search/fetch |
| **celebrating** | Bright, expanded, particles | Scale up 1.2x + confetti burst | 1.5s one-shot | Task complete |
| **connecting** | Pulsing connection rings | Concentric circles expand | 1s loop | WebSocket connecting |
| **warning** | Amber glow | Gentle pulse faster than idle | 1.5s loop | Non-critical alert |

## ClawBuddy — Kingly's Orb Mascot

### Identity

ClawBuddy is a **luminous orb** — a miniature sun with personality. Not a face, not a mascot body. A living sphere of light with two subtle "eye" highlights that convey emotion through glow, scale, and motion.

### ClawBuddy Nano Banana (5 Samples)

```
SAMPLE 1 — Glassmorphic Orb
"A glassmorphic translucent orb with soft inner purple-to-blue gradient,
two small white circular highlights as eyes, floating with subtle shadow
beneath, dark UI background, macOS-native feel, minimal, 48px diameter
equivalent. --ar 1:1 --s 250"

SAMPLE 2 — Warm Glow Orb
"A warm glowing sphere with deep indigo core fading to electric violet
edges, two bright dot eyes, soft ambient light casting on surface below,
cozy and approachable, dark theme, app icon style. --ar 1:1 --s 250"

SAMPLE 3 — Neon Pulse Orb
"A neon-accented energy orb, electric blue with magenta rim light,
two floating eye sparkles, cyberpunk-minimal style, slight motion blur
suggesting vibration, pure black background. --ar 1:1 --s 250"

SAMPLE 4 — Plushcore Orb
"A soft plushcore spherical character, matte purple with subtle fuzz
texture, two simple dot eyes, kawaii-minimal, sitting on a reflective
dark surface, gentle studio lighting. --ar 1:1 --s 250"

SAMPLE 5 — In-Situ macOS
"A small glowing purple orb avatar sitting in the bottom-right corner
of a macOS desktop screenshot, dark mode, subtle glow illuminating
nearby dock icons, two tiny eye highlights, ambient and unobtrusive.
--ar 16:9 --s 200"
```

### ClawBuddy State Sheet Prompts

```
IDLE:       "Glowing orb, slow breathing pulse, two relaxed eye dots,
             soft purple gradient, ambient shadow, peaceful. --ar 1:1"

THINKING:   "Glowing orb with intensified inner light, eyes squinted
             slightly, orbital ring rotating around it, contemplative
             amber-purple tint. --ar 1:1"

SPEAKING:   "Glowing orb with waveform ripples on surface, eyes wide
             and bright, audio visualization rings emanating outward,
             vibrant purple-blue. --ar 1:1"

LISTENING:  "Glowing orb with expanded glow radius, eyes attentive
             and upward, subtle ear-like antenna glow, receptive
             blue-purple tint. --ar 1:1"

SLEEPING:   "Dimmed orb, eyes as tiny crescents (closed), minimal glow,
             small 'z' particles floating up, deep navy tint. --ar 1:1"

ERROR:      "Orb flashing red-orange, eyes as exclamation marks,
             cracked light effect on surface, alarm state. --ar 1:1"

BG-PROCESS: "Orb with spinning dashed ring around it, eyes focused
             downward, progress-bar-like accent ring, busy but calm
             teal-purple. --ar 1:1"

WRITING:    "Orb with tiny pen/cursor trail, eyes focused left-to-right,
             text particles streaming from bottom, creative purple-green
             gradient. --ar 1:1"

RESEARCHING:"Orb with magnifying glass overlay glow, eyes scanning
             left-to-right, data particle streams flowing in, curious
             blue-cyan tint. --ar 1:1"
```

### Onboarding Emotes

| Step | Emote | ClawBuddy Treatment | Prompt Modifier |
|------|-------|---------------------|-----------------|
| **Welcome** | Wave | Orb bounces side-to-side, sparkle trail | "friendly bounce, sparkle particles trailing" |
| **AI Provider** | Thinking | Orb shows rotating options around it | "orbiting icons (brain, chip, cloud) around orb" |
| **API Key** | Secure Lock | Orb wraps in a shield/lock glow | "golden shield aura, lock icon overlay, secure" |
| **Permissions** | Handshake | Two orbs meeting, light bridge between | "two orbs connected by light beam, trust" |
| **Connected** | Celebration | Orb expands with confetti burst | "scale up, confetti particles, rainbow rim light" |

## SwiftUI Animation Specs

See `references/swiftui-animations.md` for full code snippets.

### Quick Reference

```swift
// Idle breathing
.scaleEffect(isIdle ? 0.98 : 1.02)
.animation(.easeInOut(duration: 3).repeatForever(autoreverses: true), value: isIdle)

// Thinking rotation
.rotationEffect(.degrees(isThinking ? 360 : 0))
.animation(.linear(duration: 2).repeatForever(autoreverses: false), value: isThinking)

// Error shake
.offset(x: isError ? -4 : 0)
.animation(.default.repeatCount(3, autoreverses: true).speed(4), value: isError)

// Speaking waveform (amplitude-driven)
.scaleEffect(1.0 + audioLevel * 0.15)
.animation(.spring(response: 0.1, dampingFraction: 0.5), value: audioLevel)

// Celebration burst
.scaleEffect(isCelebrating ? 1.3 : 1.0)
.animation(.spring(response: 0.4, dampingFraction: 0.5), value: isCelebrating)
```

## Lottie Motion Specs

See `references/lottie-specs.md` for full JSON templates.

### Motion Parameters Quick Ref

| State | Property | From | To | Duration | Easing |
|-------|----------|------|-----|----------|--------|
| idle | scale | 0.98 | 1.02 | 3000ms | ease-in-out |
| idle | opacity | 0.85 | 1.0 | 3000ms | ease-in-out |
| thinking | rotation | 0 | 360 | 2000ms | linear |
| thinking | innerGlow | 0.6 | 1.0 | 1000ms | ease-in-out |
| speaking | scaleX | 1.0 | 1.0+amp*0.15 | 100ms | spring |
| speaking | scaleY | 1.0 | 1.0+amp*0.1 | 100ms | spring |
| listening | ringScale | 1.0 | 1.8 | 1500ms | ease-out |
| listening | ringOpacity | 0.8 | 0.0 | 1500ms | ease-out |
| sleeping | translateY | 0 | -2 | 4000ms | ease-in-out |
| sleeping | opacity | 1.0 | 0.6 | 2000ms | ease-in-out |
| error | translateX | -4 | 4 | 167ms | ease-in-out (x3) |
| error | fill | current | #FF4444 | 200ms | ease-in |
| bg-process | dashOffset | 0 | 100 | 1000ms | linear |
| writing | dotScale (3) | 0.5 | 1.0 | 200ms | staggered 100ms |
| researching | scanX | -50% | 50% | 2000ms | ease-in-out |
| celebrating | scale | 1.0 | 1.3 | 400ms | spring(0.5) |
| celebrating | particles | emit | fade | 1500ms | ease-out |

## Reference Sheet Template

For a full character reference sheet, generate prompts for:

1. **Turnaround** (4 views): Front, 3/4, Side, Back
2. **Expression Sheet** (8-12 emotions): Happy, Sad, Angry, Surprised, Confused, Excited, Tired, Focused, Mischievous, Proud, Embarrassed, Determined
3. **State Sheet** (see state matrix above)
4. **Size/Scale Reference**: In-context with UI elements
5. **Color Palette**: Primary gradient, accent, glow, shadow

**Turnaround prompt template:**
```
Character turnaround reference sheet of {character}, {4 views: front,
three-quarter, side, back}, consistent style, white guidelines,
clean background, professional character design sheet. --ar 16:9
```

## Prior Art & References

- See `references/prior-art.md` for curated links
- See `references/swiftui-animations.md` for full SwiftUI code
- See `references/lottie-specs.md` for Lottie JSON templates
- See `references/prompt-library.md` for expanded prompt collection
## Technique Map

- **Nano Banana mode** — 5 samples per concept; vary one axis (style, mood, palette, detail, context); because rapid exploration without over-commitment.
- **Character state matrix** — idle, thinking, speaking, listening, sleeping, error, bg-process, writing, researching, celebrating, etc.; because states drive animation and visual consistency.
- **Prompt template with axes** — {style} {character_description}, {mood} mood, {palette} palette; because structured variation produces comparable samples.
- **Lottie motion specs** — Property, from, to, duration, easing per state; because design-to-implementation handoff needs precise parameters.
- **SwiftUI animation quick ref** — scaleEffect, rotationEffect, offset for state transitions; because developers need copy-paste snippets.

## Technique Notes

ClawBuddy = luminous orb with two eye highlights. Turnaround: 4 views. Expression sheet: 8-12 emotions. References: prior-art.md, swiftui-animations.md, lottie-specs.md. Related: orb (implementation), swiftui-animation (broader patterns).

---

## Prompt Architect Overlay

**Role Definition:** Character design and illustration assistant for AI product mascots, orb avatars, animated companions. Generates prompts, reference sheets, animation specs, Lottie/SwiftUI parameters.

**Input Contract:** Accepts /pencil, /pencil nano <concept>, /pencil states <character>, /pencil ref <character>, character design request, or mascot/avatar keyword. Concept or character name.

**Output Contract:** Nano: 5 text-to-image prompts (one axis varied each). States: state matrix with prompts and motion params. Ref: turnaround + expression + state sheet prompts. Lottie/SwiftUI: JSON or code snippets. ClawBuddy-specific when applicable.

**Edge Cases & Fallbacks:** If concept vague→interactive mode; ask what's needed. If ClawBuddy→use identity (luminous orb, two eyes). If animation spec needed→route to swiftui-animations.md or lottie-specs.md. If implementation→route to orb skill.
