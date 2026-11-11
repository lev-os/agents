#!/usr/bin/env node
/**
 * Fresh-agent check: does SKILL.md alone make a new agent settle the same chats as scripts/settle.mjs?
 *
 * It builds a saved thread list in a temporary folder (ten chats, each failing a different part of the
 * test, plus three that are ready), gives a fresh `claude -p` agent only SKILL.md and those files, and
 * compares the chats it would settle with the script's `settle` list. The agent gets no scripts folder,
 * so it must apply the six parts from the skill's words.
 *
 * Usage: node ~/.agents/skills/lev-ceo/tests/fresh-agent-settle.mjs [--model <id>] [--keep]
 * Exit 0: the two lists match. Exit 1: they differ. Exit 2: the agent gave no list. It calls a model once.
 */
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const { values } = parseArgs({ options: { model: { type: "string" }, keep: { type: "boolean" } } });
const SKILL = join(dirname(fileURLToPath(import.meta.url)), "..");
const NOW = "2026-11-10T20:00:00Z";
const ago = (hours) => new Date(Date.parse(NOW) - hours * 3_600_000).toISOString();

const dir = mkdtempSync(join(tmpdir(), "fresh-agent-settle-"));
const repo = join(dir, "repo");
const git = (...args) => {
  const run = spawnSync("git", ["-C", repo, "-c", "user.name=test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", ...args], { encoding: "utf8" });
  if (run.status !== 0) throw new Error(run.stderr);
  return run.stdout.trim();
};
spawnSync("git", ["init", "-q", "-b", "main", repo]);
git("commit", "-q", "--allow-empty", "--no-verify", "-m", "landed work");
const landed = git("rev-parse", "HEAD");
git("checkout", "-q", "-b", "side");
git("commit", "-q", "--allow-empty", "--no-verify", "-m", "work still on its branch");
const unlanded = git("rev-parse", "HEAD");
git("checkout", "-q", "main");

const chat = (id, title, over = {}) => ({ threadId: id, title, status: "completed", createdBy: "agent", updatedAt: ago(5), ...over });
const threads = {
  currentThreadId: "mcp:ceo",
  threads: [
    chat("mcp:ceo", "CEO > demo", { status: "running", updatedAt: ago(0) }),
    chat("mcp:landed", "demo > groups build"),
    chat("mcp:accepted", "demo > cold caller"),
    chat("mcp:worktree", "demo > phone icons"),
    chat("mcp:task", "demo > design skills hub"),
    chat("mcp:branch", "demo > test caller"),
    chat("mcp:fresh", "demo > teams tests", { updatedAt: ago(0.4) }),
    chat("mcp:running", "demo > phone alerts", { status: "running", updatedAt: ago(3) }),
    chat("mcp:question", "demo > fast feedback"),
    chat("mcp:queued", "demo > daemon role"),
    chat("mcp:word", "demo > captions"),
    chat("user-chat", "demo > release notes", { createdBy: "user" }),
    chat("mcp:theirs", "demo > call video"),
    chat("mcp:both", "demo > quick fixes"),
  ],
};
const tasks = {
  tasks: [
    { scheduledTaskId: "scheduled-task:1", title: "Move old tools to Trash", enabled: true, boundThreadId: "mcp:task" },
    { scheduledTaskId: "scheduled-task:2", title: "Old watch", enabled: false, boundThreadId: "mcp:worktree" },
  ],
};
const quiet = { questions: 0, queued: 0 };
const waits = {
  "mcp:landed": quiet, "mcp:accepted": quiet, "mcp:worktree": quiet, "mcp:task": quiet, "mcp:branch": quiet, "mcp:fresh": quiet,
  "mcp:running": quiet, "mcp:question": { questions: 1, queued: 0 }, "mcp:queued": { questions: 0, queued: 1 }, "mcp:word": quiet,
  "mcp:theirs": quiet, "mcp:both": quiet,
};
const inMain = { landed: { repo, commit: landed, into: "main" } };
const row = (thread_id, title, proof, over = {}) => ({ thread_id, title, state: "accepted", worktree: null, proof, left: [], ...over });
const mine = {
  id: "20261110-ceo-demo",
  type: "handoff",
  thread: "mcp:ceo",
  setup: { loop: { on: false, engine: "ll", ends_at: null }, unasked: ["rerun_on_report", "settle_own_workers"], quiet_hours: null, worker_limit: 5 },
  workers: [
    row("mcp:landed", "demo > groups build", inMain),
    row("mcp:accepted", "demo > cold caller", { accepted: { at: ago(6), check: "pnpm --dir core/eval exec vitest run cold-caller.test.ts: 14 passed" } }),
    row("mcp:worktree", "demo > phone icons", inMain, { worktree: join(dir, "worktrees", "phone-icons") }),
    row("mcp:task", "demo > design skills hub", inMain),
    row("mcp:branch", "demo > test caller", { landed: { repo, commit: unlanded, into: "main" } }),
    row("mcp:fresh", "demo > teams tests", inMain),
    row("mcp:running", "demo > phone alerts", inMain, { state: "running" }),
    row("mcp:question", "demo > fast feedback", inMain),
    row("mcp:queued", "demo > daemon role", inMain),
    row("mcp:word", "demo > captions", { accepted: { at: ago(6) } }, { state: "reported" }),
    row("mcp:both", "demo > quick fixes", inMain),
  ],
};
const other = {
  id: "20261109-ceo-demo-desktop",
  type: "handoff",
  thread: "desktop session 1",
  workers: [row("mcp:theirs", "demo > call video", inMain), row("mcp:both", "demo > quick fixes", inMain)],
};

