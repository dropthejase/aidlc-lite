---
name: aidlc-init
description: Use once at the start of working a repo with AI-DLC, to scaffold the living-doc and working-state folders (docs/ and .aidlc/) from templates. Run this before any other AI-DLC skill. Also reports current status when the folders already exist. Triggered with 'Using AI-DLC...'.
---

# INIT

Set up the AI-DLC folders for a repo: `docs/` (living docs, committed) and `.aidlc/` (working state, gitignored). This is a one-time scaffold — it lays down empty templates so the other skills have somewhere to write. It does not plan, design, or write any real content.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder. In particular, the templates this skill scaffolds from live at `.claude/references/templates/` (project root), never under `.claude/skills/aidlc-init/`.

If your context window is fresh, read `.claude/references/common/prerequisites.md`.

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
   INIT — setting up AI-DLC in this repo.

   Laying down docs/ (living docs, committed) and .aidlc/ (working
   state, gitignored) from templates, so the other skills have
   somewhere to write. No planning or code — just the folders.
  ════════════════════════════════════════════════════════════════════

  Initialising folders...
```

## Steps

### Step 1: Survey the repo
Determine whether the codebase is greenfield or brownfield:
- **Greenfield** — no application source, or only scaffolding (`.git`, README, `.claude/`). Nothing or very little has been built.
- **Brownfield** — an existing codebase with source files, but no `docs/`.

Determine whether the AI-DLC files have been seeded.
- Check the project root for the following files: `docs/architecture.md`, `docs/code-structure.md`, `docs/apis.md`, `docs/data-dictionary.md`, `docs/adr.md`, and `.aidlc/bugs.md`.
- Check that each file has content.

**IMPORTANT:** If it is not possible to determine whether the project is greenfield/brownfield, or to what extent the AI-DLC seed files have been created, ask the user rather than assume.

Output a short summary before continuing:

```
Scenario: greenfield | brownfield
Present:  comma-delimited list of present AI-DLC files
Missing:  comma-delimited list of missing AI-DLC files
```

### Step 2: Scaffold the missing files
Load `.claude/references/templates/`. Each template file is a meta-doc: a `## Purpose`, a `## Template` section containing a fenced ```` ```markdown ```` block, and `## Guidelines`.

**Copy only the contents of the fenced block** into the destination — not the Purpose/Guidelines wrapper.

For each of the six files: if it is missing, seed it from its template. Create the `docs/` and `.aidlc/` folders as needed. **DO NOT OVERWRITE EXISTING FILES.**

Ensure `.aidlc/` is gitignored: if no rule already covers it, append `.aidlc/` to `.gitignore`.

Browser-testing MCP servers (project-wide, used by the evaluator and any UI work) belong in a root `.mcp.json`. Because this changes project config, **propose it and get confirmation** — do not write silently. If the user agrees, ensure `.mcp.json` registers both servers (merge into an existing file; never overwrite other servers):

```json
{
  "mcpServers": {
    "chrome-devtools": { "command": "npx", "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"] },
    "playwright":      { "command": "npx", "args": ["@playwright/mcp@latest", "--isolated", "--headless"] }
  }
}
```

Both run isolated (no access to real browser sessions); Playwright also runs headless for unattended use. See `.claude/references/qa/browser-testing-guide.md`.

### Step 3: Report and prompt the next step
Tell the user what now exists, then point them at the next skill based on the scenario:

- **Greenfield + scaffolded AI-DLC files** → recommend `aidlc-plan` to spec and build the first unit.
- **Brownfield + scaffolded AI-DLC files** → recommend `aidlc-discover` to reverse-engineer the existing code into the living docs before building anything new.
- **Already scaffolded from previous sessions** → summarise current state, including a) any open units under `.aidlc/`, and b) open bugs in `.aidlc/bugs.md`. Then recommend the fitting skill — `aidlc-plan`/`aidlc-feature` to continue building, or `aidlc-fix` if there are open bugs.

**Do not start the next skill automatically.** Let the user choose.

## Best Practices
- NEVER overwrite a living doc that already has content — only seed empty templates
- DO NOT write real architecture, decisions, data models or code
- Keep repo review light: this is plumbing, not analysis
