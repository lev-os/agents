#!/usr/bin/env node
/**
 * The question cards: what JP sees for each item of a chat queue, and the message that takes his answer
 * back to the chat that asked. Stdlib only (Node 22+). It reads no chat and sends no message: a reader
 * (a subagent) reads the chats, and the chat that runs this program sends the relay.
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/cards.mjs <command> --thread <this chat's id> [options]
 *   brief --out <cards file>   -> lists the open items that a reader can write a card for (a cursor, no card
 *                                 for it, no report that holds it) in <queue>/cards-to-read.jsonl and prints
 *                                 the brief for one reader (references/card-brief.txt). Exit 2 when no item
 *                                 needs a card.
 *   merge --cards <cards file> -> checks every line, then stores each card on its item (`asks`, `context`,
 *                                 `asks_cursor`). Prints {merged, stale, moved, not_open, answered, no_question}.
 *                                 A card for an older reply (stale) or for no open item (not_open) is not
 *                                 stored. A line for a chat that has more items now than at the scan (moved),
 *                                 that a person answered, or whose reply holds no question (`asks: []`) is a
 *                                 report: it holds the card of that reply (`card_hold`), also a card that was
 *                                 stored before and a card that comes later. The hold ends when the item gets
 *                                 a new cursor (the next scan).
 *   batch [--size 5]           -> the next questions for JP, all of one project, numbered from 1: whole items
 *                                 until --size questions are reached. An item is never cut, so one item that
 *                                 holds more than --size questions makes a batch alone. Writes
 *                                 <queue>/batches/batch-<n>.html (the page to show) and batch-<n>.json
 *                                 (question number -> item, choices), and marks each item as shown for its
 *                                 reply. Prints {batch, group, page, map, questions, left, no_card, held,
 *                                 no_cursor}: no_card counts the items for `brief`; held and no_cursor name
 *                                 the items that get no card, for you to handle by hand.
 *   batch --again <n>          -> writes the page and the map of batch n again, from its items that are still
 *                                 open (an item was closed, or its card was merged again, after the batch).
 *                                 It marks no item. The questions get new numbers: show the page again.
 *   relay --item <id> --words "<JP's words>" [--picks "2a 3b"] [--note "<text>"] [--sent] [--keep-open]
 *                              -> prints the message for the chat that asked. JP's words are unchanged,
 *                                 between two marks. Every text of a reader comes after them, under the mark
 *                                 "Not JP's words", each as one line that starts with a question number or a
 *                                 choice letter. A pick is a question number of the page that showed the item
 *                                 (the map of its batch) and a choice letter; the message holds the picks as
 *                                 numbers and letters only, and the questions with the numbers of that page.
 *                                 A pick for an item that no page showed is refused. With no --sent it writes
 *                                 nothing. After the send, run it again with --sent: it records the words on
 *                                 the item and closes it (--keep-open: a question of the item is still open).
 * Every command takes --queue-root <dir> (the folder that holds the queue folders) and --now <ISO>.
 *
 * A card belongs to one reply: it holds the cursor of the item it was written for. When the chat moves,
 * the item gets a new cursor (scripts/sweep.mjs queue), the card is not shown, and `brief` lists the chat again.
 * An item that the sweep made (`source: "sweep"`) with no question (JP's message has no reply) needs no
 * reader: the program writes its card. An item with no cursor gets no card. Two open items of one chat are
 * refused by `brief` and `merge`: a card belongs to a chat. Each text of a card is one line of at most 400
 * characters, and an ask names at most 5 experts.
 *
 * Limits: scripts/queue.mjs has no lock, so run one command that writes at a time. A command that is
 * stopped between two writes is run again: `merge` and `relay --sent` give the same result, and `batch`
 * makes a new page for the same questions.
 * JSON on stdout (relay and brief: text). Exit 0 ok, exit 2 bad input (the reason on stderr).
 */
