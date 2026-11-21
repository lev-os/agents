// The stop hook, as a Claude mod (JP 2026-11-17: "a stop hook should classify the previous response and respond
// with continue with anything that is shovel ready and approved. collect all questions").
//
// It hooks the engine's own Stop event (classic.Stop). The event says what a program can know: a background task
// that still runs, a wake-up that is set, a stop that a hook already held. A small model reads the reply for the
// rest and gives one label (the rules: stop-hook/label-rules-v3.txt). The policy below turns a label into push or quiet.
//
// Mode, the one word in stop-hook/mode.txt: `off`, `shadow` (the default: write the decision, hold nothing) or `push`.
// The replay: stop-hook/replay-request.json names models; the same judge then reads each fixture.
import type { Register } from 'claude-code'
import { checkForYouForm } from './for-you-form.mjs'

const DIR = '/Users/jean-patricksmith/.local/state/lev/ceo/lost-time/stop-hook'
const MODE = `${DIR}/mode.txt`
const RULES = `${DIR}/label-rules-v3.txt`
const LIVE_LOG = `${DIR}/live-log.tsv`
const LIVE_STATE = `${DIR}/live-state.json`
const ERRORS = `${DIR}/mod-errors.txt`
const REQUEST = `${DIR}/replay-request.json`
const FIXTURES = `${DIR}/fixtures.jsonl`

