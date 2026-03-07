Feature: CLI TUI Interface
  As a developer
  I want to use the research CLI with a terminal UI
  So that I can run research from the command line

  Background:
    Given the research CLI is installed

  Scenario: TUI renders search progress
    When the user runs "research search rust concurrency"
    Then the TUI should display a progress indicator
    And backend events should appear in real-time
    And source discoveries should be listed as they arrive
    And the final summary should show total sources and cost

  Scenario: Search with custom depth
    When the user runs "research search --depth 1 quick query"
    Then the search should use the quick/brave backend
    When the user runs "research search --depth 3 deep query"
    Then the search should use the deep/valyu backend

  Scenario: CLI help displays correctly
    When the user runs "research --help"
    Then the help output should list available subcommands
    And the help should show search, status, and history commands
    And global flags --fullscreen and --debug should be listed

  Scenario: Status command shows current session
    Given a search session was recently completed
    When the user runs "research status"
    Then the TUI should display the session status
    And it should show the confidence score and source count

  Scenario: History command lists recent sessions
    When the user runs "research history -n 5"
    Then the TUI should display up to 5 recent sessions
    And each entry should show query, status, and cost

  Scenario: Graceful quit during search
    Given a search is in progress in fullscreen mode
    When the user presses Ctrl+C or 'q'
    Then the TUI should exit cleanly
    And the terminal should be restored to its original state
    And partial results should be saved
