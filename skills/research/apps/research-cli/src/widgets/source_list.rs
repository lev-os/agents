//! Source list widget for displaying discovered research sources

use ftui_core::geometry::Rect;
use ftui_render::cell::PackedRgba;
use ftui_render::frame::Frame;
use ftui_style::Style;
use ftui_widgets::paragraph::Paragraph;
use ftui_widgets::Widget;

/// Simple source list widget
pub struct SourceList<'a> {
    sources: &'a [String],
}

impl<'a> SourceList<'a> {
    pub fn new(sources: &'a [String]) -> Self {
        Self { sources }
    }
}

impl<'a> Widget for SourceList<'a> {
    fn render(&self, area: Rect, frame: &mut Frame) {
        if area.height == 0 || area.width == 0 {
            return;
        }

        // Display sources, one per line, up to area height
        let max_sources = (area.height as usize).saturating_sub(1);
        let visible_sources = self.sources.iter().take(max_sources);

        let mut y = 0;
        for (idx, source) in visible_sources.enumerate() {
            if y >= area.height {
                break;
            }

            // Truncate source text to fit width
            let max_width = area.width as usize;
            let display_text = if source.len() > max_width {
                format!("{}...", &source[..max_width.saturating_sub(3)])
            } else {
                source.clone()
            };

            let source_rect = Rect::new(area.x, area.y + y, area.width, 1);
            let style = Style::new().fg(PackedRgba::rgb(0, 255, 255)); // Cyan
            let para = Paragraph::new(format!("• {}", display_text)).style(style);
            para.render(source_rect, frame);

            y += 1;
        }

        // Show count if there are more sources
        if self.sources.len() > max_sources {
            let remaining = self.sources.len() - max_sources;
            let footer_rect = Rect::new(
                area.x,
                area.y + area.height.saturating_sub(1),
                area.width,
                1,
            );
            let style = Style::new().fg(PackedRgba::rgb(128, 128, 128)); // BrightBlack/Gray
            let para = Paragraph::new(format!("...and {} more", remaining)).style(style);
            para.render(footer_rect, frame);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_source_list_empty() {
        let sources: Vec<String> = vec![];
        let list = SourceList::new(&sources);
        assert_eq!(list.sources.len(), 0);
    }

    #[test]
    fn test_source_list_multiple() {
        let sources = vec![
            "Source 1".to_string(),
            "Source 2".to_string(),
            "Source 3".to_string(),
        ];
        let list = SourceList::new(&sources);
        assert_eq!(list.sources.len(), 3);
    }
}
