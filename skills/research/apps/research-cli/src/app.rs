//! Core application state and event loop for Research CLI

use ftui_core::event::{Event, KeyCode, KeyEvent, KeyEventKind, Modifiers};
use ftui_core::geometry::Rect;
use ftui_layout::{Constraint, Flex};
use ftui_render::frame::Frame;
use ftui_runtime::{App, Cmd, Every, Model, ScreenMode, Subscription};
use ftui_widgets::block::Block;
use ftui_widgets::borders::{BorderType, Borders};
use ftui_widgets::log_viewer::{LogViewer, LogViewerState};
use ftui_widgets::paragraph::Paragraph;
use ftui_widgets::status_line::{StatusItem, StatusLine};
use ftui_widgets::{StatefulWidget, Widget};
use std::time::Duration;
use tokio::sync::mpsc;

use crate::backends::{BackendEvent, ResearchBackend};
use crate::widgets::{CostTracker, ProgressBar, SourceList};

/// Application state machine
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResearchState {
    Idle,
    Searching,
    Extracting,
    Complete,
    Error,
}

impl ResearchState {
    pub fn as_str(&self) -> &str {
        match self {
            Self::Idle => "IDLE",
            Self::Searching => "SEARCHING",
            Self::Extracting => "EXTRACTING",
            Self::Complete => "COMPLETE",
            Self::Error => "ERROR",
        }
    }
}

/// Main research application
pub struct ResearchApp {
    pub state: ResearchState,
    pub query: String,
    pub progress: u32, // 0-100
    pub progress_total: u32,
    pub sources_found: u32,
    pub cost_usd: f64,
    pub log: LogViewer,
    pub log_state: LogViewerState,
    pub sources: Vec<String>,
    pub paused: bool,
    pub backend_rx: Option<mpsc::UnboundedReceiver<BackendEvent>>,
}

#[derive(Debug)]
pub enum Msg {
    Key(KeyEvent),
    Tick,
    BackendEvent(BackendEvent),
    Quit,
    Pause,
    Resume,
    Noop,
}

impl From<Event> for Msg {
    fn from(e: Event) -> Self {
        match e {
            Event::Key(k) => Msg::Key(k),
            _ => Msg::Noop,
        }
    }
}

impl ResearchApp {
    pub fn new(query: String) -> Self {
        let mut log = LogViewer::new(1_000);
        log.push(format!("Research query: {}", query));
        log.push("Press SPACE to pause/resume, Q to quit");
        log.push("---");

        Self {
            state: ResearchState::Idle,
            query,
            progress: 0,
            progress_total: 100,
            sources_found: 0,
            cost_usd: 0.0,
            log,
            log_state: LogViewerState::default(),
            sources: Vec::new(),
            paused: false,
            backend_rx: None,
        }
    }

    pub fn with_backend_channel(mut self, rx: mpsc::UnboundedReceiver<BackendEvent>) -> Self {
        self.backend_rx = Some(rx);
        self
    }

    pub fn start(&mut self) {
        self.state = ResearchState::Searching;
        self.log.push("[SEARCH] Starting research...");
    }

    fn handle_backend_event(&mut self, event: BackendEvent) {
        match event {
            BackendEvent::Log { message } => {
                self.log.push(message);
            }
            BackendEvent::SourceFound { title, url, source_type } => {
                self.sources_found += 1;
                let display = format!("{} - {}", title, url);
                self.sources.push(display.clone());
                self.log.push(format!("[SOURCE] {} ({})", title, source_type));
            }
            BackendEvent::Progress { current, total, message } => {
                self.progress = current;
                self.progress_total = total;
                if let Some(msg) = message {
                    self.log.push(format!("[PROGRESS] {}", msg));
                }
            }
            BackendEvent::Cost { amount_usd, backend } => {
                self.cost_usd += amount_usd;
                self.log.push(format!("[COST] {} added ${:.4}", backend, amount_usd));
            }
            BackendEvent::Status { status } => {
                self.log.push(format!("[STATUS] {}", status));
                // Update state based on status
                if status.contains("Searching") {
                    self.state = ResearchState::Searching;
                } else if status.contains("Extracting") {
                    self.state = ResearchState::Extracting;
                }
            }
            BackendEvent::Error { message } => {
                self.state = ResearchState::Error;
                self.log.push(format!("[ERROR] {}", message));
            }
            BackendEvent::Complete { summary } => {
                self.state = ResearchState::Complete;
                self.progress = self.progress_total;
                self.log.push(format!("[COMPLETE] {}", summary));
            }
        }
    }
}

impl Model for ResearchApp {
    type Message = Msg;

