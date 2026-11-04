// Run: node --test ~/.agents/skills/lev-ceo/tests/
// Every case runs the board command line in a temp folder, with XDG_STATE_HOME pointed at a temp folder,
// so the real answers file and the real board are never read or written.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "board.mjs");

function setup() {
  const root = mkdtempSync(join(tmpdir(), "board-test-"));
  mkdirSync(join(root, ".lev", "now"), { recursive: true });
  const state = join(root, "state");
  return { root, state, answers: join(state, "lev", "ceo-board", "answers.jsonl") };
}

function run(ctx, ...args) {
  const r = spawnSync(process.execPath, [SCRIPT, ...args, "--root", ctx.root], { encoding: "utf8", env: { ...process.env, XDG_STATE_HOME: ctx.state } });
  return { code: r.status, out: r.stdout, err: r.stderr, json: r.status === 0 && r.stdout ? JSON.parse(r.stdout) : null };
}

const ITEMS = [
  { id: "node-plan", title: "Go on the Node plan", thread_link: "t3-thread://v1/abc", what: "Go or hold.", choices: [{ id: "go", label: "Go" }, { id: "hold", label: "Hold" }], recommended: "go", since: "2026-11-04T00:09:00Z" },
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
    const child = spawn(process.execPath, [SCRIPT, ...args, "--root", ctx.root], { env: { ...process.env, XDG_STATE_HOME: ctx.state } });
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
