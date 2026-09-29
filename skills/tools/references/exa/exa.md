# Exa / web research

Use the configured web/Exa capability for source gathering. Preserve source
URLs, dates, claims, and uncertainty in the consuming artifact. General
research strategy and synthesis belong to the research skill; this reference
owns explicit Exa transport and API discovery.

## Direct local transport

Use the `scripts/exa.sh` file beside this reference for the bounded `search`,
`contents`, `answer`, and `status` commands. Resolve its path relative to this
file, set the target project `cwd`, and keep `EXA_API_KEY` in the process environment or the
configured local credential source. An explicit environment key takes
precedence over env files. The script bounds connect and total request time,
validates inputs, and reports non-2xx status as failure.

Bind `TOOLS_ROOT` to the absolute directory containing the loaded Tools
`SKILL.md` before these commands; it is independent of the target project cwd.

```bash
"$TOOLS_ROOT/references/exa/scripts/exa.sh" search "query" --num 10 --location CA
"$TOOLS_ROOT/references/exa/scripts/exa.sh" contents https://example.com/page
"$TOOLS_ROOT/references/exa/scripts/exa.sh" answer "question" --no-text
"$TOOLS_ROOT/references/exa/scripts/exa.sh" status
```

`status` performs a one-result search and can consume quota; `help` is offline.
Do not add a default location or treat `status` key presence as provider
authentication. A successful status call requires the API response to return
HTTP 200.

## Expanded Exa capabilities

When a task names an Exa capability beyond the local wrapper, read the current
API contract from <https://exa.ai/docs/llms.txt> and use the provider's live
endpoint or SDK. The current product surface includes search, contents, answer,
websets, monitors, batch jobs, agent runs, and team/API-key administration.
Discover the exact endpoint, required scopes, pagination, limits, and mutation
semantics before calling; do not invent a wrapper for an endpoint the local
script does not expose.

Search results and generated answers are evidence, not authority to mutate an
external system. Route implementation or other provider mutations to their
owning integration reference. For technical claims, prefer primary sources
and cite the sources in the consuming response.

Search supports `--num`, `--type`, `--category`, `--domains`, `--exclude`,
`--since`, `--until`, `--location`, `--no-text`, `--no-summary`; contents supports
`--max-chars`, `--num-sentences`, `--highlights-per-url`, `--no-summary`; answer
supports `--no-text`. All three accept `--output`. Dates use YYYY-MM-DD.
Consult current provider schemas for accepted enum values and limits.
