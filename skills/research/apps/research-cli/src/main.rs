//! Research Hub CLI - FrankenTUI-based research interface
//!
//! Provides inline and fullscreen modes for research tasks.
//!
//! Run: `cargo run --bin research -- search "rust async programming"`

use anyhow::Result;
use clap::{Parser, Subcommand};

mod app;
mod backends;
mod commands;
mod widgets;

use app::ResearchApp;
use commands::{HistoryCommand, SearchCommand, StatusCommand};

#[derive(Parser)]
#[command(name = "research")]
#[command(about = "OCLaw Research Hub CLI", long_about = None)]
#[command(version)]
struct Cli {
    #[command(subcommand)]
    command: Commands,

    /// Enable fullscreen mode instead of inline
    #[arg(short, long, global = true)]
    fullscreen: bool,

    /// Enable debug logging
    #[arg(short = 'D', long, global = true)]
    debug: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Execute a research search
    Search(SearchCommand),

    /// Show current research status
    Status(StatusCommand),

    /// Show research history
    History(HistoryCommand),
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    // Setup logging
    let log_level = if cli.debug { "debug" } else { "info" };
    tracing_subscriber::fmt()
        .with_env_filter(log_level)
        .with_target(false)
        .init();

    match cli.command {
        Commands::Search(cmd) => {
            commands::search::execute(cmd, cli.fullscreen).await?;
        }
        Commands::Status(cmd) => {
            commands::status::execute(cmd, cli.fullscreen).await?;
        }
        Commands::History(cmd) => {
            commands::history::execute(cmd, cli.fullscreen).await?;
        }
    }

    Ok(())
}
