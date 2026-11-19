# Fundamentals for shaping data, files and apps

Everything is still data: inputs, outputs and the architecture between them.
Apply each item that bears on the case; state the ones you skip and why.

## Domain model (ontology, taxonomy)

- Name the **things** people work with. Give each one an identity (what makes two
  records the same thing), an owner (who may change it) and a lifecycle (its states).
- Name the **relationships** with their cardinality (one guide has many pages).
- A taxonomy groups things; an ontology also says how they relate and change.
  A tag answers "what is this about?"; a relationship answers "what does it connect to?".
- Separate what exists today, what you infer, and what you propose.
- Test the model on one real record and one edge case (an item that fits two
  groups, an item that changes owner). Pick canonical terms; list the synonyms they replace.

## Datasets that do not match

Inspect before you consolidate:

| Check | Question |
|---|---|
| Grain | What does one row or file stand for? |
| Keys | Which field identifies it? Is it stable across sources? |
| Units and formats | Dates, measures, languages, encodings |
| Duplicates | Same thing under two keys, or two things under one key |
| Conflicts | Two sources disagree; which wins, and is it recorded? |
| Provenance | Where each value came from, so an edit can cite it |

Normalize each source to the shared model first, then consolidate into one
canonical set with one ID per thing and a mapping from every source ID.

## Files and folders

- One naming convention, stated with an example (`<id>/<lang>.json`).
- Each folder has one owner and one purpose.
- Mark source files apart from generated files, and name the command that generates them.
- One source of truth for each meaning; everything else is derived.

## App data flow

1. List the questions users need answered (find a page by guide and page ID).
2. Turn each into a query or lookup; this is the query plan.
3. Trace fetching, storage, updates and reads for each query.
4. Choose storage from the access and update needs: a relational store such as
   SQLite for queries across records, JSON for portable read-only content that
   any renderer can read, plain files for images and large blobs.
5. Show one concrete record in its final form.

## Other domains

Use the domain's native methods and artifacts, found through its owning skill.
