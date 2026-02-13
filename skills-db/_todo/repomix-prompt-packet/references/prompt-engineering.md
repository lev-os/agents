# Prompt Engineering for Code Analysis

## Core Principles

### 1. Context Primer First

Always begin prompts with 2-3 sentences establishing:
- What the codebase does (domain/purpose)
- Key technologies and frameworks
- Architectural patterns or notable approaches

**Why:** LLMs perform better with upfront context that frames subsequent analysis.

**Example:**
```
This is an e-commerce platform backend built with Node.js, Express, and PostgreSQL.
It follows clean architecture principles with distinct layers for routes, use cases,
and data access. The codebase uses dependency injection via InversifyJS.
```

---

### 2. Specificity Over Generality

Vague prompts produce vague results. Be explicit about:
- Exact goals and deliverables
- Scope boundaries
- Output format expectations
- Success criteria

**Bad:** "Review this code"
**Good:** "Review authentication implementation for security vulnerabilities, specifically checking for: 1) SQL injection in login queries, 2) proper password hashing, 3) session management weaknesses. Provide findings with severity ratings and code examples."

---

### 3. Constraint Declaration

When standards, patterns, or preferences matter, state them explicitly:
- Coding standards to follow
- Architectural patterns to maintain
- Libraries or approaches to prefer/avoid

**Example:**
```
When suggesting refactoring:
- Maintain existing TypeScript strict mode compliance
- Prefer functional patterns over class-based
- Follow existing error handling patterns using Either<Error, Result>
- Avoid introducing new dependencies
```

---

### 4. Guidance for Analysis Approach

Help the LLM analyze effectively by suggesting:
- Where to start the analysis
- What to prioritize
- How to structure the response

**Example:**
```
Analyze the data flow by:
1. Starting from the API endpoints in src/routes/
2. Tracing through controllers to service layer
3. Identifying database queries in repositories
4. Mapping the complete request→response flow
Highlight any data transformation or validation gaps.
```

---

## Prompt Patterns by Use Case

### Documentation Generation

**Template:**
```
[Context Primer: 2-3 sentences about the codebase]

Based on the provided repository snapshot, generate [type of documentation]
that includes:
1. [Specific element 1]
2. [Specific element 2]
3. [Specific element 3]

Organization: [How to structure the output]
Format: [Desired output format]
Audience: [Who will use this documentation]

[Optional: Example of desired output style]
```

**Concrete Example:**
```
This is a TypeScript REST API for a project management tool, using Express and Prisma ORM.
The API follows RESTful conventions with resource-based routing.

Generate comprehensive API documentation that includes:
1. All endpoints grouped by resource (Projects, Tasks, Users)
2. For each endpoint: HTTP method, path, auth requirements
3. Request/response schemas with example JSON
4. Common error codes and their meanings
5. Rate limiting rules

Organization: Group by resource type, then by CRUD operation
Format: OpenAPI 3.0 YAML specification
Audience: Frontend developers integrating with this API

Include a "Getting Started" section with authentication flow examples.
```

---

### Bug Investigation

**Template:**
```
[Context Primer: Architecture and tech stack]

Problem: [Exact error message or unexpected behavior]
Reproduction: [Steps to reproduce or conditions when it occurs]
Expected: [What should happen]
Actual: [What actually happens]

Analyze the codebase to:
1. Identify root cause
2. Trace the execution path leading to the issue
3. Explain why it's happening
4. Suggest a fix with code examples

Focus on: [Specific areas or patterns to examine]
```

**Concrete Example:**
```
This React + Redux application manages real-time chat functionality. State is
managed via Redux Toolkit with RTK Query for API calls.

Problem: TypeError: Cannot read property 'messages' of undefined
Reproduction: Occurs when navigating to /chat/:roomId after cold start
Expected: Chat messages should load and display
Actual: Blank screen with console error

Analyze the codebase to:
1. Identify where 'messages' is being accessed unsafely
2. Trace the Redux state initialization and API data flow
3. Explain the race condition between routing and data loading
4. Suggest fix ensuring defensive property access and loading states

Focus on:
- Redux slice selectors and their usage in components
- RTK Query hook timing in the ChatRoom component
- React Router route component mounting lifecycle
```

