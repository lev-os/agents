# Loop: a timer that repeats, with an end

A loop is off until `setup.loop.on` is true or JP's words ask for one. Wakes that reload this skill are not a reason for a loop: `SKILL.md` §2 step 1 reloads from the handoff.

1. **Define it with the ll skill** (`~/.agents/skills/ll/SKILL.md`): the goal, what one tick does, the end time and the stop rule.
2. **Give it an end time.** `setup.loop.ends_at`, from the card or JP's words; 8 hours when he names none, 24 hours at most.
3. **Pick the timer.** In T3: `schedule_task` bound to this chat, with a prompt that runs one tick of the loop; it lives through a session restart. Elsewhere: the timer the ll skill makes, which ends with the session; write that in the handoff. Tick once an hour unless JP names another interval, and never more often than every 15 minutes. This one timer drives both queue cadences (`SKILL.md` §9 step 6): each tick runs `due` and does the refresh, the hygiene or both.
4. **Stop** at the end time, when the goal's check passes, after three ticks in a row with no progress, or when only items for JP remain. Delete the timer in that turn, set `setup.loop.on: false`, and tell JP in one line why it stopped.

Done when the handoff names the loop, its timer id and its end time, or names none.
