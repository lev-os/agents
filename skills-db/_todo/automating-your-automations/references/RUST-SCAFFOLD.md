# Rust CLI Scaffold for Automation Tools

## Cargo.toml

```toml
[package]
name = "<tool-name>"
version = "0.1.0"
edition = "2024"

[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", features = ["serde"] }
rusqlite = { version = "0.32", features = ["bundled"] }
dirs = "6"

[profile.release]
opt-level = 3
lto = "thin"
strip = true
```

## Atuin-Specific Integration Pattern

The key non-obvious code: opening atuin's DB read-only and handling nanosecond timestamps.

```rust
use rusqlite::OpenFlags;

fn open_atuin_readonly() -> anyhow::Result<rusqlite::Connection> {
    let db_path = dirs::home_dir()
        .context("No home directory")?
        .join(".atuin/history.db");
    rusqlite::Connection::open_with_flags(&db_path, OpenFlags::SQLITE_OPEN_READ_ONLY)
        .context("Failed to open atuin database (is atuin installed?)")
}

// Atuin stores duration/timestamp in nanoseconds
fn ns_to_sec(ns: i64) -> f64 { ns as f64 / 1e9 }
```

## CLI Structure

```rust
#[derive(clap::Parser)]
#[command(name = "<tool-name>")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
    /// JSON output for machine consumption
    #[arg(long, global = true)]
    robot: bool,
    /// Preview without executing
    #[arg(long, global = true)]
    dry_run: bool,
}

#[derive(clap::Subcommand)]
enum Commands {
    /// Analyze patterns and suggest automations
    Analyze {
        #[arg(long, default_value = "5")]
        min_count: u32,
        #[arg(long, default_value = "20")]
        limit: u32,
    },
    /// Show database statistics
    Stats,
}
```

## Scoring Function

```rust
#[derive(serde::Serialize)]
struct AnalysisResult {
    pattern: String,
    frequency: u32,
    avg_duration_sec: f64,
    fail_rate: f64,
    score: f64,
    recommendation: String,
}

fn score_and_recommend(command: &str, frequency: u32, avg_sec: f64, fail_rate: f64) -> (f64, &'static str) {
    let freq_norm = (frequency as f64).ln() / 10.0;
    let time_norm = (avg_sec * frequency as f64).min(3600.0) / 3600.0;
    let score = (freq_norm * 0.4 + time_norm * 0.3 + fail_rate * 0.2 + 0.1).min(1.0);

    let rec = if avg_sec > 10.0 && frequency > 20 {
        "Rust CLI: long-running + frequent"
    } else if fail_rate > 0.3 {
        "Bash wrapper: retry logic + error handling"
    } else if frequency > 50 {
        "Shell alias: high frequency, quick command"
    } else {
        "Bash script: moderate complexity"
    };
    (score, rec)
}
```

## Build & Install

```bash
cargo build --release
ln -sf "$(pwd)/target/release/<tool-name>" ~/.local/bin/
```

## Checklist

- [ ] `--robot` on every subcommand
- [ ] `--dry-run` on any subcommand with side effects
- [ ] Open atuin DB as **read-only** (never write)
- [ ] Non-zero exit on failure
- [ ] Use `/rust-cli-with-sqlite` for persistent state beyond atuin reads
