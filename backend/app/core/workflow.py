"""Single-source draft selection, evidence and approval invariants."""
import hashlib
from fastapi import HTTPException

CHECKS = ('source_verified', 'claims_verified', 'audience_checked', 'recipients_checked')

def draft(session, draft_id=None):
    wanted = draft_id or session.get('selected_draft_id')
    for group in session.get('draft_outputs', []):
        for d in group.get('drafts', []):
            if d.get('draft_id') == wanted:
                return d
    raise HTTPException(404, 'Draft does not exist in this session')

def current_text(session, draft_id=None):
    d = draft(session, draft_id)
    edited = session.get('final_pack', {}).get('final_editable_blocks', [])
    for b in edited:
        if b.get('draft_id') == d['draft_id']:
            return b['text']
    for rev in reversed(session.get('revision_history', [])):
        if rev.get('draft_id') == d['draft_id']:
            return rev['result_text']
    return d['text']

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def invalidate(session, phase='selected'):
    session['approval_state'] = phase
    session['guardrail_result'] = None
    session['approval_record'] = None
    session['status'] = 'revised' if phase == 'revised' else 'drafted'

def require_reviewed(session):
    did=session.get('selected_draft_id')
    if not did: raise HTTPException(409,'Select a draft first')
    review=session.get('guardrail_result') or {}
    if review.get('draft_id') != did or review.get('text_hash') != digest(current_text(session)):
        raise HTTPException(409,'Run guardrail on the current selected text')
    if review.get('risk_level') == 'high':
        raise HTTPException(409,'High-risk draft needs revision and a new guardrail review')
    return review

def require_approved(session):
    require_reviewed(session)
    rec=session.get('approval_record') or {}
    if rec.get('draft_id') != session.get('selected_draft_id') or rec.get('text_hash') != digest(current_text(session)):
        raise HTTPException(409,'The current text has not been approved')
    if not all(rec.get('checklist',{}).get(k) is True for k in CHECKS):
        raise HTTPException(409,'Approval checklist incomplete')
    return rec

def source_evidence(source, normalized):
    raw=source.get('raw_text','')
    findings=[]
    for claim in normalized.get('claims',[]):
        claim=str(claim).strip()
        start=raw.casefold().find(claim.casefold()) if claim else -1
        findings.append({'claim':claim,'source_quote':raw[start:start+len(claim)] if start>=0 else '',
                         'start':start if start>=0 else None,'end':start+len(claim) if start>=0 else None,
                         'verified_in_source':start>=0})
    return findings
