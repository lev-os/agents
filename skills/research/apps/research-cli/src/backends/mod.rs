//! Backend integration system for research CLI tools
//!
//! Provides async wrappers around CLI tools (valyu, firecrawl, brave-search)
//! and public APIs (arXiv, Hacker News) with progress events emitted to the TUI in real-time.

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub mod valyu;
pub mod firecrawl;
pub mod brave;
pub mod mock;
pub mod perplexity;
pub mod arxiv;
pub mod github;
pub mod hackernews;

/// Progress event emitted during backend execution
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum BackendEvent {
    /// Log message to display
    Log { message: String },

    /// Source found
    SourceFound {
        title: String,
        url: String,
        source_type: String,
    },

    /// Progress update (0-100)
    Progress {
        current: u32,
        total: u32,
        message: Option<String>,
    },

    /// Cost update
    Cost {
        amount_usd: f64,
        backend: String,
    },

    /// Status change
    Status {
        status: String,
    },

    /// Error occurred
    Error {
        message: String,
    },

    /// Backend completed
    Complete {
        summary: String,
    },
}

/// Backend trait for research tools
pub trait ResearchBackend: Send + Sync {
    /// Search for information on a query
    fn search(&self, query: &str, tx: mpsc::UnboundedSender<BackendEvent>) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>>;

    /// Extract content from URLs
    fn extract(&self, urls: &[String], tx: mpsc::UnboundedSender<BackendEvent>) -> Pin<Box<dyn Future<Output = Result<Vec<ExtractedContent>>> + Send + '_>>;

    /// Get backend name
    fn name(&self) -> &str;
}

/// Search result from a backend
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResult {
    pub query: String,
    pub sources: Vec<Source>,
    pub cost_usd: f64,
    pub backend: String,
}

/// A single source from search results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Source {
    pub title: String,
    pub url: String,
    pub content: Option<String>,
    pub source_type: String,
}

/// Extracted content from a URL
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExtractedContent {
    pub url: String,
    pub title: Option<String>,
    pub markdown: String,
    pub success: bool,
}

/// Backend configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BackendConfig {
    pub api_key: Option<String>,
    pub timeout_secs: u64,
}

impl Default for BackendConfig {
    fn default() -> Self {
        Self {
            api_key: None,
            timeout_secs: 300, // 5 minutes
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn backend_config_default_has_no_api_key() {
        let config = BackendConfig::default();
        assert!(config.api_key.is_none());
    }

    #[test]
    fn backend_config_default_timeout_is_300() {
        let config = BackendConfig::default();
        assert_eq!(config.timeout_secs, 300);
    }

    #[test]
    fn backend_config_with_api_key() {
        let config = BackendConfig {
            api_key: Some("test-key-123".to_string()),
            timeout_secs: 60,
        };
        assert_eq!(config.api_key.unwrap(), "test-key-123");
        assert_eq!(config.timeout_secs, 60);
    }

    #[test]
    fn search_result_serialization_roundtrip() {
        let result = SearchResult {
            query: "test query".to_string(),
            sources: vec![Source {
                title: "Test Source".to_string(),
                url: "https://example.com".to_string(),
                content: Some("content".to_string()),
                source_type: "web".to_string(),
            }],
            cost_usd: 0.05,
            backend: "mock".to_string(),
        };

        let json = serde_json::to_string(&result).unwrap();
        let deserialized: SearchResult = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.query, "test query");
        assert_eq!(deserialized.sources.len(), 1);
        assert_eq!(deserialized.cost_usd, 0.05);
        assert_eq!(deserialized.backend, "mock");
    }

    #[test]
    fn source_serialization_roundtrip() {
        let source = Source {
            title: "My Source".to_string(),
            url: "https://example.com/page".to_string(),
            content: None,
            source_type: "academic".to_string(),
        };

        let json = serde_json::to_string(&source).unwrap();
        let deserialized: Source = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.title, "My Source");
        assert_eq!(deserialized.url, "https://example.com/page");
        assert!(deserialized.content.is_none());
        assert_eq!(deserialized.source_type, "academic");
    }

