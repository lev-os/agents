// Tests for scripts/queue.mjs. Run: node --test ~/.agents/skills/lev-ceo/tests/queue.test.mjs
// Each test runs the script as the CEO does (a child process) against its own temp --root.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join } from "node:path";
import { afterEach, beforeEach, test } from "node:test";
import { fileURLToPath } from "node:url";

import { slugify } from "../scripts/queue.mjs";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "queue.mjs");
const T0 = "2026-11-10T23:30:00Z";
const at = (min) => new Date(Date.parse(T0) + min * 60_000).toISOString().replace(/\.000Z$/, "Z");
const CEO = "mcp:ceo-thread";

let root;
beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "queue-test-"));
});
afterEach(() => rmSync(root, { recursive: true, force: true }));

function q(args, { now = T0, thread = CEO, status = 0 } = {}) {
  const run = spawnSync(process.execPath, [SCRIPT, ...args, "--thread", thread, "--now", now, "--root", root], { encoding: "utf8" });
  assert.equal(run.status, status, `exit ${run.status} for ${args.join(" ")}: ${run.stderr}${run.stdout}`);
  if (status !== 0) return run.stderr;
  return args.includes("--text") ? run.stdout : JSON.parse(run.stdout);
}
const openQueue = (opts) => q(["open", "--title", "CEO > suntiq"], opts);
const item = (id, over = {}) => ({ id, kind: "attention", title: `chat ${id}`, reason: `why ${id}`, ...over });
const put = (it, opts, ...extra) => q(["put", "--item", JSON.stringify(it), ...extra], opts);
const queueFile = (dir) => JSON.parse(readFileSync(join(dir, "queue.json"), "utf8"));
const events = (dir) => readFileSync(join(dir, "events.jsonl"), "utf8").trim().split("\n").map((line) => JSON.parse(line));

test("slug: lower case, each run of other characters is one dash, trimmed", () => {
  assert.equal(slugify("CEO > suntiq"), "ceo-suntiq");
  assert.equal(slugify("  Lev: groups / build!! "), "lev-groups-build");
});

test("open makes <slug>-<stamp> and reuses it for the same thread", () => {
  const first = openQueue();
  assert.equal(first.created, true);
  assert.equal(basename(first.path), "ceo-suntiq-20261110T2330Z");
  const queue = queueFile(first.path);
  assert.deepEqual(queue.chat, { threadId: CEO, title: "CEO > suntiq", slug: "ceo-suntiq" });
  assert.deepEqual(queue.cadence, { refreshEveryMin: 60, hygieneEveryMin: 180 });
  assert.equal(queue.lastRefreshAt, null);
  const again = openQueue({ now: at(90) });
  assert.deepEqual(again, { path: first.path, created: false });
  assert.equal(readdirSync(root).length, 1);
});

test("open keeps a queue file another writer made, items included", () => {
  const dir = join(root, "ceo-suntiq-20261110T2330Z");
  mkdirSync(dir);
  const made = { version: 1, chat: { threadId: CEO, title: "CEO > suntiq", slug: "ceo-suntiq" }, createdAt: T0, updatedAt: T0, cadence: { refreshEveryMin: 60, hygieneEveryMin: 180 }, lastRefreshAt: null, lastHygieneAt: null, items: [{ ...item("a"), threadId: null, link: null, priority: 1, status: "pending", card: { goal: "g", state: null, ask: null, recommend: null, ifNoAnswer: null }, addedAt: T0, updatedAt: T0 }] };
  writeFileSync(join(dir, "queue.json"), JSON.stringify(made));
  assert.deepEqual(openQueue({ now: at(5) }), { path: dir, created: false });
  assert.deepEqual(queueFile(dir), made);
  assert.deepEqual(q(["show"]).items.map((it) => it.id), ["a"]);
});

test("a second thread gets its own folder", () => {
  const one = openQueue();
  const two = q(["open", "--title", "CEO > leviathan"], { thread: "mcp:other", now: at(1) });
  assert.equal(two.created, true);
  assert.notEqual(one.path, two.path);
  assert.equal(basename(two.path), "ceo-leviathan-20261110T2331Z");
  put(item("x"), { thread: "mcp:other" });
  assert.equal(q(["show"]).items.length, 0);
  assert.equal(q(["show"], { thread: "mcp:other" }).items.length, 1);
});

