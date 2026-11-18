#!/usr/bin/env node
/**
 * The sweep index: one row for each open top-level chat of every project, and what the sweep does with it.
 * It sends nothing and calls no T3 tool: the chat that runs the sweep makes the T3 calls and gives this
 * program their results as files. Stdlib only (Node 22+).
 *
 * Where: ${XDG_STATE_HOME:-~/.local/state}/lev/ceo/sweep/
 *   index.json     the facts of each chat (version 2): what T3 said at the last scan, and the label a reader
 *                  gave its last reply. Written by scan and merge only.
 *   sends.jsonl    one line for each message the sweep chat sent: {threadId, at, wording, by, outcome}.
 *                  Written by sent only, one appended line for each send. It is the one place a send is written.
 *   to-read.jsonl  the chats a reader labels next, JSON Lines: {threadId, cursor, item_count, title}. Written by scan;
 *                  merge takes out each chat whose label it took.
 *   projects.json  project id -> title, from the last --projects file. Written by scan.
 *   settings.json  optional: {idle_min_before_ask, read_if_changed_within_hours, never_read: ["<part of a title>"]}
 *   lock           a file that scan, merge, sent or queue holds while it runs. A second one is refused (exit 2): run
 *                  it again. A lock is never taken over, also when its process is gone: the refusal says so
 *                  and names the file to delete. show and brief take no lock: index.json, to-read.jsonl and
 *                  projects.json are each replaced in one step (a temp file, then a rename), so a reader
 *                  sees the old file or the new one.
 *
 * Nothing decided is stored. Each command works the choice of every row out again, from the index, the send
 * log and the clock. So two files cannot disagree about a choice, and `show` is never out of date.
 * (An index that an older program wrote holds stored choices. No command uses them, and the next scan or
 * merge writes the index without them. show and sent do not write the index.)
 *
 * What is proved, and what is not. One command writes at a time (the lock). The program starts no process
 * and no worker: the test runs every command under Node's permission system. That run does not prove that it
 * opens no network connection (this Node has no network permission): for that, the test checks the imports.
 * scan, merge and sent write only in the state folder as long as no file there is a link to another place:
 * sent refuses a send log that is a link, and the other files are replaced, not written through. queue
 * writes in the queue folder (--queue-root), through the queue program; it writes no state file but the lock.
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/sweep.mjs <command> [options]
 *   scan  --threads <file> [--running <file>] [--projects <file>] [--self <thread id>]
 *           --threads   the result of t3_thread_list {allProjects:true, settled:false, includeSubagents:false,
 *                       limit:100}. Every open top-level chat, in one page: a scan marks each chat that is not
 *                       in the list as settled. The program refuses a list that it can see is another one
 *                       (empty, one page of many, with settled or worker chats). It cannot see a list
 *                       that a filter made shorter: the caller gives the whole list. Each field that
 *                       the program reads has one type (a text, a whole number, true or false); an
 *                       entry with another type in one of them is refused.
 *           --running   the result of t3_thread_list {allProjects:true, includeSubagents:true,
 *                       statuses:["running","starting","queued","preparing"]}: a chat with a running worker waits.
 *           --projects  the result of t3_project_list {limit:100}: gives each row its project's name.
 *           --self      the chat that runs the sweep; it is skipped. Give it on each scan: a scan with no
 *                       --self names no chat.
 *   merge --labels <file>     take a reader's labels (JSON Lines) for the chats in to-read.jsonl. Each label
 *                             holds the cursor the reader was given; a label for an older reply is not
 *                             taken and its chat is listed under `stale`. A label that is none of
 *                             plan_ready, needs_jp, waits_run, done is not taken (`unknown_label`). A chat
 *                             whose label was taken leaves to-read.jsonl.
 *   brief --out <file>        print the reader's brief for the chats in to-read.jsonl; the reader writes --out
 *   sent  --thread <id> --wording "<text>" [--by "<text>"]   log a message the sweep chat sent to a chat
 *   show                      print the rows
 *   queue --thread <id> [--title "<text>"] [--queue-root <dir>]
 *                             put the questions for JP into the queue of the chat that runs the sweep
 *                             (scripts/queue.mjs, called in this process; it writes in the queue folder,
 *                             ${XDG_STATE_HOME:-~/.local/state}/lev/ceo/queues, and holds the sweep lock).
 *                             Each chat that waits on JP is one item: its choice is `queue` or `unanswered`,
 *                             or it is `ask` and its newest reply also holds a question. The item's id is
 *                             the chat's id, with `source: "sweep"`, the project, the questions and the
 *                             cursor of the reply. Only items with that mark are touched. The same reply
 *                             never asks twice: an item that a person closed opens again only when the chat
 *                             has a new reply that waits on JP. An open item is closed in two cases only:
 *                             the chat was settled (or left the list), or the label of its newest reply
 *                             holds no question for JP. Its note starts with "sweep: ", and such an item
 *                             opens again when the chat is open again with the same reply. No other state
 *                             closes an item: the sweep's own chat, a chat that is never read, a snooze, a
 *                             run, a running worker. A shown item whose chat moved goes back to pending.
 *                             An open item follows its row: the title, the link and the project always;
 *                             the priority and the reason while its row is the one that asks (a row that
 *                             is skipped, runs or moved gives the reason of that state, not of the question).
 *                             --title (one character or more) opens the queue when the chat has none. It prints
 *                             {queue, project, added, updated, closed, back_to_pending, reopened, open}.
 *                             It reads and plans before it writes, and checks each planned item with the
 *                             queue program's own check before a queue is opened; the writes are one call
 *                             of the queue program for each change. A shown item goes back to pending
 *                             before it gets its new fields, so the next run finishes a run that stopped
 *                             in the middle. An item is found by its id, also when its chat moved to
 *                             another project. The queue program has no lock of its own: do not run it
 *                             by hand on this queue while this command runs.
 * scan, merge, sent and show print {scanned_at, project, counts, rows}. They take --project <title> (one
 * project; with none, all projects), --all (also the skipped and the old rows) and --text.
 * Every command takes --now <ISO> (the clock, for tests) and --root <dir> (the state folder, for tests).
 * A command reads and checks its input files before its first write: each field that it reads, in each
 * entry of the T3 lists, each label line and each line of the send log. The check is on the type of a
 * value. The tests hold a matrix of sample values (each gives exit 0 or 2 in each of those fields, and a
 * value that was taken stops no later command); a matrix is a sample, not a proof for every text.
 * A text of the right type is carried as it is: every file this program writes is JSON or JSON Lines, and
 * every value goes to the queue program as one `--name=value` argument. So a chat id or a run id may hold
 * a tab, a line break, or a leading "--" (the round-trip test takes such ids through scan, merge and
 * queue). `show --text` is for the eye only: it prints tabs between columns and is read by no command.
 * No text becomes the name of a file but one: the title of the chat that runs the sweep names its queue
 * folder, cut to 60 characters, so the title may have any length from one character. A folder given with --root or
 * --queue-root that the file system refuses (a part too long, a file in the way) is bad input (exit 2).
 * Not checked: what an older program or a hand wrote into index.json.
 * With --project, scan takes the project names of this scan (the --projects file and the chats of the
 * list), not the names an earlier scan stored.
 *
 * The cursor of a row is the chat's newest run and its item count when a reader last read its reply. A chat
 * is read again only when that changed. (T3's time of last change is no cursor: it also moves when the chat
 * got no new item.)
 *
 * Choices, in the order `show` prints them:
 *   unanswered  a person's message has no reply: the run was interrupted, failed or cancelled
 *               (not when the reader says that the message tells the chat to stop: `last_user_stops`)
 *   ask         the reply names approved work that is not done: tell the chat to continue
 *   read        the chat changed since the last read, or it was never read and stopped in the last 48 hours:
 *               a reader labels it. A chat that was read before is read again however old the change is,
 *               so a question that is on record is never hidden.
 *   queue       the reply holds questions for JP
 *   not yet     the chat changed or stopped less than 30 minutes ago
 *   leave       it runs, it waits on a run, it is done, or it was asked and no person spoke since
 *   skip        settled, snoozed, in never_read, or the chat that runs the sweep
 *   old         never read, and stopped more than 48 hours ago (or its time of last change cannot be read)
 * A program makes the choice from the label. It never decides what is approved.
 * A chat is told to continue once for each word of a person: after a send, `ask` comes back only when a
 * person spoke in the chat after the newest send in the log. The time of that word comes from the reader's
 * label, so the rule is as good as the label.
 * Exit 0 ok, exit 2 bad input (the reason on stderr).
 */
