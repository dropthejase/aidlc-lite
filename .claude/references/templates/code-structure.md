# Code Structure Template

## Purpose
Maps responsibilities to code: where each component lives and what its public surface is. Lets an agent locate the right file and judge whether a change is safe before editing.

## Template

```markdown
# Code Structure

**Last Updated:** [YYYY-MM-DD HH:MM:SS]

## Repo Structure
[Annotated tree — top 2-3 levels, one line per dir on its role. Not an exhaustive listing.]

## Components
[Logical groupings of files with one responsibility. Public surface = the contract other code depends on.]

| Component | Location | Responsibility | Public surface |
|-----------|----------|----------------|----------------|
| OrderService | `src/orders/service.ts`, `pricing.ts` | Order lifecycle, pricing | `createOrder()`, `getOrder()` |
| AuthMiddleware | `src/shared/auth/` | JWT verify, request scoping | `requireAuth()` |

## Shared Resources
[Resources multiple components touch. Name the single owner that establishes each one's
properties (dimensions, initial state, lifecycle); consumers depend on them, never set them.
Omit the section if nothing is shared.]

| Resource | Owner (sets it up) | Properties the owner fixes | Consumers |
|----------|--------------------|-----------------------------|-----------|
| `<canvas#game>` | shell | width/height, mount/teardown | each game (reads dimensions) |

## Potential Technical Debt
| Item | Location | Impact | Suggested fix |
|------|----------|--------|---------------|
| Pricing logic duplicated | `orders/`, `cart/` | totals drift | extract shared PricingRules |

## Gaps / Uncertainties
[What the code does not reveal — record the unknown, not a guess. Empty table if nothing.]

| Gap | Area | Why unresolved | How to resolve |
|-----|------|----------------|----------------|
| Auth token TTL not in code | `src/auth/` | injected at deploy, not in repo | confirm with infra / env config |
| Payment retry behaviour unclear | `services/billing` | hidden in external SDK | read SDK docs or ask owner |
```

## Guidelines

### When to update
- At **unit completion**, when files moved, a component was added/removed, a public surface changed, or structural debt was introduced. Update only the rows you touched.

### Format
- Repo Structure lists roles, not a full file listing — readers open the tree for detail.
- Public surface is the contract other code depends on — changing it is high-risk; files not in it are internal and safe to change.
- If a contract says a resource is "already set up," name who sets it up and to what (Shared Resources) — an asserted state with no named owner is the classic integration gap: every consumer assumes someone else did it, and no unit's tests catch the hole.
- No reverse-dependency ("used by") column: before changing a public surface, find-references on the symbol (e.g. `grep -rn`) for the live blast radius. This stays accurate; a hand-maintained edge list rots.
- Technical Debt here is structural/architectural; individual defects go in [bugs.md](./bugs.md).
- Technical Debt vs Gaps: debt is a **known problem** you understand and could fix (resolution = change the code). A gap is a **missing understanding** — the repo does not reveal how something works (resolution = acquire information: ask an owner, read external docs, inspect runtime config). Do not file an uncertainty as debt; a future agent would read it as "known-bad, safe to refactor" and may change behaviour it never understood.
- Gaps: record the unknown, never a guess. "Why unresolved" should say whether the answer is simply absent from the repo (config, external, deploy-time) or needs a human — so the reader knows if more searching would even help.
