# Pi worker

Pi is the thin, fast worker option. Prefer the Lev `pi` provider card and a
project execution profile over a forked Pi distribution.

A Lev-flavored Pi must load one explicit, versioned Lev extension bundle plus
the frozen project context packet. Do not use the current `--no-extensions`
provider recipe for that mode: it proves bare Pi, not Lev semantics. Keep bare
Pi as a separate diagnostic profile.

The context packet supplies the applicable project instructions, `.lev`
workstream/task, FlowMind node contract, allowed tools, proof gate, and stop
rules. Pi emits its native session transcript; Lev binds that session to the
execution and ingests it through the platforms transcript adapter.

CAAM currently manages provider CLIs it explicitly supports, not Pi itself.
When Pi calls a CAAM-supported provider, the future `plugins/caam` adapter must
bind the underlying provider profile. Until that contract exists, report the
identity boundary as unverified rather than implying a lease.

