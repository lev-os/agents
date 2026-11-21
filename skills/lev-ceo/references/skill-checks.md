# Checks for this skill

**A rule lives in the skill.** When JP rules on how a CEO node works, write the whole rule into the skill in its own words, at the step where an agent acts on it, and keep the reason in one short clause when the reason changes what an agent does. The decision record keeps the history (`SKILL.md` §6); the skill never tells an agent to read, open or load one, by path, by id or by title. No program finds an id or a title, so read your edit again for one.

**One place for each rule and each load condition.** State a rule once; a second sentence that says it in other words is the fault to look for. A load condition is written once, at the step or the Router row that points at the file. The Contents table of `SKILL.md` says only what each file holds. Text that only one branch needs goes in a file of `references/`.

After the edit, run all three from the Lev checkout, then commit the skill's files in `~/.agents` (its own git repository) by explicit path:

```bash
node --test ~/.agents/skills/lev-ceo/tests/*.test.mjs
node ~/.agents/skills/lev-ceo/scripts/citations.mjs --pointers --root "$(git rev-parse --show-toplevel)"
node ~/.agents/skills/lev-ceo/tests/fresh-agent-settle.mjs
```

What `citations.mjs` checks:

- Each path in backticks in `SKILL.md` and `references/*.md` exists, and the first line of a cited line or range is inside its file. A `file.ext:line` written outside backticks is checked too. It skips a path with a pattern character (`< > { } * $ |` or a space), a runtime path (`~/.local`, `~/.config`, `~/.Trash`, `/tmp`) and a span that starts with no known folder. It does not read `references/*.txt`, `references/*.json` or `scripts/` for this. With files named on the command line, it reads only those files.
- No file of `SKILL.md`, `references/` or `scripts/` holds a path into the decisions folder, the bare folder path included. A pattern path that says where to write a record passes.
- With `--pointers`: each file of `references/` is pointed at: `references/<name>` in `SKILL.md` outside its Contents section or in another reference file, or a script line that holds `references` and the name. It does not check that a load condition is written once; read your edit for that.

The third command gives a fresh `claude -p` agent only `SKILL.md` and checks that it picks the chats the settle script picks. It runs on JP's subscription, so it is not a paid run in the sense of `SKILL.md` §7.

`tests/queue.test.mjs` proves the queue order (priority, then age; the presented head stays), the allowed moves, the two cadences and one event line per change. `tests/sweep.test.mjs` proves the choice for each chat of the all-projects index (`references/sweep.md`, The wider sweep): a chat is asked once, a CEO chat never, a wrong list is refused, `--project` shows one project, no choice is stored, a second command that writes is refused while one holds the lock, each sample of an odd JSON value in each field of an input file gives exit 0 or 2 and stops no later command (a matrix of samples), a chat whose id holds a tab, a line break or a leading `--` goes through scan, merge and queue (a round trip), the program starts no process (a run under Node's permission system), a pinned chat keeps its pin in its row and is never left out for its age, and `queue` keeps one open item for each chat whose newest reply holds a question for JP, until a person closes it or the chat is settled. `scripts/audit-transcripts.mjs` counts what CEO sessions did (ticks that changed nothing, settle orders, repeated questions) from their transcripts.

`tests/for-you-check.test.mjs` proves the form check of a question to JP (`scripts/for-you-form.mjs`): the two faults, the parts an item needs, the older heading "Your turn", that the file imports nothing (the stop hook mod continue-approved holds a copy, so copy the file to the mod's `hooks` folder after a change), and the exit codes of `scripts/for-you-check.mjs`.
