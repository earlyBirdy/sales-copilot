from __future__ import annotations

from typing import Any

from app.core.prompt_loader import PromptLoader
from app.core.prompt_runner import PromptRunner
from app.core.settings import settings
from app.schemas.agent_outputs import SalesSignals


class ExtractorAgent:
    def __init__(self) -> None:
        self.loader = PromptLoader()
        self.runner = PromptRunner()

    def run(self, normalized_source: dict[str, Any]) -> dict[str, Any]:
        system_prompt = self.loader.load("system.md")
        extract_prompt = self.loader.load("extract.md")

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{extract_prompt}\n\n"
                    "NORMALIZED SOURCE:\n"
                    f"{self.runner.json_block(normalized_source)}"
                ),
            },
        ]

        parsed = self.runner.run_structured(
            messages=messages,
            schema_model=SalesSignals,
            schema_name="sales_signals",
            model=settings.sales_copilot_model_reasoning,
            reasoning_effort="medium",
        )
        return parsed.model_dump()
