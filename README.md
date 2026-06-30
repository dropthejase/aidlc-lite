# AIDLC-Lite

A lightweight, AI-Driven Development Lifecycle for [Claude Code](https://claude.com/claude-code). Drop it into any project and Claude gains a small set of skills that take you from idea → plan → built, reviewed code — with you approving at every gate.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- A git repository (the build loop uses worktrees for isolation)

## Install

Clone this repo anywhere, then run the interactive setup script:

```bash
git clone https://github.com/<you>/aidlc-lite /tmp/aidlc-lite
cd /tmp/aidlc-lite
./setup.sh
```

The script asks which coding agent you use, prompts for your project's absolute path, backs up any existing `.claude/` or `CLAUDE.md`, and installs the framework. Once done, open your project in Claude Code and run `/aidlc-init`.

## CLAUDE.md reminder hook

`.claude/settings.json` includes a `UserPromptSubmit` hook that randomly injects the full contents of `CLAUDE.md` into Claude's context (~20% of turns). This counteracts context-window drift in long sessions where Claude may start ignoring the project rules. No state file — it fires probabilistically on each user message.

## How it works

AIDLC-Lite splits development into a few **skills**, each a clear stage with user gates. State lives on disk — there is no hidden state file:

| You want to… | Skill | What it does |
|---|---|---|
| Set up a repo for AIDLC | `/aidlc-init` | Scaffolds `docs/` (living docs) and `.aidlc/` (working state). |
| Plan a greenfield idea | `/aidlc-plan` | Clarifies intent, agrees an architecture, decomposes into **units**, writes each unit's spec/design/tasks. Stops at planning. |
| Reverse-engineer an existing codebase | `/aidlc-discover` | Dispatches read-only crawler agents in parallel, consolidates into the living docs. |
| Build a planned unit | `/aidlc-generate-evaluate` | You are the coordinator: build code directly (or via subagents), then spawn an evaluator subagent each round to independently review against the spec. Loop until every task and AC passes, then merge. |
| Add a capability to a built unit | `/aidlc-feature` | Amends an existing unit's spec/design/tasks with a new epic, then hands off to the build loop. |
| Fix a bug | `/aidlc-fix` | Finds and proves the root cause before changing code; gates the fix. |

### Two ideas do most of the work

**Units.** A *unit* is the smallest slice you can build and verify on its own. Each gets its own plan (`spec.md`, `design.md`, `tasks.md`) under `.aidlc/<unit>/`. Independent units can build concurrently, each in its own git worktree.

**Coordinator ⇄ evaluator.** Building a unit is a loop the coordinator (Claude, in your session) drives directly. The coordinator writes code — or delegates to builder subagents for sufficiently independent tasks — then spawns an independent **evaluator** subagent each round to review against the spec, quality, and security standards. Findings from one round become the next round's instructions. The loop continues until the evaluator passes every task and acceptance criterion, or a round cap stops it. Because the coordinator owns all control flow, runaway builds are impossible. This pattern is inspired by Anthropic's [*Building agents with the Claude Agent SDK / harness design for long-running agents*](https://www.anthropic.com/engineering/harness-design-long-running-apps) post.

### Living docs vs. plan artifacts

- **`docs/`** (committed) — the current-state source of truth: `architecture.md`, `code-structure.md`, `apis.md`, `data-dictionary.md`, `adr.md`. To answer "how does the system work today," read these.
- **`.aidlc/`** (gitignored) — per-unit plans and `bugs.md`: a working scratchpad during construction, historical after.

Living docs are only ever updated through a skill, at a user-confirmed gate — never silently.

## Repo structure

```text
.
└── framework/                       # Everything to copy into your project
    ├── CLAUDE.md                    # Skill routing table + core principles
    └── .claude/
        ├── skills/                      # One subdirectory per skill — Claude loads on demand
        │   ├── aidlc-init/SKILL.md
        │   ├── aidlc-plan/SKILL.md
        │   ├── aidlc-discover/SKILL.md
        │   ├── aidlc-generate-evaluate/SKILL.md
        │   ├── aidlc-feature/SKILL.md
        │   └── aidlc-fix/SKILL.md
        ├── agents/                      # Reusable agents called by skills
        │   ├── aidlc-evaluator.md       # Reviews against spec, quality, security; returns PASS/NEEDS_WORK
        │   └── aidlc-crawler.md         # Read-only codebase scanner (used by aidlc-discover)
        ├── hooks/                       # Shell hooks wired into Claude Code lifecycle events
        │   ├── subagent-start-log.sh    # Logs subagent start to .run-logs/subagent-debug.log
        │   └── subagent-stop-log.sh     # Logs subagent stop + tool calls from its transcript
        ├── references/                  # Knowledge guides loaded into context by skills as needed
        │   ├── common/                  # Cross-cutting guides (prerequisites, quality standards…)
        │   ├── requirements/            # Requirements engineering, product thinking
        │   ├── design/                  # Architecture patterns, DDD, functional design, UX
        │   ├── develop/                 # Code generation, testing guides
        │   ├── qa/                      # Quality and security review guides
        │   └── templates/               # Canonical templates for living docs and unit plans
        └── settings.json                # Hook configuration
```

Once installed, `aidlc-init` creates these in your project:

```text
your-project/
├── docs/                            # Living docs (committed; populated by aidlc-init / aidlc-plan)
│   ├── architecture.md
│   ├── code-structure.md
│   ├── apis.md
│   ├── data-dictionary.md
│   └── adr.md
└── .aidlc/                          # Working state (gitignored; created by aidlc-init)
    ├── <unit>/
    │   ├── spec.md
    │   ├── design.md
    │   ├── tasks.md
    │   └── convo-{timestamp}.md     # Coordinator ⇄ evaluator transcript for this run
    ├── integration-{timestamp}.md   # Cross-unit integration record (written on every multi-unit merge)
    └── bugs.md
```

### Subagent strategy

Skills are instructions Claude follows directly. Subagents enter the picture in two places:

**`aidlc-discover`** dispatches a fleet of read-only `aidlc-crawler` agents in parallel — one per assigned slice of the codebase. Each returns a structured report; the skill consolidates them into the living docs. Crawlers are intentionally narrow: read-only, scoped to their slice, no cross-agent coordination needed.

**`aidlc-generate-evaluate`** makes the coordinator the builder. The coordinator spawns an `aidlc-evaluator` subagent each round for independent review — the evaluator never shares context with the coordinator, so its verdict is unbiased. The coordinator may also delegate to builder subagents when tasks are sufficiently decoupled, passing each subagent exactly the context it needs rather than relying on it to read living docs itself. When multiple units are built concurrently, each runs its own loop in its own git worktree; worktrees are merged and an integration record is written when they converge.

## Acknowledgements

AIDLC-Lite stands on the shoulders of these projects. Full license texts are in [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).

- **[AWS AI-DLC (v2)](https://github.com/awslabs/aidlc-workflows/tree/v2)** — the core inspiration. Several of the reference guides under `.claude/references/` (requirements, product, DDD, testing, and other knowledge guides) are used directly or adapted from AWS's AI-DLC v2 knowledge base. Licensed MIT-0.
- **[Planner-Generator-Evaluator](https://github.com/anthropics/cwc-long-running-agents)** and Anthropic's [*Building agents with the Claude Agent SDK / harness design for long-running agents*](https://www.anthropic.com/engineering/harness-design-long-running-apps) — the coordinator ⇄ evaluator loop design. Licensed Apache 2.0.

AIDLC-Lite is a re-imagining, not a fork; any errors or simplifications are its own.

## License

MIT — see [`LICENSE`](LICENSE). The third-party portions retain their original licenses; see [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
