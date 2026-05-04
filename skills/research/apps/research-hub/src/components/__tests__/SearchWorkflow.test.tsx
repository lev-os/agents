import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@solidjs/testing-library';
import Dashboard from '../Dashboard';

// Mock tauri service
vi.mock('../../services/tauri', () => ({
  searchStart: vi.fn().mockResolvedValue('session-new'),
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

describe('Search Workflow E2E', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('submits search with query and creates session', async () => {
    const { searchStart } = await import('../../services/tauri');
    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?');
    fireEvent.input(input, { target: { value: 'rust async patterns' } });
    const searchBtn = screen.getByText('SEARCH');
    fireEvent.click(searchBtn);
    await vi.waitFor(() => {
      expect(searchStart).toHaveBeenCalledWith('rust async patterns', 'quick');
    });
    unmount();
  });

  it('toggles search mode between quick and deep', () => {
    const { unmount } = render(() => <Dashboard />);
    const modeBtn = screen.getByText('QUICK');
    expect(modeBtn).toBeTruthy();
    fireEvent.click(modeBtn);
    expect(screen.getByText('DEEP')).toBeTruthy();
    fireEvent.click(screen.getByText('DEEP'));
    expect(screen.getByText('QUICK')).toBeTruthy();
    unmount();
  });

  it('rejects empty search query', async () => {
    const { searchStart } = await import('../../services/tauri');
    const { unmount } = render(() => <Dashboard />);
    const searchBtn = screen.getByText('SEARCH');
    expect(searchBtn.hasAttribute('disabled')).toBe(true);
    fireEvent.click(searchBtn);
    expect(searchStart).not.toHaveBeenCalled();
    unmount();
  });

  it('clears search input after successful submission', async () => {
    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?') as HTMLInputElement;
    fireEvent.input(input, { target: { value: 'test query' } });
    expect(input.value).toBe('test query');
    const searchBtn = screen.getByText('SEARCH');
    fireEvent.click(searchBtn);
    await vi.waitFor(() => {
      expect(input.value).toBe('');
    });
    unmount();
  });
});
