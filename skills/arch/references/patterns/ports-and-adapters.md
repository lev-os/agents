# Ports and adapters (hexagonal)

**Plain words:** the app talks to the outside only through interfaces it owns (ports); each technology plugs in behind one (adapter). Tests, CLI and daemon are just more adapters.

## Fits when
- A volatile outside thing (provider CLI, file system, model API, tmux) sits under stable rules.
- You need a fake for tests and a real one for production behind the same contract.
- Two or more real implementations exist or are certain soon.

## Hurts when
- One implementation forever: the port is an interface with one implementer, pure indirection.
- The port mirrors the vendor API one-to-one (a "leaky port"); you pay the cost and still couple.
- Every call site gets its own port; the app turns into a maze of tiny interfaces.

## Cost
- Lines: one interface plus one adapter per outside thing (~15-40 lines).
- Concepts: 2 (port, adapter). Owner of the port is the consumer, not the vendor.

## Tiny example
```ts
// port, owned by the core that needs it
export interface FilePort {
  read(path: string): Promise<string>;
  write(path: string, body: string, expectedHash?: string): Promise<void>;
}
// adapter at the edge
export const localFileAdapter: FilePort = {
  read: (p) => fs.readFile(p, 'utf8'),
  write: (p, b) => fs.writeFile(p, b),
};
```

## Pairs with / fights
- Pairs: dependency-injection (how adapters get in), functional-core (shell = adapters), capability-based (a port reference is an authority).
- Fights: convention-over-configuration when discovery hides which adapter is live; clean-architecture's extra rings if both are applied in full.

## In Lev
Hex canon: `*Port`/`*Adapter` naming (AGENTS.md conventions). `core/file` ships `FilePort` + `LocalFileAdapter`; `core/reconciler` is "pure, ports-injected" (`dna/index.yaml` catalog). `code-quality.yaml#core_adapter_breach` is the smell this pattern fixes.

Source: Alistair Cockburn, "Hexagonal Architecture" (2005), alistaircockburn.com/Articles/Hexagonal-Architecture.
