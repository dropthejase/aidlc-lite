# Code Generation

## General Principles (All Frameworks)

1. Scan existing code for conventions before generating new code
2. Match the project's import style (named vs. default, absolute vs. relative)
3. Follow the project's directory structure conventions
4. Use the project's established error handling pattern
5. Match existing naming conventions (camelCase, snake_case, PascalCase)

## Implementation Pattern Selection

Choose patterns based on the problem domain:

| Pattern | When to Use | Avoid When |
|---------|-------------|------------|
| **Repository** | Abstracting data access, multiple storage backends | Single database, simple CRUD only |
| **Service Layer** | Coordinating business logic across multiple repositories | Logic fits in a single model method |
| **Factory** | Complex object creation, conditional construction logic | Simple constructor suffices |
| **Strategy** | Runtime behavior variation (e.g., payment processing, notifications) | Only one algorithm exists |
| **Observer/Event** | Decoupling side effects from core logic (email, logging, cache invalidation) | Synchronous response required from all handlers |
| **Middleware/Pipeline** | Cross-cutting concerns (auth, logging, validation, rate limiting) | Single-purpose request handling |
| **Adapter** | Wrapping external APIs/SDKs behind a stable internal interface | Internal-only code with no external dependencies |

## Coding Standards

See [code-generation-patterns.md](./code-generation-patterns.md)

## Verification

- Update existing tests to cover the changed behavior
- Add new tests for new behavior, ensuring they comply with [testing-guide.md](../qa/testing-guide.md)
- Check that the code compiles
