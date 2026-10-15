---
name: shader-starter
description: Build a Figma shader fill or shader effect from a standing start, as a guided series of prompts. Optionally creates a looping Phase control for Figma Motion, then writes main.ts, features.json, and a product brief. Use in Figma Agent when asked to make a shader, grain, glow, distortion, or similar effect.
---

Run this as a **series of prompts**, in order. Ask one question, wait for the answer, act,
then move to the next. Do not batch questions or skip actions.

There are two prompts (**P1–P2**) and four actions (**A1–A4**).

---

## P1 — What are we building?

Ask, verbatim:

> **What kind of effect?** One line on the look you're after — grain, halftone, distortion, colour shift, glow, etc.

Wait for the answer.

This is a **shader effect** — it samples the layer's existing pixels and transforms them.
On an empty layer it renders nothing, so check there is something underneath. If the layer
is empty, mention that the effect needs content to work on.

Everything after this is grounded in their one-line brief.

---

## P2 — Recommend controls, confirm, and go

Based on the brief, recommend a control set that balances output quality with ease of use.
Let the effect's complexity determine the count.

### Phase — only when the user wants Figma Motion animation

**Phase is not a default control.** Include it only when the user explicitly wants the effect
to animate — i.e. they plan to use **Figma Motion keyframes** to drive the shader through a
looping cycle.

Ask the user:

> **Should this effect animate?** If you want to loop it with Figma Motion keyframes, I'll
> add a **Phase** control. Otherwise I'll leave it out and the effect stays static.

If they say **yes** (or the brief already implies animation — "pulsing", "scanning",
"drifting", "looping", etc.), include Phase:

```ts
"offset": {
  type: "number",
  label: "Phase",
  defaultValue: 0,
  control: "slider",
  min: 0, max: 100, step: 0.1,
},
```

```wgsl
let PI = 3.14159265;
let phase = offset / 100.0 * 2.0 * PI;   // 0 .. TAU across the slider
```

Set `"isAnimated": true` in `features.json`.

Route **every** animated term through `phase`, never through `frame.time`.

**How Phase works with Figma Motion:** The designer keyframes the Phase slider from 0 → 100
in Motion. Because the shader maps 0–100 to a full 0–TAU cycle, the animation loops
seamlessly — the end state is identical to the start state. This is what makes Phase
essential for looping: it gives Motion a single scrub-able value that drives all animated
terms in lockstep.

If they say **no**, omit Phase entirely. Set `"isAnimated": false` in `features.json`.
The shader will be a static effect controlled only by its look properties.

### Include on-canvas controls when they fit

If the effect has a spatial property — an origin, direction, focal point, or centre — include
an on-canvas control without asking. It replaces multiple sliders and is more intuitive for
spatial parameters.

| Effect shape | On-canvas control | `type` |
|---|---|---|
| Directional (scan lines, waves, motion blur) | Transform | `"point-angle-radius"` |
| Radial (vignette, glow, ripple) | Transform or Circle | `"point-angle-radius"` or `"circle"` |
| Single hotspot (light, focal point) | Point | `"point"` |

Use `mode: "canvas_and_ui"` so the handle appears on canvas **and** keeps numeric fields in
the panel:

```ts
"transform": {
  type: "point-angle-radius",
  label: "Transform",
  defaultValue: { x: 50, y: 50, angle: 0, radius: 30 },
  mode: "canvas_and_ui",
  positionUnit: "%",
  radiusUnit: "%",
},
```

Note: `"point-angle-radius"` with `mode: "canvas_and_ui"` and `%` units is **confirmed** from
real shader source. `"point"` and `"circle"` are inferred from the plugin API union — if
picking one of those, read a library shader that uses it first, or default to Transform.

If the effect has no spatial property, skip it — don't force one in.

### Pick the remaining controls

Choose from confirmed control types only:

| Control | `type` | Good for |
|---|---|---|
| Slider | `"number"` + `control: "slider"` | Continuous values — amount, scale, intensity |
| Colour | `"color"` | Tint, overlay, palette |
| Stepper | `"number"` + `step: 1` | Integer counts — octaves, rings, cells |
| Composite bar | `"number"` + `control: "slider"` | One slider driving multiple correlated uniforms |

For unconfirmed types (toggle, segmented picker, etc.), read a real shader with
`list_shader_fills` + `get_shader_fill` and copy the exact `type` string, or pick a confirmed
type instead. **Do not guess a type string.**

### Scaling controls to complexity

The right number of controls depends on the effect:

| Complexity | Example effects | Typical control count (excl. Phase) |
|---|---|---|
| Simple | Grain, tint, vignette | 2–3 |
| Medium | Halftone, pixelate, glow, colour shift | 3–5 |
| Complex | CRT, chromatic aberration + bloom, glass, multi-layer distortion | 5–8 |

If Phase is included, add 1 to the count above.

Complex effects deserve more controls because their look has more independent axes. A CRT
effect might reasonably expose: Phase, Transform, Scan Line Frequency, Scan Line Intensity,
Curvature, RGB Split, Bloom, Colour Temperature, and Vignette Falloff — that's 9, and each
one does something visibly different.

**Guiding principles:**
- Every control should be **visible** (moving it obviously changes the look), **independent**
 (not a second name for something already exposed), and **named in the designer's language**
 ("softness", not "sigma").
- Use **composite bars** when properties are genuinely correlated — but don't over-fold.
 If a designer would reasonably want to set bloom and curvature independently, give them
 separate controls even in the same effect.
- Leave out internal constants and anything with one right answer.
- Take values as **percentages of the frame** and convert in `render`, so the shader is
 resolution-independent.
- The **signature amount** — the one property that *is* the look (grain amount, dot size,
 warp strength, RGB split) — always gets its own control.

### Present and confirm

Present your recommendation as a single list, then ask:

> Here's what I'd build: ** **, ** **, and
> ** **. Want to adjust anything, or shall I build it?

Wait for the answer, then proceed to A1.

---

## A1 — Write the three files

| File | Contents |
|---|---|
| `main.ts` | WGSL string, `setup`, `render`, `defineProperties` |
| `features.json` | `{ name, version, isAnimated, usesMouse }` |
| `product-brief.md` | id, displayName, kind (effect), description, the original prompt |

`main.ts` imports `defineProperties` from `"figma:shaders"` and calls it on the default
export. **Not PropsKit** — PropsKit is for generative plugins only.

### Slider ranges

Default to **normalized** ranges (`0–100`, shader remaps internally) unless the user asks
otherwise. This keeps every control intuitive and consistent.

For reference, internal remapping from normalized `t = slider / 100`:

| Uniform | Typical remap |
|---|---|
| Intensity / amount | `mix(0.0, 0.5, t)` |
| Scale / zoom | `mix(0.5, 2.0, t)` |
| Distortion / warp | `mix(0.0, 0.15, t)` |
| Noise / grain | `mix(0.0, 0.25, t)` |
| Contrast | `mix(0.75, 1.25, t)` |
| Glow / bloom | `mix(0.0, 1.0, t)` |

**Speed is always an integer stepper (only when Phase is included).** Only integer multiples
of `phase` return to the same value *and* velocity at the seam. Use `step: 1`, never a
continuous slider.

### Things that silently break a shader

- **Uniform alignment.** WGSL uniform structs pack in 16-byte groups. Group scalars in fours
 and name the leftovers `_pad0`, `_pad1`, …
- **Pipeline caching.** Rebuild the pipeline when `frame.output.format` changes; cache it
 against `frame.state.pipelineFormat`.

Open the WGSL with `diagnostic(off,derivative_uniformity);`, as the real shaders do.

---

## A2 — Verify the loop (only when Phase is included)

**Skip this step entirely if the shader is static (no Phase control).**

For every animated term, confirm it uses a loop-safe pattern:

