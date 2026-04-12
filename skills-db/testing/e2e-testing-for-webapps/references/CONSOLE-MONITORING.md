# Console Error Monitoring

## Table of Contents
- [Why Monitor Console?](#why-monitor-console)
- [ConsoleMonitor Class](#consolemonitor-class)
- [Error Categories](#error-categories)
- [Usage Patterns](#usage-patterns)
- [Filtering Known Issues](#filtering-known-issues)
- [Integration with Tests](#integration-with-tests)

---

## Why Monitor Console?

Many bugs don't cause test failures but **log errors to the browser console**:

| Issue Type | Visible in UI? | In Console? | Test Fails? |
|------------|----------------|-------------|-------------|
| React hydration mismatch | Sometimes | Yes | No |
| Failed API call (with fallback) | No | Yes | No |
| JavaScript TypeError | No | Yes | No |
| CSP violation | No | Yes | No |
| Network timeout | Maybe | Yes | No |

**Console monitoring catches invisible bugs that slip past traditional assertions.**

---

## ConsoleMonitor Class

```typescript
// e2e/utils/console-monitor.ts
import { type Page, type ConsoleMessage as PWConsoleMessage } from '@playwright/test';

export type ConsoleLevel = 'error' | 'warning' | 'info' | 'log' | 'debug' | 'trace';

export type ConsoleCategory =
  | 'runtime'      // TypeError, ReferenceError, etc.
  | 'network'      // Failed fetch, CORS errors
  | 'react'        // React warnings
  | 'security'     // CSP violations
  | 'hydration'    // SSR/client mismatch
  | 'deprecation'  // Deprecated API warnings
  | 'other';

export interface ConsoleMessage {
  level: ConsoleLevel;
  text: string;
  category: ConsoleCategory;
  url?: string;
  lineNumber?: number;
  timestamp: number;
}

export class ConsoleMonitor {
  private page: Page;
  private messages: ConsoleMessage[] = [];

  constructor(page: Page) {
    this.page = page;
    this.attach();
  }

  /**
   * Attach listener to page console events.
   * Called automatically in constructor.
   */
  attach(): void {
    this.page.on('console', (msg) => this.handleConsoleMessage(msg));
  }

  private handleConsoleMessage(msg: PWConsoleMessage): void {
    const level = msg.type() as ConsoleLevel;
    const text = msg.text();
    const location = msg.location();

    this.messages.push({
      level,
      text,
      category: this.categorize(text),
      url: location.url,
      lineNumber: location.lineNumber,
      timestamp: Date.now(),
    });
  }

  /**
   * Categorize message based on content patterns.
   */
  private categorize(text: string): ConsoleCategory {
    const lowerText = text.toLowerCase();

    // Hydration errors (highest priority - serious issue)
    if (/hydrat|server.*different.*client|content.*mismatch|text content does not match/i.test(text)) {
      return 'hydration';
    }

    // React-specific warnings
    if (/^warning:\s|react|hook|useeffect|usestate|setstate.*unmounted/i.test(text)) {
      return 'react';
    }

    // Network errors
    if (/net::err|failed to (load|fetch)|cors|fetch.*failed|timeout|aborted/i.test(text)) {
      return 'network';
    }

    // Security errors
    if (/csp|content security policy|refused to|blocked by cors|unsafe-eval/i.test(text)) {
      return 'security';
    }

    // Runtime JavaScript errors
    if (/typeerror|referenceerror|syntaxerror|rangeerror|uncaught|error:/i.test(text)) {
      return 'runtime';
    }

    // Deprecation warnings
    if (/deprecat|will be removed|no longer supported/i.test(text)) {
      return 'deprecation';
    }

    return 'other';
  }

  /**
   * Get all captured messages.
   */
  getAll(): ConsoleMessage[] {
    return [...this.messages];
  }

  /**
   * Get errors only (level === 'error').
   */
  getErrors(category?: ConsoleCategory): ConsoleMessage[] {
    return this.messages.filter((msg) => {
      if (msg.level !== 'error') return false;
      if (category && msg.category !== category) return false;
      return true;
    });
  }

  /**
   * Get warnings only (level === 'warning').
   */
  getWarnings(category?: ConsoleCategory): ConsoleMessage[] {
    return this.messages.filter((msg) => {
      if (msg.level !== 'warning') return false;
      if (category && msg.category !== category) return false;
      return true;
    });
  }

  /**
   * Get errors excluding known safe patterns.
   */
  getUnexpectedErrors(): ConsoleMessage[] {
    const KNOWN_SAFE_PATTERNS = [
      /download the react devtools/i,
      /fast refresh/i,
      /chrome-extension/i,
      /gtag/i,
      /google.*analytics/i,
      /facebook.*pixel/i,
      /hotjar/i,
      /intercom/i,
      /sentry/i,
      /posthog/i,
    ];

    return this.getErrors().filter((msg) =>
      !KNOWN_SAFE_PATTERNS.some((pattern) => pattern.test(msg.text))
    );
  }

  /**
   * Get summary by category.
   */
  getSummary(): Record<ConsoleCategory, { errors: number; warnings: number }> {
    const summary: Record<ConsoleCategory, { errors: number; warnings: number }> = {
      runtime: { errors: 0, warnings: 0 },
      network: { errors: 0, warnings: 0 },
      react: { errors: 0, warnings: 0 },
      security: { errors: 0, warnings: 0 },
      hydration: { errors: 0, warnings: 0 },
      deprecation: { errors: 0, warnings: 0 },
      other: { errors: 0, warnings: 0 },
    };

    for (const msg of this.messages) {
      if (msg.level === 'error') {
        summary[msg.category].errors++;
      } else if (msg.level === 'warning') {
        summary[msg.category].warnings++;
      }
    }

    return summary;
  }

  /**
   * Print all messages for debugging.
   */
  printAll(): void {
    console.log('\n=== Console Messages ===');
    for (const msg of this.messages) {
      const icon = msg.level === 'error' ? '❌' : msg.level === 'warning' ? '⚠️' : 'ℹ️';
      console.log(`${icon} [${msg.category}] ${msg.text.slice(0, 100)}`);
    }
    console.log('========================\n');
  }

  /**
   * Clear captured messages.
   */
  clear(): void {
    this.messages = [];
  }
}
```

---

## Error Categories

| Category | Patterns | Severity | Action |
|----------|----------|----------|--------|
| `hydration` | `hydrat`, `server.*different.*client` | **Critical** | Fix SSR mismatch immediately |
| `runtime` | `TypeError`, `ReferenceError`, `Uncaught` | **High** | Fix JavaScript error |
| `network` | `net::ERR`, `fetch.*failed`, `CORS` | **Medium** | Check API/CORS config |
| `react` | `Warning:`, `useEffect`, `setState unmounted` | **Medium** | Fix hook issue |
| `security` | `CSP`, `Refused to` | **Medium** | Update CSP policy |
| `deprecation` | `deprecated`, `will be removed` | **Low** | Plan migration |
| `other` | Everything else | **Low** | Investigate if frequent |

### Hydration Errors

Most serious—indicate SSR/client mismatch:

```
Warning: Text content does not match. Server: "123" Client: "456"
Warning: Expected server HTML to contain a matching <div> in <body>.
Hydration failed because the initial UI does not match what was rendered on the server.
```

**Common causes:**
- Date/time formatting differences
- Random values generated on both server and client
- Browser-specific APIs used during SSR
- Conditional rendering based on `window`

### React Warnings

```
Warning: Can't perform a React state update on an unmounted component.
Warning: Each child in a list should have a unique "key" prop.
Warning: You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() before.
```

### Network Errors

```
net::ERR_CONNECTION_REFUSED
net::ERR_NAME_NOT_RESOLVED
Failed to fetch
CORS error: No 'Access-Control-Allow-Origin' header
```

---

## Usage Patterns

### In Page Objects

```typescript
// e2e/pages/BasePage.ts
export class BasePage {
  protected consoleMonitor: ConsoleMonitor;

  constructor(page: Page) {
    this.consoleMonitor = new ConsoleMonitor(page);
  }

  getConsoleErrors(category?: ConsoleCategory): ConsoleMessage[] {
    return this.consoleMonitor.getErrors(category);
  }

  getUnexpectedErrors(): ConsoleMessage[] {
    return this.consoleMonitor.getUnexpectedErrors();
  }

  hasHydrationErrors(): boolean {
    return this.consoleMonitor.getErrors('hydration').length > 0;
  }
}
```

### In Tests

```typescript
test('dashboard has no console errors', async ({ dashboardPage }) => {
  await dashboardPage.goto();
  await dashboardPage.waitForDashboardLoad();

  // Check for unexpected errors
  const errors = dashboardPage.getUnexpectedErrors();

  // Debug output if errors found
  if (errors.length > 0) {
    dashboardPage.consoleMonitor.printAll();
  }

  expect(errors).toHaveLength(0);
});

test('no hydration mismatches', async ({ dashboardPage }) => {
  await dashboardPage.goto();

  const hydrationErrors = dashboardPage.getConsoleErrors('hydration');
  expect(hydrationErrors).toHaveLength(0);
});

test('network requests succeed', async ({ dashboardPage }) => {
  await dashboardPage.goto();

  const networkErrors = dashboardPage.getConsoleErrors('network');
  expect(networkErrors).toHaveLength(0);
});
```

### Assertion Helpers

```typescript
// e2e/utils/assertions.ts
import { expect } from '@playwright/test';
import type { ConsoleMonitor } from './console-monitor';

export function assertNoConsoleErrors(
  monitor: ConsoleMonitor,
  options?: {
    ignoreCategories?: ConsoleCategory[];
    ignorePatterns?: RegExp[];
  }
) {
  const errors = monitor.getErrors();

  const filtered = errors.filter((error) => {
    // Ignore specified categories
    if (options?.ignoreCategories?.includes(error.category)) {
      return false;
    }

    // Ignore matching patterns
    if (options?.ignorePatterns?.some((p) => p.test(error.text))) {
      return false;
    }

    return true;
  });

  if (filtered.length > 0) {
    console.error('Console errors found:');
    filtered.forEach((e) => console.error(`  [${e.category}] ${e.text}`));
  }

  expect(filtered).toHaveLength(0);
}
```

---

## Filtering Known Issues

### Global Ignore List

```typescript
// e2e/utils/console-ignore.ts
export const GLOBAL_IGNORE_PATTERNS = [
  // Browser extensions
  /chrome-extension/i,
  /moz-extension/i,

  // Analytics (expected noise)
  /gtag|google.*analytics|ga\(/i,
  /facebook.*pixel/i,
  /hotjar/i,

  // Development tools
  /download the react devtools/i,
  /fast refresh/i,

  // Third-party services
  /intercom/i,
  /sentry/i,
  /posthog/i,

  // Known non-issues
  /ResizeObserver loop/i,  // Browser quirk, not a bug
];
```

### Per-Test Ignore

```typescript
test('dashboard with known issues', async ({ dashboardPage }) => {
  await dashboardPage.goto();

  // This page has a known deprecation warning we're tracking
  const errors = dashboardPage.getUnexpectedErrors().filter(
    (e) => !e.text.includes('deprecated API xyz')
  );

  expect(errors).toHaveLength(0);
});
```

---

## Integration with Tests

### Fixture with Console Monitoring

```typescript
// e2e/fixtures/console.ts
import { test as base } from '@playwright/test';
import { ConsoleMonitor } from '../utils/console-monitor';

type ConsoleFixtures = {
  consoleMonitor: ConsoleMonitor;
  assertNoConsoleErrors: () => void;
};

export const test = base.extend<ConsoleFixtures>({
  consoleMonitor: async ({ page }, use) => {
    const monitor = new ConsoleMonitor(page);
    await use(monitor);
  },

  assertNoConsoleErrors: async ({ consoleMonitor }, use) => {
    const assert = () => {
      const errors = consoleMonitor.getUnexpectedErrors();
      if (errors.length > 0) {
        consoleMonitor.printAll();
        throw new Error(`Found ${errors.length} unexpected console errors`);
      }
    };

    await use(assert);
  },
});

export { expect } from '@playwright/test';
```

### Auto-Assert in afterEach

```typescript
// e2e/tests/dashboard.spec.ts
import { test, expect } from '../fixtures/console';

test.describe('Dashboard', () => {
  test.afterEach(async ({ consoleMonitor }) => {
    // Automatically check for errors after every test
    const errors = consoleMonitor.getUnexpectedErrors();
    if (errors.length > 0) {
      console.warn('Console errors in test:');
      consoleMonitor.printAll();
    }
    // Don't fail here—let specific tests decide
  });

  test('loads without errors', async ({ dashboardPage, assertNoConsoleErrors }) => {
    await dashboardPage.goto();
    assertNoConsoleErrors();
  });
});
```

### Reporting

```typescript
// Add to test report
test.afterEach(async ({ consoleMonitor }, testInfo) => {
  const summary = consoleMonitor.getSummary();

  testInfo.annotations.push({
    type: 'console-summary',
    description: JSON.stringify(summary),
  });

  // Attach full log on failure
  if (testInfo.status !== 'passed') {
    const allMessages = consoleMonitor.getAll();
    await testInfo.attach('console-log', {
      body: JSON.stringify(allMessages, null, 2),
      contentType: 'application/json',
    });
  }
});
```
