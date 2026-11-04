#!/usr/bin/env node
/**
 * The CEO board: write the cards JP answers on the phone, read his taps back, check the server.
 *
 * Usage (run in the project checkout, or pass --root):
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs write --input <items.json> [--project <name>] [--server <url>] [--root <dir>]
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs answers --since <ISO time | line count> [--items <items.json>] [--root <dir>]
 *   node ~/.agents/skills/lev-ceo/scripts/board.mjs check [--root <dir>]
 *
 * write   Validates the items, writes <root>/.lev/now/ceo-board.json with `updated` from the clock, then rebuilds
 *         <root>/.lev/now/entity-explorer.html in this process through the explorer build that plugins/now exports.
 *         Any validation error: one line per error on stderr, exit 1, nothing written.
 * answers Reads the answers file, keeps page_id "ceo-board", keeps the newest `at` per item, and matches each choice
 *         against the items (by choice id, else by label). Prints {answers_file, lines, rows, skipped}; `lines` is
 *         the --after value for the next waiter (plugins/now/scripts/answers-wait.mjs). Exit 0.
 * check   Prints whether anything listens on the board's server port (the `server` key, else 3456; with no host
 *         named, on loopback and every IPv4 address of this machine), the answers file path and its line count.
 *         Reads only; starts and stops nothing. Exit 0.
 *
 * The answers file is $XDG_STATE_HOME/lev/ceo-board/answers.jsonl, else ~/.local/state/... (the rule in
 * plugins/now/src/dev-server.ts answersFilePath). Decision: .lev/pm/decisions/20261104-ceo-board-return-channel.yaml.
 */

import { existsSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { connect } from "node:net";
import { homedir, networkInterfaces } from "node:os";
import { basename, isAbsolute, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const PAGE_ID = "ceo-board";
export const DEFAULT_PORT = 3456;
const EXPLORER_BUILD = "plugins/now/scripts/build-entity-explorer.ts";
const USAGE = "usage: board.mjs write --input <items.json> [--project <name>] [--server <url>] | answers --since <ISO | lines> [--items <items.json>] | check   (each takes [--root <dir>])";

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
    if (item.thread_link !== undefined && item.thread_link !== null && !(typeof item.thread_link === "string" && /^(https?:|t3-thread:)/.test(item.thread_link))) {
      errors.push(`${at}: thread_link must start with t3-thread: or https:, or be absent (the explorer drops any other link)`);
    }
  });
  return errors;
}

/** The board file body: the old file's `server` key carries over unless a new one is given. */
export function boardDocument({ items, project, server, now }) {
  const keep = (it) => ({
    id: it.id, title: it.title, ...(it.thread_link ? { thread_link: it.thread_link } : {}), what: it.what,
    choices: it.choices.map((c) => ({ id: c.id, label: c.label })),
    ...(it.recommended ? { recommended: it.recommended } : {}), ...(it.since ? { since: it.since } : {}),
  });
  return { updated: now, project, ...(server ? { server } : {}), items: items.map(keep) };
}

/** Rebuild the explorer page in this process; returns a summary, or why it was not rebuilt. */
export async function rebuildExplorer(root) {
  const build = join(root, EXPLORER_BUILD);
  if (!existsSync(build)) return { rebuilt: false, why: `no ${EXPLORER_BUILD} under ${root}` };
  const require = createRequire(join(root, "plugins", "now", "package.json"));
  const { tsImport } = await import(pathToFileURL(require.resolve("tsx/esm/api")).href);
  const mod = await tsImport(pathToFileURL(build).href, import.meta.url);
  const { root: projectRoot, name } = mod.resolveProject(undefined, root);
  const data = mod.collectEntityExplorerData({ projectRoot, projectName: name });
  const out = join(root, ".lev", "now", "entity-explorer.html");
  const html = mod.buildEntityExplorerHtml(data);
  writeFileSync(out, html, "utf8");
  return { rebuilt: true, html: out, bytes: html.length, board_cards: data.waits.board?.items.length ?? 0, board_note: data.waits.board_note };
}

async function write(args) {
  const root = args.root;
  if (!args.input) return fail("write needs --input <items.json>");
  let input;
  try { input = JSON.parse(readFileSync(resolve(args.input), "utf8")); } catch (e) { return fail(`cannot read --input: ${e.message}`, 1); }
  const items = Array.isArray(input) ? input : input?.items;
  const errors = validateItems(items);
  if (errors.length) { for (const e of errors) process.stderr.write(`board write: ${e}\n`); process.exitCode = 1; return; }
  const file = boardPath(root);
  if (!existsSync(join(root, ".lev", "now"))) return fail(`no .lev/now folder under ${root}`, 1);
  let old = {};
  try { if (existsSync(file)) old = JSON.parse(readFileSync(file, "utf8")); } catch { old = {}; }
  const doc = boardDocument({
    items, now: new Date().toISOString(),
    project: args.project ?? (typeof input?.project === "string" ? input.project : undefined) ?? (text(old.project) ? old.project : basename(root)),
    server: args.server ?? input?.server ?? old.server,
  });
  writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  const page = await rebuildExplorer(root);
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
 * The newest answer per board item after `since`, each matched against the board items.
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
    if (index < afterLine || !line.trim()) return;
    let row;
    try { row = JSON.parse(line); } catch { skipped++; return; }
    if (row?.page_id !== PAGE_ID || !text(row.item_id)) return;
    const at = Date.parse(row.at);
    if (!Number.isNaN(afterTime) && !(at > afterTime)) return;
    const held = newest.get(row.item_id);
    if (!held || !(Date.parse(held.row.at) > at)) newest.set(row.item_id, { row, index });
  });
  const rows = [...newest.values()].sort((a, b) => a.index - b.index).map(({ row }) => {
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
  if (args.since === undefined) return fail("answers needs --since <ISO time | line count>");
  const since = /^\d+$/.test(args.since) ? Number(args.since) : args.since;
  if (typeof since === "string" && Number.isNaN(Date.parse(since))) return fail("--since must be a line count or an ISO time");
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

function fail(message, code = 1) {
  process.stderr.write(`board: ${message}\n${USAGE}\n`);
  process.exitCode = code;
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
  if (args.error) return fail(args.error);
  if (args.command === "write") return write(args);
  if (args.command === "answers") return answers(args);
  if (args.command === "check") return check(args);
  if (args.command === "--help" || args.command === "-h") return void process.stdout.write(`${USAGE}\n`);
  return fail(`unknown command '${args.command ?? ""}'`);
}

// realpath: ~/.claude/skills is a link to ~/.agents/skills, and Node names the main module by its real path.
if (process.argv[1] && existsSync(process.argv[1]) && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) await main(process.argv.slice(2));
