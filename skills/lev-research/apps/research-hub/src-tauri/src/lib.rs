mod commands;
mod research;

use commands::{search_pause, search_resume, search_start, session_get, session_list};
use research::create_session_store;
use tauri::{menu::{Menu, MenuItem}, tray::TrayIconBuilder, Manager};

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Research Hub!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            // Initialize session store
            let sessions = create_session_store();
            app.manage(sessions);

            // Build tray menu
            let quit = MenuItem::with_id(app, "quit", "Quit Research Hub", true, None::<&str>)?;
            let show = MenuItem::with_id(app, "show", "Show Window", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&show, &quit])?;

            // Create system tray
            let _tray = TrayIconBuilder::new()
                .menu(&menu)
                .tooltip("Research Hub")
                .on_menu_event(|app, event| match event.id.as_ref() {
                    "quit" => {
                        app.exit(0);
                    }
                    "show" => {
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                    _ => {}
                })
                .build(app)?;

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            greet,
            search_start,
            search_pause,
            search_resume,
            session_list,
            session_get
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
