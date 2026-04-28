import { describe, it, expect } from 'vitest';
import { render, screen } from '@solidjs/testing-library';
import LibraryView from '../LibraryView';

describe('LibraryView', () => {
  it('renders the SOURCE LIBRARY heading', () => {
    const { unmount } = render(() => <LibraryView />);
    expect(screen.getByText('SOURCE LIBRARY')).toBeTruthy();
    unmount();
  });

  it('displays the search input with placeholder', () => {
    const { unmount } = render(() => <LibraryView />);
    expect(screen.getByPlaceholderText('Search saved sources...')).toBeTruthy();
    unmount();
  });

  it('shows the coming soon message', () => {
    const { unmount } = render(() => <LibraryView />);
    expect(screen.getByText('Source Library Coming Soon')).toBeTruthy();
    unmount();
  });

  it('displays planned features list', () => {
    const { unmount } = render(() => <LibraryView />);
    expect(screen.getByText('PLANNED FEATURES')).toBeTruthy();
    expect(screen.getByText(/Save and organize sources/)).toBeTruthy();
    unmount();
  });
});
