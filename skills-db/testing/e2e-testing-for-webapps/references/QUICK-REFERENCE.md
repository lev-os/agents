# Quick Reference

## Commands

### Running Tests (Batch Mode)

```bash
# Full test suite (headless)
bun run test:e2e

# Against production
bun run test:e2e:prod

# Specific test file
bun run test:e2e e2e/tests/dashboard.spec.ts

# Specific test by name
bun run test:e2e -g "health score"

# Headed mode (visible browser)
bun run test:e2e --headed

# Debug mode (step through)
bun run test:e2e --debug

# With UI (interactive)
bun run test:e2e --ui
```

### Interactive Session (Persistent Browser)

```bash
# Setup
npm install playwright && npx playwright install chromium

# Verify
node -e "import('playwright').then(() => console.log('ok'))"

# Launch (in js_repl or Node REPL)
# See INTERACTIVE-SESSIONS.md for full bootstrap
```

```javascript
// Quick interactive launch
var { chromium } = await import("playwright");
var browser = await chromium.launch({ headless: false });
var context = await browser.newContext({ viewport: { width: 1600, height: 900 } });
var page = await context.newPage();
await page.goto("http://127.0.0.1:3000");

// Reload after changes
await page.reload({ waitUntil: "domcontentloaded" });

// Screenshot
await page.screenshot({ path: "debug.png", type: "jpeg", quality: 85 });

// Cleanup
await browser.close();
```

### Reports

```bash
# View HTML report
bunx playwright show-report

# Generate report after failed run
bunx playwright show-report playwright-report
```

### Test User Management

```bash
# Provision all test users
bun scripts/provision-e2e-test-users.ts

# Provision specific user
bun scripts/provision-e2e-test-users.ts --user=primary

# Reset user to seed state
bun scripts/reset-e2e-test-user.ts --user=primary

# Dry run (no changes)
bun scripts/provision-e2e-test-users.ts --dry-run
```

### Debugging

```bash
# Run with trace (creates trace.zip on failure)
bun run test:e2e --trace on

# Open trace viewer
bunx playwright show-trace test-results/trace.zip

# Run with video recording
bun run test:e2e --video on

# Slow motion (500ms between actions)
bun run test:e2e --slowmo 500
```

---

## Configuration Snippets

### playwright.config.ts (Production)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 60000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  fullyParallel: true,

  use: {
    baseURL: process.env.E2E_BASE_URL || 'https://your-app.com',
    trace: 'retain-on-failure',
    screenshot: 'on',
    video: 'retain-on-failure',
    actionTimeout: 30000,
    navigationTimeout: 60000,
  },

  reporter: [
    ['list'],
    ['html', { open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],

  projects: [
    {
      name: 'auth-setup',
      testMatch: /auth\.global-setup\.ts/,
    },
    {
      name: 'chromium',
      dependencies: ['auth-setup'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
    },
    {
      name: 'mobile',
      dependencies: ['auth-setup'],
      use: {
        ...devices['iPhone 14'],
        storageState: '.auth/user.json',
      },
    },
  ],
});
```

### package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test --config=playwright.config.ts",
    "test:e2e:prod": "E2E_BASE_URL=https://your-app.com playwright test --config=playwright.production.config.ts",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

### .env.local Template

```bash
# Test User Credentials
E2E_TEST_EMAIL=e2e-test@app.test
E2E_TEST_PASSWORD=your-password-here
E2E_FREE_EMAIL=e2e-free@app.test
E2E_FREE_PASSWORD=your-password-here

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # For provisioning only

# Base URL
E2E_BASE_URL=http://localhost:3000
```

### .gitignore Additions

```gitignore
# E2E Testing
.auth/
test-results/
playwright-report/
playwright/.cache/

# Keep structure
!.auth/.gitkeep
!test-results/.gitkeep
```

---

## File Structure

```
e2e/
├── auth.global-setup.ts       # Auth once, save state
├── playwright.config.ts       # Config
│
├── pages/                     # Page Objects
│   ├── BasePage.ts
│   ├── DashboardPage.ts
│   ├── SettingsPage.ts
│   └── index.ts               # Re-exports
│
├── fixtures/                  # Test data & config
│   ├── test-users.ts          # User definitions
│   ├── seed-data.ts           # Pre-seeded data
│   ├── pages.ts               # Page object fixtures
│   └── devices.ts             # Viewport configs
│
├── utils/                     # Utilities
│   ├── console-monitor.ts     # Console capture
│   └── screenshot-manager.ts  # Screenshot utilities
│
└── tests/                     # Test specs
    ├── dashboard.spec.ts
    ├── settings.spec.ts
    └── onboarding.spec.ts

scripts/
├── provision-e2e-test-users.ts
├── reset-e2e-test-user.ts
└── validate-e2e.sh
```

---

## Common Patterns

### Wait for Element

```typescript
// Wait for element to be visible
await expect(page.getByTestId('widget')).toBeVisible();

// Wait with custom timeout
await expect(page.getByTestId('widget')).toBeVisible({ timeout: 10000 });

// Wait for element to disappear
await expect(page.locator('.spinner')).toBeHidden();

// Wait for network idle
await page.waitForLoadState('networkidle');
```

### Robust Locators

```typescript
// Prefer role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { name: /dashboard/i })

// Label-based (forms)
page.getByLabel('Email')

// Fallback: test ID
page.getByTestId('health-score')

// Multi-strategy (comma = OR)
page.locator('[data-testid="submit"], button:text("Submit")').first()
```

### Form Interaction

```typescript
// Fill input
await page.getByLabel('Email').fill('test@example.com');

// Select dropdown
await page.getByLabel('Country').selectOption('US');

// Check checkbox
await page.getByLabel('I agree').check();

// Click button
await page.getByRole('button', { name: 'Submit' }).click();
```

### Assertions

```typescript
// URL
await expect(page).toHaveURL(/dashboard/);

// Text content
await expect(page.getByTestId('title')).toContainText('Welcome');

// Visibility
await expect(page.getByTestId('widget')).toBeVisible();
await expect(page.getByTestId('spinner')).toBeHidden();

// Count
await expect(page.locator('tr')).toHaveCount(10);

// Attribute
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('button')).toBeDisabled();
```

### Navigation

```typescript
// Go to URL
await page.goto('/dashboard');

