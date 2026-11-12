# Zoom-out review

The `zoom_out` lens under the cold-reader stance. One fresh reader reads a design, plan or brief with no earlier
conversation and asks one question: does it fix the root problem, in the simplest way, by reusing what exists? It is
the "goldfish" half of the elephant-goldfish model: the author knows everything, the reader knows only the text.

## Status

Calibrated on test designs; advice only (JP 2026-11-08, `.lev/pm/decisions/20261108-zoom-out-lens-calibration-rulings.yaml`
in the Leviathan repo). Version 2 answered 90 of 90 right on 30 test designs and passed core/eval's calibration check,
but agents wrote all 30 and none was a real record. It reports; it never blocks a transition, never changes a
readiness verdict, and never stands in for a check. It can gate only after a round on real design records passes.

## When to run it

Once, when the artifact is written and before it leaves its stage; the caller's own line names the point. Skip it for
a task packet (its checks already decide), for a one-line change, or when the Leviathan repo is not on this machine.
Say that you skipped it and why.

## How

The prompt lives in one place, the lens pack; never copy its text into a skill.

Each run gets its own folder, so runs can go in parallel. Run the whole block as one shell call, with ARTIFACT set to
the artifact's path; it prints the run folder. Keep that path: a later call (reading the answer, cleaning up) names
it in full.

```bash
ARTIFACT=path/to/the/artifact.md
RUN=$(mktemp -d /tmp/zoom-out.XXXXXX) && echo "$RUN"
LENS=$HOME/digital/leviathan/workshop/analysis/elephant-goldfish-model/spike2
node "$LENS/calibration/render-one.mjs" design_lens_zoom_out "$ARTIFACT" "$RUN/prompt.txt"
mkdir "$RUN/seat" && cd "$RUN/seat" && claude -p --model claude-opus-5-5 --tools "Read,Grep,Glob" \
  --disallowedTools "Bash" "Write" "Edit" "WebFetch" "WebSearch" "Agent" \
  --setting-sources local --no-session-persistence < "$RUN/prompt.txt" > "$RUN/answer.txt"
```

- The reader's whole reply is one JSON object: `evidence_refs`, `blockers`, `majors`, `nits`; each item has `scope`
  and `rationale`. One code fence around it is fine.
- When done, remove that run's folder by its full printed path (for example `rm -rf /tmp/zoom-out.Ab12Cd`).
- On a host without the `claude` command, skip the lens and say so.

## Reporting

- In review's report block, copy every item word for word as one finding line: `rationale` is the finding, `scope`
  (the part of the artifact it names) is the evidence, and the source is `zoom_out`. Then one line:
  `zoom-out evidence_refs: {the list}`.
- No blocker and at least one cited ref: add the line "the zoom-out review found no blocker". A reply that is not the
  JSON object goes in the block whole, with the line "zoom-out: could not check".
- Only blockers decide that line; majors do not (version 1 counted them and failed sound designs).
- Never tune the prompt on the artifact you are reviewing. Prompt changes go through a new calibration round
  (`calibration/method.yaml` in the lens folder).
