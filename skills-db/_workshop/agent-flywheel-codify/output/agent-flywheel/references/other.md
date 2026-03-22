# Agent-Flywheel - Other

**Pages:** 7

---

## The Agentic Coding Flywheel

**URL:** https://agent-flywheel.com/complete-guide

**Contents:**
- The Agentic Coding Flywheel
- The Complete Workflow
    - Why the flywheel compounds instead of spinning in place
      - Intent
  - Glossary
- Why Planning Is 85% of the Work
    - Interactive: The Context Horizon
  - The Human Part
  - You Don't Need to Know Everything Upfront
  - Three Reasoning Spaces

A comprehensive guide to creating extraordinary software by orchestrating swarms of AI agents using exhaustive markdown plans, polished beads, and the Agent Flywheel stack. Based on the methodology of Jeffrey Emanuel.

This is the end-to-end methodology for creating software with frontier AI models, exhaustive markdown planning, beads-based task management, and coordinated agent swarms. Every project follows the same arc, whether it is a small CLI tool or a complex web application. This guide is about moving the hardest thinking into representations that still fit into model context windows. That is the whole game.

Step through the loop. The same project gets faster and safer because every completed cycle upgrades the artifacts feeding the next one. This is the compounding return on planning.

It starts with you. You have an idea for a piece of software. Maybe a web app, maybe a CLI tool, maybe a complex system. Instead of opening an editor and starting to code, you do something that feels counterintuitive: you spend the vast majority of your time planning.

That is the whole movie. For the CASS Memory System, this process turned a 5,500-line markdown plan into 347 beads. Twenty-five agents produced 11,000 lines of working, tested code with 204 commits in about five hours. You can see the actual plan, the actual agent mail messages, and the actual beads for yourself.

The frontier models and coding agent harnesses really are that good already. They just need this extra level of tooling, prompting, and workflows to reach their full potential. The rest of this guide zooms into each stage.

You spend 85% of your time on planning. The first time you try it, it feels wrong. No code is being written. Every instinct tells you to just start building. That discomfort is the signal that you are doing it right.

Why reasoning in plan-space dominates reasoning in code-space as projects scale.

A markdown plan, even a massive 6,000-line one, is still vastly smaller than the codebase it describes. When models reason about a plan instead of raw implementation, they can hold the whole system in their context window at once. Once you start turning that plan into code, the system rapidly becomes too large to understand holistically. You are doing global reasoning while global reasoning is still possible.

Planning tokens are far fewer and cheaper than implementation tokens. A big, complex markdown plan is shorter than a few substantive code files, let alone a whole project. That means you can afford many more refinement rounds in planning than in implementation. Each planning round evaluates system-wide consequences, not just local code edits. Each improvement to the plan gets amortized across every downstream bead and code change. Planning is the cheapest place to buy correctness, coherence, and ambition.

Without front-loaded planning, agents are effectively improvising architecture from a narrow local window into the codebase. That is exactly when you get placeholder abstractions, missing workflow details, contradictory assumptions, and compatibility shims that nobody actually wanted. With a detailed plan and polished beads, the models are no longer inventing the system from scratch while coding. They are executing a constrained, coherent design.

The human is not there to hand-author every line of the plan. The human is there to inject intent, judgment, taste, product sense, and strategic direction at the point where those qualities affect the entire downstream system. Once the plan is excellent, the rest becomes much more mechanical.

When prompting the model to create the initial markdown plan, you spend a lot of time explaining the goals and intent of the project and detailing the workflows: how you want the final software to work from the standpoint of the user's interactions. The more the model understands about what you're really trying to accomplish and the end goal and why, it can do a better job for you.

Debates belong in planning, not implementation. As many important disagreements as possible should happen before the swarm is burning expensive implementation tokens. Implementation can still surface surprises, but the posture of the workflow is to front-load decisions into plan space.

The most common objection to spending 85% of your time on planning: "I don't really know all the requirements at the beginning, and I need the flexibility to change things later." This is not at all in tension with the methodology. Thorough planning does not mean transcribing requirements you already know. It means using frontier models to discover requirements you never would have found on your own, iteratively, while changes are still cheap.

When you paste a rough concept into GPT Pro and ask for a comprehensive plan, the model surfaces dozens of edge cases, architectural considerations, and workflow details you had not thought of. When you show that plan to three competing models, each one finds blind spots the others missed. When you run five rounds of refinement, each round uncovers issues invisible in the previous round. By the time you start implementation, you know far more about your own project than you would have discovered through months of coding and refactoring.

This extends even further when adding major features to existing projects. You can point an agent at an entirely separate open-source project, have it study that project's architecture, and ask it to reimagine the strongest ideas through the lens of your own project's unique capabilities. Requirements emerge from the research itself. The methodology does not demand omniscience up front; it demands a willingness to let the models do deep, iterative exploration before committing to implementation.

The methodology separates work into three spaces, each with a different artifact and a different question it answers:

Inject the same mistake at different layers. The deeper it lands, the more downstream structure has already hardened around it. This is the Law of Rework Escalation.

Fixes are pure reasoning. Zero code churn.

Fixes rewrite orchestration. High coordination cost.

Fixes pay the double-tax: implementation + cleanup.

Planning earns its keep because it is the cheapest layer for global reasoning. Press 'Inject' on any layer to visualize the cost cascade.

Plan space is where you figure out what the system should be. Bead space is where you turn that into executable memory, a graph of self-contained work units detailed enough that agents don't have to keep consulting the full plan. Code space is where agents implement, review, and test locally. The key is knowing which space you're in: if you are still redesigning the product, stay in plan space. If you are mainly packaging the work for execution, move to bead space.

Before writing the plan itself, you need a coherent foundation. Think of it as assembling a foundation bundle: a tech stack decision, an initial architectural direction, a strong AGENTS.md file bootstrapped from a known-good template, up-to-date best-practices guides, and enough product and workflow explanation for the models to understand what "good" looks like.

Keep best practices guides in the project folder and reference them in AGENTS.md. These guides should be kept up to date; you can have Claude Code search the web and update them to the latest versions of your frameworks and libraries.

A strong bootstrap move is to start every new project by copying an AGENTS.md from an existing project that already has good general behavioral rules, safety notes, tool blurbs, and coordination guidance. Later, once the plan and beads are clearer, you ask agents to replace the project-specific content while preserving the general rules that carry across projects.

You don't even need to write the initial markdown plan yourself. You can write that with GPT Pro, just explaining what it is you want to make. Claude Opus in the web app is also good for this, but GPT Pro with Extended Reasoning remains the top choice for initial planning. No other model can touch Pro on the web when it's dealing with input that easily fits into its context window. It's truly unique. And since you get it on an all-you-can-eat basis with a Pro plan, take full advantage of that.

You usually also specify the tech stack. For a web app, it's generally TypeScript, Next.js 16, React 19, Tailwind, Supabase, with anything performance-critical in Rust compiled to WASM. For a CLI tool, usually Go or Rust. If the stack isn't obvious, do a deep research round with GPT Pro or Gemini and have them study all the relevant libraries and make a suggestion taking your goals into account.

A first serious markdown plan would not say "build a notes app." It would start spelling out the actual user-visible system:

That is still only the beginning. But it already shows the difference between ordinary brainstorming and Flywheel planning: the plan tries to make the whole product legible before any code exists.

For the best results, ask multiple frontier models to independently create plans for the same project. GPT Pro, Claude Opus, Gemini with Deep Think, Grok Heavy. Each comes up with pretty different plans. Different frontier models have different "tastes" and blind spots. Passing a plan through a gauntlet of different models is the cheapest way to buy architectural robustness.

In the CASS Memory System project, the competing plans are publicly visible. This pattern has been used across at least 10 sessions spanning 7+ projects.

Then show their competing plans to GPT Pro with this prompt:

GPT Pro web app with Extended Reasoning

Forces the model to be intellectually honest about what competitors did better, then synthesize a hybrid that is stronger than any individual plan. The 'best of all worlds' phrasing appears in 10+ distinct sessions across 7+ projects in the session archive. Under the hood, the prompt's length and specificity are deliberate: by asking for git-diff style changes, complete integration of every good idea, and explicit updating of the existing plan, it prevents the model from writing a vague summary and forces structural engagement with the competing plans' actual content.

Take GPT Pro's output (the git-diff style revisions) and paste it into Claude Code or Codex to integrate the revisions in-place:

Claude critically assesses each suggestion, providing a second layer of quality filtering. The 'wholeheartedly agree / somewhat agree / disagree' framing is load-bearing: it forces the agent to evaluate each revision on a gradient rather than accepting or rejecting the whole batch. You get signal about which changes are obviously good versus which are plausible but debatable, which lets you intervene on the edge cases rather than rubber-stamping everything.

Toggle proposal plans on and off, then drag the refinement dial. The point is not “many models” in the abstract; it is that complementary strengths plus fresh-round revision produce a plan that is harder to surprise later.

All proposal sources are active. Best-of-all-worlds.

Now paste the current plan into a fresh GPT Pro conversation with this prompt. The key word is fresh. Fresh conversations prevent the model from anchoring on its own prior output. Repeat 4-5 rounds:

GPT Pro web app — fresh conversation each round

This has never failed to improve a plan significantly. Each round finds architectural issues, missing features, and robustness improvements that the previous round missed. Under the hood, asking for 'rationale/justification' prevents the model from making arbitrary changes; it has to argue for each revision, which filters out changes that seem clever but do not actually improve the plan. The git-diff format forces precision rather than vague hand-waving about what should be different.

This has never failed to improve a plan significantly. The best part is that you can start a fresh conversation in ChatGPT and do it all again once Claude Code or Codex finishes integrating your last batch of suggested revisions. After four or five rounds of this, you tend to reach a steady-state where the suggestions become very incremental.

You can still get extra mileage by blending in smart ideas from Gemini with Deep Think enabled, or from Grok Heavy, or Opus in the web app, but you still want to use GPT Pro on the web as the final arbiter of what to take from which model and how to best integrate it.

After any review pass that feels too short or self-satisfied

By claiming 80+ errors exist, the model keeps searching exhaustively rather than satisfying itself with a partial list.

Plans created this way routinely reach 3,000-6,000+ lines. They are not slop. They are the result of countless iterations and blending of ideas and feedback from many models. For the CASS GitHub Pages export feature, the plan went through multiple rounds over about 3 hours, growing to approximately 3,500 lines. You can also see a 6,000-line plan to get a feel for the scale.

It feels slow because no code is being written. But if you do it correctly and then start up enough agents in your swarm with Agent Mail, beads, and bv, the code will be written so ridiculously quickly that it more than makes up for this slow part. And what's more, the code will be really good.

When to stop refining and start converting to beads: Stay in plan refinement if whole-workflow questions are still moving around, major architecture debates are still open, or fresh models keep finding substantial missing features, constraints, or tradeoffs. Switch to beads when the plan mostly feels stable and the remaining improvements are about execution structure, testing obligations, sequencing, and embedded context rather than about what the system fundamentally is. If you are still redesigning the product, stay in plan space. If you are mainly packaging the work for execution, move to bead space.

Then you're ready to turn the plan into beads. Think of these as epics, tasks, and subtasks with an associated dependency structure. The name comes from Steve Yegge's amazing project, which is like Jira or Linear, but optimized for use by coding agents. They are stored locally in .beads/ JSONL files that commit with your code.

There are two separate stages here. The planning is and should be prior to and orthogonal to beads. You should always have a super detailed markdown plan first. Then treat transforming that markdown plan into beads as a separate, distinct problem with its own challenges. But once you're in "bead space" you never look back at the markdown plan. But that's why it's so critical to transfer all the details over to the beads.

Claude Code with Opus

This prompt forces the agent to treat plan-to-beads as a translation problem rather than task extraction. The key sentence is the requirement that beads be so detailed you never need to reopen the markdown plan. That pushes rationale, test expectations, design intent, and sequencing into the bead graph itself. Under the hood, it blocks a common failure mode where the model collapses a rich plan into terse todo items. By explicitly asking for tasks, subtasks, dependency structure, comments, and future-self context, you tell the model that memory density matters more than brevity. Restricting to the br tool prevents the agent from drifting into pseudo-beads in markdown instead of editing the actual task graph.

For existing projects with a specific plan file, prefix it: "OK so now read ALL of PLAN_FILE_NAME.md; please take ALL of that and elaborate on it..." The rest of the prompt stays the same.

Pick a concept from the plan, then compare what survives into a thin bead versus a context-rich bead. The gap is the source of most swarm confusion.

- Implement multipart file upload for PDFs and markdown.

- Documents must be embedded and stored in the vector database.

- Admins need a way to see files that failed processing.

- System is internal only. Use SSO.

- Critical paths must have Playwright coverage.

- Implement semantic search using the PGVector embeddings we just generated.

- Build a dashboard to view the indexing status of all documents.

- Add E2E tests for the whole flow.

Seems simple, but implies S3 bucket provisioning, chunking, and progress states.

Each bead carries the why, what, failure modes, and verification plan needed to execute.

Most architecture has already been decided upstream.

Fresh agents can execute without improvising architecture or silently dropping intent.

The plan is still the best artifact for whole-system thought. But once a swarm is involved, what you need is not a beautiful essay. You need a task graph that carries enough local context for agents to act correctly without repeatedly loading the whole project back into memory. If the beads are weak, the swarm becomes improvisational. If the beads are rich, the swarm becomes almost mechanical.

