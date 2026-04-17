from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Awaitable, Callable

from strands import Agent

from agents import (
    _coerce_response_text,
    build_model,
    clean_briefing_output,
    parse_quality_score,
    strip_quality_score,
)
from agents import culture_agent, funding_agent, hiring_agent, news_agent, product_agent
from config import settings


ProgressCallback = Callable[[dict[str, Any]], Awaitable[None] | None]


ORCHESTRATOR_PROMPT = (
    "You are an intelligence orchestrator managing a swarm of specialist "
    "research agents. Your job is to:\n"
    "1. Delegate research tasks to specialist agents\n"
    "2. Review each agent's output for quality and specificity\n"
    "3. If an agent scores below 6/10, provide targeted guidance and rerun it\n"
    "4. Synthesize all sections into a final executive briefing\n"
    "5. Add an opening TL;DR and a strategic recommendations section\n"
    "You are rigorous. Vague or generic outputs are not acceptable.\n\n"
    "Final output format:\n"
    "# IntelSwarm Briefing: <Company>\n"
    "Generated: <timestamp>\n\n"
    "## TL;DR\n"
    "- 3 to 5 high-value bullets\n\n"
    "Then include the five specialist sections exactly once in this order:\n"
    "Products, Hiring, Funding, News, Culture.\n\n"
    "Then conclude with:\n"
    "## ⚡ Strategic Recommendations\n"
    "- Why this company is worth watching\n"
    "- Red flags or risks\n"
    "- Best fit roles or teams to target if job seeking"
)


@dataclass
class SwarmResult:
    company: str
    markdown: str
    report_path: Path
    section_scores: dict[str, int]
    sections: dict[str, str]


SPECIALISTS = [
    ("product", product_agent),
    ("hiring", hiring_agent),
    ("funding", funding_agent),
    ("news", news_agent),
    ("culture", culture_agent),
]


async def emit_progress(progress_callback: ProgressCallback | None, event: dict[str, Any]) -> None:
    if progress_callback is None:
        return
    result = progress_callback(event)
    if asyncio.iscoroutine(result):
        await result


async def _run_specialist(module: Any, company_name: str, feedback: str | None = None) -> str:
    return await module.run(company_name, feedback)


def _build_rerun_feedback(company_name: str, agent_key: str, score: int) -> str:
    return (
        f"Your previous output for {company_name} scored {score}/10 and was too vague. "
        f"Focus on finding specific data points relevant to {agent_key}: exact role titles, "
        "exact funding amounts, publication names, exact dates, named products, and grounded facts."
    )


def _save_report(company_name: str, markdown: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_company = "".join(ch.lower() if ch.isalnum() else "_" for ch in company_name).strip("_")
    filename = f"{safe_company}_{timestamp}.md"
    path = settings.reports_dir / filename
    path.write_text(markdown, encoding="utf-8")
    return path


async def _synthesize(company_name: str, sections: dict[str, str]) -> str:
    prompt = (
        f"Create the final recruiter-style competitive intelligence briefing for {company_name}.\n\n"
        f"Current timestamp: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "Use the specialist sections below as your source material. Clean up repetition, "
        "preserve the strongest specific facts, and do not invent data.\n\n"
        f"{json.dumps(sections, indent=2)}"
    )
    agent = Agent(model=build_model(), system_prompt=ORCHESTRATOR_PROMPT)
    response = await asyncio.to_thread(agent, prompt)
    return clean_briefing_output(_coerce_response_text(response))


async def run_swarm(company_name: str, progress_callback: ProgressCallback | None = None) -> SwarmResult:
    sections: dict[str, str] = {}
    section_scores: dict[str, int] = {}

    async def run_initial(agent_key: str, module: Any) -> tuple[str, str]:
        await emit_progress(progress_callback, {"agent": agent_key, "status": "running"})
        content = await _run_specialist(module, company_name)
        score = parse_quality_score(content)
        section_scores[agent_key] = score
        sections[agent_key] = content
        await emit_progress(
            progress_callback,
            {"agent": agent_key, "status": "complete", "score": score},
        )
        return agent_key, content

    await asyncio.gather(*(run_initial(agent_key, module) for agent_key, module in SPECIALISTS))

    for agent_key, module in SPECIALISTS:
        best_content = sections[agent_key]
        best_score = section_scores[agent_key]

        for _ in range(settings.max_reruns):
            if best_score >= settings.min_quality_score:
                break

            await emit_progress(
                progress_callback,
                {
                    "agent": agent_key,
                    "status": "rerunning",
                    "reason": f"score {best_score}/10",
                },
            )
            rerun_content = await _run_specialist(
                module,
                company_name,
                _build_rerun_feedback(company_name, agent_key, best_score),
            )
            rerun_score = parse_quality_score(rerun_content)
            if rerun_score > best_score:
                best_score = rerun_score
                best_content = rerun_content
            sections[agent_key] = best_content
            section_scores[agent_key] = best_score
            await emit_progress(
                progress_callback,
                {"agent": agent_key, "status": "complete", "score": best_score},
            )

    await emit_progress(progress_callback, {"agent": "orchestrator", "status": "synthesizing"})
    clean_sections = {key: strip_quality_score(content) for key, content in sections.items()}
    markdown = await _synthesize(company_name, clean_sections)
    await emit_progress(progress_callback, {"agent": "orchestrator", "status": "complete"})

    report_path = _save_report(company_name, markdown)
    return SwarmResult(
        company=company_name,
        markdown=markdown,
        report_path=report_path,
        section_scores=section_scores,
        sections=clean_sections,
    )
