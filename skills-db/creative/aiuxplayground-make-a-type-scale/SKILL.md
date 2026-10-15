---
name: make-a-type-scale
description: Build a type scale from selected text as a guided series of prompts. Offers modular ratios, 4/8px grid-snapped scales, and platform presets, then can create FLOAT variables and a specimen table on the canvas.
---

# Make a type scale

Turn one selected piece of text into a full scale: a breakdown in chat, a specimen table on the
canvas, and optionally variables for every size and line height.

Run this as a **series of prompts**. Ask one question, wait for the answer, act, then move on.
Do not batch the questions and do not skip an action.

Six prompts (**P1–P6**, one with a follow-up **P2b**) and five actions (**A1–A5**), interleaved:

`P1 → P2 → (P2b) → P3 → A1 → A2 → P4 → P5 → A3 → P6 → A4 → A5`

**Every prompt offers numbered options, and every prompt stops.** Post the question, then wait
for a reply. Do not ask two questions in one message, do not answer your own question, and do not
guess when a reply is ambiguous — ask again, more narrowly.

**A2 comes before P4 on purpose.** Show the numbers, then ask whether to tokenise them. Nobody
can sensibly decide to commit a scale to variables before they have seen what it produces.

**A4 is itself six passes, in order: measure, compute, frame, header, rows, verify.** Every
dimension in the table is computed in pass 2 and only applied afterwards. Nothing about the layout
is decided while nodes are being created, because that is what made the old table come out
differently every run.

## When to use

- The user asks for a type scale, type ramp, typographic scale or heading sizes.
- The user has selected text and wants a system built from it.
- The user asks for font-size variables or type tokens.
- The user names a ratio or a system — "golden ratio scale", "Tailwind sizes", "minor third".
- Do **not** restyle existing text — this produces a breakdown, a specimen and optionally
  variables, and changes nothing already on the canvas.

---

## P1 — Confirm the base

Resolve the selection first. All four cases happen:

| Selection | Do this |
|---|---|
| Nothing selected | Ask them to select some text. **Stop.** |
| No `TEXT` node in the selection | Say what they selected instead, ask for text. **Stop.** |
| Exactly one `TEXT` node | Use it |
| Several `TEXT` nodes | **Do not pick for them.** List each by name and size, numbered, and ask which one. **Stop.** |

A text node nested inside a frame or group is fine — use the **text node**, not its container.

Read the font **from the node**, never assume Inter:

```js
const seg = node.getStyledTextSegments(["fontName", "fontSize"]);
```

`fontName` or `fontSize` coming back as `figma.mixed` means more than one style — use the first
segment and say so, or ask if the segments differ a lot.

Ask, verbatim:

> Base is ** ** at ** px**, taken from your selection — that becomes the body
> size.
>
> 1. Use ** px** *(default)*
> 2. A different size — tell me the number
>
> Reply `1`, or just give me a size.

**Wait.** Do not compute anything until the base is settled.

---

## P2 — Which scale?

**If they already named one in their opening message** — "golden ratio", "perfect fourth",
"Tailwind", "8px grid" — take it, skip this prompt, and say which one you took.

Otherwise, ask verbatim:

> Which scale? Reply with a number.
>
> **Modular — one ratio, compounding**
> 1. Major second `1.125` — dense UI, many usable steps
> 2. **Fifth root of two `1.1487`** — the classical one; largest step exactly double the body *(default)*
> 3. Minor third `1.2` — the safe middle
> 4. Perfect fourth `1.333` — editorial, strong hierarchy
> 5. Golden ratio `1.618` — display and marketing
>
> **Other shapes**
> 6. **Grid-snapped** — a modular scale rounded to a 4 or 8px grid
> 7. **Platform preset** — Tailwind, Material 3, Apple HIG or IBM Carbon
> 8. **Split** — a tight ratio for body, a looser one for display
>
> Or name any other ratio — all twelve are available.

**Wait.** Then: **6, 7 or 8 needs the follow-up in P2b, asked as its own message.** Do not bundle
it into this one, and do not choose the grid, preset or pair of ratios yourself.

Twelve ratios live in `RATIOS`; only five are listed because a menu of twelve is worse than a
default. Match loosely — "1.5", "perfect fifth" and "fifth" all mean the same entry.

---

## P2b — Narrow it down *(only after 6, 7 or 8)*

One question, matching what they picked. Ask verbatim, then **wait**.

**If they chose 6 — grid-snapped.** The grid and the ratio are **not independent**, so ask for
both together. Only these three pairings are collision-free at every integer base from 14 to 26:

> Which grid, and which ratio under it?
>
> 1. **4px grid**, perfect fourth `1.333` — clean at any base *(default)*
> 2. **4px grid**, perfect fifth `1.5` — bigger jumps, also clean
> 3. **8px grid**, golden ratio `1.618` — 8px needs a very wide ratio to stay distinct
>
> Or name your own grid and ratio.

**The rule is a floor on the ratio: a 4px grid needs `1.333` or wider, an 8px grid needs `1.618`.**
Anything tighter collides somewhere in the normal range of base sizes. A minor third on 4px looks
fine at 16px but collides at 14, 15, 17 and 18; an augmented fourth on 8px collides at 14, 17, 18
and 19. **A tight ratio on an 8px grid is the worst case** — at a 16px base a minor third collides
on five of six steps and collapses to `8 16 24 32 40 48`, a `+8` sequence rather than a ratio.

If they ask for a tighter pairing anyway, build it and say exactly what it degenerated into.

**If they chose 7 — a platform preset:**

> Which preset?
>
> 1. **Tailwind** — 12 14 16 18 20 24 30 36 48 60 72 96
> 2. **Material 3** — 11 12 14 16 22 24 28 32 36 45 57
> 3. **Apple HIG** — 11 12 13 15 17 20 22 28 34
> 4. **IBM Carbon** — 12 14 16 20 28 32 42 54
>
> These are literal sizes, so they ignore the base — I'll still use your font. Say **rebase** if
> you want the whole preset scaled to your px base instead.

**If they chose 8 — a split scale:**

> Two ratios, and where they cross over:
>
> 1. `1.125` body / `1.333` display, crossing 2 steps up *(default)*
> 2. `1.2` body / `1.5` display, crossing 2 steps up — more dramatic headings
> 3. `1.125` body / `1.618` display, crossing 3 steps up — a big jump to display sizes
>
> Or name your own pair and crossover.

**Two things to say when they pick, because both surprise people:**

- **A grid-snapped scale is no longer an even ratio.** Snapping is the point, but it breaks the
 exact doubling and makes some steps unequal. `snapped: true` marks the rows that moved.