| Pattern | Why it wraps |
|---|---|
| `sin(phase)`, `cos(phase + k)` | period TAU by definition |
| `fract(uv.x + offset / 100.0)` | `fract` is periodic with period 1 |
| rotate by `phase` | one full turn per loop |
| `noise(p + vec2(cos(phase), sin(phase)) * r)` | samples a circle, returns to its start |
| `sin(2.0 * phase)`, `sin(3.0 * phase)` | **integer** multiples re-align together |

If a term doesn't fit one of these patterns, rewrite it — or note that the loop won't be
seamless and which term breaks it.

**Value equality is not enough.** `sin(2.5 * phase)` returns to the same value while
travelling the opposite direction, so the seam visibly bounces. Both value and velocity must
match — layered speeds must be integers.

---

## A3 — Final checklist

Check each line. If any fails, fix it before reporting done.

### If animated (Phase included):
- [ ] Phase control exists in `defineProperties`, `type: "number"`, `min: 0`, `max: 100`
- [ ] `"isAnimated": true` in `features.json`
- [ ] No animated term reads `frame.time`
- [ ] Every animated term uses a loop-safe pattern
- [ ] Every speed / cycle multiplier is an **integer**

### If static (no Phase):
- [ ] `"isAnimated": false` in `features.json`
- [ ] No references to `frame.time` or `phase` anywhere in the shader

### Always:
- [ ] Every control drives a visible, independent property — no orphans
- [ ] If an on-canvas control is included, it has `mode: "canvas_and_ui"`
- [ ] Every `type` string is confirmed or copied from a real library shader
- [ ] Uniform scalars grouped in fours with explicit `_padN`
- [ ] Defaults look good before anyone touches a control

---

## A4 — Recommend starting values and things to try

After the shader is built, give the user a short **"Getting started"** section with two parts:

### Ideal starting values

Recommend a specific preset — actual slider values, not ranges — that produces a good-looking
result out of the box. Ground these in the brief: a subtle film grain should default to low
amount and fine scale, while a heavy CRT effect should default to visible scan lines and
noticeable curvature.

Format as a simple table:

> **Recommended starting point:**
>
> | Control | Value | Why |
> |---|---|---|
> | Phase | 0 | Loop start (keyframe to 100 in Motion for a full cycle) |
> | | | |
> | | | |
> | … | … | … |

(Include Phase row only if the shader is animated.)

These should be the `defaultValue` entries in the code — the shader should look good the
moment it's applied, not require tuning to get a first impression.

### Things to test out

Suggest **3–5 specific experiments** the user can try — concrete slider moves or combinations
that reveal interesting behaviour or push the effect in a different direction. Frame these as
actions, not descriptions:

> **Worth trying:**
> - Crank ** ** to 80–90 — the effect goes from subtle to dramatic and the
> starts to interact with it
> - Pull ** ** down to 10 while pushing ** ** up — gives a
>
> - Move the **Transform** handle to a corner — the effect becomes asymmetric and more
> cinematic
> - Set ** ** to 0 to isolate just the — useful for layering
> with other effects
> - Keyframe **Phase** from 0 → 100 in Motion to see the full loop cycle

Tailor these to the specific effect. They should teach the user what their controls actually
do and which combinations produce the most interesting results. If animated, include at least
one tip about keyframing Phase in Motion.

---

## Edge cases

- **User wants animation.** Include Phase, set `isAnimated: true`, and explain that they
 keyframe Phase 0 → 100 in Figma Motion to get a seamless loop.
- **User doesn't want animation.** Omit Phase, set `isAnimated: false`. The shader is purely
 static — all look, no motion.
- **Endless drift with no cycle.** Note the loop guarantee is off and why.
- **Effect on an empty layer.** Nothing to sample, nothing renders. Mention this.
- **Unconfirmed control type.** Read a real shader for the exact string instead of guessing.
- **It's actually a generative plugin.** Controls are PropsKit, not `defineProperties`.
 Confirm which before writing code.
