---
name: aidlc-fix
description: Use to investigate and fix a bug, regression, or unexpected behaviour on an existing codebase. Finds root cause before changing code and gates the fix and any doc updates with the user.
---

# FIX

Diagnose and fix a bug on an existing codebase. Always establish the root cause before changing any code — a fix that addresses a symptom rather than the cause tends to mask the real problem or resurface it elsewhere.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`.

## Steps

### Step 1: Understand and reproduce bug
For trivial bugs you may skip straight to **Step 4**. A bug is trivial only when all of the following hold:
- The root cause is already obvious and proven — no investigation needed (Step 2 would find nothing new).
- The fix is small and localised (roughly 1-10 lines), touching no public surface, contract, or data shape.
- It carries no security or correctness risk — it does not touch auth, access control, validation, money/quantity math, or concurrency.
- The fix is unlikely to introduce a breaking change.

Examples: a typo, a wrong log message, an off-by-one in a non-critical loop, a missing IAM permission, a mistyped config/env key, a wrong constant or default value, an incorrect import path.

If in doubt, treat it as non-trivial and do not skip — a fast wrong fix is more expensive than the full loop.

For non-trivial bugs:
- Write a failing test that reproduces it first
- Once reproduced, record the bug in `.aidlc/bugs.md` (status: open). If the bug already exists but was previously closed, reopen it.

**IMPORTANT:** if you do not understand the issue, ASK the user clarifying questions until you are clear on a) the observed behaviour and b) the expected behaviour. Do not make assumptions.

### Step 2: Root cause discovery
- Read `docs/architecture.md` and `docs/code-structure.md` for context and blast radius
- Read `.aidlc/bugs.md` in case a similar bug has already been resolved
- Determine and prove the root cause

Possible methods to isolate root cause include, but are not limited to:
- `git bisect` to find the commit that introduced a regression
- Compare a working case against the failing one (env vars, versions, config, input data) — the difference often is the cause
- Query the DB or inspect network traffic directly to verify data, rather than assume it
- Playwright MCP to observe UI behaviour
- Temporary debugging logs (clean these up in Step 4)
- ...or any other method available to you

**IMPORTANT:** DO NOT guess the root cause. Verify it empirically.

**IF YOU ARE STUCK...**
- STOP
- Explain what you have tried to the user concisely
- Signs that you are stuck include if you have tried around 5-7 times and the fix still fails

### Step 3: Present hypothesis
Present your hypothesis **CONCISELY** in the following format:

```
**Observed behaviour:** A concise 1-2 sentences on the observed error.
**Expected behaviour:** A consise 1-2 sentences on the expected behaviour.

**Hypothesis:**
- A concise but clear explanation of the root cause.
- Aim for 1-5 bullets unless absolutely unavoidable.

**Proposed fix(es):**
- Present the fix as a short bulleted list or provide options
- If providing options, also provide a recommendation, which adheres to best practice patterns and your reasoning
- Surface any genuine limitations of the fix worth flagging to the user
```

**IMPORTANT:** if the fix requires reconsidering an architectural decision, surface this to the user and ask whether to upgrade to the `aidlc-feature` skill instead.

**DO NOT MOVE TO STEP 4 UNTIL EXPLICIT USER APPROVAL**
The user may ask for further clarification or propose their own alternative fix.

### Step 4: Apply fixes
- Apply the fixes
- Check the code compiles and passes tests
- For application-level fixes that may not be easily verifiable (e.g. UI fixes), ask the user to confirm whether the fix has worked
- Clean up any debugging logs from **Step 2**

### Step 5: Document fixes
Confirm to the user whether the bug can be considered closed. If so, update `.aidlc/bugs.md` only.

Where the fix has a higher blast radius, propose living doc updates to the user:
- fix touches a public surface or new files → `docs/code-structure.md`
- fix changes a contract or data shape → `docs/apis.md` / `docs/data-dictionary.md`
- fix reverses a decision → `docs/adr.md`

## Best Practices

- ALWAYS make surgical or minimal changes where possible
- ALWAYS use production-grade patterns
- ALWAYS adopt security-first approach
- DO NOT choose the easier option if it is not defensible from an enterprise/production-grade perspective
- DO NOT use hacky workarounds to solve bugs
- NEVER assume, always clarify

## Anti-Patterns For Bug Fixes

- Editing vendored / generated code (`node_modules/`, `dist/`, `build/`, `.venv/`) — these are overwritten on the next install/build. Fix the source or patch the dependency properly.
- Widening the attack surface to make a bug go away (loosening CORS, disabling auth/SSL verification, broadening IAM, weakening validation) without explicit user permission.
- Suppressing the symptom instead of fixing the cause — swallowing exceptions, empty catch blocks, blanket try/except, `# type: ignore`, silencing the linter.
- Hardcoding a value to pass the failing case (magic number, specific ID, fixed timestamp) instead of fixing the logic.
- Weakening or deleting a test so it passes, rather than fixing the code the test caught.
- Scope creep — refactoring or "improving" unrelated code while fixing the bug; keep the change surgical.
- Adding a retry / sleep / timeout to mask a race condition or flaky behaviour without understanding why it fails.
- Treating a recurring bug as one-off — fixing this instance but not the shared root that will resurface it elsewhere.

## Documentation Standards
For guidance on how to document to the aforementioned files, refer to the `.claude/templates/` folder.
Only read this if you have forgotten the required standards.

## Further References On Standards (only read the file that applies, and only if changes are more than minimal)

- `.claude/references/develop/code-analysis-checklist.md` — coding standards checklist
- `.claude/references/develop/code-generation*.md` — coding standards guidance
- `.claude/references/qa/testing-guide.md` — writing or changing tests
- `.claude/references/security/security-baseline.md` — when the fix touches security
- `.claude/references/security/api-security.md` — only if the fix touches an API endpoint
