# Troubleshooting

## "ObligationLeak detected"

Meaning:

- A permit, ack, lease, or similar obligation was not committed or aborted.

Typical cause:

- reserving a send or resource and returning early

Fix:

- always resolve the obligation explicitly
- avoid holding it across unrelated awaits unless that is the protocol

## "RegionCloseTimeout"

Meaning:

- A region is trying to close but descendants or finalizers are not finishing.

Typical cause:

- loop without checkpoints
- child work that never observes cancellation

Fix:

- add `cx.checkpoint()?` in loops and long-running work
- make ownership and join paths explicit

## "FuturelockViolation"

Meaning:

- A task is holding obligations but has stopped making observable progress.

Typical cause:

- await while holding a permit/lock/resource that should have been resolved first

Fix:

- shorten the critical section
- restructure to avoid waiting while holding obligation-bearing state

## Deterministic Drift

Symptom:

- same seed does not produce the same behavior

Check:

- wall-clock time usage
- ambient randomness
- nondeterministic collection usage in deterministic-sensitive code

## Compat-Bridge Trouble

Symptoms:

- deadlock between runtimes
- timers or cancellation do not behave consistently
- tasks outlive the owning region

Fix:

- narrow the compat surface
- ensure `Cx` crosses the boundary explicitly
- do not keep ad hoc Tokio task ownership alive

## Browser Edition Unsupported Runtime

Symptoms:

- runtime constructors rejected in server, edge, or SSR contexts

Fix:

- move runtime creation to browser main-thread or client component code
- keep server/edge lanes bridge-only

## Advanced Surface Caution

If the user asks for:

- QUIC / HTTP3
- remote/distributed runtime
- messaging
- Browser Edition packaging/release details

Then verify the current repo state in source/docs before claiming feature completeness.

