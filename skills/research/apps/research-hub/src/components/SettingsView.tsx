import { Component, createSignal } from 'solid-js';

const SettingsView: Component = () => {
  const [dailyBudget, setDailyBudget] = createSignal(5.0);
  const [defaultMode, setDefaultMode] = createSignal<'quick' | 'deep'>('quick');
  const [maxSources, setMaxSources] = createSignal(10);
  const [notifications, setNotifications] = createSignal(true);

  const handleSave = () => {
    // TODO: Persist settings via Tauri IPC
    console.log('Settings saved:', {
      dailyBudget: dailyBudget(),
      defaultMode: defaultMode(),
      maxSources: maxSources(),
      notifications: notifications(),
    });
  };

  return (
    <div style={{ padding: '48px', 'max-width': '800px', margin: '0 auto' }}>
      <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin-bottom': '32px' }}>
        SETTINGS
      </h2>

      <div class="card" style={{ padding: '32px', 'margin-bottom': '24px' }}>
        <h3 style={{ 'font-family': 'var(--font-header)', 'font-size': '18px', 'font-weight': '700', color: 'var(--forest)', 'margin-bottom': '24px' }}>
          BUDGET
        </h3>

        <div style={{ 'margin-bottom': '24px' }}>
          <label class="label" style={{ display: 'block', color: 'var(--grid)', 'margin-bottom': '8px' }}>
            DAILY BUDGET (USD)
          </label>
          <input
            type="number"
            value={dailyBudget()}
            onInput={(e) => setDailyBudget(parseFloat(e.currentTarget.value) || 0)}
            min="0"
            step="0.50"
            style={{ width: '120px' }}
          />
          <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-top': '8px' }}>
            You'll be warned when approaching this limit
          </p>
        </div>
      </div>

      <div class="card" style={{ padding: '32px', 'margin-bottom': '24px' }}>
        <h3 style={{ 'font-family': 'var(--font-header)', 'font-size': '18px', 'font-weight': '700', color: 'var(--forest)', 'margin-bottom': '24px' }}>
          RESEARCH DEFAULTS
        </h3>

        <div style={{ 'margin-bottom': '24px' }}>
          <label class="label" style={{ display: 'block', color: 'var(--grid)', 'margin-bottom': '8px' }}>
            DEFAULT SEARCH MODE
          </label>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              onClick={() => setDefaultMode('quick')}
              class={defaultMode() === 'quick' ? 'primary' : ''}
            >
              QUICK
            </button>
            <button
              onClick={() => setDefaultMode('deep')}
              class={defaultMode() === 'deep' ? 'primary' : ''}
            >
              DEEP
            </button>
          </div>
          <p class="label" style={{ color: 'var(--grid)', opacity: 0.6, 'margin-top': '8px' }}>
            Quick: 1-2 turns, faster and cheaper. Deep: 3-5 turns, more thorough.
          </p>
        </div>

        <div style={{ 'margin-bottom': '24px' }}>
          <label class="label" style={{ display: 'block', color: 'var(--grid)', 'margin-bottom': '8px' }}>
            MAX SOURCES PER SEARCH
          </label>
          <input
            type="number"
            value={maxSources()}
            onInput={(e) => setMaxSources(parseInt(e.currentTarget.value) || 10)}
            min="5"
            max="50"
            step="5"
            style={{ width: '120px' }}
          />
        </div>
      </div>

      <div class="card" style={{ padding: '32px', 'margin-bottom': '24px' }}>
        <h3 style={{ 'font-family': 'var(--font-header)', 'font-size': '18px', 'font-weight': '700', color: 'var(--forest)', 'margin-bottom': '24px' }}>
          NOTIFICATIONS
        </h3>

        <div style={{ display: 'flex', 'align-items': 'center', gap: '16px' }}>
          <button
            onClick={() => setNotifications(!notifications())}
            class={notifications() ? 'accent-mint' : ''}
            style={{ 'min-width': '80px' }}
          >
            {notifications() ? 'ON' : 'OFF'}
          </button>
          <span style={{ color: 'var(--grid)' }}>
            Show notifications when research completes
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', 'justify-content': 'flex-end', gap: '12px' }}>
        <button>RESET TO DEFAULTS</button>
        <button class="primary" onClick={handleSave}>SAVE SETTINGS</button>
      </div>
    </div>
  );
};

export default SettingsView;
