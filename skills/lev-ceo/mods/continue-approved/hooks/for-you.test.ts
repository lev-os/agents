// The form rule of the stop hook (JP 2026-11-21, about a reply with a bare list of nine questions: "The formatting is
// crazy. What happened to expert opinions"). It only reports: one row for each reply that has a "For you" section or
// a bare list of questions, and it never holds the stop. Run: claude plugin test <the mod's folder>
import { expect, mock, test } from 'claude-code/testing'

const DIR = '/Users/jean-patricksmith/.local/state/lev/ceo/lost-time/stop-hook'
const LOG = `${DIR}/for-you-log.tsv`

// The stop-hook folder in memory, so a test reads and writes no file on disk. The mode word of the judge is `off`:
// no model is called.
const folder = (on: any, more: Record<string, string> = {}) => {
  const files: Record<string, string> = { [`${DIR}/mode.txt`]: 'off', [`${DIR}/rule6-mode.txt`]: 'off', [`${DIR}/rule5-mode.txt`]: 'off', ...more }
  on('fs.exists', (_: unknown, e: { path: string }) => ({ value: e.path in files }))
  on('fs.read', (_: unknown, e: { path: string }) => ({ value: files[e.path] ?? '' }))
  on('fs.write', (_: unknown, e: { path: string, text: string }) => { files[e.path] = e.text; return { value: undefined } })
  on('classic.Stop', () => ({}))   // the engine's own answer: the turn ends
  mock.clock(on, { now: Date.UTC(2026, 10, 21, 12, 0, 0) })
  return files
}

const BARE = [
  'The run is done, and the three checks pass. I need two calls from you before the next step:',
  '',
  '1. **How much of Lev do we freeze before the release?** A: all of it. B: only the daemon.',
  '2. **Who signs the build?** A: you. B: the machine.',
].join('\n')

const FULL = [
  'The run is done, and the three checks pass.',
  '',
  '**For you:**',
  '1. **Is the design the one to build from?**',
  '  It is the base of every later step.',
  '  - **I recommend yes**, because a reader checked it twice.',
  '  - **What 2 design experts say:**',
  '    - Malte Ubl: a design is reviewed before the build starts.',
  '    - Ryan Singer: shape the work, then bet on it.',
].join('\n')

test('a reply with a bare list of questions gets a row, and the stop is not held', async ($, on) => {
  const files = folder(on)
  const result = await $.classic.Stop({ stop_hook_active: false, last_assistant_message: BARE })
  expect(files[LOG] ?? '').toContain('bare_list(2)')
  expect(files[LOG] ?? '').toContain('2026-11-21T12:00:00.000Z')
  expect(result.block).toBeUndefined()
})

test('a "For you" item with all its parts gets a row that names no fault', async ($, on) => {
  const files = folder(on)
  await $.classic.Stop({ stop_hook_active: false, last_assistant_message: FULL })
  const rows = (files[LOG] ?? '').trim().split('\n')
  expect(rows.length).toBe(2)   // the header and one row
  expect(rows[1]?.split('\t').slice(3, 5)).toEqual(['1', 'none'])
})

test('an item with no expert lines gets a row that names the missing part', async ($, on) => {
  const files = folder(on)
  await $.classic.Stop({ stop_hook_active: false, last_assistant_message: FULL.split('\n').slice(0, 6).join('\n') })
  expect(files[LOG] ?? '').toContain('item_incomplete(expert lines)')
})

test('a reply with no question for JP gets no row', async ($, on) => {
  const files = folder(on)
  await $.classic.Stop({ stop_hook_active: false, last_assistant_message: 'The run is done, and the three checks pass. Nothing waits on you.' })
  expect(LOG in files).toBe(false)
})

test('with the mode word off the rule writes nothing', async ($, on) => {
  const files = folder(on, { [`${DIR}/for-you-mode.txt`]: 'off\n' })
  await $.classic.Stop({ stop_hook_active: false, last_assistant_message: BARE })
  expect(LOG in files).toBe(false)
})
