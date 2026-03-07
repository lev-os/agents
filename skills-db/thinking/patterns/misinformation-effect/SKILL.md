---
name: misinformation-effect
description: Recognize that memory is reconstructive and vulnerable to contamination by post-event information, leading to false but confident recollections
---

# Misinformation Effect

**What**: A cognitive bias where a person's memory of an event becomes less accurate due to information introduced after the event occurred. The post-event information merges with original memory, creating a false but felt-authentic recollection.

**When to use**: When conducting interviews, designing documentation systems, investigating incidents, collecting user feedback, or any situation where accurate recall matters and contamination is possible.

**Introduced by**: Elizabeth Loftus (1974-1978), demonstrated through false eyewitness testimony research

## Core Mechanism

Memory is not a recording—it's a reconstruction. Each time you recall an event, you rebuild it from fragments. Post-event suggestions, questions, or discussions can introduce new "fragments" that become integrated as if they were original observations.

**Key insight**: People cannot distinguish between genuinely remembered details and suggested details that feel like memories. Confidence in the false memory can be as strong as real memories.

## When to Apply

**Use awareness of misinformation effect when:**
- Conducting user interviews or research (question framing matters)
- Investigating incidents, outages, or accidents (separate witnesses, collect immediately)
- Documenting decisions (record contemporaneously, not retrospectively)
- Running postmortems (write individual timelines before group discussion)
- Gathering requirements (distinguish between "what happened" and "what we think happened")

**High-risk contexts:**
- Legal testimony and witness statements
- Medical history taking
- Security incident response
- Customer complaint investigation
- Performance feedback collection

## Execution Steps

### 1. Separate Before Contamination
Interview witnesses or participants individually before they discuss with others. Group conversations create shared false memories.

### 2. Collect Information Immediately
The longer the delay between event and documentation, the more susceptible memory becomes to suggestion. Log observations in real-time when possible.

### 3. Use Open-Ended Questions First
Start with "What happened?" rather than "Did you see X?" Leading questions introduce the very information you're trying to test for.

### 4. Document Source and Certainty
Track what was observed firsthand vs. heard from others. Ask "How certain are you?" to flag potentially contaminated memories.

### 5. Preserve Original Records
Keep first drafts, initial reports, and early notes. Don't overwrite—original documentation resists reconstruction bias.

### 6. Recognize Confidence ≠ Accuracy
High confidence in a memory doesn't validate it. Misinformation creates equally confident false memories.

### 7. Create Contamination Barriers
In incident response: Write individual timelines → Submit sealed → Group discussion only after. Prevents suggestion from spreading.

## Real-World Applications

**Loftus's Car Crash Study**: Participants shown accident footage, then asked "How fast were cars going when they smashed/hit/contacted?" The verb changed memory—"smashed" group later falsely remembered broken glass that wasn't there.

**Post-Incident Reviews**: Teams that discuss "what happened" together before writing individual accounts end up with homogenized (often inaccurate) collective memory.

**Customer Feedback**: Asking "Did the page feel slow?" implants the suggestion of slowness. Better: "How would you describe the page performance?" → Check logs for actual metrics.

**Code Review Discussions**: Discussing a bug before people review the code independently leads to groupthink about root cause. Have reviewers examine independently first.

## Key Indicators

**Signs of potential contamination:**
- Participants quote each other's phrasings
- Consensus forms quickly without evidence
- Details "remembered" after group discussion that weren't in initial reports
- Confidence increases after discussion despite no new hard evidence

**Protective factors:**
- Contemporaneous documentation exists
- Witnesses kept separate until after individual statements
- Open-ended questions used throughout
- Source attributions tracked (saw vs. heard vs. inferred)

## Common Mistakes

**Leading questions**: "The page was slow, right?" vs. "How did the page perform?"

**Group recall sessions**: Brainstorming what happened together before individual documentation.

**Overwriting original notes**: Cleaning up "messy" initial observations with post-hoc rationalization.

**Trusting confident memories**: Confidence and accuracy are weakly correlated, especially for contaminated memories.

## Related Frameworks

**Complementary**: Source Monitoring (tracking origin of memories), Availability Heuristic (recent discussions make details feel more "available")

**Contrasting**: Perfect Memory models, Rational Actor assumptions in traditional economics

**Sequential**: Event occurs → Immediate individual documentation → Protected from suggestion → Group analysis → Cross-reference with hard evidence

## Practical Examples

**Incident Response Protocol**:
1. Alert triggered at 2:47 PM
2. Responders write individual timelines in separate docs before Slack discussion
3. Submit sealed to incident commander
4. Group video call to coordinate response (but damage timeline already preserved)
5. Postmortem references individual timelines + logs, not group reconstruction

**User Research Interview**:
- ❌ "Did you find the checkout button confusing?"
- ✅ "Walk me through what you did after adding items to cart."
- ❌ "Most users have trouble with X. Did you?"
- ✅ "What, if anything, was challenging?"

**Performance Review**:
Document specific observations and examples at the time they occur, not during review season when months of subsequent information has accumulated.

## Red Flags

**Warning signs you're vulnerable:**
- "Let's all get in a room and piece together what happened"
- Updating documentation days/weeks after event
- Using others' recollections to jog your memory
- Treating memory as authoritative without corroborating evidence

**Contamination in progress:**
- Team members adopting each other's phrasing for events they witnessed separately
- Details "remembered" after discussion that weren't in initial accounts
- Convergence on narrative despite conflicting evidence

## Measurement

**Protective measures to track:**
- Time-to-documentation (target: < 1 hour for critical events)
- % of incidents with individual pre-discussion timelines
- Presence of contemporaneous logs/evidence vs. pure recall
- Interview transcripts showing question types (open vs. leading ratio)

**Contamination indicators:**
- Discrepancies between initial and later accounts
- Homogenization of independent witness statements
- Confidence ratings that increase without new evidence
- Reported details that match suggestions but not physical evidence

## Scoring Criteria

**Practitioner Weight**: 10/10 — Loftus's research directly influenced legal system reforms and expert witness standards; highly applied field with real-world consequences

**Clarity & Executability**: 8/10 — Clear mechanism and protective steps, though requires discipline to execute consistently

**Proven ROI**: 9/10 — Prevented wrongful convictions, improved incident response accuracy, foundational to cognitive interview techniques

**Novelty**: 8/10 — Counterintuitive that confident memories can be demonstrably false; challenged legal system's reliance on eyewitness testimony

**Cross-Domain Applicability**: 9/10 — Applies to law, medicine, UX research, incident response, journalism, organizational learning, everyday decision-making

**Total Score**: 44/50 (Tier 1: Canonical)
