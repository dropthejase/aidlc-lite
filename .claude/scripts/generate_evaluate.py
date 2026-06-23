#!/usr/bin/env python3
"""Build-loop driver for a single AI-DLC unit.

Runs the generator⇄evaluator loop over a unit's tasks until the evaluator
declares the unit complete (it calls the `mark_unit_complete` tool), or a
safety cap stops it. The loop — and every exit — lives here in code; the two
agents each do one pass per round and return. This is the inversion-of-control
that makes a runaway impossible: the script gates every iteration.

Channels:
- convo-{timestamp}.md  the generator↔evaluator record for THIS run (dated so a
                        later feature build on the same unit starts a fresh log).
- steer.md              optional user redirect: injected into the next round once,
                        then cleared. Lets you steer without restarting.

Stops:
- mark_unit_complete()  the evaluator's tool — success; breaks the loop.
- --max-rounds          runaway guard (default 8).
- Ctrl+C                human e-stop (the script is a foreground process).

Auth: the SDK drives the local Claude Code CLI, so it reuses your existing
Claude Code login — no API key needed when run from a logged-in environment.
"""

import argparse
import asyncio
import sys
import uuid
from datetime import datetime
from pathlib import Path

try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        AgentDefinition,
        ResultMessage,
        AssistantMessage,
        TextBlock,
        ThinkingBlock,
        ToolUseBlock,
        tool,
        create_sdk_mcp_server,
    )
except ImportError:
    sys.exit(
        "claude-agent-sdk is not installed.\n"
        "Install it into a venv first:\n"
        "  python3 -m venv .aidlc/.venv\n"
        "  .aidlc/.venv/bin/pip install claude-agent-sdk\n"
        "then run this script with that venv's python."
    )


# ── the convo format ────────────────────────────────────────────────────────
# Every run's convo-{ts}.md is born with this header, so the format is owned in
# one place (here) rather than seeded by a dead template the script then shadows.
# It is the generator↔evaluator channel: append-only, a generator entry then an
# evaluator entry per round, with a final acceptance-criteria block at completion.
CONVO_HEADER = """# Convo — {unit} — run {ts}

<!--
The generator↔evaluator channel for this unit. Append-only, newest at the bottom.
Each round: a generator entry, then an evaluator entry. The generator reads the
latest evaluator entry to pick up open findings before its next pass; the script
reads the latest verdict to decide loop or exit. Do not overwrite prior entries.

## Round N — Generator — [YYYY-MM-DD HH:MM]
**Status:** COMPLETE | COMPLETE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
**Built:** [tasks + one-line what]
**Build/tests:** [build ✓/✗, N/N tests]
**Notes:** [anything for the evaluator to scrutinise; reason for any non-COMPLETE status]

## Round N — Evaluator — [YYYY-MM-DD HH:MM]
**Verdict:** PASS | NEEDS_WORK
**Findings:**
- [Critical] `file:line` — what's wrong; concrete fix.
- [Warning] `file:line` — what's wrong; concrete fix.

## Acceptance Criteria — Evaluator — [YYYY-MM-DD HH:MM]   (once, at completion)
**Result:** PASS | FAIL
- AC1: PASS — [how verified; measured value vs threshold]
- AC2: FAIL — [what fell short]
-->

"""


# ── the unit-complete signal ────────────────────────────────────────────────
# A custom in-process tool. When the evaluator calls it, we record the fact and
# the loop reads `_state["done"]` to break. The evaluator cannot "finish the
# unit" by writing prose — it must call this, which is unambiguous to the script.
_state = {"done": False, "summary": ""}


@tool(
    "mark_unit_complete",
    "Call ONLY when every task is built, passes review, and all acceptance "
    "criteria in spec.md pass. Declares the unit finished and stops the loop.",
    {"summary": str},
)
async def mark_unit_complete(args):
    _state["done"] = True
    _state["summary"] = args.get("summary", "")
    return {"content": [{"type": "text", "text": "Unit marked complete. Loop will stop."}]}


def load_agent(path: Path) -> AgentDefinition:
    """Build an AgentDefinition from an agent .md file's body (drops frontmatter)."""
    text = path.read_text()
    body = text.split("---", 2)[2].strip() if text.startswith("---") else text
    return body


# The active run's log file. Set once per run by loop(). emit() mirrors every
# line to both stdout (live view in the shell) and this file (durable record).
# The log lives in .run-logs/ — OUTSIDE the unit/app working tree — because the
# agents run git (stash/reset/clean) on that tree and would otherwise delete it
# mid-run, as happened to an in-tree run.log. Timestamp-matched to convo-{ts}.md.
_logf = None


