#!/usr/bin/env node
/**
 * The chat queue: the chats that need the CEO or JP, worked one head per reply, kept on disk so it
 * lives through a compaction. One queue for each CEO chat. Stdlib only (Node 22+).
 *
 * Where: ${XDG_STATE_HOME:-~/.local/state}/lev/ceo/queues/<chat-slug>-<YYYYMMDDTHHMMZ>/
 *   queue.json    the queue now (schema version 1), written atomically (temp file, then rename)
 *   events.jsonl  one line per change: {at, item, from, to, note}
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/queue.mjs <command> --thread <id> [options]
 *   open    --thread <id> --title "<title>"            -> {path, created}
 *   show    --thread <id> [--all] [--text]             -> open items (all with --all), in queue order
 *   put     --thread <id> --item '<json>' | --item-file <path> [--reopen]  -> upsert by id
 *   next    --thread <id>                              -> {item, left, leftTitles}; marks the head presented
 *   resolve --thread <id> --item <id> --to done|waiting|dropped|pending --note "<text>"
 *   due     --thread <id>                              -> {refresh, hygiene}
 *   ran     --thread <id> --kind refresh|hygiene       -> stamps lastRefreshAt or lastHygieneAt
 * Every command takes --now <ISO> (the clock, for tests) and --root <dir> (the folder that holds the
 * queue folders, for tests).
 *
 * Queue order: the presented item first (it stays the head until resolved), then pending by priority
 * (1 first) then addedAt, then waiting, then done and dropped. A watch item is never the head and never
 * counted in `left`: refresh reads its chat and puts it again as attention when it needs JP.
 * Moves: pending -> presented (by next); presented -> done | waiting | dropped | pending;
 *        waiting -> pending | done | dropped.
 * JSON on stdout. Exit 0 ok, exit 2 bad input (the reason on stderr).
 */
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

export const KINDS = ["attention", "settle", "watch"];
export const STATUSES = ["pending", "presented", "waiting", "done", "dropped"];
const CLOSED = new Set(["done", "dropped"]);
const MOVES = {
  pending: ["presented"],
  presented: ["done", "waiting", "dropped", "pending"],
  waiting: ["pending", "done", "dropped"],
  done: [],
  dropped: [],
};
const CARD_KEYS = ["goal", "state", "ask", "recommend", "ifNoAnswer"];
const MANAGED = ["status", "addedAt", "updatedAt", "presentedAt", "doneAt", "outcome"];
const DEFAULT_CADENCE = { refreshEveryMin: 60, hygieneEveryMin: 180 };

export class InputError extends Error {}