---

### Architectural Planning / Refactoring

**Template:**
```
[Context Primer: Current architecture and pain points]

Goal: [Desired end state or improvement]

Analyze the current architecture and provide:
1. Assessment of [specific architectural concerns]
2. Proposed [solution type] with justification
3. Migration strategy considering [constraints]
4. Risk analysis and mitigation approaches

Constraints:
- [Operational constraints: uptime, performance, etc.]
- [Technical constraints: tech debt, compatibility, etc.]
- [Business constraints: timeline, resources, etc.]

Deliverable format: [How to structure the response]
```

**Concrete Example:**
```
This monolithic Express.js application handles user authentication, content
publishing, and payment processing. It's experiencing scaling issues under load
and deployment complexity as team size grows.

Goal: Decompose into microservices that can scale and deploy independently

Analyze the current architecture and provide:
1. Assessment of coupling points and shared dependencies
2. Proposed service boundaries with clear domain justification
3. Migration strategy prioritizing low-risk extractions first
4. Data consistency approach for distributed transactions

Constraints:
- Zero downtime during migration (500K active users)
- Must maintain existing PostgreSQL database initially
- Team of 6 engineers, can dedicate 2 to migration
- 6-month timeline for first phase

Deliverable format:
- Service boundary diagram with responsibilities
- 3-phase migration roadmap with success metrics
- Data synchronization strategy
- Risk matrix with mitigation plans
```

---

### Code Review

**Template:**
```
[Context Primer: Purpose and tech stack]

Review this codebase for:
1. [Review dimension 1]
2. [Review dimension 2]
3. [Review dimension 3]

For each finding:
- Severity: [Critical | High | Medium | Low]
- Location: [File and function/class]
- Issue: [What's wrong]
- Impact: [Why it matters]
- Recommendation: [How to fix, with code example]

Prioritize: [What matters most in this review]
```

**Concrete Example:**
```
This Python Flask API serves machine learning model predictions with high throughput
requirements. Uses SQLAlchemy ORM and Redis for caching.

Review this codebase for:
1. Security vulnerabilities (injection, authentication, authorization)
2. Performance bottlenecks (N+1 queries, inefficient algorithms, missing indexes)
3. Code quality issues (maintainability, testability, error handling)
4. ML-specific concerns (model versioning, prediction validation, fallback handling)

For each finding:
- Severity: [Critical | High | Medium | Low]
- Location: [File:line or file:function]
- Issue: [Description]
- Impact: [Performance/security/maintainability consequences]
- Recommendation: [Fix with code example]

Prioritize security and performance over style issues. Focus on production-impacting
concerns. Flag any blocking issues for immediate attention.
```

---

### Security Audit

**Template:**
```
[Context Primer: Application type and security context]

Perform security audit focusing on:
1. [Security domain 1: e.g., authentication]
2. [Security domain 2: e.g., data validation]
3. [Security domain 3: e.g., dependencies]

For each vulnerability found:
- OWASP Category: [If applicable]
- Severity: [Critical | High | Medium | Low]
- Location: [Precise code location]
- Attack Vector: [How it could be exploited]
- Impact: [What attacker could achieve]
- Remediation: [Fix with secure code example]

Compliance requirements: [Any relevant standards]
```

**Concrete Example:**
```
This Django web application handles healthcare patient data (PHI) and must comply
with HIPAA requirements. Uses PostgreSQL, Celery for background jobs, and AWS S3
for file storage.

Perform security audit focusing on:
1. Authentication & Authorization (session management, access controls)
2. Data Protection (encryption at rest/transit, PII handling, data retention)
3. Input Validation & Injection Prevention (SQL, XSS, command injection)
4. Dependency Security (outdated packages, known CVEs)
5. API Security (rate limiting, CORS, CSRF protection)

For each vulnerability found:
- OWASP Category: [If applicable]
- HIPAA Impact: [Relevant compliance concern]
- Severity: [Critical | High | Medium | Low]
- Location: [File and line]
- Attack Vector: [Exploitation method with example]
- Impact: [Data exposure risk and compliance violation]
- Remediation: [Fix with secure code + HIPAA alignment]

Compliance: HIPAA Privacy Rule and Security Rule. Flag any potential PHI exposure
immediately as Critical severity.
```