test("put adds with pending and addedAt, then upserts by id", () => {
  const { path } = openQueue();
  const added = put(item("a", { priority: 1, threadId: "mcp:a" }));
  assert.equal(added.added, true);
  assert.equal(added.item.status, "pending");
  assert.equal(added.item.addedAt, T0);
  assert.deepEqual(added.item.card, { goal: null, state: null, ask: null, recommend: null, ifNoAnswer: null });
  const updated = put(item("a", { reason: "new reason", card: { ask: "merge?" } }), { now: at(10) });
  assert.equal(updated.added, false);
  assert.equal(updated.item.reason, "new reason");
  assert.equal(updated.item.addedAt, T0, "an upsert keeps addedAt");
  assert.equal(updated.item.priority, 1, "an upsert keeps fields it does not name");
  assert.equal(updated.item.card.ask, "merge?");
  assert.equal(queueFile(path).items.length, 1);
});

test("put refuses an item without id, kind, title or reason, and a bad kind", () => {
  openQueue();
  for (const key of ["id", "kind", "title", "reason"]) {
    const bad = item("a");
    delete bad[key];
    assert.match(put(bad, { status: 2 }), new RegExp(`no ${key}`));
  }
  assert.match(put(item("a", { kind: "other" }), { status: 2 }), /kind/);
  assert.match(q(["put", "--item", "{not json"], { status: 2 }), /not JSON/);
  assert.equal(q(["show"]).items.length, 0);
});

test("put on a done item needs --reopen", () => {
  openQueue();
  put(item("a"));
  q(["next"]);
  q(["resolve", "--item", "a", "--to", "done", "--note", "merged"]);
  assert.match(put(item("a"), { status: 2 }), /--reopen/);
  const back = put(item("a", { reason: "came back" }), { now: at(5) }, "--reopen");
  assert.equal(back.item.status, "pending");
  assert.equal(back.item.doneAt, undefined);
});

test("next picks priority, then addedAt, and the presented head stays the head", () => {
  openQueue();
  put(item("low", { priority: 3 }), { now: at(0) });
  put(item("old2", { priority: 2 }), { now: at(1) });
  put(item("new2", { priority: 2 }), { now: at(2) });
  put(item("top", { priority: 1 }), { now: at(3) });
  const first = q(["next"], { now: at(4) });
  assert.equal(first.item.id, "top");
  assert.equal(first.item.status, "presented");
  assert.equal(first.left, 3);
  assert.deepEqual(first.leftTitles, ["chat old2", "chat new2", "chat low"]);
  put(item("urgent", { priority: 1 }), { now: at(5) });
  assert.equal(q(["next"], { now: at(6) }).item.id, "top", "a presented item stays the head until resolved");
  q(["resolve", "--item", "top", "--to", "done", "--note", "answered"], { now: at(7) });
  assert.equal(q(["next"], { now: at(8) }).item.id, "urgent");
  q(["resolve", "--item", "urgent", "--to", "waiting", "--note", "asked JP"], { now: at(9) });
  assert.equal(q(["next"], { now: at(10) }).item.id, "old2");
  q(["resolve", "--item", "old2", "--to", "dropped", "--note", "not needed"], { now: at(11) });
  assert.equal(q(["next"], { now: at(12) }).item.id, "new2");
  assert.deepEqual(q(["show"]).items.map((it) => it.id), ["new2", "low", "urgent"]);
});

test("next on an empty queue returns no item and writes nothing", () => {
  const { path } = openQueue();
  assert.deepEqual(q(["next"]), { item: null, left: 0, leftTitles: [] });
  assert.equal(events(path).length, 1);
});

