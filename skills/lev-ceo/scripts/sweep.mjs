#!/usr/bin/env node
/**
 * The sweep index: one row for each open top-level chat of every project, and what the sweep does with it.
 * It sends nothing and calls no T3 tool: the chat that runs the sweep makes the T3 calls and gives this
 * program their results as files. Stdlib only (Node 22+).
 *
 * Where: ${XDG_STATE_HOME:-~/.local/state}/lev/ceo/sweep/
 *   index.json     the facts of each chat (version 2): what T3 said at the last scan, and the label a reader
 *                  gave its last reply. Written by scan and merge only, atomically (temp file, then rename).
 *   sends.jsonl    one line for each message the sweep chat sent: {threadId, at, wording, by, outcome}.
 *                  Written by sent only. It is the one place a send is written.
 *   to-read.tsv    the chats a reader labels next: threadId, cursor, item count, title. Written by scan.
 *   projects.json  project id -> title, from the last --projects file
 *   settings.json  optional: {idle_min_before_ask, read_if_changed_within_hours, never_read: ["<part of a title>"]}
 *   lock/          held by scan, merge or sent while it runs. A second one is refused (exit 2): run it again.
 *                  The lock of a process that is gone is taken over. show and brief take no lock: each file
 *                  is written in one step (a temp file, then a rename), so they read the old file or the new one.
 *
 * Nothing decided is stored. Each command works the choice of every row out again, from the index, the send
 * log and the clock. So two files cannot disagree about a choice, and `show` is never out of date.
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/sweep.mjs <command> [options]
 *   scan  --threads <file> [--running <file>] [--projects <file>] [--self <thread id>]
 *           --threads   the result of t3_thread_list {allProjects:true, settled:false, includeSubagents:false,
 *                       limit:100}. Every open top-level chat, in one page: a scan marks each chat that is not
 *                       in the list as settled, so any other list is refused.
 *           --running   the result of t3_thread_list {allProjects:true, includeSubagents:true,
 *                       statuses:["running","starting","queued","preparing"]}: a chat with a running worker waits.
 *           --projects  the result of t3_project_list {limit:100}: gives each row its project's name.
 *           --self      the chat that runs the sweep; it is skipped. Give it on each scan: a scan with no
 *                       --self names no chat.
 *   merge --labels <file>     take a reader's labels (JSON Lines) for the chats in to-read.tsv. Each label
 *                             holds the cursor the reader was given; a label for an older reply is not
 *                             taken and its chat is listed under `stale`. A label that is none of
 *                             plan_ready, needs_jp, waits_run, done is not taken (`unknown_label`). A chat
 *                             whose label was taken leaves to-read.tsv.
 *   brief --out <file>        print the reader's brief for the chats in to-read.tsv; the reader writes --out
 *   sent  --thread <id> --wording "<text>" [--by "<text>"]   log a message the sweep chat sent to a chat
 *   show                      print the rows
 * scan, merge, sent and show print {scanned_at, project, counts, rows}. They take --project <title> (one
 * project; with none, all projects), --all (also the skipped and the old rows) and --text.
 * Every command takes --now <ISO> (the clock, for tests) and --root <dir> (the state folder, for tests).
 * A command reads and checks all its input before its first write, so a refused command changes nothing.
 *
 * The cursor of a row is the chat's newest run and its item count when a reader last read its reply. A chat
 * is read again only when that changed. (T3's time of last change is no cursor: it also moves when the chat
 * got no new item.)
 *
 * Choices, in the order `show` prints them:
 *   unanswered  a person's message has no reply: the run was interrupted, failed or cancelled
 *   ask         the reply names approved work that is not done: tell the chat to continue
 *   read        the chat changed since the last read: a reader labels it
 *   queue       the reply holds questions for JP
 *   not yet     the chat changed or stopped less than 30 minutes ago
 *   leave       it runs, it waits on a run, it is done, or it was asked and no person spoke since
 *   skip, old   settled, snoozed, never read, this chat; or stopped more than 48 hours ago and never read
 * A program makes the choice from the label. It never decides what is approved.
 * Exit 0 ok, exit 2 bad input (the reason on stderr).
 */
