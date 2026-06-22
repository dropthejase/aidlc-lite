---
name: aidlc-discover
description: Use on a brownfield codebase that has no living docs yet, to reverse-engineer the existing code into the docs/ living docs. Dispatches read-only crawler agents in parallel over slices of the codebase, then consolidates and writes architecture, code-structure, apis, and data-dictionary. Run after aidlc-init.
---

# DISCOVER

Reverse-engineer an existing codebase into the living docs. You are the orchestrator: you slice the codebase, dispatch one read-only `aidlc-crawler` agent per slice in parallel, consolidate their evidence-backed reports, and write the living docs yourself. The crawlers only read and report — all writing and all cross-slice synthesis is yours.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`. Discover assumes `aidlc-init` has already seeded the `docs/` templates — if they are missing, run `aidlc-init` first.

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
   DISCOVER — let's onboard onto this codebase.

   We'll fan out read-only crawlers across the code, consolidate what
   they find, and reverse-engineer it into the living docs — what's
   built, how it fits together, and what's still unclear. No changes
   to your code.
  ════════════════════════════════════════════════════════════════════
```

## Steps

### Step 1: Slice the codebase
Take a cheap top-level look (tree + build files) and partition the source into slices. Pick the coarsest partition that keeps each slice readable in one agent context, using this ladder:

- **Services / packages** if the repo has them (monorepo, multi-service) → one slice per service/package.
- Else **top-level source directories** (`api/`, `domain/`, `web/`...) → one slice each.
- Else (small or flat repo) → **one slice for the whole repo**.

Shard a slice finer only if it is too large for one context; collapse to fewer if the repo is small. **Cap at ~6 crawlers** — prefer fewer, larger slices over many tiny ones. Announce the chosen partition before dispatching.

### Step 2: Dispatch crawlers in parallel
Dispatch one `aidlc-crawler` per slice, all in the same turn so they run concurrently. Give each only its slice path and nothing of this session's context — the agent constructs its own understanding. Each returns a structured, `file:line`-backed report (findings + gaps); none writes any file.

### Step 3: Consolidate
Collect every crawler report. You — not the crawlers — do the cross-slice work:

- **Merge** the per-slice findings into a single picture (components, APIs, data models, dependencies).
- **Reconcile overlap** where two slices report the same thing or appear to conflict — verify it yourself (read the relevant files) rather than trusting either report. Never assume; confirm.
- **Synthesise architecture** across all slices: the architectural style (with evidence), how components relate, and how a request/transaction flows end-to-end. This needs the whole picture, so only you can do it — no crawler could.
- **Collect gaps** from every report into one list of unknowns.

### Step 4: Gate
Present a concise summary of what you will write into each living doc, plus the consolidated gaps list, and ask the user to approve before writing. Do not write the docs until approved.

### Step 5: Write the living docs
On approval, fill these four living docs in `docs/` from your consolidated findings:

- `architecture.md` — architectural style, component relationships, request/data flow, diagrams.
- `code-structure.md` — repo structure, components and their public surface, technical debt, and the consolidated **Gaps / Uncertainties** table.
- `apis.md` — endpoints / interfaces and their contracts.
- `data-dictionary.md` — entities, fields, and stores.

Do **not** write `adr.md` (discover records what exists, not past decisions) or `.aidlc/bugs.md`.

Seed each doc from your findings into the template `aidlc-init` laid down. If a doc already holds hand-written content, propose changes and get confirmation — never silently overwrite.

### Step 6: Point at the next step
With the living docs in place, recommend the next skill — `aidlc-feature` to build a new capability, or `aidlc-plan` to spec the first unit. Do not start it automatically.

## Best Practices
- Crawlers are read-only — all writing is the orchestrator's.
- Architecture is synthesis across slices — never delegate it to a single crawler that sees only one slice.
- Evidence over assertion — every claim that lands in a living doc should trace to a `file:line`; reconcile, don't trust, overlapping reports.
- Record unknowns as gaps — never fill a gap with a plausible guess.