To make this concrete, imagine a small internal web app called "Atlas Notes" for uploading and searching team notes. Instead of one vague task like "build Atlas Notes," the plan becomes many self-contained beads:

The titles are not the important part. What matters is that each bead is rich enough that a fresh agent can open it and immediately understand what correct implementation looks like, why it matters, and how to verify it.

For the CASS Memory System (5,500-line plan), the conversion produced 347 beads with complete dependency structure. FrankenSQLite had hundreds of beads created via parallel subagents. For complex projects, expect 200-500 initial beads.

Priority uses numbers: P0=critical, P1=high, P2=medium, P3=low, P4=backlog. Types: task, bug, feature, epic, question, docs. br ready shows only unblocked work. Storage is a SQLite + JSONL hybrid; the JSONL files commit with your code.

Before you burn up a lot of tokens with a big agent swarm on a new project, the old woodworking maxim of "Measure twice, cut once!" is worth revising as "Check your beads N times, implement once," where N is basically as many as you can stomach. This is the step most people underinvest in.

After the initial conversion finishes, do a round of this prompt. If Claude Code did a compaction at any point, be sure to tell it to re-read your AGENTS.md file first:

Claude Code with Opus — run 4-6+ times

This prompt keeps the system from freezing beads too early. It tells the model to stay in plan space for as long as it is still finding meaningful improvements, which is exactly where reasoning is cheapest and most global. The warnings against oversimplifying and losing functionality are crucial because models otherwise tend to 'improve' artifacts by deleting complexity they do not fully understand. It combines local bead QA (via br) with graph QA (via bv), and forces tests into the bead definitions themselves so test work cannot be deferred into an afterthought.

Drag the sliders or pick a preset to see how beads tighten into a stable state before implementation begins.

From real sessions, polishing involves duplicate detection and merging, quality scoring on WHAT/WHY/HOW criteria, filling empty bead descriptions, correcting dependency links, and cross-referencing beads against the markdown plan to ensure nothing was lost. FrankenSQLite identified 9 exact duplicate pairs and closed them, choosing survivors based on "richer testing specs, better dependency chains, and higher priority."

Tell agents to go through each bead and explicitly check it against the markdown plan. Or vice versa: go through the markdown plan and cross-reference every single thing against the beads (both closed and open) to ensure complete coverage.

Bead polishing follows numerical optimization convergence patterns:

Three signals indicate convergence: agent responses getting shorter (output size shrinking), the rate of change decelerating (change velocity slowing), and successive rounds becoming more similar (content similarity increasing). When the weighted convergence score reaches 0.75+, you're ready to finalize. Above 0.90, you're hitting diminishing returns.

If improvements start to flatline, start a brand new Claude Code session:

A brand new Claude Code session

Fresh sessions don't carry the accumulated assumptions of the previous session. They see the beads with genuinely new eyes.

Same fresh session, after it finishes reading

As a final step, have Codex with GPT (high reasoning effort) do one last round using the same polishing prompt. Different models catch different things.

After large bead creation batches, run a dedicated dedup pass:

Claude Code, after large bead creation batches

The full planning pipeline (Phases 1-5) is for new projects built from scratch. For existing projects that need new features, the Idea-Wizard is a formalized 6-phase pipeline:

Claude Code, for existing projects needing new features

Then: "ok and your next best 10 and why." The agent produces ideas 6-15, carefully checking each against existing beads for novelty. Having agents brainstorm 30 then winnow to 5 produces much better results than asking for 5 directly because the winnowing forces critical evaluation.

Not every change needs the full pipeline. For quick, bounded changes, use the built-in TODO system:

When the overhead of formal bead creation would slow you down more than it helps

This prompt forces the agent to externalize its local execution plan into a durable checklist instead of juggling a sprawling ad-hoc task in conversational memory. In tools that support a built-in TODO system, that checklist survives compaction. Under the hood, it creates a temporary execution scaffold that is lighter than full bead creation and much safer than 'just remember everything.' This is the right mode when the work is too small to justify immediate bead formalization but too large to trust to ephemeral context alone. When NOT to use it: if the change is expanding, depends on other work, needs graph-aware sequencing, or should be part of the permanent project record. In those cases, stop and convert it into proper beads. If an ad-hoc change later proves important, retroactively create beads for the completed work to preserve continuity.

The Idea-Wizard handles bounded improvements, new feature ideas, and fixes. But sometimes you want to add an entirely new capability to an existing project, something ambitious enough that it deserves the same depth of planning as a greenfield project, and where an external project has already solved a related problem worth studying. For these, there is a more powerful approach: study an external project that already solves a related problem, then reimagine its strongest ideas through the lens of your own project's unique strengths.

As a concrete example: adding a robust messaging substrate to the Asupersync project. Rather than designing from scratch or doing a straightforward port, the approach was to study NATS (a mature, production-grade messaging system in Go), extract its strongest architectural ideas, and reimagine them using Asupersync's correct-by-design structured concurrency primitives to create something neither project could achieve alone.

The process follows a specific prompt sequence. Each step builds on the previous, alternating between expansion (going deeper, inverting the analysis, pushing for architectural innovation) and hardening (repeated blunder hunts that stress-test the result):

Codex or Claude Code, in a session with existing project context

By asking the agent to clone and investigate the external project firsthand, you get specific, grounded proposals instead of vague suggestions based on training data alone. The 'reimagine in highly accretive ways' framing prevents a shallow porting exercise and pushes toward genuinely novel combinations.

The first draft is always too conservative. Push for depth and ambition:

Same session, immediately after the first proposal

Models produce conservative initial proposals to avoid being wrong. Explicit pressure to go deeper unlocks the genuinely creative architectural ideas that make the integration worthwhile rather than incremental.

Then invert the analysis. This technique surfaces opportunities that only exist because of your project's unique capabilities:

Same session, after deepening

Standard analysis asks 'what can we learn from them?' Inversion asks 'what can we do that they fundamentally cannot?' This surfaces the highest-value integration points: capabilities that are genuinely novel rather than just reimplementations of features the external project already has.

After each major expansion, run a blunder-hunt pass. The critical technique: repeat the exact same critique prompt 5 times in a row. Each pass finds things the previous pass missed, because the model is forced to look beyond the issues it already identified:

Run this exact prompt 5 times consecutively after each major proposal expansion

Models tend to find 15-20 issues on the first pass and declare satisfaction. Running the exact same prompt again forces them past the issues they already found. By the fifth pass, you have caught subtle logical flaws and architectural inconsistencies that no single review pass would surface. This is the critique equivalent of the bead polishing convergence pattern from Section 5.

Continue pushing for specific architectural innovations. In the Asupersync example, this meant asking: "Can you think of a clever, radically innovative way to leverage our unique capabilities so that the messaging substrate doesn't require a separate external server, but each client can self-discover and collectively act as both client and server?" Each major architectural addition gets another round of 5x blunder hunts.

When the proposal has items flagged as needing follow-on design work, address them explicitly rather than leaving them vague:

Same session, after blunder hunts surface specific open questions

Blunder hunts often identify areas where the proposal is 'honest but incomplete' rather than wrong. This prompt converts those honest gaps into concrete design decisions, preventing them from becoming ambiguity that later infects the beads and implementation.

Before sending the proposal for multi-model feedback, make it self-contained. Other models do not have your session context, so the proposal must include everything they need to give useful critique:

After the proposal reaches a stable, ambitious state

Cross-model review only works if every model can fully understand the proposal without access to your project. Adding comprehensive background sections prevents other models from making shallow suggestions based on incomplete understanding. This preparation step is what makes the multi-model feedback loop genuinely useful rather than superficial.

Follow this with another 5x blunder hunt, then de-slopify the document. Now you are ready for multi-model triangulation.

Send the self-contained proposal to GPT Pro, Claude Opus, Gemini with Deep Think, and Grok Heavy, all with the same prompt asking for improvements in git-diff format:

GPT Pro, Claude Opus (web), Gemini Deep Think, and Grok Heavy -- all four, independently

Each model has different architectural tastes and blind spots. Asking for git-diff format forces precision: the models cannot hand-wave about what should change, they have to show the exact text transformations. This makes the synthesis step tractable.

Feed the competing feedback from all models into GPT Pro using the "best of all worlds" synthesis prompt from Section 3. Apply the resulting diffs back to the proposal document in Codex or Claude Code, then de-slopify the final result.

You can see this exact process applied to Asupersync's NATS integration: the initial proposal, the version after multi-model feedback, and the full GPT Pro synthesis conversation.

From here, the proposal feeds into the standard pipeline: convert to beads (Section 4), polish obsessively (Section 5), launch the swarm (Section 7). The research-driven approach adds significant front-end effort but produces proposals with a level of architectural depth and innovation that no amount of greenfield brainstorming can match, because you are standing on the shoulders of a real, battle-tested system while leveraging capabilities that system never had access to.

Then you're ready to start implementing. The fastest way to do that is to start up a big swarm of agents that coordinate using three interlocking tools:

Hover or tap to inspect each piece. Click again to remove it and watch the system lose a capability it cannot replace. This is the Coordination Triangle.

The high-bandwidth negotiation layer.

The durable, localized issue state.

The graph-theory compass for triage.

The trio is not three nice-to-have tools. It is one operating system split into memory, communication, and leverage analysis. Remove any side of the triangle and the swarm loses determinism.

Each tool is essential but insufficient alone. Agent Mail without beads leaves agents with no structured work to coordinate around. Beads without bv leaves agents randomly choosing tasks. bv without Agent Mail leaves agents unable to communicate. The system is distributed and decentralized, with each agent using bv to find the next optimal bead, marking it as in-progress, and communicating about it via Agent Mail.

Building your own agent coordination from scratch is full of footguns that Agent Mail was designed to sidestep:

Before editing files, agents reserve them via Agent Mail:

Other agents see the reservation and work on different files. A rigid locking system would deadlock when an agent crashes while holding a lock. Advisory reservations with expiry degrade gracefully. The worst case is a brief window where two agents touch the same file, which the pre-commit guard catches anyway.

Agent Mail provides four high-level macros that wrap common multi-step patterns: macro_start_session (bootstrap: ensure project, register agent, fetch inbox), macro_prepare_thread (join existing thread with summary), macro_file_reservation_cycle (reserve, work, auto-release), and macro_contact_handshake (cross-agent contact setup).

Agent Mail uses targeted delivery and advisory locks to stay efficient. O(1) noise.

bv precomputes dependency metrics (PageRank, betweenness, HITS, eigenvector, critical path, cycle detection) so agents get deterministic, dependency-aware output. When multiple agents each independently query bv for priority, you get emergent coordination. Agents naturally spread across the optimal work frontier without needing a central coordinator.

PageRank finds what everything depends on. Betweenness finds bottlenecks. The math knows your priorities better than gut intuition.

bv was made in a single day and was just under 7k lines of Go. It was later rewritten to 80k lines with advanced features. This shows that effort does not correspond to impact. The tool started for humans but pivoted to being primarily for agents:

Advanced filtering lets you scope analysis to labels, historical point-in-time views, pre-filtered recipes, or grouped output:

Bead IDs create a unified audit trail across all coordination layers: the bead ID goes in the Agent Mail thread_id, the subject prefix ([br-123]), the file reservation reason, and the commit message. This makes all coordination activity traceable back to a single task.

The AGENTS.md file is the single most critical piece of infrastructure for agent coordination. It tells every agent how to behave, what tools exist, what safety constraints matter, and what "doing a good job" means in this repo. Every tool should come with a prepared blurb designed for inclusion in AGENTS.md. Think of these blurbs as the modern equivalent of man pages.

Every AGENTS.md should include these core rules:

More content in AGENTS.md means more frequent compactions, but it saves time and avoids mistakes by giving agents all the context upfront. This tradeoff is worth making.

If you don't have a good AGENTS.md file, none of this stuff is going to work well. You can see example AGENTS.md files for a complex NextJS webapp and a bash script project.

"Reread AGENTS.md" is the single most common prompt prefix across the entire session archive. After every context compaction, agents must re-read it:

Immediately after any context compaction (the single most commonly used prompt)

Compaction wipes out the soft operational knowledge that keeps the swarm sane: how to behave, how to coordinate, what tools exist, what rules matter, what mistakes to avoid. This one-line prompt restores that control plane in one move. It rehydrates the agent's behavioral contract after context loss. Important enough to have been automated with the post_compact_reminder tool.

The pragmatic approach: do not fight compaction, just re-read AGENTS.md and roll with it until the agent starts doing dumb stuff, then start a new session. When beads are well-constructed, compaction matters less because each bead is self-contained. The agent can pick up any bead fresh without needing the full conversation history.

All agents commit directly to main. This may surprise you if you're used to feature branches. But branch-per-agent creates merge hell with 10+ agents making frequent commits. Worktrees add filesystem complexity and path confusion. Agents lose context when switching branches. Logical conflicts survive textual merges: a function signature change on one branch and a new callsite on another merge cleanly but fail to compile. On a single branch, the second agent sees the signature change immediately and adapts.

Instead of branch isolation, three complementary mechanisms prevent conflicts: file reservations (agents reserve files via Agent Mail before editing; advisory, not rigid, with TTL expiry so dead agents cannot deadlock the system), a pre-commit guard (blocks commits to files reserved by another agent), and DCG (Destructive Command Guard, which mechanically blocks dangerous commands).

