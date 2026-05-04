//! Cost tracker widget for API cost display

use ftui_core::geometry::Rect;
use ftui_render::cell::PackedRgba;
use ftui_render::frame::Frame;
use ftui_style::Style;
use ftui_widgets::paragraph::Paragraph;
use ftui_widgets::Widget;

/// Simple cost tracker widget
pub struct CostTracker {
    cost_usd: f64,
}

impl CostTracker {
    pub fn new(cost_usd: f64) -> Self {
        Self { cost_usd }
    }

    fn format_cost(&self) -> String {
        format!("${:.4}", self.cost_usd)
    }

    fn get_color(&self) -> PackedRgba {
        if self.cost_usd < 0.01 {
            PackedRgba::rgb(0, 255, 0) // Green
        } else if self.cost_usd < 0.10 {
            PackedRgba::rgb(255, 255, 0) // Yellow
        } else {
            PackedRgba::rgb(255, 0, 0) // Red
        }
    }
}

impl Widget for CostTracker {
    fn render(&self, area: Rect, frame: &mut Frame) {
        if area.height == 0 || area.width == 0 {
            return;
        }

        let cost_text = self.format_cost();
        let style = Style::new().fg(self.get_color());

        // First line: Label
        if area.height >= 1 {
            let label_rect = Rect::new(area.x, area.y, area.width, 1);
            let label = Paragraph::new("API Cost:");
            label.render(label_rect, frame);
        }

        // Second line: Cost value
        if area.height >= 2 {
            let cost_rect = Rect::new(area.x, area.y + 1, area.width, 1);
            let cost_para = Paragraph::new(cost_text).style(style);
            cost_para.render(cost_rect, frame);
        }

        // Third line: Estimate
        if area.height >= 4 {
            let estimate = format!("Est: ${:.2}/hr", self.cost_usd * 60.0);
            let estimate_rect = Rect::new(area.x, area.y + 3, area.width, 1);
            let estimate_para =
                Paragraph::new(estimate).style(Style::new().fg(PackedRgba::rgb(128, 128, 128))); // Gray
            estimate_para.render(estimate_rect, frame);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cost_format() {
        let tracker = CostTracker::new(0.0123);
        assert_eq!(tracker.format_cost(), "$0.0123");
    }

    #[test]
    fn test_cost_color_green() {
        let tracker = CostTracker::new(0.005);
        assert_eq!(tracker.get_color(), PackedRgba::rgb(0, 255, 0));
    }

    #[test]
    fn test_cost_color_yellow() {
        let tracker = CostTracker::new(0.05);
        assert_eq!(tracker.get_color(), PackedRgba::rgb(255, 255, 0));
    }

    #[test]
    fn test_cost_color_red() {
        let tracker = CostTracker::new(0.15);
        assert_eq!(tracker.get_color(), PackedRgba::rgb(255, 0, 0));
    }
}
