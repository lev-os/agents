#!/usr/bin/env node
// Writes the page of one question sheet (groups of questions for JP, then the pins that went quiet).
// Usage: node render-sheet.mjs <sheet json> <out html>
// This is the one form of a sheet. JP 2026-11-19: "everytime we do this u print cards in a different way, the
// previous way was better it had a chat link, multiple choice, better numbering, not too many / little emojis".
// Write no other page program for a sheet; change this one.
// The sheet file: { sheet, first_number, last_number?, example?, groups: [{ mark, title, note, questions:
//   [{ n, emoji, ask, choices: ["a. ...", "b. ..."], rec: "a: why" | null, chat: "<chat title>", yours }] }],
//   pins: [{ p, chat, left, send, pin }], send?: { n, wording, chats: ["<chat title>"] } }.
// `n` counts from 1 on each sheet: number-sheet.mjs sets it and writes the map to each permanent id. One emoji for each card, one mark for each group.
// Each card names its chat; the reply under the sheet gives each chat's link, because a link inside the page
// does not open.
import { readFileSync, writeFileSync } from "node:fs";

const [source, out] = process.argv.slice(2);
const sheet = JSON.parse(readFileSync(source, "utf8"));
const esc = (text) => String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const total = sheet.groups.reduce((sum, group) => sum + group.questions.length, 0);

const card = (q) => `
    <div class="card">
      <div class="num">${q.n}</div>
      <div class="body">
        <div class="ask"><span class="emo">${esc(q.emoji)}</span>${esc(q.ask)}</div>
        ${q.choices.length ? `<div class="opts">${q.choices.map((choice) => `<span class="opt">${esc(choice)}</span>`).join("")}</div>` : ""}
        <div class="meta">${q.rec ? `<span class="rec">👉 The chat recommends: ${esc(q.rec)}</span>` : `<span class="norec">The chat gives no recommendation.</span>`}</div>
        <div class="from">💬 ${esc(q.chat)}${q.yours ? ` <span class="hand">✋ only you can do this</span>` : ""}</div>
      </div>
    </div>`;

const group = (g) => `
  <section>
    <h2><span>${esc(g.mark)}</span> ${esc(g.title)} <em>${g.questions[0].n} to ${g.questions[g.questions.length - 1].n}</em></h2>
    ${g.note ? `<p class="note">${esc(g.note)}</p>` : ""}
    ${g.questions.map(card).join("")}
  </section>`;

const pin = (p) => `
      <tr><td class="pn">P${p.p}</td><td><b>${esc(p.chat)}</b><br><span class="left">${esc(p.left)}</span></td><td>${esc(p.send)}</td><td>${esc(p.pin)}</td></tr>`;

const html = `<!doctype html>
<meta charset="utf-8">
<title>Questions for JP, sheet ${sheet.sheet}</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: var(--font-sans); color: var(--foreground); font-size: 14px; line-height: 1.45; }
  .top { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .chip { border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; font-size: 13px; color: var(--muted-foreground); }
  .chip b { color: var(--foreground); }
  section { margin-bottom: 22px; }
  h2 { font-size: 16px; margin: 0 0 4px; display: flex; align-items: baseline; gap: 8px; }
  h2 em { font-style: normal; font-size: 12px; font-weight: 400; color: var(--muted-foreground); margin-left: auto; }
  .note { margin: 0 0 8px; font-size: 13px; color: var(--muted-foreground); }
  .card { display: flex; gap: 12px; border: 1px solid var(--border); background: var(--card); border-radius: var(--radius); padding: 12px 14px; margin-top: 8px; }
  .num { flex: none; width: 30px; height: 30px; border-radius: 50%; background: var(--secondary); color: var(--secondary-foreground); font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 13px; }
  .body { min-width: 0; flex: 1; }
  .ask { font-weight: 600; }
  .emo { margin-right: 6px; }
  .opts { display: flex; flex-direction: column; gap: 4px; margin-top: 8px; }
  .opt { border: 1px solid var(--border); border-radius: 8px; padding: 4px 10px; font-size: 13px; }
  .meta { margin-top: 8px; font-size: 13px; }
  .rec { color: var(--foreground); }
  .norec { color: var(--muted-foreground); }
  .from { margin-top: 4px; font-size: 12px; color: var(--muted-foreground); }
  .hand { margin-left: 6px; padding: 1px 8px; border-radius: 999px; background: var(--warning-surface); color: var(--warning-foreground); }
  table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
  th, td { text-align: left; vertical-align: top; padding: 8px 8px; border-top: 1px solid var(--border); }
  th { font-size: 12px; font-weight: 600; color: var(--muted-foreground); border-top: none; }
  .pn { font-weight: 700; white-space: nowrap; }
  .left { color: var(--muted-foreground); }
  .how { border: 1px dashed var(--border); border-radius: var(--radius); padding: 10px 14px; font-size: 13px; }
  .how code { font-family: var(--font-mono); background: var(--code-background); padding: 1px 6px; border-radius: 6px; }
</style>
<div class="top">
  <span class="chip"><b>${total}</b> questions</span>
  <span class="chip"><b>${sheet.groups.length}</b> ${sheet.groups.length === 1 ? "group" : "groups, the urgent one first"}</span>
  ${sheet.pins.length ? `<span class="chip"><b>${sheet.pins.length}</b> quiet pins</span>` : ""}${sheet.first_number ? `<span class="chip">numbers <b>${sheet.first_number}</b> to <b>${sheet.send ? sheet.send.n : sheet.last_number}</b>, the numbers run on from the last sheet</span>` : ""}
</div>
${sheet.groups.map(group).join("")}${sheet.pins.length ? `
  <section>
    <h2><span>📌</span> Pins that went quiet <em>P1 to P${sheet.pins.length}</em></h2>
    <p class="note">For each: may I send it a message, and does the pin stay? The table holds my recommendation.</p>
    <table>
      <tr><th></th><th>Chat and the work left</th><th>Message</th><th>Pin</th></tr>${sheet.pins.map(pin).join("")}
    </table>
  </section>` : ""}${sheet.send ? `
  <section>
    <h2><span>⏸️</span> ${esc(sheet.send.title ?? "Stopped with approved work")} <em>${sheet.send.n}</em></h2>
    <div class="card">
      <div class="num">${sheet.send.n}</div>
      <div class="body">
        <div class="ask">May I send these ${sheet.send.chats.length} chats the line: ${esc(sheet.send.wording)}</div>
        <div class="opts">${sheet.send.chats.map((chat) => `<span class="opt">${esc(chat)}</span>`).join("")}</div>
        <div class="meta"><span class="rec">👉 ${esc(sheet.send.rec ?? "I recommend yes: the line starts only work that you approved before.")}</span></div>
      </div>
    </div>
  </section>` : ""}
  <div class="how">Answer by number in one message, for example <code>${esc(sheet.example ?? "1 yes · 2b · 5b · 11 no · P1 ok · P3 send, keep")}</code>. <code>recs</code> means yes to each recommendation shown. A question with no answer stays on the sheet.</div>
`;
writeFileSync(out, html);
console.log(`${total} questions, ${sheet.pins.length} pins -> ${out}`);