The recommended git workflow: Pull latest, reserve files, edit and test, commit immediately, push, release reservation. Key principles: commit early and often (small commits reduce the conflict window), push after every commit (unpushed commits are invisible to other agents), reserve before editing, release when done.

Every agent is a generalist. No role specialization. All agents read the same AGENTS.md and can pick up any bead. This is deliberately opposed to "specialist agent" architectures where one agent has a special role — specialist agents become single points of failure. When the specialist crashes or needs compaction, the whole system stalls. With 12 fungible agents, losing one makes almost no difference.

You also do not want "ringleaders": a coordinating boss agent whose crash takes down the whole system. Coordination must live in artifacts (beads, reservations, threads) and tools (bv, Agent Mail), not in any special agent.

Think of it like RaptorQ fountain codes: beads are "blobs" in a stream, any agent catches any bead in any order. There is no "rarest chunk" bottleneck, and the system is resilient to partial agent failures by design. Failure recovery is trivial: the bead remains marked in_progress, any other agent can resume it, and a replacement agent is just ntm add PROJECT --cc=1 plus the standard marching orders prompt.

Click any agent to kill it. Watch the swarm self-heal.Tap an agent, then tap again to kill it.

Every agent is fungible. Kill any of them to see the swarm self-heal without downtime or data loss.

This confuses people when they first see the prompt library. The prompts say things like "check over each bead super carefully" rather than "check over each bead in the authentication module for SQL injection risks." That generality is the point. The specificity lives in three places the agent already has access to:

The prompts are the reusable scaffolding that directs the agent's attention. The beads and AGENTS.md supply the project-specific substance. This separation means you can use the exact same prompt library across every project without modification. The prompt "reread AGENTS.md so it's still fresh in your mind" followed by "use bv to find the most impactful bead to work on next" works identically whether you are building a CLI tool, a web app, or a protocol library, because the specifics come from the project's own artifacts, not from the prompt.

Security review is baked into the standard workflow at multiple levels rather than being a separate phase. The cross-agent review prompt explicitly calls out security problems. When models reason about an entire system's architecture at once (which is what the plan enables), they spot authentication gaps, data exposure risks, and trust boundary violations without being told to look. UBS catches security anti-patterns mechanically: unpinned dependencies, missing input validation, hardcoded secrets, supply chain vulnerabilities. Beads that include comprehensive e2e tests naturally cover authentication and authorization paths.

Security vulnerabilities are usually symptoms of incomplete reasoning about the system. If the plan is detailed enough to cover all user workflows, edge cases, and failure modes, security considerations emerge from that completeness rather than requiring a separate checklist. For projects with explicit security requirements (financial, healthcare), add dedicated security review beads.

You can create sessions using Claude Code, Codex, and Gemini-CLI in different panes in tmux, or use the ntm project (Named Tmux Manager) as the command center:

NTM is useful but not mandatory. A mux is a terminal multiplexer: a layer that lets you manage multiple shell sessions inside one higher-level session manager. In practice, that usually means some combination of tabs, panes, detached sessions, and reconnection to work that is still running on a local or remote machine. tmux is the classic Unix terminal multiplexer, powerful and battle-tested. NTM is built on top of tmux, which is why it is a natural fit for multi-agent work. But tmux is only one mux. WezTerm has its own built-in mux. Zellij is another. The method cares that you have a workable orchestration layer, not that you picked one specific multiplexer.

One common alternative is WezTerm because native scrollback and text selection are more convenient than in tmux. A workable setup:

There is no single correct operator interface. NTM is one good cockpit. WezTerm tabs plus mux is another. FrankenTerm, which is built on WezTerm, is aimed more explicitly at this style of workflow but is not ready yet. The important thing is that you can launch agents, get prompts into them quickly, monitor them, and keep the coordination layer (AGENTS.md, Agent Mail, beads, bv) intact.

For concrete setup notes on these operator environments:

Give each agent these marching orders:

Every agent in the swarm gets this as their initial prompt

This is the closest thing to a canonical swarm kickoff packet. It front-loads the shared operating context, forces the agent to establish social presence through Agent Mail, and then pivots away from passive waiting toward execution. The line about 'communication purgatory' matters because swarm failure often comes from over-coordination rather than under-coordination. Under the hood, the prompt establishes a control loop: load rules, understand the codebase, join the coordination layer, claim work, keep state synchronized, and use bv whenever local judgment is insufficient. The rch requirement is especially important in real swarms because it externalizes expensive builds and tests, preventing local CPU contention from degrading the entire multi-agent system. That one sentence is operational, not cosmetic. The prompts are deliberately generic; their vagueness is a feature, letting you reuse them for every project while the agent gets specifics from AGENTS.md and the beads.

Newcomers often understand each individual tool but do not have a clean picture of the first live operating loop. In practice, the first 10 minutes look like this:

That sequence turns a pile of terminals into a coordinated swarm. Skipping the join-up steps produces duplicate work, silent conflicts, and "communication purgatory." Skipping the routing steps means agents choose work randomly instead of unlocking the dependency graph intelligently.

Efficiency definitely declines as N grows, but if you have enough tasks in beads and they have Agent Mail and you don't start them all at the exact same time, you go faster as N grows. The practical limit is around 12 agents on a single project, sometimes higher. Or run 5 agents per project across multiple projects simultaneously. Why the ratio --cc=2 --cod=1 --gmi=1? Two Claude sessions because they are great for architecture and complex reasoning; one Codex for fast iteration and testing with complementary strengths; one Gemini for a different perspective, especially good for docs and review duty.

When you start up like 5 of each kind of agent and have them all collaborate in the same shared workspace, you can hit the classic "thundering herd" problem. The fix: stagger agent starts by 30 seconds minimum, make sure agents mark beads as in-progress quickly, and wait 4 seconds after launch before sending the initial prompt. For Codex specifically: send Enter twice after pasting long prompts (Codex has an input buffer quirk that sometimes swallows the first submit).

Advance phase by phase and compare the exact same four agents under two launch strategies. The lesson is timing, not talent.

All agents wake together, re-read context together, and pile onto the same frontier.

The swarm is synchronized before any useful work has started.

Agents enter a few beats apart, so each arrival sees a different clean frontier.

Only the first agent is awake. The rest are still off the critical path.

At this phase, the herd path has 0 lock conflicts and 6 units of idle burn, while the staggered path has 0 conflicts and 2 idle burn. The difference is not smarter agents. It is whether the system lets them reach distinct frontier at distinct times.

The human tends the swarm like an operator tending a machine that mostly runs on its own. These tasks are monitoring and maintenance. The hard cognitive work already happened during planning, which is why you can tend multiple project swarms at the same time.

On roughly a 10-30 minute cadence:

Taken to its endpoint, this design supports full autonomy: one puppet master agent controlling ntm via robot mode, replacing the human for routine machine-tending. The methodology is building toward a future where the human designs the plan, polishes the beads, and then walks away entirely while agents execute, review, ship, and start the next cycle.

When the "foregone conclusion" breaks down: If you find yourself doing heavy cognitive work during implementation, that is a signal that planning or bead polishing was insufficient. The remedies are specific: vague beads means agents improvise and produce inconsistent implementations; missing dependencies means agents work on tasks whose prerequisites are not done; thin AGENTS.md means agents produce non-idiomatic code; no Agent Mail means agents step on each other's files. The fix is always the same: pause implementation, go back to bead space, and add the missing detail.

When a swarm goes bad, the failure is usually one of two things: a local coordination jam (agents stepping on each other or losing operational context) or a strategic drift problem (the swarm is busy but no longer closing the real gap to the goal).

For a small project like Atlas Notes, a first swarm might look like this: Claude agent A claims br-101 and implements upload + parse handling. Codex agent B claims br-102 and works on the search path plus tests. Claude agent C claims br-103 and builds the admin failure dashboard. Gemini agent D stays flexible: reviews recent work, checks docs, and fills in test or UX gaps where needed. All four share the same codebase, read the same AGENTS.md, coordinate via Agent Mail, and use bv whenever they are uncertain about what unlocks the most progress next. That is what makes the swarm feel like one system rather than four unrelated terminals.

When you hit rate limits, use CAAM (Coding Agent Account Manager) for sub-100ms account switching:

Code review in a multi-agent swarm follows a different rhythm than traditional code review. There is no pull request, no human reviewer, no approval gate. Instead, review is woven into the implementation cycle itself: agents review their own work after each bead, review each other's work periodically, and the human triggers broader review rounds at natural checkpoints.

If you've done a good job creating your beads, the agents will be able to get a decent sized chunk of work done in that first pass. Then, before they start moving to the next bead, have them review all their work:

After each bead is implemented; run until no more bugs are found

This prompt is short because it is not redirecting the agent into a new domain. It is forcing a mode switch from generative coding to adversarial reading. The phrase 'fresh eyes' pushes the model to reframe code it just wrote as something potentially wrong, confusing, or internally inconsistent. That reduces the pattern where an agent stops once code compiles and never performs the low-cost bug sweep that catches obvious issues. The most effective reviews use subagent delegation: dispatch a fresh subagent with no memory of the original implementation to review each changed file.

Keep running rounds until they stop finding bugs. Typically 1-2 rounds for simple beads, 2-3 for complex ones. If an agent keeps finding bugs after 3 rounds, the implementation approach may be fundamentally off; consider having a different agent take over.

Each review should answer four questions:

When reviews come back clean, have them move on to the next bead:

After self-review comes back clean

This transition prompt is the glue between beads. It combines re-reading AGENTS.md (for compaction safety), querying bv for priority, and communicating with the swarm. It ensures the agent uses graph-theory routing to choose the task that unblocks the most downstream work, rather than picking arbitrarily.

When all your beads are completed, make sure you have solid test coverage:

After initial implementation pass is complete

Larger projects produce massive test suites. BrennerBot has nearly 5,000 tests. Stuff tends to "just work" in that case. Use UBS (Ultimate Bug Scanner) as a quality gate before every commit: ubs <changed-files> catches errors beyond what linters and type checkers find, including security holes, supply chain vulnerabilities, and runtime stability issues.

After any substantive code changes, always verify with compiler checks:

For projects with a user interface, there is a dedicated polishing phase that happens after core functionality works but before shipping. This is separate from bug hunting because the problems you are looking for are not bugs; they are friction, ugliness, and missed opportunities to delight. When an agent implements an "authentication" bead, it focuses on making auth work correctly. Whether the login form has good visual hierarchy, whether the error messages are helpful, whether the flow feels smooth on mobile: these are orthogonal concerns requiring a different mode of attention. Trying to do both at once produces mediocre results on both.

The workflow has five steps: Step 1, run the general scrutiny prompt to generate a list of improvement suggestions (not code changes). Step 2, review the suggestions and pick which to pursue (human judgment step; the agent typically generates 15-30 suggestions, some excellent, some unnecessary). Step 3, turn selected suggestions into beads and implement through the normal swarm process. Step 4, run the platform-specific polish prompt. Step 5, repeat until improvements become marginal (typically 2-3 rounds).

After core functionality is working

After the scrutiny pass

The 'don't you agree?' phrasing is not politeness. It triggers the model to critically evaluate its own previous work rather than just validating it.

After agents write documentation (README, user-facing text), run a de-slopify pass to remove telltale AI writing patterns. This must be done manually, not via regex. Read each line and revise systematically:

This phase is distinct from the per-bead self-reviews above. Self-reviews happen after each bead is completed and focus on the code that was just written. Deep review happens after all (or most) beads are done and casts a wider net across the entire codebase, looking for problems that only become visible when you see how all the pieces fit together.

Cross-agent review catches a fundamentally different class of bugs than self-review. When Agent A implements a function and Agent B calls it, Agent A's self-review will never catch the fact that Agent B is passing arguments in the wrong order, because Agent A does not know about Agent B's code. Cross-agent review surfaces these integration issues.

Every 30-60 minutes during active implementation, or after a natural milestone (e.g., all beads in an epic are done), trigger cross-agent review. Do not have all agents stop to review simultaneously; pick one or two agents that just finished a bead and send them the review prompt while the others keep implementing. This keeps the swarm productive while still catching inter-agent issues.

Keep doing rounds of these two prompts until they consistently come back clean with no changes made. These prompts serve different purposes and should be alternated. This is one of the more art-than-science parts of the methodology. The prompts overlap in literal meaning, but they reliably activate different search behaviors in the models:

Alternate with the cross-agent review below

The prompt first asks the agent to build a mental model of purpose and flow, then asks for criticism. That ordering matters. A bug hunt without workflow understanding degrades into linting; a bug hunt after tracing execution flows catches logic errors, mismatched assumptions, and silent product-level breakage. The 'randomly explore' framing breaks the locality trap. Directed reviews focus on files that seem important, which are the files that got the most attention already. Bugs that survive to this phase live in utility modules, error handling paths, configuration parsing, and edge-case branches.

Alternate with the random exploration above

This prompt forces the swarm to stop treating code ownership as sacred. A large share of real defects live at the boundaries between agents' changes or in assumptions nobody revisits because they were made by 'someone else.' The instruction not to restrict review to the latest commits prevents shallow PR-style skimming and pushes the agent to trace older surrounding code, dependency surfaces, and adjacent workflows where the real root cause may live. The first-principles wording nudges the reviewer away from symptom-fixing toward actual causal diagnosis.