import { appendFileSync, existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

export const DEFAULTS = { idle_min_before_ask: 30, read_if_changed_within_hours: 48, never_read: [] };
export const ORDER = ["unanswered", "ask", "read", "queue", "not yet", "leave", "skip", "old"];
const HIDDEN = new Set(["skip", "old"]);
const WAITING = new Set(["running", "starting", "queued", "preparing"]);
const DERIVED = ["choice", "why", "idle_min", "sends"];   // worked out by each command, never stored
const LABELS = new Set(["plan_ready", "needs_jp", "waits_run", "done"]);   // what a reader may answer (references/reader-brief.txt)
const CEO_CHAT = /^ceo\s*>/i;
const SKILL = join(dirname(fileURLToPath(import.meta.url)), "..");

export class InputError extends Error {}

export function defaultRoot(env = process.env) {
  return join(env.XDG_STATE_HOME || join(homedir(), ".local", "state"), "lev", "ceo", "sweep");
}

function readJson(file, what) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch (error) {
    throw new InputError(`cannot read ${what} ${file}: ${error.message}`);
  }
}

/** The objects of a JSON Lines file; [] when the file is not there. A line that is not JSON is bad input. */
function readLines(file, what) {
  if (!existsSync(file)) return [];
  const out = [];
  readFileSync(file, "utf8").split("\n").forEach((line, at) => {
    if (!line.trim()) return;
    let value;
    try {
      value = JSON.parse(line);
    } catch {
      throw new InputError(`${what} ${file}: line ${at + 1} is not JSON`);
    }
    out.push([value, at + 1]);
  });
  return out;
}
const oneLine = (text) => String(text ?? "").replace(/[\t\r\n]+/g, " ");
const topLevel = (t) => t.relationshipToParent !== "subagent";
const cursorOf = (t) => `${t.latestRunId || ""}#${t.itemCount}`;

/** Why a scan refuses this list, or null. The list must be every open top-level chat, in one page. */
export function checkList(list) {
  const threads = (list && list.threads) || [];
  if (!threads.length) return "the list is empty";
  if (list.nextCursor !== null && list.nextCursor !== undefined) return "the list is one page of many; list again with a limit that holds every open chat";
  if (threads.some((t) => t.settled)) return "the list holds a settled chat; list with settled: false";
  if (threads.some((t) => !topLevel(t))) return "the list holds worker chats; list with includeSubagents: false";
  return null;
}

/** Minutes since the chat stopped: from the end of its newest run when a reader recorded it, else from T3's time of last change. */
export function idleMinutes(row, now) {
  const fresh = row.cursor === row.now_cursor;
  return Math.floor((now - Date.parse((fresh && row.stopped_at) || row.updated_at)) / 60000);
}

