import { Component, createSignal } from 'solid-js';

const LibraryView: Component = () => {
  const [searchQuery, setSearchQuery] = createSignal('');

  return (
    <div style={{ padding: '48px', 'max-width': '1200px', margin: '0 auto' }}>
      <h2 style={{ 'font-family': 'var(--font-header)', 'font-size': 'clamp(24px, 3vw, 32px)', 'font-weight': '700', 'line-height': '0.9', 'letter-spacing': '-0.02em', 'color': 'var(--forest)', 'margin-bottom': '24px' }}>
        SOURCE LIBRARY
      </h2>

      <div style={{ 'margin-bottom': '32px' }}>
        <input
          type="text"
          value={searchQuery()}
          onInput={(e) => setSearchQuery(e.currentTarget.value)}
          placeholder="Search saved sources..."
          style={{ width: '100%', 'max-width': '400px' }}
        />
      </div>

      <div style={{ border: '1px dashed rgba(58, 58, 56, 0.2)', 'border-radius': '2px', padding: '64px', 'text-align': 'center' }}>
        <p style={{ 'font-size': '48px', 'margin-bottom': '16px' }}>📚</p>
        <p style={{ 'font-size': '18px', color: 'var(--grid)', opacity: 0.6, 'margin-bottom': '8px' }}>
          Source Library Coming Soon
        </p>
        <p class="label" style={{ color: 'var(--grid)', opacity: 0.4 }}>
          SAVE SOURCES FROM YOUR RESEARCH SESSIONS TO BUILD YOUR KNOWLEDGE BASE
        </p>
      </div>

      <div style={{ 'margin-top': '48px' }}>
        <h3 style={{ 'font-family': 'var(--font-header)', 'font-size': '20px', 'font-weight': '700', color: 'var(--forest)', 'margin-bottom': '16px' }}>
          PLANNED FEATURES
        </h3>
        <ul style={{ color: 'var(--grid)', 'line-height': '1.8', 'padding-left': '20px' }}>
          <li>Save and organize sources from research sessions</li>
          <li>Full-text search across all saved content</li>
          <li>Tags and collections for organization</li>
          <li>Export to various formats (Markdown, BibTeX, etc.)</li>
          <li>Sync across devices</li>
        </ul>
      </div>
    </div>
  );
};

export default LibraryView;