import { mkdirSync, readdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { InputError as QueueInputError, defaultRoot, findQueue, main as queueMain, ordered } from "./queue.mjs";

export class InputError extends Error {}

const HERE = dirname(fileURLToPath(import.meta.url));
const OPEN = new Set(["pending", "presented", "waiting"]);
const KEYS = ["a", "b", "c"];
const isText = (value) => typeof value === "string";
const isRecord = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

/** The card of an item whose chat holds a message of JP with no reply: the sweep found no question in it. */
const noReply = (item) => ({
  emoji: "⏸️",
  ask: "Your last message in this chat has no reply. Shall this chat tell it to continue?",
  why: `${item.reason}.`,
  choices: [
    { label: "Yes, tell it to continue", gain: "The work goes on with no visit from you", cost: null },
    { label: "No, I go to the chat myself", gain: null, cost: "It waits until you do" },
  ],
  pick: null, because: null, experts: [], if_no_answer: "It stays as it is.", yours: false,
});

/**
 * A reader's report that holds the card of a reply: the chat has more items than at the scan (`moved`), a
 * person answered after the reply (`answered`), or the reply holds no question (`no_question`). It stands
 * for that reply: no card is shown or stored until the item has a new cursor (the next scan).
 */
const HOLDS = ["moved", "answered", "no_question"];
const held = (item) => isRecord(item.card_hold) && HOLDS.includes(item.card_hold.why) && item.card_hold.cursor === (item.cursor ?? null);

/** The asks to show for an item now, or null: a reader must write them first, or a report holds the card. */
function asksOf(item) {
  if (held(item)) return null;
  if (isText(item.cursor) && item.asks_cursor === item.cursor && Array.isArray(item.asks) && item.asks.length > 0) return item.asks;
  if (Array.isArray(item.questions) && item.questions.length === 0 && item.source === "sweep") return [noReply(item)];
  return null;
}
const forJp = (item) => OPEN.has(item.status) && item.kind !== "watch";
/** An item that a reader can write a card for: it has a cursor, no card for it, and no report holds it. */
const needsReader = (item) => isText(item.cursor) && !held(item) && asksOf(item) === null;
const chatOf = (item) => item.threadId ?? item.id;

/** A card belongs to a chat: two open items of one chat cannot both get it. */
function checkOneItemEachChat(open) {
  const first = new Map();
  for (const item of open) {
    const other = first.get(chatOf(item));
    if (other) throw new InputError(`two open items for the chat ${chatOf(item)} (${other.id}, ${item.id}): close one of them with scripts/queue.mjs resolve`);
    first.set(chatOf(item), item);
  }
}
/** The item count at the end of a cursor (`<run id>#<count>`), or NaN. */
const countOf = (cursor) => (cursor.includes("#") ? Number(cursor.slice(cursor.lastIndexOf("#") + 1)) : NaN);

// A text of a card is one line. The relay prints the reader's texts beside JP's words, and a line break in
// one of them would make a line of its own there.
// Each character that a screen can show as a line break: line feed, vertical tab, form feed, carriage
// return, next line (U+0085), and the two Unicode separators (U+2028, U+2029).
const BREAKS = String.fromCharCode(0x0a, 0x0b, 0x0c, 0x0d, 0x85, 0x2028, 0x2029);
const LINE_BREAK = new RegExp(`[${BREAKS}]`);
const MAX_TEXT = 400;      // characters in one text of a card: the brief asks the reader for 160 at most
const MAX_EXPERTS = 5;
const isLine = (value) => isText(value) && value.length <= MAX_TEXT && !LINE_BREAK.test(value);
const lineOrNull = (value) => value === null || value === undefined || isLine(value);
const SPACES = new RegExp(`[\\s${BREAKS}]+`, "g");
const oneLine = (value) => String(value ?? "").replace(SPACES, " ").trim();

function checkAsk(ask, where) {
  const bad = (what) => new InputError(`${where}: ${what}`);
  if (!isRecord(ask)) throw bad("an ask is not an object");
  if (!isLine(ask.ask) || ask.ask.trim() === "") throw bad("ask must be a text of one line (400 characters at most)");
  if (!isLine(ask.emoji)) throw bad("emoji must be a text of one line (400 characters at most)");
  for (const key of ["why", "because", "if_no_answer"]) if (!lineOrNull(ask[key])) throw bad(`${key} must be a text of one line (400 characters at most), or null`);
  if (!Array.isArray(ask.choices) || ask.choices.length > KEYS.length) throw bad(`choices must be a list of at most ${KEYS.length}`);
  for (const choice of ask.choices) {
    if (!isRecord(choice) || !isLine(choice.label) || choice.label.trim() === "") throw bad("a choice needs a label that is a text of one line (400 characters at most)");
    if (!lineOrNull(choice.gain) || !lineOrNull(choice.cost)) throw bad("gain and cost of a choice must be a text of one line (400 characters at most), or null");
  }
  if (ask.pick !== null && ask.pick !== undefined && !(Number.isInteger(ask.pick) && ask.pick >= 0 && ask.pick < ask.choices.length)) {
    throw bad("pick must be null or the position of one of the choices");
  }
  if (!Array.isArray(ask.experts) || ask.experts.length > MAX_EXPERTS || !ask.experts.every(isLine)) throw bad(`experts must be a list of at most ${MAX_EXPERTS} texts of one line (400 characters at most)`);
  if (typeof ask.yours !== "boolean") throw bad("yours must be true or false");
}

function checkLine(card, where) {
  const bad = (what) => new InputError(`${where}: ${what}`);
  if (!isRecord(card)) throw bad("not a card (a JSON object)");
  if (!isText(card.threadId) || card.threadId === "") throw bad("threadId must be a text");
  if (!isText(card.cursor)) throw bad("cursor must be a text");
  if (card.item_count_now !== null && card.item_count_now !== undefined && !Number.isFinite(card.item_count_now)) throw bad("item_count_now must be a number or null");
  if (typeof card.answered !== "boolean") throw bad("answered must be true or false");
  if (!isLine(card.context)) throw bad("context must be a text of one line (400 characters at most)");
  if (!Array.isArray(card.asks)) throw bad("asks must be a list");
  card.asks.forEach((ask, index) => checkAsk(ask, `${where}, ask ${index + 1}`));
}

function readCards(file) {
  if (!file) throw new InputError("merge: --cards <file> is required");
  let text;
  try {
    text = readFileSync(file, "utf8");
  } catch (error) {
    throw new InputError(`cannot read ${file}: ${error.message}`);
  }
  const seen = new Set();
  return text.split("\n").filter((row) => row.trim() !== "").map((row, index) => {
    const where = `${file} line ${index + 1}`;
    let card;
    try {
      card = JSON.parse(row);
    } catch (error) {
      throw new InputError(`${where}: not JSON: ${error.message}`);
    }
    checkLine(card, where);
    if (seen.has(card.threadId)) throw new InputError(`${where}: a second card for the chat ${card.threadId}`);
    seen.add(card.threadId);
    return card;
  });
}

const esc = (value) => String(value ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const STYLE = `
  .wrap { font-family: var(--font-sans); color: var(--foreground); display: grid; gap: 14px; }
  .ghead { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
  .ghead .t { font-size: 17px; font-weight: 700; letter-spacing: -.01em; }
  .ghead .s { font-size: 12.5px; color: var(--muted-foreground); }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); padding: 14px; display: grid; gap: 9px; align-content: start; }
  .q { display: grid; grid-template-columns: 34px 1fr; gap: 10px; align-items: center; }
  .q .e { width: 34px; height: 34px; border-radius: 10px; background: var(--secondary); display: grid; place-items: center; font-size: 18px; }
  .q .n { font-size: 11px; font-weight: 700; letter-spacing: .08em; color: var(--muted-foreground); }
  .q .h { font-size: 15px; font-weight: 650; line-height: 1.25; }
  .from { font-size: 11.5px; color: var(--muted-foreground); }
  .opts { display: grid; gap: 6px; }
  .opt { display: grid; grid-template-columns: 22px 1fr auto; gap: 8px; align-items: center; border: 1px solid var(--border); border-radius: 10px; padding: 8px 10px; font-size: 13.5px; line-height: 1.3; }
  .opt .k { font-family: var(--font-mono); font-weight: 700; font-size: 12px; color: var(--muted-foreground); }
  .opt .gc { display: block; font-size: 11.5px; color: var(--muted-foreground); margin-top: 2px; }
  .opt.pick { border-color: var(--success); background: color-mix(in srgb, var(--success) 13%, transparent); }
  .opt.pick .k { color: var(--success); }
  .opt .tag, .act { font-size: 10.5px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--success); white-space: nowrap; }
  .act { color: var(--warning, var(--muted-foreground)); }
  .why { font-size: 12.5px; color: var(--muted-foreground); line-height: 1.4; }
  .why b { color: var(--foreground); font-weight: 600; }
  .src { font-size: 11.5px; color: var(--muted-foreground); opacity: .85; }
  .reply { border: 1px dashed var(--border); border-radius: calc(var(--radius) + 4px); padding: 12px 14px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; font-size: 13.5px; }
  .reply .say { font-family: var(--font-mono); font-size: 12.5px; background: var(--secondary); border-radius: 8px; padding: 4px 9px; }
  .reply .or { color: var(--muted-foreground); }
  @media (max-width: 560px) { .grid { grid-template-columns: 1fr; } }`;

function cardHtml(q) {
  const options = q.choices.map((choice) => {
    const parts = [choice.gain ? `you get: ${esc(choice.gain)}` : "", choice.cost ? `it costs: ${esc(choice.cost)}` : ""].filter(Boolean).join(" · ");
    return `<div class="opt${choice.pick ? " pick" : ""}"><span class="k">${choice.key}</span><span>${esc(choice.label)}${parts ? `<span class="gc">${parts}</span>` : ""}</span><span class="tag">${choice.pick ? "its pick" : ""}</span></div>`;
  }).join("\n          ");
  const picked = q.choices.find((choice) => choice.pick);
  return `      <div class="card">
        <div class="q"><div class="e">${esc(q.emoji)}</div><div><div class="n">QUESTION ${q.n}</div><div class="h">${esc(q.ask)}</div></div></div>
        <div class="from">💬 ${esc(q.title)}${q.context ? ` · ${esc(q.context)}` : ""}</div>${q.yours ? `\n        <div class="act">✋ only you can do this</div>` : ""}${options ? `\n        <div class="opts">\n          ${options}\n        </div>` : ""}${q.why ? `\n        <div class="why"><b>Why it matters:</b> ${esc(q.why)}</div>` : ""}${picked && q.because ? `\n        <div class="why"><b>Why ${picked.key}:</b> ${esc(q.because)}</div>` : ""}${q.experts.length ? `\n        <div class="src">🎓 ${q.experts.slice(0, 3).map(esc).join(" · ")}</div>` : ""}${q.if_no_answer ? `\n        <div class="src">⏳ No answer: ${esc(q.if_no_answer)}</div>` : ""}
      </div>`;
}

function pageHtml(batch) {
  const chats = new Set(batch.questions.map((q) => q.item)).size;
  const picks = batch.questions.filter((q) => q.choices.some((choice) => choice.pick));
  const sample = batch.questions.filter((q) => q.choices.length > 1).slice(0, 2).map((q) => `${q.n}b`).join(" ") || "1b";
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>${STYLE}
</style>
</head>
<body>
<div class="wrap">
  <div class="ghead"><span class="t">📂 ${esc(batch.group)}</span><span class="s">batch ${batch.batch} · ${batch.questions.length} question${batch.questions.length === 1 ? "" : "s"} from ${chats} chat${chats === 1 ? "" : "s"} · ${batch.left} more wait${batch.left === 1 ? "s" : ""}</span></div>
  <div class="grid">
${batch.questions.map(cardHtml).join("\n")}
  </div>
  <div class="reply">
    <span>👉 Say</span>${picks.length ? `<span class="say">all yes</span><span class="or">for every green one, or name</span>` : `<span class="or">a number and a letter for each:</span>`}<span class="say">${sample}</span><span class="or">Your words go to each chat unchanged.</span>
  </div>
</div>
</body>
</html>
`;
}

/**
 * The numbers that JP saw for the asks of an item: those of the page of the batch that showed its newest
 * reply (the map file), or null when no page showed it. `batch --again` writes the map again, so the
 * numbers are those of the newest page.
 */
function shownNumbers(dir, item, asks) {
  if (!(isRecord(item.shown) && item.shown.cursor === (item.cursor ?? null))) return null;
  const file = join(dir, "batches", `batch-${item.shown.batch}.json`);
  let mine;
  try {
    mine = JSON.parse(readFileSync(file, "utf8")).questions.filter((q) => q.item === item.id);
  } catch (error) {
    throw new InputError(`relay: cannot read the map of batch ${item.shown.batch} (${file}): ${error.message}`);
  }
  const numbers = asks.map((_, index) => mine.find((q) => q.index === index)?.n);
  if (mine.length !== asks.length || !numbers.every(Number.isInteger)) {
    throw new InputError(`relay: the page of batch ${item.shown.batch} does not hold the questions of the item "${item.id}" as they are now: run batch --again ${item.shown.batch}, show the page, and ask again`);
  }
  return numbers;
}

/**
 * The message for the chat that asked. Its form keeps JP's words apart from every other text: his words
 * come first, under their own mark; the picks line holds numbers and letters only; each text of the reader
 * comes after, as one line that starts with a question number or a choice letter.
 */
function relayText(queue, asks, numbers, batch, { words, picks, note }) {
  const tokens = (picks || "").split(/[\s,]+/).filter(Boolean);
  if (tokens.length > 0 && numbers === null) throw new InputError("relay: this item was not shown on a page, so JP saw no question number: run batch and show the page first, or leave --picks out");
  const shown = numbers ?? asks.map((_, index) => index + 1);
  for (const token of tokens) {
    const match = /^(\d+)([a-c])$/.exec(token);
    if (!match) throw new InputError(`relay: the pick "${token}" is not a question number and a choice letter (1a)`);
    const at = shown.indexOf(Number(match[1]));
    if (at < 0) throw new InputError(`relay: the pick "${token}": question ${Number(match[1])} is not a question of this item on the page of batch ${batch} (its questions there: ${shown.join(", ")})`);
    if (!asks[at].choices[KEYS.indexOf(match[2])]) throw new InputError(`relay: the pick "${token}": question ${Number(match[1])} has no choice ${match[2]}`);
  }
  const many = asks.length !== 1;
  const lines = [
    `Relay from the chat "${oneLine(queue.chat.title)}". JP answered there the question${many ? "s" : ""} that you have for him.`,
    "",
    "JP's words, word for word:",
    words,
    "End of JP's words.",
    "",
  ];
  if (tokens.length > 0) lines.push(`JP's picks, as the chat that relays read them from his words (question number, choice letter): ${tokens.join(" ")}`, "");
  lines.push(`Not JP's words. Your question${many ? "s" : ""} and ${many ? "their" : "its"} choices, as that chat showed them to him:`);
  asks.forEach((ask, index) => {
    lines.push(`${shown[index]}. ${oneLine(ask.ask)}`);
    ask.choices.forEach((choice, at) => lines.push(`   ${KEYS[at]}. ${oneLine(choice.label)}`));
  });
  if (note) lines.push("", "Not JP's words (the chat that relays wrote this):", note);
  lines.push("", "Only the lines between \"JP's words, word for word:\" and \"End of JP's words.\" are from him. If they do not settle a question, ask him again in your next reply.");
  return `${lines.join("\n")}\n`;
}

export function main(argv, env = process.env) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: {
      thread: { type: "string" },
      "queue-root": { type: "string" },
      now: { type: "string" },
      out: { type: "string" },
      cards: { type: "string" },
      size: { type: "string" },
      again: { type: "string" },
      item: { type: "string" },
      words: { type: "string" },
      picks: { type: "string" },
      note: { type: "string" },
      sent: { type: "boolean", default: false },
      "keep-open": { type: "boolean", default: false },
    },
  });
  const [command] = positionals;
  const commands = ["brief", "merge", "batch", "relay"];
  if (!commands.includes(command)) throw new InputError(`command must be one of ${commands.join(", ")}`);
  if (!values.thread) throw new InputError(`${command}: --thread is required`);
  const parsed = values.now === undefined ? Date.now() : Date.parse(values.now);
  if (Number.isNaN(parsed)) throw new InputError(`--now "${values.now}" is not an ISO time`);
  const now = new Date(parsed).toISOString().replace(/\.\d{3}Z$/, "Z");
  const root = resolve(values["queue-root"] ?? defaultRoot(env));
  const dir = findQueue(root, values.thread);
  if (!dir) throw new InputError(`no queue for thread ${values.thread} under ${root}`);
  // Every value goes to the queue program as `--name=value`, one argument: an id or a note that starts
  // with "--" is then a value, never an option.
  const flag = (name, value) => `--${name}=${value}`;
  const q = (...args) => queueMain([...args, flag("thread", values.thread), flag("root", root), flag("now", now)], env);
  const queue = q("show", "--all");
  const items = ordered(queue.items);
  const put = (item, fields) => q("put", flag("item", JSON.stringify({ ...item, ...fields })));

  const open = items.filter(forJp);
  const noCursor = open.filter((item) => !isText(item.cursor) && asksOf(item) === null).map((item) => item.id);

  if (command === "brief") {
    if (!values.out) throw new InputError("brief: --out <cards file> is required");
    checkOneItemEachChat(open);
    const need = open.filter(needsReader);
    if (need.length === 0) throw new InputError(`brief: no item needs a card${noCursor.length ? ` (no card can be written for an item with no cursor: ${noCursor.join(", ")})` : ""}`);
    const list = join(dir, "cards-to-read.jsonl");
    const rows = need.map((item) => {
      const count = countOf(item.cursor);
      return JSON.stringify({ threadId: chatOf(item), cursor: item.cursor, item_count: Number.isFinite(count) ? count : null, title: item.title, questions: item.questions ?? [] });
    });
    const temp = join(dir, `.cards-to-read.${process.pid}.tmp`);
    writeFileSync(temp, `${rows.join("\n")}\n`, { flag: "wx" });
    renameSync(temp, list);
    const template = readFileSync(join(HERE, "..", "references", "card-brief.txt"), "utf8");
    // A function gives the text as it is: a "$&" in a file name is no pattern.
    return template.replaceAll("{{count}}", () => String(need.length)).replaceAll("{{to_read}}", () => list).replaceAll("{{out}}", () => resolve(values.out));
  }

  if (command === "merge") {
    const cards = readCards(values.cards);
    checkOneItemEachChat(open);
    const byThread = new Map(open.map((item) => [chatOf(item), item]));
    const out = { merged: [], stale: [], moved: [], not_open: [], answered: [], no_question: [] };
    const writes = [];
    const hold = (item, card, why) => {
      writes.push([item, { card_hold: { cursor: card.cursor, why, at: now } }]);
      out[why].push(card.threadId);
    };
    for (const card of cards) {
      const item = byThread.get(card.threadId);
      if (!item) out.not_open.push(card.threadId);
      else if (card.cursor !== item.cursor) out.stale.push(card.threadId);
      // An earlier report holds the card of this reply: it stands, whatever this line says.
      else if (held(item)) out[item.card_hold.why].push(card.threadId);
      // The cursor ends in the item count of the reply that asks. More items now: the chat moved after the
      // scan, so the question may be answered. The next scan reads it again.
      else if (Number.isFinite(card.item_count_now) && Number.isFinite(countOf(card.cursor)) && card.item_count_now !== countOf(card.cursor)) hold(item, card, "moved");
      else if (card.answered) hold(item, card, "answered");
      else if (card.asks.length === 0) hold(item, card, "no_question");
      else {
        const first = card.asks[0];
        writes.push([item, {
          asks: card.asks,
          asks_cursor: card.cursor,
          context: card.context,
          card: {
            ...item.card,
            state: card.context,
            ask: card.asks.map((ask) => ask.ask).join(" "),
            recommend: Number.isInteger(first.pick) ? first.choices[first.pick].label : null,
            ifNoAnswer: first.if_no_answer ?? null,
          },
        }]);
        out.merged.push(card.threadId);
      }
    }
    for (const [item, fields] of writes) put(item, fields);
    return out;
  }

  if (command === "batch") {
    const size = values.size === undefined ? 5 : Number(values.size);
    if (!Number.isInteger(size) || size < 1) throw new InputError("batch: --size must be a whole number of 1 or more");
    const noCard = open.filter(needsReader).length;
    const holds = open.filter(held).map((item) => ({ item: item.id, why: item.card_hold.why }));
    const rest = { no_card: noCard, held: holds, no_cursor: noCursor };
    const ready = open.filter((item) => asksOf(item) !== null && !(item.shown && item.shown.cursor === (item.cursor ?? null)));
    const groupOf = (item) => item.project || "no project";
    const folder = join(dir, "batches");
    const again = values.again !== undefined;
    let number;
    const taken = [];
    if (again) {
      number = Number(values.again);
      if (!Number.isInteger(number) || number < 1) throw new InputError("batch: --again must be the number of a batch");
      taken.push(...open.filter((item) => asksOf(item) !== null && item.shown && item.shown.batch === number && item.shown.cursor === (item.cursor ?? null)));
      if (taken.length === 0) throw new InputError(`batch: no open question of batch ${number} is left to show`);
    } else {
      if (ready.length === 0) return { batch: null, questions: [], left: 0, ...rest };
      let count = 0;
      for (const item of ready) {
        const asks = asksOf(item);
        if (groupOf(item) !== groupOf(ready[0])) continue;
        if (taken.length > 0 && count + asks.length > size) continue;
        taken.push(item);
        count += asks.length;
        if (count >= size) break;
      }
      mkdirSync(folder, { recursive: true });
      number = readdirSync(folder).filter((name) => /^batch-\d+\.json$/.test(name)).length + 1;
    }
    const group = groupOf(taken[0]);
    const questions = [];
    for (const item of taken) {
      asksOf(item).forEach((ask, index) => {
        questions.push({
          n: questions.length + 1, item: item.id, index, title: item.title, link: item.link ?? null, context: item.context ?? null,
          emoji: ask.emoji, ask: ask.ask, why: ask.why ?? null,
          choices: ask.choices.map((choice, at) => ({ key: KEYS[at], label: choice.label, gain: choice.gain ?? null, cost: choice.cost ?? null, pick: ask.pick === at })),
          because: ask.because ?? null, experts: ask.experts, if_no_answer: ask.if_no_answer ?? null, yours: ask.yours,
        });
      });
    }
    const left = ready.filter((item) => !taken.includes(item)).reduce((sum, item) => sum + asksOf(item).length, 0);
    const batch = { batch: number, group, at: now, questions, left };
    const page = join(folder, `batch-${number}.html`);
    const map = join(folder, `batch-${number}.json`);
    writeFileSync(map, `${JSON.stringify(batch, null, 1)}\n`, { flag: again ? "w" : "wx" });
    writeFileSync(page, pageHtml(batch), { flag: again ? "w" : "wx" });
    if (!again) for (const item of taken) put(item, { shown: { batch: number, cursor: item.cursor ?? null, at: now } });
    return { batch: number, group, page, map, questions: questions.map(({ n, item, ask }) => ({ n, item, ask })), left, ...rest };
  }

  // relay
  if (!values.item) throw new InputError("relay: --item <id> is required");
  if (!isText(values.words) || values.words.trim() === "") throw new InputError("relay: --words \"<JP's words>\" is required");
  const item = items.find((other) => other.id === values.item);
  if (!item) throw new InputError(`relay: no item "${values.item}" in the queue`);
  if (!OPEN.has(item.status)) throw new InputError(`relay: the item "${values.item}" is ${item.status}`);
  const asks = asksOf(item);
  if (asks === null) throw new InputError(`relay: the item "${values.item}" has no card for its newest reply`);
  const text = relayText(queue, asks, shownNumbers(dir, item, asks), item.shown?.batch, values);
  if (values.sent) {
    put(item, { relayed: [...(Array.isArray(item.relayed) ? item.relayed : []), { at: now, words: values.words }] });
    if (!values["keep-open"]) q("resolve", flag("item", item.id), flag("to", "done"), flag("note", `JP answered in the chat "${queue.chat.title}": ${values.words}`));
  }
  return text;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  try {
    const out = main(process.argv.slice(2));
    process.stdout.write(typeof out === "string" ? out : `${JSON.stringify(out, null, 2)}\n`);
  } catch (error) {
    if (error instanceof InputError || error instanceof QueueInputError || String(error?.code || "").startsWith("ERR_PARSE_ARGS")) {
      process.stderr.write(`cards: ${error.message}\n`);
      process.exit(2);
    }
    throw error;
  }
}
