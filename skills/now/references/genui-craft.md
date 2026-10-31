# GenUI craft and visual QA

Read this before you write a GenUI `source.html`, and again before you report one. It holds the house reading and component rules and the visual QA routine. Both come from accepted prior work. In Leviathan, look at `.lev/now/genui/drafts/hermit-run-review/` (`source.html` and `ux-design.md`, which logs each padding and crowding defect with its cause and fix) and `.lev/now/genui/idea-explorer/20261031/` (`src/app.css`, `verify.mjs`, `README.md`). Read them as examples. Other projects may not have them.

## Structure follows the object

GenUI means the page's structure comes from the content. The default lev.now scaffold (hero, KPI row, card grid) is the RenderSpec recipe. A GenUI page starts from what the reader must do with this one object.

- Name the object and its mechanism before you write layout, and draw that shape. For example, a run may be a loop of steps, a change a diff, a decision a debate, and a choice between options parallel columns, one for each option the content actually has. These are examples, not templates: the content decides the form and the count. In the Hermit page, the loop rail is the navigation, and each step opens the evidence that proves it.
- Put the observed bytes first. Raw replies, changed lines, commands and run ids are the product. A summary sits beside them; it never replaces them.
- Keep dense execution information rich. Use progressive disclosure: tabs, `<details>`, a row that opens a drill-down, a side sheet for setup. Keep logs, traces and exact values one click away.
- Put each limit next to the claim it limits.
- Label the data basis where the reader sees it: real (read from the source), reference (shaped from real source), synthetic or sample. Label a prototype as a prototype, and a disabled control with its reason ("Not connected"). Never show fake live status.
- Give a header one job: what this page is. Status pills go on their own row; the actions go to one side. Add page navigation only when the page has views the reader moves between. Use tabs or a rail that wraps, not a hamburger.
- Use cards when items are peers the reader compares. Use a table when items share columns. Use a sequence when order matters. A grid of interchangeable cards with an icon, a title and two lines says nothing.
- Use space, weight and alignment for emphasis. Colored left borders, decorative title underlines and glows add noise.

## Type

- Base text is 16px (`1rem`). Reading prose is 17–18px (`1.0625rem`–`1.125rem`) when the page is mostly reading. Line height is 1.5–1.7.
- Bound the prose measure: `max-width: 60ch`–`75ch` on paragraphs, leads and blockquotes.
- Labels, metadata, table cells and code have a floor of 13px. Prefer 14px (`0.875rem`). Code inside small text needs its own floor, for example `font-size: max(0.8125rem, 0.9em)`.
- The shell's house classes ship in every GenUI page: `.prose` (65ch, line height 1.7), `.prose--narrow`, `.prose--wide`, `.lead`. Use them for long reading. Set your own sizes only on your own classes.

## Spacing and padding

- Declare a few space steps as custom properties on the page root class, then use only those steps.
- Each box owns its padding in its own rule: about 1.25–1.75rem on desktop, about 1.1rem on a phone. A box with a border or background always has inner padding.
- Separate groups with more space than you put between their items.

## Scoped CSS that does not fight itself

- One `<style>` block. Prefix every selector with one page class. Set top space on `#lev-main .<page>` (about 5.5rem clears the fixed nav).
- Write every reset inside `:where()`, so it has the weight of the page class only: `.page :where(h1, h2, p, ul, ol, dl, dd, pre, figure) { margin: 0; }` and `.page :where(button) { font: inherit; color: inherit; }`. A reset such as `.page button` (0,1,1) outranks `.page-pill` (0,1,0) and erases the component's font, color, margin and padding. That was the main cause of the broken Hermit padding.
- Use theme variables only: `--color-text`, `--color-text-muted`, `--color-accent`, `--color-accent-text`, `--color-surface`, `--color-surface-alt`, `--color-border`, `--font-display`, `--font-mono`, and the status colours `--color-success`, `--color-error`, `--color-warning` with a fallback. Both modes then work.
- Measure the actual text and background pairs in both themes against a 4.5:1 target (3:1 for large text), and adjust the colours until each pair passes. Status text on a tint of its own colour is a common failure. The Hermit page fixed its pairs by mixing the text with the body colour, `color-mix(in srgb, var(--color-success) 70%, var(--color-text))`. That mix is a tested example for that page, not a general fix; measure your own pairs.

## Layout that fits a phone

- Give every grid explicit shrinkable tracks: `grid-template-columns: minmax(0, 1fr)`. An implicit track grows to its widest child and widens the page.
- Put `min-width: 0` on grid and flex children that hold text, code or tables.
- Wrap long text: `overflow-wrap: anywhere` on paths, ids, commands and table cells. Keep one short token unbroken with `white-space: nowrap` (for example a flag such as `--check`).
- On a phone, turn tables into label/value rows, let tabs and nav wrap, and make segmented controls an even grid (`repeat(auto-fit, minmax(6rem, 1fr))`). Only code and diffs may scroll sideways, inside their own box.
- Position any scroller that holds an absolutely placed element (for example a screen-reader caption), or the element escapes and widens the page.
- A dialog with a flex body needs `min-height: 0` on the body, so the body scrolls and not the dialog.

