export const meta = {
  name: 'state-machine-audit',
  description: 'Find every implicit state machine in an app (read-only), verify the riskiest claims, group them into families',
  whenToUse: 'The review skill state machine audit, for a whole app. Args: {areas?: [{key, scope}], since?: git ref, repo?: path}',
  phases: [
    { title: 'Scout', detail: 'propose areas when none are given' },
    { title: 'Find', detail: 'one finder per area, several search ways' },
    { title: 'Check', detail: 'completeness critic: search by content, merge, drop, reread risky claims' },
  ],
}

const A = args || {}
const REPO = A.repo || 'the current working directory'
const SINCE = A.since ? `Look only at files changed since git ref ${A.since} (git diff --name-only ${A.since}...HEAD), plus the files that read or write the same states.` : ''
const RO = `READ-ONLY TASK in ${REPO}. Do not edit, create, stage or commit any file. Do not run full test suites. When a code graph tool (codebase-memory-mcp) has this repo, use it, and confirm with grep and Read. Cite every claim as path:line. Skip node_modules, dist, build output, archives and worktrees. ${SINCE}`

const DEF = `Read ~/.agents/skills/review/references/state-machines.md, sections "What counts" and "Questions for each machine", and use them exactly.`

const MACHINE = {
  type: 'object',
  properties: {
    name: { type: 'string', description: 'plain name, e.g. "a flow run"' },
    evidence: { type: 'array', items: { type: 'string' }, description: 'path:line for definition, writes and reads' },
    package: { type: 'string' },
    states: { type: 'array', items: { type: 'string' } },
    known_transitions: { type: 'array', items: { type: 'string' }, description: 'from -> to (trigger)' },
    encoding: { type: 'string', description: 'string-union | enum | boolean-cluster | loose-strings | yaml | mixed' },
    persisted: { type: 'boolean' },
    crosses_boundary: { type: 'boolean' },
    duplicates_of: { type: 'array', items: { type: 'string' } },
    illegal_moves_possible: { type: 'string', description: 'a concrete illegal move the code does not stop, with path:line, or "none found"' },
    ux: { type: 'string' },
    dx: { type: 'string' },
    ax: { type: 'string' },
    change_risk: { type: 'string', enum: ['low', 'medium', 'high'] },
  },
  required: ['name', 'evidence', 'package', 'states', 'encoding', 'persisted', 'crosses_boundary', 'illegal_moves_possible', 'ux', 'dx', 'ax', 'change_risk'],
}

const FINDINGS = {
  type: 'object',
  properties: {
    implicit: { type: 'array', items: MACHINE },
    already_explicit: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, evidence: { type: 'string' }, mechanism: { type: 'string' } }, required: ['name', 'evidence', 'mechanism'] } },
    searched: { type: 'array', items: { type: 'string' } },
    not_covered: { type: 'array', items: { type: 'string' } },
  },
  required: ['implicit', 'already_explicit', 'searched', 'not_covered'],
}

phase('Scout')
let areas = Array.isArray(A.areas) && A.areas.length ? A.areas : null
if (!areas) {
  const scout = await agent(`${RO}

List the top-level folders of this repo that hold source code, and split them into 3 to 6 areas of about equal size for state machine finders. Put runtime code (jobs, runs, daemons, queues), the data model and records, plugins or extensions, and apps with UI in different areas when they exist.`, {
    label: 'scout', phase: 'Scout',
    schema: { type: 'object', properties: { areas: { type: 'array', items: { type: 'object', properties: { key: { type: 'string' }, scope: { type: 'string' } }, required: ['key', 'scope'] } } }, required: ['areas'] },
  })
  areas = (scout && scout.areas) || []
}
log(`${areas.length} areas: ${areas.map(a => a.key).join(', ')}`)

phase('Find')
const found = (await parallel(areas.map(a => () => agent(`${RO}

${DEF}

Your area: ${a.scope}.
Find every implicit state machine in this area. Search several ways: (1) by name: fields and types named status|state|phase|stage|mode|lifecycle|step; (2) by content: switch, === or includes on string literals like 'pending','running','done','failed','queued','active','blocked','idle','error','ready','draft','closed'; (3) boolean groups (isLoading, isError, isDone, started, finished); (4) stored records: which status strings are written to files, databases, logs or receipts; (5) readers of those strings in other packages.
Merge sites that are the same machine into one entry with all evidence. Prefer fewer, well-evidenced entries; do not drop a real machine.`, { label: `find:${a.key}`, phase: 'Find', schema: FINDINGS })))).filter(Boolean)

log(`Finders returned ${found.flatMap(r => r.implicit).length} candidates`)

phase('Check')
const checked = await agent(`${RO}

${DEF}

Area finders returned (JSON):
${JSON.stringify(found)}

As the completeness critic:
1. Search the whole repo BY CONTENT (status string literals, "status:" and "state:" type unions), not by folder. Add machines the finders missed, with evidence.
2. Merge entries that are the same machine seen from different packages; the merged entry lists every site and sets crosses_boundary.
3. Drop entries that are not machines; say why in "dropped".
4. Reread the code for the 5 highest-risk illegal_moves_possible claims; mark each confirmed or not.
5. Group the machines into families that should share one definition.`, {
  label: 'completeness-critic', phase: 'Check',
  schema: {
    type: 'object',
    properties: {
      machines: { type: 'array', items: MACHINE },
      families: { type: 'array', items: { type: 'object', properties: { family: { type: 'string' }, members: { type: 'array', items: { type: 'string' } }, why: { type: 'string' } }, required: ['family', 'members', 'why'] } },
      dropped: { type: 'array', items: { type: 'string' } },
      spot_checks: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, confirmed: { type: 'boolean' }, evidence: { type: 'string' } }, required: ['claim', 'confirmed', 'evidence'] } },
      gaps: { type: 'array', items: { type: 'string' } },
    },
    required: ['machines', 'families', 'dropped', 'spot_checks', 'gaps'],
  },
})

return { areas, inventory: checked, raw_counts: found.map(r => r.implicit.length), already_explicit: found.flatMap(r => r.already_explicit) }
