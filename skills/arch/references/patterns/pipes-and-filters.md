# Pipes and filters (typed pipeline stages)

**Plain words:** a job is a chain of small steps; each takes one typed input and returns one typed output. Steps know nothing of each other; the pipeline wires them.

## Fits when
- Compilers, loaders and resolvers: find → read → parse → normalize → validate → emit.
- You want to test, cache or skip a stage on its own.
- Intermediate results are useful to inspect (dry runs, debug dumps).

## Hurts when
- Stages need to share lots of context; you end up passing a god "context" object through every filter.
- Control flow branches heavily back and forth; it is a state machine, not a pipe.
- Ten one-line stages: a function with ten lines is clearer.

## Cost
- Lines: one type per stage boundary, one function per stage.
- Concepts: 2 (stage, pipeline). Streaming variants add backpressure.

## Tiny example
```ts
const pipeline = <A>(a: A) => ({ then: <B>(f: (a: A) => B) => pipeline(f(a)), value: a });

const catalog = pipeline(rootDir)
  .then(findFractalRoots)   // string -> Root[]
  .then(collectOwns)        // Root[] -> Claim[]
  .then(rejectConflicts)    // Claim[] -> Claim[] (throws on two owners)
  .then(scanOnce).value;    // Claim[] -> Catalog
```

## Pairs with / fights
- Pairs: functional-core (pure stages), parse-dont-validate (first stage parses), result-types (stages return Result), declarative-interpreter (compile pipeline).
- Fights: actor-model for the same job; pick one shape per job.

## In Lev
The fractal resolver is a pipeline: find fractal roots, collect `owns:`, reject conflicts, scan once, hand each owner its files (AGENTS.md reducer). `typed_pipeline_stages` is in `code-quality.yaml#pattern_playbook`. FlowMind compiles once; consumers cannot walk its AST (`core-boundaries/concept.yaml#flowmind_compilation`).

Sources: Frank Buschmann et al., *Pattern-Oriented Software Architecture vol. 1* (1996); Doug McIlroy, Unix pipes (1964 memo, 1973).
