# Lev Architecture Primer

> Auto-generated reference. All lev-* skills should @import this file.
> Regenerate: run the bash commands in the source prompt against `~/lev/`.
> Last generated: 2026-03-27

---

## Core Module Layout

```
~/lev/core/
├── build
├── config
├── daemon
├── domain          ← shared vocabulary, types, contracts
├── event-bus
├── event-machines
├── event-providers
├── exec            ← execution engine
├── flowmind
├── graph
├── harness         ← agent execution adapters (SDK, CLI, API)
├── index           ← LEANN semantic vector search
├── logger
├── memory
├── orchestration   ← A2A job dispatch
├── plugin-manager
├── poly            ← surface multiplexer (CLI, MCP, HTTP, gRPC, WS)
├── storage
├── telemetry
└── ui
```

## Plugin Layout

```
~/lev/plugins/
├── _archive                ├── genui-exec-daemon       ├── reasoning-enhance
├── auth-sniffer            ├── graph-adapters           ├── slate
├── beads                   ├── guardrails               ├── strands-tools
├── browser-cascade         ├── hello-world              ├── timetravel
├── claw-router             ├── mastra                   ├── token-compress
├── code-graph              ├── notion                   ├── validator
├── codex                   ├── osint                    ├── vision
├── context-compress        ├── platforms                ├── voice
├── core-autoresearch       ├── prompt-stack             ├── wiggum-marketer
├── core-bench              ├── publisher                ├── workflow-orchestrator
├── core-context            ├── deploy                   └── workshop
├── core-gameai             ├── dna
├── core-harness-patterns   ├── erc
├── core-platforms          ├── evolve-memory
├── core-reactive           ├── gemini-executor
├── core-scheduling         ├── defendr
├── core-sdlc               ├── writer
└── core-timetravel         └── core-workshop
```

## Domain Exports (Shared Vocabulary)

Source: `~/lev/core/domain/src/index.ts`

```typescript
export { Route } from './route.js';
export { Target, TargetType } from './target.js';
export { FractalOwner } from './fractal-owner.js';
export { FractalEntry } from './fractal-entry.js';
export { Manifest } from './manifest.js';
export { type LevPhase, type LevOutcome, type LevStatus, levStatus } from './status.js';
export * from './event-source.js';
export * from './dor.js';
export * from './validation.js';
export * from './harness.js';
export * from './daemon-adapter.js';
export * from './telemetry-types.js';
export * from './cron.js';
export * from './hooks.js';
export * from './exec-events.js';
export * from './execution-protocol.js';
export { INTEGRATION_POINTS } from './validation.js';
export type { SpanLike, TracerLike } from './telemetry-types.js';
```

---

## Key Patterns

### ProtocolAdapter\<TExternal, TInternal\>

Source: `~/lev/core/domain/src/protocol-adapter.ts`

Pure-function bridge between external protocol conventions and internal domain model. Handles naming convention mismatches (e.g., `costUSD` vs `costUsd`).

```typescript
export interface ProtocolAdapter<TExternal = unknown, TInternal = unknown> {
  /** Protocol identifier (e.g., 'openai', 'anthropic', 'ollama') */
  readonly protocol: string;

  /** Transform external protocol format to internal domain model */
  toInternal(external: TExternal): TInternal;

  /** Transform internal domain model to external protocol format */
  toExternal(internal: TInternal): TExternal;
}
```

No IO, no side effects. Each adapter maps a single protocol.

### ExecTransport (DI pattern)

Source: `~/lev/core/domain/src/execution-protocol.ts`

Domain defines the contract; poly provides the implementation. This breaks the circular dependency: both depend on domain, not each other.

