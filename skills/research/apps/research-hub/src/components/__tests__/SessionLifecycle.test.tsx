import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@solidjs/testing-library';
import Dashboard from '../Dashboard';

vi.mock('../../services/tauri', () => ({
  searchStart: vi.fn().mockResolvedValue('session-abc'),
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

describe('Session Lifecycle E2E', () => {
  beforeEach(async () => {
    vi.clearAllMocks();
    const tauri = await import('../../services/tauri');
    (tauri.searchStart as ReturnType<typeof vi.fn>).mockResolvedValue('session-abc');
    (tauri.sessionList as ReturnType<typeof vi.fn>).mockResolvedValue([]);
    (tauri.sessionGet as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    (tauri.listenToProgress as ReturnType<typeof vi.fn>).mockResolvedValue(() => {});
    (tauri.listenToSourceFound as ReturnType<typeof vi.fn>).mockResolvedValue(() => {});
    (tauri.listenToComplete as ReturnType<typeof vi.fn>).mockResolvedValue(() => {});
  });

  it('shows empty state when no active sessions', () => {
    const { unmount } = render(() => <Dashboard />);
    expect(screen.getByText('No active sessions')).toBeTruthy();
    unmount();
  });

  it('creates a session via searchStart after form submission', async () => {
    const { searchStart } = await import('../../services/tauri');
    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?');
    fireEvent.input(input, { target: { value: 'distributed systems' } });
    fireEvent.click(screen.getByText('SEARCH'));
    await vi.waitFor(() => {
      expect(searchStart).toHaveBeenCalledWith('distributed systems', 'quick');
    });
    unmount();
  });

  it('loads existing sessions from sessionList on mount', async () => {
    const { sessionList } = await import('../../services/tauri');
    (sessionList as ReturnType<typeof vi.fn>).mockResolvedValue([
      {
        id: 'existing-1',
        query: 'loaded-from-backend',
        mode: 'quick',
        status: 'searching',
        createdAt: new Date(),
        turns: [{ number: 1, query: 'q', confidence: 50, sourcesCount: 3, cost: 0.01, duration: 30, completedAt: new Date() }],
        sources: [{ id: 's1', url: 'https://example.com', title: 'Ex', type: 'web', relevance: 0.9, discoveredAt: new Date() }],
        cost: 0.01,
        confidence: 50,
      },
    ]);
    const { unmount } = render(() => <Dashboard />);
    await vi.waitFor(() => {
      expect(screen.getByText('loaded-from-backend')).toBeTruthy();
    });
    unmount();
  });

  it('displays session card with turn info from loaded sessions', async () => {
    const { sessionList } = await import('../../services/tauri');
    (sessionList as ReturnType<typeof vi.fn>).mockResolvedValue([
      {
        id: 'turn-test',
        query: 'neural networks',
        mode: 'quick',
        status: 'running',
        createdAt: new Date(),
        turns: [],
        sources: [],
        cost: 0,
        confidence: 0,
      },
    ]);
    const { unmount } = render(() => <Dashboard />);
    await vi.waitFor(() => {
      expect(screen.getByText('neural networks')).toBeTruthy();
    });
    // Session card should show turn info (TURN 0/2 for quick mode)
    expect(screen.getByText(/TURN 0\/2/)).toBeTruthy();
    unmount();
  });
});