test("resolve: allowed moves set their stamps; other moves are refused", () => {
  openQueue();
  put(item("a"));
  assert.match(q(["resolve", "--item", "a", "--to", "done", "--note", "x"], { status: 2 }), /pending -> done/);
  q(["next"], { now: at(1) });
  const done = q(["resolve", "--item", "a", "--to", "done", "--note", "merged PR"], { now: at(2) }).item;
  assert.equal(done.doneAt, at(2));
  assert.equal(done.outcome, "merged PR");
  assert.match(q(["resolve", "--item", "a", "--to", "pending", "--note", "x"], { status: 2 }), /done -> pending/);

  put(item("b"));
  q(["next"], { now: at(3) });
  q(["resolve", "--item", "b", "--to", "waiting", "--note", "on JP"], { now: at(4) });
  assert.match(q(["resolve", "--item", "b", "--to", "waiting", "--note", "x"], { status: 2 }), /waiting -> waiting/);
  assert.equal(q(["resolve", "--item", "b", "--to", "pending", "--note", "JP answered"], { now: at(5) }).item.status, "pending");
  q(["next"], { now: at(6) });
  assert.equal(q(["resolve", "--item", "b", "--to", "pending", "--note", "later"], { now: at(7) }).item.status, "pending");

  assert.match(q(["resolve", "--item", "nope", "--to", "done", "--note", "x"], { status: 2 }), /no item/);
  assert.match(q(["resolve", "--item", "b", "--to", "presented", "--note", "x"], { status: 2 }), /--to must be/);
  assert.match(q(["resolve", "--item", "b", "--to", "done"], { status: 2 }), /--note/);
});

test("due: both due at first, then at 60 and 180 minutes after ran", () => {
  openQueue();
  assert.deepEqual(q(["due"]), { refresh: true, hygiene: true });
  assert.deepEqual(q(["ran", "--kind", "refresh"]), { lastRefreshAt: T0 });
  assert.deepEqual(q(["ran", "--kind", "hygiene"]), { lastHygieneAt: T0 });
  assert.deepEqual(q(["due"], { now: at(59) }), { refresh: false, hygiene: false });
  assert.deepEqual(q(["due"], { now: at(60) }), { refresh: true, hygiene: false });
  q(["ran", "--kind", "refresh"], { now: at(60) });
  assert.deepEqual(q(["due"], { now: at(119) }), { refresh: false, hygiene: false });
  q(["ran", "--kind", "refresh"], { now: at(120) });
  assert.deepEqual(q(["due"], { now: at(179) }), { refresh: false, hygiene: false });
  assert.deepEqual(q(["due"], { now: at(180) }), { refresh: true, hygiene: true });
  assert.match(q(["ran", "--kind", "other"], { status: 2 }), /--kind/);
});

test("events.jsonl gets one line per change, and no temp file stays after a write", () => {
  const { path } = openQueue();
  put(item("a"), { now: at(1) });
  put(item("a", { reason: "r2" }), { now: at(2) });
  q(["next"], { now: at(3) });
  q(["next"], { now: at(4) }); // no change: no line
  q(["show"], { now: at(4) }); // a read: no line
  q(["due"], { now: at(4) }); // a read: no line
  q(["resolve", "--item", "a", "--to", "done", "--note", "ok"], { now: at(5) });
  q(["ran", "--kind", "refresh"], { now: at(6) });
  put(item("a"), { now: at(7), status: 2 }); // refused: no line
  const lines = events(path);
  assert.deepEqual(lines.map((e) => [e.item, e.from, e.to]), [
    [null, null, "open"],
    ["a", null, "pending"],
    ["a", "pending", "pending"],
    ["a", "pending", "presented"],
    ["a", "presented", "done"],
    [null, null, at(6)],
  ]);
  for (const line of lines) assert.deepEqual(Object.keys(line), ["at", "item", "from", "to", "note"]);
  assert.deepEqual(readdirSync(path).sort(), ["events.jsonl", "queue.json"]);
});

test("show --text prints one line per open item, in queue order", () => {
  openQueue();
  put(item("a", { priority: 2 }), { now: at(1) });
  put(item("b", { priority: 1, kind: "settle", members: ["mcp:1", "mcp:2"] }), { now: at(2) });
  q(["next"], { now: at(3) });
  assert.equal(q(["show", "--text"]), "1. presented settle p1 chat b — why b\n2. pending attention p2 chat a — why a\n");
});

test("a command on a thread with no queue exits 2", () => {
  assert.match(q(["show"], { status: 2 }), /run open first/);
  assert.match(q(["bogus"], { status: 2 }), /command must be/);
});
