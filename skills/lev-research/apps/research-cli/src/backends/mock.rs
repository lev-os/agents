//! Mock backend - graceful fallback when real CLIs aren't available

use super::{BackendEvent, BackendConfig, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::Result;
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct MockBackend {
    #[allow(dead_code)]
    config: BackendConfig,
}

impl MockBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }
}

impl ResearchBackend for MockBackend {
    fn search(&self, query: &str, tx: mpsc::UnboundedSender<BackendEvent>) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[MOCK] Starting simulated search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Running mock search (CLI tools not found)...".to_string(),
            });

            // Simulate delay
            tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;

            let mock_sources = vec![
                Source {
                    title: format!("Mock result 1: {}", query),
                    url: format!("https://example.com/1?q={}", urlencoding::encode(&query)),
                    content: Some(format!("Mock search result about {}. Real CLI tools (brave-search, valyu, firecrawl) are not installed.", query)),
                    source_type: "web".to_string(),
                },
                Source {
                    title: format!("Mock result 2: {}", query),
                    url: format!("https://example.org/2?q={}", urlencoding::encode(&query)),
                    content: Some(format!("Another simulated result for {}. Install CLI tools for real results.", query)),
                    source_type: "web".to_string(),
                },
                Source {
                    title: format!("Academic mock: {}", query),
                    url: format!("https://academic.example.com?q={}", urlencoding::encode(&query)),
                    content: Some(format!("Simulated academic paper on {}.", query)),
                    source_type: "academic".to_string(),
                },
            ];

            for (i, source) in mock_sources.iter().enumerate() {
                tokio::time::sleep(tokio::time::Duration::from_millis(300)).await;

                let _ = tx.send(BackendEvent::SourceFound {
                    title: source.title.clone(),
                    url: source.url.clone(),
                    source_type: source.source_type.clone(),
                });

                let _ = tx.send(BackendEvent::Progress {
                    current: (i + 1) as u32,
                    total: mock_sources.len() as u32,
                    message: Some(format!("Processing mock source {}", i + 1)),
                });
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Mock search completed - {} simulated sources (install CLI tools for real results)", mock_sources.len()),
            });

            Ok(SearchResult {
                query: query.to_string(),
                sources: mock_sources,
                cost_usd: 0.0,
                backend: "mock".to_string(),
            })
        })
    }

    fn extract(&self, _urls: &[String], tx: mpsc::UnboundedSender<BackendEvent>) -> Pin<Box<dyn Future<Output = Result<Vec<ExtractedContent>>> + Send + '_>> {
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: "[MOCK] Extract not implemented in mock backend".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "mock"
    }
}

