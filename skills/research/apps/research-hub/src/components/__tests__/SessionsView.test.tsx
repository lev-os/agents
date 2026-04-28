import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@solidjs/testing-library';
import SessionsView from '../SessionsView';

const mockSessions = [
  {
    id: 'session-1',
    query: 'rust async patterns',
    mode: 'quick' as const,
    status: 'searching' as const,
    createdAt: new Date('2026-02-03'),
    turns: [{ number: 1, query: 'rust async', confidence: 50, sourcesCount: 3, cost: 0.05, duration: 30, completedAt: new Date() }],
    sources: [
      { id: 's1', url: 'https://example.com/1', title: 'Source 1', type: 'web' as const, relevance: 0.9, discoveredAt: new Date() },
      { id: 's2', url: 'https://example.com/2', title: 'Source 2', type: 'web' as const, relevance: 0.8, discoveredAt: new Date() },
    ],
    cost: 0.05,
    confidence: 50,
  },
  {
    id: 'session-2',
    query: 'kubernetes scaling',
    mode: 'deep' as const,
    status: 'complete' as const,
    createdAt: new Date('2026-02-02'),
    completedAt: new Date('2026-02-02'),
    turns: [],
    sources: [{ id: 's3', url: 'https://example.com/3', title: 'Source 3', type: 'web' as const, relevance: 0.7, discoveredAt: new Date() }],
    cost: 0.15,
    confidence: 85,
  },
  {
    id: 'session-3',
    query: 'paused research',
    mode: 'quick' as const,
    status: 'paused' as const,
    createdAt: new Date('2026-02-01'),
    pausedAt: new Date('2026-02-01'),
    turns: [],
    sources: [],
    cost: 0.02,
    confidence: 20,
  },
];

const mockSessionDetail = {
  id: 'session-1',
  query: 'rust async patterns',
  mode: 'quick' as const,
  status: 'searching' as const,
  createdAt: new Date('2026-02-03'),
  turns: [{ number: 1, query: 'rust async', confidence: 50, sourcesCount: 3, cost: 0.05, duration: 30, completedAt: new Date() }],
  sources: [
    { id: 's1', url: 'https://example.com/1', title: 'Async Rust Guide', type: 'web' as const, relevance: 0.9, discoveredAt: new Date() },
  ],
  cost: 0.05,
  confidence: 50,
};

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

describe('SessionsView', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the ALL SESSIONS heading', () => {
    const { unmount } = render(() => <SessionsView />);
    expect(screen.getByText('ALL SESSIONS')).toBeTruthy();
    unmount();
  });

  it('displays filter buttons (ALL, ACTIVE, COMPLETE)', () => {
    const { unmount } = render(() => <SessionsView />);
    expect(screen.getByText('ALL')).toBeTruthy();
    expect(screen.getByText('ACTIVE')).toBeTruthy();
    expect(screen.getByText('COMPLETE')).toBeTruthy();
    unmount();
  });

  it('shows loading state initially', () => {
    const { unmount } = render(() => <SessionsView />);
    expect(screen.getByText('Loading sessions...')).toBeTruthy();
    unmount();
  });

  it('shows empty state after loading with no sessions', async () => {
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('No sessions found')).toBeTruthy();
    });
    unmount();
  });

  it('loads sessions from tauri on mount', async () => {
    const { sessionList } = await import('../../services/tauri');
    render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(sessionList).toHaveBeenCalled();
    });
  });

  it('renders session list when sessions exist', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('rust async patterns')).toBeTruthy();
      expect(screen.getByText('kubernetes scaling')).toBeTruthy();
      expect(screen.getByText('paused research')).toBeTruthy();
    });
    unmount();
  });

  it('shows cost for each session', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('$0.0500')).toBeTruthy();
      expect(screen.getByText('$0.1500')).toBeTruthy();
    });
    unmount();
  });

  it('shows RESUME button for paused sessions', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('RESUME')).toBeTruthy();
    });
    unmount();
  });

  it('shows PAUSE button for searching sessions', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('PAUSE')).toBeTruthy();
    });
    unmount();
  });

  it('opens detail modal when clicking a session', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    vi.mocked(tauri.sessionGet).mockResolvedValueOnce(mockSessionDetail as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('rust async patterns')).toBeTruthy();
    });
    // Click the session card
    const sessionCard = screen.getByText('rust async patterns').closest('.card');
    if (sessionCard) {
      (sessionCard as HTMLElement).click();
    }
    await vi.waitFor(() => {
      expect(screen.getByText('CLOSE')).toBeTruthy();
      expect(screen.getByText('Session ID: session-1')).toBeTruthy();
    });
    unmount();
  });

  it('shows source details in the detail modal', async () => {
    const tauri = await import('../../services/tauri');
    vi.mocked(tauri.sessionList).mockResolvedValueOnce(mockSessions as any);
    vi.mocked(tauri.sessionGet).mockResolvedValueOnce(mockSessionDetail as any);
    const { unmount } = render(() => <SessionsView />);
    await vi.waitFor(() => {
      expect(screen.getByText('rust async patterns')).toBeTruthy();
    });
    const sessionCard = screen.getByText('rust async patterns').closest('.card');
    if (sessionCard) {
      (sessionCard as HTMLElement).click();
    }
    await vi.waitFor(() => {
      expect(screen.getByText('Async Rust Guide')).toBeTruthy();
      expect(screen.getByText('https://example.com/1')).toBeTruthy();
    });
    unmount();
  });
});
