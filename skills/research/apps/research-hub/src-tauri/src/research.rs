use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use tokio::process::Command;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Source {
    pub id: String,
    pub url: String,
    pub title: String,
    #[serde(rename = "type")]
    pub source_type: String,
    pub relevance: f32,
    pub snippet: Option<String>,
    #[serde(rename = "discoveredAt")]
    pub discovered_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Turn {
    pub number: u32,
    pub query: String,
    pub confidence: f32,
    #[serde(rename = "sourcesCount")]
    pub sources_count: u32,
    pub cost: f32,
    pub duration: f32,
    #[serde(rename = "completedAt")]
    pub completed_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Session {
    pub id: String,
    pub query: String,
    pub mode: String,
    pub status: String,
    #[serde(rename = "createdAt")]
    pub created_at: DateTime<Utc>,
    #[serde(rename = "pausedAt")]
    pub paused_at: Option<DateTime<Utc>>,
    #[serde(rename = "completedAt")]
    pub completed_at: Option<DateTime<Utc>>,
    pub turns: Vec<Turn>,
    pub sources: Vec<Source>,
    pub cost: f32,
    pub confidence: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProgressPayload {
    #[serde(rename = "sessionId")]
    pub session_id: String,
    pub turn: u32,
    #[serde(rename = "maxTurns")]
    pub max_turns: u32,
    pub confidence: f32,
    pub sources: u32,
    pub cost: f32,
    pub duration: f32,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SourcePayload {
    #[serde(rename = "sessionId")]
    pub session_id: String,
    pub source: Source,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResultPayload {
    #[serde(rename = "sessionId")]
    pub session_id: String,
    pub session: Session,
}

pub type SessionStore = Arc<Mutex<HashMap<String, Session>>>;

pub fn create_session_store() -> SessionStore {
    Arc::new(Mutex::new(HashMap::new()))
}

impl Session {
    pub fn new(query: String, mode: String) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            query,
            mode,
            status: "searching".to_string(),
            created_at: Utc::now(),
            paused_at: None,
            completed_at: None,
            turns: Vec::new(),
            sources: Vec::new(),
            cost: 0.0,
            confidence: 0.0,
        }
    }

    pub fn pause(&mut self) {
        self.status = "paused".to_string();
        self.paused_at = Some(Utc::now());
    }

    pub fn resume(&mut self) {
        self.status = "searching".to_string();
        self.paused_at = None;
    }

    pub fn complete(&mut self) {
        self.status = "complete".to_string();
        self.completed_at = Some(Utc::now());
    }

    pub fn add_source(&mut self, source: Source) {
        if !self.sources.iter().any(|s| s.id == source.id) {
            self.sources.push(source);
        }
    }

    pub fn add_turn(&mut self, turn: Turn) {
        self.cost += turn.cost;
        self.confidence = turn.confidence;
        self.turns.push(turn);
    }
}

// Result types for CLI parsing
#[derive(Debug, Deserialize)]
struct BraveResult {
    title: Option<String>,
    url: Option<String>,
    description: Option<String>,
}

#[derive(Debug, Deserialize)]
struct ValyuResult {
    title: Option<String>,
    url: Option<String>,
    snippet: Option<String>,
    relevance: Option<f32>,
    #[serde(rename = "type")]
    source_type: Option<String>,
}

// Check if a CLI tool is available
async fn cli_available(cmd: &str) -> bool {
    Command::new("which")
        .arg(cmd)
        .output()
        .await
        .map(|o| o.status.success())
        .unwrap_or(false)
}

// Try Brave Search CLI
async fn try_brave_search(query: &str) -> anyhow::Result<Vec<Source>> {
    if !cli_available("brave-search").await {
        anyhow::bail!("brave-search CLI not found");
    }

    let output = Command::new("brave-search")
        .arg(query)
        .arg("--json")
        .output()
        .await?;

    if !output.status.success() {
        let error = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("Brave search failed: {}", error);
    }

    let stdout = String::from_utf8_lossy(&output.stdout);
    let results: Vec<BraveResult> = serde_json::from_str(&stdout)
        .unwrap_or_default();

    let sources = results
        .into_iter()
        .filter_map(|r| {
            Some(Source {
                id: Uuid::new_v4().to_string(),
                url: r.url?,
                title: r.title.unwrap_or_else(|| "Untitled".to_string()),
                source_type: "web".to_string(),
                relevance: 0.85,
                snippet: r.description,
                discovered_at: Utc::now(),
            })
        })
        .take(10)
        .collect();

    Ok(sources)
}

// Try Valyu CLI
async fn try_valyu_search(query: &str) -> anyhow::Result<Vec<Source>> {
    if !cli_available("valyu").await {
        anyhow::bail!("valyu CLI not found");
    }

    let output = Command::new("valyu")
        .arg("search")
        .arg(query)
        .arg("--json")
        .output()
        .await?;

    if !output.status.success() {
        let error = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("Valyu search failed: {}", error);
    }

    let stdout = String::from_utf8_lossy(&output.stdout);
    let results: Vec<ValyuResult> = serde_json::from_str(&stdout)
        .unwrap_or_default();

    let sources = results
        .into_iter()
        .filter_map(|r| {
            Some(Source {
                id: Uuid::new_v4().to_string(),
                url: r.url?,
                title: r.title.unwrap_or_else(|| "Untitled".to_string()),
                source_type: r.source_type.unwrap_or_else(|| "web".to_string()),
                relevance: r.relevance.unwrap_or(0.8),
                snippet: r.snippet,
                discovered_at: Utc::now(),
            })
        })
        .take(10)
        .collect();

    Ok(sources)
}

// Try Firecrawl CLI for deep scraping
#[allow(dead_code)]
async fn try_firecrawl_scrape(url: &str) -> anyhow::Result<String> {
    if !cli_available("firecrawl").await {
        anyhow::bail!("firecrawl CLI not found");
    }

    let output = Command::new("firecrawl")
        .arg("scrape")
        .arg(url)
        .output()
        .await?;

    if !output.status.success() {
        let error = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("Firecrawl scrape failed: {}", error);
    }

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

// Mock search for fallback when CLIs aren't available
async fn run_mock_search(query: &str) -> Vec<Source> {
    // Simulate search delay
    tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;

    vec![
        Source {
            id: Uuid::new_v4().to_string(),
            url: format!("https://example.com/search?q={}", urlencoding::encode(query)),
            title: format!("Result for \"{}\"", query),
            source_type: "web".to_string(),
            relevance: 0.95,
            snippet: Some(format!("Mock search result for query: {} (real CLIs not installed)", query)),
            discovered_at: Utc::now(),
        },
        Source {
            id: Uuid::new_v4().to_string(),
            url: format!("https://academic.example.com/paper?q={}", urlencoding::encode(query)),
            title: format!("Academic Paper: {}", query),
            source_type: "academic".to_string(),
            relevance: 0.87,
            snippet: Some(format!("Academic research on {} (mock)", query)),
            discovered_at: Utc::now(),
        },
    ]
}

/// Smart search function - tries real CLIs with graceful fallback to mock
/// Mode affects which CLI is tried first:
/// - quick: brave-search only
/// - deep: valyu (recursive)
/// - full: valyu with deep extraction
pub async fn run_search(query: &str, mode: &str) -> Vec<Source> {
    let result = match mode {
        "quick" => {
            // Quick mode: try brave-search first, then valyu, then mock
            try_brave_search(query)
                .await
                .or_else(|_| futures::executor::block_on(try_valyu_search(query)))
                .ok()
        }
        "deep" | "full" => {
            // Deep/Full mode: try valyu first (recursive search), then brave, then mock
            try_valyu_search(query)
                .await
                .or_else(|_| futures::executor::block_on(try_brave_search(query)))
                .ok()
        }
        _ => None,
    };

    // Return real results or fall back to mock
    match result {
        Some(sources) if !sources.is_empty() => sources,
        _ => {
            eprintln!("No CLI tools available, using mock search");
            run_mock_search(query).await
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // --- SessionStore tests ---

    #[test]
    fn session_store_creates_empty() {
        let store = create_session_store();
        let locked = store.lock().unwrap();
        assert!(locked.is_empty());
    }

    #[test]
    fn session_store_is_arc_cloneable() {
        let store = create_session_store();
        let clone = store.clone();
        {
            let mut locked = store.lock().unwrap();
            locked.insert(
                "s1".to_string(),
                Session::new("test".to_string(), "quick".to_string()),
            );
        }
        let locked = clone.lock().unwrap();
        assert_eq!(locked.len(), 1, "Clone should see the same data");
    }

    #[test]
    fn session_store_insert_and_retrieve() {
        let store = create_session_store();
        let session = Session::new("query".to_string(), "deep".to_string());
        let id = session.id.clone();
        store.lock().unwrap().insert(id.clone(), session);

        let locked = store.lock().unwrap();
        assert_eq!(locked.len(), 1);
        assert!(locked.contains_key(&id));
        assert_eq!(locked.get(&id).unwrap().query, "query");
    }

    #[test]
    fn session_store_multiple_sessions() {
        let store = create_session_store();
        for i in 0..5 {
            let session = Session::new(format!("query {}", i), "quick".to_string());
            let id = session.id.clone();
            store.lock().unwrap().insert(id, session);
        }
        assert_eq!(store.lock().unwrap().len(), 5);
    }

    // --- Session::new tests ---

    #[test]
    fn session_new_has_valid_uuid() {
        let session = Session::new("test query".to_string(), "quick".to_string());
        assert!(!session.id.is_empty());
        // UUID v4 format: 8-4-4-4-12 hex chars
        assert_eq!(session.id.len(), 36);
        assert_eq!(session.id.chars().filter(|c| *c == '-').count(), 4);
    }

    #[test]
    fn session_new_initial_state() {
        let session = Session::new("test query".to_string(), "quick".to_string());
        assert_eq!(session.query, "test query");
        assert_eq!(session.mode, "quick");
        assert_eq!(session.status, "searching");
        assert!(session.turns.is_empty());
        assert!(session.sources.is_empty());
        assert_eq!(session.cost, 0.0);
        assert_eq!(session.confidence, 0.0);
        assert!(session.paused_at.is_none());
        assert!(session.completed_at.is_none());
    }

    #[test]
    fn session_new_unique_ids() {
        let s1 = Session::new("q1".to_string(), "quick".to_string());
        let s2 = Session::new("q2".to_string(), "deep".to_string());
        assert_ne!(s1.id, s2.id, "Different sessions must have unique IDs");
    }

    #[test]
    fn session_new_created_at_set() {
        let before = Utc::now();
        let session = Session::new("test".to_string(), "quick".to_string());
        let after = Utc::now();
        assert!(session.created_at >= before);
        assert!(session.created_at <= after);
    }

    // --- Session status transitions ---

    #[test]
    fn session_pause_sets_status_and_timestamp() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        assert_eq!(session.status, "searching");

        session.pause();
        assert_eq!(session.status, "paused");
        assert!(session.paused_at.is_some());
    }

    #[test]
    fn session_resume_clears_paused() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        session.pause();
        assert!(session.paused_at.is_some());

        session.resume();
        assert_eq!(session.status, "searching");
        assert!(session.paused_at.is_none());
    }

    #[test]
    fn session_complete_sets_status_and_timestamp() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        session.complete();
        assert_eq!(session.status, "complete");
        assert!(session.completed_at.is_some());
    }

    #[test]
    fn session_full_lifecycle() {
        let mut session = Session::new("test".to_string(), "deep".to_string());
        assert_eq!(session.status, "searching");

        session.pause();
        assert_eq!(session.status, "paused");

        session.resume();
        assert_eq!(session.status, "searching");

        session.complete();
        assert_eq!(session.status, "complete");
        assert!(session.completed_at.is_some());
    }

    #[test]
    fn session_pause_resume_cycle() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        for _ in 0..3 {
            session.pause();
            assert_eq!(session.status, "paused");
            assert!(session.paused_at.is_some());

            session.resume();
            assert_eq!(session.status, "searching");
            assert!(session.paused_at.is_none());
        }
    }

    // --- Session::add_source tests ---

    #[test]
    fn session_add_source_basic() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        let source = Source {
            id: "src-1".to_string(),
            url: "https://example.com".to_string(),
            title: "Test".to_string(),
            source_type: "web".to_string(),
            relevance: 0.9,
            snippet: None,
            discovered_at: Utc::now(),
        };

        session.add_source(source);
        assert_eq!(session.sources.len(), 1);
        assert_eq!(session.sources[0].id, "src-1");
    }

    #[test]
    fn session_add_source_deduplicates_by_id() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        let source = Source {
            id: "src-1".to_string(),
            url: "https://example.com".to_string(),
            title: "Test".to_string(),
            source_type: "web".to_string(),
            relevance: 0.9,
            snippet: None,
            discovered_at: Utc::now(),
        };

        session.add_source(source.clone());
        session.add_source(source.clone());
        session.add_source(source);
        assert_eq!(session.sources.len(), 1, "Duplicate sources should be rejected");
    }

    #[test]
    fn session_add_source_different_ids_accepted() {
        let mut session = Session::new("test".to_string(), "quick".to_string());

        for i in 0..5 {
            let source = Source {
                id: format!("src-{}", i),
                url: format!("https://example.com/{}", i),
                title: format!("Source {}", i),
                source_type: "web".to_string(),
                relevance: 0.8,
                snippet: Some(format!("snippet {}", i)),
                discovered_at: Utc::now(),
            };
            session.add_source(source);
        }
        assert_eq!(session.sources.len(), 5);
    }

    // --- Session::add_turn tests ---

    #[test]
    fn session_add_turn_accumulates_cost() {
        let mut session = Session::new("test".to_string(), "deep".to_string());

        let turn1 = Turn {
            number: 1,
            query: "sub-query 1".to_string(),
            confidence: 0.6,
            sources_count: 5,
            cost: 0.10,
            duration: 2.5,
            completed_at: Utc::now(),
        };
        session.add_turn(turn1);
        assert!((session.cost - 0.10).abs() < 0.001);
        assert_eq!(session.confidence, 0.6);

        let turn2 = Turn {
            number: 2,
            query: "sub-query 2".to_string(),
            confidence: 0.85,
            sources_count: 8,
            cost: 0.15,
            duration: 3.0,
            completed_at: Utc::now(),
        };
        session.add_turn(turn2);
        assert!((session.cost - 0.25).abs() < 0.001);
        assert_eq!(session.confidence, 0.85);
        assert_eq!(session.turns.len(), 2);
    }

    #[test]
    fn session_add_turn_confidence_uses_latest() {
        let mut session = Session::new("test".to_string(), "quick".to_string());

        for i in 1..=5 {
            let turn = Turn {
                number: i,
                query: format!("query {}", i),
                confidence: i as f32 * 0.2,
                sources_count: i * 2,
                cost: 0.01,
                duration: 1.0,
                completed_at: Utc::now(),
            };
            session.add_turn(turn);
        }

        // Confidence should be the last turn's value (5 * 0.2 = 1.0)
        assert!((session.confidence - 1.0).abs() < 0.001);
        assert_eq!(session.turns.len(), 5);
        assert!((session.cost - 0.05).abs() < 0.001);
    }

    #[test]
    fn session_add_turn_zero_cost() {
        let mut session = Session::new("test".to_string(), "quick".to_string());
        let turn = Turn {
            number: 1,
            query: "free query".to_string(),
            confidence: 0.5,
            sources_count: 3,
            cost: 0.0,
            duration: 1.0,
            completed_at: Utc::now(),
        };
        session.add_turn(turn);
        assert_eq!(session.cost, 0.0);
    }

    // --- Serialization tests ---

    #[test]
    fn session_serialization_roundtrip() {
        let mut session = Session::new("rust concurrency".to_string(), "deep".to_string());
        session.add_source(Source {
            id: "s1".to_string(),
            url: "https://example.com".to_string(),
            title: "Test".to_string(),
            source_type: "web".to_string(),
            relevance: 0.9,
            snippet: Some("snippet".to_string()),
            discovered_at: Utc::now(),
        });

        let json = serde_json::to_string(&session).unwrap();
        let deserialized: Session = serde_json::from_str(&json).unwrap();

        assert_eq!(deserialized.id, session.id);
        assert_eq!(deserialized.query, "rust concurrency");
        assert_eq!(deserialized.mode, "deep");
        assert_eq!(deserialized.status, "searching");
        assert_eq!(deserialized.sources.len(), 1);
    }

    #[test]
    fn source_serialization_has_camelcase_fields() {
        let source = Source {
            id: "s1".to_string(),
            url: "https://example.com".to_string(),
            title: "Test".to_string(),
            source_type: "web".to_string(),
            relevance: 0.9,
            snippet: None,
            discovered_at: Utc::now(),
        };

        let json = serde_json::to_string(&source).unwrap();
        assert!(json.contains("\"discoveredAt\""), "Should use camelCase: {}", json);
        assert!(json.contains("\"type\""), "source_type should serialize as 'type': {}", json);
    }

    #[test]
    fn turn_serialization_has_camelcase_fields() {
        let turn = Turn {
            number: 1,
            query: "test".to_string(),
            confidence: 0.7,
            sources_count: 5,
            cost: 0.01,
            duration: 2.0,
            completed_at: Utc::now(),
        };

        let json = serde_json::to_string(&turn).unwrap();
        assert!(json.contains("\"sourcesCount\""), "Should use camelCase: {}", json);
        assert!(json.contains("\"completedAt\""), "Should use camelCase: {}", json);
    }

    #[test]
    fn progress_payload_serialization() {
        let payload = ProgressPayload {
            session_id: "abc-123".to_string(),
            turn: 2,
            max_turns: 5,
            confidence: 0.65,
            sources: 8,
            cost: 0.05,
            duration: 4.2,
            status: "searching".to_string(),
        };

        let json = serde_json::to_string(&payload).unwrap();
        assert!(json.contains("\"sessionId\""), "Should use camelCase: {}", json);
        assert!(json.contains("\"maxTurns\""), "Should use camelCase: {}", json);
        let deserialized: ProgressPayload = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.session_id, "abc-123");
        assert_eq!(deserialized.turn, 2);
    }

    #[test]
    fn source_payload_serialization() {
        let payload = SourcePayload {
            session_id: "xyz-789".to_string(),
            source: Source {
                id: "s1".to_string(),
                url: "https://example.com".to_string(),
                title: "Title".to_string(),
                source_type: "web".to_string(),
                relevance: 0.88,
                snippet: None,
                discovered_at: Utc::now(),
            },
        };

        let json = serde_json::to_string(&payload).unwrap();
        assert!(json.contains("\"sessionId\""), "Should use camelCase: {}", json);
        let deserialized: SourcePayload = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.session_id, "xyz-789");
        assert_eq!(deserialized.source.id, "s1");
    }

    // --- Mock search tests ---

    #[tokio::test]
    async fn run_mock_search_returns_2_sources() {
        let sources = run_mock_search("test query").await;
        assert_eq!(sources.len(), 2);
    }

    #[tokio::test]
    async fn run_mock_search_contains_query_in_urls() {
        let sources = run_mock_search("rust async").await;
        for source in &sources {
            assert!(
                source.url.contains("rust"),
                "URL '{}' should contain the query term",
                source.url
            );
        }
    }

    #[tokio::test]
    async fn run_mock_search_has_web_and_academic() {
        let sources = run_mock_search("test").await;
        let types: Vec<&str> = sources.iter().map(|s| s.source_type.as_str()).collect();
        assert!(types.contains(&"web"));
        assert!(types.contains(&"academic"));
    }

    #[tokio::test]
    async fn run_mock_search_sources_have_unique_ids() {
        let sources = run_mock_search("test").await;
        let ids: Vec<&str> = sources.iter().map(|s| s.id.as_str()).collect();
        for i in 0..ids.len() {
            for j in (i + 1)..ids.len() {
                assert_ne!(ids[i], ids[j], "Source IDs should be unique");
            }
        }
    }

    #[tokio::test]
    async fn run_mock_search_sources_have_snippets() {
        let sources = run_mock_search("deep learning").await;
        for source in &sources {
            assert!(source.snippet.is_some(), "Mock sources should have snippets");
        }
    }

    // --- run_search fallback behavior ---

    #[tokio::test]
    async fn run_search_unknown_mode_falls_back_to_mock() {
        // An unknown mode should produce results (via mock fallback)
        let sources = run_search("test", "unknown_mode").await;
        assert!(!sources.is_empty(), "Should fall back to mock for unknown mode");
    }

    #[tokio::test]
    async fn run_search_quick_mode_returns_results() {
        // On CI/test where CLIs are not installed, this falls back to mock
        let sources = run_search("test query", "quick").await;
        assert!(!sources.is_empty(), "Quick mode should return results (real or mock)");
    }
}
