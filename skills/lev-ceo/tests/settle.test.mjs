// Tests for scripts/settle.mjs. Run: node --test ~/.agents/skills/lev-ceo/tests/settle.test.mjs
// The known-bad case is the one the CEO got wrong on 2026-11-10: a finished, landed, quiet chat was
// settled while an enabled scheduled task was still bound to it; the task ran and reopened the chat.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { after, before, test } from "node:test";
import { fileURLToPath } from "node:url";

import { decide } from "../scripts/settle.mjs";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "settle.mjs");
const NOW = "2026-11-10T20:00:00Z";
const HOURS_AGO = (n) => new Date(Date.parse(NOW) - n * 3_600_000).toISOString();

let dir;
let repo;
let landed;
let unlanded;

function git(...args) {
  const run = spawnSync("git", ["-C", repo, "-c", "user.name=test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", ...args], { encoding: "utf8" });
  assert.equal(run.status, 0, run.stderr);
  return run.stdout.trim();
}

before(() => {
  dir = mkdtempSync(join(tmpdir(), "settle-test-"));
  repo = join(dir, "repo");
  assert.equal(spawnSync("git", ["init", "-q", "-b", "main", repo]).status, 0);
  git("commit", "-q", "--allow-empty", "--no-verify", "-m", "landed work");
  landed = git("rev-parse", "HEAD");
  git("checkout", "-q", "-b", "side");
  git("commit", "-q", "--allow-empty", "--no-verify", "-m", "work still on its branch");
  unlanded = git("rev-parse", "HEAD");
  git("checkout", "-q", "main");
});
after(() => rmSync(dir, { recursive: true, force: true }));

const thread = (id, over = {}) => ({ threadId: id, title: `chat ${id}`, status: "completed", updatedAt: HOURS_AGO(3), ...over });
const worker = (id, over = {}) => ({ thread_id: id, title: `chat ${id}`, proof: { landed: { repo, commit: landed, into: "main" } }, left: [], ...over });
const calm = (...ids) => Object.fromEntries(ids.map((id) => [id, { questions: 0, queued: 0 }]));

function run(input) {
  return decide({ tasks: [], waits: calm(...input.threads.map((t) => t.threadId)), now: NOW, root: dir, ...input });
}
const ids = (rows) => rows.map((row) => row.thread_id);
const reasonsFor = (out, id) => out.hold.find((row) => row.thread_id === id)?.reasons.join("; ") ?? "";

test("a finished, owned, quiet chat whose work landed is ready", () => {
  const out = run({ threads: [thread("a")], handoffs: [{ id: "ceo-one", workers: [worker("a", { worktree: "/work/a" })] }] });
  assert.deepEqual(ids(out.settle), ["a"]);
  assert.equal(out.settle[0].owner, "ceo-one");
  assert.equal(out.settle[0].cleanup.worktree, "/work/a");
  assert.deepEqual(out.hold, []);
});

test("known bad: an enabled scheduled task bound to the chat holds it; with the task off it is ready", () => {
  const input = { threads: [thread("hub")], handoffs: [{ id: "ceo-one", workers: [worker("hub")] }] };
  const task = { scheduledTaskId: "scheduled-task:1", title: "Move old tools to Trash", enabled: true, boundThreadId: "hub" };

  const bad = run({ ...input, tasks: [task] });
  assert.deepEqual(ids(bad.settle), []);
  assert.match(reasonsFor(bad, "hub"), /enabled scheduled task: Move old tools to Trash/);

  const off = run({ ...input, tasks: [{ ...task, enabled: false }] });
  assert.deepEqual(ids(off.settle), ["hub"]);
  assert.deepEqual(off.settle[0].cleanup.disabled_tasks, ["scheduled-task:1"]);

  const elsewhere = run({ ...input, tasks: [{ ...task, boundThreadId: "another chat" }] });
  assert.deepEqual(ids(elsewhere.settle), ["hub"]);
});

