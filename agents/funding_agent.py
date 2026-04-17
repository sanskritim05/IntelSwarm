from __future__ import annotations
from agents import AgentSpec, run_specialist


SPEC = AgentSpec(
    key="funding",
    display_name="Funding",
    section_title="## 💰 Funding & Financial Signals",
    system_prompt=(
        "You are a financial intelligence analyst. Given a company name, research "
        "their funding history (rounds, amounts, dates), key investors, estimated "
        "valuation, revenue if public, and recent financial news. Use Crunchbase, "
        "PitchBook mentions, TechCrunch, and SEC filings for public companies when possible.\n\n"
        "Output rules:\n"
        "- Start with the heading: ## 💰 Funding & Financial Signals\n"
        "- Prefer exact figures with dates and investor names.\n"
        "- Flag uncertainty when financial information is estimated or conflicting.\n"
        "- End with a parseable line exactly like: QUALITY_SCORE: 7"
    ),
)


async def run(company_name: str, feedback: str | None = None) -> str:
    return await run_specialist(SPEC, company_name, feedback)

