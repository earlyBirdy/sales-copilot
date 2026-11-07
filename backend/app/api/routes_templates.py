from fastapi import APIRouter,HTTPException
from app.core.preset_store import TEMPLATE_LIBRARY,preset_store
from app.core.session_store import session_store
from app.core.validators import validate_draft_set
from app.core.workflow import invalidate
from app.schemas.templates import GenerateTemplateRequest,SavedPresetRequest
from app.agents.draft_agent import DraftAgent
router=APIRouter()
@router.get('/library')
def library():return {'templates':TEMPLATE_LIBRARY}
@router.get('/presets')
def presets():return {'presets':preset_store.list()}
@router.post('/presets')
def save(payload:SavedPresetRequest):return {'preset':preset_store.save(payload.model_dump())}
@router.post('/generate-template')
def generate(payload:GenerateTemplateRequest):
    try:s=session_store.get(payload.session_id)
    except KeyError:raise HTTPException(404,'Session not found')
    t=next((x for x in TEMPLATE_LIBRARY if x['key']==payload.template_key),None)
    if not t:raise HTTPException(422,'Unknown template')
    signal={**s['sales_signals']}
    if payload.selected_cta:
        if payload.selected_cta not in signal.get('cta_options',[]):raise HTTPException(422,'Unknown CTA')
        signal['cta_options']=[payload.selected_cta]
    output=validate_draft_set(DraftAgent().run(signal,{'audience':t['audience'],'tone':t['tone'],
       'lengths':t['lengths'],'prompt_preset':t['prompt_preset'],'selected_cta':payload.selected_cta}))
    output['template_key']=t['key'];output['template_version']='v1.0.0'
    s['draft_outputs'].append(output);invalidate(s,'drafted');session_store.save(s)
    return {'session_id':payload.session_id,'draft_output':output}
