from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from app.core.prompt_loader import PromptLoader
from app.core.prompt_runner import PromptRunner
from app.core.settings import settings
from app.schemas.agent_outputs import NormalizedSource


class IntakeAgent:
    def __init__(self) -> None:
        self.loader = PromptLoader()
        self.runner = PromptRunner()

    def _tools_for_source(self, source: dict[str, Any]) -> list[dict[str, Any]]:
        url = (source.get("url") or "").strip()
        if settings.sales_copilot_enable_web_search and url and urlparse(url).scheme in {"http", "https"}:
            return [{"type": "web_search"}]
        return []

    def run(self, source: dict[str, Any]) -> dict[str, Any]:
        system_prompt = self.loader.load("system.md")
        intake_prompt = self.loader.load("intake.md")
        tools = self._tools_for_source(source)

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{intake_prompt}\n\n"
                    "SOURCE PAYLOAD:\n"
                    f"{self.runner.json_block(source)}"
                ),
            },
        ]

        parsed = self.runner.run_structured(
            messages=messages,
            schema_model=NormalizedSource,
            schema_name="normalized_source",
            model=settings.sales_copilot_model_fast,
            reasoning_effort="low",
            tools=tools or None,
        )
        return parsed.model_dump()
