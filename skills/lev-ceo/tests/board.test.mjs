// Run: node --test ~/.agents/skills/lev-ceo/tests/*.test.mjs   (Node 24 reads a bare folder as a file name)
// Every case runs the board command line in a temp folder, with XDG_STATE_HOME and TMPDIR pointed inside it,
// so the real answers file and the real board are never read or written. afterEach removes each folder setup() made.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { afterEach, test } from "node:test";
import { fileURLToPath } from "node:url";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "board.mjs");

const made = [];
afterEach(() => { for (const root of made.splice(0)) rmSync(root, { recursive: true, force: true }); });

function setup() {
  const root = mkdtempSync(join(tmpdir(), "board-test-"));
  made.push(root);
  mkdirSync(join(root, ".lev", "now"), { recursive: true });
  const state = join(root, "state");
  const tmp = join(root, "tmp");
  mkdirSync(tmp);
  return { root, state, tmp, answers: join(state, "lev", "ceo-board", "answers.jsonl") };
}

const childEnv = (ctx) => ({ ...process.env, XDG_STATE_HOME: ctx.state, TMPDIR: ctx.tmp });

function run(ctx, ...args) {
  const r = spawnSync(process.execPath, [SCRIPT, ...args, "--root", ctx.root], { encoding: "utf8", env: childEnv(ctx) });
  return { code: r.status, out: r.stdout, err: r.stderr, json: r.status === 0 && r.stdout ? JSON.parse(r.stdout) : null };
}

const ITEMS = [
  { id: "node-plan", title: "Go on the Node plan", thread_link: "t3-thread://v2/env-1/abc", what: "Go or hold.", choices: [{ id: "go", label: "Go" }, { id: "hold", label: "Hold" }], recommended: "go", since: "2026-11-04T00:09:00Z" },
  { id: "agent37-box", title: "An Agent37 box", what: "Yes or no.", choices: [{ id: "yes", label: "Yes" }, { id: "no", label: "No" }] },
];

function writeItems(ctx, items, name = "items.json") {
  const file = join(ctx.root, name);
  writeFileSync(file, JSON.stringify(items));
  return file;
}

function writeAnswers(ctx, rows) {
  mkdirSync(dirname(ctx.answers), { recursive: true });
  writeFileSync(ctx.answers, rows.map((r) => JSON.stringify(r)).join("\n") + "\n");
}

const tap = (item_id, choice, label, at, note = null) => ({ page_id: "ceo-board", item_id, choice, label, note, at });

test("write refuses an item with no choices and writes nothing", () => {
  const ctx = setup();
  const bad = [{ id: "no-choices", title: "No choices", what: "x", choices: [] }, { ...ITEMS[0], recommended: "maybe" }];
  const r = run(ctx, "write", "--input", writeItems(ctx, bad));
  assert.equal(r.code, 1);
  const lines = r.err.trim().split("\n");
  assert.equal(lines.length, 2);
  assert.match(lines[0], /no-choices.*needs at least one choice/);
  assert.match(lines[1], /recommended 'maybe' is not one of the choice ids/);
  assert.equal(existsSync(join(ctx.root, ".lev", "now", "ceo-board.json")), false);
});

test("write stamps updated and project and writes the valid items", () => {
  const ctx = setup();
  const before = Date.now();
  const r = run(ctx, "write", "--input", writeItems(ctx, ITEMS), "--project", "demo");
  assert.equal(r.code, 0, r.err);
  const board = JSON.parse(readFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), "utf8"));
  assert.equal(board.project, "demo");
  assert.ok(Date.parse(board.updated) >= before - 1000);
  assert.deepEqual(board.items.map((i) => i.id), ["node-plan", "agent37-box"]);
  assert.equal(board.items[0].recommended, "go");
  assert.equal(r.json.page.rebuilt, false, "a temp folder has no explorer build to run");
});

test("answers keeps the newest at per item, flags a stale label and an unknown item, reads a cleared row", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  writeAnswers(ctx, [
    { page_id: "other-page", item_id: "node-plan", choice: "hold", at: "2026-11-04T05:00:00Z" },
    tap("node-plan", "go", "Go", "2026-11-04T04:10:00Z"),
    tap("node-plan", "hold", "Hold", "2026-11-04T04:20:00Z"),
    tap("node-plan", "go", "Go", "2026-11-04T04:05:00Z"),
    tap("agent37-box", "maybe", "Maybe later", "2026-11-04T04:11:00Z"),
    tap("gone-item", "yes", "Yes", "2026-11-04T04:12:00Z"),
  ]);
  const r = run(ctx, "answers", "--since", "0", "--items", items);
  assert.equal(r.code, 0, r.err);
  assert.equal(r.json.lines, 6);
  const by = Object.fromEntries(r.json.rows.map((row) => [row.item_id, row]));
  assert.deepEqual(Object.keys(by).sort(), ["agent37-box", "gone-item", "node-plan"]);
  assert.equal(by["node-plan"].choice, "hold");
  assert.equal(by["node-plan"].status, "fresh");
  assert.equal(by["agent37-box"].status, "stale");
  assert.equal(by["gone-item"].status, "unknown_item");

  writeAnswers(ctx, [tap("agent37-box", "no", "No", "2026-11-04T04:00:00Z"), tap("agent37-box", null, null, "2026-11-04T04:30:00Z")]);
  const cleared = run(ctx, "answers", "--since", "0", "--items", items);
  assert.equal(cleared.json.rows.length, 1);
  assert.equal(cleared.json.rows[0].status, "cleared");
});

