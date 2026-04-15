# Language-Specific Fuzzing Guide

> Quick-start commands and patterns for each language ecosystem.

## Rust

### Setup

```bash
rustup default nightly  # Required for sanitizers
cargo install cargo-fuzz
cargo fuzz init
cargo fuzz add my_target
```

### Run

```bash
cargo fuzz run my_target                           # Basic (ASan default)
cargo fuzz run my_target -- -max_len=65536         # Bound input size
cargo fuzz run my_target -- -timeout=10            # 10s timeout per input
cargo fuzz run my_target -- -dict=dict.txt         # With dictionary
cargo fuzz run my_target -- -jobs=4 -workers=4     # Parallel
```

### Tooling

| Tool | Purpose | Install |
|------|---------|---------|
| cargo-fuzz | libFuzzer wrapper | `cargo install cargo-fuzz` |
| afl.rs | AFL++ wrapper | `cargo install afl` |
| honggfuzz-rs | honggfuzz wrapper | `cargo install honggfuzz` |
| bolero | Unified interface | Add `bolero` to dev-deps |
| cargo-nextest | Better test runner | `cargo install cargo-nextest` |

### Bolero (Write Once, Fuzz Everywhere)

```rust
use bolero::check;

#[test]
fn fuzz_with_bolero() {
    check!()
        .with_type::<Vec<u8>>()
        .cloned()
        .for_each(|data| {
            let _ = parse(&data);
        });
}
```

```bash
cargo bolero test fuzz_with_bolero --engine libfuzzer
cargo bolero test fuzz_with_bolero --engine afl
cargo bolero test fuzz_with_bolero --engine honggfuzz
cargo test fuzz_with_bolero  # Property-based mode in CI
```

---

## Go

### Native Fuzzing (Go 1.18+)

```go
func FuzzMyParser(f *testing.F) {
    // Seed corpus
    f.Add([]byte(`{"valid": true}`))
    f.Add([]byte(``))
    f.Add([]byte{0xFF})

    f.Fuzz(func(t *testing.T, data []byte) {
        result, err := MyParser(data)
        if err != nil {
            return // Graceful rejection
        }
        // Round-trip check
        encoded, err := json.Marshal(result)
        if err != nil {
            t.Fatalf("Marshal failed: %v", err)
        }
        var reparsed MyType
        if err := json.Unmarshal(encoded, &reparsed); err != nil {
            t.Fatalf("Round-trip failed: %v", err)
        }
    })
}
```

```bash
go test -fuzz=FuzzMyParser -fuzztime=60s
go test -fuzz=FuzzMyParser -fuzztime=10000x  # 10K iterations
```

Corpus location: `testdata/fuzz/FuzzMyParser/`

---

## Python

### Atheris (Coverage-Guided)

```python
import atheris
import sys

with atheris.instrument_imports():
    import target_library

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    s = fdp.ConsumeUnicode(fdp.ConsumeIntInRange(0, 1024))
    i = fdp.ConsumeInt(4)
    f = fdp.ConsumeFloat()
    b = fdp.ConsumeBool()
    target_library.process(s, i, f, b)

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

### FuzzedDataProvider Methods

| Method | Returns | Use For |
|--------|---------|---------|
| `ConsumeBytes(n)` | bytes | Raw byte buffers |
| `ConsumeUnicode(n)` | str | Text input |
| `ConsumeInt(n)` | int | n-byte integer |
| `ConsumeIntInRange(min, max)` | int | Bounded integer |
| `ConsumeFloat()` | float | IEEE 754 float |
| `ConsumeBool()` | bool | Boolean flags |
| `PickValueInList(lst)` | any | Choose from options |

---

## TypeScript / JavaScript

### fast-check (Property-Based)

```typescript
import * as fc from "fast-check";

test("parser handles arbitrary input", () => {
  fc.assert(
    fc.property(fc.string(), (input) => {
      // Must not throw
      try { parse(input); } catch (e) {
        if (e instanceof SyntaxError) return; // Expected
        throw e; // Unexpected = bug
      }
    }),
    { numRuns: 100_000 }
  );
});
```

### Jazzer.js (Coverage-Guided)

```bash
npm install @jazzer.js/core
```

```javascript
// fuzz_target.js
const { FuzzedDataProvider } = require("@jazzer.js/core");

module.exports.fuzz = function(fuzzerInputData) {
    const data = new FuzzedDataProvider(fuzzerInputData);
    const n = data.consumeIntegral(4);
    const s = data.consumeString(100, "utf-8");
    myLibrary.process(n, s);
};
```

```bash
JAZZER_FUZZ=1 npx jest  # Fuzzing mode
npx jest                # Regression mode (replays corpus)
```

---

## C/C++

### libFuzzer

```c
#include <stdint.h>
#include <stddef.h>

extern int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size > 1000000) return 0;
    parse_message(data, size);
    return 0;
}
```

```bash
clang -g -O1 -fsanitize=fuzzer,address,undefined target.c -o target
./target -max_len=65536 -timeout=10 corpus/
```

### AFL++

```bash
afl-cc -o target target.c
afl-fuzz -i corpus/ -o findings/ -- ./target @@
```
