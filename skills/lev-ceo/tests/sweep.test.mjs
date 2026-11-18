// Tests for scripts/sweep.mjs. Run: node --test ~/.agents/skills/lev-ceo/tests/sweep.test.mjs
// The choice cases call the functions; the command cases run the script as the CEO does (a child process)
// against a temp --root.
import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { chmodSync, existsSync, mkdtempSync, readdirSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { afterEach, beforeEach, test } from "node:test";
import { fileURLToPath } from "node:url";

import { checkList, choose } from "../scripts/sweep.mjs";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "sweep.mjs");
const T0 = "2026-11-18T06:00:00Z";
const NOW = Date.parse(T0);
const ago = (min) => new Date(NOW - min * 60_000).toISOString();

// A chat that stopped `min` minutes ago and was read after it stopped.
const row = (min, extra = {}) => ({ status: "completed", updated_at: ago(min), cursor: "r1#10", now_cursor: "r1#10", label: "done", ready_steps: [], questions: [], sends: [], running_children: 0, ...extra });
const asked = { sends: [{ at: ago(60) }], last_user_by: "agent", last_user_at: ago(60) };

const choices = [
  ["a chat that runs is left", row(0, { status: "running" }), "leave"],
  ["a chat with a running worker chat is left", row(50, { label: "plan_ready", running_children: 2 }), "leave"],
  ["a snoozed chat is skipped", row(50, { snoozed: true, label: "plan_ready" }), "skip"],
  ["a chat that is never read is skipped", row(50, { never_read: true, label: "plan_ready" }), "skip"],
  ["a chat that changed since the last read is read", row(50, { now_cursor: "r2#14" }), "read"],
  ["a chat that was never read and stopped 3 days ago is old", row(3 * 24 * 60, { cursor: null }), "old"],
  ["a ready label after 40 minutes is asked", row(40, { label: "plan_ready" }), "ask"],
  ["a ready label after 10 minutes is not yet asked", row(10, { label: "plan_ready" }), "not yet"],
  ["the idle time counts from the end of the run, not from the time of last change", row(5, { label: "plan_ready", stopped_at: ago(45) }), "ask"],
  ["a chat that was asked is not asked again", row(40, { label: "plan_ready", ...asked }), "leave"],
  ["a chat that was asked and holds questions goes to the queue", row(40, { label: "plan_ready", questions: ["Is it right?"], ...asked }), "queue"],
  ["a chat that was asked is asked again after a person spoke", row(40, { label: "plan_ready", sends: [{ at: ago(90) }], last_user_by: "user", last_user_at: ago(50) }), "ask"],
  ["questions for JP go to the queue", row(40, { label: "needs_jp", questions: ["Which one?"] }), "queue"],
  ["a chat that waits on a run is left", row(40, { label: "waits_run" }), "leave"],
  ["a done chat is left", row(400, { label: "done" }), "leave"],
  ["an interrupted chat with a person's message and no reply is unanswered", row(40, { status: "interrupted", label: "needs_jp", last_user_by: "user", last_user_at: ago(41) }), "unanswered"],
  ["an interrupted chat is not flagged while the person may still type", row(3, { status: "interrupted", label: "needs_jp", last_user_by: "user", last_user_at: ago(4) }), "not yet"],
  ["an interrupted chat whose last message is not a person's follows its label", row(40, { status: "interrupted", label: "waits_run", last_user_by: "agent", last_user_at: ago(41) }), "leave"],
  ["a settled chat is skipped, also when its label says ready", row(50, { settled: true, label: "plan_ready" }), "skip"],
  ["a settled chat with questions stays out of the queue", row(50, { settled: true, label: "needs_jp", questions: ["Which one?"] }), "skip"],
  ["a chat that changed 5 minutes ago is not read yet", row(5, { now_cursor: "r2#14" }), "not yet"],
  // New with the move into the CEO skill.
  ["the chat that runs the sweep is skipped", row(50, { self: true, label: "plan_ready" }), "skip"],
  ["a CEO chat with a ready label is never asked", row(40, { ceo: true, label: "plan_ready" }), "leave"],
  ["a CEO chat with questions goes to the queue", row(40, { ceo: true, label: "plan_ready", questions: ["Which one?"] }), "queue"],
];
for (const [name, r, want] of choices) {
  test(`choice: ${name}`, () => {
    const [got, why] = choose(r, NOW);
    assert.equal(got, want, why);
  });
}

// A scan marks each chat that is not in the list as settled, so the list must be every open top-level chat.
const t = (extra = {}) => ({ threadId: "a", settled: false, relationshipToParent: null, updatedAt: "2026-11-18T05:00:00Z", ...extra });
const lists = [
  ["a full list of open top-level chats is taken", { threads: [t(), t({ threadId: "b" })], nextCursor: null }, null],
  ["one page of many is refused", { threads: [t()], nextCursor: 100 }, "page"],
  ["a list that holds a settled chat is refused", { threads: [t({ settled: true })], nextCursor: null }, "settled"],
  ["a list that holds worker chats is refused", { threads: [t({ relationshipToParent: "subagent" })], nextCursor: null }, "worker"],
  ["an empty list is refused", { threads: [], nextCursor: null }, "empty"],
  ["a list with an entry that is no chat is refused", { threads: [t(), null], nextCursor: null }, "no chat"],
  ["a list with a chat that has no time of last change is refused", { threads: [t({ updatedAt: undefined })], nextCursor: null }, "time of last change"],
];
for (const [name, list, want] of lists) {
  test(`list: ${name}`, () => {
    const got = checkList(list);
    if (want === null) assert.equal(got, null);
    else assert.match(String(got), new RegExp(want));
  });
}