---

### Test Generation

**Template:**
```
[Context Primer: Tech stack and testing approach]

Analyze the [component/module/function] and generate comprehensive test cases
covering:
1. [Test category 1: e.g., happy paths]
2. [Test category 2: e.g., edge cases]
3. [Test category 3: e.g., error conditions]

For each test:
- Test name: [Descriptive name]
- Scenario: [What's being tested]
- Setup: [Test data and mocks needed]
- Assertions: [Expected outcomes]

Test framework: [Jest, pytest, etc.]
Coverage goal: [Percentage or specific paths]
```

**Concrete Example:**
```
This TypeScript module implements JWT authentication with refresh token rotation.
Current test coverage is 45%. Uses Jest and Supertest for testing.

Analyze the authentication service (src/services/AuthService.ts) and generate
comprehensive test suites covering:
1. Successful authentication flows (login, refresh, logout)
2. Edge cases (expired tokens, malformed tokens, concurrent refresh requests)
3. Error conditions (invalid credentials, revoked tokens, rate limiting)
4. Security scenarios (token theft, replay attacks, timing attacks)

For each test:
- Test name: Descriptive, following "should [expected behavior] when [condition]"
- Scenario: Clear explanation of what's being validated
- Setup: Mock data, database state, and external dependencies
- Assertions: Specific expectations for status codes, tokens, side effects

Test framework: Jest with Supertest
Mocking: Use jest.mock() for external services (Redis, database)
Coverage goal: 95%+ line coverage, all security-critical paths tested
Organize: Group by feature (login, refresh, logout) with nested describe blocks
```

---

## Advanced Prompting Techniques

### Chain-of-Thought Guidance

For complex analysis, guide the reasoning process:

```
Before providing recommendations, first:
1. Map all data flows through the system
2. Identify transformation points where bugs could occur
3. Trace the error backward from symptom to source
4. Consider timing and concurrency implications

Then provide your analysis with reasoning shown.
```

**Why:** Explicit reasoning steps improve LLM analysis quality.

---

### Few-Shot Examples

Include examples of desired output:

```
Generate API documentation following this style:

Example:
### POST /api/users
Creates a new user account.

**Authentication:** Required (API Key)

**Request Body:**
\`\`\`json
{
  "email": "user@example.com",
  "name": "John Doe"
}
\`\`\`

**Response (201):**
\`\`\`json
{
  "id": "usr_123",
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
\`\`\`

**Errors:**
- 400: Invalid email format
- 409: Email already registered

Now generate documentation for all endpoints following this exact structure.
```

---

### Structured Output Requests

Request specific output formats:

```
Provide analysis in this exact structure:

## Summary
[2-3 sentence overview of findings]

## Critical Issues
[Issues requiring immediate attention]
- Issue: [Description]
  - Impact: [Consequence]
  - Fix: [Code example]

## Improvements
[Non-critical enhancements]
- Suggestion: [Description]
  - Benefit: [Why it helps]
  - Implementation: [Approach]

## Positive Patterns
[What's working well]
- Pattern: [Description]
  - Why it works: [Explanation]
```

---

### Iterative Refinement Pattern

For large analysis, work progressively:

```
**Phase 1 Prompt:**
"Review the architecture at a high level and identify the top 3 areas of concern.
For each, provide a brief explanation of the risk."

[After receiving response, craft Phase 2 with details]

**Phase 2 Prompt:**
"You identified the authentication layer as high risk. Perform a deep security
audit of src/auth/** focusing on [specific concerns from Phase 1]. Provide
detailed findings with code examples and remediation steps."
```

**Why:** Manages token usage and allows focused deep-dives based on initial findings.

---

## Anti-Patterns to Avoid

### ❌ Vague Requests

**Bad:**
```
Look at this code and tell me what you think.
```

**Why:** Produces generic, unhelpful responses.

**Fix:** Be specific about goals, format, focus areas.

---

### ❌ Assumption Overload

