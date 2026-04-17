from __future__ import annotations
from agents import AgentSpec, run_specialist


SPEC = AgentSpec(
    key="news",
    display_name="News",
    section_title="## 📰 Recent News & Developments",
    system_prompt=(
        "You are a news intelligence analyst. Given a company name, find their "
        "most significant news from the past 6 months: product launches, "
        "partnerships, controversies, leadership changes, layoffs, expansions. "
        "Prioritize recency. Include publication names and approximate dates.\n\n"
        "Output rules:\n"
        "- Start with the heading: ## 📰 Recent News & Developments\n"
        "- Use markdown bullets ordered from most recent or most material.\n"
        "- Include publication/source names and dates for each major development.\n"
        "- End with a parseable line exactly like: QUALITY_SCORE: 7"
    ),
)


async def run(company_name: str, feedback: str | None = None) -> str:
    return await run_specialist(SPEC, company_name, feedback)

