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

## Pi-family harnesses: omo and omp

Both are pi forks with the same headless event stream, so one transcript
adapter covers pi, omo, and omp. Verified live 2026-09-26 (omo 5.0.0, omp 18.3.2).

| | omo (OmO Native) | omp (oh-my-pi) |
|---|---|---|
| Headless | `omo -p --mode json --no-session` | `omp -p --mode json --no-session` |
| RPC | `--mode rpc` | `--mode rpc` / `rpc-ui`, `acp` subcommand |
| Permissions | `--permission-preset full-access\|workspace\|read-only\|ask`, `--permission tool=action` | `--approval-mode always-ask\|write\|yolo`, `--auto-approve` |
| Model | `--model provider/id[:thinking]`, `--thinking` | `--model` (fuzzy), `--thinking`, `--smol/--slow/--plan` roles |
| Model catalog | `omo --list-models` (table) | `omp models --json` (context, maxTokens, cost) |
| Budget | none native; enforce by timeout | `--max-time 10m` |
| Session | `--session-id <id>` (exact), `--resume` | `--resume <id>`, `--session-dir` |
| Identity | `omo setup` / `/login`; `--profile` n/a | `--profile <name>` isolates auth/sessions |
| State dir | `~/.omo/agent` | `~/.omp/agent` |

```bash
(
  cd "$runner_repo"
  omo -p --mode json --session-id "$runner_session_id" \
    --permission-preset workspace \
    < "$runner_task_dir/prompt.txt" \
    > "$runner_task_dir/events.jsonl" 2> "$runner_task_dir/stderr.log"
)
jq -r 'select(.type=="agent_end") | .usage' "$runner_task_dir/events.jsonl"
```

Caveats: the omo installer migrates `~/.pi/agent` to `~/.omo/agent`; bare Pi
still needs its own `~/.pi/agent`. Never pick omo in `full-access` or omp in
`yolo` unless the Codex bypass-flag conditions above hold. CAAM does not manage
either harness; report the identity boundary as unverified.

Project config: omo reads `.omo/` (its brand overrides senpi's `.senpi`,
`omo-ai/bin/lib/launcher.js`), so project extensions live in
`.omo/extensions/`, not `.pi/extensions/`.

Through Lev: `lev exec --profile=sdlc.flowmind.exec-omo` or `exec-omp`. The
provider cards run `--mode json` and Lev's `pi-json` reader records
`worker.turn.*`, `worker.tool.called`, `worker.usage` (tokens plus the
worker's own cost) and `worker.done` per run. Lev fails the run when
`worker.done` reports an error, even on exit 0. A profile's `permission:`
(read-only | workspace | full) maps to `--permission-preset` on omo, and
`budget` / `budget_cost_usd` stop the worker once live usage crosses them.
Nothing is installed into omo, omp or pi for this.
