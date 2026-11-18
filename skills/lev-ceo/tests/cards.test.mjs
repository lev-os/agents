// Tests of scripts/cards.mjs: the question cards for JP and the relay of his answer. Run: node --test tests/cards.test.mjs
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SCRIPT = join(HERE, "..", "scripts", "cards.mjs");
const QUEUE = join(HERE, "..", "scripts", "queue.mjs");
const NOW = "2026-11-18T08:00:00Z";
const ME = "chat-me";

const run = (script, args) => spawnSync(process.execPath, [script, ...args], { encoding: "utf8" });
const cards = (root, args, status = 0) => {
  const out = run(SCRIPT, [...args, "--thread", ME, "--queue-root", root, "--now", NOW]);
  assert.equal(out.status, status, `exit ${out.status}: ${out.stderr}${out.stdout}`);
  return out;
};
const json = (out) => JSON.parse(out.stdout);
const item = (id, over = {}) => ({
  id, kind: "attention", title: `p > ${id}`, reason: "1 question(s) for JP", threadId: id, priority: 2,
  source: "sweep", project: "p1", questions: ["Q?"], cursor: `r1#40`, ...over,
});
/** A new queue root that holds the items. */
function queueWith(items) {
  const root = mkdtempSync(join(tmpdir(), "cards-"));
  const q = (args) => {
    const out = run(QUEUE, [...args, "--thread", ME, "--root", root, "--now", NOW]);
    assert.equal(out.status, 0, out.stderr);
    return out;
  };
  q(["open", "--title", "the sweep chat"]);
  for (const one of items) q(["put", "--item", JSON.stringify(one)]);
  return root;
}
const folder = (root) => join(root, readdirSync(root).find((name) => name.startsWith("the-sweep-chat")));
const stored = (root) => JSON.parse(readFileSync(join(folder(root), "queue.json"), "utf8")).items;
const bytes = (root) => readFileSync(join(folder(root), "queue.json"), "utf8");
const ask = (over = {}) => ({
  emoji: "🚀", ask: "May the chat merge the branch?", why: "The deploy waits on it.",
  choices: [{ label: "Yes, merge", gain: "Staging is current", cost: null }, { label: "No, wait", gain: null, cost: "The branch gets older" }],
  pick: 0, because: "The checks pass.", experts: ["Trunk-based development"], if_no_answer: "It waits.", yours: false, ...over,
});
const line = (id, over = {}) => ({
  threadId: id, cursor: "r1#40", item_count_now: 40, answered: false, context: "It moves the service to the new host.", asks: [ask()], ...over,
});
function lines(root, list, name = "cards.jsonl") {
  const file = join(root, name);
  writeFileSync(file, list.map((one) => (typeof one === "string" ? one : JSON.stringify(one))).join("\n"));
  return file;
}
const merge = (root, list, status = 0) => cards(root, ["merge", "--cards", lines(root, list)], status);

