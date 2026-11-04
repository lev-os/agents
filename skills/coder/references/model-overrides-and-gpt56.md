# Model overrides and GPT-5.6-family Codex runs

Use this when a user wants occasional access to a newer/high-end Codex model (for example `gpt-5.6-sol`) while preserving the existing default model (for example `gpt-5.5`).

## Durable pattern

- Keep the default model in Codex/Hermes config or the Lev exec profile.
- Use `codex exec -m <model>` only as an explicit per-run override requested by the user.
- Pair `-m` with `-c model_reasoning_effort=<level>` only when the user asks for a different effort or the task clearly needs it.
- Do not hardcode the newer model into reusable prompts, goals, or this skill.

Example one-off dispatch shape:

```bash
CODEX_HOME="${LAZYCODEX_HOME:-$HOME/.codex-lazycodex-trial}" codex exec \
  -s workspace-write \
  -m gpt-5.6-sol \
  -c model_reasoning_effort=high \
  --output-last-message /tmp/<task-id>-last.txt \
  "$(cat /tmp/<task-id>-prompt.md)" < /dev/null
```

If the provider/CLI supports `max`, use it only after confirming the local CLI/config accepts it; older Hermes/Codex paths may only expose `minimal|low|medium|high|xhigh`. For one-off model/effort tuning, run a compact live matrix first and save CSV/JSONL/report artifacts; this catches both provider acceptance and task-quality tradeoffs before changing defaults.

## Compact live reasoning-effort benchmark

When model access exists but effort behavior is uncertain, benchmark the live provider rather than assuming docs or UI labels are complete.

Suggested artifact shape:

- `results.csv` — one row per model/effort call with `ok`, `correct`, latency, token counts, and error classification.
- `results.jsonl` — raw per-call responses/errors for later inspection.
- `report.md` — human summary by model, including fastest correct effort and lowest-token correct effort.
- Harness script under the repo's `scripts/` or local tooling area so it can be rerun with a new timestamped output directory.

Session-proven GPT-5.4–5.6 acceptance pattern from a compact arithmetic matrix:

- Efforts tested: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`.
- `minimal` was rejected across GPT-5.4–5.6 family models.
- `max` was accepted by GPT-5.6-family models and rejected by GPT-5.4/5.5 models.
- `none` can be fast but wrong on reasoning/arithmetic tasks; do not treat it as a safe default for correctness-sensitive work.
- `low` was the best cheap/fast default across GPT-5.6-family models in that run; still verify against the actual task class before changing policy.

Do not store these benchmark results as global model truth. Treat them as a reusable probe pattern and a known provider-quirk starting point; rerun when provider metadata, model aliases, or task class changes.

## Checks before recommending an update

1. Verify whether the desired model appears in the live Codex/OpenAI model catalog or provider model picker.
2. If the model is already visible, a Hermes update may not be required for basic access.
3. Recommend a Hermes update when model metadata, picker UI, reasoning-effort support, or gateway behavior appears stale.
4. Keep Hermes update and external Codex CLI installation separate: Hermes can have Codex auth/model discovery even if the standalone `codex` binary is not installed.

## Setup/fix note

If the standalone `codex` command is missing and the user wants raw `codex exec`, install or update the Codex CLI with one of the upstream-supported installers, then rerun `codex --version` before dispatching workers.