test("answers matches on label when the choice id differs, and --since skips read lines or older times", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  writeAnswers(ctx, [tap("node-plan", "go", "Go", "2026-11-04T04:00:00Z"), tap("agent37-box", 1, "No", "2026-11-04T04:30:00Z")]);
  const byCount = run(ctx, "answers", "--since", "1", "--items", items);
  assert.deepEqual(byCount.json.rows.map((r) => [r.item_id, r.choice, r.status]), [["agent37-box", "no", "fresh"]]);
  const byTime = run(ctx, "answers", "--since", "2026-11-04T04:15:00Z", "--items", items);
  assert.deepEqual(byTime.json.rows.map((r) => r.item_id), ["agent37-box"]);
});

async function freePort(keepOpen) {
  const server = createServer();
  await new Promise((done) => server.listen(0, "127.0.0.1", done));
  const { port } = server.address();
  if (!keepOpen) await new Promise((done) => server.close(done));
  return { port, server };
}

async function runAsync(ctx, ...args) {
  const { spawn } = await import("node:child_process");
  return new Promise((done) => {
    const child = spawn(process.execPath, [SCRIPT, ...args, "--root", ctx.root], { env: childEnv(ctx) });
    let out = "";
    child.stdout.on("data", (d) => { out += d; });
    child.on("close", (code) => done({ code, json: code === 0 ? JSON.parse(out) : null }));
  });
}

test("check runs with no server, and sees one when it listens", async () => {
  const ctx = setup();
  const closed = await freePort(false);
  writeFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), JSON.stringify({ server: { port: closed.port }, items: [] }));
  const none = await runAsync(ctx, "check");
  assert.equal(none.code, 0);
  assert.equal(none.json.server.listening, false);
  assert.equal(none.json.server.port, closed.port);
  assert.equal(none.json.answers_file, ctx.answers);
  assert.equal(none.json.answers_lines, 0);

  const open = await freePort(true);
  writeFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), JSON.stringify({ server: `http://127.0.0.1:${open.port}`, items: [] }));
  const live = await runAsync(ctx, "check");
  open.server.close();
  assert.equal(live.json.server.listening, true);
});

test("write refuses a v1 thread link with one line, and keeps a v2 link without the list's angle brackets", () => {
  const ctx = setup();
  const v1 = run(ctx, "write", "--input", writeItems(ctx, [{ ...ITEMS[0], thread_link: "t3-thread://v1/abc" }]));
  assert.equal(v1.code, 1);
  assert.equal(v1.err.trim().split("\n").length, 1);
  assert.match(v1.err, /node-plan.*thread_link must be the thread's v2 link/);
  assert.equal(existsSync(join(ctx.root, ".lev", "now", "ceo-board.json")), false);

  const listed = "<t3-thread://v2/f4c99082/mcp:2a6d20df>";
  const ok = run(ctx, "write", "--input", writeItems(ctx, [{ ...ITEMS[0], thread_link: listed }]));
  assert.equal(ok.code, 0, ok.err);
  const board = JSON.parse(readFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), "utf8"));
  assert.equal(board.items[0].thread_link, "t3-thread://v2/f4c99082/mcp:2a6d20df");
});

test("write with an explorer build but no tsx changes nothing and says so in one line", () => {
  const ctx = setup();
  mkdirSync(join(ctx.root, "plugins", "now", "scripts"), { recursive: true });
  writeFileSync(join(ctx.root, "plugins", "now", "scripts", "build-entity-explorer.ts"), "export {};\n");
  const now = join(ctx.root, ".lev", "now");
  const oldBoard = JSON.stringify({ updated: "2026-11-01T00:00:00Z", project: "demo", items: [] });
  writeFileSync(join(now, "ceo-board.json"), oldBoard);
  writeFileSync(join(now, "entity-explorer.html"), "old page");
  const r = run(ctx, "write", "--input", writeItems(ctx, ITEMS));
  assert.equal(r.code, 1);
  assert.deepEqual(r.err.trim().split("\n"), ["board: write: nothing written: tsx not found under plugins/now: run pnpm install"]);
  assert.equal(readFileSync(join(now, "ceo-board.json"), "utf8"), oldBoard);
  assert.equal(readFileSync(join(now, "entity-explorer.html"), "utf8"), "old page");
  assert.deepEqual(readdirSync(now).sort(), ["ceo-board.json", "entity-explorer.html"]);
});

