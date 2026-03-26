# Browser And Framework Integration

Use this reference when the target includes browser execution, React, or
Next.js. The browser lane is real, but it is not "run the entire native runtime
everywhere JavaScript exists."

## The First Decision: Direct Runtime Or Bridge-Only?

| Environment | Direct Browser Edition Runtime | Guidance |
|------------|-------------------------------|----------|
| browser main thread | yes | canonical direct-runtime lane |
| browser worker | possible, validate parity and policy first | keep evidence artifacts |
| Node.js server runtime | no | bridge-only |
| Next.js server components / route handlers | no | bridge-only |
| edge/serverless runtimes with partial Web APIs | assume no unless explicitly validated | unsupported-runtime is the default posture |

Do not blur this boundary.

If the environment is not a supported direct-runtime lane, keep runtime
execution in a browser boundary and communicate over explicit RPC/API seams.

## Profile Selection Is Mandatory

Choose exactly one wasm browser profile:

- `wasm-browser-minimal`
- `wasm-browser-dev`
- `wasm-browser-prod`
- `wasm-browser-deterministic`

Rules:

- exactly one canonical profile on wasm32
- native-only features are compile-time rejected
- browser onboarding should validate profile closure before framework work

Use profile intent correctly:

- `minimal` for contract/ABI checks
- `dev` for local development and diagnostics
- `prod` for production-lean envelope
- `deterministic` for replay-oriented validation

## Vanilla Browser Pattern

Good direct-runtime posture:

- initialize in a real browser entrypoint
- keep capability boundaries explicit
- verify quiescence, cancellation, and security policy early

What to validate first:

- browser-ready handoff
- nested cancel cascade reaches quiescence
- browser fetch security/default-deny policy

Do not start with framework glue before the vanilla browser lane is green.

## React Pattern

The repo's React guidance is more specific than "use an effect."

Canonical patterns:

- task groups with explicit cancellation UX
- bounded retry after transient failure
- bulkhead isolation between independent work groups
- tracing-hook transitions with deterministic scenario ids

Practical rules:

- component lifecycle should map cleanly onto scope ownership
- user cancel actions should drive explicit cancellation, not silent abandonment
- retries should stay bounded and observable
- sibling feature areas that can overload independently should use bulkhead
  thinking rather than one shared failure domain

React anti-patterns:

- detached async work that outlives component lifecycle
- retries with no total budget
- effect cleanup that does not actually drain outstanding work
- unstructured logs that cannot be replay-correlated

## Next.js Pattern

The important mental model is phase-based:

- `ServerRendered -> Hydrating -> Hydrated -> RuntimeReady`

Use that model explicitly.

Rules:

- runtime init belongs in client-hydrated code, not server or edge phases
- hard navigation and cache revalidation should be treated as explicit runtime
  scope invalidations
- re-init should be deterministic and logged as such
- App Router boundaries are real lifecycle boundaries, not incidental framework
  details

Good posture:

- keep browser runtime creation in client components or browser-only modules
- treat `ServerRendered`/`ClientSsr` runtime init failures as misuse, not a
  flaky environment problem
- make rebootstrap on navigation or invalidation explicit

## Browser Scheduler Semantics Matter

The browser adapter is not allowed to throw away the native scheduler model.

Important semantics from the repo docs:

- lane order still matters: cancel > timed > ready
- cancel fairness must remain bounded
- scheduler pump must be non-reentrant
- wake dedup must survive host-turn boundaries
- `yield_now()` must cooperate without monopolizing the same turn
- deterministic metadata should exist for parity and replay

Practical implication for downstream code:

- do not build UI/runtime glue that assumes unlimited same-turn microtask churn
- do not inline-poll on timer callbacks or wake callbacks
- treat main-thread starvation as a semantic bug, not just a UX bug

## Worker Offload Is Policy-Governed

If browser runtime work moves into Web Workers, treat it as a policy boundary:

- ownership remains attached to the originating region/task
- cancellation must cross the worker boundary explicitly
- replay metadata must follow the job
- offload should not be used to hide scheduler bugs or unbounded main-thread
  work

## Unsupported Runtime Failures Are Useful

The browser stack deliberately throws unsupported-runtime diagnostics for bad
contexts. Treat them as guidance, not noise.

Representative codes from the repo docs:

- `ASUPERSYNC_BROWSER_UNSUPPORTED_RUNTIME`
- `ASUPERSYNC_REACT_UNSUPPORTED_RUNTIME`
- `ASUPERSYNC_NEXT_UNSUPPORTED_RUNTIME`

Typical causes:

- attempted init in Node or SSR
- missing browser DOM/WebAssembly/fetch/runtime prerequisites
- direct runtime usage in server or edge paths

Correct response:

- move runtime creation into a supported client/browser boundary
- keep server/edge paths on bridge-only adapters

## Evidence Contract For Browser Adoption

Browser work should produce artifacts, not just console impressions.

Capture:

- scenario id
- profile flags
- command bundle used
- pass/fail per step
- artifact paths
- failure excerpts and remediation hints

This matters because the browser lane has explicit policy, closure, redaction,
and replay contracts.

## Browser Troubleshooting Ladder

1. verify onboarding scenario bundle
2. verify dependency/profile policy
3. verify log-quality and redaction contracts
4. run targeted lifecycle/security/parity tests
5. escalate only with artifacts in hand

Treat missing artifacts as workflow failure.

## High-Value Adoption Advice

- start with the vanilla/browser core lane before React or Next
- validate profile closure before fighting framework behavior
- keep runtime state in client-controlled lifecycle boundaries
- make cache invalidation and hard navigation explicit rebootstrap events
- use deterministic scenario ids and structured logs from the beginning

## Anti-Patterns

- trying to run Browser Edition directly in Node, SSR, or edge by default
- mixing multiple canonical browser profiles in one wasm build
- assuming browser support means native DB/TLS/process/fs/server surfaces exist
- hiding lifecycle bugs behind retries or generic "hydration issue" language
- treating unsupported-runtime diagnostics as optional warnings

## Read Next

- `BROWSER-WASM.md`
- `TESTING-FORENSICS.md`
- `OBSERVABILITY-FORENSICS.md`
- `TROUBLESHOOTING.md`
