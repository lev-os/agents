# Explain: ADHD visual mode (default) and sizes

ADHD visual mode is the default layout of every `/explain` answer. `--plain` selects the prose report in `SKILL.md` instead. The mode changes the layout only. Scope, sources, decision discipline and ASD-STE100 stay the same.

Source: no installed ADHD skill exists. The Codex catalog lists `i-have-adhd` (smrik) with this intent only: concise paragraphs, a clear next action, manageable steps and visible progress. Its body is not available. This leaf is our own design from that intent and the neurodivergent-support patterns in `leviathan/workshop/poc/skills/domains/axioms/docs/ux-patterns.md`: numbered steps, progress indicators, breakpoints and a summary first.

## Layout

1. **Answer line.** One bold sentence of at most 20 words. It says the result, not the topic.
2. **One visual next.** Show the shape before the words: a status strip (✅ 🟡 ⬜ ⛔), a small table, an arrow chain (`A → B → C`) or a Mermaid diagram if the surface renders it. In a plain terminal, use a table or an arrow chain.
3. **Chunks.** At most 3 chunks (5 in `lg`). Each chunk starts with an emoji and a short bold heading. Each chunk has 1 to 3 bullets, with the key word of each bullet in bold. Use one level of bullets only.
4. **Risk line.** If a caveat changes what the reader does, put it on its own line that starts with ⚠️. Never drop a caveat to save space.
5. **Your move.** End with one line: `👉 Your move:` plus one next action and its owner, or `👉 Nothing needed from you.`
6. **More.** Put extra detail in a collapsed `<details>` block if the renderer supports it. If not, end with `More: say "expand".` Do not add detail past the size budget.

Rules:
- Put blank lines between chunks. A prose paragraph has at most 3 lines.
- Show progress as a bar with one segment for each named milestone. Do not invent a percentage.
- Put decisions for the reader first, before background.
- Keep exact strings, numbers, owners and links. A short link next to the claim is enough.
- A visual must show a relation, a state or an order. Do not add one for decoration.

## Sizes

A size token selects the word budget. It applies to every mode, including `--plain`. Count prose words only. Table cells, diagrams and code do not count.

| Token | Budget | Shape |
|---|---|---|
| `xs` | about 40 words | Answer line, then at most 3 bullets. A visual only if it is a one-line status strip. |
| `sm`, `short` | about 120 words | Answer line, 1 visual, at most 5 bullets. |
| `md` (default) | about 300 words | Answer line, 1 or 2 visuals, at most 3 chunks. |
| `lg`, `long` | about 600 words | Answer line, 2 visuals, at most 5 chunks. |
| `xl`, `full` | about 1000 words or more | Full coverage. Every chunk can open under `<details>`. |
| `--size <N>` or `<N>w` (for example `200w`) | about N words | Pick the nearest shape above. |

A bare number stays the conversation count (`/explain 5` reads 5 conversations). Use `--size 200` or `200w` for a word budget. Read a size token anywhere in the arguments: `/explain sm`, `/explain xs closeout`, `/explain --teach lg <topic>`.

## Check before you send

- Can the reader say the result after reading only the answer line and the visual?
- Is there exactly one next action, or a plain statement that none is needed?
- Did the size budget hide a cause, a caveat or a required step? If yes, keep the item and cut background instead.
