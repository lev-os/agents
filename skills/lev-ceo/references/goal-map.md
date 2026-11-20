# The goal map

The goal map says what JP builds, where and why: his long-horizon goals, the end state of each, the chats that serve it, and the laws each answer respects. It comes before any list of questions. Each answer to a chat flows from it.

JP 2026-11-20: "what i want to see instead of a list of 30 questions sometimes is what the fuck am i building, where, and why? what is the actual end state of all these chats? grouped semantically around long horizon product goals". And: "u need to be able to tell me that, and it matches what i actually think, then all the answers flow from that WITH the constraints of the architecutre/ux". He accepted the example below the same day: "nope that's pretty much perfect. encode this into the ceo skill".

Records: `.lev/pm/decisions/20261120-jp-wants-the-goals-and-end-states-of-all-chats-before-a-list-of-questions-and-each-answer-flows-from-them-inside-the-architecture.yaml` and `.lev/pm/decisions/20261120-jp-accepts-the-goal-map-and-the-ceo-skill-holds-the-method-that-makes-it.yaml`.

## Files

| File | What it is |
|---|---|
| `~/.local/state/lev/ceo/goal-map/goal-map.json` | The live map of this machine. You change it; `scripts/goal-map.mjs` draws and checks it |
| `references/goal-map-example.json` | The map JP accepted on 2026-11-20. Copy its form, its plain words and its size. Never show it as today's map |
| `scripts/goal-map.mjs` | `render`, `check`, `ids`; its header gives the file's form |

## When

- JP asks what he builds, where a chat fits, what the end state is, or says "goal map", "zoom out" or "the big picture".
- Before a sheet of questions, and before you write an answer to a chat in his voice.
- The first turn after compaction: read the live map before you read the queue.
- A tick reports an open chat with no place on the map.

## How to make or refresh it

Do the steps in this order. The order is the method: start from the goal, never from the questions.

1. **List the chats with a program.** `node ~/.agents/skills/lev-ceo/scripts/list-chats.mjs --projects <projects json> --out <threads json>`. Read no chat yet.
2. **Take each product's purpose from its own page, in its words.** For Lev: `docs/NORTH_STAR.md`, then `docs/VISION.md`. For another project: the first paragraph of its `README.md`, then its goal or vision page. Quote the line that says what the product is for. A chat's title, its questions and its handoff are not a source for the goal.
3. **Write the goals.** A goal is an outcome that stays true for months, in plain words: "An agent never loses its way". It is never a box, a package or a task: "finish the daemon" is not a goal. Lev gets three to six goals. Each product is one goal until JP splits it.
4. **Write the end state of each goal.** One to three sentences that say what is true when the goal is reached, in the present tense. Where a box is often misused, say what it does and what it does not: "The daemon keeps listed processes alive and does nothing else."
5. **Mark whose words each end state is.** Set `source` to the page it is from ("its readme page"), to "your words in those chats", or to "my reading". Then read the product's page and replace your reading with its words where they exist. JP corrects what is still marked as your reading.
6. **Place each chat on one goal, by the outcome its work serves.** Do not place it by its project or its title: `multiplayer > swift helper decomposition` serves the goal "each thing has one owner". A chat you cannot place from its title: read its last reply with `scripts/chat-tail.mjs`, then place it. Run `goal-map.mjs ids`, then `goal-map.mjs check`: it must exit 0.
7. **Write the laws.** At most seven, from the project's guide files (in Lev: section 3 of the root `AGENTS.md`, "The model in ten lines"). Each law is a short name and one sentence. A law is a constraint of the architecture or the UX that an answer may not break.
8. **Write one worked example** of a chat whose goal is named after a box, beside the goal it should have. Take a chat that JP has named as going wrong.
9. **Draw and show it.** `node ~/.agents/skills/lev-ceo/scripts/goal-map.mjs render --map <map json> --out <html>`, then `html_preview` and `html_render`. Under the page, say which end states are your reading and ask one thing: is this what you are building?
10. **Record his correction** as a decision, change the live map, and draw it again.

## How an answer flows from it

Before you answer a chat's question, or write the card for it:

1. Find the chat's goal and end state on the map.
2. Name the law that the question touches.
3. Ask if the work is a priority now. JP names what is not ("some things are not priority like daemon in the menu, mac sync"); a goal or a chat that is not a priority is marked on the live map in its name ("· later") and its answer is parked, not sent.
4. Answer what moves the work to the end state inside that law. When the chat's choices all miss the end state, give the end state and not a letter (`references/sweep.md`, the bullet on an answer in JP's voice).
5. When the chat works for its box and not for the goal, the answer starts with the goal card below.
6. Before you recommend an owner for a thing, test the owner yourself; never pass on a chat's recommendation. Say what the thing is in one sentence with one verb, and say the same of each box that could own it. A different verb is a different owner: core/poly binds an action to its surfaces (a map), and a gateway listens and lets a call in (a running process), so poly does not own the gateway. "The box already has a folder for it" is the law "code that exists is evidence of an intent", not a reason. On 2026-11-20 the CEO chat recommended core/poly as the owner of the gateway from the daemon chat's design, and JP answered: "no, poly is not a gateway, ur doing it again...". When no box that exists has the verb, the thing gets its own owner, and its name is JP's to rule.
7. Before the send, manage its blast radius (`references/sweep.md`, the bullet on the blast radius): priority order, a small wave, limits in the message.

## The sequence: three bands

JP 2026-11-20: "Given all our goals, u need to also be able to sequence things properly" and "Foundation and mvp are really the focus, i just want the future to be known so we dont paint ourselves in a corner" (`.lev/pm/decisions/20261120-jp-says-foundation-and-the-mvp-are-the-focus-the-future-is-designed-and-not-built-and-caller-proof-is-not-in-the-mvp.yaml`).

Before you answer a chat or send a wave, put the work in one band. Take the band from the project's own records, never from the chat's words.

| Band | What is in it | In Lev, read | What the answer says |
|---|---|---|---|
| Foundation | The steps that make the base work as intended | `.lev/pm/plans/20261110-foundation.yaml`, each step's `status` | Finish the step. Name what it still needs to be verified, and nothing more |
| MVP | The items marked for the first version | `.lev/pm/roadmap/backlog.yaml`, `mvp: true`; the board data `.lev/now/backlog.json` gives each item's stage | Build it, in the order of the backlog |
| Future | Everything else: `mvp: false`, or in no record | The same file | Design it, with options and prior art, so that today's build does not block it. Build nothing |

- A chat that builds in the future band while the foundation or the MVP is open is drifting. Say so, with the backlog item that proves it, and steer it to a design turn.
- State the MVP's assumptions in the answer when they remove work. For Lev's MVP: one machine, a contained network, no proof of who the caller is.
- When JP asks if a band is done, count from the records in this turn and say how old the board data is. Rerun no check for a count.
- Send in band order: foundation first, then MVP, then a design turn for the future, one small wave at a time (`references/sweep.md`, the bullet on the blast radius).

## The goal card

A goal card is what a chat is told about its place:

```text
Goal: <the goal's name>. End state: <the end state>.
Your part: <what this chat's work adds to the end state>.
Your box: <what the box does>. It does not: <what belongs to another owner, and to which one>.
Laws: <the laws that apply, by name>.
For each piece of code, first ask who owns it. If the owner is not your box, the work goes there.
```

A goal card goes to a chat only on JP's word, like each other send.

## What keeps it

- The tick runs `goal-map.mjs check` each time (`references/index-tick.txt`). An open chat with no place is a problem line, and you place it in your next turn.
- A chat that closes leaves the map at the next refresh (`check` lists it under `gone`).
- When JP changes a goal, an end state or a law, the change is a decision record, and the live map changes in the same turn.
- When JP accepts a new cut of the map, save it as the new `references/goal-map-example.json` and commit it.

## Example

The accepted map of 2026-11-20 is `references/goal-map-example.json`. Draw it with `goal-map.mjs render` to see it. Its form:

- Top row: You, then Lev, then the products Lev builds.
- Lev, five goals: (1) a core where each thing has one owner; (2) an agent never loses its way; (3) done means checked, not said; (4) one seat for you; (5) Lev is out, and people know why.
- The products, six groups: Multiplayer, Suntiq, Survival, the workshop, Kingly Legal (later), the NAAC record (not a product).
- Seven laws: one owner; an action, not a command; name it by what it is; code that exists is evidence of an intent; done means a check ran; it works in any project; less code.
- The worked example, the daemon chat. Its goal today: "Finish the daemon", so each missing thing becomes a daemon job. The goal it should have: "Lev's background parts stay alive, and each part lives where it belongs."