/** What the sweep does with one row: [choice, why]. `row.sends` holds the chat's lines of the send log. It changes nothing. */
export function choose(row, now, set = DEFAULTS) {
  if (row.self) return ["skip", "this chat runs the sweep"];
  if (row.never_read) return ["skip", "this chat is never read"];
  if (row.settled) return ["skip", "settled"];
  if (row.snoozed) return ["skip", "snoozed"];
  if (row.status === "running") return ["leave", "runs now"];
  if (row.running_children > 0) return ["leave", `waits on ${row.running_children} running worker chat(s)`];
  const fresh = row.cursor === row.now_cursor;
  const idle = idleMinutes(row, now);
  const wait = set.idle_min_before_ask;
  if (!fresh) {
    // A chat that changed a moment ago is in use, and a reader costs about 12,000 tokens for each chat.
    if (idle < wait) return ["not yet", `changed ${idle} min ago; read after ${wait} min`];
    const hours = idle / 60;
    // A row with no time of last change is old, not read: this test is false for it.
    if (hours <= set.read_if_changed_within_hours) return ["read", row.cursor ? "changed since the last read" : "never read"];
    return ["old", Number.isNaN(hours) ? "no time of last change, not read" : `stopped ${Math.round(hours / 24)} days ago, not read`];
  }
  // A run that did not finish after a person's message. It waits too, because the person may still type.
  if (["interrupted", "failed", "cancelled"].includes(row.status) && row.last_user_by === "user") {
    return idle >= wait ? ["unanswered", `a person's message has no reply: the run was ${row.status}`] : ["not yet", `the run was ${row.status} ${idle} min ago`];
  }
  const questions = row.questions || [];
  if (row.label === "plan_ready") {
    // One ask for each word of a person: after a send, ask again only when a person spoke in the chat after it.
    const sends = row.sends || [];
    const last = sends.length ? sends[sends.length - 1] : null;
    // The two times are compared as instants. A time that cannot be read compares false, so it keeps the hold.
    const sentAt = last ? Date.parse(last.at) : NaN;
    const spokeAfter = row.last_user_by === "user" && Date.parse(row.last_user_at) > sentAt;
    const asked = last && !spokeAfter ? (Number.isNaN(sentAt) ? "asked before" : `asked at ${new Date(sentAt).toISOString().slice(11, 16)}Z`) : null;
    const held = asked || (row.ceo ? "a CEO chat is not asked" : null);   // a CEO chat runs its own loop
    if (held) return questions.length ? ["queue", `${held}; ${questions.length} question(s) for JP`] : ["leave", asked ? `${held}; no person spoke since` : held];
    return idle >= wait ? ["ask", "may hold approved work"] : ["not yet", `stopped ${idle} min ago`];
  }
  if (questions.length) return ["queue", `${questions.length} question(s) for JP`];
  if (row.label === "waits_run") return ["leave", "waits on a run"];
  if (row.label === "needs_jp") return ["queue", "waits on JP"];
  return ["leave", row.label || "no label"];
}

/** The state folder: where each file is, and how it is read. */
function store(root) {
  const at = (name) => join(root, name);
  return {
    root,
    at,
    settings: existsSync(at("settings.json")) ? { ...DEFAULTS, ...readJson(at("settings.json"), "the settings") } : DEFAULTS,
    load() {
      const index = existsSync(at("index.json")) ? readJson(at("index.json"), "the index") : { version: 2, scanned_at: null, self: null, rows: {} };
      if (!index.rows || typeof index.rows !== "object") throw new InputError(`the index ${at("index.json")} has no rows`);
      return index;
    },
    save(index) {
      index.version = 2;
      for (const row of Object.values(index.rows)) for (const key of DERIVED) delete row[key];   // also what version 1 stored
      this.put("index.json", `${JSON.stringify(index, null, 1)}\n`);
    },
    /** Writes one file in one step: a temp file, then a rename. A reader sees the old file or the new one. */
    put(name, text) {
      const temp = at(`.${name}.${process.pid}.tmp`);
      writeFileSync(temp, text);
      renameSync(temp, at(name));
    },
    projects: () => (existsSync(at("projects.json")) ? readJson(at("projects.json"), "the projects") : {}),
    /** thread id -> its lines of the send log, oldest first. A line that is no send record is bad input. */
    sends() {
      const by = new Map();
      for (const [line, n] of readLines(at("sends.jsonl"), "the send log")) {
        if (line === null || typeof line !== "object" || typeof line.threadId !== "string") throw new InputError(`the send log ${at("sends.jsonl")}: line ${n} is not a send record`);
        by.set(line.threadId, [...(by.get(line.threadId) || []), line]);
      }
      return by;
    },
  };
}