- **A coarse grid can eat the ratio entirely.** The body size is anchored so it never drifts, but
 above it a grid wider than the gap between steps forces every step to be bumped, and the scale
 degenerates into a plain arithmetic `+grid` sequence. At a 16px base a `1.125` ratio has a
 1.78px smallest gap, so a 4px grid gives `12 16 20 24 28 32 36` — even spacing, not a ratio.
 `meta.collisions` counts it and `meta.tooCoarse` flags it. **Say so, and offer `meta.minGap` as
 a guide to the grid that would have fitted, or a wider ratio instead.** `minGap` is
 conservative — a grid wider than it does not guarantee a collision, since two close steps can
 still land on different multiples. Trust `collisions` for what happened.
- **A preset ignores the base you just confirmed.** Tailwind's sizes *are* 12/14/16/…; they are
 not derived from anything. The selection's **font** is still used. Offer `rebase: true` to
 scale the whole preset proportionally if their base differs from the preset's own.

---

## P3 — How many steps?

Big ratios grow fast, so this cannot be fixed at seven. Compute a suggestion with
`suggestStepsUp(base, r)` — the largest count up to 5 that does not immediately cross the 120px
tightening threshold — then ask verbatim:

> How many steps?
>
> 1. ** above** the body and **1 below** — the largest lands at ** px** *(suggested)*
> 2. A different spread — tell me how many above and below
>
> Reply `1`, or give me two numbers.

**Wait.** Skip this prompt entirely for a **preset**, which has a fixed number of steps by
definition — say that you are skipping it rather than silently not asking.

Why it matters, at a 16px base with five steps up:

| Ratio | Largest |
|---|---|
| `1.125` | 28.8 |
| `1.1487` | 32 |
| `1.333` | 67.3 |
| `1.5` | **121.5** — trips the tightening |
| `1.618` | **177.4** |

So a golden ratio gets **4** steps suggested, not 5. Naming the largest size in the question is
what makes the number meaningful.

---

## A1 — Compute the scale

**Derive everything. Do not hardcode sizes** — the only literals here are the preset tables,
which are literal by nature. Run this block:

```js
// ---------------------------------------------------------------- family 1: modular ratios
// `octave: k` means the ratio is 2^(1/k), so the scale hits an exact doubling every k steps.
// Those are computed from the exponent rather than by repeated multiplication, which is what
// keeps the doubling exact rather than 2.0000000000000004.
const RATIOS = [
  { key: "minor-second",   name: "Minor second",       r: 1.067 },
  { key: "root6",          name: "Sixth root of two",  octave: 6 },
  { key: "major-second",   name: "Major second",       r: 1.125 },
  { key: "root5",          name: "Fifth root of two",  octave: 5 },
  { key: "root4",          name: "Fourth root of two", octave: 4 },
  { key: "minor-third",    name: "Minor third",        r: 1.2 },
  { key: "major-third",    name: "Major third",        r: 1.25 },
  { key: "root3",          name: "Cube root of two",   octave: 3 },
  { key: "perfect-fourth", name: "Perfect fourth",     r: 1.333 },
  { key: "aug-fourth",     name: "Augmented fourth",   r: Math.SQRT2 },
  { key: "perfect-fifth",  name: "Perfect fifth",      r: 1.5 },
  { key: "golden",         name: "Golden ratio",       r: (1 + Math.sqrt(5)) / 2 },
];
const DEFAULT_RATIO = "root5";

// ---------------------------------------------------------------- family 2: platform presets
// Curated, not derived. Each carries its own base, and sizes are deduplicated — Material and
// Carbon reuse the same px value under several role names, which would give duplicate rows.
const PRESETS = {
  tailwind: { name: "Tailwind", base: 16, steps: [
    ["xs", 12], ["sm", 14], ["base", 16], ["lg", 18], ["xl", 20], ["2xl", 24],
    ["3xl", 30], ["4xl", 36], ["5xl", 48], ["6xl", 60], ["7xl", 72], ["8xl", 96]] },
  material: { name: "Material 3", base: 16, steps: [
    ["label-small", 11], ["body-small", 12], ["body-medium", 14], ["body-large", 16],
    ["title-large", 22], ["headline-small", 24], ["headline-medium", 28],
    ["headline-large", 32], ["display-small", 36], ["display-medium", 45],
    ["display-large", 57]] },
  hig: { name: "Apple HIG", base: 17, steps: [
    ["caption2", 11], ["caption1", 12], ["footnote", 13], ["subheadline", 15],
    ["body", 17], ["title3", 20], ["title2", 22], ["title1", 28], ["largeTitle", 34]] },
  carbon: { name: "IBM Carbon", base: 16, steps: [
    ["label-01", 12], ["body-01", 14], ["body-02", 16], ["heading-03", 20],
    ["heading-04", 28], ["heading-05", 32], ["heading-06", 42], ["heading-07", 54]] },
};

// The specimen field is one EM MEASURE, applied per row: never wider than 22x the size of the
// step it is set at, and never wider than the text's own natural width. A measure only means
// anything relative to the type it holds, so 22em at 32px is 704px and at 14px is 308px. Cells
// are auto-height, so a specimen wraps rather than clipping.
const FIELD_MAX_EM = 22;
const EST_ADVANCE_EM = 0.5;      // fallback average character advance, if measuring is impossible
const TIGHT_ABOVE_PX = 120;      // over this, display type needs tighter leading
const TIGHT_LINE_HEIGHT = 1.05;
const SPECIMEN_CHARS = 56;       // inside the classic 45-75 character measure
const TAPER_BASE = 1.5;          // line height at the body size
const TAPER_STEP = 0.06;         // ...falling this much per step up

function round2(v) { return Math.round(v * 100) / 100; }
function clamp(v, lo, hi) { return Math.min(hi, Math.max(lo, v)); }

function findRatio(key) {
  const hit = RATIOS.filter(function (x) { return x.key === key; })[0];
  if (!hit) throw new Error("unknown ratio: " + key);
  return hit;
}
function ratioValue(spec) {
  return spec.octave ? Math.pow(2, 1 / spec.octave) : spec.r;
}
function ratioLabel(spec) {
  return spec.name + " (" + Number(ratioValue(spec).toFixed(4)) + ")";
}

// h1 is always the LARGEST step. Beyond six there are no CSS heading names, so the extra top
// steps become display-1 (largest), display-2, ... and h1-h6 pick up below them.
function tokenName(n, stepsUp) {
  if (n === 0) return "p";
  if (n < 0) return n === -1 ? "small" : new Array(-n).join("x") + "small";
  const extras = Math.max(0, stepsUp - 6);
  const fromTop = stepsUp - n + 1;               // 1 = largest
  return fromTop <= extras ? "display-" + fromTop : "h" + (fromTop - extras);
}

function modularMultiplier(spec, n) {
  return spec.octave ? Math.pow(2, n / spec.octave) : Math.pow(ratioValue(spec), n);
}

// ---------------------------------------------------------------- family 4: split two-ratio
// Tight below the crossover, looser above. Compounding CONTINUES from the crossover, so the
// two halves join without a jump at the seam.
function splitMultiplier(bodySpec, dispSpec, crossover, n) {
  if (n <= crossover) return modularMultiplier(bodySpec, n);
  return modularMultiplier(bodySpec, crossover) *
         modularMultiplier(dispSpec, n - crossover);
}

// ---------------------------------------------------------------- family 3: grid-snapped
// Snap to the grid, ANCHORED at the body size so the one number the user confirmed survives.
// Snapping naively from one end lets a collision repair cascade: at a 16px base with a 1.125
// ratio and a 4px grid, every step gets bumped and the body size drifts to 20.
//
// Collisions are counted, not hidden. A grid coarser than the smallest gap in the scale MUST
// collide, and bumping turns the top into a plain arithmetic +grid sequence. That is forced by
// the arithmetic, so the honest move is to report it.
// Input and output are ASCENDING.
function snapAscending(sizesAsc, grid, anchorIndex) {
  const snap = function (v) { return Math.max(grid, Math.round(v / grid) * grid); };
  const a = anchorIndex == null ? 0 : anchorIndex;
  const out = sizesAsc.slice();
  let collisions = 0;
  out[a] = snap(sizesAsc[a]);
  for (let i = a + 1; i < out.length; i++) {                    // upward from the anchor
    let v = snap(sizesAsc[i]);
    if (v <= out[i - 1]) { v = out[i - 1] + grid; collisions++; }
    out[i] = v;
  }
  for (let i = a - 1; i >= 0; i--) {                            // downward from the anchor
    let v = snap(sizesAsc[i]);
    if (v >= out[i + 1]) { v = out[i + 1] - grid; collisions++; }
    out[i] = Math.max(grid, v);
  }
  return { sizes: out, collisions: collisions };
}

// The smallest gap between adjacent unsnapped steps. A grid wider than this cannot preserve
// the scale, and that is worth saying before snapping rather than after.
function minGap(sizesAsc) {
  let g = Infinity;
  for (let i = 1; i < sizesAsc.length; i++) g = Math.min(g, sizesAsc[i] - sizesAsc[i - 1]);
  return g;
}

// A step count that will not immediately trip the tightening threshold.
function suggestStepsUp(base, r) {
  for (let k = 5; k >= 1; k--) if (base * Math.pow(r, k) <= TIGHT_ABOVE_PX) return k;
  return 1;
}

// Rough width of the specimen if it cannot be measured. 56 characters at ~0.5em is about 28em,
// which is over the 22em cap, so an unmeasured field lands on the cap rather than guessing wide.
function estimateNaturalWidth(chars, largestSizePx) {
  return specimenText(chars).length * EST_ADVANCE_EM * largestSizePx;
}

// ONE em measure for the whole table, from the natural width MEASURED at the largest step — set
// the specimen to hug and read node.width. Both terms are in em, so the smaller wins and the
// same measure fits every row: never wider than 22em, never wider than the text itself.
// Unmeasured falls back to the cap, which is the narrower of the two answers.
function fieldEm(largestSizePx, naturalWidthPx) {
  if (!largestSizePx || naturalWidthPx == null) return FIELD_MAX_EM;
  return Math.min(FIELD_MAX_EM, naturalWidthPx / largestSizePx);
}

// The width of ONE specimen cell: the em measure at that row's own size. Auto height does the
// rest. A 22em measure is 22em at every step, so the column is proportional rather than uniform.
function specimenWidthPx(sizePx, em) {
  return round2(em * sizePx);
}

// Presets have no exponent, so derive an effective one from the size and the taper stays
// continuous. Reduces to the real n for a 2^(1/5) scale.
function effectiveN(sizePx, base) {
  return Math.log(sizePx / base) / Math.log(Math.pow(2, 1 / 5));
}

function lineHeightFor(sizePx, n) {
  const tapered = clamp(TAPER_BASE - TAPER_STEP * n, 1.15, 1.6);
  const tightened = sizePx > TIGHT_ABOVE_PX;
  return {
    ratio: Math.round((tightened ? Math.min(tapered, TIGHT_LINE_HEIGHT) : tapered) * 100) / 100,
    tightened: tightened,
  };
}

// Trim to a specimen length. Never longer than the limit, ellipsis included.
function specimenText(chars, limit) {
  const max = limit || SPECIMEN_CHARS;
  const t = String(chars == null ? "" : chars).trim();
  if (t.length <= max) return t;
  const cut = t.slice(0, max - 1);              // leave room for the ellipsis
  const space = cut.lastIndexOf(" ");
  return (space > 0 ? cut.slice(0, space) : cut) + "…";
}

// ---------------------------------------------------------------- the one entry point
// buildScale(base) with no options is the classical scale: 2^(n/5), five up, one down.
function buildScale(base, opts) {
  const o = opts || {};
  let rows, meta;

  if (o.preset) {
    const preset = PRESETS[o.preset];
    if (!preset) throw new Error("unknown preset: " + o.preset);
    const factor = o.rebase ? base / preset.base : 1;
    rows = preset.steps.map(function (st) {
      return { token: st[0], sizePx: st[1] * factor, n: null };
    });
    meta = { kind: "preset", label: preset.name, presetBase: preset.base * factor };
  } else {
    const stepsUp = o.stepsUp == null ? 5 : o.stepsUp;
    const stepsDown = o.stepsDown == null ? 1 : o.stepsDown;
    const bodySpec = findRatio(o.ratio || DEFAULT_RATIO);
    const dispSpec = o.displayRatio ? findRatio(o.displayRatio) : null;
    const crossover = o.crossover == null ? 2 : o.crossover;

    rows = [];
    for (let n = -stepsDown; n <= stepsUp; n++) {
      const m = dispSpec ? splitMultiplier(bodySpec, dispSpec, crossover, n)
                         : modularMultiplier(bodySpec, n);
      rows.push({ token: tokenName(n, stepsUp), n: n, sizePx: base * m });
    }
    let gridInfo = null;
    if (o.grid) {
      const raw = rows.map(function (x) { return x.sizePx; });          // ascending by n
      const bodyIndex = stepsDown;                                     // where n === 0 sits
      const snap = snapAscending(raw, o.grid, bodyIndex);
      gridInfo = {
        grid: o.grid,
        // Ground truth: how many steps had to be bumped off their snapped value.
        collisions: snap.collisions,
        // Advice, and CONSERVATIVE: two steps whose raw gap is under the grid can still snap
        // to different multiples depending on where they fall, so a grid wider than minGap does
        // not guarantee a collision. `collisions` is the ground truth; this is the guide.
        minGap: round2(minGap(raw)),
        // Derived from what actually happened, NOT from comparing the grid against a rounded
        // minGap — that reported "too coarse" alongside "0 collisions" on a grid of 4 against a
        // real gap of 3.997.
        tooCoarse: snap.collisions > 0,
      };
      rows = rows.map(function (x, i) {
        return { token: x.token, n: x.n, sizePx: snap.sizes[i], snapped: snap.sizes[i] !== x.sizePx };
      });
    }
    meta = dispSpec
      ? { kind: "split", label: ratioLabel(bodySpec) + " body / " + ratioLabel(dispSpec) +
          " display, crossing at n=" + crossover, crossover: crossover }
      : { kind: o.grid ? "snapped" : "modular", label: ratioLabel(bodySpec), ratio: ratioValue(bodySpec) };
    meta.stepsUp = stepsUp;
    meta.stepsDown = stepsDown;
    if (gridInfo) {
      meta.grid = gridInfo.grid;
      meta.collisions = gridInfo.collisions;
      meta.minGap = gridInfo.minGap;
      meta.tooCoarse = gridInfo.tooCoarse;
      meta.label += " snapped to " + gridInfo.grid + "px";
    }
  }

  rows.sort(function (a, b) { return b.sizePx - a.sizePx; });     // largest first
  const largest = rows[0].sizePx;
  // o.naturalWidthPx is the measured width once A4 has probed the real text; o.specimen falls
  // back to the estimate; neither given falls back to the cap.
  const natural = o.naturalWidthPx != null ? o.naturalWidthPx
                : o.specimen != null ? estimateNaturalWidth(o.specimen, largest)
                : null;
  const em = fieldEm(largest, natural);          // one measure, in em, for every row

  const scale = rows.map(function (x) {
    const n = x.n == null ? effectiveN(x.sizePx, base) : x.n;
    const lh = lineHeightFor(x.sizePx, n);
    const multiplier = x.sizePx / base;
    return {
      token: x.token,
      n: x.n,
      multiplier: multiplier,
      multiplierLabel: round2(multiplier) === 1 ? "1em" : Number(multiplier.toFixed(4)) + "em",
      sizePx: x.sizePx,
      sizeLabel: round2(x.sizePx),
      lineHeightRatio: lh.ratio,
      lineHeightPx: round2(x.sizePx * lh.ratio),
      tightened: lh.tightened,
      snapped: x.snapped === true,
      // PER ROW: the shared em measure at this step's own size. Never wider than 22em of it.
      maxWidthPx: specimenWidthPx(x.sizePx, em),
      fieldEm: round2(em),
      fieldCapPx: round2(FIELD_MAX_EM * x.sizePx),
      fieldCapped: em >= FIELD_MAX_EM,           // the cap bound it, not the measurement
    };
  });
  scale.meta = meta;
  return scale;
}
```

