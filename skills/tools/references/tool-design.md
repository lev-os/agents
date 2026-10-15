# Tool design and repair

Read this branch when designing a tool, writing or repairing its description,
schema or output, or diagnosing wrong-tool picks, malformed calls, oversized
results or errors an agent cannot recover from. Ordinary calls through an
existing integration stay on its leaf.

## Checks

Apply every check to each tool in scope and record its evidence beside it.

1. **Purpose** — each tool has one purpose no other tool in the catalog shares.
   When a person cannot say which of two tools fits a request, merge them or
   sharpen both descriptions until the choice is clear. Keep tools separate
   when their effects, permissions or independent calls differ.
2. **Description and examples** — state what the tool does, when to choose it,
   its inputs with types, constraints and defaults, and what it returns. Take
   each input/output example from supported behavior: the live schema, a
   declared CLI's help output, or an observed response. Label an example you could not observe as
   unverified.
3. **Bounded projections** — default to the smallest projection that answers
   the common request, with stable IDs for follow-up calls. Offer more through
   fields, pages or a file reference, and report truncation with the way to
   fetch the rest.
4. **Actionable errors** — each error names the failing input, the value
   received, the expected form with a valid example, and whether retry is safe.
   Separate input rejection, where the response shows nothing ran and a
   corrected retry is safe, from an ambiguous mutation outcome such as a timeout
   after a write, where the effect may exist. A known failure with null or
   unknown execution metadata is not evidence that nothing ran; report it as
   unknown. Expose a lookup key (resource ID, idempotency key or query) so the
   caller can check before acting again.
5. **Names** — refer to each tool by the exact name the host exposes, including
   any prefix that host adds; keep parameter and field names consistent across
   the catalog. A tool name alone does not establish an executable, subcommand
   or flag syntax. Resolve the host's actual transport and schema (tool-call
   schema, API endpoint, or a declared CLI mapping) before writing an
   executable example; otherwise label the example unresolved.

## Verification and boundaries

Exercise representative requests, including competing-tool and malformed-input
cases, against the actual tools through their resolved transport, and keep the
observed calls and responses. A
description repair is done when those observations match it. The observations
are evidence for the owning eval; they do not qualify or promote a tool.
Implementing, registering or installing a tool keeps its existing authority; a
new integration follows the Add a tool branch.