```typescript
export interface ExecutionRunRequest {
  operation: string;
  input: Record<string, unknown>;
  config?: Record<string, unknown>;
  target?: {
    surface?: string;
    capability?: string;
    version?: string;
    options?: Record<string, string>;
  };
  timeoutMs?: number;
}

export interface ExecutionRunResponse {
  status: 'EXECUTION_STATUS_SUCCEEDED' | 'EXECUTION_STATUS_FAILED' | 'EXECUTION_STATUS_TIMEOUT';
  output?: Record<string, unknown>;
  usage?: { input_tokens?: number; output_tokens?: number; total_tokens?: number; runtime_ms?: number; };
  error?: { code: string; message: string; };
}

export interface ExecTransport {
  call<T = unknown>(providerName: string, method: string, ...): Promise<T>;
  executeHandler(handler, command, ctx, options): Promise<...>;
  runExecutionRequest(request: ExecutionRunRequest): Promise<ExecutionRunResponse>;
}
```

### Route / Target (lev:// URI scheme)

Source: `~/lev/core/domain/src/route.ts`, `~/lev/core/domain/src/target.ts`

**Route** — immutable value object representing a parsed `lev://` URI:

```typescript
export class Route {
  constructor(
    public readonly uri: string,     // 'lev://memory/commands/store'
    public readonly module: string,  // 'memory'
    public readonly fractal: string, // 'commands'
    public readonly item: string     // 'store'
  ) { ... }

  static parse(uri: string): Route;
  toNamespaced(): string; // 'memory:store'
}
```

**Target** — user input before resolution to a Route. Determines resolution strategy:

```typescript
export enum TargetType {
  URI = 'uri',           // lev://module/fractal/item
  NAMESPACED = 'namespaced', // module:item
  PATH = 'path',         // module/fractal/item or module/item
  BARE = 'bare',         // just 'store' (requires manifest search)
}

export class Target {
  constructor(input: string); // auto-detects TargetType
  readonly type: TargetType;
}
```

### A2A Job Dispatcher

Source: `~/lev/core/orchestration/src/a2a/types.ts`

Structured types for dispatching work between agents. Replaces ad-hoc spawnSync patterns.

```typescript
export type AgentJobStatus =
  | 'queued' | 'running' | 'completed' | 'failed' | 'cancelled' | 'timed_out';

export interface AgentJob {
  id: string;
  prompt: string;
  inputs?: Record<string, unknown>;
  inputFiles?: string[];
  timeoutMs?: number;
  budgetTokens?: number;
  agentType?: string;                   // dispatch routing hint
  isolation?: 'main' | 'worktree';      // branch vs isolated worktree
}
```

### ProcessHarness (owned spawn primitive)

Source: `~/lev/core/harness/src/process-harness.ts`

Unified interface for spawning and controlling interactive CLI processes. Two implementations:

```typescript
export interface ProcessHarness {
  spawn(cmd: string, args: string[], opts?: SpawnOpts): Promise<Session>;
  send(session: Session, input: string): Promise<void>;
  capture(session: Session, opts?: { ... }): AsyncGenerator<OutputChunk>;
  kill(session: Session): Promise<void>;
}

export class TmuxHarness implements ProcessHarness { ... }
export class NodePtyHarness implements ProcessHarness { ... }

export function createHarness(mode?: 'tmux' | 'pty' | 'auto'): ProcessHarness;
export function createHarnessWithCleanup(mode?: 'tmux' | 'pty' | 'auto'): ProcessHarness;
```

### AdapterRegistry

Source: `~/lev/core/harness/src/providers/registry.ts`

Centralized registration and selection of agent adapters with model compatibility validation.

```typescript
export interface AgentAdapter { ... }
export type AdapterFactory = (config?: AdapterConfig) => AgentAdapter;

export class AdapterRegistry { ... }

export function registerAdapter(name: string, factory: AdapterFactory): void;
export function setAdapterCompatibility(name: string, prefixes: string[]): void;
export function getAdapterCompatibility(name: string): string[] | undefined;
```

Available adapters (from `~/lev/core/harness/src/providers/`):

- `ai-sdk.ts`
- `claude-agent-sdk.ts` (DEFAULT)
- `cursor.ts`
- `deer-flow.ts`
- `opencode.ts`
- `pi.ts`

