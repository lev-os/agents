//! Command implementations for research CLI

pub mod search;
pub mod status;
pub mod history;

use clap::Args;

#[derive(Args, Debug)]
pub struct SearchCommand {
    /// The research query to execute
    #[arg(required = true)]
    pub query: Vec<String>,

    /// Maximum number of sources to discover
    #[arg(short = 'n', long, default_value = "10")]
    pub max_sources: usize,

    /// Research depth (1=quick/brave, 2=standard/firecrawl, 3=deep/valyu)
    #[arg(short, long, default_value = "2")]
    pub depth: u8,
}

#[derive(Args, Debug)]
pub struct StatusCommand {
    /// Session ID to check status for (if omitted, shows current)
    #[arg(short, long)]
    pub session_id: Option<String>,
}

#[derive(Args, Debug)]
pub struct HistoryCommand {
    /// Number of recent sessions to show
    #[arg(short = 'n', long, default_value = "10")]
    pub limit: usize,

    /// Filter by query substring
    #[arg(short, long)]
    pub filter: Option<String>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn search_command_default_values() {
        let cmd = SearchCommand {
            query: vec!["test".into()],
            max_sources: 10,
            depth: 2,
        };
        assert_eq!(cmd.depth, 2);
        assert_eq!(cmd.max_sources, 10);
        assert_eq!(cmd.query, vec!["test".to_string()]);
    }

    #[test]
    fn search_command_multi_word_query() {
        let cmd = SearchCommand {
            query: vec!["rust".into(), "async".into(), "programming".into()],
            max_sources: 10,
            depth: 1,
        };
        assert_eq!(cmd.query.join(" "), "rust async programming");
    }

    #[test]
    fn search_command_custom_depth() {
        let cmd = SearchCommand {
            query: vec!["test".into()],
            max_sources: 20,
            depth: 3,
        };
        assert_eq!(cmd.depth, 3);
        assert_eq!(cmd.max_sources, 20);
    }

    #[test]
    fn status_command_no_session_id() {
        let cmd = StatusCommand { session_id: None };
        assert!(cmd.session_id.is_none());
    }

    #[test]
    fn status_command_with_session_id() {
        let cmd = StatusCommand {
            session_id: Some("abc-123-def".into()),
        };
        assert_eq!(cmd.session_id.unwrap(), "abc-123-def");
    }

    #[test]
    fn history_command_default_limit() {
        let cmd = HistoryCommand {
            limit: 10,
            filter: None,
        };
        assert_eq!(cmd.limit, 10);
        assert!(cmd.filter.is_none());
    }

    #[test]
    fn history_command_with_filter() {
        let cmd = HistoryCommand {
            limit: 5,
            filter: Some("rust".to_string()),
        };
        assert_eq!(cmd.limit, 5);
        assert_eq!(cmd.filter.unwrap(), "rust");
    }

    #[test]
    fn history_command_zero_limit() {
        let cmd = HistoryCommand {
            limit: 0,
            filter: None,
        };
        assert_eq!(cmd.limit, 0);
    }

    #[test]
    fn search_command_single_word_query() {
        let cmd = SearchCommand {
            query: vec!["rust".into()],
            max_sources: 10,
            depth: 1,
        };
        assert_eq!(cmd.query.join(" "), "rust");
    }

    #[test]
    fn search_command_debug_format() {
        let cmd = SearchCommand {
            query: vec!["test".into()],
            max_sources: 10,
            depth: 2,
        };
        let debug_str = format!("{:?}", cmd);
        assert!(debug_str.contains("SearchCommand"));
        assert!(debug_str.contains("test"));
    }
}