The cross-agent prompt tends to induce a suspicious, adversarial stance aimed at boundary failures and root causes in code written by others. The random-exploration prompt tends to induce a curiosity-driven stance aimed at reconstructing workflows and finding latent bugs in code that nobody is actively staring at. In practice, alternating them produces better coverage than repeating either one alone.

How to run deep bug hunting: Send the random exploration prompt to 2-3 agents simultaneously — each will explore different parts of the codebase because the randomness ensures variety. After they report back, send the cross-agent review prompt. Alternate until agents consistently come back with "I reviewed X, Y, Z files and found no issues." When two consecutive rounds both come back clean, the codebase is in good shape. If agents keep finding bugs after 4+ rounds, go back to bead space and create specific fix beads. Always run ubs . on the full project first and fix everything it flags before letting agents hunt for subtler issues.

Periodically have one agent handle git operations:

Every 1-2 hours during active development

Designating one agent prevents merge conflicts and produces coherent commit messages. The 'don't edit the code' instruction is critical: without it, agents treat the commit step as an opportunity to 'fix one more thing,' which creates unbounded scope expansion and makes the commit unpredictable. The 'logically connected groupings' instruction produces a meaningful git history instead of one monolithic 'update everything' commit that is impossible to review or bisect later.

When the swarm looks active but you suspect it is not closing the real gap to the goal:

When the swarm feels busy but directionally off

This prompt breaks the spell of local productivity. Instead of asking whether the current bead is going well, it asks whether the current frontier of work actually converges on the project outcome. If the agent concludes that finishing all open beads still would not get you there, the answer is not 'work harder.' The answer is to revise the bead graph and re-aim the swarm.

After significant implementation work

After any significant change, as a quick final pass

After agents write README or any user-facing documentation

When ending a work session, agents must complete every step. Work is NOT complete until git push succeeds. Unpushed work is stranded locally and invisible to every other agent.

For the Atlas Notes example, "done for now" would not mean "the upload page appears." It would mean: the upload, parse, search, and admin-review workflows all work end to end; the key beads are closed and remaining polish ideas exist as new beads; tests cover the critical user journeys and known failure paths; UBS and compiler/lint checks are clean; commits and pushes are complete; and the next session can restart from beads, AGENTS.md, and Agent Mail threads rather than from human memory.

A Flywheel session is only landable when a future swarm can pick it back up without the human re-explaining the project from scratch.

The Flywheel is supported by a stack of 11 purpose-built tools, all free and open-source:

Not every tool is used the same way. br, bv, ubs, and rch are ordinary shell commands. Agent Mail is primarily experienced through MCP tools and macros. The installer (agent-flywheel.com) installs all of them with a single curl|bash command.

The complete interaction flow from spawn to memory:

Use acfs newproj to bootstrap a project with full tooling:

For beginners who find the full system overwhelming:

The term "skill" confuses people at first, so define it plainly: a skill is a reusable operational instruction pack for an agent. In Claude Code terms, that usually means a SKILL.md file plus optional references, scripts, or templates that tell the agent how to use a tool, how to execute a methodology, what pitfalls to avoid, and what a good result looks like. A good skill is closer to executable know-how than to ordinary prose documentation.

A tool changes what the agent can do. A skill changes how well the agent knows how to do it. The same model with and without a good skill often behaves like two different agents.

Every Flywheel tool has a corresponding Claude Code skill that encodes best practices and automates common workflows. Many of these skills are bundled directly in the repos for the tools themselves and get installed automatically when the tool is installed, which means users often benefit from them without having to think about "skill management" explicitly. There is also a broader public skills collection at GitHub.

The prompt side has a similar split. jeffreysprompts.com has a generous free section and is open source at GitHub. It also has a paid Pro tier with additional prompts and a dedicated CLI called jfp for managing prompt collections. For a larger paid library of higher-end skills, see jeffreys-skills.md, a $20/month service with many of the strongest curated skills, new skills added continuously, and a dedicated CLI called jsm for managing them.

Both paid offerings are still under active development. That means occasional rough edges. Active work is underway to fix issues quickly, feedback is appreciated, and refunds are available for unhappy users.

Skills provide the prompts, procedures, anti-pattern guidance, and tool-specific workflows directly to agents, which reduces the amount of bespoke prompting a human needs to do by hand.

Beads, Agent Mail, and bv are all CLI tools that work identically regardless of which agent invokes them. A Claude Code agent and a Codex agent and a Gemini agent can all call br ready --json and get the same task list. The practical test: could you swap out every Claude Code agent for Codex or Gemini without changing your AGENTS.md, beads, Agent Mail setup, or workflow? If yes, you're vendor-neutral.

These gates turn the methodology into a contract. If a gate fails, drop back a phase instead of pushing forward optimistically.

On the VPS, agents run with full permissions via short aliases:

These are configured automatically by the installer. DCG provides the safety net that makes this viable.

~$500/month for Claude Max and GPT Pro subscriptions (at minimum), plus ~$50/month for a cloud server (OVH, Contabo). Multiple Max accounts may be needed for large swarms; CAAM enables instant switching when hitting rate limits. At scale, token usage for a single intensive session can reach ~20M input tokens, ~3.5M output tokens, ~2.6M reasoning tokens, and ~1.15 billion cached token reads. At full scale: 22 Claude Max accounts, 22 GPT Pro accounts, and 7 Gemini Ultra accounts.

If you simply use these tools, workflows, and prompts in the way just described, you can create really incredible software in just a couple days, sometimes in just one day. I've done it a bunch of times now and it really does work, as crazy as that may sound. You see my GitHub profile for the proof of this. It looks like the output from a team of 100+ developers.

It behaves like a flywheel rather than a checklist because each cycle makes the next one better:

Each session makes the next one better. Concretely: Session N produces raw data — CASS automatically logs every agent session. Between sessions, CM distills patterns — running cm reflect extracts procedural rules like "always run cargo check after modifying Cargo.toml" with confidence scores that decay without reinforcement and amplify with repetition. Session N+1 starts with those patterns loaded — running cm context "Building an API" retrieves relevant procedural memory. Simultaneously, UBS patterns grow as new bug classes get added. Agent Mail coordination norms get refined in AGENTS.md and skills.

The compounding is real but not automatic in the early stages. You have to actually run cm reflect, actually review CASS session data, actually update AGENTS.md with lessons learned. But even manually, spending 15 minutes between projects reviewing what worked and updating your AGENTS.md template produces outsized returns on every subsequent project.

Apply the same feedback mechanisms you would use for humans (structured surveys, satisfaction ratings, net promoter scores) directly to agents evaluating tools. After an agent finishes using a tool in a real project, ask it to fill out a structured feedback survey. Then pipe that feedback directly into another agent working on the tool itself. The iteration cycle collapses from weeks to minutes.

After an agent finishes using a tool in a real project

Many of the same concepts we use for people are directly applicable to agents. 'By robots, for robots.' This produces structured, actionable feedback. When used across multiple agents on different project types, you get a diverse sample of experiences. One caveat: as with humans who would tell you they wanted a 'faster horse' instead of a car, it is dangerous to trust agent feedback about potential new features before those features exist. The real test is always after implementation, in real-world usage.

CM (CASS Memory System) implements a three-layer memory architecture that turns raw session history into operational knowledge:

Rules have a 90-day confidence half-life (decays without feedback) and a 4x harmful multiplier (one mistake counts 4x as much as one success). Rules mature through stages: candidate to established to proven.

The cm context command is the single most important pre-task ritual. Running it at the start of a session gives agents knowledge distilled from every previous session that touched similar work.

Claude Code, targeting any skill with 10+ CASS sessions of usage data

This is the meta-skill pattern in action. The skill-refiner skill itself can be refined using its own session data, which is the self-referential property that makes the whole system accelerate. After 3-4 cycles, the skill is dramatically more reliable than the original. Each cycle takes less human effort because the meta-skill itself has improved.

The flywheel's learning loop depends on mining past sessions to find what actually works. CASS enables ritual detection: discovering prompts that are repeated so frequently they constitute validated methodology.

The mining query (user prompts live at lines 1-3 of session entries; --fields minimal reduces output 5x):

This is how the prompt library in this guide was originally discovered and validated. It was not invented top-down; it was mined bottom-up from hundreds of real sessions.

The workflow works because it keeps different kinds of context in different layers. The markdown plan holds whole-system intent and reasoning. The beads hold executable task structure and embedded local context. AGENTS.md holds operating rules and tool knowledge that must survive compaction. The codebase holds the implementation itself, which is too large to be the primary planning medium. Each layer serves a different purpose, and the methodology is disciplined about keeping the right information in the right layer.

CASS itself (a complex Rust program used by thousands of people) was made in around a week, but the human personally only spent a few hours on it. The rest of the time was spent by a swarm of agents implementing and polishing it and writing tests.

This claim sounds bold, but it follows logically from everything above. If the plan is thorough, the beads faithfully encode it with full context and correct dependencies, and the agents have a clear AGENTS.md, then implementation becomes a mechanical process of agents picking up beads, implementing them, reviewing, and moving on.

This is true when: the plan has genuinely converged (not merely become long), the beads are self-contained enough that fresh agents can execute them without guessing, the swarm has working coordination/review/testing loops, and the human is still tending when flow jams or reality diverges from the plan.

It stops being true when: architecture is still being invented during implementation, the bead graph is thin or missing dependencies, or the swarm cannot coordinate because AGENTS.md, Agent Mail, or bv usage is weak. If you find yourself doing heavy cognitive work during implementation, that is a signal that planning or bead polishing was insufficient. The remedy is to pause, go back to bead space, and add the missing detail.

A common misconception is that you have to do everything in one shot. In this approach, that's true only for version 1. Once you have a functioning v1, adding new features follows the same process: create a super detailed markdown plan for the new feature, turn it into beads, and implement. The same process that creates the initial version also handles all subsequent iterations.

Every tool ships with a prepared AGENTS.md blurb. The tool is not complete without documentation that agents can consume. But it goes further: the tools themselves should be designed by agents, for agents, with iterative feedback. If agents do not like the tools, they will not use them without constant nagging.

This is the most advanced concept in the flywheel, and the one that separates linear productivity gains from exponential ones. The core idea: your agent toolchain should improve itself using its own output as fuel.

Most developers treat skills and tools as static artifacts. You write a skill, agents use it, and if it works well enough, you move on. The recursive approach instead treats every agent session as training data for the next version of the skill, creating a tight feedback loop where the system gets measurably better each cycle without additional human effort.

Consider what happens without recursive improvement. You build a CLI tool, write a Claude Code skill for it, and deploy both. Agents use the tool, but they misinterpret certain flags, forget to pass required arguments, or use workarounds because the skill's instructions were ambiguous. Every agent that hits the same snag wastes the same tokens re-discovering the same workaround. Multiply that across dozens of agents and hundreds of sessions, and the waste is enormous. Now consider the alternative: after those sessions happen, you automatically mine them, discover the failure patterns, rewrite the skill to prevent them, and the next wave of agents never hits those snags at all. The skill becomes a living document shaped by real usage rather than a guess about how agents will behave.

What to look for in the results:

The key insight is that the rewriting step itself can be a skill. You can write a meta-skill whose entire purpose is: take a skill file + CASS session data as input, produce a better skill file as output. Then the meta-skill can also be refined using its own session data, which is the self-referential property that makes the whole system accelerate.

Each cycle takes less human effort than the previous one because the meta-skill itself has improved.

The recursive pattern operates at increasing levels of ambition. The mistake is trying to build all four layers at once. Start simple and let the need for the next layer emerge naturally.

Each layer amplifies the next. Start at Layer 1, not Layer 4.

Layer 1 requires zero infrastructure. You can do this today, right now, with any tool and two agent sessions.

Most productivity techniques produce linear improvements: you get 10% better each cycle, and those gains do not stack. The recursive skill pattern compounds because each cycle improves the tools that perform the next cycle.

When you improve the extreme-optimization skill, every future optimization pass across every tool benefits. When you improve the idea-wizard skill, every future brainstorming session across every project benefits. When you improve the skill-refiner meta-skill, every future skill refinement benefits. The improvements multiply rather than add.

The tools produced by the recursive loop are the tools that produce the next tools. This is why the Knuth analogy is apt: it is genuinely the same concept as a compiler that compiles itself, except applied to the entire agent-driven development workflow rather than just a compiler.

The recursive loop has a second, subtler benefit that matters even more at the frontier. Models have internalized vast amounts of academic CS literature: obscure algorithmic techniques, mathematical proofs, design patterns from papers that only a handful of people ever read. Most of this knowledge never surfaces because nobody asks for it with enough precision.

Skills are the mechanism for asking the right questions. Consider the difference:

The skill acts as a key that unlocks specific rooms in the model's knowledge base. Without the key, the model defaults to common patterns. With it, the model reaches into the long tail of techniques that most human developers have never encountered.

This explains why the recursive loop accelerates rather than plateaus. Each cycle of skill refinement does not just fix bugs in the skill's instructions; it also sharpens the skill's ability to extract deeper knowledge from the model. The optimization skill gets better at asking for the right techniques, because CASS sessions reveal which techniques actually produced measurable gains and which were dead ends. The next cycle of optimization is better informed because the previous cycle's results are now part of the feedback corpus.

Stack enough cycles and the result is code that looks like it was written by someone who read every obscure CS paper ever published. In a functional sense, it was. The agent served as a lens focusing decades of dispersed academic knowledge onto a single practical target. The skill was the lens prescription.

