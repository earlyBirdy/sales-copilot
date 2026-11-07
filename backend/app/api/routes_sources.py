from fastapi import APIRouter
from app.api.routes_intake import analyze
from app.schemas.source import SourceAnalyzeRequest
router=APIRouter()
@router.post('/analyze')
def source_analyze(payload:SourceAnalyzeRequest):
    source=payload.model_dump();source['intake_mode']='paste'
    return analyze(source)
