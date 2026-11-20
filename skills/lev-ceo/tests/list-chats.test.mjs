// list-chats.mjs lists the open top-level chats of every project with the t3 command line, with no model.
// The test gives it a fake t3 program, so it needs no T3 app.
import { test } from "node:test";
import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const SCRIPT = new URL("../scripts/list-chats.mjs", import.meta.url).pathname;
const DIR = mkdtempSync(join(tmpdir(), "list-chats-"));
process.on("exit", () => rmSync(DIR, { recursive: true, force: true }));

const row = (threadId, more = {}) => ({ threadId, title: threadId, status: "completed", settled: false, parentThreadId: null, itemCount: 5, updatedAt: "2026-11-20T01:00:00.000Z", ...more });
const lists = {
  p1: [row("a"), row("worker", { parentThreadId: "a", relationshipToParent: "subagent" }), row("closed", { settled: true }), row("forked", { parentThreadId: "a", relationshipToParent: "fork" }), row("imported", { parentThreadId: "import:codex:1" })],
  p2: [row("b", { itemCount: 9 })],
};
// The fake t3: `t3 thread list --project <id> --json` prints that project's rows; project "bad" fails.
const fake = join(DIR, "fake-t3.mjs");
writeFileSync(fake, `#!/usr/bin/env node
const lists = ${JSON.stringify(lists)};
const id = process.argv[process.argv.indexOf("--project") + 1];
if (!lists[id]) { console.error("No T3 Code project matches"); process.exit(1); }
console.log(JSON.stringify(lists[id]));
`);
chmodSync(fake, 0o755);
const projects = (ids) => {
  const file = join(DIR, `projects-${ids.join("-")}.json`);
  writeFileSync(file, JSON.stringify({ projects: ids.map((id) => ({ id, title: id })) }));
  return file;
};
const run = (ids, name) => {
  const out = join(DIR, `${name}.json`);
  const done = spawnSync("node", [SCRIPT, "--projects", projects(ids), "--out", out, "--t3", fake], { encoding: "utf8" });
  return { done, out };
};

test("it writes one list of every project's open top-level chats, in the form the scan takes", () => {
  const { done, out } = run(["p1", "p2"], "ok");
  assert.equal(done.status, 0, done.stderr);
  const list = JSON.parse(readFileSync(out, "utf8"));
  assert.deepEqual(list.threads.map((t) => t.threadId).sort(), ["a", "b", "forked", "imported"]);
  assert.equal(list.total, 4);
  assert.equal(list.nextCursor, null);
  assert.equal(list.threads.find((t) => t.threadId === "b").projectId, "p2");
});

test("a project that cannot be listed stops the run and writes no file: a missing chat would count as closed", () => {
  const { done, out } = run(["p1", "bad"], "bad");
  assert.equal(done.status, 1);
  assert.match(done.stderr, /bad/);
  assert.throws(() => readFileSync(out, "utf8"));
});