def emit(line=""):
    if _logf is not None:
        with _logf.open("a") as f:
            f.write(line + "\n")


def trace_line(agent, level, text):
    """Emit one agent-trace line, tagged `[HH:MM:SS | agent | LEVEL] text`.

    `level` is the *kind* of content, not a severity — TEXT (the agent's prose),
    THINK (its reasoning), TOOL (a tool call). That is what you actually filter a
    run on: `grep TOOL` = what it ran, `grep THINK` = why. agent is gen/eval,
    padded so the columns line up. stdout and the run log get the identical line."""
    emit(f"[{datetime.now():%H:%M:%S} | {agent:<4} | {level:<5}] {text}")


def _trace(label, message):
    """Tag every content block of an agent message so a watcher (and the run log)
    sees what the agent is thinking and doing in real time. Text and thinking are
    emitted in full; tool calls show name + a short arg. Tool *results* are
    deliberately not emitted — they are the bulkiest, noisiest part."""
    if not isinstance(message, AssistantMessage):
        return
    for block in message.content:
        if isinstance(block, TextBlock):
            trace_line(label, "TEXT", block.text)
        elif isinstance(block, ThinkingBlock):
            trace_line(label, "THINK", f"💭 {block.thinking}")
        elif isinstance(block, ToolUseBlock):
            inp = block.input or {}
            # the most telling single arg, per common tools
            arg = (inp.get("command") or inp.get("file_path") or inp.get("path")
                   or inp.get("pattern") or inp.get("url") or "")
            arg = str(arg).replace("\n", " ")
            if len(arg) > 120:
                arg = arg[:120] + "…"
            trace_line(label, "TOOL", f"🔧 {block.name}{(': ' + arg) if arg else ''}")


async def run_agent(prompt, system, cwd, session_id, resume, label,
                    model="sonnet", base_tools=None, add_dirs=None,
                    extra_tools=None, mcp=None):
    """Run one agent pass; return (final text, metadata dict).

    Session continuity: round 1 sets `session_id` (our own id) so the agent's
    context — the reference docs it read, the code it wrote — persists; later
    rounds pass `resume=session_id` (and no session_id, which the CLI forbids
    together) so the agent continues instead of re-reading everything cold.

    `label` ("gen"/"eval") tags every streamed line so a watcher can follow the
    run live (and tell the two agents apart in a parallel run).
    """
    if base_tools is None:
        base_tools = ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
    opts = ClaudeAgentOptions(
        model=model,
        cwd=str(cwd),
        add_dirs=[str(d) for d in (add_dirs or [])],
        system_prompt=system,
        allowed_tools=base_tools + (extra_tools or []),
        permission_mode="acceptEdits",
        mcp_servers=mcp or {},
        session_id=None if resume else session_id,
        resume=session_id if resume else None,
    )
    result, meta = "", {}
    async for message in query(prompt=prompt, options=opts):
        _trace(label, message)
        if isinstance(message, ResultMessage):
            result = message.result or ""
            usage = message.usage or {}
            meta = {
                "secs": (message.duration_ms or 0) / 1000,
                "cost": message.total_cost_usd or 0,
                "in": usage.get("input_tokens", 0),
                "out": usage.get("output_tokens", 0),
            }
    return result, meta


def metaline(agent, rnd, meta):
    """A one-line HTML-comment footer the script appends to convo per agent pass."""
    return (
        f"<!-- {agent} · round {rnd} · {meta.get('secs', 0):.1f}s · "
        f"{meta.get('in', 0)} in / {meta.get('out', 0)} out tok · "
        f"${meta.get('cost', 0):.4f} -->\n"
    )


