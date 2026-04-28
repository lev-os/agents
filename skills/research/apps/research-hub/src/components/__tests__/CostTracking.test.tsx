import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@solidjs/testing-library';
import Dashboard from '../Dashboard';

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

describe('Cost Tracking E2E', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays budget usage percentage', () => {
    // Default daySummary: cost=0.48, budget=5.0 => 10%
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('BUDGET USAGE')).toBeTruthy();
    expect(screen.getByText('10%')).toBeTruthy();
    unmount();
  });

  it('displays today cost as formatted dollar amount', () => {
    // Default daySummary cost = 0.48
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText("TODAY'S COST")).toBeTruthy();
    expect(screen.getByText('$0.48')).toBeTruthy();
    unmount();
  });

  it('displays budget remaining correctly', () => {
    // budget=5.0, cost=0.48 => remaining=$4.52
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('BUDGET REMAINING')).toBeTruthy();
    expect(screen.getByText('$4.52')).toBeTruthy();
    unmount();
  });

  it('displays total searches count', () => {
    // Default daySummary: searches=12
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('SEARCHES')).toBeTruthy();
    expect(screen.getByText('12')).toBeTruthy();
    unmount();
  });

  it('displays sources found count', () => {
    // Default daySummary: sources=156
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('SOURCES FOUND')).toBeTruthy();
    expect(screen.getByText('156')).toBeTruthy();
    unmount();
  });
});
