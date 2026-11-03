# Internal review bundles

Use this pattern when publishing a compact reader/review site from operational or product material.

## Source-of-truth boundary

1. Identify the canonical system before assembling the bundle (for example: a knowledge base or document system).
2. Treat exported/on-disk material as a **review mirror** unless the repository explicitly declares it canonical.
3. Add a short landing-page README that states: review purpose, source-of-truth boundary, included documents, and known evidence limits.
4. If the request refers to a prior *temporary wiki*, *dry run*, or *wiki on disk*, do not assume the local artifact is the intended source. Recover the prior session context, resolve the canonical root object, enumerate its children, and retrieve their current contents before rendering. Treat local mirrors only as review inputs—not proof of the canonical tree.
5. Do not imply that an operational report archive is a maintained wiki merely because it is rendered as one.

## Evidence hygiene

- Preserve provenance for every synthesized section; link or name the underlying source in the bundle.
- Label AI meeting summaries, indirect notes, and unvalidated research as directional evidence rather than settled fact.
- Keep proposed decisions visually and textually distinct from approved or live policy.

## Publication sequence

1. Render the static reader and verify local document navigation.
2. For internal material, obtain explicit approval for externally reachable publication after explaining the access-control limitation.
3. Publish only the reviewed bundle, with `index.html` at its root.
4. Perform live QA from the deployed URL: navigation, an expected substantive section, console, and a visual pass.
5. Report the live URL, permanence/expiry, and the source-of-truth boundary; do not represent publication as a canonical-system update.
