//! Firecrawl backend - web scraping and extraction

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::{json, Value};
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct FirecrawlBackend {
    config: BackendConfig,
}

impl FirecrawlBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    fn api_key(&self) -> Result<String> {
        if let Some(ref key) = self.config.api_key {
            return Ok(key.clone());
        }
        std::env::var("FIRECRAWL_API_KEY")
            .context("FIRECRAWL_API_KEY not set and no key in config")
    }
}

impl ResearchBackend for FirecrawlBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[FIRECRAWL] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching with Firecrawl...".to_string(),
            });

            let api_key = self.api_key()?;

            let client = reqwest::Client::new();
            let resp = client
                .post("https://api.firecrawl.dev/v1/search")
                .header("Authorization", format!("Bearer {}", api_key))
                .header("Content-Type", "application/json")
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .json(&json!({
                    "query": query,
                    "limit": 10,
                    "scrapeOptions": {
                        "formats": ["markdown"]
                    }
                }))
                .send()
                .await
                .context("Failed to send request to Firecrawl Search API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("Firecrawl search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("Firecrawl search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse Firecrawl JSON response")?;

            let mut sources = Vec::new();

            if let Some(results_array) = data["data"].as_array() {
                let _ = tx.send(BackendEvent::Progress {
                    current: 0,
                    total: results_array.len() as u32,
                    message: Some("Processing search results".to_string()),
                });

                for (i, result) in results_array.iter().enumerate() {
                    let title = result["metadata"]["title"]
                        .as_str()
                        .or_else(|| result["title"].as_str())
                        .unwrap_or("Untitled")
                        .to_string();
                    let url = result["url"].as_str().unwrap_or("").to_string();
                    let content = result["metadata"]["description"]
                        .as_str()
                        .or_else(|| result["description"].as_str())
                        .or_else(|| result["markdown"].as_str())
                        .map(|s| s.to_string());

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
                backend: "firecrawl".to_string(),
            })
        })
    }

    fn extract(
        &self,
        urls: &[String],
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<ExtractedContent>>> + Send + '_>> {
        let urls = urls.to_vec();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[FIRECRAWL] Scraping {} URLs", urls.len()),
            });

            let api_key = self.api_key()?;
            let client = reqwest::Client::new();
            let mut extracted = Vec::new();

            let _ = tx.send(BackendEvent::Progress {
                current: 0,
                total: urls.len() as u32,
                message: Some("Scraping pages".to_string()),
            });

            for (i, url) in urls.iter().enumerate() {
                let _ = tx.send(BackendEvent::Log {
                    message: format!("[FIRECRAWL] Scraping: {}", url),
                });

                let resp = client
                    .post("https://api.firecrawl.dev/v1/scrape")
                    .header("Authorization", format!("Bearer {}", api_key))
                    .header("Content-Type", "application/json")
                    .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                    .json(&json!({
                        "url": url,
                        "formats": ["markdown"]
                    }))
                    .send()
                    .await;

                match resp {
                    Ok(r) if r.status().is_success() => {
                        let data: Value = match r.json().await {
                            Ok(v) => v,
                            Err(e) => {
                                let _ = tx.send(BackendEvent::Error {
                                    message: format!(
                                        "Failed to parse scrape response for {}: {}",
                                        url, e
                                    ),
                                });
                                extracted.push(ExtractedContent {
                                    url: url.clone(),
                                    title: None,
                                    markdown: String::new(),
                                    success: false,
                                });
                                continue;
                            }
                        };

                        let title =
                            data["data"]["metadata"]["title"].as_str().map(|s| s.to_string());
                        let markdown =
                            data["data"]["markdown"].as_str().unwrap_or("").to_string();

                        extracted.push(ExtractedContent {
                            url: url.clone(),
                            title,
                            markdown,
                            success: true,
                        });
                    }
                    Ok(r) => {
                        let status = r.status();
                        let body = r.text().await.unwrap_or_default();
                        let _ = tx.send(BackendEvent::Error {
                            message: format!(
                                "Scrape failed for {}: HTTP {} - {}",
                                url, status, body
                            ),
                        });
                        extracted.push(ExtractedContent {
                            url: url.clone(),
                            title: None,
                            markdown: String::new(),
                            success: false,
                        });
                    }
                    Err(e) => {
                        let _ = tx.send(BackendEvent::Error {
                            message: format!("Scrape failed for {}: {}", url, e),
                        });
                        extracted.push(ExtractedContent {
                            url: url.clone(),
                            title: None,
                            markdown: String::new(),
                            success: false,
                        });
                    }
                }

                let _ = tx.send(BackendEvent::Progress {
                    current: (i + 1) as u32,
                    total: urls.len() as u32,
                    message: None,
                });
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!(
                    "Scraped {}/{} URLs successfully",
                    extracted.iter().filter(|e| e.success).count(),
                    urls.len()
                ),
            });

            Ok(extracted)
        })
    }

    fn name(&self) -> &str {
        "firecrawl"
    }
}
