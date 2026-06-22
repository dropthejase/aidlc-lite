---
name: aidlc-plan
description: Use on a greenfield project (scaffolded by aidlc-init, no code yet) to turn an idea into a buildable plan. Clarifies intent, agrees an architecture, decomposes the work into units, and writes a spec, design, and tasks for each unit. Ends at planning — it does not write application code. Run after aidlc-init.
---

# PLAN

Turn an idea into a buildable plan for a greenfield project. You clarify what is being built, agree an architecture, decompose it into units, and write each unit's `spec.md` → `design.md` → `tasks.md`. You stop at planning — building is the next skill's job (`aidlc-generate-evaluate`).

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`. Plan assumes `aidlc-init` has scaffolded the `docs/` templates and `.aidlc/` — if they are missing, run `aidlc-init` first.

## Welcome Message
Send the following first to the user:

```
   █████╗ ██╗      ██████╗ ██╗      ██████╗
  ██╔══██╗██║      ██╔══██╗██║     ██╔════╝
  ███████║██║█████╗██║  ██║██║     ██║
  ██╔══██║██║╚════╝██║  ██║██║     ██║
  ██║  ██║██║      ██████╔╝███████╗╚██████╗
  ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝ ╚═════╝

  AI-Driven Lifecycle Development

  ════════════════════════════════════════════════════════════════════
   PLAN — let's turn your idea into a buildable plan.

   We'll talk through what you're building and agree an architecture,
   break it into units, then write a spec, design, and tasks for each.
   No code yet — that comes next. You approve at every gate.
  ════════════════════════════════════════════════════════════════════
```

## Steps

### Step 1: Gather requirements until you are 95% confident of the user's goal
You will act as a senior product manager.

First read the standards this step works to — they define what "good" looks like here, so read them before producing anything:
- `.claude/references/requirements/requirements-guide.md` — FR / NFR / edge-case / acceptance-criteria standards.
- `.claude/references/requirements/product-guide.md` — who the product is for and what is valuable: personas, user stories, and slicing.

Through discussion with the user, you will need to clarify the purpose, persona(s), user stories, functional and non-functional requirements, constraints, and success criteria.

If applicable, provide a list of questions in the following format:
```
**Q1 Question Text**
```
or multiple choice
```
**Q1 Question Text**
**A** Option
**B** Option
**C** Option
**D** Option
**E** Other (append with free text)
```

**DO NOT GUESS OR ASSUME. IF IN DOUBT, ASK FOR CLARIFICATION**

Once you are confident you have gathered sufficient information, provide a concise summary in the following format:
```
**Goal:** one sentence — the problem and who it's for.
**Personas:** the personas it serves.
**User Stories:** bulleted list.
**Assumptions**: bulleted list.
**Constraints**: anything non-negotiable (tech, regulatory, budget).
**Features:** bulleted list.
**Success criteria:** how we'll know it works.
**Edge cases:** bulleted list.
**Roadmap:** features explicitly deferred or out of scope for now, as agreed with the user. Leave empty if none were discussed — **never invent a roadmap.**
```

The roadmap captures only what the user actually deferred in discussion. Do not populate it with features they didn't ask for or guess where the product is heading; an empty roadmap is correct when nothing was deferred.

**GATE** Ask user explicitly for approval. Otherwise iterate the above summary or ask more questions until you reach an agreement.

Once agreed, create an `.aidlc/{yyyymmdd-hhmmss}-{1-3 word snake case description of app}-notes.md` and jot down your notes.

Then tell the user "Let's move on to high-level architecture design!"

### Step 2: Agree the high-level architecture and units
You will act as a senior architect. You will break try to break down the **Step 1** output into independent units.

First read `.claude/references/design/architecture-patterns.md` — how to choose an architectural style and weigh its trade-offs.

Now move from problem to solution. Propose **2-3 architectural approaches** with brief trade-offs and a recommendation: components and boundaries, data, key interfaces, and the security posture (read `.claude/references/security/security-baseline.md` for the baseline).

Always recommend the production-grade, best-practice option — security-first by default. If the user asks for a cheaper or quicker shortcut, you may present it, but name the trade-off plainly and say what it costs; never let "just a POC" silently lower the bar.

With an architecture agreed, decompose it into units. A unit is the smallest slice that can be **built and verified on its own**, split on the architecture's real seams. Pick the coarsest decomposition that stays workable:
- **Small or medium app → one unit** for the whole thing. Do not split work that builds and verifies fine as a single slice.
- **Large app → multiple units**, split on real seams (independently deployable services or packages), sequenced by dependency so each unit builds on completed ones.

Once the architecture is agreed, present the units in the following format:
```
**Architecture:** the chosen approach, in a sentence.
**Units:** the slices, in dependency order.
- {unit name} — what it covers; depends on {earlier unit | nothing}.
```

**GATE** Ask the user explicitly for approval of the architecture and unit list. Otherwise iterate or ask more questions until you reach an agreement.

Once agreed, jot the architecture and unit list into your notes file from Step 1.

Then tell the user "Let's plan the units!"

### Step 3: Plan each unit
Plan units in dependency order. First, recall your notes file from Steps 1-2 — the requirements, architecture, and unit list are your source of truth here.

Load the following guides:
- `.claude/references/design/ddd-patterns.md` — domain modelling and bounded contexts.
- `.claude/references/requirements/functional-design-guide.md` — modelling business rules.
- If a unit fixes an HTTP/API contract: `.claude/references/design/api-design.md` and `.claude/references/security/api-security.md`.
- If a unit includes an LLM/AI component: `.claude/references/security/ai-security.md`.
- For user-facing UI: `.claude/references/design/ux-guide.md`.

For each unit, create `.aidlc/<unit>/`, read each .md file in `.claude/references/templates/unit/` (spec, design, tasks), and copy it into `.aidlc/<unit>/`. There is no convo template to copy — the build loop (`aidlc-generate-evaluate`) creates a dated `convo-{timestamp}.md` itself, born with the canonical format; do not seed one.

1. Populate the `spec.md` as if you were a product manager.
2. **GATE:** Ask user to review and explicitly confirm.
3. Populate the `design.md` as if you had a team of architects and security engineers.
4. **GATE:** Ask user to review and explicitly confirm. Surface any architectural decisions that may need user input.
5. Populate the `tasks.md` as if you were project managing the delivery of the unit.
6. **GATE:** Ask user to review and explicitly confirm.

Repeat the above steps within each unit until the user explicitly approves all three files.
This make take several rounds of iteration.

For architectural decisions requiring user input, format as follows:
```
**1. [Decision]**
Short description of the decision.

