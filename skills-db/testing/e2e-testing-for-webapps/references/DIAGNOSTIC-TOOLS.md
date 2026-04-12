# Diagnostic Tools

Programmatic utilities that detect visual bugs, extract layout context, and automate multi-viewport testing — giving agents structured, actionable data instead of relying solely on screenshot inspection.

> **Key insight:** Agents don't need to "see" every bug. Many visual issues (overflow, small touch targets, missing alt text, layout shift risk) are detectable programmatically. Run diagnostics FIRST, fix mechanical issues, THEN take screenshots for aesthetic/semantic review.

## Table of Contents
- [DOM Health Check](#dom-health-check)
- [Computed Styles Extraction](#computed-styles-extraction)
- [Layout Snapshot Diffing](#layout-snapshot-diffing)
- [Responsive Breakpoint Sweep](#responsive-breakpoint-sweep)
- [Interactive State Triggers](#interactive-state-triggers)
- [Failure Mode Injection](#failure-mode-injection) (separate doc)

---

## DOM Health Check

A single `page.evaluate()` call that detects common visual bugs and returns structured JSON. No screenshot needed. Run this **before** taking screenshots to catch mechanical issues first.

### When to Run

- After every page load or reload during development
- Before taking any QA screenshot
- After CSS changes that affect layout
- As part of the Edit-Reload-Verify micro-loop (see SYSTEMATIC-TESTING.md)

### The Function

```javascript
async function domHealthCheck(page) {
  return page.evaluate(() => {
    const issues = [];
    const vw = window.innerWidth;
    const vh = window.innerHeight;

    // ── Helpers ──────────────────────────────────────────

    function describe(el) {
      if (!el || el === document.body) return 'body';
      const tag = el.tagName.toLowerCase();
      const id = el.id ? '#' + el.id : '';
      const testId = el.dataset?.testid ? '[data-testid="' + el.dataset.testid + '"]' : '';
      const cls = (typeof el.className === 'string' && el.className)
        ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.')
        : '';
      return (tag + id + testId + cls).slice(0, 100);
    }

    function selector(el) {
      if (el.id) return '#' + el.id;
      if (el.dataset?.testid) return '[data-testid="' + el.dataset.testid + '"]';
      const tag = el.tagName.toLowerCase();
      const parent = el.parentElement;
      if (!parent || parent === document.documentElement) return tag;
      const siblings = [...parent.children].filter(c => c.tagName === el.tagName);
      const idx = siblings.indexOf(el);
      const nth = siblings.length > 1 ? ':nth-of-type(' + (idx + 1) + ')' : '';
      return selector(parent) + ' > ' + tag + nth;
    }

    function isVisible(el, style) {
      if (style.display === 'none') return false;
      if (style.visibility === 'hidden') return false;
      if (parseFloat(style.opacity) === 0) return false;
      return true;
    }

    function isInteractive(el) {
      return el.matches(
        'a[href], button, input, select, textarea, ' +
        '[role="button"], [role="link"], [role="tab"], [role="menuitem"], ' +
        '[onclick], [tabindex]:not([tabindex="-1"])'
      );
    }

    // ── 1. Page-Level Horizontal Scroll ──────────────────

    const docScrollW = document.documentElement.scrollWidth;
    if (docScrollW > vw + 2) {
      issues.push({
        severity: 'critical',
        category: 'viewport',
        element: 'html',
        selector: 'html',
        detail: 'Page has horizontal scroll (' + docScrollW + 'px content > ' + vw + 'px viewport)',
        fix: 'Find widest element: run [...document.body.querySelectorAll("*")].reduce((a,b) => a.getBoundingClientRect().right > b.getBoundingClientRect().right ? a : b)',
      });
    }

    // ── Element-Level Checks ─────────────────────────────

    const allEls = document.querySelectorAll('body *');
    const interactiveRects = []; // for overlap detection

    for (const el of allEls) {
      const style = getComputedStyle(el);
      if (!isVisible(el, style)) continue;

      const rect = el.getBoundingClientRect();

      // Skip zero-size unless it has content (checked separately)
      const hasSize = rect.width > 0 && rect.height > 0;

      // ── 2. Element Extends Beyond Viewport ─────────

      if (hasSize && rect.width > 10 && rect.height > 10) {
        // Only flag substantial elements, not tiny decorative ones
        if (rect.right > vw + 10) {
          issues.push({
            severity: 'major',
            category: 'viewport',
            element: describe(el),
            selector: selector(el),
            detail: 'Extends ' + Math.round(rect.right - vw) + 'px beyond right viewport edge (right: ' + Math.round(rect.right) + ', viewport: ' + vw + ')',
            fix: 'Check width, margin, padding, or position. Common causes: fixed width wider than viewport, negative margin on parent, absolutely positioned without max-width',
          });
        }
        if (rect.left < -10) {
          issues.push({
            severity: 'major',
            category: 'viewport',
            element: describe(el),
            selector: selector(el),
            detail: 'Extends ' + Math.round(Math.abs(rect.left)) + 'px beyond left viewport edge',
            fix: 'Check margin-left, transform: translateX, or left position value',
          });
        }
      }

      // ── 3. Content Overflow (Clipped Without Indicator) ──

      if (hasSize) {
        const overflowsH = el.scrollWidth > el.clientWidth + 2;
        const overflowsV = el.scrollHeight > el.clientHeight + 2;

        if (overflowsH && (style.overflowX === 'hidden' || style.overflow === 'hidden')) {
          const hasEllipsis = style.textOverflow === 'ellipsis';
          if (!hasEllipsis && el.textContent.trim().length > 0) {
            issues.push({
              severity: 'warning',
              category: 'overflow',
              element: describe(el),
              selector: selector(el),
              detail: 'Text overflows horizontally (' + el.scrollWidth + 'px > ' + el.clientWidth + 'px) and is clipped without ellipsis',
              fix: 'Add text-overflow: ellipsis + white-space: nowrap, or use overflow-wrap: break-word, or increase container width',
            });
          }
        }

        if (overflowsV && style.overflowY === 'hidden' && el.textContent.trim().length > 20) {
          issues.push({
            severity: 'warning',
            category: 'overflow',
            element: describe(el),
            selector: selector(el),
            detail: 'Content overflows vertically (' + el.scrollHeight + 'px > ' + el.clientHeight + 'px) and is clipped',
            fix: 'Increase height, use overflow-y: auto for scrolling, or add line-clamp',
          });
        }
      }

      // ── 4. Zero-Dimension Elements With Content ────────

      if (!hasSize && el.childNodes.length > 0) {
        const textContent = el.textContent.trim();
        if (textContent.length > 0 && !el.closest('[style*="display: none"]')) {
          // Verify it's not just whitespace in a layout container
          const hasDirectText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
          if (hasDirectText) {
            issues.push({
              severity: 'warning',
              category: 'layout',
              element: describe(el),
              selector: selector(el),
              detail: 'Element has text content but renders at 0×0 pixels',
              fix: 'Check display, width, height, or parent flex/grid properties that might collapse this element',
            });
          }
        }
      }

      // ── 5. Small Touch Targets ────────────────────────

      if (hasSize && isInteractive(el)) {
        const touchW = Math.max(rect.width, parseFloat(style.minWidth) || 0);
        const touchH = Math.max(rect.height, parseFloat(style.minHeight) || 0);
        if (touchW < 44 || touchH < 44) {
          issues.push({
            severity: 'minor',
            category: 'accessibility',
            element: describe(el),
            selector: selector(el),
            detail: 'Touch target too small (' + Math.round(touchW) + '×' + Math.round(touchH) + 'px, minimum 44×44)',
            fix: 'Add min-width: 44px; min-height: 44px, or increase padding',
          });
        }

        // Save for overlap detection
        interactiveRects.push({ el, rect, desc: describe(el), sel: selector(el) });
      }

      // ── 6. Images Without Dimensions ──────────────────

      if (el.tagName === 'IMG' && hasSize) {
        const hasAttrDims = el.hasAttribute('width') || el.hasAttribute('height');
        const hasCssDims = (style.width !== 'auto' && style.width !== '') ||
                           (style.height !== 'auto' && style.height !== '');
        if (!hasAttrDims && !hasCssDims) {
          issues.push({
            severity: 'minor',
            category: 'cls',
            element: describe(el),
            selector: selector(el),
            detail: 'Image without explicit dimensions causes layout shift during loading',
            fix: 'Add width and height attributes matching aspect ratio, or set CSS dimensions',
          });
        }
      }

      // ── 7. Missing Alt Text ───────────────────────────

      if (el.tagName === 'IMG' && !el.hasAttribute('alt')) {
        issues.push({
          severity: 'minor',
          category: 'accessibility',
          element: describe(el),
          selector: selector(el),
          detail: 'Image missing alt attribute',
          fix: 'Add alt="description" for informative images, or alt="" for decorative ones',
        });
      }

      // ── 8. Text Nearly Invisible (Same Color as BG) ───

      if (el.childNodes.length > 0 && hasSize) {
        const hasDirectText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (hasDirectText) {
          const color = style.color;
          const bg = style.backgroundColor;
          if (color && bg && color === bg && bg !== 'rgba(0, 0, 0, 0)') {
            issues.push({
              severity: 'major',
              category: 'accessibility',
              element: describe(el),
              selector: selector(el),
              detail: 'Text color matches background color: both are ' + color,
              fix: 'Change text color or background to ensure contrast',
            });
          }
        }
      }
    }

    // ── 9. Overlapping Interactive Elements ──────────────

    for (let i = 0; i < interactiveRects.length; i++) {
      for (let j = i + 1; j < interactiveRects.length; j++) {
        const a = interactiveRects[i].rect;
        const b = interactiveRects[j].rect;
        // Check for significant overlap (not just touching)
        const overlapX = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const overlapY = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        const overlapArea = overlapX * overlapY;
        const smallerArea = Math.min(a.width * a.height, b.width * b.height);
        if (overlapArea > 0 && smallerArea > 0 && overlapArea / smallerArea > 0.3) {
          issues.push({
            severity: 'major',
            category: 'overlap',
            element: interactiveRects[i].desc + ' ↔ ' + interactiveRects[j].desc,
            selector: interactiveRects[i].sel,
            detail: 'Interactive elements overlap by ' + Math.round(overlapArea / smallerArea * 100) + '% — users may tap the wrong one',
            fix: 'Adjust position, margin, or z-index to separate these elements',
          });
        }
      }
      // Limit O(n²) cost
      if (interactiveRects.length > 100) break;
    }

    // ── 10. Unwanted Scrollable Containers ───────────────

    for (const el of allEls) {
      const style = getComputedStyle(el);
      if (style.display === 'none') continue;
      if (el === document.documentElement || el === document.body) continue;
      // Elements with overflow: auto/scroll that are actually scrollable
      if ((style.overflowX === 'auto' || style.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 5) {
        // Filter: only flag if it's not an intentionally scrollable container
        const isIntentional = el.matches(
          '[class*="scroll"], [class*="carousel"], [class*="slider"], ' +
          '[class*="overflow"], [role="tablist"], pre, code, table'
        );
        if (!isIntentional) {
          issues.push({
            severity: 'warning',
            category: 'overflow',
            element: describe(el),
            selector: selector(el),
            detail: 'Container has unintended horizontal scroll (' + el.scrollWidth + 'px content in ' + el.clientWidth + 'px container)',
            fix: 'Check child element widths. A common cause is a child with width: 100% plus padding or border causing overflow',
          });
        }
      }
    }

    // ── Sort and Return ─────────────────────────────────

    const severityOrder = { critical: 0, major: 1, warning: 2, minor: 3, info: 4 };
    issues.sort((a, b) => (severityOrder[a.severity] ?? 9) - (severityOrder[b.severity] ?? 9));

    // Deduplicate by selector+category
    const seen = new Set();
    const deduped = issues.filter(i => {
      const key = i.selector + '|' + i.category;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });

    return {
      url: location.href,
      viewport: { width: vw, height: vh },
      timestamp: new Date().toISOString(),
      issueCount: deduped.length,
      bySeverity: {
        critical: deduped.filter(i => i.severity === 'critical').length,
        major: deduped.filter(i => i.severity === 'major').length,
        warning: deduped.filter(i => i.severity === 'warning').length,
        minor: deduped.filter(i => i.severity === 'minor').length,
      },
      issues: deduped,
    };
  });
}
```

### Using the Results

```javascript
const health = await domHealthCheck(page);

if (health.issueCount === 0) {
  console.log('DOM health check: CLEAN');
} else {
  console.log(`DOM health check: ${health.issueCount} issue(s)`);
  console.log(`  Critical: ${health.bySeverity.critical}`);
  console.log(`  Major: ${health.bySeverity.major}`);
  console.log(`  Warning: ${health.bySeverity.warning}`);
  console.log(`  Minor: ${health.bySeverity.minor}`);

  // Show top issues
  for (const issue of health.issues.slice(0, 10)) {
    console.log(`  [${issue.severity}] ${issue.category}: ${issue.detail}`);
    console.log(`    → ${issue.selector}`);
    console.log(`    Fix: ${issue.fix}`);
  }
}
```

### What Each Check Detects

| # | Check | Severity | What It Catches |
|---|-------|----------|-----------------|
| 1 | Page horizontal scroll | critical | Content wider than viewport — broken on mobile |
| 2 | Element beyond viewport | major | Elements pushed off-screen by width/margin/position |
| 3 | Content overflow clipped | warning | Text cut off without ellipsis or scroll indicator |
| 4 | Zero-dimension content | warning | Elements collapsed to 0×0 but containing text |
| 5 | Small touch targets | minor | Buttons/links too small to tap (< 44×44px) |
| 6 | Images without dimensions | minor | Layout shift risk during image loading |
| 7 | Missing alt text | minor | Accessibility violation |
| 8 | Invisible text | major | Text same color as background |
| 9 | Overlapping interactives | major | Clickable elements stacked on each other |
| 10 | Unwanted scroll containers | warning | Unexpected scrollbars on non-scrollable containers |

### Limitations

The DOM health check catches *mechanical* layout bugs. It cannot detect:
- Aesthetic issues (ugly spacing, bad visual hierarchy, inconsistent styling)
- Semantic correctness (wrong content in the right place)
- Design intent mismatches (looks "wrong" relative to mockup)
- Animation/transition quality

For these, take a screenshot and use the agent's built-in vision. The health check and visual inspection are complementary — run the health check first to fix the obvious stuff, then screenshot for the subjective stuff.

---

## Computed Styles Extraction

When the agent spots a visual problem in a screenshot, it needs to know *which CSS properties to change*. This function extracts the full layout context for a specific element.

### The Function

```javascript
async function inspectElement(page, selectorOrLocator) {
  const sel = typeof selectorOrLocator === 'string' ? selectorOrLocator : null;
  const locator = sel ? page.locator(sel) : selectorOrLocator;

  // Ensure element exists
  await locator.waitFor({ state: 'attached', timeout: 5000 });

  return locator.evaluate((el) => {
    const style = getComputedStyle(el);

    function parseNum(v) {
      return Math.round(parseFloat(v) || 0);
    }

    // Box model
    const box = {
      width: parseNum(style.width),
      height: parseNum(style.height),
      padding: {
        top: parseNum(style.paddingTop),
        right: parseNum(style.paddingRight),
        bottom: parseNum(style.paddingBottom),
        left: parseNum(style.paddingLeft),
      },
      margin: {
        top: parseNum(style.marginTop),
        right: parseNum(style.marginRight),
        bottom: parseNum(style.marginBottom),
        left: parseNum(style.marginLeft),
      },
      border: {
        top: parseNum(style.borderTopWidth),
        right: parseNum(style.borderRightWidth),
        bottom: parseNum(style.borderBottomWidth),
        left: parseNum(style.borderLeftWidth),
      },
    };

    // Actual rendered size
    const rect = el.getBoundingClientRect();
    const rendered = {
      x: Math.round(rect.x),
      y: Math.round(rect.y),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
    };

    // Position and stacking
    const position = {
      position: style.position,
      top: style.top,
      right: style.right,
      bottom: style.bottom,
      left: style.left,
      zIndex: style.zIndex,
      float: style.float !== 'none' ? style.float : undefined,
      transform: style.transform !== 'none' ? style.transform : undefined,
    };

    // Layout role (flex/grid child or container)
    const layout = {
      display: style.display,
      // As flex/grid container
      flexDirection: style.display.includes('flex') ? style.flexDirection : undefined,
      flexWrap: style.display.includes('flex') ? style.flexWrap : undefined,
      justifyContent: style.display.includes('flex') || style.display.includes('grid') ? style.justifyContent : undefined,
      alignItems: style.display.includes('flex') || style.display.includes('grid') ? style.alignItems : undefined,
      gap: style.display.includes('flex') || style.display.includes('grid') ? style.gap : undefined,
      gridTemplateColumns: style.display.includes('grid') ? style.gridTemplateColumns : undefined,
      gridTemplateRows: style.display.includes('grid') ? style.gridTemplateRows : undefined,
      // As flex child
      flexGrow: style.flexGrow !== '0' ? style.flexGrow : undefined,
      flexShrink: style.flexShrink !== '1' ? style.flexShrink : undefined,
      flexBasis: style.flexBasis !== 'auto' ? style.flexBasis : undefined,
      alignSelf: style.alignSelf !== 'auto' ? style.alignSelf : undefined,
    };

    // Typography
    const typography = {
      fontFamily: style.fontFamily.split(',')[0].trim().replace(/['"]/g, ''),
      fontSize: style.fontSize,
      fontWeight: style.fontWeight,
      lineHeight: style.lineHeight,
      letterSpacing: style.letterSpacing !== 'normal' ? style.letterSpacing : undefined,
      color: style.color,
      textAlign: style.textAlign,
      textOverflow: style.textOverflow !== 'clip' ? style.textOverflow : undefined,
      whiteSpace: style.whiteSpace !== 'normal' ? style.whiteSpace : undefined,
      wordBreak: style.wordBreak !== 'normal' ? style.wordBreak : undefined,
      overflowWrap: style.overflowWrap !== 'normal' ? style.overflowWrap : undefined,
    };

    // Overflow
    const overflow = {
      overflowX: style.overflowX,
      overflowY: style.overflowY,
      scrollWidth: el.scrollWidth,
      scrollHeight: el.scrollHeight,
      clientWidth: el.clientWidth,
      clientHeight: el.clientHeight,
      isOverflowingH: el.scrollWidth > el.clientWidth + 1,
      isOverflowingV: el.scrollHeight > el.clientHeight + 1,
    };

    // Visual
    const visual = {
      backgroundColor: style.backgroundColor,
      borderRadius: style.borderRadius !== '0px' ? style.borderRadius : undefined,
      boxShadow: style.boxShadow !== 'none' ? style.boxShadow : undefined,
      opacity: style.opacity !== '1' ? style.opacity : undefined,
    };

    // Parent chain (up to 4 ancestors, showing layout context)
    const parents = [];
    let current = el.parentElement;
    let depth = 0;
    while (current && current !== document.body && depth < 4) {
      const ps = getComputedStyle(current);
      const pr = current.getBoundingClientRect();
      parents.push({
        tag: current.tagName.toLowerCase() + (current.id ? '#' + current.id : '') +
             (current.className && typeof current.className === 'string'
               ? '.' + current.className.trim().split(/\s+/).slice(0, 1).join('.')
               : ''),
        display: ps.display,
        width: Math.round(pr.width),
        height: Math.round(pr.height),
        position: ps.position !== 'static' ? ps.position : undefined,
        overflow: ps.overflow !== 'visible' ? ps.overflow : undefined,
        flexDirection: ps.display.includes('flex') ? ps.flexDirection : undefined,
        gridTemplateColumns: ps.display.includes('grid') ? ps.gridTemplateColumns : undefined,
      });
      current = current.parentElement;
      depth++;
    }

    // Strip undefined values for clean output
    function clean(obj) {
      const result = {};
      for (const [k, v] of Object.entries(obj)) {
        if (v !== undefined) result[k] = v;
      }
      return result;
    }

    return {
      element: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
      rendered,
      box,
      position: clean(position),
      layout: clean(layout),
      typography: clean(typography),
      overflow,
      visual: clean(visual),
      parentChain: parents,
    };
  });
}
```

### Usage Pattern

```javascript
// Agent spots a misaligned button in screenshot
const info = await inspectElement(page, '[data-testid="submit-btn"]');
console.log(JSON.stringify(info, null, 2));

// Now the agent knows:
// - Exact pixel position and size
// - Box model (is padding/margin causing the issue?)
// - Parent layout (is the parent flex? grid? what direction?)
// - Overflow state (is content being clipped?)
// - Stacking context (is z-index involved?)

// Agent can make an informed CSS fix instead of guessing
```

### Debugging Common Visual Problems

| Visual Problem | What to Check in Output |
|----------------|------------------------|
| Element misaligned | `position`, `parentChain[0].display`, `layout.alignSelf`, `box.margin` |
| Element too wide/narrow | `box.width`, `layout.flexGrow/Shrink/Basis`, `parentChain[0].width` |
| Text cut off | `overflow.isOverflowingH/V`, `typography.textOverflow`, `typography.whiteSpace` |
| Element overlapping | `position.position`, `position.zIndex`, `position.top/left` |
| Unexpected gap/space | `box.margin`, `box.padding`, `parentChain[0].gap` |
| Element collapsed | `box.width`, `box.height`, `layout.display`, `layout.flexBasis` |
| Wrong font/size | `typography.fontFamily`, `typography.fontSize`, `typography.fontWeight` |
| Element invisible | `visual.opacity`, `rendered.width/height`, `position.position` |

---

## Layout Snapshot Diffing

Structural before/after comparison that catches unintended visual side effects **without relying on vision**. Captures the DOM layout tree as JSON, diffs it structurally after a code change, and flags every unexpected change — position shifts, size changes, disappeared elements, z-index changes — deterministically.

> **Key insight:** Split visual QA into two separable concerns. *Structural verification* (automated, deterministic, no screenshots needed) asks "did the layout change as intended and *only* as intended?" *Aesthetic verification* (agent vision via screenshots) asks "does the intended change look good?" This section automates the first concern entirely.

### When to Use

- **Every iteration of the Edit-Reload-Verify micro-loop** — capture before change, capture after, diff
- **Before/after CSS refactors** — prove nothing moved that shouldn't have
- **Peripheral damage detection** — replaces manual before/after screenshot comparison
- **Regression guard** — save a baseline snapshot, diff against it after any change

### captureLayoutSnapshot

Captures the position, size, text, styles, and identity of every visible element on the page.

```javascript
async function captureLayoutSnapshot(page) {
  return page.evaluate(() => {
    const elements = [];

    function stableSelector(el) {
      if (el.id) return '#' + el.id;
      if (el.dataset?.testid) return '[data-testid="' + el.dataset.testid + '"]';
      const tag = el.tagName.toLowerCase();
      const parent = el.parentElement;
      if (!parent || parent === document.documentElement) return tag;
      const siblings = [...parent.children].filter(c => c.tagName === el.tagName);
      const idx = siblings.indexOf(el);
      const nth = siblings.length > 1 ? ':nth-of-type(' + (idx + 1) + ')' : '';
      return stableSelector(parent) + ' > ' + tag + nth;
    }

    const allEls = document.querySelectorAll('body *');

    for (const el of allEls) {
      const style = getComputedStyle(el);
      if (style.display === 'none') continue;
      if (style.visibility === 'hidden' && style.position !== 'absolute') continue;

      const rect = el.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) continue;

      // Direct text content (not from children)
      const directText = [...el.childNodes]
        .filter(n => n.nodeType === 3)
        .map(n => n.textContent.trim())
        .filter(Boolean)
        .join(' ')
        .slice(0, 120);

      elements.push({
        selector: stableSelector(el),
        tag: el.tagName.toLowerCase(),
        id: el.id || undefined,
        testId: el.dataset?.testid || undefined,
        classes: el.className && typeof el.className === 'string'
          ? el.className.trim().split(/\s+/).slice(0, 4).join(' ')
          : undefined,
        text: directText || undefined,
        rect: {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          w: Math.round(rect.width),
          h: Math.round(rect.height),
        },
        styles: {
          display: style.display,
          position: style.position !== 'static' ? style.position : undefined,
          zIndex: style.zIndex !== 'auto' ? parseInt(style.zIndex) : undefined,
          overflow: style.overflow !== 'visible' ? style.overflow : undefined,
          opacity: style.opacity !== '1' ? parseFloat(style.opacity) : undefined,
          visibility: style.visibility !== 'visible' ? style.visibility : undefined,
        },
        interactive: el.matches(
          'a[href], button, input, select, textarea, ' +
          '[role="button"], [role="link"], [tabindex]:not([tabindex="-1"])'
        ),
      });
    }

    return {
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      timestamp: new Date().toISOString(),
      elementCount: elements.length,
      elements,
    };
  });
}
```

### diffLayoutSnapshots

Compares two snapshots and returns structured diffs grouped by change type.

```javascript
function diffLayoutSnapshots(before, after, options = {}) {
  const {
    positionThreshold = 3,  // ignore moves ≤ 3px (subpixel rounding)
    sizeThreshold = 3,      // ignore resize ≤ 3px
    intent = null,          // optional: { expect: [...], noChange: [...] }
  } = options;

  // Index elements by selector for matching
  const beforeMap = new Map(before.elements.map(el => [el.selector, el]));
  const afterMap = new Map(after.elements.map(el => [el.selector, el]));

  const diffs = [];

  // Find disappeared elements (in before, not in after)
  for (const [sel, bEl] of beforeMap) {
    if (!afterMap.has(sel)) {
      diffs.push({
        type: 'disappeared',
        selector: sel,
        tag: bEl.tag,
        text: bEl.text,
        before: bEl.rect,
        severity: bEl.interactive ? 'critical' : 'major',
        detail: `${bEl.tag}${bEl.text ? ' "' + bEl.text.slice(0, 40) + '"' : ''} disappeared`,
      });
    }
  }

  // Find appeared elements (in after, not in before)
  for (const [sel, aEl] of afterMap) {
    if (!beforeMap.has(sel)) {
      diffs.push({
        type: 'appeared',
        selector: sel,
        tag: aEl.tag,
        text: aEl.text,
        after: aEl.rect,
        severity: 'info',
        detail: `${aEl.tag}${aEl.text ? ' "' + aEl.text.slice(0, 40) + '"' : ''} appeared at (${aEl.rect.x},${aEl.rect.y}) ${aEl.rect.w}×${aEl.rect.h}`,
      });
    }
  }

  // Compare matched elements
  for (const [sel, bEl] of beforeMap) {
    const aEl = afterMap.get(sel);
    if (!aEl) continue;

    const changes = [];

    // Position change
    const dx = Math.abs(aEl.rect.x - bEl.rect.x);
    const dy = Math.abs(aEl.rect.y - bEl.rect.y);
    if (dx > positionThreshold || dy > positionThreshold) {
      changes.push({
        property: 'position',
        before: { x: bEl.rect.x, y: bEl.rect.y },
        after: { x: aEl.rect.x, y: aEl.rect.y },
        delta: { dx: aEl.rect.x - bEl.rect.x, dy: aEl.rect.y - bEl.rect.y },
        detail: `moved (${bEl.rect.x},${bEl.rect.y}) → (${aEl.rect.x},${aEl.rect.y})`,
      });
    }

    // Size change
    const dw = Math.abs(aEl.rect.w - bEl.rect.w);
    const dh = Math.abs(aEl.rect.h - bEl.rect.h);
    if (dw > sizeThreshold || dh > sizeThreshold) {
      changes.push({
        property: 'size',
        before: { w: bEl.rect.w, h: bEl.rect.h },
        after: { w: aEl.rect.w, h: aEl.rect.h },
        delta: { dw: aEl.rect.w - bEl.rect.w, dh: aEl.rect.h - bEl.rect.h },
        detail: `resized ${bEl.rect.w}×${bEl.rect.h} → ${aEl.rect.w}×${aEl.rect.h}`,
      });
    }

    // Text change
    if (bEl.text !== aEl.text && (bEl.text || aEl.text)) {
      changes.push({
        property: 'text',
        before: bEl.text,
        after: aEl.text,
        detail: `text "${(bEl.text || '').slice(0, 30)}" → "${(aEl.text || '').slice(0, 30)}"`,
      });
    }

    // z-index change
    if (bEl.styles?.zIndex !== aEl.styles?.zIndex) {
      changes.push({
        property: 'zIndex',
        before: bEl.styles?.zIndex,
        after: aEl.styles?.zIndex,
        detail: `z-index ${bEl.styles?.zIndex ?? 'auto'} → ${aEl.styles?.zIndex ?? 'auto'}`,
      });
    }

    // display change
    if (bEl.styles?.display !== aEl.styles?.display) {
      changes.push({
        property: 'display',
        before: bEl.styles?.display,
        after: aEl.styles?.display,
        detail: `display ${bEl.styles?.display} → ${aEl.styles?.display}`,
      });
    }

    // opacity change
    if (bEl.styles?.opacity !== aEl.styles?.opacity) {
      changes.push({
        property: 'opacity',
        before: bEl.styles?.opacity,
        after: aEl.styles?.opacity,
        detail: `opacity ${bEl.styles?.opacity ?? 1} → ${aEl.styles?.opacity ?? 1}`,
      });
    }

    // overflow change
    if (bEl.styles?.overflow !== aEl.styles?.overflow) {
      changes.push({
        property: 'overflow',
        before: bEl.styles?.overflow,
        after: aEl.styles?.overflow,
        detail: `overflow ${bEl.styles?.overflow ?? 'visible'} → ${aEl.styles?.overflow ?? 'visible'}`,
      });
    }

    // visibility change
    if (bEl.styles?.visibility !== aEl.styles?.visibility) {
      changes.push({
        property: 'visibility',
        before: bEl.styles?.visibility,
        after: aEl.styles?.visibility,
        detail: `visibility ${bEl.styles?.visibility ?? 'visible'} → ${aEl.styles?.visibility ?? 'visible'}`,
      });
    }

    if (changes.length > 0) {
      diffs.push({
        type: 'changed',
        selector: sel,
        tag: aEl.tag,
        text: aEl.text || bEl.text,
        interactive: aEl.interactive,
        changes,
        severity: aEl.interactive ? 'major' : 'minor',
      });
    }
  }

  // Apply intent validation if provided
  if (intent) {
    for (const diff of diffs) {
      // Mark expected changes
      const isExpected = intent.expect?.some(e =>
        diff.selector.includes(e.selector) ||
        diff.selector === e.selector
      );
      // Mark unexpected changes to noChange elements
      const shouldNotChange = intent.noChange?.some(sel =>
        diff.selector.includes(sel) || diff.selector === sel
      );

      diff.expected = isExpected || false;
      if (shouldNotChange && diff.type !== 'appeared') {
        diff.severity = 'critical';
        diff.unexpected = true;
        diff.detail = (diff.detail || diff.changes?.[0]?.detail || '') +
          ' [UNEXPECTED — element was declared noChange]';
      }
    }
  }

  // Sort: critical first, then major, then by type
  const severityOrder = { critical: 0, major: 1, minor: 2, info: 3 };
  diffs.sort((a, b) => (severityOrder[a.severity] ?? 9) - (severityOrder[b.severity] ?? 9));

  // Summary
  const unexpected = diffs.filter(d => d.unexpected);
  const appeared = diffs.filter(d => d.type === 'appeared');
  const disappeared = diffs.filter(d => d.type === 'disappeared');
  const changed = diffs.filter(d => d.type === 'changed');

  return {
    beforeUrl: before.url,
    afterUrl: after.url,
    beforeViewport: before.viewport,
    afterViewport: after.viewport,
    summary: {
      totalDiffs: diffs.length,
      appeared: appeared.length,
      disappeared: disappeared.length,
      changed: changed.length,
      unexpected: unexpected.length,
      hasUnexpected: unexpected.length > 0,
    },
    diffs,
  };
}
```

### Using the Results

```javascript
// Basic usage: capture before/after a change
const before = await captureLayoutSnapshot(page);

// ... make code change and reload ...
await page.reload({ waitUntil: 'domcontentloaded' });

const after = await captureLayoutSnapshot(page);
const diff = diffLayoutSnapshots(before, after);

if (diff.summary.totalDiffs === 0) {
  console.log('Layout snapshot: NO CHANGES (change may not have taken effect)');
} else {
  console.log(`Layout snapshot: ${diff.summary.totalDiffs} diff(s)`);
  console.log(`  Appeared: ${diff.summary.appeared}`);
  console.log(`  Disappeared: ${diff.summary.disappeared}`);
  console.log(`  Changed: ${diff.summary.changed}`);

  for (const d of diff.diffs.slice(0, 15)) {
    if (d.type === 'changed') {
      for (const c of d.changes) {
        console.log(`  [${d.severity}] ${d.selector}: ${c.detail}`);
      }
    } else {
      console.log(`  [${d.severity}] ${d.detail}`);
    }
  }
}
```

### Render Intent Declaration

When you know exactly what should change, declare it upfront. The diff will flag everything else as unexpected:

```javascript
const intent = {
  expect: [
    { selector: '.header', description: 'Increasing header height' },
    { selector: '#hero-title', description: 'Changing title text' },
  ],
  noChange: ['.footer', '.sidebar', 'nav', '.content-area'],
};

const before = await captureLayoutSnapshot(page);

// ... make change, reload ...

const after = await captureLayoutSnapshot(page);
const diff = diffLayoutSnapshots(before, after, { intent });

if (diff.summary.hasUnexpected) {
  console.log('UNEXPECTED CHANGES DETECTED:');
  for (const d of diff.diffs.filter(d => d.unexpected)) {
    console.log(`  [CRITICAL] ${d.selector}: ${d.changes?.[0]?.detail || d.detail}`);
  }
  // Stop and investigate before proceeding
}
```

### Integration with Edit-Reload-Verify

The snapshot diff slots into the micro-loop between reload and DOM health check:

```
1. Make code change
2. captureLayoutSnapshot(page)  →  "before" (skip if already captured)
3. Reload
4. captureLayoutSnapshot(page)  →  "after"
5. diffLayoutSnapshots(before, after)
   ├─ Unexpected changes? → Stop, investigate
   └─ Only expected changes? → Continue
6. DOM health check  →  catch mechanical bugs
7. Screenshot  →  aesthetic verification of intended changes only
8. "after" becomes "before" for next iteration
```

Step 8 is key: each iteration's "after" snapshot becomes the next iteration's "before" baseline. This chains diffs so unintended changes are caught incrementally.

### What the Diff Catches (That Vision Misses)

| Change | Vision Reliability | Snapshot Diff Reliability |
|--------|-------------------|--------------------------|
| Element moved 5px | Agents almost never notice | 100% — exact pixel delta |
| z-index changed | Invisible until something overlaps | 100% — reported immediately |
| Element disappeared | Agent may not remember it existed | 100% — listed as disappeared |
| Sibling shifted due to margin change | Agent focused on the element it changed | 100% — sibling's position delta reported |
| Overflow property changed | Invisible until content actually overflows | 100% — style change reported |
| Opacity reduced from 1 to 0.8 | Barely visible in screenshots | 100% — exact value reported |
| Text content changed | Agent may not read every label | 100% — before/after text shown |
| New rogue element appeared | Agent doesn't know it wasn't there before | 100% — listed as appeared |

### Saving and Loading Baselines

For longer-lived regression detection, save snapshots to disk:

```javascript
const fs = await import('fs');

// Save baseline
const baseline = await captureLayoutSnapshot(page);
fs.writeFileSync('/tmp/baseline-dashboard.json', JSON.stringify(baseline, null, 2));

// Later: load and compare
const saved = JSON.parse(fs.readFileSync('/tmp/baseline-dashboard.json', 'utf8'));
const current = await captureLayoutSnapshot(page);
const diff = diffLayoutSnapshots(saved, current);
```

---

## Responsive Breakpoint Sweep

Capture screenshots at every meaningful breakpoint in a single function call. The agent reviews the full set instead of manually resizing and screenshotting one viewport at a time.

### Standard Breakpoints

```javascript
const BREAKPOINTS = [
  { name: 'mobile-s',  width: 320,  height: 568,  device: 'iPhone SE (old)' },
  { name: 'mobile',    width: 375,  height: 667,  device: 'iPhone 8 / standard' },
  { name: 'mobile-l',  width: 428,  height: 926,  device: 'iPhone 14 Pro Max' },
  { name: 'tablet',    width: 768,  height: 1024, device: 'iPad Mini / standard' },
  { name: 'tablet-l',  width: 1024, height: 768,  device: 'iPad landscape' },
  { name: 'laptop',    width: 1280, height: 800,  device: 'MacBook Air 13"' },
  { name: 'desktop',   width: 1440, height: 900,  device: 'Standard desktop' },
  { name: 'desktop-l', width: 1920, height: 1080, device: 'Full HD' },
];
```

### Sweep Function

```javascript
async function breakpointSweep(page, options = {}) {
  const {
    breakpoints = BREAKPOINTS,
    path = '/tmp/breakpoints',
    prefix = 'bp',
    waitAfterResize = 300,
    runHealthCheck = true,
    url = null,  // if set, navigate here at each breakpoint
  } = options;

  const results = [];

  for (const bp of breakpoints) {
    // Resize viewport
    await page.setViewportSize({ width: bp.width, height: bp.height });

    // Navigate if URL provided (some sites need full reload at new size)
    if (url) {
      await page.goto(url, { waitUntil: 'domcontentloaded' });
    }

    // Wait for layout to settle
    await page.waitForTimeout(waitAfterResize);
    await page.evaluate(() => document.fonts.ready);

    // Run DOM health check at this viewport
    let health = null;
    if (runHealthCheck) {
      health = await domHealthCheck(page);
    }

    // Capture screenshot
    const filename = `${path}/${prefix}-${bp.name}-${bp.width}x${bp.height}.png`;
    await page.screenshot({ path: filename, type: 'png' });

    results.push({
      breakpoint: bp.name,
      width: bp.width,
      height: bp.height,
      device: bp.device,
      screenshot: filename,
      healthIssues: health?.issueCount ?? null,
      healthCritical: health?.bySeverity?.critical ?? null,
      healthMajor: health?.bySeverity?.major ?? null,
    });

    console.log(
      `  ${bp.name} (${bp.width}×${bp.height}): ` +
      (health ? `${health.issueCount} issue(s)` : 'captured')
    );
  }

  // Summary
  const issueBreakpoints = results.filter(r => r.healthCritical > 0 || r.healthMajor > 0);
  console.log(`\nBreakpoint sweep: ${results.length} viewports captured`);
  if (issueBreakpoints.length > 0) {
    console.log(`Viewports with critical/major issues: ${issueBreakpoints.map(r => r.breakpoint).join(', ')}`);
  }

  return results;
}
```

### Usage

```javascript
// Sweep all breakpoints
const results = await breakpointSweep(page, { prefix: 'dashboard' });

// Sweep with URL navigation (for SSR apps that render differently per viewport)
const results = await breakpointSweep(page, {
  url: 'http://127.0.0.1:3000/dashboard',
  prefix: 'dashboard',
});

// Sweep only mobile breakpoints
const mobileOnly = BREAKPOINTS.filter(bp => bp.width <= 428);
const results = await breakpointSweep(page, {
  breakpoints: mobileOnly,
  prefix: 'mobile-check',
});
```

### Agent Review Protocol

After a sweep, review screenshots systematically:

1. Start with the narrowest viewport (mobile-s, 320px) — most constrained
2. Check for critical layout breaks (horizontal scroll, content overflow)
3. Move to tablet — check layout transitions (sidebar collapse, grid reflow)
4. Check desktop — verify full-width layout uses space well
5. Compare breakpoint boundaries — does the transition between 768→1024 break anything?

Focus on:
- Does navigation transform correctly (hamburger ↔ full nav)?
- Do grids reflow to fewer columns?
- Is text readable without zooming at every size?
- Are touch targets adequate on mobile?
- Does anything disappear or get cut off?

---

## Interactive State Triggers

Agents can't physically hover a mouse or hold a key. These helpers force pseudo-states and UI states programmatically, enabling testing of states agents would otherwise miss entirely.

### Pseudo-State Injection

```javascript
/**
 * Force a CSS pseudo-state on an element by injecting a style rule.
 * Returns a cleanup function to remove the injected state.
 */
async function forceState(page, selector, pseudoState) {
  const stateId = `forced-state-${Date.now()}`;

  await page.evaluate(({ selector, pseudoState, stateId }) => {
    const el = document.querySelector(selector);
    if (!el) return;

    // Get the computed style of the pseudo-state by reading stylesheets
    // and inject it directly as inline styles won't work for :hover etc.
    const style = document.createElement('style');
    style.id = stateId;

    // Copy all rules that match selector:pseudo-state and apply to selector.forced-state
    const rules = [];
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) {
          if (rule.selectorText?.includes(selector + ':' + pseudoState) ||
              rule.selectorText?.includes(selector + '::' + pseudoState)) {
            // Replace :hover with .forced-hover etc
            const newSelector = rule.selectorText
              .replace(':' + pseudoState, '.forced-' + pseudoState);
            rules.push(newSelector + ' { ' + rule.style.cssText + ' }');
          }
        }
      } catch (e) {
        // Cross-origin stylesheets will throw
      }
    }

    // Also handle common hover patterns
    if (pseudoState === 'hover') {
      // CSS variables and common patterns
      rules.push(`${selector}.forced-hover { cursor: pointer; }`);
    }

    style.textContent = rules.join('\n');
    document.head.appendChild(style);
    el.classList.add('forced-' + pseudoState);
  }, { selector, pseudoState, stateId });

  // Return cleanup function
  return async () => {
    await page.evaluate(({ selector, pseudoState, stateId }) => {
      document.getElementById(stateId)?.remove();
      document.querySelector(selector)?.classList.remove('forced-' + pseudoState);
    }, { selector, pseudoState, stateId });
  };
}
```

### Simpler Alternative: CDP Force Pseudo-State

Playwright can use Chrome DevTools Protocol to force pseudo-states directly, which is more reliable than CSS injection:

```javascript
/**
 * Force pseudo-states via CDP — more reliable than CSS injection.
 * Works for :hover, :active, :focus, :focus-within, :focus-visible, :target
 */
async function cdpForceState(page, selector, states) {
  const element = page.locator(selector);
  const elementHandle = await element.elementHandle();

  const cdp = await page.context().newCDPSession(page);
  const { nodeId } = await cdp.send('DOM.pushNodeByBackendIdToFrontend', {
    backendNodeId: await elementHandle.evaluate(el => {
      // Get the backend node ID through a workaround
      return (el as any).__backendNodeId;
    }),
  });

  // Alternative: use the simpler approach
  await cdp.send('DOM.getDocument');
  const { nodeId: foundNode } = await cdp.send('DOM.querySelector', {
    nodeId: 1, // document node
    selector,
  });

  await cdp.send('CSS.forcePseudoState', {
    nodeId: foundNode,
    forcedPseudoClasses: states, // e.g., ['hover', 'focus']
  });

  return async () => {
    await cdp.send('CSS.forcePseudoState', {
      nodeId: foundNode,
      forcedPseudoClasses: [],
    });
    await cdp.detach();
  };
}
```

### Practical State Testing Shortcuts

For most QA work, use these simpler direct approaches:

```javascript
// ── Focus State ──
await page.locator('button.submit').focus();
await page.screenshot({ path: '/tmp/btn-focus.png' });

// ── Hover via dispatchEvent (triggers JS hover handlers) ──
await page.locator('button.submit').hover();
await page.screenshot({ path: '/tmp/btn-hover.png' });

// ── Active/Pressed (mouse down without releasing) ──
const btn = page.locator('button.submit');
const box = await btn.boundingBox();
await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
await page.mouse.down();
await page.screenshot({ path: '/tmp/btn-active.png' });
await page.mouse.up();

// ── Disabled State ──
await page.locator('button.submit').evaluate(el => el.disabled = true);
await page.screenshot({ path: '/tmp/btn-disabled.png' });
await page.locator('button.submit').evaluate(el => el.disabled = false);

// ── Form Error State ──
await page.locator('input[name="email"]').fill('not-an-email');
await page.locator('form').evaluate(el => el.reportValidity());
await page.screenshot({ path: '/tmp/form-error.png' });

// ── Empty State (remove all content) ──
await page.locator('[data-testid="item-list"]').evaluate(el => {
  el.dataset.originalHtml = el.innerHTML;
  el.innerHTML = '';
});
await page.screenshot({ path: '/tmp/empty-state.png' });
// Restore
await page.locator('[data-testid="item-list"]').evaluate(el => {
  el.innerHTML = el.dataset.originalHtml;
  delete el.dataset.originalHtml;
});

// ── Overflow/Long Content ──
await page.locator('[data-testid="user-name"]').evaluate(el => {
  el.dataset.originalText = el.textContent;
  el.textContent = 'Bartholomew Higginbotham-Worthington III, Esq., PhD, MBA, CFA';
});
await page.screenshot({ path: '/tmp/overflow-text.png' });
// Restore
await page.locator('[data-testid="user-name"]').evaluate(el => {
  el.textContent = el.dataset.originalText;
  delete el.dataset.originalText;
});

// ── Loading/Skeleton State ──
await page.locator('[data-testid="dashboard"]').evaluate(el => {
  el.dataset.originalHtml = el.innerHTML;
  el.innerHTML = '<div class="skeleton" style="width:100%;height:200px;background:#e0e0e0;border-radius:8px;animation:pulse 1.5s infinite"></div>';
});
await page.screenshot({ path: '/tmp/loading-state.png' });
// Restore
await page.locator('[data-testid="dashboard"]').evaluate(el => {
  el.innerHTML = el.dataset.originalHtml;
  delete el.dataset.originalHtml;
});

// ── Many Items (stress test) ──
await page.locator('[data-testid="item-list"]').evaluate(el => {
  el.dataset.originalHtml = el.innerHTML;
  const item = el.children[0]?.outerHTML || '<div class="item">Item</div>';
  el.innerHTML = Array(50).fill(item).join('');
});
await page.screenshot({ path: '/tmp/many-items.png', fullPage: true });
// Restore
await page.locator('[data-testid="item-list"]').evaluate(el => {
  el.innerHTML = el.dataset.originalHtml;
  delete el.dataset.originalHtml;
});
```

### State Testing Checklist

| State | How to Trigger | What to Check |
|-------|---------------|---------------|
| **Default** | Initial page load | Correct layout, all content visible |
| **Hover** | `.hover()` or CDP | Visual feedback (color change, shadow, scale) |
| **Focus** | `.focus()` | Visible focus ring, contrast against background |
| **Active** | `mouse.down()` | Press feedback distinct from hover |
| **Disabled** | `el.disabled = true` | Visually distinct, not clickable appearance |
| **Error** | `reportValidity()` or invalid input | Error message visible, field highlighted |
| **Empty** | Remove child content | Meaningful empty state, not blank void |
| **Overflow** | Inject very long text | Text wraps or truncates with ellipsis, no layout break |
| **Loading** | Replace content with skeleton | Skeleton matches final layout dimensions |
| **Many items** | Duplicate list items 50× | Scrollable, no layout collapse, pagination present |
| **Dark mode** | Toggle theme class/attribute | All text readable, no lost borders or shadows |

---

## Failure Mode Injection

Network failure injection, input stress testing, state corruption, and resilience scoring are covered in a dedicated reference.

**See:** FAILURE-INJECTION.md for `discoverNetworkDependencies()`, `injectNetworkFailure()`, `inputStressTest()`, `rapidInteractionTest()`, `corruptSessionState()`, and the `failureResilienceAudit()` orchestrator.
