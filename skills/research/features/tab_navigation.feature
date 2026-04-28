Feature: Tab Navigation
  As a user
  I want to switch between Dashboard, Sessions, Library, and Settings tabs
  So that I can access different sections of the app

  Background:
    Given the Research Hub application is running

  Scenario: Default tab is Dashboard
    Then the Dashboard tab should be active
    And the dashboard content should be visible
    And the search input should be visible

  Scenario: Switch to Sessions tab
    When the user clicks the "Sessions" tab
    Then the Sessions tab should be active
    And the sessions list should be visible
    And the Dashboard content should be hidden

  Scenario: Switch to Library tab
    When the user clicks the "Library" tab
    Then the Library tab should be active
    And the library content should be visible

  Scenario: Switch to Settings tab
    When the user clicks the "Settings" tab
    Then the Settings tab should be active
    And the settings content should be visible

  Scenario: Active search persists during tab switching
    Given a search is currently in progress
    When the user switches to the Sessions tab
    And then switches back to the Dashboard tab
    Then the active search should still be running
    And the progress should reflect the current state
