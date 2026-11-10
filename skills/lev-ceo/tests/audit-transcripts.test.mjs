// Tests for scripts/audit-transcripts.mjs. Run: node --test ~/.agents/skills/lev-ceo/tests/audit-transcripts.test.mjs
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { after, test } from "node:test";
import { fileURLToPath } from "node:url";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "audit-transcripts.mjs");
const dir = mkdtempSync(join(tmpdir(), "audit-test-"));
after(() => rmSync(dir, { recursive: true, force: true }));

let minute = 0;
const at = () => `2026-11-05T00:${String(minute++).padStart(2, "0")}:00Z`;
const human = (text) => ({ type: "user", timestamp: at(), message: { content: text } });
const toolResult = () => ({ type: "user", timestamp: at(), message: { content: [{ type: "tool_result", content: "ok" }] } });
const says = (text) => ({ type: "assistant", timestamp: at(), message: { content: [{ type: "text", text }] } });
const calls = (name, input) => ({ type: "assistant", timestamp: at(), message: { content: [{ type: "tool_use", name, input }] } });
const QUESTION = "1. **May I add one test person on the staging server?**\n---\n🧙🏽‍♂️ **[lev://mesh]** x | ⚡ WAITING ON JP | captured 📝";

const transcript = [
  human("yes settle the chats"),                                            // line 1: a settle order from JP
  calls("mcp__t3-code__t3_thread_organize", { action: "settle", threadId: "a" }),
  toolResult(),
  says(QUESTION),
  human("15-minute watch for the Leviathan CEO node (lev-ceo skill)"),      // line 5: a tick that only reads
  calls("mcp__t3-code__t3_thread_read", { threadId: "a" }),
  toolResult(),
  says("No change."),
  human("15-minute watch for the Leviathan CEO node (lev-ceo skill)"),      // line 9: a tick that commits
  calls("Bash", { command: "git commit -m x -- file" }),
  toolResult(),
  says(QUESTION),                                                           // the same question a second time
  human("<task-notification> <task-id>b1</task-id>"),                       // line 13: a wake
  says("Nothing new."),
];

test("it counts ticks that changed nothing, settle orders and repeated questions, with line numbers", () => {
  const file = join(dir, "session.jsonl");
  writeFileSync(file, `${transcript.map((row) => JSON.stringify(row)).join("\n")}\n`);
  const out = join(dir, "report.json");
  const run = spawnSync(process.execPath, [SCRIPT, "--since", "2026-11-01T00:00:00Z", "--out", out, `s=${file}`], { encoding: "utf8" });
  assert.equal(run.status, 0, run.stderr);
  const s = JSON.parse(readFileSync(out, "utf8")).sessions.s;

  assert.deepEqual(s.turns, { total: 4, jp: 1, tick: 2, wake: 1, relay: 0, compaction: 0 });
  assert.equal(s.ticks.changed_nothing, 1);
  assert.deepEqual(s.ticks.changed_nothing_refs, ["s:L5"]);
  assert.deepEqual(s.ticks.changed_something_refs, ["s:L9"]);
  assert.deepEqual(s.wakes, { total: 1, changed_nothing: 1 });
  assert.deepEqual(s.settle_orders.map((o) => o.ref), ["s:L1"]);
  assert.deepEqual(s.settle_calls, [{ ref: "s:L1", at: "2026-11-05T00:00:00Z", on: "jp", count: 1 }]);
  assert.deepEqual(s.questions.repeated.map((q) => [q.times, q.refs]), [[2, ["s:L1", "s:L9"]]]);
  assert.deepEqual(s.rules.mesh_line_on_every_reply, { replies: 1, with_mesh_line: 1, missing_refs: [] });
});
