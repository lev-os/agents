#!/usr/bin/env node
/**
 * The sweep index: one row for each open top-level chat of every project, and what the sweep does with it.
 * It sends nothing and calls no T3 tool: the chat that runs the sweep makes the T3 calls and gives this
 * program their results as files. Stdlib only (Node 22+).
 *
 * Where: ${XDG_STATE_HOME:-~/.local/state}/lev/ceo/sweep/
 *   index.json     the rows now (version 1), written atomically (temp file, then rename)
 *   to-read.tsv    the chats a reader labels next: threadId, cursor, item count, title
 *   sends.jsonl    one line for each message the sweep chat sent: {threadId, at, wording, by, outcome}
 *   projects.json  project id -> title, from the last --projects file
 *   settings.json  optional: {idle_min_before_ask, read_if_changed_within_hours, never_read: ["<part of a title>"]}
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
 *                             taken and its chat is listed under `stale`.
 *   brief --out <file>        print the reader's brief for the chats in to-read.tsv; the reader writes --out
 *   sent  --thread <id> --wording "<text>" [--by "<text>"]   log a message the sweep chat sent to a chat
 *   show                      print the rows
 * scan, merge, sent and show print {scanned_at, project, counts, rows}. They take --project <title> (one
 * project; with none, all projects), --all (also the skipped and the old rows) and --text.
 * Every command takes --now <ISO> (the clock, for tests) and --root <dir> (the state folder, for tests).
 * A command reads and checks all its input before its first write, so a refused command changes nothing.
 * sends.jsonl is the one place a send is written: each command reads the sends from it, not from the index.
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
import { appendFileSync, existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

export const DEFAULTS = { idle_min_before_ask: 30, read_if_changed_within_hours: 48, never_read: [] };
export const ORDER = ["unanswered", "ask", "read", "queue", "not yet", "leave", "skip", "old"];
const HIDDEN = new Set(["skip", "old"]);
const WAITING = new Set(["running", "starting", "queued", "preparing"]);
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
    try {
      out.push(JSON.parse(line));
    } catch {
      throw new InputError(`${what} ${file}: line ${at + 1} is not JSON`);
    }
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

/** What the sweep does with one row: [choice, why]. Sets row.idle_min. */
export function choose(row, now, set = DEFAULTS) {
  if (row.self) return ["skip", "this chat runs the sweep"];
  if (row.never_read) return ["skip", "this chat is never read"];
  if (row.settled) return ["skip", "settled"];
  if (row.snoozed) return ["skip", "snoozed"];
  if (row.status === "running") return ["leave", "runs now"];
  if (row.running_children > 0) return ["leave", `waits on ${row.running_children} running worker chat(s)`];
  const fresh = row.cursor === row.now_cursor;
  // The end of the newest run, when a reader recorded it; else T3's time of last change, which can be later.
  const idle = Math.floor((now - Date.parse((fresh && row.stopped_at) || row.updated_at)) / 60000);
  row.idle_min = idle;
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

function store(root) {
  const at = (name) => join(root, name);
  const settings = existsSync(at("settings.json")) ? { ...DEFAULTS, ...readJson(at("settings.json"), "the settings") } : DEFAULTS;
  return {
    at,
    settings,
    load: () => (existsSync(at("index.json")) ? readJson(at("index.json"), "the index") : { version: 1, scanned_at: null, rows: {} }),
    save(index) {
      mkdirSync(root, { recursive: true });
      writeFileSync(at("index.json.tmp"), `${JSON.stringify(index, null, 1)}\n`);
      renameSync(at("index.json.tmp"), at("index.json"));
    },
    projects: () => (existsSync(at("projects.json")) ? readJson(at("projects.json"), "the projects") : {}),
  };
}

/**
 * The choice of every row again. The sends come from sends.jsonl each time, never from the index: the log is
 * the one place a send is written, so a send that is in the log always holds its chat.
 */
function rechoose(index, now, s) {
  const sends = new Map();
  for (const line of readLines(s.at("sends.jsonl"), "the send log")) sends.set(line.threadId, [...(sends.get(line.threadId) || []), line]);
  for (const row of Object.values(index.rows)) {
    row.sends = sends.get(row.threadId) || [];
    [row.choice, row.why] = choose(row, now, s.settings);
  }
}

/** Refuses a --project that no row and no known project has. Each command calls it before its first write. */
function checkProject(project, names) {
  if (!project) return;
  const known = new Set(names.filter(Boolean).map((name) => name.toLowerCase()));
  if (!known.has(project.toLowerCase())) throw new InputError(`no project named "${project}"; the index holds: ${[...known].sort().join(", ") || "none"}`);
}
const projectsOf = (s, index) => [...Object.values(s.projects()), ...Object.values(index.rows).map((r) => r.project)];

/** The rows one reply shows: all projects, or one; without the skipped and the old rows unless `all`. */
function view(index, s, { project, all }) {
  let rows = Object.values(index.rows);
  if (project) {
    checkProject(project, projectsOf(s, index));
    rows = rows.filter((r) => (r.project || "").toLowerCase() === project.toLowerCase());
  }
  const counts = {};
  for (const r of rows) counts[r.choice] = (counts[r.choice] || 0) + 1;
  const shown = rows.filter((r) => all || !HIDDEN.has(r.choice));
  shown.sort((a, b) => ORDER.indexOf(a.choice) - ORDER.indexOf(b.choice) || (a.idle_min ?? 0) - (b.idle_min ?? 0));
  return {
    scanned_at: index.scanned_at,
    project: project || "all",
    counts,
    rows: shown.map((r) => ({ choice: r.choice, why: r.why, idle_min: r.idle_min ?? 0, project: r.project, ceo: !!r.ceo, title: r.title, link: r.link, threadId: r.threadId, questions: r.questions || [] })),
  };
}

function asText(out) {
  const head = `${out.project} · scanned ${out.scanned_at} · ${Object.entries(out.counts).map(([c, n]) => `${c} ${n}`).join(", ")}`;
  return [head, ...out.rows.map((r) => [r.choice, `${r.idle_min}m`, r.project, oneLine(r.title).slice(0, 44), r.why].join("\t"))].join("\n");
}

function writeToRead(index, s, project) {
  const rows = view(index, s, { project, all: false }).rows.filter((r) => r.choice === "read").map((r) => index.rows[r.threadId]);
  writeFileSync(s.at("to-read.tsv"), rows.map((r) => [r.threadId, r.now_cursor, r.item_count, oneLine(r.title)].join("\t")).join("\n") + (rows.length ? "\n" : ""));
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
  readLines(s.at("sends.jsonl"), "the send log");
  mkdirSync(s.at(""), { recursive: true });
  if (given) writeFileSync(s.at("projects.json"), `${JSON.stringify(given, null, 1)}\n`);
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
  rechoose(index, now, s);
  index.scanned_at = new Date(now).toISOString();
  s.save(index);
  writeToRead(index, s, o.project);
  return index;
}

function merge(s, o, now) {
  if (!o.labels) throw new InputError("merge needs --labels <file>");
  if (!existsSync(o.labels)) throw new InputError(`cannot read --labels ${o.labels}`);
  const labels = readLines(o.labels, "--labels");
  const index = s.load();
  checkProject(o.project, projectsOf(s, index));
  const pending = new Map(existsSync(s.at("to-read.tsv")) ? readFileSync(s.at("to-read.tsv"), "utf8").split("\n").filter(Boolean).map((line) => line.split("\t").slice(0, 2)) : []);
  let merged = 0;
  const missed = [];
  const stale = [];
  for (const l of labels) {
    const row = index.rows[l.threadId];
    if (!row || !pending.has(l.threadId)) { missed.push(l.threadId); continue; }
    // The reader copies the cursor it was given. A scan since then may have listed a newer reply: that label
    // is for an older reply, and the chat stays `read`.
    if (l.cursor !== pending.get(l.threadId)) { stale.push(l.threadId); continue; }
    Object.assign(row, {
      cursor: l.cursor, label: l.label, label_reason: l.label_reason || "", ready_steps: l.ready_steps || [], questions: l.questions_for_jp || [],
      waits_on: l.waits_on || "", last_user_by: l.last_user_by || "none", last_user_at: l.last_user_at || null,
      last_user_from_other_chat: !!l.last_user_from_other_chat, stopped_at: l.stopped_at || null, read_at: new Date(now).toISOString(),
    });
    merged += 1;
  }
  rechoose(index, now, s);
  s.save(index);
  return { index, extra: { merged, not_in_to_read: missed, stale } };
}

function sent(s, o, now) {
  if (!o.thread || !o.wording) throw new InputError('sent needs --thread <id> and --wording "<text>"');
  const index = s.load();
  const row = index.rows[o.thread];
  if (!row) throw new InputError(`no chat "${o.thread}" in the index`);
  checkProject(o.project, projectsOf(s, index));
  readLines(s.at("sends.jsonl"), "the send log");   // a log that cannot be read is refused before the append
  const line = { threadId: o.thread, at: new Date(now).toISOString().replace(/\.\d{3}Z$/, "Z"), wording: o.wording, by: o.by || "the sweep chat", outcome: "pending" };
  // The log first: when the save of the index fails after it, the next command still reads the send from the log.
  appendFileSync(s.at("sends.jsonl"), `${JSON.stringify(line)}\n`);
  rechoose(index, now, s);
  s.save(index);
  return index;
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
  if (command === "brief") return brief(s, o);
  let index;
  let extra = {};
  if (command === "scan") index = scan(s, o, now);
  else if (command === "merge") ({ index, extra } = merge(s, o, now));
  else if (command === "sent") index = sent(s, o, now);
  else if (command === "show") index = s.load();
  else throw new InputError("usage: sweep.mjs scan|merge|brief|sent|show (the header lists the options)");
  const out = { ...extra, ...view(index, s, o) };
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