export function slugify(title) {
  return String(title).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

export function stamp(iso) {
  return iso.replace(/[-:]/g, "").slice(0, 13) + "Z"; // 2026-11-10T23:30:00Z -> 20261110T2330Z
}

export function defaultRoot(env = process.env) {
  const state = env.XDG_STATE_HOME || join(homedir(), ".local", "state");
  return join(state, "lev", "ceo", "queues");
}

function readQueue(dir) {
  const file = join(dir, "queue.json");
  let queue;
  try {
    queue = JSON.parse(readFileSync(file, "utf8"));
  } catch (error) {
    throw new InputError(`cannot read ${file}: ${error.message}`);
  }
  if (queue?.version !== 1) throw new InputError(`${file}: version ${queue?.version} is not 1`);
  if (!Array.isArray(queue.items)) throw new InputError(`${file}: items is not a list`);
  queue.cadence = { ...DEFAULT_CADENCE, ...(queue.cadence ?? {}) };
  return queue;
}

function writeQueue(dir, queue) {
  const file = join(dir, "queue.json");
  const temp = join(dir, `.queue.json.${process.pid}.${Date.now()}.tmp`);
  writeFileSync(temp, `${JSON.stringify(queue, null, 2)}\n`);
  renameSync(temp, file);
}

function logEvent(dir, event) {
  appendFileSync(join(dir, "events.jsonl"), `${JSON.stringify(event)}\n`);
}

/** The folder of this thread's queue, newest first when several match; null when none. */
export function findQueue(root, threadId) {
  if (!existsSync(root)) return null;
  const hits = [];
  for (const name of readdirSync(root, { withFileTypes: true })) {
    if (!name.isDirectory()) continue;
    const dir = join(root, name.name);
    if (!existsSync(join(dir, "queue.json"))) continue;
    let queue;
    try {
      queue = JSON.parse(readFileSync(join(dir, "queue.json"), "utf8"));
    } catch {
      continue;
    }
    if (queue?.chat?.threadId === threadId) hits.push({ dir, createdAt: queue.createdAt ?? "", name: name.name });
  }
  hits.sort((a, b) => (b.createdAt.localeCompare(a.createdAt)) || b.name.localeCompare(a.name));
  return hits[0]?.dir ?? null;
}

const byPriority = (a, b) => (a.priority ?? 2) - (b.priority ?? 2) || String(a.addedAt ?? "").localeCompare(String(b.addedAt ?? ""));
const RANK = { presented: 0, pending: 1, waiting: 2, done: 3, dropped: 3 };

/** The items in queue order (see the header). */
export function ordered(items) {
  return [...items].sort((a, b) => (RANK[a.status] ?? 4) - (RANK[b.status] ?? 4) || byPriority(a, b));
}

/** A watch item is for the refresh pass, never for JP: refresh reads its chat and puts it again as attention when it needs him. */
const forJp = (item) => item.kind !== "watch";

/** The head: the presented item, else the first pending item that is not a watch item; null when the queue has none. */
export function head(items) {
  const presented = items.filter((item) => item.status === "presented" && forJp(item)).sort(byPriority);
  if (presented.length > 0) return presented[0];
  return items.filter((item) => item.status === "pending" && forJp(item)).sort(byPriority)[0] ?? null;
}

function validateItem(item) {
  if (item === null || typeof item !== "object" || Array.isArray(item)) throw new InputError("item: not a JSON object");
  for (const key of ["id", "kind", "title", "reason"]) {
    if (typeof item[key] !== "string" || item[key].trim() === "") throw new InputError(`item: no ${key}`);
  }
  if (!KINDS.includes(item.kind)) throw new InputError(`item ${item.id}: kind "${item.kind}" is not one of ${KINDS.join(", ")}`);
  if (item.priority !== undefined && ![1, 2, 3].includes(item.priority)) throw new InputError(`item ${item.id}: priority must be 1, 2 or 3`);
  if (item.members !== undefined) {
    if (item.kind !== "settle") throw new InputError(`item ${item.id}: members belong to a settle item only`);
    if (!Array.isArray(item.members) || item.members.some((m) => typeof m !== "string")) throw new InputError(`item ${item.id}: members must be a list of thread ids`);
  }
  for (const key of ["threadId", "link"]) {
    if (item[key] !== undefined && item[key] !== null && typeof item[key] !== "string") throw new InputError(`item ${item.id}: ${key} must be a string or null`);
  }
  if (item.card !== undefined && item.card !== null) {
    if (typeof item.card !== "object" || Array.isArray(item.card)) throw new InputError(`item ${item.id}: card must be an object`);
    for (const [key, value] of Object.entries(item.card)) {
      if (!CARD_KEYS.includes(key)) throw new InputError(`item ${item.id}: card has unknown key "${key}"`);
      if (value !== null && typeof value !== "string") throw new InputError(`item ${item.id}: card.${key} must be a string or null`);
    }
  }
}

function normalCard(card) {
  return Object.fromEntries(CARD_KEYS.map((key) => [key, card?.[key] ?? null]));
}

// ---- commands -------------------------------------------------------------------------------

function open({ root, thread, title, now }) {
  if (!title) throw new InputError("open: --title is required");
  const found = findQueue(root, thread);
  if (found) return { path: found, created: false };
  const slug = slugify(title);
  if (!slug) throw new InputError(`open: title "${title}" makes an empty slug`);
  let dir = join(root, `${slug}-${stamp(now)}`);
  for (let n = 2; existsSync(dir); n += 1) dir = join(root, `${slug}-${stamp(now)}-${n}`);
  mkdirSync(dir, { recursive: true });
  const queue = {
    version: 1,
    chat: { threadId: thread, title, slug },
    createdAt: now,
    updatedAt: now,
    cadence: { ...DEFAULT_CADENCE },
    lastRefreshAt: null,
    lastHygieneAt: null,
    items: [],
  };
  writeQueue(dir, queue);
  logEvent(dir, { at: now, item: null, from: null, to: "open", note: `queue opened for ${title}` });
  return { path: dir, created: true };
}

function show(queue, { all, text }) {
  const items = ordered(queue.items).filter((item) => all || !CLOSED.has(item.status));
  if (!text) return { chat: queue.chat, items };
  if (items.length === 0) return "(empty)";
  return items.map((item, index) => `${index + 1}. ${item.status} ${item.kind} p${item.priority ?? 2} ${item.title} — ${item.reason}`).join("\n");
}

function put(dir, queue, raw, { reopen, now }) {
  validateItem(raw);
  const index = queue.items.findIndex((item) => item.id === raw.id);
  const old = index >= 0 ? queue.items[index] : null;
  if (raw.status !== undefined && raw.status !== (old?.status ?? "pending")) {
    throw new InputError(`item ${raw.id}: put does not change status ("${raw.status}"); use next or resolve`);
  }
  const fields = Object.fromEntries(Object.entries(raw).filter(([key]) => !MANAGED.includes(key)));
  if (!old) {
    const item = {
      id: raw.id,
      kind: raw.kind,
      threadId: null,
      title: raw.title,
      link: null,
      reason: raw.reason,
      priority: 2,
      status: "pending",
      ...(raw.kind === "settle" ? { members: [] } : {}),
      ...fields,
      card: normalCard(raw.card),
      addedAt: now,
      updatedAt: now,
    };
    queue.items.push(item);
    logEvent(dir, { at: now, item: item.id, from: null, to: "pending", note: `added: ${item.title}` });
    return { item, added: true };
  }
  if (CLOSED.has(old.status) && !reopen) {
    throw new InputError(`item ${raw.id} is ${old.status}; pass --reopen to put it back in the queue`);
  }
  const item = { ...old, ...fields, card: raw.card === undefined ? old.card : normalCard(raw.card), updatedAt: now };
  let note = `updated: ${Object.keys(fields).filter((key) => key !== "id" && JSON.stringify(fields[key]) !== JSON.stringify(old[key])).join(", ") || "no field changed"}`;
  if (CLOSED.has(old.status)) {
    item.status = "pending";
    delete item.doneAt;
    delete item.presentedAt;
    note = `reopened; ${note}`;
  }
  queue.items[index] = item;
  logEvent(dir, { at: now, item: item.id, from: old.status, to: item.status, note });
  return { item, added: false };
}

function next(dir, queue, { now }) {
  const item = head(queue.items);
  const changed = item?.status === "pending";
  if (changed) {
    item.status = "presented";
    item.presentedAt = now;
    item.updatedAt = now;
    logEvent(dir, { at: now, item: item.id, from: "pending", to: "presented", note: "head of the queue" });
  }
  const rest = ordered(queue.items).filter((other) => other !== item && forJp(other) && (other.status === "pending" || other.status === "waiting"));
  return { out: { item, left: rest.length, leftTitles: rest.map((other) => other.title) }, changed };
}

function resolveItem(dir, queue, { id, to, note, now }) {
  if (!id) throw new InputError("resolve: --item is required");
  if (!["done", "waiting", "dropped", "pending"].includes(to)) throw new InputError("resolve: --to must be done, waiting, dropped or pending");
  if (!note) throw new InputError("resolve: --note is required");
  const item = queue.items.find((other) => other.id === id);
  if (!item) throw new InputError(`resolve: no item "${id}"`);
  const from = item.status;
  if (!(MOVES[from] ?? []).includes(to)) {
    throw new InputError(`resolve: ${id} cannot move ${from} -> ${to} (allowed: ${(MOVES[from] ?? []).join(", ") || "none"})`);
  }
  item.status = to;
  item.updatedAt = now;
  if (to === "done") {
    item.doneAt = now;
    item.outcome = note;
  } else if (to === "dropped") {
    item.outcome = note;
  } else if (to === "pending") {
    delete item.presentedAt;
  }
  logEvent(dir, { at: now, item: id, from, to, note });
  return { item };
}

/**
 * Due once three quarters of the interval have passed. `ran` is stamped when a pass ends, and the timer
 * fires on the hour, so a full-interval test skipped every other tick (observed 2026-11-11: ran 00:37:07,
 * next tick 01:36:16, 59 minutes, not due). The timer still fires once per interval, so nothing runs twice.
 */
const DUE_SHARE = 0.75;
function isDue(last, everyMin, now) {
  if (!last) return true;
  return Date.parse(now) - Date.parse(last) >= everyMin * 60_000 * DUE_SHARE;
}

function due(queue, { now }) {
  return {
    refresh: isDue(queue.lastRefreshAt, queue.cadence.refreshEveryMin, now),
    hygiene: isDue(queue.lastHygieneAt, queue.cadence.hygieneEveryMin, now),
  };
}

function ran(dir, queue, { kind, now }) {
  const key = { refresh: "lastRefreshAt", hygiene: "lastHygieneAt" }[kind];
  if (!key) throw new InputError("ran: --kind must be refresh or hygiene");
  const from = queue[key];
  queue[key] = now;
  logEvent(dir, { at: now, item: null, from, to: now, note: `ran ${kind}` });
  return { [key]: now };
}

// ---- main -----------------------------------------------------------------------------------

export function main(argv, env = process.env) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: {
      thread: { type: "string" },
      title: { type: "string" },
      item: { type: "string" },
      "item-file": { type: "string" },
      to: { type: "string" },
      note: { type: "string" },
      kind: { type: "string" },
      all: { type: "boolean", default: false },
      text: { type: "boolean", default: false },
      reopen: { type: "boolean", default: false },
      now: { type: "string" },
      root: { type: "string" },
    },
  });
  const [command] = positionals;
  const commands = ["open", "show", "put", "next", "resolve", "due", "ran"];
  if (!commands.includes(command)) throw new InputError(`command must be one of ${commands.join(", ")}`);
  if (!values.thread) throw new InputError(`${command}: --thread is required`);
  const parsed = values.now === undefined ? Date.now() : Date.parse(values.now);
  if (Number.isNaN(parsed)) throw new InputError(`--now "${values.now}" is not an ISO time`);
  const now = new Date(parsed).toISOString().replace(/\.\d{3}Z$/, "Z"); // seconds, as the CEO writes them
  const root = resolve(values.root ?? defaultRoot(env));

  if (command === "open") return open({ root, thread: values.thread, title: values.title, now });

  const dir = findQueue(root, values.thread);
  if (!dir) throw new InputError(`no queue for thread ${values.thread} under ${root}; run open first`);
  const queue = readQueue(dir);
  if (command === "show") return show(queue, values);
  if (command === "due") return due(queue, { now });

  let out;
  if (command === "put") {
    let text = values.item;
    if (values["item-file"]) {
      try {
        text = readFileSync(values["item-file"], "utf8");
      } catch (error) {
        throw new InputError(`put: cannot read ${values["item-file"]}: ${error.message}`);
      }
    }
    if (text === undefined) throw new InputError("put: --item or --item-file is required");
    let raw;
    try {
      raw = JSON.parse(text);
    } catch (error) {
      throw new InputError(`put: item is not JSON: ${error.message}`);
    }
    out = put(dir, queue, raw, { reopen: values.reopen, now });
  } else if (command === "next") {
    const result = next(dir, queue, { now });
    out = result.out;
    if (!result.changed) return out; // the head was already presented, or the queue is empty: no write
  } else if (command === "resolve") {
    out = resolveItem(dir, queue, { id: values.item, to: values.to, note: values.note, now });
  } else {
    out = ran(dir, queue, { kind: values.kind, now });
  }
  queue.updatedAt = now;
  writeQueue(dir, queue);
  return out;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  try {
    const out = main(process.argv.slice(2));
    process.stdout.write(typeof out === "string" ? `${out}\n` : `${JSON.stringify(out, null, 2)}\n`);
  } catch (error) {
    if (error instanceof InputError || error?.code?.startsWith?.("ERR_PARSE_ARGS")) {
      process.stderr.write(`queue: ${error.message}\n`);
      process.exit(2);
    }
    throw error;
  }
}
