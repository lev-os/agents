# Golden Artifact Troubleshooting

## "Snapshots change on every run"

| Cause | Fix |
|-------|-----|
| Timestamps in output | Scrub with `[TIMESTAMP]` or inject fake clock |
| UUIDs/random IDs | Scrub with `[UUID]` or use sequential IDs |
| HashMap iteration order | Sort keys before snapshot (insta: `set_sort_maps(true)`) |
| Floating-point instability | Round to fixed decimal places before snapshot |
| Platform differences (line endings) | Canonicalize: `\r\n` → `\n`, `\\` → `/` |
| Memory addresses in output | Scrub with `[ADDR]` pattern |

## "Snapshot review is overwhelming"

| Symptom | Fix |
|---------|-----|
| 100+ snapshots changed at once | Use `cargo insta review` TUI (interactive accept/reject) |
| Snapshots too large to read | Split into smaller focused snapshots |
| Can't tell if change is intentional | Always commit snapshot updates in separate commits |
| Nobody reviews the diffs | Enforce review policy: snapshot changes require 2nd reviewer |

## "CI fails but local passes"

| Cause | Fix |
|-------|-----|
| Different OS (line endings) | Add canonicalization |
| Different locale | Set `LC_ALL=C` in CI |
| Different timezone | Use UTC everywhere or scrub timestamps |
| Different Rust/Node version | Pin versions in CI |
| Stale snapshot files | Run `INSTA_UPDATE=unseen cargo test` to detect orphans |

## "insta specific issues"

```bash
# Snapshots marked as new but shouldn't be
# Likely: test was renamed → old snapshot orphaned, new one created
INSTA_UPDATE=unseen cargo test  # Flags unreferenced snapshots

# .snap.new files accumulating
# Run review to clean up
cargo insta review

# Inline snapshot won't update
# Make sure the @"" placeholder exists
assert_snapshot!(value, @"");  # insta will fill this in

# Snapshot path mismatch
# Check: set_snapshot_path() or set_prepend_module_to_snapshot()
```

## "Vitest/Jest specific issues"

```typescript
// toMatchSnapshot() creates huge unreadable files
// Fix: use toMatchInlineSnapshot() for small values
expect(value).toMatchInlineSnapshot(`"expected"`);

// toMatchFileSnapshot() fails with "file not found"
// First run: vitest -u creates the file
// CI: files must be committed first

// Property matchers not working
expect(obj).toMatchSnapshot({
  id: expect.any(String),       // ✓ matches any string
  id: expect.anything(),        // ✓ matches anything non-null
  id: expect.stringMatching(/^user-/), // ✓ regex match
});
```