// Known bad, 2026-11-11: a CEO asked for 17 finished, quiet, accepted chats to be settled and had read no leftover of any.
test("known bad: a finished, quiet, accepted chat is held until its leftovers are listed and each is fixed or tracked", () => {
  const out = (left) => run({ threads: [thread("w")], handoffs: [{ id: "ceo-one", workers: [worker("w", { left })] }] });

  assert.match(reasonsFor(out(undefined), "w"), /leftovers not read/);
  assert.match(reasonsFor(out(null), "w"), /leftovers not read/);
  assert.match(reasonsFor(out([{ what: "four review claims still fail" }]), "w"), /leftover with no record: four review claims still fail/);
  assert.match(reasonsFor(out(["no test moves a design by a verb"]), "w"), /leftover with no record: no test moves a design by a verb/);
  assert.match(reasonsFor(out([{ what: "a folder list is stale", record: ".lev/pm/handoffs/x-ceo.yaml#turn_0645z" }]), "w"), /tracked only in a handoff/);

  assert.deepEqual(ids(out([]).settle), ["w"]);
  assert.deepEqual(ids(out([{ what: "four review claims still fail", record: ".lev/pm/reports/debt.yaml#M826" }, { what: "three test titles said send", fixed: "d759b46ea2" }]).settle), ["w"]);
});

test("work that is still on its branch holds the chat", () => {
  const out = run({ threads: [thread("b")], handoffs: [{ id: "ceo-one", workers: [worker("b", { proof: { landed: { repo, commit: unlanded, into: "main" } } })] }] });
  assert.deepEqual(ids(out.settle), []);
  assert.match(reasonsFor(out, "b"), /not landed/);
});

