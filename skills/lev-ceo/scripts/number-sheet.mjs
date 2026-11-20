#!/usr/bin/env node
// Numbers the cards of one sheet from 1, in the order shown, and writes the map from each number to the
// permanent id of its question. The send card takes the last number.
// Usage: node number-sheet.mjs <sheet json>     (rewrites the sheet file; writes <sheet>.map.json beside it)
// JP 2026-11-20: "I don't want to have to type 101, 102" and "2b i dont wanna maintain the sheet". So a number
// lives for one sheet only. The permanent id (`id` on each question and on the send card) is what the queue
// and the rule against a repeated ask use; JP never sees it. An answer "3b" is looked up in the map of the
// sheet it answers. Run this before render-sheet.mjs.
import { readFileSync, writeFileSync } from "node:fs";

const [file] = process.argv.slice(2);
if (!file) throw new Error("usage: number-sheet.mjs <sheet json>");
const sheet = JSON.parse(readFileSync(file, "utf8"));
const numbers = {};
const seen = new Set();
let n = 0;
const take = (item, what) => {
  if (typeof item.id !== "string" || !item.id) throw new Error(`${what} has no id: ${String(item.ask ?? item.wording ?? "").slice(0, 60)}`);
  if (seen.has(item.id)) throw new Error(`the id ${item.id} is on the sheet two times`);
  seen.add(item.id);
  n += 1;
  item.n = n;
  numbers[n] = item.id;
};
for (const group of sheet.groups) for (const question of group.questions) take(question, "a question");
if (sheet.send) take(sheet.send, "the send card");
delete sheet.first_number;
delete sheet.last_number;
writeFileSync(file, `${JSON.stringify(sheet, null, 2)}\n`);
const mapFile = file.replace(/\.json$/, ".map.json");
writeFileSync(mapFile, `${JSON.stringify({ sheet: sheet.sheet, numbers }, null, 2)}\n`);
console.log(`${n} numbers -> ${mapFile}`);
