from __future__ import annotations

import json
from typing import Any, Sequence

from pydantic import BaseModel

from app.core.settings import settings


class PromptRunner:
    def __init__(self) -> None:
        self.client = None

    def _client(self):
        if self.client is None:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY required for live agent calls")
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise RuntimeError("Install backend requirements including the openai SDK") from exc
            self.client = OpenAI(api_key=settings.openai_api_key)
        return self.client

    def run_structured(
        self,
        *,
        messages: Sequence[dict[str, Any]],
        schema_model: type[BaseModel],
        schema_name: str,
        model: str,
        reasoning_effort: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> BaseModel:
        payload: dict[str, Any] = {
            "model": model,
            "input": list(messages),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema_model.model_json_schema(),
                }
            },
        }
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        if tools:
            payload["tools"] = tools

        response = self._client().responses.create(**payload)
        return schema_model.model_validate_json(response.output_text)

    def run_text(
        self,
        *,
        messages: Sequence[dict[str, Any]],
        model: str,
        reasoning_effort: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": model,
            "input": list(messages),
        }
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        if tools:
            payload["tools"] = tools

        response = self._client().responses.create(**payload)
        return response.output_text.strip()

    @staticmethod
    def json_block(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)
