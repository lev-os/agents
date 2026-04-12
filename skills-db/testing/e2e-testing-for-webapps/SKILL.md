---
name: e2e-testing-for-webapps
description: >-
  E2E testing for Next.js + Playwright + Supabase. OAuth bypass via test users, interactive
  debugging, visual QA. Use when: E2E, Playwright, visual regression, Electron testing.
---

# E2E Testing for Web & Electron Apps

> **Two modes:** Batch testing (CI/test suites) and Interactive debugging (persistent browser sessions for iterative QA). Both share the same QA methodology.

> **Stack:** Next.js 16 + Playwright + Supabase Auth + agent-native vision

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       E2E TESTING ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   MODE 1: BATCH (CI / Test Suites)                                      │
│   ═══════════════════════════════                                       │
│   Playwright Test runner → auth setup → test specs → reports            │
│   ✓ Headless CI  ✓ Parallel workers  ✓ Retries  ✓ Artifacts            │
│                                                                         │
│   MODE 2: INTERACTIVE (Debugging / Iterative QA)                        │
│   ═══════════════════════════════════════════════                       │
│   Persistent browser session → live reload → functional QA → visual QA  │
│   ✓ Desktop/Mobile/Electron  ✓ Session reuse  ✓ Screenshot analysis     │
│                                                                         │
│   SHARED INFRASTRUCTURE                                                 │
│   ═════════════════════                                                  │
│   1. Auth bypass: Supabase test users with email/password (no OAuth)    │
│   2. Console monitoring: capture runtime, network, hydration errors     │
│   3. Page Objects: BasePage → DashboardPage, SettingsPage, etc.         │
│   4. AI visual analysis: Screenshots → agent-native vision → QA        │
│   5. Diagnostic tools: DOM health check, layout snapshot diff, styles │
│   6. Failure injection: network, input stress, state corruption       │
│   7. QA methodology: inventory → functional QA → visual QA → signoff   │
│                                                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start: Batch Testing

```bash
# 1. Install Playwright
bun add -D @playwright/test && bunx playwright install chromium

# 2. Create test user in Supabase (bypasses Google OAuth)
bun scripts/provision-e2e-test-users.ts --user=primary

# 3. Run tests against production
E2E_TEST_EMAIL=test@app.test E2E_TEST_PASSWORD=xxx bun run test:e2e:prod
```

## Quick Start: Interactive Debugging

```bash
# 1. Install Playwright (npm for js_repl compat, bun for everything else)
test -f package.json || npm init -y
npm install playwright
npx playwright install chromium

# 2. Bootstrap persistent session (js_repl, Node REPL, or script)
node -e "import('playwright').then(() => console.log('ready'))"
```

Then launch a browser and start testing — see [INTERACTIVE-SESSIONS.md](references/INTERACTIVE-SESSIONS.md).

---

## The Google OAuth Bypass

**Problem:** Google blocks automated logins (CAPTCHA, headless detection).

**Solution:** Create test users with email/password auth in Supabase — same app, different auth method.

```typescript
// Sign in via Supabase (NOT Google OAuth)
const { data, error } = await supabase.auth.signInWithPassword({
  email: process.env.E2E_TEST_EMAIL,     // e2e-test@app.test
  password: process.env.E2E_TEST_PASSWORD,
});
// Inject session cookies into browser context
await context.addCookies([
  { name: 'sb-access-token', value: data.session.access_token, domain: '...', ... },
]);
```

**Why `.test` TLD?** IANA-reserved, never resolves — test emails can't leak to real inboxes.

**Deep dive:** [AUTHENTICATION.md](references/AUTHENTICATION.md)

---

## QA Inventory Methodology

Before testing, build a coverage list from **three sources:**

1. **User's requested requirements** — what was asked for
2. **Implemented features/behaviors** — what you actually built
3. **Claims in the final response** — what you intend to sign off on

Everything in any of those three sources must map to at least one QA check.

For each item, note:
- The intended functional check (user input → expected result)
- The specific state where visual check must happen
- The evidence to capture (screenshot, assertion)

Add at least **2 exploratory/off-happy-path scenarios** that could expose fragile behavior.

Update the inventory during testing if exploration reveals additional controls, states, or claims.

