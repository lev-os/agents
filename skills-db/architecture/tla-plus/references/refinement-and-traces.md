# Refinement, Stuttering, and Trace Validation

## Refinement

Refinement means every behavior of the concrete spec is allowed by the abstract spec.

Typical flow:
- write or identify the abstract spec
- instantiate it in the concrete spec
- use `WITH` when symbols differ
- check the abstract spec as a `PROPERTY` of the concrete one

Refinement mappings can use state functions, not just bare variables.

## Stuttering

You usually do not model stuttering explicitly.

`[Next]_vars` already means:
- either `Next` happens
- or the variables do not change

Do not add explicit skip actions unless you have a very specific reason.

## Trace validation

Trace validation checks whether an implementation trace corresponds to a valid spec behavior.

Use it only when:
- the event order is meaningful enough to compare against the spec
- the spec constants match the implementation that produced the trace
- you can explain how implementation events map to spec actions

For simple systems, NDJSON traces are a practical bridge between running code and a TLA+ spec.
