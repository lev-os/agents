# Sherlock child method

Load for explicit `research --sherlock`, dossiers, multi-round OSINT and saved
investigation resume. This selector is skill syntax, not a runtime flag.

1. Define target, audience, hypotheses, activated domains, source classes,
   exclusions and output directory. Confirm missing choices that materially
   change the investigation; do not pause for already-approved scope.
2. Agree a finite round/query/time/spend budget. Preserve the source presets
   (1 quick, 5 standard, 20 deep) as options, not authority to spend all rounds.
   Scope or budget expansion is a human decision.
3. Inspect `lev research --help` and the Sherlock graph plan. The implementation
   candidate is `/Users/jean-patricksmith/digital/leviathan/plugins/research/flows/sherlock.flow.yaml`.
   Execute only the implemented route and controls verified by qualification.
4. Run actual graph nodes for intake, scope/budget, round planning, collection,
   normalization and provenance, contradiction/confidence analysis, checkpoint,
   local dashboard and continue/stop. Ordinary deep POC compilation is insufficient.
5. Every round assesses leaf entities, weak relationships and domain gaps;
   generates entity, relationship, temporal, disconfirming and lateral queries;
   collects through the fixed routine/provider policy; deduplicates evidence.
6. Retain source URLs, publication/retrieval timestamps and independent ancestry
   for factual claims and edges. Keep observations separate from inferences,
   supporting evidence separate from contradicting evidence. Confidence labels
   need reliability, recency, independence and conflict rationale; numerical
   confidence is an analytic estimate, not calibrated probability or acceptance.
7. Checkpoint state and round/query history before dashboard generation. Resume
   from committed rounds without replaying them. Corrupt/incompatible state
   requires a visible error; never silently start a new investigation.
8. Build the dashboard from committed real state. Preserve dossier, entities,
   relationships, deductions, gaps, timeline, rounds, domains, confidence and
   source inspection. Saved sample assets are labeled examples, not findings.
   Local output does not authorize public deployment.
9. Report node outcomes and provider gaps. Required failure, timeout, cancellation
   or unfinished graph cannot be success. Budget-limited or partial output stays
   visibly partial and resumable. Stop at the agreed budget or a human decision.

The preserved `SOURCE.md`, `dashboard-template.html` and `data-sample.js` retain
source procedures, dual-graph/dashboard design and original state schema.
They are evidence references; source tool names are mapped to available runtime
adapters, not claims that those named tools exist on this host. Dashboard
publication and arbitrary domain expansion are superseded by explicit decisions.
Qualification in `../evaluation.json` distinguishes fixture, host and live proof.