    #[test]
    fn source_with_content() {
        let source = Source {
            title: "Test".to_string(),
            url: "https://example.com".to_string(),
            content: Some("This is the content".to_string()),
            source_type: "web".to_string(),
        };
        assert_eq!(source.content.unwrap(), "This is the content");
    }

    #[test]
    fn extracted_content_serialization_roundtrip() {
        let content = ExtractedContent {
            url: "https://example.com".to_string(),
            title: Some("Page Title".to_string()),
            markdown: "# Hello\nWorld".to_string(),
            success: true,
        };

        let json = serde_json::to_string(&content).unwrap();
        let deserialized: ExtractedContent = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.url, "https://example.com");
        assert_eq!(deserialized.title.unwrap(), "Page Title");
        assert_eq!(deserialized.markdown, "# Hello\nWorld");
        assert!(deserialized.success);
    }

    #[test]
    fn extracted_content_failed() {
        let content = ExtractedContent {
            url: "https://bad.example.com".to_string(),
            title: None,
            markdown: String::new(),
            success: false,
        };
        assert!(!content.success);
        assert!(content.title.is_none());
        assert!(content.markdown.is_empty());
    }

    #[test]
    fn backend_event_log_serialization() {
        let event = BackendEvent::Log {
            message: "test log".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        assert!(json.contains("Log"));
        assert!(json.contains("test log"));
    }

    #[test]
    fn backend_event_source_found_serialization() {
        let event = BackendEvent::SourceFound {
            title: "Title".to_string(),
            url: "https://example.com".to_string(),
            source_type: "web".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::SourceFound { title, url, source_type } => {
                assert_eq!(title, "Title");
                assert_eq!(url, "https://example.com");
                assert_eq!(source_type, "web");
            }
            _ => panic!("Expected SourceFound variant"),
        }
    }

    #[test]
    fn backend_event_progress_serialization() {
        let event = BackendEvent::Progress {
            current: 5,
            total: 10,
            message: Some("halfway".to_string()),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::Progress { current, total, message } => {
                assert_eq!(current, 5);
                assert_eq!(total, 10);
                assert_eq!(message.unwrap(), "halfway");
            }
            _ => panic!("Expected Progress variant"),
        }
    }

    #[test]
    fn backend_event_cost_serialization() {
        let event = BackendEvent::Cost {
            amount_usd: 0.025,
            backend: "valyu".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::Cost { amount_usd, backend } => {
                assert!((amount_usd - 0.025).abs() < f64::EPSILON);
                assert_eq!(backend, "valyu");
            }
            _ => panic!("Expected Cost variant"),
        }
    }

    #[test]
    fn backend_event_complete_serialization() {
        let event = BackendEvent::Complete {
            summary: "Done with 5 sources".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::Complete { summary } => {
                assert_eq!(summary, "Done with 5 sources");
            }
            _ => panic!("Expected Complete variant"),
        }
    }

    #[test]
    fn backend_event_error_serialization() {
        let event = BackendEvent::Error {
            message: "connection timeout".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::Error { message } => {
                assert_eq!(message, "connection timeout");
            }
            _ => panic!("Expected Error variant"),
        }
    }

    #[test]
    fn backend_event_status_serialization() {
        let event = BackendEvent::Status {
            status: "Searching with Brave...".to_string(),
        };
        let json = serde_json::to_string(&event).unwrap();
        let deserialized: BackendEvent = serde_json::from_str(&json).unwrap();
        match deserialized {
            BackendEvent::Status { status } => {
                assert_eq!(status, "Searching with Brave...");
            }
            _ => panic!("Expected Status variant"),
        }
    }

    #[test]
    fn search_result_empty_sources() {
        let result = SearchResult {
            query: "empty".to_string(),
            sources: vec![],
            cost_usd: 0.0,
            backend: "mock".to_string(),
        };
        assert!(result.sources.is_empty());
        assert_eq!(result.cost_usd, 0.0);
    }
}
