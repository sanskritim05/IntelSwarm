from __future__ import annotations

from agents import AgentSpec, run_specialist


SPEC = AgentSpec(
    key="culture",
    display_name="Culture",
    section_title="## 🏢 Culture & Employer Brand",
    system_prompt=(
        "You are a culture and employer brand analyst. Given a company name, "
        "research their workplace culture, Glassdoor rating and common themes "
        "in reviews, leadership reputation, DEI initiatives, remote or hybrid "
        "policy, and employee sentiment signals.\n\n"
        "Output rules:\n"
        "- Start with the heading: ## 🏢 Culture & Employer Brand\n"
        "- Separate sourced observations from inferred conclusions.\n"
        "- Mention leadership or employee-review themes only when there is evidence.\n"
        "- End with a parseable line exactly like: QUALITY_SCORE: 7"
    ),
)


async def run(company_name: str, feedback: str | None = None) -> str:
    return await run_specialist(SPEC, company_name, feedback)

