from fastapi import APIRouter,HTTPException
from app.agents.draft_agent import DraftAgent
from app.core.session_store import session_store
from app.core.validators import validate_draft_set
from app.core.workflow import draft,invalidate
from app.schemas.drafts import GenerateDraftsRequest,SelectDraftRequest
router=APIRouter()
@router.post('/generate')
def generate(payload:GenerateDraftsRequest):
    try:s=session_store.get(payload.session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    output=validate_draft_set(DraftAgent().run(s['sales_signals'],payload.model_dump()))
    s['draft_outputs'].append(output)
    invalidate(s,'drafted')
    session_store.save(s)
    return {'session_id':s['session_id'],'draft_output':output}
@router.post('/{session_id}/select-draft')
def select(session_id:str,payload:SelectDraftRequest):
    try:s=session_store.get(session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    draft(s,payload.draft_id)
    s['selected_draft_id']=payload.draft_id
    invalidate(s,'selected')
    s['final_pack']={}
    session_store.save(s)
    return {'session_id':session_id,'selected_draft_id':payload.draft_id}
