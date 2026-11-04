# Roll-up: close a run into one idea folder

A roll-up closes out a run of threads and lanes into one idea folder: a narrative, an index of what exists, and links out. It is an idea record plus its folder, with no new record type and no new skill (`.lev/pm/decisions/20261014-rollup-folder.yaml`, JP's ruling: an idea at `.lev/pm/ideas/<slug>/idea.yaml` plus files in that folder; no `.lev/pm/rollups/` folder, not a workstream).

A roll-up with a time window ("roll up the last 24h", "roll up today") is a Catch-up over that window (`SKILL.md` §7 Catch-up), not this procedure.

## Inputs

The orphan threads, lanes, handoffs, captures, decisions, backlog items and evidence folders in the current scope (`SKILL.md` §2). An orphan is a thread or lane with no capture, no handoff row or no follow-up.

## Steps

1. **Sweep.** List every input in scope: the thread sweep (`SKILL.md` §1, steps 6-10), the lanes, and `ls -t .lev/pm/handoffs/*.yaml`. Done when each input has a row with its link or path.
2. **Capture the orphans first.** For each orphan thread or lane, write a capture of what it holds into its owning workstream and `git add` it by path. Done when no orphan lacks a capture.
3. **Log what moved.** Each ruling found goes into its decision file; each "add to the MVP" or "do later" becomes one row in `.lev/pm/roadmap/backlog.yaml`. Refresh the backlog and the pages it renders through the lev-roadmap skill. Done when every decision and backlog ask has a file or a row.
4. **Write the idea folder.** `.lev/pm/ideas/<slug>/idea.yaml` plus files in that folder:
   - the Catch-up narrative at the top (`SKILL.md` §7 Catch-up);
   - an index of what exists, with counts from commands run this turn;
   - the prior art;
   - links to the architecture docs and to tracking (workstreams, decisions, backlog rows).
   Done when every input from step 1 appears in the index or the narrative.
5. **Archive and close on JP's word only.** Experiment folders go to the archive when JP says so. Archive means `git mv` into an archive folder; remove nothing (`SKILL.md` §5 Keep records). Lanes and T3 threads close only on his word, in the close order of `SKILL.md` §4.
6. **Commit** the captures, decisions, backlog rows and the idea folder by explicit path through lev-lore-commit.
7. **Reply.** A Catch-up that names the folder path; a Result when the roll-up closed things.

## Publish

When JP says "publish" or "now page", render the idea folder with the now skill and send the URL.

## Done when

No orphan thread lacks a capture, no lane lacks a follow-up row, `backlog.yaml` is refreshed, and the idea folder is committed by path.
