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

```bash
LENS=$HOME/digital/leviathan/workshop/analysis/elephant-goldfish-model/spike2
node "$LENS/calibration/render-one.mjs" design_lens_zoom_out <artifact.md> /tmp/zoom-out/prompt.txt
mkdir -p /tmp/zoom-out/seat && cd /tmp/zoom-out/seat
claude -p --model claude-opus-5-5 --tools "Read,Grep,Glob" \
  --disallowedTools "Bash" "Write" "Edit" "WebFetch" "WebSearch" "Agent" \
  --setting-sources local --no-session-persistence < /tmp/zoom-out/prompt.txt > /tmp/zoom-out/answer.txt
```

- The reader's whole reply is one JSON object: `evidence_refs`, `blockers`, `majors`, `nits`. One code fence around it
  is fine. Anything else is "could not check".
- Clean up with `rm -rf /tmp/zoom-out`.

## Reporting

- Show every blocker and major to the operator, in plain words, next to the part of the artifact it names.
- No blocker and at least one cited ref: "the zoom-out review found no blocker". Otherwise list the blockers.
- Majors are advice; they are not counted (version 1 counted them and failed sound designs).
- Never tune the prompt on the artifact you are reviewing. Prompt changes go through a new calibration round
  (`calibration/method.yaml` in the lens folder).