---

## Workflow

### Batch Mode Phases

| Phase | Steps |
|-------|-------|
| **1. Setup** | Install Playwright, create test users, configure storage state |
| **2. Implementation** | Build Page Objects, add console monitoring, capture screenshots |
| **3. Enhancement** | Add visual analysis, screenshot capture, HTML/JSON reports |
| **4. CI Integration** | Add test:e2e script, GitHub Actions workflow, artifact upload |

### Interactive Mode Loop

1. Build QA inventory from the three sources above
2. Bootstrap persistent browser session (once)
3. Start/confirm dev server
4. Launch runtime (web or Electron), keep handles alive
5. **Edit-Reload-Verify micro-loop** for each component:
   - Make one change → reload → snapshot diff → DOM health check → fix issues → screenshot → verify
6. Run functional QA with real user input (use `.click()`, not `page.evaluate()`)
7. Run separate visual QA pass
8. Run breakpoint sweep for responsive verification
9. Run failure injection pass (network failures, input stress, state corruption)
10. Verify viewport fit, capture evidence screenshots
11. Update inventory if exploration reveals new items
12. Repeat 5-11 until signoff criteria met
13. Clean up session when task is finished

**Deep dive:** Edit-Reload-Verify loop → [SYSTEMATIC-TESTING.md](references/SYSTEMATIC-TESTING.md), DOM health check → [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md)

**Deep dive:** [INTERACTIVE-SESSIONS.md](references/INTERACTIVE-SESSIONS.md)

---

## Functional QA

- Use **real user controls** for signoff: `.click()`, `.fill()`, `.press()` — NOT `page.evaluate()`
- Interact via **Playwright action methods** which simulate real mouse/keyboard and respect visibility, overlapping elements, and event bubbling — `page.evaluate()` bypasses all of this
- Verify **visible results**, not just internal state
- Cover **every control** in the QA inventory at least once
- For stateful toggles: test the full cycle (initial → changed → returned to initial)
- Test **interactive states** (hover, focus, disabled, error, empty, overflow) — see [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md)
- **Exploratory pass** (30-90 seconds) using normal input, not only the happy path
- If exploratory pass reveals new states/controls, add to inventory

## Visual QA (Separate Pass)

- Each user-visible claim needs a matching visual check + reviewed screenshot
- Inspect initial viewport **before scrolling**
- Check **all required regions**, not just the main interaction surface
- Look for: clipping, overflow, distortion, weak contrast, broken layering, alignment problems
- Judge **aesthetic quality** as well as correctness
- For dynamic visuals, inspect long enough to judge stability — don't rely on a single screenshot
- Before signoff, ask: "What visible defect would most embarrass this result?"

**Deep dive:** [VISUAL-QA.md](references/VISUAL-QA.md)

## Signoff Criteria

All three must pass independently — one does not imply the others:

1. **Functional correctness** — user input paths work, QA inventory covered
2. **Viewport fit** — intended initial view visible without unintended clipping/scrolling
3. **Visual quality** — UI is coherent, not aesthetically weak for the task
4. **Failure resilience** (optional, recommended) — app handles network errors, input stress, and state corruption gracefully — see [FAILURE-INJECTION.md](references/FAILURE-INJECTION.md)

Include brief negative confirmation of defect classes checked and not found.

---

## Test User Tiers

| Type | Email | Tier | Purpose |
|------|-------|------|---------|
| `primary` | `e2e-test@app.test` | Pro | Main tests, full features |
| `free` | `e2e-free@app.test` | Free | Paywall, limitations |
| `premium` | `e2e-premium@app.test` | Premium | All features unlocked |
| `fresh` | `e2e-new@app.test` | None | Onboarding, empty states |
| `admin` | `e2e-admin@app.test` | Admin | Admin panel tests |

---

## Key Configuration

```typescript
// playwright.production.config.ts
export default defineConfig({
  testDir: './e2e',
  timeout: 60000,
  retries: 2,
  use: {
    baseURL: 'https://your-app.com',
    trace: 'retain-on-failure',
    screenshot: 'on',
    video: 'retain-on-failure',
    actionTimeout: 30000,
    navigationTimeout: 60000,
  },
  projects: [
    { name: 'auth-setup', testMatch: /auth\.global-setup\.ts/ },
    {
      name: 'authenticated',
      dependencies: ['auth-setup'],
      use: { storageState: '.auth/user.json', ...devices['Desktop Chrome'] },
    },
  ],
});
```

