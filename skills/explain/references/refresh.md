## Refresh current state

`--refresh` is an optional modifier and combines with the existing scopes and
explanation modes. With no topic or explicit conversation-selection scope,
use the current conversation. Preserve numeric/recent/project selections from
the entrypoint; refresh each selected conversation rather than replacing the set.
It requests
fresh evidence, not a Git pull, implementation, tracker update, or task resume.
Separately authorized actions retain their own scope.

When `--refresh` is requested after a long gap or suspected refactor, refresh
before explaining because old paths, names, decisions, and test results may
describe a retired system:

1. Bind the current project and snapshot the date, checkout revision, branch,
   dirty state, and known upstream lag. Follow its config, current vocabulary,
   owner guidance, and active workstream pointers. State which checkout was
   inspected; do not call it latest without checking.
2. Extract the old conversation's load-bearing claims: purpose, chosen owners,
   implementation status, unresolved decisions, and next action. Recheck each
   against current code, declared contracts, tests, and linked runtime evidence.
   Use structural discovery tools when available. Follow moves through current
   imports, owner declarations, and Git history; a missing path or similar name
   alone does not prove deletion or equivalence.
3. Mark each consequential claim current, superseded, or unverified with a
   concrete source and date/revision. Show a compact then/now comparison when it
   helps. Preserve the original intent while using current established terms;
   conflicting owners remain an explicit gap rather than a synthesized decision.
4. Run the smallest safe check that could disprove the central current claim
   when practical. Distinguish an existing implementation, a fresh test pass,
   and live end-to-end proof. If checks or hosts are unavailable, name the gap
   and continue the evidence that is accessible.
5. Explain the purpose, material changes, surviving decisions, current blocker,
   and next eligible action. State the coverage window and what was actually
   checked. Never resume a retired plan merely because it was this chat's last
   recommendation.

Bad: repeat "create core/eval" from an old chat without checking today's tree.
Good: find its current owner and tests, explain which extraction landed, and
identify the remaining integration evidence. If no project source is accessible,
give a dated historical explanation and mark current state unverified.

## Refresh checklist

Use this checklist for an old conversation, for example two weeks old, while
other work moved the repo under it. What the conversation says about the repo
is then a dated report, not the current state. Look around first. Then present
the conversation again.

```yaml
steps:
  - id: recover
    action: From the conversation, recover the goal, the history (what was done and decided, with dates), and the last response with its open items and next steps.
    validation: "The goal, each decision and each item of the last response is listed with its date."
  - id: look_around
    action: Read the repo as it is now. Find what moved since the last substantive turn - the commits of other work, and the current state of each file, record, check and command that the history or the last response names.
    validation: "Each named thing has an observation made in this turn (a command, a file read), or the mark not found or not checked."
  - id: compare
    action: Mark each claim, open item and next step of the conversation as still true, changed, done by other work, or gone. Put the evidence beside each mark. These marks refine step 3 above - still true is current; changed, done by other work and gone are superseded; not checked is unverified.
    validation: "No item of the last response is presented again without its mark."
  - id: present_again
    action: Present the goal, the history and the last response against the current state, in the report layout of SKILL.md (Inline output). Start with what changed under the conversation. Keep the next steps that are still valid and withdraw the others.
    validation: "The reader can continue from this message without the old one, and no stale claim is given as current."
```

A refresh reads. It does not repair what it finds.
