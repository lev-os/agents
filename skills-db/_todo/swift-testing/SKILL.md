---
name: swift-testing
description: Write, migrate, and debug tests using Apple's Swift Testing framework (@Test, #expect, parameterized tests, traits). Use when the user mentions Swift Testing, @Test macro, #expect, parameterized tests, test traits, or migrating from XCTest.
---

# Swift Testing Framework

Apple's modern testing framework replacing XCTest for unit tests. Ships with Xcode 16+ and Swift 6.

## Quick Reference

```swift
import Testing

@Test func basicTest() {
    #expect(2 + 2 == 4)
}

@Test("User can log in with valid credentials")
func loginWithValidCredentials() async throws {
    let result = try await AuthService.login(user: "test", pass: "valid")
    #expect(result.isSuccess)
}
```

## Core Macros

### @Test - Define a test

```swift
// Basic test
@Test func simpleTest() { }

// With display name
@Test("Validates email format correctly")
func emailValidation() { }

// Async test
@Test func asyncOperation() async throws { }

// With traits (see Traits section)
@Test(.enabled(if: ProcessInfo.processInfo.environment["CI"] != nil))
func ciOnlyTest() { }
```

### #expect - Assert conditions

```swift
// Boolean expectation
#expect(value == expected)
#expect(array.isEmpty)
#expect(result != nil)

// With custom message
#expect(count > 0, "Count should be positive")

// Throwing expectation
#expect(throws: ValidationError.self) {
    try validator.validate(invalidInput)
}

// Specific error expectation
#expect(throws: NetworkError.timeout) {
    try await client.fetch(slowEndpoint)
}

// No throw expectation
#expect(throws: Never.self) {
    try safeOperation()
}
```

### #require - Fatal assertions

```swift
// Unwrap optionals (test fails immediately if nil)
let user = try #require(await fetchUser(id: 123))
#expect(user.name == "Alice")

// Boolean requirement (test fails immediately if false)
try #require(database.isConnected)
try #require(file.exists, "Test fixture missing")
```

## Parameterized Tests

Run the same test with multiple inputs:

```swift
@Test(arguments: ["hello", "world", "swift"])
func stringIsNotEmpty(input: String) {
    #expect(!input.isEmpty)
}

@Test(arguments: [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300)
])
func addition(a: Int, b: Int, expected: Int) {
    #expect(a + b == expected)
}

// Zip two collections (paired arguments)
@Test(arguments: zip(["a", "b"], [1, 2]))
func pairedTest(letter: String, number: Int) {
    #expect(!letter.isEmpty)
    #expect(number > 0)
}

// Cartesian product (all combinations)
@Test(arguments: ["light", "dark"], ["iPhone", "iPad"])
func themeDeviceMatrix(theme: String, device: String) {
    // Runs 4 times: light+iPhone, light+iPad, dark+iPhone, dark+iPad
}
```

## Traits

Modify test behavior with traits:

```swift
// Disabled test
@Test(.disabled("Known bug: #123"))
func brokenFeature() { }

// Conditional execution
@Test(.enabled(if: ProcessInfo.processInfo.environment["LIVE_TESTS"] != nil))
func liveAPITest() { }

// Bug reference
@Test(.bug("https://github.com/org/repo/issues/456"))
func workaroundTest() { }

// Tags for filtering
@Test(.tags(.ui, .slow))
func renderingTest() { }

// Time limit
@Test(.timeLimit(.minutes(2)))
func longRunningTest() async { }

// Serial execution (no parallelism)
@Test(.serialized)
func databaseMigrationTest() { }

// Combine traits
@Test(
    "Network timeout handling",
    .tags(.network),
    .timeLimit(.seconds(30)),
    .bug("https://example.com/issue/789", "Flaky on CI")
)
func timeoutTest() async throws { }
```

### Custom Tags

```swift
extension Tag {
    @Tag static var ui: Self
    @Tag static var slow: Self
    @Tag static var network: Self
    @Tag static var integration: Self
}

@Test(.tags(.ui, .slow))
func animationTest() { }
```

## Test Suites (@Suite)

Group related tests:

```swift
@Suite("User Authentication")
struct AuthTests {
    @Test func loginSucceeds() { }
    @Test func loginFailsWithBadPassword() { }
    @Test func logoutClearsSession() { }
}

// Nested suites
@Suite struct NetworkTests {
    @Suite struct RequestTests {
        @Test func getRequest() { }
        @Test func postRequest() { }
    }

    @Suite struct ResponseTests {
        @Test func parseJSON() { }
        @Test func handleError() { }
    }
}

// Suite-level traits (apply to all tests)
@Suite(.serialized)
struct DatabaseTests {
    @Test func migration() { }
    @Test func rollback() { }
}
```

