# Testing Guide

## Test Pyramid

Structure tests in this ratio:
```
         /  E2E  \          ~5%   (slow, expensive, high confidence)
        / Integration \      ~20%  (moderate speed, cross-component)
       /     Unit       \    ~75%  (fast, isolated, high volume)
```

Anti-pattern: the **ice cream cone** (mostly manual/E2E, few unit tests) leads to slow feedback and flaky pipelines.

### Unit Tests
- Test a single function/method/class in isolation
- Mock all external dependencies (database, network, file system)
- Execute in milliseconds; run on every commit
- Follow the arrange-act-assert pattern
- Target: every public function with non-trivial logic
- Naming: `test_[function]_[scenario]_[expected_result]`

### Integration Tests
- Test interactions between two or more components
- Use real dependencies where practical (testcontainers, localstack, test database)
- Execute in seconds; run on every PR
- Target: API endpoints, service-to-repository interactions, message flows
- Focus on contract verification between components

### End-to-End Tests
- Test complete user workflows through the full stack
- Use a deployed or containerised environment
- Execute in minutes; run before release
- Target: critical business workflows only (login, core CRUD, payment)
- Keep count small (20-30 max) — more indicates missing integration coverage

## Test Doubles

| Type | Purpose | Example |
|------|---------|---------|
| **Mock** | Verify interactions (was method X called with args Y?) | `jest.fn()`, `unittest.mock.Mock` |
| **Stub** | Return predetermined data; no interaction verification | Hard-coded return values |
| **Fake** | Working implementation with shortcuts | SQLite or in-memory DB for integration tests |
| **Spy** | Wraps real object; records calls while executing real logic | `jest.spyOn()`, Sinon spies |

- Prefer stubs over mocks — tests stay less coupled to implementation
- Use fakes (LocalStack, testcontainers) for integration tests to increase realism
- Avoid mocking what you do not own; wrap third-party libraries behind an interface and mock the interface

## Specialist Techniques

### Contract Testing
- Verify API consumer expectations match provider implementation
- Consumer writes a contract (expected request/response pairs); provider verifies independently
- Tools: Pact or similar consumer-driven contract frameworks
- Essential for microservices where cross-service integration tests are impractical

### Property-Based Testing
- Define properties that must hold for all valid inputs rather than specific examples
- Tools: Hypothesis (Python), fast-check (TypeScript), QuickCheck (Haskell-inspired)
- Example properties: "serialise → deserialise returns the original value", "sort is idempotent"
- Excellent for finding edge cases that example-based tests miss

### Mutation Testing
- Introduces small code changes and checks whether tests catch them
- A surviving mutant means a gap in test assertions
- Tools: Stryker (JS/TS), mutmut (Python), pitest (Java)
- Use selectively on critical modules — full-codebase mutation testing is expensive

### Security Tests
- **SAST**: Static analysis of source code for known vulnerability patterns
- **DAST**: Dynamic testing of running application (injection, XSS, auth bypass)
- **Dependency scan**: Check third-party packages against CVE databases
- Integrate as a blocking quality gate in CI

### Performance Tests
- **Load**: Expected concurrent users for sustained period — establish baseline
- **Stress**: Increase load until failure — find breaking point
- **Soak**: Sustained load over hours — find memory leaks, connection exhaustion
- Metrics: response time (p50, p95, p99), throughput, error rate, resource utilisation

## Test Data Strategy

- **Factories/Builders**: Generate test objects programmatically with sensible defaults (factory_boy, fishery, @faker-js/faker)
- **Fixtures**: Static data loaded before test suite for reference/lookup data
- **Isolation**: Each test owns its data — never share mutable state between tests
- **Cleanup**: Use database transactions that roll back, or truncate tables in setup
- **Synthetic**: Generated data for performance tests (realistic volume and distribution)
- **PII**: Never copy production data to test environments — mask or synthesise

## Coverage Targets

- **Line coverage**: Baseline target 80%
- **Branch coverage**: More meaningful than line coverage — catches untested conditionals
- **Mutation score**: Gold standard but expensive — use on critical modules only
- Coverage is necessary but not sufficient — 100% coverage with weak assertions catches nothing
- Enforce in CI as a gate: fail the build if coverage drops below threshold

## CI Integration

- Unit tests on every push; gate merges on green
- Integration tests on PR creation and nightly
- E2E tests nightly or on release branches — do not block every PR
- Parallelise test suites to keep total feedback under 10 minutes
- Report results as PR annotations (JUnit XML, GitHub Actions test reporter)
- Track flaky tests explicitly; quarantine or fix within one sprint

## Quality Gates

### Gate 1 — Code Review (before merge)
- All unit tests pass
- No new linter warnings
- Code coverage does not decrease
- Security scan finds no high/critical issues

### Gate 2 — Integration (after merge to main)
- All integration tests pass
- Contract tests pass
- Performance baseline not regressed (>10% degradation = fail)

### Gate 3 — Release Readiness (before deploy)
- All E2E tests pass on staging environment
- No open P0/P1 defects
- Stakeholder acceptance sign-off obtained
