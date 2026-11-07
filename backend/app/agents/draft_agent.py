from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.core.prompt_loader import PromptLoader
from app.core.prompt_runner import PromptRunner
from app.core.settings import settings
from app.schemas.agent_outputs import DraftSet


class DraftAgent:
    def __init__(self) -> None:
        self.loader = PromptLoader()
        self.runner = PromptRunner()

    def run(self, sales_signals: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        system_prompt = self.loader.load("system.md")
        draft_prompt = self.loader.load("draft.md")

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{draft_prompt}\n\n"
                    "SALES SIGNALS:\n"
                    f"{self.runner.json_block(sales_signals)}\n\n"
                    "DRAFT REQUEST:\n"
                    f"{self.runner.json_block(request)}"
                ),
            },
        ]

        parsed = self.runner.run_structured(
            messages=messages,
            schema_model=DraftSet,
            schema_name="draft_set",
            model=settings.sales_copilot_model_reasoning,
            reasoning_effort="medium",
        ).model_dump()

        return {
            "draft_set_id": f"draftset_{uuid4().hex[:8]}",
            "audience": parsed["audience"],
            "tone": parsed["tone"],
            "drafts": [
                {
                    "draft_id": f"draft_{uuid4().hex[:8]}",
                    "length": draft["length"],
                    "text": draft["text"],
                }
                for draft in parsed["drafts"]
            ],
        }
