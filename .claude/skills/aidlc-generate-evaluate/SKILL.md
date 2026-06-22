---
name: aidlc-generate-evaluate
description: Use to build a planned unit — turns a unit's spec/design/tasks into working, reviewed code. Runs a generator⇄evaluator loop over tasks.md in an isolated worktree, verifies acceptance criteria, updates the living docs, and merges. Builds one unit per run. Run after aidlc-plan (Path A) or aidlc-feature (Path C).
---

# GENERATE-EVALUATE

Build one planned unit. You are the conductor: you set up an isolated workspace, then drive a loop where a **generator** writes code and an **evaluator** reviews it — independently, in fresh context — until every task is built and passes review. Then you verify acceptance criteria, update the living docs, and merge. You do not write or review the code yourself; the generator builds, the evaluator judges. You orchestrate and own the gates.

**One unit per run** — one script invocation builds one unit in its own worktree. That is the unit of *parallelism*: because each run is self-contained (own unit folder, convo file, worktree), independent units can build **concurrently** (one run each). Units that depend on an earlier unit wait for it.

## Prerequisites
All paths below (`.claude/...`, `docs/...`, `.aidlc/...`) are relative to the **project root** — the directory that contains `.claude/` — not this skill's own folder.

If your context window is fresh, read `.claude/references/common/prerequisites.md`. This skill assumes a planned unit — `.aidlc/<unit>/spec.md`, `design.md`, and `tasks.md` must exist. If not, run `aidlc-plan` (greenfield) or `aidlc-feature` (existing codebase) first.

## Welcome Message
Send this first:

```
-------------------------------------------------------
**AI-DLC · GENERATE-EVALUATE — let's build this unit!**
-------------------------------------------------------

A generator writes the code; an evaluator independently re-runs the tests and
reviews it against the spec, quality, and security. We loop until it's built and
passes, verify the acceptance criteria, then update the docs and merge. You
approve at every gate.
```

## Steps

### Step 1: Pick the unit(s) and confirm the plan
List the units under `.aidlc/`. Identify which are **ready to build now** — `tasks.md` has unbuilt tasks and their dependencies are already built. You may build several ready units at once if none depends on another. If which to build is ambiguous, ask.

For each unit you'll build, read its `spec.md`, `design.md`, and `tasks.md` so you hold the full picture. Announce the unit(s) with a one-line summary of each.

### Step 2: Set up an isolated workspace per unit
The loop makes many commits, and parallel runs would collide in a shared working directory — so **each unit gets its own git worktree** (own working dir + branch). For **each** unit:

- **Detect existing isolation** first: if you're already in a dedicated worktree for that unit, reuse it. Never nest a worktree in a worktree.
- Otherwise propose a branch `feature/<unit>` (let the user rename) and **ask consent** to create a worktree on it off the current integration branch. Prefer the harness's native worktree tool (e.g. `EnterWorktree`); fall back to `git worktree add -b feature/<unit> <path>`.
- If the user declines isolation, work in place on a `feature/<unit>` branch — never on the integration branch directly. In-place builds cannot run in parallel.

### Step 3: Run the build loop
The loop is driven by `generate_evaluate.py` so termination is deterministic and the agents can't run away. Each round it dispatches the generator (builds/fixes all tasks) then the evaluator (re-runs tests, reviews, records findings), passing findings between them via a dated `convo-{timestamp}.md` in the unit folder — until the evaluator declares the unit done (calls `mark_unit_complete`) or the round cap stops it. Each agent's session is reused across rounds, so it doesn't re-read the references or its own prior work cold.

Set up the environment once, then run the script **inside the unit's worktree**:

```
python3 -m venv .aidlc/.venv
.aidlc/.venv/bin/pip install -q claude-agent-sdk
.aidlc/.venv/bin/python -u .claude/scripts/generate_evaluate.py \
  --unit .aidlc/<unit>/ --root . --app-dir . [--max-rounds 8]
```

