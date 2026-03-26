# Atomic JSONL Writes

## Goal
Never leave a partial or truncated JSONL file on disk.

## Steps
1. Write to a temp file in the same directory.
2. Flush and fsync the temp file.
3. Atomically replace the target file.
4. Optionally fsync the directory (Unix).

## Rust (tempfile)
```rust
let tmp = tempfile::NamedTempFile::new_in(dir)?;
{
    let mut w = std::io::BufWriter::new(tmp.as_file());
    for line in lines { writeln!(w, "{}", line)?; }
    w.flush()?;
    tmp.as_file().sync_all()?;
}
let tmp_path = tmp.into_temp_path();
tmp_path.persist(&jsonl_path)?;
```

## Notes
- On Unix, rename is atomic.
- On Windows, persist() handles safe replacement semantics.
- For maximum durability on Unix, fsync the directory after rename.
- Keep the old JSONL if the replace fails; never leave partial files.
- Prefer `tempfile::persist()` over manual rename on Windows.
- For append-only JSONL, lock + append + flush may be sufficient; for full export use temp+rename.
- Use `BufWriter` to reduce syscalls on large writes.
