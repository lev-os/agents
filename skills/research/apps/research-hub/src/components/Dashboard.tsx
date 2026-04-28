import { Component, createSignal, For, Show, onMount, onCleanup } from 'solid-js';
import * as tauri from '../services/tauri';
import SessionsView from './SessionsView';
import LibraryView from './LibraryView';
import SettingsView from './SettingsView';

/**
 * Dashboard Component - Technical Minimalist Design
 * Main interface for Research Hub with quick search, active sessions,
 * today's summary, and tab navigation footer.
 *
 * Uses SolidJS signals for reactive state management.
 * Styled with Technical Minimalist design system.
 */

interface ActiveSession {
  id: string;
  query: string;
  turn: number;
  maxTurns: number;
  confidence: number;
  sources: number;
  cost: number;
  duration: number;
  status: 'running' | 'paused' | 'complete';
}

interface RecentSession {
  id: string;
  query: string;
  status: 'completed' | 'paused' | 'failed';
  cost: number;
  timestamp: string;
}

interface DaySummary {
  searches: number;
  sources: number;
  cost: number;
  budget: number;
}

const Dashboard: Component = () => {
  const [searchQuery, setSearchQuery] = createSignal('');
  const [searchMode, setSearchMode] = createSignal<'quick' | 'deep'>('quick');
  const [activeTab, setActiveTab] = createSignal<'dashboard' | 'sessions' | 'library' | 'settings'>('dashboard');
  const [activeSessions, setActiveSessions] = createSignal<ActiveSession[]>([]);
  const [selectedSession, setSelectedSession] = createSignal<tauri.Session | null>(null);
  const [recentSessions] = createSignal<RecentSession[]>([
    { id: '20260203-2300', query: 'kubernetes-scaling', status: 'completed', cost: 0.12, timestamp: '2026-02-03 23:00' },
    { id: '20260203-2215', query: 'react-patterns', status: 'completed', cost: 0.08, timestamp: '2026-02-03 22:15' },
    { id: '20260203-2100', query: 'auth-best-practices', status: 'paused', cost: 0.04, timestamp: '2026-02-03 21:00' },
  ]);
  const [daySummary] = createSignal<DaySummary>({
    searches: 12,
    sources: 156,
    cost: 0.48,
    budget: 5.0,
  });

  const progressPercent = (session: ActiveSession) =>
    Math.round((session.turn / session.maxTurns) * 100);

  const budgetPercent = () =>
    Math.round((daySummary().cost / daySummary().budget) * 100);

  const budgetStatus = () => {
    const percent = budgetPercent();
    if (percent > 90) return 'critical';
    if (percent > 70) return 'warning';
    return 'healthy';
  };

  const statusIcon = (status: ActiveSession['status']) => {
    switch (status) {
      case 'running': return '●';
      case 'paused': return '◐';
      case 'complete': return '○';
      default: return '○';
    }
  };

  const statusColor = (status: ActiveSession['status']) => {
    switch (status) {
      case 'running': return 'var(--coral)';
      case 'paused': return 'var(--gold)';
      case 'complete': return 'var(--mint)';
      default: return 'var(--grid)';
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

  const handleSearch = async (e: Event) => {
    e.preventDefault();
    const query = searchQuery();
    if (!query.trim()) return;

    try {
      const sessionId = await tauri.searchStart(query, searchMode());
      const newSession: ActiveSession = {
        id: sessionId,
        query,
        turn: 0,
        maxTurns: searchMode() === 'deep' ? 5 : 2,
        confidence: 0,
        sources: 0,
        cost: 0,
        duration: 0,
        status: 'running',
      };
      setActiveSessions([newSession, ...activeSessions()]);
      setSearchQuery('');
    } catch (error) {
      console.error('Failed to start search:', error);
    }
  };

  onMount(async () => {
    const unlistenProgress = await tauri.listenToProgress((payload) => {
      setActiveSessions(sessions =>
        sessions.map(session =>
          session.id === payload.sessionId
            ? { ...session, turn: payload.turn, confidence: payload.confidence, sources: payload.sources, cost: payload.cost, duration: payload.duration, status: payload.status as ActiveSession['status'] }
            : session
        )
      );
    });

    const unlistenSource = await tauri.listenToSourceFound((payload) => {
      setActiveSessions(sessions =>
        sessions.map(session =>
          session.id === payload.sessionId ? { ...session, sources: session.sources + 1 } : session
        )
      );
    });

    const unlistenComplete = await tauri.listenToComplete((payload) => {
      setActiveSessions(sessions =>
        sessions.map(session =>
          session.id === payload.sessionId
            ? { ...session, status: 'complete', confidence: payload.session.confidence, sources: payload.session.sources.length, cost: payload.session.cost }
            : session
        )
      );
    });

    onCleanup(() => {
      unlistenProgress();
      unlistenSource();
      unlistenComplete();
    });

    try {
      const sessions = await tauri.sessionList();
      const mappedSessions: ActiveSession[] = sessions
        .filter(s => s.status !== 'complete')
        .map(s => ({
          id: s.id,
          query: s.query,
          turn: s.turns.length,
          maxTurns: s.mode === 'deep' ? 5 : 2,
          confidence: s.confidence,
          sources: s.sources.length,
          cost: s.cost,
          duration: s.turns[s.turns.length - 1]?.duration || 0,
          status: s.status as ActiveSession['status'],
        }));
      setActiveSessions(mappedSessions);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  });

  return (
    <div style={{ 'min-height': '100vh', 'background-color': 'var(--paper)', 'padding-bottom': '120px' }}>
      {/* Header */}
      <header style={{ 'border-bottom': '1px solid rgba(58, 58, 56, 0.2)', 'background-color': 'var(--paper)', 'position': 'sticky', 'top': '0', 'z-index': '10' }}>
        <div style={{ 'max-width': '1200px', 'margin': '0 auto', 'padding': '32px 48px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between' }}>
          <div>
            <h1 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(32px, 5vw, 48px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin': '0' }}>
              RESEARCH HUB
            </h1>
            <p class="label" style={{ 'margin-top': '8px', 'color': 'var(--grid)', 'opacity': '0.6' }}>AI-POWERED DISCOVERY</p>
          </div>
          <div class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>V1.0.0</div>
        </div>
      </header>

      {/* Tab Views */}
      <Show when={activeTab() === 'sessions'}>
        <SessionsView />
      </Show>

      <Show when={activeTab() === 'library'}>
        <LibraryView />
      </Show>

      <Show when={activeTab() === 'settings'}>
        <SettingsView />
      </Show>

      {/* Dashboard Main - only show when dashboard tab active */}
      <Show when={activeTab() === 'dashboard'}>
      <main style={{ 'max-width': '1200px', 'margin': '0 auto', 'padding': '48px' }}>
        {/* Search */}
        <section style={{ 'margin-bottom': '64px' }}>
          <label class="label" style={{ 'display': 'block', 'margin-bottom': '16px', 'color': 'var(--grid)' }}>START A SEARCH</label>
          <form onSubmit={handleSearch} style={{ 'display': 'flex', 'flex-direction': 'column', 'gap': '16px' }}>
            <div style={{ 'display': 'flex', 'gap': '12px' }}>
              <input
                type="text"
                value={searchQuery()}
                onInput={(e) => setSearchQuery(e.currentTarget.value)}
                placeholder="What would you like to research?"
                style={{ 'flex': '1' }}
              />
              <button type="button" onClick={() => setSearchMode(m => m === 'quick' ? 'deep' : 'quick')} class={searchMode() === 'deep' ? 'accent-mint' : ''}>
                {searchMode() === 'deep' ? 'DEEP' : 'QUICK'}
              </button>
              <button type="submit" disabled={!searchQuery().trim()} class="primary">SEARCH</button>
            </div>
            <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>
              {searchMode() === 'deep' ? 'Deep mode: 5 recursive turns' : 'Quick mode: Single search'}
            </p>
          </form>
        </section>

        {/* Active Sessions */}
        <section style={{ 'margin-bottom': '64px' }}>
          <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin-bottom': '24px', 'display': 'flex', 'align-items': 'center', 'gap': '16px' }}>
            ACTIVE SESSIONS
            <span class="label" style={{ 'font-size': '10px', 'color': 'var(--grid)', 'opacity': '0.6', 'margin-left': 'auto' }}>{activeSessions().length} RUNNING</span>
          </h2>
          <div style={{ 'display': 'flex', 'flex-direction': 'column', 'gap': '16px' }}>
            <For each={activeSessions()}>
              {(session) => (
                <div class="card" onClick={() => handleSessionClick(session.id)} style={{ 'padding': '32px', 'cursor': 'pointer' }}>
                  <div style={{ 'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '24px', 'gap': '32px' }}>
                    <div style={{ 'flex': '1', 'min-width': '0' }}>
                      <div style={{ 'display': 'flex', 'align-items': 'center', 'gap': '12px', 'margin-bottom': '8px' }}>
                        <span style={{ 'font-size': '16px', 'color': statusColor(session.status) }}>{statusIcon(session.status)}</span>
                        <h3 style={{ 'font-family': 'var(--font-body)', 'font-size': '18px', 'font-weight': '600', 'color': 'var(--forest)', 'margin': '0' }}>{session.query}</h3>
                      </div>
                      <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>
                        TURN {Math.ceil(session.turn)}/{session.maxTurns} •
                        {session.confidence > 0 && ` ${Math.round(session.confidence)}% CONFIDENT •`}
                        {(session.duration / 60).toFixed(1)}M ELAPSED
                      </p>
                    </div>
                    <div style={{ 'text-align': 'right' }}>
                      <p style={{ 'font-size': '24px', 'font-weight': '600', 'color': 'var(--forest)', 'margin': '0' }}>{session.sources}</p>
                      <p class="label" style={{ 'margin-top': '4px', 'color': 'var(--grid)', 'opacity': '0.6' }}>SOURCES</p>
                      <p class="label" style={{ 'margin-top': '8px', 'color': 'var(--grid)', 'opacity': '0.6' }}>${session.cost.toFixed(4)}</p>
                    </div>
                  </div>
                  <div>
                    <div style={{ 'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '8px' }}>
                      <span class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>PROGRESS</span>
                      <span class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>{progressPercent(session)}%</span>
                    </div>
                    <div style={{ 'height': '2px', 'background-color': 'rgba(58, 58, 56, 0.1)', 'border-radius': '0px', 'overflow': 'hidden' }}>
                      <div style={{ 'height': '2px', 'background-color': statusColor(session.status), 'width': `${progressPercent(session)}%`, 'transition': 'width 0.3s ease' }} />
                    </div>
                  </div>
                </div>
              )}
            </For>
            <Show when={activeSessions().length === 0}>
              <div style={{ 'border': '1px dashed rgba(58, 58, 56, 0.2)', 'border-radius': '2px', 'padding': '64px', 'text-align': 'center' }}>
                <p style={{ 'font-size': '18px', 'color': 'var(--grid)', 'opacity': '0.4', 'margin-bottom': '8px' }}>No active sessions</p>
                <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.4' }}>START A SEARCH TO BEGIN</p>
              </div>
            </Show>
          </div>
        </section>

        {/* Summary */}
        <section style={{ 'margin-bottom': '64px' }}>
          <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin-bottom': '24px' }}>TODAY'S SUMMARY</h2>
          <div class="card" style={{ 'padding': '32px' }}>
            <div style={{ 'display': 'grid', 'grid-template-columns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '32px', 'margin-bottom': '32px' }}>
              <div>
                <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6', 'margin-bottom': '8px' }}>SEARCHES</p>
                <p style={{ 'font-size': '48px', 'font-weight': '700', 'font-family': 'var(--font-header)', 'line-height': '0.9', 'color': 'var(--forest)' }}>{daySummary().searches}</p>
              </div>
              <div>
                <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6', 'margin-bottom': '8px' }}>SOURCES FOUND</p>
                <p style={{ 'font-size': '48px', 'font-weight': '700', 'font-family': 'var(--font-header)', 'line-height': '0.9', 'color': 'var(--forest)' }}>{daySummary().sources}</p>
              </div>
              <div>
                <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6', 'margin-bottom': '8px' }}>TODAY'S COST</p>
                <p style={{ 'font-size': '48px', 'font-weight': '700', 'font-family': 'var(--font-header)', 'line-height': '0.9', 'color': 'var(--mint)' }}>${daySummary().cost.toFixed(2)}</p>
              </div>
              <div>
                <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6', 'margin-bottom': '8px' }}>BUDGET REMAINING</p>
                <p style={{ 'font-size': '48px', 'font-weight': '700', 'font-family': 'var(--font-header)', 'line-height': '0.9', 'color': budgetStatus() === 'critical' ? 'var(--coral)' : budgetStatus() === 'warning' ? 'var(--gold)' : 'var(--mint)' }}>
                  ${(daySummary().budget - daySummary().cost).toFixed(2)}
                </p>
              </div>
            </div>
            <div>
              <div style={{ 'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '8px' }}>
                <span class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>BUDGET USAGE</span>
                <span class="label" style={{ 'color': budgetStatus() === 'critical' ? 'var(--coral)' : budgetStatus() === 'warning' ? 'var(--gold)' : 'var(--grid)', 'opacity': '0.6' }}>{budgetPercent()}%</span>
              </div>
              <div style={{ 'height': '4px', 'background-color': 'rgba(58, 58, 56, 0.1)', 'border-radius': '0px', 'overflow': 'hidden' }}>
                <div style={{ 'height': '4px', 'background-color': budgetStatus() === 'critical' ? 'var(--coral)' : budgetStatus() === 'warning' ? 'var(--gold)' : 'var(--mint)', 'width': `${Math.min(budgetPercent(), 100)}%`, 'transition': 'width 0.3s ease' }} />
              </div>
            </div>
          </div>
        </section>

        {/* Recent */}
        <section style={{ 'padding-bottom': '48px' }}>
          <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin-bottom': '24px' }}>RECENT SESSIONS</h2>
          <div style={{ 'display': 'flex', 'flex-direction': 'column', 'gap': '8px' }}>
            <For each={recentSessions()}>
              {(session) => (
                <div class="card" onClick={() => handleSessionClick(session.id)} style={{ 'padding': '24px', 'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'gap': '24px', 'cursor': 'pointer' }}>
                  <div style={{ 'display': 'flex', 'align-items': 'center', 'gap': '16px', 'flex': '1' }}>
                    <span style={{ 'font-size': '16px', 'color': session.status === 'completed' ? 'var(--mint)' : session.status === 'paused' ? 'var(--gold)' : 'var(--coral)' }}>
                      {session.status === 'completed' ? '○' : session.status === 'paused' ? '◐' : '×'}
                    </span>
                    <div style={{ 'flex': '1', 'min-width': '0' }}>
                      <p style={{ 'font-family': 'var(--font-body)', 'font-size': '16px', 'font-weight': '500', 'color': 'var(--forest)', 'margin': '0 0 4px 0' }}>{session.query}</p>
                      <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6' }}>{session.timestamp}</p>
                    </div>
                  </div>
                  <div style={{ 'text-align': 'right' }}>
                    <p style={{ 'font-family': 'var(--font-mono)', 'font-size': '14px', 'font-weight': '500', 'color': 'var(--forest)', 'margin': '0 0 4px 0' }}>${session.cost.toFixed(2)}</p>
                    <p class="label" style={{ 'color': 'var(--grid)', 'opacity': '0.6', 'text-transform': 'capitalize' }}>{session.status}</p>
                  </div>
                </div>
              )}
            </For>
          </div>
        </section>
      </main>
      </Show>

      {/* Session Detail Modal */}
      <Show when={selectedSession()}>
        <div
          onClick={() => setSelectedSession(null)}
          style={{
            position: 'fixed',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            'background-color': 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'z-index': '100',
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
                <p class="label" style={{ color: 'var(--grid)', opacity: '0.6' }}>
                  Session ID: {selectedSession()?.id}
                </p>
              </div>
              <button onClick={() => setSelectedSession(null)}>CLOSE</button>
            </div>

            <div style={{ display: 'grid', 'grid-template-columns': 'repeat(3, 1fr)', gap: '16px', 'margin-bottom': '24px' }}>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: '0.6', 'margin-bottom': '4px' }}>STATUS</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--forest)', 'text-transform': 'capitalize' }}>
                  {selectedSession()?.status}
                </p>
              </div>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: '0.6', 'margin-bottom': '4px' }}>CONFIDENCE</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--forest)' }}>
                  {Math.round(selectedSession()?.confidence || 0)}%
                </p>
              </div>
              <div>
                <p class="label" style={{ color: 'var(--grid)', opacity: '0.6', 'margin-bottom': '4px' }}>COST</p>
                <p style={{ 'font-size': '18px', 'font-weight': '600', color: 'var(--mint)' }}>
                  ${(selectedSession()?.cost || 0).toFixed(4)}
                </p>
              </div>
            </div>

            <div style={{ 'margin-bottom': '24px' }}>
              <p class="label" style={{ color: 'var(--grid)', opacity: '0.6', 'margin-bottom': '8px' }}>
                SOURCES ({selectedSession()?.sources.length || 0})
              </p>
              <div style={{ display: 'flex', 'flex-direction': 'column', gap: '8px', 'max-height': '200px', overflow: 'auto' }}>
                <For each={selectedSession()?.sources || []}>
                  {(source) => (
                    <div style={{ padding: '12px', 'background-color': 'rgba(58, 58, 56, 0.05)', 'border-radius': '2px' }}>
                      <p style={{ 'font-size': '14px', 'font-weight': '500', color: 'var(--forest)', margin: '0 0 4px 0' }}>
                        {source.title}
                      </p>
                      <p class="label" style={{ color: 'var(--grid)', opacity: '0.6', 'word-break': 'break-all' }}>
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

      {/* Footer Nav */}
      <nav style={{ 'position': 'fixed', 'bottom': '0', 'left': '0', 'right': '0', 'background-color': 'var(--paper)', 'border-top': '1px solid rgba(58, 58, 56, 0.2)' }}>
        <div style={{ 'max-width': '1200px', 'margin': '0 auto', 'padding': '24px 48px', 'display': 'flex', 'justify-content': 'center', 'gap': '48px' }}>
          <button onClick={() => setActiveTab('dashboard')} style={{ 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '8px', 'padding': '12px 24px', 'border': 'none', 'background-color': activeTab() === 'dashboard' ? 'rgba(26, 60, 43, 0.1)' : 'transparent', 'border-radius': '2px', 'cursor': 'pointer', 'transition': 'background-color 0.2s ease' }}>
            <span style={{ 'font-size': '20px', 'color': activeTab() === 'dashboard' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'dashboard' ? '1' : '0.6' }}>■</span>
            <span class="label" style={{ 'color': activeTab() === 'dashboard' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'dashboard' ? '1' : '0.6' }}>DASHBOARD</span>
          </button>
          <button onClick={() => setActiveTab('sessions')} style={{ 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '8px', 'padding': '12px 24px', 'border': 'none', 'background-color': activeTab() === 'sessions' ? 'rgba(26, 60, 43, 0.1)' : 'transparent', 'border-radius': '2px', 'cursor': 'pointer', 'transition': 'background-color 0.2s ease' }}>
            <span style={{ 'font-size': '20px', 'color': activeTab() === 'sessions' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'sessions' ? '1' : '0.6' }}>≡</span>
            <span class="label" style={{ 'color': activeTab() === 'sessions' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'sessions' ? '1' : '0.6' }}>SESSIONS</span>
          </button>
          <button onClick={() => setActiveTab('library')} style={{ 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '8px', 'padding': '12px 24px', 'border': 'none', 'background-color': activeTab() === 'library' ? 'rgba(26, 60, 43, 0.1)' : 'transparent', 'border-radius': '2px', 'cursor': 'pointer', 'transition': 'background-color 0.2s ease' }}>
            <span style={{ 'font-size': '20px', 'color': activeTab() === 'library' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'library' ? '1' : '0.6' }}>▭</span>
            <span class="label" style={{ 'color': activeTab() === 'library' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'library' ? '1' : '0.6' }}>LIBRARY</span>
          </button>
          <button onClick={() => setActiveTab('settings')} style={{ 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '8px', 'padding': '12px 24px', 'border': 'none', 'background-color': activeTab() === 'settings' ? 'rgba(26, 60, 43, 0.1)' : 'transparent', 'border-radius': '2px', 'cursor': 'pointer', 'transition': 'background-color 0.2s ease' }}>
            <span style={{ 'font-size': '20px', 'color': activeTab() === 'settings' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'settings' ? '1' : '0.6' }}>⚙</span>
            <span class="label" style={{ 'color': activeTab() === 'settings' ? 'var(--forest)' : 'var(--grid)', 'opacity': activeTab() === 'settings' ? '1' : '0.6' }}>SETTINGS</span>
          </button>
        </div>
      </nav>
    </div>
  );
};

export default Dashboard;