The classical scale, `buildScale(16)`:

| Token | `n` | Multiplier | Size | Line height |
|---|---|---|---|---|
| `h1` | 5 | `2em` | 32 | 1.20 → 38.4 |
| `h2` | 4 | `1.7411em` | 27.86 | 1.26 → 35.1 |
| `h3` | 3 | `1.5157em` | 24.25 | 1.32 → 32.0 |
| `h4` | 2 | `1.3195em` | 21.11 | 1.38 → 29.1 |
| `h5` | 1 | `1.1487em` | 18.38 | 1.44 → 26.5 |
| `p` | 0 | `1em` | 16 | 1.50 → 24 |
| `small` | −1 | `.8706em` | 13.93 | 1.56 → 21.7 |

---

## A2 — Show the breakdown in chat, before asking about variables

**Print the scale as a table in the conversation. Do not build anything on the canvas yet.**

This is the point of the whole series. Somebody deciding whether to commit a scale to variables
needs to see the numbers first, and a scale that looks wrong is much cheaper to reject here than
after a table and fourteen variables exist.

Report, in this order:

1. **The scale you used** — `meta.label`, e.g. `Fifth root of two (1.1487)`, and how many steps.
2. **The table** — token, multiplier, size, line height. Largest first.
3. **Anything that departed from the plain rule**, each one named:
 - `tightened` rows, and that the 120px threshold caused it
 - `snapped` rows, and that the ratio is no longer even. If `meta.tooCoarse`, say how many
 collisions there were and that the result is effectively arithmetic rather than a ratio
 - a **preset**, and that its sizes are literal rather than derived
 - a **split** scale, and where the crossover sits
4. **The consequences worth knowing** — see below.

Four things to say, because none is obvious from the numbers:

- **A modular scale is one ratio.** For the octave-exact family, `2^(n/5)`, the largest step is
 exactly double the body size and every adjacent pair shares the same ratio.
- **Line height is a heuristic**, `clamp(1.5 − 0.06n, 1.15, 1.6)`, not a law. Larger type needs
 proportionally less leading.
- **Over 120px it tightens to 1.05.** Size-driven, not token-driven: it depends on where the base
 and the ratio land, not on which heading it is. **The cut-off can invert absolute leading** —
 at a 64px base `h1` is 128 × 1.05 = 134.4px while `h2` is 111.4 × 1.26 = 140.4px, so the larger
 type gets the *smaller* line box. That is what a hard threshold does; say it rather than
 letting someone find it and assume a bug.
- **Sizes stay exact** unless snapped or preset. Rounding to whole pixels breaks the even
 ratio — offer it, never do it silently.

---

## P4 — Variables? *(skip if they already asked)*

**Read the opening message first.** If they already asked for variables, tokens, or "font size
variables", that is a yes — **do not ask again**, say you are creating them and go to P5.

Otherwise, having just shown the table, ask verbatim:

> Want me to turn these into **variables**?
>
> 1. **Yes** — one `FLOAT` variable per size and per line height
> 2. **No** — just lay out the specimen on the canvas
>
> Reply `1` or `2`.

**Wait.**

- **2 / No** → skip P5 and A3. Build the specimen with raw values and say **nothing is bound**, so
 nobody expects the table to update later.
- **1 / Yes** → P5.

---

## P5 — Name the collection

Only when variables are happening. Ask, verbatim:

> What should I call the collection?
>
> 1. **Type scale** — a new collection *(default)*
> 2. Add to an existing one: 
> 3. Something else — tell me the name
>
> Reply with a number or a name.

List the existing collections in the prompt itself, so joining one is a real option rather than a
thing they have to know to ask for:

```js
const collections = await figma.variables.getLocalVariableCollectionsAsync();
```

**Wait.** A name matching an existing collection → **add to it**, never duplicate. Use their name
**verbatim**; do not tidy capitalisation or pluralisation.

---

## A3 — Create the variables

**Skip entirely if they said no in P4.**

