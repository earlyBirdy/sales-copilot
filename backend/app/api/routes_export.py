from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from app.core.session_store import session_store
from app.core.workflow import current_text,draft,require_approved,invalidate
from app.core.export_builder import build_crm_note,build_markdown_bundle
router=APIRouter()
class ExportRequest(BaseModel):
    session_id:str
    draft_ids:list[str]|None=None
class EditableBlockUpdate(BaseModel):
    label:str=Field(min_length=1,max_length=120)
    text:str=Field(min_length=1,max_length=20000)

def load(sid):
    try:return session_store.get(sid)
    except KeyError:raise HTTPException(404,'Session not found')

@router.post('/final-pack')
def build(payload:ExportRequest):
    s=load(payload.session_id)
    did=s.get('selected_draft_id')
    if not did:raise HTTPException(409,'Select a draft before preparing a final block')
    if payload.draft_ids is not None and payload.draft_ids != [did]:
        raise HTTPException(422,'Only the selected draft can be included in this approval-bound pack')
    original=s.get('final_pack',{}).get('final_editable_blocks',[])
    existing=next((b for b in original if b.get('draft_id')==did),None)
    group_audience='message'
    for group in s['draft_outputs']:
        if any(d['draft_id']==did for d in group['drafts']):group_audience=group['audience'];break
    final={'label':f'{group_audience}_{draft(s,did)["length"]}_{did}',
        'draft_id':did,'text':existing['text'] if existing else current_text(s)}
    s['final_pack']={'source_summary':s.get('normalized_source',{}).get('summary_bullets',[]),
        'final_editable_blocks':[final],'export_meta':{'crm_note':build_crm_note(s)}}
    # Preparing blocks is not exporting and never grants approval.
    session_store.save(s)
    return {'session_id':payload.session_id,'final_pack':s['final_pack']}

@router.post('/{session_id}/editable-block')
def update(session_id:str,payload:EditableBlockUpdate):
    s=load(session_id)
    blocks=s.get('final_pack',{}).get('final_editable_blocks',[])
    block=next((x for x in blocks if x['label']==payload.label),None)
    if block is None:raise HTTPException(404,'Editable block not found')
    if block['draft_id']!=s.get('selected_draft_id'):raise HTTPException(409,'Block does not match selected draft')
    if payload.text!=block['text']:
        block['text']=payload.text;invalidate(s,'revised')
    session_store.save(s)
    return {'session_id':session_id,'final_pack':s['final_pack']}

@router.post('/markdown')
def markdown(payload:ExportRequest):
    s=load(payload.session_id);require_approved(s)
    if not s.get('final_pack',{}).get('final_editable_blocks'):raise HTTPException(409,'Build final pack first')
    s['approval_state']='exported';s['status']='exported';session_store.save(s)
    return {'session_id':payload.session_id,'markdown':build_markdown_bundle(s)}

@router.post('/email-ready')
def email_ready(payload:ExportRequest):
    s=load(payload.session_id);require_approved(s)
    blocks=s.get('final_pack',{}).get('final_editable_blocks',[])
    if not blocks:raise HTTPException(409,'Build final pack first')
    s['approval_state']='exported';s['status']='exported';session_store.save(s)
    return {'session_id':payload.session_id,'email_ready_block':blocks[0]['text']}
