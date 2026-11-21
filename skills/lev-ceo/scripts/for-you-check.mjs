#!/usr/bin/env node
// Runs the form check of a question to JP (for-you-form.mjs) on saved replies, or on one reply.
// Usage: node for-you-check.mjs <replies.jsonl> [...more]   each row {id, chat, stopped_at, reply}:
//                                                            prints the totals, then one line for each reply with a fault
//        node for-you-check.mjs --text <file>                one reply as plain text: prints its result, exit 1 on a fault
import { readFileSync } from "node:fs";
import { checkForYouForm } from "./for-you-form.mjs";

const args = process.argv.slice(2);
if (args.length === 0 || (args[0] === "--text" && args.length !== 2)) {
  console.error("usage: for-you-check.mjs <replies.jsonl> [...more] | --text <file>");
  process.exit(2);
}
if (args[0] === "--text") {
  const result = checkForYouForm(readFileSync(args[1], "utf8"));
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.faults.length ? 1 : 0);
}
const totals = { replies: 0, with_for_you: 0, with_bare_list: 0, with_incomplete_item: 0, clean_for_you: 0 };
const flagged = [];
for (const file of args) {
  for (const row of readFileSync(file, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line))) {
    if (typeof row.reply !== "string") continue;
    totals.replies += 1;
    const result = checkForYouForm(row.reply);
    const bare = result.faults.some((fault) => fault.fault === "bare_list");
    const incomplete = result.faults.some((fault) => fault.fault === "item_incomplete");
    if (result.for_you_items) totals.with_for_you += 1;
    if (bare) totals.with_bare_list += 1;
    if (incomplete) totals.with_incomplete_item += 1;
    if (result.for_you_items && !bare && !incomplete) totals.clean_for_you += 1;
    if (bare || incomplete) flagged.push({ id: row.id, at: (row.stopped_at ?? "").slice(0, 10), chat: (row.chat ?? "").slice(0, 40), faults: result.faults });
  }
}
console.log(JSON.stringify(totals));
for (const row of flagged) console.log(JSON.stringify(row));
