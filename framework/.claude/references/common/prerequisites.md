# Prerequisites

**Path anchoring.** Every path written in an AI-DLC skill or reference — `.claude/...`, `docs/...`, `.aidlc/...` — is relative to the **project root** (the directory that contains `.claude/`), NOT relative to the skill's own base directory. A skill's base dir may be reported as `.../.claude/skills/<skill>/`, but you must not resolve reference paths against it: `Load .claude/references/templates/` means `<project-root>/.claude/references/templates/`, never `.../skills/<skill>/.claude/references/templates/`. When in doubt, resolve from the project root.

A quick checklist to ensure that the `aidlc-init` skill has been run in this repo.

## Steps

List contents in the project directory and check:

- `docs/` folder exists with at the minimal, `architecture.md` and `code-structure.md`
- `.aidlc/` folder exists with at the minimal, `bugs.md`

If there are missing items, **STOP** and run the `aidlc-init` skill first.
