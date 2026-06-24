# APIs Template

## Purpose
The current API surface — endpoints, events, and their contracts. The reference for what callers depend on, so contract changes are made deliberately.

## Template

```markdown
# APIs

**Last Updated:** [YYYY-MM-DD HH:MM:SS]

## Overview
[1-2 lines: what surfaces exist — REST, GraphQL, gRPC, events, internal module APIs]

## [API / Service Name]

**Base path:** `/api/v1`  •  **Auth:** [Bearer JWT / API key / none]  •  **Style:** [REST / GraphQL / RPC]

| Method | Path | Purpose | Auth | Request | Response | Errors |
|--------|------|---------|------|---------|----------|--------|
| POST | `/orders` | Create an order | user | `CreateOrderReq` | `201 Order` | 400, 409 |
| GET | `/orders/{id}` | Fetch one order | user/owner | — | `200 Order` | 404 |

### Schemas
Request/response names map to entities in [data-dictionary.md](./data-dictionary.md) where they match 1:1.
Inline only shapes unique to the wire (envelopes, pagination, filters):

`CreateOrderReq { items: [{ sku: string, qty: int>0 }], couponCode: string? }`

## Events / Async (if any)
| Channel/Topic | Direction | Payload | Trigger | Consumers |
|---------------|-----------|---------|---------|-----------|
| `order.placed` | publish | `OrderPlaced` | order created | inventory, email |
```

## Guidelines

### When to update
- At **unit completion**, when an endpoint or event was added, removed, or changed contract (path, method, request/response shape, auth).

### Format
- One `##` block per logical API/service; one row per endpoint.
- Request/Response columns carry type names that point to data-dictionary entities — inline a shape only when it is API-specific.
- Errors column lists status codes only; state the error convention once at the top of the block.
- Internal module APIs are in scope when they are a stable contract between units.