// The commands.
let root;
beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "sweep-test-"));
});
afterEach(() => rmSync(root, { recursive: true, force: true }));

function sweep(args, { now = T0, status = 0 } = {}) {
  const run = spawnSync(process.execPath, [SCRIPT, ...args, "--now", now, "--root", root], { encoding: "utf8" });
  assert.equal(run.status, status, `exit ${run.status} for ${args.join(" ")}: ${run.stderr}${run.stdout}`);
  if (status !== 0) return run.stderr;
  return args[0] === "brief" || args.includes("--text") ? run.stdout : JSON.parse(run.stdout);
}
const file = (name, value) => {
  const path = join(root, name);
  writeFileSync(path, typeof value === "string" ? value : JSON.stringify(value));
  return path;
};
const chat = (id, projectId, title, min, extra = {}) => ({ threadId: id, projectId, title, link: `[${title}](t3-thread://x/${id})`, status: "completed", latestRunId: "r1", itemCount: 10, updatedAt: ago(min), settled: false, snoozed: false, relationshipToParent: null, model: "m", ...extra });
const THREADS = {
  threads: [
    chat("A", "p1", "leviathan > a", 60),
    chat("B", "p2", "suntiq > b", 90),
    chat("C", "p1", "CEO > leviathan", 120),
    chat("S", "p1", "lev > the sweep chat", 0, { status: "running" }),
  ],
  nextCursor: null,
};
const PROJECTS = { projects: [{ id: "p1", title: "leviathan" }, { id: "p2", title: "suntiq-product" }], nextCursor: null };
const scan = (extra = []) => sweep(["scan", "--threads", file("threads.json", THREADS), "--projects", file("projects-in.json", PROJECTS), "--self", "S", ...extra]);
const label = (id, over = {}) => JSON.stringify({ threadId: id, cursor: "r1#10", label: "plan_ready", ready_steps: ["do it"], questions_for_jp: [], last_user_by: "user", last_user_at: ago(200), stopped_at: ago(60), ...over });
const titles = (out) => out.rows.map((r) => r.title).sort();
const choiceOf = (out, id) => out.rows.find((r) => r.threadId === id)?.choice;

test("scan: one index holds the chats of every project, each with its project's name", () => {
  const out = scan();
  assert.deepEqual(titles(out), ["CEO > leviathan", "leviathan > a", "suntiq > b"]);
  assert.deepEqual(out.rows.map((r) => r.project).sort(), ["leviathan", "leviathan", "suntiq-product"]);
  assert.equal(out.counts.read, 3);
  assert.equal(out.counts.skip, 1, "the chat that runs the sweep is skipped");
  const toRead = readFileSync(join(root, "to-read.tsv"), "utf8").trim().split("\n");
  assert.equal(toRead.length, 3);
});

test("scan: --project keeps the whole index and lists only that project's chats to read", () => {
  const out = scan(["--project", "leviathan"]);
  assert.deepEqual(titles(out), ["CEO > leviathan", "leviathan > a"]);
  assert.equal(readFileSync(join(root, "to-read.tsv"), "utf8").trim().split("\n").length, 2);
  assert.equal(Object.keys(JSON.parse(readFileSync(join(root, "index.json"), "utf8")).rows).length, 4);
});

test("show: no flag shows all projects, --project shows one, and an unknown project is refused", () => {
  scan();
  assert.equal(sweep(["show"]).rows.length, 3);
  assert.deepEqual(titles(sweep(["show", "--project", "suntiq-product"])), ["suntiq > b"]);
  assert.deepEqual(titles(sweep(["show", "--project", "SUNTIQ-product"])), ["suntiq > b"], "the name matches in any case");
  assert.match(sweep(["show", "--project", "nope"], { status: 2 }), /no project named "nope"/);
});

test("scan: a wrong list is refused and the index stays as it was", () => {
  scan();
  const before = readFileSync(join(root, "index.json"), "utf8");
  const onePage = file("page.json", { threads: [THREADS.threads[0]], nextCursor: 100 });
  assert.match(sweep(["scan", "--threads", onePage], { status: 2 }), /scan refused: the list is one page of many/);
  assert.equal(readFileSync(join(root, "index.json"), "utf8"), before);
});

test("scan: a chat that left the open list is marked settled and skipped", () => {
  scan();
  const fewer = file("fewer.json", { threads: THREADS.threads.filter((c) => c.threadId !== "B"), nextCursor: null });
  const out = sweep(["scan", "--threads", fewer, "--self", "S", "--all"]);
  assert.equal(choiceOf(out, "B"), "skip");
});