/** Runs one command that writes, alone: a second writer on the same state folder is refused, not queued. */
function withLock(s, now, work) {
  mkdirSync(s.root, { recursive: true });
  const lock = s.at("lock");
  const mine = { pid: process.pid, at: new Date(now).toISOString() };
  // The lock is a folder that holds its owner. It is made beside its place and moved there in one step, and a
  // move onto a folder that holds a file fails. So a lock is never seen without its owner.
  const take = () => {
    const draft = s.at(`.lock.${process.pid}`);
    rmSync(draft, { recursive: true, force: true });
    mkdirSync(draft);
    writeFileSync(join(draft, "owner.json"), JSON.stringify(mine));
    try {
      renameSync(draft, lock);
      return true;
    } catch (error) {
      rmSync(draft, { recursive: true, force: true });
      if (error.code === "ENOTEMPTY" || error.code === "EEXIST") return false;
      throw error;
    }
  };
  // The lock leaves in one step too: it is moved away, then deleted.
  const drop = () => {
    const gone = s.at(`.lock.${process.pid}.gone`);
    rmSync(gone, { recursive: true, force: true });
    try {
      renameSync(lock, gone);
    } catch (error) {
      if (error.code === "ENOENT") return;
      throw error;
    }
    rmSync(gone, { recursive: true, force: true });
  };
  const ownerOf = () => {
    try {
      return JSON.parse(readFileSync(join(lock, "owner.json"), "utf8"));
    } catch {
      return null;
    }
  };
  // A lock is held while the process that made it is alive. Its age does not release it.
  const holds = (owner) => {
    if (!owner || !Number.isInteger(owner.pid)) return false;
    try {
      process.kill(owner.pid, 0);   // signal 0 sends nothing: it asks whether the process is there
      return true;
    } catch (probe) {
      return probe.code === "EPERM";
    }
  };
  const refused = (owner) => new InputError(`another sweep command holds ${s.root} (process ${owner?.pid}, since ${owner?.at}); run this one again when it ends. When no sweep command runs, delete ${lock}`);
  if (!take()) {
    const first = ownerOf();
    if (holds(first)) throw refused(first);
    // The owner is gone. One command at a time may remove its lock: the one that makes this folder. It looks
    // at the owner again, so it never removes the lock of a command that started in between.
    const takeover = s.at("lock-takeover");
    try {
      mkdirSync(takeover);
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
      throw new InputError(`another sweep command takes over the lock of ${s.root}; run this one again. When no sweep command runs, delete ${takeover}`);
    }
    try {
      const owner = ownerOf();
      if (holds(owner)) throw refused(owner);
      drop();
      if (!take()) throw refused(ownerOf());
    } finally {
      rmSync(takeover, { recursive: true, force: true });
    }
  }
  try {
    return work();
  } finally {
    const owner = ownerOf();
    if (owner && owner.pid === mine.pid && owner.at === mine.at) drop();   // never the lock of another command
  }
}

/** Refuses a --project that no row and no known project has. Each command calls it before its first write. */
function checkProject(project, names) {
  if (!project) return;
  const known = new Set(names.filter(Boolean).map((name) => name.toLowerCase()));
  if (!known.has(project.toLowerCase())) throw new InputError(`no project named "${project}"; the index holds: ${[...known].sort().join(", ") || "none"}`);
}
const projectsOf = (s, index) => [...Object.values(s.projects()), ...Object.values(index.rows).map((r) => r.project)];

/**
 * The rows one reply shows, each with its choice worked out now: all projects, or one; without the skipped
 * and the old rows unless `all`. `sends` is the send log (store.sends()).
 */
function view(index, s, o, now, sends) {
  checkProject(o.project, projectsOf(s, index));
  const want = o.project ? o.project.toLowerCase() : null;
  const rows = Object.values(index.rows)
    .filter((r) => !want || (r.project || "").toLowerCase() === want)
    .map((r) => {
      const row = { ...r, sends: sends.get(r.threadId) || [] };
      const [choice, why] = choose(row, now, s.settings);
      const idle = idleMinutes(row, now);
      return { choice, why, idle_min: Number.isNaN(idle) ? 0 : idle, project: r.project, ceo: !!r.ceo, title: r.title, link: r.link, threadId: r.threadId, questions: r.questions || [] };
    });
  const counts = {};
  for (const r of rows) counts[r.choice] = (counts[r.choice] || 0) + 1;
  const shown = rows.filter((r) => o.all || !HIDDEN.has(r.choice));
  shown.sort((a, b) => ORDER.indexOf(a.choice) - ORDER.indexOf(b.choice) || a.idle_min - b.idle_min);
  return { scanned_at: index.scanned_at, project: o.project || "all", counts, rows: shown };
}

