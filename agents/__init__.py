from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass

from strands import Agent
from strands.models.ollama import OllamaModel

from config import settings
from tools.search import web_search


QUALITY_SCORE_PATTERN = re.compile(r"QUALITY_SCORE:\s*(\d{1,2})", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"(?<!\n)(##\s)")


@dataclass(frozen=True)
class AgentSpec:
    key: str
    display_name: str
    section_title: str
    system_prompt: str


def build_model() -> OllamaModel:
    return OllamaModel(model_id=settings.ollama_model, host=settings.ollama_host)


def create_specialist_agent(spec: AgentSpec) -> Agent:
    return Agent(
        model=build_model(),
        tools=[web_search],
        system_prompt=spec.system_prompt,
    )


def parse_quality_score(content: str) -> int:
    match = QUALITY_SCORE_PATTERN.search(content or "")
    if not match:
        return 0
    score = int(match.group(1))
    return max(0, min(score, 10))


def strip_quality_score(content: str) -> str:
    stripped = QUALITY_SCORE_PATTERN.sub("", content)
    stripped = HEADING_PATTERN.sub(r"\n\1", stripped)
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)
    return stripped.strip()


def _strip_runtime_noise(content: str) -> str:
    cleaned_lines: list[str] = []
    for line in (content or "").splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        if stripped.startswith("Tool #"):
            continue
        if "RuntimeWarning:" in stripped:
            continue
        if "ResourceWarning:" in stripped:
            continue
        if stripped.startswith("INFO:"):
            continue
        if "with DDGS() as ddgs:" in stripped:
            continue
        if "unclosed transport" in stripped:
            continue
        if "unclosed <socket.socket" in stripped:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def clean_specialist_output(content: str, section_title: str) -> str:
    cleaned = _strip_runtime_noise(content)
    start_index = cleaned.find(section_title)
    if start_index != -1:
        cleaned = cleaned[start_index:]

    match = QUALITY_SCORE_PATTERN.search(cleaned)
    if match:
        cleaned = cleaned[: match.end()]

    return cleaned.strip()


def clean_briefing_output(content: str) -> str:
    cleaned = _strip_runtime_noise(content)
    report_index = cleaned.find("# IntelSwarm Briefing:")
    if report_index != -1:
        cleaned = cleaned[report_index:]
    return cleaned.strip()


def _coerce_response_text(response: object) -> str:
    if response is None:
        return ""
    if isinstance(response, str):
        return response

    for attr in ("output_text", "text", "content"):
        value = getattr(response, attr, None)
        if isinstance(value, str) and value.strip():
            return value

    message = getattr(response, "message", None)
    if isinstance(message, str) and message.strip():
        return message

    return str(response)


async def run_specialist(spec: AgentSpec, company_name: str, feedback: str | None = None) -> str:
    prompt = f"Research {company_name} for your specialty area."
    if feedback:
        prompt = (
            f"{prompt}\n\n"
            f"Additional review guidance:\n{feedback}\n\n"
            "Search again with more targeted queries and improve specificity."
        )

    agent = create_specialist_agent(spec)
    response = await asyncio.to_thread(agent, prompt)
    return clean_specialist_output(_coerce_response_text(response), spec.section_title)
