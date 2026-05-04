Feature: Search Workflow
  As a researcher
  I want to execute searches with different depth modes
  So that I can discover relevant sources efficiently

  Background:
    Given the Research Hub application is running
    And the user is on the Dashboard tab

  Scenario: Quick search returns results
    When the user types "rust async patterns" in the search input
    And selects "quick" search mode
    And clicks the search button
    Then a new session should be created with status "searching"
    And progress events should stream to the UI
    And at least 1 source should appear in the results
    And the session cost should be displayed

  Scenario: Deep search discovers more sources
    When the user types "kubernetes scaling strategies" in the search input
    And selects "deep" search mode
    And clicks the search button
    Then a new session should be created with mode "deep"
    And the search should execute multiple turns
    And the confidence score should increase across turns
    And more sources should be discovered than a quick search

  Scenario: Search results display source metadata
    Given a completed search session exists
    When the user views the session results
    Then each source should display a title
    And each source should display a URL
    And each source should display a relevance score
    And each source should display a source type badge

  Scenario: Empty search query is rejected
    When the user leaves the search input empty
    And clicks the search button
    Then no session should be created
    And the search input should show a validation hint