These recurring cognitive moves show up throughout real Flywheel sessions. They matter more than any single prompt because they say when to apply a move, what failure looks like, and what output is expected. Each operator has a prompt module you can paste directly into an agent session.

When the project still fits in a plan but would explode in size once implemented, multiple architectural paths are plausible, or the desired user workflow is still fuzzy

Prevents skeleton-first coding that locks in bad boundaries, and stops local code exploration from substituting for product reasoning.

When the project is important enough that one model's biases are dangerous, or early drafts feel plausible but not obviously excellent

Prevents picking the first decent plan and calling it done, or combining every idea indiscriminately instead of filtering for quality.

When review output looks too short or self-satisfied, or a large plan/bead graph still feels under-audited

Prevents asking for 'all problems' and getting a shallow pass. Models stop after finding a 'reasonable' number; this forces exhaustive search.

When a large plan is about to be turned into execution tasks, or agents are creating beads quickly and may drop rationale

A beautiful plan does not automatically produce good beads. Prevents creating terse beads that depend on tacit knowledge from the markdown file.

When a plan or bead graph has visible rough edges and the first polishing pass found real issues

Prevents treating the first decent revision as final, or continuing endless polishing after returns have gone flat.

When the agent has done several long review rounds and suggestions are getting repetitive or shallow

Prevents trusting a tired context window to keep finding subtle flaws, or mistaking context exhaustion for genuine convergence.

When beads are polished enough to execute and multiple agents are about to work in the same repository

Prevents launching too early before beads are self-contained, or letting agent identity and role specialization become load-bearing.

When the same confusion or recovery pattern appears repeatedly in CASS, agents complain about a tool, or a project finishes with clear lessons worth retaining

Prevents treating lessons as anecdotes instead of durable system inputs. This is the operator that turns repeated behavior into ritual, ritual into skill, skill into infrastructure.

All prompts in this guide are preserved verbatim from prompts that worked well in real sessions (quirks and typos included). For a much larger public prompt collection, see jeffreysprompts.com, which has a generous free section and is open source at GitHub. There is also a paid Pro tier with additional prompts and a CLI called jfp for managing prompt collections. For a larger paid library of higher-end skills, see jeffreys-skills.md ($20/month, with a dedicated CLI called jsm). Both paid offerings are still under active development.

The complete system is free and 100% open-source. A beginner with a credit card and a laptop can visit the wizard, follow step-by-step instructions to rent a VPS, paste one curl|bash command, type onboard, and start building with AI agents immediately.

You don't even need to know much at all about computers; you just need the desire to learn and some grit and determination. And about $500/month for the subscriptions, plus another $50 or so for the cloud server.

Once you get Claude Code up and running on the cloud server, you basically have an ultra competent friend who can help you with any other problems you encounter. And Jeffrey will personally answer your questions if you reach out on X or on GitHub issues.

If you want to change the entire direction of your life, it has truly never been easier. If you think you might want to do it, I really recommend just immersing yourself.

One command installs all 11 tools, three AI coding agents, and the complete environment.30 minutes to fully configured.

**Examples:**

Example 1 (unknown):
```unknown
br create --title "..." --priority 2 --label backend    # Create issue
```

Example 2 (unknown):
```unknown
br list --status open --json                             # List open issues
```

Example 3 (unknown):
```unknown
br ready --json                                          # Show unblocked tasks
```

Example 4 (unknown):
```unknown
br show <id>                                             # View issue details
```

---

## Unheard-of Velocityin Complex Software

**URL:** https://agent-flywheel.com/flywheel

**Contents:**
- Unheard-of Velocityin Complex Software
- The Agentic Coding Flywheel
  - Explore the Flywheel
  - Core Tools
  - NTM
  - Mail
  - UBS
  - BV
  - CASS
  - CM

35 interconnected tools that enable multiple AI agents to work in parallel, review each other's work, and make incredible autonomous progress, all while you're away.

“The magic isn't in any single tool. It's in how they work together. Using three tools is 10x better than using one.”

Projects simultaneously

35 tools that create unheard-of velocity

Click any tool to see details and integrations

A self-reinforcing system that enables multiple AI agents to work in parallel across 10+ projects, reviewing each other's work, creating and executing tasks, and making incredible autonomous progress while you're away.

Agent cockpit for multi-agent tmux sessions

Orchestrate multiple AI coding agents across tmux sessions. Spawn Claude, Codex, and Gemini agents in named panes. 80+ commands for session management, prompt broadcasting, file conflict detection, and context rotation. Persistent sessions survive SSH disconnects.

Like Gmail for AI coding agents

A complete coordination system for multi-agent workflows. Agents register identities, send/receive messages, search conversations, and declare file reservations to prevent edit conflicts. HTTP-only FastMCP server with static export and Web UI.

Pattern-based bug scanner with 1000+ detection rules

AST-grep patterns detecting 1000+ bug types across 8 languages. 18 detection categories from null safety to security vulnerabilities. Sub-5-second scans. Auto-wires into Claude Code, Codex, Cursor, Gemini, and Windsurf agents.

Graph-theory triage engine for task prioritization

Transforms task tracking with DAG-based analysis. Nine graph metrics, robot protocol for AI, time-travel diffing. Agents use BV to figure out what to work on next.

Blazing-fast search across AI coding agent sessions

Unified search for all AI coding sessions. Indexes 11 agent formats: Claude Code, Codex, Cursor, Gemini, ChatGPT, Cline, Aider, Pi-Agent, Factory, OpenCode, Amp. Tantivy-powered <60ms queries with optional semantic search.

Procedural memory system for AI coding agents

Transforms scattered agent sessions into persistent, cross-agent memory. Patterns discovered in Cursor automatically help Claude Code on the next session. Three-layer cognitive architecture: Episodic → Working → Procedural.

Two-person rule for dangerous command approval

Nuclear-launch-style safety for AI agents. Four risk tiers (CRITICAL/DANGEROUS/CAUTION/SAFE) with 40+ regex patterns. CRITICAL commands require 2+ approvals from different agents. Cryptographic signing, rollback support, and outcome analytics.

SIMD-accelerated safety net for dangerous commands

Claude Code PreToolUse hook blocking dangerous commands BEFORE execution. 50+ packs across 17 categories: git, filesystem, databases, Kubernetes, cloud providers, CI/CD, and more. Fail-open design ensures you're never blocked by errors.

Local-first issue tracking for AI agents

Local-first issue tracking for AI agents. SQLite primary storage with JSONL export for git. Dependencies, labels, priorities (P0-P4), blocking relationships. Non-invasive: never runs git commands automatically. The bd alias provides backward compatibility.

Sub-100ms auth switching for AI coding agents

Manage multiple accounts for Claude Code, Codex CLI, and Gemini CLI with sub-100ms switching. Smart rotation algorithms, cooldown tracking, health scoring, and vault-based profile isolation for parallel agent sessions.

Multi-repo sync with AI-driven commit automation

Synchronize 100+ GitHub repos with one command. AI-assisted code review with priority scoring. Dependency updates across package managers. Pure Bash with git plumbing.

Skill management with MCP integration and adaptive suggestions

Dual persistence (SQLite + Git), hybrid search (BM25 + semantic + RRF), UCB bandit optimization, multi-layer security (ACIP + DCG), graph analysis via bv, MCP server for AI agents.

Transparent Rust build offloading to remote workers

Claude Code PreToolUse hook that offloads cargo builds to remote workers. Intercepts build commands, syncs source via rsync + zstd, compiles on server-grade hardware, and streams artifacts back.

Terminal hypervisor for multi-agent automation

A terminal hypervisor that captures pane output in real-time, detects AI agent state transitions via pattern matching, and enables event-driven automation across multi-agent swarms.

Research orchestration inspired by Sydney Brenner

Operationalizes Sydney Brenner's scientific methodology. Orchestrates multi-agent research sessions with hypothesis lifecycle tracking, discriminative test design, anomaly management, and evidence pack integration.

Browse and install battle-tested prompts as Claude Code skills

Browse a curated library of battle-tested prompts and install them directly as Claude Code skills. Works via CLI or web UI with interactive fzf-style picker.

Auto-deprioritize background processes for responsive dev workstations

Installs ananicy-cpp with curated rules to automatically deprioritize background processes. Includes sysmoni Go TUI with per-process IO throughput, FD counts, and JSON export. Works on Linux and WSL2.

Automated iterative spec refinement with extended AI reasoning

Automates multi-round specification review using GPT Pro 5.2 Extended Reasoning. Document bundling, convergence analytics, session management, and robot mode for coding agents.

Intelligent process termination with Bayesian scoring

Four-state classification model (Useful, Useful-but-bad, Abandoned, Zombie) with evidence-based posterior inference. Interactive TUI via gum, agent/robot mode for automation.

Ultra-fast search over X/Twitter data archives

Hybrid BM25 + semantic search over X/Twitter data exports. Zero-dependency local processing with Reciprocal Rank Fusion.

Download cloud images for visual debugging

Download images from iCloud, Dropbox, Google Photos, and Google Drive share links with intelligent four-tier capture strategy and MozJPEG compression.

Convert AI chat share links to Markdown and HTML

Archive AI conversations from ChatGPT, Claude, and Gemini share links into clean Markdown and HTML files.

Compress source code for maximum LLM context efficiency

Compress structured data into token-efficient TOON format, reducing LLM context usage by 30-50%.

Monitor AI CLI network traffic for debugging and analysis

Transparent proxy that logs all HTTP traffic from AI coding agents for debugging and analysis.

Convert web pages to clean Markdown for AI consumption

Fetch web pages and convert them to clean Markdown, perfect for including documentation in LLM context.

Interactive code-to-prompt generator with token counting

Terminal UI for selecting code files and generating structured, token-counted prompts with XML-like output format optimized for LLM parsing.

Transparent proxy routing for network traffic debugging

High-performance transparent proxy for routing and debugging network traffic in development environments.

Fix malformed ASCII diagrams from AI output

Automatically correct alignment and connection issues in ASCII diagrams generated by AI or written by hand.

Track LLM provider usage and costs across agents

Monitor token usage, API costs, and rate limits across Claude, OpenAI, and other LLM providers.

Two-tier hybrid search with progressive delivery

BM25 lexical + semantic retrieval in a single binary. Returns fast initial results then refines with ML models. JSON API for agent integration.

Predictive disk-pressure defense for AI workloads

Monitors disk usage and maintains a ballast pool of pre-allocated files that can be instantly released when disk pressure spikes during builds or large clones.

Resume coding sessions across AI providers

Converts session history between Claude, Codex, Gemini, and 14+ providers. Resume work started in one agent using another without losing context.

Fallback release infra when CI is throttled

Reuses your existing GitHub Actions YAML to build releases locally via nektos/act when GitHub Actions is unavailable or rate-limited.

Git-versioned backups for AI agent configs

Creates per-agent git repositories that version-control configuration folders. Supports 13+ agent types with full history and easy restoration.

Stop Claude from forgetting project rules after compaction

A Claude Code hook that detects context compaction events and injects a reminder to re-read AGENTS.md, preventing agents from forgetting project rules.

These aren't hypothetical scenarios. These are actual daily workflows running across 8+ projects with multiple AI agents.

Keep multiple projects moving forward simultaneously, even when you don't have mental bandwidth for all of them.

Come back 3+ hours later to find incredible autonomous progress across all projects

Have your agents review each other's work to catch bugs, errors, and issues before they become problems.

Multiple agents catching each other's errors before they ship

Transform massive planning documents into executable, dependency-tracked task graphs that agents can work through systematically.

Project nearly complete the same day, agents pushing commits while you're in bed

Have agents deeply investigate code with fresh perspectives, finding bugs that humans miss.

Systematic, methodical bug discovery and correction

Start your day with all repos synced, agents spawned, and ready to execute tasks across the fleet.

Full fleet of repos synced and agents working before your first coffee is done

Use RU's Agent Sweep to intelligently commit dirty repos across your entire fleet with AI-generated commit messages.

20+ repos committed with intelligent, contextual messages while you're away

Run multiple heavy agents simultaneously without your workstation becoming unresponsive. SRPS keeps everything smooth.

Run 6+ heavy agents simultaneously without system lockup - SRPS keeps your UI snappy

Copy these prompts to your Stream Deck or command palette. Each takes under a second to execute with a single button press.

I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by. Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with "fresh eyes" to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them.

When: When you want agents to find hidden bugs and understand the codebase deeply

Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep!

When: After agents have been working independently, have them review each other

I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high-quality, like Stripe-level apps.

When: When dissatisfied with UX but don't have energy to grapple with it directly

OK so please take ALL of that and elaborate on it more and then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.)

When: After generating improvement suggestions, turn them into actionable tasks

Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things!

When: Before executing a large batch of beads, validate the plan

OK, so start systematically and methodically and meticulously and diligently executing those remaining beads tasks that you created in the optimal logical order! Don't forget to mark beads as you work on them.

When: After planning and validation, execute the work

Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover.

When: After a batch of implementation work, review everything

Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files.

When: Final step after all work is done

Each tool amplifies the others. The synergies compound over time.

NTM spawns agents that register with Mail for coordination. They use BV to find tasks to work on. The result: autonomous agents that figure out what to do next without human intervention.

“Spawn 6 agents across 3 projects. Each finds work via BV, coordinates via Mail. You return 3 hours later to merged PRs.”

CASS indexes all agent sessions for instant search. CM stores learnings as procedural memory. Together: agents that never repeat mistakes and always remember what worked.