---

## Console Error Categories

| Category | Patterns | Action |
|----------|----------|--------|
| `hydration` | `hydrat`, `server.*different.*client` | Fix SSR mismatch |
| `runtime` | `TypeError`, `ReferenceError` | Fix JS error |
| `network` | `net::ERR`, `fetch.*failed` | Check API/CORS |
| `react` | `Warning:`, `useEffect` | Fix hook issue |
| `security` | `CSP`, `Refused to` | Fix CSP policy |

**Deep dive:** [CONSOLE-MONITORING.md](references/CONSOLE-MONITORING.md)

---

## Page Object Pattern

```typescript
export class DashboardPage extends BasePage {
  static readonly PATH = '/portfolio';
  readonly healthScoreWidget = this.page.locator('[data-testid="health-score"]');
  async goto() { await super.goto(DashboardPage.PATH); }
  async getHealthScore(): Promise<number | null> {
    const text = await this.healthScoreWidget.textContent();
    return text ? parseInt(text.match(/(\d+)/)?.[1] ?? '', 10) : null;
  }
}
```

**Deep dive:** [PAGE-OBJECTS.md](references/PAGE-OBJECTS.md)

---

## AI Visual Analysis

The agent IS the vision model. Capture screenshots with Playwright, emit or save them, and the agent analyzes them directly using its built-in multimodal capabilities. No external API calls needed.

```javascript
// Codex: emit for agent to see
await codex.emitImage({ bytes: await page.screenshot({ type: "jpeg", quality: 85, scale: "css" }), mimeType: "image/jpeg" });

// Claude Code / Gemini CLI: save to file, agent reads it natively
await page.screenshot({ path: '/tmp/visual-check.png' });
```

**Deep dive:** [AI-VISUAL-ANALYSIS.md](references/AI-VISUAL-ANALYSIS.md)

---

## Running Tests

```bash
# Batch mode
bun run test:e2e                                    # Local (headless)
bun run test:e2e:prod --headed                      # Production (visible browser)
bun run test:e2e e2e/tests/dashboard.spec.ts        # Specific file
bun run test:e2e:prod                                # Production (headless)

# Interactive mode (inside persistent session)
await page.goto('http://127.0.0.1:3000');           # Navigate
await page.reload({ waitUntil: 'domcontentloaded' }); # Reload after changes
await page.screenshot({ type: 'jpeg', quality: 85 }); # Capture
```

---

## Validation Checklist

- [ ] Test users exist in Supabase with email/password auth
- [ ] Test users have `is_test_user: true` metadata
- [ ] `.auth/user.json` generated on first run
- [ ] Tests pass in headless CI (no Google OAuth prompts)
- [ ] Console errors captured and categorized
- [ ] Screenshots captured at key test steps
- [ ] DOM health check passes (no critical/major issues)
- [ ] Layout snapshot diff shows no unexpected structural changes
- [ ] QA inventory built and all items covered
- [ ] Functional QA pass completed with real user input (`.click()`, not `evaluate()`)
- [ ] Visual QA pass completed with screenshot evidence
- [ ] Breakpoint sweep completed (mobile through desktop)
- [ ] Interactive states tested (hover, focus, error, empty, overflow)
- [ ] Failure injection pass: no blank pages on API errors, no duplicate submissions
- [ ] Signoff criteria met (functional + viewport fit + visual quality + resilience)
- [ ] No flaky tests from timing issues (use proper waits)

---

## Reference Index

### By Task

