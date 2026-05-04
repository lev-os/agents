//! GitHub backend - repository and code search (optional API key)

use super::{BackendConfig, BackendEvent, ExtractedContent, ResearchBackend, SearchResult, Source};
use anyhow::{Context, Result};
use serde_json::Value;
use std::future::Future;
use std::pin::Pin;
use tokio::sync::mpsc;

pub struct GitHubBackend {
    config: BackendConfig,
}

impl GitHubBackend {
    pub fn new(config: BackendConfig) -> Self {
        Self { config }
    }

    /// Returns the API token if available (config > env var).
    /// Unlike other backends, GitHub works without a token (just rate-limited).
    fn api_key(&self) -> Option<String> {
        if let Some(ref key) = self.config.api_key {
            return Some(key.clone());
        }
        std::env::var("GITHUB_TOKEN").ok()
    }

    /// Build a reqwest client with common GitHub API headers.
    fn build_client(&self) -> reqwest::Client {
        reqwest::Client::new()
    }

    /// Parse `{owner}/{repo}` from a GitHub URL.
    /// Accepts patterns like `https://github.com/tokio-rs/tokio` or
    /// `https://github.com/tokio-rs/tokio/tree/main/...`.
    fn parse_owner_repo(url: &str) -> Option<(String, String)> {
        let url = url.trim_end_matches('/');
        let stripped = url
            .strip_prefix("https://github.com/")
            .or_else(|| url.strip_prefix("http://github.com/"))?;

        let mut parts = stripped.splitn(3, '/');
        let owner = parts.next()?.to_string();
        let repo = parts.next()?.to_string();

        if owner.is_empty() || repo.is_empty() {
            return None;
        }

        Some((owner, repo))
    }
}