“New agent asks 'how did we handle auth?' CASS finds the answer in 60ms. CM surfaces the playbook that worked.”

UBS catches bugs before they're committed. SLB prevents dangerous commands from running without approval. Together: aggressive automation with guardrails.

“Agent finds a bug, wants to `git reset --hard`. SLB requires a second agent to approve. UBS validates the fix before merge.”

SLB sends approval requests directly to agent inboxes via Mail. Recipients can review context and approve or reject. Fully auditable decision trail.

“Agent proposes database migration. SLB notifies reviewers via Mail. Second agent reviews diff, approves. Audit log preserved.”

BV tracks task patterns and completion history. CM stores what approaches worked. Together: each new task benefits from all past solutions.

“Similar bug appears in new project. CM surfaces the pattern. BV creates bead linking to successful prior fix.”

CAAM manages API keys for all your agent accounts. NTM spawns agents with the right credentials automatically. Seamless multi-account workflows.

“Rate limited on one Claude account? NTM spawns agents with fresh credentials from CAAM. No manual switching.”

RU syncs all your repos with parallel workers. NTM spawns agents into each repo. BV tracks tasks across the entire fleet. Coordinated progress across dozens of projects.

“Morning: `ru sync -j4`. RU clones 3 new repos, pulls 15 updates. NTM spawns agents. By lunch, beads completed across 8 projects.”

RU agent-sweep can coordinate via Mail to prevent conflicts. Agents claim repos before committing. Complete audit trail of which agent touched which repo.

“Agent A claims repo-1, Agent B claims repo-2. Both run agent-sweep in parallel. No conflicts, clear ownership.”

DCG blocks dangerous commands before execution. SLB provides a human-in-the-loop confirmation after Claude proposes risky operations. Together they create defense in depth - DCG catches obvious destructive patterns, SLB catches contextual risks that require human judgment.

“Claude proposes 'rm -rf ./old_code' - DCG blocks it instantly. Claude rephrases to 'mv ./old_code ./archive' - SLB prompts for confirmation before the move.”

NTM spawns multiple Claude agents. Each agent runs under DCG protection. If one agent attempts something dangerous, DCG blocks it and can notify via Mail so other agents (or you) know what happened.

“Agent 1 working on repo cleanup tries 'git clean -fdx'. DCG blocks it. Mail notification: 'Agent 1 attempted blocked command in project-x'.”

Each tool installs in under 30 seconds. Written in Go, Rust, TypeScript, Python, and Bash.

Agent cockpit for multi-agent tmux sessions

Orchestrate multiple AI coding agents across tmux sessions. Spawn Claude, Codex, and Gemini agents in named panes. 80+ commands for session management, prompt broadcasting, file conflict detection, and context rotation. Persistent sessions survive SSH disconnects.

Like Gmail for AI coding agents

A complete coordination system for multi-agent workflows. Agents register identities, send/receive messages, search conversations, and declare file reservations to prevent edit conflicts. HTTP-only FastMCP server with static export and Web UI.

Pattern-based bug scanner with 1000+ detection rules

AST-grep patterns detecting 1000+ bug types across 8 languages. 18 detection categories from null safety to security vulnerabilities. Sub-5-second scans. Auto-wires into Claude Code, Codex, Cursor, Gemini, and Windsurf agents.

Graph-theory triage engine for task prioritization

Transforms task tracking with DAG-based analysis. Nine graph metrics, robot protocol for AI, time-travel diffing. Agents use BV to figure out what to work on next.

Local-first issue tracking for AI agents

Local-first issue tracking for AI agents. SQLite primary storage with JSONL export for git. Dependencies, labels, priorities (P0-P4), blocking relationships. Non-invasive: never runs git commands automatically. The bd alias provides backward compatibility.

Blazing-fast search across AI coding agent sessions

Unified search for all AI coding sessions. Indexes 11 agent formats: Claude Code, Codex, Cursor, Gemini, ChatGPT, Cline, Aider, Pi-Agent, Factory, OpenCode, Amp. Tantivy-powered <60ms queries with optional semantic search.

Procedural memory system for AI coding agents

Transforms scattered agent sessions into persistent, cross-agent memory. Patterns discovered in Cursor automatically help Claude Code on the next session. Three-layer cognitive architecture: Episodic → Working → Procedural.

Sub-100ms auth switching for AI coding agents

Manage multiple accounts for Claude Code, Codex CLI, and Gemini CLI with sub-100ms switching. Smart rotation algorithms, cooldown tracking, health scoring, and vault-based profile isolation for parallel agent sessions.

Two-person rule for dangerous command approval

Nuclear-launch-style safety for AI agents. Four risk tiers (CRITICAL/DANGEROUS/CAUTION/SAFE) with 40+ regex patterns. CRITICAL commands require 2+ approvals from different agents. Cryptographic signing, rollback support, and outcome analytics.

SIMD-accelerated safety net for dangerous commands

Claude Code PreToolUse hook blocking dangerous commands BEFORE execution. 50+ packs across 17 categories: git, filesystem, databases, Kubernetes, cloud providers, CI/CD, and more. Fail-open design ensures you're never blocked by errors.

Multi-repo sync with AI-driven commit automation

Synchronize 100+ GitHub repos with one command. AI-assisted code review with priority scoring. Dependency updates across package managers. Pure Bash with git plumbing.

Skill management with MCP integration and adaptive suggestions

Dual persistence (SQLite + Git), hybrid search (BM25 + semantic + RRF), UCB bandit optimization, multi-layer security (ACIP + DCG), graph analysis via bv, MCP server for AI agents.

Transparent Rust build offloading to remote workers

Claude Code PreToolUse hook that offloads cargo builds to remote workers. Intercepts build commands, syncs source via rsync + zstd, compiles on server-grade hardware, and streams artifacts back.

Terminal hypervisor for multi-agent automation

A terminal hypervisor that captures pane output in real-time, detects AI agent state transitions via pattern matching, and enables event-driven automation across multi-agent swarms.

Research orchestration inspired by Sydney Brenner

Operationalizes Sydney Brenner's scientific methodology. Orchestrates multi-agent research sessions with hypothesis lifecycle tracking, discriminative test design, anomaly management, and evidence pack integration.

Browse and install battle-tested prompts as Claude Code skills

Browse a curated library of battle-tested prompts and install them directly as Claude Code skills. Works via CLI or web UI with interactive fzf-style picker.

Auto-deprioritize background processes for responsive dev workstations

Installs ananicy-cpp with curated rules to automatically deprioritize background processes. Includes sysmoni Go TUI with per-process IO throughput, FD counts, and JSON export. Works on Linux and WSL2.

Automated iterative spec refinement with extended AI reasoning

Automates multi-round specification review using GPT Pro 5.2 Extended Reasoning. Document bundling, convergence analytics, session management, and robot mode for coding agents.

Intelligent process termination with Bayesian scoring

Four-state classification model (Useful, Useful-but-bad, Abandoned, Zombie) with evidence-based posterior inference. Interactive TUI via gum, agent/robot mode for automation.

Ultra-fast search over X/Twitter data archives

Hybrid BM25 + semantic search over X/Twitter data exports. Zero-dependency local processing with Reciprocal Rank Fusion.

Download cloud images for visual debugging

Download images from iCloud, Dropbox, Google Photos, and Google Drive share links with intelligent four-tier capture strategy and MozJPEG compression.

Convert AI chat share links to Markdown and HTML

Archive AI conversations from ChatGPT, Claude, and Gemini share links into clean Markdown and HTML files.

Compress source code for maximum LLM context efficiency

Compress structured data into token-efficient TOON format, reducing LLM context usage by 30-50%.

Monitor AI CLI network traffic for debugging and analysis

Transparent proxy that logs all HTTP traffic from AI coding agents for debugging and analysis.

Convert web pages to clean Markdown for AI consumption

Fetch web pages and convert them to clean Markdown, perfect for including documentation in LLM context.

Interactive code-to-prompt generator with token counting

Terminal UI for selecting code files and generating structured, token-counted prompts with XML-like output format optimized for LLM parsing.

Transparent proxy routing for network traffic debugging

High-performance transparent proxy for routing and debugging network traffic in development environments.

Fix malformed ASCII diagrams from AI output

Automatically correct alignment and connection issues in ASCII diagrams generated by AI or written by hand.

Track LLM provider usage and costs across agents

Monitor token usage, API costs, and rate limits across Claude, OpenAI, and other LLM providers.

Two-tier hybrid search with progressive delivery

BM25 lexical + semantic retrieval in a single binary. Returns fast initial results then refines with ML models. JSON API for agent integration.

Predictive disk-pressure defense for AI workloads

Monitors disk usage and maintains a ballast pool of pre-allocated files that can be instantly released when disk pressure spikes during builds or large clones.

Resume coding sessions across AI providers

Converts session history between Claude, Codex, Gemini, and 14+ providers. Resume work started in one agent using another without losing context.

Fallback release infra when CI is throttled

Reuses your existing GitHub Actions YAML to build releases locally via nektos/act when GitHub Actions is unavailable or rate-limited.

Git-versioned backups for AI agent configs

Creates per-agent git repositories that version-control configuration folders. Supports 13+ agent types with full history and easy restoration.

Stop Claude from forgetting project rules after compaction

A Claude Code hook that detects context compaction events and injects a reminder to re-read AGENTS.md, preventing agents from forgetting project rules.

Each tool does one thing well. They compose through JSON, MCP, and Git.

Every tool has --robot mode. Designed for AI agents to call programmatically.

The flywheel effect: each tool makes the others more powerful.

Born from daily use with 3+ AI agents on production codebases.

The Agent Flywheel installer sets up all flywheel tools automatically. From zero to multi-agent workflows in 30 minutes.

---

## The Core Flywheel

**URL:** https://agent-flywheel.com/core-flywheel

**Contents:**
- The Core Flywheel
- Why a Simpler Starting Point
  - Who This Is For
- Five Terms You Need
  - How the Tools Work Together (Behind the Scenes)
- The Core Loop
    - Six stages, one loop, compounding leverage
      - Plan
  - Normal Chat Coding vs. The Core Loop
    - Why the tools matter

Three tools. One loop. Most of the value. Learn the beginner-friendly core of the Agentic Coding Flywheel: Agent Mail for coordination, br for task structure, and bv for intelligent routing.

The full Flywheel system has grown large enough that many people find it overwhelming on first contact. That reaction makes sense. But there is a much smaller core that already captures most of what makes the approach powerful.

The larger system includes planning workflows, memory systems, prompt libraries, launch tooling, safety tooling, skills, and a lot of accumulated operational detail. You do not need to absorb all of that up front.

The core loop uses just three tools. If you understand those three and use them together correctly, you already have the heart of the system.

Separate the process into two layers: the planning substrate (frontier models used to create and refine the markdown plan) and the core operating loop (Agent Mail, br, and bv once the plan is ready to drive execution).

This document is for a relatively smart software developer who is new to agentic coding and does not want to absorb the entire larger Flywheel guide up front. The goal is narrower: get you to the point where you can coordinate multiple agents without chaos, keep work organized as explicit tasks with dependencies, and keep agents working on the best next unblocked task instead of choosing randomly.

If that works well for you, the larger Flywheel stack becomes much easier to appreciate later.

If these five terms stay clear in your head, most of the rest of the guide gets much easier to follow.

You do not need to manually manage the coordination between these tools. When your AGENTS.md file is set up correctly, the agents handle the integration automatically: they use bead IDs as thread identifiers in Agent Mail, they announce claims and reserve files before editing, and they update bead status as they work. You configure this once in AGENTS.md and then the agents just do it.

The core loop is simple: generate a plan, encode it as beads, launch agents with marching orders, let them coordinate through Agent Mail while bv routes them toward the best next bead, and tend the swarm until the graph is done.

Each closed bead reshapes the graph. The next agent gets a better map. Click any stage to see the details.

Create & refine markdown plan with multiple frontier models

Ask 3+ frontier models, synthesize

Planning tokens are far cheaper than implementation tokens

The core loop moves work out of ephemeral chat and into explicit, inspectable artifacts. That is the short answer to "why bother?"

Four agents, six tasks, side by side. One side uses the core loop, the other does not. Press Start.

All agents boot up and read the codebase

All agents boot up and read the codebase

Four agents spin up in parallel and read the same codebase. Without coordination tools, they have no way to know what the others are doing.

These three tools solve three different failure modes. Each helps on its own, but the value shows up most clearly when they form a stable loop together.

Without Agent Mail, multiple agents constantly collide: two agents edit the same files, nobody knows who is doing what, messages disappear into chat history, and work gets stranded when an agent crashes.

Agent Mail gives agents a shared coordination layer with identities, threads, inboxes, and file reservations. Agents announce what they are doing, reserve edit surfaces, and recover when another agent disappears. All of this happens automatically once your AGENTS.md tells agents to use Agent Mail.

Without br, work collapses into vague conversational intentions: "fix the auth stuff," "clean up the admin area," "someone should improve tests." That kind of tasking is too fuzzy for a swarm.

br turns work into explicit beads with status, priority, and dependencies. Once work is represented that way, multiple agents can make progress without constant human steering.

Even with good beads, agents still need to know what to do next. Without bv, they choose work based on local convenience or whatever they most recently saw in context.

bv reads the bead graph and computes what is most worth doing next. That turns the swarm from "many agents doing work" into "many agents pushing the project forward efficiently."

