# Scrubber Patterns Catalog

> Standard scrubbers for neutralizing non-deterministic output before golden comparison.

## Universal Scrubber Registry (Rust)

```rust
use regex::Regex;

pub struct Scrubber {
    rules: Vec<(Regex, &'static str)>,
}

impl Scrubber {
    /// Standard scrubbers for common dynamic values
    pub fn standard() -> Self {
        Self { rules: vec![
            // UUIDs (v4)
            (Regex::new(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}").unwrap(), "[UUID]"),
            // Any UUID-shaped string
            (Regex::new(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}").unwrap(), "[UUID]"),
            // ISO 8601 timestamps
            (Regex::new(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?").unwrap(), "[TIMESTAMP]"),
            // Unix timestamps (seconds)
            (Regex::new(r"\b1[6-9]\d{8}\b").unwrap(), "[UNIX_TS]"),
            // Durations
            (Regex::new(r"\d+(\.\d+)?\s*(ms|us|µs|ns|s|sec|min|h)").unwrap(), "[DURATION]"),
            // Memory addresses
            (Regex::new(r"0x[0-9a-f]{6,16}").unwrap(), "[ADDR]"),
            // Absolute paths (Unix)
            (Regex::new(r"/home/[a-z0-9_]+/").unwrap(), "/HOME/"),
            (Regex::new(r"/tmp/[a-zA-Z0-9._-]+").unwrap(), "/TMP/"),
            // Port numbers in URLs
            (Regex::new(r"localhost:\d{4,5}").unwrap(), "localhost:[PORT]"),
            // Process IDs
            (Regex::new(r"\bpid[=: ]\d+").unwrap(), "pid=[PID]"),
        ]}
    }

    pub fn with_custom(mut self, pattern: &str, replacement: &'static str) -> Self {
        self.rules.push((Regex::new(pattern).unwrap(), replacement));
        self
    }

    pub fn scrub(&self, input: &str) -> String {
        let mut result = input.to_string();
        for (regex, replacement) in &self.rules {
            result = regex.replace_all(&result, *replacement).to_string();
        }
        result
    }
}
```

## TypeScript Scrubber

```typescript
function scrub(input: string, extraPatterns?: Array<[RegExp, string]>): string {
  const patterns: Array<[RegExp, string]> = [
    // UUIDs
    [/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, "[UUID]"],
    // ISO timestamps
    [/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?/g, "[TIMESTAMP]"],
    // Durations
    [/\d+(\.\d+)?\s*(ms|us|ns|s|sec|min)/g, "[DURATION]"],
    // Memory addresses
    [/0x[0-9a-f]{6,16}/gi, "[ADDR]"],
    // Absolute paths
    [/\/home\/[^/]+\//g, "/HOME/"],
    [/\/tmp\/[a-zA-Z0-9._-]+/g, "/TMP/"],
    // Ports
    [/localhost:\d{4,5}/g, "localhost:[PORT]"],
    ...(extraPatterns ?? []),
  ];

  let result = input;
  for (const [regex, replacement] of patterns) {
    result = result.replace(regex, replacement);
  }
  return result;
}

// For structured data (JSON objects)
function scrubObject(obj: unknown): unknown {
  if (obj === null || obj === undefined) return obj;
  if (typeof obj === "string") return scrub(obj);
  if (Array.isArray(obj)) return obj.map(scrubObject);
  if (typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([k, v]) => [k, scrubObject(v)])
    );
  }
  return obj;
}
```

## Platform Canonicalizer

```rust
fn canonicalize(output: &str) -> String {
    output
        .replace("\r\n", "\n")              // Windows line endings
        .replace('\\', "/")                 // Windows path separators
        .replace("/home/runner/", "/HOME/") // CI home directories
        .replace("/Users/", "/HOME/")       // macOS
        .replace("/home/ubuntu/", "/HOME/") // Linux
        .lines()
        .map(|l| l.trim_end())              // Trailing whitespace
        .collect::<Vec<_>>()
        .join("\n")
}
```

## Floating-Point Rounder

```rust
fn round_floats(s: &str, decimals: usize) -> String {
    let re = Regex::new(r"\d+\.\d+").unwrap();
    re.replace_all(s, |caps: &regex::Captures| {
        let f: f64 = caps[0].parse().unwrap();
        format!("{:.prec$}", f, prec = decimals)
    }).to_string()
}
```

## Map Key Sorter

```rust
fn sort_json_keys(json: &str) -> String {
    let value: serde_json::Value = serde_json::from_str(json).unwrap();
    // serde_json with preserve_order=false sorts keys
    serde_json::to_string_pretty(&value).unwrap()
}
```
