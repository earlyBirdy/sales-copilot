from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class SourceDocument:
    source_id: str
    source_type: str
    raw_text: str
    title: str = ""
    sender_company: str = ""
    sender_person: str = ""
    date: str = ""
    url: str = ""
    user_goal: str = ""
    preferred_audience: str = ""
    tone_preset: str = ""
    output_lengths: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SalesSignal:
    summary_bullets: List[str]
    company: str
    product_or_solution: str
    announcement_type: str
    target_industries: List[str]
    target_buyers: List[str]
    selling_points: List[str]
    proof_points: List[str]
    customer_pain_points: List[str]
    business_value: List[str]
    risks_or_unclear_claims: List[str]
    cta_options: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DraftRequest:
    audience: str
    tone: str
    lengths: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DraftVariant:
    length: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DraftOutput:
    audience: str
    tone: str
    drafts: List[DraftVariant]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audience": self.audience,
            "tone": self.tone,
            "drafts": [d.to_dict() for d in self.drafts],
        }


@dataclass
class FinalEditableBlock:
    label: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FinalOutputPack:
    source_summary: List[str]
    extracted_sales_signals: SalesSignal
    draft_outputs: List[DraftOutput]
    review_notes: List[str]
    final_editable_blocks: List[FinalEditableBlock]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_summary": self.source_summary,
            "extracted_sales_signals": self.extracted_sales_signals.to_dict(),
            "draft_outputs": [d.to_dict() for d in self.draft_outputs],
            "review_notes": self.review_notes,
            "final_editable_blocks": [b.to_dict() for b in self.final_editable_blocks],
        }