const LABELS = ['not_a_reply', 'jp_said_stop', 'plan_ready', 'default_ready', 'waits_run', 'needs_jp', 'done'] as const
// The policy: which labels the hook pushes on. default_ready waits for JP's ruling (may the hook take a stated default at once?).
const PUSH_ON = ['plan_ready']
const MAX_PUSHES = 3   // for each message of JP
// Two judges, and the hook pushes only when both say plan_ready. Replay r3b on 150 unseen stops: sonnet alone pushed
// wrongly in 3 of 103 and haiku alone in 2 of 103, on different stops; together 0 of 103, with 36 of 47 caught.
const LIVE_MODELS = ['sonnet', 'haiku']
// In T3 a message of JP and a notice that T3 or a mod writes arrive the same way, so the first words tell them apart.
const NOTICE = /^\s*(Delegated task node:|<task-notification>|<system-reminder>|\[Request interrupted|Message from the mod |Stop hook \(the mod |lev mod:|The [a-z-]+ plugin sent a message)/

const PUSH = [
  'Stop hook (the mod continue-approved), not JP. This approves nothing new.',
  // JP 2026-11-17T21:45Z: "we cant assume the plan is correct, it should say continue approved work or return blocked"
  'Continue approved work, or return "blocked".',
  // JP 2026-11-21, about a reply with a bare list of nine questions: "this list of questions one through nine, this is
  // the opposite of the world that I wanted to live in". So the push asks for "For you" items, never for one list.
  'Approved work is a step JP agreed to, or a step inside your own authority that needs no answer from him. A plan you proposed is not approved because you wrote it. If nothing is approved, reply with one line that starts with "blocked:" and names what you wait on. Then write each question for JP as its own "For you" item, in the form of the reply template in ~/.claude/CLAUDE.md: the question, why it matters, the choices, your recommendation and what experts say.',
].join('\n')

// ---- rule 6: a reply to JP has no bare code (JP 2026-11-12: "I don't know what P2 is"; agreed 2026-11-17) ----
// A program settles it. Its own mode, the one word in stop-hook/rule6-mode.txt: off, shadow (the default) or push.
// The same two regular expressions as scripts/reply-checks.mjs: change both, then run scripts/rules56.mjs again.
// Measured 2026-11-17 on 6,473 replies of the chats JP talks in: 885 hold a bare code; 30 of 30 sampled flags were right.
const R6_MODE = `${DIR}/rule6-mode.txt`
const R6_LOG = `${DIR}/rule6-log.tsv`
const R6_MAX = 1   // asks for each message of JP
const CODE = /(?<![\w./#-])([A-Z]{1,3}-?\d{1,4}[a-z]?)(?![\w/-])/g
const KNOWN = new Set(['T3', 'C4', 'UTF-8', 'UTF8', 'STE100', 'SHA-256', 'SHA256', 'SHA-1', 'SHA1', 'ISO-8601', 'H264', 'H265', 'MP4', 'MP3', 'S3', 'M1', 'M2', 'M3', 'M4', 'A4', 'X11', 'CO2', 'K8', 'ES5', 'ES6', 'F5', 'P2P', 'B2B', 'I18', 'V8', 'L1', 'L2', 'L3', 'L4', 'IPV4', 'IPV6', 'G1'])

// A bare code: one to three capital letters and one to four digits ("P2", "M1071", "S4a"). Allowed: in brackets after
// the words it names, in code, in a link.
function bareCodes(text: string): { code: string, near: string }[] {
  const plain = text
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`[^`\n]*`/g, ' ')
    .replace(/\]\([^)\n]*\)/g, ']')
    .replace(/https?:\/\/\S+/g, ' ')
  const out: { code: string, near: string }[] = []
  for (const lineText of plain.split('\n')) {
    for (const m of lineText.matchAll(CODE)) {
      const code = m[1] ?? ''
      const at = m.index ?? 0
      if (KNOWN.has(code.toUpperCase()) || /^GPT-?\d/.test(code)) continue
      const before = lineText.slice(0, at)
      const open = Math.max(before.lastIndexOf('('), before.lastIndexOf('['))
      const close = Math.max(before.lastIndexOf(')'), before.lastIndexOf(']'))
      if (open > close) continue
      out.push({ code, near: lineText.slice(Math.max(0, at - 70), at + code.length + 50).trim() })
    }
  }
  return out
}

// ---- rule 5: the agent opens the file before it says what the file does (agreed 2026-11-17) ----
// The plain case only, settled by a program: a turn JP started made no tool call at all, and the reply speaks of
// code or files. Its own mode word in stop-hook/rule5-mode.txt: off, shadow (the default) or push.
// Measured 2026-11-17: 32 of the 1,249 replies in a turn JP started. Whether a statement in such a reply is wrong
// is not what the check says; it says that nothing was opened in this turn.
const R5_MODE = `${DIR}/rule5-mode.txt`
const R5_LOG = `${DIR}/rule5-log.tsv`
const R5_MAX = 1   // asks for each message of JP
const CODEISH = /\b(?:core|plugins|apps|dna|tooling|docs|src)\/[\w./-]+|`[^`\n]*[./(][^`\n]*`/
let toolsInTurn = 0   // tool calls of the chat's own agent since the turn's first message

// ---- the form of a question to JP (JP 2026-11-21: "The formatting is crazy. What happened to expert opinions") ----
// A program settles it, and this rule only reports: one row for each reply that has a "For you" section or a bare
// list of questions. It holds no stop. Its mode, the one word in stop-hook/for-you-mode.txt: off or shadow (the default).
// The check is for-you-form.mjs beside this file, a copy of ~/.agents/skills/lev-ceo/scripts/for-you-form.mjs: change
// that file, run its tests (tests/for-you-check.test.mjs there), then copy it here.
// Measured 2026-11-21 on 47 saved replies that a reader judged: the check agrees on 41. The six left need judgment:
// a list of questions that is not for JP, and an ask written as prose.
const FY_MODE = `${DIR}/for-you-mode.txt`
const FY_LOG = `${DIR}/for-you-log.tsv`

const FORMAT = '\nOutput one line: the label, then " | ", then the words from the reply that decided it (at most 14 words). Nothing else.'

type Verdict = { label: string, words: string, ms: number, error?: string }

const one = (s: string, n: number) => s.replace(/\s+/g, ' ').trim().slice(0, n)
const readOr = async ($: any, path: string, fallback: string) => ((await $.fs.exists(path)) ? await $.fs.read(path) : fallback)
const fail = async ($: any, where: string, err: unknown) => {
  try { await $.fs.write(ERRORS, `${await readOr($, ERRORS, '')}${new Date(await $.clock.now()).toISOString()} ${where}: ${String(err).slice(0, 300)}\n`) } catch { /* nothing more to try */ }
}

// The same clip for a fixture and for a live reply: the end of a reply holds the plan and the questions.
const clip = (reply: string) => (reply.length <= 9000 ? reply : `${reply.slice(0, 1500)}\n[... ${reply.length - 9000} characters cut ...]\n${reply.slice(-7500)}`)

const ask = (jpBefore: string, startedBy: string, reply: string) =>
  `<jp_last_message>\n${jpBefore.slice(0, 1500) || '(not known)'}\n</jp_last_message>\n\n<turn_started_by>${startedBy === 'jp' ? 'jp' : 'notice'}</turn_started_by>\n\n<agent_reply>\n${clip(reply)}\n</agent_reply>\n\nThe label:`

const rulesText = new Map<string, string>()

async function judge($: any, model: string, jpBefore: string, startedBy: string, reply: string, rulesPath = RULES): Promise<Verdict> {
  const t0 = await $.clock.now()
  if (/^\s*API Error/.test(reply)) return { label: 'not_a_reply', words: 'API Error', ms: 0 }   // a program settles this
  if (!rulesText.has(rulesPath)) rulesText.set(rulesPath, `${await $.fs.read(rulesPath)}${FORMAT}`)
  const r = await $.model.complete({ model, system: rulesText.get(rulesPath), prompt: ask(jpBefore, startedBy, reply), maxTokens: 120, timeoutMs: 45000 })
  const ms = (await $.clock.now()) - t0
  if (!r.isAnswered) return { label: 'no_answer', words: '', ms, error: r.reason }
  const text = r.text.trim()
  const first = text.split('|')[0].toLowerCase()
  const label = LABELS.find(l => first.includes(l)) ?? 'no_label'
  return { label, words: one(text.split('|').slice(1).join('|'), 170), ms }
}

// ---- the replay: the hook's own judge over the fixtures ----
let replayStarted = false

async function replay($: any) {
  if (replayStarted || !(await $.fs.exists(REQUEST))) return
  // `fixtures` and `rules` are file names in the stop-hook folder; left out, the first set and the live rules.
  const req = JSON.parse(await $.fs.read(REQUEST)) as { id: string, models: string[], ids?: string[], fixtures?: string, rules?: string }
  const out = `${DIR}/replay-${req.id}.jsonl`
  const done = `${DIR}/replay-${req.id}.done`
  if (await $.fs.exists(done)) return
  replayStarted = true
  const rulesPath = req.rules ? `${DIR}/${req.rules}` : RULES
  const fixtures = (await $.fs.read(req.fixtures ? `${DIR}/${req.fixtures}` : FIXTURES)).split('\n').filter(Boolean).map((l: string) => JSON.parse(l))
    .filter((f: any) => !req.ids || req.ids.includes(f.id))
  let body: string = await readOr($, out, '')
  const have = new Set(body.split('\n').filter(Boolean).map((l: string) => { const o = JSON.parse(l); return `${o.model} ${o.id}` }))
  const jobs: { model: string, f: any }[] = []
  for (const model of req.models) for (const f of fixtures) if (!have.has(`${model} ${f.id}`)) jobs.push({ model, f })
  const t0 = await $.clock.now()
  for (let i = 0; i < jobs.length; i += 6) {
    const rows = await Promise.all(jobs.slice(i, i + 6).map(async ({ model, f }) => {
      try {
        const v = await judge($, model, f.jp_before, f.turn_started_by ?? 'jp', f.reply, rulesPath)
        return JSON.stringify({ id: f.id, model, ...v })
      } catch (err) {
        return JSON.stringify({ id: f.id, model, label: 'threw', words: '', ms: 0, error: String(err).slice(0, 200) })
      }
    }))
    body += `${rows.join('\n')}\n`
    await $.fs.write(out, body)
  }
  const minutes = (((await $.clock.now()) - t0) / 60000).toFixed(1)
  await $.fs.write(done, `replay ${req.id}: ${jobs.length} calls in ${minutes} minutes\n`)
  void $.prompt.submit({ text: `Message from the mod continue-approved, not from JP: the replay "${req.id}" is done (${jobs.length} judge calls, ${minutes} minutes). The answers are in ${out}.` })
}

// ---- the live hook ----
type Live = { jp_last: string, pushes: number, turn_kind: string, r6_pushes?: number, r5_pushes?: number }

const loadLive = async ($: any): Promise<Live> => JSON.parse(await readOr($, LIVE_STATE, '{"jp_last":"","pushes":0,"turn_kind":""}'))

const logLine = async ($: any, cells: (string | number)[]) => {
  const head = 'at\tmode\tturn_started_by\tbackground_tasks\twake_ups\tanswer_chars\tdecision\tlabel\tms\twords\n'
  await $.fs.write(LIVE_LOG, `${await readOr($, LIVE_LOG, head)}${cells.join('\t')}\n`)
}

// Returns the text to hold the stop with, or undefined to let the turn end.
async function atStop($: any, e: any, mode: string): Promise<string | undefined> {
  const live = await loadLive($)
  const answer: string = e.last_assistant_message ?? ''
  const tasks = (e.background_tasks ?? []).length
  const wakes = (e.session_crons ?? []).length
  const at = new Date(await $.clock.now()).toISOString()
  const row = async (decision: string, label = '', ms = 0, words = '') => { await logLine($, [at, mode, live.turn_kind, tasks, wakes, answer.length, decision, label, ms, words]); return undefined }
  // The quiet cases a program settles.
  if (e.stop_hook_active === true && live.pushes >= MAX_PUSHES) return row(`quiet: ${MAX_PUSHES} pushes since JP's last message`)
  if (answer.trim().length < 40) return row('quiet: no reply text')
  if (tasks > 0) return row('quiet: a background task of this chat still runs and wakes it')
  if (wakes > 0) return row('quiet: a wake-up is set')
  if (live.pushes >= MAX_PUSHES) return row(`quiet: ${MAX_PUSHES} pushes since JP's last message`)
  const all = await Promise.all(LIVE_MODELS.map(m => judge($, m, live.jp_last, live.turn_kind === 'jp' ? 'jp' : 'notice', answer)))
  const labels = all.map((v, i) => `${LIVE_MODELS[i]}=${v.label}${v.error ? `(${v.error})` : ''}`).join(' ')
  const ms = Math.max(...all.map(v => v.ms))
  const words = all.map(v => v.words).join(' || ')
  if (!all.every(v => PUSH_ON.includes(v.label))) return row('quiet: the judges do not both say a plan step is ready', labels, ms, words)
  if (mode !== 'push') return row('would push', labels, ms, words)
  await $.fs.write(LIVE_STATE, JSON.stringify({ ...live, pushes: live.pushes + 1 }))
  await row(`push ${live.pushes + 1} of ${MAX_PUSHES}`, labels, ms, words)
  return PUSH
}

// Rule 6 at the stop. Returns the text to hold the stop with, or undefined.
async function atStopRule6($: any, e: any): Promise<string | undefined> {
  const mode = one(await readOr($, R6_MODE, 'shadow'), 10) || 'shadow'
  if (mode === 'off') return undefined
  const found = bareCodes(e.last_assistant_message ?? '')
  if (found.length === 0) return undefined
  const codes = [...new Set(found.map(f => f.code))]
  const live = await loadLive($)
  const asked = live.r6_pushes ?? 0
  const decision = asked >= R6_MAX ? `quiet: asked ${R6_MAX} time since JP's last message` : mode === 'push' ? 'push' : 'would push'
  const at = new Date(await $.clock.now()).toISOString()
  await $.fs.write(R6_LOG, `${await readOr($, R6_LOG, 'at\tmode\tdecision\tcodes\tnear\n')}${[at, mode, decision, codes.join(' '), one(found[0]?.near ?? '', 160)].join('\t')}\n`)
  if (decision !== 'push') return undefined
  await $.fs.write(LIVE_STATE, JSON.stringify({ ...(await loadLive($)), r6_pushes: asked + 1 }))
  return [
    `Stop hook (the mod continue-approved), not JP. Your reply names things by a bare code: ${codes.slice(0, 12).join(', ')}.`,
    'JP does not know these codes. Reply with one line for each: the code, then what it is in plain words. Do not repeat the rest of the reply.',
  ].join('\n')
}

// Rule 5 at the stop, the plain case. Returns the text to hold the stop with, or undefined.
async function atStopRule5($: any, e: any): Promise<string | undefined> {
  const mode = one(await readOr($, R5_MODE, 'shadow'), 10) || 'shadow'
  if (mode === 'off' || toolsInTurn > 0) return undefined
  const answer: string = e.last_assistant_message ?? ''
  const live = await loadLive($)
  if (live.turn_kind !== 'jp' || answer.length < 200) return undefined
  const m = CODEISH.exec(answer)
  if (m === null) return undefined
  const asked = live.r5_pushes ?? 0
  const decision = asked >= R5_MAX ? `quiet: asked ${R5_MAX} time since JP's last message` : mode === 'push' ? 'push' : 'would push'
  const at = new Date(await $.clock.now()).toISOString()
  await $.fs.write(R5_LOG, `${await readOr($, R5_LOG, 'at\tmode\tdecision\tanswer_chars\tnear\n')}${[at, mode, decision, answer.length, one(answer.slice(Math.max(0, m.index - 80), m.index + 120), 200)].join('\t')}\n`)
  if (decision !== 'push') return undefined
  await $.fs.write(LIVE_STATE, JSON.stringify({ ...(await loadLive($)), r5_pushes: asked + 1 }))
  return [
    'Stop hook (the mod continue-approved), not JP. Your reply speaks of code or files, and this turn opened nothing.',
    'For each statement about what code, a file or data does: open it now and check it. Then reply with the corrections only, or with one line: checked, no change.',
  ].join('\n')
}

// The form rule at the stop. It writes its row and returns nothing: it never holds the stop.
async function atStopForYou($: any, e: any): Promise<void> {
  const mode = one(await readOr($, FY_MODE, 'shadow'), 10) || 'shadow'
  if (mode === 'off') return
  const answer: string = e.last_assistant_message ?? ''
  const found = checkForYouForm(answer)
  if (found.for_you_items === 0 && found.faults.length === 0) return
  const live = await loadLive($)
  const at = new Date(await $.clock.now()).toISOString()
  const faults = found.faults.map(f => (f.fault === 'bare_list' ? `bare_list(${f.count})` : `item_incomplete(${(f.missing ?? []).join(', ')})`))
  const head = 'at\tturn_started_by\tanswer_chars\tfor_you_items\tfaults\tnear\n'
  await $.fs.write(FY_LOG, `${await readOr($, FY_LOG, head)}${[at, live.turn_kind, answer.length, found.for_you_items, faults.join('; ') || 'none', one(found.faults[0]?.first ?? '', 120)].join('\t')}\n`)
}

export const register: Register = on => {
  // Count the tool calls of the chat's own agent, for rule 5.
  on('tool.call', async ($, e, next) => {
    if (e.agentId === undefined) toolsInTurn += 1
    return next(e)
  })

  on('session.start', async ($, e, next) => {
    const result = await next(e)
    $.clock.after(1500, () => { void replay($).catch(err => fail($, 'replay', err)) })
    return result
  })

  // Remember JP's last message, and who started the turn that runs now. The start of a turn carries the text for
  // every way in; a prompt.submit hook did not hear a prompt that a mod submitted (seen 2026-11-17).
  on('turn.start', async ($, e, next) => {
    const result = await next(e)
    if (e.agentId !== undefined || e.text.trim() === '') return result   // a helper agent's turn, or a turn that goes on
    toolsInTurn = 0
    try {
      const live = await loadLive($)
      await $.fs.write(LIVE_STATE, JSON.stringify(NOTICE.test(e.text)
        ? { ...live, turn_kind: 'notice' }
        : { jp_last: e.text.slice(0, 1500), pushes: 0, turn_kind: 'jp' }))
    } catch (err) { await fail($, 'turn.start', err) }
    return result
  })

  // The stop itself. A subagent's stop is another event, so this is the chat's own agent.
  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    void replay($).catch(err => fail($, 'replay', err))
    try {
      const mode = one(await readOr($, MODE, 'shadow'), 10) || 'shadow'
      if (e.agent_id !== undefined) return result
      if (result.block !== undefined || result.preventContinuation === true) return result   // another hook already ruled
      // Shadow waits for the judge too (about 3 s): a reload of the mod would stop a judge left behind, and the wait is the one push mode has.
      const hold = mode === 'off' ? undefined : await atStop($, e, mode)
      const fix = await atStopRule6($, e)
      const look = await atStopRule5($, e)
      try { await atStopForYou($, e) } catch (err) { await fail($, 'for-you', err) }   // it only reports, so its fault costs no other rule
      const texts = [mode === 'push' ? hold : undefined, fix, look].filter((t): t is string => t !== undefined)
      return texts.length === 0 ? result : { ...result, block: texts.join('\n\n') }
    } catch (err) { await fail($, 'classic.Stop', err); return result }
  })
}
