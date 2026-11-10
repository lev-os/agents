#!/usr/bin/env node
// Audit the CEO skill against what the CEO sessions did. Reads Claude Code session transcripts (JSONL),
// splits each into turns, and counts: loop ticks and what they changed, settle orders, repeated questions,
// and five rules the skill states. Every count carries transcript line numbers.
//
// Usage: node audit.mjs --since <ISO> --out <report.json> <name>=<transcript.jsonl> ...
import { createReadStream, writeFileSync } from "node:fs";
import { createInterface } from "node:readline";
import { parseArgs } from "node:util";

const { values, positionals } = parseArgs({
  options: { since: { type: "string" }, out: { type: "string" } },
  allowPositionals: true,
});
const since = values.since ?? "1970-01-01T00:00:00Z";

const TICK = /^(15-minute watch for the Leviathan CEO node|<command-message>ll<\/command-message>\s*<command-name>\/ll<\/command-name>\s*<command-args>run )/;
const WAKE = /^<task-notification>|^<system-reminder>\s*The session "/;
const RELAY = /^(From the (Leviathan|Multiplayer) CEO node|Handoff from CEO|Delegated task )/;
const COMPACT = /^This session is being continued from a previous conversation/;
const INTERRUPT = /^\[Request interrupted/;
const SETTLE_WORDS = /\b(settle[ds]?|archiv(e|ed|ing)|unsettle|close (the|those|these|all|idle|finished|old)|clean ?up (the )?(tabs|chats|threads|workers))\b/i;
const HANDOFF = /\.lev\/pm\/handoffs\//;

function humanText(record) {
  const content = record.message?.content;
  if (typeof content === "string") return content;
  if (!Array.isArray(content) || content.some((block) => block.type === "tool_result")) return null;
  return content.filter((block) => block.type === "text").map((block) => block.text).join("\n");
}

function classify(text) {
  const head = text.trimStart();
  if (TICK.test(head)) return "tick";
  if (WAKE.test(head)) return "wake";
  if (RELAY.test(head)) return "relay";
  if (COMPACT.test(head)) return "compaction";
  if (INTERRUPT.test(head)) return "interrupt";
  return "jp";
}

async function readTurns(name, file) {
  const turns = [];
  let turn = null;
  let line = 0;
  const lines = createInterface({ input: createReadStream(file), crlfDelay: Infinity });
  for await (const raw of lines) {
    line += 1;
    let record;
    try { record = JSON.parse(raw); } catch { continue; }
    if (record.isSidechain || record.isMeta) continue;
    if (record.type === "user") {
      const text = humanText(record);
      if (text === null) continue;
      turn = { session: name, line, at: record.timestamp, type: classify(text), text, tools: [], texts: [] };
      turns.push(turn);
    } else if (record.type === "assistant" && turn && Array.isArray(record.message?.content)) {
      for (const block of record.message.content) {
        if (block.type === "tool_use") turn.tools.push({ name: block.name, input: block.input ?? {} });
        if (block.type === "text" && block.text.trim()) turn.texts.push(block.text);
      }
    }
  }
  return turns.filter((t) => (t.at ?? since) >= since);
}

function facts(turn) {
  const bash = turn.tools.filter((t) => t.name === "Bash").map((t) => String(t.input.command ?? ""));
  const files = turn.tools.filter((t) => t.name === "Edit" || t.name === "Write").map((t) => String(t.input.file_path ?? ""));
  const short = (n) => turn.tools.filter((t) => t.name.endsWith(n));
  const settles = short("t3_thread_organize").filter((t) => t.input.action === "settle" || t.input.action === "archive");
  const reply = turn.texts.at(-1) ?? "";
  return {
    commit: bash.some((c) => /\bgit\b[^\n]*\bcommit\b/.test(c)),
    date: bash.some((c) => /(^|[\s;&|(])date(\s|$)/.test(c)),
    capture: files.some((f) => /\/captures\//.test(f)) || bash.some((c) => /\/captures\/[^\s]*\.ya?ml/.test(c) && /(>|tee|cat <<|git add)/.test(c)),
    handoff: files.some((f) => HANDOFF.test(f)) || bash.some((c) => HANDOFF.test(c)),
    otherFiles: files.filter((f) => !HANDOFF.test(f)).length,
    sends: short("t3_thread_send").length + short("send_message").length + short("SendMessage").length,
    renames: short("t3_thread_update").length,
    settles: settles.length,
    launches: short("delegate_task").length + short("t3_thread_launch").length + short("create_threads").length + short("start_session").length,
    schedules: short("schedule_task").length + short("CronCreate").length,
    unschedules: short("delete_scheduled_task").length + short("CronDelete").length,
    reply,
    mesh: reply.includes("lev://mesh"),
  };
}

const changedSomething = (f) => f.commit || f.sends > 0 || f.renames > 0 || f.settles > 0 || f.launches > 0 || f.schedules > 0 || f.unschedules > 0 || f.otherFiles > 0;

function questions(f) {
  const out = [];
  for (const row of f.reply.split("\n")) {
    const m = row.match(/^\s*(?:\d+\.|[-*])?\s*\*\*([^*]{12,}\?)\*\*/);
    if (m) out.push(m[1].trim());
  }
  return out;
}

const STOP = new Set("the a an to of in on for and or is are do does did i you we it this that be with my your as at by from should can will would which what how now yes no not".split(" "));
const tokens = (q) => new Set(q.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)));
function jaccard(a, b) {
  let both = 0;
  for (const w of a) if (b.has(w)) both += 1;
  return both / (a.size + b.size - both || 1);
}

const report = { since, sessions: {} };
const ref = (t) => `${t.session}:L${t.line}`;

for (const pair of positionals) {
  const [name, file] = pair.split("=");
  const turns = await readTurns(name, file);
  const rows = turns.map((t) => ({ t, f: facts(t) }));
  const of = (type) => rows.filter((r) => r.t.type === type);

  const ticks = of("tick");
  const wakes = of("wake");
  const jp = of("jp");
  const idle = (list) => list.filter((r) => !changedSomething(r.f));

  const asked = [];
  for (const r of rows) for (const q of questions(r.f)) asked.push({ q, ref: ref(r.t), at: r.t.at, line: r.t.line, tok: tokens(q) });
  const clusters = [];
  for (const item of asked) {
    const home = clusters.find((c) => jaccard(c[0].tok, item.tok) >= 0.6);
    if (home) home.push(item); else clusters.push([item]);
  }
  const repeated = clusters
    .filter((c) => new Set(c.map((i) => i.line)).size > 1)
    .map((c) => ({ times: new Set(c.map((i) => i.line)).size, question: c[0].q, refs: [...new Set(c.map((i) => i.ref))] }));

  const settleOrders = rows
    .filter((r) => (r.t.type === "jp" || r.t.type === "relay") && SETTLE_WORDS.test(r.t.text.slice(0, 4000)))
    .map((r) => ({ ref: ref(r.t), at: r.t.at, type: r.t.type, settles_in_turn: r.f.settles, words: r.t.text.replace(/\s+/g, " ").slice(0, 200) }));

  const settleCalls = rows.filter((r) => r.f.settles > 0).map((r) => ({ ref: ref(r.t), at: r.t.at, on: r.t.type, count: r.f.settles }));
  const launchTurns = rows.filter((r) => r.f.launches > 0);
  const commitTurns = rows.filter((r) => r.f.commit);
  const replied = jp.filter((r) => r.f.reply.length > 0);

  report.sessions[name] = {
    turns: { total: rows.length, jp: jp.length, tick: ticks.length, wake: wakes.length, relay: of("relay").length, compaction: of("compaction").length },
    ticks: {
      total: ticks.length,
      changed_nothing: idle(ticks).length,
      changed_nothing_refs: idle(ticks).map((r) => ref(r.t)),
      changed_something_refs: ticks.filter((r) => changedSomething(r.f)).map((r) => ref(r.t)),
      first: ticks[0]?.t.at ?? null,
      last: ticks.at(-1)?.t.at ?? null,
    },
    wakes: { total: wakes.length, changed_nothing: idle(wakes).length },
    settle_orders: settleOrders,
    settle_calls: settleCalls,
    questions: { asked: asked.length, repeated },
    rules: {
      capture_on_every_jp_message: { jp_turns: jp.length, with_capture_file: jp.filter((r) => r.f.capture).length },
      date_before_stamps: { jp_turns: jp.length, with_date: jp.filter((r) => r.f.date).length },
      mesh_line_on_every_reply: { replies: replied.length, with_mesh_line: replied.filter((r) => r.f.mesh).length, missing_refs: replied.filter((r) => !r.f.mesh).map((r) => ref(r.t)).slice(0, 12) },
      check_set_in_the_launch_turn: { launch_turns: launchTurns.length, with_schedule: launchTurns.filter((r) => r.f.schedules > 0).length, refs: launchTurns.map((r) => ref(r.t)) },
      handoff_updated_when_committing: { commit_turns: commitTurns.length, touching_handoff: commitTurns.filter((r) => r.f.handoff).length },
    },
  };
}

if (values.out) writeFileSync(values.out, `${JSON.stringify(report, null, 2)}\n`);
for (const [name, s] of Object.entries(report.sessions)) {
  console.log(`== ${name}`);
  console.log("turns", JSON.stringify(s.turns));
  console.log("ticks", s.ticks.total, "changed nothing", s.ticks.changed_nothing, "first", s.ticks.first, "last", s.ticks.last);
  console.log("wakes", JSON.stringify(s.wakes));
  console.log("settle orders", s.settle_orders.length, "| settle calls", JSON.stringify(s.settle_calls));
  for (const o of s.settle_orders) console.log("  ", o.ref, o.at, o.type, `settles=${o.settles_in_turn}`, "|", o.words.slice(0, 150));
  console.log("questions asked", s.questions.asked, "repeated clusters", s.questions.repeated.length);
  for (const q of s.questions.repeated) console.log("  ", `x${q.times}`, q.refs.join(" "), "|", q.question.slice(0, 120));
  console.log("rules", JSON.stringify(s.rules));
}
