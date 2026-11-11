#!/usr/bin/env node
/**
 * Ready to settle: which worker chats a CEO may settle now, and why each other chat must wait.
 *
 * A chat is ready when all seven parts hold (the seventh: JP 2026-11-11, "its not 'is it idle' is IS THE ... WORK DONE"):
 *   left      the owner listed what the final report left undone (`left:` on the worker row, [] when
 *             nothing) and each leftover is fixed (`fixed: <sha>`) or tracked (`record: <path>#<id>`)
 *   owner     exactly one CEO handoff lists it under `workers:` with `thread_id`
 *   finished  its last turn ended (completed, failed, cancelled, interrupted or rolled_back)
 *   quiet     nothing happened in it for 2 hours
 *   no waits  no pending question and no queued message (counts the CEO read this turn)
 *   no task   no enabled scheduled task is bound to it
 *   proof     its work landed (`git merge-base --is-ancestor`) or the owner accepted it on a rerun
 *
 * Usage (run in the project checkout, or pass --root):
 *   node ~/.agents/skills/lev-ceo/scripts/settle.mjs --threads <file> --tasks <file> --waits <file>
 *        [--handoff <file> ...] [--owner <handoff id>] [--self <thread id>] [--now <ISO time>]
 *        [--quiet-hours <n>] [--root <dir>] [--text]
 *
 * --threads  the `t3_thread_list` result (settled:false), or a list of rows with
 *            threadId, title, status, updatedAt
 * --tasks    the `list_scheduled_tasks` result, or a list of rows with title, enabled, boundThreadId
 * --waits    {"<thread id>": {"questions": <n>, "queued": <n>}} from `t3_pending_request` and `t3_queue`
 * --handoff  a CEO handoff (YAML or JSON); default: every <root>/.lev/pm/handoffs/*ceo*.yaml
 * --owner    list under `settle` only the chats this handoff id owns; ready chats of another CEO
 *            go under `ask_owner`
 *
 * Prints JSON: {now, settle: [...], ask_owner: [...], hold: [...]}. Each `hold` row has `reasons`.
 * Exit 0 on a run that could read its input; exit 2 on input it could not read.
 */
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { isAbsolute, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

const ENDED = new Set(["completed", "failed", "cancelled", "interrupted", "rolled_back"]);

class InputError extends Error {}

function readJson(file, what) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch (error) {
    throw new InputError(`${what}: cannot read ${file}: ${error.message}`);
  }
}

function readHandoff(file, root) {
  if (file.endsWith(".json")) return readJson(file, "handoff");
  let yaml;
  try {
    yaml = createRequire(join(root, "package.json"))("yaml");
  } catch {
    throw new InputError(`handoff: no "yaml" library under ${root}; run in the Lev checkout or pass --root`);
  }
  try {
    return yaml.parse(readFileSync(file, "utf8"));
  } catch (error) {
    throw new InputError(`handoff: cannot read ${file}: ${error.message}`);
  }
}

const rowsOf = (value, key) => (Array.isArray(value) ? value : (value?.[key] ?? []));

/** Each worker row that names a chat, with the handoff that claims it. A row without `thread_id` is a note. */
export function claims(handoffs) {
  const byThread = new Map();
  for (const handoff of handoffs) {
    for (const worker of Array.isArray(handoff?.workers) ? handoff.workers : []) {
      if (!worker || typeof worker.thread_id !== "string") continue;
      const list = byThread.get(worker.thread_id) ?? [];
      list.push({ owner: String(handoff.id ?? "unnamed handoff"), worker });
      byThread.set(worker.thread_id, list);
    }
  }
  return byThread;
}

function landedIn(landed, root) {
  const repo = isAbsolute(landed.repo ?? "") ? landed.repo : resolve(root, landed.repo ?? ".");
  const run = spawnSync("git", ["-C", repo, "merge-base", "--is-ancestor", String(landed.commit), String(landed.into)], { encoding: "utf8" });
  if (run.status === 0) return { ok: true };
  if (run.status === 1) return { ok: false, why: `not landed: ${landed.commit} is not in ${landed.into}` };
  return { ok: false, why: `can't tell if it landed: git said "${(run.stderr ?? "").trim().split("\n")[0]}"` };
}

function proofOf(worker, root) {
  const proof = worker.proof ?? {};
  if (proof.landed) return landedIn(proof.landed, root);
  const accepted = proof.accepted;
  if (accepted && !Number.isNaN(Date.parse(accepted.at)) && String(accepted.check ?? "").trim()) return { ok: true };
  if (accepted) return { ok: false, why: "acceptance has no rerun: it needs `at` and the `check` the owner ran" };
  return { ok: false, why: "no proof: work neither landed nor accepted on a rerun" };
}

