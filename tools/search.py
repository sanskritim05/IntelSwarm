from __future__ import annotations

import time
import warnings

try:
    from ddgs import DDGS
except ImportError:  # pragma: no cover - compatibility path for older environments
    from duckduckgo_search import DDGS
from strands import tool


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo. Returns top results as formatted text.
    Use this to research companies, funding, news, and hiring information.

    Args:
        query: Search query string
        max_results: Number of results to return (default 5)

    Returns:
        Formatted string of search results with titles, URLs, and snippets
    """
    time.sleep(1)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"This package \(`duckduckgo_search`\) has been renamed to `ddgs`!.*",
            category=RuntimeWarning,
        )
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

    if not results:
        return "No results found for this query."

    formatted: list[str] = []
    for index, result in enumerate(results, 1):
        title = result.get("title", "Untitled result")
        href = result.get("href", "Unknown URL")
        body = result.get("body", "No summary available.")
        formatted.append(f"{index}. {title}\n   URL: {href}\n   {body}")

    return "\n\n".join(formatted)
