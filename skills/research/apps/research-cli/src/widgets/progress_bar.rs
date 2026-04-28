//! Progress bar widget for research progress display

use ftui_core::geometry::Rect;
use ftui_render::cell::PackedRgba;
use ftui_render::frame::Frame;
use ftui_style::Style;
use ftui_widgets::paragraph::Paragraph;
use ftui_widgets::Widget;

/// Simple progress bar widget
pub struct ProgressBar {
    current: u32,
    total: u32,
}

impl ProgressBar {
    pub fn new(current: u32, total: u32) -> Self {
        Self { current, total }
    }

    fn render_bar(&self, width: usize) -> String {
        let percentage = if self.total > 0 {
            (self.current as f64 / self.total as f64 * 100.0) as u32
        } else {
            0
        };

        let filled = ((width as f64 * self.current as f64) / self.total as f64) as usize;
        let empty = width.saturating_sub(filled);

        let bar = format!(
            "[{}{}] {}%",
            "█".repeat(filled),
            "░".repeat(empty),
            percentage
        );

        bar
    }
}

impl Widget for ProgressBar {
    fn render(&self, area: Rect, frame: &mut Frame) {
        if area.height == 0 || area.width < 10 {
            return;
        }

        // Use most of the width for the bar, leaving 8 chars for percentage display
        let bar_width = area.width.saturating_sub(8) as usize;
        let bar_text = self.render_bar(bar_width);

        // Style based on progress
        let style = if self.current >= self.total {
            Style::new().fg(PackedRgba::rgb(0, 255, 0)) // Green
        } else {
            Style::new().fg(PackedRgba::rgb(0, 255, 255)) // Cyan
        };

        let paragraph = Paragraph::new(bar_text).style(style);
        paragraph.render(area, frame);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_progress_bar_render() {
        let bar = ProgressBar::new(50, 100);
        let text = bar.render_bar(20);
        assert!(text.contains("50%"));
        assert!(text.contains("█"));
        assert!(text.contains("░"));
    }

    #[test]
    fn test_progress_bar_zero() {
        let bar = ProgressBar::new(0, 100);
        let text = bar.render_bar(20);
        assert!(text.contains("0%"));
    }

    #[test]
    fn test_progress_bar_complete() {
        let bar = ProgressBar::new(100, 100);
        let text = bar.render_bar(20);
        assert!(text.contains("100%"));
    }
}
