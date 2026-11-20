#!/usr/bin/env node
/**
 * The goal map: what JP builds, grouped by long-horizon goal, with the end state of each goal, the chats that
 * serve it and the laws each answer respects (references/goal-map.md). This program draws the map from its data
 * file and checks that each open chat has one place on it. It reads no chat and sends nothing. Stdlib only.
 *
 * Usage: node goal-map.mjs <command> --map <map json> [options]
 *   render --out <html>                       -> writes the page (shown with html_preview, then html_render)
 *   check  --threads <threads json> [--self <this chat's id>]
 *                                             -> {placed, unplaced: [{title, id}], twice: [title], gone: [title]}
 *                                                exit 1 when an open chat has no place or a chat has two places
 *   ids    --threads <threads json>           -> writes each chat's id on its entry (matched by title), so a
 *                                                renamed chat keeps its place
 * The threads file is the one list-chats.mjs writes: {threads: [{threadId, title}]}.
 *
 * The map file:
 *   {at, accepted?: {by, at, words},
 *    context: [{title, text}],                                 the top row: who asks, what makes it true, what it builds
 *    sections: [{title, note?, goals: [{name, end: [{text, source?}], chats: [{title, id?, elsewhere?}]}]}],
 *    laws: [{name, text}], example?: {title, today: {title, text}, should: {title, text}}}
 * `end` is the end state in one to three sentences. `source` says whose words a part is: a page of the project, or
 * "my reading". `elsewhere` names another machine: that chat is not in this machine's list and is not checked.
 * Exit 0 ok, 1 a check failed, 2 bad input (the reason on stderr).
 */
import { readFileSync, renameSync, writeFileSync } from "node:fs";

const [command, ...args] = process.argv.slice(2);
const flag = (name) => { const at = args.indexOf(name); return at < 0 ? null : args[at + 1]; };
const refuse = (reason) => { console.error(`goal-map: ${reason}`); process.exit(2); };
const read = (file, what) => {
  if (!file) refuse(`${command ?? "no command"}: needs ${what}`);
  try { return JSON.parse(readFileSync(file, "utf8")); } catch (error) { refuse(`cannot read ${file}: ${error.message}`); }
};
const save = (file, text) => { writeFileSync(`${file}.tmp`, text); renameSync(`${file}.tmp`, file); };

const mapFile = flag("--map");
const map = read(mapFile, "--map <map json>");
const goals = (map.sections ?? []).flatMap((section) => section.goals ?? []);
if (goals.length === 0) refuse("the map has no goal");
for (const goal of goals) {
  if (!goal.name) refuse("a goal has no name");
  if (!Array.isArray(goal.end) || goal.end.every((part) => !String(part.text ?? "").trim())) refuse(`the goal "${goal.name}" has no end state`);
}
const entries = goals.flatMap((goal) => goal.chats ?? []);

