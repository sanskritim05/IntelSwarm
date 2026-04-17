from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass, field

from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from orchestrator import run_swarm


console = Console()


@dataclass
class AgentState:
    status: str = "waiting"
    score: int | None = None
    reason: str | None = None


def status_label(state: AgentState) -> str:
    mapping = {
        "waiting": "Waiting",
        "running": "Running",
        "complete": "Complete",
        "rerunning": "Rerunning",
        "synthesizing": "Synthesizing",
    }
    label = mapping.get(state.status, state.status.title())
    if state.status == "complete":
        return f"[green]OK[/green] {label}"
    if state.status in {"running", "synthesizing"}:
        return f"[cyan]...[/cyan] {label}"
    if state.status == "rerunning":
        return f"[yellow]~[/yellow] {label}"
    return label


def build_table(agent_states: dict[str, AgentState]) -> Table:
    table = Table(title="IntelSwarm Progress", box=box.ROUNDED)
    table.add_column("Agent")
    table.add_column("Status")
    table.add_column("Quality")
    table.add_column("Notes")

    rows = [
        ("Product", agent_states["product"]),
        ("Hiring", agent_states["hiring"]),
        ("Funding", agent_states["funding"]),
        ("News", agent_states["news"]),
        ("Culture", agent_states["culture"]),
        ("Orchestrator", agent_states["orchestrator"]),
    ]
    for name, state in rows:
        score = f"{state.score}/10" if state.score is not None else "-"
        notes = state.reason or "-"
        table.add_row(name, status_label(state), score, notes)
    return table


async def run_cli(company_name: str) -> None:
    agent_states = {
        key: AgentState()
        for key in ["product", "hiring", "funding", "news", "culture", "orchestrator"]
    }

    async def on_progress(event: dict[str, object]) -> None:
        agent = str(event.get("agent", "orchestrator"))
        state = agent_states.setdefault(agent, AgentState())
        state.status = str(event.get("status", state.status))
        if "score" in event and event["score"] is not None:
            state.score = int(event["score"])
        state.reason = str(event["reason"]) if event.get("reason") else None

    console.print(Panel.fit("🤖 IntelSwarm — Competitive Intelligence", border_style="cyan"))
    with Live(build_table(agent_states), console=console, refresh_per_second=5) as live:
        task = asyncio.create_task(run_swarm(company_name, progress_callback=on_progress))
        while not task.done():
            live.update(build_table(agent_states))
            await asyncio.sleep(0.1)
        result = await task
        live.update(build_table(agent_states))

    console.print()
    console.print(result.markdown)
    console.print(f"\nSaved to {result.report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IntelSwarm competitive intelligence bot")
    parser.add_argument("--company", required=True, help="Company name to research")
    parser.add_argument(
        "--output",
        default="markdown",
        choices=["markdown", "pdf"],
        help="Output format. PDF requires optional weasyprint support.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.output == "pdf":
        console.print("PDF export is not enabled in this build. Use markdown output instead.")
        raise SystemExit(1)
    asyncio.run(run_cli(args.company))


if __name__ == "__main__":
    main()