## Round markers

A step number or status dot is a true circle: a fixed `width` and `height` of the same value (24px or more for text), `flex: 0 0 <size>` or `flex-shrink: 0`, `border-radius: 50%`, and `display: grid; place-items: center`. Keep its label outside the circle, so the label wraps and never clips.

## Interaction and access

Real `<button>` elements, a visible `:focus-visible` ring, ARIA tabs with arrow keys, `aria-pressed` on toggles, `aria-current="page"` (a value, not empty) on the current link, a native `<dialog>` that Escape closes and that returns focus, status that does not depend on colour alone, and `prefers-reduced-motion`.

## Visual QA routine

Run it on every GenUI render, before you report. A PNG on disk is not an inspection.

1. **List the views.** Every distinct view and state the page has: each tab, route, dialog, selected or expanded state, the state after each primary action, and empty or error states you designed. For a collection, list every item. When you inspect only some, name the rest as not viewed.
2. **Capture.** Light and dark at 1440 and 390 wide for each view. Add 1024, 900 and 768 when the layout changes between them. Write captures to a fresh temp directory, never into the project. Use the probe below.
3. **Measure.** For each capture: the theme the page reports, document overflow, boxes that scroll sideways, text under 13px, circles that are not round, console and page errors, and the focus ring after Tab.
4. **Look.** Read each image with the image-reading tool. Write one line per image: what it shows and what is wrong. Check hierarchy, padding inside each box, crowding, clipped or colliding labels, the first line below the fixed nav, contrast, and whether the structure still expresses the object.
5. **Fix and compare.** Fix `source.html`. Re-render with the same `--title` and `--theme`. Capture again, and read the before and after images of each view you changed. Never edit the rendered HTML by hand.
6. **Report what you inspected.** List the images read, the measured values, the fixes, and each gap you could not check (for example, a width you did not view, or a browser that would not start).

### Probe

Write this to the temp QA directory as `genui-probe.mjs`. Run it from the project root, where `plugins/now` provides Playwright. Each state argument is a CSS selector to click, or a `#/…` hash route; the first capture is the page as loaded. For a page whose renderer belongs to another checkout, change the `package.json` path.

```bash
now_qa_dir="$(mktemp -d "${TMPDIR:-/tmp}/lev-now-qa.XXXXXX")"
node "$now_qa_dir/genui-probe.mjs" .lev/now/<slug>.html "$now_qa_dir" '#tab-details' '#/settings'
```

```js
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const { chromium } = createRequire(resolve('plugins/now/package.json'))('playwright');
const [html, out, ...states] = process.argv.slice(2);
const browser = await chromium.launch();
for (const theme of ['light', 'dark']) for (const width of [1440, 390]) for (const [i, state] of [null, ...states].entries()) {
  const ctx = await browser.newContext({ viewport: { width, height: width === 390 ? 844 : 900 }, colorScheme: theme });
  await ctx.addInitScript((t) => localStorage.setItem('lev-now-theme', t), theme);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  await page.goto(pathToFileURL(resolve(html)).href, { waitUntil: 'networkidle' });
  if (state?.startsWith('#/')) await page.evaluate((h) => { location.hash = h; }, state);
  else if (state) await page.locator(state).first().click();
  await page.waitForTimeout(300);
  const m = await page.evaluate(() => {
    const els = [...document.querySelectorAll('#lev-main *')].filter((el) => el.getClientRects().length);
    const name = (el) => `${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : ''}`;
    return {
      theme: document.documentElement.dataset.theme,
      docOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      sideScroll: els.filter((el) => el.scrollWidth > el.clientWidth + 1 && /auto|scroll/.test(getComputedStyle(el).overflowX)).map((el) => `${name(el)} +${el.scrollWidth - el.clientWidth}px`),
      tinyText: [...new Set(els.filter((el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(el).fontSize) < 13).map(name))],
      notRound: els.filter((el) => getComputedStyle(el).borderRadius === '50%').map((el) => el.getBoundingClientRect()).filter((b) => b.width >= 12 && Math.abs(b.width - b.height) > 0.5).length,
    };
  });
  const shot = `${out}/${theme}-${width}-${i}.png`;
  // an open modal is captured at viewport size; a full-page shot would stack it over the page
  await page.screenshot({ path: shot, fullPage: !(await page.locator('dialog[open]').count()) });
  await page.keyboard.press('Tab');
  const focus = await page.evaluate(() => { const a = document.activeElement, s = a && getComputedStyle(a); return s ? { el: a.tagName.toLowerCase(), ring: s.outlineStyle !== 'none' || s.boxShadow !== 'none' } : null; });
  console.log(JSON.stringify({ shot, state, ...m, focus, errors }));
  await ctx.close();
}
await browser.close();
```

A clean probe line has the requested `theme`, `docOverflow` of 1 or less, `sideScroll` only on code or diff boxes, empty `tinyText` and `errors`, `notRound` 0, and a focus ring. The probe measures; it does not look. Step 4 still applies to every image.
