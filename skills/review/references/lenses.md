# Lenses

The one list of thinking and review lenses for every global skill. A lens is an angle: the question the reader asks. A
stance is who the reader is (cold reader or attacker, in the review skill's SKILL.md); a lens never names a stance. A
skill names the lens ids it uses and keeps its own rules about how it uses them; it never copies this list.

- `use: think`: the author generates with the lens. The review router never dispatches a `think` row.
- `use: review`: a fresh reader, who did not write the artifact, checks it with the lens.
- `use: both`: either way.

Calibration: only `zoom_out` has a calibration round: calibrated on test designs; advice only
([zoom-out.md](zoom-out.md)). Every other lens is advice.

## Methods

| id | Question | use | Review checklist |
|---|---|---|---|
| `zoom_out` | Does it fix the root problem, in the simplest way, by reusing what exists? | review | Run it as [zoom-out.md](zoom-out.md) says; never copy its prompt. |
| `pre_mortem` | It failed six months from now: why? | both | Three failure stories; each names how we would detect it and the mitigation. |
| `devils_advocate` | What would a hostile senior engineer say? | review | Senior critique; an untested edge case; 10x scale; a production break; a deferral we will regret. Usually run under the attacker stance. |
| `first_principles` | Which needs are real, and what is the simplest build from them? | both | Each requirement traces to a need, not a habit; a simpler build was tried and rejected for a stated reason. |
| `systems_thinking` | Which loops, stocks and delays does this change? | think | |
| `second_order` | And then what happens? | both | The effect after the first effect; who adapts, and how. |
| `opportunity_cost` | What do we give up to do this? | think | |
| `reverse_brainstorm` | How would we make this fail or make it worse? | both | Each way to fail maps to a guard or to an accepted risk. Usually run under the attacker stance. |
| `jobs_to_be_done` | Which job does the user hire this for? | both | The user, the job, the moment they hire it, and what they fire. |
| `expert_dissent` | Where would a domain expert and a software or science expert disagree with this? | both | One dissent for each field, with its evidence. |
| `falsification` | Which observation would prove this wrong? | both | Each decisive claim names the observation and the verifier that can show it false. |
| `karpathy` | What does the real data show? | both | Claims cite real inputs and outputs that someone looked at, not summaries. |
| `trade_off` | What does each option win and lose? | think | |
| `six_thinking_hats` | Facts, feelings, risks, benefits, ideas, process: what does each say? | think | |

## Personas (think)

The author speaks as the persona to force a frame (pov Turn 1).

| id | Frame |
|---|---|
| `figure_storming` | A named figure handles the problem in their own way |
| `10x_dev` | The fastest builder: what to cut, what to automate |
| `elon_musk` | Delete parts, then question the requirement |
| `sam_altman` | Scale, timing and compounding |
| `buffet_bezos_dimon` | Capital, the long term, and the customer |
| `einstein_turing` | A thought experiment; what can be computed |
| `jesus_gandhi_god` | Ethics, care, and who is harmed |

## Idea wizard (think)

The idea skill's Five-Fold Path. The idea skill owns the table, its order and its emoji.

| id | Question |
|---|---|
| `evolution` | How did this come to be? |
| `impact` | What problem does it uniquely solve? |
| `relationships` | How does it connect to everything else? |
| `essence` | What is the one fundamental truth? |
| `paradigm` | What assumption does it challenge? |

## Review methods

Full procedures that a skill owns. They are advice, like the lenses.

| id | Owner | What it checks |
|---|---|---|
| `adversarial_validation` | cdo debug, T7 | A fresh validator tries to break a fix: the reproduction, edge cases, regressions, cause or symptom. PASS or FAIL only. |

## Which stance and lenses for which artifact

"Author" rows are the author's own thinking; no reader runs them.

| Artifact | Caller | Stance | Lenses |
|---|---|---|---|
| Plan or slice | lev-plan, propose | Light: cold reader. Standard: cold reader, then attacker. Deep: both, plus `pre_mortem`. | `zoom_out`; deep adds `pre_mortem` |
| Long brief | horizon | Attacker (its `red_team` step), then cold reader | `zoom_out` |
| Architecture | arch | Cold reader; attacker when the review passes too easily | `zoom_out`, `first_principles`, `second_order`, `devils_advocate` |
| Design from an interview | interview | Cold reader | `zoom_out`, `jobs_to_be_done`, `pre_mortem` |
| Design review loop | arch, interview | Author | `first_principles`, `systems_thinking`, `pre_mortem`, `jobs_to_be_done`, `reverse_brainstorm`, `expert_dissent` |
| Plan enrichment | auto-enrich | Author, privately | `pre_mortem`, `jobs_to_be_done`, `reverse_brainstorm`, `expert_dissent` |
| pov conclusion | pov | Cold reader | `zoom_out` |
| Idea | idea | Author | `evolution`, `impact`, `relationships`, `essence`, `paradigm` |
| Debug fix | cdo | Attacker | `adversarial_validation` |
| Running behaviour | exec, close, a direct request | Attacker: [hostile-run.md](hostile-run.md) | none |
