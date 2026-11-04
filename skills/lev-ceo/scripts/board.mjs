#!/usr/bin/env node
/**
 * The CEO board: write the cards JP answers on the phone, read his taps back, check the server.
 *
 * Usage (run in the project checkout, or pass --root):
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs write --input <items.json> [--project <name>] [--server <url>] [--root <dir>]
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs answers --since <ISO time with zone | line count> [--items <items.json>] [--root <dir>]
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs check [--root <dir>]
 *
 * write   Validates the items, builds <root>/.lev/now/entity-explorer.html from the new board in this process
 *         (the explorer build that plugins/now exports), then renames the page and <root>/.lev/now/ceo-board.json
 *         into place together, `updated` from the clock. A thread_link is T3's v2 link (t3-thread://v2/<environment
 *         id>/<thread id>); the angle brackets t3_thread_list wraps it in are dropped. A new project name warns on
 *         stderr. Any error: one line on stderr (one per validation error), exit 1, nothing written; when the page
 *         went in and the board rename failed, the line says "page written, board not".
 * answers Reads the answers file, keeps page_id "ceo-board", keeps the newest `at` per item over the whole file, and
 *         reports only winners past --since (a line count, or an ISO 8601 time with Z or ±hh:mm). Each is matched
 *         against the items (by choice id, else by label). Prints {answers_file, lines, rows, skipped}; `lines` is
 *         the --after value for the next waiter (plugins/now/scripts/answers-wait.mjs). Exit 0.
 * check   Prints whether anything listens on the board's server port (the `server` key, else 3456; with no host
 *         named, on loopback and every IPv4 address of this machine), the answers file path and its line count.
 *         Reads only; starts and stops nothing. Exit 0.
 *
 * The answers file is $XDG_STATE_HOME/lev/ceo-board/answers.jsonl, else ~/.local/state/... (the rule in
 * plugins/now/src/dev-server.ts answersFilePath). Decision: .lev/pm/decisions/20261104-ceo-board-return-channel.yaml.
 */

