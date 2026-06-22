# AIDLC-Lite

A lightweight, AI-Driven Development Lifecycle for [Claude Code](https://claude.com/claude-code). Drop it into any project and Claude gains a small set of skills that take you from idea → plan → built, reviewed code — with you approving at every gate.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3 (for the build loop; it installs `claude-agent-sdk` into a local venv and reuses your Claude Code login — no API key needed)
- A git repository (the build loop uses worktrees)

## Install

Copy the framework into the root of your project (the directory Claude Code opens):

```bash
# from your project root
git clone https://github.com/<you>/aidlc-lite /tmp/aidlc-lite
cp -R /tmp/aidlc-lite/.claude /tmp/aidlc-lite/CLAUDE.md .
```

That gives your repo a `.claude/` (the framework) and a root `CLAUDE.md` (which tells Claude when to reach for each skill). Open the project in Claude Code and start with `/aidlc-init`.

> If your project already has a `CLAUDE.md`, merge the two rather than overwrite — AIDLC-Lite's `CLAUDE.md` is mostly a routing table and a few principles.

## CLAUDE.md reminder hook

`.claude/settings.json` includes a `UserPromptSubmit` hook that randomly injects the full contents of `CLAUDE.md` into Claude's context (~20% of turns). This counteracts context-window drift in long sessions where Claude may start ignoring the project rules. No state file — it fires probabilistically on each user message.

## How it works

AIDLC-Lite splits development into a few **skills**, each a clear stage with user gates. State lives on disk — there is no hidden state file:

| You want to… | Skill | What it does |
|---|---|---|
| Set up a repo for AIDLC | `/aidlc-init` | Scaffolds `docs/` (living docs) and `.aidlc/` (working state). |
| Plan a greenfield idea | `/aidlc-plan` | Clarifies intent, agrees an architecture, decomposes into **units**, writes each unit's spec/design/tasks. Stops at planning. |
| Reverse-engineer an existing codebase | `/aidlc-discover` | Dispatches read-only crawler agents in parallel, consolidates into the living docs. |
| Build a planned unit | `/aidlc-generate-evaluate` | Runs a **generator ⇄ evaluator** loop in an isolated git worktree until every task and acceptance criterion passes, then merges. |
| Add a capability to a built unit | `/aidlc-feature` | Amends an existing unit's spec/design/tasks with a new epic, then hands off to the build loop. |
| Fix a bug | `/aidlc-fix` | Finds and proves the root cause before changing code; gates the fix. |

### Two ideas do most of the work

**Units.** A *unit* is the smallest slice you can build and verify on its own. Each gets its own plan (`spec.md`, `design.md`, `tasks.md`) under `.aidlc/<unit>/`. Independent units build concurrently, each in its own git worktree.

**Generator ⇄ evaluator.** Building a unit is a loop driven by `.claude/scripts/generate_evaluate.py`. A **generator** writes code; an independent **evaluator** re-runs the tests, reviews against spec/quality/security, and sanity-checks the result actually works. The loop continues — findings from one round become the next round's instructions — until the evaluator declares the unit done or a round cap stops it. The loop, and every exit, lives in the script, so a runaway is impossible. This is based on Anthropic's [*Building agents with the Claude Agent SDK / harness design for long-running agents*](https://www.anthropic.com/engineering/harness-design-long-running-apps) post.

### Living docs vs. plan artifacts

- **`docs/`** (committed) — the current-state source of truth: `architecture.md`, `code-structure.md`, `apis.md`, `data-dictionary.md`, `adr.md`. To answer "how does the system work today," read these.
- **`.aidlc/`** (gitignored) — per-unit plans and `bugs.md`: a working scratchpad during construction, historical after.

Living docs are only ever updated through a skill, at a user-confirmed gate — never silently.

## Repo structure

```
.
├── CLAUDE.md                        # Skill routing table + core principles (committed; copy to your project)
├── .claude/
│   ├── skills/                      # One subdirectory per skill — Claude loads on demand
│   │   ├── aidlc-init/SKILL.md
│   │   ├── aidlc-plan/SKILL.md
│   │   ├── aidlc-discover/SKILL.md
│   │   ├── aidlc-generate-evaluate/SKILL.md
│   │   ├── aidlc-feature/SKILL.md
│   │   └── aidlc-fix/SKILL.md
│   ├── agents/                      # Reusable agents called by the build loop
│   │   ├── aidlc-generator.md       # Implements tasks; writes production code
│   │   ├── aidlc-evaluator.md       # Reviews against spec, quality, security; returns PASS/NEEDS_WORK
│   │   └── aidlc-crawler.md         # Read-only codebase scanner (used by aidlc-discover)
│   ├── references/                  # Knowledge guides loaded into context by skills as needed
│   │   ├── common/                  # Cross-cutting guides (prerequisites, quality standards…)
│   │   ├── requirements/            # Requirements engineering, product thinking
│   │   ├── design/                  # Architecture patterns, DDD, functional design, UX
│   │   ├── develop/                 # Code generation, testing guides
│   │   ├── qa/                      # Quality and security review guides
│   │   └── templates/               # Canonical templates for living docs and unit plans
│   └── scripts/
│       └── generate_evaluate.py     # The build loop — drives generator ⇄ evaluator, owns all exits
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
    │   └── convo-{timestamp}.md     # Generator ⇄ evaluator transcript for this run
    ├── integration-{timestamp}.md   # Cross-unit integration record (written on every multi-unit merge)
    └── bugs.md
```

### Subagent strategy

Skills are instructions Claude follows directly; they do not spawn subagents on their own. Subagents enter the picture in two places:

**`aidlc-discover`** dispatches a fleet of read-only `aidlc-crawler` agents in parallel — one per assigned slice of the codebase. Each returns a structured report; the skill consolidates them into the living docs. Crawlers are intentionally narrow: read-only, scoped to their slice, no cross-agent coordination needed.

**`aidlc-generate-evaluate`** runs the `generate_evaluate.py` build loop, which drives the generator and evaluator as separate Claude agents. The loop owns all control flow and all exit conditions — agents cannot end the loop themselves, which makes runaway builds impossible. Generator and evaluator never share a context window, so the evaluator's verdict is independent. When multiple units are built concurrently, each gets its own loop instance and its own git worktree; worktrees are merged and an integration record is written when they converge.

## Acknowledgements

AIDLC-Lite stands on the shoulders of these projects. Full license texts are in [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).

- **[AWS AI-DLC (v2)](https://github.com/awslabs/aidlc-workflows/tree/v2)** — the core inspiration. Several of the reference guides under `.claude/references/` (requirements, product, DDD, testing, and other knowledge guides) are used directly or adapted from AWS's AI-DLC v2 knowledge base. Licensed MIT-0.
- **[Planner-Generator-Evaluator](https://github.com/anthropics/cwc-long-running-agents)** and Anthropic's [*Building agents with the Claude Agent SDK / harness design for long-running agents*](https://www.anthropic.com/engineering/harness-design-long-running-apps) — the generator ⇄ evaluator harness and inversion-of-control loop design. Licensed Apache 2.0.

AIDLC-Lite is a re-imagining, not a fork; any errors or simplifications are its own.

## License

MIT — see [`LICENSE`](LICENSE). The third-party portions retain their original licenses; see [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