const state = join(dir, "state");
const handoffs = join(dir, ".lev", "pm", "handoffs");
mkdirSync(state, { recursive: true });
mkdirSync(handoffs, { recursive: true });
const save = (path, value) => (writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`), path);
const files = {
  threads: save(join(state, "threads.json"), threads),
  tasks: save(join(state, "tasks.json"), tasks),
  waits: save(join(state, "waits.json"), waits),
  mine: save(join(handoffs, "20261110-ceo-demo.json"), mine),
  other: save(join(handoffs, "20261109-ceo-demo-desktop.json"), other),
};
copyFileSync(join(SKILL, "SKILL.md"), join(dir, "SKILL.md"));

const script = spawnSync(process.execPath, [
  join(SKILL, "scripts", "settle.mjs"), "--threads", files.threads, "--tasks", files.tasks, "--waits", files.waits,
  "--handoff", files.mine, "--handoff", files.other, "--owner", mine.id, "--now", NOW, "--root", dir,
], { encoding: "utf8" });
if (script.status !== 0) throw new Error(script.stderr);
const expected = JSON.parse(script.stdout).settle.map((r) => r.thread_id).sort();

const prompt = [
  `You are a new agent. The file ${join(dir, "SKILL.md")} is the lev-ceo skill; read it in full and follow its section 4 (Settle).`,
  `You are the CEO node whose handoff is ${files.mine} (id ${mine.id}); your own chat is mcp:ceo. Another CEO's handoff is ${files.other}.`,
  `The three saved reads are ${files.threads}, ${files.tasks} and ${files.waits}. The clock reads ${NOW}.`,
  `The settle script is not on this machine and there is no T3 tool: apply the skill's test yourself, part by part, to every chat in the thread list.`,
  `You may read files and run git. Change nothing.`,
  `End your reply with one line of JSON and nothing after it: {"settle": [<the thread ids you would settle yourself, now, without asking>]}`,
].join("\n");
const args = ["-p", prompt, "--allowedTools", "Read,Bash(git:*)"];
if (values.model) args.push("--model", values.model);
const agent = spawnSync("claude", args, { cwd: dir, encoding: "utf8", timeout: 600_000, maxBuffer: 16 * 1024 * 1024 });
const answer = [...(agent.stdout ?? "").matchAll(/\{\s*"settle"\s*:\s*\[[^\]]*\]\s*\}/g)].at(-1)?.[0];

if (!values.keep) rmSync(dir, { recursive: true, force: true });
console.log(`script  ${JSON.stringify(expected)}`);
if (!answer) {
  console.log(`agent   gave no list (claude exit ${agent.status})\n${(agent.stdout || agent.stderr || "").slice(-1500)}`);
  process.exit(2);
}
const got = JSON.parse(answer).settle.map(String).sort();
console.log(`agent   ${JSON.stringify(got)}`);
const same = JSON.stringify(got) === JSON.stringify(expected);
console.log(same ? "MATCH: the fresh agent settles the same chats as the script" : "DIFFERENT: the skill's words and the script disagree");
if (!same) console.log((agent.stdout ?? "").slice(-2500));
process.exit(same ? 0 : 1);
