# Page Object Model with Playwright

## Table of Contents
- [Why Page Objects?](#why-page-objects)
- [Project Structure](#project-structure)
- [BasePage Class](#basepage-class)
- [Page Implementation Example](#page-implementation-example)
- [Locator Strategies](#locator-strategies)
- [Fixtures Integration](#fixtures-integration)
- [Anti-Patterns](#anti-patterns)

---

## Why Page Objects?

Page Object Model (POM) provides:

| Benefit | Without POM | With POM |
|---------|-------------|----------|
| **Maintenance** | Change locator in 50 tests | Change in 1 file |
| **Reusability** | Duplicate code everywhere | Single method, many tests |
| **Readability** | `page.click('[data-testid="submit"]')` | `loginPage.submit()` |
| **Abstraction** | Test knows UI implementation | Test knows intent |

---

## Project Structure

```
e2e/
├── pages/
│   ├── BasePage.ts           # Foundation class
│   ├── DashboardPage.ts      # Portfolio dashboard
│   ├── SettingsPage.ts       # User settings
│   ├── PricingPage.ts        # Pricing/upgrade
│   ├── OnboardingWizard.ts   # New user flow
│   └── index.ts              # Re-exports
├── fixtures/
│   ├── test-users.ts         # User definitions
│   ├── seed-data.ts          # Pre-defined data
│   └── devices.ts            # Viewport configs
├── utils/
│   ├── console-monitor.ts    # Console error capture
│   ├── screenshot.ts         # Screenshot utilities
│   └── ai-analyzer.ts        # AI visual analysis
├── auth.global-setup.ts      # One-time auth
└── tests/
    ├── dashboard.spec.ts
    ├── settings.spec.ts
    └── onboarding.spec.ts
```

---

## BasePage Class

Foundation class with common utilities:

```typescript
// e2e/pages/BasePage.ts
import { type Page, type Locator, expect } from '@playwright/test';
import { ConsoleMonitor, type ConsoleMessage } from '../utils/console-monitor';

export interface NavigationOptions {
  waitUntil?: 'load' | 'domcontentloaded' | 'networkidle';
  timeout?: number;
  screenshot?: boolean;
}

export class BasePage {
  readonly page: Page;
  protected consoleMonitor: ConsoleMonitor;

  constructor(page: Page) {
    this.page = page;
    this.consoleMonitor = new ConsoleMonitor(page);
  }

  // --- Navigation ---

  async goto(path: string, options: NavigationOptions = {}) {
    const { waitUntil = 'load', timeout = 30000, screenshot = false } = options;

    const response = await this.page.goto(path, { waitUntil, timeout });

    if (screenshot) {
      await this.screenshot('after-navigation');
    }

    return response;
  }

  async waitForNavigation(options: { waitUntil?: 'load' | 'networkidle' } = {}) {
    await this.page.waitForLoadState(options.waitUntil ?? 'networkidle');
  }

  // --- Locators ---

  getByTestId(testId: string): Locator {
    return this.page.getByTestId(testId);
  }

  getByRole(role: Parameters<Page['getByRole']>[0], options?: Parameters<Page['getByRole']>[1]): Locator {
    return this.page.getByRole(role, options);
  }

  getByLabel(text: string | RegExp): Locator {
    return this.page.getByLabel(text);
  }

  getByText(text: string | RegExp): Locator {
    return this.page.getByText(text);
  }

  // --- Assertions ---

  async assertVisible(locator: Locator, options?: { timeout?: number }) {
    await expect(locator).toBeVisible({ timeout: options?.timeout });
  }

  async assertText(locator: Locator, text: string | RegExp) {
    await expect(locator).toContainText(text);
  }

  async assertURL(pattern: string | RegExp) {
    await expect(this.page).toHaveURL(pattern);
  }

  // --- Screenshots ---

  async screenshot(stepName: string, options?: { fullPage?: boolean }): Promise<string> {
    const timestamp = Date.now();
    const device = this.isMobile() ? 'mobile' : 'desktop';
    const filename = `${stepName}_${device}_${timestamp}.png`;
    const path = `test-results/screenshots/${filename}`;

    await this.page.screenshot({
      path,
      fullPage: options?.fullPage ?? false,
    });

    return path;
  }

  // --- Console Monitoring ---

  getConsoleErrors(category?: string): ConsoleMessage[] {
    return this.consoleMonitor.getErrors(category);
  }

  getUnexpectedErrors(): ConsoleMessage[] {
    return this.consoleMonitor.getUnexpectedErrors();
  }

  // --- Utilities ---

  isMobile(): boolean {
    const viewport = this.page.viewportSize();
    return viewport ? viewport.width < 768 : false;
  }

  async waitForSpinnersToDisappear(timeout = 15000) {
    await this.page.waitForFunction(() => {
      const spinners = document.querySelectorAll('[class*="spinner"], [class*="loading"]');
      return spinners.length === 0;
    }, { timeout });
  }

  async waitForHydration() {
    // Wait for Next.js hydration to complete
    await this.page.waitForFunction(() => {
      return document.readyState === 'complete' &&
        !document.querySelector('[data-hydrating="true"]');
    });
  }
}
```

---

## Page Implementation Example

```typescript
// e2e/pages/DashboardPage.ts
import { type Page, type Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  static readonly PATH = '/portfolio';

  // --- Locators (defined once) ---
  readonly pageTitle: Locator;
  readonly healthScoreWidget: Locator;
  readonly healthScoreValue: Locator;
  readonly positionsTable: Locator;
  readonly positionRows: Locator;
  readonly syncButton: Locator;
  readonly positionsSearch: Locator;

  constructor(page: Page) {
    super(page);

    // Use multiple strategies for robust locators
    this.pageTitle = page.getByRole('heading', { name: /portfolio|dashboard/i });

    this.healthScoreWidget = page.locator(
      '[data-testid="health-score-widget"], [class*="health-score"]'
    ).first();

    this.healthScoreValue = page.locator(
      '[data-testid="health-score-value"], [class*="score-value"]'
    ).first();

    this.positionsTable = page.locator(
      '[data-testid="positions-table"], table:has(th:text("Ticker"))'
    ).first();

    this.positionRows = page.locator('[data-testid="position-row"], tbody tr');

    this.syncButton = page.getByRole('button', { name: /sync|refresh|update/i });

    this.positionsSearch = page.getByPlaceholder(/search.*position/i);
  }

  // --- Navigation ---

  async goto() {
    await super.goto(DashboardPage.PATH, { waitUntil: 'networkidle' });
    await this.waitForDashboardLoad();
  }

  async waitForDashboardLoad() {
    await this.assertVisible(this.pageTitle, { timeout: 10000 });
    await this.waitForSpinnersToDisappear();
  }

  // --- Health Score ---

  async getHealthScore(): Promise<number | null> {
    await this.assertVisible(this.healthScoreValue);
    const text = await this.healthScoreValue.textContent();
    if (!text) return null;

    const match = text.match(/(\d+)/);
    return match ? parseInt(match[1], 10) : null;
  }

  async assertHealthScoreInRange(min: number, max: number) {
    const score = await this.getHealthScore();
    if (score === null) throw new Error('Health score not found');
    if (score < min || score > max) {
      throw new Error(`Health score ${score} not in range [${min}, ${max}]`);
    }
  }

  // --- Positions ---

  async getPositionCount(): Promise<number> {
    await this.assertVisible(this.positionsTable);
    return this.positionRows.count();
  }

  async getPositionTickers(): Promise<string[]> {
    await this.assertVisible(this.positionsTable);
    const rows = await this.positionRows.all();
    const tickers: string[] = [];

    for (const row of rows) {
      const tickerCell = row.locator('td').first();
      const text = await tickerCell.textContent();
      if (text) tickers.push(text.trim());
    }

    return tickers;
  }

  async searchPositions(query: string) {
    await this.positionsSearch.fill(query);
    // Wait for debounce
    await this.page.waitForTimeout(500);
  }

  async clickPosition(ticker: string) {
    const row = this.page.locator(`tr:has-text("${ticker}")`).first();
    await row.click();
    await this.waitForNavigation();
  }

  // --- Actions ---

  async triggerSync() {
    await this.syncButton.click();
    await this.waitForSpinnersToDisappear();
  }
}
```

---

## Locator Strategies

### Priority Order (Playwright Recommended)

1. **`getByRole()`** — ARIA roles (best for accessibility)
2. **`getByLabel()`** — Form labels
3. **`getByPlaceholder()`** — Input placeholders
4. **`getByText()`** — Visible text content
5. **`getByTestId()`** — Last resort with `data-testid`

### Examples

```typescript
// ✅ BEST: Role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { name: /dashboard/i })
page.getByRole('link', { name: 'Settings' })

// ✅ GOOD: Label-based (accessible)
page.getByLabel('Email')
page.getByLabel(/password/i)

// ✅ OK: Text-based
page.getByText('Sign in')
page.getByText(/loading/i)

// ⚠️ FALLBACK: Test ID (when above don't work)
page.getByTestId('health-score')

// ❌ AVOID: CSS selectors (fragile)
page.locator('.btn-primary')
page.locator('#submit-button')
```

### Robust Multi-Strategy Locators

```typescript
// Use comma-separated selectors for fallback
const button = page.locator(
  'button[data-testid="submit"], button:text("Submit"), [type="submit"]'
).first();

// Or use .or() for explicit fallback
const healthScore = page
  .getByTestId('health-score')
  .or(page.locator('[class*="health-score"]'))
  .first();
```

---

## Fixtures Integration

Use Playwright fixtures to inject Page Objects:

```typescript
// e2e/fixtures/pages.ts
import { test as base } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';
import { SettingsPage } from '../pages/SettingsPage';

type PageFixtures = {
  dashboardPage: DashboardPage;
  settingsPage: SettingsPage;
};

export const test = base.extend<PageFixtures>({
  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  settingsPage: async ({ page }, use) => {
    const settingsPage = new SettingsPage(page);
    await use(settingsPage);
  },
});

export { expect } from '@playwright/test';
```

### Usage in Tests

```typescript
// e2e/tests/dashboard.spec.ts
import { test, expect } from '../fixtures/pages';

test.describe('Dashboard', () => {
  test('displays health score in valid range', async ({ dashboardPage }) => {
    await dashboardPage.goto();

    const score = await dashboardPage.getHealthScore();
    expect(score).toBeGreaterThanOrEqual(0);
    expect(score).toBeLessThanOrEqual(100);
  });

  test('shows all seeded positions', async ({ dashboardPage }) => {
    await dashboardPage.goto();

    const tickers = await dashboardPage.getPositionTickers();
    expect(tickers).toContain('AAPL');
    expect(tickers).toContain('NVDA');
  });

  test('has no console errors', async ({ dashboardPage }) => {
    await dashboardPage.goto();

    const errors = dashboardPage.getUnexpectedErrors();
    expect(errors).toHaveLength(0);
  });
});
```

---

## Anti-Patterns

### DON'T: Logic in Tests

```typescript
// ❌ BAD: Test knows implementation
test('login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="submit"]');
  await page.waitForURL('/dashboard');
});

// ✅ GOOD: Test expresses intent
test('login', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto();
  await loginPage.login('test@example.com', 'password123');
  await dashboardPage.assertVisible(dashboardPage.pageTitle);
});
```

### DON'T: Hardcoded Waits

```typescript
// ❌ BAD: Arbitrary wait
await page.waitForTimeout(3000);

// ✅ GOOD: Wait for specific condition
await page.waitForLoadState('networkidle');
await dashboardPage.waitForSpinnersToDisappear();
await expect(dashboardPage.healthScoreWidget).toBeVisible();
```

### DON'T: Duplicate Locators

```typescript
// ❌ BAD: Same locator in multiple tests
test('test 1', async ({ page }) => {
  await page.click('[data-testid="submit"]');
});
test('test 2', async ({ page }) => {
  await page.click('[data-testid="submit"]');  // Duplicated!
});

// ✅ GOOD: Define once in Page Object
class FormPage extends BasePage {
  readonly submitButton = this.page.getByTestId('submit');

  async submit() {
    await this.submitButton.click();
  }
}
```

### DON'T: JavaScript Injection

```typescript
// ❌ BAD: Direct DOM manipulation
await page.evaluate(() => {
  document.querySelector('button').click();
});

// ✅ GOOD: Playwright's realistic actions
await page.getByRole('button', { name: 'Submit' }).click();
```

---

## Page Object Inventory Template

| Page Object | File | Path | Key Methods |
|-------------|------|------|-------------|
| `BasePage` | `BasePage.ts` | - | `goto()`, `screenshot()`, `getConsoleErrors()` |
| `DashboardPage` | `DashboardPage.ts` | `/portfolio` | `getHealthScore()`, `getPositions()` |
| `SettingsPage` | `SettingsPage.ts` | `/settings` | `updateProfile()`, `changePlan()` |
| `PricingPage` | `PricingPage.ts` | `/pricing` | `selectPlan()`, `getPrices()` |
| `OnboardingWizard` | `OnboardingWizard.ts` | `/onboarding` | `completeStep()`, `skipOnboarding()` |
| `LoginPage` | `LoginPage.ts` | `/login` | `login()`, `assertError()` |
