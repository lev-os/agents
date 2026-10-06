# Declarative data plus an interpreter (code as data)

**Plain words:** describe *what* should happen in data (YAML, JSON, a small language); one engine reads that data and does it. New behavior is new data, not new code.

## Fits when
- Many variants differ only in values and wiring (flows, gates, entity kinds, profiles).
- Non-programmers or agents author behavior, and a validator must check it before it runs.
- You want to analyze behavior before executing it (lint, diff, dry run, compile to another target).

## Hurts when
- The data grows conditionals, loops and variables: you built a bad programming language in YAML.
- Errors point at the engine, not at the line of data that caused them.
- Only one variant exists; a function was enough.

## Cost
- Lines: schema + engine (large, once) then tiny per variant.
- Concepts: 3 (schema, interpreter, compile vs interpret). The engine is the deep module; the data must stay shallow.

## Tiny example
```ts
const flow = { steps: [{ op: 'read', path: 'task.yaml' }, { op: 'check', id: 'has_owner' }] } as const;
type Step = (typeof flow.steps)[number];
const ops = {
  read: async (s: Extract<Step, { op: 'read' }>) => fs.readFile(s.path, 'utf8'),
  check: async (s: Extract<Step, { op: 'check' }>) => runCheck(s.id),
};
for (const s of flow.steps) await (ops[s.op] as (x: Step) => Promise<unknown>)(s);
```

## Pairs with / fights
- Pairs: parse-dont-validate (schema first), pipes-and-filters (compile stages), state-machines (a machine is data), convention-over-configuration.
- Fights: ad hoc scripts with the same logic; two interpreters for one format (split-brain).

## In Lev
The ratchet thesis: code is an artifact of Lev IR (`dna/thesis.yaml`). FlowMind compiles `*.flow.yaml` once into a flow graph; `config.yaml` is FlowMind. AGENTS.md "skills before flows": test as a skill by hand before paying for a flow.

Sources: Harold Abelson and Gerald Sussman, *SICP* ch. 4 (1985); Martin Fowler, *Domain-Specific Languages* (2010).