/// Check if a CLI tool is available
pub async fn cli_available(cmd: &str) -> bool {
    tokio::process::Command::new("which")
        .arg(cmd)
        .output()
        .await
        .map(|o| o.status.success())
        .unwrap_or(false)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::backends::{BackendConfig, BackendEvent, ResearchBackend};
    use tokio::sync::mpsc;

    #[tokio::test]
    async fn mock_search_returns_3_sources() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _rx) = mpsc::unbounded_channel();
        let result = backend.search("test query", tx).await.unwrap();
        assert_eq!(result.sources.len(), 3);
        assert_eq!(result.backend, "mock");
        assert_eq!(result.cost_usd, 0.0);
    }

    #[tokio::test]
    async fn mock_search_query_propagated() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _rx) = mpsc::unbounded_channel();
        let result = backend.search("rust async", tx).await.unwrap();
        assert_eq!(result.query, "rust async");
        // Each source title should contain the query
        for source in &result.sources {
            assert!(
                source.title.contains("rust async"),
                "Source title '{}' should contain the query",
                source.title
            );
        }
    }

    #[tokio::test]
    async fn mock_search_emits_events() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, mut rx) = mpsc::unbounded_channel();
        let _ = backend.search("test", tx).await.unwrap();

        let mut event_count = 0;
        while let Ok(_event) = rx.try_recv() {
            event_count += 1;
        }
        // Expected: Log + Status + 3*(SourceFound + Progress) + Complete = 9
        assert!(
            event_count >= 8,
            "Expected at least 8 events, got {}",
            event_count
        );
    }

    #[tokio::test]
    async fn mock_search_event_sequence() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, mut rx) = mpsc::unbounded_channel();
        let _ = backend.search("test", tx).await.unwrap();

        let mut events = Vec::new();
        while let Ok(event) = rx.try_recv() {
            events.push(event);
        }

        // First event should be a Log
        assert!(
            matches!(&events[0], BackendEvent::Log { .. }),
            "First event should be Log, got {:?}",
            events[0]
        );

        // Second event should be Status
        assert!(
            matches!(&events[1], BackendEvent::Status { .. }),
            "Second event should be Status, got {:?}",
            events[1]
        );

        // Last event should be Complete
        assert!(
            matches!(events.last().unwrap(), BackendEvent::Complete { .. }),
            "Last event should be Complete, got {:?}",
            events.last().unwrap()
        );
    }

    #[tokio::test]
    async fn mock_search_sources_have_valid_urls() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _) = mpsc::unbounded_channel();
        let result = backend.search("rust async", tx).await.unwrap();
        for source in &result.sources {
            assert!(
                source.url.starts_with("https://"),
                "URL '{}' should start with https://",
                source.url
            );
        }
    }

    #[tokio::test]
    async fn mock_search_sources_encode_query_in_url() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _) = mpsc::unbounded_channel();
        let result = backend.search("rust async", tx).await.unwrap();
        for source in &result.sources {
            assert!(
                source.url.contains("rust%20async") || source.url.contains("rust+async"),
                "URL '{}' should contain encoded query",
                source.url
            );
        }
    }

    #[tokio::test]
    async fn mock_search_has_web_and_academic_types() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _) = mpsc::unbounded_channel();
        let result = backend.search("test", tx).await.unwrap();
        let types: Vec<&str> = result.sources.iter().map(|s| s.source_type.as_str()).collect();
        assert!(types.contains(&"web"), "Should contain web sources");
        assert!(types.contains(&"academic"), "Should contain academic sources");
    }

    #[tokio::test]
    async fn mock_search_sources_have_content() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _) = mpsc::unbounded_channel();
        let result = backend.search("deep learning", tx).await.unwrap();
        for source in &result.sources {
            assert!(
                source.content.is_some(),
                "Mock source '{}' should have content",
                source.title
            );
        }
    }

    #[tokio::test]
    async fn mock_backend_name_is_mock() {
        let backend = MockBackend::new(BackendConfig::default());
        assert_eq!(backend.name(), "mock");
    }

    #[tokio::test]
    async fn mock_extract_returns_empty() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _) = mpsc::unbounded_channel();
        let result = backend
            .extract(&["https://example.com".to_string()], tx)
            .await
            .unwrap();
        assert!(result.is_empty());
    }

    #[tokio::test]
    async fn mock_extract_emits_log() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, mut rx) = mpsc::unbounded_channel();
        let _ = backend
            .extract(&["https://example.com".to_string()], tx)
            .await
            .unwrap();
        let event = rx.try_recv().expect("Should emit at least one event");
        assert!(
            matches!(event, BackendEvent::Log { .. }),
            "Extract should emit a Log event"
        );
    }

    #[tokio::test]
    async fn cli_available_returns_true_for_ls() {
        // 'ls' should be available on any Unix system
        assert!(cli_available("ls").await);
    }

    #[tokio::test]
    async fn cli_available_returns_false_for_nonexistent() {
        assert!(!cli_available("this-command-definitely-does-not-exist-42xyz").await);
    }

    #[tokio::test]
    async fn e2e_full_search_pipeline() {
        // Test complete pipeline: init → events → complete
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, mut rx) = mpsc::unbounded_channel();
        let result = backend.search("full pipeline test", tx).await.unwrap();

        // Verify result structure
        assert_eq!(result.query, "full pipeline test");
        assert_eq!(result.sources.len(), 3);
        assert_eq!(result.backend, "mock");

        // Verify event pipeline completeness
        let mut events = Vec::new();
        while let Ok(event) = rx.try_recv() {
            events.push(event);
        }

        // Should have: Log, Status, 3x(SourceFound, Progress), Complete = 9 events
        assert!(events.len() >= 8, "Full pipeline should emit at least 8 events, got {}", events.len());

        // First two events should be Log and Status
        assert!(matches!(&events[0], BackendEvent::Log { .. }));
        assert!(matches!(&events[1], BackendEvent::Status { .. }));

        // Last event should be Complete
        assert!(matches!(events.last().unwrap(), BackendEvent::Complete { .. }));

        // Count SourceFound events
        let source_found_count = events.iter().filter(|e| matches!(e, BackendEvent::SourceFound { .. })).count();
        assert_eq!(source_found_count, 3, "Should have 3 SourceFound events");

        // Count Progress events
        let progress_count = events.iter().filter(|e| matches!(e, BackendEvent::Progress { .. })).count();
        assert_eq!(progress_count, 3, "Should have 3 Progress events");
    }

    #[tokio::test]
    async fn e2e_concurrent_searches_dont_interfere() {
        // Two concurrent searches should produce independent results
        let backend1 = MockBackend::new(BackendConfig::default());
        let backend2 = MockBackend::new(BackendConfig::default());
        let (tx1, _rx1) = mpsc::unbounded_channel();
        let (tx2, _rx2) = mpsc::unbounded_channel();

        let (result1, result2) = tokio::join!(
            backend1.search("query alpha", tx1),
            backend2.search("query beta", tx2)
        );

        let r1 = result1.unwrap();
        let r2 = result2.unwrap();

        assert_eq!(r1.query, "query alpha");
        assert_eq!(r2.query, "query beta");

        // Source titles should reflect their respective queries
        assert!(r1.sources[0].title.contains("query alpha"));
        assert!(r2.sources[0].title.contains("query beta"));

        // Both should have independent source sets
        assert_eq!(r1.sources.len(), 3);
        assert_eq!(r2.sources.len(), 3);
    }

    #[tokio::test]
    async fn e2e_error_event_propagation() {
        // When the receiver is dropped, search should still complete without panic
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, rx) = mpsc::unbounded_channel();

        // Drop receiver immediately
        drop(rx);

        // Search should still complete (sends fail silently)
        let result = backend.search("orphaned search", tx).await;
        assert!(result.is_ok(), "Search should complete even if receiver is dropped");
        let r = result.unwrap();
        assert_eq!(r.query, "orphaned search");
        assert_eq!(r.sources.len(), 3);
    }

    #[tokio::test]
    async fn e2e_search_result_cost_is_zero_for_mock() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, _rx) = mpsc::unbounded_channel();
        let result = backend.search("cost check", tx).await.unwrap();
        assert_eq!(result.cost_usd, 0.0, "Mock backend should have zero cost");
    }

    #[tokio::test]
    async fn e2e_progress_events_count_up_correctly() {
        let backend = MockBackend::new(BackendConfig::default());
        let (tx, mut rx) = mpsc::unbounded_channel();
        let _ = backend.search("progress test", tx).await.unwrap();

        let mut events = Vec::new();
        while let Ok(event) = rx.try_recv() {
            events.push(event);
        }

        let progress_events: Vec<_> = events.iter().filter_map(|e| {
            if let BackendEvent::Progress { current, total, .. } = e {
                Some((*current, *total))
            } else {
                None
            }
        }).collect();

        // Progress should count 1, 2, 3 out of 3
        assert_eq!(progress_events.len(), 3);
        for (i, (current, total)) in progress_events.iter().enumerate() {
            assert_eq!(*current, (i + 1) as u32);
            assert_eq!(*total, 3);
        }
    }
}
