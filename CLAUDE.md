# AI-DLC (AI-Driven Development Lifecycle)

This project uses AI-DLC to drive the development of production grade systems.

## Core Principles

- Security-first, production-grade — even if the user says "just a POC".
- Surgical changes — touch only what the task needs; match existing style.
- Run tests when a change touches multiple files.
- Communicate with clarity and conciseness. Do not provide contradicting statements.

### IMPORTANT: NEVER MAKE ASSUMPTIONS

- Verify by reading files purposively, not just grepping
- Conduct research using available Skills or MCP tools rather than guessing
- Ask questions if the user's answer is unclear, rather than assuming

## When To Run AI-DLC Skills

**On every user turn, consider whether to run AI-DLC skills**
**Prompt the user to consider one or more of the following skills**

| Situation | Skill |
|-----------|-------|
| New project, nothing built | `aidlc-init` → `aidlc-plan` |
| Resuming an in-progress build (`docs/` + `.aidlc/` exist) | `aidlc-init` |
| Existing codebase, no `docs/` | `aidlc-init` → `aidlc-discover` |
| New feature on a project that has `docs/` | `aidlc-feature` |
| Bug, regression, or unexpected behaviour | `aidlc-fix` |

Anything else (questions, explanations) — answer directly, no skill.

## Navigating This Repo

The following files provide a quick way of navigating this repository:

`docs/` contain living documents. They are committed and should be the source of truth for the repo in its current state. It contains:
- `architecture.md` — how the system is shaped: components, boundaries, key decisions in brief.
- `code-structure.md` — where things live: directory layout, modules, what each owns.
- `apis.md` — endpoints / interfaces and their contracts.
- `data-dictionary.md` — data models, entities, and their fields.
- `adr.md` — the decision log: why choices were made, what was rejected, what superseded what.

`.aidlc/` is working state (gitignored) and contains:
- per-unit plans (`<unit>/spec.md`, `design.md`, `tasks.md`) - authoritative spec of a unit being built, but may become historical after. The build loop also writes a dated `convo-{timestamp}.md` per run (the generator↔evaluator record).
- `bugs.md` - a record of known and fixed bugs.

A unit is the smallest independently buildable and verifiable slice of work — one or more related epics with their requirements, edge cases, and acceptance criteria. Each unit gets its own plan (`spec.md`, `design.md`, `tasks.md`) and is built and verified as a whole before the next unit starts.

## IMPORTANT: ALWAYS KEEP DOCUMENTS UPDATED

The living docs are only useful if they stay current. After any change that alters how the system works, update the affected `docs/` file — but propose the change and get user confirmation first; never edit living docs silently. Skills enforce this at unit completion; outside a skill, apply the same discipline by hand.
