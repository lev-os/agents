# Checks for this skill

Load this file before you edit this skill (`SKILL.md` §8).

**A rule lives in the skill.** When JP rules on how a CEO node works, write the whole rule into the skill in its own words, at the step where an agent acts on it, and keep the reason in one short clause when the reason changes what an agent does. The decision record keeps the history (`SKILL.md` §6); the skill never tells an agent to read, open or load one, by path, by id or by title. `citations.mjs` fails on a path into the decisions folder, in `SKILL.md`, `references/` and `scripts/`. No program finds an id or a title, so read your edit again for one. Text that only one branch needs goes in a file of `references/`, and `SKILL.md` names it in Contents with each place that loads it. A load condition is written once, in `SKILL.md`; a reference file that names its own must use the same moments.

After the edit, run all three:

```bash
node --test ~/.agents/skills/lev-ceo/tests/*.test.mjs                    # settle, citations, audit, board, queue, sweep
node ~/.agents/skills/lev-ceo/scripts/citations.mjs --root "$(git rev-parse --show-toplevel)"   # exit 0: every cited file exists, and no decision record is cited
node ~/.agents/skills/lev-ceo/tests/fresh-agent-settle.mjs               # a fresh agent with only SKILL.md picks the script's chats
```

`tests/queue.test.mjs` proves the queue order (priority, then age; the presented head stays), the allowed moves, the two cadences and one event line per change. `tests/sweep.test.mjs` proves the choice for each chat of the all-projects index (`references/sweep.md`, The wider sweep): a chat is asked once, a CEO chat never, a wrong list is refused, `--project` shows one project, no choice is stored, a second command that writes is refused while one holds the lock, each sample of an odd JSON value in each field of an input file gives exit 0 or 2 and stops no later command (a matrix of samples), a chat whose id holds a tab, a line break or a leading `--` goes through scan, merge and queue (a round trip), the program starts no process (a run under Node's permission system), a pinned chat keeps its pin in its row and is never left out for its age, and `queue` keeps one open item for each chat whose newest reply holds a question for JP, until a person closes it or the chat is settled. `scripts/audit-transcripts.mjs` counts what CEO sessions did (ticks that changed nothing, settle orders, repeated questions) from their transcripts.
