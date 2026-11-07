from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, HTTPException,Query
from pydantic import BaseModel
from app.core.session_store import session_store
from app.core.workflow import CHECKS,require_reviewed,current_text,digest
router=APIRouter()
class ApprovalRequest(BaseModel):
    approval_state:Literal['approved']
    checklist:dict[str,bool]

@router.get('')
def list_all(company:str='',source_type:str='',status:str='',date:str=''):
    return {'sessions':session_store.list({'company':company,'source_type':source_type,'status':status,'date':date})}
@router.get('/{session_id}')
def get(session_id:str):
    try:return session_store.get(session_id)
    except KeyError:raise HTTPException(404,'Session not found')
@router.post('/{session_id}/approval')
def approve(session_id:str,payload:ApprovalRequest):
    try:s=session_store.get(session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    require_reviewed(s)
    if any(payload.checklist.get(c) is not True for c in CHECKS):
        raise HTTPException(409,'All four approval checks must be explicitly confirmed')
    s['approval_record']={'draft_id':s['selected_draft_id'],'text_hash':digest(current_text(s)),
        'checklist':{c:True for c in CHECKS},'approved_at':datetime.now(timezone.utc).isoformat()}
    s['approval_state']='approved';s['status']='approved';session_store.save(s)
    return {'session_id':session_id,'approval_state':'approved'}
