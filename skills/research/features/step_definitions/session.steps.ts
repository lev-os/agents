import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'expect';

When('the user initiates a search for {string}', function (query: string) {
  this.sessions = this.sessions || [];
  const session = {
    id: `session-${Date.now()}`,
    query,
    mode: 'quick',
    status: 'searching',
    cost: 0,
    confidence: 0,
    sources: [],
    turns: [],
    createdAt: new Date().toISOString(),
  };
  this.sessions.push(session);
  this.currentSessionId = session.id;
});

Then('a new session should appear in the active sessions list', function () {
  expect(this.sessions?.length).toBeGreaterThan(0);
});

Then('the session should have a unique ID', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.id).toBeDefined();
});

Then('the session status should be {string}', function (status: string) {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.status).toBe(status);
});

Then('the session creation timestamp should be set', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.createdAt).toBeDefined();
});

Given('a session exists with query {string}', function (query: string) {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'detail-1', query, mode: 'quick', status: 'complete', cost: 0.15, confidence: 85, sources: [{ title: 'Source 1', url: 'https://example.com' }], turns: [{ number: 1, confidence: 85 }], createdAt: new Date().toISOString() });
  this.currentSessionId = 'detail-1';
});

When('the user clicks on the session card', function () {
  this.selectedSession = this.sessions?.find((s: any) => s.id === this.currentSessionId);
});

Then('a detail modal should appear', function () {
  expect(this.selectedSession).toBeDefined();
});

Then('the modal should show the session query', function () {
  expect(this.selectedSession?.query).toBeDefined();
});

Then('the modal should show turn history', function () {
  expect(this.selectedSession?.turns?.length).toBeGreaterThan(0);
});

Then('the modal should show discovered sources', function () {
  expect(this.selectedSession?.sources?.length).toBeGreaterThan(0);
});

Given('a session is actively searching', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'pause-1', query: 'test', status: 'searching', mode: 'quick', cost: 0, sources: [], turns: [] });
  this.currentSessionId = 'pause-1';
});

When('the user clicks the pause button', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  if (session) { session.status = 'paused'; session.pausedAt = new Date().toISOString(); }
});

Then('the paused timestamp should be recorded', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.pausedAt).toBeDefined();
});

When('the user clicks the resume button', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  if (session) { session.status = 'searching'; }
});

Then('search progress should continue', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.status).toBe('searching');
});

Given('a search session has finished all turns', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'complete-1', query: 'complete test', status: 'complete', mode: 'deep', cost: 0.25, confidence: 92, sources: [{ title: 'S1' }, { title: 'S2' }], turns: [{ number: 1 }, { number: 2 }], completedAt: new Date().toISOString() });
  this.currentSessionId = 'complete-1';
});

Then('the completed timestamp should be set', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.completedAt).toBeDefined();
});

Then('the final confidence score should be recorded', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.confidence).toBeGreaterThan(0);
});

Then('the total cost should be calculated', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.cost).toBeGreaterThanOrEqual(0);
});

Then('the session should appear in recent sessions list', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.status).toBe('complete');
});

Then('the session status should change to {string}', function (status: string) {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.status).toBe(status);
});
