from __future__ import annotations

from typing import Any

from app.core.prompt_loader import PromptLoader
from app.core.prompt_runner import PromptRunner
from app.core.settings import settings
from app.schemas.agent_outputs import GuardrailReview


class GuardrailAgent:
    def __init__(self) -> None:
        self.loader = PromptLoader()
        self.runner = PromptRunner()

    def run(self, draft_text: str, session_context: dict[str, Any]) -> dict[str, Any]:
        system_prompt = self.loader.load("system.md")
        guardrail_prompt = self.loader.load("guardrail.md")

        payload = {
            "draft_text": draft_text,
            "session_context": session_context,
        }

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"{guardrail_prompt}\n\n"
                    "GUARDRAIL PAYLOAD:\n"
                    f"{self.runner.json_block(payload)}"
                ),
            },
        ]

        parsed = self.runner.run_structured(
            messages=messages,
            schema_model=GuardrailReview,
            schema_name="guardrail_review",
            model=settings.sales_copilot_model_fast,
            reasoning_effort="low",
        )
        return parsed.model_dump()