## Setup and Teardown

```swift
@Suite struct ViewModelTests {
    var viewModel: ViewModel!

    // Per-test setup (init runs before each test)
    init() {
        viewModel = ViewModel()
    }

    // Per-test teardown
    deinit {
        viewModel = nil
    }

    @Test func initialState() {
        #expect(viewModel.items.isEmpty)
    }
}

// Async setup
@Suite struct AsyncSetupTests {
    var database: Database

    init() async throws {
        database = try await Database.connect()
    }
}
```

## Confirmation (Async Event Verification)

Wait for async events/callbacks:

```swift
@Test func notificationReceived() async {
    await confirmation { confirm in
        NotificationCenter.default.addObserver(
            forName: .userLoggedIn,
            object: nil,
            queue: .main
        ) { _ in
            confirm()
        }

        await loginUser()
    }
}

// Expected count
@Test func multipleCallbacks() async {
    await confirmation(expectedCount: 3) { confirm in
        for _ in 0..<3 {
            asyncOperation { confirm() }
        }
    }
}
```

## Migrating from XCTest

| XCTest | Swift Testing |
|--------|---------------|
| `class FooTests: XCTestCase` | `@Suite struct FooTests` |
| `func testBar()` | `@Test func bar()` |
| `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTAssertThrowsError(...)` | `#expect(throws: Error.self) { }` |
| `XCTUnwrap(optional)` | `try #require(optional)` |
| `override func setUp()` | `init()` |
| `override func tearDown()` | `deinit` |
| `setUpWithError() async` | `init() async throws` |
| `expectation(description:)` | `await confirmation { }` |

### Migration Example

**Before (XCTest):**
```swift
class UserServiceTests: XCTestCase {
    var service: UserService!

    override func setUp() {
        super.setUp()
        service = UserService()
    }

    func testFetchUserReturnsUser() async throws {
        let user = try await service.fetch(id: 1)
        XCTAssertEqual(user.name, "Alice")
        XCTAssertNotNil(user.email)
    }

    func testFetchInvalidUserThrows() async {
        do {
            _ = try await service.fetch(id: -1)
            XCTFail("Expected error")
        } catch {
            XCTAssertTrue(error is UserError)
        }
    }
}
```

**After (Swift Testing):**
```swift
@Suite struct UserServiceTests {
    let service = UserService()

    @Test func fetchUserReturnsUser() async throws {
        let user = try await service.fetch(id: 1)
        #expect(user.name == "Alice")
        #expect(user.email != nil)
    }

    @Test func fetchInvalidUserThrows() async {
        #expect(throws: UserError.self) {
            try await service.fetch(id: -1)
        }
    }
}
```

## Running Tests

### Xcode
- Cmd+U: Run all tests
- Click diamond in gutter: Run single test
- Test Navigator (Cmd+6): Browse and run

### Command Line
```bash
# Run all tests
swift test

# Run specific test
swift test --filter "UserServiceTests/fetchUser"

# Run tagged tests
swift test --filter ".tags(.network)"

# Parallel execution (default)
swift test --parallel

# Serial execution
swift test --no-parallel
```

## Best Practices

1. **Use descriptive names** - `@Test("Login fails with expired token")` over `@Test func testLoginFail()`

2. **Prefer #expect over #require** - Use `#require` only when subsequent assertions depend on the unwrapped value

3. **Parameterize repetitive tests** - Don't copy-paste tests with different inputs

4. **Tag for CI filtering** - Use `.tags(.slow)` for tests to skip in fast feedback loops

5. **Keep suites focused** - One suite per logical unit (ViewModel, Service, etc.)

6. **Avoid shared mutable state** - Struct suites with `init()` > class with setUp()

## Common Gotchas

- **Mixing frameworks**: Swift Testing and XCTest can coexist but don't share state
- **No setUp/tearDown**: Use `init`/`deinit` instead (or async `init`)
- **Parallel by default**: Tests run concurrently unless `.serialized` applied
- **#expect vs #require**: `#expect` logs and continues; `#require` halts the test
- **Confirmation timeout**: Default is 60 seconds; use `timeout:` parameter for slower operations
