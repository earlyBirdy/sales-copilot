from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NormalizedSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: str
    title: str
    company: str
    product_or_solution: str
    summary_bullets: list[str] = Field(min_length=3, max_length=3)
    claims: list[str]
    explicit_cta: list[str]


class SalesSignals(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str
    product_or_solution: str
    announcement_type: Literal[
        "launch", "event", "promotion", "partnership", "certification", "article", "update"
    ]
    target_industries: list[str]
    target_buyers: list[str]
    selling_points: list[str]
    proof_points: list[str]
    customer_pain_points: list[str]
    business_value: list[str]
    risks_or_unclear_claims: list[str]
    cta_options: list[str]


class DraftVariant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    length: Literal["short", "medium", "long"]
    text: str


class DraftSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audience: str
    tone: str
    drafts: list[DraftVariant]


class RevisedDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


class GuardrailReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_notes: list[str]
    risk_level: Literal["low", "medium", "high"]