Plus: `interface.ts`, `registry.ts`, `usage-mapper.ts`, `promise-detection.test.ts`, `registry.test.ts`, `claude-agent-sdk.test.ts`

---

## DNA Contracts

Three contract files in `~/lev/dna/`:

### core-contract.dna.yaml

> Behavioral contract for any `core/` module. Stricter than plugin-contract.

| ID | Enforcement |
|----|-------------|
| `has_package` | gate |
| `namespace_is_lev` | gate |
| `has_spec` | gate |
| `has_config` | gate |
| `no_plugin_imports` | gate |
| `no_sibling_state_mutation` | guard |
| `levevent_only` | aspirational |
| `no_commands_dir` | aspirational |
| `no_barrel_reexports` | aspirational |
| `xdg_compliant` | gate |
| `export_typed_api` | (behavior) |
| `validate_against_spec` | (behavior) |
| `emit_lifecycle_events` | (behavior) |
| `declare_config_surface` | (behavior) |
| `missing_spec` | (failure mode) |
| `plugin_dependency` | (failure mode) |
| `legacy_path` | (failure mode) |

### plugin-contract.dna.yaml

> Behavioral contract for any Lev plugin. DNA compiler turns constraints into executable gate nodes.

| ID | Enforcement |
|----|-------------|
| `has_package` | gate |
| `type_is_plugin` | gate |
| `namespace_is_lev` | gate |
| `has_integration` | gate |
| `has_capabilities` | gate |
| `coupling_declared` | guard |
| `flowmind_paths_valid` | gate |
| `flowmind_triggers_declared` | aspirational |
| `poly_surfaces_have_command` | gate |
| `no_commands_dir` | aspirational |
| `no_barrel_reexports` | aspirational |
| `no_core_imports` | gate |
| `xdg_compliant` | gate |
| `register_at_install` | (behavior) |
| `declare_fractal_surface` | (behavior) |
| `validate_on_load` | (behavior) |
| `discover_flowmind_programs` | (behavior) |
| `expose_poly_surfaces` | (behavior) |
| `emit_lifecycle_events` | (behavior) |
| `missing_package` | (failure mode) |
| `wrong_type` | (failure mode) |
| `missing_integration` | (failure mode) |
| `flowmind_path_missing` | (failure mode) |
| `cross_plugin_import` | (failure mode) |
| `legacy_path_write` | (failure mode) |

### validate-chain.dna.yaml

> Meta-DNA for the ValidatorChain itself. The chain validates itself.

| ID | Enforcement |
|----|-------------|
| `composable` | gate |
| `contract_aware` | gate |
| `detect_contract` | (step) |
| `structural_validation` | (step) |
| `compile_contract` | (step) |
| `validate_topology` | (step) |
| `eval_constraints` | (step) |
| `emit_report` | (step) |
| `missing_contract` | (failure mode) |
| `compile_failure` | (failure mode) |

**Enforcement levels:**
- **gate** — hard failure, blocks build/install/load
- **guard** — warning, logged, does not block
- **aspirational** — future goal, tracked but not enforced

---

## Poly Surfaces

```
~/lev/core/poly/src/surfaces/
├── cli/     ← Commander-based CLI (discovery.ts scans handlers)
├── grpc/    ← gRPC protocol surface
├── http/    ← HTTP/REST surface
├── mcp/     ← Model Context Protocol surface
└── ws/      ← WebSocket surface
```

## Harness Adapters

```
~/lev/core/harness/src/providers/
├── ai-sdk.ts                    ← Vercel AI SDK adapter
├── claude-agent-sdk.ts          ← Claude Agent SDK (DEFAULT)
├── claude-agent-sdk.test.ts
├── cursor.ts                    ← Cursor editor adapter
├── deer-flow.ts                 ← HTTP-based research agent
├── index.ts
├── interface.ts                 ← AgentAdapter base interface
├── opencode.ts                  ← OpenCode adapter
├── pi.ts                        ← Pi agent adapter
├── promise-detection.test.ts
├── registry.ts                  ← AdapterRegistry class
├── registry.test.ts
└── usage-mapper.ts              ← Token usage normalization
```

