# Code Analysis Checklist

Used by the reviewer to assess generated or modified code.

## Naming & Readability

- [ ] Variables and functions are self-documenting — no abbreviations, no misleading names
- [ ] Booleans use `is`/`has`/`can` prefix
- [ ] Functions use verb + noun

## Documentation

- [ ] New files have a module-level docstring describing purpose and responsibilities
- [ ] Public functions and classes have docstrings where intent isn't obvious
- [ ] Functions and parameters are typed

## Function Design

- [ ] Functions are focused and reasonably sized — no obvious bloat or mixed responsibilities
- [ ] Guard clauses used to reduce nesting

## Structure

- [ ] One primary export per file
- [ ] Organised by feature not layer
- [ ] No duplicate logic, no circular dependencies

## Error Handling

- [ ] Errors propagated with context — never swallowed silently
- [ ] I/O operations have explicit error handling
- [ ] User-facing errors reveal no internal details

## Logging

- [ ] Key operations logged at appropriate level (start, success, failure)
- [ ] No sensitive data logged (passwords, tokens, PII)
- [ ] Structured format with correlation ID where applicable

## Security

- [ ] No hardcoded credentials, magic numbers, or URLs
- [ ] Security checklist passed — see `references/security/security-baseline.md` (includes AI and API extensions)

## Testing

- [ ] Tests accompany all new code — see `references/qa/testing-guide.md`
- [ ] Existing integration tests pass — no regressions
- [ ] Build compiles cleanly (e.g. `tsc --noEmit`, `cargo check`)
- [ ] No shared mutable state between tests

## Technical Debt

- [ ] No TODO/FIXME left untracked
- [ ] No suppressed linter warnings
- [ ] No dead code or commented-out blocks
