//! Search command implementation

use anyhow::Result;
use tokio::sync::mpsc;
use std::thread;

use crate::app;
use crate::backends::{BackendConfig, ResearchBackend};
use crate::backends::valyu::ValyuBackend;
use crate::backends::firecrawl::FirecrawlBackend;
use crate::backends::brave::BraveBackend;
use crate::backends::perplexity::PerplexityBackend;
use crate::backends::arxiv::ArxivBackend;
use crate::backends::hackernews::HackerNewsBackend;
use crate::backends::github::GitHubBackend;
use crate::backends::mock::MockBackend;

/// Check if an API key environment variable is set and non-empty
fn get_api_key(env_var: &str) -> Option<String> {
    std::env::var(env_var).ok().filter(|k| !k.is_empty())
}

fn config_with_key(key: String) -> BackendConfig {
    BackendConfig {
        api_key: Some(key),
        timeout_secs: 300,
    }
}

pub async fn execute(cmd: super::SearchCommand, fullscreen: bool) -> Result<()> {
    let query = cmd.query.join(" ");
    tracing::info!("Starting search: query={}", query);

    let (tx, rx) = mpsc::unbounded_channel();

    let backend: Box<dyn ResearchBackend + Send> = match cmd.depth {
        1 => {
            if let Some(key) = get_api_key("BRAVE_API_KEY") {
                tracing::info!("Using Brave Search API");
                Box::new(BraveBackend::new(config_with_key(key)))
            } else {
                tracing::warn!("BRAVE_API_KEY not set, falling back to mock");
                Box::new(MockBackend::new(BackendConfig::default()))
            }
        }
        2 => {
            if let Some(key) = get_api_key("FIRECRAWL_API_KEY") {
                tracing::info!("Using Firecrawl API");
                Box::new(FirecrawlBackend::new(config_with_key(key)))
            } else {
                tracing::warn!("FIRECRAWL_API_KEY not set, falling back to mock");
                Box::new(MockBackend::new(BackendConfig::default()))
            }
        }
        3 => {
            if let Some(key) = get_api_key("VALYU_API_KEY") {
                tracing::info!("Using Valyu API");
                Box::new(ValyuBackend::new(config_with_key(key)))
            } else {
                tracing::warn!("VALYU_API_KEY not set, falling back to mock");
                Box::new(MockBackend::new(BackendConfig::default()))
            }
        }
        4 => {
            if let Some(key) = get_api_key("PERPLEXITY_API_KEY") {
                tracing::info!("Using Perplexity API");
                Box::new(PerplexityBackend::new(config_with_key(key)))
            } else {
                tracing::warn!("PERPLEXITY_API_KEY not set, falling back to mock");
                Box::new(MockBackend::new(BackendConfig::default()))
            }
        }
        5 => {
            tracing::info!("Using arXiv API (public, no key needed)");
            Box::new(ArxivBackend::new(BackendConfig::default()))
        }
        6 => {
            tracing::info!("Using Hacker News Algolia API (public, no key needed)");
            Box::new(HackerNewsBackend::new(BackendConfig::default()))
        }
        7 => {
            let config = if let Some(key) = get_api_key("GITHUB_TOKEN") {
                tracing::info!("Using GitHub API (authenticated)");
                config_with_key(key)
            } else {
                tracing::info!("Using GitHub API (unauthenticated, rate-limited)");
                BackendConfig::default()
            };
            Box::new(GitHubBackend::new(config))
        }
        _ => {
            // Default: try perplexity → brave → mock
            if let Some(key) = get_api_key("PERPLEXITY_API_KEY") {
                tracing::info!("Default depth: using Perplexity API");
                Box::new(PerplexityBackend::new(config_with_key(key)))
            } else if let Some(key) = get_api_key("BRAVE_API_KEY") {
                tracing::info!("Default depth: using Brave Search API");
                Box::new(BraveBackend::new(config_with_key(key)))
            } else {
                tracing::info!("No API keys found, using mock backend");
                Box::new(MockBackend::new(BackendConfig::default()))
            }
        }
    };

    let tx_clone = tx.clone();
    let query_clone = query.clone();

    let backend_handle = tokio::spawn(async move {
        match backend.search(&query_clone, tx_clone).await {
            Ok(_result) => {
                tracing::info!("Search completed successfully");
            }
            Err(e) => {
                tracing::error!("Search failed: {}", e);
            }
        }
    });

    let app = app::ResearchApp::new(query).with_backend_channel(rx);

    let fullscreen_copy = fullscreen;
    let tui_handle = thread::spawn(move || {
        app::run(app, fullscreen_copy)
    });

    let tui_result = tui_handle.join().map_err(|_| anyhow::anyhow!("TUI thread panicked"))?;
    backend_handle.abort();
    tui_result?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn get_api_key_returns_none_for_unset() {
        // Use a key name that definitely won't be set
        assert!(get_api_key("__RESEARCH_TEST_NONEXISTENT_KEY__").is_none());
    }

    #[test]
    fn config_with_key_sets_api_key() {
        let config = config_with_key("test-key".to_string());
        assert_eq!(config.api_key.unwrap(), "test-key");
        assert_eq!(config.timeout_secs, 300);
    }

    #[test]
    fn get_api_key_returns_none_for_empty() {
        std::env::set_var("__RESEARCH_TEST_EMPTY_KEY__", "");
        assert!(get_api_key("__RESEARCH_TEST_EMPTY_KEY__").is_none());
        std::env::remove_var("__RESEARCH_TEST_EMPTY_KEY__");
    }

    #[test]
    fn get_api_key_returns_some_for_set() {
        std::env::set_var("__RESEARCH_TEST_SET_KEY__", "my-api-key");
        let result = get_api_key("__RESEARCH_TEST_SET_KEY__");
        assert_eq!(result.unwrap(), "my-api-key");
        std::env::remove_var("__RESEARCH_TEST_SET_KEY__");
    }
}