async def loop(unit: Path, root: Path, max_rounds: int, extra_dirs):
    global _logf
    ts = datetime.now()
    convo = unit / f"convo-{ts:%Y%m%d-%H%M%S}.md"
    convo.write_text(CONVO_HEADER.format(unit=unit.name, ts=f"{ts:%Y-%m-%d %H:%M:%S}"))
    # Run log: outside the agents' working tree, timestamp-matched to the convo.
    logdir = root / ".run-logs"
    logdir.mkdir(exist_ok=True)
    _logf = logdir / f"{unit.name}-{ts:%Y%m%d-%H%M%S}.log"
    _logf.write_text(f"# Run log — {unit.name} — {ts:%Y-%m-%d %H:%M:%S} — convo-{ts:%Y%m%d-%H%M%S}.md\n\n")
    steer = unit / "steer.md"

    gen_system = load_agent(root / ".claude/agents/aidlc-generator.md")
    eval_system = load_agent(root / ".claude/agents/aidlc-evaluator.md")

    done_server = create_sdk_mcp_server(name="unit", tools=[mark_unit_complete])
    done_tool = "mcp__unit__mark_unit_complete"

    # One session per agent, reused across rounds: round 1 establishes it, later
    # rounds resume it so neither agent re-reads the references (or its own prior
    # work) cold. convo.md stays the cross-agent channel — the generator and
    # evaluator have separate sessions and can only see each other through it.
    gen_sid, eval_sid = str(uuid.uuid4()), str(uuid.uuid4())

    emit(f"▶ Building unit '{unit.name}' — convo: {convo.name}\n")

    for rnd in range(1, max_rounds + 1):
        emit(f"── Round {rnd}/{max_rounds} ──")
        resume = rnd > 1

        steer_note = ""
        if steer.exists() and steer.read_text().strip():
            steer_note = f"\n\nUSER STEER (apply this round):\n{steer.read_text().strip()}\n"
            steer.write_text("")  # consume once
            emit("  (applied steer.md)")

        _, gen_meta = await run_agent(
            prompt=(
                f"Build unit '{unit.name}'. Its plan and the running log are in {unit}/ "
                f"(spec.md, design.md, tasks.md, {convo.name}). Implement every unbuilt "
                f"task; if {convo.name} has open evaluator findings, fix those first. "
                f"Append your round entry to {convo.name}.{steer_note}"
            ),
            system=gen_system,
            cwd=root,
            session_id=gen_sid,
            resume=resume,
            label="gen",
            model="sonnet",
            add_dirs=extra_dirs,
            # Browser tools so the generator can smoke-test its own UI work before
            # handoff (page loads, renders, console clean) — fail fast instead of
            # discovering it broken a round later.
            extra_tools=["mcp__playwright__*", "mcp__chrome-devtools__*"],
        )
        with convo.open("a") as f:
            f.write(metaline("generator", rnd, gen_meta))
        emit("  generator: done")

        _, eval_meta = await run_agent(
            prompt=(
                f"Review unit '{unit.name}'. Plan and log in {unit}/ "
                f"(spec.md, tasks.md, {convo.name}). Review the diff against the spec "
                f"and append your verdict and findings to {convo.name}. "
                f"If — and only if — every task passes and all acceptance criteria in "
                f"spec.md pass, append a final '<DONE>' line to {convo.name} and call the "
                f"mark_unit_complete tool."
            ),
            system=eval_system,
            cwd=root,
            session_id=eval_sid,
            resume=resume,
            label="eval",
            model="haiku",
            base_tools=["Read", "Grep", "Glob", "Bash"],
            add_dirs=extra_dirs,
            extra_tools=[done_tool],
            mcp={"unit": done_server},
        )
        with convo.open("a") as f:
            f.write(metaline("evaluator", rnd, eval_meta))
        emit("  evaluator: done")

        if _state["done"]:
            emit(f"\n✅ Unit complete: {_state['summary']}")
            return "complete"

    emit(f"\n⚠ Hit max rounds ({max_rounds}) without completion — escalating to user.")
    return "escalated"


def main():
    ap = argparse.ArgumentParser(description="Run the AI-DLC build loop for one unit.")
    ap.add_argument("--unit", required=True, help="Path to the unit folder, e.g. .aidlc/my-unit/")
    ap.add_argument("--root", default=".", help="Project root (where .claude/ lives). Default: cwd")
    ap.add_argument("--app-dir", default=None, help="Where application code is written, if outside root.")
    ap.add_argument("--max-rounds", type=int, default=8, help="Runaway guard. Default: 8")
    args = ap.parse_args()

    unit = Path(args.unit).resolve()
    root = Path(args.root).resolve()
    if not (unit / "tasks.md").exists():
        sys.exit(f"No tasks.md in {unit} — run aidlc-plan or aidlc-feature first.")

    # Grant agents access to dirs outside root (the unit folder, and an app dir if separate).
    extra_dirs = [unit]
    if args.app_dir:
        extra_dirs.append(Path(args.app_dir).resolve())

    try:
        outcome = asyncio.run(loop(unit, root, args.max_rounds, extra_dirs))
    except KeyboardInterrupt:
        emit("\n⏹ Stopped by user (Ctrl+C).")
        sys.exit(130)
    sys.exit(0 if outcome == "complete" else 2)


if __name__ == "__main__":
    main()
