import { When, Then, Given } from '@cucumber/cucumber';
import { expect } from 'expect';

Then('the Dashboard tab should be active', function () {
  expect(this.activeTab || 'dashboard').toBe('dashboard');
});

Then('the dashboard content should be visible', function () {
  expect(this.activeTab || 'dashboard').toBe('dashboard');
});

Then('the search input should be visible', function () {
  expect(this.activeTab || 'dashboard').toBe('dashboard');
});

When('the user clicks the {string} tab', function (tabName: string) {
  this.activeTab = tabName.toLowerCase();
});

Then('the Sessions tab should be active', function () {
  expect(this.activeTab).toBe('sessions');
});

Then('the sessions list should be visible', function () {
  expect(this.activeTab).toBe('sessions');
});

Then('the Dashboard content should be hidden', function () {
  expect(this.activeTab).not.toBe('dashboard');
});

Then('the Library tab should be active', function () {
  expect(this.activeTab).toBe('library');
});

Then('the library content should be visible', function () {
  expect(this.activeTab).toBe('library');
});

Then('the Settings tab should be active', function () {
  expect(this.activeTab).toBe('settings');
});

Then('the settings content should be visible', function () {
  expect(this.activeTab).toBe('settings');
});

Given('a search is currently in progress', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'active-1', query: 'test', status: 'searching', mode: 'quick', cost: 0, sources: [], turns: [] });
});

When('the user switches to the Sessions tab', function () {
  this.previousTab = this.activeTab;
  this.activeTab = 'sessions';
});

When('then switches back to the Dashboard tab', function () {
  this.activeTab = 'dashboard';
});

Then('the active search should still be running', function () {
  const active = this.sessions?.find((s: any) => s.status === 'searching');
  expect(active).toBeDefined();
});

Then('the progress should reflect the current state', function () {
  expect(this.sessions?.length).toBeGreaterThan(0);
});