test("merge then sent: a ready chat is asked once, a CEO chat never, and questions go to the queue", () => {
  scan();
  const labels = file("labels.jsonl", [label("A"), label("B", { label: "needs_jp", ready_steps: [], questions_for_jp: ["Which one?"] }), label("C")].join("\n") + "\n");
  const merged = sweep(["merge", "--labels", labels]);
  assert.equal(merged.merged, 3);
  assert.equal(choiceOf(merged, "A"), "ask");
  assert.equal(choiceOf(merged, "B"), "queue");
  assert.equal(choiceOf(merged, "C"), "leave");
  const sent = sweep(["sent", "--thread", "A", "--wording", "Continue approved work, or return \"blocked\"."]);
  assert.equal(choiceOf(sent, "A"), "leave", "no second ask until a person speaks");
  const lines = readFileSync(join(root, "sends.jsonl"), "utf8").trim().split("\n").map((l) => JSON.parse(l));
  assert.deepEqual(lines.map((l) => [l.threadId, Date.parse(l.at)]), [["A", NOW]]);
  assert.match(sweep(["sent", "--thread", "nope", "--wording", "x"], { status: 2 }), /no chat "nope" in the index/);
});

test("settings: a title in never_read is never listed to read", () => {
  file("settings.json", { never_read: ["suntiq > b"] });
  const out = scan(["--all"]);
  assert.equal(choiceOf(out, "B"), "skip");
  assert.equal(readFileSync(join(root, "to-read.tsv"), "utf8").trim().split("\n").length, 2);
});

