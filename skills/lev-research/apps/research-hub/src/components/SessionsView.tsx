import { Component, createSignal, For, Show, onMount } from 'solid-js';
import * as tauri from '../services/tauri';

interface SessionItem {
  id: string;
  query: string;
  mode: 'quick' | 'deep' | 'full';
  status: 'idle' | 'searching' | 'extracting' | 'synthesizing' | 'complete' | 'paused' | 'error';
  cost: number;
  confidence: number;
  sourcesCount: number;
  createdAt: string;
}

const SessionsView: Component = () => {
  const [sessions, setSessions] = createSignal<SessionItem[]>([]);
  const [selectedSession, setSelectedSession] = createSignal<tauri.Session | null>(null);
  const [loading, setLoading] = createSignal(true);
  const [filter, setFilter] = createSignal<'all' | 'active' | 'complete'>('all');

  const filteredSessions = () => {
    const f = filter();
    return sessions().filter(s => {
      if (f === 'all') return true;
      if (f === 'active') return s.status !== 'complete' && s.status !== 'error';
      if (f === 'complete') return s.status === 'complete';
      return true;
    });
  };

  const statusColor = (status: SessionItem['status']) => {
    switch (status) {
      case 'searching':
      case 'extracting':
      case 'synthesizing':
        return 'var(--coral)';
      case 'paused':
        return 'var(--gold)';
      case 'complete':
        return 'var(--mint)';
      case 'error':
        return 'var(--coral)';
      default:
        return 'var(--grid)';
    }
  };

  const statusIcon = (status: SessionItem['status']) => {
    switch (status) {
      case 'searching':
      case 'extracting':
      case 'synthesizing':
        return '●';
      case 'paused':
        return '◐';
      case 'complete':
        return '○';
      case 'error':
        return '×';
      default:
        return '○';
    }
  };

  const handleSessionClick = async (sessionId: string) => {
    try {
      const session = await tauri.sessionGet(sessionId);
      setSelectedSession(session);
    } catch (error) {
      console.error('Failed to load session:', error);
    }
  };

  const handleResume = async (sessionId: string) => {
    try {
      await tauri.searchResume(sessionId);
    } catch (error) {
      console.error('Failed to resume session:', error);
    }
  };

  const handlePause = async (sessionId: string) => {
    try {
      await tauri.searchPause(sessionId);
    } catch (error) {
      console.error('Failed to pause session:', error);
    }
  };

  onMount(async () => {
    try {
      const rawSessions = await tauri.sessionList();
      const mapped: SessionItem[] = rawSessions.map(s => ({
        id: s.id,
        query: s.query,
        mode: s.mode,
        status: s.status,
        cost: s.cost,
        confidence: s.confidence,
        sourcesCount: s.sources.length,
        createdAt: new Date(s.createdAt).toLocaleString(),
      }));
      setSessions(mapped);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
    }
  });

  return (
    <div style={{ padding: '48px', 'max-width': '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '32px' }}>
        <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', margin: 0 }}>
          ALL SESSIONS
        </h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setFilter('all')}
            class={filter() === 'all' ? 'primary' : ''}
          >
            ALL
          </button>
          <button
            onClick={() => setFilter('active')}
            class={filter() === 'active' ? 'primary' : ''}
          >
            ACTIVE
          </button>
          <button
            onClick={() => setFilter('complete')}
            class={filter() === 'complete' ? 'primary' : ''}
          >
            COMPLETE
          </button>
        </div>
      </div>

      <Show when={loading()}>
        <div style={{ 'text-align': 'center', padding: '64px', color: 'var(--grid)', opacity: 0.6 }}>
          Loading sessions...
        </div>
      </Show>

      <Show when={!loading() && filteredSessions().length === 0}>
        <div style={{ border: '1px dashed rgba(58, 58, 56, 0.2)', 'border-radius': '2px', padding: '64px', 'text-align': 'center' }}>
          <p style={{ 'font-size': '18px', color: 'var(--grid)', opacity: 0.4, 'margin-bottom': '8px' }}>No sessions found</p>
          <p class="label" style={{ color: 'var(--grid)', opacity: 0.4 }}>START A SEARCH FROM THE DASHBOARD</p>
        </div>
      </Show>

      <Show when={!loading() && filteredSessions().length > 0}>
        <div style={{ display: 'flex', 'flex-direction': 'column', gap: '8px' }}>
          <For each={filteredSessions()}>
            {(session) => (
              <div
                class="card"
                onClick={() => handleSessionClick(session.id)}
                style={{
                  padding: '24px',
                  display: 'flex',
                  'align-items': 'center',
                  'justify-content': 'space-between',
                  gap: '24px',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s ease',
                }}
              >
                <div style={{ display: 'flex', 'align-items': 'center', gap: '16px', flex: 1 }}>
                  <span style={{ 'font-size': '16px', color: statusColor(session.status) }}>
                    {statusIcon(session.status)}
                  </span>
                  <div style={{ flex: 1, 'min-width': 0 }}>
                    <p style={{ 'font-family': 'var(--font-body)', 'font-size': '16px', 'font-weight': '500', color: 'var(--forest)', margin: '0 0 4px 0' }}>
                      {session.query}
                    </p>
                    <p class="label" style={{ color: 'var(--grid)', opacity: 0.6 }}>
                      {session.createdAt} • {session.mode.toUpperCase()} • {session.sourcesCount} sources
                    </p>
                  </div>
                </div>
                <div style={{ display: 'flex', 'align-items': 'center', gap: '16px' }}>
                  <div style={{ 'text-align': 'right' }}>
                    <p style={{ 'font-family': 'var(--font-mono)', 'font-size': '14px', 'font-weight': '500', color: 'var(--forest)', margin: '0 0 4px 0' }}>
                      ${session.cost.toFixed(4)}
                    </p>
                    <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'text-transform': 'capitalize' }}>
                      {session.status}
                    </p>
                  </div>
                  <Show when={session.status === 'paused'}>
                    <button onClick={(e) => { e.stopPropagation(); handleResume(session.id); }} class="accent-mint">
                      RESUME
                    </button>
                  </Show>
                  <Show when={session.status === 'searching' || session.status === 'extracting'}>
                    <button onClick={(e) => { e.stopPropagation(); handlePause(session.id); }}>
                      PAUSE
                    </button>
                  </Show>
                </div>
              </div>
            )}
          </For>
        </div>
      </Show>

      {/* Session Detail Modal */}
      <Show when={selectedSession()}>
        <div
          onClick={() => setSelectedSession(null)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            'background-color': 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'z-index': 100,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            class="card"
            style={{
              width: '600px',
              'max-height': '80vh',
              overflow: 'auto',
              padding: '32px',
            }}
          >
            <div style={{ display: 'flex', 'justify-content': 'space-between', 'align-items': 'flex-start', 'margin-bottom': '24px' }}>
              <div>
                <h3 style={{ 'font-family': 'var(--font-header)', 'font-size': '24px', 'font-weight': '700', color: 'var(--forest)', margin: '0 0 8px 0' }}>
                  {selectedSession()?.query}
                </h3>
                <p class="label" style={{ color: 'var(--grid)', opacity: 0.6 }}>
                  Session ID: {selectedSession()?.id}
                </p>
              </div>
              <button onClick={() => setSelectedSession(null)}>CLOSE</button>
            </div>

            <div style={{ display: 'grid', 'grid-template-columns': 'repeat(3, 1fr)', gap: '16px', 'margin-bottom': '24px' }}>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-bottom': '4px' }}>STATUS</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--forest)', 'text-transform': 'capitalize' }}>
                  {selectedSession()?.status}
                </p>
              </div>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-bottom': '4px' }}>CONFIDENCE</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--forest)' }}>
                  {Math.round(selectedSession()?.confidence || 0)}%
                </p>
              </div>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-bottom': '4px' }}>COST</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--mint)' }}>
                  ${(selectedSession()?.cost || 0).toFixed(4)}
                </p>
              </div>
            </div>

            <div style={{ 'margin-bottom': '24px' }}>
              <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-bottom': '8px' }}>
                SOURCES ({selectedSession()?.sources.length || 0})
              </p>
              <div style={{ display: 'flex', 'flex-direction': 'column', gap: '8px', 'max-height': '200px', overflow: 'auto' }}>
                <For each={selectedSession()?.sources || []}>
                  {(source) => (
                    <div style={{ padding: '12px', 'background-color': 'rgba(58, 58, 56, 0.05)', 'border-radius': '2px' }}>
                      <p style={{ 'font-size': '14px', 'font-weight': '500', color: 'var(--forest)', margin: '0 0 4px 0' }}>
                        {source.title}
                      </p>
                      <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'word-break': 'break-all' }}>
                        {source.url}
                      </p>
                    </div>
                  )}
                </For>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </div>
  );
};

export default SessionsView;