// Wait for navigation
await page.waitForURL(/settings/);

// Click and wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.getByRole('link', { name: 'Settings' }).click(),
]);
```

---

## Troubleshooting

### Batch Mode Issues

| Problem | Fix |
|---------|-----|
| Test times out | `test.setTimeout(120000)` for slow pages |
| Element not found | `await page.pause()` to inspect, or screenshot |
| Auth session expired | Delete `.auth/` and re-run |
| Flaky tests | Use `expect(...).toPass({ timeout: 10000 })` or `test.describe.configure({ retries: 3 })` |
| CI-specific failures | Add `test.setTimeout(120000)` for CI, use `workers: 1` |

### Interactive Session Issues

| Problem | Fix |
|---------|-----|
| `Cannot find module 'playwright'` | Run setup in current workspace, verify import |
| Browser executable missing | `npx playwright install chromium` |
| `net::ERR_CONNECTION_REFUSED` | Dev server not running, check port, use `127.0.0.1` |
| `electron.launch` hangs | Verify `electron` dep, confirm `args`, ensure dev server running |
| `Identifier has already been declared` | Use `var`, new name, or wrap in `{ ... }` |
| `Protocol error: Not supported` | Don't use `appWindow.context().newPage()` in Electron |
| `js_repl` timed out | Break into shorter cells |
| Browser ops fail immediately | Check sandbox mode (`--sandbox danger-full-access` for Codex) |

### Common Debug Techniques

```typescript
// Pause and inspect (batch mode)
await page.pause();

// Take debug screenshot
await page.screenshot({ path: 'debug.png' });

// Print page HTML
console.log(await page.content());