function asText(out) {
  const head = `${out.project} · scanned ${out.scanned_at} · ${Object.entries(out.counts).map(([c, n]) => `${c} ${n}`).join(", ")}`;
  return [head, ...out.rows.map((r) => [r.choice, `${r.idle_min}m`, r.project, oneLine(r.title).slice(0, 44), r.why].join("\t"))].join("\n");
}

function scan(s, o, now) {
  // Every input is read and checked before the first write: a refused scan changes nothing.
  if (!o.threads) throw new InputError("scan needs --threads <file>");
  const whole = readJson(o.threads, "--threads");
  const refused = checkList(whole);
  if (refused) throw new InputError(`scan refused: ${refused}`);
  const given = o.projects ? Object.fromEntries((readJson(o.projects, "--projects").projects || []).map((p) => [p.id, p.title])) : null;
  const names = given || s.projects();
  const projectOf = (t) => names[t.projectId] || t.projectId || "(no project)";
  const index = s.load();
  checkProject(o.project, [...Object.values(names), ...whole.threads.map(projectOf), ...Object.values(index.rows).map((r) => r.project)]);
  const kids = new Map();
  if (o.running) {
    for (const k of readJson(o.running, "--running").threads || []) {
      if (!topLevel(k) && WAITING.has(k.status)) kids.set(k.parentThreadId, (kids.get(k.parentThreadId) || 0) + 1);
    }
  }
  const sends = s.sends();

  if (given) s.put("projects.json", `${JSON.stringify(given, null, 1)}\n`);
  index.self = o.self || null;   // the chat this scan names; an earlier scan's chat is a chat like any other
  const never = s.settings.never_read.map((part) => part.toLowerCase());
  const seen = new Set();
  for (const t of whole.threads) {
    seen.add(t.threadId);
    const row = index.rows[t.threadId] || (index.rows[t.threadId] = { threadId: t.threadId, cursor: null, label: null, ready_steps: [], questions: [] });
    const title = t.title || "";
    Object.assign(row, {
      title, link: t.link, status: t.status, updated_at: t.updatedAt, item_count: t.itemCount, snoozed: !!t.snoozed, settled: !!t.settled, model: t.model,
      project_id: t.projectId || null, project: projectOf(t),
      now_cursor: cursorOf(t), ceo: CEO_CHAT.test(title), self: t.threadId === index.self,
      never_read: never.some((part) => title.toLowerCase().includes(part)),
      running_children: kids.get(t.threadId) || 0,
    });
  }
  for (const id of Object.keys(index.rows)) if (!seen.has(id)) index.rows[id].settled = true;   // it left the open list
  index.scanned_at = new Date(now).toISOString();
  s.save(index);
  // The list for the reader: what this scan says to read, in the project asked for.
  const toRead = view(index, s, { project: o.project }, now, sends).rows.filter((r) => r.choice === "read").map((r) => index.rows[r.threadId]);
  s.put("to-read.tsv", toRead.map((r) => [r.threadId, r.now_cursor, r.item_count, oneLine(r.title)].join("\t")).join("\n") + (toRead.length ? "\n" : ""));
  return { index, sends };
}

function merge(s, o, now) {
  if (!o.labels) throw new InputError("merge needs --labels <file>");
  if (!existsSync(o.labels)) throw new InputError(`cannot read --labels ${o.labels}`);
  const labels = readLines(o.labels, "--labels").map(([label]) => label);
  const index = s.load();
  checkProject(o.project, projectsOf(s, index));
  const sends = s.sends();
  const listed = existsSync(s.at("to-read.tsv")) ? readFileSync(s.at("to-read.tsv"), "utf8").split("\n").filter(Boolean) : [];
  const pending = new Map(listed.map((line) => line.split("\t").slice(0, 2)));
  const taken = new Set();
  let merged = 0;
  const missed = [];
  const stale = [];
  const unknown = [];
  for (const l of labels) {
    const id = l && typeof l === "object" ? l.threadId : undefined;
    const row = index.rows[id];
    if (!row || !pending.has(id) || taken.has(id)) { missed.push(id ?? null); continue; }
    // The reader copies the cursor it was given. A scan since then may have listed a newer reply: that label
    // is for an older reply, and the chat stays `read`.
    if (l.cursor !== pending.get(id)) { stale.push(id); continue; }
    // A label that is none of the four gives no choice. It is not taken, so the chat is read again.
    if (!LABELS.has(l.label)) { unknown.push(id); continue; }
    Object.assign(row, {
      cursor: l.cursor, label: l.label, label_reason: l.label_reason || "", ready_steps: l.ready_steps || [], questions: l.questions_for_jp || [],
      waits_on: l.waits_on || "", last_user_by: l.last_user_by || "none", last_user_at: l.last_user_at || null,
      last_user_from_other_chat: !!l.last_user_from_other_chat, stopped_at: l.stopped_at || null, read_at: new Date(now).toISOString(),
    });
    taken.add(id);
    merged += 1;
  }
  s.save(index);
  // A chat whose label was taken leaves the list: the brief counts what is left, and a reader is not started twice.
  const left = listed.filter((line) => !taken.has(line.split("\t")[0]));
  s.put("to-read.tsv", left.join("\n") + (left.length ? "\n" : ""));
  return { index, sends, extra: { merged, not_in_to_read: missed, stale, unknown_label: unknown } };
}

