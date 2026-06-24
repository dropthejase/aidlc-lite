---
name: aidlc-generate-evaluate
description: Use to build one or more planned units — turns spec/design/tasks into working, reviewed code. You are the coordinator: you build code directly (delegating to builder subagents when tasks are sufficiently independent), then spawn an evaluator subagent each round to review it. Loop until every task passes and acceptance criteria are met, then update the living docs and merge. Run after aidlc-plan (Path A) or aidlc-feature (Path C).
---

# GENERATE-EVALUATE

You are the coordinator. You own quality, you own the loop, you own the gates. Each round: build (directly or via subagents), then spawn an **evaluator** subagent to independently review the result against the spec. The evaluator writes its verdict to `convo-{timestamp}.md`; you read it, fix findings, and loop — until every task passes and every acceptance criterion in `spec.md` is met. Then you update the living docs and merge.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`. This skill assumes planned units — `.aidlc/<unit>/spec.md`, `design.md`, and `tasks.md` must exist. If not, run `aidlc-plan` (greenfield) or `aidlc-feature` (existing codebase) first.

## Welcome Message
Send this first:

```
-------------------------------------------------------
**AI-DLC · GENERATE-EVALUATE — let's build this unit!**
-------------------------------------------------------

You're the coordinator: build the code directly or via subagents, then an
evaluator subagent independently reviews it against the spec each round. We loop
until it passes, verify acceptance criteria, then update the docs and merge.
You approve at every gate.
```

## Steps

### Step 1: Pick the unit(s) and confirm the plan
List units under `.aidlc/`. Identify which are **ready to build now** — `tasks.md` has unbuilt tasks and their dependencies are already built. You may build several ready units at once if none depends on another. If ambiguous, ask.

For each unit, read `spec.md`, `design.md`, and `tasks.md`. Announce a one-line summary per unit.

### Step 2: Set up an isolated workspace per unit
Each unit builds in its own git worktree so parallel runs don't collide.

- **Detect existing isolation** first: if you're already in a dedicated worktree for that unit, reuse it. Never nest a worktree in a worktree.
- Otherwise propose a branch `feature/<unit>` (let the user rename) and **ask consent** to create a worktree off the current integration branch. Prefer the harness's native worktree tool (`EnterWorktree`); fall back to `git worktree add -b feature/<unit> ../<repo>-<unit>` (sibling directory).
- If the user declines isolation, work in place on a `feature/<unit>` branch — never on the integration branch directly.

### Step 3: Build-evaluate loop

Each round:

**3a — Build**

Read the coding references once at the start of round 1:
- `docs/code-structure.md` — component boundaries and where things live.
- `.claude/references/develop/` — coding and testing practices.

Implement all unbuilt tasks (or fix open evaluator findings if round 2+). You can either:
- Implement tasks yourself; OR
- Delegate to builder subagents **only when tasks are sufficiently decoupled** (separate files, no shared state).

Update each task's status in `tasks.md` as you go.

Check it works:
- Run the build and tests; fix anything broken.
- For UI work, use Playwright and/or Chrome DevTools per `.claude/references/qa/browser-testing-guide.md`

Commit on the feature branch with a focused message. Then append a round entry to `convo-{timestamp}.md`:

```
## Round N — Coordinator — [YYYY-MM-DD HH:MM]
**Status:** COMPLETE | COMPLETE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
**Built:** [tasks + one-line what]
**Build/tests:** [build ✓/✗, N/N tests]
**Notes:** [anything for the evaluator to scrutinise]
```

**3b — Evaluate (subagent)**

Spawn the `aidlc-evaluator` subagent with the following prompt:

```
Review unit '<unit>'.
- Plan files: .aidlc/<unit>/spec.md, tasks.md, convo-{timestamp}.md
- The implementation is on branch feature/<unit> in worktree <path>
- Run `git diff $(git merge-base HEAD <integration-branch>) HEAD` to see what was built
- Append your verdict to convo-{timestamp}.md using this exact heading format:

## Round N — Evaluator — [YYYY-MM-DD HH:MM]
**Verdict:** PASS | NEEDS_WORK
**Findings:**
- [Critical] `file:line` — what's wrong; concrete fix.
- [Warning] `file:line` — what's wrong; concrete fix.

- If every task passes AND every acceptance criterion in spec.md passes, append a final `<DONE>` line after your entry
```

Wait for the subagent to finish, then read its verdict from `convo-{timestamp}.md`.

**3c — Loop or exit**
- Verdict **PASS** and `<DONE>` present → unit complete. Go to Step 4.
- Verdict **NEEDS_WORK** → read the findings, fix them next round (back to 3a).
- No convergence after **8 rounds** → escalate. Read the latest `convo-{timestamp}.md` with the user and decide before continuing.

### Step 4: Update the living docs
Report what changed in each affected doc and **ask the user to confirm before writing** — never edit living docs silently:
- `docs/code-structure.md` — new components/modules, where things live.
- `docs/apis.md` — endpoints or interfaces added/changed.
- `docs/data-dictionary.md` — new entities or fields.
- `docs/adr.md` — any decision taken during the build not already recorded at design time.
- `docs/architecture.md` — only if a component boundary or the high-level shape changed.

If unsure on formatting, see the counterparts in `.claude/references/templates/`.

### Step 5: Merge and integrate
Show the user the diff and AC results, then **ask approval to merge** `feature/<unit>` into the integration branch. On approval, merge and remove the worktree.

When **more than one unit built concurrently**, integrate in dependency order and re-verify after each merge:
1. Merge in dependency order — a unit only after the units it depends on.
2. After each merge, re-run the merged unit's tests on the integration branch.
3. A conflict or new failure is a finding — fix on the integration branch before merging the next.
4. For a UI/visual app, after all merges: serve the assembled app and smoke-check it per `.claude/references/qa/browser-testing-guide.md` — each entry point reachable, something visibly renders, console clean.

When 2+ units merged concurrently, write `.aidlc/integration-{timestamp}.md` capturing: units merged and order, conflicts and resolutions, fixes applied, post-merge verification result, and records updated. Its absence unambiguously means no concurrent integration was needed.

### Step 6: Point at the next step
Report what now exists. Check `.aidlc/` for remaining units:
- **More remain** → name the next in dependency order, suggest re-running this skill.
- **None remain** → the plan is built. Suggest running the app, or `aidlc-feature` for new capability.

## Best Practices
- You own quality — you carry the coding references and design context; the evaluator merely verifies, it doesn't catch what you missed.
- Never evaluate your own work - always use the `evaluator` subagent.
- The loop converges on findings, not tasks — evaluator findings are your instructions for the next round.
- A unit that won't converge before 8 rounds is usually a spec/design gap, not a coding one — escalate, don't grind.
- Living docs and the merge are gated — report, confirm, then act. Never touch the integration branch without approval.

## Subagent-Driven Development Guidelines
- Hand each subagent exactly what it needs in the prompt (task list, relevant files, coding references, convo file path, and any open evaluator findings) — they should not crawl `docs/` or guess at context.
- Subagents should not read or update the living docs, `tasks.md`, or `convo.md` — that is the coordinator's job.
- You are responsible for verifying subagent outputs, running tests, and committing the result.