// Check viewport dimensions (interactive mode)
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
})));
```

---

## Checklist: New Test

- [ ] Extend Page Object or create new one
- [ ] Use role-based locators where possible
- [ ] Add `await expect(...).toBeVisible()` after navigation
- [ ] Check console errors: `expect(page.getConsoleErrors()).toHaveLength(0)`
- [ ] Add screenshot at key steps (if using AI analysis)
- [ ] Test both desktop and mobile viewports
- [ ] Verify test passes in headless mode
- [ ] Run full suite before committing

---

## Checklist: New Test User

- [ ] Define in `e2e/fixtures/test-users.ts`
- [ ] Add env vars: `E2E_*_EMAIL`, `E2E_*_PASSWORD`
- [ ] Create seed data in `e2e/fixtures/seed-data.ts`
- [ ] Run provisioning: `bun scripts/provision-e2e-test-users.ts --user=<type>`
- [ ] Add credentials to `.env.local`
- [ ] Add to CI secrets

---

## Checklist: Interactive QA Session

- [ ] QA inventory built from requirements + features + claims
- [ ] Dev server running in persistent TTY
- [ ] Browser/Electron session bootstrapped
- [ ] Edit-Reload-Verify loop used for each component (not building blind)
- [ ] DOM health check passes (no critical/major issues)
- [ ] Functional QA: all inventory items tested with `.click()` / `.fill()` (not `evaluate()`)
- [ ] Interactive states tested (hover, focus, error, empty, overflow)
- [ ] Exploratory pass: 30-90 seconds of unscripted interaction
- [ ] Visual QA: all claims verified with screenshot evidence
- [ ] Breakpoint sweep: mobile through desktop screenshots
- [ ] Viewport fit: initial view checked (screenshot + numeric)
- [ ] Failure injection: smoke test (all-APIs-down + storage-wipe) passes
- [ ] Failure injection: submit buttons prevent duplicate submissions
- [ ] Signoff: functional + viewport + visual + resilience all pass independently
- [ ] Session cleaned up (or intentionally kept alive)

---

## Diagnostic Tools (Quick Use)

### DOM Health Check

```javascript
// Paste domHealthCheck function from DIAGNOSTIC-TOOLS.md, then:
const health = await domHealthCheck(page);
console.log(`Issues: ${health.issueCount} (${health.bySeverity.critical} critical, ${health.bySeverity.major} major)`);
for (const i of health.issues.slice(0, 5)) console.log(`  [${i.severity}] ${i.detail}`);
```

### Computed Styles (Debug a Specific Element)

```javascript
// Paste inspectElement function from DIAGNOSTIC-TOOLS.md, then:
const info = await inspectElement(page, '[data-testid="problem-element"]');
console.log(JSON.stringify(info, null, 2));
```

### Breakpoint Sweep

```javascript
// Paste BREAKPOINTS + breakpointSweep from DIAGNOSTIC-TOOLS.md, then:
const results = await breakpointSweep(page, { prefix: 'my-page' });
// Review screenshots in /tmp/breakpoints/
```

### Layout Snapshot Diff

```javascript
// Paste captureLayoutSnapshot + diffLayoutSnapshots from DIAGNOSTIC-TOOLS.md, then:
const before = await captureLayoutSnapshot(page);
// ... make change, reload ...
const after = await captureLayoutSnapshot(page);
const diff = diffLayoutSnapshots(before, after);
console.log(`Diffs: ${diff.summary.totalDiffs} (${diff.summary.disappeared} gone, ${diff.summary.appeared} new, ${diff.summary.changed} changed)`);
for (const d of diff.diffs.slice(0, 10)) {
  if (d.type === 'changed') d.changes.forEach(c => console.log(`  [${d.severity}] ${d.selector}: ${c.detail}`));
  else console.log(`  [${d.severity}] ${d.detail}`);
}
```

### State Matrix Sweep

```javascript
// See SYSTEMATIC-TESTING.md for STATE_MATRIX definition + stateMatrixSweep function
const results = await stateMatrixSweep(page, STATE_MATRIX, {
  url: 'http://127.0.0.1:3000',
  screenshotDir: '/tmp/matrix',
});
```

### Failure Injection (Quick Smoke Test)

```javascript
// Paste injectNetworkFailure + corruptSessionState from FAILURE-INJECTION.md, then:

// 1. Block all APIs — does the page show an error or go blank?
const inj = await injectNetworkFailure(page, '**/api/**', 'abort', { log: false });
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
const blank = await page.evaluate(() => document.body.innerText.trim().length < 20);
console.log(`All APIs down: ${blank ? 'FAIL (blank page)' : 'PASS'}`);
await page.screenshot({ path: '/tmp/smoke-apis-down.png' });
await inj.remove();

// 2. Return 500 for specific endpoint
const inj2 = await injectNetworkFailure(page, '**/api/v1/data', 'status', { status: 500 });
await page.reload({ waitUntil: 'domcontentloaded' });
await page.screenshot({ path: '/tmp/500-test.png' });
await inj2.remove();

// 3. Test double-click on submit
// Paste rapidInteractionTest from FAILURE-INJECTION.md, then:
const result = await rapidInteractionTest(page, 'button[type="submit"]');
console.log(`Double-click: [${result.severity}] ${result.detail}`);
```

### Network Dependency Discovery

```javascript
// Paste discoverNetworkDependencies from FAILURE-INJECTION.md, then:
const deps = await discoverNetworkDependencies(page, async (p) => {
  await p.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
});
// deps[].pathPattern can be used with injectNetworkFailure
```

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `E2E_TEST_EMAIL` | Yes | Primary test user email |
| `E2E_TEST_PASSWORD` | Yes | Primary test user password |
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes | Supabase anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Provisioning | Admin key for user creation |
| `E2E_BASE_URL` | Optional | Override test target URL |
| `CI` | Auto | Set by CI systems, enables CI-specific config |
