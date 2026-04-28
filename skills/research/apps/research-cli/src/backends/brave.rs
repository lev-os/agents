//! Brave backend - fast web search

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::Value;
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct BraveBackend {
    config: BackendConfig,
}

impl BraveBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    fn api_key(&self) -> Result<String> {
        if let Some(ref key) = self.config.api_key {
            return Ok(key.clone());
        }
        std::env::var("BRAVE_API_KEY").context("BRAVE_API_KEY not set and no key in config")
    }
}

impl ResearchBackend for BraveBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[BRAVE] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching with Brave...".to_string(),
            });

            let api_key = self.api_key()?;

            let client = reqwest::Client::new();
            let resp = client
                .get("https://api.search.brave.com/res/v1/web/search")
                .query(&[("q", &query), ("count", &"10".to_string())])
                .header("X-Subscription-Token", &api_key)
                .header("Accept", "application/json")
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .send()
                .await
                .context("Failed to send request to Brave Search API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("Brave search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("Brave search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse Brave JSON response")?;

            let mut sources = Vec::new();

            if let Some(results_array) = data["web"]["results"].as_array() {
                let _ = tx.send(BackendEvent::Progress {
                    current: 0,
                    total: results_array.len() as u32,
                    message: Some("Processing search results".to_string()),
                });

                for (i, result) in results_array.iter().enumerate() {
                    let title = result["title"].as_str().unwrap_or("Untitled").to_string();
                    let url = result["url"].as_str().unwrap_or("").to_string();
                    let content = result["description"].as_str().map(|s| s.to_string());

                    let _ = tx.send(BackendEvent::SourceFound {
                        title: title.clone(),
                        url: url.clone(),
                        source_type: "web".to_string(),
                    });

                    sources.push(Source {
                        title,
                        url,
                        content,
                        source_type: "web".to_string(),
                    });

                    let _ = tx.send(BackendEvent::Progress {
                        current: (i + 1) as u32,
                        total: results_array.len() as u32,
                        message: None,
                    });
                }
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Found {} sources", sources.len()),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd: 0.0,
                backend: "brave".to_string(),
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
                message: "[BRAVE] Extract not supported, use Firecrawl".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "brave"
    }
}
