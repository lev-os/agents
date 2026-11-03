# Research / Workshop Intake Proof Artifact Pattern

Use this reference when a POC lane grows out of research intake: paper/video/repo capture, feature parity, many spike candidates, and an implementation roadmap.

## Durable pattern

When proving whether an external paper or ecosystem should shape Lev, treat `sources -> intake -> analysis -> verify` as one proof lane:

1. Preserve raw provenance first: PDF/API metadata, source tar/extracted source, video extract, and repo clone manifests.
2. Create a machine-readable source manifest with repo URL, local path, head SHA, role, evidence anchor, file count, and cleanliness.
3. Restore or verify captured clones before analysis; the durable lesson is `verify clean checkouts match manifest heads`, not the transient failure that made them dirty.
4. Produce both human and machine artifacts:
   - source inventory
   - repo intake summary JSON/TSV
   - paper insights
   - 1:1 feature parity matrix
   - POC spike set, with each spike carrying claim, verifier, artifact, ownership, and disposition
   - combined analysis
   - implementation roadmap
   - verification report
5. Verification should check presence/non-empty artifacts, JSON validity, manifest deliverables, repo cleanliness/head match, counts, and source evidence anchors.

## Ownership boundary to record

For self-evolving-agent / learning-loop POCs, explicitly separate:

- deterministic code: schemas, validators, redaction, eligibility, replay, scoring, clustering, classifiers, promotion/rollback, exports
- FlowMind/DNA/YAML: topology, evaluator slots, field allowlists, policies, allowed actions, lifecycle gates, rollout rules
- LLMs: bounded summaries, typed observations, critique normalization, candidate drafts, evidence narratives

LLMs must not own final scores, admission decisions, canonical mutation, or promotion.

## POC spike minimum schema

Each spike should include:

- claim
- verifier that can falsify the claim
- output artifact
- deterministic-code / YAML-policy / LLM ownership split
- lifecycle disposition: adopt, extract, monitor, or reject

## Verification report minimum counters

- required artifacts present/non-empty
- captured repo count
- clean repo checkout count
- POC spike count
- feature parity row count
- missing manifest deliverables
- source evidence checks for the central paper claims