/** Why the row's `left` list does not let the chat settle; [] when every leftover has a way out. */
function leftProblems(worker) {
  const left = worker.left;
  if (!Array.isArray(left)) return ["leftovers not read: the row has no `left` list (use [] when the report left nothing)"];
  const problems = [];
  for (const item of left) {
    const entry = item && typeof item === "object" ? item : { what: item }; // a bare string has no way out
    const what = String(entry.what ?? "").trim() || "an entry with no `what`";
    const fixed = String(entry.fixed ?? "").trim();
    const record = String(entry.record ?? "").trim();
    if (!fixed && !record) problems.push(`leftover with no record: ${what}`);
    else if (record && /handoffs\//.test(record)) problems.push(`leftover tracked only in a handoff: ${what}`);
  }
  return problems;
}

/** Decide every unsettled chat. Pure but for the git call in `proofOf`. */
export function decide({ threads, tasks, waits, handoffs, owner, self, now, quietHours = 2, root = process.cwd() }) {
  const byThread = claims(handoffs);
  const out = { now: new Date(now).toISOString(), settle: [], ask_owner: [], hold: [] };
  for (const thread of threads) {
    const id = thread.threadId;
    if (thread.settled === true || id === self) continue;
    const row = { thread_id: id, title: thread.title ?? "", owner: null };
    const reasons = [];
    const claimed = byThread.get(id) ?? [];

    if (claimed.length === 0) reasons.push("no owner: no CEO handoff lists it under workers");
    else if (claimed.length > 1) reasons.push(`two owners: ${claimed.map((c) => c.owner).join(" and ")}`);
    else row.owner = claimed[0].owner;

    if (!ENDED.has(thread.status)) reasons.push(`not finished: status ${thread.status}`);

    const idle = (new Date(now) - new Date(thread.updatedAt)) / 3_600_000;
    if (!(idle >= quietHours)) reasons.push(`not quiet: last activity ${Math.max(idle, 0).toFixed(1)} hours ago, needs ${quietHours}`);

    const wait = waits[id];
    if (!wait) reasons.push("waits not read: no pending-question and queue counts for it");
    else {
      if (wait.questions > 0) reasons.push(`${wait.questions} pending question(s)`);
      if (wait.queued > 0) reasons.push(`${wait.queued} queued message(s)`);
    }

    const bound = tasks.filter((task) => task.boundThreadId === id);
    for (const task of bound.filter((t) => t.enabled)) reasons.push(`enabled scheduled task: ${task.title}`);

    if (claimed.length === 1) {
      const proof = proofOf(claimed[0].worker, root);
      if (!proof.ok) reasons.push(proof.why);
      reasons.push(...leftProblems(claimed[0].worker));
    }

    if (reasons.length > 0) {
      out.hold.push({ ...row, reasons });
      continue;
    }
    const worker = claimed[0].worker;
    const ready = {
      ...row,
      cleanup: {
        worktree: worker.worktree ?? null,
        disabled_tasks: bound.map((task) => task.scheduledTaskId ?? task.title),
      },
    };
    (owner && row.owner !== owner ? out.ask_owner : out.settle).push(ready);
  }
  return out;
}

function main(argv) {
  const { values } = parseArgs({
    args: argv,
    options: {
      threads: { type: "string" },
      tasks: { type: "string" },
      waits: { type: "string" },
      handoff: { type: "string", multiple: true },
      owner: { type: "string" },
      self: { type: "string" },
      now: { type: "string" },
      "quiet-hours": { type: "string" },
      root: { type: "string" },
      text: { type: "boolean" },
    },
  });
  for (const need of ["threads", "tasks", "waits"]) if (!values[need]) throw new InputError(`--${need} <file> is required`);
  const root = resolve(values.root ?? process.cwd());
  const listing = readJson(values.threads, "threads");
  const folder = join(root, ".lev", "pm", "handoffs");
  const files = values.handoff ?? (existsSync(folder) ? readdirSync(folder).filter((f) => /ceo/.test(f) && /\.ya?ml$/.test(f)).map((f) => join(folder, f)) : []);
  const result = decide({
    threads: rowsOf(listing, "threads"),
    tasks: rowsOf(readJson(values.tasks, "tasks"), "tasks"),
    waits: readJson(values.waits, "waits"),
    handoffs: files.map((file) => readHandoff(file, root)),
    owner: values.owner,
    self: values.self ?? (Array.isArray(listing) ? undefined : listing.currentThreadId),
    now: values.now ?? new Date().toISOString(),
    quietHours: values["quiet-hours"] ? Number(values["quiet-hours"]) : 2,
    root,
  });
  if (!values.text) return console.log(JSON.stringify(result, null, 2));
  for (const row of result.settle) console.log(`settle     ${row.title} (${row.thread_id})`);
  for (const row of result.ask_owner) console.log(`ask owner  ${row.title} (${row.thread_id}) · ${row.owner}`);
  for (const row of result.hold) console.log(`hold       ${row.title} (${row.thread_id}) · ${row.reasons.join("; ")}`);
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    if (!(error instanceof InputError)) throw error;
    console.error(error.message);
    process.exit(2);
  }
}
