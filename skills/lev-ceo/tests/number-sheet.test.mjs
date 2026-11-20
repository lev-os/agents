// A sheet counts its cards from 1 (JP 2026-11-20: "2b i dont wanna maintain the sheet"). The permanent id of each
// question stays in a map file beside the sheet, so an answer by number finds its question.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";

const SCRIPT = new URL("../scripts/number-sheet.mjs", import.meta.url).pathname;
const DIR = mkdtempSync(join(tmpdir(), "number-sheet-"));
process.on("exit", () => rmSync(DIR, { recursive: true, force: true }));

const question = (id, n) => ({ id, n, emoji: "🔎", ask: `ask ${id}`, choices: [], rec: null, chat: "a chat", yours: false });
const run = (sheet) => {
  const file = join(DIR, `sheet-${sheet.sheet}.json`);
  writeFileSync(file, JSON.stringify(sheet));
  execFileSync("node", [SCRIPT, file]);
  return { sheet: JSON.parse(readFileSync(file, "utf8")), map: JSON.parse(readFileSync(join(DIR, `sheet-${sheet.sheet}.map.json`), "utf8")) };
};

test("cards count from 1 in the order shown, and the send card takes the last number", () => {
  const out = run({
    sheet: 8,
    first_number: 91,
    last_number: 112,
    groups: [
      { mark: "🔴", title: "one", note: null, questions: [question("q-75", 75), question("q-91", 91)] },
      { mark: "🔵", title: "two", note: null, questions: [question("q-66", 66)] },
    ],
    pins: [],
    send: { id: "send-8", n: 112, wording: "w", chats: ["a"] },
  });
  assert.deepEqual(out.sheet.groups.map((g) => g.questions.map((q) => q.n)), [[1, 2], [3]]);
  assert.equal(out.sheet.send.n, 4);
  assert.equal(out.sheet.first_number, undefined);
  assert.equal(out.sheet.last_number, undefined);
  assert.deepEqual(out.map, { sheet: 8, numbers: { 1: "q-75", 2: "q-91", 3: "q-66", 4: "send-8" } });
});

test("a question with no permanent id stops the run, so no answer can lose its question", () => {
  const bad = { sheet: 9, groups: [{ mark: "🔴", title: "one", note: null, questions: [{ ...question("x", 5), id: undefined }] }], pins: [] };
  assert.throws(() => run(bad), /has no id/);
});

test("the same id two times stops the run", () => {
  const bad = { sheet: 10, groups: [{ mark: "🔴", title: "one", note: null, questions: [question("q-1", 1), question("q-1", 2)] }], pins: [] };
  assert.throws(() => run(bad), /two times/);
});

// JP 2026-11-20: "these questions are stale", "I DID THIS SHIT ALREADY", "YOU FUCKING DO IT". Four of six errand
// cards were not true or not his to do. So a card reaches him only with proof and a fresh check.
const fresh = (id, n, more = {}) => ({ ...question(id, n), checked_at: "2026-11-20T01:00Z", ...more });
const strict = (sheet, now = "2026-11-20T01:30Z") => {
  const file = join(DIR, `strict-${sheet.sheet}.json`);
  writeFileSync(file, JSON.stringify(sheet));
  return execFileSync("node", [SCRIPT, file, "--strict", "--now", now], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
};
const one = (q, n = 20) => ({ sheet: n, groups: [{ mark: "🔴", title: "one", note: null, questions: [q] }], pins: [] });

test("strict: an errand card with no proof that an agent tried is refused", () => {
  assert.throws(() => strict(one(fresh("q-1", 1, { yours: true }), 20)), /no proof/);
  strict(one(fresh("q-1", 1, { yours: true, proof: "agent-desktop press on the system dialog is denied: it needs his password" }), 21));
});

test("strict: a card whose chat was last checked over 60 minutes ago is refused", () => {
  assert.throws(() => strict(one(fresh("q-1", 1, { checked_at: "2026-11-19T17:21Z" }), 22)), /checked 4\d\d minutes ago/);
  assert.throws(() => strict(one(question("q-1", 1), 23)), /never checked/);
});

test("without --strict a sheet with no check times still gets its numbers", () => {
  const out = run({ sheet: 24, groups: [{ mark: "🔴", title: "one", note: null, questions: [question("q-1", 9)] }], pins: [] });
  assert.equal(out.sheet.groups[0].questions[0].n, 1);
});
