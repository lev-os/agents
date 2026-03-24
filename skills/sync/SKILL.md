---
name: sync
description: Sync the local repository with the remote repository, ensuring that all changes are up to date and conflicts are resolved.
---

# Sync it all

For all submodules and the root repository, run the following commands to ensure that everything is up to date:

Syncing a repo:
1- `git add .`
2- `git status` > craft simple commit message
3- `git commit -m {commit message}`
4- `git pull origin {currentBranch}`
5- if conflicts, resolve if trivial, otherwise launch exploration subagents and ask user for help

Caveats:
- You need to do 1-5 for all submodules first, then do 1-5 for the root repository. This is because submodule changes need to be committed and pushed before the root repository can be updated to point to the new submodule commits.
- If there are conflicts in the submodules, you will need to resolve them before you can update the root repository. This may involve launching exploration subagents to help understand the changes and how to resolve the conflicts.

I don't want to stop and deal w/ per submodule conflicts, and I don't want you making product/architecture decisions with merges.

Report the full status at the end:
- What you think the path forward is for any remaining conflicts, and what you need from the user to resolve them
- Or say "bingo bongo, everything is synced and up to date"