/** Logs one send. The log is all it writes: the hold on the chat is worked out from the log by each command. */
function sent(s, o, now) {
  if (!o.thread || !o.wording) throw new InputError('sent needs --thread <id> and --wording "<text>"');
  const index = s.load();
  if (!index.rows[o.thread]) throw new InputError(`no chat "${o.thread}" in the index`);
  checkProject(o.project, projectsOf(s, index));
  s.sends();   // a log that cannot be read is refused before the append
  // The time keeps its milliseconds: it is compared with the time of a person's message.
  const line = { threadId: o.thread, at: new Date(now).toISOString(), wording: o.wording, by: o.by || "the sweep chat", outcome: "pending" };
  appendFileSync(s.at("sends.jsonl"), `${JSON.stringify(line)}\n`);
  return { index, sends: s.sends() };
}

function brief(s, o) {
  if (!o.out) throw new InputError("brief needs --out <file>, the file the reader writes");
  const toRead = s.at("to-read.tsv");
  const count = existsSync(toRead) ? readFileSync(toRead, "utf8").split("\n").filter(Boolean).length : 0;
  if (!count) throw new InputError("nothing to read: to-read.tsv is empty; run scan first");
  const fill = { count, to_read: toRead, rules: join(SKILL, "references", "label-rules.txt"), out: resolve(o.out) };
  return readFileSync(join(SKILL, "references", "reader-brief.txt"), "utf8").replace(/\{\{(\w+)\}\}/g, (whole, key) => (key in fill ? String(fill[key]) : whole));
}

export function main(argv) {
  const { values: o, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: {
      threads: { type: "string" }, running: { type: "string" }, projects: { type: "string" }, self: { type: "string" },
      labels: { type: "string" }, out: { type: "string" }, thread: { type: "string" }, wording: { type: "string" }, by: { type: "string" },
      project: { type: "string" }, all: { type: "boolean" }, text: { type: "boolean" }, now: { type: "string" }, root: { type: "string" },
    },
  });
  const command = positionals[0];
  const now = o.now ? Date.parse(o.now) : Date.now();
  if (Number.isNaN(now)) throw new InputError(`--now ${o.now} is not a time`);
  const s = store(resolve(o.root || defaultRoot()));
  const writers = { scan, merge, sent };
  let done;
  if (command === "brief") return brief(s, o);
  if (command === "show") done = { index: s.load(), sends: s.sends() };
  else if (writers[command]) done = withLock(s, now, () => writers[command](s, o, now));
  else throw new InputError("usage: sweep.mjs scan|merge|brief|sent|show (the header lists the options)");
  const out = { ...(done.extra || {}), ...view(done.index, s, o, now, done.sends) };
  return o.text ? asText(out) : JSON.stringify(out, null, 1);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    console.log(main(process.argv.slice(2)));
  } catch (error) {
    if (!(error instanceof InputError) && error.code !== "ERR_PARSE_ARGS_UNKNOWN_OPTION") throw error;
    console.error(error.message);
    process.exit(2);
  }
}