impl ResearchBackend for GitHubBackend {
    fn search(
        &self,
        query: &str,
        tx: mpsc::UnboundedSender<BackendEvent>,
    ) -> Pin<Box<dyn Future<Output = Result<SearchResult>> + Send + '_>> {
        let query = query.to_string();
        Box::pin(async move {
            let _ = tx.send(BackendEvent::Log {
                message: format!("[GITHUB] Starting repository search: {}", query),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Searching GitHub repositories...".to_string(),
            });

            let client = self.build_client();
            let mut req = client
                .get("https://api.github.com/search/repositories")
                .query(&[
                    ("q", query.as_str()),
                    ("sort", "stars"),
                    ("per_page", "10"),
                ])
                .header("Accept", "application/vnd.github+json")
                .header("User-Agent", "research-cli/0.1")
                .timeout(std::time::Duration::from_secs(self.config.timeout_secs));

            if let Some(ref token) = self.api_key() {
                req = req.header("Authorization", format!("Bearer {}", token));
            }

            let resp = req
                .send()
                .await
                .context("Failed to send request to GitHub Search API")?;

            if !resp.status().is_success() {
                let status = resp.status();
                let body = resp.text().await.unwrap_or_default();
                let _ = tx.send(BackendEvent::Error {
                    message: format!("GitHub search failed: HTTP {} - {}", status, body),
                });
                anyhow::bail!("GitHub search failed: HTTP {} - {}", status, body);
            }

            let data: Value = resp
                .json()
                .await
                .context("Failed to parse GitHub JSON response")?;

            let mut sources = Vec::new();

            if let Some(items) = data["items"].as_array() {
                let _ = tx.send(BackendEvent::Progress {
                    current: 0,
                    total: items.len() as u32,
                    message: Some("Processing repository results".to_string()),
                });

                for (i, item) in items.iter().enumerate() {
                    let full_name = item["full_name"]
                        .as_str()
                        .unwrap_or("unknown/repo")
                        .to_string();
                    let html_url = item["html_url"].as_str().unwrap_or("").to_string();
                    let description = item["description"]
                        .as_str()
                        .unwrap_or("No description");
                    let stars = item["stargazers_count"].as_u64().unwrap_or(0);
                    let language = item["language"]
                        .as_str()
                        .unwrap_or("Unknown");

                    let content_str =
                        format!("{} | \u{2b50} {} | {}", description, stars, language);

                    let _ = tx.send(BackendEvent::SourceFound {
                        title: full_name.clone(),
                        url: html_url.clone(),
                        source_type: "repository".to_string(),
                    });

                    sources.push(Source {
                        title: full_name,
                        url: html_url,
                        content: Some(content_str),
                        source_type: "repository".to_string(),
                    });

                    let _ = tx.send(BackendEvent::Progress {
                        current: (i + 1) as u32,
                        total: items.len() as u32,
                        message: None,
                    });
                }
            }

            let _ = tx.send(BackendEvent::Complete {
                summary: format!("Found {} repositories", sources.len()),
            });

            Ok(SearchResult {
                query,
                sources,
                cost_usd: 0.0, // GitHub API is free
                backend: "github".to_string(),
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
                message: format!("[GITHUB] Extracting README from {} URL(s)", urls.len()),
            });

            let _ = tx.send(BackendEvent::Status {
                status: "Fetching GitHub READMEs...".to_string(),
            });

            let client = self.build_client();
            let mut results = Vec::new();

            for (i, url) in urls.iter().enumerate() {
                let _ = tx.send(BackendEvent::Progress {
                    current: i as u32,
                    total: urls.len() as u32,
                    message: Some(format!("Fetching README: {}", url)),
                });

                let (owner, repo) = match Self::parse_owner_repo(url) {
                    Some(pair) => pair,
                    None => {
                        let _ = tx.send(BackendEvent::Log {
                            message: format!(
                                "[GITHUB] Skipping non-GitHub URL: {}",
                                url
                            ),
                        });
                        results.push(ExtractedContent {
                            url: url.clone(),
                            title: None,
                            markdown: String::new(),
                            success: false,
                        });
                        continue;
                    }
                };

                let api_url = format!(
                    "https://api.github.com/repos/{}/{}/readme",
                    owner, repo
                );

                let mut req = client
                    .get(&api_url)
                    .header("Accept", "application/vnd.github.raw+json")
                    .header("User-Agent", "research-cli/0.1")
                    .timeout(std::time::Duration::from_secs(self.config.timeout_secs));

                if let Some(ref token) = self.api_key() {
                    req = req.header("Authorization", format!("Bearer {}", token));
                }

                match req.send().await {
                    Ok(resp) if resp.status().is_success() => {
                        let markdown = resp.text().await.unwrap_or_default();
                        let title = format!("{}/{}", owner, repo);

                        let _ = tx.send(BackendEvent::SourceFound {
                            title: title.clone(),
                            url: url.clone(),
                            source_type: "readme".to_string(),
                        });

                        results.push(ExtractedContent {
                            url: url.clone(),
                            title: Some(title),
                            markdown,
                            success: true,
                        });
                    }
                    Ok(resp) => {
                        let status = resp.status();
                        let _ = tx.send(BackendEvent::Log {
                            message: format!(
                                "[GITHUB] README not found for {}/{}: HTTP {}",
                                owner, repo, status
                            ),
                        });
                        results.push(ExtractedContent {
                            url: url.clone(),
                            title: None,
                            markdown: String::new(),
                            success: false,
                        });
                    }
                    Err(e) => {
                        let _ = tx.send(BackendEvent::Error {
                            message: format!(
                                "Failed to fetch README for {}/{}: {}",
                                owner, repo, e
                            ),
                        });
                        results.push(ExtractedContent {
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

            let success_count = results.iter().filter(|r| r.success).count();

            let _ = tx.send(BackendEvent::Complete {
                summary: format!(
                    "Extracted {}/{} READMEs",
                    success_count,
                    results.len()
                ),
            });

            Ok(results)
        })
    }

    fn name(&self) -> &str {
        "github"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_owner_repo_standard_url() {
        let result = GitHubBackend::parse_owner_repo("https://github.com/tokio-rs/tokio");
        assert_eq!(result, Some(("tokio-rs".to_string(), "tokio".to_string())));
    }

    #[test]
    fn parse_owner_repo_with_trailing_slash() {
        let result = GitHubBackend::parse_owner_repo("https://github.com/rust-lang/rust/");
        assert_eq!(
            result,
            Some(("rust-lang".to_string(), "rust".to_string()))
        );
    }

    #[test]
    fn parse_owner_repo_with_subpath() {
        let result =
            GitHubBackend::parse_owner_repo("https://github.com/serde-rs/serde/tree/main/serde");
        assert_eq!(
            result,
            Some(("serde-rs".to_string(), "serde".to_string()))
        );
    }

    #[test]
    fn parse_owner_repo_non_github_url() {
        let result = GitHubBackend::parse_owner_repo("https://gitlab.com/foo/bar");
        assert!(result.is_none());
    }

    #[test]
    fn parse_owner_repo_missing_repo() {
        let result = GitHubBackend::parse_owner_repo("https://github.com/tokio-rs");
        assert!(result.is_none());
    }

    #[test]
    fn parse_owner_repo_empty_parts() {
        let result = GitHubBackend::parse_owner_repo("https://github.com//");
        assert!(result.is_none());
    }

    #[test]
    fn api_key_returns_none_when_no_config() {
        // Only test that config with no api_key returns None when env is absent
        // Don't manipulate GITHUB_TOKEN (it may be set in real env)
        let backend = GitHubBackend::new(BackendConfig {
            api_key: None,
            timeout_secs: 30,
        });
        // If GITHUB_TOKEN is set in env, this returns Some — that's fine
        // We're just testing the config path
        if std::env::var("GITHUB_TOKEN").is_err() {
            assert!(backend.api_key().is_none());
        }
    }

    #[test]
    fn api_key_prefers_config_over_env() {
        // Config key always wins, regardless of env
        let backend = GitHubBackend::new(BackendConfig {
            api_key: Some("config-token".to_string()),
            timeout_secs: 30,
        });
        assert_eq!(backend.api_key(), Some("config-token".to_string()));
    }

    #[test]
    fn api_key_uses_config_when_provided() {
        let backend = GitHubBackend::new(BackendConfig {
            api_key: Some("my-key-123".to_string()),
            timeout_secs: 300,
        });
        assert_eq!(backend.api_key(), Some("my-key-123".to_string()));
    }

    #[test]
    fn name_returns_github() {
        let backend = GitHubBackend::new(BackendConfig::default());
        assert_eq!(backend.name(), "github");
    }
}
