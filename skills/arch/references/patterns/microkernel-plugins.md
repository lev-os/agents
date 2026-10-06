# Microkernel and plugin architecture

**Plain words:** a small core provides the extension points and the rules; features arrive as plugins that register against those points. The core never imports a plugin.

## Fits when
- Third parties or later sessions add features without editing the core.
- Features vary by project and must be switched on and off.
- One capability must reach many surfaces (CLI, MCP, HTTP) through one registry.

## Hurts when
- The extension points are guessed before two real plugins exist; you freeze the wrong API.
- Plugins import each other; the "kernel" is now a dependency hairball.
- The kernel grows to hold every shared helper (dumping ground).

## Cost
- Lines: registry plus a declared plugin contract (config + handler shape).
- Concepts: 3 (kernel, extension point, plugin contract) plus discovery and versioning.

## Tiny example
```ts
// plugin: plugins/hello/src/handlers/greet.js
export async function handler(args: { name: string }) { return { text: `hi ${args.name}` }; }

// kernel: registry built from discovery, surfaces project it
const registry = new Map<string, (a: unknown) => Promise<unknown>>();
for (const op of discoverHandlers()) registry.set(op.id, op.handler);
export const call = (id: string, args: unknown) => registry.get(id)?.(args);
```

## Pairs with / fights
- Pairs: convention-over-configuration (discovery), ports-and-adapters (plugins implement ports), capability-based (plugins get only granted ports), modular-monolith.
- Fights: shared mutable state between plugins; cross-plugin imports.

## In Lev
`plugins/*` (~56) with `src/handlers/*.js` exporting `handler`; no cross-plugin imports, no barrel re-exports; shared contracts move to `core/domain`/`core/utils` (AGENTS.md). Poly projects one handler onto every surface. `dna/plugin-contract.dna.yaml` is the plugin contract.

Sources: Buschmann et al., *POSA vol. 1* (1996), "Microkernel"; Mark Richards, *Software Architecture Patterns* (O'Reilly, 2015).
