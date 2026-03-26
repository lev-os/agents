# Interactive Browser Sessions

Persistent Playwright sessions for iterative debugging — keep browser handles alive across code changes instead of restarting the entire toolchain.

## Table of Contents
- [Preconditions](#preconditions)
- [One-Time Setup](#one-time-setup)
- [Bootstrap](#bootstrap)
- [Session Modes](#session-modes)
- [Web Sessions](#web-sessions)
- [Electron Sessions](#electron-sessions)
- [Iteration Patterns](#iteration-patterns)
- [Dev Server Management](#dev-server-management)
- [Cleanup](#cleanup)
- [Common Failure Modes](#common-failure-modes)

---

## Preconditions

**For Codex (js_repl):**
- Enable in `~/.codex/config.toml`: `[features]` → `js_repl = true`
- Or start with `--enable js_repl`
- Currently requires `--sandbox danger-full-access`
- After enabling, start a new session so the tool list refreshes
- Treat `js_repl_reset` as recovery, not routine — resetting destroys your handles

**For Claude Code:**
- Use Bash tool to run Node.js scripts or interactive node sessions
- Or use persistent terminal sessions (tmux/screen) for the dev server

**Universal:**
- Run setup from the same project directory you need to debug
- Prefer `127.0.0.1` over `localhost` for local servers

---

## One-Time Setup

```bash
test -f package.json || npm init -y
npm install playwright
# Web-only (headed Chromium or mobile emulation):
npx playwright install chromium
# Electron-only (if the target workspace IS the app):
# npm install --save-dev electron
node -e "import('playwright').then(() => console.log('playwright import ok')).catch((error) => { console.error(error); process.exit(1); })"
```

If you switch to a different workspace later, repeat setup there.

---

## Bootstrap

Run once per session to initialize handles:

```javascript
var chromium;
var electronLauncher;
var browser;
var context;
var page;
var mobileContext;
var mobilePage;
var electronApp;
var appWindow;

try {
  ({ chromium, _electron: electronLauncher } = await import("playwright"));
  console.log("Playwright loaded");
} catch (error) {
  throw new Error(
    `Could not load playwright from the current cwd. Run setup commands first. Original error: ${error}`
  );
}
```

**Binding rules:**
- Use `var` for shared top-level handles (later cells/calls reuse them)
- Keep setup cells short — happy path only
- If a handle looks stale, set it to `undefined` and rerun rather than adding recovery logic
- Prefer one named handle per surface (`page`, `mobilePage`, `appWindow`)

**Shared web helpers:**

```javascript
var resetWebHandles = function () {
  context = undefined;
  page = undefined;
  mobileContext = undefined;
  mobilePage = undefined;
};

var ensureWebBrowser = async function () {
  if (browser && !browser.isConnected()) {
    browser = undefined;
    resetWebHandles();
  }
  browser ??= await chromium.launch({ headless: false });
  return browser;
};

var reloadWebContexts = async function () {
  for (const currentContext of [context, mobileContext]) {
    if (!currentContext) continue;
    for (const p of currentContext.pages()) {
      await p.reload({ waitUntil: "domcontentloaded" });
    }
  }
  console.log("Reloaded existing web tabs");
};
```

---

## Session Modes

Use an **explicit viewport** by default. Treat native-window mode as a separate validation pass.

| Mode | When | Characteristics |
|------|------|-----------------|
| **Explicit viewport** (default) | Routine iteration, breakpoint checks, reproducible screenshots, snapshot diffs | Stable across machines, avoids window-manager variability |
| **Native window** (`viewport: null`) | Validate launched window size, OS-level DPI, browser chrome interactions | Separate headed pass for environment-specific checks |
| **Electron** | Always native-window behavior | Launches with `noDefaultViewport`, check as-launched size before resizing |

**Rules:**
- For deterministic high-DPI, keep explicit viewport and add `deviceScaleFactor` instead of switching to native
- Switching modes = context reset. Close old page/context, create new ones
- When signoff depends on both breakpoints and real desktop: do explicit viewport first, then native-window validation

---

## Web Sessions

### Desktop Web Context

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

if (page?.isClosed()) page = undefined;

await ensureWebBrowser();
context ??= await browser.newContext({
  viewport: { width: 1600, height: 900 },
});
page ??= await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded:", await page.title());
```

If stale: set `context = page = undefined` and rerun.

### Mobile Web Context

```javascript
var MOBILE_TARGET_URL = typeof TARGET_URL === "string"
  ? TARGET_URL
  : "http://127.0.0.1:3000";

if (mobilePage?.isClosed()) mobilePage = undefined;

await ensureWebBrowser();
mobileContext ??= await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
});
mobilePage ??= await mobileContext.newPage();

await mobilePage.goto(MOBILE_TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded mobile:", await mobilePage.title());
```

If stale: set `mobileContext = mobilePage = undefined` and rerun.

### Native-Window Web Pass

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

await ensureWebBrowser();

await page?.close().catch(() => {});
await context?.close().catch(() => {});
page = undefined;
context = undefined;

browser ??= await chromium.launch({ headless: false });
context = await browser.newContext({ viewport: null });
page = await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded native window:", await page.title());
```

---

## Electron Sessions

Set `ELECTRON_ENTRY` to `.` when the current workspace is the Electron app and `package.json` points `main` to the right entry file. Use a specific path like `./main.js` to target a different entry.

### Launch or Reuse

```javascript
var ELECTRON_ENTRY = ".";

if (appWindow?.isClosed()) appWindow = undefined;

if (!appWindow && electronApp) {
  await electronApp.close().catch(() => {});
  electronApp = undefined;
}

electronApp ??= await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow ??= await electronApp.firstWindow();

console.log("Loaded Electron window:", await appWindow.title());
```

If not running from the Electron app workspace, pass `cwd` explicitly.

If stale: set `electronApp = appWindow = undefined` and rerun.

### Restart (Main-Process / Preload / Startup Changes)

```javascript
await electronApp.close().catch(() => {});
electronApp = undefined;
appWindow = undefined;

electronApp = await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow = await electronApp.firstWindow();
console.log("Relaunched Electron window:", await appWindow.title());
```

Include the same `cwd` if your launch requires one.

---

## Iteration Patterns

### Reload Decision Tree

| Change Type | Action |
|-------------|--------|
| Renderer-only (CSS, component, template) | Reload existing page/window |
| Main-process, preload, or startup code | Relaunch Electron |
| Uncertain about process ownership | Relaunch (don't guess) |

### Web Renderer Reload

```javascript
await reloadWebContexts();
```

### Electron Renderer Reload

```javascript
await appWindow.reload({ waitUntil: "domcontentloaded" });
console.log("Reloaded Electron window");
```

### Edit-Reload-Verify Micro-Loop

After every code change, run this tight loop before moving on:

1. Reload: `await page.reload({ waitUntil: 'domcontentloaded' })`
2. Layout snapshot diff: `diffLayoutSnapshots(before, after)` — catch unintended structural changes
3. DOM health check: `domHealthCheck(page)` — fix critical/major issues
4. Screenshot: `await page.screenshot({ path: '/tmp/verify.png' })` — aesthetic check only
5. Move to next change only after all three pass

Each iteration's "after" snapshot becomes the next iteration's "before" baseline.

**Full details:** SYSTEMATIC-TESTING.md | **Functions:** DIAGNOSTIC-TOOLS.md

### Quick Failure Injection

During interactive debugging, inject failures to test error handling without leaving the session:

```javascript
// Test: what happens if the save API fails?
const inj = await injectNetworkFailure(page, '**/api/v1/save', 'status', { status: 500 });
await page.getByRole('button', { name: 'Save' }).click();
await page.screenshot({ path: '/tmp/save-failure.png' });
await inj.remove();

// Test: what happens if ALL APIs fail?
const inj = await injectNetworkFailure(page, '**/api/**', 'abort');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.screenshot({ path: '/tmp/all-apis-down.png' });
await inj.remove();

// Test: what happens if auth expires?
await corruptSessionState(page, 'expire-auth');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.screenshot({ path: '/tmp/auth-expired.png' });
```

**Functions:** FAILURE-INJECTION.md | **When to run:** After functional QA confirms the happy path works

### Default Posture

- Keep each cell/script short and focused on one interaction burst
- Reuse existing top-level bindings (`browser`, `context`, `page`, `electronApp`, `appWindow`)
- If you need isolation, create a new page or context inside the same browser
- For Electron, use `electronApp.evaluate(...)` only for main-process inspection
- Fix helper mistakes in place — do not reset the REPL unless the kernel is actually broken

---

## Dev Server Management

For local web debugging, keep the app running in a persistent TTY session (tmux, screen, or separate terminal). Do not rely on one-shot background commands.

```bash
npm start
```

Before `page.goto(...)`, verify the chosen port is listening and the app responds.

For Electron debugging, launch the app through `_electron.launch(...)` so the same session owns the process. If the Electron renderer depends on a separate dev server (Vite, Next), keep that server running in a persistent TTY and then relaunch/reload Electron from your session.

---

## Cleanup

Only run cleanup when the task is actually finished. This is manual — exiting the session does not implicitly close browsers or Electron apps.

```javascript
if (electronApp) {
  await electronApp.close().catch(() => {});
}

if (mobileContext) {
  await mobileContext.close().catch(() => {});
}

if (context) {
  await context.close().catch(() => {});
}

if (browser) {
  await browser.close().catch(() => {});
}

browser = undefined;
context = undefined;
page = undefined;
mobileContext = undefined;
mobilePage = undefined;
electronApp = undefined;
appWindow = undefined;

console.log("Playwright session closed");
```

Run this and wait for the `"Playwright session closed"` log before quitting.

---

## Common Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module 'playwright'` | Not installed in current workspace | Run one-time setup, verify import |
| Browser executable missing | Playwright installed but browsers not | `npx playwright install chromium` |
| `page.goto: net::ERR_CONNECTION_REFUSED` | Dev server not running | Check persistent TTY, recheck port, use `127.0.0.1` |
| `electron.launch` hangs/times out | Bad entry path or missing dep | Verify `electron` dep, confirm `args` target, ensure renderer dev server running |
| `Identifier has already been declared` | `let`/`const` redeclared in REPL | Use `var`, choose new name, or wrap in `{ ... }`. `js_repl_reset` only if kernel stuck |
| `Protocol error (Target.createTarget): Not supported` | Tried `appWindow.context().newPage()` in Electron | Use `BrowserWindow.capturePage()` + `nativeImage.resize()` instead |
| `js_repl` timed out | Cell too long | Break into shorter, focused cells |
| Browser/network ops fail immediately | Sandbox blocking | Confirm `--sandbox danger-full-access` (Codex) |
