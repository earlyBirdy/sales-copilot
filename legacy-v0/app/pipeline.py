from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.models import (
    SourceDocument,
    SalesSignal,
    DraftRequest,
    DraftVariant,
    DraftOutput,
    FinalEditableBlock,
    FinalOutputPack,
)


BASE_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = BASE_DIR / "prompts"
EXAMPLES_DIR = BASE_DIR / "examples"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def intake_stage(source: SourceDocument) -> dict:
    raw = source.raw_text.strip()
    bullets = [
        f"{source.sender_company or 'The source'} shares an announcement relevant to sales outreach.",
        "The content appears suitable for repackaging into audience-specific sales drafts.",
        "The source should be reviewed for key claims, proof points, and usable CTA angles.",
    ]
    return {
        "source_type": source.source_type,
        "title": source.title,
        "raw_text": raw,
        "company": source.sender_company or "Unknown company",
        "product_or_solution": source.title or "Unspecified solution",
        "summary_bullets": bullets,
        "claims": [],
        "explicit_cta": [],
    }


def extraction_stage(normalized: dict) -> SalesSignal:
    company = normalized.get("company", "Unknown company")
    product = normalized.get("product_or_solution", "Unspecified solution")

    return SalesSignal(
        summary_bullets=normalized["summary_bullets"],
        company=company,
        product_or_solution=product,
        announcement_type="update",
        target_industries=["industrial", "enterprise"],
        target_buyers=["sales leads", "technical buyers"],
        selling_points=[
            "relevant market update",
            "usable as outreach trigger",
            "can be adapted by audience",
        ],
        proof_points=[
            "source-provided announcement",
            "named company reference",
            "named topic or title",
        ],
        customer_pain_points=[
            "limited time to rewrite updates manually",
            "need for consistent messaging",
        ],
        business_value=[
            "saves sales drafting time",
            "improves message consistency",
        ],
        risks_or_unclear_claims=[
            "verify technical or commercial claims before external use",
        ],
        cta_options=[
            "Happy to share a short summary if useful.",
            "Let me know if you want a version tailored to your use case.",
            "We can turn this into a customer-ready note if needed.",
        ],
    )


def build_text(extraction: SalesSignal, audience: str, tone: str, length: str) -> str:
    opener_map = {
        "internal": f"Sharing a quick update from {extraction.company}.",
        "customer": f"I came across this update from {extraction.company} and thought it may be relevant.",
        "prospect": f"Noticed this recent update from {extraction.company} and thought it may be worth flagging.",
        "partner": f"Flagging a potentially useful market update from {extraction.company}.",
        "linkedin_dm": f"Thought this update from {extraction.company} may interest you.",
        "linkedin_post": f"Interesting update from {extraction.company}.",
        "crm_note": f"Captured update from {extraction.company}.",
    }

    value = extraction.business_value[0] if extraction.business_value else "useful commercial relevance"
    point = extraction.selling_points[0] if extraction.selling_points else "relevant positioning"

    if length == "short":
        return f"{opener_map.get(audience, 'Sharing an update.')} Main angle: {point}. {extraction.cta_options[0]}"
    if length == "medium":
        return (
            f"{opener_map.get(audience, 'Sharing an update.')} "
            f"The source points to {point}, with business value around {value}. "
            f"{extraction.cta_options[1]}"
        )
    return (
        f"{opener_map.get(audience, 'Sharing an update.')} "
        f"The source suggests {point}, and it can support conversations about {', '.join(extraction.customer_pain_points)}. "
        f"From a sales perspective, the main value is that it {value}. "
        f"{extraction.cta_options[2]}"
    )


def drafting_stage(extraction: SalesSignal, request: DraftRequest) -> DraftOutput:
    drafts = [
        DraftVariant(length=length, text=build_text(extraction, request.audience, request.tone, length))
        for length in request.lengths
    ]
    return DraftOutput(audience=request.audience, tone=request.tone, drafts=drafts)


def generate_review_notes(extraction: SalesSignal, draft_outputs: List[DraftOutput]) -> List[str]:
    notes = []
    for risk in extraction.risks_or_unclear_claims:
        notes.append(f"Review check: {risk}")
    if any(output.audience == "linkedin_post" for output in draft_outputs):
        notes.append("Check public wording carefully before posting externally.")
    if not notes:
        notes.append("No major review notes detected.")
    return notes


def build_final_pack(extraction: SalesSignal, draft_outputs: List[DraftOutput]) -> FinalOutputPack:
    final_blocks = []
    for output in draft_outputs:
        for draft in output.drafts:
            final_blocks.append(
                FinalEditableBlock(
                    label=f"{output.audience}_{draft.length}",
                    text=draft.text,
                )
            )

    return FinalOutputPack(
        source_summary=extraction.summary_bullets,
        extracted_sales_signals=extraction,
        draft_outputs=draft_outputs,
        review_notes=generate_review_notes(extraction, draft_outputs),
        final_editable_blocks=final_blocks,
    )


def run_sales_copilot(source: SourceDocument, draft_requests: List[DraftRequest]) -> FinalOutputPack:
    _ = load_prompt("system.md")
    _ = load_prompt("intake.md")
    _ = load_prompt("extract.md")
    _ = load_prompt("draft.md")
    _ = load_prompt("revise.md")

    normalized = intake_stage(source)
    extraction = extraction_stage(normalized)
    draft_outputs = [drafting_stage(extraction, request) for request in draft_requests]
    return build_final_pack(extraction, draft_outputs)


def main() -> None:
    sample_path = EXAMPLES_DIR / "sample_email_input.json"
    payload = json.loads(sample_path.read_text(encoding="utf-8"))

    source = SourceDocument(**payload)
    requests = [
        DraftRequest(audience=source.preferred_audience or "customer", tone=source.tone_preset or "professional_neutral", lengths=source.output_lengths or ["short", "medium"]),
        DraftRequest(audience="linkedin_post", tone="social_light", lengths=["short"]),
    ]

    result = run_sales_copilot(source, requests)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
