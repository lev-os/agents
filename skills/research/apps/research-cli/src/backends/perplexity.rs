//! Perplexity backend - AI-powered search with citations

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::{json, Value};
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct PerplexityBackend {
    config: BackendConfig,
}

impl PerplexityBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    fn api_key(&self) -> Result<String> {
        if let Some(ref key) = self.config.api_key {
            return Ok(key.clone());
        }
        std::env::var("PERPLEXITY_API_KEY")
            .context("PERPLEXITY_API_KEY not set and no key in config")
    }
}

impl ResearchBackend for PerplexityBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[PERPLEXITY] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching with Perplexity AI...".to_string(),
            });

            let api_key = self.api_key()?;

            let client = reqwest::Client::new();
            let resp = client
                .post("https://api.perplexity.ai/chat/completions")
                .header("Authorization", format!("Bearer {}", api_key))
                .header("Content-Type", "application/json")
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .json(&json!({
                    "model": "sonar",
                    "messages": [{"role": "user", "content": query}]
                }))
                .send()
                .await
                .context("Failed to send request to Perplexity API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("Perplexity search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("Perplexity search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse Perplexity JSON response")?;

            let mut sources = Vec::new();

            // Extract the synthesized answer
            let synthesis = data["choices"][0]["message"]["content"]
                .as_str()
                .unwrap_or("")
                .to_string();

            sources.push(Source {
                title: "Perplexity Synthesis".to_string(),
                url: String::new(),
                content: Some(synthesis),
                source_type: "synthesis".to_string(),
            });

            // Extract citations
            let citations: Vec<String> = data["citations"]
                .as_array()
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_default();

            let total = citations.len() as u32 + 1; // +1 for synthesis

            let _ = tx.send(BackendEvent::Progress {
                current: 1,
                total,
                message: Some("Processed synthesis".to_string()),
            });

            for (i, citation_url) in citations.iter().enumerate() {
                let title = format!("Citation {}", i + 1);

                let _ = tx.send(BackendEvent::SourceFound {
                    title: title.clone(),
                    url: citation_url.clone(),
                    source_type: "citation".to_string(),
                });

                sources.push(Source {
                    title,
                    url: citation_url.clone(),
                    content: None,
                    source_type: "citation".to_string(),
                });

                let _ = tx.send(BackendEvent::Progress {
                    current: (i + 2) as u32, // +2: 1 for synthesis + 1 for 0-index
                    total,
                    message: None,
                });
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!(
                    "Synthesized answer with {} citations",
                    citations.len()
                ),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd: 0.0,
                backend: "perplexity".to_string(),
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
                message: "[PERPLEXITY] Extraction handled inline during search".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "perplexity"
    }
}
