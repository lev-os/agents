Feature: Error Handling and Recovery
  As a user
  I want the app to handle errors gracefully
  So that I can continue working even when services fail

  Background:
    Given the Research Hub application is running

  Scenario: Backend CLI not available falls back to mock
    Given no search CLI tools are installed
    When the user initiates a search
    Then the search should proceed using the mock backend
    And a notice should indicate mock results are being used
    And mock results should still display in the UI

  Scenario: Search timeout handling
    Given a search backend is responding slowly
    When the search exceeds the configured timeout
    Then the session should show an error state
    And the user should be able to retry the search
    And partial results should be preserved if available

  Scenario: Network error during search
    Given the network connection is unavailable
    When the user initiates a search
    Then an appropriate error message should be displayed
    And the session should transition to a failed state
    And the user should be offered a retry option

  Scenario: Recovery after transient error
    Given a search previously failed due to a transient error
    When the user clicks retry
    Then a new search attempt should begin
    And the previous partial results should be available
    And the cost should only reflect successful operations
