from __future__ import annotations
import os
import warnings
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings(
    "ignore",
    message=r"This package \(`duckduckgo_search`\) has been renamed to `ddgs`!.*",
    category=RuntimeWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"unclosed transport <_SelectorSocketTransport.*",
    category=ResourceWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"unclosed <socket\.socket .*127\.0\.0\.1.*11434.*",
    category=ResourceWarning,
)


@dataclass(frozen=True)
class Settings:
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    min_quality_score: int = int(os.getenv("MIN_QUALITY_SCORE", "6"))
    max_reruns: int = int(os.getenv("MAX_RERUNS", "2"))
    reports_dir: Path = Path(os.getenv("REPORTS_DIR", "./reports"))


settings = Settings()
settings.reports_dir.mkdir(parents=True, exist_ok=True)