```js
const collection = existing || figma.variables.createVariableCollection(collectionName);
const modeId = collection.modes[0].modeId;

for (const step of scale) {
  const size = figma.variables.createVariable("size/" + step.token, collection, "FLOAT");
  size.scopes = ["FONT_SIZE"];
  size.setValueForMode(modeId, step.sizePx);
  size.description = step.multiplierLabel + " — " + scale.meta.label +
    (step.snapped ? ", snapped to " + scale.meta.grid + "px" : "");

  const lh = figma.variables.createVariable("line-height/" + step.token, collection, "FLOAT");
  lh.scopes = ["LINE_HEIGHT"];
  lh.setValueForMode(modeId, step.lineHeightPx);
  lh.description = "ratio " + step.lineHeightRatio + (step.tightened ? " (tightened)" : "");
}
```

- **Set `scopes` explicitly.** The default `ALL_SCOPES` pollutes every property picker.
- Names are `size/h1` and `line-height/h1`, so Figma groups them. The scale and the multiplier go
 in the description — that is what makes it legible to whoever inherits it.
- **Re-running must update, not duplicate.** Look for an existing variable of the same name in
 the collection and set its value instead.

---

## P6 — How should the rows line up?

The last decision before anything is drawn, and the only part of the table that is a matter of
taste. Ask verbatim:

> How should the cells line up across each row?
>
> 1. **Baseline** — the numbers sit on the first baseline of the specimen beside them *(default)*
> 2. **Top** — every cell flush with the top of its row
> 3. **Centre** — every cell centred against the row
>
> Reply `1`, `2` or `3`.

**Wait.** These map straight onto `counterAxisAlignItems`: `BASELINE`, `MIN`, `CENTER`. Everything
else about the table — the columns, their order, their widths, the gaps, the padding — is fixed and
computed, so this is the only thing to ask.

**Baseline is the default because it is what makes a specimen table read as a table.** `13.93` set
at 12px next to a 32px specimen has nothing in common with it visually unless the two sit on one
baseline; top-aligning them puts the number level with the specimen's ascenders, which reads as a
misalignment even though it is a straight edge.

---

## A4 — Build the specimen table, in six passes

One auto-layout frame on the **page**, clear of existing content. A header row, then one row per
step, largest first.

**Run the passes in order and do not merge them.** Every dimension is computed in pass 2; passes
3–5 only apply numbers that already exist. Deciding a width or an alignment while creating nodes is
what made this table come out differently every run.

| Pass | | |
|---|---|---|
| 1 | **Measure** | one probe node, reused: the specimen at the largest size, then every metadata string at 12px |
| 2 | **Compute** | `tableLayout(scale, …)` — column widths, gaps, padding, alignment, total width |
| 3 | **Frame** | the outer vertical auto-layout frame |
| 4 | **Header** | a header row using the *same* column widths |
| 5 | **Rows** | one row per step, largest first, fixed column order |
| 6 | **Verify** | read the geometry back off the canvas and check the columns actually line up |

### The five columns are fixed

| Column | Contents | Align |
|---|---|---|
| Token | `h1` | left |
| Multiplier | `2em` | right |
| Size | `32`, with `†` if snapped | right |
| Line height | `38.4 (1.2)` — one string, `*` if tightened | right |
| Specimen | the selection's own characters via `specimenText()`, in its font at that size | left |

The specimen column is the point of the table: the same words at every step, in the real font, so
the scale can be judged rather than read as numbers. **Do not add, drop or reorder columns**, and
do not ask which ones they want — a table whose shape changes per run is the thing being fixed.

**The four metadata columns are set at one fixed 12px in every row.** Only the specimen changes
size down the table. Setting `32` at 32px and `13.93` at 13.93px is what makes columns impossible
to align and lets the numbers, rather than the specimen, drive the row height. The metadata is
chrome; it is not part of the scale.

**Every cell is a single text node**, which is why the line height column is one string rather
than a value plus a muted ratio. Two nodes in a cell needs a wrapper frame, and a frame is not
what `BASELINE` lines up. Departures go in **footnotes under the table** instead — `footnotes()`
returns them.

### Pass 2 — the layout engine

```js
// ---------------------------------------------------------------- the table layout
// FIXED columns, in this order, every time. Contents come from cellText(); the specimen column
// is the measured field, and it is the ONE column whose width is per-row.
const COLUMNS = [
  { key: "token",      header: "Token",       align: "LEFT" },
  { key: "multiplier", header: "Multiplier",  align: "RIGHT" },
  { key: "size",       header: "Size",        align: "RIGHT" },
  { key: "lineHeight", header: "Line height", align: "RIGHT" },
  { key: "specimen",   header: "Specimen",    align: "LEFT" },
];

// Metadata is chrome, set at ONE size in every row. It does not scale with the scale.
const META_SIZE_PX = 12;
const META_LINE_HEIGHT_PX = 16;   // 12 x 4/3 — a whole number, on the 4px grid
const CELL_GRID = 4;              // column widths round UP to this
const CELL_MIN_PX = 36;           // a floor, so a one-character column is not absurd
const COL_GAP = 24;               // fixed, not derived from the scale: gutters are not type
const ROW_GAP = 16;
const TABLE_PAD = 32;

// Row alignment maps onto auto layout's counterAxisAlignItems. BASELINE is native, HORIZONTAL
// only, and aligns the FIRST text baseline of each cell.
const ROW_ALIGN = { baseline: "BASELINE", top: "MIN", center: "CENTER" };

function ceilTo(v, grid) { return Math.ceil(v / grid) * grid; }

// One string per cell — a cell is one text node, never a nested frame.
function cellText(step, key) {
  if (key === "token") return step.token;
  if (key === "multiplier") return step.multiplierLabel;
  if (key === "size") return String(step.sizeLabel) + (step.snapped ? "†" : "");
  if (key === "lineHeight") {
    return step.lineHeightPx + " (" + step.lineHeightRatio + (step.tightened ? "*" : "") + ")";
  }
  return null;                                  // the specimen is the measured field
}

// The WIDEST cell in a column decides its width — header included — measured from the real
// typeface at the metadata size, then rounded UP to the grid. One number per METADATA column,
// used in every row: that is what makes the four left columns line up. Hugging each cell to its
// own content is what made the old table a ragged staircase.
// measure(text, sizePx) -> px. In Figma that is a probe text node; without one it estimates.
function columnWidths(scale, measure) {
  const m = measure || function (text, sizePx) {
    return String(text).length * EST_ADVANCE_EM * sizePx;
  };
  return COLUMNS.map(function (c) {
    if (c.key === "specimen") {
      // PER ROW, from buildScale: 22em of each step's own size. widthPx here is the widest of
      // them — the largest step's — which the header spans and which sets the table's width.
      // Pass 5 reads step.maxWidthPx for the body rows; perRow says so rather than implying one.
      return { key: c.key, header: c.header, align: c.align,
               widthPx: scale[0].maxWidthPx, perRow: true };
    }
    let w = m(c.header, META_SIZE_PX);
    scale.forEach(function (s) { w = Math.max(w, m(cellText(s, c.key), META_SIZE_PX)); });
    return { key: c.key, header: c.header, align: c.align,
             widthPx: Math.max(CELL_MIN_PX, ceilTo(w, CELL_GRID)) };
  });
}

// Departures from the plain rule go under the table, so no cell needs a second node.
function footnotes(scale) {
  const notes = [];
  if (scale.some(function (s) { return s.tightened; })) {
    notes.push("* line height tightened to " + TIGHT_LINE_HEIGHT +
               " — anything over " + TIGHT_ABOVE_PX + "px");
  }
  if (scale.some(function (s) { return s.snapped; })) {
    notes.push("† snapped to " + scale.meta.grid + "px — the ratio is not even here");
  }
  return notes;
}

// Everything the build needs, computed ONCE. Pass this into the construction and decide nothing
// else along the way.
function tableLayout(scale, opts) {
  const o = opts || {};
  const cols = columnWidths(scale, o.measure);
  const inner = cols.reduce(function (a, c) { return a + c.widthPx; }, 0) +
                COL_GAP * (cols.length - 1);
  const align = ROW_ALIGN[o.rowAlign == null ? "baseline" : o.rowAlign];
  if (!align) throw new Error("unknown row alignment: " + o.rowAlign);
  return {
    columns: cols,
    rowAlign: align,
    metaSizePx: META_SIZE_PX,
    metaLineHeightPx: META_LINE_HEIGHT_PX,
    colGap: COL_GAP,
    rowGap: ROW_GAP,
    padding: TABLE_PAD,
    innerWidthPx: inner,
    tableWidthPx: inner + TABLE_PAD * 2,
    footnotes: footnotes(scale),
  };
}
```

