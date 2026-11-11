## Horizon Brief: 20261104-node-mise-and-stageshow-retest

Intent: one Node setup (mise) on both Macs in place of nvm and Homebrew's Node, then a 3-run retest of stageshow against Impeccable.
Source: JP 2026-11-03 "/goal ... 1 · Run the Node plan ... 2 · Retest stageshow ... /horizon and keep it updated as u go"; the plan in the skill-consolidation reply of 2026-11-03 (steps 1-7); decisions `~/.agents/.lev/pm/decisions/20261103-creative-hub-after-trial.yaml` (2a: 3-run retest, longer budget). Intent IDs INT-1 (Node on this Mac), INT-2 (Node on MacBook), INT-3 (keep caches), INT-4 (qmd works), INT-5 (retest).
Plan: plan_not_required: two bounded machine and trial runs; this brief is the plan and is kept current as work goes.
Ledger: this brief's stage rows (no Lev task folder).
Run: long (two stages, several hours); limits: no Leviathan writes except reads; no here.now; no force-push; never delete caches; JP stop wins.
State: disk: this file; confidence medium; blocker none.

### Status (updated as work goes)
| Time (UTC) | Stage | State | Evidence |
|---|---|---|---|
| 2026-11-04 03:45 | S0 survey | done | see Findings |
| 2026-11-04 04:20 | S1 this Mac | done; all S1 rows pass after the last edit | `sh /tmp/s1-check.sh` output in chat; chezmoi 0326671f. mise 2026.11.0, Node 24.22.2; 13 global tools reinstalled (npm 11 needed `--allow-scripts` for agent-browser, agent-desktop, oh-my-codex, open-computer-use, keytar, node-pty, sharp, esbuild); brew node, node@24, nvm, repomix removed; caches kept (npm 11G, pnpm 5.8G, bun 7.3G) |
| 2026-11-04 04:20 | S1 side finds | noted | demo host had been running from a deleted worktree: remade `~/digital/multiplayer-worktrees/demo-server` (detached, origin/main e55105b16) and restarted it. simlock gateway exits silently when started through the `installs/node/24` link: its job points at the real `24.22.2` folder, so a Node patch update needs `simlock daemon install` or a path edit. Old global tools under `/opt/homebrew/lib/node_modules` stay until T3 restarts, because running sessions find CLIs there |
| 2026-11-04 04:10 | S2 MacBook | done; all S2 rows pass after the last edit | `sh /tmp/s2-check.sh` over ssh. Before: qmd failed from `sh -c` ("node@24 is not installed"), two Nodes on PATH. After: one mise Node 24.22.2 everywhere; qmd answers (17,681 files); simlock worker, Multiplayer relay (HTTP 200 on :4610) and bridge (registered with kingly-multiplayer.fly.dev as jp-macbook-claude, jp-macbook-codex) run on mise Node. Global tools: the old nvm 24 set plus the Homebrew-npm set, installed at latest (several newer than before, for example gemini 0.38 to 0.66) |
| 2026-11-04 04:10 | S2 side finds | noted | Restart exposed two dormant faults: `/opt/homebrew/bin/pnpm` was gone (brew pnpm 12.16.1 installed), and `~/Library/pnpm` is root-owned since 2024 (both services got `PNPM_HOME=~/.local/share/pnpm`; a `sudo chown` would fix the folder). The relay also needed `pnpm install --frozen-lockfile` in `apps/multiplayer` (packages from Oct 17). Brew `node` stays installed but unlinked, because `birdclaw` is hard-wired to it. `~/.nvm` (7.3 GB) kept for a week. MacBook Leviathan is 151 commits behind (not touched). Launchd backups in `~/.local/state/launchagents-bak-20261104/` |
| 2026-11-04 04:40 | S3 batch 1 (r1-stageshow, r1-impeccable, r2-stageshow) | done | each run folder has its files; worker times 24, 12 and 24 min |
| 2026-11-04 04:55 | S3 batch 2 (r2-impeccable, r3-stageshow, r3-impeccable) | done | S3-files: no file missing across 6 runs (`/tmp/retest-prep.mjs`); 30 digests frozen in `frozen-digests.txt` before grading |
| 2026-11-04 05:03 | S4 grading and page | done; returned | S4-verdicts: 9 pairs x 2 orders in `grader-p.json`, `grader-q.json`; `verdicts.json`: Impeccable 6, stageshow 0, tie 3 (all ties are heroes). Averages stageshow / Impeccable: designed 3.50 / 4.33, fidelity 3.44 / 4.78, craft 3.11 / 4.11, clarity 3.83 / 4.39. Page `~/.local/state/lev/skill-trials/20261104-stageshow-retest/results.html` opened in Brave. Blind check: no arm name in any blind file name |

