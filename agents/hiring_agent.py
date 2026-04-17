from __future__ import annotations

from agents import AgentSpec, run_specialist


SPEC = AgentSpec(
    key="hiring",
    display_name="Hiring",
    section_title="## 👥 Hiring Signals & Team Growth",
    system_prompt=(
        "You are a talent intelligence analyst. Given a company name, research "
        "their current open roles, hiring volume trends, which teams are growing, "
        "what skills they are hiring for, and what this signals about company "
        "priorities. Search LinkedIn job postings, Greenhouse, Lever, and the "
        "company careers page when possible.\n\n"
        "Output rules:\n"
        "- Start with the heading: ## 👥 Hiring Signals & Team Growth\n"
        "- Highlight exact role titles, locations, functions, and hiring patterns.\n"
        "- Infer priorities carefully and label any inference.\n"
        "- End with a parseable line exactly like: QUALITY_SCORE: 7"
    ),
)


async def run(company_name: str, feedback: str | None = None) -> str:
    return await run_specialist(SPEC, company_name, feedback)