Hover or tap to inspect each piece. Click again to remove it and watch the system lose a capability it cannot replace. This is the Coordination Triangle.

The high-bandwidth negotiation layer.

The durable, localized issue state.

The graph-theory compass for triage.

The trio is not three nice-to-have tools. It is one operating system split into memory, communication, and leverage analysis. Remove any side of the triangle and the swarm loses determinism.

One reason agentic coding feels confusing at first is that the active artifact keeps changing. The easiest way to stay oriented is to know what the current artifact means and what you do with it next.

An idea becomes a plan, a plan becomes beads, beads become finished code. Click any stage to see the artifact, what it means, and your next move.

You know the goal, not the system.

Turn it into a serious markdown plan.

Raw idea to finished code. Each stage adds precision.

Prose becomes executable memory. This is where agents stop guessing.

Each completed bead reshapes the graph and unblocks new work. Finished beads create ready beads.

Plan space is where you decide the workflows, constraints, architecture, and testing expectations. Bead space is where you transform that thinking into executable memory for agents. Code space is where agents implement the local task that a bead defines.

The general rule is simple. Debates belong in plan space. Translation and dependency shaping belong in bead space. Implementation belongs in code space.

A strong plan lets a fresh reader answer five questions without guessing: what are the main workflows? What constraints matter? What architecture are we choosing? How will we know it works? What failure cases must not disappear into hand-waving?

It gives a fresh agent workflows, constraints, architecture, testing, and failure handling in one place. Before you turn the plan into beads, check that these five questions are answerable from the plan alone.

When something feels wrong, use the smallest escalation that actually fits the problem:

A small project makes the workflow easier to picture. Imagine building an internal tool called Atlas Notes: team members upload Markdown notes, the system tags and indexes them, users can search them quickly, and admins can inspect failed ingestions.

If you gave four agents only that vague description, they would step on each other and make mismatched assumptions. The core loop instead looks like this:

The bead is the unit of work agents actually execute. Weak beads force improvisation. Rich beads make execution mechanical. Here is a real bead from the ACFS project:

The prose does not need polish. A fresh agent should be able to understand the task, the reason for it, and the acceptance criteria without reopening the whole markdown plan. You can browse real beads from actual Flywheel projects at FrankenEngine, FrankenTUI, and Asupersync.

Quality thresholds get easier to feel when you compare weak and strong versions directly. The weak version names a topic. The strong version scopes the actual requirement, constraint, and testing obligation.

A weak artifact names a topic. A strong one carries scope, constraints, and a test plan. See the difference.

The weak version names a topic. The strong version scopes the actual requirement, the constraint, and the testing obligation.

Once you launch agents with good marching orders, they automatically handle the coordination mechanics. A typical bead thread in Agent Mail looks like this — created entirely by agents, not by you:

You do not write these messages. The agents create them because your AGENTS.md tells them to coordinate through Agent Mail and use bead IDs as thread anchors. Your job is to monitor these threads to see if work is flowing or stuck.

This section describes what you, the human, actually do. The agents handle the coordination plumbing (Agent Mail messages, file reservations, bead status updates). Your job is to create the conditions for them to succeed.

Steps 3-5 repeat for every bead. You stop thinking about the process after the second cycle.

Ask 3+ frontier models for competing plans, synthesize into one

A markdown plan covering workflows, architecture, and tests

Ask 3+ frontier models for competing plans, synthesize into one

A markdown plan covering workflows, architecture, and tests

Before beads or swarms or file reservations, create a serious markdown plan. Do not settle for one quick draft from one model.

GPT Pro web app with Extended Reasoning, or your strongest available model

Different frontier models have different blind spots. Competitive synthesis forces the model to admit where others are better and merge the strongest ideas.

At minimum, you want: the user-facing workflows, the important constraints, the major architectural decisions, and the testing expectations.

You do not need to manually create every bead yourself. Tell a coding agent to do the conversion:

Claude Code with Opus

Beads become the active source of truth for execution. Once they're strong enough, you never look back at the markdown plan.

Then polish the beads 4-6 times with fresh review passes. Each round catches things the previous round missed. This is the "measure twice, cut once" of the methodology.

Once beads are polished and your AGENTS.md is solid, start up a swarm of agents. Give each one these marching orders:

Every agent in the swarm gets this as their initial prompt

Every agent is fungible and a generalist. The specifics come from AGENTS.md and the beads, not from the prompt. This generic prompt works for every project.

Stagger agent starts by at least 30 seconds to avoid the "thundering herd" problem where all agents grab the same bead. Start smaller than your ego wants to: 1 agent to learn, 2 to feel coordination, 4 for real swarm behavior.

Now you are the operator. On roughly a 10-15 minute cadence, check on the swarm:

That is usually enough to keep the loop healthy without turning the human into a full-time traffic cop.

After agents finish each bead, have them review their own work:

After each bead is implemented — run until no more bugs found

Forces a mode switch from writing to adversarial reading while the code is still fresh. One of the cheapest quality multipliers in the whole method.

Then they move to the next bead using bv to find the most impactful one. The cycle repeats until the graph is done.

The human is not supposed to micromanage every code edit or manually coordinate Agent Mail threads. The human is there to keep the structure clean enough that the agents can work effectively inside it.

You design the system and tend the swarm. Agents do the coordination work.

GPT Pro, Claude, Gemini web apps

Ask multiple frontier models for competing plans, then synthesize into one strong design document

This is where 85% of your thinking goes. No code yet.

All of this is configured once in your AGENTS.md. You do not need to manually invoke Agent Mail calls, update bead statuses, or thread bead IDs into messages. The agents do it because the operating manual tells them to.

When the swarm looks active but you suspect it is not actually closing the real gap, stop and ask:

If the answer is "no," the fix is usually not more implementation effort. Revise the bead graph, add missing work, or step back into planning.

Even in the smaller core-loop version, you still need a minimal AGENTS.md. It does not have to be a giant doctrine document, but it should say:

When an agent vanishes mid-bead, the recovery path should be boring:

At some point, the workflow stops feeling like extra ceremony and starts feeling like a calmer control surface:

That operator feeling is a good sign. It usually means the artifacts are carrying the work instead of your short-term memory.

People often assume the magic of the Flywheel comes from the total number of tools. It does not. Most of the value comes from three things:

Those three properties are already present in the core loop. That is why the smaller system gets you surprisingly far.

You probably do not need it for a tiny one-file change with no real dependency structure, a purely local experiment, or a quick one-agent cleanup that does not need externalized coordination.

The loop earns its keep when work has enough structure, enough ambiguity, or enough parallelism that explicit planning, explicit tasks, and explicit coordination start paying for themselves.

Once the core loop is running smoothly, three helper utilities significantly improve safety, quality, and learning. They are multipliers on top of the core loop, not prerequisites.

A Claude Code hook that blocks dangerous git and filesystem commands before execution. Sub-millisecond latency, mechanical enforcement.

Works automatically. When a dangerous command is blocked, use safer alternatives or ask the user to run it manually.

Multi-language bug scanner with guardrails. Run it on changed files before every commit to catch injection, unquoted variables, and other hazards.

ubs <changed-files> before every commit. Exit 0 = safe. Exit >0 = fix and re-run.

Indexes prior agent conversations so solved problems can be reused. Finds patterns, decisions, and solutions across session history.

Search before reinventing a solution. If an agent solved a similar problem before, CASS will find it.

If you are just getting started, you do not need to master all of this immediately:

Those things help. Some help a lot. But they are multipliers on top of the core loop, not prerequisites. You can run the core loop with separate terminal tabs and no special session manager.

Even in the smaller version, a few principles still matter a lot:

If you violate those, the workflow quickly degrades back into ordinary multi-agent chaos.

Start smaller than your ego wants to:

If you want to feel the method instead of only reading about it:

Those five steps are enough to make the core loop stop feeling theoretical.

If you want the loop on one screen, keep this:

Move up to the full guide when one or more of these becomes true:

At that point, the bigger document stops feeling like overhead and starts feeling like leverage.

Once the core loop feels natural, the full methodology adds richer planning workflows, memory systems, prompt libraries, and the complete Dicklesworthstone stack.

**Examples:**

Example 1 (unknown):
```unknown
## Upload workflow
```

Example 2 (unknown):
```unknown
- Users drag Markdown files into the upload surface.
```

Example 3 (unknown):
```unknown
- The system parses frontmatter plus body text and stores a normalized note record.
```

Example 4 (unknown):
```unknown
## Constraints
```

---

## Welcome & Overview

**URL:** https://agent-flywheel.com/learn/welcome

**Contents:**
- Welcome & Overview
  - New to ACFS?
- What You Now Have
  - Beautiful Terminal
  - Modern CLI Tools
  - Language Runtimes
  - Three Coding Agents
- The Mental Model
  - ACFS Architecture Explorer
- What You'll Learn

Understand what you have and what you're about to learn

Complete the setup wizard first to get the most from these lessons.

Understand what you have and what you're about to learn.

Congratulations! You've just set up a fully-armed agentic engineering workstation.

Here's what's installed on your VPS:

zsh, Oh My Zsh, and Powerlevel10k for a stunning shell experience

lsd, bat, ripgrep, fzf, and zoxide for supercharged productivity

JavaScript (Bun), Python (uv), Rust, and Go ready to go

Claude Code (cc), Codex CLI (cod), and Gemini CLI (gmi)

Think of your setup like this:

Click any component to explore

Select a component to see details, commands, and dependencies

Your laptop is just the remote control. The real work happens on the VPS.

If your SSH connection drops? No problem. Your work continues in tmux.

Navigating the filesystem with confidence

Staying connected to your VPS

Persistent sessions that survive disconnects

Talking to Claude, Codex, and Gemini

Orchestrating multiple agents at once

Putting it all together for maximum velocity

Mark complete to track your learning progress.

---

## Learning Hub

**URL:** https://agent-flywheel.com/learn

---

## AI AgentsCoding For You

**URL:** https://agent-flywheel.com/

**Contents:**
- AI AgentsCoding For You
  - The Flywheel Methodology
  - The Core Flywheel
- Everything You Need
  - One-liner Install
  - Three AI Agents
  - Idempotent & Safe
  - Vibe Mode
  - Modern Shell
  - Interactive Tutorial

Transform a fresh cloud server into a fully-configured agentic coding environment. Claude Code, OpenAI Codex, Google Gemini: all pre-configured with 30+ modern developer tools. All totally free and open-source.

The definitive guide to planning-first agentic development: decompose complex projects into beads, detect convergence, coordinate agent swarms, and ship 10× faster with the Flywheel approach.

New to the Flywheel? Start with just three tools — Agent Mail, beads, and bv. This focused guide covers the core loop that captures most of the methodology's value, without the full system's complexity.

A single curl command installs and configures your complete agentic coding environment

A single command transforms your VPS. No manual configuration, no dependency hell.

Claude Code, Codex CLI, and Gemini CLI, all configured with optimal settings for coding.

Re-run anytime. Idempotent phases resume on failure. SHA256 verified installers.

Passwordless sudo with dangerous flags enabled for maximum velocity on throwaway VPS environments.

zsh + oh-my-zsh + powerlevel10k with lsd, atuin, fzf, and zoxide; developer UX perfected.

Run 'onboard' after setup for guided lessons from Linux basics to full agentic workflows. Preview lessons

Twenty interconnected tools that transform multi-agent workflows. Each tool enhances the others.

The wizard guides you from "I have a laptop" to "AI agents are coding for me"

Agentic workflows need dedicated compute. A VPS gives you a 24/7 server that's always ready.

AI agents consume significant RAM and CPU. Running them locally drains your battery and slows everything down.

Each agent uses ~2GB RAM. With 10+ agents, you need 48-64GB—more than most laptops have.

Cloud giants charge by the hour and make billing unpredictable. A dedicated VPS is simpler and cheaper.

A 64GB VPS costs ~$40-56/month flat. Equivalent cloud resources would cost 3-5x more.

Your VPS runs 24/7. Queue up tasks before bed, wake up to completed code.

AI agents can refactor, test, and iterate autonomously—compounding progress overnight.

Ready to see if this approach is right for you?

We believe in radical transparency. Here's who will get the most value from this setup.

You want AI to write real, production code for you

Full implementations, not just suggestions

Sites like Lovable.dev are too limiting for what you want to build

You need full control and complexity

You're willing to invest ~$500/month in AI subscriptions

Claude Max + ChatGPT Pro + VPS hosting

You can follow step-by-step instructions

No coding experience required, just patience

You want a completely free solution

AI subscriptions have real costs

You only want occasional AI help with snippets

This is for full agentic workflows

You're looking for mobile-first development

This requires a desktop or laptop

You need enterprise compliance out of the box

This is for individual developers

Sound like you? Let's talk about the investment.

Complete transparency: here's what you'll actually pay each month. The tools are free; you pay for the AI services.

64GB RAM Ubuntu server (Contabo, OVH)

64GB RAM for 10+ agents

Anthropic's Claude Code CLI

$400 for power users (2 accounts)

ChatGPT 5.2 Pro for extended thinking planning

Essential for plan documents

Estimated Monthly Total

Consider: a junior developer costs $5,000+/month. For under $700, you get 10+ AI agents working 24/7, writing code while you sleep.

I'm Jeffrey Emanuel, and I built this because I was being inundated with requests from friends, older relatives, and strangers on the internet asking me to help them get started with using AI for software development.