### Return (2026-11-04 05:03)
Every S1, S2, S3 and S4 row passed after its last edit. Open for JP, not blocking this goal:
- Hub routing for mock product shots, now that the retest favours Impeccable (decision `20261103-creative-hub-after-trial`, mock_product_shots).
- Done 2026-11-11 (JP: "kill those agent browser sessions ... then finish this task"): old Homebrew global tools moved to the Trash on both Macs. Before the move: stopped the leftover agent-browser processes (MacBook 2390 and 31901, running since Oct 30), and on Mac Studio an orphan agent-device daemon, an old simlock daemon and an old TypeScript language server; reinstalled agentmail-cli 0.7.1, claude-code-router 3.0.6, monid cli 0.1.6, pi-interview 0.8.7 and vercel 55.0.0 under mise Node on the MacBook. Mac Studio: 14 links to `~/.Trash/homebrew-bin-links-20261111/`, the folder (632 MB) to `~/.Trash/homebrew-node_modules-20261111`. MacBook: 10 links and every entry except `npm` (1.1 GB) to the same Trash names; birdclaw 0.13.0 still runs. After the move all commands resolve to mise in `zsh -lc` and `sh -c` and run; `qmd status`, `claude --version` and `codex --version` pass on both.
- MacBook: `sudo chown -R` on `~/Library/pnpm` done by JP 2026-11-03 (checked: owner jean-patricksmith, 0 files owned by anyone else); move `~/.nvm` to the Trash after 2026-11-11 (T3 scheduled task "MacBook ~/.nvm to Trash on 2026-11-11", Wednesdays 10:00); birdclaw: JP 2026-11-03 "yea stay outta there". Homebrew `node` stays installed and unlinked; birdclaw calls it by full path.
- `~/.zshenv` on this Mac holds two plain-text X login tokens (not in chezmoi); the MacBook never had them. JP 2026-11-03 "remove the tokens on both machines": the command guard blocks the edit, so JP runs the delete line. JP 2026-11-04 "2b" (stop relying on bird): `LAST30DAYS_HOST=grok-bot` in `~/.config/last30days/.env` on both Macs (official sources only: X API, then xAI, then xurl; doctor reports "will use: xai"); the MacBook's xAI key copied into that file; xurl 1.3.4 installed on both and added to chezmoi `dot_default-npm-packages` (27bf492b). 2026-11-04: bird uninstalled on both Macs (JP "3 yea"); MacBook Python 3.13 from mise, MacBook only (JP "2 a", chezmoi 0dff962f; last30days doctor runs in zsh -lc, zsh -ic and sh -c). X Bearer Token stored: Mac Studio keychain `last30days-X_BEARER_TOKEN`; MacBook `~/.config/last30days/.env` (owner-only; its keychain is locked over ssh); xurl app-only on both. doctor: "will use: xapi". Live search answers 403 client-not-enrolled: the app must be attached to a Project with API access (credits) in the console. Waits on JP.

### Findings (S0, this Mac, 2026-11-04)
- `node` = Homebrew 26.12.1; also Homebrew `node@24` (for qmd) and an unused Homebrew `nvm`; `~/.nvm` absent; `.zshrc` sources a missing `~/.nvm/nvm.sh`.
- Leviathan `.nvmrc` = 24; `package.json` engines `node >=24`. So this Mac runs Leviathan on 26, not the pinned 24.
- Global npm packages under `/opt/homebrew/lib` (12): @google/gemini-cli, agent-browser, agent-desktop, agent-device, mobile-use, npm, oh-my-codex, open-computer-use, pi-interactive-shell, simlock, typescript-language-server, typescript.
- Homebrew formulas that need Homebrew `node`: repomix. pnpm (Homebrew, 11.7.0) and bun are standalone.
- Running launchd jobs that use Homebrew Node: `ai.kinglystudio.multiplayer-demo-host` (`/opt/homebrew/bin/node`), `com.callstack.simlock.gateway` (`/opt/homebrew/Cellar/node/26.12.1_1/bin/node` + `/opt/homebrew/lib/node_modules/simlock`). levd runs on bun. Five unloaded jobs point at a dead `~/.nvm/.../v22.16.0` (already broken; not touched).
- This session's hook `~/.claude/hooks/shell-shape-guard.mjs` runs `node` from PATH; `~/.local/bin` is 2nd on PATH.
- Caches: `~/.npm` 10 GB, pnpm store 5.8 GB, `~/.bun` 7.3 GB. MacBook: `~/.npm` 48 GB, `~/.nvm` 7.3 GB (8 versions).
- Machine load 21-30 at survey time.

