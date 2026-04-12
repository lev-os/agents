# Failure Mode Injection

Chaos testing for frontend applications — systematically inject network failures, input stress, rapid interactions, and state corruption to verify the app degrades gracefully instead of breaking silently. Uses pure Playwright (`page.route()`, `page.evaluate()`) with zero external dependencies.

> **Key insight:** Happy-path testing covers ~5% of real-world conditions. The bugs that destroy user trust — blank pages after API errors, lost form data on timeout, silent failures after auth expiry, duplicate submissions on double-click — only surface when things go wrong. This engine breaks things on purpose so you can verify they break gracefully.

## Table of Contents
- [Network Dependency Discovery](#network-dependency-discovery)
- [Network Failure Injection](#network-failure-injection)
- [Input Stress Testing](#input-stress-testing)
- [Rapid Interaction Testing](#rapid-interaction-testing)
- [State Corruption Injection](#state-corruption-injection)
- [Failure Resilience Audit](#failure-resilience-audit)
- [Failure Resilience Scorecard](#failure-resilience-scorecard)
- [Integration](#integration)
- [Common Recipes](#common-recipes)
- [Graceful Degradation Reference](#graceful-degradation-reference)

---

## Network Dependency Discovery

Before injecting failures, discover what network requests the page actually makes. This records all fetch/XHR traffic during a user flow and returns a dependency map you can target for injection.

### The Function

```javascript
async function discoverNetworkDependencies(page, interactionFn) {
  const requests = [];

  const handler = (request) => {
    const url = request.url();
    // Skip static assets and browser internals
    if (/\.(js|css|png|jpg|jpeg|gif|svg|woff2?|ttf|ico)(\?|$)/.test(url)) return;
    if (url.startsWith('data:') || url.startsWith('chrome-extension:')) return;

    requests.push({
      url,
      method: request.method(),
      resourceType: request.resourceType(),
      timestamp: Date.now(),
    });
  };

  page.on('request', handler);

  try {
    // Run the user flow that triggers network requests
    await interactionFn(page);
    // Brief settle time for any trailing requests
    await page.waitForTimeout(1000);
  } finally {
    page.removeListener('request', handler);
  }

  // Deduplicate by URL+method, keep first occurrence
  const seen = new Set();
  const unique = [];
  for (const req of requests) {
    const key = req.method + ' ' + req.url;
    if (seen.has(key)) continue;
    seen.add(key);
    unique.push(req);
  }

  // Derive URL patterns for route matching
  const dependencies = unique.map(req => {
    const parsed = new URL(req.url);
    return {
      url: req.url,
      method: req.method,
      resourceType: req.resourceType,
      // Pattern for page.route() — matches this specific API path
      pattern: '**' + parsed.pathname + (parsed.search ? parsed.search : ''),
      // Broader pattern — matches any request to this path
      pathPattern: '**' + parsed.pathname,
    };
  });

  console.log(`Discovered ${dependencies.length} network dependencies:`);
  for (const dep of dependencies) {
    console.log(`  ${dep.method} ${dep.url}`);
  }

  return dependencies;
}
```

### Usage

```javascript
// Discover all API calls made during page load
const deps = await discoverNetworkDependencies(page, async (p) => {
  await p.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
});

// Discover all API calls made during a specific user flow
const flowDeps = await discoverNetworkDependencies(page, async (p) => {
  await p.goto('http://127.0.0.1:3000/settings');
  await p.getByRole('button', { name: 'Save' }).click();
  await p.waitForLoadState('networkidle');
});

// Output:
// Discovered 3 network dependencies:
//   GET https://api.example.com/v1/user/profile
//   GET https://api.example.com/v1/dashboard/data
//   POST https://api.example.com/v1/analytics/event
```

---

## Network Failure Injection

Intercept matching network requests and inject controlled failures using `page.route()`. This is pure Playwright — no external tools or libraries needed.

### Failure Modes

| Mode | What It Does | Simulates |
|------|-------------|-----------|
| `abort` | Immediately kills the request (`net::ERR_FAILED`) | Network down, DNS failure, CORS block |
| `timeout` | Delays response, then aborts | Slow/hung server, CDN timeout |
| `status` | Returns specified HTTP status code with empty body | Server errors (500, 503), auth failures (401, 403), rate limits (429) |
| `empty` | Returns 200 with empty JSON body `{}` | API returns no data, missing fields |
| `malformed` | Returns 200 with invalid JSON | Corrupt response, proxy mangling, encoding error |
| `slow` | Adds configurable latency before forwarding real response | Slow API, congested network, 3G connection |
| `partial` | Returns truncated JSON response | Connection dropped mid-transfer |

### The Function

```javascript
async function injectNetworkFailure(page, urlPattern, mode, options = {}) {
  const {
    status = 500,
    delay = 10000,
    body = null,
    contentType = 'application/json',
    count = Infinity,   // How many requests to intercept (then stop)
    log = true,
  } = options;

  let intercepted = 0;

  const handler = async (route) => {
    intercepted++;
    const request = route.request();
    if (log) {
      console.log(`[INJECT] ${mode} → ${request.method()} ${request.url()} (#${intercepted})`);
    }

    if (count !== Infinity && intercepted > count) {
      // Stop intercepting after N requests
      await route.continue();
      return;
    }

    switch (mode) {
      case 'abort':
        await route.abort('failed');
        break;

      case 'timeout':
        // Delay then abort — simulates a hung server
        await new Promise(r => setTimeout(r, delay));
        await route.abort('timedout');
        break;

      case 'status':
        await route.fulfill({
          status,
          contentType,
          body: body ?? JSON.stringify({ error: `Injected ${status} error`, status }),
        });
        break;

      case 'empty':
        await route.fulfill({
          status: 200,
          contentType,
          body: body ?? '{}',
        });
        break;

      case 'malformed':
        await route.fulfill({
          status: 200,
          contentType,
          body: body ?? '{"data": [{"id": 1, "name": "trunca',
        });
        break;

      case 'slow':
        // Forward real response but with added latency
        await new Promise(r => setTimeout(r, delay));
        await route.continue();
        break;

      case 'partial':
        // Fetch real response, then truncate it
        try {
          const response = await route.fetch();
          const realBody = await response.text();
          const truncated = realBody.slice(0, Math.max(10, Math.floor(realBody.length / 3)));
          await route.fulfill({
            status: 200,
            contentType,
            body: truncated,
          });
        } catch {
          await route.fulfill({
            status: 200,
            contentType,
            body: '{"dat',
          });
        }
        break;

      default:
        console.warn(`Unknown injection mode: ${mode}`);
        await route.continue();
    }
  };

  await page.route(urlPattern, handler);

  // Return an uninstall function
  return {
    interceptedCount: () => intercepted,
    remove: async () => {
      await page.unroute(urlPattern, handler);
      if (log) console.log(`[INJECT] Removed ${mode} injection for ${urlPattern} (intercepted ${intercepted} requests)`);
    },
  };
}
```

### Usage

```javascript
// Block all API calls (nuclear option — see what happens when everything fails)
const injection = await injectNetworkFailure(page, '**/api/**', 'abort');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.screenshot({ path: '/tmp/all-apis-down.png' });
await injection.remove();

// Return 500 for a specific endpoint
const injection = await injectNetworkFailure(page, '**/api/v1/dashboard/data', 'status', { status: 500 });
await page.reload({ waitUntil: 'domcontentloaded' });
// Check: does the page show an error message? Or go blank?
await injection.remove();

// Simulate 3G latency on all API calls
const injection = await injectNetworkFailure(page, '**/api/**', 'slow', { delay: 3000 });
await page.reload({ waitUntil: 'domcontentloaded' });
// Check: are loading states shown? Does the UI remain interactive?
await injection.remove();

// Inject failure only for the first request (test retry logic)
const injection = await injectNetworkFailure(page, '**/api/v1/save', 'status', {
  status: 503,
  count: 1,  // First request fails, subsequent ones succeed
});
await page.getByRole('button', { name: 'Save' }).click();
// Check: does the app retry? Show an error with retry button?
await injection.remove();
```

### Per-Endpoint Injection (Systematic)

```javascript
// Discover dependencies, then test each one
const deps = await discoverNetworkDependencies(page, async (p) => {
  await p.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
});

const results = [];
for (const dep of deps) {
  for (const mode of ['abort', 'status', 'empty']) {
    const injection = await injectNetworkFailure(page, dep.pathPattern, mode, {
      status: 500,
      log: false,
    });

    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);

    // Capture evidence
    const screenshot = `/tmp/inject-${dep.method}-${new URL(dep.url).pathname.replace(/\//g, '_')}-${mode}.png`;
    await page.screenshot({ path: screenshot });

    const consoleErrors = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });

    // Check for signs of bad failure handling
    const pageContent = await page.content();
    const hasBlankBody = pageContent.includes('<body></body>') ||
      (await page.evaluate(() => document.body.innerText.trim().length)) < 10;
    const hasUncaughtError = await page.evaluate(() =>
      document.body.innerText.includes('Unhandled') ||
      document.body.innerText.includes('undefined') ||
      document.body.innerText.includes('Cannot read prop')
    );

    results.push({
      endpoint: dep.url,
      method: dep.method,
      mode,
      screenshot,
      blankPage: hasBlankBody,
      uncaughtError: hasUncaughtError,
      consoleErrors: consoleErrors.length,
      severity: hasBlankBody ? 'critical' : hasUncaughtError ? 'major' : 'ok',
    });

    await injection.remove();
  }
}

// Report
for (const r of results) {
  const icon = r.severity === 'critical' ? 'CRIT' : r.severity === 'major' ? 'MAJOR' : 'OK';
  console.log(`  [${icon}] ${r.method} ${new URL(r.endpoint).pathname} → ${r.mode}: ${r.severity}`);
}
```

---

## Input Stress Testing

Fill form inputs with adversarial content to verify the UI handles boundary conditions — overflow text, Unicode edge cases, injection payloads, and paste bombs.

### Stress Vectors

```javascript
const INPUT_STRESS_VECTORS = {
  // ── Length boundaries ──
  empty: '',
  single: 'A',
  maxLength: 'A'.repeat(10000),
  pasteBomb: 'A'.repeat(50000),

  // ── Unicode edge cases ──
  unicode: '\u{1F4A9}\u{1F600}\u{1F923}\u{2764}\u{FE0F}\u{1F525}\u{1F60D}\u{1F389}', // emoji
  rtl: '\u{202E}This text is reversed\u{202C}', // right-to-left override
  zalgo: 'T\u0336\u0359\u0325h\u0354\u0324\u034Ei\u0334\u0356\u0344s\u0337\u0347\u0340 i\u0335\u034E\u0340s\u0336\u0327\u0344 Z\u0337\u0340\u0356a\u0334\u0325\u0353l\u0334\u0355\u0344g\u0335\u0347\u0352o\u0336\u0322',
  cjk: '\u4F60\u597D\u4E16\u754C\uFF01\u3053\u3093\u306B\u3061\u306F\u4E16\u754C\uFF01\uC548\uB155\uD558\uC138\uC694 \uC138\uACC4!', // Chinese + Japanese + Korean
  mathSymbols: '\u00BD \u00BE \u221A\u03C0 \u2211\u222B \u2264\u2265 \u2260\u2248',
  nullByte: 'before\x00after',
  newlines: 'line1\nline2\rline3\r\nline4',
  tabs: 'col1\tcol2\tcol3\tcol4',

  // ── Injection payloads (verify they're displayed, not executed) ──
  xssScript: '<script>alert("xss")</script>',
  xssImg: '<img src=x onerror=alert(1)>',
  xssEvent: '" onmouseover="alert(1)" data-x="',
  sqlInjection: "' OR '1'='1'; DROP TABLE users; --",
  templateLiteral: '${process.env.SECRET}',
  htmlEntities: '&lt;b&gt;bold&lt;/b&gt; &amp; &quot;quoted&quot;',

  // ── Whitespace and invisible characters ──
  onlySpaces: '     ',
  leadingTrailingSpaces: '  hello  ',
  zeroWidthSpace: 'hello\u200Bworld',
  nonBreakingSpace: 'hello\u00A0world',
};
```

### The Function

```javascript
async function inputStressTest(page, selector, options = {}) {
  const {
    vectors = INPUT_STRESS_VECTORS,
    screenshotDir = '/tmp/stress',
    checkConsoleErrors = true,
  } = options;

  const results = [];
  const input = page.locator(selector);

  if (!(await input.isVisible())) {
    return { error: `Input not visible: ${selector}`, results: [] };
  }

  for (const [name, value] of Object.entries(vectors)) {
    // Clear and fill
    await input.clear();
    try {
      await input.fill(value);
    } catch (fillError) {
      // Some inputs reject certain content — that's acceptable
      results.push({
        vector: name,
        value: value.slice(0, 50) + (value.length > 50 ? '...' : ''),
        result: 'rejected',
        severity: 'ok',
        detail: `Input rejected value: ${fillError.message.slice(0, 100)}`,
      });
      continue;
    }

    // Brief settle
    await page.waitForTimeout(100);

    // Check for layout damage
    const layoutDamage = await page.evaluate((sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;

      const rect = el.getBoundingClientRect();
      const parent = el.parentElement;
      const parentRect = parent ? parent.getBoundingClientRect() : null;

      return {
        inputWidth: Math.round(rect.width),
        inputHeight: Math.round(rect.height),
        overflowsParent: parentRect ? rect.right > parentRect.right + 5 || rect.bottom > parentRect.bottom + 50 : false,
        pageHorizontalScroll: document.documentElement.scrollWidth > window.innerWidth + 2,
      };
    }, selector);

    // Check for console errors
    const errors = [];
    if (checkConsoleErrors) {
      const errorHandler = (msg) => { if (msg.type() === 'error') errors.push(msg.text()); };
      page.on('console', errorHandler);
      await page.waitForTimeout(200);
      page.removeListener('console', errorHandler);
    }

    // Check for XSS execution (if this was an injection payload)
    let xssExecuted = false;
    if (name.startsWith('xss') || name.startsWith('sql') || name.startsWith('template')) {
      xssExecuted = await page.evaluate(() => {
        // Check if an alert dialog was triggered (it would be caught by Playwright)
        // Check for injected elements
        return document.querySelectorAll('img[src="x"]').length > 0 ||
               document.querySelectorAll('script:not([src])').length > 1; // More than the app's own scripts
      });
    }

    // Determine severity
    let severity = 'ok';
    let detail = 'Input handled correctly';

    if (xssExecuted) {
      severity = 'critical';
      detail = 'XSS payload was executed — input is not sanitized';
    } else if (layoutDamage?.pageHorizontalScroll) {
      severity = 'major';
      detail = `Input caused page-level horizontal scroll (${name}: "${value.slice(0, 30)}...")`;
    } else if (layoutDamage?.overflowsParent) {
      severity = 'major';
      detail = 'Input overflows its parent container';
    } else if (errors.length > 0) {
      severity = 'warning';
      detail = `Console errors: ${errors[0].slice(0, 100)}`;
    }

    // Screenshot if issue found
    let screenshot = null;
    if (severity !== 'ok') {
      screenshot = `${screenshotDir}/${name}.png`;
      await page.screenshot({ path: screenshot });
    }

    results.push({
      vector: name,
      value: value.slice(0, 50) + (value.length > 50 ? `... (${value.length} chars)` : ''),
      result: severity === 'ok' ? 'handled' : 'issue',
      severity,
      detail,
      screenshot,
    });
  }

  // Clear input after testing
  await input.clear();

  // Summary
  const issues = results.filter(r => r.severity !== 'ok');
  console.log(`Input stress test on ${selector}: ${results.length} vectors, ${issues.length} issues`);
  for (const issue of issues) {
    console.log(`  [${issue.severity.toUpperCase()}] ${issue.vector}: ${issue.detail}`);
  }

  return { selector, results, issueCount: issues.length };
}
```

### Usage

```javascript
// Test a specific input with all vectors
const results = await inputStressTest(page, '#email-input');

// Test with only length vectors
const lengthResults = await inputStressTest(page, '#name-input', {
  vectors: {
    empty: INPUT_STRESS_VECTORS.empty,
    maxLength: INPUT_STRESS_VECTORS.maxLength,
    pasteBomb: INPUT_STRESS_VECTORS.pasteBomb,
  },
});

// Test all visible inputs on the page
const inputs = await page.locator('input:visible, textarea:visible').all();
for (const input of inputs) {
  const id = await input.getAttribute('id') || await input.getAttribute('name') || 'unknown';
  const selector = (await input.getAttribute('id')) ? `#${await input.getAttribute('id')}` : `[name="${await input.getAttribute('name')}"]`;
  await inputStressTest(page, selector, { screenshotDir: `/tmp/stress/${id}` });
}
```

---

## Rapid Interaction Testing

Simulate rapid, repeated user interactions to detect duplicate submissions, race conditions, and missing disabled-state enforcement.

### The Function

```javascript
async function rapidInteractionTest(page, selector, options = {}) {
  const {
    action = 'click',
    count = 5,
    intervalMs = 50,
    screenshotDir = '/tmp/rapid',
  } = options;

  const el = page.locator(selector);
  if (!(await el.isVisible())) {
    return { error: `Element not visible: ${selector}`, results: [] };
  }

  // Record network requests triggered by rapid interaction
  const requests = [];
  const requestHandler = (request) => {
    if (request.resourceType() === 'fetch' || request.resourceType() === 'xhr') {
      requests.push({
        url: request.url(),
        method: request.method(),
        timestamp: Date.now(),
      });
    }
  };
  page.on('request', requestHandler);

  // Record console errors
  const errors = [];
  const errorHandler = (msg) => { if (msg.type() === 'error') errors.push(msg.text()); };
  page.on('console', errorHandler);

  // Perform rapid interactions
  const startTime = Date.now();
  for (let i = 0; i < count; i++) {
    try {
      switch (action) {
        case 'click':
          await el.click({ timeout: 2000 }).catch(() => {});
          break;
        case 'dblclick':
          await el.dblclick({ timeout: 2000 }).catch(() => {});
          break;
        case 'enter':
          await el.press('Enter', { timeout: 2000 }).catch(() => {});
          break;
      }
    } catch {
      // Element may become disabled/hidden — that's actually good
      break;
    }
    if (intervalMs > 0) await page.waitForTimeout(intervalMs);
  }

  // Wait for any in-flight requests to complete
  await page.waitForTimeout(2000);

  page.removeListener('request', requestHandler);
  page.removeListener('console', errorHandler);

  // Analyze results
  const screenshot = `${screenshotDir}/rapid-${action}-${count}x.png`;
  await page.screenshot({ path: screenshot });

  // Check for duplicate submissions
  const postRequests = requests.filter(r => r.method === 'POST' || r.method === 'PUT' || r.method === 'PATCH');
  const duplicateSubmissions = postRequests.length > 1;

  // Check if element was properly disabled after first interaction
  const isNowDisabled = await el.isDisabled().catch(() => true);
  const isNowHidden = !(await el.isVisible().catch(() => false));

  let severity = 'ok';
  let detail = 'Rapid interaction handled correctly';

  if (duplicateSubmissions) {
    severity = 'critical';
    detail = `${postRequests.length} duplicate submissions detected (${postRequests.map(r => r.method + ' ' + new URL(r.url).pathname).join(', ')})`;
  } else if (errors.length > 0) {
    severity = 'major';
    detail = `Console errors during rapid interaction: ${errors[0].slice(0, 100)}`;
  } else if (postRequests.length === 1 && !isNowDisabled && !isNowHidden) {
    severity = 'warning';
    detail = 'Button not disabled after submission — could lead to duplicates with slower networks';
  }

  const result = {
    selector,
    action,
    attemptedClicks: count,
    mutatingRequests: postRequests.length,
    consoleErrors: errors.length,
    elementDisabledAfter: isNowDisabled,
    elementHiddenAfter: isNowHidden,
    severity,
    detail,
    screenshot,
  };

  console.log(`Rapid ${action} test on ${selector}: [${severity.toUpperCase()}] ${detail}`);

  return result;
}
```

### Usage

```javascript
// Test submit button for double-click protection
await page.getByLabel('Email').fill('test@example.com');
const result = await rapidInteractionTest(page, 'button[type="submit"]', {
  action: 'click',
  count: 5,
  intervalMs: 30,
});
// severity: 'critical' if multiple POST requests were sent

// Test Enter key rapid-fire on a search input
await page.getByLabel('Search').fill('test query');
const result = await rapidInteractionTest(page, '[data-testid="search-input"]', {
  action: 'enter',
  count: 10,
  intervalMs: 20,
});
```

### What Graceful Handling Looks Like

| Behavior | Grade |
|----------|-------|
| Button disables after first click, only one request sent | OK |
| Button shows loading spinner, ignores subsequent clicks | OK |
| Multiple requests sent but server deduplicates (idempotency) | Warning (client should still prevent) |
| Multiple identical POST requests sent, no deduplication | Critical |
| Console errors or unhandled promise rejections | Major |
| Page goes blank or navigates away unexpectedly | Critical |

---

## State Corruption Injection

Simulate mid-flow session corruption — expired auth tokens, wiped localStorage, corrupted storage data. These conditions happen regularly in production (token expires while user is typing, browser clears storage, another tab logs out) but are almost never tested.

### The Function

```javascript
async function corruptSessionState(page, mode, options = {}) {
  const {
    log = true,
    waitAfter = 1000,
  } = options;

  if (log) console.log(`[CORRUPT] Injecting: ${mode}`);

  switch (mode) {
    case 'expire-auth': {
      // Clear all auth-related cookies
      const cookies = await page.context().cookies();
      const authCookies = cookies.filter(c =>
        /token|session|auth|sb-/i.test(c.name)
      );
      if (authCookies.length > 0) {
        // Clear by setting expired
        await page.context().clearCookies();
        // Re-add non-auth cookies
        const nonAuthCookies = cookies.filter(c =>
          !/token|session|auth|sb-/i.test(c.name)
        );
        if (nonAuthCookies.length > 0) {
          await page.context().addCookies(nonAuthCookies);
        }
        if (log) console.log(`[CORRUPT] Cleared ${authCookies.length} auth cookies`);
      }

      // Also clear auth from localStorage
      await page.evaluate(() => {
        const keys = Object.keys(localStorage);
        for (const key of keys) {
          if (/token|session|auth|sb-|supabase/i.test(key)) {
            localStorage.removeItem(key);
          }
        }
      });
      break;
    }

    case 'wipe-storage': {
      // Nuclear: clear everything
      await page.evaluate(() => {
        localStorage.clear();
        sessionStorage.clear();
      });
      if (log) console.log('[CORRUPT] Cleared localStorage + sessionStorage');
      break;
    }

    case 'corrupt-storage': {
      // Inject malformed JSON into storage keys
      await page.evaluate(() => {
        const keys = Object.keys(localStorage);
        for (const key of keys) {
          const val = localStorage.getItem(key);
          if (val && (val.startsWith('{') || val.startsWith('['))) {
            // Corrupt JSON by truncating it
            localStorage.setItem(key, val.slice(0, Math.max(5, Math.floor(val.length / 3))));
          }
        }
      });
      const corruptedCount = await page.evaluate(() => Object.keys(localStorage).length);
      if (log) console.log(`[CORRUPT] Corrupted JSON in ${corruptedCount} localStorage keys`);
      break;
    }

    case 'expire-token-header': {
      // Intercept all requests and inject an expired/invalid auth header
      await page.route('**/*', async (route) => {
        const headers = route.request().headers();
        if (headers['authorization']) {
          headers['authorization'] = 'Bearer expired_invalid_token_000';
        }
        await route.continue({ headers });
      });
      if (log) console.log('[CORRUPT] Intercepting requests with expired auth header');
      break;
    }

    case 'stale-version': {
      // Simulate app version mismatch (API expects newer client)
      await page.route('**/api/**', async (route) => {
        await route.fulfill({
          status: 426,
          contentType: 'application/json',
          body: JSON.stringify({
            error: 'Upgrade Required',
            message: 'Client version outdated. Please refresh the page.',
            minVersion: '99.0.0',
          }),
        });
      });
      if (log) console.log('[CORRUPT] All API requests return 426 Upgrade Required');
      break;
    }

    default:
      throw new Error(`Unknown corruption mode: ${mode}`);
  }

  // Wait for the corruption to take effect
  await page.waitForTimeout(waitAfter);
}
```

### Usage

```javascript
// Simulate auth expiry mid-flow
await page.goto('http://127.0.0.1:3000/settings');
await page.getByLabel('Display Name').fill('New Name');
// Now corrupt the session before saving
await corruptSessionState(page, 'expire-auth');
await page.getByRole('button', { name: 'Save' }).click();
// Check: does the app redirect to login? Show an error? Lose the form data?
await page.screenshot({ path: '/tmp/auth-expired-save.png' });

// Simulate corrupted localStorage
await page.goto('http://127.0.0.1:3000/dashboard');
await corruptSessionState(page, 'corrupt-storage');
await page.reload({ waitUntil: 'domcontentloaded' });
// Check: does the app crash? Show a recovery message? Silently re-fetch data?
await page.screenshot({ path: '/tmp/corrupt-storage.png' });
```

### Corruption Modes Reference

| Mode | What It Simulates | Expected Graceful Behavior |
|------|-------------------|---------------------------|
| `expire-auth` | Token expired, user logged out in another tab | Redirect to login, preserve intended destination, don't lose form data |
| `wipe-storage` | Browser cleared storage, incognito mode, storage quota exceeded | Re-fetch data from server, show login if auth lost, don't crash |
| `corrupt-storage` | Corrupt write, extension interference, storage migration bug | Parse errors caught, fallback to defaults, don't show raw JSON errors |
| `expire-token-header` | API rejects all authenticated requests | Show auth error, redirect to login, don't spin forever |
| `stale-version` | Deployed new API version, client is stale | Show "please refresh" message, don't show cryptic error |

---

## Failure Resilience Audit

The orchestrator that ties everything together. Runs a user flow cleanly first (baseline), then re-runs it under each failure condition, capturing evidence at each step.

### The Function

```javascript
async function failureResilienceAudit(page, flowFn, options = {}) {
  const {
    screenshotDir = '/tmp/resilience',
    injections = ['abort', 'status-500', 'empty', 'slow', 'expire-auth', 'corrupt-storage'],
    networkPatterns = null, // Auto-discovered if null
    skipInputStress = false,
    skipRapidInteraction = false,
    submitSelector = null,  // For rapid interaction test
    inputSelectors = [],    // For input stress test
  } = options;

  const results = {
    baseline: null,
    network: [],
    inputs: [],
    interactions: [],
    stateCorruption: [],
    scorecard: null,
  };

  // ── Step 1: Baseline run ──────────────────────────────
  console.log('=== BASELINE RUN ===');

  // Discover network dependencies during baseline
  let dependencies = [];
  if (networkPatterns) {
    dependencies = networkPatterns.map(p => ({ pathPattern: p, url: p, method: 'GET' }));
  }

  const baselineErrors = [];
  const baselineErrorHandler = (msg) => { if (msg.type() === 'error') baselineErrors.push(msg.text()); };
  page.on('console', baselineErrorHandler);

  if (!networkPatterns) {
    dependencies = await discoverNetworkDependencies(page, flowFn);
  } else {
    await flowFn(page);
  }

  page.removeListener('console', baselineErrorHandler);

  await page.screenshot({ path: `${screenshotDir}/baseline.png` });

  results.baseline = {
    screenshot: `${screenshotDir}/baseline.png`,
    consoleErrors: baselineErrors.length,
    networkDeps: dependencies.length,
    status: baselineErrors.length === 0 ? 'clean' : 'has-errors',
  };

  console.log(`Baseline: ${dependencies.length} network deps, ${baselineErrors.length} console errors`);

  // ── Step 2: Network failure injection ────────────────
  console.log('\n=== NETWORK FAILURE INJECTION ===');

  // Parse injection list into network modes and state modes
  const networkModes = injections.filter(i =>
    ['abort', 'timeout', 'empty', 'malformed', 'slow', 'partial'].includes(i) ||
    i.startsWith('status-')
  );
  const stateModes = injections.filter(i =>
    ['expire-auth', 'wipe-storage', 'corrupt-storage', 'expire-token-header', 'stale-version'].includes(i)
  );

  for (const dep of dependencies) {
    for (const mode of networkModes) {
      let actualMode = mode;
      let modeOptions = {};

      // Parse 'status-500' format
      if (mode.startsWith('status-')) {
        actualMode = 'status';
        modeOptions.status = parseInt(mode.split('-')[1], 10);
      }

      const injection = await injectNetworkFailure(page, dep.pathPattern, actualMode, {
        ...modeOptions,
        log: false,
      });

      try {
        await flowFn(page);
      } catch {
        // Flow may throw due to timeouts — that's expected
      }

      await page.waitForTimeout(1000);

      const screenshotPath = `${screenshotDir}/net-${new URL(dep.url).pathname.replace(/\//g, '_').slice(1)}-${mode}.png`;
      await page.screenshot({ path: screenshotPath });

      // Assess damage
      const assessment = await page.evaluate(() => {
        const bodyText = document.body.innerText.trim();
        return {
          bodyLength: bodyText.length,
          hasErrorMessage: /error|failed|try again|went wrong|unavailable/i.test(bodyText),
          hasBlankPage: bodyText.length < 20,
          hasRawError: /undefined|null|NaN|TypeError|Cannot read/i.test(bodyText),
          hasRetryOption: /retry|try again|reload|refresh/i.test(bodyText),
        };
      });

      let severity = 'ok';
      if (assessment.hasBlankPage) severity = 'critical';
      else if (assessment.hasRawError) severity = 'major';
      else if (!assessment.hasErrorMessage) severity = 'warning';

      results.network.push({
        endpoint: dep.url,
        method: dep.method,
        failureMode: mode,
        severity,
        assessment,
        screenshot: screenshotPath,
      });

      const icon = { critical: 'CRIT', major: 'MAJOR', warning: 'WARN', ok: 'OK' }[severity];
      console.log(`  [${icon}] ${dep.method} ${new URL(dep.url).pathname} → ${mode}`);

      await injection.remove();
    }
  }

  // ── Step 3: State corruption ─────────────────────────
  if (stateModes.length > 0) {
    console.log('\n=== STATE CORRUPTION ===');

    for (const mode of stateModes) {
      // Start fresh
      await flowFn(page);
      await page.waitForTimeout(500);

      await corruptSessionState(page, mode, { log: false });

      // Trigger an action that requires the corrupted state
      try {
        // Try to navigate or interact — this surfaces the corruption
        await page.reload({ waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);
      } catch {
        // May timeout — that's data
      }

      const screenshotPath = `${screenshotDir}/corrupt-${mode}.png`;
      await page.screenshot({ path: screenshotPath });

      const assessment = await page.evaluate(() => {
        const bodyText = document.body.innerText.trim();
        return {
          bodyLength: bodyText.length,
          hasErrorMessage: /error|failed|try again|went wrong|unavailable|sign in|log in/i.test(bodyText),
          hasBlankPage: bodyText.length < 20,
          hasRawError: /undefined|null|NaN|TypeError|Cannot read|SyntaxError|JSON/i.test(bodyText),
          hasLoginRedirect: /sign in|log in|login|authenticate/i.test(bodyText),
        };
      });

      let severity = 'ok';
      if (assessment.hasBlankPage) severity = 'critical';
      else if (assessment.hasRawError) severity = 'major';
      else if (!assessment.hasErrorMessage && !assessment.hasLoginRedirect) severity = 'warning';

      results.stateCorruption.push({
        mode,
        severity,
        assessment,
        screenshot: screenshotPath,
      });

      const icon = { critical: 'CRIT', major: 'MAJOR', warning: 'WARN', ok: 'OK' }[severity];
      console.log(`  [${icon}] ${mode}`);

      // Clean up route interceptions from certain modes
      if (mode === 'expire-token-header' || mode === 'stale-version') {
        await page.unroute('**/*');
      }
    }
  }

  // ── Step 4: Input stress ─────────────────────────────
  if (!skipInputStress && inputSelectors.length > 0) {
    console.log('\n=== INPUT STRESS ===');
    for (const sel of inputSelectors) {
      await flowFn(page); // Reset to clean state
      const stressResult = await inputStressTest(page, sel, {
        screenshotDir: `${screenshotDir}/input-stress`,
      });
      results.inputs.push(stressResult);
    }
  }

  // ── Step 5: Rapid interaction ────────────────────────
  if (!skipRapidInteraction && submitSelector) {
    console.log('\n=== RAPID INTERACTION ===');
    await flowFn(page); // Reset to clean state
    const rapidResult = await rapidInteractionTest(page, submitSelector, {
      screenshotDir: `${screenshotDir}/rapid`,
    });
    results.interactions.push(rapidResult);
  }

  // ── Step 6: Generate scorecard ───────────────────────
  results.scorecard = generateScorecard(results);
  console.log('\n' + formatScorecard(results.scorecard));

  return results;
}
```

---

## Failure Resilience Scorecard

A structured grade for each failure category, plus an overall resilience grade.

### Scorecard Generation

```javascript
function generateScorecard(results) {
  function worstSeverity(items) {
    if (items.some(i => i.severity === 'critical')) return 'critical';
    if (items.some(i => i.severity === 'major')) return 'major';
    if (items.some(i => i.severity === 'warning')) return 'warning';
    return 'ok';
  }

  function severityToScore(sev) {
    return { ok: 4, warning: 3, major: 1, critical: 0 }[sev] ?? 0;
  }

  function scoreToGrade(score) {
    if (score >= 3.5) return 'A';
    if (score >= 2.5) return 'B';
    if (score >= 1.5) return 'C';
    if (score >= 0.5) return 'D';
    return 'F';
  }

  const categories = {};

  // Network resilience
  if (results.network.length > 0) {
    const networkWorst = worstSeverity(results.network);
    const networkAvg = results.network.reduce((sum, r) => sum + severityToScore(r.severity), 0) / results.network.length;
    categories.network = {
      grade: scoreToGrade(networkAvg),
      worst: networkWorst,
      tested: results.network.length,
      critical: results.network.filter(r => r.severity === 'critical').length,
      major: results.network.filter(r => r.severity === 'major').length,
      warning: results.network.filter(r => r.severity === 'warning').length,
      ok: results.network.filter(r => r.severity === 'ok').length,
    };
  }

  // State corruption resilience
  if (results.stateCorruption.length > 0) {
    const stateWorst = worstSeverity(results.stateCorruption);
    const stateAvg = results.stateCorruption.reduce((sum, r) => sum + severityToScore(r.severity), 0) / results.stateCorruption.length;
    categories.stateCorruption = {
      grade: scoreToGrade(stateAvg),
      worst: stateWorst,
      tested: results.stateCorruption.length,
      critical: results.stateCorruption.filter(r => r.severity === 'critical').length,
      major: results.stateCorruption.filter(r => r.severity === 'major').length,
      warning: results.stateCorruption.filter(r => r.severity === 'warning').length,
      ok: results.stateCorruption.filter(r => r.severity === 'ok').length,
    };
  }

  // Input stress resilience
  if (results.inputs.length > 0) {
    const allInputResults = results.inputs.flatMap(r => r.results || []);
    const inputWorst = worstSeverity(allInputResults);
    const inputAvg = allInputResults.length > 0
      ? allInputResults.reduce((sum, r) => sum + severityToScore(r.severity), 0) / allInputResults.length
      : 4;
    categories.inputStress = {
      grade: scoreToGrade(inputAvg),
      worst: inputWorst,
      tested: allInputResults.length,
      critical: allInputResults.filter(r => r.severity === 'critical').length,
      major: allInputResults.filter(r => r.severity === 'major').length,
      warning: allInputResults.filter(r => r.severity === 'warning').length,
      ok: allInputResults.filter(r => r.severity === 'ok').length,
    };
  }

  // Rapid interaction resilience
  if (results.interactions.length > 0) {
    const interactionWorst = worstSeverity(results.interactions);
    categories.rapidInteraction = {
      grade: scoreToGrade(severityToScore(interactionWorst)),
      worst: interactionWorst,
      tested: results.interactions.length,
    };
  }

  // Overall grade: weighted average of category grades
  const allGrades = Object.values(categories).map(c => {
    return { A: 4, B: 3, C: 2, D: 1, F: 0 }[c.grade] ?? 0;
  });
  const overallScore = allGrades.length > 0
    ? allGrades.reduce((a, b) => a + b, 0) / allGrades.length
    : 0;

  return {
    overall: scoreToGrade(overallScore),
    categories,
    timestamp: new Date().toISOString(),
  };
}
```

### Scorecard Formatting

```javascript
function formatScorecard(scorecard) {
  const lines = [];
  lines.push('╔══════════════════════════════════════════════╗');
  lines.push(`║   FAILURE RESILIENCE SCORECARD: ${scorecard.overall}            ║`);
  lines.push('╠══════════════════════════════════════════════╣');

  for (const [name, cat] of Object.entries(scorecard.categories)) {
    const label = {
      network: 'Network Failures',
      stateCorruption: 'State Corruption',
      inputStress: 'Input Stress',
      rapidInteraction: 'Rapid Interaction',
    }[name] || name;

    const counts = [];
    if (cat.critical > 0) counts.push(`${cat.critical} critical`);
    if (cat.major > 0) counts.push(`${cat.major} major`);
    if (cat.warning > 0) counts.push(`${cat.warning} warning`);

    const detail = counts.length > 0 ? counts.join(', ') : 'all passed';
    lines.push(`║  ${cat.grade} ${label.padEnd(20)} ${detail.padEnd(21)}║`);
  }

  lines.push('╠══════════════════════════════════════════════╣');
  lines.push(`║  Tested: ${scorecard.timestamp.slice(0, 19).padEnd(34)}║`);
  lines.push('╚══════════════════════════════════════════════╝');

  return lines.join('\n');
}
```

### Grade Thresholds

| Grade | Meaning |
|-------|---------|
| **A** | Resilient — all failure modes handled gracefully, user always sees helpful feedback |
| **B** | Good — most failures handled, minor gaps (missing retry buttons, unclear messages) |
| **C** | Fragile — some failures cause confusing UX but no data loss or blank pages |
| **D** | Poor — multiple failures cause blank pages, raw errors, or lost user input |
| **F** | Broken — critical failures (data loss, XSS, blank pages on common failure modes) |

---

## Integration

### With Edit-Reload-Verify Loop

Failure injection is NOT part of the tight Edit-Reload-Verify loop (that would be too slow). Instead, run it as a **separate pass** after functional QA:

```
Edit-Reload-Verify (per component) → Functional QA → Visual QA → Failure Injection → Signoff
```

### With Interactive Sessions

During interactive debugging, use targeted injection to test specific concerns:

```javascript
// Quick test: "what happens if this API call fails?"
const inj = await injectNetworkFailure(page, '**/api/v1/save', 'status', { status: 500 });
await page.getByRole('button', { name: 'Save' }).click();
await page.screenshot({ path: '/tmp/save-failure.png' });
// Agent reviews screenshot: is there an error message?
await inj.remove();
```

### With Batch Mode (Playwright Test)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Failure resilience', () => {
  test('dashboard handles API failure gracefully', async ({ page }) => {
    // Inject 500 for the main data endpoint
    await page.route('**/api/v1/dashboard', route =>
      route.fulfill({ status: 500, body: '{"error":"Internal Server Error"}' })
    );

    await page.goto('/dashboard');

    // Should show error state, NOT blank page
    await expect(page.getByText(/error|failed|unavailable/i)).toBeVisible();
    // Should NOT show raw error details to user
    await expect(page.getByText(/TypeError|undefined|null/i)).not.toBeVisible();
  });

  test('form preserves data on submission failure', async ({ page }) => {
    await page.goto('/settings');
    await page.getByLabel('Display Name').fill('Test Name');

    // Inject failure for save endpoint
    await page.route('**/api/v1/settings', route =>
      route.fulfill({ status: 500, body: '{"error":"Server Error"}' })
    );

    await page.getByRole('button', { name: 'Save' }).click();

    // Form data should be preserved
    await expect(page.getByLabel('Display Name')).toHaveValue('Test Name');
    // Error message should be visible
    await expect(page.getByText(/error|failed/i)).toBeVisible();
  });

  test('submit button prevents double submission', async ({ page }) => {
    await page.goto('/checkout');
    let requestCount = 0;
    page.on('request', req => {
      if (req.url().includes('/api/v1/purchase') && req.method() === 'POST') requestCount++;
    });

    await page.getByRole('button', { name: 'Purchase' }).click();
    await page.getByRole('button', { name: 'Purchase' }).click({ timeout: 1000 }).catch(() => {});
    await page.getByRole('button', { name: 'Purchase' }).click({ timeout: 1000 }).catch(() => {});

    await page.waitForTimeout(2000);
    expect(requestCount).toBeLessThanOrEqual(1);
  });
});
```

---

## Common Recipes

### Recipe: Test All API Endpoints for 500 Handling

```javascript
// Discover + test every endpoint in one shot
const deps = await discoverNetworkDependencies(page, async (p) => {
  await p.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
});

for (const dep of deps) {
  const inj = await injectNetworkFailure(page, dep.pathPattern, 'status', { status: 500, log: false });
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);

  const isBlank = await page.evaluate(() => document.body.innerText.trim().length < 20);
  const icon = isBlank ? 'CRIT' : 'OK';
  console.log(`  [${icon}] ${dep.method} ${new URL(dep.url).pathname}`);

  if (isBlank) await page.screenshot({ path: `/tmp/500-${new URL(dep.url).pathname.replace(/\//g, '_')}.png` });
  await inj.remove();
}
```

### Recipe: Test Form Resilience

```javascript
// Fill form, then break everything, then check form data is preserved
await page.goto('http://127.0.0.1:3000/settings');
await page.getByLabel('Name').fill('Important Data');
await page.getByLabel('Email').fill('user@example.com');

// Break the save endpoint
const inj = await injectNetworkFailure(page, '**/api/v1/settings', 'abort');
await page.getByRole('button', { name: 'Save' }).click();
await page.waitForTimeout(2000);

// Verify form data survived
const nameValue = await page.getByLabel('Name').inputValue();
const emailValue = await page.getByLabel('Email').inputValue();
console.log(`Form preserved: name="${nameValue}", email="${emailValue}"`);
console.log(nameValue === 'Important Data' ? 'OK: Data preserved' : 'CRIT: Data lost!');

await inj.remove();
```

### Recipe: Test Auth Expiry During Flow

```javascript
// Start a multi-step flow
await page.goto('http://127.0.0.1:3000/onboarding/step-1');
await page.getByLabel('Company Name').fill('Acme Corp');
await page.getByRole('button', { name: 'Next' }).click();
await page.waitForURL('**/step-2');

// Expire auth mid-flow
await corruptSessionState(page, 'expire-auth');

// Try to continue
await page.getByLabel('Industry').selectOption('Technology');
await page.getByRole('button', { name: 'Next' }).click();
await page.waitForTimeout(3000);

// Check outcome
await page.screenshot({ path: '/tmp/auth-expired-midflow.png' });
const currentUrl = page.url();
const bodyText = await page.evaluate(() => document.body.innerText);
const hasLoginPrompt = /sign in|log in|session expired/i.test(bodyText);
console.log(`URL after expiry: ${currentUrl}`);
console.log(hasLoginPrompt ? 'OK: Login prompt shown' : 'WARN: No auth error shown');
```

### Recipe: Quick Resilience Smoke Test

The minimum viable failure injection — run this in under 30 seconds:

```javascript
// 1. Block ALL API calls and see what happens
const inj = await injectNetworkFailure(page, '**/api/**', 'abort', { log: false });
await page.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
const blankOnAbort = await page.evaluate(() => document.body.innerText.trim().length < 20);
await page.screenshot({ path: '/tmp/smoke-all-apis-down.png' });
await inj.remove();

// 2. Wipe storage and reload
await page.goto('http://127.0.0.1:3000/dashboard', { waitUntil: 'networkidle' });
await corruptSessionState(page, 'wipe-storage');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
const blankOnWipe = await page.evaluate(() => document.body.innerText.trim().length < 20);
await page.screenshot({ path: '/tmp/smoke-storage-wiped.png' });

// 3. Report
console.log('=== SMOKE TEST ===');
console.log(`All APIs down: ${blankOnAbort ? 'FAIL (blank page)' : 'PASS (error state shown)'}`);
console.log(`Storage wiped:  ${blankOnWipe ? 'FAIL (blank page)' : 'PASS (recovered)'}`);
```

---

## Graceful Degradation Reference

What "good" failure handling looks like for each failure type. Use this as a checklist when evaluating screenshots after injection.

| Failure Type | Critical (Fix Now) | Acceptable |
|-------------|-------------------|------------|
| **API returns 500** | Blank page, raw error text, app crash | Error message with retry option, data preserved |
| **API times out** | Infinite spinner, frozen UI | Timeout message after reasonable wait, retry option |
| **API returns empty** | `undefined` rendered, layout collapse | Empty state UI, "no data" message |
| **API returns malformed JSON** | Unhandled exception, blank page | Parse error caught, fallback to cached/empty state |
| **Network down (abort)** | Silent failure, stale data shown as current | Offline banner, cached data labeled as stale |
| **Auth expired** | Infinite redirect loop, blank page, 401 cascade | Redirect to login, preserve intended destination |
| **Storage wiped** | Crash on hydration, infinite loop | Re-fetch from server, re-authenticate if needed |
| **Storage corrupted** | `SyntaxError` in console, blank page | Parse errors caught, clear corrupt data, re-fetch |
| **Double-click submit** | Multiple identical POST requests | Button disabled after first click, or server idempotency |
| **Long input text** | Layout explosion, horizontal scroll | Text truncated/wrapped, layout stable |
| **XSS payload in input** | Script executes | Payload displayed as plain text, properly escaped |
| **Paste bomb (50KB)** | Browser hangs, tab crashes | Input truncated to maxlength, or warning shown |
| **Rapid navigation** | Race condition, wrong data rendered | Previous requests cancelled, latest data shown |

### Agent Judgment Checklist

After each injection, the agent should check:

1. **Is the page still navigable?** — Can you click links, use the nav? Or is it frozen?
2. **Is there a helpful error message?** — Not raw error text, but a user-friendly message
3. **Is user input preserved?** — Form data, selections, scroll position
4. **Is there a recovery path?** — Retry button, back button, login redirect
5. **Are console errors caught?** — No unhandled promise rejections or uncaught TypeErrors
6. **Is the failure mode clear?** — User can understand what went wrong and what to do next
