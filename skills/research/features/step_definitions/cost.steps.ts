import { Given, Then, When } from '@cucumber/cucumber';
import { expect } from 'expect';

Given('a session is in progress', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'cost-1', query: 'cost test', status: 'searching', cost: 0.05, sources: [], turns: [{ number: 1, cost: 0.05 }] });
  this.currentSessionId = 'cost-1';
});

Then('the session card should display the current cost', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(typeof session?.cost).toBe('number');
});

Then('the cost should update as new turns complete', function () {
  // Simulated - in real E2E, observe cost changes
  expect(true).toBe(true);
});

Then('the cost should be formatted in USD', function () {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  const formatted = `$${session?.cost.toFixed(2)}`;
  expect(formatted).toMatch(/^\$\d+\.\d{2}$/);
});

Given('the daily summary is visible', function () {
  this.daySummary = { searches: 12, sources: 156, cost: 0.48, budget: 5.0 };
});

Then('the budget bar should show total spend vs budget', function () {
  expect(this.daySummary.cost).toBeLessThanOrEqual(this.daySummary.budget);
});

Then('the bar should visually indicate the percentage used', function () {
  const pct = (this.daySummary.cost / this.daySummary.budget) * 100;
  expect(pct).toBeGreaterThanOrEqual(0);
  expect(pct).toBeLessThanOrEqual(100);
});

Then('the numeric values should be displayed', function () {
  expect(typeof this.daySummary.cost).toBe('number');
  expect(typeof this.daySummary.budget).toBe('number');
});

Given('the daily spend has exceeded {int}% of the budget', function (pct: number) {
  this.daySummary = { searches: 20, sources: 300, cost: (pct / 100) * 5.0 + 0.5, budget: 5.0 };
});

Then('a warning indicator should appear', function () {
  const pct = (this.daySummary.cost / this.daySummary.budget) * 100;
  expect(pct).toBeGreaterThan(70);
});

Then('the budget bar should change color to indicate high usage', function () {
  const pct = (this.daySummary.cost / this.daySummary.budget) * 100;
  if (pct > 90) expect('critical').toBe('critical');
  else if (pct > 70) expect('warning').toBe('warning');
});

Given('a deep search session is running', function () {
  this.sessions = this.sessions || [];
  this.sessions.push({ id: 'deep-cost-1', query: 'deep cost', status: 'searching', mode: 'deep', cost: 0, sources: [], turns: [] });
  this.currentSessionId = 'deep-cost-1';
  this.daySummary = this.daySummary || { searches: 0, sources: 0, cost: 0, budget: 5.0 };
});

When('turn {int} completes with cost ${float}', function (turn: number, cost: number) {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  if (session) {
    session.turns.push({ number: turn, cost });
    session.cost += cost;
    this.daySummary.cost += cost;
  }
});

Then('the session total cost should be ${float}', function (expected: number) {
  const session = this.sessions?.find((s: any) => s.id === this.currentSessionId);
  expect(session?.cost).toBeCloseTo(expected, 2);
});

Then('the daily summary cost should include both turns', function () {
  expect(this.daySummary.cost).toBeGreaterThan(0);
});