test("write warns when --project names a new board owner", () => {
  const ctx = setup();
  writeFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), JSON.stringify({ project: "alpha", items: [] }));
  const r = run(ctx, "write", "--input", writeItems(ctx, ITEMS), "--project", "beta");
  assert.equal(r.code, 0, r.err);
  assert.match(r.err, /board owner changes from alpha to beta/);
  const same = run(ctx, "write", "--input", writeItems(ctx, ITEMS), "--project", "beta");
  assert.equal(same.err, "");
});

test("answers --since <lines> dedupes over the whole file: an older tap past the cut loses to a newer one before it", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  const filler = Array.from({ length: 8 }, (_, i) => tap("agent37-box", "yes", "Yes", `2026-11-04T03:0${i}:00Z`));
  writeAnswers(ctx, [
    ...filler,                                               // lines 1-8
    tap("node-plan", "hold", "Hold", "2026-11-04T04:20:00Z"), // line 9: newer, before the cut
    tap("agent37-box", "no", "No", "2026-11-04T04:30:00Z"),   // line 10
    tap("node-plan", "go", "Go", "2026-11-04T04:10:00Z"),     // line 11: older, past the cut
  ]);
  const r = run(ctx, "answers", "--since", "10", "--items", items);
  assert.equal(r.code, 0, r.err);
  assert.equal(r.json.lines, 11);
  assert.deepEqual(r.json.rows, []);
  const all = run(ctx, "answers", "--since", "9", "--items", items);
  assert.deepEqual(all.json.rows.map((row) => [row.item_id, row.choice]), [["agent37-box", "no"]]);
});

test("answers --since takes only a line count or an ISO time with a zone", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  for (const bad of ["2026-11-04T04:15:00", "2026-11-04", "yesterday", "Nov 4 2026 04:15 GMT"]) {
    const r = run(ctx, "answers", "--since", bad, "--items", items);
    assert.equal(r.code, 1, bad);
    assert.equal(r.err.trim().split("\n").length, 1, bad);
    assert.match(r.err, /ISO 8601 time with a zone/, bad);
  }
  for (const good of ["2026-11-04T04:15:00Z", "2026-11-04T04:15:00.5+05:30", "0"]) assert.equal(run(ctx, "answers", "--since", good, "--items", items).code, 0, good);
});

/**
 * A stand-in explorer build: a fake tsx whose tsImport is a plain import, and a build that draws the ids of the
 * board file it is handed. The page then shows which board it was built from.
 */
function fakeExplorer(ctx) {
  const now = join(ctx.root, "plugins", "now");
  const api = join(now, "node_modules", "tsx", "esm");
  mkdirSync(api, { recursive: true });
  mkdirSync(join(now, "scripts"), { recursive: true });
  writeFileSync(join(now, "package.json"), JSON.stringify({ name: "now", type: "module" }));
  writeFileSync(join(now, "node_modules", "tsx", "package.json"), JSON.stringify({ name: "tsx", type: "module", exports: { "./esm/api": "./esm/api.mjs" } }));
  writeFileSync(join(api, "api.mjs"), "export const tsImport = (url) => import(url);\n");
  writeFileSync(join(now, "scripts", "build-entity-explorer.ts"), [
    'import { readFileSync } from "node:fs";',
    'export const resolveProject = (_name, root) => ({ root, name: "demo" });',
    'export const collectEntityExplorerData = ({ boardPath }) => ({ waits: { board: JSON.parse(readFileSync(boardPath, "utf8")), board_note: null } });',
    'export const buildEntityExplorerHtml = (data) => `<p>cards: ${data.waits.board.items.map((i) => i.id).join(",")}</p>`;',
    "",
  ].join("\n"));
}