    fn init(&mut self) -> Cmd<Self::Message> {
        self.start();
        Cmd::None
    }

    fn update(&mut self, msg: Msg) -> Cmd<Self::Message> {
        match msg {
            Msg::Key(k) if k.kind == KeyEventKind::Press => {
                if k.modifiers.contains(Modifiers::CTRL) && k.code == KeyCode::Char('c') {
                    return Cmd::Quit;
                }
                match k.code {
                    KeyCode::Char('q') => return Cmd::Quit,
                    KeyCode::Char(' ') => {
                        self.paused = !self.paused;
                        if self.paused {
                            self.log.push("--- PAUSED ---");
                        } else {
                            self.log.push("--- RESUMED ---");
                        }
                    }
                    KeyCode::PageUp => self.log.page_up(&self.log_state),
                    KeyCode::PageDown => self.log.page_down(&self.log_state),
                    _ => {}
                }
            }
            Msg::BackendEvent(event) => {
                self.handle_backend_event(event);
            }
            Msg::Tick if !self.paused => {
                // Poll backend events from channel
                let events: Vec<_> = if let Some(rx) = &mut self.backend_rx {
                    let mut evts = Vec::new();
                    while let Ok(event) = rx.try_recv() {
                        evts.push(event);
                    }
                    evts
                } else {
                    vec![]
                };
                for event in events {
                    self.handle_backend_event(event);
                }
            }
            Msg::Quit => return Cmd::Quit,
            _ => {}
        }
        Cmd::None
    }

    fn view(&self, frame: &mut Frame) {
        let area = Rect::from_size(frame.buffer.width(), frame.buffer.height());

        // Layout: Status bar (1) | Main content (remaining)
        let chunks = Flex::vertical()
            .constraints([Constraint::Fixed(1), Constraint::Min(5)])
            .split(area);

        // Status bar
        let status_text = self.state.as_str();
        let progress_text = format!("{}%", self.progress);

        let status = StatusLine::new()
            .left(StatusItem::text(status_text))
            .center(StatusItem::progress(self.progress as u64, self.progress_total as u64))
            .right(StatusItem::key_hint("SPACE", "Pause"))
            .right(StatusItem::key_hint("Q", "Quit"));

        status.render(chunks[0], frame);

        // Main content: Split into 3 columns
        let main_chunks = Flex::horizontal()
            .constraints([
                Constraint::Percentage(60.0), // Log viewer
                Constraint::Percentage(20.0), // Sources
                Constraint::Percentage(20.0), // Cost & progress
            ])
            .split(chunks[1]);

        // Log viewer
        let log_block = Block::new()
            .title(" Research Log ")
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded);

        let log_inner = log_block.inner(main_chunks[0]);
        log_block.render(main_chunks[0], frame);

        let mut log_state = self.log_state.clone();
        self.log.render(log_inner, frame, &mut log_state);

        // Sources list
        let sources_block = Block::new()
            .title(" Sources ")
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded);

        let sources_inner = sources_block.inner(main_chunks[1]);
        sources_block.render(main_chunks[1], frame);

        let source_list = SourceList::new(&self.sources);
        source_list.render(sources_inner, frame);

        // Cost tracker & progress bar
        let right_chunks = Flex::vertical()
            .constraints([Constraint::Percentage(50.0), Constraint::Percentage(50.0)])
            .split(main_chunks[2]);

        // Progress bar
        let progress_block = Block::new()
            .title(" Progress ")
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded);

        let progress_inner = progress_block.inner(right_chunks[0]);
        progress_block.render(right_chunks[0], frame);

        let progress_bar = ProgressBar::new(self.progress, self.progress_total);
        progress_bar.render(progress_inner, frame);

        // Cost tracker
        let cost_block = Block::new()
            .title(" Cost ")
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded);

        let cost_inner = cost_block.inner(right_chunks[1]);
        cost_block.render(right_chunks[1], frame);

        let cost_tracker = CostTracker::new(self.cost_usd);
        cost_tracker.render(cost_inner, frame);
    }

    fn subscriptions(&self) -> Vec<Box<dyn Subscription<Self::Message>>> {
        // Update at 10 ticks per second (100ms interval)
        vec![Box::new(Every::new(Duration::from_millis(100), || {
            Msg::Tick
        }))]
    }
}

/// Run the research app with a configured app instance
pub fn run(app: ResearchApp, fullscreen: bool) -> std::io::Result<()> {
    let mode = if fullscreen {
        ScreenMode::AltScreen
    } else {
        ScreenMode::Inline { ui_height: 20 }
    };

    App::new(app)
        .screen_mode(mode)
        .run()
}
