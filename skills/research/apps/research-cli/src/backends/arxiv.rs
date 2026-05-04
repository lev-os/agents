//! arXiv backend - academic paper search (no API key needed)

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct ArxivBackend {
    config: BackendConfig,
}

impl ArxivBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    /// Helper to extract text between XML tags from a fragment.
    /// Returns the first match or None.
    fn extract_tag(xml: &str, tag: &str) -> Option<String> {
        let open = format!("<{}", tag);
        let close = format!("</{}>", tag);
        if let Some(start_pos) = xml.find(&open) {
            // Skip past the opening tag (handle attributes like <link href="...">)
            let after_open = &xml[start_pos + open.len()..];
            if let Some(gt) = after_open.find('>') {
                let content_start = &after_open[gt + 1..];
                if let Some(end_pos) = content_start.find(&close) {
                    let text = &content_start[..end_pos];
                    return Some(text.trim().to_string());
                }
            }
        }
        None
    }

    /// Extract the href attribute from a <link> tag with a specific title or rel.
    fn extract_pdf_link(entry: &str) -> Option<String> {
        // Look for <link ... title="pdf" ... href="..." />
        let mut search_from = 0;
        while let Some(pos) = entry[search_from..].find("<link") {
            let abs_pos = search_from + pos;
            let tag_end = entry[abs_pos..].find("/>").or_else(|| entry[abs_pos..].find('>'));
            if let Some(end) = tag_end {
                let tag = &entry[abs_pos..abs_pos + end + 2];
                if tag.contains("title=\"pdf\"") {
                    // Extract href
                    if let Some(href_start) = tag.find("href=\"") {
                        let href_rest = &tag[href_start + 6..];
                        if let Some(href_end) = href_rest.find('"') {
                            return Some(href_rest[..href_end].to_string());
                        }
                    }
                }
                search_from = abs_pos + end + 1;
            } else {
                break;
            }
        }
        None
    }

    /// Extract all <author><name>...</name></author> values from an entry.
    fn extract_authors(entry: &str) -> Vec<String> {
        let mut authors = Vec::new();
        let mut search_from = 0;
        while let Some(pos) = entry[search_from..].find("<author>") {
            let abs_pos = search_from + pos;
            if let Some(end_pos) = entry[abs_pos..].find("</author>") {
                let author_block = &entry[abs_pos..abs_pos + end_pos];
                if let Some(name) = Self::extract_tag(author_block, "name") {
                    authors.push(name);
                }
                search_from = abs_pos + end_pos + 9;
            } else {
                break;
            }
        }
        authors
    }
}

impl ResearchBackend for ArxivBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[ARXIV] Starting search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching arXiv...".to_string(),
            });

            let client = reqwest::Client::new();
            let resp = client
                .get("http://export.arxiv.org/api/query")
                .query(&[
                    ("search_query", format!("all:{}", query).as_str()),
                    ("start", "0"),
                    ("max_results", "10"),
                    ("sortBy", "relevance"),
                ])
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs))
                .send()
                .await
                .context("Failed to send request to arXiv API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("arXiv search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("arXiv search failed: HTTP {} - {}", status, body);
            }

            let xml = resp
                .text()
                .await
                .context("Failed to read arXiv response body")?;

            // Split on <entry> to get individual entries (skip the first chunk which is feed metadata)
            let entry_chunks: Vec<&str> = xml.split("<entry>").collect();
            let entries = if entry_chunks.len() > 1 {
                &entry_chunks[1..]
            } else {
                &[]
            };

            let _ = tx.send(BackendEvent::Progress {
                current: 0,
                total: entries.len() as u32,
                message: Some("Processing arXiv results".to_string()),
            });

            let mut sources = Vec::new();

            for (i, entry) in entries.iter().enumerate() {
                let title = Self::extract_tag(entry, "title")
                    .unwrap_or_else(|| "Untitled".to_string())
                    // arXiv titles often contain newlines
                    .replace('\n', " ")
                    .split_whitespace()
                    .collect::<Vec<&str>>()
                    .join(" ");

                let summary = Self::extract_tag(entry, "summary").map(|s| {
                    s.replace('\n', " ")
                        .split_whitespace()
                        .collect::<Vec<&str>>()
                        .join(" ")
                });

                // <id> contains the arxiv URL (e.g., http://arxiv.org/abs/1234.5678v1)
                let url = Self::extract_tag(entry, "id").unwrap_or_default();

                let pdf_url = Self::extract_pdf_link(entry);

                let authors = Self::extract_authors(entry);
                let author_str = if authors.is_empty() {
                    String::new()
                } else {
                    format!(" ({})", authors.join(", "))
                };

                let display_title = format!("{}{}", title, author_str);

                let _ = tx.send(BackendEvent::SourceFound {
                    title: display_title.clone(),
                    url: url.clone(),
                    source_type: "academic".to_string(),
                });

                // Build content: summary + pdf link if available
                let content = match (&summary, &pdf_url) {
                    (Some(s), Some(pdf)) => Some(format!("{}\n\nPDF: {}", s, pdf)),
                    (Some(s), None) => Some(s.clone()),
                    (None, Some(pdf)) => Some(format!("PDF: {}", pdf)),
                    (None, None) => None,
                };

                sources.push(Source {
                    title: display_title,
                    url,
                    content,
                    source_type: "academic".to_string(),
                });

                let _ = tx.send(BackendEvent::Progress {
                    current: (i + 1) as u32,
                    total: entries.len() as u32,
                    message: None,
                });
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Found {} papers", sources.len()),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd: 0.0,
                backend: "arxiv".to_string(),
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
                message: "[ARXIV] Extract not supported (papers are PDFs)".to_string(),
            });

            Ok(Vec::new())
        })
    }

    fn name(&self) -> &str {
        "arxiv"
    }
}
