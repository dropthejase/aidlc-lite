# API Security

Applies when the application exposes or consumes APIs. Read alongside `security-baseline.md`.

## OWASP API Security Top 10 (2023)

For every API, verify defenses against each category:

1. **API1 — Broken Object Level Authorization (BOLA)**: Enforce server-side ownership checks for every object access. Never trust client-supplied IDs as proof of entitlement. Centralize authorization logic — do not duplicate it per endpoint. Log all failed authorization attempts.

2. **API2 — Broken Authentication**: Implement rate limiting and brute-force protection specifically on auth endpoints (stricter than general rate limits). Use short-lived tokens. Implement account lockout with notification. Never expose session tokens in URLs or logs.

3. **API3 — Broken Object Property Level Authorization (BOPLA)**: Design response schemas to expose only the fields the consumer needs — not the full database row. Validate write payloads field-by-field; reject unexpected fields (no mass assignment). Regularly review and deprecate legacy fields.

4. **API4 — Unrestricted Resource Consumption**: Apply rate limits on every public endpoint. Set max request size, pagination limits, and query depth limits. Alert on consumption patterns inconsistent with normal usage. Implement cost budgets for expensive operations (search, export, AI).

5. **API5 — Broken Function Level Authorization (BFLA)**: Restrict admin and privileged endpoints by role — deny by default. Verify the caller's role before executing any state-changing or elevated operation. Never rely on obscurity (unlisted endpoints are not protected endpoints).

6. **API6 — Unrestricted Access to Sensitive Business Flows**: Identify business-critical flows (checkout, account creation, voting, messaging). Apply velocity limits, CAPTCHA, or step-up authentication to prevent automated abuse. Monitor for bot-like usage patterns.

7. **API7 — Server Side Request Forgery (SSRF)**: Validate and allowlist all outbound URLs derived from user input. Block requests to internal networks (169.254.x.x, 10.x.x.x, 172.16-31.x.x). Disable HTTP redirects for server-initiated requests. Never expose raw server-side errors to the client.

8. **API8 — Security Misconfiguration**: Disable debug endpoints and verbose error messages in production. Set security headers on all API responses. Enforce HTTPS only. Review CORS policy — allow only expected origins. Automate configuration checks in CI.

9. **API9 — Improper Inventory Management**: Maintain a complete inventory of all API endpoints, versions, and owners. Decommission deprecated versions — do not leave them running. Version APIs explicitly; retire old versions on a defined schedule.

10. **API10 — Unsafe Consumption of APIs**: Treat third-party API responses as untrusted input — validate and sanitize before processing. Maintain an inventory of all third-party integrations and review quarterly. Do not forward raw third-party errors to end users.

## API Design Security Patterns

- **Authentication**: Require authentication on all non-public endpoints. Use OAuth2/OIDC for delegated access. Use scoped API keys for service-to-service. Never use query string tokens.
- **Versioning**: Version all APIs from day one (`/v1/`). Never silently break contracts. Maintain an explicit deprecation and sunset policy.
- **Error responses**: Return generic error messages to clients. Log full detail server-side only. Never expose stack traces, SQL errors, or internal paths.
- **Input validation**: Validate type, format, length, and range on every field. Reject requests that fail validation — do not sanitize and proceed silently.
- **Pagination**: Enforce max page size on all list endpoints. Use cursor-based pagination for large datasets to prevent offset attacks.

## API Security Checklist

For code review and design review, verify:
- [ ] Every endpoint requires authentication unless explicitly public
- [ ] Object ownership verified server-side on every request (BOLA)
- [ ] Response schema returns only necessary fields (no over-exposure)
- [ ] Write endpoints reject unexpected fields (no mass assignment)
- [ ] Rate limiting applied to all public endpoints
- [ ] Admin/privileged endpoints restricted by role, deny by default
- [ ] Business-critical flows protected against automated abuse
- [ ] All outbound URLs validated and allowlisted
- [ ] CORS allows only expected origins
- [ ] Debug endpoints and verbose errors disabled in production
- [ ] All API versions inventoried with an assigned owner
- [ ] Third-party API responses validated before processing
- [ ] Security headers set on all API responses
- [ ] Auth endpoints have stricter rate limits than general endpoints
