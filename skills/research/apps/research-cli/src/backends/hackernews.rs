//! Hacker News backend - tech news search via Algolia (no API key needed)

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::Value;
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct HackerNewsBackend {
    config: BackendConfig,
}

impl HackerNewsBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }
}

impl ResearchBackend for HackerNewsBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[HN] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching Hacker News...".to_string(),
            });

            let client = reqwest::Client::new();
            let resp = client
                .get("https://hn.algolia.com/api/v1/search")
                .query(&[
                    ("query", query.as_str()),
                    ("tags", "story"),
                    ("hitsPerPage", "10"),
                ])
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .send()
                .await
                .context("Failed to send request to HN Algolia API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("HN search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("HN search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse HN Algolia JSON response")?;

            let mut sources = Vec::new();

            if let Some(hits) = data["hits"].as_array() {
                let _ = tx.send(BackendEvent::Progress {
                    current: 0,
                    total: hits.len() as u32,
                    message: Some("Processing HN results".to_string()),
                });

                for (i, hit) in hits.iter().enumerate() {
                    let title = hit["title"].as_str().unwrap_or("Untitled").to_string();
                    let points = hit["points"].as_u64().unwrap_or(0);
                    let object_id = hit["objectID"].as_str().unwrap_or("");

                    // Some HN posts (Ask HN, Show HN) have no external URL
                    let url = hit["url"]
                        .as_str()
                        .filter(|u| !u.is_empty())
                        .map(|u| u.to_string())
                        .unwrap_or_else(|| {
                            format!("https://news.ycombinator.com/item?id={}", object_id)
                        });

                    let content = hit["story_text"]
                        .as_str()
                        .filter(|s| !s.is_empty())
                        .map(|s| s.to_string());

                    let display_title = format!("{} ({} pts)", title, points);

                    let _ = tx.send(BackendEvent::SourceFound {
                        title: display_title.clone(),
                        url: url.clone(),
                        source_type: "news".to_string(),
                    });

                    sources.push(Source {
                        title: display_title,
                        url,
                        content,
                        source_type: "news".to_string(),
                    });

                    let _ = tx.send(BackendEvent::Progress {
                        current: (i + 1) as u32,
                        total: hits.len() as u32,
                        message: None,
                    });
                }
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Found {} stories", sources.len()),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd: 0.0,
                backend: "hackernews".to_string(),
            })
        })
    }

    fn extract(
        &self,
        _urls: &[String],
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<ExtractedContent>>> + Send + '_>> {
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: "[HN] Extract not supported, use Firecrawl".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "hackernews"
    }
}
