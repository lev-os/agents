// Loaded into every cu session. Plain `var`/function declarations so they stay global.
var sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// Accessibility tree as text. opts: textLimit ("max" for long text), maxTreeNodes, maxTreeDepth.
async function tree(app, opts = {}) {
  return String(await app.getAXState({ emit: false, disableDiffing: true, ...opts }));
}
// Lines of a tree that match a regex, trimmed.
function grep(t, re) {
  return t.split("\n").map((l) => l.trim()).filter((l) => re.test(l));
}
// Element number at the start of a tree line ("176 scroll area ..." -> "176").
function idx(line) {
  return String(line).trim().split(" ")[0];
}
// Move through a list and gather tree lines matching `keep`, oldest first, without duplicates.
// With `target` it scrolls the first element matching it; with target null it presses Page Up/Down
// `pages` times (chat apps often ignore scroll events and label no element as scrollable).
// The tree often holds more than the visible screen: check what one read gives before you scroll.
// Stops after `max` scrolls, when `until(lines)` is true, or when a scroll shows nothing new. Element numbers change after a scroll; this re-finds the target each time.
async function scrollCollect(app, target, keep, { dir = "up", pages = 3, max = 25, until, opts = {} } = {}) {
  var seen = new Set(), all = [];
  var add = (t) => {
    var fresh = grep(t, keep).filter((l) => !seen.has(l.replace(/^\d+ /, "")));
    fresh.forEach((l) => seen.add(l.replace(/^\d+ /, "")));
    if (dir === "up") all = fresh.concat(all); else all = all.concat(fresh);
    return fresh.length;
  };
  var t = await tree(app, opts);
  add(t);
  for (var i = 0; i < max; i++) {
    if (until && until(all)) break;
    if (target) {
      var line = grep(t, target)[0];
      if (!line) throw new Error("scrollCollect: no element matches " + target);
      await app.scroll(idx(line), dir, pages);
    } else {
      // Page keys move chat lists that ignore scroll events (Discord, tested 2026-10-21).
      for (var k = 0; k < pages; k++) await app.pressKey(dir === "up" ? "Page_Up" : "Page_Down");
    }
    await sleep(1000);
    t = await tree(app, opts);
    if (add(t) === 0) break;
  }
  return all.map((l) => l.replace(/^\d+ /, ""));
}
// Wait until the app's tree matches `re` (page loads). Returns the tree.
async function waitFor(app, re, { timeout = 15000, opts = {} } = {}) {
  var t0 = Date.now(), t = "";
  while (Date.now() - t0 < timeout) {
    t = await tree(app, opts);
    if (re.test(t)) return t;
    await sleep(500);
  }
  throw new Error("waitFor: timed out waiting for " + re);
}
// Open a URL in a new tab of the browser's front window (the user's running profile), then bind the app.
// Uses macOS `open`, which is much faster than typing into the address bar (each key press re-reads the window).
// In the Codex sandbox `open` cannot find apps, so it falls back to Cmd+T, the URL and Return (fast there).
async function openUrl(appName, url) {
  try {
    if (typeof process === "undefined") throw new Error("Codex sandbox: no open");
    var { execFileSync } = await import("node:child_process");
    execFileSync("open", ["-a", appName, url], { stdio: "ignore" });
    return cua.getApp(appName, { initialState: false });
  } catch (e) {
    var app = await cua.getApp(appName, { initialState: false });
    await app.pressKey("super+t");
    await app.typeText(url);
    await app.pressKey("Return");
    return app;
  }
}
// Close the front tab of a browser app.
async function closeTab(app) {
  await app.pressKey("super+w");
}
// Save a screenshot to its own PNG file and return the path. Open the file only when you need to see it.
// The Codex engine runs in a sandbox that cannot write files: there the image goes back to cu,
// which saves it and prints "[image saved: <path>]".
async function shot(app, name = "shot") {
  var bytes = await app.getScreenshot({ emit: false });
  try {
    var fs = await import("node:fs");
    fs.mkdirSync("/tmp/ocu-shots", { recursive: true });
    var file = `/tmp/ocu-shots/${name}-${Date.now()}.png`;
    fs.writeFileSync(file, bytes);
    return file;
  } catch (e) {
    await nodeRepl.emitImage(bytes);
    return "(screenshot: see the [image saved: ...] line)";
  }
}
// Write long results to /tmp/ocu-out/<name> and return the path; print a short summary instead of the whole list.
async function save(name, text) {
  var body = typeof text === "string" ? text : JSON.stringify(text, null, 2);
  var file = `/tmp/ocu-out/${name}`;
  try {
    var fs = await import("node:fs");
    fs.mkdirSync("/tmp/ocu-out", { recursive: true });
    fs.writeFileSync(file, body);
  } catch (e) {
    nodeRepl.write(`<<CU_SAVE ${name}>>\n${body}\n<<CU_SAVE_END>>`);
  }
  return file;
}
