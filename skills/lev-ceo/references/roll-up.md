# Roll-up: close a run into one idea folder

A roll-up closes a run of chats and lanes into one idea folder: a narrative, an index of what exists, and links out. It is an idea record plus its folder, with no new record type (`.lev/pm/decisions/20261014-rollup-folder.yaml`: an idea at `.lev/pm/ideas/<slug>/idea.yaml` plus files in that folder).

A roll-up with a time window ("roll up the last 24h") is a Catch-up over that window (`references/catch-up.md`), not this procedure.

## Steps

1. **Sweep.** List every chat, lane, handoff, decision, backlog item and evidence folder in scope (`references/sweep.md`; `ls -t .lev/pm/handoffs/*.yaml`). Mark each orphan: a chat or lane with no row in a handoff and no follow-up. Done when each input has a row with its link or path.
2. **Classify the orphans first.** For each orphan, write the records of what it holds (`AGENTS.md` rule 1): its rulings, its ideas, its backlog asks. Done when no orphan holds something no record has.
3. **Log what moved.** Each ruling goes into its decision file; each "add to the MVP" or "do later" becomes one row in `.lev/pm/roadmap/backlog.yaml`. Refresh the backlog through the lev-roadmap skill.
4. **Write the idea folder,** `.lev/pm/ideas/<slug>/idea.yaml` plus files in it:
   - the Catch-up narrative at the top;
   - an index of what exists, with counts from commands run this turn;
   - the prior art;
   - links to the architecture docs, workstreams, decisions and backlog rows.
   Done when every input from step 1 is in the index or the narrative.
5. **Settle** your own finished chats with the settle script (`SKILL.md` §4). Moving a folder to an archive is JP's call (`SKILL.md` §6): `git mv`, and remove nothing.
6. **Commit** the records and the idea folder by explicit path through the lev-lore-commit skill.
7. **Reply** with a Catch-up that names the folder path.

When JP says "publish" or "now page", render the idea folder with the now skill and send him the link.

Done when no orphan holds an unrecorded ruling, `backlog.yaml` is refreshed, and the idea folder is committed by path.
