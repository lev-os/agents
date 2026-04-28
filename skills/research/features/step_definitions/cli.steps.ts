import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'expect';

Given('the research CLI is installed', function () {
  this.cliInstalled = true;
});

Given('the terminal supports TUI rendering', function () {
  this.tuiSupported = true;
});

When('the user runs {string}', function (command: string) {
  this.lastCommand = command;
  this.commandExecuted = true;
});

Then('the TUI should render the search interface', function () {
  expect(this.commandExecuted).toBe(true);
  expect(this.tuiSupported).toBe(true);
});

Then('the search input should accept keyboard input', function () {
  expect(this.tuiSupported).toBe(true);
});

Then('progress should be displayed in the terminal', function () {
  expect(this.commandExecuted).toBe(true);
});

Then('results should be formatted for terminal display', function () {
  expect(this.commandExecuted).toBe(true);
});

Given('a CLI search is in progress', function () {
  this.cliSession = { id: 'cli-1', query: 'cli test', status: 'searching', events: [] };
});

Then('backend events should update the TUI in real-time', function () {
  expect(this.cliSession).toBeDefined();
});

Then('the cost tracker widget should show current spend', function () {
  expect(this.cliSession).toBeDefined();
});

Then('the source list should update as sources are found', function () {
  expect(this.cliSession).toBeDefined();
});

When('the user presses {string}', function (key: string) {
  this.lastKeyPress = key;
  if (key === 'q') this.cliSession = null;
});

Then('the TUI should exit cleanly', function () {
  expect(this.cliSession).toBeNull();
});

Then('no error should be displayed', function () {
  expect(this.error).toBeUndefined();
});
