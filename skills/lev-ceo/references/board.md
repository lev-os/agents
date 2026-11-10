# The board: JP answers on his phone

The board is the phone's view of what waits on JP: `.lev/now/ceo-board.json`, drawn as choice cards in the Waits-on-you view of `.lev/now/entity-explorer.html`. A tap lands in the answers file (`.lev/pm/decisions/20261104-ceo-board-return-channel.yaml`). Use it when JP asks for it or works from his phone. `board.mjs` is `scripts/board.mjs`; run it in the Lev checkout.

## Put the waits on the board

1. **Fresh read first.** Before a wait becomes a card, read that chat's newest messages (`references/sweep.md`, step 4). Drop the wait when JP already answered it there.
2. **Write the items** to `~/.local/state/lev/ceo-board/items.json`, one for each For you item and each chat that waits on JP:
   - `id`: a short slug of the wait. `title`: the question in plain words.
   - `thread_link`: the chat's `link` in the v2 form, `t3-thread://v2/<environment id>/<thread id>`.
   - `what`: one or two sentences. `choices`: the chat's own choices, plus at most one "Talk first". Never a question the chat did not ask.
   - `recommended`: the id of your own pick. `since`: when the wait began; leave it out when you can't tell.
3. **Write the board:** `node ~/.agents/skills/lev-ceo/scripts/board.mjs write --input <items.json>`. Exit 1 prints one line per error and writes nothing: fix the items and run it again. A warning "board owner changes from X to Y" means you replaced another CEO's board: check that you meant to.
4. **Check the server:** `board.mjs check`. When `server.listening` is false, start it once as a background shell: `npx tsx plugins/now/src/cli.ts --serve --port 3456 --bind $(tailscale ip -4 | head -1)`. A server another session started stays as it is.
5. **Start one waiter** as a background shell: `node plugins/now/scripts/answers-wait.mjs --file <answers_file> --after <answers_lines> --timeout 3600`, both values from `check`. Its exit wakes you. The waiter fires once; it is a wait, not a loop.

Done when `check` shows `listening: true`, the board's `updated` is this turn's, one waiter runs, and the handoff names the waiter's background id and its `--after` count. With no wait on JP, write an empty list so old cards leave the phone, and start no waiter.

## Board answers

When the waiter exits:

1. Exit 0: `board.mjs answers --since <the waiter's --after count>`. Exit 2 means the timeout passed with no tap: go to step 4.
2. Act on each row by its `status`:
   - `fresh`: read that chat's newest messages first. When JP already answered there, send nothing and note it in the handoff. Else `t3_thread_send` to the item's chat with the text `JP (board): <label>`, plus ` · note: <note>` when there is one. The `threadId` is everything after `<environment id>/` in the link, used as written. He tapped that text, so it is text he approved.
   - `stale`: the card changed after his tap. Act on nothing and ask again in the reply.
   - `unknown_item`: the card left the board. Act on nothing and name it in the reply.
   - `cleared`: he took the tap back. When its answer already went out, send `JP (board): withdrawn`.
3. A `fresh` row that settles a ruling: write its decision file with `decided_by: JP`, `decided_at` the row's `at`, and his label and note as his words. When JP's own answer in the chat differs from the tap, the chat answer is the ruling.
4. Write the board again without the answered items, then start a new waiter with `--after` the `lines` that `answers` printed.

Done when every row has its action, the board's `updated` is this turn's, and one new waiter runs (or none, when the board is empty).

## Commands

- `board.mjs write --input <items.json> [--project <name>] [--server <url>]`: checks every item, builds the explorer page, then moves the page and the board into place together.
- `board.mjs answers --since <line count | ISO time with zone> [--items <items.json>]`: the newest tap for each item; `lines` is the next waiter's `--after`.
- `board.mjs check`: whether the server listens, the answers file and its line count. Reads only.
