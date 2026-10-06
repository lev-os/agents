# Domain-driven design, tactical (entities, value objects, aggregates, bounded contexts)

**Plain words:** model the business with types that carry identity (entity), types defined only by their value (value object), and a root that guards a cluster's rules (aggregate). Each model is valid inside one bounded context with one vocabulary.

## Fits when
- Rules span several objects ("a task cannot complete while a child is open").
- The same word means different things in different modules (needs a context line).
- Invalid states keep slipping in through ad hoc writes.

## Hurts when
- Data is just passed through; entities become getter bags ("anemic") with ceremony.
- Aggregates are drawn too big: every write locks the world, every test builds the world.
- Repositories, factories and domain services are added by template, not by need.

## Cost
- Lines: value objects are tiny; aggregates add a write path that must go through the root.
- Concepts: 4-5 (entity, value object, aggregate, bounded context, ubiquitous language). Use the first three plus contexts; skip the rest until forced.

## Tiny example
```ts
type Stage = 'captured' | 'crystallized' | 'manifesting' | 'completed';
export class Workstream {               // aggregate root
  private constructor(readonly id: string, private tasks: Map<string, Stage>) {}
  complete(taskId: string): Workstream {
    if (this.tasks.get(taskId) !== 'manifesting') throw new Error('not running');
    return new Workstream(this.id, new Map(this.tasks).set(taskId, 'completed'));
  }
}
```

## Pairs with / fights
- Pairs: clean-architecture (domain at the center), state-machines (aggregate transitions), parse-dont-validate (value objects are parsed values), event-sourcing (aggregate emits events).
- Fights: vertical-slice when a slice wants to mutate the aggregate's internals; CRUD screens.

## In Lev
Workstreams are the aggregate root (`.lev/pm/workstreams/<id>/state/workstream.yaml`, AGENTS.md). Bounded contexts: one concern, one owning package (`core-boundaries/concept.yaml#bounded_context_owner`). Vocabulary discipline is the ubiquitous-language rule (`dna/vernacular.yaml`). Gate A→M miss = missing bounded context (failure mode 8).

Sources: Eric Evans, *Domain-Driven Design* (2003); Vaughn Vernon, *Implementing DDD* (2013), "Effective Aggregate Design".