### Pass 1 — one probe, reused for every measurement

**Do not pick a width from a formula alone.** A fixed multiple is wrong for most typefaces — a
condensed face leaves a slack, empty field and a wide one runs out of room. Measure, then clamp:

```js
// ONE probe node for the whole pass: the specimen at the largest size, then every metadata
// string at 12px. Create it once, remove it once.
const probe = figma.createText();
probe.fontName = font;                        // the selection's font, already loaded
probe.textAutoResize = "WIDTH_AND_HEIGHT";    // hug, so width is the natural width
function measure(text, sizePx) {
  probe.fontSize = sizePx;
  probe.characters = String(text);
  return probe.width;
}

probe.fontSize = largest;                     // scale[0].sizePx
probe.characters = specimen;                  // the 56-character trimmed string
const natural = probe.width;

const scale = buildScale(base, { /* … */ naturalWidthPx: natural });
const layout = tableLayout(scale, { measure: measure, rowAlign: answerFromP6 });

probe.remove();                               // MUST remove it — createText() lands on the page
```

- **Never wider than `22 ×` the size of the step it is set at.** This is a hard cap, and it is
 **per row** — 22em is 704px on a 32px `h1` and 308px on a 14px `small`. A measure only means
 anything relative to the type it holds, so one absolute width cannot be right for both.
- **Never wider than the text's own natural width**, so a condensed face gets a narrower field
 rather than a slack, half-empty one. The measurement is taken once, at the largest step, and
 divided by that size to get an em value every row can use.
- **The smaller of the two wins**, which is `fieldEm()`. `scale[n].fieldEm` is the measure,
 `fieldCapPx` is 22em of that row, and `fieldCapped` says whether the cap or the measurement
 decided — so you can say which one bound it.
- **Every specimen cell is auto-height** (`textAutoResize = "HEIGHT"`), so it wraps to as many
 lines as it needs and no step can clip.

`probe.remove()` is not optional. `figma.createText()` puts the node on the current page, so
skipping it leaves a stray text layer on the canvas.

**If measuring is impossible**, `estimateNaturalWidth(chars, largest)` gives `56 × 0.5em ≈ 28em`,
which is over the cap, so the field lands on 22em — and `columnWidths` falls back to the same
average advance. Passing no width at all also lands on the cap, which is the narrower of the two
answers rather than a guess in either direction.

**Length.** The string is capped at **56 characters**, broken at a word boundary, and
**identical in every row**, so the only thing changing down the table is the size.

**56 characters at 22em wraps, and it is meant to.** An average advance of ~0.5em wants about
28em, so the cap bites and most faces run to two lines at every step. Because the measure is the
same em value in every row, they wrap at **the same point in every row** — the specimen column is
proportional rather than uniform, one shape at seven sizes. That is the deliberate trade: the old
one-shared-width field kept the table rectangular but gave `small` a field twenty times its own
size. Under `BASELINE` the *first* line's baseline is the one that aligns, which is the right one.

**The specimen column's right edge is therefore ragged, by design.** It is the last column, so the
four metadata columns still line up exactly — every cell before it has a fixed width identical in
every row. Pass 6 checks that, and checks each specimen against its own cap instead of against the
other rows.

### Passes 3–5 — apply the numbers, decide nothing

**Row-major, with a fixed width on every cell.** The outer frame is vertical, each row is
horizontal, and each cell is a fixed-width text node. That is the only structure where both things
hold at once: the four metadata columns line up because their widths are identical in every row,
and rows line up because `counterAxisAlignItems` governs the whole row. The specimen is fixed-width
too — just to **its own row's** width, which is why it is the last column and why nothing to its
left can be knocked out of line by it. **A column-major table — one vertical frame
per column — gets the columns for free and destroys the rows**, because a 12px token cell and a
96px specimen cell hug to different heights and nothing keeps step *n* level across the columns.

```js
const table = figma.createAutoLayout();       // pass 3
table.name = "Type scale — " + scale.meta.label;
table.layoutMode = "VERTICAL";
table.itemSpacing = layout.rowGap;
table.paddingTop = table.paddingBottom = table.paddingLeft = table.paddingRight = layout.padding;
figma.currentPage.appendChild(table);
table.layoutSizingHorizontal = "HUG";         // hug both — the fixed cells set the width
table.layoutSizingVertical = "HUG";

// specimenW is the PER-ROW specimen width — step.maxWidthPx. The header passes nothing and gets
// the column's widest, so the header spans the column.
function buildRow(name, texts, sizePx, lineHeightPx, opacity, specimenW) {
  const row = figma.createAutoLayout();
  row.name = name;
  row.layoutMode = "HORIZONTAL";
  row.itemSpacing = layout.colGap;
  row.counterAxisAlignItems = layout.rowAlign;  // BASELINE | MIN | CENTER
  row.fills = [];                              // rows are structure, not surface
  table.appendChild(row);
  row.layoutSizingHorizontal = "HUG";          // identical cells ⇒ identical row widths
  row.layoutSizingVertical = "HUG";

  layout.columns.forEach(function (col, i) {
    const cell = figma.createText();
    cell.name = col.key;
    cell.fontName = font;
    cell.characters = texts[i];
    row.appendChild(cell);                     // append BEFORE sizing
    cell.textAutoResize = "HEIGHT";            // auto height — BEFORE the width, or it collapses
    cell.fontSize = col.key === "specimen" ? sizePx : layout.metaSizePx;
    cell.lineHeight = { unit: "PIXELS",
      value: col.key === "specimen" ? lineHeightPx : layout.metaLineHeightPx };
    const w = col.perRow && specimenW != null ? specimenW : col.widthPx;
    cell.resize(w, cell.height);               // fixed width, auto height
    cell.textAlignHorizontal = col.align;
    if (opacity != null) cell.opacity = opacity;
  });
  return row;
}

// pass 4 — the header, on the SAME column widths and the SAME alignments
buildRow("header", layout.columns.map(function (c) { return c.header; }),
         layout.metaSizePx, layout.metaLineHeightPx, 0.4);

// pass 5 — one row per step, largest first. The specimen gets THIS step's width: 22em of its own
// size, at most — never the largest step's.
scale.forEach(function (step) {
  buildRow(step.token,
    layout.columns.map(function (c) {
      return c.key === "specimen" ? specimen : cellText(step, c.key);
    }),
    step.sizePx, step.lineHeightPx, null, step.maxWidthPx);
});
```

