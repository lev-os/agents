# AI Slop Patterns — Complete Reference

## Table of Contents
- [The Underlying Mechanism](#the-underlying-mechanism)
- [Paraprosdokians & Melodramatic Antitheses](#paraprosdokians--melodramatic-antitheses)
- [Negative Parallelism Family](#negative-parallelism-family)
- [AI Vocabulary](#ai-vocabulary)
- [Copula Avoidance ("serves as" for "is")](#copula-avoidance-serves-as-for-is)
- [Significance & Legacy Inflation](#significance--legacy-inflation)
- [Superficial "-ing" Analysis](#superficial--ing-analysis)
- [Promotional & Travel-Guide Puffery](#promotional--travel-guide-puffery)
- [The Challenges / Future Outlook Formula](#the-challenges--future-outlook-formula)
- [Weasel Attribution](#weasel-attribution)
- [Rule of Three](#rule-of-three)
- [Elegant Variation](#elegant-variation)
- [Monotony & Rhythm](#monotony--rhythm)
- [Awkward Generic Analogies](#awkward-generic-analogies)
- [Filler](#filler)
- [Unearned Profundity & "Here's Why"](#unearned-profundity--heres-why)
- [Forced Enthusiasm](#forced-enthusiasm)
- [Vapid Openers & Transitions](#vapid-openers--transitions)
- [Unnecessary Hedges](#unnecessary-hedges)
- [Emdash Patterns](#emdash-patterns)
- [Formatting Tells](#formatting-tells)
- [Red Herrings](#red-herrings)
- [Anti-Slop Directives for Fresh Copy](#anti-slop-directives-for-fresh-copy)
- [Integration with Workflow](#integration-with-workflow)
- [When to Keep Patterns](#when-to-keep-patterns)

---

## The Underlying Mechanism

LLMs regress to the statistical mean: rare, specific, nuanced facts get replaced
by generic, important-sounding claims that could apply to anything. "Inventor of
the first train-coupling device" becomes "a revolutionary titan of industry."
**The subject becomes simultaneously less specific and more exaggerated.**

This is the single most useful diagnostic: if a sentence inflates importance
while containing no fact particular to this subject, it's slop. And it dictates
the fix: de-slopifying is not just deleting tics — it's reinstating the concrete
detail the slop displaced. When you cut "a testament to the enduring power of
collaboration," replace it with the actual fact, or with nothing.

---

## Paraprosdokians & Melodramatic Antitheses

The setup → clever reversal construction. Frontier models use it to manufacture
punchiness even when the subject doesn't warrant it. Especially common in
marketing copy and README taglines. Canonical examples:

- "Four steps, and only one of them is yours."
- "A thousand integrations, and you'll only ever click one."
- "Everything about billing changed. Your invoice didn't."
- "Ten features. Zero headaches."

**Fix:** Write straightforward copy. State what the tool does, how to use it,
and what it integrates with, without the dramatic pivot. If the reversal is
carrying the sentence, the sentence has no content; find the content and state it.

---

## Negative Parallelism Family

Contrast formulas that deny a strawman before stating the point. The output
reads as though it's clearing up a misconception nobody had:

| Pattern | Fix |
|---------|-----|
| "It's not X, it's Y" / "not a mirror but a portal" | "This is Y" |
| "It's not just X, it's also Y" / "Not only... but also..." | "This does X and Y" |
| "It's not about X, it's about Y" | Just explain Y |
| "doesn't just X — it Y" | State Y |
| "no X, no Y, just Z" | "Z" |
| "X rather than Y" (as a reflexive closer) | Usually just X |
| Cross-sentence: "...renowned for X. His life, however, took a path that..." | Merge into one plain statement |

The tell is that nobody claimed X. The denial exists only to make Y sound profound.

---

## AI Vocabulary

Statistically overused words. One occurrence is coincidence; several,
co-occurring, is one of the strongest tells. They cluster: where there is one,
there are likely others.

**Core list:** Additionally (sentence-initial), align with, boasts (meaning
"has"), bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance,
fostering, garner, highlight (as a verb), interplay, intricate/intricacies, key
(as an adjective), landscape (abstract), leverage, meticulous(ly), pivotal,
robust, seam (as in "prove the seam"), seamless, showcase, smoke-test, spine
(as in "the spine of the system"), tapestry (abstract), testament, underscore
(as a verb), valuable, vibrant, comprehensive (unearned).

Notes:
- The list drifts over time ("delve" peaked in 2023–24 and faded; "highlighting"
  / "showcasing" / "emphasizing" persist). Judge by density and co-occurrence,
  not by any fixed word.
- A word being overused does not make its synonyms suspect. And check context:
  "underscore" the character is fine; "underscores the importance" is not.
- Fix by substituting the plain word (delve → look at; boasts → has; leverage →
  use) or deleting the clause the word props up.

---

## Copula Avoidance ("serves as" for "is")

LLMs dodge plain "is/are." AI copyedits will "improve" text this way; reverse it.

| Tell | Fix |
|------|-----|
| serves as / stands as / functions as / operates as / acts as [a] | is |
| marks the / represents a | is, or state the event |
| boasts / features / maintains / offers [a] | has |
| holds the distinction of being | is |
| "began his career as" / "ventured into politics as a candidate" | was |
| "X refers to..." (defining lead) | "X is..." |
| "The Foo Library is a comprehensive toolkit designed to..." | "Foo does X." |

---

## Significance & Legacy Inflation

Puffing up importance by tying arbitrary facts to broader trends. Words to
watch: is a testament/reminder, a crucial/pivotal/vital/key role/moment,
underscores/highlights its importance, reflects broader, symbolizing its
ongoing/enduring/lasting, contributing to the, setting the stage for,
marking/shaping the, represents/marks a shift, key turning point, evolving
landscape, focal point, indelible mark, deeply rooted.

Variants:
- **Debate-situating:** "has generated debate about...", "prompted broader
  reflection on...", "raising philosophical questions about..."
- **Hedged importance:** conceding low importance, then asserting importance
  anyway: "Though it saw only limited application, it contributes to the broader
  history of early aviation engineering."
- Appears even for mundane subjects (etymology, population data, a config flag).

**Fix:** Cut the significance claim; keep (or add) the fact. "The v2 release
marks a pivotal moment" → "v2 fixes the three crash bugs reported since March."

---

## Superficial "-ing" Analysis

A present-participle clause bolted onto a sentence's end, adding fake analysis
of significance. Watch for trailing: highlighting..., underscoring...,
emphasizing..., ensuring..., reflecting..., symbolizing..., contributing to...,
cultivating..., fostering..., encompassing..., enhancing..., showcasing...,
demonstrating..., confirming its relevance..., cementing...

> "The station has supported express trains, contributing to the socio-economic
> development of the region."

Web-search-enabled models attach these claims to cited sources regardless of
whether the source says anything close; verify or cut.

**Fix:** Delete the clause. The sentence almost always survives intact.

---

## Promotional & Travel-Guide Puffery

Even when asked for neutral style, LLM output drifts toward ad copy or a travel
guide, using the same phrases regardless of topic. Words to watch: boasts a,
vibrant, rich (heritage), profound, exemplifies, commitment to, natural beauty,
nestled, in the heart of, groundbreaking, renowned, featuring, diverse array,
stunning, breathtaking, seamlessly connecting, dependable value-driven
experiences.

> "Nestled within the breathtaking region..., X stands as a vibrant town with a
> rich cultural heritage."

Newer models are subtler: fewer superlatives, same relentless positivity. In
tech writing this surfaces as "commitment to developer experience," "thoughtfully
designed," "powerful yet simple." **Fix:** State the property or delete the claim.

A related move is proving importance by enumerating coverage instead of stating
facts: "featured in [outlets]," "as seen in," "trusted by industry leaders,"
"maintains an active social media presence," award-and-recognition sections.
Either cite the one concrete thing the coverage said, or cut.

---

## The Challenges / Future Outlook Formula

A rigid closing template: "Despite its [praise], X faces several challenges..."
→ list → "Despite these challenges..." → vaguely positive assessment or
speculation about future initiatives. Section headers "Challenges and Legacy,"
"Future Outlook," "Future Prospects," and "X and Y" paired-noun headings
generally ("Awards and recognition").

The sign is the formula, not any mention of a real challenge. **Fix:** Keep the
one genuine limitation, stated plainly; delete the arc.

---

## Weasel Attribution

| Pattern | Fix |
|---------|-----|
| "Experts argue..." / "Observers have cited..." / "Some critics argue..." | Name the source or cut the claim |
| "Industry reports suggest..." | Cite the report or delete |
| "several sources/publications" (when few exist) | Count honestly |
| "researchers and conservationists" (unnamed interest) | Who, specifically? |
| "such as..." implying a longer list that doesn't exist | List what's real |
| Views of one source presented as widely held | Attribute to the one source |

---

## Rule of Three

LLMs overuse three-beat structures to make superficial analysis look
comprehensive: "adjective, adjective, adjective"; "short phrase, short phrase,
and short phrase"; "Think bigger. Act bolder. Move faster." Watch for lists
where every bullet ends in exactly three examples ("tiles, metals, and
plastics" / "outlets, switches, and fixtures" / "model making, woodworking, and
other craft projects" — the third often padded with "and other X").

**Fix:** Keep the claims that are true and specific; two honest items beat three
vague ones. Break the cadence.

---

## Elegant Variation

Repetition-penalty artifact: rotating synonyms to avoid repeating a term ("the
constraints of socialist realism" → "state-imposed artistic norms" → "the
artistic norms of their time"; "the tool" → "the utility" → "the solution").
In technical writing, repeat the term; variation makes readers wonder if two
names mean two things. (Caveat: some human writers, especially non-native
speakers taught to avoid repetition, do this too.)

---

## Monotony & Rhythm

- Sentences of near-identical length; paragraphs with identical shape; cadence
  that never varies. Vary sentence length; let some paragraphs be one line.
- Unnaturally consistent tense and point of view throughout — human writing
  drifts and shifts register occasionally.

---

## Awkward Generic Analogies

AI metaphors are plausible but generic — in the right ballpark, clearly not
thought through, gesturing at meaning without achieving it:

- "Learning the ukulele is like teaching your fingers to dance again."
- "Every chord is a puzzle piece that finally clicks into a song."
- "X is a mirror for learning itself: messy, slow, and quietly addictive."

Human metaphors are either highly specific (personal experience) or culturally
resonant (shared reference). **Fix:** Delete the metaphor, or replace with a
concrete comparison that actually holds up under a second read.

---

## Filler

Surface polish with nothing underneath — AI's signature. Two tests:

1. **The compression test:** Can this paragraph's content fit in one sentence?
   If four sentences carry one sentence of meaning, cut three.
2. **The throughline test:** Halfway through, can you say what the author is
   claiming? Words that individually make sense but don't accumulate into a
   point are filler; delete or rewrite around the actual claim.

---

## Unearned Profundity & "Here's Why"

| Pattern | Fix |
|---------|-----|
| "Here's why" / "Here's why it matters" | Explain directly |
| "Here's the thing" / "But here's the kicker" | Usually delete |
| "Here's what you need to know" | Just tell them |
| "Something shifted." / "Everything changed." (dramatic pivot sentences) | State what actually changed |
| Mid-sentence questions: "The solution? Simpler than you think." / "But now?" | State the solution |

---

## Forced Enthusiasm

| Pattern | Fix |
|---------|-----|
| "Let's dive in!" / "Let's get started!" | Just start |
| "Excited to share..." / "We're thrilled to announce..." | Just share/announce it |
| "Get ready to..." | Just tell them what to do |
| "...has never been easier!" | State how it works |

---

## Vapid Openers & Transitions

| Pattern | Fix |
|---------|-----|
| "In today's fast-paced world..." / "As technology continues to evolve..." | Delete; these say nothing |
| "At its core..." / "Fundamentally..." / "In essence..." | Usually delete |
| "At the end of the day..." / "When it comes to..." | Delete or recast |
| "Additionally, ..." starting successive sentences | Restructure; connect ideas for real |

---

## Unnecessary Hedges

| Pattern | Fix |
|---------|-----|
| "It's worth noting that..." / "It should be noted that..." | Just note it |
| "It's important to remember..." | Just state the fact |
| "Keep in mind that..." | Often deletable |
| "It goes without saying..." | Then don't say it |

Keep a hedge only when the caveat genuinely changes what the reader will do.

---

## Emdash Patterns

LLM output uses emdashes where humans use commas, parentheses, or colons, and
uses them formulaically to punch up clauses and parallelisms ("This isn't X —
it's Y"). AI emdashes are often surrounded by spaces ( — ), against typographic
convention.

| Original | Alternatives |
|----------|--------------|
| `X—Y—Z` | `X; Y; Z` or `X, Y, Z` |
| `The tool—which is powerful—works well` | `The tool, which is powerful, works well` |
| `We built this—and it works` | `We built this, and it works` |
| `Here's the thing—it matters` | Recast entirely |

One or two per document is normal human writing; several per paragraph is the
tell. Strongest in combination with other signs, weak alone (newer models
suppress emdashes, and professional human writers use them). Calibration: this
tell is about emdashes as prose punctuation. Leave dash/minus characters alone
when they do non-prose work: math formulas, code snippets, CLI flags, numeric
ranges (1–5), and table or list syntax.

---

## Formatting Tells

- **Inline bold-header bullets**: `- **Snappy Label:** explanation text` lists —
  the single most recognizable AI structure in READMEs and posts. Convert to
  prose or plain bullets unless the doc genuinely needs a glossary shape.
- Bold scattered on words with no emphasis logic; every instance of a chosen
  term bolded "key takeaways"-style.
- Emoji as bullets or section decoration (✅ 🎯 🚀 ✨) in professional text.
- Heavy bullet-list density where prose would flow better (RLHF loves lists).
- Title Case In Every Section Heading (use sentence case).
- Redundant title heading repeating the document's name at the top.
- Headings that contain only sub-headings, no body text; skipped heading levels.
- Horizontal rules between every section of a short document.
- Small tables for content that reads better as prose.
- Unicode styling: 𝗯𝗼𝗹𝗱/𝘪𝘵𝘢𝘭𝘪𝘤 letters, → arrows, × signs.
- Curly quotes/apostrophes mixed inconsistently with straight ones. (Weak alone:
  Word/macOS smart quotes produce them too.)

---

## Red Herrings

Do NOT treat these as slop on their own:

- Perfect grammar / zero typos (humans have spell-check and Grammarly)
- No contractions (house style, editing artifact, or ESL phrasing)
- A single "academic" word ("ascertain," "multifaceted") — professionals talk
  this way; density and co-occurrence are the signal, not presence
- Occasional emdash, one deliberate triad, one bold key term
- Output from an "AI writing detector" — these tools false-positive constantly;
  never cite one as evidence in either direction

And the inverse: text bearing several tells may still be human ("we contain
multitudes") — which doesn't matter here, since the goal is good prose, not
attribution. Fix the pattern, skip the accusation.

---

## Anti-Slop Directives for Fresh Copy

When writing new text (not just editing), apply these as constraints up front:

1. State the technical reality directly; no architectural metaphors for simple
   code, no "load-bearing"/"foundational tapestry"/"intricate dance."
2. No setup/reversal constructions in copy; describe function, usage, integration.
3. Open documents with content, not throat-clearing. First sentence = most
   useful fact.
4. Cultivate specificity: root claims in particular, verifiable detail (version
   numbers, measured results, actual behavior). Specificity is the one quality
   slop cannot fake, and the strongest positive defense.
5. No self-congratulation ("we're proud," "commitment to excellence") and no
   over-apologizing in changelogs or responses ("You're entirely right, thank
   you for your sharp eye"); acknowledge and state the fix.
6. Use rhetorical devices (emdash, triad, parallelism) only deliberately and
   rarely — the difference between a writer and a model is intention and dosage.

---

## Integration with Workflow

### As Part of Bead Workflow

```bash
br create "De-slopify README.md" -t docs -p 3
br create "De-slopify API documentation" -t docs -p 3
```

### As Final Pass Before Commit

```
Now, before we commit, please read through README.md and look for any telltale
signs of "AI slop" style writing...
```

### Files to Check

README.md, CONTRIBUTING.md, API docs, blog posts, landing pages, changelogs,
any public-facing text.

---

## When to Keep Patterns

- **Technical accuracy** — don't sacrifice correctness for style
- **Necessary structure** — headers and lists that organize real content are fine
- **Clear explanations** — being thorough isn't slop; filler is saying nothing at length
- **Code examples** — focus on prose, not code
- **Earned devices** — a device used once, deliberately, for real effect can stay
