#!/usr/bin/env node
/**
 * The question cards: what JP sees for each item of a chat queue, and the message that takes his answer
 * back to the chat that asked. Stdlib only (Node 22+). It reads no chat and sends no message: a reader
 * (a subagent) reads the chats, and the chat that runs this program sends the relay.
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/cards.mjs <command> --thread <this chat's id> [options]
 *   brief --out <cards file>   -> lists the open items with no card for their newest reply in
 *                                 <queue>/cards-to-read.jsonl and prints the brief for one reader
 *                                 (references/card-brief.txt). Exit 2 when no item needs a card.
 *   merge --cards <cards file> -> checks every line, then stores each card on its item (`asks`, `context`,
 *                                 `asks_cursor`). Prints {merged, stale, not_open, answered}.
 *   batch [--size 5]           -> the next questions for JP: at most --size questions, all of one project,
 *                                 numbered from 1. Writes <queue>/batches/batch-<n>.html (the page to show)
 *                                 and batch-<n>.json (question number -> item, choices), and marks each item
 *                                 as shown for its reply. Prints {batch, group, page, map, questions, left, no_card}.
 *   relay --item <id> --words "<JP's words>" [--picks "1a 2b"] [--note "<text>"] [--sent] [--keep-open]
 *                              -> prints the message for the chat that asked: JP's words unchanged, and every
 *                                 other sentence marked as not his. A pick is a question number of that item
 *                                 and a choice letter. With no --sent it writes nothing. After the send, run it
 *                                 again with --sent: it records the words on the item and closes it
 *                                 (--keep-open: a question of the item is still open).
 * Every command takes --queue-root <dir> (the folder that holds the queue folders) and --now <ISO>.
 *
 * A card belongs to one reply: it holds the cursor of the item it was written for. When the chat moves,
 * the item gets a new cursor (scripts/sweep.mjs queue), the card is not shown, and `brief` lists the chat again.
 * An item with no question (JP's message has no reply) needs no reader: the program writes its card.
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
const textOrNull = (value) => value === null || value === undefined || isText(value);
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

/** The asks to show for an item now, or null when a reader must write them first. */
function asksOf(item) {
  if (isText(item.cursor) && item.asks_cursor === item.cursor && Array.isArray(item.asks) && item.asks.length > 0) return item.asks;
  if (Array.isArray(item.questions) && item.questions.length === 0 && item.source === "sweep") return [noReply(item)];
  return null;
}
const forJp = (item) => OPEN.has(item.status) && item.kind !== "watch";

function checkAsk(ask, where) {
  const bad = (what) => new InputError(`${where}: ${what}`);
  if (!isRecord(ask)) throw bad("an ask is not an object");
  if (!isText(ask.ask) || ask.ask.trim() === "") throw bad("ask must be a text");
  if (!isText(ask.emoji)) throw bad("emoji must be a text");
  for (const key of ["why", "because", "if_no_answer"]) if (!textOrNull(ask[key])) throw bad(`${key} must be a text or null`);
  if (!Array.isArray(ask.choices) || ask.choices.length > KEYS.length) throw bad(`choices must be a list of at most ${KEYS.length}`);
  for (const choice of ask.choices) {
    if (!isRecord(choice) || !isText(choice.label) || choice.label.trim() === "") throw bad("a choice needs a label that is a text");
    if (!textOrNull(choice.gain) || !textOrNull(choice.cost)) throw bad("gain and cost of a choice must be a text or null");
  }
  if (ask.pick !== null && ask.pick !== undefined && !(Number.isInteger(ask.pick) && ask.pick >= 0 && ask.pick < ask.choices.length)) {
    throw bad("pick must be null or the position of one of the choices");
  }
  if (!Array.isArray(ask.experts) || !ask.experts.every(isText)) throw bad("experts must be a list of texts");
  if (typeof ask.yours !== "boolean") throw bad("yours must be true or false");
}

