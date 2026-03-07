//! Valyu backend - recursive confidence research

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::{json, Value};
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct ValyuBackend {
    config: BackendConfig,
}

impl ValyuBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    fn api_key(&self) -> Result<String> {
        if let Some(ref key) = self.config.api_key {
            return Ok(key.clone());
        }
        std::env::var("VALYU_API_KEY").context("VALYU_API_KEY not set and no key in config")
    }
}

impl ResearchBackend for ValyuBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[VALYU] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching with Valyu...".to_string(),
            });

            let api_key = self.api_key()?;

            let client = reqwest::Client::new();
            let resp = client
                .post("https://api.valyu.network/v1/search")
                .header("x-api-key", &api_key)
                .header("Content-Type", "application/json")
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .json(&json!({
                    "query": query,
                    "search_type": "all",
                    "max_num_results": 10
                }))
                .send()
                .await
                .context("Failed to send request to Valyu API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("Valyu search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("Valyu search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse Valyu JSON response")?;

            let mut sources = Vec::new();

            if let Some(results_array) = data["results"].as_array() {
                let _ = tx.send(BackendEvent::Progress {
                    current: 0,
                    total: results_array.len() as u32,
                    message: Some("Processing search results".to_string()),
                });

                for (i, result) in results_array.iter().enumerate() {
                    let title = result["title"].as_str().unwrap_or("Untitled").to_string();
                    let url = result["url"].as_str().unwrap_or("").to_string();
                    let content = result["content"].as_str().map(|s| s.to_string());
                    let source_type = result["source"].as_str().unwrap_or("general").to_string();

                    let _ = tx.send(BackendEvent::SourceFound {
                        title: title.clone(),
                        url: url.clone(),
                        source_type: source_type.clone(),
                    });

                    sources.push(Source {
                        title,
                        url,
                        content,
                        source_type,
                    });

                    let _ = tx.send(BackendEvent::Progress {
                        current: (i + 1) as u32,
                        total: results_array.len() as u32,
                        message: None,
                    });
                }
            }

            let cost_usd = data["total_deduction_dollars"].as_f64().unwrap_or(0.0);

            let _ = tx.send(BackendEvent::Cost {
                amount_usd: cost_usd,
                backend: "valyu".to_string(),
            });

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Found {} sources (${:.4})", sources.len(), cost_usd),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd,
                backend: "valyu".to_string(),
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
                message: "[VALYU] Direct extraction not supported".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "valyu"
    }
}
