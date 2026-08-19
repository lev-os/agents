---
name: coding-agent
description: "Launch Codex, Claude Code, or OpenCode as bounded CLI workers for implementation, fixes, refactors, reviews, and read-heavy exploration. Use when work is clear enough to hand off; skip tiny edits, naming, unresolved design, and simple read-only lookup."
---

# Coding Agent

Treat each CLI agent as a bounded worker: give it a frozen task, capture its
process and output, then verify its claims independently. Do not require a
project-specific runtime or a particular host process API.

## Route the Work

- Use the runner the user requested. Otherwise use an installed, authenticated
  runner that fits the task; do not hardcode a model when its own config already
  carries policy.
- Delegate prompts that read like work orders: implement, fix, refactor, test,
  review, or perform bounded exploration.
- Keep decisions with the controller: architecture, API shape, naming, unclear
  requirements, releases/secrets, and tiny obvious edits where delegation costs
  more than doing the work.
- For mixed tasks, decide and freeze the ambiguous parts first, then delegate the
  mechanical build-out.

## Prepare

1. Resolve the exact working directory, trust level, allowed write scope, and
   expected proof before launch.
2. Use an isolated worktree only when concurrent work or branch isolation needs
   one. Do not invent Git operations the task did not request.
3. Write the prompt to a temporary file. Include the goal, exact repo and paths,
   constraints, non-goals, verification commands, and final report shape.
4. Use the safest unattended permission mode that can complete the task. Use
   bypass modes only in a trusted checkout with a bounded prompt.

## Launch

Use the host's background-process facility when available; otherwise launch in
the shell, record the PID, and redirect output to files. Run from the target
working directory. For a shell fallback, background the selected command and
capture `$!`; do not launch all three examples.

```bash
# Codex: final answer in $OUTPUT_FILE, progress in $LOG_FILE
codex exec -s workspace-write -C "$WORKDIR" \
  -o "$OUTPUT_FILE" - < "$PROMPT_FILE" > "$LOG_FILE" 2>&1

# Claude Code: trusted unattended worker with observable event stream
(cd "$WORKDIR" && claude -p --permission-mode bypassPermissions \
  --output-format stream-json --include-partial-messages --verbose \
  < "$PROMPT_FILE" > "$EVENTS_FILE" 2> "$LOG_FILE")

# OpenCode: trusted unattended worker
opencode run --dir "$WORKDIR" --dangerously-skip-permissions \
  "$(< "$PROMPT_FILE")" > "$OUTPUT_FILE" 2> "$LOG_FILE"
```

Apply a user-requested model with the runner's native model flag. Otherwise let
the runner configuration choose. For read-only review, use the runner's
read-only, plan, or restricted-tool mode instead of the mutation examples above.

Keep normal project configuration enabled for implementation runs. Never add
Claude Code `--safe-mode` or `--bare` to normal or fallback launch recipes:
they remove project instructions, skills, plugins, hooks, MCP servers, and
custom agents that may carry the repository's execution contract. Treat a
customization failure as a diagnostic to report or repair, not a reason to run
the same mutation with fewer guardrails.

For Claude Code, `stream-json` is the progress ledger. Preserve the full event
file, monitor bounded tails or event-file growth while the process runs, and
extract the terminal `type: "result"` record into `OUTPUT_FILE` only after the
process exits. `stderr` is diagnostic output; an empty `LOG_FILE` is not proof
that the worker is idle.

## Monitor and Continue

- Capture the process handle and session ID when the runner exposes one. Poll
  process state and inspect bounded event/log tails; quiet alone is not proof of
  a hang. For Claude Code, prefer `EVENTS_FILE` activity over waiting for a
  text-mode final answer.
- Report only milestones, questions, failures, or completion.
- Send follow-up corrections through the same session when possible. Resume by
  explicit session ID; avoid `--last` when parallel runs could race.
- If a worker fails, preserve its output and error, then either resume with a
  focused correction or report the blocker. Do not silently replace delegation
  with unrelated hand edits.

## Verify

Treat the worker's final message as a claim. Inspect the complete diff, rerun the
declared focused checks, and review for scope creep before reporting completion.
Do not delegate the final judgment to the worker that produced the change.
