# AI Visual Analysis

## Table of Contents
- [Why AI Visual Analysis?](#why-ai-visual-analysis)
- [Agent-Native Vision](#agent-native-vision)
- [Screenshot Capture for Analysis](#screenshot-capture-for-analysis)
- [What to Look For](#what-to-look-for)
- [Focus-Specific Guidance](#focus-specific-guidance)
- [Structured Analysis Pattern](#structured-analysis-pattern)
- [Comparison Analysis](#comparison-analysis)
- [Severity Thresholds](#severity-thresholds)
- [Integration with Batch Tests](#integration-with-batch-tests)

---

> **Core principle:** The coding agent (Claude Code, Codex, Gemini CLI) IS the vision model. Capture screenshots with Playwright, emit or save them, and the agent analyzes them directly using its built-in multimodal capabilities. No external vision API calls needed.

## Why AI Visual Analysis?

Traditional visual regression (pixel diff) fails at:

| Scenario | Pixel Diff | Agent Vision |
|----------|------------|--------------|
| Font rendering difference | FALSE POSITIVE | Ignores |
| Button moved 2px | FALSE POSITIVE | Ignores |
| Text truncated/cut off | MISSES | Catches |
| Wrong icon displayed | MISSES | Catches |
| Poor contrast (a11y) | MISSES | Catches |
| Layout broken on mobile | MISSES | Catches |
| "Looks wrong" to human | MISSES | Catches |

**The agent understands semantics.** It answers: "Does this look right?" not "Are pixels identical?"

### Why Agent-Native Is Better Than API Calls

| Factor | External Vision API | Agent-Native |
|--------|-------------------|--------------|
| Cost per image | $0.01–0.05 | $0 (included in agent session) |
| Latency | Network round-trip | Instant (in-context) |
| Context | Image only | Image + full codebase knowledge + task context |
| Interactivity | One-shot | Can zoom in, retake, ask follow-ups |
| API key management | Required | None |
| Provider lock-in | Yes | No — works with any coding agent |

---

## Agent-Native Vision

Each coding agent has built-in image understanding. Emit or save screenshots, and the agent views them directly.

### Codex (js_repl)

```javascript
// Emit screenshot — the agent sees it immediately
var bytes = await page.screenshot({ type: "jpeg", quality: 85, scale: "css" });
await codex.emitImage({ bytes, mimeType: "image/jpeg" });
// Agent now sees the image in context and can reason about it
```

### Claude Code

```javascript
// Save screenshot to a file — the agent reads it with built-in image understanding
await page.screenshot({ path: '/tmp/screenshot-check.png' });
// Agent uses its Read tool on the file to view it natively
```

### Gemini CLI

```javascript
// Same pattern — save to file, agent views it natively
await page.screenshot({ path: '/tmp/screenshot-check.png' });
```

### Mobile Screenshots

```javascript
// Codex
await codex.emitImage({
  bytes: await mobilePage.screenshot({ type: "jpeg", quality: 85, scale: "css" }),
  mimeType: "image/jpeg",
});

// Claude Code / Gemini CLI
await mobilePage.screenshot({ path: '/tmp/mobile-check.png' });
```

---

## Screenshot Capture for Analysis

### Quick Capture Patterns

```javascript
// Viewport screenshot (default — preferred for visual QA)
await page.screenshot({ path: '/tmp/viewport.png' });

// Full-page screenshot (secondary, for scrollable content)
await page.screenshot({ path: '/tmp/fullpage.png', fullPage: true });

// Specific element
await page.locator('[data-testid="dashboard"]').screenshot({ path: '/tmp/widget.png' });

// Clipped region
await page.screenshot({
  path: '/tmp/region.png',
  clip: { x: 0, y: 0, width: 800, height: 600 },
});
```

### Before Taking a Screenshot

```javascript
// Wait for page to be visually stable
await page.waitForLoadState('networkidle');
await page.evaluate(() => document.fonts.ready);

// Optional: disable animations for consistent captures
await page.addStyleTag({
  content: '*, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; }'
});
```

For CSS normalization, coordinate alignment, and click-back helpers, see SCREENSHOTS.md.

---

## What to Look For

When analyzing a screenshot, systematically check:

### 1. Layout Issues
- Overlapping elements
- Misalignment (text, buttons, sections)
- Broken grids or flex layouts
- Uneven spacing or padding
- Elements pushed off-screen

### 2. Content Issues
- Truncated or clipped text
- Missing content that should be visible
- Placeholder text still showing ("Lorem ipsum", "TODO")
- Wrong content in the right place
- Empty states shown when data exists

### 3. Accessibility
- Poor color contrast (text hard to read)
- Text too small to read comfortably
- Missing visual hierarchy (all text same size/weight)
- Focus indicators not visible
- Touch targets too small (< 44px on mobile)

### 4. Mobile-Specific
- Horizontal scroll (content wider than viewport)
- Elements too small to tap
- Text requires zooming to read
- Navigation inaccessible
- Content cut off at viewport edges

### 5. UX & Aesthetics
- Confusing layout (unclear where to look/click)
- Hidden or obscured CTAs
- Poor visual feedback (no loading states, no hover states)
- Inconsistent styling (mixed fonts, colors, spacing)
- Overall aesthetic coherence — does it look intentional?

---

## Focus-Specific Guidance

When analyzing specific page types, prioritize accordingly:

### Dashboard
- Data visualization clarity (charts, gauges, numbers readable?)
- Information hierarchy (most important metrics prominent?)
- Loading states (spinners visible when expected?)
- Empty states handled gracefully?

### Checkout / Forms
- Form field visibility and labels clear?
- Error messages visible and helpful?
- Button prominence (primary CTA clearly visible?)
- Trust signals present (security badges, logos)?
- Price display accurate and visible?

### Mobile Viewport
- Touch target size (minimum 44x44px)
- No horizontal overflow / side scrolling
- Text readable without zooming
- Navigation accessible (hamburger menu works?)
- No content cut off at viewport edges

### Accessibility Focus
- Color contrast ratios (WCAG 2.1 AA: 4.5:1 for text)
- Focus indicators visible
- Text sizing (minimum 16px body on mobile)
- Visual alternatives for color-coded information
- Keyboard navigation hints visible

---

## Structured Analysis Pattern

When performing visual QA, structure your findings consistently:

### Analysis Template

```
Assessment: pass | warning | fail
Confidence: 0-100

Summary: [one-sentence overall assessment]

Issues:
1. [severity: critical|major|minor|info] [category: layout|accessibility|content|mobile|ux]
   Description: What's wrong
   Location: Where on the page
   Fix: Suggested fix

Negative confirmation: No [defect classes checked] found.
```

### Example Analysis

```
Assessment: warning
Confidence: 85

Summary: Dashboard loads correctly but has minor spacing issues in the sidebar.

Issues:
1. [minor] [layout] Sidebar navigation items have inconsistent vertical spacing —
   "Settings" has 8px gap above while others have 12px. Location: left sidebar.
   Fix: Normalize padding-top on .nav-item elements.

2. [info] [ux] The "Last updated" timestamp in the header is light gray on white,
   low contrast but still readable. Location: top-right header area.
   Fix: Darken to #666 or use the secondary text color token.

Negative confirmation: No clipping, overflow, broken layouts, missing content,
or accessibility blockers found.
```

---

## Comparison Analysis

When comparing before/after screenshots (e.g., after a code change):

### What to Capture

```javascript
// Before the change
await page.screenshot({ path: '/tmp/before.png' });

// Make the code change, reload
await page.reload({ waitUntil: 'domcontentloaded' });

// After the change
await page.screenshot({ path: '/tmp/after.png' });
```

### What to Report

Categorize each difference:

| Category | Meaning | Action |
|----------|---------|--------|
| **Intentional** | Expected change based on the task | Verify it matches intent |
| **Unintentional** | Something changed that shouldn't have | Investigate as regression |
| **Missing** | Expected change is not present | Implementation may be incomplete |

### Multi-Viewport Comparison

```javascript
// Desktop before/after
await page.screenshot({ path: '/tmp/desktop-before.png' });
// ... make change ...
await page.screenshot({ path: '/tmp/desktop-after.png' });

// Mobile before/after
await mobilePage.screenshot({ path: '/tmp/mobile-before.png' });
// ... reload ...
await mobilePage.screenshot({ path: '/tmp/mobile-after.png' });
```

---

## Severity Thresholds

### When to Flag vs Ignore

```
FAIL (must fix):
- Any critical issue (broken layout, unreadable content, app unusable)
- Multiple major issues in the same view
- Accessibility blocker (text unreadable, controls unreachable)

WARNING (should fix):
- Single major issue that doesn't block usage
- Multiple minor issues suggesting systematic problem
- Mobile-only issue on a mobile-first product

PASS:
- No issues found
- Only info-level observations
- Minor issues that don't affect usability
```

### Structured Decision

| Condition | Result |
|-----------|--------|
| Any critical issue | FAIL |
| 3+ major issues | FAIL |
| 1-2 major issues | WARNING |
| Minor issues only (≤ 5) | PASS |
| Info-level only | PASS |

---

## Integration with Batch Tests

### Pixel-Level Regression (No Agent Needed)

For CI pipelines without an agent present, use Playwright's built-in `toHaveScreenshot()`:

```typescript
test('dashboard visual regression', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,
    animations: 'disabled',
  });
});
```

### Agent-Driven CI (Agent Present)

When an agent runs in CI (via `claude-code-action` or similar), it views screenshots natively — same as interactive mode. See ADVANCED-TECHNIQUES.md for agent-driven CI QA patterns.

### Combining Both

```
CI Pipeline:
1. Playwright runs → toHaveScreenshot() catches pixel regressions automatically
2. Agent runs → views screenshots of failures, triages intelligently
3. Agent reports findings as PR comment with embedded screenshots
```

---

## When to Use Visual Analysis

| Scenario | Approach |
|----------|----------|
| **Interactive QA session** | Agent takes + views screenshots directly |
| **After UI changes** | Before/after comparison |
| **CI with agent** | Agent views failure screenshots in CI |
| **CI without agent** | `toHaveScreenshot()` pixel regression only |
| **Mobile verification** | Agent views mobile viewport screenshots |
| **Design fidelity check** | Agent compares mockup vs implementation |
