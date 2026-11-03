# Runtime capability surface audits

Use this reference when auditing whether an external agent framework is merely an app/runtime or is abstracting the same class of surfaces Lev cares about: hooks, MCP, CLI config, provider-native tools, declarative specs, and policy/evidence envelopes.

## Session lesson: Pydantic AI 2.0 under-counted parity

A prior pass reduced Pydantic AI 2.0 to a small 7-row parity artifact. The user correctly objected: the important surface was not the row count; it was how Pydantic AI composes agent-runtime behavior through `AgentSpec`, `AbstractCapability`, hooks, MCP, native/local tools, and deferred loading.

When the user asks "how are they doing this?" or compares a framework to Lev's abstract hook / agent CLI config concept, do not summarize top-level marketing features. Audit the actual extension/config surface.

## Minimum audit dimensions

1. **Declarative config/spec layer**
   - YAML/JSON schema fields
   - load/save APIs
   - merge/override semantics with runtime arguments
   - editor/schema generation, if present

2. **Capability/extension contract**
   - Methods on the abstract base class, not just named built-ins
   - Serialization names and `from_spec`/registry hooks
   - Payload methods: tools, toolsets, native tools, model settings, instructions, descriptions
   - Ordering, prefixing, wrapper/middleware affordances

3. **Hook taxonomy**
   - run/node/model/tool/output phases
   - before/after/wrap/error variants
   - stream hooks
   - validation vs execution hooks
   - whether hooks can modify, skip, defer, retry, or only observe

4. **MCP surface**
   - client vs server projection
   - local stdio vs remote HTTP/SSE
   - provider-native MCP selection/fallback
   - Claude-style `mcpServers` config loading
   - env expansion and secret handling
   - tool prefixing, prompts/resources/sampling, per-call middleware

5. **CLI / external process abstraction**
   - whether the framework abstracts arbitrary external CLIs/process runners or only its own runtime
   - argv templates, config schemas, profile/provider selection, working directory/env handling
   - generated MCP/HTTP/SDK/CLI surfaces from one manifest, if any

6. **Deferred/on-demand loading**
   - load tools/capabilities dynamically
   - whether load state persists in message history/run context
   - discovery APIs for available/loaded capability/tool ids

7. **Policy/evidence/operation envelope**
   - side-effect classification
   - dry-run/confirmation semantics
   - receipts/proofs/artifact refs
   - error/result envelope stability across surfaces

## Useful technique

For captured source trees, run an AST inventory of class/function method names on the likely core files. This catches surfaces hidden behind abstract methods that docs summarize too lightly. For Pydantic AI, the decisive signal was that `AbstractCapability` exposed ~46 lifecycle/payload methods, not that docs listed a handful of capabilities.

## Output guidance

Return a grouped surface map, not a toy feature count. Use categories like:

- Spec/config
- Capability payload
- Hooks
- MCP/local/native
- Toolsets/deferred loading
- CLI/web/UI surfaces
- Packaging/extensibility
- Local framework equivalent
- Gap / extraction opportunity

When comparing to Lev, state the center of gravity explicitly:

- Pydantic-style frameworks: agent-runtime behavior config
- Lev/Poly: external execution/surface config across CLIs/MCP/HTTP/SDK/processes

Then identify the bridge concept, e.g. `CapabilityContract` / `HookBundle` / `McpSurface` / `CliSurface` / `DeferredLoadPolicy` / `PolicyEvidenceEnvelope`.