import { existsSync, mkdtempSync, readFileSync, realpathSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { connect } from "node:net";
import { homedir, networkInterfaces, tmpdir } from "node:os";
import { basename, isAbsolute, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const PAGE_ID = "ceo-board";
export const DEFAULT_PORT = 3456;
const EXPLORER_BUILD = "plugins/now/scripts/build-entity-explorer.ts";
const USAGE = "usage: board.mjs write --input <items.json> [--project <name>] [--server <url>] | answers --since <ISO time with zone | lines> [--items <items.json>] | check   (each takes [--root <dir>])";
/** The one link form the board stores: T3's own v2 link, as t3_thread_list returns it. */
export const THREAD_LINK_PREFIX = "t3-thread://v2/";
/**
 * T3 opens a v2 link only with both parts: t3-thread://v2/<environment id>/<thread id>. The thread id is kept as
 * written (it may hold percent escapes such as command%3Amcp); a space, a quote or an angle bracket ends a link.
 * The thread id holds no '/' and does not end in '.', ')' or ',': those come from a link pasted out of prose.
 */
export const THREAD_LINK = /^t3-thread:\/\/v2\/[^/\s"<>]+\/[^/\s"<>]*[^/\s"<>.),]$/;
/** An ISO 8601 time with its zone: Z or ±hh:mm. */
const ZONED_TIME = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$/;

// ---- paths

export function answersFilePath(env = process.env) {
  const stateHome = env.XDG_STATE_HOME;
  const base = stateHome && isAbsolute(stateHome) ? stateHome : join(homedir(), ".local", "state");
  return join(base, "lev", "ceo-board", "answers.jsonl");
}

const boardPath = (root) => join(root, ".lev", "now", "ceo-board.json");

// ---- write

const ISO = /^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$/;
const text = (v) => typeof v === "string" && v.trim() !== "";
/** t3_thread_list returns `<t3-thread://v2/...>`; the board keeps the link inside one pair of brackets. */
export const bareLink = (v) => (typeof v === "string" && /^<.*>$/.test(v.trim()) ? v.trim().slice(1, -1) : v);
const firstLine = (e) => String(e?.message ?? e).split("\n")[0];

/** Every error in the items, one string each; an empty list means the items are valid. */
export function validateItems(items) {
  if (!Array.isArray(items)) return ["items must be a list (or an object with an items list)"];
  const errors = [];
  const ids = new Set();
  items.forEach((item, i) => {
    const at = `item ${i + 1}${text(item?.id) ? ` (${item.id})` : ""}`;
    if (item === null || typeof item !== "object" || Array.isArray(item)) { errors.push(`${at}: must be an object`); return; }
    if (!text(item.id)) errors.push(`${at}: id is missing`);
    else if (ids.has(item.id)) errors.push(`${at}: id is used twice`);
    else ids.add(item.id);
    if (!text(item.title)) errors.push(`${at}: title is missing`);
    if (!text(item.what)) errors.push(`${at}: what is missing`);
    const choices = Array.isArray(item.choices) ? item.choices : [];
    if (!choices.length) errors.push(`${at}: needs at least one choice`);
    const choiceIds = new Set();
    choices.forEach((c, j) => {
      if (!text(c?.id) || !text(c?.label)) errors.push(`${at}: choice ${j + 1} needs an id and a label`);
      else if (choiceIds.has(c.id)) errors.push(`${at}: choice id ${c.id} is used twice`);
      else choiceIds.add(c.id);
    });
    if (item.recommended !== undefined && item.recommended !== null && !choiceIds.has(item.recommended)) {
      errors.push(`${at}: recommended '${item.recommended}' is not one of the choice ids`);
    }
    if (item.since !== undefined && item.since !== null && !(typeof item.since === "string" && ISO.test(item.since) && !Number.isNaN(Date.parse(item.since)))) {
      errors.push(`${at}: since must be an ISO date, e.g. 2026-11-04T04:00:00Z`);
    }
    const link = bareLink(item.thread_link);
    if (link !== undefined && link !== null && !(typeof link === "string" && THREAD_LINK.test(link))) {
      errors.push(`${at}: thread_link must be the thread's v2 link from t3_thread_list (${THREAD_LINK_PREFIX}<environment id>/<thread id>), or be absent`);
    }
  });
  return errors;
}

/** The board file body: the old file's `server` key carries over unless a new one is given. */
export function boardDocument({ items, project, server, now }) {
  const keep = (it) => ({
    id: it.id, title: it.title, ...(it.thread_link ? { thread_link: bareLink(it.thread_link) } : {}), what: it.what,
    choices: it.choices.map((c) => ({ id: c.id, label: c.label })),
    ...(it.recommended ? { recommended: it.recommended } : {}), ...(it.since ? { since: it.since } : {}),
  });
  return { updated: now, project, ...(server ? { server } : {}), items: items.map(keep) };
}

/**
 * Build the explorer page in this process from the board file given, and return its HTML without writing it.
 * null when the --root folder has no explorer build; throws one-line errors otherwise.
 */
export async function buildExplorer(root, boardFile) {
  const build = join(root, EXPLORER_BUILD);
  if (!existsSync(build)) return null;
  const require = createRequire(join(root, "plugins", "now", "package.json"));
  let api;
  try { api = require.resolve("tsx/esm/api"); } catch { throw new Error("tsx not found under plugins/now: run pnpm install"); }
  const { tsImport } = await import(pathToFileURL(api).href);
  const mod = await tsImport(pathToFileURL(build).href, import.meta.url);
  const { root: projectRoot, name } = mod.resolveProject(undefined, root);
  const data = mod.collectEntityExplorerData({ projectRoot, projectName: name, boardPath: boardFile });
  return { html: mod.buildEntityExplorerHtml(data), board_cards: data.waits.board?.items.length ?? 0, board_note: data.waits.board_note };
}

async function write(args) {
  const root = args.root;
  if (!args.input) return fail("write needs --input <items.json>", { usage: true });
  let input;
  try { input = JSON.parse(readFileSync(resolve(args.input), "utf8")); } catch (e) { return fail(`cannot read --input: ${firstLine(e)}`); }
  const items = Array.isArray(input) ? input : input?.items;
  const errors = validateItems(items);
  if (errors.length) { for (const e of errors) process.stderr.write(`board write: ${e}\n`); process.exitCode = 1; return; }
  const file = boardPath(root);
  if (!existsSync(join(root, ".lev", "now"))) return fail(`no .lev/now folder under ${root}`);
  let old = {};
  try { if (existsSync(file)) old = JSON.parse(readFileSync(file, "utf8")); } catch { old = {}; }
  const doc = boardDocument({
    items, now: new Date().toISOString(),
    project: args.project ?? (typeof input?.project === "string" ? input.project : undefined) ?? (text(old.project) ? old.project : basename(root)),
    server: args.server ?? input?.server ?? old.server,
  });
  const json = `${JSON.stringify(doc, null, 2)}\n`;
  // The page is built from a draft board first; the page and the board then rename into place together,
  // so a failed build leaves the old board beside the old page.
  const scratch = mkdtempSync(join(tmpdir(), "ceo-board-"));
  const pageFile = join(root, ".lev", "now", "entity-explorer.html");
  const pageTmp = `${pageFile}.${process.pid}.tmp`;
  const boardTmp = `${file}.${process.pid}.tmp`;
  let page;
  let pageMoved = false;
  try {
    const draft = join(scratch, "ceo-board.json");
    writeFileSync(draft, json, "utf8");
    const built = await buildExplorer(root, draft);
    if (built) writeFileSync(pageTmp, built.html, "utf8");
    writeFileSync(boardTmp, json, "utf8");
    if (built) { renameSync(pageTmp, pageFile); pageMoved = true; }
    renameSync(boardTmp, file);
    page = built
      ? { rebuilt: true, html: pageFile, bytes: built.html.length, board_cards: built.board_cards, board_note: built.board_note }
      : { rebuilt: false, why: `no ${EXPLORER_BUILD} under ${root}` };
  } catch (e) {
    // The page went in before the board failed: say so, so the CEO node knows the page shows cards the board lacks.
    return fail(`write: ${!pageMoved ? "nothing written" : "page written, board not"}: ${firstLine(e)}`);
  } finally {
    for (const p of [pageTmp, boardTmp, scratch]) rmSync(p, { recursive: true, force: true });
  }
  if (text(old.project) && old.project !== doc.project) process.stderr.write(`board write: board owner changes from ${old.project} to ${doc.project}\n`);
  print({ board: file, items: doc.items.length, updated: doc.updated, project: doc.project, page });
}

// ---- answers

/** Complete lines only: a line still being written waits for the next read. */
export function completeLines(file) {
  if (!existsSync(file)) return [];
  const body = readFileSync(file, "utf8");
  const end = body.lastIndexOf("\n");
  return end === -1 ? [] : body.slice(0, end).split("\n");
}

const norm = (s) => (typeof s === "string" ? s.trim().toLowerCase() : "");

/**
 * The newest answer per board item over every line, reported only when that winner is past `since` (its line
 * index at or after a line count, or its `at` after a time), each matched against the board items. Dedupe runs over
 * the whole file because `at` is the phone's clock: a newer row may sit before a line cut and an older one after it.
 * status: fresh (matches a choice id or label, or a note on a known item), stale (names no current choice),
 * unknown_item (the item is not on the board), cleared (choice and note both null).
 */
export function readAnswers({ lines, since, items }) {
  const afterLine = typeof since === "number" ? since : 0;
  const afterTime = typeof since === "string" ? Date.parse(since) : Number.NaN;
  const byItem = new Map((items ?? []).map((it) => [it.id, it]));
  const newest = new Map();
  let skipped = 0;
  lines.forEach((line, index) => {
    if (!line.trim()) return;
    let row;
    try { row = JSON.parse(line); } catch { if (index >= afterLine) skipped++; return; }
    if (row?.page_id !== PAGE_ID || !text(row.item_id)) return;
    const at = Date.parse(row.at);
    const held = newest.get(row.item_id);
    if (!held || !(Date.parse(held.row.at) > at)) newest.set(row.item_id, { row, index });
  });
  const past = ({ row, index }) => index >= afterLine && (Number.isNaN(afterTime) || Date.parse(row.at) > afterTime);
  const rows = [...newest.values()].filter(past).sort((a, b) => a.index - b.index).map(({ row }) => {
    const base = { item_id: row.item_id, choice: row.choice ?? null, label: row.label ?? null, note: row.note ?? null, at: row.at ?? null };
    const item = byItem.get(row.item_id);
    if (!item) return { ...base, status: "unknown_item" };
    if (base.choice === null && base.note === null) return { ...base, status: "cleared" };
    if (base.choice === null) return { ...base, status: "fresh" };
    const choices = item.choices ?? [];
    const hit = choices.find((c) => c.id === String(base.choice)) ?? choices.find((c) => norm(c.label) === norm(base.label));
    return hit ? { ...base, choice: hit.id, label: hit.label, status: "fresh" } : { ...base, status: "stale" };
  });
  return { rows, skipped };
}

function answers(args) {
  if (args.since === undefined) return fail("answers needs --since <ISO time with zone | line count>", { usage: true });
  const since = /^\d+$/.test(args.since) ? Number(args.since) : args.since;
  if (typeof since === "string" && !(ZONED_TIME.test(since) && !Number.isNaN(Date.parse(since)))) {
    return fail(`answers: --since '${since}' must be a line count or an ISO 8601 time with a zone, e.g. 2026-11-04T04:15:00Z`);
  }
  const itemsFile = args.items ? resolve(args.items) : boardPath(args.root);
  let items = [];
  try { const doc = JSON.parse(readFileSync(itemsFile, "utf8")); items = Array.isArray(doc) ? doc : doc.items ?? []; }
  catch { process.stderr.write(`board answers: no items read from ${itemsFile}; every row reads unknown_item\n`); }
  const file = answersFilePath();
  const lines = completeLines(file);
  const { rows, skipped } = readAnswers({ lines, since, items });
  print({ answers_file: file, lines: lines.length, since, items_file: itemsFile, rows, skipped });
}

// ---- check

/**
 * The board's server host and port: the `server` key (a URL, a port, or {host, port}), else port 3456.
 * host null means none was named: check then tries loopback and every IPv4 address of this machine,
 * because the server may bind the tailnet address only (observed 2026-11-04: 100.69.101.5:3456, none on 127.0.0.1).
 */
export function serverTarget(board) {
  const s = board?.server;
  if (typeof s === "number") return { host: null, port: s };
  if (typeof s === "string") { try { const u = new URL(s); return { host: u.hostname || null, port: Number(u.port) || DEFAULT_PORT }; } catch { /* fall through */ } }
  if (s && typeof s === "object") return { host: text(s.host) ? s.host : text(s.bind) ? s.bind : null, port: Number(s.port) || DEFAULT_PORT };
  return { host: null, port: DEFAULT_PORT };
}

function localHosts() {
  const own = Object.values(networkInterfaces()).flat().filter((a) => a && a.family === "IPv4" && !a.internal).map((a) => a.address);
  return ["127.0.0.1", ...own];
}

export function isListening({ host, port }, timeoutMs = 800) {
  return new Promise((done) => {
    const socket = connect({ host, port });
    const finish = (ok) => { socket.destroy(); done(ok); };
    socket.setTimeout(timeoutMs, () => finish(false));
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
  });
}

async function check(args) {
  let board = null;
  try { board = JSON.parse(readFileSync(boardPath(args.root), "utf8")); } catch { board = null; }
  const { host, port } = serverTarget(board);
  const hosts = host ? [host] : localHosts();
  const answered = (await Promise.all(hosts.map(async (h) => ((await isListening({ host: h, port })) ? h : null)))).filter(Boolean);
  const file = answersFilePath();
  print({
    server: { port, tried: hosts, listening: answered.length > 0, listening_on: answered.map((h) => `${h}:${port}`), from: board?.server ? "board server key" : "default" },
    answers_file: file, answers_lines: completeLines(file).length,
    board: board ? { path: boardPath(args.root), items: Array.isArray(board.items) ? board.items.length : 0, updated: board.updated ?? null } : null,
  });
}

// ---- command line

function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }

/** One line on stderr, exit 1; a usage error adds the usage line. */
function fail(message, { usage = false } = {}) {
  process.stderr.write(`board: ${message}\n${usage ? `${USAGE}\n` : ""}`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const args = { command, root: process.cwd() };
  const flags = { "--input": "input", "--project": "project", "--server": "server", "--since": "since", "--items": "items", "--root": "root" };
  for (let i = 0; i < rest.length; i += 2) {
    const key = flags[rest[i]];
    const value = rest[i + 1];
    if (!key || value === undefined || value.startsWith("--")) return { command, error: `unknown or incomplete argument '${rest[i]}'` };
    args[key] = value;
  }
  args.root = resolve(args.root);
  return args;
}

async function main(argv) {
  const args = parseArgs(argv);
  if (args.error) return fail(args.error, { usage: true });
  if (args.command === "write") return write(args);
  if (args.command === "answers") return answers(args);
  if (args.command === "check") return check(args);
  if (args.command === "--help" || args.command === "-h") return void process.stdout.write(`${USAGE}\n`);
  return fail(`unknown command '${args.command ?? ""}'`, { usage: true });
}

// realpath: ~/.claude/skills is a link to ~/.agents/skills, and Node names the main module by its real path.
if (process.argv[1] && existsSync(process.argv[1]) && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  await main(process.argv.slice(2)).catch((e) => fail(firstLine(e)));
}
