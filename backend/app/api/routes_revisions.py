from fastapi import APIRouter,HTTPException
from app.agents.revision_agent import RevisionAgent
from app.core.session_store import session_store
from app.core.validators import validate_revised_draft
from app.core.workflow import current_text,draft,invalidate
from app.schemas.revisions import ReviseDraftRequest
router=APIRouter()
@router.post('/revise')
def revise(payload:ReviseDraftRequest):
    try:s=session_store.get(payload.session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    if s.get('selected_draft_id')!=payload.draft_id:raise HTTPException(409,'Select this draft before revising')
    revised=validate_revised_draft(RevisionAgent().run(current_text(s),payload.instruction,s))
    s['revision_history'].append({'revision_id':revised['revision_id'],'draft_id':payload.draft_id,
          'instruction':payload.instruction,'result_text':revised['text']})
    # An editable final block becomes stale after a revision.
    s['final_pack']={}
    invalidate(s,'revised');session_store.save(s)
    return {'session_id':payload.session_id,'draft_id':payload.draft_id,'revised_draft':revised}
