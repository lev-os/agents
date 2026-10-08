# Explain: Teach route

`--teach` applies the method of Matt Pocock's Teach skill inside Explain. This
route loads no other skill: the method and the course workspace contract live
in this leaf, and the four workspace file formats are upstream copies under
[teach/](teach/) with one relative link repointed.
Upstream: https://github.com/mattpocock/skills/tree/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/teach
(MIT; see [teach-LICENSE.txt](teach-LICENSE.txt)).

## Contents

- [Apply the method to the requested surface](#apply-the-method-to-the-requested-surface): every `--teach` request
- [Standalone course mode](#standalone-course-mode): an explicit request for a durable course
- [Source preservation](#source-preservation): what was kept from upstream
- `<teach-batch>`: the inline lesson template

## Apply the method to the requested surface

Use the mission and existing understanding from the conversation. Ask one
substantial question only when these cannot be established. Build a mental map
from point A (what is unclear) to point B (one demonstrable ability), with all
material topic branches, prerequisites and unresolved choices. The topics are
that map's nodes, not an unrelated syllabus.

Use tools/skills in your environment for speed and efficiency. Inspect available
rendering and feedback tools and load their instructions. For an in-chat lesson,
use embedded visuals when available, otherwise inline Mermaid or a requested
local lesson. For a durable lesson/course, use Now or the user's established
surface with the standalone course mode below. Use Sites only for an explicitly
requested website. The active user's surface and persistence instructions govern:
an inline lesson does not initialize MISSION.md, NOTES.md or a course at the repo
top level. Keep learning notes in conversation unless durable records are requested.

Teach in 2-3 short stanzas per concept batch: section/description, a concrete
worked example and visual, then one prediction, classification or retrieval
question with immediate feedback. Use 1-2 meaningful visuals in an ordinary
explanation or 2-3 in a batch that needs separate map, example and practice views.
Scale dynamically to breadth and interaction, not a fixed page template.

Disambiguate overloaded terms, look for conflating, do domain modeling, and
consolidate real aliases before layering abstractions. Separate sources,
constructions and hypotheses. When the evidence does not show which version is
newer or better, say so and leave that choice with the user. Give one primary
source per concept batch.
Teach-style difficulty comes from retrieving or applying an idea, not from dense
terminology. Use balanced answer choices. In chat, withhold a practice
question's answer until the user replies; the rest of the response may
continue. Learning remains unverified until the user demonstrates it.

## Standalone course mode

Enter only on an explicit request for a durable course, lesson files or
multi-session records, or when the user points at an existing teaching
workspace (a directory that holds `MISSION.md`). A wish to keep learning is a
reason to offer this mode, not to enter it. Before the first write, confirm the
workspace directory with the user; a project repository's top level is not a
teaching workspace. The workspace is stateful: read its files before teaching
and keep them current, because they carry the learning across sessions.

| File | Holds | Before writing, read |
|---|---|---|
| `MISSION.md` | Why the user is learning; grounds every lesson choice | [teach/MISSION-FORMAT.md](teach/MISSION-FORMAT.md) |
| `RESOURCES.md` | Trusted knowledge sources and wisdom communities, with named gaps | [teach/RESOURCES-FORMAT.md](teach/RESOURCES-FORMAT.md) |
| `GLOSSARY.md` | Canonical terms, added once the user can use them | [teach/GLOSSARY-FORMAT.md](teach/GLOSSARY-FORMAT.md) |
| `learning-records/NNNN-slug.md` | Demonstrated understanding, stated prior knowledge, corrected misconceptions, mission shifts | [teach/LEARNING-RECORD-FORMAT.md](teach/LEARNING-RECORD-FORMAT.md) |
| `lessons/NNNN-slug.html` | One self-contained lesson per tangible win | Lesson rules below |
| `reference/*.html` | Printable quick-reference sheets: syntax, algorithms, routines, glossaries | Lesson rules below |
| `assets/*` | The shared stylesheet and reusable quiz, simulator and diagram components | Lesson rules below |
| `NOTES.md` | The user's stated teaching preferences and your working notes | Plain prose |

Mission first. If `MISSION.md` is missing or vague, interview the user about
why they want this before teaching; an ungrounded lesson feels abstract and
gives no basis for choosing what comes next. Missions change: confirm with the
user before changing one, then update the file and add a learning record.
Write a learning record only from the user's own evidence: an answer, a
completed exercise, or stated prior knowledge. Material that was only taught
stays pending, and a proposal never calls it demonstrated.

When the user names a topic, teach it. Otherwise read the mission and learning
records, then teach the most relevant thing in the zone of proximal development:
just hard enough. Knowledge comes before skill. For acquisition, difficulty is
the enemy, so include only the knowledge the target skill needs, cite a trusted
source for each claim, and draw on `RESOURCES.md` rather than parametric memory.
Until it is well populated, finding high-trust sources is the first job. Weigh
knowledge against skill by topic: theory leans on knowledge, a physical
practice on skill.

For practice, difficulty is the tool: retrieval, spacing and interleaving
(skills only) build storage strength, while fluent in-the-moment recall can
fake mastery. Practice is an interactive in-browser task or a guided sequence
of real-world steps, with immediate and, where possible, automatic feedback.
Quiz choices share one word count, and one character count where possible,
and carry no formatting clue.

Lesson rules: one tightly scoped win tied to the mission, short enough for
working memory, clean Tufte-like typography the user will want to revisit,
anchors to related lessons and reference sheets, one recommended primary
source, and a reminder that the user can ask follow-up questions. Read
`assets/` before authoring and build from its components; the shared stylesheet
is the first asset, and a new reusable piece becomes an asset rather than
inline code. Open the finished lesson with a CLI command when possible.
Reference sheets outlive lessons: keep them compressed, printable and current,
and use the glossary's terms in every lesson.

Wisdom comes from practice outside the workspace. Attempt the answer to a
wisdom question, then point to a high-reputation community where the user can
test the skill; respect an opt-out recorded in `RESOURCES.md`.

## Source preservation

Retained from Teach: mission, zone of proximal development, trusted sources,
knowledge before practice, retrieval/interleaving/spacing, tight feedback,
reference material and one tangible learning win. Its default standalone HTML
and workspace files are adapted to the user's explicit inline/dynamic surface
request. Standalone course mode keeps the upstream workspace contract and file
formats. Its explicit-only invocation remains intact: `explain --teach` is an
explicit request, not blanket permission for automatic sessions, writes or
publication.

<teach-batch>
Win: {what the reader will be able to distinguish or do}

Map: {present uncertainty -> topic branches -> observable learning outcome}

Concept: {plain explanation and source}

Example: {one concrete case + first visual}

Practice: {one prediction/classification + feedback interaction/second visual}

Next: {branch selected by demonstrated understanding; do not assume mastery}
</teach-batch>
