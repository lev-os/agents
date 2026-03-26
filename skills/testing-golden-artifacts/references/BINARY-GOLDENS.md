# Binary Golden File Patterns

> When golden output is binary (images, protobuf, compiled artifacts, database pages), byte-for-byte comparison is usually too strict. Use semantic comparison instead.

## Decision: Byte-Exact vs Semantic

| Output Type | Comparison Method | Why |
|-------------|------------------|-----|
| Text/JSON/YAML | Byte-exact (after canonicalization) | Deterministic text output |
| Protocol Buffers | Decode → compare structure | Field ordering may vary |
| Images (PNG/JPG) | Perceptual hash or pixel RMSE | Rendering differences across platforms |
| SQLite DB files | Query results, not raw bytes | WAL state, page layout vary |
| Compiled binaries | Skip (test behavior instead) | Never golden a binary |
| ZIP/tar archives | Extract → compare contents | Timestamps, ordering differ |
| PDF documents | Extract text → compare | Metadata, font embedding differ |

## Pattern 1: Protobuf/MessagePack Semantic Comparison

```rust
/// Compare binary formats by decoding to a common structure
fn assert_binary_golden_semantic<T: Deserialize + PartialEq + Debug>(
    test_name: &str,
    actual_bytes: &[u8],
    decode: fn(&[u8]) -> Result<T, Error>,
) {
    let golden_path = golden_path_bin(test_name);

    if updating_goldens() {
        fs::write(&golden_path, actual_bytes).unwrap();
        return;
    }

    let expected_bytes = fs::read(&golden_path).unwrap();

    // Decode both to structured representation
    let actual = decode(actual_bytes)
        .expect("Failed to decode actual output");
    let expected = decode(&expected_bytes)
        .expect("Failed to decode golden file");

    // Compare structure, not bytes
    assert_eq!(actual, expected,
        "Semantic golden mismatch for {test_name}");
}
```

## Pattern 2: Image Comparison with Tolerance

```rust
/// Compare images allowing small pixel differences
fn assert_image_golden(
    test_name: &str,
    actual: &image::DynamicImage,
    max_pixel_diff: u8,    // Per-channel tolerance (0-255)
    max_diff_percent: f64, // Max % of pixels that can differ
) {
    let golden_path = golden_path_with_ext(test_name, "png");

    if updating_goldens() {
        actual.save(&golden_path).unwrap();
        return;
    }

    let expected = image::open(&golden_path)
        .unwrap_or_else(|_| panic!("Golden image not found: {}", golden_path.display()));

    assert_eq!(actual.dimensions(), expected.dimensions(),
        "Image dimensions differ");

    let total_pixels = (actual.width() * actual.height()) as f64;
    let mut diff_pixels = 0u64;

    for (x, y, actual_px) in actual.pixels() {
        let expected_px = expected.get_pixel(x, y);
        let channel_diff = actual_px.0.iter().zip(expected_px.0.iter())
            .any(|(a, e)| a.abs_diff(*e) > max_pixel_diff);
        if channel_diff { diff_pixels += 1; }
    }

    let diff_percent = (diff_pixels as f64 / total_pixels) * 100.0;
    assert!(diff_percent <= max_diff_percent,
        "Image diff: {diff_percent:.2}% pixels differ (max: {max_diff_percent}%)");
}
```

## Pattern 3: Archive Content Comparison

```rust
/// Compare archives by extracting and comparing file-by-file
fn assert_archive_golden(test_name: &str, actual_zip_bytes: &[u8]) {
    let golden_path = golden_path_with_ext(test_name, "zip");

    if updating_goldens() {
        fs::write(&golden_path, actual_zip_bytes).unwrap();
        return;
    }

    let expected_bytes = fs::read(&golden_path).unwrap();

    let actual_files = extract_zip_to_map(actual_zip_bytes);
    let expected_files = extract_zip_to_map(&expected_bytes);

    // Compare file lists
    let actual_names: BTreeSet<_> = actual_files.keys().collect();
    let expected_names: BTreeSet<_> = expected_files.keys().collect();
    assert_eq!(actual_names, expected_names,
        "Archive file lists differ");

    // Compare each file's content
    for (name, actual_content) in &actual_files {
        let expected_content = expected_files.get(name).unwrap();
        assert_eq!(actual_content, expected_content,
            "Archive file {name} differs");
    }
}

fn extract_zip_to_map(bytes: &[u8]) -> BTreeMap<String, Vec<u8>> {
    let cursor = std::io::Cursor::new(bytes);
    let mut archive = zip::ZipArchive::new(cursor).unwrap();
    let mut files = BTreeMap::new();
    for i in 0..archive.len() {
        let mut entry = archive.by_index(i).unwrap();
        if entry.is_file() {
            let mut content = Vec::new();
            std::io::Read::read_to_end(&mut entry, &mut content).unwrap();
            files.insert(entry.name().to_string(), content);
        }
    }
    files
}
```

## Pattern 4: Database State Comparison

```rust
/// Compare database state via queries, not raw file bytes
fn assert_db_golden(test_name: &str, db: &Database) {
    let golden_path = golden_path_with_ext(test_name, "json");

    // Extract queryable state
    let state = json!({
        "tables": db.list_tables(),
        "row_counts": db.list_tables().iter()
            .map(|t| (t.clone(), db.count_rows(t)))
            .collect::<HashMap<_, _>>(),
        "schema_version": db.schema_version(),
    });

    let actual = serde_json::to_string_pretty(&state).unwrap();

    if updating_goldens() {
        fs::write(&golden_path, &actual).unwrap();
        return;
    }

    let expected = fs::read_to_string(&golden_path).unwrap();
    assert_eq!(actual, expected,
        "Database state golden mismatch for {test_name}");
}
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Golden a SQLite .db file | WAL state, page layout are non-deterministic | Query the data, golden the results |
| Golden a compiled binary | Platform-dependent, non-reproducible | Golden the behavior (test outputs) |
| Byte-compare compressed data | Compression is non-deterministic | Decompress, then compare |
| Byte-compare floating-point binary | Bit-level representation varies | Decode to f64, use epsilon |
| Golden files >10MB | Slow CI, hard to review | Subset or summarize |
