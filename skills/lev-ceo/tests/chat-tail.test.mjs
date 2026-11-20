// chat-tail.mjs prints a chat's state and the end of its last long reply through the t3 command line.
// The test gives it a fake t3 program, so it needs no T3 app.
import { test } from "node:test";
import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const SCRIPT = new URL("../scripts/chat-tail.mjs", import.meta.url).pathname;
const DIR = mkdtempSync(join(tmpdir(), "chat-tail-"));
process.on("exit", () => rmSync(DIR, { recursive: true, force: true }));

const long = "x".repeat(300);
const chats = {
  asks: { thread: { title: "a > asks", status: "completed", activeRunId: null, pendingRequestCount: 0, updatedAt: "2026-11-20T01:00:00.000Z" },
    messages: [{ role: "user", text: "do   the\nthing" }, { role: "assistant", text: `${long} work done.\n**For you:**\n1. **May I push?**` }, { role: "assistant", text: "ok" }] },
  runs: { thread: { title: "b > runs", status: "running", activeRunId: "run-1", pendingRequestCount: 2, updatedAt: "2026-11-20T01:05:00.000Z" },
    messages: [{ role: "assistant", text: `${long} the end of a reply with no question` }] },
};
const fake = join(DIR, "fake-t3.mjs");
writeFileSync(fake, `#!/usr/bin/env node
const chats = ${JSON.stringify(chats)};
const id = process.argv[process.argv.indexOf("show") + 1];
if (!chats[id]) { console.error("No thread matches " + id); process.exit(1); }
console.log(JSON.stringify(chats[id]));
`);
chmodSync(fake, 0o755);
const run = (...more) => {
  const done = spawnSync("node", [SCRIPT, "--t3", fake, ...more], { encoding: "utf8" });
  return { done, rows: done.stdout.trim().split("\n").filter(Boolean).map((line) => JSON.parse(line)) };
};

test("the tail starts at the last For you of the last long reply, and a short closing line is not the reply", () => {
  const { done, rows } = run("asks");
  assert.equal(done.status, 0, done.stderr);
  assert.equal(rows[0].tail, "**For you:**\n1. **May I push?**");
  assert.equal(rows[0].last_user, "do the thing");
  assert.equal(rows[0].running, false);
  assert.equal(rows[0].title, "a > asks");
});

test("a reply with no question gives its last characters, cut at --max, with the run state and the waiting requests", () => {
  const { rows } = run("--max", "11", "runs");
  assert.equal(rows[0].tail, "no question");
  assert.equal(rows[0].running, true);
  assert.equal(rows[0].pending, 2);
});

test("a chat that cannot be read gets an error line and exit 1, and the other chats are still printed", () => {
  const { done, rows } = run("gone", "asks");
  assert.equal(done.status, 1);
  assert.match(rows[0].error, /No thread matches gone/);
  assert.equal(rows[1].thread_id, "asks");
});
