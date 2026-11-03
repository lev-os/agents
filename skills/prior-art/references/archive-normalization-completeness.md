# Archive normalization completeness audits

Use this when a normalized corpus claims to represent a raw export and the user needs to know whether it is semantically complete.

## Evidence chain

1. Read cache/state, pending-trigger, and receipt files first. Treat the receipt-recorded raw path and fingerprint as the primary lineage; do not silently substitute a newer-looking archive.
2. Inventory the normalized corpus by:
   - row count by artifact kind
   - unique source-object IDs by kind
   - repeated references versus byte-identical duplicate rows
   - presence of `text`, `content`, body, and excerpt fields
   - excerpt equality to file title/name
3. Inspect the normalization implementation when available. Record limits and fallbacks such as whitespace compaction, fixed excerpt length, or `plain_text -> preview_plain_text -> title`.
4. Compare normalized text to the raw source, not just normalized metadata. Count mapped records, mismatches, truncated records, and lost characters.

## ZIP audit without extraction

Use Python `zipfile` to inspect archives in place so the audit does not mutate evidence.

Distinguish these counts explicitly:

- ZIP file entries versus directory entries
- attachment path entries versus unique attachment IDs
- raw message records versus normalized semantic objects
- file references versus unique files
- channel-day JSON versus metadata JSON

Duplicate attachment paths are common. Parse the file ID from each member name and compare sets in both directions:

- normalized IDs missing a raw member
- raw members missing a normalized object
- raw file-reference IDs missing a downloaded member
- downloaded member IDs missing a raw file reference

## Slack huddle-specific checks

Slack huddle notes may be exported as extensionless `application/vnd.slack-docs` files containing HTML such as `quip-canvas-content`. The message/file metadata can have empty `plain_text` and `preview_plain_text`, causing normalized rows to contain only the huddle title even though the ZIP member contains substantial note text.

For huddles, report separately:

- huddle reference rows
- unique huddle note file IDs
- downloaded huddle path entries
- unique downloaded note documents
- note-body bytes and extracted visible text
- counts with Summary and Action Items sections
- minimal or “not enough to summarize” notes

Do not equate AI huddle notes with a full conversation transcript. Huddle-note HTML can link to a `huddle_transcript` file without embedding or downloading it. Extract every linked transcript ID, then check:

1. archive member names
2. attachment IDs in message JSON
3. all related local archives
4. locally extracted files

A transcript URL is provenance, not local transcript evidence. Also check for audio/recording members and an actual Transcript section before claiming conversational completeness.

## Scope comparison

A receipt archive may cover one channel while another local export covers the workspace, DMs, or additional channels. Compare channel lists, day-file counts, huddle ID sets, and common-member hashes. State one of these conclusions precisely:

- complete for normalized objects in the receipt scope
- complete for exported note bodies but not transcripts/audio
- incomplete for the workspace because channels or DMs are absent
- incomplete because normalized excerpts truncate source text

## Reporting contract

Return:

- a direct yes/no verdict for normalized semantic completeness
- exact normalized, receipt, state, and raw archive paths
- counts by artifact kind and unique ID
- raw archive inventory and attachment MIME counts
- bidirectional coverage results
- the strongest completeness limitation
- a clear distinction between note-level comparison and original-conversation comparison
- whether any files were modified

Avoid presenting arbitrary word counts as absolute truth. If visible-text counts are useful, name the extraction method or round the word count while keeping byte and object counts exact.