test("brief lists the open items that have no card for their reply, and prints the brief for a reader", () => {
  const root = queueWith([item("a"), item("b"), item("w", { kind: "watch" })]);
  merge(root, [line("a")]);
  const out = cards(root, ["brief", "--out", join(root, "out.jsonl")]);
  const list = readFileSync(join(folder(root), "cards-to-read.jsonl"), "utf8").trim().split("\n").map((l) => JSON.parse(l));
  assert.deepEqual(list.map((l) => l.threadId), ["b"]);
  assert.deepEqual(list[0], { threadId: "b", cursor: "r1#40", item_count: 40, title: "p > b", questions: ["Q?"] });
  assert.match(out.stdout, /1 chats/);
  assert.match(out.stdout, /out\.jsonl/);
  assert.doesNotMatch(out.stdout, /\{\{/);
});

test("brief with nothing to read ends with exit 2 and writes no list", () => {
  const root = queueWith([item("a")]);
  merge(root, [line("a")]);
  const out = cards(root, ["brief", "--out", join(root, "out.jsonl")], 2);
  assert.match(out.stderr, /no item needs a card/);
  assert.equal(existsSync(join(folder(root), "cards-to-read.jsonl")), false);
});

test("merge stores the asks of a card on its item, for the reply the card was written for", () => {
  const root = queueWith([item("a")]);
  const out = json(merge(root, [line("a")]));
  assert.deepEqual(out, { merged: ["a"], stale: [], not_open: [], answered: [] });
  const [a] = stored(root);
  assert.equal(a.asks_cursor, "r1#40");
  assert.equal(a.asks[0].ask, "May the chat merge the branch?");
  assert.equal(a.context, "It moves the service to the new host.");
  assert.equal(a.card.ask, "May the chat merge the branch?");
  assert.equal(a.card.recommend, "Yes, merge");
  assert.equal(a.card.ifNoAnswer, "It waits.");
  assert.equal(a.status, "pending");
});

test("merge takes no card for an older reply, for a chat with no open item, or for a chat JP answered", () => {
  const root = queueWith([item("a"), item("b"), item("c")]);
  const out = json(merge(root, [line("a", { cursor: "r0#30" }), line("zz"), line("c", { answered: true, asks: [] }), line("b")]));
  assert.deepEqual(out, { merged: ["b"], stale: ["a"], not_open: ["zz"], answered: ["c"] });
  const byId = Object.fromEntries(stored(root).map((i) => [i.id, i]));
  assert.equal(byId.a.asks, undefined);
  assert.equal(byId.c.asks, undefined);
  assert.equal(byId.c.status, "pending");
});

test("merge refuses a card line of the wrong form with exit 2, before any write", () => {
  const bad = [
    "not json",
    "null",
    line("a", { asks: "one" }),
    line("a", { asks: [ask({ ask: 7 })] }),
    line("a", { asks: [ask({ choices: [{ label: 1 }] })] }),
    line("a", { asks: [ask({ choices: [{ label: "x" }, { label: "y" }, { label: "z" }, { label: "q" }] })] }),
    line("a", { asks: [ask({ pick: 2 })] }),
    line("a", { asks: [ask({ pick: "0" })] }),
    line("a", { asks: [ask({ experts: "tmux" })] }),
    line("a", { asks: [ask({ yours: "yes" })] }),
    line("a", { asks: [ask({ if_no_answer: 3 })] }),
    line("a", { answered: "no" }),
    line("a", { context: null }),
    line("a", { cursor: 4 }),
    line("a", { asks: [] }),
  ];
  for (const one of bad) {
    const root = queueWith([item("a"), item("b")]);
    const before = bytes(root);
    const out = merge(root, [line("b"), one], 2);
    assert.match(out.stderr, /^cards: /, JSON.stringify(one));
    assert.doesNotMatch(out.stderr, /\n\s+at /, "no stack trace");
    assert.equal(bytes(root), before, `a write before exit 2: ${JSON.stringify(one)}`);
  }
});

test("batch shows at most five questions of one project, numbers them, and writes the page and its map", () => {
  const two = [ask({ ask: "First of two?" }), ask({ ask: "Second of two?" })];
  const root = queueWith([
    item("a"), item("b"), item("c", { project: "p2" }), item("d"), item("e"), item("f"),
  ]);
  merge(root, [line("a"), line("b", { asks: two }), line("c"), line("d", { asks: [...two, ask({ ask: "Third?" })] }), line("e", { asks: two }), line("f")]);
  const out = json(cards(root, ["batch"]));
  assert.equal(out.batch, 1);
  assert.equal(out.group, "p1");
  assert.deepEqual(out.questions.map((q) => [q.n, q.item]), [[1, "a"], [2, "b"], [3, "b"], [4, "e"], [5, "e"]], "d has 3 questions and does not fit");
  assert.equal(out.left, 5, "d (3), f (1) and c (1) are left");
  const html = readFileSync(out.page, "utf8");
  assert.ok(html.startsWith("<!doctype html>"));
  assert.match(html, /QUESTION 5/);
  assert.doesNotMatch(html, /QUESTION 6/);
  assert.match(html, /Trunk-based development/);
  const map = JSON.parse(readFileSync(out.map, "utf8"));
  assert.equal(map.questions[2].ask, "Second of two?");
  assert.deepEqual(map.questions[2].choices.map((c) => c.key), ["a", "b"]);
});

test("batch does not show a question twice, and the next batch holds what is left", () => {
  const root = queueWith([item("a"), item("b"), item("c", { project: "p2" })]);
  merge(root, [line("a"), line("b"), line("c")]);
  assert.deepEqual(json(cards(root, ["batch"])).questions.map((q) => q.item), ["a", "b"]);
  const second = json(cards(root, ["batch"]));
  assert.equal(second.batch, 2);
  assert.deepEqual(second.questions.map((q) => q.item), ["c"]);
  const third = json(cards(root, ["batch"]));
  assert.deepEqual(third, { batch: null, questions: [], left: 0, no_card: 0 });
  assert.deepEqual(readdirSync(join(folder(root), "batches")).sort(), ["batch-1.html", "batch-1.json", "batch-2.html", "batch-2.json"]);
});

test("batch shows no card that was written for an older reply, and counts it", () => {
  const root = queueWith([item("a"), item("b")]);
  merge(root, [line("a"), line("b")]);
  const moved = run(QUEUE, ["put", "--item", JSON.stringify(item("a", { cursor: "r2#55" })), "--thread", ME, "--root", root, "--now", NOW]);
  assert.equal(moved.status, 0, moved.stderr);
  const out = json(cards(root, ["batch"]));
  assert.deepEqual(out.questions.map((q) => q.item), ["b"]);
  assert.equal(out.no_card, 1);
});

test("the page shows the text of a chat as text, never as markup", () => {
  const root = queueWith([item("a", { title: "p > <b>bold</b>" })]);
  merge(root, [line("a", { asks: [ask({ ask: "Is <script>alert(1)</script> safe?", experts: ["a & b"] })] })]);
  const html = readFileSync(json(cards(root, ["batch"])).page, "utf8");
  assert.doesNotMatch(html, /<script>alert/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.match(html, /a &amp; b/);
  assert.doesNotMatch(html, /<b>bold<\/b>/);
});

test("relay prints JP's words unchanged, marks every other sentence as not his, and writes nothing", () => {
  const root = queueWith([item("a")]);
  merge(root, [line("a")]);
  const before = bytes(root);
  const words = 'yes, but "only" after 5pm — ok?';
  const out = cards(root, ["relay", "--item", "a", "--words", words, "--picks", "1a", "--note", "The chat that relays reads this as a yes."]);
  assert.ok(out.stdout.includes(`JP's words, word for word:\n${words}\n`), out.stdout);
  assert.match(out.stdout, /1\. May the chat merge the branch\?\n {3}His pick: a\. Yes, merge/);
  assert.match(out.stdout, /Not JP's words[^\n]*:\nThe chat that relays reads this as a yes\./);
  assert.match(out.stdout, /the sweep chat/);
  assert.equal(bytes(root), before);
});

test("relay refuses a pick that names no question or no choice, and an item with no card", () => {
  const root = queueWith([item("a"), item("b")]);
  merge(root, [line("a")]);
  for (const picks of ["2a", "1c", "a1", "1"]) {
    assert.match(cards(root, ["relay", "--item", "a", "--words", "yes", "--picks", picks], 2).stderr, /pick/);
  }
  assert.match(cards(root, ["relay", "--item", "b", "--words", "yes"], 2).stderr, /no card/);
  assert.match(cards(root, ["relay", "--item", "zz", "--words", "yes"], 2).stderr, /no item/);
  assert.match(cards(root, ["relay", "--item", "a", "--words", " "], 2).stderr, /--words/);
});

test("relay --sent closes the item with JP's words, and --keep-open records them and leaves it open", () => {
  const root = queueWith([item("a"), item("b")]);
  merge(root, [line("a"), line("b")]);
  cards(root, ["relay", "--item", "a", "--words", "yes do it", "--sent"]);
  cards(root, ["relay", "--item", "b", "--words", "first one yes", "--sent", "--keep-open"]);
  const byId = Object.fromEntries(stored(root).map((i) => [i.id, i]));
  assert.equal(byId.a.status, "done");
  assert.match(byId.a.outcome, /yes do it/);
  assert.deepEqual(byId.a.relayed, [{ at: NOW, words: "yes do it" }]);
  assert.equal(byId.b.status, "pending");
  assert.deepEqual(byId.b.relayed, [{ at: NOW, words: "first one yes" }]);
  assert.match(cards(root, ["relay", "--item", "a", "--words", "again", "--sent"], 2).stderr, /done/);
  assert.match(cards(root, ["relay", "--item", "a", "--words", "again"], 2).stderr, /the item "a" is done/, "no message for a closed item");
});

test("bad input ends with exit 2 and the reason, never a stack trace", () => {
  const root = queueWith([item("a")]);
  const cases = [
    [["nope"], /command must be one of/],
    [["merge"], /--cards/],
    [["merge", "--cards", join(root, "missing.jsonl")], /cannot read/],
    [["merge", "--cards", root], /cannot read/],
    [["brief"], /--out/],
    [["batch", "--size", "0"], /--size/],
    [["batch", "--size"], /./],
  ];
  for (const [args, reason] of cases) {
    const out = cards(root, args, 2);
    assert.match(out.stderr, reason);
    assert.doesNotMatch(out.stderr, /\n\s+at /);
  }
  const none = run(SCRIPT, ["batch", "--thread", "nobody", "--queue-root", root, "--now", NOW]);
  assert.equal(none.status, 2);
  assert.match(none.stderr, /no queue/);
});

test("the program starts no process and opens no connection: it runs under Node's permission system", () => {
  const source = readFileSync(SCRIPT, "utf8");
  for (const name of ["child_process", "worker_threads", "node:net", "node:http", "node:https", "node:dgram", "node:cluster", "getBuiltinModule", "fetch("]) {
    assert.equal(source.includes(name), false, `the program names ${name}`);
  }
  const root = queueWith([item("a")]);
  const file = lines(root, [line("a")]);
  const guarded = (args) => spawnSync(process.execPath, [
    "--permission", "--allow-fs-read=*", `--allow-fs-write=${root}`, `--allow-fs-write=${join(root, "*")}`,
    SCRIPT, ...args, "--thread", ME, "--queue-root", root, "--now", NOW,
  ], { encoding: "utf8" });
  for (const args of [["merge", "--cards", file], ["batch"], ["relay", "--item", "a", "--words", "yes", "--sent"]]) {
    const out = guarded(args);
    assert.equal(out.status, 0, out.stderr);
  }
});
