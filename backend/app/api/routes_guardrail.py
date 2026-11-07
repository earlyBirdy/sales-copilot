from fastapi import APIRouter,HTTPException
from app.agents.guardrail_agent import GuardrailAgent
from app.core.session_store import session_store
from app.core.validators import validate_guardrail
from app.core.workflow import current_text,digest
from app.schemas.guardrail import GuardrailRequest
router=APIRouter()
@router.post('/guardrail')
def guardrail(payload:GuardrailRequest):
    try:s=session_store.get(payload.session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    if s.get('selected_draft_id')!=payload.draft_id:raise HTTPException(409,'Select the draft before review')
    text=current_text(s)
    review=validate_guardrail(GuardrailAgent().run(text,s))
    patterns=['guarantee','fully secure','certified','best','always']
    ann=[]; lower=text.casefold()
    for term in patterns:
        pos=lower.find(term)
        if pos>=0:ann.append({'term':term,'start':pos,'end':pos+len(term),'note':'Review this assertion against source evidence'})
    # Unverified source quotes are not certified source matches. Flag for manual checking.
    unverified=[x for x in s.get('source_evidence',[]) if not x['verified_in_source']]
    if unverified:review['review_notes'].append(f'{len(unverified)} extracted claims lack an exact source quote; manually verify')
    if ann and review['risk_level']=='low':review['risk_level']='medium'
    s['guardrail_result']={'draft_id':payload.draft_id,'text_hash':digest(text),'risk_level':review['risk_level'],
        'review_notes':review['review_notes'],'annotations':ann}
    s['guardrail_annotations']=ann;s['review_notes']=review['review_notes']
    s['approval_state']='guardrail_checked';s['status']='reviewed';s['approval_record']=None
    session_store.save(s)
    return {'session_id':payload.session_id,'draft_id':payload.draft_id,**s['guardrail_result']}
