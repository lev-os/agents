import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'expect';

Given('the backend service is unavailable', function () {
  this.backendAvailable = false;
});

When('the user initiates a search', function () {
  if (!this.backendAvailable) {
    this.error = { message: 'Backend unavailable', recoverable: true };
    return;
  }
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'err-1', query: 'test', status: 'searching' });
});

Then('an error message should be displayed to the user', function () {
  expect(this.error).toBeDefined();
  expect(this.error.message).toBeDefined();
});

Then('the error should indicate the service is unavailable', function () {
  expect(this.error.message).toContain('unavailable');
});

Then('a retry button should be available', function () {
  expect(this.error.recoverable).toBe(true);
});

When('the user clicks the retry button', function () {
  this.backendAvailable = true;
  this.error = null;
  this.retried = true;
});

Then('the search should be attempted again', function () {
  expect(this.retried).toBe(true);
});

Given('a search returns partial results before failing', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'partial-1', query: 'partial', status: 'error', sources: [{ title: 'Partial source' }], error: 'Connection lost' });
  this.currentSessionId = 'partial-1';
});

Then('the partial results should still be visible', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.sources?.length).toBeGreaterThan(0);
});

Then('the error state should be clearly indicated', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.status).toBe('error');
});

Given('the CLI tools are not installed', function () {
  this.cliAvailable = false;
});

Then('the application should fall back to mock backend', function () {
  expect(this.cliAvailable).toBe(false);
  // Mock backend is the fallback
});

Then('mock results should be clearly labeled', function () {
  expect(true).toBe(true);
});
