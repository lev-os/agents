# Article synthesis: briefs, states, and controlled rendering

Use this reference when a film needs product facts, real product assets, seekable animation, long renders, hybrid footage, or several aspect ratios. It turns the useful production methods in the archived article into checks. The cited article is a source of ideas, not proof that its model, tools, APIs, prices, or performance claims are current.

## Contents

1. Source and limits
2. Write the production brief
3. Keep real assets distinct from concept screens
4. Tell the story with states
5. Make frames seekable and stable under blur
6. Put picture and sound on one clock
7. Respect host capture and render access
8. Gate long runs and critique with evidence
9. Use generate-then-trace only when it fits
10. Recompose each aspect ratio
11. Keep project records for the next run
12. The studio failure map
13. Keep archival anecdotes out of acceptance rules

## 1. Source and limits

The source is “Opus 5.5 Motion Design: What the Viral 'One-Prompt' Videos Are Hiding,” by seeco (`@seeconvm`), posted as an X article on 2026-10-02: [article](https://x.com/i/article/2106091215502422016). The fuller Brave/CUA capture is `provenance/article-browser.txt` (SHA-256 `d18fd804f7a4b35d34695394ea051faacc3ca8cc52a0e5df03e17659d6ec3c85`); capture metadata is in `provenance/article-browser.json`. The earlier plain-text capture is `provenance/article.txt` (SHA-256 `78bf38a28dcde0e3e43b54ae171a9552c43d46a8b12f5071ece53af2a3911211`). The archived `provenance/article-cover.png` is a decorative overview, not runtime or measured evidence. Line ranges below refer to `article-browser.txt` unless stated otherwise.

The earlier text capture omitted embedded material. The fuller browser capture recovers the `seek(t)` contract and studio table, plus the style-guide prompt, storyboard, state chain, spring expression, critique checklist, project layout, and six gates. The article mentions an XML prompt at lines 95–99 but does not provide an XML schema; treat only its visible state-chain example as source material. Do not invent missing syntax.

Article statements about model and tool behavior are attributed to the article only. They are not verified current APIs, product capabilities, or requirements. Its examples and reported outcomes stay in the archive; they do not set universal timings, scores, costs, or success rates. The install, package, model-selection, and CLI commands in the article are examples, not active setup instructions.

Choose a renderer from the task's requirements. The article reports that an installed framework was skipped in favor of a simple HTML route; package presence alone does not prove which engine a render used. Name a required engine in the brief and verify the actual output path. Creative values such as “something new every 2 to 4 seconds” are source suggestions, not universal gates.

## 2. Write the production brief

Before code or a full render, write a brief that turns the request into choices a reviewer can check. The article's compact fields are a useful base:

- **FILM**: one sentence the viewer keeps, audience, duration, and formats;
- **ASSETS**: real logo, real UI screenshots, brand type and colors, and audio;
- **VISUAL**: what to keep from a reference and which clichés to avoid;
- **HARD LINE**: never invent product screens or metrics;
- **DELIVER**: storyboard, contact sheet, final video, poster frame, and source when requested.

Add the factual source for each claim, missing assets and blockers, languages, audio rights, review captures, and stop conditions. Keep the person's explicit brief as the authority. If a required fact or asset is missing, name it as a blocker before rendering.

A one-line showreel prompt can test a rig or produce a low-stakes fictional study. It leaves too many decisions open for a product film, where claims and screens must be real.

Use [direction](direction.md) for the direction card and concept choice, [story and motion](story-and-motion.md) for the selling arc, and [pipeline](pipeline.md) for formats, language versions, cutdowns, longer films, and export to another engine. In the article's reference-led branch, prepare a style guide (palette, type, shot lengths, transitions, camera, texture) and a shot list from the reference's grammar; show both and wait for the requested approval before writing scene code. Do not add this approval pause when the person has already approved the direction and asks you to proceed. The source's “take the grammar, never the subjects, logos or copy” remains the rule.

## 3. Keep real assets distinct from concept screens

When the film represents a real product, use supplied or host-observed product screens, words, and numbers. Keep a source note for each important screen or claim. If a state cannot be seen in an approved source, request a screenshot or mark the screen as a concept. Never present an invented dashboard, result, review, or metric as a real product state.

A fictional screen can act as a film set when the brief asks for an explainer or fictional concept. Label it as a concept in the deliverable and keep it separate from evidence about a real product. “It looks plausible” is not evidence that the product has that state. A staged editor, timeline, waveform, or export button can give every element a known state; do not imply that this illustrative interface is the actual product.

## 4. Tell the story with states

For each beat, write three things: its entry state, its exit state, and its purpose for the viewer. Describe what changes in what the viewer sees or understands. Cut a beat that has activity but no purpose. A persistent shape or UI container can carry continuity across beats; each change should reveal a fact or move the story forward.

The article's illustrative 16-second beat sheet is: 0–2s hook (image that earns attention); 2–5s problem (friction shown); 5–9s reveal (real interaction); 9–13s proof (one screen or number); 13–16s close (clean state and readable CTA). Its example morph chain is logo → CTA button → typed email field → loader → success check → dashboard → chart → tooltip → command palette → toast → logo. Use these as examples only; keep each chosen beat's entry, exit, and purpose explicit. The referenced XML schema is not present in the capture.

Treat a loop as a requested delivery property. When requested, match the full visual state and motion across the seam. An end card, CTA, or silent ending is optional and belongs only when the brief calls for it. See [scene cookbook, loop end card](scene-cookbook.md#26-the-loop-end-card) for one optional construction.

## 5. Make frames seekable and stable under blur

Define one time function, `seek(t) -> frame`, that paints the requested time from declared inputs. Do not rely on a timer, accumulated drawing state, or the order in which frames were requested. In render mode, avoid CSS transitions, `setTimeout`, and `requestAnimationFrame`; use seeded noise rather than `Math.random`. For a value with changing targets, model the known target changes in the timeline and evaluate its spring response at the requested time. Do not restart a spring based on the last frame rendered; that makes backward and shuffled seeks disagree.

With motion blur, geometry can sample several times inside one output frame's shutter. Discrete text, counters, labels, and other frame-level values must use the output frame index divided by the output frame rate, so every subframe shows the same value. The fuller article gives this abstract retargeting expression: `track(t) = v0 + Σ (v_i − v_(i−1)) × spring(t − t_i)` (lines 101–107). Here each `t_i` is a target-change time and `v_i` a target value; the expression is not a drop-in API or a complete spring specification. Use the selected engine's defined response and verify arbitrary seeks.

Check the same times in forward, reverse, and shuffled order. Compare rendered pixels or computed visual properties, not only DOM markup. If the selected engine cannot seek independently, state that limitation and do not claim deterministic seeking.

## 6. Put picture and sound on one clock

When the person supplies a track, use it as the timing source: inspect its BPM, first beat, and meaningful drops before setting scene cues. Keep cuts, state changes, and effects aligned to that measured timeline. Do not replace supplied music with a newly composed score by default. Compose an original score only when the brief needs one and no supplied track is selected, or the person asks for it. If rights or the requested use are unclear, ask before replacing or embedding the audio.

The article proposes aligning interface changes to beats, major moments to downbeats, and effects to visible hits; its example analyzer reports BPM, beats, downbeats, and hits (lines 108–113). Use an approved local analyzer when available, then follow the supplied track and the person's timing direction. Do not install the article's example dependencies by default. The detailed supplied-track and original-score branches are in [sound design](sound-design.md#4-when-the-user-names-a-sound-or-brings-a-track).

## 7. Respect host capture and render access

For external websites, use the host's CUA browser or an approved connector to observe the page and capture permitted assets. Preserve the useful outputs—source notes, screenshots, sections, logo candidates, font metadata, and palette samples—in the project. Do not use `site-kit`, `ui-shot`, or URL-downloading scripts to bypass host browser rules, login boundaries, site controls, or access limits. If a page blocks capture or an asset is missing, ask for the supplied screenshot or file. Follow the user's required browser for local `file://` URLs; use Brave when the active instructions require it.

The commands in the pipeline reference describe available project interfaces. They do not grant authority to execute them. Run browser-based capture or rendering scripts only when the current task authorizes the render and the host permits that browser technology. Follow CUA policy even when a project script offers another route. Do not copy the article's package-install commands or `.env` key example into active setup; use existing tools and the host's approved secret handling, and never expose keys in prompts or output. If execution is unavailable, keep the plan and evidence requirements, then report the exact blocked operation.

## 8. Gate long runs and critique with evidence

Set checkpoints before a long render: freeze the brief and asset list; inspect the reference; capture one representative test frame; review the beat map or animatic; approve the key look and story; then render full quality. Stop at a missing required asset, an unclear reference, or a test frame that shows the wrong direction. Fix those before producing many finished frames.

Declare a finite number of critique passes for the task. Each finding should point to a time or frame and state the visible defect. The article proposes one frame per beat for an initial contact sheet before showing work (lines 39–54). Its later QA examples are a contact sheet at 2 frames per second and 6 columns, a 12-frame strip around the fastest move, a 360-pixel-wide phone view, playback of the loop twice, and hashing the same rendered frame twice (lines 114–130). Adjust sampling to the film so it includes every important state and transition. A pass may prioritize the three worst defects, as the article's example does; re-render affected times and record whether they are fixed. The article's 1–10 scores and “8+” rule are not acceptance gates; use the brief and evidence, and preserve unresolved findings.

For sustained work, the article's six gates are a useful sequence: (1) approve references and product assets; (2) approve the style guide and shot list; (3) critique stills for every shot; (4) review a 960×540 animatic; (5) render a full pass, then polish picture and sound; (6) check requested formats and loop join, export a poster frame, and update the readme. The article uses placeholder audio at gate 4. Use the exact supplied track or voice when the brief requires it; never use placeholder audio when the person or task says no placeholders. A placeholder is allowed only when the brief permits it and it cannot be mistaken for final audio. No gate permits bypassing host policy or proceeding past a missing required asset.

## 9. Use generate-then-trace only when it fits

Code rendering suits typography, product UI, data stories, and other deterministic graphic scenes. For photoreal scenes, complex characters, or organic physical motion, use supplied footage or consider a separately approved generated-video path. For a film that needs organic character motion or physical action, a hybrid branch can start with generated base footage and redraw or trace a graphic layer over it. The article describes this as a way to keep a code-drawn visual style over generated character footage (lines 151–152). Treat it as optional, not a required tool or an automatically available service. The article names one model and one repository as anecdotes; it does not establish their present availability or behavior.

Choose this branch only when the person asks for or approves generated footage and the source, rights, and disclosure are clear. Preserve the base footage and derived overlay as separate inputs. Review the composite for identity drift, invented product evidence, visual mismatch, and continuity. If parallel chapter work is authorized, give each worker a bounded chapter and disjoint files; the article cites `ANIMATION_GUIDE.md` for that handoff, but its example does not itself authorize delegation.

## 10. Recompose each aspect ratio

Derive each requested aspect ratio from the same story and cue timeline, then recompose its layout. Do not call a crop a responsive version. Vertical layouts usually need larger type and fewer elements; square layouts may need tighter holds; wide layouts can use more spatial context. These are starting choices from the article, not fixed rules.

For every version, check text size, safe areas, source facts, CTA, pacing, and transitions at the intended display size. Keep the semantic beat timing shared unless the brief requests a different edit. The full format and cutdown workflow is in [pipeline](pipeline.md#7-formats-and-platforms).

## 11. Keep project records for the next run

Keep the decisions where the next authorized run can read them, not only in chat. The article's example separates a brief, style guide, shot list, approved assets, source composition, review evidence, and one output per format (lines 131–141). Adapt those records to the project's existing layout in [pipeline](pipeline.md#1-project-layout); this example does not require a new directory schema. The article's one-line prompt includes a URL, duration, aspect ratio, and local reference (line 155); treat it as a prompt example, not a registered command. A one-line invocation can be a later convenience after its defaults, inputs, and stop points are explicit.

## 12. The studio failure map

| Failure described in the article | Operative correction |
|---|---|
| Frames drift and edits restart the work | Seekable time function, seeded inputs, no timers (§5). |
| The renderer cannot inspect its output | Capture and review only through host-permitted tools (§7–8). |
| Safe defaults fill every blank | Production brief with approved assets and hard lines (§2–3). |
| Separate films share the same look | Reference-derived style guide; preserve grammar, not source identity (§3). |
| Effects have no story | Beat states with entry, exit, and viewer purpose (§4). |
| Motion feels weightless or sound floats over it | Retargeted springs and a shared measured timeline (§5–6). |
| The first render becomes the final | Finite evidence-based critique, then bounded repairs (§8). |
| Each project starts from zero | Durable brief, source, review, and delivery records (§11). |

### Judgment checks

| Notice | Why | Test | Bad → good | Exception |
|---|---|---|---|---|
| Product facts or fixed deliverables drive the film | Open choices produce unsupported defaults | Map every claim, asset, format, and blocker to the brief | Vibe prompt → source-linked production brief | One-line prompt for an explicitly fictional rig test |
| A frame represents a real product | Plausible fiction can misstate the product | Each screen and number has a supplied or host-observed source, or a concept label | Invented dashboard → approved screen or labeled concept | Fully fictional concept, clearly labeled |
| A beat changes what the viewer sees or knows | Effects alone do not tell a story | State entry, state exit, and purpose are written | “Add particles” → a named state change with viewer purpose | Abstract loop still needs a deliberate state pattern |
| Frames may be requested out of order or blurred | Hidden state makes output drift | Render repeated times in shuffled order; hold discrete values at output-frame time | Accumulated animation → `seek(t)` with seeded inputs | Sequential-only engine, with the limit reported |
| Music or voice is supplied | Replacing it changes the user's timing and intent | Measure beats and build cues from that source | New score by default → supplied track as timing source | User asks for an original or replacement track |
| A site or browser renderer is involved | Host access rules control capture and execution | Check task authority and host CUA policy first | URL scraper → host CUA capture; unauthorized render → report blocker | Code browser only when host and task both permit it |
| A render will run beyond a short sample | Missing inputs multiply wasted work | Record each gate's evidence before starting the next | Full render with missing screenshots → gated stills and animatic | Unattended run only when specifically authorized and still gated |
| Several aspect ratios are requested | Cropping can hide text or change emphasis | Inspect the final layout at each target ratio | Reuse one crop → recompose from shared story and cues | Exact crop when requested |
| The delivery must loop | A forced ending can damage the loop | Compare first/last visual and audio state | Mandatory end card or silence → seamless direct join | Add CTA/outro only when the brief asks for it |

## 13. Keep archival anecdotes out of acceptance rules

The archived article includes attributed stories about model effort settings, long prompts, overnight runs, creator names, view and bookmark counts, API use, costs, turnaround, commercial services, repositories, and reported results. These remain archival source claims in `provenance/article-browser.txt`, principally lines 6–8, 25–38, 55–86, 95–100, 107–116, 142–157, and 220–233. Do not use them as current model facts, universal budgets, quality thresholds, or proof that a workflow succeeds. The article's source/rig commands do not authorize installing dependencies, accessing keys, or invoking a named model.

Use the reproducible checks in the selected project and the user's acceptance criteria. See [pipeline](pipeline.md#10-qa) for delivery QA and [wow library](wow-library.md#1-the-bar-in-numbers) for source-sample ranges, which are heuristics rather than universal acceptance limits.
