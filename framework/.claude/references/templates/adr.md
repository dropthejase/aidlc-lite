# Architecture Decision Log Template

## Purpose
The chronological record of *why* — decisions that had a real alternative, what was chosen, and what was rejected. Stops settled choices being re-litigated or silently reversed.

## Template

```markdown
# Architecture Decision Log

**Last Updated:** [YYYY-MM-DD HH:MM:SS]

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 001 | Use PostgreSQL for persistence | Accepted | 2026-06-17 |
| 002 | JWT for API authentication | Superseded by 005 | 2026-06-17 |

---

## ADR-001: Use PostgreSQL for persistence
**Status:** Accepted  •  **Date:** 2026-06-17

**Context:** [The requirement/constraint that forced a choice]
**Decision:** [What we chose]
**Alternatives:** [What we rejected, and the one-line reason]
**Consequences:** [Trade-offs accepted — including the downsides]
```

## Guidelines

### When to update
- At **design sign-off** for a unit (after `design.md` is agreed, before construction). This is the single trigger — same for a first build and for a later change via `aidlc-feature`/`aidlc-fix`.
- Only when a decision had a **real alternative** and is cross-cutting or hard to reverse. Most units add nothing. Implementation shape stays in `unit/design.md`, not here.

### Writing
- Living log — never delete. To reverse a decision, add a new ADR and mark the old one `Superseded by NNN`. The rejected reasoning is what stops a future reader re-litigating it.
- Focus on WHY — the code shows what was built. Be honest about the downsides of the chosen option.
- Keep each entry to the four fields; if it needs more than a short paragraph each, the scope is too broad.
