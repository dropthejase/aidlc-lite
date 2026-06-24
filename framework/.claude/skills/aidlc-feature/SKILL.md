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

If there is **no `docs/`**, run `aidlc-discover` first. If there is **no codebase at all**, run `aidlc-init` → `aidlc-plan`.

## Welcome Message
Send this first:

```
-------------------------------------------------------
**AI-DLC · FEATURE — let's extend what you've built!**
-------------------------------------------------------

A feature is a child of a unit. We'll find the unit this belongs to, add the new
requirement to its spec, design, and tasks as a new epic, then build it with
generate-evaluate. If it turns out to be a whole new slice, we'll switch to
planning a new unit instead. You approve at every gate.
```

## Steps

### Step 1: Is this really a feature?
A feature **extends one already-built unit**. Load the living docs and unit list to place the request against what exists:
- `docs/architecture.md`, `docs/code-structure.md`, `docs/apis.md`, `docs/data-dictionary.md`, `docs/adr.md`
- Units under `.aidlc/` and which are `status: complete` — candidate host units.

Route:
- **Extends a built unit** → feature. Continue to Step 2.
- **New slice** (new subsystem, service, or page) → not a feature. Tell the user to run `aidlc-plan` then `aidlc-generate-evaluate`. Stop.
- **Host unit not built yet** → build it first via `aidlc-generate-evaluate`.
- **Ambiguous / spans two units** → present options and ask.

### Step 2: Clarify the feature and confirm the host unit
Act as a senior product manager. Clarify what the feature adds, who it's for, and which existing behaviour it touches. **DO NOT GUESS OR ASSUME. IF IN DOUBT, ASK.**

Provide a concise summary and gate it:
```
**Feature:** one sentence — what it adds and for whom.
**Host unit:** the unit it extends, and why.
**New requirements:** bulleted list (FRs / edge cases).
**Touches:** existing components/files it will change (from the living docs).
**Acceptance criteria:** how we'll know it works (Given/When/Then).
```

**GATE** — iterate until the user explicitly approves scope and host unit.

### Step 3: Amend the host unit's plan
The unit was built around its existing epics (`F1: …`); add the feature as a **new epic** (`F2: …`, `F3: …`) so the original build's record stays intact. Read the host unit's current `spec.md`, `design.md`, and `tasks.md` first — you are extending them, not rewriting what's built.

Load the planning guides relevant to the feature (skip what doesn't apply):
- `.claude/references/requirements/requirements-guide.md`
- `.claude/references/requirements/functional-design-guide.md`
- HTTP/API changes: `.claude/references/design/api-design.md` and `.claude/references/security/api-security.md`
- LLM/AI component: `.claude/references/security/ai-security.md`
- User-facing UI: `.claude/references/design/ux-guide.md`

Amend each file as a new epic — **GATE after each one**, user must explicitly confirm before proceeding:

1. **`spec.md`** — add new FRs, edge cases, and ACs under the new epic heading. Leave existing requirements untouched.
2. **`design.md`** — add a new epic section: components extended, new interfaces, data changes. Reuse existing patterns; surface new decisions for `adr.md`.
3. **`tasks.md`** — append tasks under the new epic, all `not_started`. Each task names real files it will create/modify (verified against `docs/code-structure.md`, not guessed) and what its tests should prove. Leave `done` tasks untouched.

Then mark the unit as having unbuilt work: set `status: in-progress` in `spec.md` frontmatter and bump `last-updated: {now}` in all three files.

### Step 4: Update the living docs
Report what each affected doc will change and **ask the user to confirm before writing**:
- `docs/code-structure.md` — components/modules added or changed.
- `docs/apis.md` — endpoints or interfaces added/changed.
- `docs/data-dictionary.md` — new entities or fields.
- `docs/adr.md` — any decision taken planning this feature not already recorded.
- `docs/architecture.md` — only if a component boundary or the high-level shape changed.

### Step 5: Hand off to build
> Feature planned. The {unit} unit now has unbuilt tasks for it. Ready to build? Run `aidlc-generate-evaluate` to build the {unit} unit — it will build only the new tasks.

**DO NOT START BUILDING AUTOMATICALLY.**

## Best Practices
- A feature amends an existing unit, never creates one — new slices are `aidlc-plan`'s job.
- Plan, don't build — this skill writes the plan delta, never application code.
- Extend, don't rewrite — add a new epic; leave built requirements and done tasks intact.
- Plan against reality — read the living docs and the actual code; tasks must name real files, verified not guessed.
- Living docs are gated — report, confirm, then write. Never edit them silently.
