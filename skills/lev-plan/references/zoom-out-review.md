# Zoom-out review (advice only)

One fresh reviewer reads a design, plan or brief with no earlier conversation and asks one question: does it fix the
root problem, in the simplest way, by reusing what exists? It is the "goldfish" half of the elephant-goldfish model:
the author knows everything, the reviewer knows only the text.

The skills that use this step: lev-plan (and propose, which forwards to it), horizon, arch, interview.

## Status

Advice only (JP 2026-11-08, `.lev/pm/decisions/20261108-zoom-out-lens-calibration-rulings.yaml` in the Leviathan
repo). It reports; it never blocks a transition, never changes a readiness verdict, and never stands in for a check.
It was calibrated on 30 test designs (version 2: 90 of 90 reviewer answers right, core/eval's calibration check
passed), but all of them were written by agents and none was a real record. It can gate only after a round on real
design records passes.

## When to run it

Once, when the artifact is written and before it leaves its stage:

| Skill | Point |
|---|---|
| lev-plan / propose | Review mode, inside `judge_readiness`, after the deterministic checks |
| horizon | `set_review`, before the brief is rendered |
| arch | Before the candidate design and decision log are handed back |
| interview | After the design artifact under `.lev/pm/designs/` is written |

Skip it for a task packet (its checks already decide), for a one-line change, or when the Leviathan repo is not on
this machine. Say that you skipped it and why.

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

- The reviewer runs in an empty folder: it must not see the conversation, the author's notes or earlier answers.
- Its whole reply is one JSON object: `evidence_refs`, `blockers`, `majors`, `nits`. One code fence around it is fine.
  Anything else is "could not check".
- Clean up with `rm -rf /tmp/zoom-out`.

## Reporting

- Show every blocker and major to the operator, in plain words, next to the part of the artifact it names.
- No blocker and at least one cited ref: "the zoom-out review found no blocker". Otherwise list the blockers.
- Majors are advice; they are not counted (version 1 counted them and failed sound designs).

## Rules that stop self-scoring

- The author never edits, drops or re-words a finding.
- Fix the artifact, then run the reviewer again at most once, and report both answers, not only the clean one.
- A finding you think is wrong stays in the report, with your reason beside it. The operator settles it.
- Never tune the prompt on the artifact you are reviewing. Prompt changes go through a new calibration round
  (`calibration/method.yaml` in the lens folder).
