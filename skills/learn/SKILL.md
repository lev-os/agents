---
name: learn
description: "Use when a lesson must change future agent work: a person asks to codify a correction, capture codify hands over a saved record, or a retro, a plan or a design holds evidence of what should happen next time. Compares every place in the active project that can change that behaviour, proposes the most correct one with its proof, and applies it only after approval."
skill_type: workflow
category: lifecycle
triggers:
  - learn
  - codify
---

# /learn - Put a lesson where it acts

Use the evidence to describe what happened and what should happen next time.
Compare the places that can change that behaviour in the active project. Show
the proposed edit, why it belongs there, and how to prove it works. Apply the
proposal after approval.

A **lesson** is one behaviour to change, with its evidence. A **place** is a
file or setting that the agent, the workflow or the reviewer loads at the moment
that behaviour happens. Learn owns the method. The project's own instructions
and settings supply the real places, owners and paths.

## Inputs

| From | You get |
|---|---|
| Capture codify | A reference to a saved record, the source evidence and the behaviour the person wants to change |
| A project retro | Clustered evidence (for example repeated commit trailers) and the project's own rules for its places |
| Planning or solution design | The evidence the plan or design already holds |
| A person, directly | The correction in their words. When it is not saved yet, load `skill://capture` first: capture saves it in its record, reads it back and hands the reference back to learn |

## Steps

1. **Read the evidence.** Open the saved record or source and read it back.
   Done when every statement about what happened cites a turn, a path with a
   line, a commit or a run. A reference you cannot read stops learn: report it.
2. **Decompose what happened.** Name the task, the moment the behaviour went
   wrong, the agent or program that decided, and what it had loaded then.
   Done when you can say "at <moment>, <actor> did <x> because it loaded <y>"
   or say which part is unknown.
3. **Describe the intended behaviour from first principles.** One sentence:
   what should happen next time, at that moment. Use the words the project
   already has for each thing (search its glossary, docs and records first).
   Done when the sentence names the moment, the actor and the result.
4. **Find every place.** Read the project's instruction chain and settings,
   then list each place in "Where to look" that can change this behaviour,
   with its path, what loads it, when, and its owner. Done when every row of
   "Where to look" has a place, or "none in this project" with the search
   you ran.
5. **Pick the most correct place.** Use "How to choose". Map the change to
   the forms this project declares for that place (its rules, flows, config
   or checks), as its instructions name them. Done when one place is picked
   and each other candidate has one line on why it is not the place.
6. **Propose.** Show the proposal (see Output) in the reply. Apply nothing.
7. **Apply after approval.** When the person says yes to this proposal, the
   owner of the place applies the edit through the project's normal path:
   for a generated file, edit its source and regenerate. Apply only the
   approved edit. A changed request is a new proposal.
8. **Prove it.** Run the evidence from the destination table and report
   each claim pass, fail or could not check, with `path:line` or the command
   and its exit code. Done when no claim is left unanswered.

## Where to look

Read these to find the places. Each project has its own subset; the
instruction files and settings say which.

| Type of place | Where to look |
|---|---|
| Instructions | The chain an agent loads: global (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`), repo root (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) and each folder's own file on the path to the work. Follow every `@file` import and pointer |
| Skills | Project skills (`.agents/skills/`, `.claude/skills/`) and global skills (`~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/`); a skill may be generated from a source file |
| Docs and specs | The docs, specs and designs that instructions or skills point at |
| Workflows and config | The flow or pipeline that owns the step, and the project settings it reads |
| Hooks | Agent hooks (`.claude/settings.json`, `~/.claude/settings.json`), git hooks, CI jobs |
| Checks | Tests, lint rules, eval packs and review rows, with the program or reviewer that runs them |

## How to choose

Find where the decision is made, what loads there and who owns it. Compare all
the places that apply before you pick the most correct one. The breadth of a
file cannot settle the choice: a global file is not more correct because it
reaches more work, and a folder file is not more correct because it is small.

| What needs to change | Destinations to inspect | Evidence that it worked |
|---|---|---|
| What an agent knows while doing a task | Folder, repo or global instructions, project or global skills, and the docs or specs they load | Start a fresh task from its normal entry point. Observe which guidance it loads and what it does. |
| What a workflow does | The owning flow, its project configuration or an existing hook | Exercise the relevant branch with the changed setting or input and observe the resulting action. |
| What passes review | A module spec, test, eval pack or agent review row | Use the existing evaluator. A valid case passes and a planted violation fails. A review row needs an observed reviewer answer before it counts as exercised. |

Rules for the pick:

- **A place that acts beats a place that tells.** A line in an instruction file
  can be loaded and still not change what the agent does. A check or a hook acts
  on its own. When a check or hook is the correct place, pick it, and say what
  still needs proof.
- **One meaning, one place.** When a place already holds the rule, change that
  line. Add a line only when no place holds it.
- **The owner decides how it lands.** When the project says a file belongs to a
  person, hand them the proposed line. A generated file changes at its source.
- **When a check fits, use the check guide the project's instructions name** to
  write the case that passes and the planted fault that fails.
- **One request, one proposal.** Promote a lesson when a person or a retro asks.
  A repeat alone does not make a lesson a check.

If the project has no evaluator or no known loading path for the place, say
which part of the proposal still needs proof.

## Output

```text
Lesson: <what happened, with its evidence>
Intended behaviour: <one sentence: moment, actor, result>
Place: <path or setting> (owner: <who>)
Edit: <the exact diff or line>
Why here: <where the decision is made and what loads this place then>
Not there: <each other candidate: one line why not>
Proof: <the check from the destination table: command, case or observation>
Still needs proof: <what no check here can show yet>
```

## Stop if

- The evidence cannot be read back.
- The edit would mint a new name, command or public type, or change a ruling:
  ask the person who owns that choice.
- The person has not approved the proposal: show it and wait.

## Related

- `/capture` saves the material first; `capture codify` then loads learn.
- `/review` gives a fresh reader for the proof.
- A project's retro skill harvests its own evidence and adds its own rules for
  the places.