## Registry Structure

Source: `~/lev/core/poly/registry.yaml`

```yaml
version: '2.0'
binaries:
  watch:
    binary: lev-watch
    platforms: [darwin-arm64, darwin-x64, linux-x64, windows-x64]
    source: core/poly/binaries/lev-watch
    type: go
    description: Native file watcher with gitignore support
  kernel:
    binary: lev-kernel
    platforms: [darwin-arm64, linux-x64]
    source: os/kernel
    type: go
    description: Telemetry pattern detection
    websocket: ws://localhost:8081/patterns
  serena:
    binary: uvx
    type: python-uvx
    description: LSP symbol navigation (30+ languages)
    mcp: true
  grepai:
    binary: grepai
    type: go
    description: Semantic code search CLI
  fastmcp_rust:
    binary: fastmcp_rust
    type: rust
    description: Preferred MCP engine for poly-bound component surfaces
    mcp: true
daemons:
  leann-grpc:
    source: process
    command: uv run python python/server.py --port 50052
    port: 50052
    protocol: grpc
    type: python
    description: LEANN semantic vector search (gRPC)
    capabilities: [semantic_search, vector_rag, embeddings]
  bd: ...
```

---

## Fractal Config Pattern

Source: `~/lev/dna/fractal.yaml`

> "Fractal roots are the source of truth. Registries are derived artifacts."

Resolution order (inline key -> domain file -> domain folder glob):

```
~/.config/lev/           (global)
.lev/config.yaml         (project-local canonical root)
.lev/config/*.yaml       (project-local shards)
```

Principles:
- Multiple read shapes allowed; canonical writes converge on `.lev/config.yaml` + optional shards
- Resolvers normalize shape before evaluating meaning (authoring format != runtime shape)
- Project root resolved once per entry root; relative globs interpret from that root
- Only boundary-approved knob subsets compile onto the execution plane
- Poly consumes a compiled registry view; it must not become the authoring surface

---

## CLI Discovery

Source: `~/lev/core/poly/src/surfaces/cli/discovery.ts`

```typescript
const HANDLER_DIRS = ['src/commands', 'src/handlers'];

export function discoverCommands(): CommandRegistry {
  // Scans core modules:
  for (const moduleName of coreModules) {
    for (const handlerDir of HANDLER_DIRS) {
      scanDir(join(CORE_DIR, moduleName, handlerDir), moduleName, commands);
    }
  }
  // Scans plugins:
  for (const pluginName of plugins) {
    for (const handlerDir of HANDLER_DIRS) {
      scanDir(join(PLUGINS_DIR, pluginName, handlerDir), `plugin:${pluginName}`, commands);
    }
  }
}
```

Both `src/commands/` and `src/handlers/` are scanned for every core module and plugin.

---

## 6-Tier CLI Verb Taxonomy

| Tier | Category | Verbs |
|------|----------|-------|
| 1 | Core | `exec`, `validate`, `compile`, `runner`, `profile` |
| 2 | SDLC | `sdlc`, `loop`, `autodev`, `work`, `review` |
| 3 | Bench | `bench run`, `bench list`, `bench validate` |
| 4 | Research | `research`, `experiment` (via `handlers/`) |
| 5 | Graph | `graph show`, `graph traverse`, `graph propose` |
| 6 | Swarm | `swarm spawn`, `swarm status`, `swarm merge` |

---

## External Tools (NOT our code)

| Tool | Language | Purpose |
|------|----------|---------|
| `ntm` | Go | External tmux agent spawning. We own `TmuxHarness` instead. |
| `bd` / `beads` | Rust | Issue tracking CLI |
| `ck` | Rust | Code knowledge search CLI |
