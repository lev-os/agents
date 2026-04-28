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

describe('Tab Navigation E2E', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('defaults to dashboard tab with search input visible', () => {
    const { unmount } = render(() => <Dashboard />);
    const input = screen.getByPlaceholderText('What would you like to research?');
    expect(input).toBeTruthy();
    expect(screen.getByText('ACTIVE SESSIONS')).toBeTruthy();
    unmount();
  });

  it('switches to sessions tab and hides search input', () => {
    const { unmount } = render(() => <Dashboard />);
    const sessionsTab = screen.getByText('SESSIONS');
    fireEvent.click(sessionsTab);
    expect(screen.getByTestId('sessions-view')).toBeTruthy();
    expect(screen.queryByPlaceholderText('What would you like to research?')).toBeNull();
    unmount();
  });

  it('switches to library tab and shows library view', () => {
    const { unmount } = render(() => <Dashboard />);
    const libraryTab = screen.getByText('LIBRARY');
    fireEvent.click(libraryTab);
    expect(screen.getByTestId('library-view')).toBeTruthy();
    expect(screen.queryByPlaceholderText('What would you like to research?')).toBeNull();
    unmount();
  });

  it('switches to settings tab and shows settings view', () => {
    const { unmount } = render(() => <Dashboard />);
    const settingsTab = screen.getByText('SETTINGS');
    fireEvent.click(settingsTab);
    expect(screen.getByTestId('settings-view')).toBeTruthy();
    expect(screen.queryByPlaceholderText('What would you like to research?')).toBeNull();
    unmount();
  });

  it('returns to dashboard tab and search input reappears', () => {
    const { unmount } = render(() => <Dashboard />);
    // Navigate away
    fireEvent.click(screen.getByText('SESSIONS'));
    expect(screen.queryByPlaceholderText('What would you like to research?')).toBeNull();
    // Navigate back
    fireEvent.click(screen.getByText('DASHBOARD'));
    expect(screen.getByPlaceholderText('What would you like to research?')).toBeTruthy();
    expect(screen.getByText('ACTIVE SESSIONS')).toBeTruthy();
    unmount();
  });
});