**Why it matters?** Why it matters.

**Option A: description of option**
(+) 1-3 lines on pros
(-) 1-3 lines on cons

**Option B: description of option**
(+) 1-3 lines on pros
(-) 1-3 lines on cons

**Recommendation:** Your recommendation and why. Prefer the production grade approach. **AVOID WEASEL WORDS**
---
```

Be prepared to expand further if the user requests more information before making an architectural decision.

**IMPORTANT:** Do not guess the pros and cons. Research if required.

### Step 4: Write the living docs
With the plan settled, populate the following living docs:
- `docs/architecture.md`
- `docs/adr.md`
- `docs/apis.md`
- `docs/data-dictionary.md`

These pull the whole plan together across **all** units — the cross-unit, system-level view no single unit's plan holds. (`generate-evaluate` keeps them current as each unit is built.) With one unit this overlaps the unit's own design and may feel repetitive — that's expected; the value shows with multiple units.

**If in doubt about formatting, refer to their counterparts in `.claude/references/templates/`**

### Step 5: Stop and suggest building
Planning is done. Report what now exists (living docs updated, units planned under `.aidlc/`) and **suggest** moving to construction:

> Planning complete. Ready to start building? Run `aidlc-generate-evaluate` to start building!

**DO NOT START BUILDING AUTOMATICALLY.** On the user's go-ahead, hand off to `aidlc-generate-evaluate` for the first unit.

## Best Practices
- Plan, don't build — this skill writes specs and plans, never application code.
- **THINK BIG** - Feel free to suggest additional features that the user may not have thoguht of.
- Do research on similar products if required. Read `.claude/references/requirements/market-research-methods.md` and/or browse the web if required. Add to your `notes.md`.
- One unit unless the app is genuinely too large to build and verify as one slice — prefer fewer, larger units.
- Always recommend the production-grade, best-practice, security-first option — even for a POC. A cheaper shortcut may be offered, but only with its trade-off stated plainly; never let "just a POC" silently lower the bar.