import { appendFileSync, closeSync, existsSync, lstatSync, mkdirSync, openSync, readFileSync, renameSync, rmSync, writeFileSync, writeSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { InputError as QueueInputError, defaultRoot as defaultQueueRoot, findQueue, main as queueMain, validateItem as checkQueueItem } from "./queue.mjs";

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
  let text;
  try {
    text = readFileSync(file, "utf8");
  } catch (error) {
    throw new InputError(`cannot read ${what} ${file}: ${error.message}`);
  }
  text.split("\n").forEach((line, at) => {
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
const oneLine = (text) => (typeof text === "string" ? text : "").replace(/[\t\r\n]+/g, " ");
/** A time as an instant. Only a text is a time: any other value is a time that cannot be read (NaN), never a stop. */
const instant = (value) => (typeof value === "string" ? Date.parse(value) : NaN);
const isText = (value) => typeof value === "string";
const isTexts = (value) => Array.isArray(value) && value.every(isText);
// What a label line may hold, beside its threadId: [key, the test, the words of the refusal]. A missing key is fine.
const LABEL_FIELDS = [
  ["cursor", isText, "a text"], ["label_reason", isText, "a text"], ["waits_on", isText, "a text"], ["last_user_by", isText, "a text"],
  ["last_user_at", (v) => v === null || isText(v), "a time as text, or null"], ["stopped_at", (v) => v === null || isText(v), "a time as text, or null"],
  ["ready_steps", isTexts, "a list of texts"], ["questions_for_jp", isTexts, "a list of texts"],
  ["last_user_stops", (v) => typeof v === "boolean", "true or false"],
  ["last_user_from_other_chat", (v) => typeof v === "boolean", "true or false"],
];
const isRecord = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const orNone = (ok) => (value) => value === null || value === undefined || ok(value);
const isFlag = (value) => typeof value === "boolean";
// What an entry of a T3 list may hold in the fields this program reads: [key, the test, the words of the refusal].
const CHAT_FIELDS = [
  ["itemCount", (v) => Number.isInteger(v) && v >= 0, "a whole number"],
  ["latestRunId", orNone(isText), "a text or null"], ["projectId", orNone(isText), "a text or null"], ["title", orNone(isText), "a text or null"],
  ["link", orNone(isText), "a text or null"], ["status", orNone(isText), "a text or null"], ["model", orNone(isText), "a text or null"],
  ["relationshipToParent", orNone(isText), "a text or null"], ["parentThreadId", orNone(isText), "a text or null"],
  ["settled", orNone(isFlag), "true, false or null"], ["snoozed", orNone(isFlag), "true, false or null"],
];
const WORKER_FIELDS = [
  ["relationshipToParent", orNone(isText), "a text or null"], ["parentThreadId", orNone(isText), "a text or null"], ["status", orNone(isText), "a text or null"],
];
/** The first field of `entry` that has a wrong type, as words, or null. */
function wrongField(entry, fields) {
  for (const [key, ok, words] of fields) if (!ok(entry[key])) return `${key} is not ${words}`;
  return null;
}
const topLevel = (t) => t.relationshipToParent !== "subagent";
const cursorOf = (t) => `${t.latestRunId || ""}#${t.itemCount}`;

/** Why a scan refuses this list, or null. The list must be every open top-level chat, in one page. */
export function checkList(list) {
  const threads = (list && list.threads) || [];
  if (!Array.isArray(threads) || !threads.length) return "the list is empty";
  if (list.nextCursor !== null && list.nextCursor !== undefined) return "the list is one page of many; list again with a limit that holds every open chat";
  if (threads.some((t) => !isRecord(t) || typeof t.threadId !== "string" || !t.threadId.trim())) return "the list holds an entry that is no chat (it has no threadId)";
  const noTime = threads.find((t) => Number.isNaN(instant(t.updatedAt)));
  if (noTime) return `the chat ${noTime.threadId} has no time of last change (updatedAt) that can be read`;
  // Every field the program reads has one type. A value of another type is refused here, before any write,
  // so no command meets it later.
  for (const t of threads) {
    const wrong = wrongField(t, CHAT_FIELDS);
    if (wrong) return `the chat ${t.threadId}: ${wrong}`;
  }
  if (threads.some((t) => t.settled)) return "the list holds a settled chat; list with settled: false";
  if (threads.some((t) => !topLevel(t))) return "the list holds worker chats; list with includeSubagents: false";
  return null;
}

/** Minutes since the chat stopped: from the end of its newest run when a reader recorded it, else from T3's time of last change. */
export function idleMinutes(row, now) {
  const fresh = row.cursor === row.now_cursor;
  return Math.floor((now - instant((fresh && row.stopped_at) || row.updated_at)) / 60000);
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
    if (Number.isNaN(hours)) return ["old", "no time of last change, not read"];
    // A chat that was read before is read again however old the change is: its row may hold a question
    // for JP, and `old` would hide it. The age limit is for chats that were never read.
    if (row.cursor) return ["read", "changed since the last read"];
    if (hours <= set.read_if_changed_within_hours) return ["read", "never read"];
    return ["old", `stopped ${Math.round(hours / 24)} days ago, never read`];
  }
  // A run that did not finish after a person's message. It waits too, because the person may still type.
  // Not when that message tells the chat to stop ("nvm"): the person ended the run, and the label decides.
  if (["interrupted", "failed", "cancelled"].includes(row.status) && row.last_user_by === "user" && row.last_user_stops !== true) {
    return idle >= wait ? ["unanswered", `a person's message has no reply: the run was ${row.status}`] : ["not yet", `the run was ${row.status} ${idle} min ago`];
  }
  const questions = row.questions || [];
  if (row.label === "plan_ready") {
    // One ask for each word of a person: after a send, ask again only when a person spoke in the chat after it.
    // The hold is the newest send by its time, not the last line of the log: a line may be logged late.
    // Times are compared as instants. A time that cannot be read keeps the hold: a send's, or the person's.
    const times = (row.sends || []).map((send) => instant(send.at));
    const unreadable = times.some(Number.isNaN);
    const sentAt = unreadable ? NaN : Math.max(...times);
    const spokeAfter = row.last_user_by === "user" && instant(row.last_user_at) > sentAt;
    const asked = times.length && !spokeAfter ? (unreadable ? "asked before" : `asked at ${new Date(sentAt).toISOString().slice(11, 16)}Z`) : null;
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
      if (!isRecord(index) || !isRecord(index.rows)) throw new InputError(`the index ${at("index.json")} has no rows`);
      // The rows are a dictionary by chat id. It has no prototype, so an id such as "__proto__" is a key like any other.
      index.rows = Object.assign(Object.create(null), index.rows);
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
      rmSync(temp, { force: true });
      writeFileSync(temp, text, { flag: "wx" });   // a new file: never written through a link that is in its place
      renameSync(temp, at(name));
    },
    /** project id -> its name, as the last scan with --projects stored it. */
    projects() {
      const stored = existsSync(at("projects.json")) ? readJson(at("projects.json"), "the projects") : {};
      return new Map(isRecord(stored) ? Object.entries(stored).filter(([, name]) => isText(name)) : []);
    },
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

/**
 * Runs one command that writes, alone: a second writer on the same state folder is refused, not queued.
 * The lock is one file, made with the flag that fails when the file is there (one step for the file system).
 * No command removes a lock that it did not make. So a lock that a stopped process left stays, and the
 * refusal says how to remove it. (An earlier form took such a lock over, and a reader showed that the
 * take-over could remove the lock of a live command.)
 */
function withLock(s, now, work) {
  try {
    mkdirSync(s.root, { recursive: true });
  } catch (error) {
    // --root is a path that the file system refuses (a part too long, a file in the way): bad input.
    throw new InputError(`cannot make the state folder ${s.root}: ${error.code || error.message}`);
  }
  const lock = s.at("lock");
  let handle;
  try {
    handle = openSync(lock, "wx");
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
    let owner = null;
    try {
      owner = JSON.parse(readFileSync(lock, "utf8"));
    } catch { /* the owner is between its two steps, or the file is not a lock of this program */ }
    let state = "its owner is not known";
    if (owner && Number.isInteger(owner.pid)) {
      let alive = true;
      try {
        process.kill(owner.pid, 0);   // signal 0 sends nothing: it asks whether the process is there
      } catch (probe) {
        alive = probe.code === "EPERM";
      }
      state = alive ? `process ${owner.pid} holds it since ${owner.at}` : `process ${owner.pid} took it at ${owner.at} and is gone`;
    }
    throw new InputError(`another sweep command holds the state folder ${s.root}: ${state}. Run this command again when it ends. A lock is never taken over: when no sweep command runs, delete ${lock}`);
  }
  try {
    writeSync(handle, JSON.stringify({ pid: process.pid, at: new Date(now).toISOString() }));
    closeSync(handle);
    return work();
  } finally {
    rmSync(lock, { force: true });
  }
}

/** Refuses a --project that is not one of `names`. Each command calls it before its first write. */
function checkProject(project, names) {
  if (!project) return;
  const known = new Set(names.filter((name) => isText(name) && name).map((name) => name.toLowerCase()));
  if (!known.has(project.toLowerCase())) throw new InputError(`no project named "${project}"; the known projects are: ${[...known].sort().join(", ") || "none"}`);
}
const projectsOf = (s, index) => [...s.projects().values(), ...Object.values(index.rows).map((r) => r.project)];
/** The name of a row's project as a text, also for a row that an older program wrote. */
const projectName = (r) => (isText(r.project) ? r.project : "");

/**
 * The rows one reply shows, each with its choice worked out now: all projects, or one; without the skipped
 * and the old rows unless `all`. `sends` is the send log (store.sends()). It checks nothing and writes
 * nothing: the command checks --project before its first write.
 */
function view(index, s, o, now, sends) {
  const want = o.project ? o.project.toLowerCase() : null;
  const rows = Object.values(index.rows)
    .filter((r) => !want || projectName(r).toLowerCase() === want)
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
  let given = null;
  if (o.projects) {
    const list = readJson(o.projects, "--projects");
    const entries = isRecord(list) ? list.projects : null;
    if (!Array.isArray(entries)) throw new InputError(`--projects ${o.projects} holds no list of projects`);
    const bad = entries.findIndex((p) => !isRecord(p) || !isText(p.id) || !isText(p.title));
    if (bad >= 0) throw new InputError(`--projects ${o.projects}: entry ${bad + 1} is no project (its id and its title must be texts)`);
    given = new Map(entries.map((p) => [p.id, p.title]));
  }
  const names = given || s.projects();
  const projectOf = (t) => names.get(t.projectId) || t.projectId || "(no project)";
  const index = s.load();
  // The names of this scan, not the ones an earlier scan stored: after the write, the rows hold these names.
  checkProject(o.project, [...names.values(), ...whole.threads.map(projectOf)]);
  const kids = new Map();
  if (o.running) {
    const list = readJson(o.running, "--running");
    const entries = isRecord(list) ? list.threads ?? [] : null;
    if (!Array.isArray(entries)) throw new InputError(`--running ${o.running} holds no list of chats`);
    entries.forEach((k, at) => {
      const wrong = isRecord(k) ? wrongField(k, WORKER_FIELDS) : "it is no chat";
      if (wrong) throw new InputError(`--running ${o.running}: entry ${at + 1}: ${wrong}`);
      if (!topLevel(k) && WAITING.has(k.status)) kids.set(k.parentThreadId, (kids.get(k.parentThreadId) || 0) + 1);
    });
  }
  const sends = s.sends();

  if (given) s.put("projects.json", `${JSON.stringify(Object.fromEntries(given), null, 1)}\n`);
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
  s.put(TO_READ, toRead.map((r) => `${JSON.stringify({ threadId: r.threadId, cursor: r.now_cursor, item_count: r.item_count, title: r.title })}\n`).join(""));
  return { index, sends };
}

// The list for the reader is JSON Lines: a line is {threadId, cursor, item_count, title}. JSON carries any
// text, so an id or a run id that holds a tab or a line break comes back as it went in.
const TO_READ = "to-read.jsonl";
function toReadRows(s) {
  if (!existsSync(s.at(TO_READ))) return [];
  return readFileSync(s.at(TO_READ), "utf8").split("\n").filter(Boolean).map((line) => {
    try {
      const one = JSON.parse(line);
      if (isRecord(one) && isText(one.threadId) && isText(one.cursor) && Number.isInteger(one.item_count) && isText(one.title)) return one;
    } catch { /* the refusal below */ }
    throw new InputError(`${s.at(TO_READ)} holds a line that this program did not write; run scan again`);
  });
}

function merge(s, o, now) {
  if (!o.labels) throw new InputError("merge needs --labels <file>");
  if (!existsSync(o.labels)) throw new InputError(`cannot read --labels ${o.labels}`);
  const labels = readLines(o.labels, "--labels").map(([label, n]) => {
    if (label === null || typeof label !== "object" || Array.isArray(label) || typeof label.threadId !== "string") throw new InputError(`--labels ${o.labels}: line ${n} is not a label (an object with a threadId)`);
    // Each field is checked here, before any write: a value of the wrong type never reaches the index.
    for (const [key, ok, words] of LABEL_FIELDS) {
      if (label[key] !== undefined && !ok(label[key])) throw new InputError(`--labels ${o.labels}: line ${n}: ${key} is not ${words}`);
    }
    return label;
  });
  const index = s.load();
  checkProject(o.project, projectsOf(s, index));
  const sends = s.sends();
  const listed = toReadRows(s);
  const pending = new Map(listed.map((one) => [one.threadId, one.cursor]));
  const taken = new Set();
  let merged = 0;
  const missed = [];
  const stale = [];
  const unknown = [];
  for (const l of labels) {
    const id = l.threadId;
    const row = index.rows[id];
    if (!row || !pending.has(id) || taken.has(id)) { missed.push(id); continue; }
    // The reader copies the cursor it was given. A scan since then may have listed a newer reply: that label
    // is for an older reply, and the chat stays `read`.
    if (l.cursor !== pending.get(id)) { stale.push(id); continue; }
    // A label that is none of the four gives no choice. It is not taken, so the chat is read again.
    if (!LABELS.has(l.label)) { unknown.push(id); continue; }
    Object.assign(row, {
      cursor: l.cursor, label: l.label, label_reason: l.label_reason || "", ready_steps: l.ready_steps || [], questions: l.questions_for_jp || [],
      waits_on: l.waits_on || "", last_user_by: l.last_user_by || "none", last_user_at: l.last_user_at || null,
      last_user_from_other_chat: !!l.last_user_from_other_chat, last_user_stops: l.last_user_stops === true,
      stopped_at: l.stopped_at || null, read_at: new Date(now).toISOString(),
    });
    taken.add(id);
    merged += 1;
  }
  s.save(index);
  // A chat whose label was taken leaves the list: the brief counts what is left, and a reader is not started twice.
  s.put(TO_READ, listed.filter((one) => !taken.has(one.threadId)).map((one) => `${JSON.stringify(one)}\n`).join(""));
  return { index, sends, extra: { merged, not_in_to_read: missed, stale, unknown_label: unknown } };
}

/** Logs one send. The log is all it writes: the hold on the chat is worked out from the log by each command. */
function sent(s, o, now) {
  if (!o.thread || !o.wording) throw new InputError('sent needs --thread <id> and --wording "<text>"');
  const index = s.load();
  if (!index.rows[o.thread]) throw new InputError(`no chat "${o.thread}" in the index`);
  checkProject(o.project, projectsOf(s, index));
  s.sends();   // a log that cannot be read is refused before the append
  // An append goes through a link to the file it names. The program writes in the state folder only.
  const log = s.at("sends.jsonl");
  if (existsSync(log) && lstatSync(log).isSymbolicLink()) throw new InputError(`the send log ${log} is a link to another file; the program writes in the state folder only`);
  // The time keeps its milliseconds: it is compared with the time of a person's message.
  const line = { threadId: o.thread, at: new Date(now).toISOString(), wording: o.wording, by: o.by || "the sweep chat", outcome: "pending" };
  appendFileSync(log, `${JSON.stringify(line)}\n`);
  return { index, sends: s.sends() };
}

/**
 * Puts the questions of the index into the queue of the chat that runs the sweep (scripts/queue.mjs, called
 * in this process). One item for each chat that waits on JP; the item's id is the chat's id.
 * It reads and plans first, checks each planned item with the queue program's own check, then writes.
 */
function queue(s, o, now) {
  if (!o.thread) throw new InputError("queue needs --thread <the chat that runs the sweep>");
  const index = s.load();
  const sends = s.sends();
  checkProject(o.project, projectsOf(s, index));
  const rows = view(index, s, { project: o.project, all: true }, now, sends).rows;
  const queueRoot = resolve(o["queue-root"] || defaultQueueRoot());
  const asQueue = (work) => {
    try {
      return work();
    } catch (error) {
      if (error instanceof QueueInputError) throw new InputError(`queue: ${error.message}`);
      throw error;
    }
  };
  // Every value goes to the queue program as `--name=value`, one argument. A value that starts with "--"
  // (a chat id, a note) is then a value, never an option.
  const flag = (name, value) => `--${name}=${value}`;
  const call = (command, values = {}, more = []) => asQueue(() => queueMain([
    command, ...Object.entries(values).map(([name, value]) => flag(name, value)), ...more,
    flag("thread", o.thread), flag("root", queueRoot), flag("now", new Date(now).toISOString()),
  ]));
  const exists = asQueue(() => findQueue(queueRoot, o.thread)) !== null;
  if (!exists && !o.title) throw new InputError(`no queue for thread ${o.thread} under ${queueRoot}; give --title "<the chat's title>" (one character or more) to open one`);
  const items = exists ? call("show", {}, ["--all"]).items : [];
  const want = o.project ? o.project.toLowerCase() : null;
  // Only the items this command made are its own. An item the CEO put by hand, and a settle item, stay as they are.
  // An item is found by its id, whatever project it had: a chat may move to another project. --project
  // narrows the rows (view), so an item whose chat is not in the rows is left.
  const own = new Map(items.filter((i) => i.source === "sweep").map((i) => [i.id, i]));
  const byHand = new Set(items.filter((i) => i.source !== "sweep").map((i) => i.id));
  const closed = (item) => item.status === "done" || item.status === "dropped";
  const steps = [];
  const count = { added: 0, updated: 0, closed: 0, back_to_pending: 0, reopened: 0 };
  const put = (fields, reopen) => steps.push({ command: "put", fields, more: reopen ? ["--reopen"] : [] });
  const move = (id, to, note) => steps.push({ command: "resolve", values: { item: id, to, note } });
  // The note of an item that this command closed starts with these words, so a later run can tell it from an
  // item that a person closed.
  const BY_SWEEP = "sweep: ";
  const bySweep = (item) => isText(item.outcome) && item.outcome.startsWith(BY_SWEEP);
  const close = (item, why) => {
    move(item.id, "done", `${BY_SWEEP}${why}`);
    count.closed += 1;
  };
  const backToPending = (item) => {
    if (item.status !== "presented") return;
    move(item.id, "pending", "the chat moved; the card that was shown is out of date");
    count.back_to_pending += 1;
  };
  const chatOf = (r) => ({ title: oneLine(r.title).trim() || "(no title)", link: isText(r.link) ? r.link : null, project: projectName(r) });
  // An open item that keeps its question while its row does not ask (a snooze, a run, a chat that moved)
  // follows the chat of its row: the title, the link, the project. Its reason and its priority stay those
  // of the reply that asks: the row gives the reason of the skip.
  const follow = (item, r) => {
    const chat = chatOf(r);
    if (!Object.keys(chat).some((key) => JSON.stringify(item[key] ?? null) !== JSON.stringify(chat[key]))) return;
    put({ id: item.id, kind: item.kind, reason: item.reason, ...chat });
    count.updated += 1;
  };
  const seen = new Set();
  for (const r of rows) {
    seen.add(r.threadId);
    const row = index.rows[r.threadId];
    const item = own.get(r.threadId);
    const fresh = !!row.cursor && row.cursor === row.now_cursor;   // the label is of the chat's newest reply
    const asks = fresh && r.questions.length > 0;
    // The chat waits on JP: his message has no reply, or its newest reply holds a question for him. A reply
    // that also names approved work (`ask`) still holds its question.
    if (r.choice === "unanswered" || r.choice === "queue" || (r.choice === "ask" && asks)) {
      if (byHand.has(r.threadId)) continue;
      const fields = {
        id: r.threadId, kind: "attention", reason: r.why, priority: r.choice === "unanswered" ? 1 : 2,
        threadId: r.threadId, source: "sweep", questions: r.questions, cursor: row.cursor, ...chatOf(r),
      };
      const differs = (key) => JSON.stringify(item[key] ?? null) !== JSON.stringify(fields[key] ?? null);
      if (!item) { put(fields); count.added += 1; }
      else if (item.cursor === row.cursor) {
        // The same reply does not ask twice: an item that a person closed stays closed. One that this command
        // closed (the chat was settled, or left the list) opens again, because nobody answered it.
        if (closed(item)) { if (bySweep(item)) { put(fields, true); count.reopened += 1; } }
        else if (["priority", "project", "title", "link", "reason"].some(differs)) { put(fields); count.updated += 1; }   // the row changed, the reply did not
      }
      else if (closed(item)) { put(fields, true); count.reopened += 1; }
      else { backToPending(item); put(fields); count.updated += 1; }   // the move first: a stop after it leaves the old cursor, and the next run puts the fields
      continue;
    }
    if (!item || closed(item)) continue;
    // An open item is closed in two cases only: the chat was settled, or the label of its newest reply holds
    // no question for JP. A row that holds a question keeps its item whatever its choice is: the sweep's own
    // chat, a chat that is never read, a snooze, a run, a running worker. The question is still open when
    // that state ends.
    if (row.settled) { close(item, "the chat is settled"); continue; }
    if (!fresh) { backToPending(item); follow(item, r); continue; }   // the chat moved and no reader read it yet
    if (asks || r.choice === "not yet") { follow(item, r); continue; }   // "not yet": the clock decides in a few minutes
    close(item, `the newest reply holds no question for JP: ${r.why}`);
  }
  for (const item of own.values()) {
    if (seen.has(item.id) || closed(item) || want) continue;   // with --project, a chat that is not in the rows may be another project's
    close(item, "the chat is not in the index");
  }
  // Each planned item is checked with the queue program's own check before a queue is opened or written.
  for (const step of steps) {
    if (step.command === "put") asQueue(() => checkQueueItem(step.fields));
  }

  const path = exists ? findQueue(queueRoot, o.thread) : call("open", { title: o.title }).path;
  for (const step of steps) {
    if (step.command === "put") call("put", { item: JSON.stringify(step.fields) }, step.more);
    else call(step.command, step.values);
  }
  const open = call("show").items.filter((i) => i.source === "sweep").length;
  return { queue: path, project: o.project || "all", ...count, open };
}

function brief(s, o) {
  if (!o.out) throw new InputError("brief needs --out <file>, the file the reader writes");
  const count = toReadRows(s).length;
  if (!count) throw new InputError(`nothing to read: ${TO_READ} is empty; run scan first`);
  const fill = { count, to_read: s.at(TO_READ), rules: join(SKILL, "references", "label-rules.txt"), out: resolve(o.out) };
  return readFileSync(join(SKILL, "references", "reader-brief.txt"), "utf8").replace(/\{\{(\w+)\}\}/g, (whole, key) => (key in fill ? String(fill[key]) : whole));
}

export function main(argv) {
  const { values: o, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: {
      threads: { type: "string" }, running: { type: "string" }, projects: { type: "string" }, self: { type: "string" },
      labels: { type: "string" }, out: { type: "string" }, thread: { type: "string" }, wording: { type: "string" }, by: { type: "string" },
      title: { type: "string" }, "queue-root": { type: "string" },
      project: { type: "string" }, all: { type: "boolean" }, text: { type: "boolean" }, now: { type: "string" }, root: { type: "string" },
    },
  });
  const command = positionals[0];
  const now = o.now === undefined ? Date.now() : Date.parse(o.now);   // an empty --now is a --now that is no time
  if (Number.isNaN(now)) throw new InputError(`--now ${o.now} is not a time`);
  const s = store(resolve(o.root || defaultRoot()));
  const writers = new Map([["scan", scan], ["merge", merge], ["sent", sent]]);   // a Map: "constructor" is no command
  let done;
  if (command === "brief") return brief(s, o);
  if (command === "queue") return JSON.stringify(withLock(s, now, () => queue(s, o, now)), null, 1);
  if (command === "show") {
    done = { index: s.load(), sends: s.sends() };
    checkProject(o.project, projectsOf(s, done.index));
  } else if (writers.has(command)) done = withLock(s, now, () => writers.get(command)(s, o, now));
  else throw new InputError("usage: sweep.mjs scan|merge|brief|sent|show|queue (the header lists the options)");
  const out = { ...(done.extra || {}), ...view(done.index, s, o, now, done.sends) };
  return o.text ? asText(out) : JSON.stringify(out, null, 1);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    console.log(main(process.argv.slice(2)));
  } catch (error) {
    // Bad input is exit 2 with the reason: what this program refuses, and an option that Node's parser refuses.
    if (!(error instanceof InputError) && !String(error.code || "").startsWith("ERR_PARSE_ARGS")) throw error;
    console.error(error.message);
    process.exit(2);
  }
}
