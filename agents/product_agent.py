from __future__ import annotations

from agents import AgentSpec, run_specialist


SPEC = AgentSpec(
    key="product",
    display_name="Product",
    section_title="## 🛍️ Products & Technology",
    system_prompt=(
        "You are a product intelligence analyst. Given a company name, research "
        "their core products, key features, target customers, tech stack (if "
        "public), and how they differentiate from competitors. Use web search "
        "to find current information. Be specific and avoid vague claims.\n\n"
        "Output rules:\n"
        "- Start with the heading: ## 🛍️ Products & Technology\n"
        "- Use concise markdown bullets and short paragraphs.\n"
        "- Cite concrete product names, customer segments, technologies, or dates when available.\n"
        "- End with a parseable line exactly like: QUALITY_SCORE: 7"
    ),
)


async def run(company_name: str, feedback: str | None = None) -> str:
    return await run_specialist(SPEC, company_name, feedback)

