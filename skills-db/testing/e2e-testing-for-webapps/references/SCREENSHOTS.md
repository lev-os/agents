# Screenshot Capture & Normalization

Screenshot strategies for model-assisted QA: CSS pixel normalization, coordinate alignment, web vs Electron paths, and click-back helpers.

## Table of Contents
- [Default: Model-Bound Screenshots](#default-model-bound-screenshots)
- [Shared Helpers](#shared-helpers)
- [Web CSS Normalization](#web-css-normalization)
- [Electron CSS Normalization](#electron-css-normalization)
- [Raw Screenshot Exception](#raw-screenshot-exception)
- [When to Use What](#when-to-use-what)

---

## Default: Model-Bound Screenshots

If you plan to emit a screenshot for model interpretation (e.g., `codex.emitImage(...)` or attaching to a report), **normalize to CSS pixels** for the exact region captured. This:

- Keeps returned coordinates aligned with Playwright CSS pixels for follow-up clicks
- Reduces image payload size and model token cost

**Do NOT emit raw native-window screenshots by default.** Skip normalization only when you explicitly need device-pixel fidelity (Retina/DPI artifact debugging, pixel-accurate rendering inspection).

### The `scale: "css"` Caveat

Do not assume `page.screenshot({ scale: "css" })` is always enough in native-window mode (`viewport: null`). In Chromium on macOS Retina displays, headed native-window screenshots can still come back at device-pixel size even with `scale: "css"`. The same applies to Electron windows (launched with `noDefaultViewport`).

---

## Shared Helpers

```javascript
var emitJpeg = async function (bytes) {
  await codex.emitImage({
    bytes,
    mimeType: "image/jpeg",
  });
};

var emitWebJpeg = async function (surface, options = {}) {
  await emitJpeg(await surface.screenshot({
    type: "jpeg",
    quality: 85,
    scale: "css",
    ...options,
  }));
};

var clickCssPoint = async function ({ surface, x, y, clip }) {
  await surface.mouse.click(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};

var tapCssPoint = async function ({ page, x, y, clip }) {
  await page.touchscreen.tap(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};
```

**Conventions:**
- Use `page` or `mobilePage` for web, `appWindow` for Electron as the `surface`
- Treat `clip` as CSS pixels from `getBoundingClientRect()` in the renderer
- Prefer JPEG at `quality: 85` unless lossless fidelity is specifically required
- For full-image captures, use returned `{ x, y }` directly
- For clipped captures, add the clip origin back when clicking

---

## Web CSS Normalization

### Standard Path (Explicit Viewport)

Works directly with `scale: "css"` — the preferred path:

```javascript
// Full viewport
await emitWebJpeg(page);

// Mobile
await emitWebJpeg(mobilePage);

// Clipped region
await emitWebJpeg(page, { clip });
await emitWebJpeg(mobilePage, { clip });
```

### Click-Back from Model Coordinates

```javascript
// Full viewport — model returns { x, y }
await clickCssPoint({ surface: page, x, y });

// Mobile tap
await tapCssPoint({ page: mobilePage, x, y });

// From clipped screenshot — add clip origin
await clickCssPoint({ surface: page, clip, x, y });
await tapCssPoint({ page: mobilePage, clip, x, y });

// From element bounding box
const box = await locator.boundingBox();
await clickCssPoint({ surface: page, clip: box, x, y });
```

### Native-Window Fallback

When `scale: "css"` still returns device-pixel size in native-window mode, resize inside the current page with canvas (no scratch page needed):

```javascript
var emitWebScreenshotCssScaled = async function ({ page, clip, quality = 0.85 } = {}) {
  var NodeBuffer = (await import("node:buffer")).Buffer;
  const target = clip
    ? { width: clip.width, height: clip.height }
    : await page.evaluate(() => ({
        width: window.innerWidth,
        height: window.innerHeight,
      }));

  const screenshotBuffer = await page.screenshot({
    type: "png",
    ...(clip ? { clip } : {}),
  });

  const bytes = await page.evaluate(
    async ({ imageBase64, targetWidth, targetHeight, quality }) => {
      const image = new Image();
      image.src = `data:image/png;base64,${imageBase64}`;
      await image.decode();

      const canvas = document.createElement("canvas");
      canvas.width = targetWidth;
      canvas.height = targetHeight;

      const ctx = canvas.getContext("2d");
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(image, 0, 0, targetWidth, targetHeight);

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg", quality)
      );

      return new Uint8Array(await blob.arrayBuffer());
    },
    {
      imageBase64: NodeBuffer.from(screenshotBuffer).toString("base64"),
      targetWidth: target.width,
      targetHeight: target.height,
      quality,
    }
  );

  await emitJpeg(bytes);
};
```

Usage:

```javascript
// Full viewport fallback — returned { x, y } are direct CSS coordinates
await emitWebScreenshotCssScaled({ page });
await clickCssPoint({ surface: page, x, y });

// Clipped fallback — add clip origin
await emitWebScreenshotCssScaled({ page, clip });
await clickCssPoint({ surface: page, clip, x, y });
```

---

## Electron CSS Normalization

For Electron, normalize in the main process using `BrowserWindow.capturePage()` and `nativeImage.resize()`. **Do NOT use** `appWindow.context().newPage()` or `electronApp.context().newPage()` as a scratch page — Electron contexts do not support that path reliably.

```javascript
var emitElectronScreenshotCssScaled = async function ({ electronApp, clip, quality = 85 } = {}) {
  const bytes = await electronApp.evaluate(async ({ BrowserWindow }, { clip, quality }) => {
    const win = BrowserWindow.getAllWindows()[0];
    const image = clip ? await win.capturePage(clip) : await win.capturePage();

    const target = clip
      ? { width: clip.width, height: clip.height }
      : (() => {
          const [width, height] = win.getContentSize();
          return { width, height };
        })();

    const resized = image.resize({
      width: target.width,
      height: target.height,
      quality: "best",
    });

    return resized.toJPEG(quality);
  }, { clip, quality });

  await emitJpeg(bytes);
};
```

### Full Electron Window

```javascript
await emitElectronScreenshotCssScaled({ electronApp });
await clickCssPoint({ surface: appWindow, x, y });
```

### Clipped Electron Region (CSS Pixels from Renderer)

```javascript
var clip = await appWindow.evaluate(() => {
  const rect = document.getElementById("board").getBoundingClientRect();
  return {
    x: Math.round(rect.x),
    y: Math.round(rect.y),
    width: Math.round(rect.width),
    height: Math.round(rect.height),
  };
});

await emitElectronScreenshotCssScaled({ electronApp, clip });
await clickCssPoint({ surface: appWindow, clip, x, y });
```

---

## Raw Screenshot Exception

Use only when raw pixels matter more than CSS-coordinate alignment — Retina/DPI artifact debugging, pixel-accurate rendering inspection, or fidelity-sensitive review.

```javascript
// Web desktop
await codex.emitImage({
  bytes: await page.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});

// Electron
await codex.emitImage({
  bytes: await appWindow.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});

// Mobile
await codex.emitImage({
  bytes: await mobilePage.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});
```

---

## When to Use What

| Scenario | Path | Normalization |
|----------|------|---------------|
| Explicit viewport, any platform | `emitWebJpeg(page)` | `scale: "css"` works directly |
| Mobile emulation | `emitWebJpeg(mobilePage)` | `scale: "css"` works directly |
| Native window, macOS non-Retina | `emitWebJpeg(page)` | Usually works |
| Native window, macOS Retina | `emitWebScreenshotCssScaled({ page })` | Canvas resize fallback |
| Electron, any platform | `emitElectronScreenshotCssScaled({ electronApp })` | Main-process resize |
| DPI/Retina artifact debugging | Raw `page.screenshot()` | None (intentional) |
| Local-only inspection (not emitted) | Raw capture | None needed |
| Batch test report artifacts | `page.screenshot({ path })` | Playwright default |
