import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@solidjs/testing-library';
import Dashboard from '../Dashboard';

// Mock the tauri service — all async functions resolve to safe defaults,
// event listeners return a no-op unlisten function.
// Note: vi.mock factories are hoisted, so we cannot reference outer variables.
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

// Mock child view components that Dashboard imports (they don't exist yet)
vi.mock('../SessionsView', () => ({ default: () => <div data-testid="sessions-view" /> }));
vi.mock('../LibraryView', () => ({ default: () => <div data-testid="library-view" /> }));
vi.mock('../SettingsView', () => ({ default: () => <div data-testid="settings-view" /> }));

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders without crashing', () => {
    const { unmount } = render(() => <Dashboard />);
    expect(document.body.querySelector('header')).toBeTruthy();
    unmount();
  });

  it('displays the header text', () => {
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('RESEARCH HUB')).toBeTruthy();
    unmount();
  });

  it('displays all four tab buttons', () => {
    const { unmount } = render(() => <Dashboard />);

    expect(screen.getByText('DASHBOARD')).toBeTruthy();
    expect(screen.getByText('SESSIONS')).toBeTruthy();
    expect(screen.getByText('LIBRARY')).toBeTruthy();
    expect(screen.getByText('SETTINGS')).toBeTruthy();
    unmount();
  });

  it('displays the search input', () => {
    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?');
    expect(input).toBeTruthy();
    unmount();
  });

  it('shows the "No active sessions" placeholder on initial render', () => {
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('No active sessions')).toBeTruthy();
    unmount();
  });
});