I wanted one resource I could point people to that would help them "from soup to nuts" in getting set up; even if they have almost no computer expertise, just motivation and desire.

This is also a platform to share my suite of totally free, open-source agentic coding tools. I originally built these for myself to move faster in my consulting work with Private Equity and Hedge Funds. Now I want to help others be more productive and creative too.

Created by Jeffrey Emanuel

---

## The Agentic Coding FlywheelTL;DR EditionTL;DR Edition

**URL:** https://agent-flywheel.com/tldr

**Contents:**
- The Agentic Coding FlywheelTL;DR EditionTL;DR Edition
- Why a Flywheel?
- Core Flywheel Tools
  - Mail
    - Why It's Useful
    - Key Features
    - Tech Stack
    - Synergies
  - BV
    - Why It's Useful

16 core tools and 13 supporting utilities that transform multi-agent AI coding workflows. Each tool makes the others more powerful - the more you use it, the faster it spins. While others argue about agentic coding, we're just over here building as fast as we can.

A flywheel stores rotational energy - the more you spin it, the easier each push becomes. These tools work the same way. The more you use them, the more valuable the system becomes.

Every agent session generates searchable history (CASS). Past solutions become retrievable memory (CM). Dependencies surface bottlenecks (BV). Agents coordinate without conflicts (Mail). Each piece feeds the others.

The result: I shipped 20,000+ lines of production Go code in a single day with BV. The flywheel keeps spinning faster - my GitHub commits accelerate each week because each tool amplifies the others.

Hover over tools to see connections

The backbone of multi-agent development: session management, communication, task tracking, static analysis, memory, search, safety guards, multi-repo sync, and automated setup. These tools form a self-reinforcing loop where each makes the others more powerful.

A mail-like coordination layer for multi-agent workflows. Agents send messages, read threads, and reserve files asynchronously via MCP tools - like Gmail for AI coding agents. HTTP-only FastMCP transport with static export.

Critical for multi-agent setups. When 5+ Claude Code instances work the same codebase, they need to coordinate who's editing what. Agent Mail prevents merge conflicts via advisory file reservations with pre-commit guard enforcement, and builds an audit trail of all agent decisions via SQLite + Git dual persistence.

A fast terminal UI for viewing and analyzing Beads issues. Applies graph theory (PageRank, betweenness centrality, critical path) to identify which tasks unblock the most other work.

Issue tracking is really a dependency graph. BV lets Claude prioritize beads intelligently by computing actual bottlenecks. The --robot-insights flag gives PageRank rankings for what to tackle first.

Local-first issue tracking for AI agents. SQLite for fast local queries, JSONL export for git-friendly collaboration. Full dependency graph with blocking/blocked-by relationships, priorities P0-P4.

Your issues travel with your repo - no external service required. Non-invasive design: never runs git commands automatically. Agents can create, update, and close issues with simple CLI commands. The bd alias provides backward compatibility.

Coding Agent Session Search

Blazing-fast search across all your past AI coding agent sessions. Indexes 11 agent formats: Claude Code, Codex, Cursor, Gemini, ChatGPT, Cline, Aider, Pi-Agent, Factory, OpenCode, Amp. Sub-60ms queries with optional semantic search.

You've solved this problem before - but which session? CASS lets you search 'how did I fix that React hydration error' and instantly find the exact conversation. Three search modes (lexical, semantic, hybrid), HTML export with encryption, and multi-machine sync via SSH.

One-command bootstrap that transforms a fresh Ubuntu VPS into a fully-configured agentic coding environment. CLI provides doctor (47+ health checks), update (category-specific), cheatsheet (50+ aliases), and session management.

Setting up a new development environment takes hours. ACFS does it in 30 minutes, installing 30+ tools, three AI agents, and all flywheel tooling. Post-install CLI provides `acfs doctor` for health checks and `acfs update` for maintenance.

A meta-runner that fans out per-language scanners across 8 languages (JS/TS, Python, Go, Rust, C/C++, Java, Ruby, Swift). Uses ast-grep for AST-based pattern matching with 18 detection categories and 1000+ bug patterns.

AI coding agents move 10-100x faster than humans. UBS keeps pace with sub-5-second scans and auto-wires guardrails into Claude Code, Codex, Cursor, Gemini, and Windsurf agents. The --beads-jsonl output creates Beads issues directly from findings.

Destructive Command Guard

Claude Code PreToolUse hook that blocks dangerous commands BEFORE execution. 50+ packs across 17 categories: git (reset --hard, force push), filesystem (rm -rf), databases (DROP TABLE), Kubernetes, cloud providers, and more.

AI agents can and will run 'rm -rf /' if they think it solves your problem. DCG catches catastrophic commands before they execute with sub-millisecond latency. Safe directory exceptions (/tmp, /var/tmp, $TMPDIR) allow temp operations without friction.

Multi-repo management system: sync 100+ repos, AI-assisted code review with priority scoring, dependency updates across package managers, and agent-driven commit automation.

Managing 100+ repos manually is impossible. 'ru sync' handles clone/pull in parallel. 'ru review' discovers issues/PRs via GraphQL batch queries, scores by priority (security+50, bugs+30, age), and spawns isolated Claude Code sessions in worktrees.

Cross-agent procedural memory system. Transforms scattered sessions from all your AI agents into persistent, unified knowledge. Three-layer cognitive architecture: Episodic (raw sessions via CASS) → Working (diary summaries) → Procedural (playbook rules with confidence tracking).

A debugging technique discovered in Cursor is immediately available to Claude Code. Rules have 90-day decay half-life and 4× harmful weight for mistakes. Bad rules auto-invert into anti-pattern warnings. Every agent learns from every other agent's experience.

A multi-agent tmux orchestration tool with 80+ commands. Spawns Claude, Codex, and Gemini agents in named panes with type classification (cc/cod/gmi). Monitors context windows, detects file conflicts, and provides robot mode for automation.

Running multiple AI agents simultaneously creates chaos without orchestration. NTM provides the command center: spawn agents with one command, broadcast prompts to specific types, monitor context usage, and coordinate via Agent Mail. Sessions persist across SSH disconnects and system reboots.

Simultaneous Launch Button

Nuclear-launch-style two-person rule for dangerous commands. Four risk tiers classify commands via 40+ regex patterns: CRITICAL (2+ approvals), DANGEROUS (1 approval), CAUTION (30s auto-approve), SAFE (skip). Cryptographic signing, rollback support, and outcome analytics.

AI agents can and will run destructive commands if they think it solves your problem. SLB intercepts commands like 'rm -rf /', 'DROP DATABASE', and 'terraform destroy' requiring explicit approval from another agent or human reviewer before execution. Watch mode lets reviewing agents stream pending requests.

Local-first skill management platform: dual persistence (SQLite + Git), hybrid search (BM25 + semantic + RRF), UCB bandit optimization, multi-layer security (ACIP + DCG), graph analysis via bv, MCP server for AI agents.

AI agents need reusable context to be effective. MS doesn't just store skills—it learns which ones work via UCB bandit optimization. Context-aware auto-loading suggests skills based on project type. Pack contracts optimize token budgets. The MCP server makes skills native tools for any AI agent.

Remote Compilation Helper

Claude Code PreToolUse hook that offloads Rust compilation to remote workers. Intercepts cargo commands, syncs source via rsync + zstd, compiles on server-grade hardware, streams artifacts back.

Multi-agent swarms trigger many concurrent builds. RCH intercepts commands before execution and routes them to remote workers with health probes and priority scheduling. Agent detection coordinates builds across Claude Code, Codex, and Gemini sessions.

Coding Agent Account Manager

Manages multiple accounts for Claude Code, Codex CLI, and Gemini CLI with sub-100ms switching. Vault profiles store auth files for instant activation without browser flows. Smart rotation algorithms automatically select the best profile based on cooldown state, health, and usage patterns.

When running multiple agents, you'll hit rate limits. CAAM lets you switch accounts instantly - no browser login, no waiting. Profile isolation enables parallel sessions where each agent uses its own credentials. Health scoring (🟢/🟡/🔴) shows which profiles are ready vs. cooling down.

Terminal hypervisor that captures pane output in real-time, detects agent state transitions through pattern matching, and enables event-driven automation across multiple AI coding agents.

When running multiple AI agents in WezTerm, you need to know when they hit rate limits, complete tasks, or need approval. WA observes all panes with sub-50ms latency and triggers automated responses.

Multi-agent scientific research orchestration platform based on Sydney Brenner's methodology. Manages full research artifact lifecycle: hypotheses, discriminative tests, anomalies, critiques, and evidence packs with cockpit runtime for parallel agent sessions.

Transforms AI agents into a collaborative research group with rigorous scientific discipline. The Brenner approach emphasizes exclusion over accumulation, third-alternative thinking, and discriminative experiments that collapse hypothesis space fast.

Extend the ecosystem with GitHub issue sync, archive search, and prompt crafting utilities. These tools enhance the core flywheel for specialized workflows.

Get Image from Internet Link

Downloads full-resolution images from iCloud, Dropbox, Google Photos, and Google Drive share links using a four-tier capture strategy with headless Chromium automation.

When debugging remotely, users share cloud links but you're SSH'd into a headless server. GIIL's four-tier capture (download button → CDN interception → element screenshot → viewport fallback) ensures maximum quality retrieval for AI agent analysis.

System Resource Protection Script

Installs ananicy-cpp with curated rules to auto-deprioritize background processes. Includes sysmoni Go TUI (Bubble Tea) with IO throughput, FD counts, per-core sparklines, JSON export. Works on Linux and WSL2.

When running cargo build, npm install, or multiple AI agents, SRPS prevents unresponsive systems by lowering priority of known resource hogs. Safety-first: no automated process killing. Helper tools for diagnostics.

Ultra-fast search over X/Twitter data archives with sub-millisecond latency. Uses hybrid BM25 + semantic search with Reciprocal Rank Fusion. Indexes tweets, likes, DMs, and Grok conversations.

Your X archive is a goldmine of bookmarks, threads, and ideas, but Twitter's search is terrible. XF makes your archive instantly searchable (<10ms) with both keyword and semantic matching. DM context search shows full conversation threads.

World-class terminal UI for combining source code files into LLM-ready prompts. Tree explorer with vim-style navigation, live syntax preview, token counting, and structured XML-like output optimized for AI parsing.

Crafting prompts with code context is tedious and error-prone. S2P provides visual file selection with sizes and line counts, real-time token/cost estimation, quick file-type shortcuts (1-9,0,r), and produces structured output that LLMs parse reliably.

Automated Plan Reviser Pro

Iterative specification refinement via GPT Pro 5.2 Extended Reasoning + Oracle. Document bundling (README + spec + impl), convergence analytics with weighted scoring, session management, and robot mode JSON API for coding agents.

Complex specs need 15-20 review cycles. APR automates the loop: rounds 1-3 fix architecture, 4-7 refine interfaces, 8-12 handle edge cases, 13+ polish abstractions. Convergence score (≥0.75 = stable) tells you when to stop.

Official CLI for jeffreysprompts.com - browse, search, and install battle-tested prompts as Claude Code skills. Features interactive fzf-style picker and task-based suggestion engine.

Instead of writing prompts from scratch, install proven patterns. The interactive mode (jfp i) lets you fuzzy-search the entire library, while jfp suggest recommends prompts based on your task description. Premium features include collections, cross-machine sync, and a skills marketplace.

Bayesian-inference zombie/abandoned process detection using four-state classification (Useful, Useful-but-bad, Abandoned, Zombie) with evidence-based posterior probability scoring.

When builds hang or test runners go rogue, PT computes P(state|evidence) using process type, age, CPU/IO activity, memory, and past decisions. Confidence levels (very_high >0.99 to low <0.80) guide safe termination with identity validation and staged kill signals.

Token-Optimized Notation

Token-optimized notation format for efficient LLM context packing. Compresses structured data into a dense format that maximizes information per token.

LLM context windows are precious. TRU compresses JSON, YAML, and other structured data into a compact notation that conveys the same information in fewer tokens, letting you fit more context into each request.

Transparent HTTP/HTTPS proxy for debugging and inspecting network traffic. Routes requests through a local proxy for analysis.

When debugging API integrations or AI agent network calls, you need visibility into what's being sent and received. Rust Proxy provides transparent interception without modifying your code.

Network observer for AI CLI tools that logs requests and responses without proxying. Passive monitoring of LLM API traffic.

Understanding what your AI agents are actually sending to APIs helps with debugging, cost tracking, and optimization. RANO passively observes network traffic without adding proxy overhead.

Converts websites to clean Markdown for LLM consumption. Strips ads, navigation, and boilerplate to extract just the content.

AI agents need web content in a format they can understand. MDWB fetches pages and converts them to clean Markdown, perfect for feeding into LLM context windows.

ASCII Art Diagram Corrector

Fixes malformed ASCII art diagrams generated by AI. Corrects alignment, box characters, and connection lines.

AI models often generate ASCII diagrams with alignment issues, broken lines, or inconsistent characters. AADC automatically detects and fixes these problems.

Coding Agent Usage Tracker

Tracks LLM provider usage across multiple coding agents. Monitors API calls, token consumption, and costs.

When running multiple AI agents simultaneously, costs can spiral. CAUT provides visibility into which agents are using how many tokens and at what cost.

The fastest way to set up the entire flywheel ecosystem is with ACFS. One command, 30 minutes, and you're ready to go.

Or use the step-by-step wizard for guided setup.

---
