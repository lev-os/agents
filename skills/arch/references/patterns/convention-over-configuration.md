# Convention over configuration (discovery by place and name)

**Plain words:** where a file lives and what it is named decide what it does. Put a handler in `src/handlers/` and it becomes an operation; no registry entry to write.

## Fits when
- Many similar things get added often (handlers, flows, entity folders).
- Hand-maintained registries keep drifting from the files.
- A newcomer should guess where something goes and be right.

## Hurts when
- Magic: a file has behavior nobody can find by grepping a call site.
- Two conventions claim one folder; load order silently picks a winner.
- The convention covers 80% and the other 20% grow ad hoc config flags.

## Cost
- Lines: negative for users (no registration); one scanner plus a collision check, once.
- Concepts: 2 (convention, discovery) plus an escape hatch that must stay small.

## Tiny example
```ts
// scanner: owner declares which folder names it owns; collisions are build errors
const owns = { poly: ['src/handlers'], flowmind: ['flows'] };
for (const [owner, dirs] of Object.entries(owns))
  for (const d of dirs) if (claimed.has(d)) throw new Error(`${d}: ${claimed.get(d)} vs ${owner}`);
    else claimed.set(d, owner);
```

## Pairs with / fights
- Pairs: microkernel-plugins (discovery), declarative-interpreter, vertical-slice (folder = feature).
- Fights: dependency-injection when discovery also picks implementations; make discovery find *what exists* and the composition root choose *what is wired*.

## In Lev
Fractal ownership: a module declares `owns:` folder names; two owners of one name is a build error, load order never decides (AGENTS.md reducer). Operations are found from `src/handlers`, never hand-declared. Today the owner groups are hard-coded in `core/config/src/source-catalog.ts` (gap until the `owns:` reader lands).

Sources: David Heinemeier Hansson, Rails doctrine "Convention over Configuration" (rubyonrails.org/doctrine, 2016).
