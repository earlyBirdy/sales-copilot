from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from app.agents.intake_agent import IntakeAgent
from app.agents.extractor_agent import ExtractorAgent
from app.core.intake_pipeline import normalize_unified_intake,parse_uploaded,MAX_BYTES,gmail_placeholder
from app.core.validators import validate_normalized_source,validate_sales_signals
from app.core.workflow import source_evidence
from app.core.session_store import session_store
from app.schemas.intake import UnifiedIntakeRequest,GmailPlaceholderRequest
router=APIRouter()

def analyze(source):
    normalized=validate_normalized_source(IntakeAgent().run(source))
    signals=validate_sales_signals(ExtractorAgent().run(normalized))
    session=session_store.create(source,normalized,signals)
    session['source_evidence']=source_evidence(source,normalized)
    session_store.save(session)
    return session

@router.post('/unified')
def intake(payload:UnifiedIntakeRequest):
    return analyze(normalize_unified_intake(payload.model_dump()))

@router.post('/upload')
async def upload(file:UploadFile=File(...),title:str=Form(''),sender_company:str=Form(''),user_goal:str=Form('')):
    data=await file.read(MAX_BYTES+1)
    parsed=parse_uploaded(file.filename or '',data)
    ext=(file.filename or '').lower().rsplit('.',1)[-1]
    source={'source_type':'email' if ext=='eml' else 'document','title':title or parsed.get('title') or file.filename,
       'raw_text':parsed['raw_text'],'sender_company':sender_company,'sender_person':parsed.get('sender_person',''),
       'user_goal':user_goal,'intake_mode':'upload','filename':file.filename}
    return analyze(source)

@router.post('/gmail-placeholder')
def gmail(payload:GmailPlaceholderRequest):
    return gmail_placeholder(payload.model_dump())
