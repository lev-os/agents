# State machine audit

Find every implicit state machine in an app, check it against what the code allows, and score what it costs a user
(UX), a developer (DX) and an agent (AX). The audit reports what exists. It does not design the fix: the fix starts
from the pov skill's shape mode (the ideal first), and this audit's inventory is the input to its levify step.

## The request it codifies

JP, 2026-11-15, word for word:

> Find all of the implicit state machines in my app (there are probably a ton). Make the best decision that will
> elevate all three: the user experience (UX), developer experience (DX), and agent experience (AX) always, without
> breaking anything. Also, make state machines explicit.

"Find all" is this audit. "Make the best decision" and "make state machines explicit" are pov shape mode, then a plan.

## What counts

An implicit state machine is code where a thing moves between named states, but the states and the allowed moves
are not declared in one place:

- a string field (status, state, phase, stage, mode, kind, step) compared with `===` or `switch` in more than one file;
- a group of booleans (isLoading, isRunning, done, failed) that together encode one state;
- a status string written in one package or service and read in another, or sent over an API;
- a status list in config or YAML that code copies;
- retry, backoff or lease counters that decide what happens next;
- lifecycle words that live only in comments.

A machine that is already explicit (a declared lifecycle, a statechart library machine, a typed transition table)
is listed apart, so that it is not counted twice. A one-off flag or a config enum with no moves is not a machine.

## Questions for each machine

The reader answers each one with `path:line`:

1. **States.** Which states exist, and where is each one written and read?
2. **Encoding.** String union, enum, boolean group, loose strings, YAML, or mixed?
3. **Stored.** Is the state saved to a file, a database, a log or a receipt?
4. **Crosses a boundary.** Is it read or written by more than one package, or over CLI, HTTP or MCP?
5. **Copies.** Where else are the same states defined again?
6. **Illegal move.** Name one move the code does not stop (for example, a finished thing goes back to running), or
   "none found".
7. **Cost.** What does a user see wrong (UX)? What does a developer have to guess (DX)? What can an agent not ask or
   check (AX)?
8. **Risk of change.** Low, medium or high, and why.

## How to run it

| Scope | Run |
|---|---|
| One module or folder | One fresh reader (review skill Steps), with the questions above as its checklist |
| A whole app | The saved workflow: the Workflow tool with `scriptPath: ~/.agents/skills/review/references/state-machines.workflow.js` and `args: {areas: [{key, scope}, ...]}`. With no `areas`, a scout agent proposes 3 to 6. Only when the person opted into a workflow |
| Only what changed since the last run | The same workflow with `args.since: <git ref>`; the readers look only at files changed since that ref |

The workflow runs: area finders that search several ways (by name, by string literal, boolean groups, stored
records, readers in other packages), then a completeness critic that searches again by content, merges the same
machine seen from different packages, drops false finds and rereads the five riskiest illegal-move claims in the
code. It returns the inventory, the families of machines that should share one definition, and the gaps.

Cost of a whole-app run on Leviathan, 2026-11-15: 9 agents, about 25 minutes, 1.4 million agent tokens.

## Output

The report file (review skill, Report) holds, for each machine, the answers above, and then:

- the families, each with its members and why they belong together;
- the illegal moves the critic confirmed by reading the code, each with `path:line`;
- the gaps: what was searched only by count, or not at all. They are the block's not-reached line.

The block's stop line for an audit is `audit stopped: {n} machines, {f} families, {i} confirmed illegal moves`.

The chat gets one line for the run, and the count of machines, families and confirmed illegal moves. A confirmed
illegal move is a fault: the project's own rules decide whether it becomes a debt row or a fix.

## Program checks that stop new ones

The audit is judgment work. Two program checks make it cheaper over time:

- a commit hook check that refuses a new inline status union or status literal at a call site, with a count that
  only goes down;
- a nightly replay of stored history through each declared lifecycle, counting illegal moves for each machine.
