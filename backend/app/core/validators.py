from __future__ import annotations

from typing import Any

from app.schemas.agent_outputs import DraftSet, GuardrailReview, NormalizedSource, RevisedDraft, SalesSignals

def validate_normalized_source(payload: dict[str, Any]) -> dict[str, Any]:
    return NormalizedSource.model_validate(payload).model_dump()

def validate_sales_signals(payload: dict[str, Any]) -> dict[str, Any]:
    return SalesSignals.model_validate(payload).model_dump()

def validate_draft_set(payload: dict[str, Any]) -> dict[str, Any]:
    DraftSet.model_validate({
        "audience": payload.get("audience"),
        "tone": payload.get("tone"),
        "drafts": [{"length": d.get("length"), "text": d.get("text")} for d in payload.get("drafts", [])],
    })
    return payload

def validate_revised_draft(payload: dict[str, Any]) -> dict[str, Any]:
    RevisedDraft.model_validate({"text": payload.get("text")})
    return payload

def validate_guardrail(payload: dict[str, Any]) -> dict[str, Any]:
    GuardrailReview.model_validate({"review_notes": payload.get("review_notes", []), "risk_level": payload.get("risk_level", "low")})
    return payload

def require_nonempty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")

def validate_final_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for block in blocks:
      label = block.get("label", "")
      text = block.get("text", "")
      require_nonempty_string(label, "label")
      require_nonempty_string(text, "text")
      if label in seen:
          raise ValueError(f"duplicate export label: {label}")
      seen.add(label)
      out.append({"label": label, "text": text})
    return out