test("brief: the reader's brief names the list, the rules, the output file and the count", () => {
  scan();
  const out = sweep(["brief", "--out", join(root, "labels.jsonl")]);
  assert.match(out, /label the last reply of 3 chats/);
  assert.ok(out.includes(join(root, "to-read.tsv")));
  assert.ok(out.includes(join(root, "labels.jsonl")));
  const rules = out.match(/The label rules: `([^`]+)`/)[1];
  assert.ok(existsSync(rules), `${rules} exists`);
  assert.doesNotMatch(out, /\{\{/, "no placeholder is left");
});

test("the program sends nothing: it and the queue program it calls import only fs, os, path, url and util, and load no code at run time", () => {
  const importsOf = (path) => {
    const source = readFileSync(path, "utf8");
    assert.doesNotMatch(source, /\bimport\s*\(|\brequire\s*\(|\beval\s*\(|new Function|process\.binding|getBuiltinModule|\bfetch\s*\(/, path);
    return [...new Set([...source.matchAll(/^\s*import\s[^;]*?["']([^"']+)["']\s*;/gm)].map((m) => m[1]))].sort();
  };
  const builtin = ["node:fs", "node:os", "node:path", "node:url", "node:util"];
  assert.deepEqual(importsOf(SCRIPT), ["./queue.mjs", ...builtin]);
  assert.deepEqual(importsOf(QUEUE), builtin);
});

// The second reader (review-step-1-reread.json) found that a search of the source text misses a process start.
// So the claim is proved by a run: Node's permission system refuses a process, a worker, an addon, and a write
// outside the state folder. (Node 24 has no permission for the network; the list of imports above covers it.)
const PERMISSION = process.allowedNodeEnvironmentFlags.has("--permission") ? "--permission" : "--experimental-permission";
function guarded(args, { status = 0 } = {}) {
  const real = realpathSync(root);
  const run = spawnSync(process.execPath, [PERMISSION, "--allow-fs-read=*", `--allow-fs-write=${real}`, `--allow-fs-write=${join(real, "*")}`, SCRIPT, ...args, "--now", T0, "--root", real], { encoding: "utf8" });
  assert.equal(run.status, status, `exit ${run.status} for ${args.join(" ")}: ${run.stderr}`);
  return run;
}

test("under Node's permission system every command runs: no process, no worker, no write outside the state folder", () => {
  const real = realpathSync(root);
  const control = spawnSync(process.execPath, [PERMISSION, "--allow-fs-read=*", "-e", "require('node:child_process').spawnSync(process.execPath, ['-e', ''])"], { encoding: "utf8" });
  assert.notEqual(control.status, 0, "control: the permission system refuses a process start");
  assert.match(control.stderr, /ERR_ACCESS_DENIED/);
  guarded(["scan", "--threads", file("threads.json", THREADS), "--projects", file("projects-in.json", PROJECTS), "--self", "S"]);
  guarded(["merge", "--labels", file("labels.jsonl", label("A") + "\n")]);
  guarded(["sent", "--thread", "A", "--wording", "continue"]);
  guarded(["show"]);
  guarded(["brief", "--out", join(real, "labels-next.jsonl")]);   // B and C are still on the list
});

test("merge: a chat whose label was taken leaves the list, so a second reader is not started for it", () => {
  scan();
  sweep(["merge", "--labels", file("labels.jsonl", label("A") + "\n")]);
  const left = readFileSync(join(root, "to-read.tsv"), "utf8").trim().split("\n").map((line) => line.split("\t")[0]);
  assert.deepEqual(left.sort(), ["B", "C"]);
  assert.deepEqual(sweep(["merge", "--labels", file("labels.jsonl", label("A") + "\n")]).not_in_to_read, ["A"]);
  sweep(["merge", "--labels", file("labels-2.jsonl", label("B") + "\n" + label("C") + "\n")]);
  assert.match(sweep(["brief", "--out", join(root, "labels-3.jsonl")], { status: 2 }), /nothing to read/);
});

test("nothing decided is stored: the index holds facts, and each command works the choice out again", () => {
  readyA();
  const index = JSON.parse(readFileSync(join(root, "index.json"), "utf8"));
  for (const r of Object.values(index.rows)) for (const key of ["choice", "why", "idle_min", "sends"]) assert.equal(key in r, false, `${r.threadId} stores ${key}`);
});

test("show: a send that is in the log holds the chat, with no scan or merge in between", () => {
  readyA();
  assert.equal(choiceOf(sweep(["show"]), "A"), "ask");
  writeFileSync(join(root, "sends.jsonl"), JSON.stringify({ threadId: "A", at: T0, wording: "continue" }) + "\n");
  assert.equal(choiceOf(sweep(["show"]), "A"), "leave");
});

test("show: the choice follows the clock, not the last scan", () => {
  const threads = THREADS.threads.map((c) => (c.threadId === "A" ? { ...c, updatedAt: ago(5) } : c));
  const first = sweep(["scan", "--threads", file("threads-2.json", { ...THREADS, threads }), "--self", "S"]);
  assert.equal(choiceOf(first, "A"), "not yet");
  assert.equal(choiceOf(sweep(["show"], { now: "2026-11-18T07:00:00Z" }), "A"), "read");
});

test("sent: the time keeps its milliseconds, so a person's message 250 ms before the send keeps the hold", () => {
  scan();
  sweep(["merge", "--labels", file("labels.jsonl", label("A", { last_user_at: "2026-11-18T06:00:00.250Z" }) + "\n")]);
  sweep(["sent", "--thread", "A", "--wording", "continue"], { now: "2026-11-18T06:00:00.500Z" });
  assert.equal(choiceOf(sweep(["show"], { now: "2026-11-18T06:01:00Z" }), "A"), "leave");
});

test("lock: a command that writes is refused while another one holds the state folder", () => {
  scan();
  const before = stateFiles();
  writeFileSync(join(root, "lock"), JSON.stringify({ pid: process.pid, at: T0 }));
  assert.match(sweep(["scan", "--threads", file("threads.json", THREADS), "--self", "S"], { status: 2 }), /another sweep command holds/);
  assert.match(sweep(["sent", "--thread", "A", "--wording", "x"], { status: 2 }), /another sweep command holds/);
  assert.deepEqual(stateFiles(), before);
  assert.equal(sweep(["show"]).rows.length, 3, "a command that only reads is not held");
});

// The third reader (review-step-1-third.json) made a command remove the lock of a live one, through the
// take-over of a dead lock. So no lock is taken over: the command says its owner is gone and which file to delete.
test("lock: the lock of a process that is gone is never taken over; the refusal says so and names the file to delete", () => {
  scan();
  const before = stateFiles();
  writeFileSync(join(root, "lock"), JSON.stringify({ pid: 2147483646, at: T0 }));
  const refused = sweep(["scan", "--threads", file("threads.json", THREADS), "--self", "S"], { status: 2 });
  assert.match(refused, /another sweep command holds/);
  assert.match(refused, /process 2147483646 .* is gone/);
  assert.ok(refused.includes(`delete ${join(root, "lock")}`));
  assert.deepEqual(stateFiles(), before);
  assert.equal(existsSync(join(root, "lock")), true, "the lock stays for a person or an agent to delete");
  rmSync(join(root, "lock"));
  scan();
  assert.equal(existsSync(join(root, "lock")), false, "a command leaves no lock behind");
  assert.match(sweep(["scan", "--threads", file("page.json", { threads: [THREADS.threads[0]], nextCursor: 100 })], { status: 2 }), /scan refused/);
  assert.equal(existsSync(join(root, "lock")), false, "a refused command gives the lock back");
});

test("lock: eight scans at the same time each end with exit 0 or a refusal, and the index is whole", async () => {
  const threads = file("threads.json", THREADS);
  const one = (n) => new Promise((done) => {
    const child = spawn(process.execPath, [SCRIPT, "scan", "--threads", threads, "--self", n % 2 ? "S" : "A", "--now", T0, "--root", root]);
    let err = "";
    child.stderr.on("data", (chunk) => { err += chunk; });
    child.on("close", (status) => done({ status, err }));
  });
  const runs = await Promise.all([0, 1, 2, 3, 4, 5, 6, 7].map(one));
  for (const run of runs) {
    assert.ok(run.status === 0 || run.status === 2, `exit ${run.status}: ${run.err}`);
    if (run.status === 2) assert.match(run.err, /another sweep command/);
  }
  assert.ok(runs.some((run) => run.status === 0), "one scan wrote");
  const index = JSON.parse(readFileSync(join(root, "index.json"), "utf8"));
  assert.equal(Object.keys(index.rows).length, 4);
  assert.ok(["S", "A"].includes(index.self));
  for (const row of Object.values(index.rows)) assert.equal(row.self, row.threadId === index.self, "the rows agree with the scan that wrote last");
  assert.deepEqual(readdirSync(root).filter((name) => /^\.|lock|\.tmp$/.test(name)), []);
});

test("the state folder holds no temp file and no lock after scan, merge and sent", () => {
  readyA();
  sweep(["sent", "--thread", "A", "--wording", "continue"]);
  const known = new Set(["index.json", "to-read.tsv", "sends.jsonl", "projects.json", "settings.json"]);
  const made = readdirSync(root).filter((name) => /^\.|lock|\.tmp$/.test(name) && !known.has(name));
  assert.deepEqual(made, []);
});

test("merge: a label the program does not know is not taken, and its chat stays `read`", () => {
  scan();
  const out = sweep(["merge", "--labels", file("labels.jsonl", label("A", { label: "default_ready" }) + "\n" + label("B") + "\n")]);
  assert.deepEqual(out.unknown_label, ["A"]);
  assert.equal(out.merged, 1);
  assert.equal(choiceOf(out, "A"), "read");
  assert.ok(readFileSync(join(root, "to-read.tsv"), "utf8").includes("A\t"));
});

test("the send log: a line that is JSON but no send record is bad input, before any write", () => {
  scan();
  writeFileSync(join(root, "sends.jsonl"), "null\n");
  const before = stateFiles();
  const renamed = file("projects-2.json", { projects: [{ id: "p1", title: "renamed" }] });
  assert.match(sweep(["scan", "--threads", file("threads.json", THREADS), "--projects", renamed], { status: 2 }), /line 1 is not a send record/);
  assert.match(sweep(["sent", "--thread", "A", "--wording", "x"], { status: 2 }), /line 1 is not a send record/);
  assert.match(sweep(["show"], { status: 2 }), /line 1 is not a send record/);
  assert.deepEqual(stateFiles(), before);
});

// Found by the reader of 2026-11-18 (review-step-1.json). Each of these failed before its fix.
const stateFiles = () => ["index.json", "to-read.tsv", "sends.jsonl", "projects.json"].map((name) => (existsSync(join(root, name)) ? readFileSync(join(root, name), "utf8") : null));
const readyA = () => {
  scan();
  sweep(["merge", "--labels", file("labels.jsonl", label("A") + "\n")]);
};
const sendAt = (iso) => ({ sends: [{ at: iso }] });

test("choice: a person's message 500 ms before the send does not free the chat for a second ask", () => {
  const r = row(40, { label: "plan_ready", ...sendAt("2026-11-18T05:00:00.500Z"), last_user_by: "user", last_user_at: "2026-11-18T05:00:00Z" });
  assert.equal(choose(r, NOW)[0], "leave");
});

test("choice: times are compared as instants, also with a time zone offset", () => {
  const r = row(40, { label: "plan_ready", ...sendAt("2026-11-18T05:00:00Z"), last_user_by: "user", last_user_at: "2026-11-18T06:00:00+02:00" });
  assert.equal(choose(r, NOW)[0], "leave", "06:00+02:00 is 04:00Z, before the send");
});

test("choice: a send with no time keeps the hold and does not crash", () => {
  const r = row(40, { label: "plan_ready", sends: [{ wording: "continue" }], last_user_by: "user", last_user_at: ago(10) });
  assert.equal(choose(r, NOW)[0], "leave");
});

test("choice: a row with no time of last change that was never read is old, as in the old program", () => {
  assert.equal(choose({ status: "completed", cursor: null, now_cursor: "r1#10", questions: [], sends: [] }, NOW)[0], "old");
});

test("merge: a label for an older reply than the one in the list is not taken", () => {
  scan();
  const old = file("labels-old.jsonl", label("A") + "\n");   // the reader was given A at r1#10
  const threads = THREADS.threads.map((c) => (c.threadId === "A" ? { ...c, latestRunId: "r2", itemCount: 11, updatedAt: ago(40) } : c));
  sweep(["scan", "--threads", file("threads-2.json", { ...THREADS, threads }), "--self", "S"]);
  const out = sweep(["merge", "--labels", old]);
  assert.equal(out.merged, 0);
  assert.deepEqual(out.stale, ["A"]);
  assert.equal(choiceOf(out, "A"), "read");
});

test("merge: a label that names no cursor is not taken", () => {
  scan();
  const out = sweep(["merge", "--labels", file("labels.jsonl", label("A", { cursor: undefined }) + "\n")]);
  assert.equal(out.merged, 0);
  assert.deepEqual(out.stale, ["A"]);
});

test("merge: a send that is in the log but not in the index still holds the chat", () => {
  readyA();
  // As after a crash of `sent` between its two writes: the log has the line, the index does not.
  writeFileSync(join(root, "sends.jsonl"), JSON.stringify({ threadId: "A", at: T0, wording: "continue" }) + "\n");
  const out = sweep(["merge", "--labels", file("none.jsonl", "")]);
  assert.equal(choiceOf(out, "A"), "leave");
});

test("an unknown --project is refused before scan, merge or sent writes anything", () => {
  readyA();
  const before = stateFiles();
  const threads = THREADS.threads.map((c) => (c.threadId === "B" ? { ...c, itemCount: 99 } : c));
  assert.match(sweep(["scan", "--threads", file("threads-2.json", { ...THREADS, threads }), "--project", "nope"], { status: 2 }), /no project named "nope"/);
  assert.match(sweep(["merge", "--labels", file("labels-b.jsonl", label("B") + "\n"), "--project", "nope"], { status: 2 }), /no project named "nope"/);
  assert.match(sweep(["sent", "--thread", "A", "--wording", "x", "--project", "nope"], { status: 2 }), /no project named "nope"/);
  assert.deepEqual(stateFiles(), before);
});

test("scan: the chat that runs the sweep is the one this scan names, not the one an earlier scan named", () => {
  scan();
  const out = sweep(["scan", "--threads", file("threads.json", THREADS), "--all"]);
  assert.equal(choiceOf(out, "S"), "leave", "S runs now; with no --self it is a chat like any other");
});

test("merge: a labels file with a bad line is refused with exit 2 and the index stays as it was", () => {
  scan();
  const before = readFileSync(join(root, "index.json"), "utf8");
  assert.match(sweep(["merge", "--labels", file("bad.jsonl", label("A") + "\nBAD JSON\n")], { status: 2 }), /line 2 is not JSON/);
  assert.equal(readFileSync(join(root, "index.json"), "utf8"), before);
});

// Found by the third reader (review-step-1-third.json). Each of these failed before its fix.
test("scan: a --project that the new project names do not hold is refused before any write", () => {
  readyA();
  const before = stateFiles();
  const renamed = file("projects-2.json", { projects: [{ id: "p1", title: "renamed" }, { id: "p2", title: "suntiq-product" }] });
  const threads = THREADS.threads.map((c) => (c.threadId === "A" ? { ...c, itemCount: 11 } : c));
  const refused = sweep(["scan", "--threads", file("threads-2.json", { ...THREADS, threads }), "--projects", renamed, "--project", "leviathan"], { status: 2 });
  assert.match(refused, /no project named "leviathan"/);
  assert.deepEqual(stateFiles(), before);
});

test("choice: the newest send holds the chat, also when an older send is the last line of the log", () => {
  const sends = [{ at: "2026-11-18T05:00:00Z" }, { at: "2026-11-18T04:00:00Z" }];
  const r = row(40, { label: "plan_ready", sends, last_user_by: "user", last_user_at: "2026-11-18T04:30:00Z" });
  assert.equal(choose(r, NOW)[0], "leave", "the person spoke before the 05:00Z send");
  assert.equal(choose({ ...r, last_user_at: "2026-11-18T05:10:00Z" }, NOW)[0], "ask", "the person spoke after every send");
});

test("choice: a chat that was read before and changed is read again, however old; only a chat that was never read is old", () => {
  const days = 5 * 24 * 60;
  const known = row(days, { cursor: "r1#9", now_cursor: "r1#10", label: "needs_jp", questions: ["Which design?"] });
  assert.equal(choose(known, NOW)[0], "read", "its recorded question is not hidden behind `old`");
  assert.equal(choose(row(days, { cursor: null, now_cursor: "r1#10" }), NOW)[0], "old");
  assert.equal(choose({ ...known, updated_at: "not-a-date" }, NOW)[0], "old", "a time that cannot be read never gives read");
});

test("bad input: a line that is no label, a list entry that is no chat, a chat with no time, an option with no value, and a folder as a file all give exit 2", () => {
  scan();
  const before = stateFiles();
  for (const line of ["null", "42", "[]", "{}", '"text"']) {
    assert.match(sweep(["merge", "--labels", file("odd.jsonl", label("A") + "\n" + line + "\n")], { status: 2 }), /line 2 is not a label/, line);
  }
  assert.match(sweep(["merge", "--labels", root], { status: 2 }), /cannot read --labels/);
  assert.match(sweep(["scan", "--threads", file("null.json", { threads: [null], nextCursor: null })], { status: 2 }), /scan refused: .*no chat/);
  const noTime = THREADS.threads.map((c) => (c.threadId === "A" ? { ...c, updatedAt: "not-a-date" } : c));
  assert.match(sweep(["scan", "--threads", file("no-time.json", { ...THREADS, threads: noTime })], { status: 2 }), /scan refused: .*time of last change/);
  assert.match(sweep(["scan", "--threads"], { status: 2 }), /--threads/);
  assert.deepEqual(stateFiles(), before);
});

test("an index of the older program loses its stored choices at the next scan or merge", () => {
  readyA();
  const path = join(root, "index.json");
  const index = JSON.parse(readFileSync(path, "utf8"));
  index.version = 1;
  Object.assign(index.rows.A, { choice: "ask", why: "cached", idle_min: 120, sends: [{ at: T0 }] });
  writeFileSync(path, JSON.stringify(index));
  assert.equal(choiceOf(sweep(["show"]), "A"), "ask", "the stored sends are not used: the log is empty");
  sweep(["merge", "--labels", file("none.jsonl", "")]);
  const after = JSON.parse(readFileSync(path, "utf8"));
  assert.equal(after.version, 2);
  for (const key of ["choice", "why", "idle_min", "sends"]) assert.equal(key in after.rows.A, false, key);
});

test("each state file is replaced in one step: a scan and a merge work when the files are read-only", () => {
  scan();
  for (const name of ["index.json", "to-read.tsv", "projects.json"]) chmodSync(join(root, name), 0o444);
  scan();
  sweep(["merge", "--labels", file("labels.jsonl", label("A") + "\n")]);
  assert.equal(JSON.parse(readFileSync(join(root, "index.json"), "utf8")).rows.A.label, "plan_ready");
});

test("sent: a send log that is a link to a file outside the state folder is refused, and that file is not written", () => {
  readyA();
  const outside = mkdtempSync(join(tmpdir(), "sweep-outside-"));
  const target = join(outside, "target.jsonl");
  writeFileSync(target, "");
  symlinkSync(target, join(root, "sends.jsonl"));
  assert.match(sweep(["sent", "--thread", "A", "--wording", "x"], { status: 2 }), /is a link/);
  assert.equal(readFileSync(target, "utf8"), "");
  rmSync(outside, { recursive: true, force: true });
});

test("scan: a tab in a title does not add a column to the list for the reader", () => {
  const threads = THREADS.threads.map((c) => (c.threadId === "A" ? { ...c, title: "leviathan >\ta\ttab" } : c));
  sweep(["scan", "--threads", file("threads-2.json", { ...THREADS, threads }), "--self", "S"]);
  for (const line of readFileSync(join(root, "to-read.tsv"), "utf8").trim().split("\n")) assert.equal(line.split("\t").length, 4, line);
});

test("brief: the reader copies each chat's cursor into its label", () => {
  scan();
  assert.match(sweep(["brief", "--out", join(root, "labels.jsonl")]), /`cursor`: as in the list/);
});

// ---- queue: the index's questions go into the CEO skill's queue program (scripts/queue.mjs) ----
// The design, in one place:
//   node sweep.mjs queue --thread <the chat that runs the sweep> [--title "<its title>"] [--project <title>]
//   - Each row whose choice is `queue` or `unanswered` becomes one item of scripts/queue.mjs: id = the thread id,
//     kind attention, priority 1 for unanswered and 2 for queue, with `source: "sweep"`, `project`, `questions`
//     and `cursor` (the chat's cursor at the read).
//   - Only items with `source: "sweep"` are touched. An item the CEO put by hand, and a settle item, stay.
//   - An open item whose row holds no question any more is resolved done. A presented item whose chat moved goes
//     back to pending. A done item opens again only when the chat's cursor changed and it holds questions again.
//   - With --project, rows and items of other projects are not touched.
//   - The queue is the one of --thread: a chat for all projects has one queue for all projects.
const QUEUE = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "queue.mjs");
const qroot = () => join(root, "queues");
const sync = (extra = [], opts) => sweep(["queue", "--thread", "S", "--title", "CEO > all", "--queue-root", qroot(), ...extra], opts);
function queue(args) {
  const out = spawnSync(process.execPath, [QUEUE, ...args, "--thread", "S", "--now", T0, "--root", qroot()], { encoding: "utf8" });
  assert.equal(out.status, 0, out.stderr);
  return JSON.parse(out.stdout);
}
const items = () => queue(["show", "--all"]).items;
const itemOf = (id) => items().find((i) => i.id === id);

// A, B, C as in THREADS, plus D: a run that was interrupted after a person's message.
const WITH_D = { ...THREADS, threads: [...THREADS.threads, chat("D", "p2", "suntiq > d", 50, { status: "interrupted" })] };
function base() {
  sweep(["scan", "--threads", file("threads.json", WITH_D), "--projects", file("projects-in.json", PROJECTS), "--self", "S"]);
  const labels = [
    label("A"),
    label("B", { label: "needs_jp", ready_steps: [], questions_for_jp: ["Which one?"] }),
    label("C", { questions_for_jp: ["May I?"] }),
    label("D", { label: "needs_jp", ready_steps: [], stopped_at: ago(50), last_user_at: ago(51) }),
  ];
  sweep(["merge", "--labels", file("labels.jsonl", labels.join("\n") + "\n")]);
}
// The chat `id` got a new run: the scan sees a new cursor, and a reader labels it again.
function moved(id, over) {
  const threads = WITH_D.threads.map((c) => (c.threadId === id ? { ...c, latestRunId: "r2", itemCount: 14, updatedAt: ago(40) } : c));
  sweep(["scan", "--threads", file("threads-2.json", { ...WITH_D, threads }), "--self", "S"]);
  if (over) sweep(["merge", "--labels", file("labels-2.jsonl", label(id, { cursor: "r2#14", stopped_at: ago(40), ...over }) + "\n")]);
}

test("queue: each chat with questions, and each unanswered chat, becomes one item with its project", () => {
  base();
  const out = sync();
  assert.equal(out.added, 3);
  assert.deepEqual(items().map((i) => i.id).sort(), ["B", "C", "D"]);
  const b = itemOf("B");
  assert.equal(b.kind, "attention");
  assert.equal(b.source, "sweep");
  assert.equal(b.project, "suntiq-product");
  assert.deepEqual(b.questions, ["Which one?"]);
  assert.equal(b.cursor, "r1#10");
  assert.equal(itemOf("D").priority, 1, "a person's message with no reply goes first");
  assert.equal(itemOf("A"), undefined, "a chat with approved work and no question is not JP's");
});

test("queue: a second run adds nothing", () => {
  base();
  sync();
  const again = sync();
  assert.equal(again.added, 0);
  assert.equal(items().length, 3);
});

test("queue: an item whose chat holds no question any more is resolved done", () => {
  base();
  sync();
  moved("B", { label: "done", ready_steps: [], questions_for_jp: [] });
  const out = sync();
  assert.equal(out.closed, 1);
  assert.equal(itemOf("B").status, "done");
});

test("queue: a presented item whose chat moved goes back to pending", () => {
  base();
  sync();
  queue(["resolve", "--item", "D", "--to", "done", "--note", "answered"]);   // D is the head; clear it
  assert.equal(queue(["next"]).item.id, "B");
  moved("B");   // not read again yet: the row says read
  const out = sync();
  assert.equal(out.back_to_pending, 1);
  assert.equal(itemOf("B").status, "pending");
});

test("queue: a done item opens again only when the chat moved and holds questions again", () => {
  base();
  sync();
  queue(["resolve", "--item", "B", "--to", "done", "--note", "JP: a"]);
  assert.equal(sync().reopened, 0, "the same reply does not ask twice");
  assert.equal(itemOf("B").status, "done");
  moved("B", { label: "needs_jp", ready_steps: [], questions_for_jp: ["And now?"] });
  assert.equal(sync().reopened, 1);
  assert.equal(itemOf("B").status, "pending");
  assert.deepEqual(itemOf("B").questions, ["And now?"]);
});

test("queue: --project puts one project's chats and leaves the items of the others", () => {
  base();
  const out = sync(["--project", "leviathan"]);
  assert.equal(out.added, 1);
  assert.deepEqual(items().map((i) => i.id), ["C"]);
  sync();
  moved("B", { label: "done", ready_steps: [], questions_for_jp: [] });
  assert.equal(sync(["--project", "leviathan"]).closed, 0, "B is a suntiq-product chat");
  assert.equal(itemOf("B").status, "pending");
});

test("queue: an item the CEO put by hand is not touched, also when its id is the id of a chat with questions", () => {
  base();
  sync(["--project", "leviathan"]);   // opens the queue; B is a suntiq-product chat, so it has no item yet
  queue(["put", "--item", JSON.stringify({ id: "hand", kind: "attention", title: "by hand", reason: "the CEO put it" })]);
  queue(["put", "--item", JSON.stringify({ id: "B", kind: "attention", title: "B by hand", reason: "the CEO put it" })]);
  const out = sync();
  assert.equal(out.added, 1, "only D is new");
  assert.equal(itemOf("hand").status, "pending");
  assert.equal(itemOf("B").title, "B by hand");
  assert.equal(itemOf("B").source, undefined);
});

test("queue: with no queue and no --title it is refused", () => {
  base();
  assert.match(sweep(["queue", "--thread", "S", "--queue-root", qroot()], { status: 2 }), /no queue for thread S/);
  assert.equal(existsSync(qroot()), false, "a refused command makes no queue folder");
});

test("queue: an item whose chat moved and still asks gets the new questions, and a shown one goes back to pending", () => {
  base();
  sync();
  queue(["resolve", "--item", "D", "--to", "done", "--note", "answered"]);
  assert.equal(queue(["next"]).item.id, "B");
  moved("B", { label: "needs_jp", ready_steps: [], questions_for_jp: ["A new one?"] });
  const out = sync();
  assert.equal(out.updated, 1);
  assert.equal(out.back_to_pending, 1);
  assert.equal(itemOf("B").status, "pending");
  assert.deepEqual(itemOf("B").questions, ["A new one?"]);
  assert.equal(itemOf("B").cursor, "r2#14");
});

test("queue: an item whose chat was settled is resolved done", () => {
  base();
  sync();
  const threads = WITH_D.threads.filter((c) => c.threadId !== "B");
  sweep(["scan", "--threads", file("threads-3.json", { ...WITH_D, threads }), "--self", "S"]);
  assert.equal(sync().closed, 1);
  assert.equal(itemOf("B").status, "done");
});

test("queue: a refused run changes no queue", () => {
  base();
  sync();
  const dir = join(qroot(), readdirSync(qroot())[0]);
  const before = readFileSync(join(dir, "queue.json"), "utf8") + readFileSync(join(dir, "events.jsonl"), "utf8");
  moved("B", { label: "done", ready_steps: [], questions_for_jp: [] });
  assert.match(sync(["--project", "nope"], { status: 2 }), /no project named/);
  writeFileSync(join(root, "sends.jsonl"), "null\n");
  assert.match(sync([], { status: 2 }), /not a send record/);
  assert.equal(readFileSync(join(dir, "queue.json"), "utf8") + readFileSync(join(dir, "events.jsonl"), "utf8"), before);
});

test("queue: it runs under Node's permission system, with the queue folder inside the state folder", () => {
  const real = realpathSync(root);
  guarded(["scan", "--threads", file("threads.json", WITH_D), "--projects", file("projects-in.json", PROJECTS), "--self", "S"]);
  guarded(["merge", "--labels", file("labels.jsonl", label("B", { label: "needs_jp", ready_steps: [], questions_for_jp: ["Which one?"] }) + "\n")]);
  const run = guarded(["queue", "--thread", "S", "--title", "CEO > all", "--queue-root", join(real, "queues")]);
  assert.equal(JSON.parse(run.stdout).added, 1);
});

test("queue: two runs at the same time are not both let in", () => {
  base();
  writeFileSync(join(root, "lock"), JSON.stringify({ pid: process.pid, at: T0 }));
  assert.match(sync([], { status: 2 }), /another sweep command holds/);
});