### Definitions
- One Node: `which -a node` lists only mise paths (the shim, and the `~/.local/bin` link to it); no Homebrew or nvm node.
- mise shims: `~/.local/share/mise/shims`; they pick the version from `.nvmrc` or the global default at run time, with no shell hook, so launchd, GUI apps, hooks and `sh -c` see the same Node.
- Caches kept: `~/.npm`, the pnpm store and `~/.bun` keep their size within normal drift (never emptied).

### Success Predicate
On both Macs, every shell kind (interactive zsh, `sh -c`, launchd) gets Node 24 from mise, Leviathan's `node -v` prints v24, the 12 global tools and repomix run, the two launchd jobs run on mise Node, qmd answers `qmd status` from `sh -c`, no Homebrew node/node@24/nvm formula is installed, caches are kept; and the retest returns blind verdicts in both orders for all 9 pairs (3 runs x hero still, hero video, bento), shown on a results page opened in Brave.

### Does Not Count
- mise installed but Homebrew node still first on PATH somewhere (S1-path).
- Only interactive zsh checked (S1-path checks `sh -c` and launchd).
- A launchd job that "loads" but crashes (S1-jobs checks the process and its log).
- qmd checked only in a login shell (S1-qmd).
- An emptied cache (S1-cache compares sizes).
- MacBook "done" from this Mac's checks (S2 reruns every row over ssh).
- Retest with fewer than 3 runs per arm, a changed brief, or graders who see arm names (S3, S4).
- A worker's own "looked at frames" taken as craft proof (graders decide).

### Stages
| Stage | Artifact | Rows (proof) | Rules out | Known-bad input | Waits on |
|---|---|---|---|---|---|
| S1 this Mac | mise + node 24; `~/.local/bin/{node,npm,npx}` links; zsh files; chezmoi commit | S1-path: `which -a node` in zsh, `sh -c`, `env -i` + launchd PATH (command) | a second Node | today's output lists 2 paths | none |
| | | S1-repo: `node -v` in Leviathan = v24 (command) | wrong pin | today prints v26.12.1 | S1-path |
| | | S1-tools: each global tool `--version` (command) | tools lost with brew node | — | S1-path |
| | | S1-jobs: both launchd jobs running with mise node in `ps` (command) | dead services | — | S1-tools |
| | | S1-qmd: `sh -c 'qmd status'` exits 0 (command) | qmd on wrong Node | — | S1-path |
| | | S1-brew: `brew list` has no node, node@24, nvm (command) | leftovers | today lists 3 | all S1 rows |
| | | S1-cache: cache sizes vs Findings (command) | lost caches | — | S1-brew |
| S2 MacBook | same over ssh; `mise sync node --nvm` | S2-* = S1-* rows over ssh | second-machine drift | today: 2 nodes on PATH | S1 |
| S3 retest | `~/.local/state/lev/skill-trials/20261104-stageshow-retest/runs/r{1,2,3}-{stageshow,impeccable}/` | S3-files: every run has b1-still.png, b1-demo.mp4/webm, b2-bento.png, notes.md (command) | missing outputs | — | S1 (node) |
| S4 grading | blind/{p,q}, verdicts.json, results.html | S4-verdicts: 9 pairs x 2 orders (command count) + graders' answers (review) | order bias | an order-dependent pair = tie | S3 |

### Review
Checklist: PATH order per shell kind; launchd jobs with hard-coded paths; native modules (qmd better-sqlite3, node-llama-cpp) on a matching ABI; brew dependents; blind folders free of arm names.
Blocks when: any S1/S2 row fails; any blind file name or content names an arm.
Outside-loop proof: command rows above; graders answer craft.

### Repair
Recall: the failing stage; cap 2 tries per row; at cap stop and report the exact gap to JP.

### Return
Return when every row above passes after the last edit, and results.html is open in Brave.
Incomplete only on JP stop, MacBook unreachable, or worker budget out; report the strongest verified state.

### Resume
Frontier: see Status table; next unit is the first row not marked done.

### Open Branches
- Five unloaded launchd jobs on a dead nvm path (clawdbot, pm2, apple-testerd, oracle): left as found; owner JP.
- Hub routing after the retest: only if the retest changes the picture; owner JP.

### Fidelity and Route
| Intent ID | Source ref | Brief destination | Ledger row | Preservation | Route / blocker |
|---|---|---|---|---|---|
| INT-1 | plan steps 1-7 | S1 | S1-* | preserved | exec now |
| INT-2 | JP "check my mackbook via ssh" | S2 | S2-* | preserved | after S1 |
| INT-3 | JP "preserve the cache if possible" | S1, S2 | S1-cache | preserved | — |
| INT-4 | JP "no wonder i had so much trouble w/ qmd" | S1, S2 | S1-qmd | preserved | — |
| INT-5 | decision 20261103 2a | S3, S4 | S3-files, S4-verdicts | preserved | after S1 |

Next: resume S1.
