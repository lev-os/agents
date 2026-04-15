# Fuzz Harness Catalog

> Complete code templates for every fuzzing pattern. Copy, adapt, run.

## Contents

1. [Crash Detector (Raw Bytes)](#crash-detector)
2. [Round-Trip (Serialize/Deserialize)](#round-trip)
3. [Differential (Two Implementations)](#differential)
4. [Stateful (Operation Sequences)](#stateful)
5. [Grammar-Based (Syntax-Aware)](#grammar-based)
6. [Custom Mutator (Domain-Specific)](#custom-mutator)
7. [Concurrency (Race Conditions)](#concurrency)

---

## Crash Detector

### Rust (cargo-fuzz)

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if data.len() > 1_000_000 { return; }
    let _ = my_crate::parse(data);
});
```

### Go (native)

```go
func FuzzParse(f *testing.F) {
    f.Add([]byte("valid input"))
    f.Add([]byte{})
    f.Add([]byte{0xFF, 0xFE})

    f.Fuzz(func(t *testing.T, data []byte) {
        _ = Parse(data)
    })
}
```

### Python (Atheris)

```python
import atheris
import sys

with atheris.instrument_imports():
    import my_library

def TestOneInput(data):
    if len(data) > 1_000_000:
        return
    try:
        my_library.parse(data)
    except (ValueError, TypeError):
        pass  # Expected error types

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

### TypeScript (Jazzer.js)

```javascript
module.exports.fuzz = function(data) {
    if (data.length > 1_000_000) return;
    try {
        myLibrary.parse(data.toString("utf-8"));
    } catch (e) {
        if (e instanceof SyntaxError) return; // Expected
        throw e; // Unexpected = bug
    }
};
```

---

## Round-Trip

### Rust (Structured + Raw)

```rust
#![no_main]
use arbitrary::Arbitrary;
use libfuzzer_sys::fuzz_target;

#[derive(Debug, Arbitrary)]
enum FuzzValue {
    Null,
    Bool(bool),
    Int(i64),
    Float(f64),
    Text(String),
    Blob(Vec<u8>),
}

#[derive(Debug, Arbitrary)]
struct FuzzInput {
    raw: Vec<u8>,
    values: Vec<FuzzValue>,
}

fuzz_target!(|input: FuzzInput| {
    // Strategy 1: Raw bytes must not panic
    if input.raw.len() <= 65536 {
        let _ = parse(&input.raw);
    }

    // Strategy 2: Structured values must round-trip
    if !input.values.is_empty() && input.values.len() <= 1000 {
        let native: Vec<Value> = input.values.iter()
            .map(|v| v.into())
            .collect();
        let bytes = serialize(&native);
        let recovered = parse(&bytes)
            .expect("Cannot parse our own output");
        assert_eq!(native, recovered, "Round-trip corruption");
    }
});
```

### Go

```go
func FuzzRoundTrip(f *testing.F) {
    f.Add([]byte(`{"key":"value"}`))

    f.Fuzz(func(t *testing.T, data []byte) {
        var parsed interface{}
        if err := json.Unmarshal(data, &parsed); err != nil {
            return
        }
        reencoded, err := json.Marshal(parsed)
        if err != nil {
            t.Fatalf("Marshal failed: %v", err)
        }
        var reparsed interface{}
        if err := json.Unmarshal(reencoded, &reparsed); err != nil {
            t.Fatalf("Round-trip parse failed: %v", err)
        }
        if !reflect.DeepEqual(parsed, reparsed) {
            t.Fatal("Round-trip changed value")
        }
    })
}
```

---

## Differential

### Rust (Full Pattern)

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;
use arbitrary::Arbitrary;
use std::collections::BTreeMap;

#[derive(Arbitrary, Debug)]
enum Op<K: Ord, V> {
    Insert { key: K, val: V },
    Get { key: K },
    Remove { key: K },
    Len,
}

fuzz_target!(|ops: Vec<Op<u8, u16>>| {
    let mut ours = MyMap::new();
    let mut reference = BTreeMap::new();

    for op in &ops {
        match op {
            Op::Insert { key, val } => {
                assert_eq!(ours.insert(*key, *val), reference.insert(*key, *val));
            }
            Op::Get { key } => {
                assert_eq!(ours.get(key), reference.get(key));
            }
            Op::Remove { key } => {
                assert_eq!(ours.remove(key), reference.remove(key));
            }
            Op::Len => {
                assert_eq!(ours.len(), reference.len());
            }
        }
    }
    // Final state must match
    assert!(ours.iter().eq(reference.iter()));
});
```

### Python (Differential JSON)

```python
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    json_str = fdp.ConsumeUnicode(sys.maxsize)
    try:
        ours = ujson.loads(json_str)
        ref = json.loads(json_str)
    except Exception:
        return
    if json.dumps(ref) != json.dumps(ours):
        raise RuntimeError(f"Disagreement: {json_str!r}")
```

---

## Stateful

### Rust (Database/Filesystem)

```rust
#![no_main]
use arbitrary::Arbitrary;
use libfuzzer_sys::fuzz_target;

#[derive(Debug, Arbitrary)]
enum FileOp {
    Create { name: u8, content: Vec<u8> },
    Read { name: u8 },
    Delete { name: u8 },
    Rename { from: u8, to: u8 },
    List,
    Sync,
}

fuzz_target!(|ops: Vec<FileOp>| {
    if ops.len() > 200 { return; }
    if ops.iter().any(|op| matches!(op,
        FileOp::Create { content, .. } if content.len() > 10_000
    )) { return; }

    let fs = TestFs::new_in_memory();
    let mut model = HashMap::new();

    for op in &ops {
        match op {
            FileOp::Create { name, content } => {
                let key = format!("f{name}");
                let _ = fs.write(&key, content);
                model.insert(key, content.clone());
            }
            FileOp::Read { name } => {
                let key = format!("f{name}");
                let fs_result = fs.read(&key).ok();
                let model_result = model.get(&key);
                assert_eq!(fs_result.as_deref(), model_result.map(|v| v.as_slice()));
            }
            FileOp::Delete { name } => {
                let key = format!("f{name}");
                let _ = fs.delete(&key);
                model.remove(&key);
            }
            FileOp::Rename { from, to } => {
                let from_key = format!("f{from}");
                let to_key = format!("f{to}");
                if let Some(data) = model.remove(&from_key) {
                    let _ = fs.rename(&from_key, &to_key);
                    model.insert(to_key, data);
                }
            }
            FileOp::List => {
                let fs_list: BTreeSet<_> = fs.list().into_iter().collect();
                let model_list: BTreeSet<_> = model.keys().cloned().collect();
                assert_eq!(fs_list, model_list);
            }
            FileOp::Sync => { let _ = fs.sync(); }
        }
    }

    fs.check_invariants().expect("Invariant violation");
});
```

---

## Custom Mutator

### Rust (Compressed Data)

```rust
#![no_main]
use libfuzzer_sys::{fuzz_target, fuzz_mutator};

fuzz_target!(|data: &[u8]| {
    if let Ok(decompressed) = decompress(data) {
        let _ = parse_message(&decompressed);
    }
});

fuzz_mutator!(|data: &mut [u8], size: usize, max_size: usize, seed: u32| {
    // Decompress → mutate → recompress
    if let Ok(decompressed) = decompress(&data[..size]) {
        let mut mutated = decompressed;
        // Apply standard mutations to decompressed data
        libfuzzer_sys::fuzzer_mutate(&mut mutated, mutated.len(), mutated.len() * 2);
        if let Ok(recompressed) = compress(&mutated) {
            let new_size = recompressed.len().min(max_size);
            data[..new_size].copy_from_slice(&recompressed[..new_size]);
            return new_size;
        }
    }
    // Fallback: standard mutation on raw bytes
    libfuzzer_sys::fuzzer_mutate(data, size, max_size)
});
```

### Python (Custom Mutator for Compressed Formats)

```python
def CustomMutator(data, max_size, seed):
    try:
        decompressed = zlib.decompress(data)
    except zlib.error:
        decompressed = b"Hello"
    decompressed = atheris.Mutate(decompressed, len(decompressed))
    return zlib.compress(decompressed)

atheris.Setup(sys.argv, TestOneInput, custom_mutator=CustomMutator)
```

---

## Concurrency

### Rust (Thread Safety)

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;
use arbitrary::Arbitrary;
use std::sync::Arc;
use std::thread;

#[derive(Debug, Arbitrary)]
struct ConcurrentOps {
    thread1_ops: Vec<Op>,
    thread2_ops: Vec<Op>,
}

fuzz_target!(|input: ConcurrentOps| {
    if input.thread1_ops.len() > 50 || input.thread2_ops.len() > 50 { return; }

    let shared = Arc::new(MyConcurrentMap::new());
    let s1 = shared.clone();
    let s2 = shared.clone();

    let t1 = thread::spawn(move || {
        for op in &input.thread1_ops { execute(&s1, op); }
    });
    let t2 = thread::spawn(move || {
        for op in &input.thread2_ops { execute(&s2, op); }
    });

    t1.join().unwrap();
    t2.join().unwrap();

    // Invariant: must be in consistent state after concurrent access
    shared.check_invariants().expect("Concurrent invariant violation");
});
```

**Note:** Run with ThreadSanitizer:
```bash
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly fuzz run concurrent_target
```
