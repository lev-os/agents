//! History command - show research history

use anyhow::Result;

pub async fn execute(cmd: super::HistoryCommand, _fullscreen: bool) -> Result<()> {
    println!("History command not yet implemented");
    println!("Limit: {}, Filter: {:?}", cmd.limit, cmd.filter);
    Ok(())
}
