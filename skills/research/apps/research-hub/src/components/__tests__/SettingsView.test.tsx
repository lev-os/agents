import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@solidjs/testing-library';
import SettingsView from '../SettingsView';

describe('SettingsView', () => {
  it('renders the SETTINGS heading', () => {
    const { unmount } = render(() => <SettingsView />);
    expect(screen.getByText('SETTINGS')).toBeTruthy();
    unmount();
  });

  it('displays budget section with daily budget input', () => {
    const { unmount } = render(() => <SettingsView />);
    expect(screen.getByText('BUDGET')).toBeTruthy();
    expect(screen.getByText('DAILY BUDGET (USD)')).toBeTruthy();
    unmount();
  });

  it('displays research defaults with mode toggle', () => {
    const { unmount } = render(() => <SettingsView />);
    expect(screen.getByText('RESEARCH DEFAULTS')).toBeTruthy();
    expect(screen.getByText('QUICK')).toBeTruthy();
    expect(screen.getByText('DEEP')).toBeTruthy();
    unmount();
  });

  it('displays notifications toggle defaulting to ON', () => {
    const { unmount } = render(() => <SettingsView />);
    expect(screen.getByText('ON')).toBeTruthy();
    unmount();
  });

  it('toggles notifications off when clicked', () => {
    const { unmount } = render(() => <SettingsView />);
    const toggle = screen.getByText('ON');
    fireEvent.click(toggle);
    expect(screen.getByText('OFF')).toBeTruthy();
    unmount();
  });

  it('has save and reset buttons', () => {
    const { unmount } = render(() => <SettingsView />);
    expect(screen.getByText('SAVE SETTINGS')).toBeTruthy();
    expect(screen.getByText('RESET TO DEFAULTS')).toBeTruthy();
    unmount();
  });

  it('save button calls handleSave', () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    const { unmount } = render(() => <SettingsView />);
    fireEvent.click(screen.getByText('SAVE SETTINGS'));
    expect(consoleSpy).toHaveBeenCalledWith('Settings saved:', expect.any(Object));
    consoleSpy.mockRestore();
    unmount();
  });
});
