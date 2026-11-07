from fastapi import APIRouter
from app.api.routes_guardrail import guardrail
from app.schemas.safety import SafetyReviewRequest
router=APIRouter()
@router.post('/review')
def review(payload:SafetyReviewRequest):
    return guardrail(payload)
