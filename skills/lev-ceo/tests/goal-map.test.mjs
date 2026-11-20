// goal-map.mjs draws the goal map from its data file and checks that each open chat has one place on it.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const SCRIPT = new URL("../scripts/goal-map.mjs", import.meta.url).pathname;
const EXAMPLE = new URL("../references/goal-map-example.json", import.meta.url).pathname;
const DIR = mkdtempSync(join(tmpdir(), "goal-map-"));
process.on("exit", () => rmSync(DIR, { recursive: true, force: true }));

const map = {
  context: [{ title: "You", text: "say an outcome" }, { title: "Lev", text: "makes it true" }],
  sections: [{
    title: "Lev", note: "the note",
    goals: [
      { name: "One owner", end: [{ text: "The daemon keeps <listed> processes alive." }, { text: "A second part.", source: "my reading" }], chats: [{ title: "lev > daemon", id: "t-daemon" }, { title: "lev > pool" }] },
      { name: "Survival", end: [{ text: "Version 1.0 is approved." }], chats: [{ title: "survival > store", elsewhere: "MacBook" }, { title: "lev > closed" }] },
    ],
  }],
  laws: [{ name: "One owner.", text: "Each thing lives in the module that owns it." }],
  example: { title: "The daemon chat", today: { title: "Its goal today", text: "Finish the daemon." }, should: { title: "The goal it should have", text: "Each part lives where it belongs." } },
};
const write = (name, value) => { const file = join(DIR, name); writeFileSync(file, JSON.stringify(value)); return file; };
const threads = (rows) => ({ threads: rows.map(([threadId, title]) => ({ threadId, title })) });
const run = (...args) => spawnSync("node", [SCRIPT, ...args], { encoding: "utf8" });

test("check passes when each open chat has one place; a chat on another machine and the CEO chat itself are not counted", () => {
  const done = run("check", "--map", write("map.json", map), "--threads", write("ok.json", threads([["t-daemon", "lev > daemon (renamed)"], ["t2", "lev > pool"], ["self", "CEO > global"]])), "--self", "self");
  assert.equal(done.status, 0, done.stderr + done.stdout);
  const out = JSON.parse(done.stdout);
  assert.equal(out.placed, 2);
  assert.deepEqual(out.unplaced, []);
  assert.deepEqual(out.gone, ["lev > closed"]);
});

test("check exits 1 and names an open chat that has no place on the map, and a chat that is on it twice", () => {
  const twice = structuredClone(map);
  twice.sections[0].goals[1].chats.push({ title: "lev > pool" });
  const done = run("check", "--map", write("twice.json", twice), "--threads", write("new.json", threads([["t-daemon", "lev > daemon"], ["t2", "lev > pool"], ["t3", "lev > brand new"]])));
  assert.equal(done.status, 1);
  const out = JSON.parse(done.stdout);
  assert.deepEqual(out.unplaced, [{ title: "lev > brand new", id: "t3" }]);
  assert.deepEqual(out.twice, ["lev > pool"]);
});

test("render writes one page with each goal, its end state, its source mark, each chat, each law and the example, with text escaped", () => {
  const out = join(DIR, "map.html");
  const done = run("render", "--map", write("render.json", map), "--out", out);
  assert.equal(done.status, 0, done.stderr);
  const html = readFileSync(out, "utf8");
  assert.ok(html.startsWith("<!doctype html>"));
  for (const part of ["One owner", "The daemon keeps &lt;listed&gt; processes alive.", "(my reading)", "<i>lev &gt; daemon</i>", "survival &gt; store (MacBook)", "<b>One owner.</b>", "Its goal today", "Each part lives where it belongs."]) {
    assert.ok(html.includes(part), `the page lacks: ${part}`);
  }
});

test("a map with a goal that has no end state is refused: a goal with no end state is a list of chats, not a goal", () => {
  const bad = structuredClone(map);
  bad.sections[0].goals[0].end = [];
  const done = run("render", "--map", write("bad.json", bad), "--out", join(DIR, "bad.html"));
  assert.equal(done.status, 2);
  assert.match(done.stderr, /One owner.*no end state/);
});

test("the example in the skill, the map JP accepted on 2026-11-20, renders", () => {
  const done = run("render", "--map", EXAMPLE, "--out", join(DIR, "example.html"));
  assert.equal(done.status, 0, done.stderr);
  assert.ok(readFileSync(join(DIR, "example.html"), "utf8").includes("A core where each thing has one owner"));
});