function checkLine(card, where) {
  const bad = (what) => new InputError(`${where}: ${what}`);
  if (!isRecord(card)) throw bad("not a card (a JSON object)");
  if (!isText(card.threadId) || card.threadId === "") throw bad("threadId must be a text");
  if (!isText(card.cursor)) throw bad("cursor must be a text");
  if (typeof card.answered !== "boolean") throw bad("answered must be true or false");
  if (!isText(card.context)) throw bad("context must be a text");
  if (!Array.isArray(card.asks)) throw bad("asks must be a list");
  if (!card.answered && card.asks.length === 0) throw bad("a chat that JP did not answer needs one ask or more");
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

function relayText(queue, asks, { words, picks, note }) {
  const chosen = new Map();
  for (const token of (picks || "").split(/[\s,]+/).filter(Boolean)) {
    const match = /^(\d+)([a-c])$/.exec(token);
    const ask = match ? asks[Number(match[1]) - 1] : null;
    const index = match ? KEYS.indexOf(match[2]) : -1;
    if (!ask || !ask.choices[index]) throw new InputError(`relay: the pick "${token}" names no question and choice of this item (write a question number and a letter, 1a)`);
    chosen.set(Number(match[1]) - 1, `${match[2]}. ${ask.choices[index].label}`);
  }
  const lines = [
    `Relay from the chat "${queue.chat.title}". JP answered there the question${asks.length === 1 ? "" : "s"} that you have for him.`,
    "",
    "JP's words, word for word:",
    words,
    "",
    `Your question${asks.length === 1 ? "" : "s"}, as that chat showed ${asks.length === 1 ? "it" : "them"} to him:`,
  ];
  asks.forEach((ask, index) => {
    lines.push(`${index + 1}. ${ask.ask}`);
    if (chosen.has(index)) lines.push(`   His pick: ${chosen.get(index)}`);
  });
  if (note) lines.push("", "Not JP's words (the chat that relays wrote this):", note);
  lines.push("", "Only the lines under \"JP's words\" and each \"His pick\" are from him. If they do not settle a question, ask him again in your next reply.");
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
  const q = (...args) => queueMain([...args, "--thread", values.thread, "--root", root, "--now", now], env);
  const queue = q("show", "--all");
  const items = ordered(queue.items);
  const put = (item, fields) => q("put", "--item", JSON.stringify({ ...item, ...fields }));

  if (command === "brief") {
    if (!values.out) throw new InputError("brief: --out <cards file> is required");
    const need = items.filter((item) => forJp(item) && isText(item.cursor) && asksOf(item) === null);
    if (need.length === 0) throw new InputError("brief: no item needs a card");
    const list = join(dir, "cards-to-read.jsonl");
    const rows = need.map((item) => {
      const count = Number(item.cursor.slice(item.cursor.lastIndexOf("#") + 1));
      return JSON.stringify({ threadId: item.threadId ?? item.id, cursor: item.cursor, item_count: Number.isFinite(count) ? count : null, title: item.title, questions: item.questions ?? [] });
    });
    const temp = join(dir, `.cards-to-read.${process.pid}.tmp`);
    writeFileSync(temp, `${rows.join("\n")}\n`, { flag: "wx" });
    renameSync(temp, list);
    const template = readFileSync(join(HERE, "..", "references", "card-brief.txt"), "utf8");
    return template.replaceAll("{{count}}", String(need.length)).replaceAll("{{to_read}}", list).replaceAll("{{out}}", resolve(values.out));
  }

  if (command === "merge") {
    const cards = readCards(values.cards);
    const byThread = new Map(items.filter(forJp).map((item) => [item.threadId ?? item.id, item]));
    const out = { merged: [], stale: [], not_open: [], answered: [] };
    const writes = [];
    for (const card of cards) {
      const item = byThread.get(card.threadId);
      if (!item) out.not_open.push(card.threadId);
      else if (card.cursor !== item.cursor) out.stale.push(card.threadId);
      else if (card.answered) out.answered.push(card.threadId);
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
    const open = items.filter(forJp);
    const noCard = open.filter((item) => asksOf(item) === null).length;
    const ready = open.filter((item) => asksOf(item) !== null && !(item.shown && item.shown.cursor === (item.cursor ?? null)));
    if (ready.length === 0) return { batch: null, questions: [], left: 0, no_card: noCard };
    const groupOf = (item) => item.project || "no project";
    const group = groupOf(ready[0]);
    const taken = [];
    let count = 0;
    for (const item of ready) {
      const asks = asksOf(item);
      if (groupOf(item) !== group) continue;
      if (taken.length > 0 && count + asks.length > size) continue;
      taken.push(item);
      count += asks.length;
      if (count >= size) break;
    }
    const folder = join(dir, "batches");
    mkdirSync(folder, { recursive: true });
    const number = readdirSync(folder).filter((name) => /^batch-\d+\.json$/.test(name)).length + 1;
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
    writeFileSync(map, `${JSON.stringify(batch, null, 1)}\n`, { flag: "wx" });
    writeFileSync(page, pageHtml(batch), { flag: "wx" });
    for (const item of taken) put(item, { shown: { batch: number, cursor: item.cursor ?? null, at: now } });
    return { batch: number, group, page, map, questions: questions.map(({ n, item, ask }) => ({ n, item, ask })), left, no_card: noCard };
  }

  // relay
  if (!values.item) throw new InputError("relay: --item <id> is required");
  if (!isText(values.words) || values.words.trim() === "") throw new InputError("relay: --words \"<JP's words>\" is required");
  const item = items.find((other) => other.id === values.item);
  if (!item) throw new InputError(`relay: no item "${values.item}" in the queue`);
  if (!OPEN.has(item.status)) throw new InputError(`relay: the item "${values.item}" is ${item.status}`);
  const asks = asksOf(item);
  if (asks === null) throw new InputError(`relay: the item "${values.item}" has no card for its newest reply`);
  const text = relayText(queue, asks, values);
  if (values.sent) {
    put(item, { relayed: [...(Array.isArray(item.relayed) ? item.relayed : []), { at: now, words: values.words }] });
    if (!values["keep-open"]) q("resolve", "--item", item.id, "--to", "done", "--note", `JP answered in the chat "${queue.chat.title}": ${values.words}`);
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