| I need to... | Read |
|--------------|------|
| **Set up test user auth bypass** | [AUTHENTICATION.md](references/AUTHENTICATION.md) |
| **Debug interactively with persistent browser** | [INTERACTIVE-SESSIONS.md](references/INTERACTIVE-SESSIONS.md) |
| **Run systematic visual QA and signoff** | [VISUAL-QA.md](references/VISUAL-QA.md) |
| **Capture and normalize screenshots** | [SCREENSHOTS.md](references/SCREENSHOTS.md) |
| **Implement Page Objects** | [PAGE-OBJECTS.md](references/PAGE-OBJECTS.md) |
| **Monitor console errors** | [CONSOLE-MONITORING.md](references/CONSOLE-MONITORING.md) |
| **Add AI visual analysis** | [AI-VISUAL-ANALYSIS.md](references/AI-VISUAL-ANALYSIS.md) |
| **Generate reports and CI artifacts** | [REPORTING.md](references/REPORTING.md) |
| **Quick commands & troubleshooting** | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| **Three-image LLM diff, SoM overlays, stabilization** | [ADVANCED-TECHNIQUES.md](references/ADVANCED-TECHNIQUES.md) |
| **Playwright Test Agents, agent-driven CI QA** | [ADVANCED-TECHNIQUES.md](references/ADVANCED-TECHNIQUES.md) |
| **Run DOM health check, extract computed styles** | [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md) |
| **Layout snapshot diff, render intent declaration** | [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md) |
| **Responsive breakpoint sweep, state triggers** | [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md) |
| **Human-like interaction (avoid evaluate() trap)** | [SYSTEMATIC-TESTING.md](references/SYSTEMATIC-TESTING.md) |
| **Edit-Reload-Verify loop, state matrix sweep** | [SYSTEMATIC-TESTING.md](references/SYSTEMATIC-TESTING.md) |
| **Interactive state catalog, peripheral checks** | [SYSTEMATIC-TESTING.md](references/SYSTEMATIC-TESTING.md) |
| **Inject network failures, test error handling** | [FAILURE-INJECTION.md](references/FAILURE-INJECTION.md) |
| **Input stress testing, rapid interaction, state corruption** | [FAILURE-INJECTION.md](references/FAILURE-INJECTION.md) |
| **Failure resilience audit and scorecard** | [FAILURE-INJECTION.md](references/FAILURE-INJECTION.md) |

### By Topic

| Topic | Reference |
|-------|-----------|
| Google OAuth bypass, Supabase test users, provisioning | [AUTHENTICATION.md](references/AUTHENTICATION.md) |
| Persistent sessions, Electron, mobile, reload/relaunch | [INTERACTIVE-SESSIONS.md](references/INTERACTIVE-SESSIONS.md) |
| QA inventory, functional/visual QA, viewport fit, signoff | [VISUAL-QA.md](references/VISUAL-QA.md) |
| CSS normalization, model-bound screenshots, click helpers | [SCREENSHOTS.md](references/SCREENSHOTS.md) |
| Page Object Model, BasePage, locator strategies, fixtures | [PAGE-OBJECTS.md](references/PAGE-OBJECTS.md) |
| Browser console capture, error categorization, filtering | [CONSOLE-MONITORING.md](references/CONSOLE-MONITORING.md) |
| Agent-native visual analysis, structured QA, severity thresholds | [AI-VISUAL-ANALYSIS.md](references/AI-VISUAL-ANALYSIS.md) |
| HTML/JSON reports, CI artifacts, screenshot management | [REPORTING.md](references/REPORTING.md) |
| LLM diff, SoM overlays, ARIA, stabilization, Test Agents, CI QA | [ADVANCED-TECHNIQUES.md](references/ADVANCED-TECHNIQUES.md) |
| CLI commands, config snippets, failure modes | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| DOM health check, layout snapshot diff, computed styles, breakpoint sweep, state triggers | [DIAGNOSTIC-TOOLS.md](references/DIAGNOSTIC-TOOLS.md) |
| Human-like interaction, Edit-Reload-Verify loop, state matrix, state catalog | [SYSTEMATIC-TESTING.md](references/SYSTEMATIC-TESTING.md) |
| Network failure injection, input stress, state corruption, resilience scorecard | [FAILURE-INJECTION.md](references/FAILURE-INJECTION.md) |

---

## Tools & Scripts

| Tool | Purpose |
|------|---------|
| `scripts/provision-e2e-test-users.ts` | Create test users in Supabase |
| `scripts/reset-e2e-test-user.ts` | Reset user to known seed state |
| `scripts/validate-e2e.sh` | Validate E2E setup |
