# Bugs Log Template

## Purpose
Track defects **and how they were solved**. The fix record keeps reasoning out of sprawling git logs and lets the agent reuse a prior solution when a similar issue recurs.

## Template

```markdown
# Bugs

## [BUG-001] Short description
- **Scope:** unit-name(s) or 'all' if project-level
- **Status:** open | in-progress | partial-resolve | resolved
- **Last Updated:** YYYY-MM-DD HH:MM:SS
- **Observed Behaviour:** 1-2 lines setences.
- **Expected Behaviour:** 1-2 lines setences.
- **Root Cause:** 5 bulleted sentences following '5 Whys' format.
- **Fix:** 1-3 sentences on how it was resolved.
- **Files changed:** comma-delimited list of files touched.
- **Tests:** What to run and what passing looks like.
```

## Guidelines

### When to update
- When something built does not work: record the bug (`open`) on discovery, and update the same entry to `resolved` once fixed. One entry per defect; do not delete resolved entries.

### Format
- Use a reproducing test as the `Tests` line where possible — it is what proves the fix and guards against regression.
- Structural/architectural debt belongs in `code-structure.md`, not here; this log is for defects.
