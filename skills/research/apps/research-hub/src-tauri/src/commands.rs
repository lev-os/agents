use crate::research::*;
use tauri::{AppHandle, Emitter, State};
use std::sync::Arc;

#[tauri::command]
pub async fn search_start(
    query: String,
    mode: String,
    sessions: State<'_, SessionStore>,
    app: AppHandle,
) -> Result<String, String> {
    // Create new session
    let session = Session::new(query.clone(), mode.clone());
    let session_id = session.id.clone();

    // Store session
    {
        let mut store = sessions.lock().map_err(|e| e.to_string())?;
        store.insert(session_id.clone(), session.clone());
    }

    // Spawn background task for research
    let sessions_clone = Arc::clone(&sessions);
    let app_clone = app.clone();
    let session_id_clone = session_id.clone();
    let query_clone = query.clone();
    let mode_clone = mode.clone();

    tokio::spawn(async move {
        if let Err(e) = run_research_task(
            session_id_clone,
            query_clone,
            mode_clone,
            sessions_clone,
            app_clone,
        )
        .await
        {
            eprintln!("Research task error: {}", e);
        }
    });

    Ok(session_id)
}

#[tauri::command]
pub async fn search_pause(
    session_id: String,
    sessions: State<'_, SessionStore>,
) -> Result<(), String> {
    let mut store = sessions.lock().map_err(|e| e.to_string())?;

    if let Some(session) = store.get_mut(&session_id) {
        session.pause();
        Ok(())
    } else {
        Err(format!("Session {} not found", session_id))
    }
}

#[tauri::command]
pub async fn search_resume(
    session_id: String,
    sessions: State<'_, SessionStore>,
    app: AppHandle,
) -> Result<(), String> {
    // Resume session status
    {
        let mut store = sessions.lock().map_err(|e| e.to_string())?;
        if let Some(session) = store.get_mut(&session_id) {
            session.resume();
        } else {
            return Err(format!("Session {} not found", session_id));
        }
    }

    // Restart research task
    let sessions_clone = Arc::clone(&sessions);
    let app_clone = app.clone();
    let session_id_clone = session_id.clone();

    tokio::spawn(async move {
        // Get session details for resumption
        let (query, mode) = {
            let store = sessions_clone.lock().unwrap();
            if let Some(session) = store.get(&session_id_clone) {
                (session.query.clone(), session.mode.clone())
            } else {
                return;
            }
        };

        if let Err(e) = run_research_task(
            session_id_clone,
            query,
            mode,
            sessions_clone,
            app_clone,
        )
        .await
        {
            eprintln!("Research task error on resume: {}", e);
        }
    });

    Ok(())
}

#[tauri::command]
pub async fn session_list(sessions: State<'_, SessionStore>) -> Result<Vec<Session>, String> {
    let store = sessions.lock().map_err(|e| e.to_string())?;
    let session_list: Vec<Session> = store.values().cloned().collect();
    Ok(session_list)
}

#[tauri::command]
pub async fn session_get(
    session_id: String,
    sessions: State<'_, SessionStore>,
) -> Result<Session, String> {
    let store = sessions.lock().map_err(|e| e.to_string())?;

    store
        .get(&session_id)
        .cloned()
        .ok_or_else(|| format!("Session {} not found", session_id))
}

// Background research task
async fn run_research_task(
    session_id: String,
    query: String,
    mode: String,
    sessions: SessionStore,
    app: AppHandle,
) -> anyhow::Result<()> {
    let max_turns = match mode.as_str() {
        "quick" => 2,
        "deep" => 5,
        "full" => 10,
        _ => 2,
    };

    for turn_num in 1..=max_turns {
        // Check if session is paused
        {
            let store = sessions.lock().unwrap();
            if let Some(session) = store.get(&session_id) {
                if session.status == "paused" {
                    break;
                }
            }
        }

        // Run search with real CLIs (graceful fallback to mock)
        let sources = run_search(&query, &mode).await;

        // Add sources to session and emit events
        {
            let mut store = sessions.lock().unwrap();
            if let Some(session) = store.get_mut(&session_id) {
                for source in &sources {
                    session.add_source(source.clone());

                    // Emit source found event
                    let payload = SourcePayload {
                        session_id: session_id.clone(),
                        source: source.clone(),
                    };
                    let _ = app.emit("research:source_found", payload);
                }
            }
        }

        // Simulate turn completion
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;

        let turn = Turn {
            number: turn_num,
            query: query.clone(),
            confidence: (turn_num as f32 / max_turns as f32) * 100.0,
            sources_count: sources.len() as u32,
            cost: 0.01 + (turn_num as f32 * 0.005),
            duration: turn_num as f32 * 2.0,
            completed_at: chrono::Utc::now(),
        };

        // Add turn to session
        {
            let mut store = sessions.lock().unwrap();
            if let Some(session) = store.get_mut(&session_id) {
                session.add_turn(turn.clone());

                // Emit progress event
                let payload = ProgressPayload {
                    session_id: session_id.clone(),
                    turn: turn_num,
                    max_turns,
                    confidence: session.confidence,
                    sources: session.sources.len() as u32,
                    cost: session.cost,
                    duration: turn.duration,
                    status: session.status.clone(),
                };
                let _ = app.emit("research:progress", payload);
            }
        }
    }

    // Complete session
    {
        let mut store = sessions.lock().unwrap();
        if let Some(session) = store.get_mut(&session_id) {
            session.complete();

            // Emit completion event
            let payload = ResultPayload {
                session_id: session_id.clone(),
                session: session.clone(),
            };
            let _ = app.emit("research:complete", payload);
        }
    }

    Ok(())
}
