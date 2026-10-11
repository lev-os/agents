# Explain: Code tour route

`--code <path or module>` makes a **guided tour**: one `/now` page file with
several pages, next and back, that walks the reader down the four C4 levels
(context, containers, components, code) until they can change the code with
confidence. The tour is a durable file, so this route overrides "deliver in
chat". It reads the target; it never edits it.

Load these skills before you design a page: `now` (the renderer and its
component list), `archify` (diagrams), `arch` (the judgment on patterns and
gaps), `writing` (the last pass on every sentence). Load `ux` only when the
reader or the page order is unclear.

## Steps

1. **Bound the target.** Resolve the path to one package, module or folder.
   Record the commit (`git rev-parse --short HEAD`) and whether the target has
   unsaved changes. Ask one question only when the path matches nothing.
   Done when: the target, the commit and the dirty state are written down.

2. **Read it, level by level.** Use the project's code-graph tools first, then
   read the files. Collect, with `path:line` for each item:
   - Context: what the target is for, who calls it, what it depends on.
   - Containers: what loads or runs apart (entry points, handlers, commands,
     the data it reads and writes).
   - Components: the 6 to 10 modules that carry the design, and who calls whom.
   - Code: the 5 to 8 functions a change is most likely to touch.
   Done when: every item has a line reference you opened yourself this session.
   A note from a subagent or an index is a lead, not a reference.

3. **Judge it** with the `arch` skill, one area at a time. For each area name
   the **pattern** in use, the **gap** (a risk, a duplicate, a surprise), and
   one or two **other patterns** that fit, each with its tradeoff. A gap needs
   evidence at a line; a taste is not a gap. Say "no gap found" when true.
   Done when: every component page and every code page has all three.

4. **Order the pages.** One idea per page, one screen of reading, about 8 to 14
   pages for a package:
   - 1 Start here: what the reader can do at the end, the map of the tour, the commit.
   - 2 to 3 Context. 3 to 4 Containers. Then one page per component group.
   - One page per load-bearing function.
   - Last two: all gaps in one table, ranked; then "change it safely" (the
     checks to run, the files that move together) and what was not read.
   Each page has, in this order: a two-sentence claim, one diagram or one
   snippet (not both unless the snippet explains the diagram), then pattern,
   gap, other patterns. End each page with one prediction question whose answer
   is the next page's first line.
   Done when: a reader can stop on any page and say what that page proved.

5. **Draw the diagrams.** Write each as Mermaid in the page: `flowchart` for
   context, containers and components, `sequenceDiagram` for a call path. Keep
   a diagram under 12 nodes; split a larger one across two pages. For the one
   or two diagrams the reader will explore (usually containers and
   components), also make an archify file from the same facts
   (`node bin/archify.mjs deliver ...` in the archify skill) and save it beside
   the tour as `<slug>-<diagram>.html`. Link it from the page with an `action`
   of variant `link`.
   Done when: every diagram node names a real file, package or function.

6. **Cut the snippets.** Copy the lines from the file; never retype them. A
   snippet is 5 to 25 lines. Put `path:start-end` in `filename`, set
   `startLine` to `start` so the rows show the file's line numbers, and list
   the lines that matter in `highlightLines` (file line numbers, or `'a-b'` ranges). Name those
   lines, and why, in the text under the snippet.
   Done when: `sed -n 'start,endp' path` prints each snippet exactly.

7. **Build the RenderSpec** at `.lev/now/<slug>-tour.json` in the project:
   - root: one `section` of variant `sidebar`.
   - its children: one `navigation` (variant `list`; `group` is the C4 level,
     `badge` is the page number), then one `section` per page with
     `props.route`, then one `navigation` (variant `pager`) with the same items.
   - a page's children are ordinary components: `text`, `diagram`,
     `code-block`, `data-table` (pattern, gap, other patterns), `card` variant
     `callout` for the prediction question, `action` for links.
   Render with the command in the `now` skill, then open the HTML.
   Done when: the render command exits 0 and the file opens.

8. **Rewrite for a person** with the `writing` skill. The reader is one
   engineer who must change this code next week. Replace each label with the
   plain sentence it stood for, keep every identifier and number exact, and
   cut any sentence that the diagram or the snippet already says.
   Done when: no fact, name, number or line reference changed in the rewrite.

9. **Check the tour**, then report. Open every page by its link; use next and
   back from the first page to the last; confirm that each diagram drew; run
   the `sed` check of step 6 for every snippet. In chat give: the file path,
   the page list, the three gaps that matter most, and what you did not read.
   Done when: each check has its command or observation beside it.

## Rules

- Evidence beside the claim: every claim about the code carries `path:line`.
- The tour describes the commit of step 1. Say so on page 1; a dirty target is
  marked "moving".
- Reuse the `now` components. Reach for `custom-html` only for an interaction
  that no component gives.
- `--code` composes with the other flags: `--teach` adds retrieval practice
  to each level, `--levify` maps the target to its Lev owner and layer.
