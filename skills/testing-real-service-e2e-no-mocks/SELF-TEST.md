# Self-Test: testing-real-service-e2e-no-mocks

## Positive Triggers (MUST activate)

- "Replace mocked tests with real database tests"
- "Mock-free testing" / "no mock" / "without mocks"
- "Transaction rollback isolation"
- "testcontainers"
- "Test data factory" / "fishery" / "faker"
- "Real API integration tests"
- "REAL_API_TESTS" / "TEST_DATABASE_AVAILABLE"
- "Stripe test mode" / "PayPal sandbox" for testing
- "Structured test logging" / "JSON-line test output"
- "This mock is hiding bugs"
- "Test against real database"
- "sqlx::test"
- "withTestTransaction"
- "How do I set up integration tests with a real Postgres?"

## Negative Triggers (MUST NOT activate)

- "Snapshot test this output" (use /testing-golden-artifacts)
- "Find crashes in this parser" (use /testing-fuzzing)
- "Oracle problem" (use /testing-metamorphic)
- "Compare against reference impl" (use /testing-conformance-harnesses)
- "E2E browser testing" / "Playwright" (use /e2e-testing-for-webapps)
- "Unit test this pure function" (standard testing — mocks OK for pure functions)

## Boundary Cases

- "Integration testing" → Activate (this IS integration testing)
- "E2E testing" → Activate if testing API/service endpoints; use /e2e-testing-for-webapps if browser-based
- "Test this webhook handler" → Activate (real webhook simulation is core pattern)
- "Database testing" → Activate
- "How do I test billing flows?" → Activate (Stripe test mode is core pattern)
