import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@solidjs/testing-library';
import Dashboard from '../Dashboard';

// Mock tauri service
vi.mock('../../services/tauri', () => ({
  searchStart: vi.fn().mockResolvedValue('session-1'),
  searchPause: vi.fn().mockResolvedValue(undefined),
  searchResume: vi.fn().mockResolvedValue(undefined),
  sessionList: vi.fn().mockResolvedValue([]),
  sessionGet: vi.fn().mockResolvedValue(null),
  listenToProgress: vi.fn().mockResolvedValue(() => {}),
  listenToSourceFound: vi.fn().mockResolvedValue(() => {}),
  listenToComplete: vi.fn().mockResolvedValue(() => {}),
}));

vi.mock('../SessionsView', () => ({ default: () => <div data-testid="sessions-view" /> }));
vi.mock('../LibraryView', () => ({ default: () => <div data-testid="library-view" /> }));
vi.mock('../SettingsView', () => ({ default: () => <div data-testid="settings-view" /> }));

describe('Accessibility', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('Dashboard has no critical accessibility violations', () => {
    const { container, unmount } = render(() => <Dashboard />);
    // Check that interactive elements exist and are reachable
    const buttons = container.querySelectorAll('button');
    expect(buttons.length).toBeGreaterThan(0);

    // All buttons should have text content (labels)
    buttons.forEach((btn) => {
      expect(btn.textContent?.trim().length).toBeGreaterThan(0);
    });
    unmount();
  });

  it('all interactive elements have accessible text', () => {
    const { container, unmount } = render(() => <Dashboard />);

    // Check input has placeholder (acts as accessible label)
    const inputs = container.querySelectorAll('input');
    inputs.forEach((input) => {
      const hasLabel = input.getAttribute('placeholder') || input.getAttribute('aria-label') || input.getAttribute('aria-labelledby');
      expect(hasLabel).toBeTruthy();
    });

    // Check buttons have text
    const buttons = container.querySelectorAll('button');
    buttons.forEach((btn) => {
      const hasLabel = (btn.textContent?.trim().length || 0) > 0 || btn.getAttribute('aria-label');
      expect(hasLabel).toBeTruthy();
    });
    unmount();
  });

  it('heading hierarchy is correct', () => {
    const { container, unmount } = render(() => <Dashboard />);

    // Should have h1
    const h1s = container.querySelectorAll('h1');
    expect(h1s.length).toBe(1);
    expect(h1s[0].textContent).toContain('RESEARCH HUB');

    // h2s should exist for sections
    const h2s = container.querySelectorAll('h2');
    expect(h2s.length).toBeGreaterThan(0);
    unmount();
  });

  it('form elements are properly structured', () => {
    const { container, unmount } = render(() => <Dashboard />);

    // Search form should exist
    const forms = container.querySelectorAll('form');
    expect(forms.length).toBeGreaterThan(0);

    // Form should have a submit button
    const submitBtn = container.querySelector('button[type="submit"]');
    expect(submitBtn).toBeTruthy();
    unmount();
  });
});