- **The header is a row like any other**, on the same widths and the same alignments, so a
 right-aligned number column gets a right-aligned header. It is distinguished by **opacity only**.
 No divider rule: a `FILL`-width divider inside a hugging frame is a circular constraint, and
 circular constraints are exactly what makes output unpredictable.
- **`counterAxisAlignItems = "BASELINE"` is horizontal-only.** If the API refuses it, fall back to
 `"MIN"` and **say the rows are top-aligned instead** — do not silently ship a different table.
- **Append order is the layout order**, so the table's children go in exactly this sequence and
 nothing is reordered afterwards:

 | | Child | Type |
 |---|---|---|
 | 1 | `Base px · <meta.label>` | text, metadata size |
 | 2 | the header row | frame |
 | 3… | one row per step, largest first | frames |
 | last | `layout.footnotes` joined by newlines — **omitted** when there are none | text, metadata size, 0.4 opacity |

 The title and the footnotes are **text nodes, not rows**, which is why pass 6 filters on
 `type === "FRAME"` before comparing signatures. Neither is fixed to a column width, so neither
 affects the table's width.

**Construction rules — every one of these is a way this breaks:**

- **Load every font first**, using the family and style read from the selection, not a hardcoded
 default. Inter's bold is `"Semi Bold"`, not `"SemiBold"`.
- Build with `figma.createAutoLayout()`, never `createFrame` plus a manual `layoutMode`.
- `appendChild` **before** setting `layoutSizingHorizontal` / `Vertical`.
- `textAutoResize = "HEIGHT"` **before** any `FILL` or fixed width, or the text collapses to a
 near-zero-width thread.
- `resize()` resets sizing modes to `FIXED` — which is what a cell wants, so resize it **last**,
 and never resize a frame that is meant to hug.
- **`lineHeight` takes `{ unit, value }`**, not a bare number:
 `{ unit: "PIXELS", value: step.lineHeightPx }`.
- Set `x`/`y` **after** appending to the page — they are parent-relative, and a page child's
 coordinates are absolute.

Bind rows to their variables when variables exist, so the table stays live:

```js
specimen.setBoundVariable("fontSize", sizeVar);
specimen.setBoundVariable("lineHeight", lhVar);
```

**Bind the specimen cell only.** The metadata cells are 12px labels *about* the scale, not
instances of it — binding `size/h1` to the cell that reads "32" would resize the label to 32px and
undo the whole layout.

### Pass 6 — verify the geometry off the canvas

**Read it back. Do not assume it worked.** A column that did not line up is a failure to fix, not
a look to accept:

```js
const rows = table.children.filter(function (n) { return n.type === "FRAME"; });
const body = rows.slice(1);                     // rows[0] is the header

// The four metadata cells must match exactly. The specimen's WIDTH is per-row by design, so only
// its x is compared — and because it is the last column, that x is identical anyway.
const signature = rows.map(function (r) {
  return r.children.slice(0, 4).map(function (c) {
    return Math.round(c.x * 100) / 100 + ":" + Math.round(c.width * 100) / 100;
  }).join(" | ") + " || x" + Math.round(r.children[4].x * 100) / 100;
});
const aligned = signature.every(function (s) { return s === signature[0]; });

// Instead, each specimen is checked against its OWN cap, and for auto height.
const capped = body.every(function (r, i) {
  const cell = r.children[4];
  return cell.textAutoResize === "HEIGHT" &&
         cell.width <= FIELD_MAX_EM * scale[i].sizePx + 0.02 &&
         Math.abs(cell.width - scale[i].maxWidthPx) < 0.02;
});
```

Check all five, and fix rather than report:

- [ ] Every row has the **same number of children**, in the same column order
- [ ] The four metadata cells' `x` and `width` are **identical in every row**, and every
 specimen sits at the **same `x`** — the signature above matches
- [ ] Every specimen is **at most `22 ×` its own font size**, and equals its row's
 `maxWidthPx` — `capped` above
- [ ] Every specimen is **auto-height**, so a wrapped line grows the row instead of clipping
- [ ] No cell is taller than its row

Row widths are **not** all equal, and must not be forced to be: a row's width is its four fixed
cells plus its own specimen, so `layout.innerWidthPx` is the *widest* row — the largest step's —
not a value every row shares. Then say the table's total width (`layout.tableWidthPx`), the field
measure in em, and how many lines the specimen wrapped to.

---

## A5 — Final gate: do not finish until every line is true

Check each against the canvas and the variables panel, not from memory.

- [ ] Sizes were **computed**, not typed in as literals — except a preset, which is literal by
 definition
- [ ] For an octave-exact ratio, the largest step is exactly `2^(stepsUp/octave)` × the base
- [ ] Every prompt was posted **on its own** and waited for a reply — none bundled, none
 self-answered, none guessed at
- [ ] Every prompt offered **numbered options**, so a one-character reply was enough
- [ ] **P2b was asked** when they picked 6, 7 or 8 — the grid, preset and ratio pair were never
 chosen for them
- [ ] Several text nodes selected → they were **asked which one**, not picked for
- [ ] P3 was skipped for a preset, and the skip was **stated** rather than silent
- [ ] The **breakdown was shown in chat before** the variables question was asked
- [ ] The variables question was **not asked** if the opening message already asked for them
- [ ] **P6 was asked**, and the alignment it produced is the one on the canvas
- [ ] Every specimen uses the **selection's font**, and the font was loaded first
- [ ] The specimen string is **≤ 56 characters**, broken at a word boundary, and identical in
 every row
- [ ] The specimen width was **measured from the real font**, not taken from a formula
- [ ] The probe text node was **removed** — no stray layer left on the canvas
- [ ] Every specimen field is **at most `22 ×` its own font size** — the cap is per row, not the
 largest step's width reused down the table
