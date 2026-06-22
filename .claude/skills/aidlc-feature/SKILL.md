---
name: aidlc-feature
description: Use to add a new capability to an existing project that already has living docs (`docs/`) and at least one built unit. A feature is a child of a unit — it amends that unit's spec/design/tasks with a new epic and new unbuilt tasks, never a new unit. Clarifies the feature, locates its host unit, writes the plan delta, updates the living docs, then hands off to aidlc-generate-evaluate to build it. Run on Path C (existing codebase + docs, new capability wanted).
---

# FEATURE

Add a capability to a system that already exists. A **feature is a child of a unit** — it extends a unit that was already built. You locate the host unit, amend its `spec.md` → `design.md` → `tasks.md` with a new epic and new unbuilt tasks, update the living docs, then hand off to `aidlc-generate-evaluate` to build it. You stop at planning — building is the next skill's job.

If the work is a **new slice** rather than an extension of an existing unit, this is not a feature — stop and use `aidlc-plan` to add a unit, then `aidlc-generate-evaluate`.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`. Feature assumes:
- `docs/` living docs exist, and
- at least one unit under `.aidlc/` is built (`status: complete`).

If there is **no `docs/`** (a codebase was never reverse-engineered), run `aidlc-discover` first. If there is **no codebase at all**, this is greenfield — run `aidlc-init` → `aidlc-plan`.

## Welcome Message
Send this first:

```
-------------------------------------------------------
**AI-DLC · FEATURE — let's extend what you've built!**
-------------------------------------------------------

A feature is a child of a unit. We'll find the unit this belongs to, add the new requirement to its spec, design, and tasks as a new epic, then build it with generate-evaluate. If it turns out to be a whole new slice, we'll switch to planning a new unit instead. You approve at every gate.
```

## Steps

### Step 1: Is this really a feature?
A feature **extends one already-built unit** (e.g. "3 lives + pause" extends the `space-invaders` unit). Decide this before any planning — if it's not a feature, the rest of this skill doesn't apply. Load the living docs and the unit list so you can place the request against what exists:
- `docs/architecture.md`, `docs/code-structure.md` — components, boundaries, where things live.
- `docs/apis.md`, `docs/data-dictionary.md` — interfaces and data it may touch.
- `docs/adr.md` — decisions already taken (build on them, don't relitigate).
- the units under `.aidlc/` and which are `status: complete` — these are the candidate host units.

Then route:
- **Extends an existing built unit** → it's a feature. Continue to Step 2 and name that host unit.
- **A new slice that stands on its own** (a new subsystem, service, or page) → **not a feature. STOP and redirect:** tell the user to run `aidlc-plan` to add a unit, then `aidlc-generate-evaluate`. Do not proceed.
- **The unit it would extend isn't built yet** → build that unit first via `aidlc-generate-evaluate`; a feature only extends completed work.
- **Ambiguous / spans two units** → present the options and ask which unit hosts it (or whether to split the work).

### Step 2: Clarify the feature and confirm the host unit
Act as a senior product manager. Through discussion, clarify what the feature adds, who it's for, and which existing behaviour it touches. Use the question format from `aidlc-plan` Step 1 when you need to ask:
```
**Q1 Question Text**
**A** Option
**B** Option
**C** Other (append with free text)
```

**DO NOT GUESS OR ASSUME. IF IN DOUBT, ASK.**

Provide a concise summary and gate it:
```
**Feature:** one sentence — what it adds and for whom.
**Host unit:** the unit it extends, and why.
**New requirements:** bulleted list (FRs / edge cases).
**Touches:** existing components/files it will change (from the living docs).
**Acceptance criteria:** how we'll know it works (Given/When/Then).
```

**GATE** Ask the user explicitly to approve the feature scope and host unit. Iterate until agreed.

### Step 3: Amend the host unit's plan
This is the core of the skill. The unit was built around its existing epics (`F1: …`); the feature is added as a **new epic** (`F2: …`, `F3: …`) so the original build's record stays intact and the new work is clearly delimited. Read the host unit's current `spec.md`, `design.md`, and `tasks.md` first — you are extending them, not rewriting what's built.

Load the planning guides relevant to the feature (skip what doesn't apply):
- `.claude/references/requirements/requirements-guide.md` — FR / edge-case / acceptance-criteria standards.
- `.claude/references/requirements/functional-design-guide.md` — modelling business rules.
- If it changes an HTTP/API contract: `.claude/references/design/api-design.md` and `.claude/references/security/api-security.md`.
- If it adds an LLM/AI component: `.claude/references/security/ai-security.md`.
- If it changes user-facing UI: `.claude/references/design/ux-guide.md`.

Amend each file as a new epic, behind its own gate:

1. **`spec.md`** — add the feature's new FRs, edge cases, and acceptance criteria under a new epic heading. Leave the existing (built) requirements untouched.
   **GATE:** user reviews and explicitly confirms.
2. **`design.md`** — add a new epic section describing how the feature fits the existing design: components it extends, new interfaces, data changes. Reuse existing patterns by default; surface any genuinely new decision for `adr.md`.
   **GATE:** user reviews and explicitly confirms. Surface architectural decisions needing input using the format in `aidlc-plan` Step 3.
3. **`tasks.md`** — append the feature's tasks under a new epic, all `not_started`. Each task names the real files it will create/modify (verified against `docs/code-structure.md` and the code, not guessed) and what its tests should prove. Leave already-`done` tasks as they are.
   **GATE:** user reviews and explicitly confirms.

Then mark the unit as having unbuilt work again, so `aidlc-generate-evaluate` re-detects it as buildable and the timestamps prove the amend came after the original build:
- In `spec.md` frontmatter, set `status: in-progress`.
- Bump `last-updated: {now}` in all three amended files.

### Step 4: Update the living docs
Report what each affected living doc will change and **ask the user to confirm before writing** — never edit living docs silently:
- `docs/code-structure.md` — components/modules the feature adds or changes ownership of.
- `docs/apis.md` — endpoints or interfaces added/changed.
- `docs/data-dictionary.md` — new entities or fields.
- `docs/adr.md` — any decision taken planning this feature not already recorded.
- `docs/architecture.md` — only if a component boundary or the high-level shape changed.

If unsure on formatting, see the counterparts in `.claude/references/templates/`.

### Step 5: Hand off to build
Planning the feature is done. Report what now exists (host unit amended with a new epic + unbuilt tasks, living docs updated) and **suggest** building:

> Feature planned. The {unit} unit now has unbuilt tasks for it. Ready to build? Run `aidlc-generate-evaluate` to build the {unit} unit — it will build only the new tasks.

**DO NOT START BUILDING AUTOMATICALLY.** On the user's go-ahead, hand off to `aidlc-generate-evaluate` for the host unit.

## Best Practices
- A feature is a child of a unit — it amends an existing unit, never creates one. New slices are `aidlc-plan`'s job.
- Plan, don't build — this skill writes the plan delta, never application code.
- Extend, don't rewrite — add a new epic; leave built requirements and done tasks intact, so the original build's record survives.
- Plan against reality — read the living docs and the actual code; tasks must name real files, verified not guessed.
- Security-first, production-grade — a feature is held to the same bar as the original build, even for a small add-on.
- Living docs are gated — report, confirm, then write. Never edit them silently.
