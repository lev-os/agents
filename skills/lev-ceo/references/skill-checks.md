# Checks for this skill

Load this file before you edit this skill (`SKILL.md` §8).

**A rule lives in the skill.** When JP rules on how a CEO node works, write the whole rule into the skill in its own words, at the step where an agent acts on it, and keep the reason in one short clause when the reason changes what an agent does. The decision record keeps the history (`SKILL.md` §6); the skill never tells an agent to read, open or load one, by path, by id or by title. No program finds an id or a title, so read your edit again for one.

**One place for each rule and each load condition.** State a rule once; a second sentence that says it in other words is the fault to look for. A load condition is written once, at the step or the Router row that points at the file. The Contents table of `SKILL.md` says only what each file holds. Text that only one branch needs goes in a file of `references/`.

After the edit, run all three from the Lev checkout, then commit the skill's files in `~/.agents` (its own git repository) by explicit path:

```bash
node --test ~/.agents/skills/lev-ceo/tests/*.test.mjs
node ~/.agents/skills/lev-ceo/scripts/citations.mjs --pointers --root "$(git rev-parse --show-toplevel)"
node ~/.agents/skills/lev-ceo/tests/fresh-agent-settle.mjs
```

What `citations.mjs` checks, and no more:

- Each path in backticks in `SKILL.md` and `references/*.md` exists, and a cited line is inside its file. It skips a path with a pattern character (`< > { } * $ |` or a space), a runtime path (`~/.local`, `~/.config`, `~/.Trash`, `/tmp`) and a span that starts with no known folder. It does not read `references/*.txt`, `references/*.json` or `scripts/` for this.
- No file of `SKILL.md`, `references/` or `scripts/` holds a path of a record in the decisions folder. A pattern path that says where to write a record passes.
- With `--pointers`: each file of `references/` is named by `SKILL.md` outside its Contents section, by another reference file, or by a script.

The third command gives a fresh `claude -p` agent only `SKILL.md` and checks that it picks the chats the settle script picks. It runs on JP's subscription, so it is not a paid run in the sense of `SKILL.md` §7.

`tests/queue.test.mjs` proves the queue order (priority, then age; the presented head stays), the allowed moves, the two cadences and one event line per change. `tests/sweep.test.mjs` proves the choice for each chat of the all-projects index (`references/sweep.md`, The wider sweep): a chat is asked once, a CEO chat never, a wrong list is refused, `--project` shows one project, no choice is stored, a second command that writes is refused while one holds the lock, each sample of an odd JSON value in each field of an input file gives exit 0 or 2 and stops no later command (a matrix of samples), a chat whose id holds a tab, a line break or a leading `--` goes through scan, merge and queue (a round trip), the program starts no process (a run under Node's permission system), a pinned chat keeps its pin in its row and is never left out for its age, and `queue` keeps one open item for each chat whose newest reply holds a question for JP, until a person closes it or the chat is settled. `scripts/audit-transcripts.mjs` counts what CEO sessions did (ticks that changed nothing, settle orders, repeated questions) from their transcripts.
