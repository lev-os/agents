Feature: Cost Tracking
  As a researcher
  I want to monitor search costs and budget usage
  So that I can manage my research spending

  Background:
    Given the Research Hub application is running
    And the user is on the Dashboard tab

  Scenario: Display per-session cost
    Given a session is in progress
    Then the session card should display the current cost
    And the cost should update as new turns complete
    And the cost should be formatted in USD

  Scenario: Daily budget bar shows usage
    Given the daily summary is visible
    Then the budget bar should show total spend vs budget
    And the bar should visually indicate the percentage used
    And the numeric values should be displayed

  Scenario: Budget threshold alert
    Given the daily spend has exceeded 80% of the budget
    Then a warning indicator should appear
    And the budget bar should change color to indicate high usage

  Scenario: Cost accumulates across turns
    Given a deep search session is running
    When turn 1 completes with cost $0.10
    And turn 2 completes with cost $0.15
    Then the session total cost should be $0.25
    And the daily summary cost should include both turns