test("write refuses a v2 link T3 cannot open, and keeps a trimmed bracketed one", () => {
  const ctx = setup();
  for (const bad of ["t3-thread://v2/env", "t3-thread://v2/env/", "t3-thread://v2//abc", "t3-thread://v2/env/a b", 't3-thread://v2/env/a"b', "<<t3-thread://v2/env/abc>>"]) {
    const r = run(ctx, "write", "--input", writeItems(ctx, [{ ...ITEMS[0], thread_link: bad }]));
    assert.equal(r.code, 1, bad);
    assert.equal(r.err.trim().split("\n").length, 1, bad);
    assert.match(r.err, /thread_link must be the thread's v2 link/, bad);
  }
  assert.equal(existsSync(join(ctx.root, ".lev", "now", "ceo-board.json")), false);
  const escaped = "t3-thread://v2/f4c99082/thread:delegated-task:command%3Amcp-1";
  const ok = run(ctx, "write", "--input", writeItems(ctx, [{ ...ITEMS[0], thread_link: `  <${escaped}>  ` }]));
  assert.equal(ok.code, 0, ok.err);
  const board = JSON.parse(readFileSync(join(ctx.root, ".lev", "now", "ceo-board.json"), "utf8"));
  assert.equal(board.items[0].thread_link, escaped);
});

test("write builds the page from the new board, then leaves no .tmp file and no scratch folder", () => {
  const ctx = setup();
  fakeExplorer(ctx);
  const now = join(ctx.root, ".lev", "now");
  writeFileSync(join(now, "ceo-board.json"), JSON.stringify({ updated: "2026-11-01T00:00:00Z", project: "demo", items: [{ id: "old-card" }] }));
  writeFileSync(join(now, "entity-explorer.html"), "old page");
  const r = run(ctx, "write", "--input", writeItems(ctx, ITEMS));
  assert.equal(r.code, 0, r.err);
  assert.equal(r.json.page.rebuilt, true);
  assert.equal(r.json.page.board_cards, 2);
  assert.equal(readFileSync(join(now, "entity-explorer.html"), "utf8"), "<p>cards: node-plan,agent37-box</p>");
  assert.deepEqual(JSON.parse(readFileSync(join(now, "ceo-board.json"), "utf8")).items.map((i) => i.id), ["node-plan", "agent37-box"]);
  assert.deepEqual(readdirSync(now).sort(), ["ceo-board.json", "entity-explorer.html"]);
  assert.deepEqual(readdirSync(ctx.tmp), [], "the scratch folder in the temp folder is gone");
});

test("write says 'page written, board not' when only the board rename fails, and leaves no .tmp file", () => {
  const ctx = setup();
  fakeExplorer(ctx);
  const now = join(ctx.root, ".lev", "now");
  mkdirSync(join(now, "ceo-board.json"));
  writeFileSync(join(now, "ceo-board.json", "keep.txt"), "a folder where the board should be");
  const r = run(ctx, "write", "--input", writeItems(ctx, ITEMS));
  assert.equal(r.code, 1);
  const lines = r.err.trim().split("\n");
  assert.equal(lines.length, 1, r.err);
  assert.match(lines[0], /^board: write: page written, board not: /);
  assert.equal(readFileSync(join(now, "entity-explorer.html"), "utf8"), "<p>cards: node-plan,agent37-box</p>");
  assert.deepEqual(readdirSync(now).sort(), ["ceo-board.json", "entity-explorer.html"]);
  assert.deepEqual(readdirSync(join(now, "ceo-board.json")), ["keep.txt"]);
  assert.deepEqual(readdirSync(ctx.tmp), []);
});

test("answers counts a bad line as skipped only past the cut", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  mkdirSync(dirname(ctx.answers), { recursive: true });
  writeFileSync(ctx.answers, ["not json, before the cut", JSON.stringify(tap("node-plan", "go", "Go", "2026-11-04T04:00:00Z")), "not json, past the cut", ""].join("\n"));
  const r = run(ctx, "answers", "--since", "2", "--items", items);
  assert.equal(r.code, 0, r.err);
  assert.equal(r.json.lines, 3);
  assert.equal(r.json.skipped, 1);
  assert.equal(run(ctx, "answers", "--since", "0", "--items", items).json.skipped, 2);
});

test("answers breaks a tie on at by line: the later line wins", () => {
  const ctx = setup();
  const items = writeItems(ctx, ITEMS);
  writeAnswers(ctx, [tap("node-plan", "go", "Go", "2026-11-04T04:00:00Z"), tap("node-plan", "hold", "Hold", "2026-11-04T04:00:00Z")]);
  const r = run(ctx, "answers", "--since", "0", "--items", items);
  assert.deepEqual(r.json.rows.map((row) => [row.item_id, row.choice]), [["node-plan", "hold"]]);
});

test("an error no command catches prints one line and exits 1", () => {
  const ctx = setup();
  mkdirSync(ctx.answers, { recursive: true }); // the answers file is a folder: reading it throws EISDIR
  const r = run(ctx, "answers", "--since", "0", "--items", writeItems(ctx, ITEMS));
  assert.equal(r.code, 1);
  assert.equal(r.err.trim().split("\n").length, 1, r.err);
  assert.match(r.err, /^board: EISDIR/);
});
