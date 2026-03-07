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

describe('Performance Baselines', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('Dashboard renders in under 100ms', () => {
    const start = performance.now();
    const { unmount } = render(() => <Dashboard />);
    const elapsed = performance.now() - start;

    expect(elapsed).toBeLessThan(100);
    console.log(`Dashboard render: ${elapsed.toFixed(2)}ms`);
    unmount();
  });

  it('Tab switch completes in under 50ms', async () => {
    const { container, unmount } = render(() => <Dashboard />);

    // Find the Sessions tab button and measure click time
    const buttons = container.querySelectorAll('nav button');
    const sessionsBtn = Array.from(buttons).find(b => b.textContent?.includes('SESSIONS'));

    if (sessionsBtn) {
      const start = performance.now();
      sessionsBtn.click();
      const elapsed = performance.now() - start;

      expect(elapsed).toBeLessThan(50);
      console.log(`Tab switch: ${elapsed.toFixed(2)}ms`);
    }
    unmount();
  });

  it('renders with default mock data in under 200ms', () => {
    const start = performance.now();
    const { unmount } = render(() => <Dashboard />);
    const elapsed = performance.now() - start;

    expect(elapsed).toBeLessThan(200);
    console.log(`Dashboard render (baseline): ${elapsed.toFixed(2)}ms`);
    unmount();
  });

  it('multiple sequential renders stay consistent', () => {
    const times: number[] = [];

    for (let i = 0; i < 5; i++) {
      const start = performance.now();
      const { unmount } = render(() => <Dashboard />);
      times.push(performance.now() - start);
      unmount();
    }

    const avg = times.reduce((a, b) => a + b, 0) / times.length;
    const max = Math.max(...times);

    // Average should be under 100ms, max under 200ms
    expect(avg).toBeLessThan(100);
    expect(max).toBeLessThan(200);
    console.log(`Render times: avg=${avg.toFixed(2)}ms, max=${max.toFixed(2)}ms`);
  });
});
