Feature: Session Management
  As a researcher
  I want to manage my research sessions
  So that I can track, pause, resume, and review my work

  Background:
    Given the Research Hub application is running
    And the user is on the Dashboard tab

  Scenario: Create a new session via search
    When the user initiates a search for "machine learning optimization"
    Then a new session should appear in the active sessions list
    And the session should have a unique ID
    And the session status should be "searching"
    And the session creation timestamp should be set

  Scenario: View session detail modal
    Given a session exists with query "distributed systems"
    When the user clicks on the session card
    Then a detail modal should appear
    And the modal should show the session query
    And the modal should show turn history
    And the modal should show discovered sources

  Scenario: Pause and resume a session
    Given a session is actively searching
    When the user clicks the pause button
    Then the session status should change to "paused"
    And the paused timestamp should be recorded
    When the user clicks the resume button
    Then the session status should change to "searching"
    And search progress should continue

  Scenario: Complete session lifecycle
    Given a search session has finished all turns
    Then the session status should be "complete"
    And the completed timestamp should be set
    And the final confidence score should be recorded
    And the total cost should be calculated
    And the session should appear in recent sessions list