**Bad:**
```
Review for bugs.
```

**Why:** LLM doesn't know:
- What kind of bugs to look for
- What severity matters
- What output format you want
- What context to consider

**Fix:** Specify bug categories, severity levels, output structure, and constraints.

---

### ❌ Missing Context

**Bad:**
```
[Pastes code snapshot with no explanation]

Fix the authentication bug.
```

**Why:** LLM lacks:
- Tech stack knowledge
- Architecture understanding
- Bug symptom details
- Expected behavior

**Fix:** Always include context primer, clear problem statement, reproduction steps.

---

### ❌ Unconstrained Creativity

**Bad:**
```
Redesign this architecture however you think is best.
```

**Why:** Ignores:
- Business constraints
- Team capabilities
- Migration costs
- Existing investments

**Fix:** State constraints, preferences, migration considerations, success criteria.

---

### ❌ Token Waste

**Bad:**
```
Here's my entire codebase (uncompressed). Write complete docs for everything.
```

**Why:**
- Exceeds context limits or wastes tokens
- Lacks prioritization
- No guidance on format

**Fix:** Use compression, focus on specific modules, provide format examples, prioritize.

---

## Prompt Quality Checklist

Before submitting a prompt packet, verify:

- [ ] **Context primer included** (2-3 sentences about codebase)
- [ ] **Goal is specific** (not "review code" but "identify security vulnerabilities in auth layer")
- [ ] **Output format defined** (structure, style, detail level)
- [ ] **Constraints stated** (coding standards, patterns to maintain, things to avoid)
- [ ] **Scope is bounded** (specific files/modules if not full codebase)
- [ ] **Success criteria clear** (what makes a good response)
- [ ] **Examples provided** (if output format is non-standard)
- [ ] **Priority established** (what matters most)
- [ ] **Technical details precise** (exact error messages, file paths, line numbers)
- [ ] **Assumptions minimized** (provide context rather than assuming LLM knows)

---

## Model-Specific Considerations

### Claude (Anthropic)

**Strengths:**
- Excellent at following detailed instructions
- Strong code analysis and reasoning
- Good with long context windows

**Optimization tips:**
- Use XML tags for structured sections: `<context>`, `<task>`, `<constraints>`
- Provide explicit reasoning steps for complex analysis
- Leverage large context window with full snapshots when beneficial

**Example:**
```
<context>
This is a microservices architecture using Go and gRPC...
</context>

<task>
Analyze service-to-service communication patterns and identify potential failure modes...
</task>

<constraints>
- Must maintain backward compatibility
- Cannot introduce new dependencies
- Performance degradation not acceptable
</constraints>
```

---

### GPT-4 (OpenAI)

**Strengths:**
- Strong general knowledge
- Good at creative problem-solving
- Versatile across domains

**Optimization tips:**
- Be very explicit about output format (tends toward verbosity)
- Use system message for persistent constraints
- Provide few-shot examples for consistent formatting

---

### Gemini (Google)

**Strengths:**
- Large context window
- Good at multi-modal tasks
- Strong reasoning capabilities

**Optimization tips:**
- Leverage large context for comprehensive snapshots
- Structure prompts clearly with sections
- Provide examples of desired output

---

## Progressive Enhancement Workflow

Start simple, refine based on results:

**Iteration 1:**
```
Review this authentication implementation for security issues.
```

**After reviewing results, refine:**

**Iteration 2:**
```
Review authentication (src/auth/**) for security, focusing on:
1. Password handling and storage
2. Session management
3. Token validation

Provide findings with severity ratings.
```

**After reviewing results, refine further:**

**Iteration 3:**
```
[Full context primer]

Security audit of authentication system (src/auth/**) checking:
1. Password hashing: bcrypt with sufficient work factor?
2. Session management: secure cookies, proper expiration, CSRF protection?
3. JWT validation: signature verification, expiration checks, revocation?
4. Input validation: email format, password requirements, injection prevention?

For each finding:
- OWASP category
- Severity (Critical/High/Medium/Low)
- Location (file:line)
- Attack vector with example
- Remediation with code

[Constraints section]
```

Track what works and build reusable prompt templates from successful patterns.