const esc = (text) => String(text ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");

function render() {
  const out = flag("--out");
  if (!out) refuse("render: needs --out <html>");
  const colors = ["--primary", "--chart-2", "--chart-3", "--chart-4", "--chart-5", "--border"];
  const top = (map.context ?? []).map((box) => `<div class="box"><b>${esc(box.title)}</b><span>${esc(box.text)}</span></div>`).join('<div class="arrow">→</div>');
  const columns = (map.context ?? []).map(() => "1fr").join(" auto ");
  let color = 0;
  const sections = (map.sections ?? []).map((section, at) => {
    const tint = at === 0 ? () => colors[0] : () => colors[Math.min(++color, colors.length - 1)];
    const rows = (section.goals ?? []).map((goal) => {
      const end = goal.end.map((part) => `${esc(part.text)}${part.source ? ` <span class="src">(${esc(part.source)})</span>` : ""}`).join(" ");
      const chips = (goal.chats ?? []).map((chat) => `<i>${esc(chat.title)}${chat.elsewhere ? ` (${esc(chat.elsewhere)})` : ""}</i>`).join("");
      return `<div class="g" style="border-left-color: var(${tint()})"><span class="name">${esc(goal.name)}</span>\n<div class="end">End state: ${end}</div>\n<div class="chips">${chips}</div></div>`;
    }).join("\n");
    return `<h3>${esc(section.title)}${section.note ? ` <small>· ${esc(section.note)}</small>` : ""}</h3>\n${rows}`;
  }).join("\n");
  const laws = (map.laws ?? []).length === 0 ? "" : `<h3>The laws each answer must respect</h3>\n<ol>${map.laws.map((law) => `<li><b>${esc(law.name)}</b> ${esc(law.text)}</li>`).join("")}</ol>`;
  const example = !map.example ? "" : `<h3>${esc(map.example.title)}</h3>\n<div class="two"><div class="box bad"><b>${esc(map.example.today.title)}</b><p>${esc(map.example.today.text)}</p></div><div class="box good"><b>${esc(map.example.should.title)}</b><p>${esc(map.example.should.text)}</p></div></div>`;
  save(out, `<!doctype html>
<meta charset="utf-8">
<style>
  .wrap { font-family: var(--font-sans); color: var(--foreground); font-size: 13.5px; line-height: 1.45; }
  .top { display: grid; grid-template-columns: ${columns}; gap: 8px; align-items: stretch; margin-bottom: 14px; }
  .box { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 9px 11px; }
  .box b { display: block; }
  .box span { color: var(--muted-foreground); font-size: 12px; }
  .box p { margin: 4px 0 0; }
  .arrow { align-self: center; color: var(--muted-foreground); font-size: 18px; }
  h3 { font-size: 14px; margin: 16px 0 6px; padding-bottom: 5px; border-bottom: 1px solid var(--border); }
  h3 small { font-weight: 400; color: var(--muted-foreground); }
  .g { padding: 8px 0 8px 12px; border-left: 3px solid var(--primary); margin: 8px 0; }
  .name { font-weight: 600; }
  .end { margin: 2px 0 5px; }
  .src { color: var(--muted-foreground); font-size: 12px; }
  .chips { display: flex; flex-wrap: wrap; gap: 4px; }
  .chips i { font-style: normal; font-size: 11.5px; padding: 1px 7px; border: 1px solid var(--border); border-radius: 999px; color: var(--muted-foreground); }
  ol { margin: 6px 0 0; padding-left: 20px; }
  ol li { margin: 3px 0; }
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
  .bad { border-left: 3px solid var(--destructive); } .good { border-left: 3px solid var(--success); }
</style>
<div class="wrap">
<div class="top">${top}</div>
${sections}
${laws}
${example}
</div>
`);
  console.log(JSON.stringify({ out, goals: goals.length, chats: entries.length }));
}

const openChats = () => {
  const self = flag("--self");
  return (read(flag("--threads"), "--threads <threads json>").threads ?? []).filter((thread) => thread.threadId !== self);
};
const matches = (entry, thread) => (entry.id ? entry.id === thread.threadId : entry.title === thread.title);

function check() {
  const open = openChats();
  const here = entries.filter((entry) => !entry.elsewhere);
  const seen = new Map();
  for (const entry of here) seen.set(entry.id ?? entry.title, (seen.get(entry.id ?? entry.title) ?? 0) + 1);
  const twice = here.filter((entry) => seen.get(entry.id ?? entry.title) > 1).map((entry) => entry.title).filter((title, at, all) => all.indexOf(title) === at);
  const unplaced = open.filter((thread) => !here.some((entry) => matches(entry, thread))).map((thread) => ({ title: thread.title, id: thread.threadId }));
  const gone = here.filter((entry) => !open.some((thread) => matches(entry, thread))).map((entry) => entry.title);
  console.log(JSON.stringify({ placed: open.length - unplaced.length, unplaced, twice, gone }));
  process.exit(unplaced.length > 0 || twice.length > 0 ? 1 : 0);
}

function ids() {
  const open = openChats();
  let written = 0;
  for (const entry of entries) {
    if (entry.id || entry.elsewhere) continue;
    const same = open.filter((thread) => thread.title === entry.title);
    if (same.length === 1) { entry.id = same[0].threadId; written += 1; }
  }
  save(mapFile, `${JSON.stringify(map, null, 2)}\n`);
  console.log(JSON.stringify({ written, without_id: entries.filter((entry) => !entry.id && !entry.elsewhere).map((entry) => entry.title) }));
}

if (command === "render") render();
else if (command === "check") check();
else if (command === "ids") ids();
else refuse(`unknown command "${command ?? ""}": use render, check or ids`);