test("a commit git cannot find reads can't tell, never landed", () => {
  const out = run({ threads: [thread("b")], handoffs: [{ id: "ceo-one", workers: [worker("b", { proof: { landed: { repo, commit: "0000000000000000000000000000000000000000", into: "main" } } })] }] });
  assert.match(reasonsFor(out, "b"), /can't tell if it landed/);
});

test("an acceptance counts only with a time and the check the owner reran", () => {
  const handoff = (accepted) => [{ id: "ceo-one", workers: [worker("c", { proof: { accepted } })] }];
  const said = run({ threads: [thread("c")], handoffs: handoff({ at: HOURS_AGO(4) }) });
  assert.match(reasonsFor(said, "c"), /acceptance has no rerun/);
  const reran = run({ threads: [thread("c")], handoffs: handoff({ at: HOURS_AGO(4), check: "lev check --source x.eval.yaml: passed 5" }) });
  assert.deepEqual(ids(reran.settle), ["c"]);
  const none = run({ threads: [thread("c")], handoffs: [{ id: "ceo-one", workers: [worker("c", { proof: undefined })] }] });
  assert.match(reasonsFor(none, "c"), /no proof/);
});

test("a chat no CEO lists is held: it is JP's own or nobody's", () => {
  const out = run({ threads: [thread("jp", { createdBy: "user" })], handoffs: [{ id: "ceo-one", workers: [] }] });
  assert.match(reasonsFor(out, "jp"), /no owner/);
});

test("a prose worker row without thread_id claims nothing", () => {
  const out = run({ threads: [thread("d")], handoffs: [{ id: "ceo-one", workers: [{ name: "chat d", where: "T3 chat d" }] }] });
  assert.match(reasonsFor(out, "d"), /no owner/);
});

test("a chat two CEOs list is held until one owner remains", () => {
  const out = run({ threads: [thread("e")], handoffs: [{ id: "ceo-one", workers: [worker("e")] }, { id: "ceo-two", workers: [worker("e")] }] });
  assert.match(reasonsFor(out, "e"), /two owners: ceo-one and ceo-two/);
});

test("a pending question, a queued message or unread waits each hold the chat", () => {
  const handoffs = [{ id: "ceo-one", workers: [worker("f")] }];
  assert.match(reasonsFor(run({ threads: [thread("f")], handoffs, waits: { f: { questions: 1, queued: 0 } } }), "f"), /1 pending question/);
  assert.match(reasonsFor(run({ threads: [thread("f")], handoffs, waits: { f: { questions: 0, queued: 2 } } }), "f"), /2 queued message/);
  assert.match(reasonsFor(run({ threads: [thread("f")], handoffs, waits: {} }), "f"), /waits not read/);
});

test("a running chat and a chat active in the last 2 hours are held", () => {
  const handoffs = [{ id: "ceo-one", workers: [worker("g"), worker("h")] }];
  const out = run({ threads: [thread("g", { status: "running" }), thread("h", { updatedAt: HOURS_AGO(0.5) })], handoffs });
  assert.deepEqual(ids(out.settle), []);
  assert.match(reasonsFor(out, "g"), /not finished: status running/);
  assert.match(reasonsFor(out, "h"), /not quiet/);
});

test("with --owner, another CEO's ready chat goes under ask_owner; the CEO's own chat is never listed", () => {
  const out = run({
    threads: [thread("mine"), thread("theirs"), thread("ceo-chat")],
    handoffs: [{ id: "ceo-one", workers: [worker("mine"), worker("ceo-chat")] }, { id: "ceo-two", workers: [worker("theirs")] }],
    owner: "ceo-one",
    self: "ceo-chat",
  });
  assert.deepEqual(ids(out.settle), ["mine"]);
  assert.deepEqual(ids(out.ask_owner), ["theirs"]);
  assert.deepEqual(out.hold, []);
});

test("the command reads its files, prints JSON and exits 0; a missing file exits 2", () => {
  const file = (name, value) => {
    const path = join(dir, name);
    writeFileSync(path, JSON.stringify(value));
    return path;
  };
  const args = [
    SCRIPT,
    "--threads", file("threads.json", { currentThreadId: "ceo-chat", threads: [thread("a"), thread("hub"), thread("ceo-chat")] }),
    "--tasks", file("tasks.json", { tasks: [{ title: "nightly", enabled: true, boundThreadId: "hub" }] }),
    "--waits", file("waits.json", calm("a", "hub")),
    "--handoff", file("handoff.json", { id: "ceo-one", workers: [worker("a"), worker("hub")] }),
    "--now", NOW,
    "--root", dir,
  ];
  const ok = spawnSync(process.execPath, args, { encoding: "utf8" });
  assert.equal(ok.status, 0, ok.stderr);
  const out = JSON.parse(ok.stdout);
  assert.deepEqual(ids(out.settle), ["a"]);
  assert.deepEqual(ids(out.hold), ["hub"]);

  const missing = spawnSync(process.execPath, [SCRIPT, "--threads", join(dir, "nope.json"), "--tasks", args[4], "--waits", args[6]], { encoding: "utf8" });
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /cannot read/);
});

const LEV_ROOT = process.env.LEV_ROOT ?? join(homedir(), "digital", "leviathan");
test("a YAML handoff is read with the checkout's yaml library", { skip: !existsSync(join(LEV_ROOT, "node_modules", "yaml")) && "no Lev checkout with yaml installed" }, () => {
  const handoff = join(dir, "20261110-ceo-test.yaml");
  writeFileSync(handoff, `id: ceo-yaml\ntype: handoff\nworkers:\n  - thread_id: "y"\n    title: yaml chat\n    proof: {accepted: {at: '${HOURS_AGO(5)}', check: "node --test: 12 pass"}}\n    left: []\n`);
  const threads = join(dir, "y-threads.json");
  writeFileSync(threads, JSON.stringify([thread("y")]));
  const waits = join(dir, "y-waits.json");
  writeFileSync(waits, JSON.stringify(calm("y")));
  const tasks = join(dir, "y-tasks.json");
  writeFileSync(tasks, "[]");
  const run = spawnSync(process.execPath, [SCRIPT, "--threads", threads, "--tasks", tasks, "--waits", waits, "--handoff", handoff, "--now", NOW, "--root", LEV_ROOT], { encoding: "utf8" });
  assert.equal(run.status, 0, run.stderr);
  assert.deepEqual(ids(JSON.parse(run.stdout).settle), ["y"]);
});
