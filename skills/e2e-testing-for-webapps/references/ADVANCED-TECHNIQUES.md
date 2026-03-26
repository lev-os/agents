# Advanced Techniques

Patterns discovered from the Playwright + AI testing ecosystem. These complement the core skill with cutting-edge approaches used in production.

## Table of Contents
- [Three-Image LLM Visual Diff](#three-image-llm-visual-diff)
- [Screenshot Stabilization](#screenshot-stabilization)
- [Agent-Driven Visual Questions](#agent-driven-visual-questions)
- [Playwright Built-in Visual Comparisons](#playwright-built-in-visual-comparisons)
- [Set-of-Marks Vision Overlays](#set-of-marks-vision-overlays)
- [ARIA Snapshot Navigation](#aria-snapshot-navigation)
- [Playwright Test Agents](#playwright-test-agents)
- [Agent-Driven CI QA](#agent-driven-ci-qa)
- [Dynamic Script Generation](#dynamic-script-generation)
- [Structured Verification Types](#structured-verification-types)
- [Image Compression for LLM Submission](#image-compression-for-llm-submission)
- [Design-to-Implementation Diff](#design-to-implementation-diff)
- [Docker Deterministic Rendering](#docker-deterministic-rendering)
- [Dev Server Auto-Detection](#dev-server-auto-detection)
- [Notable Open-Source Projects](#notable-open-source-projects)

---

## Three-Image LLM Visual Diff

The gold standard for AI-powered visual regression: capture baseline, current, and pixel-diff images, then send all three to a vision LLM for intelligent explanation of what changed. Dramatically better than pixel-diff alone because the LLM explains *what* changed and *whether it matters*.

Source: [Arghajit47/Playwright-Visual-Testing](https://github.com/Arghajit47/Playwright-Visual-Testing)

### Workflow

```
1. Capture baseline screenshot (golden reference)
2. Capture current screenshot (after code change)
3. Generate pixel diff image (red/pink highlights on changes)
4. Send all three to vision LLM with structured prompt
5. Get JSON output: { changes: [{ location, baseline_state, current_state, description }] }
```

### Pixel Diff with looks-same

`looks-same` uses CIEDE2000 color tolerance (perceptual, not raw RGB) and has configurable antialiasing tolerance, making it more reliable than `pixelmatch` for cross-platform rendering differences.

```typescript
import looksSame from 'looks-same';

async function generateDiff(baselinePath: string, currentPath: string, diffPath: string): Promise<boolean> {
  const result = await looksSame(baselinePath, currentPath, {
    tolerance: 2.3,  // CIEDE2000 perceptual tolerance (default)
    antialiasingTolerance: 4,  // Handle cross-platform font rendering
    ignoreCaret: true,  // Ignore blinking cursor differences
  });

  if (!result.equal) {
    await looksSame.createDiff({
      reference: baselinePath,
      current: currentPath,
      diff: diffPath,
      highlightColor: '#ff00ff',
      tolerance: 2.3,
    });
  }

  return result.equal;
}
```

### Forced Reasoning Prompt

The key insight: force the LLM through a step-by-step analysis to avoid hallucinated or superficial answers.

```typescript
const VISUAL_DIFF_PROMPT = `You are a Visual QA Analyst. Analyze these three images:
1. BASELINE (reference/golden screenshot)
2. CURRENT (latest screenshot)
3. DIFF (pixel differences highlighted in red/pink)

Follow this exact reasoning process:
Step 1: Scan the DIFF image for red/pink highlighted regions
Step 2: For each highlighted region, examine the BASELINE at those coordinates
Step 3: Examine the CURRENT at the same coordinates
Step 4: Describe what changed from baseline to current

Return JSON:
{
  "changes": [
    {
      "location": "top-right corner, navigation bar area",
      "baseline_state": "Blue 'Submit' button with white text",
      "current_state": "Gray 'Submit' button with dark text, appears disabled",
      "description": "Submit button changed from active (blue) to disabled (gray) state",
      "severity": "major",
      "likely_intentional": false
    }
  ],
  "summary": "One-sentence overall assessment",
  "regression_detected": true
}

Rules:
- Only report changes visible in the DIFF highlights
- Distinguish intentional changes from regressions
- Ignore antialiasing and sub-pixel rendering differences
- Rate severity: critical (broken), major (functional impact), minor (cosmetic), info (expected)`;
```

### Viewing Three Images as the Agent

Save all three images and view them with the agent's built-in vision:

```javascript
// Save baseline, current, and diff for agent inspection
await fs.promises.writeFile('/tmp/baseline.png', baselineBuffer);
await fs.promises.writeFile('/tmp/current.png', currentBuffer);
await fs.promises.writeFile('/tmp/diff.png', diffBuffer);

// Codex: emit all three
await codex.emitImage({ bytes: baselineBuffer, mimeType: "image/png" });
await codex.emitImage({ bytes: currentBuffer, mimeType: "image/png" });
await codex.emitImage({ bytes: diffBuffer, mimeType: "image/png" });

// Claude Code / Gemini CLI: agent reads the saved files with built-in vision
```

The agent then applies the forced reasoning process (scan diff highlights, compare baseline vs current, classify severity) using its own visual understanding. No external API call needed.

---

## Screenshot Stabilization

Before capturing screenshots for comparison, stabilize the page to avoid false positives from animations, loading states, font rendering, and scrollbars.

Source: [Argos CI](https://argos-ci.com/docs/playwright)

### CSS Injection for Deterministic Screenshots

```typescript
async function stabilizeForScreenshot(page: Page): Promise<void> {
  await page.addStyleTag({
    content: `
      /* Disable all animations and transitions */
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
        caret-color: transparent !important;
      }

      /* Hide scrollbars */
      ::-webkit-scrollbar { display: none !important; }
      * { scrollbar-width: none !important; }

      /* Force consistent font rendering */
      * {
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: geometricPrecision !important;
      }

      /* Convert sticky/fixed to absolute to prevent viewport-dependent positioning */
      [style*="position: fixed"],
      [style*="position: sticky"] {
        position: absolute !important;
      }
    `,
  });
}
```

### Wait Strategies Before Screenshot

```typescript
async function waitForStableScreenshot(page: Page): Promise<void> {
  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);

  // Wait for all images
  await page.evaluate(() => {
    const images = Array.from(document.images);
    return Promise.all(
      images
        .filter(img => !img.complete)
        .map(img => new Promise(resolve => {
          img.addEventListener('load', resolve);
          img.addEventListener('error', resolve);
        }))
    );
  });

  // Wait for network idle
  await page.waitForLoadState('networkidle');

  // Wait for aria-busy to clear (loading indicators)
  await page.waitForFunction(() => {
    return !document.querySelector('[aria-busy="true"]');
  }, { timeout: 5000 }).catch(() => {});

  // Small settle time for any final renders
  await page.waitForTimeout(100);
}
```

### Masking Dynamic Content

Use `data-visual-test` attributes to handle elements that change between runs:

```html
<!-- Make element transparent (keeps layout, hides content) -->
<div data-visual-test="transparent">
  <span>Current time: 12:34:56</span>
</div>

<!-- Remove element completely -->
<div data-visual-test="removed">
  <img src="random-avatar.png" />
</div>

<!-- Black out element (keeps size, hides content) -->
<div data-visual-test="blackout">
  <canvas id="animated-chart"></canvas>
</div>
```

```typescript
async function applyVisualTestMasks(page: Page): Promise<void> {
  await page.evaluate(() => {
    document.querySelectorAll('[data-visual-test="transparent"]').forEach(el => {
      (el as HTMLElement).style.opacity = '0';
    });
    document.querySelectorAll('[data-visual-test="removed"]').forEach(el => {
      (el as HTMLElement).style.display = 'none';
    });
    document.querySelectorAll('[data-visual-test="blackout"]').forEach(el => {
      (el as HTMLElement).style.background = '#000';
      (el as HTMLElement).innerHTML = '';
    });
  });
}
```

---

## Agent-Driven Visual Questions

The simplest pattern for ad-hoc visual checks: capture a screenshot, emit/save it, and the agent (you) answers the question using built-in vision. No external API calls.

Inspired by: [Philip Fong](https://dev.to/philipfong/using-ai-in-playwright-tests-35od)

### Interactive Pattern (Agent Sees Directly)

```javascript
// Capture and emit for agent to view
await page.screenshot({ path: '/tmp/checkout-check.png', type: 'jpeg', quality: 85 });
// Agent reads the image and answers: "Is there a visible order total with a dollar amount?"

// Mobile check
await page.setViewportSize({ width: 375, height: 667 });
await page.screenshot({ path: '/tmp/mobile-nav-check.png', type: 'jpeg', quality: 85 });
// Agent reads the image and answers: "Is the navigation collapsed into a hamburger menu?"
```

### Codex Pattern (emitImage)

```javascript
var bytes = await page.screenshot({ type: "jpeg", quality: 85, scale: "css" });
await codex.emitImage({ bytes, mimeType: "image/jpeg" });
// Agent sees the screenshot and can answer any visual question about it
```

### Structured Self-Check

When doing visual QA, frame questions as YES/NO with reasoning:

```
For each screenshot, ask yourself:
1. YES/NO: Does the layout look correct for this viewport?
2. YES/NO: Is all expected content visible and readable?
3. YES/NO: Are there any visual defects (clipping, overflow, contrast)?
4. If NO to any: describe the issue, its location, and severity.
```

This replaces the external `askAI()` API pattern — the agent's built-in vision is the analysis engine.

---

## Playwright Built-in Visual Comparisons

Playwright's built-in `toHaveScreenshot()` provides pixel-level visual regression without external services. Use this for baseline comparisons; use AI analysis (above) for semantic understanding.

### Complete Options Reference

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `animations` | `"disabled"` / `"allow"` | `"disabled"` | Fast-forward finite, cancel infinite animations |
| `caret` | `"hide"` / `"initial"` | `"hide"` | Hide text cursor |
| `clip` | `{x, y, width, height}` | -- | Rectangular clipping region |
| `fullPage` | boolean | `false` | Capture entire scrollable page |
| `mask` | `Locator[]` | -- | Overlay colored boxes on dynamic elements |
| `maskColor` | CSS color string | `#FF00FF` | Custom mask overlay color |
| `maxDiffPixels` | number | -- | Absolute pixel count tolerance (50-200 recommended) |
| `maxDiffPixelRatio` | number 0-1 | -- | Percentage tolerance (0.005-0.02 starting point) |
| `scale` | `"css"` / `"device"` | `"css"` | Pixel scaling for high-DPI |
| `stylePath` | string / string[] | -- | CSS file(s) injected during screenshot |
| `threshold` | number 0-1 | `0.2` | Per-pixel color sensitivity in YIQ space |
| `timeout` | number (ms) | config default | Retry duration for auto-waiting |

### Dynamic Content Masking

```typescript
await expect(page).toHaveScreenshot('dashboard.png', {
  mask: [
    page.locator('.timestamp'),
    page.locator('.user-avatar'),
    page.locator('[data-testid="live-feed"]'),
  ],
  maskColor: '#FF00FF',
  maxDiffPixels: 100,
});
```

### CSS Injection via stylePath

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      stylePath: './screenshot.css',
      maxDiffPixels: 100,
    },
  },
});
```

```css
/* screenshot.css — hide dynamic content for stable baselines */
#datetime { display: none; }
.live-activity-feed { visibility: hidden; }
iframe[src$="/demo.html"] { visibility: hidden; }
main a:visited { color: var(--color-link); }
```

### Snapshot Path Organization

Use `snapshotPathTemplate` to organize baselines by platform, browser, and branch:

```typescript
export default defineConfig({
  // Organize: __snapshots__/desktop-chrome/linux/tests/home.spec.ts/hero.png
  snapshotPathTemplate: '{snapshotDir}/{projectName}/{platform}/{testFilePath}/{arg}{ext}',

  projects: [
    { name: 'desktop-chrome', use: { viewport: { width: 1280, height: 720 } } },
    { name: 'tablet', use: { viewport: { width: 768, height: 1024 } } },
    { name: 'mobile', use: { viewport: { width: 375, height: 667 } } },
  ],
});
```

Available tokens: `{arg}`, `{ext}`, `{platform}`, `{projectName}`, `{snapshotDir}`, `{testDir}`, `{testFileDir}`, `{testFileName}`, `{testFilePath}`, `{testName}`.

### Full-Page Screenshot with Dynamic Height

```typescript
async function captureFullPage(page: Page, name: string) {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.waitForLoadState('networkidle');
  const height = await page.evaluate(() =>
    document.documentElement.getBoundingClientRect().height
  );
  await page.setViewportSize({ width: 1280, height: Math.ceil(height) });
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveScreenshot(name, {
    fullPage: true,
    animations: 'disabled',
    caret: 'hide',
  });
}
```

---

## Set-of-Marks Vision Overlays

Annotate screenshots with numbered markers on interactive elements so vision LLMs have spatial awareness of what can be clicked, typed, or interacted with.

Source: [testchimphq/ai-wright](https://github.com/testchimphq/ai-wright)

### How It Works

```
1. Query DOM for all interactive elements (buttons, links, inputs, etc.)
2. Get bounding boxes for each element
3. Draw numbered labels on the screenshot at each element's position
4. Send annotated screenshot + element map to LLM
5. LLM references elements by number: "Click element #3"
```

```typescript
interface ElementMark {
  id: number;
  tag: string;
  role?: string;
  text?: string;
  bbox: { x: number; y: number; width: number; height: number };
  attributes: Record<string, string>;
}

async function getInteractiveElements(page: Page): Promise<ElementMark[]> {
  return page.evaluate(() => {
    const selectors = 'a, button, input, select, textarea, [role="button"], [role="link"], [onclick], [tabindex]';
    const elements = document.querySelectorAll(selectors);
    const marks: ElementMark[] = [];

    elements.forEach((el, idx) => {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      marks.push({
        id: idx + 1,
        tag: el.tagName.toLowerCase(),
        role: el.getAttribute('role') || undefined,
        text: (el.textContent || '').trim().slice(0, 50),
        bbox: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
        attributes: {
          ...(el.getAttribute('name') && { name: el.getAttribute('name')! }),
          ...(el.getAttribute('type') && { type: el.getAttribute('type')! }),
          ...(el.getAttribute('placeholder') && { placeholder: el.getAttribute('placeholder')! }),
        },
      });
    });

    return marks;
  });
}
```

---

## ARIA Snapshot Navigation

Use Playwright's accessibility tree instead of CSS selectors or vision for element discovery. More token-efficient than screenshots and more reliable than CSS selectors.

Source: [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp), [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser)

```typescript
// Get accessibility snapshot (Playwright 1.49+)
const snapshot = await page.accessibility.snapshot();

// Navigate using ARIA roles and names
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
await page.getByRole('navigation').getByRole('link', { name: 'Settings' }).click();

// Combine with visual verification
const ariaTree = await page.accessibility.snapshot();
const screenshot = await page.screenshot();
// Send both to LLM: "Given this accessibility tree and screenshot, verify the form is complete"
```

**When to use which:**

| Approach | Best For | Token Cost |
|----------|----------|------------|
| ARIA snapshot | Navigation, form filling, element discovery | Low |
| Vision screenshot | Visual QA, layout verification, aesthetic judgment | High |
| SoM overlays | Interactive debugging, click targets | Medium |
| Combo (ARIA + screenshot) | Full QA signoff | Medium-High |

---

## Playwright Test Agents

Playwright v1.56+ includes built-in AI-powered test agents — three specialized agents that handle the full lifecycle of test creation and maintenance.

Source: [Playwright Test Agents Docs](https://playwright.dev/docs/test-agents)

### The Three Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Planner** | Explores app, discovers flows | URL + app description | Markdown test plans |
| **Generator** | Converts plans to code | Test plans | Playwright test files with robust locators |
| **Healer** | Auto-repairs broken tests | Failed test + error | Fixed test (avg ~8 seconds) |

### Quick Start

```bash
# Initialize agents with Claude as the LLM backend
npx playwright init-agents --loop=claude

# Generate test plan for a page
npx playwright test --agents planner --url https://your-app.com/dashboard

# Generate test code from plan
npx playwright test --agents generator --plan tests/plans/dashboard.md

# Auto-heal broken tests
npx playwright test --agents healer --failed tests/dashboard.spec.ts
```

### Results (Community Benchmarks)

- First-run pass rate: **87%**
- Weekly test maintenance: **8 hours → 2 hours**
- Auto-heal success rate: **~8 seconds** per fix

### CLI+SKILLs Mode (v1.58+)

Token-efficient alternative to MCP — uses structured prompts instead of tool calls:

```bash
npx playwright test --agents generator --mode skills
```

---

## Agent-Driven CI QA

Use AI agents as automated QA reviewers in CI/CD pipelines. Three production-proven architectures:

### Architecture A: PR-Triggered Black-Box QA ("Quinn")

Claude Code + Playwright MCP runs in GitHub Actions when a PR label is added. The agent can only interact through the browser — no source code access.

Source: [alexop.dev](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)

```yaml
# .github/workflows/qa-agent.yml
name: AI QA Review
on:
  pull_request:
    types: [labeled]

jobs:
  qa:
    if: contains(github.event.label.name, 'qa-review')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude QA
        uses: anthropics/claude-code-action@v1
        with:
          claude_args: |
            --mcp-config '{"mcpServers":{"playwright":{
              "command":"npx","args":["@playwright/mcp@latest","--headless"]
            }}}'
          prompt: |
            Test the deployed preview at ${{ env.PREVIEW_URL }}.
            Check desktop (1280x720) and mobile (375x667) viewports.
            Report bugs as a Markdown comment with embedded screenshots.
```

**Key aspects:**
- Black-box testing — agent cannot read source code, only interact through browser
- Restricted MCP tools: `browser_navigate`, `browser_click`, `browser_type`, `browser_take_screenshot`, `browser_resize`
- Tests both desktop and mobile viewports
- Generates Markdown bug reports as PR comments
- Execution time: 7-10 minutes per PR

### Architecture B: Council of Sub-Agents

8 specialized agents in a pipeline, each with a distinct role:

Source: [OpenObserve](https://openobserve.ai/blog/autonomous-qa-testing-ai-agents-claude-code/)

```
Analyst → Architect → Engineer → Sentinel → Healer → Scribe → Orchestrator → Test Inspector
```

The **Sentinel** is a hard quality gate — tests must pass before proceeding. Results:
- Test coverage: 380 → 700+ tests (+84%)
- Flaky tests: -85%
- Time to first passing test: 1 hour → 5 minutes

Built with Claude Code slash commands in `.claude/commands/`.

### Architecture C: Single-Call Multi-Viewport (Argos CI)

```typescript
import { argosScreenshot } from '@argos-ci/playwright';

test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await argosScreenshot(page, 'homepage', {
    viewports: ['macbook-16', 'ipad-2', 'iphone-x'],
  });
});
```

---

## Dynamic Script Generation

Instead of hardcoding test scenarios, have the LLM write fresh Playwright scripts for each test request and execute via a runner.

Source: [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)

```javascript
// run.js — universal Playwright script runner
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = { screenshots: [], console: [], errors: [] };

  page.on('console', msg => results.console.push(msg.text()));
  page.on('pageerror', err => results.errors.push(err.message));

  try {
    // Dynamic script is imported/required here
    const script = require(process.argv[2]);
    await script({ browser, context, page, results });
  } finally {
    console.log(JSON.stringify(results, null, 2));
    await browser.close();
  }
})();
```

The LLM generates the test script, writes it to a temp file, then runs: `node run.js /tmp/test-checkout-flow.js`

---

## Structured Verification Types

Define verification assertions as typed enums instead of free-text, enabling more reliable automated QA.

Source: [Ilikepizza2/VibeCheck](https://github.com/Ilikepizza2/VibeCheck), [testchimphq/ai-wright](https://github.com/testchimphq/ai-wright)

```typescript
type VerificationType =
  | { type: 'text_contains'; selector: string; expected: string }
  | { type: 'text_equals'; selector: string; expected: string }
  | { type: 'is_visible'; selector: string }
  | { type: 'is_hidden'; selector: string }
  | { type: 'is_enabled'; selector: string }
  | { type: 'is_disabled'; selector: string }
  | { type: 'has_value'; selector: string; expected: string }
  | { type: 'has_attribute'; selector: string; attribute: string; expected: string }
  | { type: 'has_class'; selector: string; className: string }
  | { type: 'element_count'; selector: string; expected: number }
  | { type: 'url_contains'; expected: string }
  | { type: 'url_equals'; expected: string }
  | { type: 'title_contains'; expected: string }
  | { type: 'screenshot_matches'; name: string; threshold?: number }
  | { type: 'visual_check'; description: string; expected: string };

async function runVerification(page: Page, v: VerificationType): Promise<{ passed: boolean; actual?: string }> {
  switch (v.type) {
    case 'text_contains':
      const text = await page.locator(v.selector).textContent();
      return { passed: text?.includes(v.expected) ?? false, actual: text ?? '' };
    case 'is_visible':
      const visible = await page.locator(v.selector).isVisible();
      return { passed: visible };
    case 'element_count':
      const count = await page.locator(v.selector).count();
      return { passed: count === v.expected, actual: String(count) };
    case 'visual_check':
      // Capture screenshot for agent to inspect with built-in vision
      await page.screenshot({ path: `/tmp/verify-${Date.now()}.png` });
      // Agent views the screenshot and evaluates: v.description + v.expected
      return { passed: true, actual: 'Agent reviews screenshot directly' };
    // ... other cases
  }
}
```

---

## Image Compression for Agent Context

Compress screenshots to reduce the agent's context window usage. Smaller images = faster processing and more room for other content.

```typescript
import sharp from 'sharp';

async function compressImage(buffer: Buffer, quality: number = 70): Promise<Buffer> {
  return sharp(buffer)
    .jpeg({ quality, progressive: true })
    .toBuffer();
}

async function prepareForLLM(screenshotBuffer: Buffer, maxSizeMB: number = 4): Promise<Buffer> {
  let compressed = screenshotBuffer;
  let quality = 85;

  while (compressed.length > maxSizeMB * 1024 * 1024 && quality > 20) {
    compressed = await compressImage(screenshotBuffer, quality);
    quality -= 15;
  }

  return compressed;
}
```

---

## Design-to-Implementation Diff

Compare design mockups (from Figma, Sketch, etc.) against live page screenshots to verify implementation fidelity.

Source: [outhsics/ui-diff-tool](https://github.com/outhsics/ui-diff-tool)

### Workflow

```
1. Export design mockup as PNG at target viewport size
2. Capture live page screenshot at same viewport
3. Generate pixel diff
4. Classify severity by diff percentage:
   - < 1%: low (sub-pixel rendering)
   - 1-5%: medium (minor spacing/color)
   - 5-15%: high (layout shift)
   - > 15%: critical (major deviation)
5. Agent views all three images and applies structured repair analysis
```

### AI Repair Prompt

```typescript
const DESIGN_DIFF_PROMPT = `Compare the DESIGN mockup against the IMPLEMENTATION screenshot.

For each deviation:
1. Describe what differs (spacing, color, typography, layout, element presence)
2. Classify severity: low | medium | high | critical
3. Suggest specific CSS fix

Return JSON:
{
  "fidelity_score": 0-100,
  "deviations": [
    {
      "area": "header navigation",
      "description": "Logo is 24px from left edge, design shows 32px",
      "severity": "medium",
      "css_fix": ".logo { margin-left: 32px; }"
    }
  ]
}`;
```

---

## Docker Deterministic Rendering

For CI visual regression, use the official Playwright Docker image to ensure identical rendering across environments. Eliminates false positives from OS font rendering, GPU differences, and system library versions.

```yaml
# .github/workflows/visual-tests.yml
jobs:
  visual-tests:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v1.58.2-noble
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: visual-diffs
          path: test-results/
```

**Why Docker matters for visual tests:**
- Font rendering differs between macOS, Windows, and Linux
- Anti-aliasing algorithms vary by GPU driver
- System library versions affect text metrics
- Docker pins ALL of these variables

**Updating baselines:**

```bash
# Generate baselines inside the same Docker image
docker run --rm -v $(pwd):/work -w /work mcr.microsoft.com/playwright:v1.58.2-noble \
  npx playwright test --update-snapshots
```

---

## Dev Server Auto-Detection

Auto-detect running dev servers to know which localhost port to target.

Source: [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)

```typescript
import { execSync } from 'child_process';

interface DevServer {
  port: number;
  pid: number;
  command: string;
}

function detectDevServers(): DevServer[] {
  const ports = [3000, 3001, 4000, 4200, 5000, 5173, 8000, 8080, 8888];
  const servers: DevServer[] = [];

  for (const port of ports) {
    try {
      const result = execSync(`lsof -i :${port} -t 2>/dev/null`).toString().trim();
      if (result) {
        const pid = parseInt(result.split('\n')[0]);
        const cmd = execSync(`ps -p ${pid} -o command= 2>/dev/null`).toString().trim();
        servers.push({ port, pid, command: cmd });
      }
    } catch {
      // Port not in use
    }
  }

  return servers;
}

// Usage: auto-set TARGET_URL
const servers = detectDevServers();
if (servers.length > 0) {
  const TARGET_URL = `http://127.0.0.1:${servers[0].port}`;
}
```

---

## Notable Open-Source Projects

Projects referenced in this document and worth exploring further:

| Project | What It Does | Key Pattern |
|---------|-------------|-------------|
| [Arghajit47/Playwright-Visual-Testing](https://github.com/Arghajit47/Playwright-Visual-Testing) | AI-powered visual regression with Gemini/Claude | Three-image LLM diff |
| [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) | Claude Code skill for dynamic Playwright automation | Dynamic script generation |
| [disler/bowser](https://github.com/disler/bowser) | Four-layer agentic browser automation | Composable skill architecture |
| [testchimphq/ai-wright](https://github.com/testchimphq/ai-wright) | AI-native Playwright actions with vision | Set-of-Marks overlays |
| [Ilikepizza2/VibeCheck](https://github.com/Ilikepizza2/VibeCheck) | MCP server for visual QA in Cursor | LLM-driven test recording |
| [noiv/skill-playwright-minimal](https://github.com/noiv/skill-playwright-minimal) | Persistent browser daemon for Claude Code | File-based IPC |
| [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser) | Agent browser skill with ARIA snapshots | Named persistent pages |
| [Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern) | Vision-first browser automation | Multi-strategy scraping |
| [outhsics/ui-diff-tool](https://github.com/outhsics/ui-diff-tool) | Design-to-implementation diff | AI repair prompts |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Official Playwright MCP server | A11y-first navigation |
| [Argos CI](https://argos-ci.com) | Visual testing platform | Screenshot stabilization |
| [Visual-Regression-Tracker](https://github.com/Visual-Regression-Tracker/agent-playwright) | Self-hosted visual regression | looks-same integration |
| [autospec-ai/playwright](https://github.com/autospec-ai/playwright) | AI-generated E2E tests from code diffs | Diff-driven test generation |
| [testdino-hq/playwright-skill](https://github.com/testdino-hq/playwright-skill) | 70+ guides, 5 skill packs for Claude Code | `npx skills add` install |
| [jarbon/coTestPilot](https://github.com/jarbon/coTestPilot) | GPT-4 Vision for AI bug detection | Vision-driven bug reports |
| [zerostep-ai/zerostep](https://github.com/zerostep-ai/zerostep) | `ai()` function for Playwright | Natural-language actions |
| [executeautomation/mcp-playwright](https://github.com/executeautomation/mcp-playwright) | MCP server for LLM-driven Playwright | Tool-use browser control |
| [Lost Pixel](https://github.com/lost-pixel/lost-pixel) | Open-source Percy/Chromatic alternative | Storybook + Playwright |
| [BackstopJS](https://github.com/garris/BackstopJS) | Viewport-based visual regression | Multi-viewport baselines |
