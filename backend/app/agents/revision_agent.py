from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.core.prompt_loader import PromptLoader
from app.core.prompt_runner import PromptRunner
from app.core.settings import settings
from app.schemas.agent_outputs import RevisedDraft


class RevisionAgent:
    def __init__(self) -> None:
        self.loader = PromptLoader()
        self.runner = PromptRunner()

    def run(self, draft_text: str, instruction: str, context: dict[str, Any]) -> dict[str, Any]:
        system_prompt = self.loader.load("system.md")
        revise_prompt = self.loader.load("revise.md")

        payload = {
            "draft_text": draft_text,
            "instruction": instruction,
            "context": context,
        }

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{revise_prompt}\n\n"
                    "REVISION PAYLOAD:\n"
                    f"{self.runner.json_block(payload)}"
                ),
            },
        ]

        parsed = self.runner.run_structured(
            messages=messages,
            schema_model=RevisedDraft,
            schema_name="revised_draft",
            model=settings.sales_copilot_model_reasoning,
            reasoning_effort="medium",
        )

        return {
            "revision_id": f"rev_{uuid4().hex[:8]}",
            "text": parsed.text,
        }
