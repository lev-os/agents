# Visual QA Methodology

Systematic quality assurance combining functional testing, visual inspection, and viewport verification. Treat functional QA and visual QA as separate passes — one does not prove the other.

## Table of Contents
- [QA Inventory](#qa-inventory)
- [Session Loop](#session-loop)
- [Functional QA Checklist](#functional-qa-checklist)
- [Visual QA Checklist](#visual-qa-checklist)
- [Viewport Fit Checks](#viewport-fit-checks)
- [Signoff Criteria](#signoff-criteria)

---

## QA Inventory

Build the inventory **before testing** from three sources:

1. **User's requested requirements** — what was asked for
2. **Implemented features/behaviors** — what you actually built
3. **Claims in the final response** — what you intend to sign off on

Anything in any of those three sources must map to at least one QA check.

### Building the Inventory

For each claim, control, or implemented behavior:

| Field | What to Record |
|-------|---------------|
| **Item** | The user-visible control, feature, or claim |
| **Functional check** | User input → expected visible result |
| **Visual state** | Specific state where visual check must happen |
| **Evidence** | Screenshot or assertion to capture |

- List every meaningful user-facing control, mode switch, or interactive behavior
- List the state changes or view changes each control can cause
- If a requirement is visually central but subjective, convert it into an observable QA check
- Add at least **2 exploratory/off-happy-path scenarios**

### Maintaining the Inventory

Update during testing if:
- Exploration reveals an additional control, state, or visible claim
- A functional pass reveals a visual dependency not previously noted
- An edge case surfaces that should be covered

---

## Session Loop

1. Bootstrap session once, keep Playwright handles alive across iterations
2. Launch the target runtime from the current workspace
3. Make the code change
4. Reload or relaunch using the correct path for that change
5. Update the shared QA inventory if exploration reveals something new
6. Re-run functional QA
7. Re-run visual QA
8. Capture final artifacts only after the current state is the one being evaluated

### Reload Decision

| Change Type | Action |
|-------------|--------|
| Renderer-only change | Reload existing page or Electron window |
| Main-process, preload, or startup change | Relaunch Electron |
| New uncertainty about process ownership | Relaunch instead of guessing |

---

## Functional QA Checklist

- [ ] Use **real user controls** for signoff: keyboard, mouse, click, touch, or Playwright input APIs
- [ ] Verify at least one **end-to-end critical flow**
- [ ] Confirm the **visible result** of that flow, not just internal state
- [ ] For realtime or animation-heavy apps, verify behavior under **actual interaction timing**
- [ ] Work through the **shared QA inventory** rather than ad hoc spot checks
- [ ] Cover every obvious visible control at least once before signoff
- [ ] For reversible controls or stateful toggles, test the **full cycle**: initial → changed → returned to initial
- [ ] After scripted checks pass, do a short **exploratory pass** using normal input for 30-90 seconds
- [ ] If exploratory pass reveals a new state, control, or claim, **add it to inventory** and cover it

### What Counts as Signoff Input

| Counts | Does NOT Count |
|--------|----------------|
| `page.click()`, `page.fill()`, `page.keyboard.press()` | `page.evaluate(() => button.click())` |
| `page.touchscreen.tap()` | `page.evaluate(() => setState(...))` |
| Playwright locator actions | Direct DOM manipulation |

`page.evaluate(...)` and `electronApp.evaluate(...)` may inspect or stage state, but they **do not count as signoff input**.

---

## Visual QA Checklist

- [ ] Treat visual QA as **separate from functional QA**
- [ ] Use the same shared QA inventory — do not start from a different implicit list
- [ ] Restate user-visible claims and verify each one explicitly
- [ ] A user-visible claim is **not signed off** until inspected in the specific state where it's meant to be perceived
- [ ] Inspect the **initial viewport before scrolling**
- [ ] Confirm the initial view supports the interface's primary claims
- [ ] Inspect **all required visible regions**, not just the main interaction surface
- [ ] Inspect the states/modes in the QA inventory, including at least one **post-interaction state**
- [ ] If motion or transitions are part of the experience, inspect at least one **in-transition state**
- [ ] If labels/overlays/annotations track changing content, verify that relationship **after the state change**
- [ ] For dynamic visuals, inspect long enough to judge **stability, layering, and readability**
- [ ] Inspect the **densest realistic state** you can reach, not only empty/loading/collapsed state
- [ ] If there's a defined minimum supported viewport, run a separate visual QA pass there
- [ ] **Distinguish presence from implementation**: if an affordance is there but not perceptible (weak contrast, occlusion, clipping, instability), that's a visual failure
- [ ] If any required region is clipped, cut off, obscured, or outside the viewport, that's a bug even if scroll metrics look fine

### Defect Classes to Check

- Clipping and overflow
- Distortion and misalignment
- Layout imbalance and inconsistent spacing
- Illegible text and weak contrast
- Broken layering (z-index issues)
- Awkward motion states
- Aesthetic coherence — the UI should feel intentional and visually pleasing

### Screenshot Guidance

- Prefer **viewport screenshots** for signoff
- Use full-page captures only as secondary debugging artifacts
- Capture focused screenshots when a region needs closer inspection
- If motion makes a screenshot ambiguous, wait for the UI to settle
- Before signoff, ask: **"What visible part have I not yet inspected closely?"**
- Before signoff, ask: **"What visible defect would most likely embarrass this result?"**

---

## Viewport Fit Checks

Do not assume a screenshot is acceptable just because the main widget is visible.

### Define the Intended Initial View

| Interface Type | Intended Initial View |
|----------------|----------------------|
| Scrollable page | Above-the-fold experience |
| App-like shell, game, editor, dashboard | Full interactive surface + controls + status |
| Electron/desktop app | As-launched window size, placement, and renderer layout |

### Check Rules

1. **Screenshots are primary evidence** for fit — numeric checks support but don't overrule
2. Signoff fails if any required region is **clipped, obscured, or outside viewport** in the initial view
3. Scrolling is acceptable only when the product is **designed to scroll** and the initial view still communicates the core experience
4. For **fixed-shell interfaces**, scrolling is NOT acceptable if needed to reach the primary interactive surface
5. Do not rely on **document scroll metrics alone** — fixed-height shells can clip while page-level metrics look clean
6. **Check region bounds**, not just document bounds — verify each required region fits in the viewport

### Web/Renderer Numeric Check

```javascript
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

### Electron Numeric Check

```javascript
console.log(await appWindow.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Augment with `getBoundingClientRect()` checks for specific required regions when clipping is a realistic failure mode.

---

## Signoff Criteria

### All Must Pass Independently

| Criterion | What It Proves |
|-----------|---------------|
| **Functional correctness** | User input paths work, QA inventory covered |
| **Viewport fit** | Intended initial view visible without unintended clipping/scroll |
| **Visual quality** | UI is coherent, not aesthetically weak for the task |

One does not imply the others.

### Signoff Checklist

- [ ] Functional path passed with **normal user input**
- [ ] Coverage is explicit against inventory: note which requirements, features, controls, states, and claims were exercised
- [ ] **Call out any intentional exclusions**
- [ ] Visual QA pass covered the **whole relevant interface**
- [ ] Each user-visible claim has a matching visual check + reviewed screenshot from the correct state and viewport
- [ ] Viewport-fit checks passed for intended initial view and any minimum supported viewport
- [ ] If the product launches in a window, **as-launched size, placement, and layout** were checked before resize
- [ ] UI is not just functional — it is **visually coherent** and not aesthetically weak
- [ ] Short **exploratory pass** was completed, and the response mentions what it covered
- [ ] If screenshot review and numeric checks **disagreed**, the discrepancy was investigated
- [ ] Include brief **negative confirmation** of defect classes checked and not found (e.g., "No clipping, overflow, contrast, or layering issues found")
- [ ] Cleanup was executed, or session intentionally kept alive for further work