- [ ] No specimen field is wider than the **text's natural width**, so none is left half empty
- [ ] Every specimen cell is **auto-height**, and nothing clips
- [ ] A4 ran as **six passes**, and every dimension came from `tableLayout` rather than being
 decided while building
- [ ] The **five columns** are the fixed five, in order — none added, dropped or reordered
- [ ] Every cell is **one text node** at a **fixed width**, and for the four metadata columns that
 width is **identical in every row** — verified by reading `x` and `width` back off the
 canvas, not from memory. The specimen is the one per-row width, checked against its own cap
- [ ] The four metadata columns are at **one 12px size** in every row; only the specimen changes
 size
- [ ] The **header row uses the same widths and alignments** as the body rows
- [ ] Numbers are **right-aligned**, labels and the specimen left-aligned
- [ ] `counterAxisAlignItems` is set on **every** row, header included, to the same value
- [ ] If `BASELINE` was refused, the fallback to `MIN` was **stated**
- [ ] Only the **specimen** cell is bound to variables — never a metadata label
- [ ] Any step over **120px** uses the tightened `1.05`, and is reported as tightened
- [ ] Snapped rows are flagged, and the loss of an even ratio was stated
- [ ] The body size is **exactly on the grid** and did not drift from the confirmed base
- [ ] If `meta.tooCoarse`, the collision count and the degeneration to arithmetic were reported
- [ ] No two tokens share a size — snapping collisions were repaired
- [ ] No text node collapsed — `textAutoResize` set before any `FILL`
- [ ] `lineHeight` set as `{ unit, value }`, never a bare number
- [ ] Variables created **only if asked**, in the collection **name the user gave**, with
 explicit `FONT_SIZE` / `LINE_HEIGHT` scopes — never `ALL_SCOPES`
- [ ] Re-running updated variables rather than duplicating them
- [ ] The table is a child of the **page**, clear of existing content
- [ ] Nothing already on the canvas was restyled

Then report: the base, the scale, the step count, the sizes, any tightened or snapped rows, the
table's total width, the row alignment used, the field measure in em and whether the cap or the
measurement set it, where the variables went, and that it is one undo step.

---

## Common edge cases

- **Nothing selected, or not text.** Ask which text to use. Do not invent a base.
- **Several text nodes selected.** List them numbered, with name and size, and ask. Picking the
 first or the largest silently is how the wrong font ends up in the whole scale.
- **An ambiguous reply** — "the bigger one", "whichever". Ask again, more narrowly, naming the
 actual candidates. Do not guess.
- **Mixed formatting.** `fontName` / `fontSize` come back as `figma.mixed`. Use the first styled
 segment and say so, or ask if they differ a lot.
- **The font will not load.** Report the family and style that failed rather than substituting
 Inter — a scale set in the wrong face is worthless.
- **They named a ratio not in `RATIOS`.** Any number works — pass it through as a one-off and say
 it is not one of the named intervals.
- **A big ratio with many steps.** A golden ratio with five steps up reaches 177px at a 16px
 base. `suggestStepsUp` proposes four instead; if they insist on more, build it and name the
 largest size so the consequence is explicit.
- **The table gets wide at large scales.** The field is capped at `22 ×` the step it is set at, so
 a 110px `h1` still gives a 2420px field, and that row is what sets the table's width. The cap is
 doing its job rather than failing, but warn before building, since it is a big frame.
 `layout.tableWidthPx` is the number to quote. Fewer steps up, or a smaller base, is the fix — not
 a narrower field, which just wraps the specimen further.
- **`counterAxisAlignItems = "BASELINE"` is refused.** It is only valid on a `HORIZONTAL` layout,
 so check the row's `layoutMode` was set first. If it still refuses, use `"MIN"` on **every** row
 and say the rows are top-aligned — a table with baseline rows and one top-aligned row is worse
 than a consistently top-aligned one.
- **A metadata string longer than the column.** It cannot happen by construction: `columnWidths`
 measures every cell in the column, header included, and takes the widest. If a cell does look
 clipped, the width was computed from a different string than the one that got set — the two must
 both come from `cellText`.
- **A base under 12px.** The specimen at `small` ends up *smaller* than the 12px metadata. That is
 fine and stays fine: the metadata size is fixed on purpose, so the row still lines up. Do not
 scale the metadata down to match.
- **Whole-pixel rounding after the fact.** Changing a size changes the string in the size column,
 which changes that column's width. Recompute `tableLayout` and rebuild rather than editing cells
 in place, or the columns drift.
- **A condensed or a very wide face.** A condensed face whose 56 characters fit inside 22em gets a
 field at its **natural** width — narrower than the cap, and no wrap. A wide one is held at 22em
 and wraps. `fieldCapped` says which happened; say it either way.
- **A monospace font.** Average advance is closer to 0.6em, so 56 characters wants about 34em, gets
 held at 22em, and wraps to two lines at every step. Correct, and worth saying.
- **Snapping collides.** A tight ratio at small sizes rounds two steps to the same multiple.
 `snapAscending` bumps by one grid unit and counts it — say which rows moved and that the ratio
 is no longer even there. Snapping is **anchored at the body size** and works outward, because
 snapping from one end lets the repair cascade and drift the base: a 16px base with a `1.125`
 ratio and a 4px grid put the body at 20 before this was fixed.
- **A base that is not on the grid.** A grid scale snaps the body too — a 15px base with a 4px
 grid puts `p` at 16. That is the point of a grid scale, but say the base moved rather than
 letting them find it.
- **A preset with a different base.** Tailwind is built on 16px. If the selection is 20px, either
 keep the preset's literal sizes (default) or pass `rebase: true` to scale it all
 proportionally. Say which you did.
- **A split scale where the crossover is above the top step.** It degenerates to a plain modular
 scale on the body ratio. Correct, but say so rather than implying two ratios are in play.
- **They declined variables.** Raw values, and say nothing is bound.
- **The collection name already exists.** Add to it. Two same-named collections is worse.
- **Long example text.** Trimmed to 56 characters at a word boundary before anything is laid out,
 so every row holds the same string. It will still wrap — 56 characters wants ~28em and the field
 is 22em — and it wraps at the same point in every row, which is the intended look.
- **A single word longer than 56 characters.** Hard-cut with an ellipsis, and say so, since the
 specimen will not read as language.
- **More than six steps up.** There are only six CSS heading names, so the extra top steps become
 `display-1`, `display-2`, sitting above `h1`.
- **Awkward numbers.** A 16px base gives `small` 13.93. Offer whole-pixel rounding — or a
 grid-snapped scale, which is the systematic version of the same wish.
- **A baseline grid wanted.** Round line heights up to the nearest 4 or 8px, and say it trades
 ratio exactness for vertical rhythm. This is separate from snapping the *sizes*.
- **`setBoundVariable` refused for a field.** Set the raw value and say the row is not live.
