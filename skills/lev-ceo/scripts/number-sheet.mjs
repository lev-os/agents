#!/usr/bin/env node
// Numbers the cards of one sheet from 1, in the order shown, and writes the map from each number to the
// permanent id of its question. The send card takes the last number.
// Usage: node number-sheet.mjs <sheet json> [--strict [--now <UTC time>]]
//        (rewrites the sheet file; writes <sheet>.map.json beside it)
// JP 2026-11-20: "I don't want to have to type 101, 102" and "2b i dont wanna maintain the sheet". So a number
// lives for one sheet only. The permanent id (`id` on each question and on the send card) is what the queue
// and the rule against a repeated ask use; JP never sees it. An answer "3b" is looked up in the map of the
// sheet it answers. Run this before render-sheet.mjs.
//
// --strict is the gate before a sheet is shown. It refuses the sheet, and numbers nothing, when:
//   - a card has no `checked_at`, or its `checked_at` is over 60 minutes before now. `checked_at` is the time you
//     last read the card's chat AND tested that the card is still true (the app is open, the permission is off,
//     the thing it names is there). A chat that did not move is not proof: JP acts outside the chat.
//   - a card with `yours: true` (an errand for him) has no `proof`: what an agent tried, and why it could not do it.
// JP 2026-11-20: "these questions are stale", "I DID THIS SHIT ALREADY", "YOU FUCKING DO IT. YOU NEED TO FIGURE
// OUT HOW TO AUTOMATE THESE THINGS". Four of six errand cards of sheet 7 were not true or not his to do.
import { readFileSync, writeFileSync } from "node:fs";

const args = process.argv.slice(2);
const nowAt = args.indexOf("--now");
const file = args.find((arg, i) => !arg.startsWith("--") && (nowAt < 0 || i !== nowAt + 1));
if (!file) throw new Error("usage: number-sheet.mjs <sheet json> [--strict [--now <UTC time>]]");
const strict = args.includes("--strict");
const now = nowAt < 0 ? Date.now() : Date.parse(args[nowAt + 1]);
const MAX_AGE_MIN = 60;

const sheet = JSON.parse(readFileSync(file, "utf8"));
const numbers = {};
const seen = new Set();
const refused = [];
let n = 0;
const short = (item) => String(item.ask ?? item.wording ?? "").slice(0, 60);
const take = (item, what) => {
  if (typeof item.id !== "string" || !item.id) throw new Error(`${what} has no id: ${short(item)}`);
  if (seen.has(item.id)) throw new Error(`the id ${item.id} is on the sheet two times`);
  seen.add(item.id);
  if (strict) {
    const at = Date.parse(item.checked_at ?? "");
    if (Number.isNaN(at)) refused.push(`${item.id}: never checked (no checked_at): ${short(item)}`);
    else if (now - at > MAX_AGE_MIN * 60000) refused.push(`${item.id}: checked ${Math.round((now - at) / 60000)} minutes ago, the limit is ${MAX_AGE_MIN}: ${short(item)}`);
    if (item.yours && !String(item.proof ?? "").trim()) refused.push(`${item.id}: an errand for JP with no proof that an agent tried it: ${short(item)}`);
  }
  n += 1;
  item.n = n;
  numbers[n] = item.id;
};
// JP 2026-11-21, on a sheet of hand-cut cards ("what acts", "what?", "are u implying we're starting over?"): "its
// like w/ every load of the cards you also need to re-orient and read the holistic view per project". So strict
// also refuses a group with no `end_state` (the goal's end state, copied from the goal map) and a card with no
// `what` (one sentence: what the thing is and what waits on it, for a reader who never saw the chat).
for (const group of sheet.groups) {
  if (strict && !String(group.end_state ?? "").trim()) refused.push(`group "${group.title}": no end_state. Read the goal map and the project's own page, then copy the goal's end state here`);
  for (const question of group.questions) {
    if (strict && !String(question.what ?? "").trim()) refused.push(`${question.id}: no \`what\` line (what the thing is and what waits on it): ${short(question)}`);
    take(question, "a question");
  }
}
if (sheet.send) take(sheet.send, "the send card");
if (refused.length) throw new Error(`the sheet is not shown; ${refused.length} card(s) refused:\n${refused.join("\n")}`);
delete sheet.first_number;
delete sheet.last_number;
writeFileSync(file, `${JSON.stringify(sheet, null, 2)}\n`);
const mapFile = file.replace(/\.json$/, ".map.json");
writeFileSync(mapFile, `${JSON.stringify({ sheet: sheet.sheet, numbers }, null, 2)}\n`);
console.log(`${n} numbers -> ${mapFile}`);
