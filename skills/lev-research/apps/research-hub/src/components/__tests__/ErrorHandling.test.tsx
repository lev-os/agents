import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@solidjs/testing-library';
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

describe('Error Handling E2E', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('handles searchStart rejection without crashing', async () => {
    const { searchStart } = await import('../../services/tauri');
    (searchStart as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network error'));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?');
    fireEvent.input(input, { target: { value: 'failing query' } });
    fireEvent.click(screen.getByText('SEARCH'));

    await vi.waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Failed to start search:', expect.any(Error));
    });
    // Component should still be functional
    expect(screen.getByText('RESEARCH HUB')).toBeTruthy();
    consoleSpy.mockRestore();
    unmount();
  });

  it('handles sessionList rejection on mount without crashing', async () => {
    const { sessionList } = await import('../../services/tauri');
    (sessionList as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Backend unavailable'));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const { unmount } = render(() => <Dashboard />);

    await vi.waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Failed to load sessions:', expect.any(Error));
    });
    // Component should still render
    expect(screen.getByText('RESEARCH HUB')).toBeTruthy();
    expect(screen.getByText('No active sessions')).toBeTruthy();
    consoleSpy.mockRestore();
    unmount();
  });

  it('handles sessionGet rejection when clicking a session', async () => {
    const { sessionGet } = await import('../../services/tauri');
    (sessionGet as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Session not found'));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const { unmount } = render(() => <Dashboard />);
    // Recent sessions are hardcoded and clickable
    const recentSession = screen.getByText('kubernetes-scaling');
    fireEvent.click(recentSession);

    await vi.waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Failed to load session:', expect.any(Error));
    });
    // Component should not crash
    expect(screen.getByText('RESEARCH HUB')).toBeTruthy();
    consoleSpy.mockRestore();
    unmount();
  });
});
