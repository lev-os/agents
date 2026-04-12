# Systematic Testing

Workflow patterns and methodology for thorough, disciplined UI testing. These patterns prevent the common failure mode where agents build an entire page and only look at it once at the end.

> **Core principle:** Don't build blind. Every component gets verified as it's built, not after the whole page is done. Mechanical issues are caught programmatically; aesthetic issues are caught visually; coverage gaps are caught systematically.

## Table of Contents
- [Human-Like Interaction](#human-like-interaction)
- [Edit-Reload-Verify Micro-Loop](#edit-reload-verify-micro-loop)
- [State Matrix Sweep](#state-matrix-sweep)
- [Interactive State Catalog](#interactive-state-catalog)
- [Peripheral Vision Check](#peripheral-vision-check)
- [Failure Injection Pass](#failure-injection-pass)

---

## Human-Like Interaction

**The most dangerous trap for agent QA:** interacting with pages programmatically via `page.evaluate()` or direct DOM manipulation instead of through Playwright's action methods (`.click()`, `.fill()`, `.press()`). This produces misleading results because the agent bypasses the same barriers a real user would hit.

### The Problem

```javascript
// ❌ WRONG — bypasses all real-user constraints
await page.evaluate(() => {
  document.querySelector('#submit').click();  // Works even if button is hidden behind a modal
});

// ❌ WRONG — sets value without triggering input events
await page.evaluate(() => {
  document.querySelector('#email').value = 'test@example.com';
});

// ✅ RIGHT — uses Playwright's action methods
await page.locator('#submit').click();  // Fails if element is obscured, hidden, or disabled
await page.locator('#email').fill('test@example.com');  // Triggers focus, input, change events
```

### Why Playwright Actions Are Better Than evaluate()

Playwright's action methods (`.click()`, `.fill()`, `.check()`, `.press()`, `.selectOption()`) perform **actionability checks** before acting:

| Check | What It Prevents |
|-------|------------------|
| **Visible** | Clicking hidden elements that users can't see |
| **Stable** | Clicking during animations before element settles |
| **Enabled** | Clicking disabled buttons |
| **Not obscured** | Clicking elements hidden behind modals, overlays, or other elements |
| **Receives events** | Clicking elements with `pointer-events: none` |
| **Editable** | Typing into read-only or disabled inputs |

`page.evaluate()` bypasses ALL of these checks. A button that's completely hidden behind a modal overlay will "work" via `evaluate()` but be untouchable by a real user.

### Rules for Realistic Interaction

1. **Always use Playwright action methods for functional QA:**

```javascript
// Click
await page.locator('button', { hasText: 'Submit' }).click();
await page.getByRole('button', { name: 'Submit' }).click();

// Fill forms
await page.getByLabel('Email').fill('test@example.com');
await page.getByLabel('Password').fill('secret123');

// Keyboard
await page.keyboard.press('Enter');
await page.keyboard.press('Tab');
await page.keyboard.press('Escape');

// Select
await page.getByLabel('Country').selectOption('US');

// Check/uncheck
await page.getByLabel('I agree').check();
```

2. **Reserve `page.evaluate()` ONLY for:**
   - Reading state (getting text, checking computed styles)
   - Setting up test conditions (injecting data, simulating states)
   - DOM health checks and diagnostics
   - Situations where there is no user-facing equivalent

3. **When `.click()` fails, that IS the bug:**

```javascript
// If this fails because the element is obscured:
await page.locator('#submit-btn').click();
// ↑ The error message tells you WHY a real user can't click it:
//   "element is not visible"
//   "element is behind another element <div class='modal-overlay'>"
//   "element is disabled"
//   "element is outside of the viewport"
//
// Don't "fix" this by switching to evaluate() — fix the underlying UI bug!
```

### Detecting Obscured Elements Programmatically

Add this check to the DOM health check or run it standalone — it finds interactive elements that exist in the DOM but can't be clicked by a real user:

```javascript
async function findObscuredInteractives(page) {
  return page.evaluate(() => {
    const issues = [];
    const interactives = document.querySelectorAll(
      'a[href], button, input, select, textarea, [role="button"], [onclick]'
    );

    for (const el of interactives) {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) continue;

      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') continue;

      // Check what element is actually at this position
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const topElement = document.elementFromPoint(centerX, centerY);

      if (topElement && topElement !== el && !el.contains(topElement) && !topElement.closest(el.tagName === 'A' ? 'a' : el.tagName.toLowerCase())) {
        const tag = el.tagName.toLowerCase();
        const id = el.id ? '#' + el.id : '';
        const text = (el.textContent || '').trim().slice(0, 30);

        const blockerTag = topElement.tagName.toLowerCase();
        const blockerId = topElement.id ? '#' + topElement.id : '';
        const blockerClass = topElement.className && typeof topElement.className === 'string'
          ? '.' + topElement.className.trim().split(/\s+/)[0]
          : '';

        issues.push({
          element: tag + id + (text ? ' "' + text + '"' : ''),
          blockedBy: blockerTag + blockerId + blockerClass,
          position: { x: Math.round(centerX), y: Math.round(centerY) },
          severity: 'critical',
          detail: 'Interactive element is obscured by another element — users cannot click it',
          fix: 'Check z-index, position, and stacking order. The blocking element may be an overlay, modal backdrop, or incorrectly positioned sibling.',
        });
      }
    }

    return issues;
  });
}
```

### Pointer-Events Check

Another common invisible blocker — `pointer-events: none` makes elements unclickable even though they look normal:

```javascript
async function findPointerEventsDisabled(page) {
  return page.evaluate(() => {
    const issues = [];
    const interactives = document.querySelectorAll(
      'a[href], button, input, [role="button"], [onclick]'
    );

    for (const el of interactives) {
      const style = getComputedStyle(el);
      if (style.pointerEvents === 'none') {
        const tag = el.tagName.toLowerCase();
        const text = (el.textContent || '').trim().slice(0, 30);
        issues.push({
          element: tag + (el.id ? '#' + el.id : '') + (text ? ' "' + text + '"' : ''),
          severity: 'critical',
          detail: 'Interactive element has pointer-events: none — visually present but unclickable',
          fix: 'Remove pointer-events: none from this element or its ancestor',
        });
      }
    }
    return issues;
  });
}
```

### Quick Rule

> **If you're reaching for `page.evaluate()` to trigger an interaction, stop and ask: "Could a human do this?" If yes, use Playwright's action method instead. If the action method fails, that failure IS the bug.**

---

## Edit-Reload-Verify Micro-Loop

The single most important workflow improvement for agent-driven UI development. Instead of build-everything-then-look, verify after every meaningful change.

### The Loop

```
┌──────────────────────────────────────────────────────────┐
│                    EDIT-RELOAD-VERIFY                      │
│                                                          │
│  1. Make code change (one component / one fix)           │
│           ↓                                              │
│  2. Reload page                                          │
│           ↓                                              │
│  3. Layout snapshot diff (structural)                    │
│     ├─ Unexpected changes? → Stop, investigate           │
│     └─ Only expected changes? → Continue                 │
│           ↓                                              │
│  4. Run DOM health check (programmatic)                  │
│     ├─ Issues found? → Fix them, go to step 2           │
│     └─ Clean? → Continue                                 │
│           ↓                                              │
│  5. Take screenshot (aesthetic verification only)        │
│     ├─ Problems? → Fix them, go to step 1                │
│     └─ Looks good? → Continue                            │
│           ↓                                              │
│  6. Move to next component                               │
│           ↓                                              │
│     (Repeat 1-5 for each component)                      │
│           ↓                                              │
│  7. Final: full-page screenshot + signoff                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### Step 1: Make one focused change

One component, one style fix, one layout adjustment. Not three things at once. If something breaks, you know exactly what caused it.

#### Step 2: Reload

```javascript
await page.reload({ waitUntil: 'domcontentloaded' });
// For apps with client-side hydration, also wait:
await page.waitForLoadState('networkidle');
```

#### Step 3: Layout snapshot diff (catches unintended structural changes)

```javascript
// "before" was captured at end of previous iteration (or before first change)
const after = await captureLayoutSnapshot(page);
const diff = diffLayoutSnapshots(before, after);

if (diff.summary.hasUnexpected) {
  console.log('UNEXPECTED LAYOUT CHANGES:');
  for (const d of diff.diffs.filter(d => d.unexpected)) {
    console.log(`  ${d.selector}: ${d.changes?.[0]?.detail || d.detail}`);
  }
  // Stop and investigate — your change broke something else
}
// This snapshot becomes "before" for next iteration
before = after;
```

Skip this step for the very first change (no baseline yet). After that, each "after" becomes the next "before".

#### Step 4: DOM health check (catches mechanical bugs)

```javascript
const health = await domHealthCheck(page);
if (health.bySeverity.critical > 0 || health.bySeverity.major > 0) {
  // Fix these before proceeding — don't screenshot a broken page
  for (const issue of health.issues.filter(i => i.severity === 'critical' || i.severity === 'major')) {
    console.log(`FIX: [${issue.severity}] ${issue.detail}`);
    console.log(`  → ${issue.fix}`);
  }
  // Go back to step 1 and fix
}
```

#### Step 5: Screenshot + visual check (aesthetic verification only)

```javascript
await page.screenshot({ path: '/tmp/verify-step-N.png' });
// Agent views the screenshot and checks:
// - Does this component look correct?
// - Does it fit naturally with surrounding content?
// - Is spacing/alignment consistent with the rest of the page?
// Note: structural correctness was already verified by snapshot diff
```

#### Step 6: Move to next component

Only after the current component passes all three checks.

#### Step 7: Final full-page verification

```javascript
// Desktop
await page.screenshot({ path: '/tmp/final-desktop.png' });

// Mobile (resize or use mobile context)
await page.setViewportSize({ width: 375, height: 667 });
await page.screenshot({ path: '/tmp/final-mobile.png' });

// Full page (scrollable content)
await page.screenshot({ path: '/tmp/final-fullpage.png', fullPage: true });
```

### When to Use Which Check

| Situation | Snapshot Diff | DOM Health Check | Screenshot |
|-----------|:---:|:---:|:---:|
| After CSS layout change | Yes | Yes | Yes |
| After adding new component | Yes | Yes | Yes |
| After text content change | Yes | No | Yes |
| After color/theme change | No | No | Yes |
| After responsive breakpoint work | Yes | Yes | Yes |
| After fixing a health check issue | Yes | Yes | No (unless visual fix) |
| Quick "did my change work?" | Yes | No | Yes |
| Before signoff | No (use full suite) | Yes | Yes |

### Anti-Patterns

- **Building an entire page before looking** — The #1 failure mode. Errors compound, making it harder to find which change caused which problem.
- **Only running DOM health check** — Catches mechanical bugs but misses aesthetic issues, wrong content, and design intent mismatches.
- **Only taking screenshots** — Misses issues the agent can't always spot visually (overflow clipped to invisible, small touch targets, missing alt text).
- **Skipping reload** — Stale page state masks new bugs or hides fixes.
- **Making multiple changes between verifications** — When something breaks, you can't tell which change caused it.

---

## State Matrix Sweep

Agents almost always test only: `desktop + happy path + light mode + logged in`. This leaves the vast majority of states untested. A state matrix systematically covers the combinations that matter.

### Defining the Matrix

Identify the dimensions relevant to your app:

```javascript
const STATE_MATRIX = {
  viewport: [
    { name: 'mobile', width: 375, height: 667 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'desktop', width: 1440, height: 900 },
  ],
  data: [
    { name: 'empty', setup: async (page) => {
      // Clear data or navigate to empty state
      await page.evaluate(() => {
        document.querySelectorAll('[data-testid="item"]').forEach(el => el.remove());
      });
    }},
    { name: 'typical', setup: async (page) => {
      // Default state — no changes needed
    }},
    { name: 'overflow', setup: async (page) => {
      // Inject long text, many items
      await page.evaluate(() => {
        document.querySelectorAll('[data-testid="title"]').forEach(el => {
          el.textContent = 'A'.repeat(200);
        });
      });
    }},
  ],
  theme: [
    { name: 'light', setup: async (page) => {
      await page.evaluate(() => document.documentElement.classList.remove('dark'));
    }},
    { name: 'dark', setup: async (page) => {
      await page.evaluate(() => document.documentElement.classList.add('dark'));
    }},
  ],
};
```

### Sweep Execution

```javascript
async function stateMatrixSweep(page, matrix, options = {}) {
  const {
    url = null,
    screenshotDir = '/tmp/matrix',
    runHealthCheck = true,
  } = options;

  const results = [];
  const dimensions = Object.entries(matrix);

  // Generate all combinations
  function* combinations(dims, current = {}) {
    if (dims.length === 0) {
      yield { ...current };
      return;
    }
    const [dimName, states] = dims[0];
    const rest = dims.slice(1);
    for (const state of states) {
      yield* combinations(rest, { ...current, [dimName]: state });
    }
  }

  const combos = [...combinations(dimensions)];
  console.log(`State matrix: ${combos.length} combinations`);

  for (const combo of combos) {
    // Build descriptive name
    const parts = Object.entries(combo).map(([dim, state]) => state.name);
    const label = parts.join('-');

    // Apply viewport
    if (combo.viewport) {
      await page.setViewportSize({
        width: combo.viewport.width,
        height: combo.viewport.height,
      });
    }

    // Navigate if needed
    if (url) {
      await page.goto(url, { waitUntil: 'domcontentloaded' });
    } else {
      await page.reload({ waitUntil: 'domcontentloaded' });
    }

    // Apply each state's setup (skip viewport, already applied)
    for (const [dimName, state] of Object.entries(combo)) {
      if (dimName !== 'viewport' && state.setup) {
        await state.setup(page);
      }
    }

    // Wait for settle
    await page.waitForTimeout(200);

    // Health check
    let health = null;
    if (runHealthCheck) {
      health = await domHealthCheck(page);
    }

    // Screenshot
    const filename = `${screenshotDir}/${label}.png`;
    await page.screenshot({ path: filename });

    const result = {
      label,
      states: Object.fromEntries(Object.entries(combo).map(([k, v]) => [k, v.name])),
      screenshot: filename,
      healthIssues: health?.issueCount ?? null,
      criticalOrMajor: (health?.bySeverity?.critical ?? 0) + (health?.bySeverity?.major ?? 0),
    };
    results.push(result);

    const status = result.criticalOrMajor > 0
      ? `⚠ ${result.criticalOrMajor} critical/major`
      : '✓';
    console.log(`  ${label}: ${status}`);
  }

  // Summary
  const failing = results.filter(r => r.criticalOrMajor > 0);
  console.log(`\nMatrix sweep complete: ${results.length} combinations`);
  if (failing.length > 0) {
    console.log(`Failing combinations (${failing.length}):`);
    for (const f of failing) {
      console.log(`  ${f.label}: ${f.criticalOrMajor} critical/major issues`);
    }
  }

  return results;
}
```

### Usage

```javascript
const results = await stateMatrixSweep(page, STATE_MATRIX, {
  url: 'http://127.0.0.1:3000/dashboard',
  screenshotDir: '/tmp/dashboard-matrix',
});

// Agent reviews screenshots of failing combinations first,
// then spot-checks a sample of passing ones
```

### High-Value State Combinations

These specific combinations catch the most bugs. If you can't test the full matrix, test at least these:

| Combination | Why It Catches Bugs |
|-------------|---------------------|
| `mobile + empty` | Empty states often have no mobile layout |
| `mobile + overflow` | Long text breaks mobile layouts first |
| `desktop + empty` | Huge empty void with no content is ugly |
| `dark + error` | Error messages designed for light mode become invisible |
| `tablet + many-items` | Grid reflow + scroll behavior edge case |
| `mobile + dark + logged-out` | The least-tested combination; often completely broken |

### Keeping the Matrix Manageable

The full Cartesian product can be large (3 viewports × 3 data × 2 themes = 18 screenshots). To keep it practical:

1. **Start with the high-value combinations** (table above) — catch the most bugs with fewest tests
2. **Add full matrix for critical pages** — the landing page, dashboard, checkout
3. **Use breakpoint sweep separately** for responsive-only concerns (no state variations)
4. **Skip redundant combinations** — if light/dark doesn't affect a page (no theme support), drop that dimension

---

## Interactive State Catalog

A systematic reference of UI states that agents should test for each component type. Most agents only test the default happy-path state. This catalog ensures coverage of every meaningful state.

### Universal States (Test for Every Component)

| State | Description | How to Trigger |
|-------|-------------|---------------|
| **Default** | Initial render | Page load |
| **Loading** | Data still fetching | Intercept network, or inject skeleton |
| **Empty** | No data / no items | Clear content |
| **Error** | Operation failed | Inject error state |
| **Overflow** | Content exceeds bounds | Inject very long text |

### Button States

| State | How to Test |
|-------|------------|
| Default | Screenshot on load |
| Hover | `await button.hover()` |
| Focus | `await button.focus()` |
| Active/Pressed | `mouse.down()` on button position |
| Disabled | `el.disabled = true` |
| Loading | `el.textContent = 'Loading...'; el.disabled = true` |
| With long text | `el.textContent = 'Confirm and Submit This Very Long Action'` |

### Form Input States

| State | How to Test |
|-------|------------|
| Empty | Clear field |
| Filled | `.fill('test value')` |
| Focused | `.focus()` |
| Error / Invalid | Fill invalid value + `form.reportValidity()` |
| Disabled | `el.disabled = true` |
| Read-only | `el.readOnly = true` |
| With very long value | `.fill('A'.repeat(200))` |
| With special characters | `.fill('O\'Brien <script>alert(1)</script>')` |
| Placeholder visible | Clear field, check placeholder styling |
| With helper text | Check helper/hint text below field |

### Navigation States

| State | How to Test |
|-------|------------|
| Default | Page load |
| Active page highlighted | Navigate to each page, verify active indicator |
| Mobile hamburger closed | Mobile viewport, screenshot |
| Mobile hamburger open | Click hamburger, screenshot |
| With many items | Inject additional nav items |
| With very long labels | Inject long text into nav items |
| Sticky behavior | Scroll down 500px, screenshot |

### List/Table States

| State | How to Test |
|-------|------------|
| Empty | Remove all items |
| Single item | Keep only one item |
| Few items (< 5) | Normal load |
| Many items (50+) | Duplicate items |
| With pagination | Navigate to page 2+ |
| Loading | Replace with skeleton rows |
| Error | Replace with error message |
| With very wide content | Inject long text in a cell |
| Sorted (ascending) | Click sort header |
| Sorted (descending) | Click sort header twice |
| Filtered (no results) | Apply filter that matches nothing |

### Modal/Dialog States

| State | How to Test |
|-------|------------|
| Closed | Default |
| Open | Trigger modal open |
| With backdrop | Verify overlay behind modal |
| With long content | Inject tall content, check scroll behavior |
| Mobile viewport | Open on mobile, check full-screen behavior |
| With form inside | Fill form, check error states |
| Dismiss via backdrop click | Click outside modal |
| Dismiss via Escape key | `await page.keyboard.press('Escape')` |

### Card/Widget States

| State | How to Test |
|-------|------------|
| Default | Page load |
| Loading | Replace content with skeleton |
| Empty | Clear content |
| With image | Verify image loads |
| With broken image | Set `src` to invalid URL |
| With long title | Inject long title text |
| Hover (if interactive) | `.hover()` |
| Selected/active | Toggle selection |

### Toast/Notification States

| State | How to Test |
|-------|------------|
| Success | Trigger success action |
| Error | Trigger error action |
| Warning | Trigger warning |
| Info | Trigger info |
| With long message | Inject long text |
| Multiple simultaneous | Trigger several in sequence |
| Auto-dismiss | Wait for auto-dismiss timer |
| Manual dismiss | Click close button |

### Component State Testing Protocol

For each component you build or modify:

1. **Identify applicable states** from the catalogs above
2. **Test default state first** — this is your baseline
3. **Test error/empty states next** — these are most often broken
4. **Test overflow states** — text wrapping/truncation is a common failure
5. **Test interactive states** (hover, focus, disabled) — often unstyled
6. **Screenshot evidence** for each state that matters for signoff
7. **DOM health check** at each state — catches overflow, small targets

---

## Peripheral Vision Check

After fixing a visual issue, agents often create new problems in adjacent areas. The peripheral vision check prevents this.

### The Pattern

```
1. Fix an issue in component A
2. Reload
3. Verify component A is fixed (screenshot)
4. ★ Also screenshot components adjacent to A
5. Compare adjacent areas to pre-fix state
6. If anything changed unexpectedly → investigate
```

### Implementation

```javascript
async function peripheralCheck(page, fixedSelector, adjacentSelectors) {
  // Screenshot the fixed element
  const fixedEl = page.locator(fixedSelector);
  await fixedEl.screenshot({ path: '/tmp/fixed-element.png' });

  // Screenshot each adjacent element
  for (const [name, sel] of Object.entries(adjacentSelectors)) {
    const el = page.locator(sel);
    if (await el.isVisible()) {
      await el.screenshot({ path: `/tmp/adjacent-${name}.png` });
    }
  }

  // Run DOM health check on the whole page
  const health = await domHealthCheck(page);
  if (health.issueCount > 0) {
    console.log('Peripheral check found issues:');
    for (const issue of health.issues) {
      console.log(`  [${issue.severity}] ${issue.detail}`);
    }
  }

  return health;
}

// Usage after fixing a header layout issue:
await peripheralCheck(page, 'header', {
  'hero': '[data-testid="hero-section"]',
  'nav': 'nav',
  'sidebar': '[data-testid="sidebar"]',
  'first-section': 'main > section:first-child',
});
```

### What to Watch For

| Change Type | Common Peripheral Damage |
|-------------|--------------------------|
| Changed element width | Adjacent elements reflow, change size |
| Changed margin/padding | Sibling elements shift position |
| Changed position/z-index | Overlapping with previously separated elements |
| Changed font size | Line heights change, vertical rhythm breaks |
| Changed flex properties | Sibling flex items redistribute space |
| Changed grid template | Grid items jump to different cells |
| Changed overflow | Previously hidden content now visible (or vice versa) |

### Quick Peripheral Check (No Helper Needed)

For a fast peripheral check without the helper function:

```javascript
// Take full-page screenshot before the fix
await page.screenshot({ path: '/tmp/before-fix.png', fullPage: true });

// Make the fix, reload
await page.reload({ waitUntil: 'domcontentloaded' });

// Take full-page screenshot after the fix
await page.screenshot({ path: '/tmp/after-fix.png', fullPage: true });

// Agent compares both screenshots:
// - Is the fix visible?
// - Did anything ELSE change?
// - Are adjacent areas still correct?
```

This before/after pattern is the simplest way to catch peripheral damage and requires no setup. The agent's built-in vision compares the two screenshots for unintended differences.

---

## Failure Injection Pass

After functional QA confirms the happy path works and visual QA confirms it looks right, run a failure injection pass to verify the app handles errors gracefully. This is a separate pass — don't mix it into the Edit-Reload-Verify loop.

### When to Run

```
Edit-Reload-Verify (per component)
    ↓
Functional QA (happy path)
    ↓
Visual QA (aesthetic check)
    ↓
★ Failure Injection Pass ← here
    ↓
Signoff
```

Run failure injection **after** the happy path is confirmed working. Testing error handling on broken code just generates noise.

### Minimum Viable Pass (30 seconds)

At minimum, test two things:

1. **Block all API calls** — does the page show an error state or go blank?
2. **Wipe storage and reload** — does the app recover or crash?

```javascript
// 1. Block all APIs
const inj = await injectNetworkFailure(page, '**/api/**', 'abort', { log: false });
await page.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
const blankOnAbort = await page.evaluate(() => document.body.innerText.trim().length < 20);
await page.screenshot({ path: '/tmp/smoke-apis-down.png' });
await inj.remove();

// 2. Wipe storage
await page.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
await corruptSessionState(page, 'wipe-storage');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
const blankOnWipe = await page.evaluate(() => document.body.innerText.trim().length < 20);
await page.screenshot({ path: '/tmp/smoke-storage-wiped.png' });

console.log(`APIs down: ${blankOnAbort ? 'FAIL' : 'PASS'}`);
console.log(`Storage wiped: ${blankOnWipe ? 'FAIL' : 'PASS'}`);
```

### Full Pass

For thorough coverage, use the `failureResilienceAudit` orchestrator. It discovers network dependencies, tests each with multiple failure modes, and generates a resilience scorecard.

**Full details:** FAILURE-INJECTION.md

### What to Fix vs. Accept

| Finding | Action |
|---------|--------|
| Blank page on any API error | Fix immediately — critical |
| Raw error text shown to user (`TypeError`, `undefined`) | Fix immediately — major |
| No error message when API fails (page looks normal but data missing) | Fix — user doesn't know something went wrong |
| Error message shown but no retry/recovery option | Acceptable for v1, improve later |
| Form data lost after failed submission | Fix — users hate re-entering data |
| Double-click sends duplicate requests | Fix for payment/order flows, warn for others |
| Storage wipe causes crash | Fix — this happens in incognito mode |
