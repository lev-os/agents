// Tests for scripts/for-you-form.mjs and scripts/for-you-check.mjs. Run: node --test tests/for-you-check.test.mjs
// The form cases come from 47 saved replies that a reader judged on 2026-11-21.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { checkForYouForm } from "../scripts/for-you-form.mjs";

const scripts = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts");
const kinds = (text) => checkForYouForm(text).faults.map((fault) => fault.fault);
const FULL = "**For you:**\n1. **Is the design the one to build from?**\n  It is the foundation.\n  - **I recommend yes**, because it is read.\n  - **What 3 design experts say:**\n    - Ubl: review first.\n";
const BARE = "I need two calls from you:\n\n1. **How much Lev before release?** A: freeze Lev. B: fix the case first.\n2. **Who signs the build?** A: you. B: the machine.\n";

test("a full For you item has no fault", () => {
  assert.deepEqual(kinds(FULL), []);
});

test("the older heading Your turn is the same section, so its questions are no bare list", () => {
  const reply = "Done.\n\n**Your turn:**\n1. **Which call screen do we build toward?**\n2. **Do we keep the old one?**\n";
  assert.ok(!kinds(reply).includes("bare_list"), "questions under Your turn are items");
  assert.ok(kinds(reply).includes("item_incomplete"), "and each item is checked for its parts");
});

test("an item names each part it lacks", () => {
  const reply = "**For you:**\n1. **Pick the supervisor**\n  It restarts the daemon.\n";
  assert.deepEqual(checkForYouForm(reply).faults[0].missing, ["question mark", "recommendation", "expert lines"]);
});

test("expert lines count under the labels that replies use: practices say, products do, examples show", () => {
  const item = (label) => `**For you:**\n1. **Which supervisor?**\n  - **I recommend a.**\n  - **${label}**\n    - systemd: restarts with a limit.\n`;
  assert.deepEqual(kinds(item("What 3 process-supervision practices say:")), []);
  assert.deepEqual(kinds(item("What 2 products do (from memory, not fetched):")), []);
  assert.deepEqual(kinds(item("What 5 product design examples show:")), []);
});

test("a recommendation on the first line of the item counts", () => {
  const reply = "**For you:**\n1. **Where does a reviewer read the proof?** I recommend the commit's Tested line.\n  - **What 2 review experts say:**\n    - Google: evidence beside the claim.\n";
  assert.deepEqual(kinds(reply), []);
});

test("list lines with a bold question and more text after it are a bare list outside For you", () => {
  assert.deepEqual(kinds(BARE), ["bare_list"]);
});

test("one question in a list, a quoted question and a question in a code block are no bare list", () => {
  const reply = "- Is that acceptable?\n> 1. Why?\n> 2. When?\n```\n- a?\n- b?\n```\n";
  assert.deepEqual(kinds(reply), []);
});

test("the form file imports nothing, so a mod can hold a copy of it", () => {
  const source = readFileSync(join(scripts, "for-you-form.mjs"), "utf8");
  assert.equal(/^\s*import\b|\bimport\s*\(|\brequire\s*\(|\bprocess\./m.test(source), false);
});

test("the command exits 1 for a reply with a fault and 0 for a clean one, and counts saved replies", () => {
  const dir = mkdtempSync(join(tmpdir(), "for-you-check-"));
  const run = (...args) => spawnSync(process.execPath, [join(scripts, "for-you-check.mjs"), ...args], { encoding: "utf8" });
  writeFileSync(join(dir, "bare.txt"), BARE);
  writeFileSync(join(dir, "full.txt"), FULL);
  writeFileSync(join(dir, "replies.jsonl"), `${JSON.stringify({ id: "a", reply: BARE })}\n${JSON.stringify({ id: "b", reply: FULL })}\n`);
  assert.equal(run("--text", join(dir, "bare.txt")).status, 1);
  assert.equal(run("--text", join(dir, "full.txt")).status, 0);
  const counted = run(join(dir, "replies.jsonl"));
  assert.equal(counted.status, 0);
  assert.deepEqual(JSON.parse(counted.stdout.split("\n")[0]), { replies: 2, with_for_you: 1, with_bare_list: 1, with_incomplete_item: 0, clean_for_you: 1 });
  assert.equal(run().status, 2);
});