`--root` is where `.claude/` lives; `--app-dir` is where application code is written (use `.` when they're the same, or point it at the repo root if the framework sits in a subdir). The SDK reuses the current Claude Code login — no API key. `.aidlc/` is gitignored, so the venv isn't committed.

**To build independent units in parallel**, run one invocation per unit concurrently (each in its own worktree, e.g. in the background). Runs share no state — separate unit folders, convo files, worktrees.

While it runs:
- **Watch it live** — the script streams each agent's reasoning and tool calls to stdout, prefixed `[gen]`/`[eval]`. The full trace is also saved to `.run-logs/<unit>-{timestamp}.log` (paired to the convo by timestamp); `tail -f` it to follow a backgrounded run.
- **Steer** without restarting — write to `.aidlc/<unit>/steer.md`; the next round applies it once, then clears it.
- **Stop** with `Ctrl+C`. The script also stops at `--max-rounds` (default 8).

The evaluator only completes the unit once every task **and** every acceptance criterion in `spec.md` passes. On exit:
- **complete** (exit 0) → built, reviewed, ACs pass. Go to Step 4.
- **escalated** (hit the cap) → not converging, usually a spec/design gap. Read the latest `convo-*.md` with the user and decide before continuing.

### Step 4: Update the living docs
Report what changed in each affected doc and **ask the user to confirm before writing** — never edit living docs silently:
- `docs/code-structure.md` — new components/modules, where things live.
- `docs/apis.md` — endpoints or interfaces added/changed.
- `docs/data-dictionary.md` — new entities or fields.
- `docs/adr.md` — any decision taken during the build not already recorded at design time.
- `docs/architecture.md` — only if a component boundary or the high-level shape changed.

If unsure on formatting, see the counterparts in `.claude/references/templates/`.

### Step 5: Merge and integrate
For each completed unit, show the user its diff and AC results, then **ask approval to merge** `feature/<unit>` into the integration branch. On approval, merge and remove the worktree.

When **more than one unit built concurrently**, merging isn't enough — units in separate worktrees never saw each other's code, so integrate and re-verify the combined result:
1. Merge in **dependency order** — a unit only after the units it depends on.
2. After each merge, **re-run the merged unit's tests on the integration branch** (an earlier merge may have changed shared ground).
3. A conflict or new failure is a finding — fix on the integration branch (or re-open the unit) before merging the next.
4. For a **UI/visual app**, a green suite isn't enough: unit suites pass in isolation and miss cross-unit contract gaps (a shared canvas nobody sized, a global two units both write). After the merges, serve the assembled app and smoke-check it in a real browser per `.claude/references/qa/browser-testing-guide.md` — each entry point reachable, something visibly renders (bounds check), console clean. Treat failures as findings.

**Record the integration.** A per-unit `convo-{ts}.md` is scoped to one worktree and ends at that unit's completion — it cannot show that integration happened, what it did, or that it came after. So when you integrate 2+ concurrent units, write `.aidlc/integration-{timestamp}.md` (a sibling of the unit folders, one per pass) capturing: units merged and their order, conflicts hit and how resolved, fixes applied, the post-merge verification result (suite + assembled-app smoke check), and the records you updated (ADR / bugs / code-structure). Its timestamp falls after every unit convo by construction — that ordering is the proof it's a later step. **Always write it when 2+ units merged, even on a clean merge** (so its absence unambiguously means "no concurrent integration was needed"). Reference it from the integration commit message (`integrate(<units>): ...`).

Integration is complete only when all units are merged, the integrated suite passes, (for UI apps) the assembled-app smoke check is clean, and the integration record is written. Do not merge without approval; commit nothing to the integration branch beyond the merge and integration fixes.

### Step 6: Point at the next step
Report what now exists (unit built, ACs verified, docs updated, merged). Then check `.aidlc/` for remaining units:
- **More remain** → name the next in dependency order, suggest re-running this skill. Don't start it automatically.
- **None remain** → the plan is built. Suggest running the app, or `aidlc-feature` for new capability.

## Best Practices
- The generator builds, the evaluator judges, the script orchestrates — independent review in fresh context is the whole point.
- Verify, never assume — the evaluator re-runs the build and tests rather than trusting the generator's summary.
- The loop converges on failures, not tasks — the evaluator's findings are the generator's next instructions, carried in `convo-*.md`.
- A unit that won't converge before the cap is usually a spec/design gap, not a coding one — escalate, don't grind.
- Living docs and the merge are gated — report, confirm, then act. Never touch the integration branch without approval.
